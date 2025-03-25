import { NextRequest, NextResponse } from 'next/server';
import { readFile, readdir } from 'fs/promises';
import path from 'path';
import { existsSync } from 'fs';

export async function GET(
  request: NextRequest,
  { params }: { params: { fileId: string } }
) {
  try {
    const fileId = params.fileId;
    if (!fileId) {
      return NextResponse.json(
        { error: 'No file ID provided' },
        { status: 400 }
      );
    }

    // Find the file by ID prefix in the uploads directory
    const uploadDir = path.join(process.cwd(), 'uploads');
    const files = await readdir(uploadDir);
    
    // Find the file that starts with the fileId
    const matchingFile = files.find(file => file.startsWith(fileId));
    
    if (!matchingFile) {
      return NextResponse.json(
        { error: 'File not found' },
        { status: 404 }
      );
    }

    // Look for the processed output file in the uploads directory
    const outputFilePath = path.join(uploadDir, 'RCM-High-Level-View.xlsx');
    
    // If the processed file doesn't exist, try to use the template as a fallback
    if (!existsSync(outputFilePath)) {
      // Try different possible template paths
      const possiblePaths = [
        path.join(process.cwd(), 'backends', 'rcm-converter', 'templates', 'rcm-control-view.xlsx'),
        path.join(process.cwd(), '..', 'backends', 'rcm-converter', 'templates', 'rcm-control-view.xlsx'),
        path.join(process.cwd(), '..', '..', 'backends', 'rcm-converter', 'templates', 'rcm-control-view.xlsx')
      ];
      
      let templatePath = null;
      for (const p of possiblePaths) {
        if (existsSync(p)) {
          templatePath = p;
          break;
        }
      }
      
      if (!templatePath) {
        console.error('Neither processed file nor template found');
        return NextResponse.json(
          { error: 'Processed file not found. Please try uploading again.' },
          { status: 404 }
        );
      }
      
      try {
        const fileBuffer = await readFile(templatePath);
        
        // Set up headers for Excel file download
        const headers = new Headers();
        headers.set('Content-Disposition', `attachment; filename="RCM-High-Level-View.xlsx"`);
        headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        
        return new NextResponse(fileBuffer, {
          status: 200,
          headers,
        });
      } catch (error) {
        console.error('Error reading template file:', error);
        return NextResponse.json(
          { error: 'Template file could not be read' },
          { status: 500 }
        );
      }
    }
    
    // Return the processed file
    try {
      const fileBuffer = await readFile(outputFilePath);
      
      // Set up headers for Excel file download
      const headers = new Headers();
      headers.set('Content-Disposition', `attachment; filename="RCM-High-Level-View.xlsx"`);
      headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
      
      return new NextResponse(fileBuffer, {
        status: 200,
        headers,
      });
    } catch (error) {
      console.error('Error reading processed file:', error);
      return NextResponse.json(
        { error: 'Processed file could not be read' },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('Error during file download:', error);
    return NextResponse.json(
      { error: 'Failed to process download request' },
      { status: 500 }
    );
  }
} 