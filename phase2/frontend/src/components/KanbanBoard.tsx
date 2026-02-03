'use client';

import React, { useState, useEffect, useRef } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import TaskCard from './TaskCard'; // Import TaskCard component
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

  // Define color scheme for each column
  const getColumnStyles = (status: ColumnType, isOver: boolean) => {
    const baseClasses = "flex-1 min-w-[300px] max-w-md rounded-xl transition-all duration-200";

    switch(status) {
      case 'To Do':
        return `${baseClasses} ${
          isOver
            ? 'bg-blue-50 border-2 border-blue-400 shadow-lg'
            : 'bg-gradient-to-b from-blue-50 to-blue-100 border border-blue-200 shadow-sm hover:shadow-md'
        }`;
      case 'In Progress':
        return `${baseClasses} ${
          isOver
            ? 'bg-orange-50 border-2 border-orange-400 shadow-lg'
            : 'bg-gradient-to-b from-orange-50 to-orange-100 border border-orange-200 shadow-sm hover:shadow-md'
        }`;
      case 'Done':
        return `${baseClasses} ${
          isOver
            ? 'bg-green-50 border-2 border-green-400 shadow-lg'
            : 'bg-gradient-to-b from-green-50 to-green-100 border border-green-200 shadow-sm hover:shadow-md'
        }`;
      default:
        return `${baseClasses} ${
          isOver
            ? 'bg-gray-50 border-2 border-gray-400 shadow-lg'
            : 'bg-gradient-to-b from-gray-50 to-gray-100 border border-gray-200 shadow-sm hover:shadow-md'
        }`;
    }
  };

  return (
    <div
      ref={drop}
      className={getColumnStyles(status, isOver)}
    >
      <div className="p-4">
        {/* Column Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${
              status === 'To Do' ? 'bg-blue-500' :
              status === 'In Progress' ? 'bg-orange-500' :
              'bg-green-500'
            }`}></div>
            <h2 className="font-bold text-gray-800 text-lg">{status}</h2>
            <span className={`text-xs px-2 py-1 rounded-full ${
              status === 'To Do' ? 'bg-blue-200 text-blue-800' :
              status === 'In Progress' ? 'bg-orange-200 text-orange-800' :
              'bg-green-200 text-green-800'
            }`}>
              {filteredTasks.length}
            </span>
          </div>
        </div>

        {/* Task Count Bar */}
        <div className="mb-4">
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div
              className={`h-1.5 rounded-full ${
                status === 'To Do' ? 'bg-blue-500' :
                status === 'In Progress' ? 'bg-orange-500' :
                'bg-green-500'
              }`}
              style={{ width: `${Math.min(100, (filteredTasks.length / Math.max(tasks.length, 1)) * 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Tasks Container */}
        <div className="space-y-3 max-h-[calc(100vh-250px)] overflow-y-auto pr-2">
          {filteredTasks.length > 0 ? (
            filteredTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onTaskEdit={onTaskEdit}
                onTaskDelete={onTaskDelete}
                animateTask={animateTask}
              />
            ))
          ) : (
            <div className="text-center py-8 text-gray-500">
              <div className="mx-auto w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-sm">No tasks</p>
            </div>
          )}
        </div>
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
      className={`cursor-move transform transition-all duration-200 ${
        isDragging ? 'opacity-60 scale-95 shadow-lg z-10' :
        animateTask === task.id ? 'animate-pulse bg-blue-50 rounded-lg p-1' : 'opacity-100 shadow-sm hover:shadow-md'
      }`}
    >
      <TaskCard
        task={task}
        onEdit={onTaskEdit}
        onDelete={() => onTaskDelete(task.id)}
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
      <div className="flex space-x-6 overflow-x-auto pb-4 -mx-2 px-2">
        <Column
          status="To Do"
          tasks={boardTasks}
          onTaskDrop={handleTaskDrop}
          onTaskEdit={onTaskUpdate}
          onTaskDelete={onTaskDelete}
          animateTask={animateTask}
        />
        <Column
          status="In Progress"
          tasks={boardTasks}
          onTaskDrop={handleTaskDrop}
          onTaskEdit={onTaskUpdate}
          onTaskDelete={onTaskDelete}
          animateTask={animateTask}
        />
        <Column
          status="Done"
          tasks={boardTasks}
          onTaskDrop={handleTaskDrop}
          onTaskEdit={onTaskUpdate}
          onTaskDelete={onTaskDelete}
          animateTask={animateTask}
        />
      </div>
    </DndProvider>
  );
};

export default KanbanBoard;