"""Configuration data for transcript processing."""

import os

# Make sure this path points to your actual template file
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'Scoping Document.xlsx')

# Verify the template exists
if not os.path.exists(TEMPLATE_PATH):
    raise FileNotFoundError(f"Template file not found at: {TEMPLATE_PATH}")

QUESTION_HEADER_MAPPING = {
    "What is the name of the system?": "System Name",
    "Please provide a high-level description of the system.": "System Description",
    "How is the system being used by the client?": "System Usage by Client",
    "Who or what team is responsible for administering this system?": "System Administration Responsibility",
    "How is access provisioned to the system for new hires, additional access requests, and role changes?": "Access Provisioning Process",
    "How is access removed from the system for terminations and role changes?": "Access Removal Process",
    "How is access configured within the system (e.g., role-based access, permissions, object-based access)?": "Access Configuration",
    "If role-based, do the system administrators have the ability to modify the roles?": "Role Modification Capability",
    "Does management perform a periodic review of all custom roles?": "Role Review",
    "What roles or permissions grant privileged access and who has access to these privileged user accounts?": "Privileged Access",
    "Are there any system, shared, or generic user accounts that are interactive?": "System Accounts",
    "How and where are the credentials to these accounts being stored?": "Credential Storage for System Accounts",
    "Who has access to the credentials for these accounts?": "System Account Credential Access",
    "Does management perform periodic user access reviews for this system?": "User Access Review",
    "Does the system have activity logging functionality?": "Activity Logging Functionality",
    "Does management perform periodic activity reviews of user activity?": "Admin Activity Review",
    "How do users authenticate into the system?": "User Authentication Method",
    "Does management perform a periodic review of the system's authentication configurations?": "Authentication Configuration Review",
    "What types of changes can management perform within the system (e.g., configurations, workflows, code)?": "Change Types",
    "Who has access to make changes to the application?": "Change Access",
    "Are there any non-production environments that are used for developing and testing changes prior to deployment?": "Separate Environments",
    "For each type of change, what is the process for requesting, developing, testing, approving, and deploying the change?": "Change Management Process",
    "If this is a SaaS system, does the vendor push updates, patches, and/or bug fixes? If so, what is the process for deploying these changes to production?": "Vendor Update Process",
    "Is there an inherent system functionality that prevents users from both developing and deploying a change to production?": "Segregation of Duties",
    "Does management perform a periodic review of changes to the system to validate that they were appropriately requested, tested, and approved prior to deployment to production?": "Change Review Process",
    "Are there any scheduled automated jobs or interfaces between this application and other in-scope systems? If so:": "Automated Jobs Overview",
    "What tools are used to run, schedule, and monitor the automated jobs/interfaces?": "Job Management Tools",
    "In case of a job/interface failure, what is management's process for resolving the failure?": "Job Failure Resolution",
    "Where is this system's data stored (e.g., vendor-managed database, proprietary database, third-party database provider)?": "Data Storage Location",
    "How often does management perform data backups?": "Backup Frequency",
    "What types of backups are performed (e.g., full, incremental, differential)?": "Backup Types",
    "In case of a backup failure, what is management's process for resolving the failure?": "Backup Failure Resolution",
    "Does management perform an annual review of the vendor's SOC 1 Type 2 report to ensure the vendor's internal control environment is effective and that management is performing the required complementary user entity controls (CUECs)?": "SOC Report Review"
}

AGENDA = {
    "Section 1: System Overview": [
        "What is the name of the system?",
        "Please provide a high-level description of the system.",
        "How is the system being used by the client?",
        "Who or what team is responsible for administering this system?"
    ],
    "Section 2: Access to Programs and Data": [
        "How is access provisioned to the system for new hires, additional access requests, and role changes?",
        "How is access removed from the system for terminations and role changes?",
        "How is access configured within the system (e.g., role-based access, permissions, object-based access)?",
        "If role-based, do the system administrators have the ability to modify the roles?",
        "Does management perform a periodic review of all custom roles?",
        "What roles or permissions grant privileged access and who has access to these privileged user accounts?",
        "Are there any system, shared, or generic user accounts that are interactive?",
        "How and where are the credentials to these accounts being stored?",
        "Who has access to the credentials for these accounts?",
        "Does management perform periodic user access reviews for this system?",
        "Does the system have activity logging functionality?",
        "Does management perform periodic activity reviews of user activity?",
        "How do users authenticate into the system?",
        "Does management perform a periodic review of the system's authentication configurations?"
    ],
    "Section 3: Change Management": [
        "What types of changes can management perform within the system (e.g., configurations, workflows, code)?",
        "Who has access to make changes to the application?",
        "Are there any non-production environments that are used for developing and testing changes prior to deployment?",
        "For each type of change, what is the process for requesting, developing, testing, approving, and deploying the change?",
        "If this is a SaaS system, does the vendor push updates, patches, and/or bug fixes? If so, what is the process for deploying these changes to production?",
        "Is there an inherent system functionality that prevents users from both developing and deploying a change to production?",
        "Does management perform a periodic review of changes to the system to validate that they were appropriately requested, tested, and approved prior to deployment to production?"
    ],
    "Section 4: Operations Management": [
        "Are there any scheduled automated jobs or interfaces between this application and other in-scope systems? If so:",
        "What tools are used to run, schedule, and monitor the automated jobs/interfaces?",
        "In case of a job/interface failure, what is management's process for resolving the failure?",
        "Where is this system's data stored (e.g., vendor-managed database, proprietary database, third-party database provider)?",
        "How often does management perform data backups?",
        "What types of backups are performed (e.g., full, incremental, differential)?",
        "In case of a backup failure, what is management's process for resolving the failure?"
    ],
    "Section 5: IT Entity Level Controls": [
        "Does management perform an annual review of the vendor's SOC 1 Type 2 report to ensure the vendor's internal control environment is effective and that management is performing the required complementary user entity controls (CUECs)?"
    ]
}

