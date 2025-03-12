import { useState, useEffect } from 'react';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [serverStatus, setServerStatus] = useState('Checking...');
    const [uploadProgress, setUploadProgress] = useState('');

    useEffect(() => {
        checkServerStatus();
    }, []);

    const checkServerStatus = async () => {
        try {
            const response = await fetch('http://localhost:5000/health');
            const data = await response.json();
            console.log('Server health check response:', data);
            setServerStatus(data.status === 'healthy' ? 'Server is healthy' : 'Server is not responding');
        } catch (error) {
            console.error('Server health check error:', error);
            setServerStatus('Server is not responding');
        }
    };

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        console.log('Selected file:', selectedFile);
        setFile(selectedFile);
        setMessage('');
        setUploadProgress('');
    };

    const handleClearTemplate = async () => {
        try {
            const response = await fetch('http://localhost:5000/clear-template', {
                method: 'POST',
            });
            const data = await response.json();
            if (response.ok) {
                setMessage('Template cleared successfully!');
            } else {
                setMessage(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Clear template error:', error);
            setMessage(`Error: ${error.message}`);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage('Please select a file first');
            return;
        }

        setLoading(true);
        setUploadProgress('Starting upload...');
        console.log('Upload started with file:', file.name, 'size:', file.size, 'type:', file.type);
        
        const formData = new FormData();
        console.log('FormData created');
        formData.append('file', file);

        try {
            console.log('Sending request to server...');
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                },
            });
            console.log('Received response:', response.status);

            if (response.ok) {
                setUploadProgress('Processing response...');
                const contentType = response.headers.get('content-type');
                console.log('Response content type:', contentType);

                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    console.log('JSON response:', data);
                    setMessage(data.message || 'File processed successfully!');
                } else {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = "Scoping Document - Updated.xlsx";
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    setMessage('File processed and downloaded successfully!');
                }
            } else {
                const errorText = await response.text();
                console.error('Upload error response:', errorText);
                try {
                    const errorJson = JSON.parse(errorText);
                    setMessage(`Error: ${errorJson.error}`);
                } catch {
                    setMessage(`Error: ${errorText}`);
                }
            }
        } catch (error) {
            console.error('Upload error:', error);
            setMessage(`Error: ${error.message}`);
        } finally {
            setLoading(false);
            setUploadProgress('');
        }
    };

    return (
        <div className="p-6 max-w-2xl mx-auto bg-white rounded-xl shadow-md">            
            <div className="bg-gray-50 p-4 rounded mb-4">
                <div className="font-medium">Server Status:</div>
                <div className={serverStatus.includes('healthy') ? 'text-green-500' : 'text-red-500'}>
                    {serverStatus}
                </div>
            </div>

            <div className="flex items-center gap-2 mb-4">
                <label className="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600 transition-colors">
                    Choose File
                    <input
                        type="file"
                        onChange={handleFileChange}
                        accept=".docx"
                        className="hidden"
                    />
                </label>
                <span className="text-gray-500">
                    {file ? file.name : 'No file chosen'}
                </span>
            </div>

            <div className="space-y-2">
                <button
                    onClick={handleUpload}
                    disabled={loading}
                    className="w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    {loading ? 'Processing...' : 'Upload File'}
                </button>

                <button 
                    onClick={handleClearTemplate}
                    disabled={loading}
                    className="w-full bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    Clear Template
                </button>
            </div>

            {uploadProgress && (
                <div className="mt-2 text-sm text-gray-600">
                    {uploadProgress}
                </div>
            )}

            {message && (
                <div className="mt-4 p-4 rounded bg-gray-50">
                    <div className="font-medium">Status:</div>
                    <div className={message.includes('Error') ? 'text-red-500' : 'text-green-500'}>
                        {message}
                    </div>
                </div>
            )}
        </div>
    );
};

export default FileUpload;