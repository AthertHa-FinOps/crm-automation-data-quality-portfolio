# CRM data standards and exception-review SOP

**Scope:** A fictional 700-lead source CSV and 733-row CRM-style CSV. This document distinguishes controls enforced by the repository's Python review from procedures proposed for a real CRM team. Nothing here is an employer-approved policy.

## 1. Record and field rules

| Field | Implemented check in `run_analysis.py` | Proposed operator rule / limitation |
|---|---|---|
| `crm_id` | Rejects blank IDs or duplicates after trim and case normalization; retains original value | Confirm native CRM identifier and never replace it with a fabricated ID; the illustrated `C00000` pattern is **not** enforced |
| `lead_id` (source) | Rejects blank IDs or duplicates after trim and case normalization | Keep the original source-row key; the illustrated `L0000` pattern is **not** enforced |
| `email` | Trims/lowercases into `normalized_email`; flags blank, basic format failures and case/spacing differences | Do not treat the simplified regex as delivery/ownership verification; hold unverified addresses |
| `phone` | Strips non-digits and optional leading country code 1; suggests `NNN-NNN-NNNN`; flags invalid formats and differing digits for a unique source match | Phone agreement does not prove ownership; confirm the current number with an authorized source |
| `last_name` | Compares the original text exactly to the single matched source row; differences raise `LAST_NAME_CONFLICT` | Comparison is **case-sensitive**, not fuzzy matching; verify legal name and effective correction |
| `province` | Suggests `ON` for common Ontario variants and flags changed formatting | The script does not enforce a complete Canadian province dictionary |
| `lead_source` | Flags a blank/whitespace-only value | Decide required intake provenance in the actual CRM's field rules |
| `first_name`, `city`, `created_date` | Original values preserved; **not** compared to source or validated for authority, timing or uniqueness | A creation timestamp is not confirmation that a contact detail is current or correct |
| `source_match` | Reports `ONE_EMAIL_MATCH`, `NO_EMAIL_MATCH`, `UNVERIFIABLE_EMAIL`, or `AMBIGUOUS_EMAIL` (on applicable inputs) | Matching is by normalized email alone; use an authoritative identifier before any edit or merge |
| `matched_source_id` | Populated only for one valid-email source match; otherwise blank | A trace link, **not** identity verification or permission to overwrite |
| `review_flags` | Lists all triggered rules; `PASS_PRELIMINARY` means no rule fired | Neither a flag nor a preliminary pass is human approval |

All nine original CRM input fields are retained. Normalized values and review outcomes are **new output columns**, not changes to the input records. The script does not validate contact consent, access permissions, email deliverability or all field requirements.

## 2. Duplicate and discrepancy policy — proposed

- `POTENTIAL_DUPLICATE` means two or more nonblank normalized CRM emails match, including malformed repeated strings. An email group is not a confirmed duplicate.
- Review source IDs, inquiry/transaction history, approved amendments and record ownership. Even matching names and phones are **not** sufficient authorization to merge or delete.
- For a surname or phone conflict, preserve both values and verify which record is authoritative. **Do not default to the newest timestamp.** Check when and by whom a field was confirmed.
- Where the source cannot be matched, hold the exception; investigate extract coverage, other intake channels and trustworthy alternate identifiers. Do not label it a newly created or unauthorized contact.
- For missing or malformed values, request evidence rather than inventing a replacement. Keep requested changes pending approval.

## 3. Repeatable review procedure — proposed, not a completed live process

1. Secure approval to work with the dataset; preserve an unchanged copy and note extract date and systems.
2. Run `python 02-crm-data-quality/run_analysis.py`; verify source, CRM and output counts plus blank/duplicate ID checks.
3. Check the [control report](../02-crm-data-quality/outputs/control_report.md) and filter [review output](../02-crm-data-quality/outputs/crm_review.csv) by issue. The 15 valid-looking unmatched and 13 malformed nonblank addresses are different populations ([count bridge](COUNT_RECONCILIATION.md)).
4. Investigate the source evidence using `matched_source_id` only where uniquely present. Record the uncertainty and do **not** silently accept generated suggested values.
5. Assign the question to the authorized record owner. Keep disputed records unchanged until evidence, privacy/consent requirements and any approval step are satisfied.
6. Record approved changes in the CRM's native audit trail or a controlled log. Retain both the original and approved value and the evidence used.
7. After an authorized change, repeat the extract/reconciliation and have a separate reviewer confirm the resolution where the team's policy requires it. **This portfolio performs no live updates or post-change validation.**

## 4. Proposed change log fields

| Column | Meaning |
|---|---|
| CRM ID and field | Exact record and attribute being reviewed |
| Original value / proposed value | Do not overwrite the original evidence in the log |
| Source ID and supporting evidence | Link or dated reference; note when unavailable |
| Disposition | Hold, request evidence, approved correction or closed without change |
| Record owner / approver | Person authorized to decide, not inferred from the email |
| Approval evidence and date | Who confirmed the value and when |
| Operator and change timestamp | Who applied an authorized correction and when |
| Second check / outcome | Follow-up verification, if performed |

No log rows or human approvals have been fabricated in this sample.

## 5. Fictional correction request to a record owner

> **Subject:** Confirm phone discrepancy for CRM C00016
>
> The CRM-style export shows `416-555-0598` on C00016, while fictional lead record L0315 shows `416-555-3858`. I have left both records unchanged.
>
> Can you confirm which number was last verified, when it was confirmed and what evidence we should retain? Once the authorized owner approves a correction, it can be recorded using the team's change-control procedure.

This is a sample message only; it has not been sent.

## 6. Scope and limitations

The sample uses deliberately planted issues; detection and false-positive rates on unseen contacts have **not** been measured. The script checks record identifiers for presence and uniqueness but does not enforce production ID formats. Email is the only source-match key; phone and surname compare only after a unique email match. There is no native CRM import, live contact merge, user-permission test or approved corrective action in this repository.

[Five sample exceptions](REVIEW_DECISIONS.md) · [Manager's review brief](OPERATIONS_BRIEF.md) · [Blank personal review log](MANUAL_REVIEW.md)
