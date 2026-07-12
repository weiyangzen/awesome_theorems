# THM-M-0981 rev-5.6 intake

This is the `planned` rev-5.6 dossier for the Kolmogorov probability axioms. It does not inherit
proof credit from the legacy `S1_M_261.lean` wrapper or from the untrusted source-status label.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every normalized mathlib probability measure satisfies the empty-set, unit-mass, and countable-disjoint-additivity clauses | Exact elaboration and fingerprint belong to the statement phase |
| Objects | Arbitrary universe, measurable sample type, `Measure`, measurable event sequences, `ENNReal` values | No topology, random variables, filtrations, or stochastic processes are part of this root |
| Positivity | Probability values are nonnegative by the `ENNReal` codomain | A separate real-valued positivity conjunct would require a checked transport |
| Normalization | `P univ = 1`, with `P empty = 0` retained explicitly in the crosswalk | Whether the empty-set clause is definitionally/redundantly supplied is not proof credit here |
| Additivity | Countable additivity for pairwise disjoint measurable sequences | Finite additivity and continuity are consequences, not root clauses |
| Foundations | Lean 4 kernel and pinned mathlib | Exact toolchain, imports, axioms, TCB, and dependency fingerprint remain open |

The structured binder order, hypotheses, conclusion, alternate packaging candidates, and boundary
cases are frozen in `intake.json`. The statement phase is now self-tested in `Statement.lean`,
`statement.json`, and `statement-validation.md`: the exact target elaborates with one direct import,
and checked iff theorems connect both the historical expanded shape and `ProbabilityMeasure`
subtype packaging. `source_statement_crosswalk.md` records the primary-source location and the work
still required for H0.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Intake and statement are worker-self-tested pending master acceptance. No later phase or
theorem-completion gate is claimed.

## Intake verdict

Lifecycle is `planned`; provisional root vector remains `[H1, M3, R3]`. The statement node now has
a normalized expression hash, environment fingerprint, checked transports, and mutation results,
but master acceptance is pending. The next dependent gate is anchor audit. The theorem is not
complete.
