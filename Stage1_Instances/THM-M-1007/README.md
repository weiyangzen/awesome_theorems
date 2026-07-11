# THM-M-1007 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Kolmogorov's three-series theorem. The
manifest's historical `已验证` label is discovery metadata and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Almost-sure convergence of a series of independent real random variables, characterized by the three truncated-series conditions | Exact Lean binders and elaboration belong to the dependent statement phase |
| Probability model | A probability space `(Omega, F, P)` and an independent sequence `X n : Omega -> Real` | The precise mathlib measurability and independence interfaces remain to be selected |
| Truncation | A fixed threshold `c > 0`; `Y n = X n * 1_{|X n| <= c}` (equivalently, zero outside the threshold) | Alternate `<`/`<=` and truncation encodings require checked transports |
| Three conditions | Summability of `P(|X n| > c)`, convergence of `sum E[Y n]`, and summability of `Var(Y n)` | No condition is credited as machine checked |
| Conclusion | Almost-sure convergence of the partial sums of `X` in `Real` | Pointwise-series and partial-sum formulations require an equivalence check |
| Degenerate cases | Positive finite thresholds only; null-set changes and equality at the cutoff must be accounted for | Boundary mutations are deferred to statement work |
| Foundations | Lean 4 kernel, pinned mathlib, and an explicit classical/choice/measure-theory policy | Exact toolchain, imports, dependency closure, and TCB remain open |

The root must remain the biconditional theorem. One direction or any finite/discrete special case is
only a subordinate obligation, never a substituted completion. The structured claim is frozen in
`intake.json`; source wording and normalization risks are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the statement gate: there is no elaborated expression hash, environment fingerprint, checked
transport, or mutation record. No theorem completion is claimed.

## Validation

The exact intake-only checks and their results are recorded in `validation.md`. They validate
membership, repository consistency, JSON syntax, and dossier hygiene, not a Lean proof.
