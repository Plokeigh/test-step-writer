import csv
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Control:
    control_id: str
    short_name: str
    description: str
    key_control: bool
    control_type: str
    nature: str
    frequency: str
    scoping_headers: List[str]
    evaluation_criteria: str
    risk_id: str = ""
    risk_description: str = ""

    @staticmethod
    def select_control_variant(variants: List['Control'], scoping_info: str) -> 'Control':
        """Returns the most appropriate control variant based on the scoping information."""
        if not variants:
            raise ValueError("No control variants provided")
        if len(variants) == 1:
            return variants[0]
            
        # Create comparison text for each variant
        variant_texts = [
            f"Control: {v.short_name}\nCriteria: {v.evaluation_criteria}"
            for v in variants
        ]
        
        return variants[0]  # Placeholder - actual selection will be done by MatrixGenerator

    def __post_init__(self):
        if self.scoping_headers is None:
            self.scoping_headers = []
        
        # Process any semicolon-separated headers in the scoping_headers list
        # This ensures that headers like "Role Modification Capability; Role Review"
        # are properly expanded into separate entries
        processed_headers = []
        for header in self.scoping_headers:
            if isinstance(header, str) and ";" in header:
                # Split the semicolon-separated header into individual headers
                for sub_header in header.split(";"):
                    processed_headers.append(sub_header.strip())
            else:
                processed_headers.append(header)
        
        self.scoping_headers = processed_headers

# Define path for the CSV file relative to this script
CONTROLS_CSV_PATH = Path(__file__).parent / "standard_controls.csv"

def load_standard_controls_from_csv(file_path: Path) -> List[Control]:
    """Loads control definitions from a specified CSV file."""
    controls = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile: # Use utf-8-sig to handle BOM
            reader = csv.DictReader(csvfile)
            if not reader.fieldnames:
                 print(f"Warning: CSV file might be empty or missing headers: {file_path}")
                 return [] # Return empty list if no headers

            # Get expected field names from the dataclass
            expected_headers = Control.__annotations__.keys()

            for i, row in enumerate(reader):
                try:
                    # Handle boolean conversion for key_control
                    key_control_str = row.get('key_control', 'false').strip().lower()
                    key_control = key_control_str == 'true'

                    # Get scoping_headers. The __post_init__ will handle splitting if it's a single string.
                    # We pass it as a list containing the single string value from the CSV.
                    scoping_headers_val = row.get('scoping_headers', '')
                    scoping_headers_list = [scoping_headers_val] if scoping_headers_val else []

                    # Prepare data dictionary, filtering based on expected fields
                    control_data = {
                        field: row.get(field, '')
                        for field in expected_headers
                        if field not in ['key_control', 'scoping_headers'] # Handle these separately
                    }
                    control_data['key_control'] = key_control
                    control_data['scoping_headers'] = scoping_headers_list
                    
                    # Ensure all expected fields are present, providing defaults if necessary
                    for field in expected_headers:
                        if field not in control_data:
                            # Set a reasonable default (e.g., empty string, False for bool)
                            # This handles cases where a column might be missing in the CSV for a row
                            default_value = False if field == 'key_control' else [] if field == 'scoping_headers' else ''
                            control_data[field] = default_value
                            print(f"Warning: Missing value for '{field}' in row {i+1}. Using default: '{default_value}'")

                    controls.append(Control(**control_data))

                except Exception as e:
                     # Log error for the specific row but continue processing others
                     print(f"Error processing row {i+1} in {file_path}: {row}. Error: {e}")

    except FileNotFoundError:
        print(f"Error: Controls CSV file not found at {file_path}")
        # Critical error: Control definitions are required.
        raise FileNotFoundError(f"Required control definitions file not found: {file_path}")
    except Exception as e:
        # Catch other potential file reading errors (e.g., permissions, decoding)
        print(f"Error reading CSV file {file_path}: {e}")
        raise # Re-raise other critical errors

    return controls

# Load standard controls from the CSV file
STANDARD_CONTROLS = load_standard_controls_from_csv(CONTROLS_CSV_PATH)

# Removed the large hardcoded STANDARD_CONTROLS list
# Define standard controls based on the mapping table
# STANDARD_CONTROLS = [
#     # Access Provisioning
#     Control(
#         control_id="APD-01",
#         short_name="Access Provisioning - Automated Workflow",
# ... (rest of the list removed) ...
#         )
#     )
# ] # End of STANDARD_CONTROLS list   