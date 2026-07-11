# THM-M-0451 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Neron-Tate canonical-height theorem. The
Stage0 phrase "height of points on elliptic curves" is not precise enough to select a single formal
theorem, so this intake freezes the standard existence-and-properties package described in
`intake.json`. Exact source pinning and Lean elaboration remain dependent phases.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Arithmetic object | An elliptic curve `E` over a number field `K` and its group `E(K)` | The exact mathlib object model and required smoothness data remain to be selected |
| Naive height | Absolute logarithmic Weil height of the projective `x`-coordinate, with the identity handled by the selected convention | Height normalization must be pinned before elaboration |
| Canonical height | `hat_h(P) = (1/2) lim_{n -> infinity} 4^{-n} h_x([2^n]P)` under the stated normalization | Existence of the limit is part of the root, not an assumed definition |
| Comparison | `hat_h(P) - (1/2) h_x(P)` is bounded independently of `P` | The bound may depend on `E`, `K`, and the chosen height normalization |
| Quadratic law | `hat_h([m]P) = m^2 hat_h(P)` and the parallelogram identity | All integers `m`; no special-rank restriction |
| Positivity kernel | `hat_h(P) >= 0`, and `hat_h(P) = 0` exactly for torsion points | This equivalence uses the number-field hypothesis |
| Derived pairing | Polarization of `hat_h` to the Neron-Tate pairing | Candidate corollary; it receives no intake proof credit |
| Foundations | Lean 4 kernel plus pinned mathlib and an accepted classical/choice policy | Toolchain, imports, dependency closure, and TCB fingerprint are open |

The scope excludes local Neron functions, general abelian varieties, function fields, and
Gross-Zagier formulas. Those are related theories, not substitutes for this elliptic-curve
number-field root.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact-statement gate: the repository currently supplies neither a canonical Lean expression nor
an environment fingerprint, and the local mathlib search found no canonical-height declaration.
This dossier claims scope intake only, not source acceptance, kernel closure, or theorem completion.

The open phase graph is in `task-dag.json`; source genealogy and statement risks are in
`source_statement_crosswalk.md`. Validation commands and their exact outcomes are recorded in
`validation.md`.
