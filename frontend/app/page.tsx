'use client';

import React from 'react';
import Link from 'next/link';

export default function Home() {
  const tools = [
    {
      name: 'Resources',
      description: 'Access useful templates, documents, and resources to help streamline your work. Download and use these materials to enhance your productivity.',
      path: '/resources',
      icon: '📚',
      color: 'from-orange-500 to-orange-600'
    },
    {
      name: 'Step Writer',
      description: 'Upload an Excel file with SOX control information (ID, Title, Description, Testing Attributes, Evidence) and generate structured test steps and attributes formatted for GRC tool upload.',
      path: '/step-writer',
      icon: '📝',
      color: 'from-purple-500 to-purple-600'
    },
  ];

  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center animate-fade-in">
            <h1 className="text-5xl font-bold text-gray-900 sm:text-6xl md:text-7xl mb-8">
              Welcome to{' '}
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                SOX Testing Hub
              </span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-xl text-gray-600 sm:text-2xl md:mt-5 md:max-w-3xl">
              Your comprehensive platform for SOX compliance testing, test step creation, and control validation.
            </p>
          </div>
        </div>
      </div>

      {/* Tools Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {tools.map((tool) => (
            <div
              key={tool.name}
              className="animate-fade-in lg:col-span-1"
            >
              <Link
                href={tool.path}
                className="card group block h-full"
              >
                <div className={`p-8 bg-gradient-to-r ${tool.color} rounded-t-xl`}>
                  <div className="text-5xl mb-4 transform group-hover:scale-110 transition-transform duration-200">
                    {tool.icon}
                  </div>
                </div>
                <div className="p-8">
                  <h3 className="text-2xl font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-200">
                    {tool.name}
                  </h3>
                  <p className="mt-4 text-gray-600 text-lg leading-relaxed">
                    {tool.description}
                  </p>
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
} 