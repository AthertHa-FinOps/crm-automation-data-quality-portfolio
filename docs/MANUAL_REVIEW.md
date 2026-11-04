# Five-record independent review log

**Status: Not yet completed.** This is for an actual personal check of five fictional CRM exceptions. The existing [suggested dispositions](REVIEW_DECISIONS.md) were prepared with AI assistance and do not count as your independent decisions.

## Procedure

1. Open the [CRM input](../02-crm-data-quality/data/crm_export.csv) and [source extract](../02-crm-data-quality/data/source_leads.csv) before reading the suggested disposition. For an already-familiar case, describe the review as *reference-informed* rather than blind.
2. Inspect the records and decide whether the generated flag is appropriate. Note if a value is merely formatted differently, if evidence is incomplete or if a recommendation would be unsafe.
3. Record the actual decision, required authority and date. Do not claim a correction was applied or an owner was contacted unless it happened.
4. Compare your answer with the [proposed table](REVIEW_DECISIONS.md) afterward. Keep any disagreement rather than rewriting the original result.

| CRM record(s) | Your own finding / flag correct? | Source evidence and unresolved issue | Proposed action (hold / investigate / recommend update) | Date of actual review |
|---|---|---|---|---|
| C00004 / C00522 | | | | |
| C00007 / L0640 | | | | |
| C00016 / L0315 | | | | |
| C00012 | | | | |
| C00006 | | | | |

This worksheet stays empty until you complete the checks. A false positive should be reported only if you really identify one.

## Optional actual testing evidence

| Check you performed | Actual command / environment | Observed result and evidence location | Date |
|---|---|---|---|
| Run the Python reconciliation | | | |
| Run the CRM test suite | | | |
| Explain one flagged record without the proposed action | | | |
| Re-test n8n with fictional input (optional) | | | |

See the [data standards and SOP](DATA_STANDARDS.md) for the proposed approval and change-log process. No customer contact, system update or completed demonstration is implied.
