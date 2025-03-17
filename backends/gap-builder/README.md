# Gap Builder

A tool for generating ITGC gaps and recommendations based on control templates using Azure OpenAI API.

## Overview

Gap Builder is a tool that helps IT auditors create standardized gap descriptions and recommendations for IT General Controls (ITGC). The tool:

1. Takes an Excel template with control information including Control ID, Control Name, Control Description, Application, Current Process, and Gap Status.
2. Uses Azure OpenAI API to analyze each control with a gap status and generates:
   - Gap Title: A brief summary of the gap
   - Gap Description: A detailed explanation of the gap
   - Recommendation: Actionable steps to remediate the gap
3. Outputs a filled Excel document with the generated content

## Prerequisites

- Python 3.10+
- Azure OpenAI API access with a deployed model
- Excel template file with required columns

## Setup

1. Clone the repository or download the code
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install python-dotenv flask flask-cors openpyxl openai==0.28
   ```
4. Copy the `.env.template` file to `.env` and update with your Azure OpenAI API settings:
   ```
   cp .env.template .env
   ```
5. Edit the `.env` file with your actual API credentials:
   ```
   OPENAI_API_TYPE=azure
   OPENAI_API_BASE=https://your-azure-openai-resource.openai.azure.com/
   OPENAI_API_VERSION=2023-05-15
   OPENAI_API_KEY=your-api-key-here
   AZURE_DEPLOYMENT_NAME=your-deployment-name
   ```

## Running the Tool

### Using the Batch File (Windows)

1. Edit the `start_server.bat` file if necessary to set the correct Python path
2. Double-click the `start_server.bat` file to run the server

### Manual Start

1. Activate your virtual environment (if using one)
2. Run the Flask app:
   ```
   python app.py
   ```
3. Open a web browser and navigate to `http://localhost:5002`

## Using the Tool

1. Prepare your Excel template with the following columns:
   - Control ID
   - Control Name
   - Control Description
   - Application
   - Current Process
   - Gap Status (must be one of: Not Implemented, Partially Implemented, Improvement Needed)
   - Gap Title (will be filled by the tool)
   - Gap Description (will be filled by the tool)
   - Recommendation (will be filled by the tool)
   
2. Upload the template through the web interface
3. The tool will process each row with a Gap Status and generate content
4. Download the processed Excel file with the generated gaps and recommendations

## How It Works

1. The tool ingests your Excel template
2. For each control with a Gap Status, it:
   - References the gap_definitions.py file which contains example gaps and recommendations
   - Finds relevant examples based on the Control ID and Gap Status
   - Uses Azure OpenAI API to generate customized gap content
   - Updates the template with the generated content
3. The tool returns the completed Excel file with all gaps and recommendations filled out

## Customizing Gap Definitions

You can customize the example gaps and recommendations by editing the `models/gap_definitions.py` file. Adding more examples will improve the quality of the generated content. 