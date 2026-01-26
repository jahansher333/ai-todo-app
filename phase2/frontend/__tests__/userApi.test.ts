import { userApi } from '@/lib/api';
import MockAdapter from 'axios-mock-adapter';
import apiClient from '@/lib/api';

describe('User API Functions', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(apiClient);
  });

  afterEach(() => {
    mock.reset();
  });

  test('login should call POST /auth/login and return user data with token', async () => {
    const loginData = {
      email: 'test@example.com',
      password: 'password123'
    };

    const mockResponse = {
      id: 'user123',
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User',
      token: 'mock-jwt-token'
    };

    mock.onPost('/auth/login').reply(200, mockResponse);

    const result = await userApi.login(loginData.email, loginData.password);
    expect(result).toEqual(mockResponse);
  });

  test('login should handle invalid credentials', async () => {
    const loginData = {
      email: 'invalid@example.com',
      password: 'wrongpassword'
    };

    mock.onPost('/auth/login').reply(401, { detail: 'Incorrect email or password' });

    await expect(userApi.login(loginData.email, loginData.password)).rejects.toEqual(
      expect.objectContaining({ response: expect.objectContaining({ status: 401 }) })
    );
  });

  test('register should call POST /auth/register and return user data with token', async () => {
    const userData = {
      email: 'newuser@example.com',
      password: 'password123',
      firstName: 'New',
      lastName: 'User'
    };

    const mockResponse = {
      id: 'user456',
      email: 'newuser@example.com',
      first_name: 'New',
      last_name: 'User',
      token: 'mock-jwt-token'
    };

    mock.onPost('/auth/register').reply(200, mockResponse);

    const result = await userApi.register(userData);
    expect(result).toEqual(mockResponse);
  });

  test('register should handle invalid email format', async () => {
    const userData = {
      email: 'invalid-email',
      password: 'password123'
    };

    mock.onPost('/auth/register').reply(400, { detail: 'Invalid email format' });

    await expect(userApi.register(userData)).rejects.toEqual(
      expect.objectContaining({ response: expect.objectContaining({ status: 400 }) })
    );
  });

  test('register should handle weak password', async () => {
    const userData = {
      email: 'weak@example.com',
      password: 'weak'
    };

    mock.onPost('/auth/register').reply(400, { detail: 'Password must be at least 6 characters long' });

    await expect(userApi.register(userData)).rejects.toEqual(
      expect.objectContaining({ response: expect.objectContaining({ status: 400 }) })
    );
  });

  test('register should handle existing email', async () => {
    const userData = {
      email: 'existing@example.com',
      password: 'password123'
    };

    mock.onPost('/auth/register').reply(400, { detail: 'User with this email already exists' });

    await expect(userApi.register(userData)).rejects.toEqual(
      expect.objectContaining({ response: expect.objectContaining({ status: 400 }) })
    );
  });

  test('API should handle network errors', async () => {
    mock.onPost('/auth/login').networkError();

    await expect(userApi.login('test@example.com', 'password123')).rejects.toEqual(
      expect.objectContaining({ message: 'Network Error' })
    );
  });
});