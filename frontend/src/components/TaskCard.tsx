'use client';

import React from 'react';
import { Task } from '@/types/index'; // Assuming Task type is defined in types
import { format } from 'date-fns';

interface TaskCardProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onEdit, onDelete }) => {
  // Determine if the task is overdue
  const isOverdue = task.due && new Date(task.due) < new Date() && !task.completed;

  // Priority badge styling based on priority level
  const getPriorityClass = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className={`border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow bg-white ${
      isOverdue && !task.completed ? 'ring-2 ring-red-500' : ''
    }`}>
      <div className="flex justify-between items-start">
        <h3 className="font-semibold text-gray-900">{task.title}</h3>
        <div className="flex space-x-2">
          {onEdit && (
            <button
              onClick={() => onEdit(task)}
              className="text-blue-600 hover:text-blue-800"
              aria-label="Edit task"
            >
              ✏️
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(task.id)}
              className="text-red-600 hover:text-red-800"
              aria-label="Delete task"
            >
              🗑️
            </button>
          )}
        </div>
      </div>

      {task.description && (
        <p className="mt-2 text-sm text-gray-600">{task.description}</p>
      )}

      <div className="mt-3 flex flex-wrap gap-2">
        {/* Priority badge */}
        <span className={`text-xs px-2 py-1 rounded-full border ${getPriorityClass(task.priority)}`}>
          {task.priority}
        </span>

        {/* Tags as chips */}
        {task.tags && (
          <div className="flex flex-wrap gap-1">
            {typeof task.tags === 'string' ? (
              // If tags is a JSON string, parse it and map over the array
              (() => {
                try {
                  const tagsArray = JSON.parse(task.tags);
                  return Array.isArray(tagsArray) && tagsArray.length > 0 ? (
                    tagsArray.map((tag: string, index: number) => (
                      <span
                        key={index}
                        className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full"
                      >
                        {tag}
                      </span>
                    ))
                  ) : null;
                } catch (e) {
                  // If parsing fails, treat as a single tag or empty
                  return task.tags ? (
                    <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                      {task.tags}
                    </span>
                  ) : null;
                }
              })()
            ) : Array.isArray(task.tags) ? (
              // If tags is already an array, map over it directly
              task.tags.map((tag: string, index: number) => (
                <span
                  key={index}
                  className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full"
                >
                  {tag}
                </span>
              ))
            ) : task.tags ? (
              // If tags is a single value (string), display it
              <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                {task.tags}
              </span>
            ) : null}
          </div>
        )}
      </div>

      {/* Due date */}
      {task.due && (
        <div className={`mt-3 text-xs ${
          isOverdue && !task.completed ? 'text-red-600 font-medium' : 'text-gray-500'
        }`}>
          Due: {format(new Date(task.due), 'MMM dd, yyyy')}
        </div>
      )}

      {/* Completion status */}
      <div className="mt-3">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => {}} // This would be handled by a parent component
          className="mr-2"
        />
        <span className="text-sm text-gray-600">
          {task.completed ? 'Completed' : 'Pending'}
        </span>
      </div>
    </div>
  );
};

export default TaskCard;