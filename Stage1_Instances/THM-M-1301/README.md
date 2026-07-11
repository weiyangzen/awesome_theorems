# THM-M-1301 rev-5.6 intake

This directory is the `planned` intake for the target labelled "Bony paraproduct decomposition".
The repository's source wording, "paradifferential methods for nonlinear PDE", names a theory rather
than one proposition. Intake therefore freezes the ambiguity instead of inventing an exact theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root selection | choose a precise decomposition theorem from Bony's 1981 calculus | source pinpoint and exact statement remain open |
| Dyadic resolution | low/high frequency cutoffs and admissible partition | normalization and ambient distribution space remain open |
| Paraproducts | the two low-high interactions | no operator has yet been defined in Lean |
| Resonant term | the comparable-frequency interaction | convergence/topology hypotheses remain open |
| Identity | product equals the two paraproducts plus resonant term | only a candidate architecture, not a frozen claim |
| Foundations | distributions, Fourier localization, infinite sums, topology | foundation, TCB, and computation profiles require audit |

The candidate nodes are structured in `intake.json`. `source_statement_crosswalk.md` records why the
catalogue wording cannot yet be treated as an exact source statement.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
statement identification: the manifest supplies no domains, hypotheses, or conclusion, and no Lean
declaration has been selected. No historical "verified" label or nearby object model receives proof
credit. The theorem is not complete.

## Validation

The commands and exact results in `validation.md` establish manifest membership, repository-standard
consistency, JSON syntax, and dossier hygiene only. No Lean theorem is introduced in this phase.
