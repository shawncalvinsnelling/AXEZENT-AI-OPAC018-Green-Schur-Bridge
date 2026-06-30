# Receipts

This directory contains the full detailed per-type audit receipt for the OPAC-018 Green-Schur package.

- `opac18_green_schur_sage_results.json` records all 32 tested finite Cartan systems, highest-root marks, Green-ratio values, Schur complement values, and failure lists.
- `SHA256SUMS.txt` records package hashes.

Truth boundary: Sage is an exact-arithmetic audit, not a substitute for independent referee verification. Re-running `sage sage/opac18_green_schur_sage_test_fixed.sage` should regenerate the JSON receipt in the same schema.
