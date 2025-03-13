'use client';

import React from 'react';

export default function Resources() {
  return (
    <main className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Resources</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Access useful templates, documents, and resources to help streamline your work. 
            Download and use these materials to enhance your productivity.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">ITGC Walkthrough Agenda</h2>
          <p className="text-gray-600 mb-6">
            A comprehensive template for conducting ITGC walkthroughs. This agenda helps ensure 
            all necessary topics are covered during your walkthrough sessions.
          </p>
          <button
            onClick={() => window.location.href = '/resources/itgc-walkthrough-agenda.docx'}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors duration-200 font-medium"
          >
            Download ITGC Walkthrough Agenda
          </button>
        </div>
      </div>
    </main>
  );
} 