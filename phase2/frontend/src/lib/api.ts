// API client with JWT header
import axios from 'axios';
import { formatErrorMessage } from './errorHandler';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token to every request
apiClient.interceptors.request.use(
  (config) => {
    // Get token from wherever you store it (localStorage, cookies, etc.)
    const token = localStorage.getItem('access_token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Token might be expired or invalid, redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export default apiClient;

// Helper function to normalize task tags
const normalizeTaskTags = (task: any) => {
  if (task.tags) {
    if (typeof task.tags === 'string') {
      try {
        // Parse JSON string to array
        const parsedTags = JSON.parse(task.tags);
        return { ...task, tags: Array.isArray(parsedTags) ? parsedTags : [task.tags] };
      } catch (e) {
        // If parsing fails, treat as single tag
        return { ...task, tags: [task.tags] };
      }
    } else if (Array.isArray(task.tags)) {
      return task; // Already an array
    } else {
      return { ...task, tags: [String(task.tags)] }; // Convert to array
    }
  }
  return { ...task, tags: [] }; // Default to empty array
};

// Export specific API functions
export const taskApi = {
  // Get all tasks for a user
  getTasks: async (userId: string, params?: { status?: string; priority?: string; search?: string }) => {
    const response = await apiClient.get(`/api/${userId}/tasks`, { params });
    // Normalize tags for all tasks
    return response.data.map((task: any) => normalizeTaskTags(task));
  },

  // Create a new task
  createTask: async (userId: string, taskData: any) => {
    // Convert tags array to JSON string for backend
    const taskDataToSend = {
      ...taskData,
      tags: typeof taskData.tags === 'string' ? taskData.tags : JSON.stringify(taskData.tags || [])
    };
    const response = await apiClient.post(`/api/${userId}/tasks`, taskDataToSend);
    return normalizeTaskTags(response.data);
  },

  // Update a task
  updateTask: async (userId: string, taskId: string, taskData: any) => {
    // Convert tags array to JSON string for backend
    const taskDataToSend = {
      ...taskData,
      tags: typeof taskData.tags === 'string' ? taskData.tags : JSON.stringify(taskData.tags || [])
    };
    const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, taskDataToSend);
    return normalizeTaskTags(response.data);
  },

  // Delete a task
  deleteTask: async (userId: string, taskId: string) => {
    const response = await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Update task completion status
  updateTaskCompletion: async (userId: string, taskId: string, completed: boolean) => {
    const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`, { completed });
    return normalizeTaskTags(response.data);
  },
};

// Export user-related API functions
export const userApi = {
  // Login
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },

  // Register
  register: async (userData: { email: string; password: string; firstName?: string; lastName?: string }) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },
};