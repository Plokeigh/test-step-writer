from backend.services.matrix_generator import MatrixGenerator
import os
import sys

def main():
    # Debug information
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Initialize the generator
    generator = MatrixGenerator()
    
    # Path to your input scoping document
    input_file = "path/to/your/scoping_document.xlsx"
    
    # Generate the matrix
    matrix_wb = generator.process_scoping_document(input_file)
    
    # Save the output
    output_file = "risk_control_matrix.xlsx"
    matrix_wb.save(output_file)
    print(f"Matrix generated successfully and saved to {output_file}")

if __name__ == "__main__":
    main() 