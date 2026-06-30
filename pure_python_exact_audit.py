#!/usr/bin/env python3
"""
Pure-Python exact audit for the Green-Schur OPAC-018 package.

Purpose:
  Independent check that does not import Sage, NumPy, SymPy, or any root-system library.
  Uses only Python's standard library and fractions.Fraction.

Truth boundary:
  This is an exact arithmetic audit of Cartan matrices, Green-ratio inequalities,
  Schur complement inequalities, and root-count sanity checks in the stated finite
  test range. It is not a substitute for independent mathematical referee review.
"""
from __future__ import annotations

from collections import deque
from fractions import Fraction
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Matrix = List[List[int]]
QMatrix = List[List[Fraction]]
Vector = Tuple[int, ...]


def q(x: int | Fraction) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x, 1)


def transpose(A: Sequence[Sequence[int]]) -> Matrix:
    return [list(row) for row in zip(*A)]


def determinant(M: Sequence[Sequence[int | Fraction]]) -> Fraction:
    A = [[q(x) for x in row] for row in M]
    n = len(A)
    det = Fraction(1)
    for i in range(n):
        pivot = None
        for r in range(i, n):
            if A[r][i] != 0:
                pivot = r
                break
        if pivot is None:
            return Fraction(0)
        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
            det *= -1
        pv = A[i][i]
        det *= pv
        for r in range(i + 1, n):
            factor = A[r][i] / pv
            if factor:
                for c in range(i, n):
                    A[r][c] -= factor * A[i][c]
    return det


def inverse(M: Sequence[Sequence[int | Fraction]]) -> QMatrix:
    A = [[q(x) for x in row] for row in M]
    n = len(A)
    I = [[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = None
        for r in range(i, n):
            if A[r][i] != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
            I[i], I[pivot] = I[pivot], I[i]
        pv = A[i][i]
        for c in range(n):
            A[i][c] /= pv
            I[i][c] /= pv
        for r in range(n):
            if r == i:
                continue
            factor = A[r][i]
            if factor:
                for c in range(n):
                    A[r][c] -= factor * A[i][c]
                    I[r][c] -= factor * I[i][c]
    return I


def minor(A: Sequence[Sequence[int]], idx: int) -> Matrix:
    return [[A[i][j] for j in range(len(A)) if j != idx] for i in range(len(A)) if i != idx]


def refl(v: Vector, i: int, A: Matrix) -> Vector:
    # A is Bourbaki convention A_ij=<alpha_i^vee, alpha_j>.
    pair = sum(v[j] * A[i][j] for j in range(len(A)))
    w = list(v)
    w[i] -= pair
    return tuple(w)


def roots(A: Matrix) -> set[Vector]:
    n = len(A)
    gens = [tuple(1 if i == j else 0 for j in range(n)) for i in range(n)]
    seen = set(gens + [tuple(-x for x in g) for g in gens])
    dq = deque(seen)
    while dq:
        v = dq.popleft()
        for i in range(n):
            w = refl(v, i, A)
            if w not in seen:
                seen.add(w)
                dq.append(w)
                if len(seen) > 10000:
                    raise RuntimeError("too many roots; likely bad Cartan matrix")
    return seen


def highest_marks(A: Matrix) -> Tuple[List[int], int]:
    R = roots(A)
    pos = [r for r in R if all(x >= 0 for x in r) and any(x > 0 for x in r)]
    maxh = max(sum(r) for r in pos)
    tops = [r for r in pos if sum(r) == maxh]
    if len(tops) != 1:
        raise RuntimeError(f"highest root not unique: {tops}")
    return list(tops[0]), len(R)


def cartan_A(n: int) -> Matrix:
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 2
    for i in range(n - 1):
        A[i][i + 1] = A[i + 1][i] = -1
    return A


def cartan_B(n: int) -> Matrix:
    A = cartan_A(n)
    A[n - 2][n - 1] = -1
    A[n - 1][n - 2] = -2
    return A


def cartan_C(n: int) -> Matrix:
    A = cartan_A(n)
    A[n - 2][n - 1] = -2
    A[n - 1][n - 2] = -1
    return A


def cartan_D(n: int) -> Matrix:
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 2
    for i in range(n - 3):
        A[i][i + 1] = A[i + 1][i] = -1
    A[n - 3][n - 2] = A[n - 2][n - 3] = -1
    A[n - 3][n - 1] = A[n - 1][n - 3] = -1
    return A


def cartan_from_edges(n: int, edges: Iterable[Tuple[int, int]]) -> Matrix:
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 2
    for i, j in edges:
        A[i][j] = A[j][i] = -1
    return A


def cartan_E6() -> Matrix:
    return cartan_from_edges(6, [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5)])


def cartan_E7() -> Matrix:
    return cartan_from_edges(7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (2, 6)])


def cartan_E8() -> Matrix:
    return cartan_from_edges(8, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)])


