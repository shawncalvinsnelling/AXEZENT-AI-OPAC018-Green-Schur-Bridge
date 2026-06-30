# OPAC-018 Green-Schur candidate audit in SageMath
# Run with: sage opac18_green_schur_sage_test.sage
# Output: opac18_green_schur_sage_results.json
#
# Truth boundary:
# - Tests the Green ratio lemma and Schur complement bound on finite Cartan matrices.
# - Confirms the proof convention must use B_ij=(beta_i,beta_j^vee), the transpose of
#   Bourbaki's common convention A_ij=(alpha_i^vee,alpha_j).
# - Does NOT by itself verify the Cellini-Marietti c_epsilon bridge or peer-review OPAC-018.

from sage.all import QQ, matrix
from collections import deque
import json


def json_safe(obj):
    """Convert Sage integers/rationals and nested containers into JSON-safe Python values."""
    try:
        from sage.rings.integer import Integer
        from sage.rings.rational import Rational
    except Exception:
        Integer = ()
        Rational = ()
    if isinstance(obj, bool) or obj is None or isinstance(obj, (str, int, float)):
        return obj
    if Integer and isinstance(obj, Integer):
        return int(obj)
    if Rational and isinstance(obj, Rational):
        return str(obj)
    if isinstance(obj, (list, tuple)):
        return [json_safe(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    return str(obj)


def mat_inv(M):
    X = matrix(QQ, M).inverse()
    return [[QQ(X[i, j]) for j in range(X.ncols())] for i in range(X.nrows())]


def mat_T(A):
    return [list(row) for row in zip(*A)]


def det(M):
    return QQ(matrix(QQ, M).det())


def minor(A, idx):
    return [[A[i][j] for j in range(len(A)) if j != idx] for i in range(len(A)) if i != idx]


def refl(v, i, A):
    # A is Bourbaki convention A_ij=<alpha_i^vee, alpha_j>.
    # s_i(v)=v-<alpha_i^vee,v>*alpha_i in simple-root coordinates.
    pair = sum(v[j] * A[i][j] for j in range(len(A)))
    w = list(v)
    w[i] -= pair
    return tuple(w)


def roots(A):
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


def highest_marks(A):
    R = roots(A)
    pos = [r for r in R if all(x >= 0 for x in r) and any(x > 0 for x in r)]
    maxh = max(sum(r) for r in pos)
    tops = [r for r in pos if sum(r) == maxh]
    if len(tops) != 1:
        raise RuntimeError("highest root not unique: %s" % (tops,))
    return list(tops[0]), len(R)


def cartan_A(n):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 2
    for i in range(n - 1):
        A[i][i + 1] = A[i + 1][i] = -1
    return A


def cartan_B(n):
    A = cartan_A(n)
    A[n - 2][n - 1] = -1
    A[n - 1][n - 2] = -2
    return A


def cartan_C(n):
    A = cartan_A(n)
    A[n - 2][n - 1] = -2
    A[n - 1][n - 2] = -1
    return A


def cartan_D(n):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 2
    for i in range(n - 3):
        A[i][i + 1] = A[i + 1][i] = -1
    A[n - 3][n - 2] = A[n - 2][n - 3] = -1
    A[n - 3][n - 1] = A[n - 1][n - 3] = -1
    return A


def cartan_from_edges(n, edges):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 2
    for i, j in edges:
        A[i][j] = A[j][i] = -1
    return A


def cartan_E6():
    return cartan_from_edges(6, [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5)])


def cartan_E7():
    return cartan_from_edges(7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (2, 6)])


def cartan_E8():
    return cartan_from_edges(8, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)])


def cartan_F4():
    return [[2, -1, 0, 0], [-1, 2, -2, 0], [0, -1, 2, -1], [0, 0, -1, 2]]


def cartan_G2():
    return [[2, -1], [-3, 2]]


def finite_types(max_classical_rank=8):
    out = []
    for n in range(1, max_classical_rank + 1):
        out.append(("A%d" % n, cartan_A(n)))
    for n in range(2, max_classical_rank + 1):
        out.append(("B%d" % n, cartan_B(n)))
        out.append(("C%d" % n, cartan_C(n)))
    for n in range(4, max_classical_rank + 1):
        out.append(("D%d" % n, cartan_D(n)))
    out += [("E6", cartan_E6()), ("E7", cartan_E7()), ("E8", cartan_E8()), ("F4", cartan_F4()), ("G2", cartan_G2())]
    return out


