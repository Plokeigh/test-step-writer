from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from docx import Document # Use python-docx
import os
import logging
import traceback
from dotenv import load_dotenv
import openai
import tempfile # Keep tempfile for temporary saving

# Clear any existing OpenAI-related environment variables
for key in list(os.environ.keys()):
    if key.startswith('OPENAI_') or key.startswith('AZURE_'):
        del os.environ[key]

# Load environment variables
load_dotenv(override=True)

# Configure OpenAI for Azure
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv('AZURE_DEPLOYMENT_NAME') # Get deployment name

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Flowchart Creator App - .env file location: {os.path.abspath('.env')}")
logger.debug(f"Flowchart Creator App - API type: {openai.api_type}")
logger.debug(f"Flowchart Creator App - API base: {openai.api_base}")
logger.debug(f"Flowchart Creator App - API version: {openai.api_version}")
logger.debug(f"Flowchart Creator App - API key loaded: {bool(openai.api_key)}")
logger.debug(f"Flowchart Creator App - Deployment name: {AZURE_DEPLOYMENT_NAME}")

app = Flask(__name__)
# Allow requests from the Next.js frontend development server
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Configuration
UPLOAD_FOLDER = 'uploads_flowchart' # Use a different upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB max size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'docx'}

def read_docx_content(file_path):
    """Reads text content from a .docx file."""
    try:
        doc = Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        logger.info(f"Successfully read content from {file_path}")
        return '\n'.join(full_text)
    except Exception as e:
        logger.error(f"Error reading docx file {file_path}: {str(e)}")
        raise

def generate_mermaid_code(text_content: str) -> str:
    """Uses OpenAI to generate Mermaid flowchart syntax from text."""
    if not openai.api_key or not AZURE_DEPLOYMENT_NAME:
        logger.error("OpenAI API key or deployment name not configured.")
        raise ValueError("OpenAI API key or deployment name not configured.")

    # --- Updated System Prompt (v4 - Simplified Labels & Unique IDs) --- #
    system_prompt = """You are an AI assistant specialized in analyzing process descriptions (e.g., from SOX walkthroughs) and converting them into Mermaid flowchart code that visually resembles typical process diagrams.

**Primary Goal:** Create a clear flowchart grouped by major process areas, using appropriate shapes and including relevant details like actors and control IDs within step descriptions. Ensure the output is robust and renders correctly.

**Detailed Instructions:**
1.  **Identify Major Processes:** Analyze the text to identify distinct high-level process areas (e.g., "Overhead Allocation", "Contract Approval").
2.  **Group by Process:** Use Mermaid `subgraph` syntax ONLY for these major process areas.
3.  **Use Appropriate Shapes:** Employ different node shapes:
    *   Start/End: `NodeId([Start/End Label])` (Stadium)
    *   Steps: `NodeId[Step Description]` (Rectangle - Default)
    *   Inputs/Outputs/Docs: `NodeId[/Document or Input/Output/]` (Parallelogram)
    *   Decisions: `NodeId{Decision Text?}` (Diamond)
4.  **Detailed Step Nodes:** Create nodes for each step within its process subgraph. The node label MUST be descriptive and include:
    *   The core action.
    *   The primary Actor/Team/System (e.g., `Actor: Sr. Accountant`).
    *   Any Control IDs (e.g., `Control: R208`).
    *   **Use this format:** `NodeId[Action Description - Actor: Name, Control: ID]` (Use hyphens or simple separators instead of nested parentheses).
5.  **Globally Unique & Simple Node IDs:** Ensure ALL node IDs (e.g., `OA1`, `CMP_Start`) are UNIQUE across the entire diagram, not just within a subgraph. Use simple alphanumeric IDs (letters and numbers, underscores allowed if needed).
6.  **Logical Flow & Connections:** Use `-->` for sequence. Use labeled arrows `-->|Label|` for decision outcomes.
7.  **Clarity and Conciseness:** Keep node labels reasonably concise.

**Output Format:**
- Generate ONLY the Mermaid code block: ```mermaid ... ```.
- Use `graph TD` orientation.
- Ensure valid Mermaid syntax.
- NO extra text, titles, or comments outside the code block.
- If insufficient info: `graph TD\nA[Insufficient information to generate flowchart.]`

**Example Mermaid Output Snippet (Target Style v4):**
```mermaid
graph TD
    subgraph "Overhead Allocation"
        OA_Start([Start Overhead Allocation]) --> OA1[Perform annual OH rate analysis - Actor: Sr. Accountant, Control: R208];
        OA1 --> OA2[Review/approve OH rates - Actor: Asst. Controller, Control: INV-07];
        OA2 --> OA3[Quarterly OH absorption analysis - Actor: Sr. Accountant];
        OA3 --> OA_End([End OH Allocation Cycle]);
    end

    subgraph "COGS Calculation"
        COGS_Start([Start COGS Process]) --> COGS1[Monthly: Prepare COGS calculations - Actor: Sr. Accountant];
        COGS1 --> COGS2[Submit COGS file for review/approval - Actor: Sr. Accountant, Control: R196];
        COGS2 --> COGS3[Review/approve COGS file - Actor: Asst. Controller];
        COGS3 --> COGS_End([End COGS Cycle]);
    end
```"""
    # --- End of Updated System Prompt --- #

    user_prompt = f"""Generate a Mermaid flowchart based on the following text, grouping steps into major process subgraphs, using appropriate shapes, ensuring globally unique Node IDs, and using the specified label format:

{text_content}"""

    try:
        logger.debug("Sending request to OpenAI with V4 prompt (Simplified Labels, Unique IDs)...")
        response = openai.ChatCompletion.create(
            engine=AZURE_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2500,
            temperature=0.2,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )
        mermaid_code = response.choices[0].message['content'].strip()

        # Clean the response (same logic as before)
        if mermaid_code.startswith("```mermaid"):
             mermaid_code = mermaid_code[len("```mermaid"):].strip()
        if mermaid_code.endswith("```"):
            mermaid_code = mermaid_code[:-len("```")].strip()

        if not mermaid_code.lower().startswith('graph'):
             mermaid_code = "graph TD\n" + mermaid_code

        logger.debug("Received and cleaned Mermaid code (V4 prompt).")
        return mermaid_code
    except Exception as e:
        logger.error(f"Error calling OpenAI API for V4 Mermaid generation: {str(e)}")
        logger.error(traceback.format_exc())
        error_message = str(e).replace('\n', ' ').replace('"', '\"')
        return f"graph TD\n    A[Error generating flowchart: {error_message}]"


