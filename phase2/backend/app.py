from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
import asyncio
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
import json
import logging
import os
import uuid

try:
    import dapr.aio.clients as dapr_clients
    from dapr.conf import Settings
    from dapr.clients.grpc._state import StateItem
    from dapr.clients.grpc._crypto import CryptoError
except ImportError:
    print("Dapr not available in current environment - using mock implementation")

    class MockDaprClient:
        def __init__(self):
            pass

        async def publish_event(self, pubsub_name: str, topic_name: str, data: dict, **kwargs):
            print(f"[MOCK] Publishing event to {pubsub_name}/{topic_name}: {data}")

        async def save_state(self, store_name: str, key: str, value: str, **kwargs):
            print(f"[MOCK] Saving state {key} to {store_name}: {value}")

        async def get_state(self, store_name: str, key: str, **kwargs):
            print(f"[MOCK] Getting state {key} from {store_name}")
            return type('MockState', (), {'data': b'', 'etag': '1'})()

        async def invoke_binding(self, binding_name: str, operation: str, data: bytes = b'', metadata: dict = None):
            print(f"[MOCK] Invoking binding {binding_name} with operation {operation}")
            return type('MockBindingResponse', (), {'data': b'', 'metadata': {}})()

    dapr_clients = type('MockModule', (), {'DaprClient': MockDaprClient})()

# Import models
from pydantic import BaseModel
from enum import Enum

class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatusEnum = TaskStatusEnum.pending
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None
    tags: List[str] = []
    is_recurring: bool = False
    recurring_rule_id: Optional[str] = None  # Reference to recurring rule
    reminder_ids: List[str] = []  # List of associated reminder IDs
    parent_task_id: Optional[str] = None  # For recurring tasks - reference to original task
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None
    tags: List[str] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    status: Optional[TaskStatusEnum] = None

class Reminder(BaseModel):
    id: str
    task_id: str
    trigger_at: datetime
    channel: str = "in_app"
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RecurringRule(BaseModel):
    id: str
    pattern_type: str  # daily, weekly, monthly, custom
    cron_expression: Optional[str] = None
    interval_days: Optional[int] = None
    max_occurrences: Optional[int] = None
    end_date: Optional[datetime] = None

# Initialize Dapr client
dapr_client = dapr_clients.DaprClient()

app = FastAPI(title="Todo Backend with Dapr", version="5.0.0")

