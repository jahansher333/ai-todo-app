import { taskApi } from '@/lib/api';
import MockAdapter from 'axios-mock-adapter';
import apiClient from '@/lib/api';

describe('Task API Functions', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(apiClient);
  });

  afterEach(() => {
    mock.reset();
  });

  test('getTasks should call GET /api/{userId}/tasks with various filter combinations', async () => {
    const userId = 'user123';
    const mockTasks = [
      { id: '1', title: 'Task 1', completed: false, priority: 'high' },
      { id: '2', title: 'Task 2', completed: true, priority: 'low' }
    ];

    mock.onGet(new RegExp(`/api/${userId}/tasks`)).reply(200, mockTasks);

    const result = await taskApi.getTasks(userId);
    expect(result).toEqual(mockTasks);

    // Test with filters
    const filteredResult = await taskApi.getTasks(userId, { status: 'completed', priority: 'high' });
    expect(filteredResult).toEqual(mockTasks);
  });

  test('createTask should call POST /api/{userId}/tasks with various task data', async () => {
    const userId = 'user123';
    const taskData = {
      title: 'New Task',
      description: 'Task Description',
      completed: false,
      priority: 'medium'
    };
    const createdTask = { ...taskData, id: 'task123', user_id: userId };

    mock.onPost(new RegExp(`/api/${userId}/tasks`)).reply(200, createdTask);

    const result = await taskApi.createTask(userId, taskData);
    expect(result).toEqual(createdTask);
  });

  test('updateTask should call PUT /api/{userId}/tasks/{taskId} with valid/invalid data', async () => {
    const userId = 'user123';
    const taskId = 'task123';
    const taskData = {
      title: 'Updated Task',
      description: 'Updated Description',
      completed: true,
      priority: 'high'
    };
    const updatedTask = { ...taskData, id: taskId, user_id: userId };

    mock.onPut(new RegExp(`/api/${userId}/tasks/${taskId}`)).reply(200, updatedTask);

    const result = await taskApi.updateTask(userId, taskId, taskData);
    expect(result).toEqual(updatedTask);
  });

  test('deleteTask should call DELETE /api/{userId}/tasks/{taskId}', async () => {
    const userId = 'user123';
    const taskId = 'task123';
    const deleteResponse = { message: 'Task deleted successfully' };

    mock.onDelete(new RegExp(`/api/${userId}/tasks/${taskId}`)).reply(200, deleteResponse);

    const result = await taskApi.deleteTask(userId, taskId);
    expect(result).toEqual(deleteResponse);
  });

  test('updateTaskCompletion should call PATCH /api/{userId}/tasks/{taskId}/complete', async () => {
    const userId = 'user123';
    const taskId = 'task123';
    const completed = true;
    const updatedTask = {
      id: taskId,
      title: 'Test Task',
      completed: true,
      user_id: userId
    };

    mock.onPatch(new RegExp(`/api/${userId}/tasks/${taskId}/complete`)).reply(200, updatedTask);

    const result = await taskApi.updateTaskCompletion(userId, taskId, completed);
    expect(result).toEqual(updatedTask);
  });

  test('API should handle error responses appropriately', async () => {
    const userId = 'user123';

    // Mock error responses
    mock.onGet(new RegExp(`/api/${userId}/tasks`)).reply(500, { error: 'Server error' });

    await expect(taskApi.getTasks(userId)).rejects.toEqual(
      expect.objectContaining({ response: expect.objectContaining({ status: 500 }) })
    );
  });
});