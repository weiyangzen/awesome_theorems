# THM-M-0413 rev-5.6 dossier

This directory is the `planned` rev-5.6 dossier for the theorem that the ring of integers of a
number field is a Dedekind domain. The generated source label `已验证` is discovery metadata only.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every finite extension `K/Q`; its elements integral over `Z` form a Dedekind domain | Elaborated as `Stage1.THMM0413.Statement` in `Statement.lean` |
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

## Historical intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: the target has no elaborated expression hash, environment
fingerprint, checked transport, or mutation result. The theorem is not complete.

## Statement phase

`statement.json` is the phase-specific authority. The exact target uses the ordered context
`(K : Type u) [Field K] [NumberField K]` and concludes
`IsDedekindDomain (NumberField.RingOfIntegers K)`. It elaborates with the sole declared import
`Mathlib.NumberTheory.NumberField.Basic`; its transport to `integralClosure Z K`, degree-one
boundary probe, and three required negative mutations were checked with pinned Lean 4.29.0 and
mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

This statement result is provisional pending master acceptance. It does not update the historical
intake receipt, establish proof closure, or make the theorem complete.

## Anchor-audit phase

`anchor-audit.json` is the phase-specific authority. At pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the exact candidate is
`NumberField.RingOfIntegers.instIsDedekindDomain` from
`Mathlib.NumberTheory.NumberField.Basic`. Its body instantiates the terminal theorem
`IsIntegralClosure.isDedekindDomain` from
`Mathlib.RingTheory.DedekindDomain.IntegralClosure`. `AnchorAudit.lean` names and checks both routes;
Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for each route.

The pinned external `flt-regular` checkout and repository-local legacy sources supplied no
distinct proof candidate: the legacy wrapper resolves to the same mathlib instance. Thus the
machine-debt classification is `local_wrapper_upstream_mathlib`, with no new external dependency
needed. This provisional audit does not freeze or close the transitive obligation graph and does
not establish theorem completion.

## Validation

The exact structural commands and results for this dossier are recorded in `validation.md`. These
checks establish target membership, standard consistency, JSON syntax, and local reference hygiene
only; they are not kernel evidence.
