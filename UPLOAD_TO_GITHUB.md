# Upload to GitHub

## Simple drag-and-drop method

1. Download and unzip this package.
2. Open the extracted folder:
   `AXEZENT-AI-OPAC018-Green-Schur-Bridge`
3. Create a new GitHub repository named:
   `AXEZENT-AI-OPAC018-Green-Schur-Bridge`
4. Drag **all files and folders inside this extracted folder** into the GitHub web upload page.
5. Commit with this message:

```text
Initial public referee package for OPAC-018 Green-Schur Bridge v1.4
```

## Recommended local verification

Run:

```bash
python verify_manifest.py
```

Expected output:

```text
MANIFEST_CHECK_PASS
```

If SageMath is installed, optionally regenerate the exact-arithmetic audit:

```bash
sage sage/opac18_green_schur_sage_test_fixed.sage
python verify_manifest.py
```

## Public status line

Complete OPAC-018 solution candidate manuscript; exact Sage audit passed; external referee review pending.
