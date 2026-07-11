# THM-M-1139 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the source record named **Hopf引理** (Hopf
lemma). The available record says only “the sign of the derivative at the boundary.” That wording
does not uniquely determine a theorem, so intake deliberately preserves the ambiguity rather than
inventing a stronger or weaker target.

## Scope map

| Surface | Provisional in-scope interpretation | Intake boundary |
|---|---|---|
| Exact root | Classical Hopf boundary point lemma for a nonconstant harmonic function | Not frozen: the source does not specify binders, regularity, geometry, normal convention, or extremum convention |
| Analytic domain | Finite-dimensional Euclidean domain with a distinguished boundary point | Dimension, openness/connectedness, closure representation, and boundary regularity remain open |
| PDE layer | Laplacian/harmonic special case suggested by the neighboring Laplace and maximum-principle records | A general elliptic operator is a distinct stronger scope and is not silently substituted |
| Geometric layer | Interior tangent-ball (interior sphere) condition at the boundary point | Exact ball witnesses and normal construction remain open |
| Extremum layer | Strict boundary maximum, with minimum form obtained via `-u` | Global/local extremum and strictness hypotheses require a source decision |
| Conclusion | Strict sign of a one-sided inward normal derivative | Outward normal reverses the sign; classical derivative versus liminf quotient remains open |
| Degeneracies | Constants, flat extrema, missing tangent balls, and insufficient differentiability | Must become explicit exclusions or branches, never tacit assumptions |
| Formal layer | Lean 4 plus a future pinned mathlib environment | No declaration, import, expression hash, transport, or proof is credited |

The canonical structured record is `intake.json`. `source_statement_crosswalk.md` maps every phrase
actually present in the repository source and lists the source work required before the dependent
statement phase may freeze Lean binders.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

The next node must first resolve the statement ambiguity from a primary mathematical source or an
accepted scope ruling. It must then elaborate the exact chosen target and mutation-test the normal
orientation, extremum direction, strictness, interior-sphere hypothesis, regularity, and constant
case. Anchor search and proof inspection remain later phases.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R3]`. The first failed theorem gate is
exact source-statement identification. The source metadata's “verified” label is explicitly
untrusted and supplies no human-source or kernel credit. The theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier-local reference integrity only.
