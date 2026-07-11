# THM-M-1057 rev-5.6 intake

This is the `planned` intake dossier for the ergodic real-valued form of Kingman's
subadditive ergodic theorem. Historical slot `S1-M-249` is discovery material only.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Space and dynamics | Probability space and ergodic measure-preserving `T` | Sigma-finite and non-ergodic variants excluded |
| Process | Integrable real `X_n`, `X_0 = 0` a.e., subadditive cocycle a.e. | Extended-real and two-parameter encodings excluded |
| Lower control | Finite uniform lower bound for `E[X_n]/n`, `n >= 1` | Exact minimal classical hypothesis awaits source audit |
| Conclusion | A.e. convergence of `X_n/n` to `inf_{n>=1} E[X_n]/n` | `L1` convergence is not claimed |
| Lean candidate | legacy `StatementShape` and `KingmanConclusion` | No expression hash, transport, or mutation result yet |
| Foundations | Lean kernel, pinned mathlib, classical measure theory | Environment and TCB fingerprints remain open |

The future architecture must cover probability/dynamics, measurability and integrability,
expectation subadditivity, maximal/ergodic estimates, a.e. convergence, invariance, and
ergodic constancy. These are scope nodes, not frozen obligations or proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed
theorem gate is the exact statement gate. In particular, the legacy package selects a
`limit` as input, its positive-index normalization needs checking, and its disjunctive
cocycle field must be compared with the source inequality. The theorem is not complete.

## Validation

The commands and results in `validation.md` establish target membership, repository
standard consistency, JSON syntax, and dossier-local integrity only.
