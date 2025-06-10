# SOX Test Step Writer

An AI-powered tool for generating detailed test steps and test attributes for SOX (Sarbanes-Oxley) compliance controls.

## Overview

This application helps auditors and compliance professionals automatically generate comprehensive test steps and test attributes from SOX control descriptions. It uses Azure OpenAI to intelligently transform control information into actionable testing procedures.

## Features

### 🤖 AI-Powered Generation
- **Smart Test Step Creation**: Automatically generates detailed test steps from control descriptions
- **Attribute Generation**: Creates meaningful test attributes with past-tense validation descriptions
- **N/A Scenario Handling**: Intelligently extrapolates test steps when only control descriptions are available
- **Evidence Specification**: Automatically identifies and lists required evidence for each control

### 📊 Excel Integration
- **Excel Input Processing**: Reads SOX control information from Excel files
- **Template Generation**: Creates formatted Excel templates with generated test steps
- **Standardized Output**: Produces consistent, professional test step documentation

### 🎯 Intelligent Processing
- **Creative Extrapolation**: For controls with limited information, the AI creatively determines logical test steps based on control descriptions
- **Control Type Recognition**: Identifies different types of controls (reviews, reconciliations, authorizations, monitoring)
- **Evidence Mapping**: Maps control activities to appropriate evidence types

## Project Structure

```
test-step-writer/
├── frontend/                 # Next.js frontend application
│   ├── app/
│   │   └── step-writer/     # SOX test step writer interface
│   └── components/          # Reusable UI components
├── backends/
│   └── upload-app/          # Python Flask backend
│       ├── app.py          # Main Flask application
│       └── sox_processor.py # Core SOX processing logic
└── README.md
```

## Technology Stack

- **Frontend**: Next.js, React, TypeScript
- **Backend**: Python Flask
- **AI**: Azure OpenAI (GPT-4)
- **File Processing**: pandas, openpyxl for Excel handling
- **Document Generation**: python-docx, Excel template creation

## Key Components

### SOX Processor (`sox_processor.py`)
The core engine that:
- Parses Excel files containing SOX control information
- Generates AI-powered test steps and attributes
- Creates formatted Excel templates for auditing workflows
- Handles both complete control information and N/A scenarios

### Frontend Interface
- Modern, intuitive interface for uploading SOX control files
- Real-time processing status and progress tracking
- Download functionality for generated test step templates

## Input Format

The tool expects Excel files with the following columns:
- **Ref ID** (Column A): Control reference identifier
- **Control Description** (Column B): Detailed description of the control
- **Testing Attributes** (Column C): Testing procedures (optional)
- **Design Attributes** (Column D): Design specifications (optional)
- **Evidence of Control** (Column E): Required evidence (optional)

## Output Format

Generated Excel templates include:
- **Control ID**: Reference identifier
- **Test Step Name**: Concise, actionable test step names
- **Test Step Description**: Detailed testing instructions
- **Attribute Name**: Meaningful validation attribute names
- **Attribute Description**: Past-tense descriptions of what was verified

## AI Capabilities

### For Complete Controls
- Transforms testing attributes into proper test step format
- Avoids copying verbatim text, instead creating testing-focused instructions
- Generates "Obtain Evidence" steps with specific evidence lists
- Creates meaningful attribute names and descriptions

### For N/A Scenarios
- Analyzes control descriptions to identify key elements
- Extrapolates logical evidence requirements
- Creates realistic test steps based on control objectives
- Generates professional, audit-ready procedures

## Getting Started

### Prerequisites
- Node.js and npm for frontend
- Python 3.8+ for backend
- Azure OpenAI API access

### Environment Setup
Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_azure_openai_key
OPENAI_API_BASE=your_azure_endpoint
OPENAI_API_VERSION=2024-08-01-preview
OPENAI_ENGINE=gpt-4o
```

### Installation

1. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. **Backend Setup**
   ```bash
   cd backends/upload-app
   pip install -r requirements.txt
   python app.py
   ```

## Usage

1. **Upload SOX Control File**: Upload an Excel file containing your SOX controls
2. **AI Processing**: The system analyzes each control and generates test steps
3. **Download Template**: Receive a formatted Excel template with generated test steps
4. **Review and Customize**: Review the generated test steps and customize as needed

## Example Output

For a control describing "Monthly reconciliation of investment accounts":

**Generated Test Steps:**
- Obtain Evidence
- Inspect Reconciliation Process
- Verify Calculation Accuracy
- Inspect Review Evidence
- Validate Documentation Completeness

Each step includes detailed descriptions and meaningful test attributes.

## Contributing

This tool is designed to streamline SOX compliance testing by leveraging AI to generate comprehensive, professional test procedures from control descriptions.

## License

[Add your license information here] 