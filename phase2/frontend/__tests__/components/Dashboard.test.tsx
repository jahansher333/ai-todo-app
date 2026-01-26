import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing';
import Dashboard from '@/app/dashboard/page'; // Adjust path as needed

// Mock the API module
jest.mock('@/lib/api', () => ({
  taskApi: {
    getTasks: jest.fn(),
    createTask: jest.fn(),
    updateTask: jest.fn(),
    deleteTask: jest.fn(),
    updateTaskCompletion: jest.fn(),
  },
  userApi: {
    login: jest.fn(),
    register: jest.fn(),
  }
}));

describe('Dashboard Component', () => {
  test('renders dashboard with loading state initially', () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Dashboard />
      </MockedProvider>
    );

    // Check for loading indicators
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('fetches and displays tasks when mounted', async () => {
    const mockTasks = [
      { id: '1', title: 'Task 1', completed: false, priority: 'high' },
      { id: '2', title: 'Task 2', completed: true, priority: 'low' }
    ];

    // Mock the getTasks function
    const { taskApi } = require('@/lib/api');
    (taskApi.getTasks as jest.MockedFunction<any>).mockResolvedValue(mockTasks);

    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Dashboard />
      </MockedProvider>
    );

    // Wait for tasks to be loaded and displayed
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });
  });

  test('handles error when fetching tasks fails', async () => {
    // Mock the getTasks function to reject
    const { taskApi } = require('@/lib/api');
    (taskApi.getTasks as jest.MockedFunction<any>).mockRejectedValue(new Error('Failed to fetch'));

    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Dashboard />
      </MockedProvider>
    );

    // Wait for error handling
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});