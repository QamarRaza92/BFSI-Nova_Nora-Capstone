# BFSI Claims Processing Agent — Mock Data

Synthetic capstone data:
- 15 policy PDFs in `policies/`
- 30 historical claims in `claims_history.csv`
- 15 evaluation claims in `test_claims.csv`

Design:
- Policy IDs P001–P015.
- Historical customers C001–C014 have deliberately varied claim patterns.
- Test claims include covered, excluded, over-limit, repeated-claim, and adversarial/prompt-injection cases.
- `expected_behavior` is a testing guide, not ground truth for a production system.

Important:
- All data is synthetic.
- The policy PDFs are the source corpus for RAG.
- `claims_history.csv` is used by the history and fraud tools.
- `test_claims.csv` is used for evaluation.
