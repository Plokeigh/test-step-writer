import os
import openai
from docx import Document # python-docx library
import logging
import tempfile
import traceback
import re # <--- Add import
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Set to DEBUG for more verbose output during development

# Load environment variables
load_dotenv()

# Configure OpenAI for Azure (ensure these env vars are set correctly)
openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION", "2024-08-01-preview")
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_ENGINE = os.getenv("OPENAI_ENGINE", "gpt-4o") # Specify your deployment name/engine

logger.debug(f"Transcript_processor.py - API type: {openai.api_type}")
logger.debug(f"Transcript_processor.py - API base: {openai.api_base}")
logger.debug(f"Transcript_processor.py - API version: {openai.api_version}")
logger.debug(f"Transcript_processor.py - Engine: {OPENAI_ENGINE}")
logger.debug(f"Transcript_processor.py - API Key Loaded: {bool(openai.api_key)}")

def get_answer_from_transcript(transcript: str, question: str) -> str:
    """Uses OpenAI to find the answer to a specific question within the transcript
       and format it as a process flow.
    """
    if not openai.api_key:
        logger.error("OpenAI API key not configured.")
        return "Error: OpenAI API key not configured."

    system_prompt = ("""You are an AI assistant specialized in analyzing financial process walkthrough transcripts. 
Your task is to answer specific questions based ONLY on the provided transcript text. 
Format the answer as a detailed process flow, highlighting:

1.  **Sequence of Steps:** Clearly outline the order of actions.
2.  **Individuals Involved:** Identify roles (e.g., preparer, reviewer, approver) and specific actions they perform.
3.  **Systems/Applications/Tools:** Mention any software or tools used at each step (e.g., NetSuite, Concur, ADP, Excel).
4.  **Key Controls/Actions:** Describe significant actions, checks, or controls performed within the process.

Structure the response clearly. Use bullet points or numbered lists for steps if appropriate. 
If the transcript explicitly states the information for the question is not available or the process described doesn't apply, state that clearly. 
Do not invent information or make assumptions beyond the transcript content.""")

    # Rewritten user_prompt using a single multi-line f-string
    user_prompt = f"""Based *only* on the following transcript, please answer the question below. 
Format your answer as a detailed process flow as described in the system prompt.

**Transcript:**
{transcript}

**Question:** {question}

**Formatted Answer (Process Flow):**"""

    try:
        logger.debug(f"Sending request to OpenAI for question: {question[:50]}...")
        response = openai.ChatCompletion.create(
            engine=OPENAI_ENGINE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000, # Adjust as needed
            temperature=0.2, # Lower temperature for more factual responses
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].message['content'].strip()
        logger.debug(f"Received answer from OpenAI for question: {question[:50]}...")
        return answer
    except Exception as e:
        logger.error(f"Error calling OpenAI API for question '{question[:50]}...': {str(e)}")
        logger.error(traceback.format_exc())
        return f"Error processing question: {str(e)}"

def generate_process_flow_doc(transcript_text: str, title: str, questions: list[str]) -> str:
    """Processes transcript against agenda questions and generates a Word document.

    Args:
        transcript_text: The full text of the meeting transcript.
        title: The title for the document (from agenda A1).
        questions: A list of questions (from agenda A2 onwards).

    Returns:
        The file path to the generated Word document in a temporary directory.
    """
    logger.info("Starting process flow document generation.")

    # Questions list is now passed directly
    if not questions:
        # This check should ideally be done in app.py after reading the excel
        raise ValueError("Agenda question list is empty.")

    logger.info(f"Generating document titled '{title}' with {len(questions)} questions.")

    # Create a new Word document
    document = Document()
    # Use the title from the agenda file
    document.add_heading(title, level=0)

    # Process each question from the list
    for i, question in enumerate(questions):
        logger.info(f"Processing question {i+1}/{len(questions)}: {question[:100]}...")

        # Add the question to the document
        document.add_heading(f"Question {i+1}: {question}", level=2)

        # Get the formatted answer from AI
        answer = get_answer_from_transcript(transcript_text, question)

        # --- Add these lines to clean the answer ---
        # Remove ### heading markers
        cleaned_answer = re.sub(r'^###\s+', '', answer, flags=re.MULTILINE)
        # Remove ** bold markers
        cleaned_answer = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_answer)
        # --- End of added lines ---

        # Add the cleaned answer to the document
        document.add_paragraph(cleaned_answer) # <-- Use cleaned_answer here
        document.add_paragraph() # Add a blank line for spacing

    # Save the document to a temporary file
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        output_path = temp_file.name
        temp_file.close()
        document.save(output_path)
        logger.info(f"Successfully generated Word document: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error saving Word document: {str(e)}")
        logger.error(traceback.format_exc())
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
        raise