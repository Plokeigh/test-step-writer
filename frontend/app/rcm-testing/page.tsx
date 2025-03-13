'use client';

import React, { useState } from 'react';

export default function RCMTesting() {
  const [status, setStatus] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownloadTemplate = async () => {
    setIsDownloading(true);
    try {
      const response = await fetch('http://localhost:3003/api/download-template');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'ITGC Testing Upload Template.xlsx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      setStatus('Template downloaded successfully!');
      setTimeout(() => setStatus(''), 5000);
    } catch (error) {
      console.error('Error:', error);
      setStatus(`Error downloading template: ${error instanceof Error ? error.message : 'Unknown error occurred'}`);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    if (!formData.get('file')) {
      alert('Please select an RCM template file');
      return;
    }

    setIsProcessing(true);
    setStatus('Processing...');

    try {
      const response = await fetch('http://localhost:3003/api/generate-testing', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      
      // Get filename from Content-Disposition header if available
      const contentDisposition = response.headers.get('Content-Disposition');
      const filenameMatch = contentDisposition && contentDisposition.match(/filename="(.+)"/);
      const filename = filenameMatch ? filenameMatch[1] : 'testing_templates.zip';
      
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setStatus('Testing templates generated and downloaded successfully!');
      setTimeout(() => setStatus(''), 5000);
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">RCM Testing Generator</h1>
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-6 text-gray-700">
            <h2 className="text-xl font-semibold mb-3">Tool Description</h2>
            <p className="mb-3">This tool generates testing templates from your RCM file:</p>
            <ol className="list-decimal list-inside space-y-2 ml-4">
              <li>Download the ITGC Testing Upload Template below</li>
              <li>Fill out the template with your RCM data</li>
              <li>Upload your completed RCM template Excel file</li>
              <li>The tool creates one folder for each unique control ID found in Column A</li>
              <li>All folders are placed in a "Testing" zip folder</li>
              <li>An Excel testing template is created for each control with key information from the RCM</li>
              <li>Files are named as [Fiscal Year]-[Control ID]-[Testing Period]</li>
            </ol>
          </div>
          
          <div className="mb-6">
            <button
              onClick={handleDownloadTemplate}
              disabled={isDownloading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
            >
              {isDownloading ? 'Downloading...' : 'Download ITGC Testing Upload Template'}
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                Upload Completed RCM Template Excel File
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
                         file:bg-blue-50 file:text-blue-700
                         hover:file:bg-blue-100"
              />
              <p className="text-xs text-gray-500 mt-1">
                Only Excel files (.xlsx, .xls) are accepted
              </p>
            </div>

            <button
              type="submit"
              disabled={isProcessing}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
            >
              {isProcessing ? 'Processing...' : 'Generate Testing Templates'}
            </button>
          </form>

          {status && (
            <div 
              className={`mt-4 p-3 rounded-md ${
                status.includes('Error') 
                  ? 'bg-red-50 text-red-700' 
                  : 'bg-green-50 text-green-700'
              }`}
            >
              {status}
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 