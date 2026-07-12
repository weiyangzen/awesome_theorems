# THM-M-1352 rev-5.6 intake

`THM-M-1352` is the ordinary-differential-equations catalog item `Floquet理论` (Floquet theory).
The repository supplies only the gloss `周期线性系统的理论` (the theory of periodic linear
systems), Gaston Floquet, the year 1883, and an untrusted `verified` label. Those fields identify a
subject family, not a binder-complete proposition.

## Intake result

This dossier creates a fail-closed `planned` instance and preserves that ambiguity. Floquet theory
contains distinct results about time-shifted principal matrix solutions, monodromy, Floquet
decomposition, real versus complex normal forms, characteristic multipliers and exponents,
reduction to constant coefficients, and stability. The catalog does not select one result or a
source-defined conjunction.

The adjacent catalog items are material boundaries: `THM-M-1353` separately names the Floquet
theorem and a fundamental solution matrix, `THM-M-1354` names characteristic exponents, and
`THM-M-1355` names linear-system stability. Importing any of those conclusions into this target
without an authoritative source decision would substitute or broaden the claim.

## Source and formal boundary

Floquet's 1883 paper is a matching historical source-family lead, and Teschl's modern Section 3.6
was inspected to discriminate the family into separate lemmas, theorem, and corollaries. Neither
source is cited or selected by the catalog, and no theorem/page passage has been admitted with a
complete premise, conclusion, proof-boundary, errata, and independent-review crosswalk.

`IntakeProbe.lean` elaborates only adjacent pinned periodic-function, ODE, matrix, determinant, and
matrix-exponential APIs. A bounded exact-topic search found no Floquet declaration in repo-local
Lean or pinned mathlib. This is discovery-only evidence, not an exhaustive anchor audit or proof of
absence from external Lean projects.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: `H5` classifies the supplied theory label as not yet one stable proposition; it
does not say that a correctly stated Floquet theorem is false or open. No exact usable formal
artifact or source-faithful proof reconstruction is identified. All six downstream tasks remain
open. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance
is claimed.
