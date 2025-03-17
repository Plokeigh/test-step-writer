from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class GapExample:
    """Example of a gap for a specific control and gap status"""
    control_id: str
    gap_status: str  # Updated to only allow "gap" or "informal process"
    gap_title: str
    gap_description: str
    recommendation: str
    application: Optional[str] = None  # Added to support application-specific examples

# Define standard gap examples based on common control gaps
# These will be used by the AI to generate similar gaps based on the input
GAP_EXAMPLES = [
    # Access Provisioning - Gap
    GapExample(
        control_id="APD-01",
        gap_status="gap",
        gap_title="Absence of Formalized Controls and Documentation for Access Provisioning",
        gap_description=(
            "Access provisioning is handled on an ad-hoc basis, where managers request access directly or "
            "provide access themselves without a formal process or oversight. New or modified user access requests "
            "are informally documented and approved by the appropriate personnel prior to users obtaining access to "
            "the application. This increases the risk of unauthorized access to the application and its data, potentially "
            "resulting in inappropriate access rights."
        ),
        recommendation=(
            "Implement a formally documented access provisioning policy with defined steps and completion timeframes: "
            "1. Develop a formally documented access provisioning policy with defined steps and completion timeframes "
            "2. Implement a ticketing system or standardized request form to track access requests and approvals "
            "3. Clearly define and enforce segregation of duties for access requests, approvals, and provisioning activities "
            "4. Standardize the approval workflow for different access types, specifying required approvers "
            "5. Conduct periodic reviews of the provisioning process for compliance and effectiveness "
            "6. Define regular user access recertification process to verify continued need of access granted rights "
            "7. Explore automation, such as HR system integration, to enhance efficiency and reduce manual errors"
        )
    ),
    
    # Access Provisioning - Informal Process
    GapExample(
        control_id="APD-01",
        gap_status="informal process",
        gap_title="Inconsistent Management of Access Provisioning Controls",
        gap_description=(
            "While access provisioning is handled on an ad-hoc basis, where Manager/Requestor "
            "manually edits or modifies user access based on payroll information without formal "
            "request, approval workflow, or a tracking system to track and document these changes. "
            "Currently, there is no standardized process to ensure consistent documentation, appropriate segregation of duties, or "
            "comprehensive review of access requirements before provisioning."
        ),
        recommendation=(
            "Formalize the existing access provisioning process by: "
            "1. Develop a formally documented access provisioning policy with defined steps and completion timeframes "
            "2. Implement a ticketing system or standardized request form to track access requests and approvals "
            "3. Clearly define and enforce segregation of duties for access requests, approvals, and provisioning activities "
            "4. Standardize the approval workflow for different access types, specifying required approvers "
            "5. Conduct periodic reviews of the provisioning process for compliance and effectiveness "
            "6. Define regular user access recertification process to verify continued need of access granted rights "
            "7. Explore automation, such as HR system integration, to enhance efficiency and reduce manual errors"
        )
    ),
    
    # Access Provisioning - Informal Process (Segregation of Duties)
    GapExample(
        control_id="APD-01",
        gap_status="informal process",
        gap_title="Access Provisioning Process Lacking Segregation of Duties",
        gap_description=(
            "The current access provisioning process includes proper approvals, but lacks adequate segregation of duties. "
            "The same administrator who provisions the access is also responsible for verifying approvals. "
            "This creates a potential conflict where access could be granted without proper oversight, potentially "
            "resulting in inappropriate access rights."
        ),
        recommendation=(
            "Enhance the access provisioning process by: "
            "1. Separating the duties of approval verification and account creation "
            "2. Implementing a secondary review of all access provisioning activities "
            "3. Configuring the ticketing system to enforce workflow steps "
            "4. Creating automated reports that identify any access granted outside the standard process "
            "5. Implementing regular reviews of access rights to ensure appropriate segregation of duties "
            "6. Documenting clear responsibilities for each role in the access provisioning process"
        )
    ),
    
    # Azure Access Provisioning - Informal Process
    GapExample(
        control_id="APD-01_Azure",
        gap_status="informal process",
        gap_title="Absence of Formalized Procedures and Controls for Azure Access",
        gap_description=(
            "While standard access to Azure is provisioned through HR processes and controls specifically for elevated access levels to mitigate handing: "
            "1. Absence of documented comprehensive detailed access management procedure "
            "2. Undefined development request path or tracking system for elevated access "
            "3. Inconsistent approval processes for elevated access changes and IT service leadership "
            "4. Manual standard Azure access is elevated through HR rather than formal procedures "
            "5. The absence of a formal elevated access provisioning process creates inconsistency in how access is requested, approved, and provisioned, increasing the risk of inappropriate or excessive access being granted."
        ),
        recommendation=(
            "1. Develop a formally documented comprehensive detailed access management procedure "
            "2. Implement a standardized request path or tracking system for elevated access "
            "3. Establish a formal approval workflow including direct managers and IT/infosec leadership "
            "4. Ensure that appropriate approvals are captured and retained "
            "5. Retain records of all access provisioning activities to maintain a reliable audit trail "
            "6. Provide training to all relevant stakeholders on the newly implemented processes "
            "7. Schedule quarterly reviews of access provisioning effectiveness and compliance"
        ),
        application="Azure"
    ),
    
    # Terminated User Access Removal - Gap
    GapExample(
        control_id="APD-02",
        gap_status="gap",
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
    
    # User Access Review - Informal Process
    GapExample(
        control_id="APD-04",
        gap_status="informal process",
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
    
    # Change Management - Gap
    GapExample(
        control_id="CM-01",
        gap_status="gap",
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
    
    # Integration Monitoring - Informal Process
    GapExample(
        control_id="MO-01",
        gap_status="informal process",
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
    
    # Backup Management - Informal Process
    GapExample(
        control_id="MO-02",
        gap_status="informal process",
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
    
    # SOC Report Review - Informal Process
    GapExample(
        control_id="ITELC-01",
        gap_status="informal process",
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
    examples = [
        example for example in GAP_EXAMPLES 
        if example.control_id == control_id and example.gap_status == gap_status
    ]
    
    if application:
        examples = [example for example in examples if example.application == application]
        
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
    examples = [example for example in GAP_EXAMPLES if example.control_id == control_id]
    
    if application:
        examples = [example for example in examples if example.application == application]
        
    return examples 