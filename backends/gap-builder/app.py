from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import logging
import traceback
import tempfile
import openai
from dotenv import load_dotenv
from services.gap_generator import GapGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

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

# Log configuration
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

@app.route('/api/generate-gaps', methods=['POST'])
def generate_gaps():
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
        
        # Check if file is provided
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Invalid file type. Only Excel files (.xlsx, .xls) are allowed.'}), 400
            
        # Save uploaded file temporarily
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, 'input.xlsx')
        output_path = os.path.join(temp_dir, 'output.xlsx')
        file.save(input_path)
        
        # Generate gaps and recommendations
        generator = GapGenerator()
        try:
            workbook = generator.process_template(input_path)
            workbook.save(output_path)
        except Exception as e:
            logger.error(f"Gap generation error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'error': f'Gap generation failed: {str(e)}'}), 500
        
        return send_file(
            output_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='itgc_gaps_recommendations.xlsx'
        )
        
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

# Create a simple templates directory and HTML file for the frontend
os.makedirs('backends/gap-builder/templates', exist_ok=True)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Get host and port from environment or use defaults
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5002))  # Use 5002 to avoid conflicts with other tools
    
    app.run(host=host, port=port, debug=True) 