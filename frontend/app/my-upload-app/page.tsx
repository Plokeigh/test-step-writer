'use client';

import React, { useState } from 'react';

export default function UploadApp() {
  const [status, setStatus] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isClearing, setIsClearing] = useState(false);

  const handleClearTemplate = async () => {
    setIsClearing(true);
    setStatus('Clearing template...');

    try {
      const response = await fetch('http://localhost:3002/clear-template', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      setStatus('Template cleared successfully!');
      setTimeout(() => setStatus(''), 3000);
    } catch (error) {
      console.error('Error:', error);
      setStatus(`Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`);
    } finally {
      setIsClearing(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fileInput = e.currentTarget.querySelector('input[type="file"]') as HTMLInputElement;
    
    if (!fileInput?.files?.[0]) {
      alert('Please select a file');
      return;
    }

    setIsProcessing(true);
    setStatus('Processing...');

    try {
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      const response = await fetch('http://localhost:3002/upload', {
        method: 'POST',
        headers: {
          'Accept': 'application/json, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        },
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          console.error('Error parsing error response:', e);
        }
        throw new Error(errorMessage);
      }

      // Check if we received an Excel file
      const contentType = response.headers.get('Content-Type');
      if (contentType?.includes('spreadsheet')) {
        // Handle Excel file download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
        const filename = filenameMatch ? filenameMatch[1] : 'Scoping Document - Updated.xlsx';
        
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setStatus('File processed and downloaded successfully!');
      } else {
        // Handle JSON response
        const result = await response.json();
        setStatus(result.message || 'File processed successfully!');
      }

      // Clear the file input
      fileInput.value = '';
      
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Scoping Doc Builder</h1>
        
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">How to Use</h2>
          <div className="space-y-4 text-gray-600">
            <p className="font-medium text-gray-900">Before you begin:</p>
            <ol className="list-decimal list-inside space-y-2">
              <li>Save your meeting transcript as a Word document (.docx file)</li>
              <li>Make sure your transcript is clear and well-formatted for best results</li>
            </ol>

            <p className="font-medium text-gray-900 mt-4">Processing your transcript:</p>
            <ol className="list-decimal list-inside space-y-2">
              <li>Click the "Upload File" button and select your meeting transcript</li>
              <li>Wait for the processing to complete - this may take a few moments</li>
              <li>Your processed Scoping Document will automatically download</li>
              <li>Repeat these steps for each meeting transcript you want to process</li>
            </ol>

            <p className="font-medium text-gray-900 mt-4">When you're finished:</p>
            <ol className="list-decimal list-inside space-y-2">
              <li>Click the "Clear Template" button to reset the template for future use</li>
              <li>This will remove all processed data while keeping the template structure intact</li>
            </ol>
            
            <p className="font-bold text-red-600 mt-6 border border-red-200 p-4 bg-red-50 rounded-md">
              <span className="underline">Disclaimer:</span> The content generated by this tool utilizes an AI model that, while highly accurate, may occasionally produce errors or inaccuracies. It is essential that you thoroughly review and verify all outputs before use. Documents generated by this tool are intended solely as drafts or guides and should NEVER be considered finalized or submitted directly to clients without careful prior review.
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                Upload Word Document (.docx)
              </label>
              <input
                type="file"
                id="file"
                name="file"
                accept=".docx"
                className="block w-full text-sm text-gray-500
                         file:mr-4 file:py-2 file:px-4
                         file:rounded-md file:border-0
                         file:text-sm file:font-semibold
                         file:bg-blue-50 file:text-blue-700
                         hover:file:bg-blue-100"
              />
              <p className="text-xs text-gray-500 mt-1">
                Only .docx files are accepted
              </p>
            </div>

            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={isProcessing}
                className="flex-1 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {isProcessing ? 'Processing...' : 'Upload File'}
              </button>

              <button
                type="button"
                onClick={handleClearTemplate}
                disabled={isClearing}
                className="flex-1 flex justify-center py-2 px-4 border border-red-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
              >
                {isClearing ? 'Clearing...' : 'Clear Template'}
              </button>
            </div>
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