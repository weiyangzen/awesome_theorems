# THM-M-0452 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Neron-Tate pairing. The source inventory
only says "height pairing of elliptic curves"; this intake resolves that ambiguity to the standard
polarization of the canonical height on rational points of an elliptic curve over a number field.
Exact source verification and Lean elaboration remain later phases.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Arithmetic object | An elliptic curve `E` over a number field `K`, with point group `E(K)` | The exact mathlib curve and rational-point encodings remain open |
| Input height | The Neron-Tate canonical height `hat_h : E(K) -> Real` with its standard normalization | Existence and properties may not be assumed unless supplied by a checked dependency |
| Pairing | `<P,Q> = (hat_h(P+Q) - hat_h(P) - hat_h(Q)) / 2` | An alternate polarization convention requires a checked transport |
| Algebraic laws | Symmetry and additivity in each argument, hence integer bilinearity | Rational extension is not part of the root |
| Diagonal | `<P,P> = hat_h(P)` | This fixes the factor and sign convention |
| Kernel | `<P,P> >= 0`, with equality exactly when `P` is torsion | Positive definiteness is properly on `E(K) / E(K)_tors` |
| Foundations | Lean 4 kernel, pinned mathlib, and an explicitly audited classical policy | Imports, versions, and environment fingerprint remain open |

The root excludes local Neron symbols, height pairings on general abelian varieties, the Weil or
Tate pairings on torsion, and Gross-Zagier. Those are not substitutes for this theorem.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The exact-statement gate is the
first failed theorem gate: no canonical Lean target or environment fingerprint is frozen. This
dossier claims intake scope only, not source acceptance, kernel closure, or theorem completion.

