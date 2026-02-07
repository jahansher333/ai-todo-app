'use client';

import React, { useState, useEffect } from 'react';
import { Task } from '@/types/index'; // Assuming Task type is defined in types

interface TaskFormProps {
  task?: Task;
  onSubmit: (task: Task) => void;
  onCancel: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState<Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>>({
    title: '',
    description: '',
    completed: false,
    priority: 'medium',
    tags: [], // Store as array internally for form manipulation
    due: null,
    recurring: 'none',
  });

  const [tagInput, setTagInput] = useState('');
  const [showDatePicker, setShowDatePicker] = useState(false);

  // Populate form if editing existing task
  useEffect(() => {
    if (task) {
      // Handle tags field - convert string to array if it's a JSON string
      let processedTags: string[] = [];
      if (task.tags) {
        if (typeof task.tags === 'string') {
          try {
            // Try to parse as JSON array
            const parsedTags = JSON.parse(task.tags);
            if (Array.isArray(parsedTags)) {
              processedTags = parsedTags;
            } else {
              processedTags = [String(parsedTags)]; // If not an array, convert to single-item array
            }
          } catch (e) {
            // If parsing fails, treat as a single tag
            processedTags = [task.tags];
          }
        } else if (Array.isArray(task.tags)) {
          processedTags = task.tags;
        } else {
          processedTags = [String(task.tags)];
        }
      }

      setFormData({
        title: task.title || '',
        description: task.description || '',
        completed: task.completed || false,
        priority: task.priority || 'medium',
        tags: processedTags, // Store as array for form manipulation
        due: task.due || null,
        recurring: task.recurring || 'none',
      });
    }
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;

    if (name === 'completed') {
      setFormData(prev => ({
        ...prev,
        [name]: (e.target as HTMLInputElement).checked
      }));
    } else if (name === 'priority' || name === 'recurring') {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleAddTag = () => {
    if (tagInput.trim() && Array.isArray(formData.tags) && !formData.tags.includes(tagInput.trim())) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, tagInput.trim()]
      }));
      setTagInput('');
    }
  };

  const handleRemoveTag = (index: number) => {
    setFormData(prev => ({
      ...prev,
      tags: Array.isArray(prev.tags) ? prev.tags.filter((_, i) => i !== index) : []
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Create task object with proper structure
    // Convert tags array back to JSON string for backend
    const tagsJson = JSON.stringify(Array.isArray(formData.tags) ? formData.tags : []);

    const taskData = {
      ...formData,
      tags: tagsJson, // Convert array back to JSON string for backend
      id: task?.id || undefined, // Don't include id if creating new task
      user_id: task?.user_id || undefined, // Don't include user_id in form submission
      created_at: task?.created_at || undefined, // Don't include timestamp if creating new task
      updated_at: task?.updated_at || undefined, // Don't include timestamp if creating new task
    };

    // Cast to any first to bypass TypeScript error, then to Task
    onSubmit(taskData as any as Task);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md w-full max-w-2xl">
      <h2 className="text-xl font-bold mb-4">{task ? 'Edit Task' : 'Add New Task'}</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="due" className="block text-sm font-medium text-gray-700 mb-1">
            Due Date
          </label>
          <div className="relative">
            <input
              type="text"
              id="due"
              name="due"
              value={formData.due ? new Date(formData.due).toLocaleDateString() : ''}
              readOnly
              onClick={() => setShowDatePicker(!showDatePicker)}
              placeholder="Click to select date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
            />
            {showDatePicker && (
              <input
                type="date"
                value={formData.due ? new Date(formData.due).toISOString().split('T')[0] : ''}
                onChange={(e) => setFormData(prev => ({ ...prev, due: e.target.value ? new Date(e.target.value).toISOString() : null }))}
                className="absolute mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 z-10 bg-white"
              />
            )}
          </div>
        </div>

        <div>
          <label htmlFor="recurring" className="block text-sm font-medium text-gray-700 mb-1">
            Recurring
          </label>
          <select
            id="recurring"
            name="recurring"
            value={formData.recurring}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="none">None</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Tags
        </label>
        <div className="flex mb-2">
          <input
            type="text"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
            placeholder="Add a tag and press Enter"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="button"
            onClick={handleAddTag}
            className="px-4 py-2 bg-blue-500 text-white rounded-r-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Add
          </button>
        </div>

        {/* Display current tags */}
        {formData.tags && Array.isArray(formData.tags) && formData.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-2">
            {formData.tags.map((tag, index) => (
              <div key={index} className="flex items-center bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm">
                {tag}
                <button
                  type="button"
                  onClick={() => handleRemoveTag(index)}
                  className="ml-1 text-blue-600 hover:text-blue-800 focus:outline-none"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="mb-4">
        <label className="inline-flex items-center">
          <input
            type="checkbox"
            name="completed"
            checked={formData.completed}
            onChange={handleChange}
            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
          <span className="ml-2 text-sm text-gray-700">Completed</span>
        </label>
      </div>

      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {task ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;