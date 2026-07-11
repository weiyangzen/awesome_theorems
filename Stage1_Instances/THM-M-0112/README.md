# THM-M-0112 rev-5.6 intake

This is a new rev-5.6 `planned` instance for the Lefschetz hyperplane theorem. Historical
`S1_M_035.lean` material is discovery input only and supplies no accepted proof or statement credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Selected root | weak topological Lefschetz for a smooth complex projective variety and a smooth hyperplane section | Exact Lean object model and dimension convention remain for the statement phase |
| Geometric input | connected smooth complex projective `X`, complex dimension `n`, smooth hyperplane section `Y`, inclusion `i : Y -> X` | Projectivity, smoothness, connectedness, and transversality may not be dropped |
| Conclusion | `i_* : pi_k(Y) -> pi_k(X)` is an isomorphism for `k < n - 1` and surjective for `k = n - 1` | Basepoints and the low-dimensional range must be made explicit in Lean |
| Equivalent classical form | relative homotopy groups `pi_k(X,Y)` vanish for `k < n` | Candidate equivalence only; no checked transport is credited |
| Consequences | connectedness and fundamental-group comparison in the applicable dimensions | Consequences are not substitutes for the root |
| Excluded siblings | hard Lefschetz, cohomological weak Lefschetz, affine/generalized variants | Separate theorems; none broadens or replaces this target |
| Foundations | Lean 4 kernel, pinned mathlib, classical topology and algebraic-geometry dependencies | Exact toolchain, imports, axioms, TCB, and computation profile remain open |

The root selection resolves the source metadata's ambiguous phrase "topological properties of a
hyperplane section" conservatively and agrees with the legacy dossier's explicit selection. It
does not claim that this choice has passed independent source review.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact-statement gate: no elaborated Lean expression, environment fingerprint, checked relative-
homotopy transport, or mutation suite exists. This intake is self-tested as an intake artifact only;
the theorem is not complete and all dependent phases remain open.

Exact validation commands and results are recorded in `validation.md`.
