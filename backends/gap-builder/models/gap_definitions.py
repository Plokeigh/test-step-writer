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
        gap_title="Absence of Access Provisioning Process and Controls",
        gap_description=(
            "The organization has no established process for managing user access provisioning. "
            "Access is granted on an ad-hoc basis with limited consistency, documentation, or oversight. "
            "There is a lack of tracking of access requests, approvals, or provisioning dates. "
            "Segregation of duties is not consistently enforced, and controls to prevent or detect inappropriate access rights are limited. "
            "This increases the risk of unauthorized access to the application and its data, "
            "potentially leading to data breaches, unauthorized transactions, or compliance violations."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Create a formally documented system access management policy "
            "2. Implement a ticketing system or standardized request form to track access requests and approvals "
            "3. Ensure that documented approvals are captured and retained for all access requests. "
            "4. Ensure that system screenshots confirming what access was granted are documented for all access requests "
            "5. Retain records of all access provisioning activities to maintain a reliable audit trail."
            "6. Provide training to all relevant stakeholders on the newly implemented processes."
            "7. Where possible consider establishing a formal approval workflow involving direct managers and system owners."
        )
    ),
    
    # Access Provisioning - Informal Process
    GapExample(
        control_id="APD-01",
        gap_status="informal process",
        gap_title="Absence of Formalized Process for Concur Access Provisioning",
        gap_description=(
            "We understand that all Company employees obtain standard access to the system for expense reporting purposes "
            "and that this standard access should not be considered in-scope for SOX purposes. Therefore, this control "
            "should apply to users requesting above standard access to the system. "
            "Management has an informal process for above standard access provisioning to the system, which is often documented via email, "
            "but lacks formally documented procedures and controls for requesting, approving, and provisioning above "
            "standard access within Concur. "
            "The absence of a formal access provisioning process can lead to inconsistencies in how access is requested, "
            "approved, and provisioned, increasing the risk of inappropriate or excessive access being granted without "
            "sufficient oversight."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Develop a formally documented system access management policy. "
            "2. Implement a standardized request form or ticketing system for above standard access requests. "
            "3. Establish a formal approval workflow involving direct managers and IT/Finance leadership. "
            "4. Ensure that specific roles / permissions are documented for all above standard access requests. "
            "5. Ensure that documented approvals are captured and retained for all above standard access requests. "
            "6. Ensure that system screenshots confirming what access was granted are documented for all above standard access requests. "
            "7. Retain records of all access provisioning activities to maintain a reliable audit trail. "
            "8. Provide training to all relevant stakeholders on the newly implemented processes."
        )
    ),
    
    # Terminated User Access Removal - Informal Process (JPMC-specific)
    GapExample(
        control_id="APD-02",  # Assuming APD-02 based on termination context; adjust if needed
        gap_status="informal process",
        gap_title="Absence of Formal Terminated Access Removal Process for JPMC",
        gap_description=(
            "The organization lacks a formalized process for removing system access upon employee termination, "
            "currently relying on informal email communication. "
            "The termination notification process relies on manual HR communication to system administrators "
            "without a consistent, traceable workflow or ticketing system. "
            "While access is generally removed within a reasonable timeframe, there is no formal tracking "
            "mechanism to monitor compliance consistently. "
            "Evidence of access removal is captured through screenshots, but the overall documentation process "
            "could benefit from more structure and centralized retention for audit purposes."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Develop a formally documented IT terminations access removal policy outlining specific "
            "responsibilities of HR, system administrators, and Company management in the access removal process. "
            "2. Implement a standardized ticketing system for all termination notifications to ensure "
            "consistent communication between HR and system administrators. "
            "3. Establish a formal documentation standard that includes termination date, notification date, "
            "removal date, administrator name, and verification evidence. This should include timestamped "
            "system screenshots confirming access removal for each user. "
            "4. Define escalation procedures for instances where access removal cannot be completed within "
            "the required three business days. "
            "5. Ensure all evidence (tickets, screenshots, confirmation emails) is stored in a centralized "
            "repository accessible for audit purposes. "
            "6. Provide training to all relevant stakeholders on the newly implemented processes."
        )
    ),
    
    # Terminated User Access Removal - Complete Gap
    GapExample(
        control_id="APD-02",  # Assuming APD-02 based on termination context; adjust if needed
        gap_status="gap",
        gap_title="Absence of Terminated Access Removal Process for JPMC",
        gap_description=(
            "The organization has no established process for removing system access upon "
            "employee termination. "
            "There is not a consistent method for notifying system administrators when employees leave the organization, "
            "which can result in delayed or missed access removals. "
            "No tracking mechanism exists to verify that access is removed within required timeframes, "
            "creating potential compliance risks and security vulnerabilities. "
            "Documentation of access removal actions is inconsistent, with limited evidence collection, "
            "verification procedures, or centralized record-keeping for audit purposes. "
            "This increases the risk of unauthorized system access by former employees, "
            "potentially leading to data breaches or unauthorized transactions."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Develop a formally documented IT terminations access removal policy outlining specific "
            "responsibilities of HR, system administrators, and Company management in the access removal process. "
            "2. Implement a standardized ticketing system for all termination notifications to ensure "
            "consistent communication between HR and system administrators. "
            "3. Establish a formal documentation standard that includes termination date, notification date, "
            "removal date, administrator name, and verification evidence. This should include timestamped "
            "system screenshots confirming access removal for each user. "
            "4. Define escalation procedures for instances where access removal cannot be completed within "
            "the required three business days. "
            "5. Ensure all evidence (tickets, screenshots, confirmation emails) is stored in a centralized "
            "repository accessible for audit purposes. "
            "6. Provide training to all relevant stakeholders on the newly implemented processes."
        )
    ),

    # Annual Role Permissions Review - Gap
    GapExample(
        control_id="APD-03",
        gap_status="gap",
        gap_title="Absence of Annual Roles Permissions Review for Azure",
        gap_description=(
            "Management is not currently performing a consistent annual review of all actively held roles and their permissions "
            "within Azure, despite having a defined control objective to ensure that permissions associated "
            "with each role remain appropriate. "
            "While the Company currently uses primarily out-of-the-box roles, the absence of a periodic review presents a risk, as even "
            "predefined roles may grant access that becomes inappropriate over time as business requirements and user "
            "responsibilities change. "
            "Without regular reviews, it can be challenging to identify potential segregation of duties "
            "conflicts or excessive permissions that may exist within the roles being used in Azure."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal annual roles permissions review process, assigning clear ownership to qualified personnel. "
            "2. Create review templates for documenting roles permissions reviews and for evidencing completion each review period. "
            "3. Maintain a complete inventory of roles within the application, including standard and custom roles. "
            "4. Document role purposes, permissions, and user assignments to assess appropriateness and segregation of duties. "
            "5. Implement management sign-off to certify the annual review completion and remediation. "
            "6. Address identified issues through formal remediation actions (ticketing, lookbacks, corrective actions). "
            "7. Schedule recurring reviews and consider additional frequency for high-risk roles."
        )
    ),
    
    # Annual Role Permissions Review - Informal Process
    GapExample(
        control_id="APD-03",
        gap_status="informal process",
        gap_title="Informal Annual Roles Permissions Review Process for Azure",
        gap_description=(
            "Management conducts occasional reviews of Azure roles and permissions, but lacks a "
            "formalized, documented annual review process with consistent scheduling and methodology. "
            "While some review activities occur, they are performed inconsistently without standardized "
            "templates, complete role inventories, or formal documentation requirements. "
            "The current informal approach relies more on individual knowledge than established "
            "procedures, which can lead to inconsistencies in review scope and thoroughness. "
            "Evidence collection is somewhat limited and lacks standardization, making it more challenging to demonstrate "
            "the effectiveness and completeness of reviews during audit examinations. "
            "Without a more structured approach, the assessment of segregation of duties risks "
            "and potential excessive permissions within the Azure environment may be inconsistent."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal annual roles permissions review process, assigning clear ownership to qualified personnel. "
            "2. Create review templates for documenting roles permissions reviews and for evidencing completion each review period. "
            "3. Maintain a complete inventory of roles within the application, including standard and custom roles. "
            "4. Document role purposes, permissions, and user assignments to assess appropriateness and segregation of duties. "
            "5. Implement management sign-off to certify the annual review completion and remediation. "
            "6. Address identified issues through formal remediation actions (ticketing, lookbacks, corrective actions). "
            "7. Schedule recurring reviews and consider additional frequency for high-risk roles."
        )
    ),

        # Quarterly User Access Review - Gap (Azure)
    GapExample(
        control_id="APD-04",
        gap_status="gap",
        gap_title="Absence of Quarterly User Access Reviews for Azure",
        gap_description=(
            "Management does not currently perform quarterly user access reviews to validate the appropriateness of access "
            "to in-scope IT applications for all active users, including non-human and admin accounts. "
            "Without a formal review process, there isn't a systematic way to identify inactive users whose "
            "access should be revoked or users with inappropriate access levels that need modification or removal. "
            "The lack of regular access reviews increases the risk that unauthorized or excessive access may persist, "
            "potentially allowing individuals to perform inappropriate transactions "
            "or access sensitive data. "
            "There isn't an established process for tracking, documenting, and remediating identified access issues, "
            "including the execution of lookback procedures when inappropriate access is discovered."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal quarterly user access review process with clear definitions of management ownership and responsibilities. "
            "2. Create review templates to document these application user access reviews, including assessments of inactive, inappropriate, or terminated accounts. "
            "3. Generate application user access listings, including all active users, their roles / permissions, and if possible, their account creation and last login dates. "
            "4. Implement formal IPE procedures involving the documentation of report generation / query evidence. "
            "5. Ensure that these reviews include secondary reviews to independently evaluate the primary reviewer's access. "
            "6. Formalize remediation / lookback procedures and define timeframes for the implementation of access changes. "
            "7. Implement calendar-driven accountability measures ensuring timely quarterly reviews."
        )
    ),
    
    # Quarterly User Access Review - Informal Process (Azure)
    GapExample(
        control_id="APD-04",
        gap_status="informal process",
        gap_title="Informal Quarterly User Access Reviews for Azure",
        gap_description=(
            "Management performs occasional reviews of user access in Azure, but lacks a formalized, "
            "documented quarterly review process with consistent scheduling and methodology. "
            "While some user access verification activities occur, they are performed inconsistently without "
            "standardized templates, complete user inventories, or formal documentation requirements. "
            "The current informal approach may not comprehensively cover all user types, including non-human "
            "accounts and administrative users, creating potential security gaps. "
            "Evidence collection is limited and lacks standardization, making it challenging to demonstrate "
            "the effectiveness and completeness of reviews during audit examinations. "
            "Remediation of identified access issues occurs on an ad-hoc basis without consistent tracking, "
            "defined timeframes for resolution, or formal lookback procedures to assess potential impacts."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal quarterly user access review process with clear definitions of management ownership and responsibilities. "
            "2. Create review templates to document these application user access reviews, including assessments of inactive, inappropriate, or terminated accounts. "
            "3. Generate application user access listings, including all active users, their roles / permissions, and if possible, their account creation and last login dates. "
            "4. Implement formal IPE procedures involving the documentation of report generation / query evidence. "
            "5. Ensure that these reviews include secondary reviews to independently evaluate the primary reviewer's access. "
            "6. Formalize remediation / lookback procedures and define timeframes for the implementation of access changes. "
            "7. Implement calendar-driven accountability measures ensuring timely quarterly reviews."
        )
    ),
    
    # Generic/Non-Human Accounts Management - Gap (Azure)
    GapExample(
        control_id="APD-05",
        gap_status="gap",
        gap_title="Absence of Formalized Controls for Generic/Non-Human Account Management for NetSuite",
        gap_description=(
            "Management utilizes generic/non-human accounts within this system, which warrants careful management. "
            "The credentials for the non-human account(s) are not currently stored in a secure credential management "
            "solution (vault system), but are instead known by individual Company employees. "
            "This approach to credential management increases security risks, including the potential "
            "for unauthorized access if the individual(s) with knowledge of the credentials leaves the organization "
            "or becomes unavailable. It also makes accountability and establishing an audit trail for actions performed "
            "using the account more challenging."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Maintain a complete inventory of generic / non-human accounts, including purpose, access level, password knowledge, and management practices. "
            "2. Deploy a secure credential management (vault) solution such as LastPass, CyberArk, Secret Server, or Keeper. "
            "3. Ensure that access to the vaults where generic account credentials are stored is appropriately limited. "
            "4. Periodically review generic accounts, confirming adherence to procedures and continued business justification. This can be done as part of the quarterly user access reviews. "
            "5. Train personnel on credential management policies and secure handling practices."
        )
    ),
    
    # Generic/Non-Human Accounts Management - Informal Process (Azure)
    GapExample(
        control_id="APD-05",
        gap_status="informal process",
        gap_title="Informal Controls for Generic/Non-Human Account Management for NetSuite",
        gap_description=(
            "Management has established generic/non-human accounts within NetSuite with some informal "
            "controls, but lacks a comprehensive and formalized approach to their management. "
            "While there is some awareness of which employees know these account credentials, the sharing and "
            "tracking of this information occurs through informal channels without consistent documentation. "
            "Some basic password management practices exist, but credentials are not consistently stored in a "
            "secure credential management solution (vault system), increasing potential security vulnerabilities. "
            "There is limited monitoring of generic account usage and no formal periodic review process to "
            "validate the continued business need and appropriate configuration of these accounts. "
            "This inconsistent approach to credential management increases security risks and challenges "
            "in establishing accountability for actions performed using these accounts."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Maintain a complete inventory of generic / non-human accounts, including purpose, access level, password knowledge, and management practices. "
            "2. Deploy a secure credential management (vault) solution such as LastPass, CyberArk, Secret Server, or Keeper. "
            "3. Ensure that access to the vaults where generic account credentials are stored is appropriately limited. "
            "4. Periodically review generic accounts, confirming adherence to procedures and continued business justification. This can be done as part of the quarterly user access reviews. "
            "5. Train personnel on credential management policies and secure handling practices."
        )
    ),
    
    # Monthly Administrator Activity Monitoring - Gap
    GapExample(
        control_id="APD-06",
        gap_status="gap",
        gap_title="Absence of Monthly Admin Activity Log Reviews for Bill.com",
        gap_description=(
            "Management does not currently perform periodic reviews of administrator activity logs within Bill.com, "
            "although the system has the capability to generate these logs. "
            "There isn't a formalized process for generating, assessing, and documenting the review of administrative "
            "activities such as direct data changes, transactions, and other privileged actions performed within Bill.com. "
            "Without periodic reviews of administrator activity logs, the ability to identify, "
            "investigate, and resolve potentially inappropriate administrative actions in a timely manner is limited."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal process for the monthly review of Bill.com administrator activity logs. "
            "2. Create review templates to document these monthly admin activity reviews, including assessments of inappropriate actions. "
            "3. Determine which specific admin activities should be monitored (e.g., configuration changes, direct data modifications, user access changes). "
            "4. Generate admin activity logs, including all active admins and their activities within the review period. "
            "5. Implement formal IPE procedures, involving the documentation of report generation / query evidence. "
            "6. Ensure that these reviews include secondary reviews to independently evaluate the primary reviewer's activities. "
            "7. Formalize remediation / lookback procedures and define timeframes for the implementation of access changes. "
            "8. Implement calendar-driven accountability measures ensuring timely monthly reviews."
        )
    ),
    
    # Monthly Administrator Activity Monitoring - Informal Process
    GapExample(
        control_id="APD-06",
        gap_status="informal process",
        gap_title="Informal Monthly Admin Activity Log Reviews for Bill.com",
        gap_description=(
            "Management occasionally reviews administrator activity logs within Bill.com on an ad-hoc basis, "
            "but lacks a formalized, consistent process for these reviews. "
            "While some administrator activity monitoring occurs, it is performed without standardized templates, "
            "documented procedures, or consistent scheduling, making it harder to ensure completeness. "
            "The current informal approach to log review lacks clear definition of which specific administrative "
            "actions should be monitored and lacks formal documentation of the review process and findings. "
            "Evidence collection is somewhat limited and inconsistent, creating challenges in demonstrating the "
            "effectiveness of monitoring activities during audit examinations. "
            "Investigation and remediation of identified issues occurs on an ad-hoc basis without formal "
            "tracking, defined timeframes for resolution, or documentation requirements."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal process for the monthly review of Bill.com administrator activity logs. "
            "2. Create review templates to document these monthly admin activity reviews, including assessments of inappropriate actions. "
            "3. Determine which specific admin activities should be monitored (e.g., configuration changes, direct data modifications, user access changes). "
            "4. Generate admin activity logs, including all active admins and their activities within the review period. "
            "5. Implement formal IPE procedures, involving the documentation of report generation / query evidence. "
            "6. Ensure that these reviews include secondary reviews to independently evaluate the primary reviewer's activities. "
            "7. Formalize remediation / lookback procedures and define timeframes for the implementation of access changes. "
            "8. Implement calendar-driven accountability measures ensuring timely monthly reviews."
        )
    ),
    
    # Annual Password Configuration Review - Gap
    GapExample(
        control_id="APD-07",
        gap_status="gap",
        gap_title="Absence of Annual Authentication Configuration Reviews",
        gap_description=(
            "Management does not currently perform annual reviews of authentication configurations, including password "
            "settings for non-SSO systems and SSO integration configurations for SSO-enabled applications. "
            "There isn't a formalized process to verify that these authentication configurations align with "
            "the organization's security standards and that no unauthorized changes have occurred. "
            "Without regular reviews, there is less assurance that password settings and SSO configurations "
            "maintain compliance with the company's security policies over time, potentially leading to "
            "weakened security controls. "
            "There isn't a formal IT authentication policy documented and maintained by Company Management "
            "that addresses both password requirements and SSO implementation standards."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Create a formal Company IT Authentication Policy document that addresses both password configurations and SSO implementations, to be reviewed annually. "
            "2. Establish a formal process for the annual review of both non-SSO password configurations and SSO integration settings. "
            "3. Create review templates to document these annual authentication configuration reviews. "
            "4. For non-SSO systems, review specific settings including: minimum character length, complexity requirements, lockout policies, password history, and multi-factor authentication settings. "
            "5. For SSO-enabled systems, review identity provider configurations, certificate expirations, authentication protocols, and user attribute mappings. "
            "6. Document system screenshots of all current authentication configurations. All screenshots should show the date / time. "
            "7. Define procedures for the handling of settings that don't adhere to the authentication policy but cannot be modified by Company. "
            "8. Implement calendar-driven accountability measures ensuring timely annual reviews."
        )
    ),
    
    # Annual Password Configuration Review - Informal Process
    GapExample(
        control_id="APD-07",
        gap_status="informal process",
        gap_title="Informal Annual Authentication Configuration Reviews",
        gap_description=(
            "Management occasionally checks authentication configurations, including password settings for "
            "non-SSO systems and SSO integration configurations for SSO-enabled applications, but lacks a "
            "formalized, documented review process with consistent scheduling and methodology. "
            "While some verification of password and SSO settings occurs, it is performed without standardized "
            "templates, consistent documentation, or reference to a formal IT authentication policy. "
            "The current informal approach relies more on individual knowledge than established procedures, "
            "creating potential inconsistency in review scope and thoroughness across different authentication methods. "
            "Evidence collection is limited and lacks standardization, making it more challenging to demonstrate "
            "that authentication configurations maintain compliance with security standards over time. "
            "The company has some general authentication guidelines, but lacks a comprehensive, formally documented "
            "IT authentication policy that would provide clear standards for both password and SSO configuration reviews."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Create a formal Company IT Authentication Policy document that addresses both password configurations and SSO implementations, to be reviewed annually. "
            "2. Establish a formal process for the annual review of both non-SSO password configurations and SSO integration settings. "
            "3. Create review templates to document these annual authentication configuration reviews. "
            "4. For non-SSO systems, review specific settings including: minimum character length, complexity requirements, lockout policies, password history, and multi-factor authentication settings. "
            "5. For SSO-enabled systems, review identity provider configurations, certificate expirations, authentication protocols, and user attribute mappings. "
            "6. Document system screenshots of all current authentication configurations. All screenshots should show the date / time. "
            "7. Define procedures for the handling of settings that don't adhere to the authentication policy but cannot be modified by Company. "
            "8. Implement calendar-driven accountability measures ensuring timely annual reviews."
        )
    ),
    
    # Change Management - Gap
    GapExample(
        control_id="CM-01",
        gap_status="gap",
        gap_title="Absence of Formal Change Management Processes for Concur",
        gap_description=(
            "Management lacks a formal, documented change management process for the Concur system, leading "
            "to primarily ad-hoc modifications to workflow configurations and approval routing without consistent oversight "
            "or control. "
            "There isn't a standardized request process or ticketing system to document and track changes before "
            "they are implemented in the production environment. "
            "Changes are sometimes made directly in the production environment without prior testing in a non-production "
            "environment, increasing the risk of unintended consequences that could impact financial data integrity. "
            "Management does not consistently maintain evidence of testing or formal approvals prior to implementing changes, "
            "hindering the validation that changes function as intended and are appropriately authorized."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Develop a formal change management policy specific to Concur workflow modifications and approval routing changes. "
            "2. Implement a standardized change request process using a ticketing system to formally document all Concur changes. "
            "3. Establish a non-production environment for testing Concur changes prior to deployment in production. "
            "4. Define appropriate testing requirements and standards to validate that changes function as intended before deployment. "
            "5. Implement an approval workflow requiring documented sign-off from relevant stakeholders before any change is deployed to production. "
            "6. Ensure segregation of duties by preventing individuals from both developing and deploying their own changes without independent review. "
            "7. Maintain documentation of all change requests, test results, approvals, and implementations for audit purposes."
        )
    ),

    GapExample(
    control_id="CM-01",
    gap_status="informal process",
    gap_title="Informal Change Management Processes for Concur",
    gap_description=(
        "Management follows an informal, often undocumented change management process for the Concur system, "
        "relying primarily on email communications and verbal approvals for workflow configurations and "
        "approval routing changes. "
        "While some change requests may be documented, there is no standardized process or centralized "
        "tracking system to ensure consistency and completeness in how changes are requested, approved, "
        "and implemented. "
        "Limited testing of changes may occur, but it is conducted inconsistently and without formal "
        "testing procedures or documentation standards to fully validate that changes function as intended. "
        "Approval for changes is often obtained informally, sometimes through email or verbal confirmation, but "
        "lacks a structured workflow with clearly defined roles and responsibilities for authorization. "
        "Documentation of changes is maintained inconsistently, making it more difficult to establish a "
        "complete audit trail of modifications to the production environment."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Develop a formal change management policy specific to Concur workflow modifications and approval routing changes. "
        "2. Implement a standardized change request process using a ticketing system to formally document all Concur changes. "
        "3. Establish a non-production environment for testing Concur changes prior to deployment in production. "
        "4. Define appropriate testing requirements and standards to validate that changes function as intended before deployment. "
        "5. Implement an approval workflow requiring documented sign-off from relevant stakeholders before any change is deployed to production. "
        "6. Ensure segregation of duties by preventing individuals from both developing and deploying their own changes without independent review. "
        "7. Maintain documentation of all change requests, test results, approvals, and implementations for audit purposes."
    )
),

    GapExample(
    control_id="CM-02",
    gap_status="gap",
    gap_title="Absence of Separate Environment for Concur",
    gap_description=(
        "Management does not currently have a separate pre-production environment established for Concur, "
        "which limits the ability to properly test changes before implementing them in the "
        "production environment. "
        "Configuration changes, workflow modifications, and approval routing updates are often made directly "
        "in the production environment without prior testing in a separate instance. "
        "The absence of a separate pre-production environment increases the risk of unintended "
        "consequences when making changes, potentially affecting financial data integrity and system functionality. "
        "Without a separate testing environment, it is challenging to validate that changes will function "
        "as intended before they impact end users and business operations."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Collaborate with Concur to establish a separate pre-production environment for testing purposes. "
        "2. Document the configuration and setup of the pre-production environment to ensure it appropriately "
        "mirrors the production environment. "
        "3. Develop procedures to ensure that all significant changes are first implemented and tested in the "
        "pre-production environment before deployment to production. "
        "4. Establish a process for refreshing the pre-production environment regularly to maintain alignment "
        "with the production environment. "
        "5. Implement change management procedures that require documented testing in the pre-production "
        "environment before changes can be approved for production deployment. "
        "6. Train relevant personnel on the proper use of the pre-production environment for testing purposes."
    )
),

    GapExample(
    control_id="CM-02",
    gap_status="informal process",
    gap_title="Underutilized Separate Environment for Concur",
    gap_description=(
        "Management has established a separate pre-production environment for Concur, but it is not "
        "consistently utilized for testing changes before implementing them in the production environment. "
        "The pre-production environment exists but is infrequently used, with many configuration changes, "
        "workflow modifications, and approval routing updates still being made directly in the production environment. "
        "The pre-production environment may not be regularly refreshed to mirror the production environment, "
        "which can diminish its value as a testing platform since it might not accurately reflect "
        "current production configurations. "
        "Without consistent utilization of the existing pre-production environment, the organization cannot "
        "effectively validate that changes will function as intended before they impact end users and "
        "business operations, creating unnecessary risk to financial data integrity and system functionality."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Develop formal procedures requiring the use of the existing pre-production environment for testing "
        "all significant changes before deployment to production. "
        "2. Establish a regular schedule to refresh the pre-production environment to ensure it accurately "
        "reflects the current production configuration. "
        "3. Document the configuration and setup of the pre-production environment to confirm it appropriately "
        "mirrors the production environment. "
        "4. Update change management procedures to require documented testing in the pre-production "
        "environment before changes can be approved for production deployment. "
        "5. Implement monitoring to ensure compliance with the requirement to use the pre-production "
        "environment for testing. "
        "6. Train relevant personnel on the proper use of the pre-production environment for testing purposes."
    )
),

    GapExample(
    control_id="CM-03",
    gap_status="gap",
    gap_title="Absence of Monthly Change Review Process for NetSuite",
    gap_description=(
        "Management does not currently perform periodic reviews of changes deployed to the NetSuite production "
        "environment, creating a risk that unauthorized or untested modifications may go undetected. "
        "Without a periodic review process, management cannot easily verify that all changes were properly "
        "requested, tested, and approved prior to implementation in the production environment. "
        "The organization lacks a formalized escalation and resolution procedure to address unauthorized changes "
        "that might be identified during reviews, potentially allowing improper changes to remain in the "
        "production environment."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Establish a formal monthly review process to validate all changes deployed to the NetSuite production environment. "
        "2. Create review templates to document these monthly change reviews, including assessments of unauthorized changes. "
        "3. Determine which change types should be monitored (the following should be included for NetSuite: configuration, workflow, integration, bundle audit trail, and script changes). "
        "4. Generate the respective change logs, including users who made each change, change date, change type. etc. "
        "5. Implement formal IPE procedures, involving the documentation of report generation / query evidence. "
        "6. Ensure that these reviews include secondary reviews to independently evaluate the primary reviewer's changes. "
        "7. Formalize remediation / lookback procedures. "
        "8. Implement calendar-driven accountability measures ensuring timely monthly reviews."
    )
),

    GapExample(
    control_id="CM-03",
    gap_status="informal process",
    gap_title="Informal Monthly Change Review Process for NetSuite",
    gap_description=(
        "Management occasionally reviews changes deployed to the NetSuite production environment, but "
        "lacks a formalized, documented monthly review process with consistent scheduling and methodology. "
        "While some monitoring of deployed changes occurs, it is performed without standardized templates, "
        "consistent coverage of all relevant change types, or formal documentation requirements. "
        "The current informal approach relies more on individual knowledge than established "
        "procedures, potentially creating inconsistency in review scope and thoroughness. "
        "Evidence collection is somewhat limited and lacks standardization, making it more challenging to demonstrate "
        "the effectiveness and completeness of reviews during audit examinations. "
        "The organization has an inconsistent approach to addressing unauthorized changes when identified, "
        "without formal escalation procedures or documentation requirements for resolution activities."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Establish a formal monthly review process to validate all changes deployed to the NetSuite production environment. "
        "2. Create review templates to document these monthly change reviews, including assessments of unauthorized changes. "
        "3. Determine which change types should be monitored (the following should be included for NetSuite: configuration, workflow, integration, bundle audit trail, and script changes). "
        "4. Generate the respective change logs, including users who made each change, change date, change type. etc. "
        "5. Implement formal IPE procedures, involving the documentation of report generation / query evidence. "
        "6. Ensure that these reviews include secondary reviews to independently evaluate the primary reviewer's changes. "
        "7. Formalize remediation / lookback procedures. "
        "8. Implement calendar-driven accountability measures ensuring timely monthly reviews."
    )
),

    GapExample(
    control_id="CM-04",
    gap_status="gap",
    gap_title="Absence of Vendor Change Management Process for Concur",
    gap_description=(
        "Management has not established a formal process to document, test, and approve critical releases, "
        "patches, or upgrades from Concur (SaaS provider) before they are implemented in the production "
        "environment. "
        "There isn't a ticketing system or other formal documentation method used to track vendor-initiated changes "
        "to the Concur application, resulting in reduced visibility into system modifications. "
        "Management does not typically perform testing of vendor updates in a non-production environment prior to "
        "implementation, increasing the risk that changes could negatively impact financial data integrity "
        "or system functionality. "
        "The organization has not implemented an approval workflow requiring business owner sign-off for "
        "vendor-initiated changes before they are deployed to the production environment."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Develop a formal vendor change management policy specific to Concur updates, patches, and releases. "
        "2. Implement a ticketing system to document all vendor-initiated changes, including release notes, impact, and change timeline. "
        "3. Request a sandbox or test environment from Concur to evaluate updates prior to migration to the production environment. "
        "4. Develop testing procedures to validate that vendor changes function as intended. "
        "5. Implement a formal approval process requiring business owner sign-off before vendor changes are deployed to production. "
        "6. Maintain documentation of all vendor change notifications, testing results, approvals, and implementations. "
        "7. Establish a post-implementation verification process to confirm vendor changes were successfully deployed without issue. "
        "8. Create a communication process to notify end users about significant vendor updates and any potential impacts."
    )
),

    GapExample(
    control_id="CM-04",
    gap_status="informal process",
    gap_title="Informal Vendor Change Management Process for Concur",
    gap_description=(
        "Management has an informal approach to handling Concur (SaaS provider) updates, patches, and releases, "
        "primarily relying on vendor notifications without a structured process for documentation and review. "
        "While vendor change notifications are received, they are not consistently documented in a ticketing "
        "system or centralized repository, creating challenges in tracking system modifications over time. "
        "Limited testing of vendor updates may occur on an ad-hoc basis, but lacks formal testing procedures "
        "and documentation standards to fully validate that changes will function as intended in the production environment. "
        "Approval for vendor changes is often obtained informally, perhaps through email or verbal confirmation, but "
        "lacks a structured workflow with clearly defined roles and responsibilities for authorization. "
        "The organization has some awareness of upcoming vendor changes but lacks a comprehensive approach "
        "to managing and documenting the entire vendor change lifecycle from notification to post-implementation review."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Develop a formal vendor change management policy specific to Concur updates, patches, and releases. "
        "2. Implement a ticketing system to document all vendor-initiated changes, including release notes, impact, and change timeline. "
        "3. Request a sandbox or test environment from Concur to evaluate updates prior to migration to the production environment. "
        "4. Develop testing procedures to validate that vendor changes function as intended. "
        "5. Implement a formal approval process requiring business owner sign-off before vendor changes are deployed to production. "
        "6. Maintain documentation of all vendor change notifications, testing results, approvals, and implementations. "
        "7. Establish a post-implementation verification process to confirm vendor changes were successfully deployed without issue. "
        "8. Create a communication process to notify end users about significant vendor updates and any potential impacts."
    )
),

    # Integration Monitoring - Informal Process
    GapExample(
        control_id="MO-01",
        gap_status="gap",
        gap_title="Absence of Scheduled Job / Integration Failure Monitoring for NetSuite",
        gap_description=(
            "While NetSuite has an automated job syncing with Adaptive Planning on a weekly basis, there is "
            "no formal monitoring process in place to ensure timely detection and resolution of job failures. (Note: Please refer to "
            "the Bill.com & Concur rows above for their respective NetSuite-related integrations / jobs.) "
            "The current process relies primarily on native error handling functionality within Adaptive Planning "
            "without documented procedures for consistent monitoring and failure alert review. "
            "There isn't a formalized ticketing or documentation process to track job failures, investigations, "
            "and resolutions, which limits accountability and auditability. "
            "The process lacks defined timelines and escalation procedures for addressing failures, potentially "
            "resulting in delayed identification and resolution of issues affecting financial data integrity."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Implement a formal procedure for monitoring the NetSuite / Adaptive job, including specific roles and responsibilities. "
            "2. Configure automated email notifications / alerts to be sent to appropriate IT personnel immediately upon failure detection. "
            "3. Establish a formal ticketing process to log all job failures, including failure details and investigation / resolution steps. "
            "4. Define specific timeframes for addressing and resolving job failures based on severity and impact to financial reporting. "
            "5. Consider leveraging a monitoring tool that provides real-time visibility into the status of the NetSuite / Adaptive job. "
            "6. Maintain documentation of all job failures, including notification, investigation, and resolution for audit purposes. "
            "7. Establish formal escalation procedures for instances when job failures cannot be resolved within defined timeframes."
        )
    ),

    GapExample(
    control_id="MO-01",
    gap_status="informal process",
    gap_title="Informal Scheduled Job / Integration Failure Monitoring for NetSuite",
    gap_description=(
        "Management has an informal approach to monitoring the NetSuite job syncing with Adaptive Planning, "
        "primarily relying on native error notifications without structured processes for consistent review. "
        "While job failures may be detected through the native error handling functionality in Adaptive Planning, "
        "there is no standardized procedure for reviewing these alerts or ensuring that appropriate personnel "
        "are consistently notified when failures occur. "
        "Job failures are typically addressed when discovered, but without a formal ticketing system or "
        "documentation requirements, it can be challenging to track investigation steps and resolution actions. "
        "The informal monitoring approach lacks defined response timeframes and escalation paths, potentially "
        "resulting in inconsistent handling of failures depending on who receives the notification and their "
        "availability. "
        "Documentation of job failures and their resolution is limited and inconsistent, making it difficult "
        "to establish a reliable audit trail or identify recurring issues that may require systemic fixes."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Implement a formal procedure for monitoring the NetSuite / Adaptive job, including specific roles and responsibilities. "
        "2. Configure automated email notifications / alerts to be sent to appropriate IT personnel immediately upon failure detection. "
        "3. Establish a formal ticketing process to log all job failures, including failure details and investigation / resolution steps. "
        "4. Define specific timeframes for addressing and resolving job failures based on severity and impact to financial reporting. "
        "5. Consider leveraging a monitoring tool that provides real-time visibility into the status of the NetSuite / Adaptive job. "
        "6. Maintain documentation of all job failures, including notification, investigation, and resolution for audit purposes. "
        "7. Establish formal escalation procedures for instances when job failures cannot be resolved within defined timeframes."
    )
),

    # Backup Management - Informal Process
    GapExample(
        control_id="MO-02",
        gap_status="informal process",
        gap_title="Inadequate Data Backup Process for LampWeb",
        gap_description=(
            "While Management performs some data backups for the LampWeb system, the process lacks formalization "
            "and consistency in execution. Backups may be performed on an ad-hoc basis rather than consistently following the "
            "required daily incremental and weekly full backup schedule. "
            "There isn't a structured process for reviewing backup logs to ensure successful completion, with "
            "reviews occurring sporadically rather than on the required weekly cadence. "
            "Failed backups might be noted but are not consistently documented in a formal ticketing system, "
            "creating potential gaps in the audit trail and possibly allowing backup failures to go unaddressed. "
            "The organization could benefit from clearer roles and responsibilities for backup management, which would enhance "
            "oversight and accountability for this data protection control."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal backup policy that clearly defines daily incremental and weekly full backup requirements for LampWeb. "
            "2. Implement automated backup scheduling to ensure consistent execution according to the defined schedule. "
            "3. Develop a standardized process for the designated administrator to review backup logs on a weekly basis. "
            "4. Create backup log review templates to document the completion and results of each weekly review. "
            "5. Implement a formal ticketing process to document all backup failures, including failure details and resolution steps. "
            "6. Define specific timeframes for addressing and resolving backup failures based on criticality. "
            "7. Consider implementing automated monitoring tools that provide real-time alerts for backup failures."
        )
    ),

    GapExample(
    control_id="MO-02",
    gap_status="gap",
    gap_title="Absence of Data Backup Process for LampWeb",
    gap_description=(
        "Management does not currently maintain a formal backup process for the LampWeb system, with no consistent "
        "daily incremental or weekly full backups being performed according to a defined schedule. "
        "There isn't a defined backup strategy or documented procedures for creating and maintaining data "
        "backups of this financially significant system. "
        "The organization has not assigned specific responsibility for backup management to any particular administrator, "
        "resulting in limited oversight for this data protection function. "
        "No process exists for regularly reviewing backup logs or documenting backup failures, increasing the "
        "risk that data loss could occur without timely detection or mitigation. "
        "The absence of a robust backup system creates risk to business continuity and data integrity "
        "in the event of system failure, data corruption, or other disruptive events."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Establish a formal backup policy that clearly defines daily incremental and weekly full backup requirements for LampWeb. "
        "2. Implement a backup solution capable of performing the required backup schedule and retention requirements. "
        "3. Designate specific administrators responsible for backup management and oversight. "
        "4. Develop and document standardized procedures for executing and verifying backups. "
        "5. Implement a formal process for weekly review of backup logs by the designated administrator. "
        "6. Create a ticketing system to document and track the resolution of any backup failures. "
        "7. Consider implementing automated monitoring tools that provide real-time alerts for backup failures. "
        "8. Train relevant personnel on backup procedures and response protocols for backup failures."
    )
),

    GapExample(
        control_id="MO-03",
        gap_status="informal process",
        gap_title="Inadequate Backup Restoration Testing for LampWeb",
        gap_description=(
            "While system backups are being performed for LampWeb, the organization conducts limited and "
            "inconsistent testing of backup restoration capabilities. "
            "Restoration tests are performed on an ad-hoc basis rather than consistently following the required quarterly "
            "schedule, with some quarters potentially having no testing performed. "
            "When tests are conducted, they may involve only basic file-level restoration rather than "
            "comprehensive system recovery testing that would validate complete restoration is possible in a "
            "disaster scenario. "
            "Documentation of restoration tests is often minimal and inconsistent, sometimes lacking detailed information "
            "about the test procedures, results, anomalies encountered, or corrective actions taken. "
            "There are no formally defined success criteria to objectively evaluate restoration test results, making "
            "it more difficult to determine if the tests are effectively validating backup integrity and completeness."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal quarterly schedule for LampWeb backup restoration testing with specific testing dates. "
            "2. Develop comprehensive test scenarios that validate both file-level recovery and full system restoration capabilities. "
            "3. Create detailed documentation templates for recording all aspects of restoration tests, including procedures followed, "
            "results obtained, anomalies identified, and corrective actions implemented. "
            "4. Define clear success criteria for restoration tests to objectively evaluate whether backups are valid and complete. "
            "5. Implement a ticketing system to formally document each quarterly test and track any required remediation actions. "
            "6. Establish timeframes for addressing any issues identified during restoration testing. "
            "7. Assign specific responsibility for overseeing the quarterly testing program and ensuring tests are performed as scheduled."
        )
    ),
    
    # SOC Report Review - Informal Process
    GapExample(
        control_id="ITELC-01",
        gap_status="gap",
        gap_title="Absence of Formal SOC Report Review Process for Azure",
        gap_description=(
            "Management does not currently perform a formal review of SOC 1 Type II reports for service organizations "
            "to systematically identify qualified opinions or exceptions in testing, resulting in potential unaddressed "
            "control deficiencies within these service organizations. "
            "There isn't an established process to identify and map complementary user entity controls (CUECs) "
            "from the service organizations' SOC 1 reports to controls within the company's environment, "
            "potentially leaving gaps in the control framework unidentified and unresolved. "
            "Management has not implemented procedures to systematically identify subservice organizations used by service "
            "providers, obtain their SOC 1 reports, or map complementary subservice organization controls "
            "(CSOCs) to ensure comprehensive coverage of the control environment. "
            "No consistent alternative monitoring mechanisms have been established in cases where SOC 1 reports may not "
            "be available, leaving the company with less assurance regarding the effectiveness of controls at "
            "service and subservice organizations."
        ),
        recommendation=(
            "For the system(s) listed in column E, perform the following steps: "
            "1. Establish a formal procedure for obtaining SOC 1 Type II reports and bridge letters annually from all service organizations, designating specific responsibility to the Department Head, Controller, or VP of Finance, and IT Management. "
            "2. Implement a structured process to review each SOC 1 report's period coverage, audit opinion (qualified or unqualified), and identified control exceptions or deficiencies. "
            "3. Develop a formal documentation template to record the review results for each service organization, including any exceptions requiring follow-up and their resolution status. "
            "4. Create a comprehensive mapping document that identifies all CUECs from each service organization's SOC 1 report and links them to existing controls within the company's environment. "
            "5. Establish procedures to identify all subservice organizations and obtain their respective SOC 1 reports or equivalent assurance documentation. "
            "6. Develop a process to map CSOCs to controls at the subservice organization level, documenting any gaps and their resolution. "
            "7. Implement alternative monitoring procedures when SOC 1 reports are unavailable, such as requesting SOC 2 reports, or conducting direct vendor inquiries. "
            "8. Establish a schedule for annual review of this process with formal sign-off by relevant Department Heads, Controller or VP of Finance, and IT Management to ensure ongoing compliance."
        )
    ),

    GapExample(
    control_id="ITELC-01",
    gap_status="informal process",
    gap_title="Informal SOC Report Review Process for Azure",
    gap_description=(
        "Management occasionally reviews SOC 1 Type II reports for Azure, but lacks a formalized, "
        "documented process with consistent methodology and comprehensive coverage. "
        "While SOC reports are sometimes obtained, the review is performed without structured templates "
        "or formal documentation of findings, making it more challenging to track identified exceptions, "
        "qualified opinions, or their resolution over time. "
        "Complementary user entity controls (CUECs) mentioned in SOC reports are reviewed in an ad-hoc manner, "
        "without systematic mapping to the company's internal control environment, potentially leaving "
        "control gaps unidentified and unaddressed. "
        "The current approach includes limited consideration of subservice organizations and their "
        "complementary subservice organization controls (CSOCs), with inconsistent efforts to obtain "
        "and review subservice SOC reports. "
        "Alternative monitoring procedures for situations where SOC 1 reports are unavailable are "
        "implemented inconsistently and without clear guidelines for what constitutes acceptable "
        "alternative assurance."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Establish a formal procedure for obtaining SOC 1 Type II reports and bridge letters annually from all service organizations, designating specific responsibility to the Department Head, Controller, or VP of Finance, and IT Management. "
        "2. Implement a structured process to review each SOC 1 report's period coverage, audit opinion (qualified or unqualified), and identified control exceptions or deficiencies. "
        "3. Develop a formal documentation template to record the review results for each service organization, including any exceptions requiring follow-up and their resolution status. "
        "4. Create a comprehensive mapping document that identifies all CUECs from each service organization's SOC 1 report and links them to existing controls within the company's environment. "
        "5. Establish procedures to identify all subservice organizations and obtain their respective SOC 1 reports or equivalent assurance documentation. "
        "6. Develop a process to map CSOCs to controls at the subservice organization level, documenting any gaps and their resolution. "
        "7. Implement alternative monitoring procedures when SOC 1 reports are unavailable, such as requesting SOC 2 reports, or conducting direct vendor inquiries. "
        "8. Establish a schedule for annual review of this process with formal sign-off by relevant Department Heads, Controller or VP of Finance, and IT Management to ensure ongoing compliance."
    )
),

    GapExample(
    control_id="PD-01",
    gap_status="gap",
    gap_title="Absence of Formal Program Development (PD) and System Implementation Controls",
    gap_description=(
        "Management does not currently have a formalized program development (PD) process in place to govern the "
        "implementation of new systems or significant enhancements to existing systems within the IT "
        "environment, resulting in less structured project management. "
        "There are no standardized procedures for consistently conducting and documenting User Acceptance Testing (UAT) "
        "prior to deploying new systems or enhancements, nor are there formal processes for tracking and "
        "resolving identified issues or defects. "
        "There are no formal data validation procedures established to ensure that data is properly migrated and "
        "converted into new systems, increasing the risk of incomplete or inaccurate data transfers. "
        "Management does not perform a formalized review of user access for new systems prior to go-live "
        "to ensure appropriate role configuration, restriction of access based on job responsibilities, "
        "and consideration of segregation of duties. "
        "The organization has not established formal Go/No-Go criteria or a structured management approval process for "
        "new system implementations, potentially allowing systems to be placed into production without "
        "thorough preparation and validation."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Develop and implement a formal Program Development (PD) methodology that includes standardized phases, deliverables, and approval gates for all new system implementations and significant enhancements. "
        "2. Establish a project charter template that requires documentation of scope, objectives, stakeholders, milestones, resources, risks, and success criteria, with formal management approval required to initiate any project. "
        "3. Implement a standardized User Acceptance Testing (UAT) process that includes test planning, execution, defect tracking, and formal sign-off by business stakeholders prior to deployment. "
        "4. Create formal data validation procedures that require verification of completeness, accuracy, and integrity of data during migration to new systems, with documented results and approvals. "
        "5. Develop a user access review process for new systems that validates appropriate role configuration, access restrictions based on job responsibilities, and absence of segregation of duties conflicts prior to go-live. "
        "6. Establish clear Go/No-Go criteria that must be satisfied before deployment, including checklist verification of all preceding control activities and formal management approval. "
        "7. Implement a post-implementation review process to verify that all Program Development controls were effectively executed and to identify opportunities for improvement. "
        "8. Provide comprehensive training on the new Program Development methodology to all relevant stakeholders, including IT, business users, and management."
    )
),

