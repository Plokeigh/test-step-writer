from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import openai
from docx import Document
import traceback
import logging
import openpyxl

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
logger.debug(f"App.py - Environment variable raw value: {os.environ.get('OPENAI_API_KEY')}")

# Import your existing functions and data structures
from transcript_processor import (
    process_transcript,
    parse_output,
    update_template
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
TEMPLATE_PATH = os.path.join('templates', 'Scoping Document.xlsx')
ALLOWED_EXTENSIONS = {'docx'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)  # Ensure templates directory exists

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_docx(file_path):
    """Read content from a Word document."""
    try:
        doc = Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        logger.error(f"Error reading DOCX file: {str(e)}")
        raise

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

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    """Handle file uploads with detailed logging"""
    logger.info("Received request to /upload endpoint")
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.debug(f"Request origin: {request.headers.get('Origin')}")
    
    if request.method == 'OPTIONS':
        logger.debug("Handling OPTIONS request")
        return '', 204
    
    logger.info("Processing POST request")
    logger.debug(f"Files in request: {request.files}")
    logger.debug(f"Form data in request: {request.form}")
    
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    logger.info(f"Received file: {file.filename}")
    
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    
    # Add file size check here
    file_contents = file.read()
    file.seek(0)  # Reset file pointer after reading
    
    if len(file_contents) == 0:
        logger.error("Uploaded file is empty")
        return jsonify({'error': 'Uploaded file is empty'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logger.info(f"Saving file to: {filepath}")
            file.save(filepath)
            
            # Process the transcript
            logger.info("Reading DOCX file")
            transcript_text = read_docx(filepath)
            
            logger.info("Processing transcript with GPT")
            output = process_transcript(transcript_text)
            
            logger.info("Parsing GPT output")
            data = parse_output(output)
            
            # Update the template
            logger.info(f"Updating template at: {os.path.abspath(TEMPLATE_PATH)}")
            update_template(data, TEMPLATE_PATH)
            logger.info("Template updated successfully")
            
            # Clean up the uploaded file
            os.remove(filepath)
            logger.info("Cleaned up temporary file")
            
            # Return the updated Excel template as a download
            return send_file(
                TEMPLATE_PATH,
                as_attachment=True,
                download_name="Scoping Document - Updated.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Clean up on error
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
                logger.info("Cleaned up temporary file after error")
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
    logger.error(f"Invalid file type: {file.filename}")
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint with detailed status"""
    logger.info("Health check requested")
    origin = request.headers.get('Origin')
    logger.debug(f"Health check origin: {origin}")
    
    template_exists = os.path.exists(TEMPLATE_PATH)
    template_size = os.path.getsize(TEMPLATE_PATH) if template_exists else 0
    
    status = {
        'status': 'healthy',
        'template': {
            'exists': template_exists,
            'path': os.path.abspath(TEMPLATE_PATH),
            'size': template_size
        },
        'upload_folder_exists': os.path.exists(UPLOAD_FOLDER),
        'openai_key_configured': bool(openai.api_key)
    }
    logger.debug(f"Health status: {status}")
    return jsonify(status), 200

@app.route('/clear-template', methods=['POST'])
def clear_template():
    """Clear all data from template except headers."""
    logger.info("Received request to clear template")
    
    if not os.path.exists(TEMPLATE_PATH):
        logger.error("Template file not found")
        return jsonify({'error': 'Template file not found'}), 404
    
    try:
        wb = openpyxl.load_workbook(TEMPLATE_PATH)
        sheet = wb.active
        
        # Keep the header row and delete everything else
        if sheet.max_row > 1:  # Only delete if there are rows beyond the header
            sheet.delete_rows(2, sheet.max_row - 1)
        
        wb.save(TEMPLATE_PATH)
        logger.info("Template cleared successfully")
        
        return jsonify({'message': 'Template cleared successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error clearing template: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

# Startup checks
def run_startup_checks():
    """Perform startup checks and log results"""
    logger.info("Running startup checks...")
    
    if not os.path.exists('templates'):
        logger.info("Creating templates directory")
        os.makedirs('templates', exist_ok=True)
    
    if not os.path.exists(TEMPLATE_PATH):
        logger.warning(f"Template file not found at {os.path.abspath(TEMPLATE_PATH)}")
    else:
        logger.info(f"Template file found at {os.path.abspath(TEMPLATE_PATH)}")
    
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
    # Enable debug mode for detailed error messages
    app.run(debug=True, port=3002, host='localhost')