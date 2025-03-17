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
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Generate ITGC Gap Analysis</h2>
          <p className="text-gray-600 mb-6">
            Upload your IT General Controls (ITGC) assessment template and this tool will automatically
            generate gap descriptions and recommendations based on the control status.
          </p>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                Upload Excel Template
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
        
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">How It Works</h2>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="flex-shrink-0 bg-red-100 rounded-full p-2">
                <span className="text-red-600 text-xl">1</span>
              </div>
              <div className="ml-4">
                <h3 className="font-medium text-gray-900">Upload your template</h3>
                <p className="text-gray-600">Upload your Excel template with control assessment information.</p>
              </div>
            </div>
            
            <div className="flex items-start">
              <div className="flex-shrink-0 bg-red-100 rounded-full p-2">
                <span className="text-red-600 text-xl">2</span>
              </div>
              <div className="ml-4">
                <h3 className="font-medium text-gray-900">AI Gap Analysis</h3>
                <p className="text-gray-600">Our AI analyzes your controls and generates tailored gap descriptions.</p>
              </div>
            </div>
            
            <div className="flex items-start">
              <div className="flex-shrink-0 bg-red-100 rounded-full p-2">
                <span className="text-red-600 text-xl">3</span>
              </div>
              <div className="ml-4">
                <h3 className="font-medium text-gray-900">Download Results</h3>
                <p className="text-gray-600">Receive your enhanced Excel file with gap titles, descriptions, and recommendations.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 