def cartan_F4() -> Matrix:
    return [[2, -1, 0, 0], [-1, 2, -2, 0], [0, -1, 2, -1], [0, 0, -1, 2]]


def cartan_G2() -> Matrix:
    return [[2, -1], [-3, 2]]


def finite_types(max_classical_rank: int = 8) -> List[Tuple[str, Matrix]]:
    out: List[Tuple[str, Matrix]] = []
    for n in range(1, max_classical_rank + 1):
        out.append((f"A{n}", cartan_A(n)))
    for n in range(2, max_classical_rank + 1):
        out.append((f"B{n}", cartan_B(n)))
        out.append((f"C{n}", cartan_C(n)))
    for n in range(4, max_classical_rank + 1):
        out.append((f"D{n}", cartan_D(n)))
    out += [("E6", cartan_E6()), ("E7", cartan_E7()), ("E8", cartan_E8()), ("F4", cartan_F4()), ("G2", cartan_G2())]
    return out


def frac_str(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def green_values(B: Matrix, marks: Sequence[int]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    G = inverse(B)
    values = []
    fails = []
    for e in range(len(B)):
        ratios = [G[e][j] / Fraction(marks[j], 1) for j in range(len(B))]
        lhs = max(ratios)
        mid = G[e][e] / Fraction(marks[e], 1)
        rhs = G[e][e]
        item = {
            "node": e,
            "lhs_max_ratio": frac_str(lhs),
            "mid_diag_over_mark": frac_str(mid),
            "rhs_diag": frac_str(rhs),
            "ratios": [frac_str(r) for r in ratios],
            "passed": lhs <= mid <= rhs,
        }
        values.append(item)
        if not item["passed"]:
            fails.append(item)
    return values, fails


def schur_values(C: Matrix) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    values = []
    fails = []
    n = len(C)
    for alpha in range(n):
        B = minor(C, alpha)
        Binv = inverse(B)
        rest = [i for i in range(n) if i != alpha]
        a = [-C[alpha][j] for j in rest]
        b = [-C[i][alpha] for i in rest]
        S = sum(Fraction(a[p]) * Binv[p][q] * Fraction(b[q]) for p in range(n - 1) for q in range(n - 1))
        schur = Fraction(2) - S
        ratio = determinant(C) / determinant(B)
        item = {"node": alpha, "S": frac_str(S), "2_minus_S": frac_str(schur), "det_ratio": frac_str(ratio), "passed": (schur == ratio and S < 2)}
        values.append(item)
        if not item["passed"]:
            fails.append(item)
    return values, fails


def expected_root_counts() -> Dict[str, int]:
    e: Dict[str, int] = {}
    e.update({f"A{n}": n * (n + 1) for n in range(1, 9)})
    e.update({f"B{n}": 2 * n * n for n in range(2, 9)})
    e.update({f"C{n}": 2 * n * n for n in range(2, 9)})
    e.update({f"D{n}": 2 * n * (n - 1) for n in range(4, 9)})
    e.update({"E6": 72, "E7": 126, "E8": 240, "F4": 48, "G2": 12})
    return e


def main() -> int:
    expected = expected_root_counts()
    summary = []
    failures = []
    for name, A in finite_types(8):
        marks, count = highest_marks(A)
        B_proof = transpose(A)
        gv, gf = green_values(B_proof, marks)
        sv, sf = schur_values(B_proof)
        bgv, bgf = green_values(A, marks)
        item = {
            "type": name,
            "rank": len(A),
            "root_count": count,
            "expected_root_count": expected[name],
            "highest_root_marks": marks,
            "green_ratio_values_proof_convention": gv,
            "green_ratio_failures_proof_convention": gf,
            "schur_values_proof_convention": sv,
            "schur_failures_proof_convention": sf,
            "green_ratio_values_bourbaki_orientation": bgv,
            "green_ratio_failures_bourbaki_orientation": bgf,
        }
        summary.append(item)
        if count != expected[name] or gf or sf:
            failures.append(item)
    report = {
        "truth_label": "PURE_PYTHON_EXACT_CARTAN_AUDIT",
        "manuscript_version": "v1.4 mainstream hardening package",
        "dependency_policy": "standard library only; no Sage, NumPy, SymPy, or root-system libraries",
        "scope": "A1-A8, B2-B8, C2-C8, D4-D8, E6, E7, E8, F4, G2",
        "tested_claims": [
            "root counts match expected finite systems",
            "Green ratio maximum lemma in proof Cartan convention",
            "Schur complement bound a^T B^-1 b < 2 for every deleted node",
        ],
        "total_types": len(summary),
        "failures": failures,
        "passed": len(failures) == 0,
        "summary": summary,
    }
    out = Path("receipts/opac18_green_schur_pure_python_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "total_types": report["total_types"], "failures": len(report["failures"]), "output": str(out)}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
