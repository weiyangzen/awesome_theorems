# THM-M-0413 rev-5.6 intake

This directory is the `planned` rev-5.6 dossier for the theorem that the ring of integers of a
number field is a Dedekind domain. The generated source label `已验证` is discovery metadata only.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every finite extension `K/Q`; its elements integral over `Z` form a Dedekind domain | Exact Lean binders, imports, and normalized expression belong to the statement phase |
| Domain | Number fields, including the degree-one case `K = Q` | Arbitrary fields and infinite algebraic extensions are excluded |
| Object | The integral closure of `Z` in `K`, with its induced ring structure | A chosen order smaller than the full ring of integers is excluded |
| Conclusion | The complete mathlib Dedekind-domain predicate | Ideal factorization alone is a consequence/alternate characterization, not a substitute root |
| Source | Classical algebraic-number-theory theorem and its proof premises | Edition/page, errata, and premise-to-node review remain open |
| Machine | Lean 4 plus a pinned mathlib environment | No Lean checkout, declaration lookup, elaboration, or proof credit exists in this intake |
| Foundations | Kernel, typeclass, classical-choice, quotient, and dependency closure | Exact foundation and TCB profiles remain open |

The intended later architecture must expose the integral-closure definition, noetherianity,
integral closedness, and the nonzero-prime/maximal or dimension-one condition without treating this
outline as a frozen obligation registry. The registry is deliberately deferred until after exact
statement and anchor audit phases.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: the target has no elaborated expression hash, environment
fingerprint, checked transport, or mutation result. The theorem is not complete.

## Validation

The exact structural commands and results for this dossier are recorded in `validation.md`. These
checks establish target membership, standard consistency, JSON syntax, and local reference hygiene
only; they are not kernel evidence.
