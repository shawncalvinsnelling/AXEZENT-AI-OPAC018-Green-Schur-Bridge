# START HERE

This repository contains the complete public referee package for:

**The Green-Schur Bridge for OPAC-018**  
*A Classification-Free Cartan-Schur Proof Candidate of the Root Polytope Projection Bound*  
Shawn Calvin Snelling — Axezent AI Research Lab

## Read first

1. `README.md`
2. `CLAIMS_AND_NONCLAIMS.md`
3. `paper/Green-Schur-Bridge-for-OPAC018-Complete-Referee-Edition-v1_4.pdf`
4. `docs/INFINITE_FAMILY_SYMBOLIC_SUPPLEMENT.md`
5. `docs/GEOMETRIC_DICTIONARY.md`
6. `receipts/opac18_green_schur_sage_results.json`
7. `receipts/opac18_green_schur_pure_python_results.json`

## Verify package integrity

```bash
python verify_manifest.py
```

Expected:

```text
MANIFEST_CHECK_PASS
```

## Run independent pure-Python audit

```bash
python pure_python_exact_audit.py
python counterexample_stress_test.py
python verify_manifest.py
```

Optional Sage audit, when SageMath is installed:

```bash
sage sage/opac18_green_schur_sage_test_fixed.sage
python verify_manifest.py
```

## Truth boundary

This is a complete OPAC-018 solution candidate manuscript with exact-arithmetic audit assets.  
Independent referee review remains pending.
