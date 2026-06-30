# Geometric Dictionary for the Green-Schur Proof

Truth status: explanatory bridge between matrix notation and convex geometry.

The manuscript proves a containment statement about projected root polytopes. The matrix proof is a coordinate engine for the same geometric statement.

## Dictionary

| Matrix/algebra object | Convex-geometric meaning |
|---|---|
| `P_Phi = ConvHull(Phi)` | The original root polytope. |
| `P_U = ConvHull(Phi cap U)` | The target root polytope inside the projected subspace. |
| `pi_U(P_Phi)` | Shadow of the full root polytope on `U`. |
| `kappa(Phi,U)` | Smallest dilation needed so the shadow fits inside `P_U`. |
| `||pi_U(alpha)||_{P_U}` | Gauge distance of a projected root inside the target polytope. |
| `r_alpha` | Local codimension-one bound controlling the worst projected root. |
| `c_epsilon` | Component height coefficient for a neighboring branch after deleting `alpha`. |
| `G = B^{-1}` | Green kernel measuring how local component weight propagates through the Cartan block. |
| `c_epsilon <= G_epsilon,epsilon` | Geometric height is bounded by the diagonal response of the component. |
| `a^T B^{-1} b < 2` | Total local branch interaction is strictly below the critical dilation threshold. |

## Example: A2 projection to a simple-root line

Let `Phi=A2` with simple roots

```text
alpha_1 = (1,0),
alpha_2 = (-1/2, sqrt(3)/2).
```

The six roots are

```text
±alpha_1, ±alpha_2, ±(alpha_1+alpha_2).
```

Project to `U = span(alpha_1)`. The projected coordinates on the `alpha_1` line are

```text
-1, -1/2, -1/2, 1/2, 1/2, 1.
```

The target polytope is

```text
P_U = [-1,1].
```

Every projected root already lies in `P_U`, so

```text
kappa(A2,U) = 1 < 2.
```

This toy example shows what the theorem controls in general: the shadow of the full root polytope fits inside a strict dilation of the root polytope already present in the subspace.

## Geometric role of the Green-Schur bridge

The hard case is when a projected root lands near a boundary direction of `P_U`. Cellini-Marietti reduce this to local constants `r_alpha`. The Green-Schur argument proves these local constants never reach `2` by bounding component heights through inverse-Cartan Green ratios and then using the Schur complement.

Thus the algebraic chain

```text
c_epsilon <= G_epsilon,epsilon
r_alpha <= a^T B^{-1} b < 2
```

is the coordinate version of the convex statement

```text
pi_U(P_Phi) is contained in kappa P_U for some kappa < 2.
```