GapExample(
    control_id="PD-01",
    gap_status="informal process",
    gap_title="Informal Program Development (PD) and System Implementation Controls",
    gap_description=(
        "Management follows an informal, often ad-hoc approach to program development and system implementation, "
        "with inconsistent application of project management principles and limited documentation of key "
        "activities and approvals. "
        "While some level of User Acceptance Testing (UAT) is performed for new systems or enhancements, "
        "it lacks standardized test plans, formal documentation, and structured processes for consistently tracking and "
        "resolving identified issues or defects. "
        "Data migration activities occur during implementations, but validation procedures are inconsistent "
        "and lack formal documentation to consistently demonstrate the completeness and accuracy of transferred data. "
        "Pre-implementation user access reviews happen occasionally but without standardized methodology "
        "to ensure appropriate role configuration, proper access restrictions, or adequate segregation of "
        "duties considerations. "
        "The organization uses some general readiness considerations before go-live decisions, but lacks "
        "formally defined Go/No-Go criteria and structured management approval processes, resulting in "
        "inconsistent evaluation of implementation readiness across different projects."
    ),
    recommendation=(
        "For the system(s) listed in column E, perform the following steps: "
        "1. Develop and implement a formal Program Development (PD) methodology that includes standardized phases, deliverables, and approval gates for all new system implementations and significant enhancements. "
        "2. Establish a project charter template that requires documentation of scope, objectives, stakeholders, milestones, resources, risks, and success criteria, with formal management approval required to initiate any project. "
        "3. Implement a standardized User Acceptance Testing (UAT) process that includes test planning, execution, defect tracking, and formal sign-off by business stakeholders prior to deployment. "
        "4. Create formal data validation procedures that require verification of completeness, accuracy, and integrity of data during migration to new systems, with documented results and approvals. "
        "5. Develop a user access review process for new systems that validates appropriate role configuration, access restrictions based on job responsibilities, and absence of segregation of duties conflicts prior to go-live. "
        "6. Establish clear Go/No-Go criteria that must be satisfied before deployment, including checklist verification of all preceding control activities and formal management approval. "
        "7. Implement a post-implementation review process to verify that all Program Development controls were effectively executed and to identify opportunities for improvement. "
        "8. Provide comprehensive training on the new Program Development methodology to all relevant stakeholders, including IT, business users, and management."
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