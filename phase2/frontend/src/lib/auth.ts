// Mock authentication implementation for the chatbot
// In a real implementation, this would integrate with Better-Auth

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

// Mock user data - will be updated with real data from token
let MOCK_USER: any = {
  id: null,
  email: null,
  name: null
};

// Mock authentication state
let isAuthenticatedState = false;
let authToken: string | null = null;

/**
 * Get the current authentication token
 */
export async function getAuthToken(): Promise<string> {
  if (!authToken) {
    // In a real implementation, this would retrieve the token from storage or session
    // Check for both possible token locations
    authToken = localStorage.getItem('auth-token') || localStorage.getItem('access_token') || '';
  }
  return authToken;
}

/**
 * Set the authentication token
 */
export function setAuthToken(token: string): void {
  authToken = token;
  localStorage.setItem('auth-token', token);
  localStorage.setItem('access_token', token);  // Also set in access_token for consistency
}

/**
 * Mock login function
 */
async function internalLogin(email: string, password: string): Promise<boolean> {
  // In a real implementation, this would call the backend auth API
  if (email && password) {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.token;

        if (token) {
          setAuthToken(token);
          isAuthenticatedState = true;
          return true;
        }
      }
    } catch (error) {
      console.error('Login error:', error);
    }

    // Fallback to mock token if API call fails
    isAuthenticatedState = true;
    const mockToken = `mock.${btoa(JSON.stringify({ user_id: 'user123', exp: Math.floor(Date.now() / 1000) + 3600 }))}.signature`;
    setAuthToken(mockToken);
    return true;
  }
  return false;
}

/**
 * Mock logout function
 */
async function internalLogout(): Promise<void> {
  try {
    // In a real implementation, this would call the backend logout API
    const token = await getAuthToken();
    if (token) {
      await fetch('/api/auth/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });
    }
  } catch (error) {
    console.error('Logout error:', error);
  }

  isAuthenticatedState = false;
  authToken = null;
  localStorage.removeItem('auth-token');
  localStorage.removeItem('access_token');  // Also remove from access_token
}

/**
 * Check if user is authenticated
 */
export function checkAuthStatus(): boolean {
  // In a real implementation, this would validate the token
  // Check multiple possible token locations
  const token = localStorage.getItem('auth-token') || localStorage.getItem('access_token') || localStorage.getItem('token');
  if (token) {
    try {
      // Handle both JWT and mock token formats
      let payload: any;

      if (token.startsWith('mock.')) {
        // Handle mock token format
        const parts = token.split('.');
        if (parts.length === 3) {
          payload = JSON.parse(atob(parts[1]));
        }
      } else {
        // Handle standard JWT format
        const parts = token.split('.');
        if (parts.length === 3) {
          payload = JSON.parse(atob(parts[1]));
        }
      }

      if (payload) {
        const now = Math.floor(Date.now() / 1000);

        // Check if token has expiration and if it's not expired
        if (!payload.exp || payload.exp > now) {
          // Update MOCK_USER with data from token
          MOCK_USER = {
            id: payload.user_id || payload.id || payload.sub,
            email: payload.email || payload.sub || 'user@example.com',
            name: payload.name || payload.first_name || payload.last_name || 'User'
          };

          // Store user ID in localStorage for dashboard compatibility
          if (payload.user_id) {
            localStorage.setItem('user_id', payload.user_id);
          } else if (payload.id) {
            localStorage.setItem('user_id', payload.id);
          } else if (payload.sub) {
            localStorage.setItem('user_id', payload.sub);
          }

          isAuthenticatedState = true;
          return true;
        }
      }
    } catch (e) {
      console.error('Error validating token:', e);
      // If token decoding fails, try to get user ID directly from localStorage
      const userId = localStorage.getItem('user_id');
      if (userId) {
        MOCK_USER = {
          id: userId,
          email: localStorage.getItem('user_email') || 'user@example.com',
          name: localStorage.getItem('user_name') || 'User'
        };
        isAuthenticatedState = true;
        return true;
      }
    }
  }

  isAuthenticatedState = false;
  return false;
}

/**
 * React hook for authentication state
 */
export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Function to update auth state
  const updateAuthState = () => {
    const authStatus = checkAuthStatus();
    setIsAuthenticated(authStatus);

    if (authStatus) {
      // Ensure user ID is properly set from localStorage if not already in MOCK_USER
      const userIdFromStorage = localStorage.getItem('user_id');
      if (userIdFromStorage) {
        MOCK_USER.id = userIdFromStorage;
      }
      setUser({...MOCK_USER});
    } else {
      setUser(null);
    }
  };

  useEffect(() => {
    // Check auth status on mount and set up listener for changes
    updateAuthState();

    // Set up event listener to catch auth changes from other parts of the app
    const handleStorageChange = () => {
      updateAuthState();
    };

    // Listen for custom auth events as well
    const handleCustomAuthEvent = () => {
      updateAuthState();
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('authChange', handleCustomAuthEvent);

    setIsLoading(false);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('authChange', handleCustomAuthEvent);
    };
  }, []);

  return {
    isAuthenticated,
    user,
    isLoading,
    login: async (email: string, password: string) => {
      const result = await internalLogin(email, password);
      if (result) {
        // Dispatch custom event to notify other components
        updateAuthState();
        window.dispatchEvent(new CustomEvent('authChange'));
      }
      return result;
    },
    logout: async () => {
      await internalLogout();
      updateAuthState();
      window.dispatchEvent(new CustomEvent('authChange'));
    }
  };
}

// Export login and logout functions for direct use
export { internalLogin as login, internalLogout as logout };