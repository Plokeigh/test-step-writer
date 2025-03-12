from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from services.matrix_generator import MatrixGenerator
import tempfile
import os
import logging
import traceback
from dotenv import load_dotenv
import openai

# Clear any existing OpenAI-related environment variables
for key in list(os.environ.keys()):
    if key.startswith('OPENAI_') or key.startswith('AZURE_'):
        del os.environ[key]

# Load environment variables
load_dotenv(override=True)

# Configure OpenAI for Azure
openai.api_type = "azure"  # Force azure type
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Clear any existing OpenAI configuration
if hasattr(openai, '_default_api_key'):
    delattr(openai, '_default_api_key')
if hasattr(openai, '_default_api_base'):
    delattr(openai, '_default_api_base')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"App.py - .env file location: {os.path.abspath('.env')}")
logger.debug(f"App.py - API type: {openai.api_type}")
logger.debug(f"App.py - API base: {openai.api_base}")
logger.debug(f"App.py - API version: {openai.api_version}")
logger.debug(f"App.py - API key (first 5 chars): {openai.api_key[:5] if openai.api_key else 'None'}")
logger.debug(f"App.py - Deployment name: {os.getenv('AZURE_DEPLOYMENT_NAME')}")

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-matrix', methods=['POST'])
def generate_matrix():
    try:
        # Test OpenAI connection before processing
        try:
            test_response = openai.ChatCompletion.create(
                engine=os.getenv('AZURE_DEPLOYMENT_NAME'),
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            logger.debug("OpenAI connection test successful")
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {str(e)}")
            return jsonify({'error': f'OpenAI connection failed: {str(e)}'}), 500

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        # Save uploaded file temporarily
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, 'input.xlsx')
        output_path = os.path.join(temp_dir, 'output.xlsx')
        file.save(input_path)
        
        # Generate matrix
        generator = MatrixGenerator()
        try:
            workbook = generator.process_scoping_document(input_path)
            workbook.save(output_path)
        except Exception as e:
            logger.error(f"Matrix generation error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'error': f'Matrix generation failed: {str(e)}'}), 500
        
        return send_file(
            output_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='risk_control_matrix.xlsx'
        )
        
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3001, debug=True)