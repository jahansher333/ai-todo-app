'use client';

import React, { useState, useEffect } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import TaskCard from './TaskCard';
import { Task } from '@/types/index'; // Assuming Task type is defined in types

// Column types
type ColumnType = 'To Do' | 'In Progress' | 'Done';

interface ColumnProps {
  status: ColumnType;
  tasks: Task[];
  onTaskDrop: (taskId: string, newStatus: string) => void;
  onTaskEdit: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
  animateTask?: string | null;
}

const Column: React.FC<ColumnProps> = ({ status, tasks, onTaskDrop, onTaskEdit, onTaskDelete, animateTask }) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: 'TASK',
    drop: (item: { id: string }) => onTaskDrop(item.id, status),
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }));

  // Filter tasks based on column status
  const filteredTasks = tasks.filter(task => {
    if (status === 'Done') return task.completed;
    if (status === 'To Do') return !task.completed;
    if (status === 'In Progress') return !task.completed && task.status === 'In Progress';
    return false;
  });

  return (
    <div
      ref={drop}
      className={`flex-1 min-w-[300px] p-4 rounded-lg border ${
        isOver ? 'bg-blue-50 border-blue-300' : 'bg-gray-50 border-gray-200'
      }`}
    >
      <h2 className="font-bold text-lg mb-4 text-center">{status} ({filteredTasks.length})</h2>
      <div className="space-y-3">
        {filteredTasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onTaskEdit={onTaskEdit}
            onTaskDelete={onTaskDelete}
            animateTask={animateTask}
          />
        ))}
      </div>
    </div>
  );
};

interface TaskItemProps {
  task: Task;
  onTaskEdit: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
  animateTask?: string | null;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskEdit, onTaskDelete, animateTask }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'TASK',
    item: { id: task.id },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));

  return (
    <div
      ref={drag}
      className={`cursor-move transform transition-all duration-300 ${
        isDragging ? 'opacity-50 scale-95' :
        animateTask === task.id ? 'animate-pulse bg-blue-50 rounded-lg p-1' : 'opacity-100'
      }`}
    >
      <TaskCard
        task={task}
        onEdit={onTaskEdit}
        onDelete={onTaskDelete}
      />
    </div>
  );
};

interface KanbanBoardProps {
  tasks: Task[];
  onTaskUpdate: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
  animateTask?: string | null;
}

const KanbanBoard: React.FC<KanbanBoardProps> = ({ tasks, onTaskUpdate, onTaskDelete, animateTask }) => {
  const [boardTasks, setBoardTasks] = useState<Task[]>(tasks);

  // Update tasks when props change
  useEffect(() => {
    setBoardTasks(tasks);
  }, [tasks]);

  const handleTaskDrop = (taskId: string, newStatus: string) => {
    // In a real app, this would update the task status in the backend
    // For now, we'll just update the local state
    const updatedTasks = boardTasks.map(task => {
      if (task.id === taskId) {
        // Update the status based on the column
        if (newStatus === 'Done') {
          return { ...task, completed: true };
        } else if (newStatus === 'To Do' || newStatus === 'In Progress') {
          return { ...task, completed: false, status: newStatus };
        }
      }
      return task;
    });

    setBoardTasks(updatedTasks);

    // Find the updated task and call onTaskUpdate
    const updatedTask = updatedTasks.find(task => task.id === taskId);
    if (updatedTask) {
      onTaskUpdate(updatedTask);
    }
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="flex space-x-4 overflow-x-auto pb-4">
        <Column
          status="To Do"
          tasks={boardTasks}
          onTaskDrop={handleTaskDrop}
          onTaskEdit={(task) => onTaskUpdate(task)}
          onTaskDelete={onTaskDelete}
          animateTask={animateTask}
        />
        <Column
          status="In Progress"
          tasks={boardTasks}
          onTaskDrop={handleTaskDrop}
          onTaskEdit={(task) => onTaskUpdate(task)}
          onTaskDelete={onTaskDelete}
          animateTask={animateTask}
        />
        <Column
          status="Done"
          tasks={boardTasks}
          onTaskDrop={handleTaskDrop}
          onTaskEdit={(task) => onTaskUpdate(task)}
          onTaskDelete={onTaskDelete}
          animateTask={animateTask}
        />
      </div>
    </DndProvider>
  );
};

export default KanbanBoard;