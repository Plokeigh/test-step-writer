'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RCMConverter() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('');
  const router = useRouter();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setMessage('');
      setMessageType('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setMessage('Please select an RCM file to upload.');
      setMessageType('error');
      return;
    }

    // Only allow Excel files
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      setMessage('Only Excel files (.xlsx or .xls) are allowed.');
      setMessageType('error');
      return;
    }

    setIsUploading(true);
    setMessage('Processing your RCM file...');
    setMessageType('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Replace with your actual API endpoint for backend processing
      const response = await fetch('/api/rcm-converter/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to process the RCM file.');
      }

      const result = await response.json();
      
      // Handle successful response
      setMessage('RCM file processed successfully! Downloading high-level view...');
      setMessageType('success');
      
      // Trigger file download - this would be implemented in the backend
      window.location.href = `/api/rcm-converter/download/${result.fileId}`;
      
    } catch (error) {
      console.error('Error:', error);
      setMessage('An error occurred while processing the file. Please try again.');
      setMessageType('error');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            RCM High-Level View Conversion Tool
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Convert a detailed Risk Control Matrix (RCM) into a high-level view by extracting control information and mapping it to a template.
          </p>
        </div>

        {/* Process Steps */}
        <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-8">
          <div className="px-4 py-5 sm:px-6">
            <h2 className="text-xl font-medium text-gray-900">Process Steps</h2>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              How the RCM conversion works
            </p>
          </div>
          <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
            <ol className="list-decimal pl-5 space-y-3">
              <li className="text-gray-700">
                <span className="font-medium">Input:</span> Upload an RCM document to the tool.
              </li>
              <li className="text-gray-700">
                <span className="font-medium">Data Extraction:</span> Tool scans the RCM for two key columns: "Control ID" and "Gap Status".
              </li>
              <li className="text-gray-700">
                <span className="font-medium">System Name Extraction:</span> Extract all unique system/application names from the Control ID column. Control IDs follow the format: "[Control-Code]-[System]" (e.g., "APD-01-Azure").
              </li>
              <li className="text-gray-700">
                <span className="font-medium">Control Mapping:</span> For each unique system, map against each control listed in column A of the template.
              </li>
              <li className="text-gray-700">
                <span className="font-medium">Status Visualization:</span> Apply conditional formatting based on Gap Status:
                <ul className="list-disc pl-5 mt-2 space-y-1">
                  <li><span className="text-red-600 font-medium">"Gap":</span> Highlight the corresponding cell RED</li>
                  <li><span className="text-green-600 font-medium">"No Gap":</span> Highlight the corresponding cell GREEN</li>
                  <li><span className="text-yellow-600 font-medium">"Informal Process":</span> Highlight the corresponding cell YELLOW</li>
                  <li><span className="text-gray-600 font-medium">Missing control:</span> Highlight the corresponding cell GREY</li>
                </ul>
              </li>
              <li className="text-gray-700">
                <span className="font-medium">Output:</span> Generate the finalized RCM control view template with all mappings and formatting applied.
              </li>
            </ol>
          </div>
        </div>

        {/* File Upload Form - Simplified */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700">
                Upload Excel File
              </label>
              <input
                id="file-upload"
                name="file-upload"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500
                         file:mr-4 file:py-2 file:px-4
                         file:rounded-md file:border-0
                         file:text-sm file:font-semibold
                         file:bg-teal-50 file:text-teal-700
                         hover:file:bg-teal-100"
              />
              <p className="mt-1 text-sm text-gray-500">
                Excel files only (.xlsx, .xls)
              </p>
            </div>

            <button
              type="submit"
              disabled={isUploading || !file}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50"
            >
              {isUploading ? 'Processing...' : 'Convert RCM'}
            </button>
          </form>
          
          {/* Status Messages */}
          {message && (
            <div 
              className={`mt-4 p-4 rounded ${
                messageType === 'success' 
                  ? 'bg-green-50 text-green-800' 
                  : messageType === 'error' 
                  ? 'bg-red-50 text-red-800' 
                  : 'bg-blue-50 text-blue-800'
              }`}
            >
              {message}
            </div>
          )}
          
          {file && (
            <div className="mt-4 text-sm text-gray-600">
              Selected file: <span className="font-medium">{file.name}</span> ({(file.size / 1024).toFixed(2)} KB)
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 