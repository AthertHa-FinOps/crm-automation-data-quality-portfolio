# CRM Data Quality — Business Case Study

**Purpose:** Investigate data-quality problems between a fictional lead source and a fictional CRM export without risking the destruction of original records.

**Scenario:** 700 source leads are compared with 733 CRM export records. The two counts are deliberately different. Some records have format inconsistencies, corrupted or absent emails, conflicting contact details or duplicate email values.

**Approach:** I used AI-assisted Python and SQLite code to create a repeatable comparison. The script preserves the original CRM rows, adds suggested normalized values and flags discrepancies. Each exception is an item for review, not an automatic permission to alter customer data.

**Deliverables:** A CSV review file retaining all 733 CRM records, a count-and-issue report, ten existing SQLite queries, six automated tests, and source data that can be inspected.

**What an operations team should decide:** Which record is authoritative, whether duplicates are versions of the same contact, whether unmatched records came from another intake channel, and which corrections require approval.

**Experience supporting the approach:** My paid real estate work involved checking agreement and supporting-document accuracy, identifying conflicting records and coordinating fixes before contractual deadlines. This portfolio is a separate technical exercise, not proof of paid HubSpot/Salesforce administration.

**Limitations:** Synthetic data, email-based joins, no live CRM, no operational performance benchmark, no completed n8n integration. AI contributed to the code and writing; the repository tests make the recorded exercise reproducible.

Start with the [control report](02-crm-data-quality/outputs/control_report.md) and [review output](02-crm-data-quality/outputs/crm_review.csv).
