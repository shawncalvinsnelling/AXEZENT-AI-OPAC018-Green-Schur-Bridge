# Infinite-Family Symbolic Supplement

Truth status: referee hardening supplement, not a replacement for the type-free proof.

The main manuscript does not depend on checking the infinite classical families one by one. Its logical core uses finite-type Cartan symmetrizability, nonsingular M-matrix inverse positivity, highest-root dominance, and the Schur complement. Those facts apply uniformly to every finite crystallographic root system.

This supplement addresses a common referee question: what happens to the classical families as the rank grows?

## Classical determinant recurrences

For the standard finite crystallographic Cartan matrices, the determinants satisfy the following rank-uniform formulas.

| Family | Rank range | Determinant |
|---|---:|---:|
| `A_n` | `n >= 1` | `n + 1` |
| `B_n` | `n >= 2` | `2` |
| `C_n` | `n >= 2` | `2` |
| `D_n` | `n >= 4` | `4` |

The `A_n` determinant follows from the tridiagonal recurrence

```text
D_n = 2 D_{n-1} - D_{n-2},  D_0 = 1, D_1 = 2,
```

so `D_n = n + 1`.

The `B_n` and `C_n` determinant recurrences terminate at the single doubled edge and give determinant `2` for all `n >= 2`. The `D_n` recurrence terminates at the fork and gives determinant `4` for all `n >= 4`.

## Schur complement rank-uniformity

For any simple root deletion block

```text
C = [[2, -a^T], [-b, B]],
```

the Schur complement identity gives

```text
det(C) = det(B) * (2 - a^T B^{-1} b).
```

Since the finite-type determinant formulas above are positive, and principal blocks decompose into products of positive classical determinants, `det(C)>0` and `det(B)>0`. Therefore

```text
2 - a^T B^{-1} b > 0,
```

hence

```text
a^T B^{-1} b < 2.
```

This conclusion is independent of rank `n`, so the Schur side does not degrade as `n -> infinity` across the classical families.

## A_n inverse formula sanity check

For the type `A_n` Cartan matrix,

```text
(A_n^{-1})_{ij} = min(i,j) * (n + 1 - max(i,j)) / (n + 1),   1 <= i,j <= n.
```

The highest-root marks are all `1`. Therefore the Green ratio condition reduces to proving that the maximum in row `e` occurs at the diagonal entry. The displayed formula makes this immediate:

- for `j <= e`, the row entries increase up to `j=e`;
- for `j >= e`, the row entries decrease after `j=e`.

Thus

```text
max_j (A_n^{-1})_{ej} = (A_n^{-1})_{ee}.
```

This is the concrete rank-uniform version of the Green Ratio Maximum Lemma in type `A`.

## Why the paper still remains classification-free

The manuscript does not need these family formulas. They are included to reassure readers who expect the infinite classical families to be explicitly sanity-checked. The proof itself remains type-free: it uses the structural Cartan/M-matrix/Schur facts, not an induction over `A_n`, `B_n`, `C_n`, or `D_n`.
