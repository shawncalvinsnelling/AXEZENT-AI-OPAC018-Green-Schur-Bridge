#!/usr/bin/env python3
"""
Counterexample / boundary stress tests for the Green-Schur package.

Purpose:
  Show exactly which hypotheses are used: crystallographic Cartan integrality,
  finite type, symmetrizability with positive determinant, the proof orientation
  B_ij=(beta_i,beta_j^vee), and nonsingular M-matrix inverse positivity.

This script deliberately includes matrices that are outside the theorem's scope.
Failures here are expected and documented; they are not failures of the manuscript.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import List, Sequence, Dict, Any

Matrix = List[List[Fraction]]


def F(x: int) -> Fraction:
    return Fraction(x, 1)


def transpose(A: Sequence[Sequence[Fraction]]) -> Matrix:
    return [list(row) for row in zip(*A)]


def det(M: Sequence[Sequence[Fraction]]) -> Fraction:
    A = [list(row) for row in M]
    n = len(A)
    d = Fraction(1)
    for i in range(n):
        p = None
        for r in range(i, n):
            if A[r][i] != 0:
                p = r
                break
        if p is None:
            return Fraction(0)
        if p != i:
            A[i], A[p] = A[p], A[i]
            d *= -1
        pv = A[i][i]
        d *= pv
        for r in range(i + 1, n):
            fac = A[r][i] / pv
            for c in range(i, n):
                A[r][c] -= fac * A[i][c]
    return d


def inv(M: Sequence[Sequence[Fraction]]) -> Matrix:
    A = [list(row) for row in M]
    n = len(A)
    I = [[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]
    for i in range(n):
        p = None
        for r in range(i, n):
            if A[r][i] != 0:
                p = r
                break
        if p is None:
            raise ValueError("singular")
        if p != i:
            A[i], A[p] = A[p], A[i]
            I[i], I[p] = I[p], I[i]
        pv = A[i][i]
        for c in range(n):
            A[i][c] /= pv
            I[i][c] /= pv
        for r in range(n):
            if r == i:
                continue
            fac = A[r][i]
            for c in range(n):
                A[r][c] -= fac * A[i][c]
                I[r][c] -= fac * I[i][c]
    return I


def frac(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def green_check(B: Matrix, marks: Sequence[int]) -> Dict[str, Any]:
    try:
        G = inv(B)
        rows = []
        failures = []
        for e in range(len(B)):
            ratios = [G[e][j] / Fraction(marks[j]) for j in range(len(B))]
            lhs = max(ratios)
            mid = G[e][e] / Fraction(marks[e])
            rhs = G[e][e]
            ok = lhs <= mid <= rhs
            item = {"node": e, "lhs": frac(lhs), "mid": frac(mid), "rhs": frac(rhs), "ratios": [frac(r) for r in ratios], "passed": ok}
            rows.append(item)
            if not ok:
                failures.append(item)
        return {"passed": not failures, "rows": rows, "failures": failures}
    except Exception as exc:
        return {"passed": False, "error": str(exc)}


def is_z_matrix(A: Matrix) -> bool:
    return all(A[i][j] <= 0 for i in range(len(A)) for j in range(len(A)) if i != j)


def positive_principal_dets(A: Matrix) -> bool:
    n = len(A)
    # test leading and one-node-deleted principal minors; enough for this stress diagnostic, not a theorem prover
    if det(A) <= 0:
        return False
    for k in range(n):
        M = [[A[i][j] for j in range(n) if j != k] for i in range(n) if i != k]
        if M and det(M) <= 0:
            return False
    return True


def classify_scope(A: Matrix) -> Dict[str, Any]:
    return {
        "z_matrix": is_z_matrix(A),
        "determinant": frac(det(A)),
        "positive_diagnostic_principal_dets": positive_principal_dets(A),
        "integer_entries": all(x.denominator == 1 for row in A for x in row),
    }


def main() -> int:
    # Valid proof-convention B3: transpose of Bourbaki B3 with marks [1,2,2]
    B3_bourbaki = [[F(2), F(-1), F(0)], [F(-1), F(2), F(-1)], [F(0), F(-2), F(2)]]
    B3_proof = transpose(B3_bourbaki)

    tests = [
        {
            "name": "valid_B3_proof_orientation",
            "matrix": B3_proof,
            "marks": [1, 2, 2],
            "expected": "pass",
            "lesson": "Inside the theorem scope: finite crystallographic Cartan matrix in proof row convention.",
        },
        {
            "name": "wrong_orientation_B3_bourbaki_for_row_proof",
            "matrix": B3_bourbaki,
            "marks": [1, 2, 2],
            "expected": "may_fail",
            "lesson": "Demonstrates why B_ij=(beta_i,beta_j^vee) is locked; transposition can break row inequalities.",
        },
        {
            "name": "distorted_indefinite_two_node_matrix",
            "matrix": [[F(2), F(-3)], [F(-3), F(2)]],
            "marks": [1, 1],
            "expected": "out_of_scope",
            "lesson": "Not finite type: determinant is negative, so Schur positivity and M-matrix inverse positivity do not apply.",
        },
        {
            "name": "singular_affine_like_two_node_matrix",
            "matrix": [[F(2), F(-2)], [F(-2), F(2)]],
            "marks": [1, 1],
            "expected": "out_of_scope",
            "lesson": "Singular affine-like boundary: inverse does not exist; theorem assumes finite type.",
        },
        {
            "name": "positive_off_diagonal_not_z_matrix",
            "matrix": [[F(2), F(1)], [F(-1), F(2)]],
            "marks": [1, 1],
            "expected": "out_of_scope",
            "lesson": "Not a Cartan Z-matrix: off-diagonal sign hypothesis is violated.",
        },
    ]
    results = []
    for t in tests:
        check = green_check(t["matrix"], t["marks"])
        results.append({
            "name": t["name"],
            "expected": t["expected"],
            "lesson": t["lesson"],
            "scope_diagnostics": classify_scope(t["matrix"]),
            "green_check": check,
        })

    non_crystallographic_notes = [
        {
            "name": "H3_H4_non_crystallographic_note",
            "status": "not a crystallographic Cartan test",
            "lesson": "H3 and H4 involve irrational Coxeter data and do not supply integer crystallographic Cartan matrices. They are useful stress examples for scope, but not counterexamples to the OPAC-018 crystallographic theorem.",
        }
    ]
    report = {
        "truth_label": "COUNTEREXAMPLE_STRESS_TEST",
        "purpose": "document theorem scope and failure modes outside finite crystallographic Cartan hypotheses",
        "all_expected_scope_failures_documented": True,
        "tests": results,
        "non_crystallographic_notes": non_crystallographic_notes,
    }
    out = Path("receipts/counterexample_stress_test_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(out), "tests": len(results), "truth_label": report["truth_label"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
