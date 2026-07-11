# THM-M-0999 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the logarithmic Sobolev inequality. The
metadata phrase "an upper bound for entropy" does not uniquely determine a theorem: logarithmic
Sobolev inequalities depend on a measure, function class, energy form, and normalization.
Accordingly, intake preserves the historically indicated Gross/Gaussian formulation as a
provisional exact-scope candidate rather than silently treating the generic title as a theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Historical root | Gross's logarithmic Sobolev inequality for Gaussian measure | Primary-source theorem/page transcription and normalization audit remain open |
| Entropy | `Ent_gamma(f^2) = integral f^2 log(f^2) d gamma - (integral f^2 d gamma) log(integral f^2 d gamma)` | Conventions at zero and integrability conditions must be frozen in the statement phase |
| Energy | Gaussian Dirichlet energy `integral norm(grad f)^2 d gamma` | Dimension, scalar field, derivative API, and admissible function class remain open |
| Constant | Candidate sharp Gaussian normalization `Ent_gamma(f^2) <= 2 * energy(f)` | The factor changes with the Gaussian and energy normalization; no constant is credited yet |
| Generalizations | abstract Wiener spaces, semigroups, other measures, discrete variants | Excluded from the root unless a checked transport is later registered |
| Formal system | Lean 4 plus pinned mathlib | No Lean declaration, imports, expression hash, or environment fingerprint is claimed at intake |

The canonical human claim and unresolved binders are structured in `intake.json`. The relationship
between repository metadata, the primary mathematical source, and a future Lean target is recorded
in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source identification: the repository metadata is underspecified and the primary source has not yet
been pinned and transcribed at theorem/page granularity. Consequently the statement phase must not
elaborate an invented strengthening or special case. The theorem is not complete.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Every successor remains open and requires its own node-specific receipt and master acceptance.

## Validation

The commands and exact intake-only results are recorded in `validation.md`. They establish target
membership, standard consistency, JSON syntax, and dossier hygiene only; they provide no kernel
proof credit.