RESPONSE_EXAMPLES = {
    "System Name": [
        "NetSuite",
        "Salesforce",
        "Workday",
        "FastPath",
        "SAP S/4HANA"
    ],
    "System Description": [
        "This system is primarily used for financial management, accounting, and reporting. It offers modules for Accounts Payable, Accounts Receivable, and General Ledger transactions.",
        "This is a cloud-based CRM platform providing sales, marketing, and service functionalities. It supports lead management, opportunity tracking, and customer support processes."
    ],
    "System Usage by Client": [
        "The client utilizes this system to handle core financial processes such as invoicing, expense management, and financial reporting. It also supports approvals for purchase orders and vendor payments.",
        "This system is used as the primary CRM solution, tracking customer interactions, managing sales opportunities, and enabling marketing campaigns."
    ],
    "System Administration Responsibility": [
        "The IT Infrastructure Team, led by John Johnson (Director of Infrastructure).",
        "The Accounting Department, overseen by Stan Smith (Corporate Controller).",
        "A dedicated Business Systems group that manages user provisioning and system configurations."
    ],
    "Access Provisioning Process": [
        "Access provisioning is triggered by HR updates (e.g., new hires in Workday), which automatically create a ticket in ServiceNow. The ticket includes necessary role information and requires manager approval before the IT admin grants access.",
        "Managers or employees submit a request via an email or ticketing system (e.g., Jira). The request is reviewed by the system admin for appropriateness, then approved by the requester's manager before the admin provisions access.",
        "An IAM solution (e.g., SailPoint) is configured to automate new hire provisioning based on predefined role-to-job-function mappings. Approvals occur electronically within the IAM tool."
    ],
    "Access Removal Process": [
        "Upon termination, HR updates the employee record. An automated feed from the HR system creates a termination ticket in ServiceNow, prompting the system admin to remove access within 1 business day.",
        "For role changes, the manager submits an access modification ticket. Access is adjusted (added or removed) after the manager and system owner approve.",
        "In cases where manual removals are required, an HR-generated notification or spreadsheet is sent to the IT admin. Access must be removed within 1-3 business days."
    ],
    "Access Configuration": [
        "Access is configured using a role-based model, where each role has predefined permissions aligned with specific job functions (e.g., Accounts Payable Clerk).",
        "Permissions are assigned individually to each user (permission-based). Administrative permissions are granted only upon documented managerial approval.",
        "A combination of role-based and object-based access is used. Users inherit role permissions and are further restricted by object-level settings (e.g., can only view certain financial reports)."
    ],
    "Role Modification Capability": [
        "Yes; System administrators can create, modify, or delete custom roles. These changes must follow a defined change management process, including ticket creation, approval, and testing.",
        "Yes; but no additional detail was provided in the walkthrough meeting.",
        "No; Only vendor-provided roles exist, and the client cannot alter role definitions without vendor assistance."
    ],
    "Role Review": [
        "Yes; management performs an annual review of all roles and permissions.",
        "Yes; management performs reviews of all roles and permissions, but they do not formally document the review",
        "No; management only looks at roles/permissions when an issue arises or new roles are created.",
        "No; Only vendor-provided roles exist, and the client cannot alter role definitions without vendor assistance."
   ],
    "Privileged Access": [
        "Yes; Users with privileged access include super admins and a few IT admins who can modify system configurations, assign roles, and make high-level financial entries.",
        "Yes; but no additional detail was provided in the walkthrough meeting.",
        "No; All users share similar access privileges, and there are no administrator-level or super user accounts in this system."
    ],

    "System Accounts": [
        "Yes; The system includes a built-in admin account that can be accessed interactively for troubleshooting.",
        "Yes; but no additional detail was provided in the walkthrough meeting.",
        "No; while there is a system account, only the vendor has access to the credentials.",
        "No; there are no interactive system accounts within the system.",
        "No; All user accounts are tied to individual employees; there are no generic or shared credentials that can be used interactively."
    ],
    "Credential Storage for System Accounts": [
        "N/A - No Interactive System Accounts",
        "Credentials for the integration account are stored in a secure password management solution called Keeper.",
        "The vendors admin account credentials are fully controlled by the vendor; there is no local storage of these credentials.",
        "In certain cases, out-of-the-box admin credentials are memorized by the lead IT admin, with no formal documentation."
    ],
    "System Account Credential Access": [
        "N/A - No Interactive System Accounts",
        "IT Security staff and approved admins have rights to retrieve credentials from the secure storage solution.",
        "Only the vendor's support team can access the vendor-provided admin account credentials.",
        "Access to the shared admin credentials is granted to all systems engineers without formal logging of usage."
    ],
    "User Access Review": [
        "Yes; Management conducts quarterly access reviews. A report of all users and their permissions (IPE) is generated, reviewed line-by-line, and signed off by both the controller and the CFO.",
        "Yes; Reviews take place semi-annually. The IT admin pulls a user listing, which is then validated by the system owner. All changes and approvals are documented in a shared drive.",
        "Yes; but no additional detail was provided in the walkthrough meeting.",
        "Yes; Annual reviews are performed due to the systems low risk profile. The user listing is exported, and each manager certifies the appropriateness of their teams access."
    ],
    "Activity Logging Functionality": [
        "The system maintains logs of [types of activities]. Logs are retained for [duration] and include [detail level].",
        "Activity logging captures [event types] and includes [specific details]. Logs are stored in [location] for [duration].",
        "No, the system does not have activity logging capabilities or audit trail functionality."
    ],
    "Admin Activity Review": [
        "Yes; Admin activities are reviewed monthly by the IT Security Manager. Any anomalies result in a risk assessment and potential escalation to senior management.",
        "Yes; but no additional detail was provided in the walkthrough meeting.",
        "No; The system logs are not reviewed unless there is an incident",
        "N/A; the system does not have activity logging capabilities or audit trail functionality."
    ],
    "User Authentication Method": [
        "Primary authentication is through Okta SSO with enforced MFA for all users.",
        "The system uses a hybrid authentication approach where regular users authenticate through Azure AD SSO with MFA, while system administrators maintain direct application credentials as a backup authentication path.",
        "Authentication is managed through the native application login page which requires a password + email MFA."
    ],
    "Authentication Configuration Review": [
        "Yes; The client periodically reviews authentication configurations (e.g., password policies, MFA settings) to ensure alignment with security standards.",
        "Yes; but no additional detail was provided in the walkthrough meeting.",
        "No; The client does not perform periodic reviews of the systems authentication configurations."
    ],
    "Change Types": [
        "Management can perform configuration changes to adjust system settings (e.g., modifying approval thresholds), update workflows (e.g., adding new approval steps), and modify custom code (e.g., Apex classes in Salesforce). These changes are managed through our ticketing system (ServiceNow).",
        "The system allows for limited configuration changes (e.g., updating picklist values) that can be performed by system administrators. More complex changes, such as modifying workflows or updating custom code, require involvement from our IT development team and follow our standard change management process.",
        "Management does not have the ability to make any changes to this system. All system configurations, workflows, and code are managed entirely by the vendor."
    ],
    "Change Access": [
        "Access to make changes is restricted to the IT team and a small group of system administrators. The IT team has full access to make configuration, workflow, and code changes, while business system administrators can only perform configuration updates. All change access is granted through role-based permissions in the system.",
        "The following roles have change capabilities: System Administrator (configuration changes), IT Developer (code and workflow changes), and Business Analyst (workflow changes). These roles are assigned to individuals based on their job function and are reviewed quarterly to ensure appropriate access."
    ],
    "Separate Environments": [
        "Management maintains separate Development, QA, and Staging environments for implementing and testing changes.",
        "Management does not have any separate environments for this system"
    ],
    "Change Management Process": [
        "The client's change management process includes the following steps: 1) Change request submission via ServiceNow, 2) Development in the appropriate environment, 3) Testing by an independent team, 4) Approval by the system owner and IT Manager, 5) Deployment to production by the IT Operations team following a pre-defined deployment plan.",
        "The client requires all changes to follow a standardized process with clearly defined stages. Each stage has specific requirements, such as mandatory fields in the change request (description, justification, impact assessment), documented test cases and results, and formal approvals by the relevant stakeholders (system owner, IT Manager, Change Advisory Board (CAB).",
        "For configuration changes: The process begins with a ServiceNow ticket containing detailed requirements and impact assessment. Changes are first implemented in the sandbox environment, with comprehensive documentation including rollback procedures. Testing is performed by a separate QA team, and results are reviewed by the system owner. After approval, the IT Operations team handles the production deployment following established deployment procedures. Critical changes require additional CAB review.",
        "For code changes: Developers create Jira tickets and implement changes in feature branches within GitHub. All code changes undergo peer review and automated testing through Jenkins pipelines. Changes require approval from both technical leads and business stakeholders before merging. Production deployments are handled exclusively by the DevOps team through automated CI/CD processes, with developers explicitly restricted from production access.",
        "Emergency changes follow an expedited process but maintain key controls: 1) Emergency ticket creation with detailed justification, 2) Verbal approval from IT Director required before any work begins, 3) Changes implemented with at least two team members present, 4) Post-implementation review within 24 hours including formal documentation and retroactive approvals, 5) Incident report detailing why emergency process was needed.",
        "The change management process varies by change type. Minor configuration updates require ticket creation, testing in UAT, and system owner approval. Major changes additionally require security review, CAB approval, and documented rollback plans. Code changes follow git-flow with feature branches, mandatory code review, automated testing, and separate deployment team. All changes are documented in ServiceNow with requirements, test results, approvals, and post-implementation verification.",
        "There is no formal change management process in place. Changes are requested verbally or via email, and developers make changes directly in the production environment without formal approvals or testing. There is no documentation of changes, and no review process exists to validate changes were appropriate."
    ],
    "Vendor Update Process": [
        "Yes, the vendor releases monthly updates that include new features, bug fixes, and security patches. The client receives release notes 2 weeks in advance. The client's IT team tests the updates in their Staging environment before deploying them to Production. Deployment to Production requires approval from the client's IT Manager and Business Owner.",
        "No, the vendor does not push automatic updates. All changes are managed internally."
    ],
    "Segregation of Duties": [
        "The system enforces segregation of duties through role-based access controls. Developers can make changes in the Development and QA environments but cannot deploy to Production. The Production deployment is performed by the IT Operations team, who do not have access to make changes in the development environments.",
        "No, there is no inherent system functionality preventing users from both developing and deploying changes."
    ],
    "Change Review Process": [
        "On a quarterly basis, management performs a thorough review of system changes. The review focuses on verifying that each change has followed the client's defined process, including proper documentation (change request, test results, deployment plan), approvals, and segregation of duties. Any identified issues are escalated to the client's IT Steering Committee for further action.",
        "Management conducts monthly reviews of all system changes. The review involves generating a change report from ServiceNow, which includes details such as the change description, requester, developer, tester, approver, and deployment date. Each change is reviewed to ensure compliance with the client's change management policy, with any deviations investigated and documented.",
        "No periodic review of changes is performed."
    ],
    "Automated Jobs Overview": [
        "Yes, the system has [number/types] of automated jobs/interfaces with [systems]. These jobs perform [functions].",
        "No automated jobs or interfaces are currently implemented for this system.",
    ],
    "Job Management Tools": [
        "Jobs are managed using [tool names]. These tools provide [capabilities] for scheduling and monitoring.",
        "The following tools are used: [tool list]. Each tool is responsible for [specific function].",
        "The automated jobs are configured using native system functionality and are scheduled to run [insert frequency] and will notify the system administrator team"
    ],
    "Job Failure Resolution": [
        "Job failures are handled through a defined process: 1) [detection method], 2) [notification process], 3) [resolution steps].",
        "The failure resolution process includes [steps] and involves [teams/roles].",
        "Job failures automatically notify the system administrator team via e-mail. Upon receiving the notification, the team will attempt to re-run the job, if it doesn't immediately re-run they open a ticket and log the resolution process within the ticket."
    ],
    "Data Storage Location": [
        "N/A this is a vendor managed system so the vendor manages data storage.",
        "Data is stored in [storage type] managed by [provider/team].",
        "The system utilizes [storage solution] for data storage, which is [management details]."
    ],
    "Backup Frequency": [
        "N/A - This is a SaaS application, all backups are managed by the vendor.",
        "Backups are handled entirely by the vendor as part of their SaaS service.",
        "Backups are performed on a [frequency] basis according to [schedule].",
        "The backup schedule includes [timing details] for different types of backups."
    ],
    "Backup Types": [
        "N/A - All backup types and strategies are managed by the vendor as part of their SaaS service.",
        "Not applicable - backup implementation is handled by the SaaS vendor.",
        "The following backup types are performed: [list of backup types]. Each type covers [scope].",
        "Backup strategy includes [types] with [specific details about each type]."
    ],
    "Backup Failure Resolution": [
        "N/A - Backup failure resolution is managed by the vendor as part of their SaaS service.",
        "N/A - the vendor is responsible for monitoring and resolving any backup failures.",
        "Backup failures are addressed through [process steps]. Resolution includes [specific actions].",
        "The backup failure resolution process involves [steps] and requires [requirements]."
    ],
    "SOC Report Review": [
        "Yes, management performs annual SOC 1 Type 2 report reviews. The review process includes [specific checks] and is documented in [location].",
        "N/A - The application is not managed by the vendor and therefore, management does not need to perform SOC report reviews",
        "No, management does not perform regular SOC report reviews."
    ]
}

