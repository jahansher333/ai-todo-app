'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../lib/auth';
import { sendChatMessage, ChatRequest, ChatResponse } from '../lib/api';

interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

export function ChatInterface() {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const [isAuthChecked, setIsAuthChecked] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const { user, isAuthenticated } = useAuth();

  // Set current user ID when user is available
  useEffect(() => {
    const setUserId = () => {
      console.log('Checking auth state in ChatInterface:', {
        isAuthenticated,
        userExists: !!user,
        userId: user?.id,
        localStorageUserId: localStorage.getItem('user_id'),
        localStorageAccessToken: localStorage.getItem('access_token')
      });

      // First check if we have a user from the auth hook
      if (isAuthenticated && user && user.id) {
        console.log('Setting user ID from auth hook:', user.id);
        setCurrentUserId(user.id);
        setIsAuthChecked(true);
      } else {
        // Fallback to localStorage if auth hook doesn't have the user
        const userIdFromStorage = localStorage.getItem('user_id');
        if (userIdFromStorage) {
          console.log('Setting user ID from localStorage:', userIdFromStorage);
          setCurrentUserId(userIdFromStorage);
          setIsAuthChecked(true);
        } else {
          // Also check for any token which might indicate login
          const token = localStorage.getItem('access_token') || localStorage.getItem('auth-token') || localStorage.getItem('token');
          if (token) {
            // Try to decode the token to get user ID if possible
            try {
              const tokenParts = token.split('.');
              if (tokenParts.length === 3) {
                const payload = JSON.parse(atob(tokenParts[1]));
                if (payload.user_id) {
                  console.log('Setting user ID from decoded token:', payload.user_id);
                  setCurrentUserId(payload.user_id);
                  setIsAuthChecked(true);
                } else if (payload.id) {
                  console.log('Setting user ID from decoded token (id field):', payload.id);
                  setCurrentUserId(payload.id);
                  setIsAuthChecked(true);
                } else if (payload.sub) {
                  console.log('Setting user ID from decoded token (sub field):', payload.sub);
                  setCurrentUserId(payload.sub);
                  setIsAuthChecked(true);
                }
              }
            } catch (e) {
              console.warn('Could not decode token to get user ID', e);
            }
          }
        }
      }
    };

    // Initial call after a slight delay to ensure auth state is loaded
    const timer = setTimeout(setUserId, 100);

    // Set up event listener to catch auth changes from other parts of the app
    const handleStorageChange = () => {
      console.log('Storage change detected, updating user ID');
      setUserId();
    };

    // Listen for custom auth events as well
    const handleCustomAuthEvent = () => {
      console.log('Auth change event detected, updating user ID');
      setUserId();
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('authChange', handleCustomAuthEvent);

    return () => {
      clearTimeout(timer);
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('authChange', handleCustomAuthEvent);
    };
  }, [isAuthenticated, user]);

  // Check auth status on mount if not already checked
  useEffect(() => {
    if (!isAuthChecked) {
      // Manual check for auth status in localStorage
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth-token') || localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');

      if (token || userId) {
        if (userId) {
          setCurrentUserId(userId);
        } else if (token) {
          try {
            const tokenParts = token.split('.');
            if (tokenParts.length === 3) {
              const payload = JSON.parse(atob(tokenParts[1]));
              if (payload.user_id) {
                setCurrentUserId(payload.user_id);
              } else if (payload.id) {
                setCurrentUserId(payload.id);
              } else if (payload.sub) {
                setCurrentUserId(payload.sub);
              }
            }
          } catch (e) {
            console.warn('Could not decode token to get user ID', e);
          }
        }
        setIsAuthChecked(true);
      }
    }
  }, [isAuthChecked]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Try to get user ID from multiple sources to ensure we have it
    let userIdToUse = currentUserId;
    if (!userIdToUse) {
      userIdToUse = localStorage.getItem('user_id');
    }
    if (!userIdToUse && user && user.id) {
      userIdToUse = user.id;
    }

    // Also try to extract from token if we still don't have it
    if (!userIdToUse) {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth-token') || localStorage.getItem('token');
      if (token) {
        try {
          const tokenParts = token.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            if (payload.user_id) {
              userIdToUse = payload.user_id;
            } else if (payload.id) {
              userIdToUse = payload.id;
            } else if (payload.sub) {
              userIdToUse = payload.sub;
            }
          }
        } catch (e) {
          console.warn('Could not decode token to get user ID', e);
        }
      }
    }

    // Log for debugging
    console.log('Chat submit - inputValue:', inputValue, 'currentUserId:', currentUserId, 'user.id:', user?.id, 'localStorage user_id:', localStorage.getItem('user_id'), 'userIdToUse:', userIdToUse);

    if (!inputValue.trim() || isLoading) {
      console.log('Submit prevented - Missing data:', {
        hasInput: !!inputValue.trim(),
        hasUserId: !!userIdToUse,
        isLoading
      });
      return;
    }

    // If we still don't have a user ID, try to get it from localStorage as a final fallback
    if (!userIdToUse) {
      // Attempt to find any user ID from storage
      const userIdFromStorage = localStorage.getItem('user_id');
      if (userIdFromStorage) {
        userIdToUse = userIdFromStorage;
      } else {
        // Try to extract from token if available
        const token = localStorage.getItem('access_token') || localStorage.getItem('auth-token');
        if (token) {
          try {
            const parts = token.split('.');
            if (parts.length === 3) {
              const payload = JSON.parse(atob(parts[1]));
              userIdToUse = payload.user_id || payload.id || payload.sub || null;
            }
          } catch (e) {
            console.warn('Could not decode token to get user ID', e);
          }
        }
      }
    }

    // Add user message to UI immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    const newInputValue = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare chat request
      const request: ChatRequest = {
        message: newInputValue,
      };

      // Send to backend using the fallback user ID
      const response: ChatResponse = await sendChatMessage(userIdToUse!, request);

      // Add assistant response to UI
      const assistantMessage: ChatMessage = {
        id: `response-${Date.now()}`,
        content: response.response,
        role: 'assistant',
        timestamp: response.timestamp,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to UI
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 bg-white border border-gray-200 rounded-lg">
      {/* Chat header */}
      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200 rounded-t-lg">
        <h2 className="text-lg font-semibold text-gray-800">AI Task Assistant</h2>
        <p className="text-sm text-gray-600">Ask me to add, list, update, or complete tasks</p>
      </div>

      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-25 min-h-0">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
            <div className="mb-4 text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-800">Welcome to your AI Task Assistant!</h3>
            <p className="mt-1 text-gray-600">I can help you manage your tasks using natural language.</p>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-left">
              <div className="bg-blue-50 p-3 rounded-lg">
                <p className="font-medium text-blue-800">Try saying:</p>
                <ul className="mt-1 space-y-1 text-blue-700">
                  <li>• "Add task: Buy groceries"</li>
                  <li>• "Show all tasks"</li>
                </ul>
              </div>
              <div className="bg-green-50 p-3 rounded-lg">
                <p className="font-medium text-green-800">Or try:</p>
                <ul className="mt-1 space-y-1 text-green-700">
                  <li>• "Complete task 3"</li>
                  <li>• "Delete task: Buy milk"</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-200' : 'text-gray-500'}`}>
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[80%]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4 bg-white rounded-b-lg">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Message the AI assistant..."
            disabled={isLoading}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            aria-label="Type your message"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105 shadow-md hover:shadow-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500 flex justify-between">
          <span>AI Assistant</span>
          <span>Status: {isAuthenticated || currentUserId || localStorage.getItem('user_id') || localStorage.getItem('access_token') ? 'Connected' : 'Not authenticated'}</span>
        </div>
      </form>
    </div>
  );
}