'use client';

import React, { useState } from 'react';

export default function GapBuilder() {
  const [status, setStatus] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    if (!formData.get('file')) {
      alert('Please select a file');
      return;
    }

    setIsProcessing(true);
    setStatus('Processing...');

    try {
      // Point to the backend API endpoint for the Gap Builder
      const response = await fetch('http://localhost:5002/api/generate-gaps', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'itgc_gaps_recommendations.xlsx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setStatus('Gap analysis generated successfully!');
      setTimeout(() => setStatus(''), 3000);
    } catch (error) {
      console.error('Error:', error);
      setStatus(`Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Gap Builder</h1>
        
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">How to Use</h2>
          <div className="space-y-4 text-gray-600">
            <ol className="list-decimal list-inside space-y-2">
              <li>Upload the finalized RCM Builder document into the Gap Builder tool by clicking on the "Choose File". Be sure to not add any rows or modify the header names in the RCM as this will prevent the tool from working.</li>
              <li>Click the "Generate Gap Analysis" button to start processing the RCM.</li>
              <li>After a short period of time a version of the RCM you uploaded with updated gap-related columns will automatically download.</li>
              <li>Review columns K-M for accuracy and make updates as appropriate.</li>
            </ol>
            <p className="font-medium text-gray-900 mt-4">Congratulations you have succesfully completed your AI IT SOX Diagnostics journey and your delverables are ready to submit to the client!</p>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                Upload Excel File
              </label>
              <input
                type="file"
                id="file"
                name="file"
                accept=".xlsx,.xls"
                className="block w-full text-sm text-gray-500
                         file:mr-4 file:py-2 file:px-4
                         file:rounded-md file:border-0
                         file:text-sm file:font-semibold
                         file:bg-red-50 file:text-red-700
                         hover:file:bg-red-100"
              />
              <p className="mt-1 text-sm text-gray-500">
                The template must include the following columns: Control ID, Control Name, Control Description, 
                Application, Current Process, Gap Status, Gap Title, Gap Description, Recommendation
              </p>
            </div>

            <button
              type="submit"
              disabled={isProcessing}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              {isProcessing ? 'Processing...' : 'Generate Gap Analysis'}
            </button>
          </form>

          {status && (
            <div className={`mt-4 text-sm ${status.includes('Error') ? 'text-red-600' : 'text-green-600'}`}>
              {status}
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 