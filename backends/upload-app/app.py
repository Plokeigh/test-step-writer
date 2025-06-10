from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import openai
from docx import Document
import traceback
import logging
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure OpenAI for Azure
openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION", "2023-05-15")
openai.api_key = os.getenv("OPENAI_API_KEY")

logger.debug(f"App.py - .env file location: {os.path.abspath('.env')}")
logger.debug(f"App.py - API type: {openai.api_type}")
logger.debug(f"App.py - API base: {openai.api_base}")

# Import the SOX testing functions
from sox_processor import (
    generate_test_steps,
    export_test_plan_to_word
)

app = Flask(__name__)

# Updated CORS configuration to allow Next.js dev server
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-Requested-With", "Accept", "Origin", "Authorization"],
        "expose_headers": ["Content-Type", "Content-Disposition"],
        "supports_credentials": False,
        "max_age": 3600
    }
})

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    origin = request.headers.get('Origin')
    if origin == 'http://localhost:3000':
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Expose-Headers', 'Content-Disposition')
        response.headers.add('Access-Control-Max-Age', '3600')
    return response

@app.route('/generate-test-steps', methods=['POST', 'OPTIONS'])
def generate_test_steps_endpoint():
    """Handle Excel file upload with SOX controls and generate test steps template."""
    logger.info("Received request to /generate-test-steps endpoint")

    if request.method == 'OPTIONS':
        logger.debug("Handling OPTIONS request")
        return '', 204

    logger.info("Processing POST request for SOX test step generation")

    files = request.files.getlist('files')
    
    if not files or len(files) == 0:
        logger.error("No files uploaded")
        return jsonify({'error': "No Excel file uploaded"}), 400

    # We only need one Excel file
    file = files[0]
    
    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Please upload an Excel file (.xlsx or .xls)'}), 400

    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the Excel file to generate test steps
        result = generate_test_steps([filepath])
        
        # Return the Excel template as a download
        if 'excelTemplatePath' in result:
            return send_file(
                result['excelTemplatePath'],
                as_attachment=True,
                download_name="SOX_Test_Steps_Template.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({
                'success': True,
                'result': result
            }), 200

    except Exception as e:
        logger.error(f"Error generating test steps: {str(e)}")
        return jsonify({
            'error': f"An error occurred during processing: {str(e)}",
        }), 500
    finally:
        # Clean up uploaded file
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up temporary file: {filepath}")
        # Clean up generated template file
        if 'result' in locals() and 'excelTemplatePath' in result:
            template_path = result['excelTemplatePath']
            if os.path.exists(template_path):
                try:
                    os.remove(template_path)
                    logger.info(f"Cleaned up generated template: {template_path}")
                except Exception as remove_err:
                    logger.error(f"Error cleaning up template {template_path}: {remove_err}")

@app.route('/export-test-plan', methods=['POST', 'OPTIONS'])
def export_test_plan_endpoint():
    """Export test plan as Word document."""
    logger.info("Received request to /export-test-plan endpoint")

    if request.method == 'OPTIONS':
        logger.debug("Handling OPTIONS request")
        return '', 204

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Generate Word document from test plan data
        doc_path = export_test_plan_to_word(data)
        
        # Send the generated Word document
        return send_file(
            doc_path,
            as_attachment=True,
            download_name=f"{data.get('controlName', 'TestPlan').replace(' ', '_')}.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        logger.error(f"Error exporting test plan: {str(e)}")
        return jsonify({
            'error': f"An error occurred during export: {str(e)}",
        }), 500
    finally:
        # Clean up generated file
        if 'doc_path' in locals() and os.path.exists(doc_path):
            try:
                os.remove(doc_path)
                logger.info(f"Cleaned up generated document: {doc_path}")
            except Exception as remove_err:
                logger.error(f"Error cleaning up generated file {doc_path}: {remove_err}")

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    logger.info("Health check requested")
    status = {
        'status': 'healthy',
        'upload_folder_exists': os.path.exists(UPLOAD_FOLDER),
        'openai_key_configured': bool(openai.api_key)
    }
    logger.debug(f"Health status: {status}")
    return jsonify(status), 200

# Startup checks
def run_startup_checks():
    """Perform startup checks and log results"""
    logger.info("Running startup checks...")

    if not os.path.exists(UPLOAD_FOLDER):
        logger.info(f"Creating upload folder at {os.path.abspath(UPLOAD_FOLDER)}")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if not openai.api_key:
        logger.warning("OpenAI API key not configured")
    else:
        logger.info("OpenAI API key configured")

if __name__ == '__main__':
    run_startup_checks()
    logger.info("Starting Flask server...")
    # Enable debug mode for detailed error messages during development
    app.run(debug=True, port=3002, host='localhost')