'use client';

import React, { useState } from 'react';
import Link from 'next/link';

export default function StepWriter() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
    }
  };

  const removeFile = () => {
    setUploadedFile(null);
  };

  const generateTestSteps = async () => {
    if (!uploadedFile) {
      alert('Please upload an Excel file first');
      return;
    }

    setIsProcessing(true);

    try {
      const formData = new FormData();
      formData.append('files', uploadedFile);

      const response = await fetch('http://localhost:3002/generate-test-steps', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // The response should be the Excel file for download
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'SOX_Test_Steps_Template.xlsx';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      // Clear the uploaded file after successful processing
      setUploadedFile(null);
      
    } catch (error) {
      console.error('Error generating test steps:', error);
      alert('Error generating test steps. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/" className="text-blue-600 hover:text-blue-800 mb-4 inline-flex items-center">
            ← Back to Hub
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">SOX Step Writer</h1>
          <p className="text-xl text-gray-600">
            Upload an Excel file with SOX control information and generate structured test steps and attributes formatted for GRC tool upload.
          </p>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <h2 className="text-lg font-semibold text-blue-900 mb-3">📋 Instructions</h2>
          <div className="text-sm text-blue-800 space-y-2">
            <p><strong>Expected Excel Format:</strong></p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li><strong>Column A:</strong> Ref ID (Control ID, e.g., ACT-AHA-01)</li>
              <li><strong>Column B:</strong> Control Description</li>
              <li><strong>Column C:</strong> Testing Attributes</li>
              <li><strong>Column D:</strong> Design Attributes</li>
              <li><strong>Column E:</strong> Evidence of Control</li>
            </ul>
            <p className="mt-3"><strong>Output:</strong> Excel template with generated test steps ready for GRC tool upload.</p>
          </div>
        </div>

        {/* File Upload Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Upload SOX Controls Excel File</h2>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <div className="text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <div className="mt-4">
                <label htmlFor="file-upload" className="cursor-pointer">
                  <span className="mt-2 block text-sm font-medium text-gray-900">
                    {uploadedFile ? uploadedFile.name : 'Upload Excel file with SOX controls'}
                  </span>
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    className="sr-only"
                    accept=".xlsx,.xls"
                    onChange={handleFileUpload}
                  />
                </label>
                <p className="mt-2 text-xs text-gray-500">
                  Supported formats: Excel (.xlsx, .xls)
                </p>
              </div>
            </div>
          </div>

          {/* Uploaded File Display */}
          {uploadedFile && (
            <div className="mt-4">
              <div className="flex items-center justify-between bg-gray-50 p-3 rounded">
                <div className="flex items-center">
                  <span className="text-green-500 mr-2">📄</span>
                  <span className="text-sm text-gray-700">{uploadedFile.name}</span>
                  <span className="text-xs text-gray-500 ml-2">
                    ({(uploadedFile.size / 1024).toFixed(1)} KB)
                  </span>
                </div>
                <button
                  onClick={removeFile}
                  className="text-red-500 hover:text-red-700 text-sm"
                >
                  Remove
                </button>
              </div>
            </div>
          )}

          {/* Generate Button */}
          {uploadedFile && (
            <div className="mt-6">
              <button
                onClick={generateTestSteps}
                disabled={isProcessing}
                className="w-full bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-lg font-medium"
              >
                {isProcessing ? (
                  <>
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Processing Controls...</span>
                  </>
                ) : (
                  <>
                    <span>⚡</span>
                    <span>Generate Test Steps Template</span>
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Process Overview */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <span className="text-purple-600 text-xl">1</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Upload Excel</h3>
              <p className="text-sm text-gray-600">Upload your Excel file with SOX control information in the specified format.</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <span className="text-purple-600 text-xl">2</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">AI Processing</h3>
              <p className="text-sm text-gray-600">AI analyzes each control and generates detailed test steps and attributes.</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                <span className="text-purple-600 text-xl">3</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Download Template</h3>
              <p className="text-sm text-gray-600">Receive a formatted Excel template ready for upload to your GRC tool.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 