QUESTION_GUIDANCE = {
    "System Name": {
        "purpose": "To identify the specific name or title of the application under review",
        "process_background": """
        This question is straightforward, typically yielding a simple answer such as "NetSuite," 
        or another application name.
        """
    },
    
    "System Description": {
        "purpose": "To understand the general functionality and purpose of the system (e.g., ERP, CRM, financial reporting tool)",
        "process_background": """
        The client will describe what the system is used for and its primary features 
        (e.g., NetSuite is used for journal entries, trial balances, and financial reporting).
        """
    },
    
    "System Usage by Client": {
        "purpose": "To gather details on the specific ways and processes in which the client utilizes the system within their organization",
        "process_background": """
        The client may describe various use cases, integrations, 
        or add-ons (e.g., using NetSuite for journal entries, trial balance maintenance, 
        interfaces with other applications, etc.), as well as any key business processes that rely on the system.
        """
    },
    
    "System Administration Responsibility": {
        "purpose": "To identify the individuals or teams overseeing system administration, including user access, maintenance, and overall management",
        "process_background": """
        Accounting/finance leads (e.g., CFO, controller) often have 
        administrative responsibilities for financial systems. In some cases, IT personnel may 
        also have system administration roles for technical maintenance and user provisioning.
        """
    },
    "Access Provisioning Process": {
        "purpose": """
        To understand the end-to-end process for provisioning access to the system, covering 
        new hires, additional access requests, and role changes.
        """,
        "process_background": """
        - New user access provisioning applies to new hires, additional access requests, and role changes
        - New hires are not synonymous with new users in this context
        - Process may differ slightly but the key principles are the same
        """
    },
    "Access Removal Process": {
        "purpose": """
        To understand the process for revoking system access when an employee is terminated 
        or changes roles, ensuring timely removal and proper documentation.
        """,
        "process_background": """
        Access removal processes vary based on environment maturity and automation capabilities:
        - Mature environments often use automated HR system triggers and IAM solutions
        - Less automated environments rely on manual steps and notifications
        - Timeliness of access removal is critical for security
        """
    },
    "Access Configuration": {
        "purpose": """
        To understand how user access is structured and managed within the system, including 
        the methods used for granting and restricting access.
        """,
        "process_background": """
        Systems typically use one or more of these access control methods:
        - Role-Based: Users assigned predefined roles with associated permissions
        - Permission-Based: Individual permissions assigned directly to users
        - Object-Based: Access granted to specific system objects with varying permission levels
        - Hybrid: Combination of multiple access control methods
        """
    },
    "Role Modification Capability": {
        "purpose": """
        To determine the extent of system administrators' ability to customize roles and 
        permissions, and the controls surrounding these modifications.
        """,
        "process_background": """
        Role modification capabilities vary by system:
        - Some systems allow complete role customization
        - Others restrict modifications to predefined templates
        - Changes typically require testing in non-production environment
        - Proper change management procedures should govern modifications
        """
    },
    "Role Review": {
        "purpose": """
        - If system administrators (or other personnel) can create or modify roles, there must be a formal control 
          ensuring a periodic (annual or more frequent) review of all existing roles and permissions
        - This review helps confirm that roles/permissions remain aligned with current job responsibilities and 
          compliance requirements
        """,
        "process_background": """
        Key Components:
        - Documentation Requirements:
          * System-generated documentation of role/permission definitions
          * Especially critical for custom/homegrown systems
          * Clear documentation of review process and results
        
        - Reviewer Qualifications:
          * Must understand both system and business processes
          * Ability to interpret technical meaning of roles/permissions
          * Knowledge to assess appropriateness of assignments
        
        - Review Process Integration:
          * Supports regular user access review process
          * Helps validate user-to-role assignments
          * Ensures clear understanding of role implications
        """
    },
    "Privileged Access": {
        "purpose": """
        - To confirm whether there are any users with privileged access in the system
        - To identify the specific roles or permissions that grant privileged access
        - To understand the nature and scope of privileged access capabilities
        """,
        "process_background": """
        - In most systems, there are typically a few users in IT and accounting who have privileged access
        - However, in some rare cases, all users may have the same level of access
        - If privileged access exists, it's important to understand the roles and permissions associated with it
        """
    },
    "System Accounts": {
        "purpose": """
        - To identify the existence of any system, shared, or generic user accounts not assigned to specific employees
        - To understand how these accounts are used within the system
        - To determine if the shared/generic accounts are interactive (can be logged into)
        """,
        "process_background": """
        - System, shared, or generic accounts are common in many systems, though not all
        - Examples include out-of-the-box vendor accounts (e.g. NetSuite admin), integration accounts, 
          and company-created admin accounts
        - These accounts may be used by vendors for troubleshooting, enable system integrations, 
          or allow company configuration changes
        - Companies may create admin accounts to restrict super privileged access
        """
    },
    "Credential Storage for System Accounts": {
        "purpose": """
        - To find out how and where the credentials for shared/generic accounts are stored
        - To verify the security of credential storage methods
        - To ensure appropriate credential management practices
        """,
        "process_background": """
        - Credential storage is critical for shared/generic accounts
        - Best practice is to use enterprise credential management solutions
        - Insecure storage methods pose significant risks
        - Regular credential rotation and monitoring should be implemented
        """
    },
    "System Account Credential Access": {
        "purpose": """
        - To know who has access to the credentials for shared/generic accounts
        - To verify appropriate restriction of credential access
        - To ensure proper monitoring of credential usage
        """,
        "process_background": """
        - Access to shared account credentials should be strictly limited
        - Credential access should be logged and monitored
        - Regular review of credential access rights is important
        - Access should be based on job function and business need
        """
    },
    "User Access Review": {
        "purpose": """
        - This is a very key control on the access to programs and data side of ITGCs
        - To ensure management is performing periodic reviews of user access to systems to validate appropriateness
        """,
        "process_background": """
        - Best practice is to perform user access reviews on a quarterly basis
        - Semi-annual or annual reviews may be a flag warranting further examination, unless very low risk system
        - Typical review process includes:
          * IT admin pulls report of all users with access, including permissions and roles
          * Report sent to primary reviewer (controller, system owner, etc.)
          * IPE documentation (screenshots/video) of user listing generation
          * Primary reviewer transfers data to review template
          * Account checks performed between IPE and review sheet
          * Line-by-line review of user access appropriateness
          * Secondary review of primary reviewer's access
          * Documentation of review with comments/checkmarks
          * Primary and secondary reviewer sign-offs
          * All documentation retained in review workbook
        - Mature organizations may use IAM solutions:
          * Automated ingestion of user listings
          * Manager certifications based on HR data
          * Compliance team oversight
        - Inappropriate access handling:
          * Risk assessment and documentation
          * Activity log review
          * Access modification/removal
          * Impact investigation if needed
          * Validation of changes via updated user listing
        """
    },
    "Activity Logging Functionality": {
        "purpose": """
        - To determine if the system can log and report on user activities, particularly focusing on high-level 
          or administrative user actions
        - To verify the system's capability to track and maintain detailed audit trails
        """,
        "process_background": """
        - High-level or administrative users often have extensive privileges ("keys to the Kingdom")
        - These privileges can include changing configurations or assigning themselves roles that allow 
          performing critical (e.g., financial) transactions
        - System should maintain detailed logs of administrative and high-privilege activities
        - Logs should be protected from unauthorized modification and retained for an appropriate period
        """
    },
    "Admin Activity Review": {
        "purpose": """
        - To verify that management is conducting periodic reviews of activity logs to detect unauthorized 
          or inappropriate activities
        - To ensure proper oversight of high-privilege user actions
        """,
        "process_background": """
        - If audit logs exist and there are individuals with elevated access, management should periodically 
          generate and review reports detailing administrative activities
        - Reviews typically include retaining IPE to document activities, checking for irregularities, 
          and signing off on the review
        - Important to have proper segregation of duties so that no individual is reviewing their own activity
        - Process should include clear procedures for investigating and escalating suspicious activities
        """
    },
    "User Authentication Method": {
        "purpose": """
        - To determine the primary method(s) by which end-users and administrators log into the system
        - To identify whether alternative or backup authentication paths exist, especially for privileged accounts
        - To understand authentication methods for both regular and emergency situations
        """,
        "process_background": """
        - Some organizations use a centralized SSO solution like Okta to manage and streamline authentication
        - Other organizations may rely on direct login through the vendor's web application
        - Even with SSO in place, certain privileged or administrator accounts may have SSO bypass capabilities:
          * Emergency access requirements
          * Break-glass scenarios
          * System maintenance needs
        - Authentication methods should align with organizational security policies
        - Backup authentication paths should be strictly controlled and monitored
        """
    },
    "Authentication Configuration Review": {
        "purpose": """
        - To verify that management regularly reviews and validates authentication configurations
        - To ensure alignment with organizational security policies and industry standards
        - To confirm proper documentation of configuration reviews and changes
        """,
        "process_background": """
        - Authentication configurations should be reviewed periodically (typically annually)
        - Review components include:
          * Password complexity requirements
          * Account lockout settings
          * Session timeout parameters
          * Multi-factor authentication settings
        - For vendor-managed systems:
          * Review available configuration options
          * Document vendor-enforced settings
          * Validate compliance with security policies
        - For SSO implementations:
          * Review SSO configuration settings
          * Validate federation protocols
          * Assess backup authentication methods
        """
    },
    "Change Types": {
        "purpose": """
        - To identify and document all types of changes that can be made within the system
        - To understand the potential impact of different change types on system functionality
        - To ensure appropriate controls exist for each change category
        """,
        "process_background": """
        Changes typically fall into several categories:
        - Configuration Changes:
          * System settings modifications
          * Parameter updates
          * Feature enablement/disablement
        - Workflow Changes:
          * Process flow modifications
          * Approval routing updates
          * Automation rule changes
        - Code Changes:
          * Custom development
          * Script modifications
          * Integration updates
        - Each change type requires:
          * Appropriate authorization
          * Risk assessment
          * Testing requirements
          * Documentation standards
        """
    },
    "Change Access": {
        "purpose": """
        - To identify and confirm exactly which individuals or roles are authorized to make changes to the application
        - To ensure that only appropriate personnel have elevated or administrative rights to modify the system
        """,
        "process_background": """
        - This question often builds upon any previous discussion about user access rights
        - Even if user access details were covered earlier, it is important to clarify specifically who can 
          perform changes and in what capacity
        - The discussion may involve distinguishing between routine users, IT staff, controllers, or any 
          other roles that have permissions to make critical alterations to the application
        """
    },
    "Separate Environments": {
        "purpose": """
        - To confirm whether changes (code or configuration) are tested in a separate environment before going live
        - To mitigate the risk of unintended consequences such as data corruption, functionality errors, or system instability
        - To ensure best practices in change management, especially for key financial systems
        """,
        "process_background": """
        - Non-production environments (often called QA, UAT, sandbox, test environment, or pre-prod) are used to 
          replicate the production setup and validate changes before deployment
        - Commonly, there may be multiple stages (e.g., Dev → UAT → Production) to progressively test and approve changes
        - Some systems or vendors do not provide a test environment, in which case changes might be tested 
          directly in production—this is a significant concern
        """
    },
    "Change Management Process": {
        "purpose": """
        - To understand the complete lifecycle of system changes from request to deployment
        - To verify proper controls exist at each stage of the change process
        - To ensure appropriate segregation of duties throughout change management
        """,
        "process_background": """
        Configuration Changes:
        - Requesting:
          * Typically initiated via ticketing system (ServiceNow, Jira)
          * Formal change request describing system alterations
        - Development:
          * Changes built in test/sandbox environment when possible
          * Documentation of requirements, plan, and rollback strategy
        - Testing:
          * Testing performed by someone other than developer
          * Verification of change alignment with requirements
        - Approval:
          * Separate approver reviews testing results
          * Formal approval required before production deployment
        - Deployment:
          * Handled by different individual than developer/tester
          * Workflow-driven process ensuring step completion
          * Possible CAB review for critical changes
          
        Code Changes:
        - Requesting:
          * Ticket creation (often Jira) and developer assessment
        - Development:
          * Pull requests in code repository (GitHub, Git)
          * Branch/clone development with rollback capability
        - Testing and Peer Review:
          * Code review by peer/superior
          * Automated testing in CI/CD pipelines
          * Iterative improvement based on feedback
        - Approval/Merging:
          * Formal approval for pull request merging
          * Prevention of self-approval
        - Deployment:
          * CI/CD automation or scheduled manual deployment
          * UAT in development/sandbox environment
          * Production deployment with additional approval
          * Strict developer exclusion from production deployment
        """
    },
    "Vendor Update Process": {
        "purpose": """
        - To understand how vendor-initiated changes are managed and controlled
        - To verify proper testing and validation of vendor updates
        - To ensure appropriate oversight of vendor change deployment
        """,
        "process_background": """
        Vendor update scenarios typically include:
        - Automated Updates:
          * Vendor-controlled deployment schedule
          * Limited client involvement
          * Post-deployment validation
        
        - Coordinated Updates:
          * Advance notification from vendor
          * Client testing opportunity
          * Scheduled deployment window
        
        - Client-Controlled Updates:
          * Client determines deployment timing
          * Pre-deployment testing required
          * Standard change process followed
        
        Key considerations:
        - Update documentation and communication
        - Testing requirements and procedures
        - Impact assessment process
        - Rollback capabilities
        """
    },
    "Segregation of Duties": {
        "purpose": """
        - To determine if the system enforces segregation of duties through built-in or configurable controls
        - Specifically, whether there is a feature or configuration setting that prevents a single individual 
          from both creating (developing) and deploying a change into the production environment
        """,
        "process_background": """
        - Some systems use role- or permission-based segregation: developers cannot deploy, and those with 
          deploy rights cannot develop
        - In other configurations, any user can develop or deploy, but the system prevents the same individual 
          from carrying out both tasks on the same change
        - GitHub, for example, can be configured to disallow a developer from merging their own changes into production
        """
    },
    "Change Review Process": {
        "purpose": """
        - To confirm whether there is a formal, recurring process that verifies each change has proper documentation and approvals
        - Especially critical if there is no inherent system functionality preventing an individual from both 
          developing and deploying a change, as this review compensates for the lack of automated segregation of duties
        """,
        "process_background": """
        - Management typically pulls a report of all system changes made within a set period (often quarterly, 
          though monthly or semiannual reviews may also occur)
        - Screenshots, row counts, and IP logs may be used to demonstrate how the change report was generated
        - A reviewer (someone not involved in creating or deploying the changes being reviewed) examines each change to ensure:
          -It was appropriately requested (e.g., tied to a ticket or pull request)
          -It was tested by someone other than the developer
          -It was properly approved prior to being deployed into production
        - If the reviewer also performed any changes, a secondary reviewer must verify those specific changes
        - Any identified "inappropriate" or undocumented changes should trigger an investigation, with details documented
        - After confirming all changes are valid, a final sign-off closes the review process
        """
    },
    "Automated Jobs Overview": {
        "purpose": """
        - To identify all automated processes and system interfaces
        - To understand the criticality and impact of automated operations
        - To verify proper controls over automated job execution
        """,
        "process_background": """
        Common automated processes include:
        - Data Transfers:
          * System-to-system interfaces
          * Batch data processing
          * File transfers
        
        - Scheduled Operations:
          * Backup procedures
          * Maintenance routines
          * Report generation
        
        - Integration Points:
          * API connections
          * Database synchronization
          * Real-time data exchange
        
        Control considerations:
        - Job scheduling and monitoring
        - Error handling procedures
        - Data validation requirements
        - Recovery procedures
        """
    },
    "Job Management Tools": {
        "purpose": """
        - To identify tools and systems used for managing automated jobs and interfaces
        - To verify monitoring and alerting capabilities for job execution
        - To ensure proper oversight of automated processes
        """,
        "process_background": """
        Tool configurations typically include:
        - Native Application Tools:
          * Built-in scheduling capabilities
          * Integrated monitoring features
          * System-specific alerting
        
        - Third-Party Solutions:
          * Enterprise job schedulers
          * Monitoring platforms
          * Alert management systems
        
        - Hybrid Approaches:
          * Multiple tool integration
          * Cross-platform monitoring
          * Consolidated alerting
        
        Key requirements:
        - Real-time status monitoring
        - Immediate failure notification
        - Historical execution tracking
        - Performance analytics
        """
    },
    "Job Failure Resolution": {
        "purpose": """
        - To verify procedures for detecting and resolving automated job failures
        - To ensure timely response to job execution issues
        - To confirm proper documentation of failure resolution
        """,
        "process_background": """
        Standard resolution process includes:
        - Detection Phase:
          * Automated failure detection
          * Alert generation and notification
          * Initial impact assessment
        
        - Response Phase:
          * Issue investigation
          * Root cause analysis
          * Resolution planning
        
        - Recovery Phase:
          * Job restart procedures
          * Data validation checks
          * Business impact verification
        
        - Documentation Phase:
          * Incident recording
          * Resolution documentation
          * Preventive measure implementation
        """
    },
    "Data Storage Location": {
        "purpose": """
        - To identify where system data is stored and managed
        - To understand data ownership and responsibility
        - To verify proper data management controls
        """,
        "process_background": """
        Common storage scenarios:
        - Vendor-Managed:
          * SaaS provider hosts data
          * Provider handles backups
          * Limited client control
        
        - Client-Managed:
          * On-premise infrastructure
          * Full client control
          * Internal backup responsibility
        
        - Hybrid Solutions:
          * Mixed storage locations
          * Shared responsibilities
          * Multiple backup strategies
        
        Key considerations:
        - Data sovereignty
        - Backup responsibilities
        - Recovery capabilities
        - Access controls
        """
    },
    "Backup Frequency": {
        "purpose": """
        - To determine the frequency of data backups for a system (often a proprietary database)
        - To gauge how regularly data is being protected
        - To assess the risk of potential data loss between backups
        """,
        "process_background": """
        - Backups can be done weekly, monthly, yearly, or some combination thereof
        - The frequency can vary based on the organization's policies, the criticality of data, or other operational factors
        - In an "ideal" scenario, incremental/differential backups might be performed weekly, with full backups 
          perhaps once or twice a year
        """
    },
    "Backup Types": {
        "purpose": """
        - To understand the types of backups performed for system data
        - To verify appropriate backup strategies are in place
        - To ensure comprehensive data protection coverage
        """,
        "process_background": """
        Common backup types include:
        - Full Backups:
          * Complete system state capture
          * All data and configurations
          * Baseline for recovery
        
        - Incremental Backups:
          * Changes since last backup
          * Faster execution time
          * Efficient storage usage
        
        - Differential Backups:
          * Changes since last full backup
          * Intermediate recovery point
          * Balance of speed and completeness
        
        Key considerations:
        - Recovery time objectives
        - Storage requirements
        - Backup window constraints
        - Retention requirements
        """
    },
    "Backup Failure Resolution": {
        "purpose": """
        - To verify procedures for handling backup failures
        - To ensure timely detection and resolution of backup issues
        - To confirm proper documentation of backup recovery processes
        """,
        "process_background": """
        Standard resolution workflow:
        - Detection:
          * Automated monitoring alerts
          * Backup completion checks
          * System status verification
        
        - Response:
          * Issue investigation
          * Impact assessment
          * Resolution planning
        
        - Recovery:
          * Backup job restart
          * Alternative backup methods
          * Data consistency validation
        
        - Documentation:
          * Failure root cause analysis
          * Resolution steps recorded
          * Preventive measures implemented
        """
    },
    "SOC Report Review": {
        "purpose": """
        - To verify management's review of vendor SOC reports
        - To ensure understanding and implementation of CUECs
        - To confirm proper vendor control assessment
        """,
        "process_background": """
        Review components include:
        - SOC Report Analysis:
          * Coverage period verification
          * Control objective review
          * Exception assessment
          * Impact evaluation
        
        - CUEC Implementation:
          * Identification of requirements
          * Gap analysis performance
          * Control implementation
          * Ongoing monitoring
        
        - Vendor Assessment:
          * Control environment evaluation
          * Subservice organization review
          * Risk assessment completion
          * Remediation planning
        
        Documentation requirements:
        - Review evidence retention
        - Gap analysis results
        - Action plan tracking
        - Management sign-off
        """
    }
}

GPT_CONFIG = {
    "model": "gpt-4o",
    "max_tokens": 5000,
    "temperature": 0.3,
    "system_role": "You are a helpful assistant that extracts answers from meeting transcripts."
} 