# THM-M-1006 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Burkholder-Davis-Gundy
inequalities. It records scope only and inherits no proof credit from the source label
`已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Two-sided comparison, for every `0 < p`, between the `p`-moment of a finite-time martingale maximum and the `p/2`-moment of its discrete quadratic variation | Frozen as `Stage1Instances.THM_M_1006.StatementShape` |
| Objects | Real-valued, zero-initial, `Nat`-indexed martingales on a probability space and filtration | `MeasureTheory.Martingale`, a finite supremum, and a finite sum of squared increments |
| Constants | Positive finite constants depending only on `p`, uniformly in the martingale and horizon | Optimal constants are excluded |
| Variants | Finite discrete-time, stopped/localized, continuous local-martingale, terminal-time, and stopping-time forms | Variants require checked transports and cannot substitute for the root |
| Boundary cases | `p > 0`; zero martingale and zero quadratic variation must be admitted | `p = 0`, negative `p`, vector-valued and jump-process generalizations are excluded |
| Foundations | Lean 4 kernel, pinned mathlib, classical probability APIs | Exact toolchain, imports, axioms, and TCB closure remain open |

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The dependent statement task must resolve the discrete/continuous-time ambiguity without weakening
the classical two-sided theorem. The anchor audit must then map primary-source hypotheses and locate
any exact Lean declarations before the obligation denominator is frozen.

## Current verdict

Lifecycle remains `planned`. The statement phase selected and locally elaborated the finite
discrete-time form in `Statement.lean`; `statement.json` freezes its ordered scope. Anchor audit and
all later phases remain open, and the theorem is not complete.

## Validation

Intake checks are recorded in `validation.md`; statement checks are recorded in
`statement_validation.md`.
