# THM-M-0986 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Khinchin's weak law of large numbers. The
historical `S1_M_266.lean` module is discovery input only and contributes no accepted proof state.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact human root | iid real random variables with a finite first absolute moment; sample means converge in probability to the common expectation | Exact source wording and Lean elaboration remain open |
| Probability model | an explicit probability measure on a measurable sample space | Typeclass, measurability, and integrability context must be fingerprinted later |
| Independence/distribution | pairwise independence and identical distribution relative to the same measure | Equivalence to alternate iid APIs is not credited |
| Conclusion | convergence in probability, represented provisionally by `TendstoInMeasure` | Metric threshold and event-probability formulations need checked transports |
| Boundary behavior | finite prefixes, including the `n = 0` inverse convention, do not affect an `atTop` limit | Mutation tests belong to the statement phase |
| Generalizations | Banach-valued weak and strong laws are useful candidate bridges | They are not substituted for the frozen real-valued root |
| Foundations | Lean 4 kernel and a pinned mathlib closure | Foundation, trust, and computation profiles remain open |

The prospective proof architecture is: probability-space data, measurability and integrability,
iid interface, empirical-average normalization, convergence bridge, and the root conclusion. This
is a scope map, not a frozen obligation registry or proof tree.

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H1, M3, R3]`. The first failed theorem
gate is the exact statement gate: no normalized Lean expression hash, environment fingerprint,
checked transports, or mutation record exists. The theorem is not complete.

## Validation

The commands and exact intake-level results are recorded in `validation.md`. They establish target
membership, repository-standard consistency, JSON syntax, and dossier hygiene only.
