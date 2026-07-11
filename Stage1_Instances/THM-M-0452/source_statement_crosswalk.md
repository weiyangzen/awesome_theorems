# Source-statement crosswalk

| Claim component | Human source anchor | Lean target needed | Intake assessment |
|---|---|---|---|
| Polarization and self-pairing | J. H. Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed., Springer GTM 106 (2009), Chapter VIII, section 9, discussion following Theorem 9.3 | Canonical height and a real-valued polarization definition | Primary theorem family located; exact page/theorem numbering and normalization await fixed-copy review |
| Symmetry and bilinearity | Same source family, Neron-Tate pairing corollaries following the canonical-height theorem | Point-group addition, negation, and integer scalar laws | Must be derived from checked quadratic/parallelogram laws, not postulated |
| Diagonal positivity and torsion kernel | Same section's canonical-height positivity and zero-kernel results | Ordered-real inequality and formal torsion predicate | Number-field premise is essential |
| Positive definite quotient | Standard passage from the semidefinite pairing on `E(K)` to `E(K)/E(K)_tors` | A quotient group and well-defined descended pairing | Quotient formulation is part of the intended root, but encoding is open |

Discovery link, not an immutable evidence receipt: <https://doi.org/10.1007/978-0-387-09494-6>

The repository source phrase is too short to distinguish this pairing from local Neron pairings,
the torsion-valued Weil/Tate pairings, or general abelian-variety height pairings. This intake makes
that distinction explicit. The statement phase must check the source numbering and convention,
freeze whether bilinearity is expressed on points or the torsion quotient, and mutation-test the
number-field premise, factor `1/2`, torsion kernel, negative scalars, and diagonal identity.

Repo-local interfaces in `S1_M_044.lean` and the canonical-height boundary in `S1_M_093.lean` are
discovery hints only: they do not construct the canonical height or close this target. No H0 or
machine-closure credit is assigned.
