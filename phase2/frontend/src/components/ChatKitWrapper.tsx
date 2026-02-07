'use client';

import { useAuth } from '../lib/auth';
import { ProtectedRoute } from './ProtectedRoute';
import { ChatInterface } from './ChatInterface';

interface ChatKitWrapperProps {
  children?: React.ReactNode;
}

export function ChatKitWrapper({ children }: ChatKitWrapperProps) {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading chat interface...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-800">Authentication Required</h2>
          <p className="mt-2 text-gray-600">Please log in to access the chat interface.</p>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="flex flex-col h-full">
        {children || <ChatInterface />}
      </div>
    </ProtectedRoute>
  );
}