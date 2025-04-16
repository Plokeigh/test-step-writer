import os
import openai
import openpyxl
from docx import Document
from typing import Dict, List, Optional
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Load environment variables at the start
load_dotenv()

# Configure OpenAI for Azure
openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION", "2024-08-01-preview")
openai.api_key = os.getenv("OPENAI_API_KEY")

logger.debug(f"Transcript_processor.py - .env file location: {os.path.abspath('.env')}")
logger.debug(f"Transcript_processor.py - API type: {openai.api_type}")
logger.debug(f"Transcript_processor.py - API base: {openai.api_base}")
logger.debug(f"Transcript_processor.py - Environment variable raw value: {os.environ.get('OPENAI_API_KEY')}")

# Import everything from config
from config import (
    QUESTION_HEADER_MAPPING,
    AGENDA,
    RESPONSE_EXAMPLES,
    QUESTION_GUIDANCE
)
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook

def extract_section_text(transcript: str, section: str) -> str:
    """Extract relevant section text from the transcript with surrounding context."""
    try:
        sections = transcript.split("Section")
        
        # Find the current section index
        current_section_idx = -1
        for idx, s in enumerate(sections):
            if section.replace("Section ", "") in s:
                current_section_idx = idx
                break
                
        if current_section_idx == -1:
            return transcript
            
        # Combine current section with previous and next sections if they exist
        context = []
        if current_section_idx > 0:
            context.append(sections[current_section_idx - 1])
        context.append(sections[current_section_idx])
        if current_section_idx < len(sections) - 1:
            context.append(sections[current_section_idx + 1])
            
        return " ".join(context).strip()
        
    except Exception as e:
        logger.error(f"Error extracting section {section}: {str(e)}")
        return transcript

def create_enhanced_prompt(transcript: str, section: str, question: str) -> str:
    """Create an enhanced prompt that better handles cross-referenced answers."""
    question_key = QUESTION_HEADER_MAPPING.get(question)
    guidance = QUESTION_GUIDANCE.get(question_key, {})

    purpose = guidance.get('purpose', 'Not specified')
    process_background = guidance.get('process_background', '')

    # Add related questions that might contain relevant information
    related_questions = []
    for q, header in QUESTION_HEADER_MAPPING.items():
        if any(keyword in q.lower() for keyword in question.lower().split()):
            if q != question:
                related_questions.append(q)

    prompt = f"""
    You are an IT audit specialist analyzing an ITGC walkthrough transcript.
    Your goal is to accurately document the client's **current process** based **only** on information provided in the transcript.

    **IMPORTANT:** Focus on what the **client states they actually do**. If the transcript describes a process suggested by a consultant that the client is *not* currently doing, **ignore** that description and treat the process as not performed by the client. Only document processes the client confirms are their active practice.

    First, review the transcript section for information related to the specific question below. Look for:
        - Direct statements from the client about their current practices.
        - Descriptions of the client's actual operational steps.

    Consider that relevant information might be mentioned while discussing related topics or split across the conversation.

    Related questions that might contain relevant information:
    {related_questions}

    Respond with "N/A - This information was not discussed in the walkthrough meeting transcript." only if:
    - No information about the client's actual current process for this question is found.
    - The client states they do not perform this process, or the only description is a suggestion they haven't adopted.

    Guidelines for your response if information IS found:
    - Provide direct, factual information about the client's **current** process.
    - Exclude consultant suggestions not confirmed by the client.
    - Be concise and focus on the client's actual practices mentioned in the transcript.

    Review the context for this question:
       - Purpose: {purpose}
       - Process Background: {process_background}

    Analyze the transcript section based on the instructions above and provide a clear, factual response reflecting the client's **current state**.

    Question: {question}

    Transcript section:
    {transcript}

    Before responding, verify:
    1. Does the answer describe the client's **actual current** process, not a suggestion?
    2. Is the answer based solely on client-confirmed information from the transcript?
    3. Is the answer concise and directly relevant to the question?
    """
    return prompt

