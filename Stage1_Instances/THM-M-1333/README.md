# THM-M-1333 rev-5.6 dossier

This directory is the `planned` intake for the Peano existence theorem for ordinary differential
equations. The repository catalogue supplies only "existence of solutions under a continuity
condition." That wording does not determine the state space, neighborhood, interval, derivative
convention, or whether the intended result is scalar, vector-valued, qualitative, or quantitative.
The intake preserved those choices rather than silently selecting a stronger or narrower theorem.
The statement phase now freezes the conventional finite-dimensional local formulation in
`Statement.lean`; `statement.json` records its normalized expression and environment fingerprint.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root claim | local existence through prescribed initial data | no uniqueness or global continuation |
| Domain | real time and a finite-dimensional real state space | exact dimension and neighborhood encoding remain open |
| Assumption | continuity of the vector field near the initial point | exact set and endpoint hypotheses require a source pin |
| Interval | a genuinely nontrivial local interval | one-sided/two-sided and quantitative radius remain open |
| Solution | initial value plus ODE on the selected interval | derivative-within and integral-equation packaging remain open |
| Architecture | bound, approximants, compactness, limit, differentiation | candidate map only; no obligation is frozen or closed |
| Foundations | finite-dimensional compactness, integration, classical subsequence extraction | logic, imports, TCB, and computation profiles require audit |

The candidate scope nodes from intake have now been replaced by the versioned registry in
`obligation-registry.json`. `typed-graphs.json` separately records proof, refinement, provenance,
evidence, trust, documentation, and workflow edges. The selected proof route uses delayed Euler
approximants, finite-dimensional Arzela-Ascoli, passage to the integral equation, and recovery of
the derivative. These are frozen open obligations, not proof-coverage claims.

## Current verdict

Lifecycle remains `planned`; provisional root vector remains `[H2, M4, R3]`. The exact selected Lean
expression now elaborates with one minimal import, but an independently inspected primary-source
formulation has not yet been accepted. The mathlib Picard-Lindelof module is a nearby theorem under
stronger Lipschitz hypotheses and cannot substitute for Peano existence.

The theorem is not complete. The obligation receipt closes no mathematical obligation and records
the first open cut as construction of Euler approximants, compactness, limit passage, and
differentiation. The catalogue's untrusted "verified" status receives no assurance credit.

## Validation

`validation.md` records the intake checks; `statement-validation.md` records the exact Lean
elaboration and statement mutation checks. No kernel-proof claim is made.
