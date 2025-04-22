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

# Import the new processing function (will be created in transcript_processor.py)
from transcript_processor import (
    generate_process_flow_doc
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
ALLOWED_EXTENSIONS = {'docx', 'txt', 'xlsx'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Increase max size for potentially larger transcripts (32MB)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_content(file_path):
    """Read content from a supported file type (.docx, .txt)."""
    try:
        file_ext = file_path.rsplit('.', 1)[1].lower()
        if file_ext == 'docx':
            doc = Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return '\n'.join(full_text)
        elif file_ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        raise

def read_agenda_excel(file_obj_or_path):
    """Read agenda from an Excel file (.xlsx) provided as a path or file-like object.

    Reads title from cell A1 and questions from A2, A3, ...

    Returns:
        tuple: (title: str, questions: list[str])
    """
    try:
        # openpyxl can load directly from a file-like object or path
        workbook = openpyxl.load_workbook(file_obj_or_path)
        sheet = workbook.active

        title = sheet['A1'].value
        if not title:
            title = "Walkthrough Summary" # Default title if A1 is empty
            logger.warning("Agenda cell A1 is empty, using default title.")
        else:
            title = str(title).strip()

        questions = []
        row = 2 # Start reading questions from A2
        while True:
            cell_value = sheet[f'A{row}'].value
            if cell_value is None or str(cell_value).strip() == "":
                break # Stop if cell is empty
            questions.append(str(cell_value).strip())
            row += 1

        if not questions:
            raise ValueError("No questions found in agenda file starting from cell A2.")

        # Determine if input was path or object for logging
        log_source = getattr(file_obj_or_path, 'filename', file_obj_or_path) # Use filename if available, else the path itself
        logger.info(f"Read title '{title}' and {len(questions)} questions from agenda: {log_source}")
        workbook.close()
        return title, questions

    except Exception as e:
        logger.error(f"Error reading agenda Excel file {file_obj_or_path}: {str(e)}")
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
    """Handle transcript and agenda file uploads, process, and return Word doc."""
    logger.info("Received request to /upload endpoint")

    if request.method == 'OPTIONS':
        logger.debug("Handling OPTIONS request")
        return '', 204

    logger.info("Processing POST request")
    logger.debug(f"Files in request: {list(request.files.keys())}")

    if 'transcript' not in request.files or 'agenda' not in request.files:
        logger.error("Missing 'transcript' or 'agenda' file part in the request")
        return jsonify({'error': "Missing 'transcript' or 'agenda' file part"}), 400

    transcript_file = request.files['transcript']
    agenda_file = request.files['agenda']

    logger.info(f"Received transcript: {transcript_file.filename}")
    logger.info(f"Received agenda: {agenda_file.filename}")

    if transcript_file.filename == '' or agenda_file.filename == '':
        logger.error("One or both files not selected")
        return jsonify({'error': 'No selected file for transcript or agenda'}), 400

    # Read file contents immediately for size check
    transcript_contents = transcript_file.read()
    agenda_contents = agenda_file.read()
    transcript_file.seek(0) # Reset file pointer
    agenda_file.seek(0)

    if not transcript_contents or not agenda_contents:
         logger.error("One or both uploaded files are empty")
         return jsonify({'error': 'Uploaded transcript or agenda file is empty'}), 400

    transcript_filepath = None
    agenda_filepath = None
    output_doc_path = None

    if transcript_file and allowed_file(transcript_file.filename) and \
       agenda_file and allowed_file(agenda_file.filename):
        try:
            # Save uploaded files temporarily
            transcript_filename = secure_filename(transcript_file.filename)
            agenda_filename = secure_filename(agenda_file.filename)

            transcript_filepath = os.path.join(app.config['UPLOAD_FOLDER'], transcript_filename)
            agenda_filepath = os.path.join(app.config['UPLOAD_FOLDER'], agenda_filename)

            logger.info(f"Saving transcript to: {transcript_filepath}")
            transcript_file.save(transcript_filepath)
            # logger.info(f"Saving agenda to: {agenda_filepath}") # No longer saving agenda
            # agenda_file.save(agenda_filepath) # <--- REMOVE THIS LINE

            # Explicitly delete Flask file objects after saving/using
            del transcript_file
            # Keep agenda_file object reference until after it's read

            # Read file contents
            logger.info("Reading transcript file content")
            transcript_text = read_file_content(transcript_filepath)
            logger.info("Reading agenda file content directly from object")
            agenda_title, agenda_questions = read_agenda_excel(agenda_file) # <--- Pass file object directly

            # Now we can delete the agenda_file reference
            del agenda_file

            # Process transcript and agenda to generate Word doc
            logger.info("Processing transcript and agenda to generate Word document")
            # This function should return the path to the generated .docx file
            output_doc_path = generate_process_flow_doc(transcript_text, agenda_title, agenda_questions)
            logger.info(f"Generated Word document at: {output_doc_path}")

            # Send the generated Word document
            return send_file(
                output_doc_path,
                as_attachment=True,
                download_name="Processed_Walkthrough.docx",
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        except Exception as e:
            logger.error(f"Error processing files: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'error': f"An error occurred during processing: {str(e)}",
            }), 500
        finally:
            # Clean up uploaded files and generated doc
            if transcript_filepath and os.path.exists(transcript_filepath):
                os.remove(transcript_filepath)
                logger.info(f"Cleaned up temporary transcript file: {transcript_filepath}")
            if agenda_filepath and os.path.exists(agenda_filepath):
                os.remove(agenda_filepath)
                logger.info(f"Cleaned up temporary agenda file: {agenda_filepath}")
            if output_doc_path and os.path.exists(output_doc_path):
                 try:
                     os.remove(output_doc_path)
                     logger.info(f"Cleaned up generated Word document: {output_doc_path}")
                 except Exception as remove_err:
                     logger.error(f"Error cleaning up generated file {output_doc_path}: {remove_err}")

    else:
        allowed_types = ", ".join(ALLOWED_EXTENSIONS)
        error_msg = f"Invalid file type. Allowed types: {allowed_types}"
        logger.error(error_msg)
        # Check which file caused the error
        if not allowed_file(transcript_file.filename):
            error_msg += f" (Transcript: {transcript_file.filename})"
        if not allowed_file(agenda_file.filename):
            error_msg += f" (Agenda: {agenda_file.filename})"
        return jsonify({'error': error_msg}), 400

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