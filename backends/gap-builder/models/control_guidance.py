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
    "What roles or permissions grant privileged access?": "Privileged Access",
    "Who has access to these privileged user accounts?": "Privileged User Account Access",
    "Are there any system, shared, or generic user accounts that are interactive?": "System Accounts",
    "How and where are the credentials to these accounts being stored?": "Credential Storage for System Accounts",
    "Who has access to the credentials for these accounts?": "System Account Credential Access",
    "Does management perform periodic user access reviews for this system?": "User Access Review",
    "Does the system have activity logging functionality?": "Activity Logging Functionality",
    "Does management perform periodic activity reviews of user activity?": "User Activity Review",
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

QUESTION_GUIDANCE = {
    "System Name": {
        "purpose": "To identify the specific name or title of the application under review",
        "process_background": """
        This question is straightforward, typically yielding a simple answer such as "NetSuite," 
        or another application name.
        """,
        "flags_to_watch": []
    },
    
    "System Description": {
        "purpose": "To understand the general functionality and purpose of the system (e.g., ERP, CRM, financial reporting tool)",
        "process_background": """
        The client will describe what the system is used for and its primary features 
        (e.g., NetSuite is used for journal entries, trial balances, and financial reporting).
        """,
        "flags_to_watch": []
    },
    
    "System Usage by Client": {
        "purpose": "To gather details on the specific ways and processes in which the client utilizes the system within their organization",
        "process_background": """
        The client may describe various use cases, integrations, 
        or add-ons (e.g., using NetSuite for journal entries, trial balance maintenance, 
        interfaces with other applications, etc.), as well as any key business processes that rely on the system.
        """,
        "flags_to_watch": []
    },
    
    "System Administration Responsibility": {
        "purpose": "To identify the individuals or teams overseeing system administration, including user access, maintenance, and overall management",
        "process_background": """
        Accounting/finance leads (e.g., CFO, controller) often have 
        administrative responsibilities for financial systems. In some cases, IT personnel may 
        also have system administration roles for technical maintenance and user provisioning.
        """,
        "flags_to_watch": [
            "Overlap or unclear division of responsibilities between finance and IT",
            "Multiple administrators with similar or overlapping privileges"
        ]
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
        """,
        "flags_to_watch": [
            "Lack of formal access request process (verbal requests, direct emails without tickets)",
            "No approvals or additional approvals beyond the requester",
            "Same person requesting and provisioning access for their own team",
            "Admin reviewing and provisioning the access is the same person requesting it"
        ]
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
        """,
        "flags_to_watch": [
            "Access removal taking longer than 3 business days after termination",
            "Lack of formal notifications or tickets for terminations and role changes",
            "No clear process for role-based access adjustments",
            "User accounts remaining active after termination without mitigating controls"
        ]
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
        """,
        "flags_to_watch": [
            "Unclear or inconsistent access control methodology"
        ]
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
        """,
        "flags_to_watch": [
            "Uncontrolled role modification capabilities",
            "Missing change management process for role changes",
            "Lack of testing before role modifications",
            "No periodic review of role configurations",
            "Potential segregation of duties conflicts in role design"
        ]
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
        """,
        "flags_to_watch": [
            "Lack of clear privileged access definition",
            "All users having same level of access without business justification",
            "Excessive number of privileged roles",
            "Unclear separation between regular and privileged access"
        ]
    },
    "Privileged User Account Access": {
        "purpose": """
        - To determine which individuals or employees have access to privileged user accounts
        - To verify business justification for privileged access assignments
        - To ensure appropriate distribution of privileged access
        """,
        "process_background": """
        - Privileged access is typically limited to specific IT and accounting personnel
        - Access should be based on job responsibilities and business needs
        - Regular review of privileged access assignments is important
        """,
        "flags_to_watch": [
            "Excessive number of users with privileged access",
            "Missing or inadequate business justification for access",
            "Lack of regular privileged access reviews",
            "Inappropriate privileged access assignments"
        ]
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
        """,
        "flags_to_watch": [
            "Excessive number of shared/generic accounts",
            "Interactive accounts without clear business justification",
            "Shared accounts used for regular operations",
            "No tracking of shared account usage"
        ]
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
        """,
        "flags_to_watch": [
            "Insecure credential storage methods",
            "Lack of enterprise credential management solution",
            "Missing credential rotation process",
            "Inadequate password security controls"
        ]
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
        """,
        "flags_to_watch": [
            "Wide access to shared account credentials",
            "No monitoring of credential access",
            "Missing credential checkout process",
            "Lack of regular access reviews",
            "Unrestricted sharing of credentials"
        ]
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
        """,
        "flags_to_watch": [
            "Infrequent reviews (semi-annual/annual) without risk justification",
            "Missing documentation of review process and IPE",
            "No individual user-level review evidence",
            "Self-review without secondary approval",
            "Lack of risk assessment for inappropriate access",
            "No investigation of potential unauthorized actions",
            "Missing validation of access changes",
            "Untimely review completion",
            "Insufficient retention of review documentation"
        ]
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
        """,
        "flags_to_watch": [
            "Missing or incomplete audit logging capabilities",
            "Inability to track administrative actions",
            "Insufficient log retention periods",
            "Logs vulnerable to unauthorized modification",
            "Limited or no logging of critical activities"
        ]
    },
    "User Activity Review": {
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
        """,
        "flags_to_watch": [
            "Lack of reviews for users with high-level/admin rights",
            "Missing documentation or evidence of review",
            "Administrators reviewing their own activity",
            "No clear investigation/escalation process",
            "Incomplete or inconsistent review procedures",
            "Reviews not performed timely or regularly"
        ]
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
        """,
        "flags_to_watch": [
            "Undocumented SSO bypass capabilities",
            "Unclear tracking of users with bypass ability",
            "Missing procedures for emergency authentication",
            "Lack of monitoring for SSO bypass usage",
            "Insufficient controls around alternative access paths",
            "Weak password requirements for direct authentication"
        ]
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
        """,
        "flags_to_watch": [
            "Missing or infrequent configuration reviews",
            "Lack of documentation for current settings",
            "Non-compliance with security policies",
            "Undocumented exceptions or deviations",
            "Insufficient validation of vendor settings",
            "Missing SSO configuration assessment"
        ]
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
        """,
        "flags_to_watch": [
            "Undefined or unclear change categories",
            "Missing controls for specific change types",
            "Insufficient testing requirements",
            "Lack of change documentation standards",
            "Inadequate segregation of duties",
            "Uncontrolled custom development capability"
        ]
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
        """,
        "flags_to_watch": [
            "Overly broad change access permissions",
            "Unclear or undocumented change authorization",
            "Potential segregation of duties issues"
        ]
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
        """,
        "flags_to_watch": [
            "No separate environment for testing changes",
            "Vendor claims of unavailable test environments"
        ]
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
        """,
        "flags_to_watch": [
            "Missing formal change management process",
            "Insufficient testing procedures",
            "Lack of proper approvals",
            "Poor documentation retention",
            "Inadequate segregation of duties",
            "No rollback procedures",
            "Missing post-implementation verification",
            "Undefined emergency change process"
        ]
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
        """,
        "flags_to_watch": [
            "No visibility into vendor updates",
            "Missing update testing procedures",
            "Lack of impact assessment",
            "Insufficient update documentation",
            "No rollback capability",
            "Poor vendor communication",
            "Missing validation procedures"
        ]
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
        """,
        "flags_to_watch": [
            "Complete lack of inherent segregation functionality",
            "Reliance solely on manual oversight without system restrictions",
            "Insufficient technical controls for enforcing separation",
            "Missing configuration options for segregation"
        ]
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
          * It was appropriately requested (e.g., tied to a ticket or pull request)
          * It was tested by someone other than the developer
          * It was properly approved prior to being deployed into production
        - If the reviewer also performed any changes, a secondary reviewer must verify those specific changes
        - Any identified "inappropriate" or undocumented changes should trigger an investigation, with details documented
        - After confirming all changes are valid, a final sign-off closes the review process
        """,
        "flags_to_watch": [
            "No formal periodic review process",
            "Self-review without secondary reviewer",
            "Insufficient evidence of review steps",
            "Missing investigation process for unauthorized changes"
        ]
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
        """,
        "flags_to_watch": [
            "Undocumented automated processes",
            "Missing monitoring procedures",
            "Inadequate error handling",
            "Lack of recovery procedures",
            "Poor job documentation",
            "No alert mechanism for failures",
            "Missing validation controls"
        ]
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
        """,
        "flags_to_watch": [
            "Missing job management tools",
            "Inadequate monitoring capabilities",
            "Delayed failure detection",
            "No alert mechanism",
            "Poor historical tracking",
            "Insufficient documentation",
            "Lack of escalation procedures"
        ]
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
        """,
        "flags_to_watch": [
            "No formal failure detection process",
            "Missing resolution procedures",
            "Poor incident documentation",
            "Lack of root cause analysis",
            "Insufficient preventive measures",
            "Delayed failure response",
            "Missing validation steps"
        ]
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
        """,
        "flags_to_watch": [
            "Unclear data storage location",
            "Undefined backup responsibilities",
            "Missing recovery procedures",
            "Poor access controls",
            "Insufficient security measures",
            "Lack of data sovereignty consideration",
            "Inadequate provider oversight"
        ]
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
        """,
        "flags_to_watch": [
            "Infrequent or nonexistent backups",
            "Long gaps between backup executions",
            "Vague or unclear backup schedule",
            "Missing backup frequency documentation"
        ]
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
        """,
        "flags_to_watch": [
            "Single backup type without justification",
            "Missing backup strategy documentation",
            "Inadequate backup coverage",
            "No backup validation process",
            "Poor retention management",
            "Insufficient recovery testing",
            "Missing monitoring procedures"
        ]
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
        """,
        "flags_to_watch": [
            "No backup failure detection process",
            "Missing resolution procedures",
            "Poor failure documentation",
            "Lack of root cause analysis",
            "Insufficient preventive measures",
            "Delayed failure response",
            "Missing validation steps"
        ]
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
        """,
        "flags_to_watch": [
            "Missing annual SOC review",
            "Incomplete CUEC implementation",
            "Poor exception handling",
            "Lack of documentation",
            "Insufficient risk assessment",
            "No remediation tracking",
            "Missing management oversight",
            "Inadequate subservice organization review"
        ]
    }
}

GPT_CONFIG = {
    "model": "gpt-4o",
    "max_tokens": 5000,
    "temperature": 0.3,
    "system_role": "You are a helpful assistant that extracts answers from meeting transcripts."
} 