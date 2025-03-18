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
        gap_title="Complete Absence of Access Provisioning Process and Controls",
        gap_description=(
            "The organization has no established process (formal or informal) for managing user access provisioning. "
            "Access is granted on a completely ad-hoc basis with no consistency, documentation, or oversight. "
            "There is no tracking of who requested access, who approved it, or when it was provisioned. "
            "No segregation of duties exists, and there are no controls to prevent or detect inappropriate access rights. "
            "This significantly increases the risk of unauthorized access to the application and its data, "
            "potentially resulting in data breaches, unauthorized transactions, or compliance violations."
        ),
        recommendation=(
            "Establish a comprehensive access provisioning process from scratch: "
            "1. Create a formal access provisioning policy with clearly defined procedures, roles, and timeframes "
            "2. Implement a ticketing system or standardized request form to track access requests and approvals "
            "3. Establish and enforce segregation of duties for access requests, approvals, and provisioning activities "
            "4. Define appropriate approval workflows for different access types, specifying required approvers "
            "5. Implement periodic reviews of the provisioning process to ensure effectiveness and compliance "
            "6. Establish a regular user access recertification process to verify continued need of access "
            "7. Explore automation opportunities, such as HR system integration, to enhance efficiency and reduce manual errors"
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
    
    # Terminated User Access Removal - Informal Process (JPMC-specific)
    GapExample(
        control_id="APD-02-JPMC",
        gap_status="informal process",
        gap_title="Absence of Formal Termination Procedure for System Access Removal",
        gap_description=(
            "The organization lacks a standardized, formalized process for removing system access upon employee termination, "
            "currently relying on informal email documentation. The termination notification process depends on manual HR communication "
            "to system administrators without a consistent, traceable workflow or ticketing system. While access is reported to be removed "
            "within three business days, there is no formal tracking mechanism to monitor compliance with this timeframe requirement. "
            "Additionally, evidence of access removal is inconsistently documented via screenshots, creating risks associated with unauthorized "
            "access from terminated employees."
        ),
        recommendation=(
            "Implement a standardized termination procedure by: "
            "1. Developing a formalized termination notification workflow clearly defining responsibilities of HR and system administrators. "
            "2. Deploying a centralized ticketing system for tracking and documenting termination notifications and access removal actions. "
            "3. Establishing formal tracking and monitoring procedures to ensure access removal occurs within three business days. "
            "4. Standardizing documentation to include termination date, notification date, removal date, administrator responsible, and evidence of completion. "
            "5. Conducting monthly reconciliations to verify no terminated users retain active system access. "
            "6. Ensuring evidence (screenshots, tickets, confirmation emails) is stored in a centralized and accessible repository for audit purposes. "
            "7. Providing periodic training for HR and system administrators on the new termination access removal processes."
        )
    ),
    
    # Terminated User Access Removal - Complete Gap
    GapExample(
        control_id="APD-02",
        gap_status="gap",
        gap_title="Complete Absence of Terminated User Access Removal Process",
        gap_description=(
            "The organization has no established process whatsoever for removing system access when employees are terminated. "
            "There is no communication between HR and IT regarding terminations, and no mechanism exists to identify or track "
            "terminated employees who still have active system access. Access removal is completely overlooked or forgotten unless "
            "someone happens to remember to manually request it. No documentation or verification of access removal occurs at any point. "
            "Testing revealed multiple terminated employees who retained active system access for months after their termination date, "
            "creating significant risks of unauthorized access, data breaches, and potential malicious activity from former employees."
        ),
        recommendation=(
            "Establish a comprehensive terminated user access removal process from scratch: "
            "1. Create a formal termination process policy outlining specific procedures, responsibilities, and timeframes for access removal "
            "2. Implement an automated notification system from HR to IT when employees are terminated "
            "3. Develop a tracking mechanism to monitor all terminations and verify access removal completion "
            "4. Establish a maximum timeframe (24-48 hours) for removing access after termination notification "
            "5. Implement a standard documentation protocol for recording termination date, notification date, and access removal actions "
            "6. Develop reconciliation procedures to regularly compare active user lists against employment records "
            "7. Create an escalation process for access removal that hasn't been completed within the defined timeframe "
            "8. Implement periodic audits to ensure the process is functioning effectively and no terminated users retain access"
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
    
    # Annual Role Permissions Review - Gap
    GapExample(
        control_id="APD-03",
        gap_status="gap",
        gap_title="Absence of Periodic Role and Permission Review Process",
        gap_description=(
            "The organization does not currently perform a periodic review of all roles and permissions within the system, "
            "despite having the capability to create and define system roles. There is no established process to "
            "confirm roles and permissions remain appropriate for business functions and comply with segregation of duties requirements. "
            "The organization lacks an established procedure for identifying inappropriate role configurations, creating remediation tickets, "
            "and performing validation procedures to resolve potential impacts. This increases the risk of inappropriate permissions over time "
            "as business processes and user responsibilities change."
        ),
        recommendation=(
            "Establish a formal annual role and permission review process with clear ownership and accountability for management oversight: "
            "1. Establish a formal annual role and permission review process with clear ownership and accountability for management oversight "
            "2. Develop a standardized review template that documents all system roles (particularly custom roles), their associated permissions, and their business justification "
            "3. Implement a process to regularly review system-provided role and permission listings with adequate HR information (terminated employees) "
            "4. Clearly define the scope and completion timeframe of the review "
            "5. Ensure validation that existing roles and permissions based on job functions and segregation of duties requirements "
            "6. Establish procedures for remediating identified inappropriate permissions, including ticket creation, implementation, and verification "
            "7. Implement feedback procedures to identify the potential impact of any inappropriate permissions discovered during the review process "
            "8. Ensure complete documentation, remediation activities, and verification evidence are centrally maintained and accessible for audit purposes "
            "9. Train system administrators and business owners on the role review process, emphasizing the importance of properly managing permissions"
        )
    ),
    
    # Annual Role Permissions Review - Informal Process
    GapExample(
        control_id="APD-03",
        gap_status="informal process",
        gap_title="Inadequate Annual Role and Permission Review Process",
        gap_description=(
            "On an annual basis, Management performs a review of the roles and permissions for the application to validate the permissions associated with each role are appropriate. If "
            "issues are identified during the assessment, Management communicates these findings via email to system administrators. However, the review process "
            "is entirely managed through email exchanges without formal documentation or centralized tracking. There is no standardized template used to document the review, "
            "and no ticketing system is utilized to track approval of role configurations or remediation efforts when issues are found. Evidence of the review and any subsequent "
            "actions taken are scattered across multiple email threads, making it difficult to verify completion or trace the history of identified issues. "
            "The reliance on email and lack of structured documentation significantly limits accountability, consistency, and the ability to demonstrate "
            "that appropriate oversight of system roles and permissions is maintained."
        ),
        recommendation=(
            "Formalize and enhance the existing role and permission review process by: "
            "1. Establish a formal annual role and permission review process with clear ownership and accountability for management oversight "
            "2. Develop a standardized review template that documents all system roles (particularly custom roles), their associated permissions, and their business justification "
            "3. Implement a ticketing system to formally document review findings, approvals, and track remediation efforts to completion "
            "4. Clearly define the scope and completion timeframe of the review "
            "5. Ensure validation that existing roles and permissions based on job functions and segregation of duties requirements "
            "6. Establish procedures for remediating identified inappropriate permissions, including ticket creation, implementation, and verification "
            "7. Implement feedback procedures to identify the potential impact of any inappropriate permissions discovered during the review process "
            "8. Ensure complete documentation, remediation activities, and verification evidence are centrally maintained and accessible for audit purposes "
            "9. Train system administrators and business owners on the role review process, emphasizing the importance of properly managing permissions"
        )
    ),

        # Quarterly User Access Review - Gap (Azure)
    GapExample(
        control_id="APD-04-Azure",
        gap_status="gap",
        gap_title="Absence of Quarterly User Access Review Process",
        gap_description=(
            "Management does not perform periodic user access reviews to validate the appropriateness of access to IT systems. "
            "Despite having the capability to create and manage user accounts and administrative privileges, "
            "there is no established process to periodically review whether existing access should be modified or removed. "
            "The organization lacks a process to identify inactive users, review accounts with elevated privileges, or validate that "
            "access is appropriate for users' current roles. Without regular reviews, inappropriate or excessive access may persist "
            "indefinitely, creating significant security risks and potential compliance violations."
        ),
        recommendation=(
            "Establish quarterly user access reviews with clear management ownership and responsibilities: "
            "1. Establish quarterly user access reviews with clear management ownership and responsibilities "
            "2. Generate comprehensive user access listings, including roles, permissions, and login activity "
            "3. Implement formal IT controls with documented evidence of report generation and validation "
            "4. Verify administrative access is appropriately limited to only users that require elevated privileges "
            "5. Include secondary reviews to independently validate the primary reviewer's access decisions "
            "6. Maintain remediation activities and verify timely implementation of access changes within three business days "
            "7. Maintain evidence of completed review and remediation verification "
            "8. Implement calendar-driven accountability measures ensuring timely quarterly reviews"
        ),
        application="Azure"
    ),
    
    # Quarterly User Access Review - Informal Process (Azure)
    GapExample(
        control_id="APD-04-Azure",
        gap_status="informal process",
        gap_title="Inadequate Quarterly User Access Review Process",
        gap_description=(
            "On a quarterly basis, Management performs a review of all users, including regular accounts and administrative accounts, with access to the Azure environment. The list of "
            "active users is reviewed to identify any inactive users whose access is to be revoked or users with inappropriate access levels that need to be modified or removed. "
            "When users with inappropriate access are identified, access is modified within 3 business days of identification, and if necessary, followup procedures are performed. "
            "However, this process is entirely managed through email exchanges without formal documentation or centralized tracking. There is no standardized template used to document the review, "
            "and no ticketing system is utilized to track remediation efforts when issues are found. Evidence of the review and any subsequent "
            "actions taken are scattered across multiple email threads, making it difficult to verify that inappropriate access is consistently identified and addressed within the required timeframe. "
            "The lack of structured documentation significantly limits accountability and the ability to demonstrate compliance with access control requirements."
        ),
        recommendation=(
            "Formalize and enhance the existing quarterly user access review process by: "
            "1. Establish quarterly user access reviews with clear management ownership and responsibilities "
            "2. Generate comprehensive user access listings, including roles, permissions, and login activity "
            "3. Implement formal IT controls with documented evidence of report generation and validation "
            "4. Verify administrative access is appropriately limited to only users that require elevated privileges "
            "5. Include secondary reviews to independently validate the primary reviewer's access decisions "
            "6. Maintain remediation activities and verify timely implementation of access changes within three business days "
            "7. Maintain evidence of completed review and remediation verification "
            "8. Implement calendar-driven accountability measures ensuring timely quarterly reviews"
        ),
        application="Azure"
    ),
    
    # Generic/Non-Human Accounts Management - Gap (Azure)
    GapExample(
        control_id="APD-05-Azure",
        gap_status="gap",
        gap_title="Absence of Secure Credential Management Controls for Privileged Generic Accounts",
        gap_description=(
            "Management has generic/non-human accounts within their IT systems, including a privileged IT Admin account that has elevated access rights which presents increased security risks. "
            "There is no formal inventory or documentation of these generic accounts, and no secure credential management practices are implemented. "
            "Passwords for these accounts are shared verbally or via email, with no consistent policies to track who has knowledge of them. "
            "Password changes are not required when personnel with knowledge of credentials leave the organization, and there is no formal process for managing, monitoring, or reviewing these privileged "
            "accounts. The organization lacks appropriate procedures for identifying outdated or unused generic accounts, and there is no audit trail for actions performed using the accounts. "
            "The absence of controls around these high-risk accounts creates significant security vulnerabilities that could lead to unauthorized access or system compromise."
        ),
        recommendation=(
            "Implement comprehensive controls for generic/non-human accounts: "
            "1. Complete a comprehensive inventory of generic accounts, including purpose, access level, and management practices "
            "2. Deploy secure credential management tools (such as CyberArk, Secret Server, or Keeper) "
            "3. Establish policies for justification, approval, credential rotation, and secure vault storage "
            "4. Implement unique credentials for each account and enforce strong password complexity limitations "
            "5. Monitor activity at privileged generic account activities to add fraud controls "
            "6. Periodically review generic account usage, confirming adherence to procedures and continued business justification "
            "7. Implement automated notification of password changes and establish credential rotation schedules "
            "8. Train personnel on credential management policies and secure handling practices"
        ),
        application="Azure"
    ),
    
    # Generic/Non-Human Accounts Management - Informal Process (Azure)
    GapExample(
        control_id="APD-05-Azure",
        gap_status="informal process",
        gap_title="Inadequate Management of Generic and Privileged Non-Human Accounts",
        gap_description=(
            "There are system / non-human accounts that are tracked and managed informally."
            "Basic rules are established based on business need and the passwords are locked"
            "within a vault management system. However, this process is inconsistent and not formalized. "
            "The password handling procedures are not well-documented, and IT staff rely on informal knowledge sharing to manage these credentials. "
            "When IT Admin account changes are needed, the 'Mag Day IT Manager has' access to the IT Admin account credentials which are stored in the history. This approach lacks the structure "
            "and controls needed for secure credential management, creating potential security vulnerabilities and accountability gaps."
        ),
        recommendation=(
            "Formalize and enhance the management of generic and privileged non-human accounts: "
            "1. Complete a comprehensive inventory of generic accounts, including purpose, access level, and management practices "
            "2. Deploy secure credential management tools (such as CyberArk, Secret Server, or Keeper) "
            "3. Establish policies for justification, approval, credential rotation, and secure vault storage "
            "4. Implement unique credentials for each account and enforce strong password complexity limitations "
            "5. Monitor activity at privileged generic account activities to add fraud controls "
            "6. Periodically review generic account usage, confirming adherence to procedures and continued business justification "
            "7. Implement automated notification of password changes and establish credential rotation schedules "
            "8. Train personnel on credential management policies and secure handling practices"
        ),
        application="Azure"
    ),
    
    # Monthly Administrator Activity Monitoring - Gap
    GapExample(
        control_id="APD-06",
        gap_status="gap",
        gap_title="Absence of Periodic Administrator Activity Review",
        gap_description=(
            "Management does not perform periodic reviews of administrator activity logs within NetSuite, despite the "
            "system maintaining logs of user activities that could be utilized for monitoring purposes. "
            "There is no established process to detect, review, or investigate direct data changes, transactions, "
            "and other privileged actions performed within the system. "
            "The organization lacks procedures to identify inappropriate administrator activities that could impact financial data integrity. "
            "Without regular reviews, unauthorized or erroneous administrator actions, including database modifications, system configuration changes, "
            "and access control alterations, may go undetected, creating significant security and data integrity risks."
        ),
        recommendation=(
            "Establish a formal monthly administrator activity review process with clear management oversight: "
            "1. Establish a formal, documented procedure for monthly reviews of NetSuite administrator activity logs "
            "2. Identify and designate specific individuals responsible for generating activity log reports and those responsible for reviewing them "
            "3. Implement a process to capture comprehensive logs of all administrator activities, including direct data changes, transactions, and other privileged actions "
            "4. Define thresholds and criteria to identify suspicious or unexpected administrative activities "
            "5. Develop a standardized review template that captures date, reviewer information, activities reviewed, and any findings "
            "6. Implement a process to investigate any unusual or unauthorized administrative activities identified during reviews "
            "7. Document all findings and remediation actions in a centralized repository accessible for audit purposes "
            "8. Maintain evidence of all reviews, including screenshots of activity logs reviewed, reviewer signoff, and resolution of identified issues "
            "9. Implement a calendar-driven approach to ensure timely completion of monthly reviews"
        )
    ),
    
    # Monthly Administrator Activity Monitoring - Informal Process
    GapExample(
        control_id="APD-06",
        gap_status="informal process",
        gap_title="Inadequate Monitoring of Administrator Activity Logs",
        gap_description=(
            "Administrator direct data changes, transactions, and activities are logged, and security "
            "teams review these logs on an informal basis when requested to identify any inappropriate "
            "activities which are then investigated. However, this review process is not formally "
            "documented or consistently performed on a periodic basis. There is no standardized template "
            "for documenting the review, and no formal procedures exist for identifying suspicious activities "
            "or escalating potential issues. The logs are not proactively monitored for unauthorized changes "
            "or privileged account misuse, and evidence of reviews is maintained inconsistently, typically in "
            "email communications rather than a structured repository or ticketing system."
        ),
        recommendation=(
            "Formalize and enhance the administrator activity monitoring process by: "
            "1. Establish a formal, documented procedure for monthly reviews of administrator activity logs "
            "2. Identify and designate specific individuals responsible for generating activity log reports and those responsible for reviewing them "
            "3. Implement a process to capture comprehensive logs of all administrator activities, including direct data changes, transactions, and other privileged actions "
            "4. Define thresholds and criteria to identify suspicious or unexpected administrative activities "
            "5. Develop a standardized review template that captures date, reviewer information, activities reviewed, and any findings "
            "6. Implement a process to investigate any unusual or unauthorized administrative activities identified during reviews "
            "7. Document all findings and remediation actions in a centralized repository accessible for audit purposes "
            "8. Maintain evidence of all reviews, including screenshots of activity logs reviewed, reviewer signoff, and resolution of identified issues "
            "9. Implement a calendar-driven approach to ensure timely completion of monthly reviews"
        )
    ),
    
    # Annual Password Configuration Review - Gap
    GapExample(
        control_id="APD-07-Non-SSO",
        gap_status="gap",
        gap_title="Absence of Annual Password Configuration Review Process for Non-SSO Systems",
        gap_description=(
            "Management does not perform periodic reviews of authentication configurations for non-SSO systems "
            "including Bit.com, Shopify, JPMC, Web Fargo, and NetSuite (PharPlus), as required by the company's "
            "information security policies. Though these systems have authentication capabilities, "
            "there is no formalized process to verify that password configurations in these systems align with the "
            "company's password policy requirements. No documentation exists to show that configurations are reviewed "
            "for minimum password length, complexity, expiration, and lockout settings. Without regular reviews, "
            "system password configurations may drift from security policy requirements over time, potentially leading "
            "to weaker security controls and increased risk of unauthorized access."
        ),
        recommendation=(
            "Establish a formal annual password configuration review process: "
            "1. Develop a formal, documented procedure for annual reviews of password configurations for all non-SSO systems "
            "2. Create a standardized template to document each system's current password parameters, including minimum length, "
            "complexity, expiration, and lockout settings "
            "3. Implement a process to validate that password settings support the requirements specified in the company's password policy "
            "4. Clearly document any discrepancies "
            "5. For vendor-provided applications where password settings cannot be directly configured, document the vendor's "
            "configuration and formally assess whether they provide consistent security protection "
            "6. Maintain evidence of the review through screenshots of system configurations, email correspondence with vendors, or "
            "report documentation "
            "7. Update the company's password policy, including business justification and compensating controls when required "
            "8. Implement a formal sign-off process requiring appropriate management approval of the annual authentication "
            "configuration assessment "
            "9. Establish a process to address and remediate any identified gaps between system configurations and password policy "
            "requirements"
        )
    ),
    
    # Annual Password Configuration Review - Informal Process
    GapExample(
        control_id="APD-07-Non-SSO",
        gap_status="informal process",
        gap_title="Inadequate Annual Password Configuration Review Process for Non-SSO Systems",
        gap_description=(
            "On an annual basis, at a scope was non-SSO application password configurations are "
            "informally reviewed by IT security personnel to the company's password policy and to confirm "
            "that no changes have been made to the configurations. However, this review process lacks formality "
            "and consistent documentation. While basic reviews occur, there is no standardized template to capture "
            "the specific password parameters for each system, and the assessment criteria for determining compliance "
            "with password policy are not clearly defined. Evidence of reviews is maintained inconsistently, and there "
            "is no formal sign-off procedure or tracking system to ensure all in-scope systems are evaluated. Additionally, "
            "there is no formal process to address and remediate identified configuration gaps when systems cannot meet "
            "policy requirements."
        ),
        recommendation=(
            "Formalize and enhance the existing password configuration review process by: "
            "1. Develop a formal, documented procedure for annual reviews of password configurations for all non-SSO systems "
            "2. Create a standardized template to document each system's current password parameters, including minimum length, "
            "complexity, expiration, and lockout settings "
            "3. Implement a process to validate that password settings support the requirements specified in the company's password policy "
            "4. Clearly document any discrepancies "
            "5. For vendor-provided applications where password settings cannot be directly configured, document the vendor's "
            "configuration and formally assess whether they provide consistent security protection "
            "6. Maintain evidence of the review through screenshots of system configurations, email correspondence with vendors, or "
            "report documentation "
            "7. Update the company's password policy, including business justification and compensating controls when required "
            "8. Implement a formal sign-off process requiring appropriate management approval of the annual authentication "
            "configuration assessment "
            "9. Establish a process to address and remediate any identified gaps between system configurations and password policy "
            "requirements"
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