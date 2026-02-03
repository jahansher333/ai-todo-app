import { getAuthToken } from './auth'; // Adjust import based on your auth implementation

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Generic API request function with JWT token
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  includeToken: boolean = true
): Promise<T> {
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(includeToken ? { 'Authorization': `Bearer ${await getAuthToken()}` } : {}),
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const errorData = await response.text();
    // If it's a 401 error, redirect to login
    if (response.status === 401) {
      localStorage.removeItem('auth-token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      window.location.href = '/login';
    }
    throw new Error(`API request failed: ${response.status} - ${errorData}`);
  }

  // Handle responses that might not have JSON content
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json();
  } else {
    return response.text() as unknown as T;
  }
}

/**
 * Chat API functions
 */
export interface ChatRequest {
  message: string;
  conversation_id?: string;
  model_preferences?: {
    temperature?: number;
  };
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  action_taken: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  sequence_number: number;
}

export interface GetConversationsResponse {
  conversations: Conversation[];
  total_count: number;
  limit: number;
  offset: number;
}

export interface GetMessagesResponse {
  messages: Message[];
}

/**
 * Send a chat message to the AI assistant
 */
export async function sendChatMessage(userId: string, request: ChatRequest): Promise<ChatResponse> {
  return apiRequest<ChatResponse>(`/api/${userId}/chat`, {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

/**
 * Get user's conversations
 */
export async function getUserConversations(userId: string): Promise<GetConversationsResponse> {
  return apiRequest<GetConversationsResponse>(`/api/${userId}/conversations`);
}

/**
 * Get messages from a specific conversation
 */
export async function getConversationMessages(userId: string, conversationId: string): Promise<GetMessagesResponse> {
  return apiRequest<GetMessagesResponse>(`/api/${userId}/conversations/${conversationId}/messages`);
}

/**
 * Health check for the API
 */
export async function healthCheck(): Promise<{ status: string; service: string }> {
  return apiRequest<{ status: string; service: string }>('/', {}, false);
}

/**
 * Generic error handler for API responses
 */
export function handleApiError(error: any): string {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return 'Network error: Please check your connection';
  }
  if (error.response?.status === 401) {
    return 'Unauthorized: Please log in again';
  }
  if (error.response?.status === 403) {
    return 'Forbidden: You do not have access to this resource';
  }
  if (error.response?.status === 429) {
    return 'Rate limit exceeded: Please try again later';
  }
  if (error.response?.status >= 500) {
    return 'Server error: Please try again later';
  }
  return error.message || 'An unexpected error occurred';
}

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
    const response = await apiRequest(`/api/${userId}/tasks`, { method: 'GET', params });
    // Normalize tags for all tasks
    return response.map((task: any) => normalizeTaskTags(task));
  },

  // Create a new task
  createTask: async (userId: string, taskData: any) => {
    // Convert tags array to JSON string for backend
    const taskDataToSend = {
      ...taskData,
      tags: typeof taskData.tags === 'string' ? taskData.tags : JSON.stringify(taskData.tags || [])
    };
    const response = await apiRequest(`/api/${userId}/tasks`, { method: 'POST', body: JSON.stringify(taskDataToSend) });
    return normalizeTaskTags(response);
  },

  // Update a task
  updateTask: async (userId: string, taskId: string, taskData: any) => {
    // Convert tags array to JSON string for backend
    const taskDataToSend = {
      ...taskData,
      tags: typeof taskData.tags === 'string' ? taskData.tags : JSON.stringify(taskData.tags || [])
    };
    const response = await apiRequest(`/api/${userId}/tasks/${taskId}`, { method: 'PUT', body: JSON.stringify(taskDataToSend) });
    return normalizeTaskTags(response);
  },

  // Delete a task
  deleteTask: async (userId: string, taskId: string) => {
    const response = await apiRequest(`/api/${userId}/tasks/${taskId}`, { method: 'DELETE' });
    return response;
  },

  // Update task completion status
  updateTaskCompletion: async (userId: string, taskId: string, completed: boolean) => {
    const response = await apiRequest(`/api/${userId}/tasks/${taskId}/complete`, { method: 'PATCH', body: JSON.stringify({ completed }) });
    return normalizeTaskTags(response);
  },
};

// Export user-related API functions
export const userApi = {
  // Login
  login: async (email: string, password: string) => {
    const response = await apiRequest('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }, false);
    return response;
  },

  // Register
  register: async (userData: { email: string; password: string; firstName?: string; lastName?: string }) => {
    const response = await apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(userData) }, false);
    return response;
  },
};