@app.on_event("startup")
async def startup_event():
    """Initialize Dapr client on startup"""
    global dapr_client
    try:
        dapr_client = dapr_clients.DaprClient()
        print("Connected to Dapr sidecar")
    except Exception as e:
        print(f"Could not connect to Dapr sidecar: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close Dapr client on shutdown"""
    if hasattr(dapr_client, '__del__'):
        dapr_client.__del__()

@app.get("/")
async def root():
    return {"message": "Todo Backend with Dapr Integration"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "5.0.0"}

@app.get("/health/ready")
async def ready_check():
    # Add any additional readiness checks here
    return {"status": "ready"}

@app.post("/tasks/", response_model=Task)
async def create_task(task_create: TaskCreate):
    try:
        # Generate a unique ID for the task
        task_id = f"task_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(task_create.title) % 10000:04d}"

        # Create task object
        task = Task(
            id=task_id,
            title=task_create.title,
            description=task_create.description,
            priority=task_create.priority,
            due_date=task_create.due_date,
            tags=task_create.tags,
            is_recurring=False,  # Default to non-recurring
            recurring_rule_id=None,
            reminder_ids=[],
            parent_task_id=None
        )

        # Save task to Dapr state store
        await dapr_client.save_state(
            store_name="task-state",
            key=f"task:{task.id}",
            value=task.model_dump_json(),
            options={
                "consistency": "strong"
            }
        )

        # Publish task created event to Dapr pub/sub
        await dapr_client.publish_event(
            pubsub_name="task-pubsub",
            topic_name="task-events",
            data={
                "type": "created",
                "task_id": task.id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": task.model_dump()
            }
        )

        print(f"Task {task.id} created and event published")
        return task

    except Exception as e:
        print(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    try:
        # Retrieve task from Dapr state store
        state_response = await dapr_client.get_state(
            store_name="task-state",
            key=f"task:{task_id}"
        )

        if not state_response.data:
            raise HTTPException(status_code=404, detail="Task not found")

        task_data = json.loads(state_response.data.decode())
        return Task(**task_data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting task: {str(e)}")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    try:
        # Retrieve current task
        state_response = await dapr_client.get_state(
            store_name="task-state",
            key=f"task:{task_id}"
        )

        if not state_response.data:
            raise HTTPException(status_code=404, detail="Task not found")

        current_task_data = json.loads(state_response.data.decode())
        current_task = Task(**current_task_data)

        # Update task with provided values
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(current_task, field, value)

        # Update timestamp
        current_task.updated_at = datetime.utcnow()

        # Save updated task to Dapr state store
        await dapr_client.save_state(
            store_name="task-state",
            key=f"task:{task_id}",
            value=current_task.model_dump_json(),
            etag=state_response.etag,
            options={
                "concurrency": "first-write",
                "consistency": "strong"
            }
        )

        # Publish task updated event
        await dapr_client.publish_event(
            pubsub_name="task-pubsub",
            topic_name="task-events",
            data={
                "type": "updated",
                "task_id": task_id,
                "timestamp": datetime.utcnow().isoformat(),
                "changes": task_update.model_dump(exclude_unset=True),
                "data": current_task.model_dump()
            }
        )

        return current_task

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        # Publish task deleted event first
        await dapr_client.publish_event(
            pubsub_name="task-pubsub",
            topic_name="task-events",
            data={
                "type": "deleted",
                "task_id": task_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        # Delete task from Dapr state store
        await dapr_client.delete_state(
            store_name="task-state",
            key=f"task:{task_id}"
        )

        return {"message": f"Task {task_id} deleted successfully"}

    except Exception as e:
        print(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")

@app.post("/tasks/{task_id}/recurring", response_model=Task)
async def create_recurring_task(task_id: str, recurring_rule: RecurringRule):
    try:
        # Retrieve current task
        state_response = await dapr_client.get_state(
            store_name="task-state",
            key=f"task:{task_id}"
        )

        if not state_response.data:
            raise HTTPException(status_code=404, detail="Task not found")

        current_task_data = json.loads(state_response.data.decode())
        current_task = Task(**current_task_data)

        # Update task to be recurring
        current_task.is_recurring = True
        current_task.recurring_rule_id = recurring_rule.id

        # Save updated task to Dapr state store
        await dapr_client.save_state(
            store_name="task-state",
            key=f"task:{task_id}",
            value=current_task.model_dump_json(),
            etag=state_response.etag,
            options={
                "concurrency": "first-write",
                "consistency": "strong"
            }
        )

        # Save recurring rule to Dapr state store
        await dapr_client.save_state(
            store_name="task-state",
            key=f"rule:{recurring_rule.id}",
            value=recurring_rule.model_dump_json(),
            options={
                "consistency": "strong"
            }
        )

        # Publish recurring task created event
        await dapr_client.publish_event(
            pubsub_name="task-pubsub",
            topic_name="task-events",
            data={
                "type": "recurring_created",
                "task_id": task_id,
                "rule_id": recurring_rule.id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "task": current_task.model_dump(),
                    "rule": recurring_rule.model_dump()
                }
            }
        )

        # Schedule the recurring task using Dapr bindings if needed
        # This could trigger a cron job or similar mechanism
        await dapr_client.invoke_binding(
            binding_name="recurring-scheduler",
            operation="create",
            data=json.dumps({
                "task_id": task_id,
                "rule_id": recurring_rule.id,
                "cron_expression": recurring_rule.cron_expression
            }).encode('utf-8')
        )

        return current_task

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating recurring task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating recurring task: {str(e)}")

@app.post("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: str):
    try:
        # Retrieve current task
        state_response = await dapr_client.get_state(
            store_name="task-state",
            key=f"task:{task_id}"
        )

        if not state_response.data:
            raise HTTPException(status_code=404, detail="Task not found")

        current_task_data = json.loads(state_response.data.decode())
        current_task = Task(**current_task_data)

        # Update task status and completion time
        current_task.status = TaskStatusEnum.completed
        current_task.completed_at = datetime.utcnow()
        current_task.updated_at = datetime.utcnow()

        # Handle recurring tasks - generate next occurrence if needed
        if current_task.is_recurring:
            await _handle_recurring_task_completion(current_task)

        # Save updated task to Dapr state store
        await dapr_client.save_state(
            store_name="task-state",
            key=f"task:{task_id}",
            value=current_task.model_dump_json(),
            etag=state_response.etag,
            options={
                "concurrency": "first-write",
                "consistency": "strong"
            }
        )

        # Publish task completed event
        await dapr_client.publish_event(
            pubsub_name="task-pubsub",
            topic_name="task-events",
            data={
                "type": "completed",
                "task_id": task_id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": current_task.model_dump()
            }
        )

        return current_task

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error completing task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error completing task: {str(e)}")

async def _handle_recurring_task_completion(completed_task: Task):
    """
    Handle the completion of a recurring task by creating the next occurrence
    """
    try:
        # Get recurring rule for this task
        rule_response = await dapr_client.get_state(
            store_name="task-state",
            key=f"rule:{completed_task.id}"
        )

        if not rule_response.data:
            print(f"No recurring rule found for task {completed_task.id}")
            return

        rule_data = json.loads(rule_response.data.decode())
        rule = RecurringRule(**rule_data)

        # Determine if we should create a new occurrence
        should_create_next = True

        # Check max occurrences
        if rule.max_occurrences:
            # Count occurrences - this is simplified logic
            # In a real implementation, you'd track completed instances
            pass

        # Check end date
        if rule.end_date and datetime.utcnow() > rule.end_date:
            should_create_next = False

        if should_create_next:
            # Create new task instance based on the original
            new_task_id = f"task_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(completed_task.title) % 10000:04d}_recur"

            # Calculate next due date based on pattern (simplified logic)
            next_due_date = completed_task.due_date
            if completed_task.due_date:
                if rule.interval_days:
                    next_due_date = completed_task.due_date + timedelta(days=rule.interval_days)
                elif rule.pattern_type == "daily":
                    next_due_date = completed_task.due_date + timedelta(days=1)
                elif rule.pattern_type == "weekly":
                    next_due_date = completed_task.due_date + timedelta(weeks=1)
                elif rule.pattern_type == "monthly":
                    next_due_date = completed_task.due_date + timedelta(days=30)

            new_task = Task(
                id=new_task_id,
                title=completed_task.title,
                description=completed_task.description,
                priority=completed_task.priority,
                due_date=next_due_date,
                tags=completed_task.tags,
                is_recurring=True
            )

            # Save new recurring task
            await dapr_client.save_state(
                store_name="task-state",
                key=f"task:{new_task.id}",
                value=new_task.model_dump_json(),
                options={
                    "consistency": "strong"
                }
            )

            # Publish event for new recurring task
            await dapr_client.publish_event(
                pubsub_name="task-pubsub",
                topic_name="task-events",
                data={
                    "type": "created",
                    "task_id": new_task.id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": new_task.model_dump(),
                    "source": "recurring_generation"
                }
            )

            print(f"Created new recurring task {new_task.id} from {completed_task.id}")

    except Exception as e:
        print(f"Error handling recurring task completion: {str(e)}")

@app.post("/tasks/{task_id}/reminders")
async def add_reminder(task_id: str, reminder: Reminder):
    try:
        # Verify task exists
        state_response = await dapr_client.get_state(
            store_name="task-state",
            key=f"task:{task_id}"
        )

        if not state_response.data:
            raise HTTPException(status_code=404, detail="Task not found")

        # Save reminder to Dapr state store
        await dapr_client.save_state(
            store_name="task-state",
            key=f"reminder:{reminder.id}",
            value=reminder.model_dump_json(),
            options={
                "consistency": "strong"
            }
        )

        # Update task to include reminder ID
        current_task_data = json.loads(state_response.data.decode())
        current_task = Task(**current_task_data)
        
        if reminder.id not in current_task.reminder_ids:
            current_task.reminder_ids.append(reminder.id)
            
            await dapr_client.save_state(
                store_name="task-state",
                key=f"task:{task_id}",
                value=current_task.model_dump_json(),
                etag=state_response.etag,
                options={
                    "concurrency": "first-write",
                    "consistency": "strong"
                }
            )

        # Publish reminder scheduled event
        await dapr_client.publish_event(
            pubsub_name="task-pubsub",
            topic_name="reminders",
            data={
                "type": "scheduled",
                "reminder_id": reminder.id,
                "task_id": task_id,
                "trigger_at": reminder.trigger_at.isoformat(),
                "channel": reminder.channel,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        # Also publish to task-events topic for comprehensive tracking
        await dapr_client.publish_event(
            pubsub_name="task-pubsub",
            topic_name="task-events",
            data={
                "type": "reminder_added",
                "task_id": task_id,
                "reminder_id": reminder.id,
                "timestamp": datetime.utcnow().isoformat(),
                "data": reminder.model_dump()
            }
        )

        return {"message": f"Reminder {reminder.id} scheduled for task {task_id}"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error scheduling reminder: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error scheduling reminder: {str(e)}")

@app.get("/dapr/subscribe")
async def dapr_subscribe():
    """
    Dapr subscription endpoint for pub/sub
    """
    subscriptions = [
        {
            "pubsubname": "task-pubsub",
            "topic": "task-events",
            "route": "/events/task-events"
        },
        {
            "pubsubname": "task-pubsub",
            "topic": "reminders",
            "route": "/events/reminders"
        }
    ]
    return subscriptions

@app.post("/events/task-events")
async def handle_task_events(data: dict):
    """
    Handle incoming task events from Dapr pub/sub
    """
    try:
        event_type = data.get("type", "unknown")
        task_id = data.get("task_id", "unknown")
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        print(f"Processing task event: {event_type} for task {task_id} at {timestamp}")

        # Process different event types
        if event_type == "created":
            print(f"Task {task_id} was created")
        elif event_type == "updated":
            print(f"Task {task_id} was updated")
        elif event_type == "completed":
            print(f"Task {task_id} was completed")
        elif event_type == "deleted":
            print(f"Task {task_id} was deleted")
        else:
            print(f"Unknown event type: {event_type}")

        # Could forward to external systems or trigger additional actions here
        return {"status": "processed"}

    except Exception as e:
        print(f"Error handling task event: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/events/reminders")
async def handle_reminder_events(data: dict):
    """
    Handle incoming reminder events from Dapr pub/sub
    """
    try:
        reminder_id = data.get("reminder_id", "unknown")
        task_id = data.get("task_id", "unknown")
        trigger_at = data.get("trigger_at", datetime.utcnow().isoformat())
        channel = data.get("channel", "in_app")

        print(f"Processing reminder event: {reminder_id} for task {task_id} via {channel} at {trigger_at}")

        # In a real implementation, this would send the actual notification
        # depending on the channel (in_app, webhook, email)

        if channel == "in_app":
            print(f"Sending in-app notification for reminder {reminder_id}")
        elif channel == "webhook":
            print(f"Sending webhook notification for reminder {reminder_id}")
        elif channel == "email":
            print(f"Sending email notification for reminder {reminder_id}")

        return {"status": "processed"}

    except Exception as e:
        print(f"Error handling reminder event: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/dapr/bindings/recurring-scheduler")
async def handle_recurring_scheduler(input_data: dict):
    """
    Handle recurring task scheduler events from Dapr bindings
    This endpoint is called by Dapr when a recurring task should be processed
    """
    try:
        task_id = input_data.get("task_id")
        rule_id = input_data.get("rule_id")
        operation = input_data.get("operation", "process")

        print(f"Processing recurring task scheduler event: {operation} for task {task_id}, rule {rule_id}")

        if operation == "process":
            # Retrieve the original task
            original_task_response = await dapr_client.get_state(
                store_name="task-state",
                key=f"task:{task_id}"
            )

            if not original_task_response.data:
                print(f"Original task {task_id} not found")
                return {"status": "error", "message": "Original task not found"}

            original_task_data = json.loads(original_task_response.data.decode())
            original_task = Task(**original_task_data)

            # Retrieve the recurring rule
            rule_response = await dapr_client.get_state(
                store_name="task-state",
                key=f"rule:{rule_id}"
            )

            if not rule_response.data:
                print(f"Recurring rule {rule_id} not found")
                return {"status": "error", "message": "Recurring rule not found"}

            rule_data = json.loads(rule_response.data.decode())
            rule = RecurringRule(**rule_data)

            # Create a new instance of the recurring task
            new_task_id = f"task_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_recur"

            # Calculate next due date based on the rule
            next_due_date = original_task.due_date
            if original_task.due_date:
                if rule.interval_days:
                    next_due_date = original_task.due_date + timedelta(days=rule.interval_days)
                elif rule.pattern_type == "daily":
                    next_due_date = original_task.due_date + timedelta(days=1)
                elif rule.pattern_type == "weekly":
                    next_due_date = original_task.due_date + timedelta(weeks=1)
                elif rule.pattern_type == "monthly":
                    next_due_date = original_task.due_date + timedelta(days=30)

            new_task = Task(
                id=new_task_id,
                title=original_task.title,
                description=original_task.description,
                priority=original_task.priority,
                due_date=next_due_date,
                tags=original_task.tags,
                is_recurring=True,
                recurring_rule_id=rule_id,
                parent_task_id=task_id,  # Reference back to the original task
                reminder_ids=[]  # New instance will have its own reminders
            )

            # Save new recurring task instance
            await dapr_client.save_state(
                store_name="task-state",
                key=f"task:{new_task.id}",
                value=new_task.model_dump_json(),
                options={
                    "consistency": "strong"
                }
            )

            # Publish event for new recurring task
            await dapr_client.publish_event(
                pubsub_name="task-pubsub",
                topic_name="task-events",
                data={
                    "type": "recurring_instance_created",
                    "task_id": new_task.id,
                    "parent_task_id": task_id,
                    "rule_id": rule_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": new_task.model_dump()
                }
            )

            print(f"Created new recurring task instance {new_task.id} from {task_id}")

        return {"status": "processed"}

    except Exception as e:
        print(f"Error handling recurring scheduler event: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)