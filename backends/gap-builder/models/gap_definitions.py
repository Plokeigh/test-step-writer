from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class GapExample:
    """Example of a gap for a specific control and gap status"""
    control_id: str
    gap_status: str
    gap_title: str
    gap_description: str
    recommendation: str

# Define standard gap examples based on common control gaps
# These will be used by the AI to generate similar gaps based on the input
GAP_EXAMPLES = [
    # Access Provisioning - Not Implemented
    GapExample(
        control_id="APD-01",
        gap_status="Not Implemented",
        gap_title="Lack of Formal User Access Provisioning Process",
        gap_description=(
            "The organization has not established a formal user access provisioning process for the application. "
            "New user access is currently granted on an ad-hoc basis without consistent managerial approval or documentation. "
            "This increases the risk of unauthorized access to the application and its data."
        ),
        recommendation=(
            "Implement a formal user access provisioning process that includes the following elements: "
            "1. Standardized access request form or workflow "
            "2. Mandatory approval from the user's manager "
            "3. Secondary approval from the application owner "
            "4. Documentation of all approvals "
            "5. Regular audit of access provisioning activities"
        )
    ),
    
    # Access Provisioning - Partially Implemented
    GapExample(
        control_id="APD-01",
        gap_status="Partially Implemented",
        gap_title="Inconsistent Application of Access Approval Requirements",
        gap_description=(
            "While a formal user access provisioning process exists, it is not consistently followed. "
            "Approximately 30% of sampled access grants lacked documented manager approval. "
            "The system administrators sometimes provision access without verifying all required approvals "
            "are in place, especially for urgent requests."
        ),
        recommendation=(
            "Strengthen the existing access provisioning process by: "
            "1. Implementing system controls that prevent administrators from creating accounts without "
            "documented approvals "
            "2. Creating an expedited approval process for urgent requests that still maintains proper documentation "
            "3. Conducting quarterly reviews of access provisioning activities to ensure compliance "
            "4. Providing additional training to system administrators on the importance of following "
            "the approval process"
        )
    ),
    
    # Access Provisioning - Improvement Needed
    GapExample(
        control_id="APD-01",
        gap_status="Improvement Needed",
        gap_title="Access Provisioning Process Lacking Segregation of Duties",
        gap_description=(
            "The current access provisioning process includes proper approvals, but lacks adequate segregation of duties. "
            "The same administrator who provisions the access is also responsible for verifying approvals. "
            "This creates a potential conflict where access could be granted without proper oversight."
        ),
        recommendation=(
            "Enhance the access provisioning process by: "
            "1. Separating the duties of approval verification and account creation "
            "2. Implementing a secondary review of all access provisioning activities "
            "3. Configuring the ticketing system to enforce workflow steps "
            "4. Creating automated reports that identify any access granted outside the standard process"
        )
    ),
    
    # Terminated User Access Removal - Not Implemented
    GapExample(
        control_id="APD-02",
        gap_status="Not Implemented",
        gap_title="No Formal Process for Removing Terminated User Access",
        gap_description=(
            "The organization does not have a formal process for removing access for terminated employees. "
            "HR does not consistently notify IT of terminations, and there is no verification that access "
            "has been removed after termination. Testing identified 5 terminated employees that still had "
            "active accounts 30+ days after their termination date."
        ),
        recommendation=(
            "Develop and implement a terminated user access removal process that includes: "
            "1. Automated notification from HR to IT upon employee termination "
            "2. Required timeframe for access removal (typically 24-48 hours) "
            "3. Documentation of access removal actions "
            "4. Weekly reconciliation of terminated employees against active user accounts "
            "5. Quarterly review of the process effectiveness"
        )
    ),
    
    # User Access Review - Partially Implemented
    GapExample(
        control_id="APD-04",
        gap_status="Partially Implemented",
        gap_title="Incomplete User Access Reviews",
        gap_description=(
            "User access reviews are performed, but they do not include all system access types. "
            "Reviews focus on standard user accounts but exclude service accounts, administrative "
            "accounts, and temporary access. Additionally, there is limited documentation of "
            "access removal actions taken based on review findings."
        ),
        recommendation=(
            "Enhance the user access review process by: "
            "1. Expanding the scope to include all account types (standard, administrative, service, temporary) "
            "2. Creating a standardized template for reviewers to document their assessments "
            "3. Implementing a tracking mechanism for access changes identified during reviews "
            "4. Establishing timeframes for completing remediation actions "
            "5. Requiring evidence of completion for any access modifications"
        )
    ),
    
    # Change Management - Not Implemented
    GapExample(
        control_id="CM-01",
        gap_status="Not Implemented",
        gap_title="Absence of Formal Change Management Process",
        gap_description=(
            "The organization does not have a formal change management process for the application. "
            "Changes are implemented directly in production without consistent testing, documentation, "
            "or approval. This increases the risk of unintended system disruptions and unauthorized changes."
        ),
        recommendation=(
            "Implement a comprehensive change management process that includes: "
            "1. Change request documentation with business justification "
            "2. Risk assessment of proposed changes "
            "3. Testing requirements appropriate to the change risk level "
            "4. Approval requirements based on change impact "
            "5. Implementation planning including rollback procedures "
            "6. Post-implementation verification"
        )
    ),
    
    # Integration Monitoring - Improvement Needed
    GapExample(
        control_id="MO-01",
        gap_status="Improvement Needed",
        gap_title="Limited Monitoring of Critical System Interfaces",
        gap_description=(
            "The current monitoring of system interfaces is limited to detecting complete failures. "
            "There is no monitoring for partial failures, data quality issues, or performance degradation. "
            "Additionally, monitoring alerts are only sent to a general IT inbox rather than specific "
            "responsible individuals."
        ),
        recommendation=(
            "Enhance the interface monitoring capabilities by: "
            "1. Implementing data validation checks for critical interfaces "
            "2. Creating performance baseline metrics and monitoring for deviations "
            "3. Configuring alerts to be sent to specific responsible teams/individuals "
            "4. Developing escalation procedures for unresolved interface issues "
            "5. Implementing periodic interface reconciliation checks"
        )
    ),
    
    # Backup Management - Partially Implemented
    GapExample(
        control_id="MO-02",
        gap_status="Partially Implemented",
        gap_title="Inadequate Testing of System Backup Restoration",
        gap_description=(
            "While system backups are being performed regularly, there is limited testing of backup "
            "restoration capabilities. The organization has performed basic file-level restoration tests "
            "but has not conducted full system recovery testing to validate that complete restoration "
            "is possible in a disaster scenario."
        ),
        recommendation=(
            "Strengthen the backup management process by: "
            "1. Implementing a quarterly schedule for comprehensive restoration testing "
            "2. Developing specific test scenarios that validate critical system functionality after restoration "
            "3. Documenting restoration procedures with specific step-by-step instructions "
            "4. Creating success criteria for restoration tests to objectively evaluate results "
            "5. Addressing any issues identified during testing within defined timeframes"
        )
    ),
    
    # SOC Report Review - Improvement Needed
    GapExample(
        control_id="ITELC-01",
        gap_status="Improvement Needed",
        gap_title="Incomplete Vendor SOC Report Review Process",
        gap_description=(
            "The organization reviews vendor SOC reports, but does not adequately assess the impact of "
            "vendor control exceptions on the organization's control environment. Additionally, complementary "
            "user entity controls (CUECs) identified in the reports are not systematically evaluated to "
            "ensure they are implemented within the organization."
        ),
        recommendation=(
            "Enhance the SOC report review process by: "
            "1. Creating a standardized template for documenting review results, including vendor exceptions "
            "2. Implementing a process to assess the risk of each vendor exception to the organization "
            "3. Maintaining an inventory of required CUECs and mapping them to internal controls "
            "4. Establishing a tracking mechanism for remediation activities "
            "5. Requiring management signoff on the assessment of exceptions and CUEC implementation"
        )
    )
]

def find_gap_examples_by_control_and_status(control_id: str, gap_status: str) -> List[GapExample]:
    """
    Find gap examples that match the given control ID and gap status.
    
    Args:
        control_id: The ID of the control
        gap_status: The gap status to match
        
    Returns:
        A list of matching gap examples
    """
    return [
        example for example in GAP_EXAMPLES 
        if example.control_id == control_id and example.gap_status == gap_status
    ]

def find_gap_examples_by_control(control_id: str) -> List[GapExample]:
    """
    Find gap examples that match the given control ID.
    
    Args:
        control_id: The ID of the control
        
    Returns:
        A list of matching gap examples
    """
    return [example for example in GAP_EXAMPLES if example.control_id == control_id] 