def process_transcript(transcript: str) -> str:
    """Process transcript with additional validation for N/A responses."""
    responses = []
    
    # First pass - gather all responses
    initial_responses = {}
    for section, questions in AGENDA.items():
        section_text = extract_section_text(transcript, section)
        
        for question in questions:
            enhanced_prompt = create_enhanced_prompt(section_text, section, question)
            try:
                response = openai.ChatCompletion.create(
                    engine="gpt-4o-it-risk",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an IT audit specialist analyzing ITGC walkthrough transcripts. "
                                "Your primary directive is to ONLY use information explicitly stated in the transcript. "
                                "You must not make assumptions or infer information that isn't directly discussed. "
                                "**Crucially, differentiate between the client's description of their actual current process and any consultant suggestions or explanations of ideal processes.** "
                                "If a topic isn't explicitly covered as the client's current practice, respond with the exact N/A message. "
                                "If the topic is discussed as the client's current practice, provide only factual information directly from the transcript. "
                                "Never generate responses based on typical practices or assumptions."
                            )
                        },
                        {"role": "user", "content": enhanced_prompt}
                    ],
                    max_tokens=5000,
                    temperature=0.1,
                )
                answer = response.choices[0].message['content']
                initial_responses[question] = answer
                
            except Exception as e:
                logger.error(f"Error processing question '{question}': {str(e)}")
                initial_responses[question] = "Error processing response"

    # Second pass - validate N/A responses
    for section, questions in AGENDA.items():
        for question in questions:
            answer = initial_responses[question]
            
            # If the answer is N/A, do an additional check
            if "N/A" in answer:
                validation_prompt = f"""
                Review this entire transcript again, specifically looking for ANY mention of information related to: "{question}"
                
                Consider:
                1. Information mentioned while discussing other topics
                2. Implicit details in process descriptions
                3. Related information that could answer this question
                4. Examples or scenarios that describe this process
                
                If you find ANY relevant information, provide it. Only confirm N/A if you are absolutely certain no relevant information exists.

                Transcript:
                {transcript}
                """
                
                try:
                    validation_response = openai.ChatCompletion.create(
                        engine="gpt-4o-it-risk",
                        messages=[
                            {"role": "system", "content": "You are an IT audit specialist doing a thorough validation of potentially missed information."},
                            {"role": "user", "content": validation_prompt}
                        ],
                        max_tokens=5000,
                        temperature=0.1,
                    )
                    validated_answer = validation_response.choices[0].message['content']
                    
                    # If validation found information, use it instead
                    if "N/A" not in validated_answer:
                        answer = validated_answer
                
                except Exception as e:
                    logger.error(f"Error validating N/A response for '{question}': {str(e)}")
            
            responses.append(f"Question: {question}\nAnswer: {answer}\n<|endofresponse|>")
    
    return "\n".join(responses)

def standardize_response(original_answer: str, header: str, all_responses: Dict[str, str]) -> str:
    """
    Compare the response to Example Responses and rewrite to match format/length/verbiage.
    """
    # If the answer indicates the topic wasn't discussed, return it as-is
    if original_answer.strip() == "N/A - This information was not discussed in the walkthrough meeting transcript.":
        return original_answer

    logger.debug(f"Standardizing response for header: {header}")
    logger.debug(f"Header exists in QUESTION_GUIDANCE: {header in QUESTION_GUIDANCE}")
    logger.debug(f"Header exists in RESPONSE_EXAMPLES: {header in RESPONSE_EXAMPLES}")
    
    # Special handling for system account related fields
    if header in ["Credential Storage for System Accounts", "System Account Credential Access"]:
        system_accounts_response = all_responses.get("System Accounts", "")
        if system_accounts_response.lower().startswith("no"):
            return "N/A - No Interactive System Accounts"
    
    if not original_answer or header not in QUESTION_GUIDANCE:
        logger.warning(f"Header {header} not found in QUESTION_GUIDANCE or empty answer")
        return original_answer.replace('"', '').replace("'", '').strip('[]').strip()
    
    guidance = QUESTION_GUIDANCE[header]
    examples = RESPONSE_EXAMPLES.get(header, [])
    logger.debug(f"Found {len(examples)} examples for header {header}")
    
    # Combined prompt that handles both extraction and formatting in one step
    formatting_prompt = f"""
    Original response: "{original_answer}"

    Purpose of this question: {guidance.get('purpose', '')}

    Your task is to extract the core factual information from the original response and format it to exactly match these example responses:
    {examples}

    Critical Requirements:
    1. Extract ONLY factual process information and current state
    2. Remove ALL explanatory text and examples
    3. Remove ANY information that could belong to other headers
    4. Focus on "what is" rather than "what should be"
    5. Pick ONE example response as a template and follow its exact format
    6. Response must be a single statement/paragraph (no bullet points)
    7. Must match the length and detail level of examples
    8. Must start with similar phrases as the examples when applicable
    9. Do not use quotes, brackets, or special characters

    Provide the final formatted response:
    """
    
    try:
        format_response = openai.ChatCompletion.create(
            engine="gpt-4o-it-risk",
            messages=[
                {
                    "role": "system",
                    "content": "You are an IT audit specialist and technical writer. Extract factual information and format it to exactly match the example responses."
                },
                {"role": "user", "content": formatting_prompt}
            ],
            max_tokens=750,
            temperature=0.1
        )
        
        standardized_response = format_response.choices[0].message['content'].strip()
        
        # Clean up the response
        cleaned_response = ' '.join(standardized_response.split())  # Remove line breaks
        cleaned_response = cleaned_response.replace('Response:', '').replace('Final response:', '')
        cleaned_response = cleaned_response.strip('[]"\'`').strip()
        
        return cleaned_response

    except Exception as e:
        logger.error(f"Error standardizing response for {header}: {str(e)}")
        return original_answer.replace('"', '').replace("'", '').strip('[]').strip()

