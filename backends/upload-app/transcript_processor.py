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

# --- Define System Prompts ---
PROCESS_RESPONSE_SYSTEM_PROMPT = """You are an AI assistant specialized in analyzing financial process walkthrough transcripts for the purpose of documenting Financial SOX (Sarbanes-Oxley) processes and controls.
Your task is to answer specific questions based *exclusively* on the provided transcript text. Focus ONLY on information that directly answers the specific question asked, keeping in mind the SOX context.

Format the answer as a detailed process flow, highlighting:
1.  **Sequence of Steps:** Clearly outline the order of actions.
2.  **Individuals Involved:** Identify roles (e.g., preparer, reviewer, approver) and specific actions they perform, relevant to their responsibilities in a SOX process.
3.  **Systems/Applications/Tools:** Mention any software or tools used at each step (e.g., NetSuite, Concur, ADP, Excel), noting their role in the control environment if specified.
4.  **Key Controls/Actions:** Describe significant actions, checks, or controls performed within the process. This is crucial for SOX documentation, so be thorough in capturing control activities mentioned.

**Crucially:**
- Only include details that directly address the question from a SOX process perspective.
- Avoid including information about related processes or topics, even if mentioned nearby in the transcript, if they do not directly answer the *specific question*. Other questions may cover those related details.
- Be concise. Your primary goal is to answer the question asked using only the directly relevant transcript text.
- Structure the response clearly. Use bullet points or numbered lists for steps if appropriate.
- If the transcript explicitly states the information for the question is not available or the process described doesn't apply, state that clearly.
- Do not invent information or make assumptions beyond the transcript content."""

NORMAL_RESPONSE_SYSTEM_PROMPT = """You are an AI assistant specialized in analyzing financial process walkthrough transcripts, with a focus on supporting Financial SOX (Sarbanes-Oxley) process documentation.
Your task is to answer specific questions based *exclusively* on the provided transcript text. Please be mindful of information that could be relevant to understanding SOX controls or process steps.

**Instructions:**
- Provide a direct and concise answer to the question using ONLY the information explicitly stated in the transcript.
- Do NOT format the answer as a process flow.
- Do NOT include sections like 'Sequence of Steps', 'Individuals Involved', etc.
- Focus solely on extracting the information that directly answers the question, paying attention to details pertinent to financial controls if mentioned.
- If the transcript explicitly states the information for the question is not available, state that clearly.
- Do not invent information or make assumptions beyond the transcript content."""

OTHER_TOPICS_SYSTEM_PROMPT = """You are an AI assistant skilled at analyzing financial transcripts for the purpose of enhancing Financial SOX (Sarbanes-Oxley) process documentation.
Your task is to identify and list any accounting-related topics discussed in the provided 'Transcript' that are NOT already covered by the 'Provided Answers'. These topics should ideally be relevant from a SOX perspective, such as unaddressed controls, risks, or process steps.

Output Instructions:
1.  Carefully compare the 'Transcript' against the 'Provided Answers'.
2.  For each accounting-related topic or process found in the 'Transcript' but missing from the 'Provided Answers' (especially those pertinent to SOX controls or financial reporting risks):
    *   Start with a primary bullet point stating the topic.
    *   Under this, use indented sub-bullets to provide as much detail as possible about this topic directly from the transcript. This includes any mentioned processes, controls, systems involved, roles, or accounting treatment that would be valuable for SOX documentation.
3.  Crucially, your response should ONLY contain these identified topics and their details, formatted as described.
4.  Do NOT include introductory phrases, meta-commentary like "The transcript mentions," or "This topic was not covered."
5.  Exclude all non-accounting related discussions (e.g., personal chats, off-topic remarks).
6.  If, after careful review, absolutely no additional accounting-related topics relevant to SOX are found that are not in the 'Provided Answers', then and only then, respond with the exact phrase: 'No additional accounting-related topics were identified.'

Focus on extracting and presenting information valuable for understanding the process from a SOX control standpoint.
"""

# --- End Define System Prompts ---

