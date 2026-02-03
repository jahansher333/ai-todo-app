'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);

    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      // If logged in, redirect to dashboard
      router.push('/dashboard');
    }
    // If not logged in, stay on landing page (default behavior)
  }, [router]);

  // Global keyboard shortcut for search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Focus search when '/' is pressed and not in an input field
      if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes((e.target as HTMLElement).tagName)) {
        e.preventDefault();
        const searchInput = document.getElementById('global-search-input');
        if (searchInput) {
          searchInput.focus();
        }
      }

      // Allow escape to blur search
      if (e.key === 'Escape') {
        const searchInput = document.getElementById('global-search-input');
        if (document.activeElement === searchInput) {
          (searchInput as HTMLInputElement).blur();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  // Since we're redirecting if logged in, we'll show the landing page content here
  return (
    <div className="min-h-screen w-full overflow-x-auto bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Floating particles background - rendered only on client side to prevent hydration errors */}
      {isMounted && (
        <div className="fixed inset-0 overflow-hidden pointer-events-none w-full max-w-full">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-full opacity-20 animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${3 + Math.random() * 4}s`
              }}
            ></div>
          ))}
        </div>
      )}

      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-xl z-50 border-b border-white/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full max-w-full">
          <div className="flex justify-between items-center h-16 w-full max-w-full">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="h-10 w-10 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                  <span className="text-white font-bold text-xl">T</span>
                </div>
                <span className="ml-3 text-2xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  TodoJira
                </span>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-700 hover:text-blue-600 transition-all duration-300 font-medium hover:scale-105">
                Features
              </a>
              <a href="#how-it-works" className="text-gray-700 hover:text-blue-600 transition-all duration-300 font-medium hover:scale-105">
                How It Works
              </a>
              <a href="#search-capabilities" className="text-gray-700 hover:text-blue-600 transition-all duration-300 font-medium hover:scale-105">
                Search
              </a>
              <a href="/chat" className="text-gray-700 hover:text-blue-600 transition-all duration-300 font-medium hover:scale-105 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                Chat
              </a>
              <a href="/login" className="text-gray-700 hover:text-blue-600 transition-all duration-300 font-medium hover:scale-105">
                Login
              </a>
              <div className="flex items-center space-x-2 bg-gray-100 px-3 py-1 rounded-lg border border-gray-200">
                <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="text-sm text-gray-600">Press '/' to search</span>
              </div>
              <a
                href="/chat"
                className="px-6 py-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-110 shadow-lg hover:shadow-xl font-semibold"
              >
                Try Chatbot →
              </a>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center">
              <button className="p-2 rounded-md text-gray-700 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-24 pb-20 px-4 sm:px-6 lg:px-8 relative w-full max-w-full">
        <div className="max-w-7xl mx-auto w-full max-w-full">
          <div className="text-center w-full max-w-full">
            <div className={`transition-all duration-1000 ease-out transform ${isMounted ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'} w-full max-w-full`}>
              <div className="inline-block px-4 py-1 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full mb-6">
                <span className="text-sm font-medium bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  🚀 Productivity Redefined
                </span>
              </div>

              <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-gray-900 mb-6 leading-tight">
                <span className="block">Transform Your Workflow</span>
                <span className="block bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent mt-2">
                  With Jira-Powered Tasks
                </span>
              </h1>

              <p className="text-xl sm:text-2xl text-gray-600 max-w-3xl mx-auto mb-10 leading-relaxed">
                The ultimate task management platform designed for modern teams who demand excellence.
                <span className="font-semibold text-gray-800"> Plan, track, and achieve more</span> with our intuitive Jira-inspired interface.
              </p>

              {/* Enhanced Search Interface */}
              <div className="w-full max-w-4xl mx-auto mb-16">
                <div className="relative group">
                  <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
                  <div className="relative bg-white/90 backdrop-blur-lg rounded-2xl shadow-xl border border-white/50">
                    <div className="flex items-center p-2">
                      <div className="flex-1 flex items-center pl-4">
                        <svg className="h-6 w-6 text-gray-400 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                        <input
                          id="global-search-input"
                          type="text"
                          placeholder="Search tasks, projects, teammates, or anything..."
                          className="w-full py-5 text-lg bg-transparent border-0 focus:outline-none focus:ring-0 placeholder-gray-500"
                        />
                      </div>
                      <div className="flex items-center pr-2">
                        <kbd className="px-3 py-2 text-sm font-semibold text-gray-500 bg-gray-100 border border-gray-300 rounded-lg shadow-inner">/</kbd>
                        <div className="mx-2 text-gray-300">•</div>
                        <kbd className="px-3 py-2 text-sm font-semibold text-gray-500 bg-gray-100 border border-gray-300 rounded-lg shadow-inner">ESC</kbd>
                      </div>
                    </div>

                    {/* Recent searches suggestions */}
                    <div className="border-t border-gray-100 px-6 py-4 bg-gray-50/50 rounded-b-2xl">
                      <div className="flex flex-wrap gap-3">
                        <span className="text-sm text-gray-600">Recent searches:</span>
                        <button className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200 transition-colors">urgent tasks</button>
                        <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm hover:bg-purple-200 transition-colors">bug fixes</button>
                        <button className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm hover:bg-green-200 transition-colors">sprint 3</button>
                        <button className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-sm hover:bg-yellow-200 transition-colors">john.doe</button>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-6 text-center">
                  <p className="text-gray-600 text-sm">Quick search tips: Press <kbd className="px-2 py-1 text-xs font-semibold text-gray-500 bg-gray-100 border border-gray-300 rounded">/</kbd> to focus search anytime</p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
                <a
                  href="/login"
                  className="px-10 py-5 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white font-bold rounded-2xl hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-110 shadow-2xl hover:shadow-3xl text-lg"
                >
                  Start Free Trial →
                </a>
                <a
                  href="#features"
                  className="px-10 py-5 border-2 border-gray-300 text-gray-700 font-bold rounded-2xl hover:border-blue-500 hover:text-blue-600 transition-all duration-300 transform hover:scale-105 text-lg"
                >
                  Explore Features
                </a>
              </div>
            </div>
          </div>

          {/* Animated Dashboard Preview */}
          <div className="mt-20 relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-3xl blur-3xl transform scale-150 rotate-12"></div>
            <div className="relative bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden">
              <div className="h-14 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200/50 flex items-center px-6 space-x-3">
                <div className="w-4 h-4 bg-red-400 rounded-full shadow-sm"></div>
                <div className="w-4 h-4 bg-yellow-400 rounded-full shadow-sm"></div>
                <div className="w-4 h-4 bg-green-400 rounded-full shadow-sm"></div>
              </div>
              <div className="p-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-2xl border-l-4 border-red-500 shadow-sm">
                    <div className="flex items-center mb-4">
                      <div className="w-3 h-3 bg-red-400 rounded-full mr-2"></div>
                      <span className="text-sm font-semibold text-red-700">To Do</span>
                    </div>
                    <div className="h-4 bg-red-200 rounded w-3/4 mb-3"></div>
                    <div className="h-3 bg-red-100 rounded w-1/2 mb-2"></div>
                    <div className="flex gap-2 mt-4">
                      <span className="px-2 py-1 bg-red-200 text-red-800 text-xs rounded-full">Bug</span>
                      <span className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded-full">Urgent</span>
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-6 rounded-2xl border-l-4 border-yellow-500 shadow-sm">
                    <div className="flex items-center mb-4">
                      <div className="w-3 h-3 bg-yellow-400 rounded-full mr-2"></div>
                      <span className="text-sm font-semibold text-yellow-700">In Progress</span>
                    </div>
                    <div className="h-4 bg-yellow-200 rounded w-3/4 mb-3"></div>
                    <div className="h-3 bg-yellow-100 rounded w-1/2 mb-2"></div>
                    <div className="flex gap-2 mt-4">
                      <span className="px-2 py-1 bg-yellow-200 text-yellow-800 text-xs rounded-full">Feature</span>
                      <span className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded-full">Dev</span>
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-2xl border-l-4 border-green-500 shadow-sm">
                    <div className="flex items-center mb-4">
                      <div className="w-3 h-3 bg-green-400 rounded-full mr-2"></div>
                      <span className="text-sm font-semibold text-green-700">Done</span>
                    </div>
                    <div className="h-4 bg-green-200 rounded w-3/4 mb-3"></div>
                    <div className="h-3 bg-green-100 rounded w-1/2 mb-2"></div>
                    <div className="flex gap-2 mt-4">
                      <span className="px-2 py-1 bg-green-200 text-green-800 text-xs rounded-full">Complete</span>
                      <span className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded-full">Review</span>
                    </div>
                  </div>
                </div>

                <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-white/60 p-4 rounded-xl border border-gray-200/50">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-medium text-gray-600">Progress</span>
                      <span className="text-sm font-bold text-blue-600">78%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div className="bg-gradient-to-r from-blue-500 to-indigo-500 h-3 rounded-full" style={{width: '78%'}}></div>
                    </div>
                  </div>
                  <div className="bg-white/60 p-4 rounded-xl border border-gray-200/50">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-medium text-gray-600">Team Activity</span>
                      <span className="text-sm font-bold text-green-600">Active</span>
                    </div>
                    <div className="flex space-x-1">
                      {[...Array(5)].map((_, i) => (
                        <div key={i} className="w-8 h-8 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-full border-2 border-white shadow-sm"></div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Search Capabilities Section */}
      <section id="search-capabilities" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-indigo-50/50 to-blue-50/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Powerful <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Search Capabilities</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Find exactly what you need with our advanced search and filtering system.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Search Results Preview */}
            <div className="bg-white/80 backdrop-blur-xl p-6 rounded-2xl border border-white/20 shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-8 h-8 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center mr-3">1</span>
                Smart Search
              </h3>
              <div className="space-y-3">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-gray-900">Fix login authentication bug</div>
                      <div className="text-sm text-gray-600">TASK-123 • High Priority</div>
                    </div>
                    <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">Bug</span>
                  </div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-gray-900">Implement user dashboard</div>
                      <div className="text-sm text-gray-600">TASK-456 • Medium Priority</div>
                    </div>
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Feature</span>
                  </div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-gray-900">Update documentation</div>
                      <div className="text-sm text-gray-600">TASK-789 • Low Priority</div>
                    </div>
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Docs</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Search Filters */}
            <div className="bg-white/80 backdrop-blur-xl p-6 rounded-2xl border border-white/20 shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-8 h-8 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center mr-3">2</span>
                Advanced Filters
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded cursor-pointer">
                  <span className="text-gray-700">Status: All</span>
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded cursor-pointer">
                  <span className="text-gray-700">Priority: All</span>
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded cursor-pointer">
                  <span className="text-gray-700">Assignee: Anyone</span>
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded cursor-pointer">
                  <span className="text-gray-700">Date Range: Anytime</span>
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white/80 backdrop-blur-xl p-6 rounded-2xl border border-white/20 shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <span className="w-8 h-8 bg-green-100 text-green-600 rounded-lg flex items-center justify-center mr-3">3</span>
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button className="w-full text-left p-3 hover:bg-blue-50 rounded-lg border border-blue-100 transition-colors">
                  <div className="font-medium text-blue-700">Create New Task</div>
                  <div className="text-sm text-blue-600">⌘ + T</div>
                </button>
                <button className="w-full text-left p-3 hover:bg-purple-50 rounded-lg border border-purple-100 transition-colors">
                  <div className="font-medium text-purple-700">Open Dashboard</div>
                  <div className="text-sm text-purple-600">⌘ + D</div>
                </button>
                <button className="w-full text-left p-3 hover:bg-green-50 rounded-lg border border-green-100 transition-colors">
                  <div className="font-medium text-green-700">View Reports</div>
                  <div className="text-sm text-green-600">⌘ + R</div>
                </button>
                <button className="w-full text-left p-3 hover:bg-yellow-50 rounded-lg border border-yellow-100 transition-colors">
                  <div className="font-medium text-yellow-700">Settings</div>
                  <div className="text-sm text-yellow-600">⌘ + ,</div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
              Powerful Features for <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Modern Teams</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to plan, track, and deliver exceptional results with ease.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {[
              {
                icon: "🎨",
                title: "Customizable Kanban Boards",
                description: "Create personalized workflows with drag-and-drop boards that adapt to your team's unique process."
              },
              {
                icon: "🔍",
                title: "Advanced Filtering & Search",
                description: "Quickly find what you need with powerful filters, search capabilities, and smart tags."
              },
              {
                icon: "⚡",
                title: "Real-time Collaboration",
                description: "Stay in sync with instant notifications, live updates, and seamless team coordination."
              },
              {
                icon: "🔒",
                title: "Enterprise Security",
                description: "Bank-level security with JWT authentication, encrypted data, and compliance features."
              },
              {
                icon: "🔄",
                title: "Smart Automation",
                description: "Automate repetitive tasks and streamline workflows with custom rules and triggers."
              },
              {
                icon: "📱",
                title: "Fully Responsive",
                description: "Access your tasks anywhere, anytime with our beautifully designed mobile experience."
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="group bg-white/80 backdrop-blur-xl p-8 rounded-3xl border border-white/20 hover:border-blue-200/50 transition-all duration-500 transform hover:-translate-y-2 shadow-lg hover:shadow-2xl"
              >
                <div className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300">{feature.icon}</div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors duration-300">{feature.title}</h3>
                <p className="text-gray-600 text-lg leading-relaxed">{feature.description}</p>
                <div className="mt-6 w-12 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Search Demo Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto text-center">
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              See Search in Action
            </h2>
            <p className="text-xl text-gray-600">
              Experience lightning-fast search across your entire project
            </p>
          </div>

          <div className="bg-gray-900 rounded-2xl p-6 text-left overflow-hidden">
            <div className="flex items-center space-x-2 mb-4 text-gray-300">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="ml-4 text-sm">Search Console</span>
            </div>

            <div className="font-mono text-green-400 mb-2">$ search "urgent bugs"</div>

            <div className="space-y-2 text-gray-200 text-sm">
              <div className="flex items-center">
                <span className="text-yellow-400 mr-3">›</span>
                <span>Finding all urgent bugs across 12,543 tasks...</span>
              </div>
              <div className="flex items-center">
                <span className="text-green-400 mr-3">✓</span>
                <span>Found 23 urgent bugs assigned to you</span>
              </div>
              <div className="flex items-center">
                <span className="text-blue-400 mr-3">•</span>
                <span className="text-gray-300">TASK-123: Fix login authentication - <span className="text-red-400">High Priority</span></span>
              </div>
              <div className="flex items-center">
                <span className="text-blue-400 mr-3">•</span>
                <span className="text-gray-300">TASK-456: Database connection timeout - <span className="text-red-400">Critical</span></span>
              </div>
              <div className="flex items-center">
                <span className="text-blue-400 mr-3">•</span>
                <span className="text-gray-300">TASK-789: Payment gateway error - <span className="text-red-400">High Priority</span></span>
              </div>
              <div className="flex items-center mt-4">
                <span className="text-cyan-400 mr-3">⚡</span>
                <span className="text-gray-300">Search completed in 0.04 seconds</span>
              </div>
            </div>
          </div>

          <div className="mt-8 flex justify-center space-x-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">0.04s</div>
              <div className="text-sm text-gray-600">Avg. Search Speed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">10K+</div>
              <div className="text-sm text-gray-600">Tasks Indexed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">99.9%</div>
              <div className="text-sm text-gray-600">Accuracy Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50/50 to-purple-50/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
              How It <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Works</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get started in minutes and boost your productivity immediately.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            {[
              {
                step: "01",
                title: "Sign Up & Customize",
                description: "Create your account and customize your workspace to match your team's unique workflow and preferences."
              },
              {
                step: "02",
                title: "Organize & Prioritize",
                description: "Create tasks, set priorities, define deadlines, and organize them in your personalized Kanban board."
              },
              {
                step: "03",
                title: "Collaborate & Achieve",
                description: "Work together in real-time, track progress, and achieve your goals faster with our intuitive tools."
              }
            ].map((step, index) => (
              <div
                key={index}
                className="text-center group"
              >
                <div className="relative mb-8">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full blur-xl scale-110 group-hover:scale-125 transition-transform duration-500"></div>
                  <div className="relative w-24 h-24 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto group-hover:scale-110 transition-transform duration-300 shadow-2xl">
                    {step.step}
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors duration-300">{step.title}</h3>
                <p className="text-gray-600 text-lg">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            {[
              { number: "10K+", label: "Active Users" },
              { number: "99.9%", label: "Uptime" },
              { number: "24/7", label: "Support" },
              { number: "150+", label: "Countries" }
            ].map((stat, index) => (
              <div key={index} className="group">
                <div className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2 group-hover:scale-110 transition-transform duration-300">
                  {stat.number}
                </div>
                <div className="text-gray-600 text-lg font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-28 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl sm:text-5xl font-bold text-white mb-6">
            Ready to Transform Your Workflow?
          </h2>
          <p className="text-xl text-blue-100 mb-10 max-w-2xl mx-auto">
            Join thousands of innovative teams already using our platform to achieve more with less effort.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
            <a
              href="/login"
              className="px-10 py-5 bg-white text-blue-600 font-bold rounded-2xl hover:bg-gray-50 transition-all duration-300 transform hover:scale-110 shadow-2xl hover:shadow-3xl text-lg"
            >
              Get Started Free
            </a>
            <a
              href="#features"
              className="px-10 py-5 border-2 border-white/30 text-white font-bold rounded-2xl hover:border-white hover:bg-white/10 transition-all duration-300 transform hover:scale-105 text-lg"
            >
              Learn More
            </a>
          </div>
          <p className="text-blue-200 mt-8 text-sm">
            No credit card required • 14-day free trial • Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            <div>
              <div className="flex items-center mb-6">
                <div className="h-10 w-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                  <span className="text-white font-bold text-xl">T</span>
                </div>
                <span className="ml-3 text-2xl font-bold">TodoJira</span>
              </div>
              <p className="text-gray-400 mb-6 leading-relaxed">
                Empowering teams to achieve more with intelligent task management and seamless collaboration tools.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-blue-600 transition-colors duration-300">
                  <span className="text-sm">f</span>
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-blue-400 transition-colors duration-300">
                  <span className="text-sm">t</span>
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-blue-700 transition-colors duration-300">
                  <span className="text-sm">in</span>
                </a>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-6 text-lg">Product</h4>
              <ul className="space-y-4 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors duration-200">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Integrations</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Roadmap</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-6 text-lg">Company</h4>
              <ul className="space-y-4 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors duration-200">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Contact</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-6 text-lg">Support</h4>
              <ul className="space-y-4 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors duration-200">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Community</a></li>
                <li><a href="#" className="hover:text-white transition-colors duration-200">Status</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              &copy; 2026 TodoJira. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">Privacy</a>
              <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">Terms</a>
              <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">Cookies</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}