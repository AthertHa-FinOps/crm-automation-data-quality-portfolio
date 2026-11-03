# Two-minute portfolio walkthrough outline

**Format:** A guide for a future demonstration. No recording or independent owner-review result is claimed here.

**0:00–0:20 — Explain the comparison.** Open the [scorecard](reconciliation-scorecard.svg). The fictional source has 700 leads and the CRM export has 733 rows. A row-count difference does not itself establish which records need changing.

**0:20–0:55 — Inspect a disputed surname.** Find C00007 in the [review CSV](../02-crm-data-quality/outputs/crm_review.csv), then use `matched_source_id` to find L0640 in the source extract. CRM says Patei; source says Patel. Explain why this requires checking the record's authority and date, rather than automatically editing it.

**0:55–1:20 — Check a possible duplicate.** Compare CRM records C00004 and C00522, which share a normalized email. Explain why both are preserved for review rather than merged.

**1:20–1:40 — Reconcile the counts.** Open the [count bridge](COUNT_RECONCILIATION.md). Python has 15 valid-looking unmatched emails; SQL includes 13 malformed addresses and reports 28.

**1:40–2:00 — Describe what passed.** Open the [test workflow](../.github/workflows/data-quality-tests.yml). Explain the record-quality checks and isolated n8n export tests. One local n8n missing-email test (T03) also returned HTTP 422 on November 3, 2026; see the [record](../01-lead-to-crm-automation/evidence/T03-2026-11-03.md). State clearly that no HubSpot end-to-end run is recorded.

## Questions worth preparing

- If the source row is old and the CRM phone number is newer, what evidence controls the decision?
- If a family uses one email address, when is a merge unsafe?
- Why are the 311 flagged rows not the sum of issue categories?
- Which tests demonstrate the actual workflow, and which only inspect its source?
- What should an operator do when a contact write may have succeeded but the API response is lost?

A recorded demonstration and independent review are separate steps. The [completion checklist](COMPLETION_CHECKLIST.md) identifies the supporting evidence required.
