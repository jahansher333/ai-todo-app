'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import KanbanBoard from '@/components/KanbanBoard';
import TaskForm from '@/components/TaskForm';
import Filters from '@/components/Filters';
import { FloatingChatButton } from '@/components/FloatingChatButton';
import { taskApi } from '@/lib/api';
import { Task } from '@/types/index';
import { formatErrorMessage } from '@/lib/errorHandler';

const DashboardPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [viewMode, setViewMode] = useState<'kanban' | 'list'>('kanban'); // Toggle between Kanban and List view
  const [filters, setFilters] = useState({
    status: null as string | null,
    priority: null as string | null,
    search: '',
    sortBy: 'created_at'
  });
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [animateTask, setAnimateTask] = useState<string | null>(null);
  const router = useRouter();
  const taskRefs = useRef<{[key: string]: HTMLLIElement | null}>({});
  
  const setTaskRef = (id: string) => (element: HTMLLIElement | null) => {
    taskRefs.current[id] = element;
  };

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }

    const userId = localStorage.getItem('user_id');
    if (!userId) {
      // If user ID is not available, redirect to login
      router.push('/login');
      return;
    }

    fetchTasks(userId);

    // Dispatch auth change event to notify other components
    window.dispatchEvent(new CustomEvent('authChange'));
  }, []);

  // Fetch tasks when filters change
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const userId = localStorage.getItem('user_id');

    if (!token || !userId) {
      router.push('/login');
      return;
    }

    fetchTasks(userId);
  }, [filters]);

  const fetchTasks = async (userId: string) => {
    try {
      setLoading(true);
      const tasksData = await taskApi.getTasks(userId, {
        status: filters.status || undefined,
        priority: filters.priority || undefined,
        search: filters.search || undefined
      });

      // Apply sorting
      let sortedTasks = [...tasksData];
      sortedTasks.sort((a, b) => {
        switch (filters.sortBy) {
          case 'due':
            if (!a.due_date) return 1;
            if (!b.due_date) return -1;
            return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
          case 'priority':
            const priorityOrder: {[key: string]: number} = { high: 3, medium: 2, low: 1 };
            return priorityOrder[b.priority] - priorityOrder[a.priority];
          case 'title':
            return a.title.localeCompare(b.title);
          case 'updated_at':
            return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
          case 'created_at':
          default:
            return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        }
      });

      setTasks(sortedTasks);
    } catch (err: any) {
      setError(formatErrorMessage(err) || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = () => {
    setEditingTask(null);
    setShowTaskForm(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      const token = localStorage.getItem('access_token');
      const userId = localStorage.getItem('user_id');

      if (!token || !userId) {
        router.push('/login');
        return;
      }

      await taskApi.deleteTask(userId, taskId);
      setTasks(tasks.filter(task => task.id !== taskId));

      // Trigger animation for deleted task
      setAnimateTask(taskId);
      setTimeout(() => {
        setAnimateTask(null);
      }, 500);
    } catch (err: any) {
      setError(formatErrorMessage(err) || 'Failed to delete task');
    }
  };

  const handleSubmitTask = async (taskData: any) => {
    try {
      const token = localStorage.getItem('access_token');
      const userId = localStorage.getItem('user_id');

      if (!token || !userId) {
        router.push('/login');
        return;
      }

      if (editingTask) {
        // Update existing task
        const updatedTask = await taskApi.updateTask(userId, editingTask.id, taskData);
        setTasks(tasks.map(t => t.id === editingTask.id ? updatedTask : t));

        // Trigger animation for updated task
        setAnimateTask(updatedTask.id);
        setTimeout(() => {
          setAnimateTask(null);
        }, 500);
      } else {
        // Create new task
        const newTask = await taskApi.createTask(userId, taskData);
        setTasks([...tasks, newTask]);

        // Trigger animation for new task
        setAnimateTask(newTask.id);
        setTimeout(() => {
          setAnimateTask(null);
        }, 500);
      }

      setShowTaskForm(false);
      setEditingTask(null);
    } catch (err: any) {
      setError(formatErrorMessage(err) || 'Failed to save task');
    }
  };

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
  };

  const handleUpdateTask = async (taskData: any) => {
    try {
      const token = localStorage.getItem('access_token');
      const userId = localStorage.getItem('user_id');

      if (!token || !userId) {
        router.push('/login');
        return;
      }

      const updatedTask = await taskApi.updateTask(userId, taskData.id, taskData);
      setTasks(tasks.map(t => t.id === taskData.id ? updatedTask : t));

      // Trigger animation for updated task
      setAnimateTask(updatedTask.id);
      setTimeout(() => {
        setAnimateTask(null);
      }, 500);
    } catch (err: any) {
      setError(formatErrorMessage(err) || 'Failed to update task');
    }
  };

  const handleUserLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600 font-medium">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center">
                <div className="h-8 w-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">T</span>
                </div>
                <span className="ml-2 text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  TodoJira
                </span>
              </Link>
            </div>

            <div className="hidden md:flex items-center space-x-6">
              <button
                onClick={() => setViewMode(viewMode === 'kanban' ? 'list' : 'kanban')}
                className="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Switch to {viewMode === 'kanban' ? 'List' : 'Kanban'} View
              </button>

              <button
                onClick={handleUserLogout}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all duration-200 flex items-center space-x-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clipRule="evenodd" />
                </svg>
                <span>Logout</span>
              </button>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-md text-gray-700 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Mobile sidebar */}
        {sidebarOpen && (
          <div className="md:hidden bg-white border-t border-gray-200">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <button
                onClick={() => {
                  setViewMode(viewMode === 'kanban' ? 'list' : 'kanban');
                  setSidebarOpen(false);
                }}
                className="block px-3 py-2 rounded-md text-base font-medium text-white bg-blue-600 w-full text-left"
              >
                Switch to {viewMode === 'kanban' ? 'List' : 'Kanban'} View
              </button>
              <button
                onClick={() => {
                  handleUserLogout();
                  setSidebarOpen(false);
                }}
                className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 w-full text-left"
              >
                Logout
              </button>
            </div>
          </div>
        )}
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Welcome Banner */}
        <div className="mb-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl shadow-lg overflow-hidden">
          <div className="p-6 md:p-8">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between">
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-white mb-2">
                  Welcome back! 👋
                </h1>
                <p className="text-blue-100">
                  You have {tasks.filter(t => !t.completed).length} pending tasks to tackle today.
                </p>
              </div>
              <div className="mt-4 md:mt-0">
                <button
                  onClick={handleAddTask}
                  className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-all duration-200 transform hover:scale-105 flex items-center space-x-2"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                  </svg>
                  <span>Add Task</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow p-6 border border-gray-100 transform transition-all duration-300 hover:scale-105">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-blue-100 text-blue-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-gray-600">Total Tasks</h3>
                <p className="text-2xl font-semibold text-gray-900">{tasks.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow p-6 border border-gray-100 transform transition-all duration-300 hover:scale-105">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-green-100 text-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-gray-600">Completed</h3>
                <p className="text-2xl font-semibold text-gray-900">{tasks.filter(t => t.completed).length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow p-6 border border-gray-100 transform transition-all duration-300 hover:scale-105">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-yellow-100 text-yellow-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-gray-600">Pending</h3>
                <p className="text-2xl font-semibold text-gray-900">{tasks.filter(t => !t.completed).length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-6">
          <Filters onFilterChange={handleFilterChange} />
        </div>

        {/* Error message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg mb-6" role="alert">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Task Form Modal */}
        {showTaskForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fadeIn">
            <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl transform transition-all duration-300 scale-100 opacity-100">
              <TaskForm
                task={editingTask || undefined}
                onSubmit={handleSubmitTask}
                onCancel={() => setShowTaskForm(false)}
              />
            </div>
          </div>
        )}

        <div className="flex flex-col gap-6">
          {/* Task View */}
          {viewMode === 'kanban' ? (
            <div className="animate-slideUp flex-1">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Kanban Board</h2>
                <p className="text-gray-600">{tasks.length} tasks</p>
              </div>
              <div className="overflow-x-auto -mx-4 px-4">
                <KanbanBoard
                  tasks={tasks}
                  onTaskUpdate={handleUpdateTask}
                  onTaskDelete={handleDeleteTask}
                  animateTask={animateTask}
                />
              </div>
            </div>
          ) : (
            <div className="animate-slideUp">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800">List View</h2>
                <p className="text-gray-600">{tasks.length} tasks</p>
              </div>
              <div className="bg-white shadow rounded-lg overflow-hidden">
                <ul className="divide-y divide-gray-200">
                  {tasks.map((task) => (
                    <li
                      key={task.id}
                      ref={task.id === animateTask ? setTaskRef(task.id) : null}
                      className={`transition-all duration-300 ${
                        animateTask === task.id ? 'animate-pulse bg-blue-50' : 'bg-white'
                      }`}
                    >
                      <div className="px-6 py-5 sm:px-6 flex justify-between items-center hover:bg-gray-50 transition-colors duration-200">
                        <div className="flex items-center">
                          <input
                            type="checkbox"
                            checked={task.completed}
                            onChange={() => {
                              const updatedTask = { ...task, completed: !task.completed };
                              handleUpdateTask(updatedTask);
                            }}
                            className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                          />
                          <div className="ml-4">
                            <p className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                              {task.title}
                            </p>
                            <p className="text-sm text-gray-500 max-w-md truncate">
                              {task.description}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                            task.priority === 'high' ? 'bg-red-100 text-red-800' :
                            task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {task.priority}
                          </span>
                          {task.due && (
                            <span className="text-xs text-gray-500 whitespace-nowrap">
                              {new Date(task.due).toLocaleDateString()}
                            </span>
                          )}
                          <button
                            onClick={() => handleEditTask(task)}
                            className="text-blue-600 hover:text-blue-900 p-1 rounded hover:bg-blue-50 transition-colors duration-200"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                          </button>
                          <button
                            onClick={() => handleDeleteTask(task.id)}
                            className="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50 transition-colors duration-200"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {tasks.length === 0 && !loading && (
            <div className="text-center py-16 animate-fadeIn">
              <div className="mx-auto h-24 w-24 text-gray-400 flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-24 w-24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks yet</h3>
              <p className="mt-1 text-gray-500">Get started by creating your first task.</p>
              <div className="mt-6">
                <button
                  onClick={handleAddTask}
                  className="inline-flex items-center px-6 py-3 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transform hover:scale-105 transition-all duration-200"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="-ml-1 mr-3 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2 0h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                  </svg>
                  Add your first task
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Floating Chat Button */}
      <FloatingChatButton />

      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.02); }
          100% { transform: scale(1); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out;
        }
        .animate-slideUp {
          animation: slideUp 0.5s ease-out;
        }
        .animate-pulse {
          animation: pulse 0.5s ease-in-out;
        }
      `}</style>
    </div>
  );
};

export default DashboardPage;