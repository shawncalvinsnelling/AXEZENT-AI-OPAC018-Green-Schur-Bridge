#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

root = Path(__file__).resolve().parent
manifest = root / "receipts" / "SHA256SUMS.txt"
if not manifest.exists():
    print("MANIFEST_CHECK_FAIL: receipts/SHA256SUMS.txt missing")
    sys.exit(1)

expected = {}
for line in manifest.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line:
        continue
    digest, rel = line.split(maxsplit=1)
    expected[rel] = digest

ok = True
for rel, digest in expected.items():
    path = root / rel
    if not path.exists():
        print(f"MISSING {rel}")
        ok = False
        continue
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != digest:
        print(f"HASH_MISMATCH {rel}\n  expected {digest}\n  got      {got}")
        ok = False
    else:
        print(f"OK {rel}")

tracked = set(expected)
for path in sorted(root.rglob("*")):
    if path.is_file():
        rel = path.relative_to(root).as_posix()
        if rel not in tracked and rel != "receipts/SHA256SUMS.txt":
            print(f"UNTRACKED {rel}")

if ok:
    print("MANIFEST_CHECK_PASS")
else:
    print("MANIFEST_CHECK_FAIL")
    sys.exit(1)
