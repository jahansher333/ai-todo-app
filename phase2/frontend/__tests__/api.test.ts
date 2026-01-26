import apiClient, { taskApi, userApi } from '@/lib/api';
import MockAdapter from 'axios-mock-adapter';

describe('API Client Configuration', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(apiClient);
  });

  afterEach(() => {
    mock.reset();
  });

  test('should have correct base URL configured', () => {
    // Check that the base URL is properly set
    expect(apiClient.defaults.baseURL).toBeDefined();
  });

  test('should inject JWT token in request headers', async () => {
    // Mock token in localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(() => 'mock-jwt-token'),
        setItem: jest.fn(),
        removeItem: jest.fn(),
      },
      writable: true,
    });

    mock.onGet('/test').reply(200, {});

    await apiClient.get('/test');

    const lastRequest = mock.history.get[mock.history.get.length - 1];
    expect(lastRequest.headers['Authorization']).toBe('Bearer mock-jwt-token');
  });

  test('should handle error for 401 Unauthorized responses', async () => {
    // Mock localStorage to track token removal
    const localStorageMock = {
      getItem: jest.fn(),
      setItem: jest.fn(),
      removeItem: jest.fn(),
    };
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock,
      writable: true,
    });

    // Mock window.location for redirect
    const originalLocation = window.location;
    delete (window as any).location;
    window.location = {
      ...originalLocation,
      href: '',
      assign: jest.fn(),
      replace: jest.fn(),
    };

    mock.onGet('/protected').reply(401);

    await expect(apiClient.get('/protected')).rejects.toThrow();

    // Verify token was removed from localStorage
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('access_token');

    // Restore original location
    window.location = originalLocation;
  });

  test('should handle timeout', async () => {
    // Set a very short timeout for testing
    apiClient.defaults.timeout = 10; // 10ms

    // Simulate a slow response to trigger timeout
    mock.onGet('/slow').reply(() => {
      return new Promise(resolve => {
        setTimeout(() => resolve([200, { data: 'response' }]), 100); // 100ms > 10ms timeout
      });
    });

    await expect(apiClient.get('/slow')).rejects.toThrow();
  });
});