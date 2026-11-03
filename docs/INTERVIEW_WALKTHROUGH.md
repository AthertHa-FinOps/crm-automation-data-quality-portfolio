# Recruiter walkthrough — script for a future genuine demonstration

**No video or live CRM demo is represented as already recorded.** Use this guide only after independently checking the files and being able to explain them without reading AI-generated answers.

## Suggested two-minute sequence

**0:00–0:20:** Open [the illustrative scorecard](reconciliation-scorecard.svg) and explain the business problem: 700 fictional source leads, 733 fictional CRM rows, no assumption that row totals should match.

**0:20–0:55:** Open [C00007 in the review CSV](../02-crm-data-quality/outputs/crm_review.csv) and the source record L0640. Show the surname conflict. Explain what evidence would authorize changing either record.

**0:55–1:20:** Open C00004 and C00522. Explain why a shared normalized email identifies a review candidate but does not prove safe deletion or merging.

**1:20–1:40:** Open [the count bridge](COUNT_RECONCILIATION.md). Explain 15 valid-looking unmatched emails, 13 malformed nonblank and why SQL Q9 reports 28.

**1:40–2:00:** Open [the test suite](../02-crm-data-quality/tests/). Show what GitHub Actions confirms and state that no HubSpot API or n8n end-to-end integration has been verified.

### Interview prompts for independent preparation

- What if the original source is out of date and the CRM phone number is newer?
- What if two CRM entries share a family email but represent different people?
- Why is a sample with many planted errors **not** evidence of a typical company error rate?
- If AI writes the SQL, what must you personally verify before making a business decision?

Recording an actual walkthrough or personally reviewing exceptions is a separate future step. This script is not evidence of those actions.
