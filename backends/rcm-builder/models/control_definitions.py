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

# Define standard controls based on the mapping table
STANDARD_CONTROLS = [
    # Access Provisioning
    Control(
        control_id="APD-01",
        short_name="Access Provisioning - Automated Workflow",
        description=(
            "New access and modified access in [INSERT SYSTEM NAME] follows a workflow that requires"
            "approval by the requestor's manager and the [INSERT SYSTEM NAME] application owner."
            "Once approved, the ticketing system automatically triggers the creation or modification of the user account/role."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Access Provisioning Process"],
        evaluation_criteria="Approvals and formal automated access requesting process present."
    ),

    Control(
        control_id="APD-01",
        short_name="Access Provisioning - Manual Approval",
        description=(
            "New access or changes to existing user access to [INSERT SYSTEM NAME] "
            "is approved by the employee's manager prior to being provisioned by the"
            "[INSERT SYSTEM] administrators"
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Access Provisioning Process"],
        evaluation_criteria="Approvals and formal manual access requesting process present."
    ),

    Control(
        control_id="APD-01",
        short_name="Access Provisioning",
        description=(
            "New user access (including transferred individuals) is approved by the [INSERT ADMIN] "
            "and Department Head prior to users obtaining access to company systems. For an individual "
            "transferring within the company, new user access is approved by the Controller and occurs "
            "only after incompatible access rights from their previous roles have been revoked."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Access Provisioning Process"],
        evaluation_criteria="New user/transfer provisioning process was described."
    ),

        Control(
        control_id="APD-01",
        short_name="Access Provisioning",
        description=(
            "For [INSERT SYSTEM] access above standard or view-only roles, new access or changes to "
            "existing user access are documented via ticket or email, are submitted by users' managers, "
            "and are approved by the VP of IT or SVP of Finance prior to being provisioned by the [INSERT SYSTEM] administrators."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Access Provisioning Process"],
        evaluation_criteria="New user/transfer provisioning process was described."
    ),

    Control(
        control_id="APD-02",
        short_name="Terminated User Access Removal -Hybrid",
        description=(
            "When a user's termination date is recorded in [INSERT HR SYSTEM NAME], an automated feed "
            "alerts [INSERT SYSTEM NAME]. This triggers an auto-generated ticket "
            "prompting the [INSERT SYSTEM NAME] admin to disable the user's access within 24 hours."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Access Removal Process"],
        evaluation_criteria="Formal automated access removal process was described."
    ),

    Control(
        control_id="APD-02",
        short_name="Terminated User Access Removal - Manual",
        description=(
            "When an employee is terminated, the HR team emails a termination notification to the "
            "[INSERT SYSTEM NAME] admin distribution list. The admin team manually disables the "
            "user's access within 1 business day."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Access Removal Process"],
        evaluation_criteria="Formal manual access removal process was described."
    ),

    Control(
        control_id="APD-03",
        short_name="Annual Role Permissions Review 1",
        description=(
            "Annually, the [INSERT SYSTEM NAME] admin team performs a review of roles within "
            "[INSERT SYSTEM NAME] to ensure the permissions associated with each role are "
            "appropriate. If any roles with inappropriate permissions are identified,"
            "risk assessment procedures and remediation steps are taken, including"
            "adjusting the permissions, documenting the rationale, and reviewing activity logs."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Annually",
        scoping_headers=["Role Modification Capability; Role Review"],
        evaluation_criteria="Must start with 'Yes;'"
    ),

    Control(
        control_id="APD-03",
        short_name="Annual Role Permissions Review 2",
        description=(
            "Annually, [INSERT SYSTEM NAME] admin team performs a review over all "
            "permissions assigned to user roles within NetSuite. The list of permissions is reviewed "
            "to identify any inappropriate role capabilities. Any inappropriate roles are modified "
            "timely, and the activity of users with access to those roles is researched and resolved "
            "appropriately."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Annually",
        scoping_headers=["Role Modification Capability; Role Review"],
        evaluation_criteria="Must start with 'Yes;'"
    ),

    Control(
        control_id="APD-04",
        short_name="User Access Review",
        description=(
            "Quarterly, the [INSERT ADMIN] performs reviews of all users with access to "
            "[INSERT SYSTEM NAME] to identify any users whose access is inappropriate "
            "and needs to be modified or removed. Inappropriate access identified "
            "through this process is remediated within 5 business days, with risk investigation procedures "
            "performed if necessary."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Quarterly",
        scoping_headers=["User Access Review"],
        evaluation_criteria="Must start with'Yes;'"
    ),
    
    Control(
        control_id="APD-04",
        short_name="Quarterly User Access Recertification",
        description=(
            "Quarterly, [INSERT SYSTEM NAME] administrators perform a user recertification "
            "of all users with access to [INSERT SYSTEM NAME]. The list of active "
            "users is reviewed to verify that existing access rights are appropriate."
            "Any inappropriate access is corrected, and the activity of users with inappropriate"
            "access is researched and resolved appropriately."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Quarterly",
        scoping_headers=["User Access Review"],
        evaluation_criteria="Must start with'Yes;'"
    ),    

    Control(
        control_id="APD-05",
        short_name="Shared Account Inventory and Access Review",
        description=(
            "Annually, the [INSERT ADMIN] performs a review all shared/generic "
            "accounts within [INSERT SYSTEM]. For each account, the review validates: "
            "(1) credentials are properly stored, "
            "(2) users with access to these credentials are appropriate based on business need, "
            "and (3) credential storage methods meet security requirements. Any identified issues "
            " are documented and remediated within 5 business days."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Annually",
        scoping_headers=["System Accounts; System Account Credential Access"],
        evaluation_criteria="Shared/generic account credential usage was described."
    ),

    Control(
        control_id="APD-06",
        short_name="Monthly Admin Activity Review",
        description=(
            "Monthly, [INSERT SYSTEM NAME] logs of administrative actions are generated. The [INSERT ADMIN] "
            "reviews the logs against open support tickets to ensure that all administrative activities "
            "have appropriate authorization. Inappropriate activity is investigated and"
            "any remediation actions taken where necessary."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Monthly",
        scoping_headers=["Admin Activity Review"],
        evaluation_criteria="Must start with'Yes;'"
    ),

    Control(
        control_id="APD-07",
        short_name="Annual Authentication Configuration Review",
        description=(
            "Annually, management reviews SSO configurations and application password settings"
            "to determine whether they align with company policy. Identified configuration gaps"
            "are documented and remediated in accordance with policy requirements."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Annually",
        scoping_headers=["Authentication Configuration Review"],
        evaluation_criteria="Must start with'Yes;'"
    ),

    Control(
        control_id="CM-01",
        short_name="Change Testing & Approval",
        description=(
            "Changes to [INSERT SYSTEM NAME] production environment are authorized by management, "
            "tested in an environment other than production, and approved before deployment."
        ),
        key_control=True,
        control_type="Manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Change Management Process"],
        evaluation_criteria="Formal change approval process was described."
    ),
    Control(
        control_id="CM-02",
        short_name="Separate Environments",
        description=(
            "Dedicated non-production environments are maintained for "
            "developing and testing changes to [INSERT SYSTEM NAME] before migrating them to production."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Separate Environments"],
        evaluation_criteria="Various change environments were listed."
    ),
    Control(
        control_id="CM-03",
        short_name="Quarterly Change Review 1",
        description=(
            "Quarterly, [INSERT ADMIN] reviews the [INSERT SYSTEM NAME] audit trail to analyze "
            "all changes deployed to production and validate whether each change was appropriately "
            "tested, approved, and segregation of duties maintained. Unauthorized changes are "
            "investigated, and remediated."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Quarterly",
        scoping_headers=["Change Review Process"],
        evaluation_criteria="Must start with'Yes;'"
    ),

    Control(
        control_id="CM-03",
        short_name="Quarterly Change Review 2",
        description=(
            "On a quarterly basis, [INSERT ADMIN] reviews all [INSERT SYSTEM NAME} changes deployed to production for "
            "appropriateness by identifying the associated ticket, ensuring the change was tested and "
            "approved, and confirming the change was developed and deployed by different individuals."
            "Inappropriate changes are investigated and any remediation actions taken where necessary."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Quarterly",
        scoping_headers=["Change Review Process"],
        evaluation_criteria="Must start with'Yes;'"
    ),

    Control(
        control_id="CM-04",
        short_name="Developer Segregation of Duties",
        description=(
            "Access to deploy changes to the [INSERT SYSTEM NAME] production environment is "
            "restricted to users without development rights."
        ),
        key_control=True,
        control_type="Automated",
        nature="Preventative",
        frequency="Automated",
        scoping_headers=["Segregation of Duties; Change Access"],
        evaluation_criteria="Client explicitly confirmed that users cannot both develop and migrate changes to production"
    ),

    Control(
        control_id="CM-05",
        short_name="Emergency Changes",
        description=(
            "Emergency changes to [INSERT SYSTEM NAME] production environment are documented prior to implementation"
            "and are reviewed and approved by management within 2 days of implementation."
        ),
        key_control=True,
        control_type="Manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Change Management Process"],
        evaluation_criteria="Formal change approval process was described."
    ),

    Control(
        control_id="MO-01",
        short_name="Integration Monitoring",
        description=(
            "Financially significant [INSERT SYSTEM NAME] integrations"
            "are monitored for failures. Integration failures "
            "alert the [INSERT SYSTEM NAME] and relevant IT teams via automated notifications. "
            "Failures are logged in a ticket, investigated, and resolved "
            "in a timely manner in accordance with SLA requirements."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Job Management Tools; Job Failure Resolution"],
        evaluation_criteria="Tools for monitoring jobs were listed and a process for resolving job failures was described."
    ),

    Control(
        control_id="MO-01",
        short_name="Job Failure Review",
        description=(
            "Daily, the [INSERT SYSTEM] administrators perform a review over all [INSERT SYSTEM NAME] "
            "scheduled job errors. Failures are investigated and corrective actions are taken to "
            "resolve errors and prevent recurrence and documented in an issue ticket."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Daily",
        scoping_headers=["Job Management Tools", "Job Failure Resolution"],
        evaluation_criteria="Periodic review of job failures was described."
    ),

    Control(
        control_id="MO-01",
        short_name="Job Monitoring & Alerts",
        description=(
            "A job monitoring solution is configured to monitor all critical "
            "automated jobs in [INSERT SYSTEM NAME]. Any job failure generates an alert to the"
            "[INSERT ADMIN], who logs the event in a ticket along with a root cause analysis"
            "and details on any corrective action performed to remediate the job failure."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad Hoc",
        scoping_headers=["Job Management Tools; Job Failure Resolution"],
        evaluation_criteria="Monitoring tool and job failure resolution process described."
    ),

    Control(
        control_id="MO-02",
        short_name="Data Backups",
        description=(
            "As a SaaS solution, [INSERT SYSTEM NAME] is responsible for all system and data backups. "
            "Management relies on [INSERT SYSTEM NAME]'s SOC 1 Type 2 report to gain "
            "assurance over [INSERT SYSTEM NAME]'s backup controls and related monitoring."
        ),
        key_control=False,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Ad-Hoc",
        scoping_headers=["Backup Frequency; Backup Types; Backup Failure Resolution"],
        evaluation_criteria="Client confirms that the system is SaaS"
    ),

    Control(
        control_id="MO-02",
        short_name="Data Backups",
        description=(
            "Management maintains on-premise backups of [INSERT SYSTEM NAME] data daily "
            "(incremental) and weekly (full). Backup logs are reviewed weekly by the [INSERT ADMIN], "
            "and any failed backup is documented in an issue ticket."
        ),
        key_control=True,
        control_type="IT-dependent manual",
        nature="Preventative",
        frequency="Weekly",
        scoping_headers=["Backup Frequency; Backup Types; Backup Failure Resolution"],
        evaluation_criteria="The system is not purely SaaS and they manage backups themselves."
    ),

    Control(
        control_id="MO-03",
        short_name="Backup Restoration Testing",
        description=(
            "As a SaaS solution, [INSERT SYSTEM NAME] is responsible for all system and data backups. "
            "Management relies on [INSERT SYSTEM NAME]'s SOC 1 Type 2 report to gain "
            "assurance over [INSERT SYSTEM NAME]'s backup controls and related monitoring."
        ),
        key_control=False,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Ad-Hoc",
        scoping_headers=["Backup Frequency; Backup Types; Backup Failure Resolution"],
        evaluation_criteria="Client clearly indicated that the system is a vendor managed product and the the vendor is in charge of storing/backing up data."
    ),

    Control(
        control_id="MO-03",
        short_name="Backup Restoration Testing",
        description=(
            "Quarterly, Management performs test restores of [INSERT SYSTEM NAME] backup "
            "data to validate the integrity and completeness of backup files. The restore process is "
            "documented in a ticket, including any anomalies and corrective actions. "
        ),
        key_control=False,
        control_type="IT-dependent manual",
        nature="Detective",
        frequency="Quarterly",
        scoping_headers=["Backup Frequency; Backup Types; Backup Failure Resolution"],
        evaluation_criteria="On-prem or hybrid environment that requires demonstration of backup integrity."
    ),

    Control(
        control_id="ITELC-01",
        short_name="SOC Report Review",
        description=(
            "Annually, [INSERT SYSTEM NAME]'s SOC 1 Type 2 report covering the "
            "[INSERT SYSTEM NAME] system is obtained and reviewed by [INSERT ADMIN] "
            "leadership and IT security personnel. The report is analyzed for exceptions, control "
            "gaps, testing exceptions and [INSERT SYSTEM NAME]'s documented remediation plans. "
            "[INSERT SYSTEM NAME] user entity controls are mapped to Management's "
            "internal controls to identify gaps requiring remediation. [INSERT SYSTEM NAME]'s "
            "key subservice organizations are identified and their SOC reports reviewed as needed by "
            "[INSERT SYSTEM NAME] vendor management."
        ),
        key_control=True,
        control_type="Manual",
        nature="Detective",
        frequency="Annually",
        scoping_headers=["SOC report Review"],
        evaluation_criteria="Process on SOC review process was described."
    )
]  # End of STANDARD_CONTROLS list   