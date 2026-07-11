# THM-M-1517 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for "Lagrangian mechanics". The source label is a
theory-sized topic rather than a uniquely quantified theorem, so the intake does not pretend that
an exact root has already been recovered.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human claim | For a smooth finite-dimensional Lagrangian, stationary admissible trajectories satisfy the Euler-Lagrange equations | This is the narrow mathematical reading to audit, not yet an accepted replacement for the underspecified source wording |
| Objects | configuration space, time interval, Lagrangian, twice differentiable path, endpoint-fixed variation, action functional | Exact scalar field, regularity, coordinates/manifold model, and endpoint conventions remain open |
| Forward direction | stationarity of the action implies Euler-Lagrange equations | Candidate canonical direction; no converse is included without additional hypotheses |
| Converse | Euler-Lagrange equations imply vanishing first variation for admissible variations | A related candidate branch, not silently included in the root |
| Mechanics interpretation | generalized coordinates, forces, momenta, energy, constraints | Out of the canonical root unless a source audit makes a particular consequence explicit |
| Degenerate cases | empty/degenerate intervals, nonsmooth paths, free endpoints, constrained or singular Lagrangians | Excluded from proof credit; each needs an explicit later decision |
| Formal system | Lean 4 plus pinned mathlib | No Lean declaration, imports, or environment fingerprint is credited at intake |

## Open task DAG

`STATEMENT` must resolve the source ambiguity and elaborate one exact target. `ANCHOR_AUDIT` then
searches mathlib and immutable external Lean sources. `OBLIGATION_TREE` freezes the typed proof and
provenance graphs; only afterward may `PROOF`, `VALIDATION`, and `RELEASE` proceed. These are the
dependent nodes listed in the authoritative rev-5.6 execution DAG; none is accepted here.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first failed theorem gate is
exact source-statement identity: the repository provides only "the classical-mechanics Lagrangian
formulation" and no mathematical formula, hypotheses, edition, or pinpoint. Consequently the
candidate Euler-Lagrange implication is not yet the canonical theorem and theorem completion is
false.

The structured intake is in `intake.json`; source genealogy and the non-equivalence boundaries are
recorded in `source_statement_crosswalk.md`. Validation in `validation.md` establishes only target
membership and dossier integrity.