def get_next_empty_row(sheet) -> int:
    """
    Find the next empty row in the sheet.
    """
    row = 2  # assume row 1 has headers
    while sheet.cell(row=row, column=1).value is not None:
        row += 1
    return row

def parse_output(output: str) -> Dict[str, str]:
    """
    Takes the combined GPT output and organizes it into a dictionary keyed by question header.
    """
    responses = output.split("<|endofresponse|>")
    data = {}
    
    # Create reverse mapping from header to question
    reverse_mapping = {v: k for k, v in QUESTION_HEADER_MAPPING.items()}
    
    for response in responses:
        if response.strip():
            # Split on "Question:" and "Answer:" more robustly
            parts = response.strip().split("Question:", 1)
            if len(parts) > 1:
                question_answer = parts[1].split("Answer:", 1)
                if len(question_answer) > 1:
                    question = question_answer[0].strip()
                    answer = question_answer[1].strip()
                    
                    # Get the header from the mapping
                    header = QUESTION_HEADER_MAPPING.get(question)
                    if header:
                        data[header] = answer
                        logger.debug(f"Parsed question: {question}")
                        logger.debug(f"Parsed header: {header}")
                        logger.debug(f"Parsed answer: {answer}")
    
    # Log all found headers for debugging
    logger.info(f"Found responses for headers: {list(data.keys())}")
    
    # Check for missing headers and log them
    expected_headers = set(QUESTION_HEADER_MAPPING.values())
    found_headers = set(data.keys())
    missing_headers = expected_headers - found_headers
    
    if missing_headers:
        logger.warning(f"Missing responses for headers: {missing_headers}")
        # For missing headers, try to get their questions and log them too
        missing_questions = [reverse_mapping.get(h) for h in missing_headers]
        logger.warning(f"Corresponding missing questions: {missing_questions}")
    
    return data

def update_template(data: Dict[str, str], template_path: str) -> None:
    """
    Fill Excel template with standardized responses.
    """
    try:
        workbook = load_workbook(template_path)
        worksheet = workbook.active
        
        headers = [cell.value.strip() if cell.value else None for cell in worksheet[1]]
        next_row = get_next_empty_row(worksheet)
        
        logger.info(f"Found {len(headers)} headers in template")
        logger.info(f"Processing data for {len(data)} responses")
        
        # Log which headers were found in both template and data
        matching_headers = set(headers) & set(data.keys())
        logger.info(f"Found matching data for {len(matching_headers)} headers")
        
        # Update Excel with standardized responses
        cells_updated = 0
        for col, header in enumerate(headers, start=1):
            if header and header in data:
                standardized_response = standardize_response(data[header], header, data)
                worksheet.cell(row=next_row, column=col, value=standardized_response)
                cells_updated += 1
                logger.debug(f"Updated cell for header: {header}")
        
        logger.info(f"Updated {cells_updated} cells in template")
        
        # Identify and log headers that weren't updated
        missing_updates = [h for h in headers if h and h not in data]
        if missing_updates:
            logger.warning(f"No data found for these headers: {missing_updates}")
        
        workbook.save(template_path)
        logger.info(f"Template saved successfully at row {next_row}")
        
    except Exception as e:
        logger.error(f"Error updating template: {str(e)}")
        raise

def main(transcript_path: str, template_path: str) -> None:
    """
    End-to-end flow:
      1. Read transcript
      2. Generate responses for each question using the guidance
      3. Parse and standardize the responses
      4. Write formatted responses to Excel
    """
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OpenAI API key not found in environment variables")
        
    transcript_file = Path(transcript_path)
    template_file = Path(template_path)
    
    if not transcript_file.exists():
        raise FileNotFoundError(f"Transcript file not found: {transcript_path}")
    if not template_file.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
        
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    logger.info(f"Processing transcript: {transcript_path}")
    with open(transcript_file, 'r', encoding='utf-8') as file:
        transcript_text = file.read()
    
    # Process transcript and get initial responses
    output = process_transcript(transcript_text)
    
    # Convert the raw GPT output into a dictionary keyed by question header
    standardized_data = parse_output(output)
    
    # Update Excel template with standardized responses
    update_template(standardized_data, template_path)
    
    logger.info("Processing completed successfully!")

if __name__ == "__main__":
    # Example usage (replace these with your actual file paths)
    transcript_path = "path_to_your_transcript.txt"
    template_path = "path_to_your_template.xlsx"
    main(transcript_path, template_path)