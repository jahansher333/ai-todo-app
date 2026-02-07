// Chat-related TypeScript types

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
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

export interface GetConversationsResponse {
  conversations: Conversation[];
  total_count: number;
  limit: number;
  offset: number;
}

export interface GetMessagesResponse {
  messages: Message[];
}

export interface User {
  id: string;
  email: string;
  name: string;
}