def green_test(B, marks):
    G = mat_inv(B)
    n = len(B)
    fails = []
    values = []
    for e in range(n):
        ratios = [G[e][j] / QQ(marks[j]) for j in range(n)]
        lhs = max(ratios)
        mid = G[e][e] / QQ(marks[e])
        rhs = G[e][e]
        row = {
            "node": e,
            "lhs_max_ratio": str(lhs),
            "mid_diag_over_mark": str(mid),
            "rhs_diag": str(rhs),
            "ratios": [str(r) for r in ratios],
        }
        values.append(row)
        if not (lhs <= mid <= rhs):
            fails.append(row)
    return fails, values


def schur_test(C):
    n = len(C)
    fails = []
    values = []
    for alpha in range(n):
        B = minor(C, alpha)
        Binv = mat_inv(B)
        rest = [i for i in range(n) if i != alpha]
        a = [-C[alpha][j] for j in rest]
        b = [-C[i][alpha] for i in rest]
        S = sum(QQ(a[p]) * Binv[p][q] * QQ(b[q]) for p in range(n - 1) for q in range(n - 1))
        schur = QQ(2) - S
        ratio = det(C) / det(B)
        values.append({"node": alpha, "S": str(S), "2_minus_S": str(schur), "det_ratio": str(ratio)})
        if schur != ratio or not (S < 2):
            fails.append({"node": alpha, "S": str(S), "2_minus_S": str(schur), "det_ratio": str(ratio)})
    return fails, values


def main():
    expected_counts = {}
    expected_counts.update({"A%d" % n: n * (n + 1) for n in range(1, 9)})
    expected_counts.update({"B%d" % n: 2 * n * n for n in range(2, 9)})
    expected_counts.update({"C%d" % n: 2 * n * n for n in range(2, 9)})
    expected_counts.update({"D%d" % n: 2 * n * (n - 1) for n in range(4, 9)})
    expected_counts.update({"E6": 72, "E7": 126, "E8": 240, "F4": 48, "G2": 12})

    summary = []
    failures = []
    for name, A in finite_types(8):
        marks, count = highest_marks(A)
        B_proof = mat_T(A)
        green_fails, green_values = green_test(B_proof, marks)
        schur_fails, schur_values = schur_test(B_proof)
        bourbaki_green_fails, bourbaki_green_values = green_test(A, marks)
        item = {
            "type": name,
            "rank": len(A),
            "root_count": count,
            "expected_root_count": expected_counts[name],
            "highest_root_marks": marks,
            "green_ratio_failures_proof_convention": green_fails,
            "green_ratio_values_proof_convention": green_values,
            "schur_failures_proof_convention": schur_fails,
            "green_ratio_failures_bourbaki_orientation": len(bourbaki_green_fails),
            "green_ratio_values_bourbaki_orientation": bourbaki_green_values,
            "schur_values_proof_convention": schur_values,
        }
        summary.append(item)
        if count != expected_counts[name] or green_fails or schur_fails:
            failures.append(item)

    report = {
        "truth_label": "FINITE_CARTAN_EXACT_SAGE_TEST",
        "manuscript_version": "v1.4 mainstream-hardening package",
        "receipt_level": "full detailed per-type audit",
        "scope": "A1-A8, B2-B8, C2-C8, D4-D8, E6, E7, E8, F4, G2",
        "important_convention": "Green ratio lemma should be stated using B = transpose(Bourbaki Cartan), i.e. B_ij=(beta_i,beta_j^vee). It fails in non-simply-laced types if the opposite convention is used.",
        "tested_claims": [
            "root counts match expected finite root systems",
            "Green ratio maximum lemma in proof Cartan convention",
            "Schur complement bound a^T B^-1 b < 2 for every deleted node",
        ],
        "not_tested": [
            "Cellini-Marietti c_epsilon exact notation bridge",
            "external referee acceptance",
            "full OPAC-018 transfer beyond the cited reduction",
        ],
        "total_types": len(summary),
        "failures": failures,
        "passed": len(failures) == 0,
        "summary": summary,
    }
    os.makedirs("receipts", exist_ok=True)
    with open("receipts/opac18_green_schur_sage_results.json", "w") as f:
        json.dump(json_safe(report), f, indent=2, sort_keys=True)
    print(json.dumps(json_safe({"passed": report["passed"], "total_types": report["total_types"], "failures": len(report["failures"]), "output": "receipts/opac18_green_schur_sage_results.json"}), indent=2))


main()
