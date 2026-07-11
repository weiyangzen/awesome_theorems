# THM-M-1216 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Kenig-Ponce-Vega theorem entry. The
catalogue phrase "low regularity for dispersive equations" is not precise enough to be a unique
theorem. For a concrete starting scope, this intake selects the real-line KdV local
well-posedness result associated with Kenig, Ponce, and Vega's 1996 bilinear-estimate paper. That
selection remains provisional until the statement phase verifies the primary paper's exact
theorem, hypotheses, endpoint convention, and conclusion.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Equation | real-line KdV, conventionally `u_t + u_xxx + u * u_x = 0` | Coefficients and solution notion require primary-source verification |
| Initial data | inhomogeneous Sobolev data on `R`, with candidate range `s > -3/4` | Endpoint and exact topology are not yet accepted |
| Conclusion | local existence, uniqueness, persistence, and continuous dependence | Lifespan dependence and uniqueness class remain open |
| Proof route | Airy evolution, Bourgain restriction spaces, bilinear derivative estimate, contraction | Architecture only; no leaf receives proof credit |
| Lean surface | legacy discovery module `AwesomeTheorems.Stage1.S1_M_154` | Its abstract wrapper is not the exact PDE statement and is unaccepted |
| Foundations | Lean 4 kernel plus pinned mathlib | Exact toolchain, imports, axioms, and dependency closure remain open |

The initial proof-package scope is: statement and notation freeze; concrete `H^s(R)` and
`X^{s,b}` object model; Airy linear estimates; the threshold bilinear estimate; contraction and
trace/persistence bridges; and the final well-posedness wrapper. No branch is excluded at intake.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. `H1` records only a named
primary-source candidate, not an accepted source audit. `M4` records that the catalogue claim is
ambiguous and the existing abstract Lean shape is not an exact formal target. The first failed
gate is the exact statement gate. This intake does not claim a Lean proof or theorem completion.

The exact validation commands and results are recorded in `validation.md`.