def get_answer_from_transcript(transcript: str, question: str, question_type: str) -> str:
    """Uses OpenAI to find the answer to a specific question within the transcript,
       selecting the appropriate prompt based on the question_type.

    Args:
        transcript: The full text of the meeting transcript.
        question: The specific question to answer.
        question_type: The type of question ('Normal Response' or 'Process Response').

    Returns:
        The formatted answer string or an error message.
    """
    if not openai.api_key:
        logger.error("OpenAI API key not configured.")
        return "Error: OpenAI API key not configured."

    # Select the appropriate system prompt based on the question type
    if question_type == "Normal Response":
        system_prompt = NORMAL_RESPONSE_SYSTEM_PROMPT
        user_prompt_format = f"""Based *only* on the following transcript, please provide a direct and concise answer to the question below.

**Transcript:**
{transcript}

**Question:** {question}

**Direct Answer:**"""
        logger.debug(f"Using NORMAL response prompt for question: {question[:50]}...")
    elif question_type == "Process Response":
        system_prompt = PROCESS_RESPONSE_SYSTEM_PROMPT
        user_prompt_format = f"""Based *only* on the following transcript, please answer the question below.
Format your answer as a detailed process flow as described in the system prompt.

**Transcript:**
{transcript}

**Question:** {question}

**Formatted Answer (Process Flow):**"""
        logger.debug(f"Using PROCESS response prompt for question: {question[:50]}...")
    else:
        logger.warning(f"Unknown question type '{question_type}' for question: {question[:50]}... Defaulting to Process Response.")
        # Default to process response or handle as an error if preferred
        system_prompt = PROCESS_RESPONSE_SYSTEM_PROMPT
        user_prompt_format = f"""Based *only* on the following transcript, please answer the question below.
Format your answer as a detailed process flow as described in the system prompt.

**Transcript:**
{transcript}

**Question:** {question}

**Formatted Answer (Process Flow):**"""

    # Format the user prompt
    user_prompt = user_prompt_format.format(transcript=transcript, question=question)

    try:
        logger.debug(f"Sending request to OpenAI for question: {question[:50]}...")
        response = openai.ChatCompletion.create(
            engine=OPENAI_ENGINE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000, # Adjust as needed
            temperature=0.1, # Lower temperature for more factual responses
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

# Insert helper function to identify other accounting-related topics
def get_other_topics(transcript: str, provided_answers: str) -> str:
    user_prompt = f"""Please review the 'Transcript' and 'Provided Answers' below.
Identify and detail any additional accounting-related topics from the transcript that are not covered in the answers, following the system prompt's output instructions.

Transcript:
'''{transcript}'''

Provided Answers:
'''{provided_answers}'''

Additional Accounting-Related Topics Discovered:"""
    try:
        response = openai.ChatCompletion.create(
            engine=OPENAI_ENGINE,
            messages=[
                {"role": "system", "content": OTHER_TOPICS_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000,
            temperature=0.2,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logger.error(f"Error identifying other topics: {str(e)}")
        logger.error(traceback.format_exc())
        return f"Error identifying other topics: {str(e)}"

def generate_process_flow_doc(transcript_text: str, title: str, questions: list[tuple[str, str]]) -> str:
    """Processes transcript against questions (with types) and generates a Word document.

    Args:
        transcript_text: The full text of the meeting transcript.
        title: The title for the document (from agenda A1).
        questions: A list of tuples, where each tuple contains (question_text, question_type).
                   Example: [('What is limit?', 'Normal Response'), ('Describe process?', 'Process Response')]

    Returns:
        The file path to the generated Word document in a temporary directory.
    """
    logger.info("Starting process flow document generation.")

    if not questions:
        raise ValueError("Question list is empty.")

    logger.info(f"Generating document titled '{title}' with {len(questions)} questions.")

    document = Document()
    document.add_heading(title, level=0)
    all_answers_combined = ""  # To store all answers for later comparison

    # Process each question from the list
    for i, (question_text, question_type) in enumerate(questions): # <-- Unpack tuple
        logger.info(f"Processing question {i+1}/{len(questions)} (Type: {question_type}): {question_text[:100]}...")

        # Add the question to the document
        document.add_heading(f"Question {i+1}: {question_text}", level=2) # <-- Use question_text

        # Get the formatted answer from AI, passing the type
        answer = get_answer_from_transcript(transcript_text, question_text, question_type) # <-- Pass type

        # --- Clean the answer (removes markdown common in AI responses) ---
        cleaned_answer = re.sub(r'^###\s+', '', answer, flags=re.MULTILINE) # Remove ### headings
        cleaned_answer = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_answer) # Remove **bold**
        cleaned_answer = re.sub(r'^#+\s+', '', cleaned_answer, flags=re.MULTILINE) # Remove other # headings
        cleaned_answer = re.sub(r'^-\s+', '', cleaned_answer, flags=re.MULTILINE) # Remove leading hyphens if desired (optional)
        # --- End cleaning ---

        # Add the cleaned answer to the document
        document.add_paragraph(cleaned_answer)
        document.add_paragraph() # Add a blank line for spacing
        all_answers_combined += f"Question: {question_text}\nAnswer: {cleaned_answer}\n\n"

    # --- New Step: Identify Other Topics ---
    logger.info("Identifying other accounting-related topics not covered by questions.")
    other_topics = get_other_topics(transcript_text, all_answers_combined)

    document.add_heading("Other Topics Discussed During the Meeting", level=1)
    document.add_paragraph(other_topics)

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