# Exception review — five inspectable fictional examples

**Evidence type:** Examples from fictional source and CRM extracts, with AI-assisted suggested follow-up actions. These are not independently signed-off personal review decisions or approved CRM updates.

| CRM ID | Underlying source and CRM evidence | Generated flag | Suggested action / decision gate |
|---|---|---|---|
| **C00004** | CRM C00004 and C00522 share `mei.khan288@example.com`; source L0419 has the same email | `POTENTIAL_DUPLICATE` | **Hold both** for review of source IDs, event history and whether either row is a legitimate update. Email equality alone does not authorize merging |
| **C00007** | Source L0640 surname **Patel**; CRM C00007 surname **Patei**; email `ava.patel326@example.com` matches | `LAST_NAME_CONFLICT` | Verify against the authoritative source and determine whether either record is outdated before proposing an update |
| **C00016** | Source L0315 phone **416-555-3858**; CRM C00016 phone **416-555-0598**; email `olivia.garcia393@example.com` matches | `PHONE_CONFLICT` | Check approved contact changes or source record dates; do not overwrite without confirmation |
| **C00012** | CRM C00012 has an **empty email field**, making email-only matching impossible | `MISSING_EMAIL` | Seek an authoritative ID or follow the missing-data exception process, not an invented email |
| **C00006** | CRM C00006 email `wyatt.park1007@example.com`; no matching email in the 700-row source extract | `EMAIL_NOT_IN_SOURCE` | Confirm extract coverage and alternate lead intake before deciding the record is extraneous |

A supplementary edge case, **C00108**, carries both `INVALID_EMAIL` and `POTENTIAL_DUPLICATE` because its malformed `@@` address is repeated. This shows why a duplicate flag can coexist with **unverifiable identity**.

## Source trace and approval

The [review CSV](../02-crm-data-quality/outputs/crm_review.csv) includes `matched_source_id` for exactly one matching source email: C00007 links to L0640 and C00016 to L0315. The field remains blank if the source match is absent, malformed or ambiguous. A trace link does not prove that the source is newer or that two records belong to the same person.

These are **proposed triage actions**, not completed investigations. Live corrections would require dated supporting evidence, a record owner and an approved change procedure. The [personal review log](MANUAL_REVIEW.md) remains blank.

## Review policy

- **No automatic deletion:** Duplication may represent history, a second inquiry or separate legitimate records.
- **No silent overwrite:** A source-versus-CRM conflict requires authoritative evidence and approval.
- **No invented match:** Missing or malformed contact keys are held rather than guessed.
- **Keep the trail:** Original record, detected issue and proposed disposition remain visible.

**Verification boundary:** The IDs, fields and flags above are grounded in the committed fictional CSV extracts and generated review output. The suggested actions are a review framework, not decisions executed on a production system. The [personal review log](MANUAL_REVIEW.md) is intentionally blank until genuinely completed.

[Original source CSV](../02-crm-data-quality/data/source_leads.csv) · [CRM input CSV](../02-crm-data-quality/data/crm_export.csv) · [Generated review output](../02-crm-data-quality/outputs/crm_review.csv)
