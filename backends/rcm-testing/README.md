# RCM Testing Generator

This tool processes RCM (Risk Control Matrix) templates and generates testing templates for each unique control ID.

## Features

- Processes Excel RCM templates (.xlsx, .xls)
- Extracts control IDs from Column A
- Creates a folder structure with one folder per control ID
- Generates Excel testing templates for each control with:
  - Named format: [Fiscal Year]-[Control ID]-[Testing Period]
  - Summary tab populated with data from the RCM template
  - Test Steps tab for documenting test procedure results
- Compresses all folders and files into a downloadable zip file

## How It Works

1. User uploads an RCM template Excel file
2. The tool processes the file and extracts key information:
   - Control IDs from Column A
   - Fiscal Year from Column B
   - Testing Period from Column C 
   - Business Cycle from Column D
   - Sub Process from Column E
   - Control Description from Column H
   - Application from Column F
3. For each unique control ID, the tool creates:
   - A folder named with the Control ID
   - An Excel testing template file with the Summary tab pre-populated
4. All folders are placed in a "Testing" folder which is compressed into a zip file
5. The zip file is automatically downloaded to the user's computer

## Running the Application

1. Run the start-server.bat file to start the Flask backend
2. The server will run on port 3003

## Requirements

- Python 3.8 or higher
- Flask
- Flask-CORS
- OpenPyXL
- Other dependencies will be installed automatically by the start-server.bat script 