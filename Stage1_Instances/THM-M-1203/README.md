# THM-M-1203 rev-5.6 intake

This is the `planned` instance for the metadata label "Oleinik entropy condition". The seed says
only "the entropy condition for scalar conservation laws". That label can denote a shock
secant-slope condition, a one-sided estimate for convex flux, or a condition embedded in a larger
existence/uniqueness result. Intake therefore records the ambiguity rather than selecting a
broadened theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Equation | One-dimensional scalar law `u_t + f(u)_x = 0` | No system, source term, or multidimensional extension |
| Discontinuity | Left/right traces and Rankine-Hugoniot speed | Trace orientation is not yet frozen |
| Oleinik condition | Intermediate-state secant-slope/one-sided admissibility | Exact inequality, strictness, and flux assumptions await primary transcription |
| Solution theory | Weak-solution context only as needed to type the condition | No existence, uniqueness, regularity, or convergence theorem is claimed |
| Related notions | One-sided spatial estimate and convex-entropy formulation are crosswalk candidates | No equivalence is credited |
| Formal surface | Lean 4 with pinned mathlib | No module, expression, imports, or environment fingerprint yet |

## Open task DAG

After `S56-M-1203-INTAKE`, the blueprint orders `STATEMENT`, `ANCHOR_AUDIT`,
`OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE`. The statement phase must first obtain a
pinpoint primary statement and freeze conventions before elaborating Lean.

## Verdict

Lifecycle remains `planned`, with provisional vector `[H3, M4, R3]`. The first failed theorem gate
is exact source-statement identity. The validation receipt checks only this intake's structure and
prohibited-token boundary; it is not kernel evidence and the theorem is not complete.