@app.route('/api/create-flowchart', methods=['POST'])
def create_flowchart_endpoint():
    """Handles .docx upload, generates Mermaid code, and returns it."""
    logger.info("Received request to /api/create-flowchart")

    if 'document' not in request.files:
        logger.error("No 'document' file part in the request")
        return jsonify({'error': "Missing 'document' file part"}), 400

    file = request.files['document']

    if file.filename == '':
        logger.error("No file selected")
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        docx_filepath = None
        temp_dir = None # Initialize temp_dir
        try:
            filename = secure_filename(file.filename)
            # Use tempfile for secure temporary storage
            temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
            docx_filepath = os.path.join(temp_dir, filename)

            logger.info(f"Saving uploaded docx to temporary path: {docx_filepath}")
            file.save(docx_filepath)
            del file # Release file handle

            # Read content
            logger.info("Reading docx content...")
            text_content = read_docx_content(docx_filepath)

            if not text_content:
                logger.warning("Docx file seems to be empty.")
                # Return valid Mermaid code for empty document
                return jsonify({'mermaid_code': 'graph TD\n    A[Uploaded document is empty]'}), 200

            # Generate Mermaid code
            logger.info("Generating Mermaid code via AI...")
            mermaid_code = generate_mermaid_code(text_content)

            logger.info("Successfully generated Mermaid code.")
            return jsonify({'mermaid_code': mermaid_code}), 200

        except Exception as e:
            logger.error(f"Error processing flowchart request: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            error_message = str(e).replace('\n', ' ').replace('"', '\"')
             # Return error as JSON, not Mermaid
            return jsonify({'error': f'An error occurred: {error_message}'}), 500
        finally:
            # Clean up the temporary file and directory
            if docx_filepath and os.path.exists(docx_filepath):
                try:
                    os.remove(docx_filepath)
                    logger.info(f"Cleaned up temporary file: {docx_filepath}")
                except Exception as cleanup_err:
                    logger.error(f"Error cleaning up temporary file {docx_filepath}: {cleanup_err}")
            if temp_dir and os.path.exists(temp_dir):
                 try:
                     os.rmdir(temp_dir)
                     logger.info(f"Cleaned up temporary directory: {temp_dir}")
                 except Exception as cleanup_err:
                     logger.error(f"Error cleaning up temporary directory {temp_dir}: {cleanup_err}")
    else:
        logger.error(f"Invalid file type uploaded: {file.filename}")
        return jsonify({'error': 'Invalid file type. Only .docx allowed'}), 400

if __name__ == '__main__':
    logger.info("Starting Flowchart Creator Flask server...")
    # Ensure the deployment name is set
    if not AZURE_DEPLOYMENT_NAME:
        logger.critical("AZURE_DEPLOYMENT_NAME environment variable is not set. Exiting.")
    else:
         # Run on port 3003
        app.run(port=3003, debug=True, host='localhost')