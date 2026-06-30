# AXEZENT-AI-OPAC018-Green-Schur-Bridge

Complete Referee Edition v1.4 mainstream-hardening package.

Author: Shawn Calvin Snelling  
Affiliation: Axezent AI Research Lab

## Status

Complete OPAC-018 solution candidate manuscript. Exact Sage detailed audit packaged. Pure-Python independent audit packaged. Counterexample stress-test protocol packaged. External referee review pending.

## Core claim

This package presents a Green-Schur classification-free proof candidate for the OPAC-018 root-polytope projection bound. The manuscript proves the local inequality `r_alpha < 2` by an inverse-Cartan Green ratio lemma and a Schur complement argument, then transfers the result through the Cellini-Marietti reduction framework.

## Truth boundary

This package does not claim P vs NP, the Riemann Hypothesis, the Traveling Salesman Problem, journal acceptance, arXiv acceptance, or historical recognition. Sage and Python scripts are included as exact-arithmetic audits, not as substitutes for independent referee verification.

## Run the audits

From the repository root:

```bash
python verify_manifest.py
python pure_python_exact_audit.py
python counterexample_stress_test.py
```

Optional Sage audit, if SageMath is installed:

```bash
sage sage/opac18_green_schur_sage_test_fixed.sage
python verify_manifest.py
```

Expected pure-Python summary:

```json
{
  "passed": true,
  "total_types": 32,
  "failures": 0,
  "output": "receipts/opac18_green_schur_pure_python_results.json"
}
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

- `paper/Green-Schur-Bridge-for-OPAC018-Complete-Referee-Edition-v1_4.pdf`
- `paper/main.tex`
- `sage/opac18_green_schur_sage_test_fixed.sage`
- `pure_python_exact_audit.py`
- `counterexample_stress_test.py`
- `receipts/opac18_green_schur_sage_results.json` full detailed per-type Sage-compatible receipt
- `receipts/opac18_green_schur_pure_python_results.json` independent exact audit receipt
- `receipts/counterexample_stress_test_results.json` stress-test receipt
- `receipts/SHA256SUMS.txt`
- `docs/INFINITE_FAMILY_SYMBOLIC_SUPPLEMENT.md`
- `docs/GEOMETRIC_DICTIONARY.md`
- `docs/COUNTEREXAMPLE_STRESS_TEST_PROTOCOL.md`
- `docs/ARXIV_SUBMISSION_PLAN.md`
- `.github/workflows/manifest-check.yml`
- `.github/workflows/python-exact-audit.yml`
- `.github/workflows/sage-audit-manual.yml`
- `CLAIMS_AND_NONCLAIMS.md`
- `SUBMISSION_COVER_LETTER_DRAFT.md`

## v1.4 mainstream-hardening update

v1.4 adds the final reviewer-facing assets requested for mainstream mathematical review:

1. Infinite-family symbolic supplement for `A_n`, `B_n`, `C_n`, and `D_n`.
2. Counterexample/stress-test script documenting failure modes outside the theorem's hypotheses.
3. Geometric dictionary translating the matrix proof back into convex containment language.
4. Pure-Python exact audit with no Sage, NumPy, SymPy, or root-system library dependency.
5. GitHub Actions workflows for manifest and pure-Python audits, plus a manual Sage audit workflow.
6. arXiv submission plan with safe status wording.
