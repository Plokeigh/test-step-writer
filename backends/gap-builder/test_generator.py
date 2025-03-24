import os
import sys
from services.gap_generator import GapGenerator

def test_recommendation_formatting():
    """
    Test the GapGenerator's recommendation formatting with the new REVIEW prefix.
    """
    # Create a test recommendation
    test_recommendation = """For the system(s) listed in column E, perform the following steps:

1. Develop a formally documented Salesforce access management policy.
2. Implement a standardized request form or ticketing system for all access requests, including additional access and role changes.
3. Establish a formal approval workflow involving direct managers and IT leadership for all access provisioning activities.
"""

    # Initialize the generator
    generator = GapGenerator()
    
    # Format the recommendation
    formatted = generator.format_recommendation(test_recommendation)
    
    # Print the result
    print("Original recommendation:")
    print(test_recommendation)
    print("\nFormatted recommendation:")
    print(formatted)
    
    # Check if REVIEW prefix is added correctly
    assert "REVIEW1." in formatted, "REVIEW1 prefix not found"
    assert "REVIEW2." in formatted, "REVIEW2 prefix not found"
    assert "REVIEW3." in formatted, "REVIEW3 prefix not found"
    
    print("Test passed! REVIEW prefixes successfully added.")

if __name__ == "__main__":
    test_recommendation_formatting() 