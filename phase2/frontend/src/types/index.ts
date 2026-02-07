// Define the Task type to match the backend model
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  due?: string | null; // ISO date string
  recurring: 'daily' | 'weekly' | 'monthly' | 'none';
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  status?: string; // Additional field for UI state
}

// Define the User type to match the backend model
export interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  is_active: boolean;
}

// Define filter options type
export interface FilterOptions {
  status: string | null;
  priority: string | null;
  search: string;
  sortBy: string;
}