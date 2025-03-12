import React from 'react';
import FileUploadComponent from './components/FileUploadComponent';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Meeting Transcript Processor</h1>
        <FileUploadComponent />
      </div>
    </div>
  );
}

export default App;