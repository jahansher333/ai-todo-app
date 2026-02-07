'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth'; // Assuming you have an auth hook
import { ChatInterface } from '@/components/ChatInterface';

export default function ChatPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading } = useAuth();
  const [hasCheckedAuth, setHasCheckedAuth] = useState(false);

  useEffect(() => {
    // Check authentication status
    if (!isLoading) {
      if (!isAuthenticated || !user) {
        // Redirect to login if not authenticated
        router.push('/login');
      } else {
        setHasCheckedAuth(true);
      }
    }
  }, [isAuthenticated, user, isLoading, router]);

  // Show loading state while checking auth
  if (isLoading || !hasCheckedAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading chat...</p>
        </div>
      </div>
    );
  }

  // Render the chat interface if authenticated
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Task Assistant</h1>
          <p className="text-gray-600">Chat with your AI assistant to manage your tasks</p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
}