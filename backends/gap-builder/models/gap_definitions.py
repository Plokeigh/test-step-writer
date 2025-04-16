import csv
from pathlib import Path
import logging
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

@dataclass
class GapExample:
    """Example of a gap for a specific control and gap status"""
    control_id: str
    gap_status: str  # Updated to only allow "gap" or "informal process"
    gap_title: str
    gap_description: str
    recommendation: str
    application: Optional[str] = None  # Added to support application-specific examples

# Define path for the CSV file relative to this script
GAP_EXAMPLES_CSV_PATH = Path(__file__).parent / "gap_examples.csv"

def load_gap_examples_from_csv(file_path: Path) -> List[GapExample]:
    """Loads gap example definitions from a specified CSV file."""
    examples = []
    try:
        # Use utf-8-sig to handle potential BOM (Byte Order Mark)
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                 logger.warning(f"Gap examples CSV file might be empty or missing headers: {file_path}")
                 return [] # Return empty list if no headers

            # Get expected field names from the dataclass annotations
            expected_headers = GapExample.__annotations__.keys()

            for i, row in enumerate(reader):
                try:
                    # Handle optional application field
                    # Provide default '' if key is missing, then check if it's empty
                    application_val = row.get('application', '')
                    # Convert empty string or explicitly "None" string to None type
                    if not application_val or application_val.strip().upper() == 'NONE':
                        application_val = None
                    else:
                        application_val = application_val.strip() # Clean up whitespace


                    # Prepare data dictionary, filtering based on expected fields
                    gap_data = {
                        # Provide default '' if key is missing
                        field: row.get(field, '').strip()
                        for field in expected_headers
                        if field != 'application' # Handle optional field separately
                    }
                    gap_data['application'] = application_val

                    # Ensure all required fields (non-optional) are present and not empty
                    missing_or_empty_fields = [
                        field for field in expected_headers
                        if field != 'application' and not gap_data.get(field)
                    ]
                    if missing_or_empty_fields:
                        logger.warning(f"Missing required value(s) for {missing_or_empty_fields} in row {i+1} of {file_path}. Skipping row: {row}")
                        continue # Skip row if required fields are missing or empty

                    examples.append(GapExample(**gap_data))

                except Exception as e:
                     # Log error for the specific row but continue processing others
                     logger.error(f"Error processing row {i+1} in {file_path}: {row}. Error: {e}", exc_info=True)

    except FileNotFoundError:
        logger.error(f"Error: Gap examples CSV file not found at {file_path}")
        # Critical error: Gap examples are required.
        raise FileNotFoundError(f"Required gap examples file not found: {file_path}")
    except Exception as e:
        # Catch other potential file reading errors (e.g., permissions, decoding)
        logger.error(f"Error reading CSV file {file_path}: {e}", exc_info=True)
        raise # Re-raise other critical errors

    return examples

# Load gap examples from the CSV file
GAP_EXAMPLES = load_gap_examples_from_csv(GAP_EXAMPLES_CSV_PATH)

# Define standard gap examples based on common control gaps
# These will be used by the AI to generate similar gaps based on the input
# GAP_EXAMPLES = [
# // ... existing code ...
# ]

# Update the find functions to accommodate application-specific filtering
def find_gap_examples_by_control_and_status(control_id: str, gap_status: str, application: Optional[str] = None) -> List[GapExample]:
    """
    Find gap examples that match the given control ID and gap status.
    
    Args:
        control_id: The ID of the control
        gap_status: The gap status to match (either "gap" or "informal process")
        application: Optional application name to filter by
        
    Returns:
        A list of matching gap examples
    """
    # Extract the base control ID (e.g., "APD-01" from "APD-01-Azure")
    base_control_id = control_id.split('-')
    if len(base_control_id) >= 2:
        base_control_id = f"{base_control_id[0]}-{base_control_id[1]}"
    else:
        base_control_id = control_id
        
    # Normalize gap status
    normalized_gap_status = gap_status.lower()
    if "informal" in normalized_gap_status or "partially" in normalized_gap_status:
        normalized_gap_status = "informal process"
    else:
        normalized_gap_status = "gap"
        
    examples = [
        example for example in GAP_EXAMPLES 
        if example.control_id == base_control_id and example.gap_status == normalized_gap_status
    ]
    
    if application:
        app_examples = [example for example in examples if example.application == application]
        # If there are application-specific examples, return those. Otherwise, fall back to the general examples.
        if app_examples:
            return app_examples
        
    return examples

def find_gap_examples_by_control(control_id: str, application: Optional[str] = None) -> List[GapExample]:
    """
    Find gap examples that match the given control ID.
    
    Args:
        control_id: The ID of the control
        application: Optional application name to filter by
        
    Returns:
        A list of matching gap examples
    """
    # Extract the base control ID (e.g., "APD-01" from "APD-01-Azure")
    base_control_id = control_id.split('-')
    if len(base_control_id) >= 2:
        base_control_id = f"{base_control_id[0]}-{base_control_id[1]}"
    else:
        base_control_id = control_id
        
    examples = [example for example in GAP_EXAMPLES if example.control_id == base_control_id]
    
    if application:
        app_examples = [example for example in examples if example.application == application]
        # If there are application-specific examples, return those. Otherwise, fall back to the general examples.
        if app_examples:
            return app_examples
        
    return examples 