# THM-M-1007 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Kolmogorov's three-series theorem. The
manifest's historical `已验证` label is discovery metadata and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Almost-sure convergence of a series of independent real random variables, characterized by the three truncated-series conditions | Elaborated as `Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget` |
| Probability model | A probability space `(Omega, F, P)` and an independent sequence `X n : Omega -> Real` | Frozen using `Measurable`, `IsProbabilityMeasure`, and `iIndepFun` |
| Truncation | A fixed threshold `c > 0`; `Y n = X n * 1_{|X n| <= c}` (equivalently, zero outside the threshold) | Inclusive cutoff and strict large-jump event frozen; boundary probes elaborate |
| Three conditions | Summability of `P(|X n| > c)`, convergence of `sum E[Y n]`, and summability of `Var(Y n)` | No condition is credited as machine checked |
| Conclusion | Almost-sure convergence of the partial sums of `X` in `Real` | Pointwise-series and partial-sum formulations require an equivalence check |
| Degenerate cases | Positive finite thresholds only; null-set changes and equality at the cutoff must be accounted for | Boundary mutations are deferred to statement work |
| Foundations | Lean 4 kernel, pinned mathlib, and an explicit classical/choice/measure-theory policy | Statement elaborated with Lean 4.29.0 and pinned mathlib; full TCB closure remains later validation work |

The root must remain the biconditional theorem. One direction or any finite/discrete special case is
only a subordinate obligation, never a substituted completion. The structured claim is frozen in
`intake.json`; source wording and normalization risks are recorded in
`source_statement_crosswalk.md`.

## Statement verdict

Lifecycle remains `planned`. The exact statement is self-tested pending master acceptance, with an
elaborated expression hash, environment fingerprint, alias transport, four distinguished structural
mutations, and cutoff boundary probes in `statement.json`. Source audit, obligation construction,
proof, release validation, and theorem completion remain open.

## Validation

Intake-only checks remain in `validation.md`; the pinned Lean statement checks are recorded in
`statement_validation.md`. Neither record claims a proof of the three-series theorem.
