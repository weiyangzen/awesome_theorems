# THM-M-0150 rev-5.6 intake

This directory is the `planned` intake for the repository label "Hacon-McKernan theorem". The
repository gloss, "finite generation for varieties of general type", is treated as the canonical
ring finite-generation theorem, not as proof that the source label or its reported 2006 date is
precise. The standard primary source is the joint BCHM paper and the exact attribution remains an
explicit source-audit item.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Geometric object | A smooth projective variety `X` of general type over `C` | Scheme/variety encoding and universe parameters remain for the statement phase |
| Root conclusion | Finite generation of `R(X,K_X) = direct_sum_{m >= 0} H^0(X, O_X(mK_X))` as a graded `C`-algebra | No Lean declaration or elaboration is credited at intake |
| Source bridge | BCHM finite generation of the log canonical ring, specialized to `Delta = 0` | Hypothesis-by-hypothesis specialization must be audited |
| Equivalent geometry | Existence of the canonical model and related minimal-model consequences | Not part of the root unless checked transports are later supplied |
| Degenerate/boundary cases | Dimension zero, non-general-type varieties, singular/log pairs, nonclosed or positive-characteristic bases | Excluded from the root; possible generalizations must not silently replace it |
| Formal foundation | Lean 4 with pinned mathlib | Algebraic varieties, canonical divisors, section rings, and finite generation APIs are not yet located |

The canonical human claim and its ordered assumptions are structured in `intake.json`. Primary
source terminology and the repository wording are aligned in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: no canonical Lean expression, minimal imports, elaboration hash,
environment fingerprint, or checked encoding transports exist. This intake makes no machine-proof
or theorem-completion claim.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The immediate task is to encode the exact root without broadening it to arbitrary log pairs or
weakening finite generation to a finite-dimensional graded piece.

## Validation

The exact local commands and results are recorded in `validation.md`. They validate manifest
membership, repository structure, JSON syntax, and dossier-local references only.
