# THM-M-1201 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label "entropy condition". The
Stage0 record supplies only "condition for uniqueness of weak solutions", the year 1971, and Peter
Lax. Those fields do not determine one theorem: scalar Kruzkov entropy inequalities and Lax shock
admissibility for hyperbolic systems have different domains, hypotheses, and conclusions.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Historical identity | determine which 1971 Lax result the record intends | title, theorem/page, and edition are not supplied |
| PDE model | conservation laws and their weak solutions | scalar/system, dimension, flux regularity, and initial/boundary data are unresolved |
| Entropy data | entropy/entropy-flux pairs, inequality, and admissibility | convexity, distributional formulation, and quantification over entropies are unresolved |
| Claimed result | a precisely sourced uniqueness or contraction theorem | an individual-shock criterion must not be broadened into general uniqueness |
| Lean target | definitions for weak/entropy solutions followed by the exact sourced conclusion | no module, declaration, or expression may be frozen before disambiguation |
| Foundations | Lean 4 kernel plus versioned analysis/PDE dependencies | measure/distribution/Bochner/classical assumptions and TCB remain open |

## Open intake DAG

1. `SRC-ID`: locate the intended primary Lax publication and exact theorem/page.
2. `CLAIM-ID`: transcribe its PDE, ordered binders, hypotheses, solution class, entropy condition, and conclusion.
3. `DISAMBIG`: distinguish it from Kruzkov scalar entropy uniqueness and from the Lax shock inequalities.
4. `LEAN-SURFACE`: inventory repo-local and pinned mathlib definitions only after `CLAIM-ID` closes.
5. `STATEMENT`: elaborate and mutation-test the exact target in the dependent statement phase.

`SRC-ID -> CLAIM-ID -> DISAMBIG -> LEAN-SURFACE -> STATEMENT`. This is a workflow DAG, not a
proof tree and provides no proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first failed gate is source
identity/exact claim: selecting a familiar entropy theorem would broaden or substitute the target.
The dossier and crosswalk are complete for intake, while all theorem-completion claims remain false.

## Validation

The exact commands and results in `validation.md` establish manifest membership, repository-standard
consistency, JSON syntax, dossier references, and clean text formatting only.
