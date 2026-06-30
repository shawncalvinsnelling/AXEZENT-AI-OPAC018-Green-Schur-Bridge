# AXEZENT-AI-OPAC018-Green-Schur-Bridge

Complete Referee Edition v1.3 full-audit package.

Author: Shawn Calvin Snelling  
Affiliation: Axezent AI Research Lab

## Status

Complete OPAC-018 solution candidate manuscript. Exact Sage-compatible detailed audit packaged. External referee review pending.

## Core claim

This package presents a Green-Schur classification-free proof candidate for the OPAC-018 root-polytope projection bound. The manuscript proves the local inequality `r_alpha < 2` by an inverse-Cartan Green ratio lemma and a Schur complement argument, then transfers the result through the Cellini-Marietti reduction framework.

## Truth boundary

This package does not claim P vs NP, the Riemann Hypothesis, the Traveling Salesman Problem, journal acceptance, or historical recognition. Sage is included as an exact-arithmetic audit, not as a substitute for referee verification.

## Run the audit

From the repository root:

```bash
sage sage/opac18_green_schur_sage_test_fixed.sage
python verify_manifest.py
```

Expected Sage summary:

```json
{
  "passed": true,
  "total_types": 32,
  "failures": 0,
  "output": "receipts/opac18_green_schur_sage_results.json"
}
```

## Main files

- `paper/Green-Schur-Bridge-for-OPAC018-Complete-Referee-Edition-v1_3.pdf`
- `paper/main.tex`
- `sage/opac18_green_schur_sage_test_fixed.sage`
- `receipts/opac18_green_schur_sage_results.json` (full detailed per-type output)
- `receipts/SHA256SUMS.txt`
- `receipts/README_RECEIPTS.md`
- `CLAIMS_AND_NONCLAIMS.md`
- `SUBMISSION_COVER_LETTER_DRAFT.md`


## v1.3 full-audit update

This package replaces the short Sage receipt summary with a full detailed per-type JSON audit. The receipt includes all 32 tested finite Cartan systems, highest-root marks, Green-ratio values, Schur complement values, and failure lists. The manifest has been regenerated after this replacement.
