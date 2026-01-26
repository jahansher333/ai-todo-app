import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing';
import Login from '@/app/login/page'; // Adjust path as needed

// Mock the API module
jest.mock('@/lib/api', () => ({
  userApi: {
    login: jest.fn(),
    register: jest.fn(),
  }
}));

describe('Login Component', () => {
  test('renders login form with email and password fields', () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Login />
      </MockedProvider>
    );

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  test('allows user to enter email and password', () => {
    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Login />
      </MockedProvider>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(emailInput).toHaveValue('test@example.com');
    expect(passwordInput).toHaveValue('password123');
  });

  test('calls login API when form is submitted', async () => {
    const mockLoginResponse = {
      id: 'user123',
      email: 'test@example.com',
      token: 'mock-jwt-token'
    };

    // Mock the login function
    const { userApi } = require('@/lib/api');
    (userApi.login as jest.MockedFunction<any>).mockResolvedValue(mockLoginResponse);

    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Login />
      </MockedProvider>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const loginButton = screen.getByRole('button', { name: /login/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(userApi.login).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  test('shows error message when login fails', async () => {
    // Mock the login function to reject
    const { userApi } = require('@/lib/api');
    (userApi.login as jest.MockedFunction<any>).mockRejectedValue(new Error('Invalid credentials'));

    render(
      <MockedProvider mocks={[]} addTypename={false}>
        <Login />
      </MockedProvider>
    );

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const loginButton = screen.getByRole('button', { name: /login/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });
});