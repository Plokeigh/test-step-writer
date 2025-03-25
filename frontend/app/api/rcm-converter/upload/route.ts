import { NextRequest, NextResponse } from 'next/server';
import { writeFile, mkdir } from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file uploaded' },
        { status: 400 }
      );
    }

    // Check if it's an Excel file
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      return NextResponse.json(
        { error: 'Only Excel files (.xlsx or .xls) are allowed' },
        { status: 400 }
      );
    }

    const buffer = await file.arrayBuffer();
    const filename = file.name;

    // Create a unique ID using timestamp
    const timestamp = Date.now();
    const fileId = `${timestamp}-${Math.floor(Math.random() * 1000)}`;
    
    // Create uploads directory if it doesn't exist
    const uploadDir = path.join(process.cwd(), 'uploads');
    await mkdir(uploadDir, { recursive: true });
    
    // Save the file to the uploads directory
    const filePath = path.join(uploadDir, `${fileId}-${filename}`);
    await writeFile(filePath, new Uint8Array(buffer));

    // Call the Python backend to process the file
    try {
      // Path to the backend run.bat file
      const backendPath = path.join(process.cwd(), '..', 'backends', 'rcm-converter', 'run.bat');
      
      // Execute the backend script
      execSync(`"${backendPath}" "${filePath}"`, { 
        stdio: 'pipe',
        windowsHide: true
      });
      
      // The output file will be in the same directory with a new name
      const outputDir = path.dirname(filePath);
      const outputFile = path.join(outputDir, 'RCM-High-Level-View.xlsx');
      
      return NextResponse.json({
        message: 'File processed successfully',
        fileId,
        originalName: filename
      });
    } catch (error) {
      console.error('Error calling Python backend:', error);
      return NextResponse.json(
        { error: 'Failed to process file with backend' },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('Error handling file upload:', error);
    return NextResponse.json(
      { error: 'Failed to process file' },
      { status: 500 }
    );
  }
} 