'use client';

// Simple test component to verify the chat interface works
import { ChatInterface } from './ChatInterface';

export function TestChatInterface() {
  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Chat Interface Test</h1>
      <p className="mb-4">Below is the chat interface component:</p>
      <div className="border rounded-lg overflow-hidden">
        <ChatInterface />
      </div>
    </div>
  );
}