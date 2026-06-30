# Counterexample Stress-Test Protocol

Truth status: scope testing. These tests intentionally leave the theorem's hypotheses.

Professional reviewers often ask where a proof fails if its hypotheses are weakened. The script

```text
counterexample_stress_test.py
```

runs matrices that are valid, transposed, singular, indefinite, or non-Cartan-like.

## What is tested

1. Valid `B3` proof orientation.
2. Wrong `B3` orientation to show why the row convention matters.
3. Indefinite two-node matrix with negative determinant.
4. Singular affine-like two-node matrix.
5. A matrix with a positive off-diagonal entry, violating the Cartan Z-matrix condition.

The script also records why non-crystallographic systems such as `H3` and `H4` are not OPAC-018 crystallographic Cartan tests: they involve non-crystallographic Coxeter data and do not supply the integer crystallographic Cartan matrices used in the theorem.

## Expected conclusion

The valid test passes. Out-of-scope tests either fail the Green ratio check or are diagnosed as violating one of the structural hypotheses:

```text
finite type
crystallographic Cartan integrality
Z-matrix sign condition
nonsingular M-matrix inverse positivity
proof orientation B_ij=(beta_i,beta_j^vee)
```

This protects the manuscript against accidental overgeneralization.
