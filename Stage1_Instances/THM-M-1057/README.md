# THM-M-1057 rev-5.6 intake

This is the `planned` dossier for the ergodic real-valued form of Kingman's
subadditive ergodic theorem. Historical slot `S1-M-249` is discovery material only.
The statement phase has self-tested the exact target in `Statement.lean`. The
anchor audit now records checked pinned-mathlib support and the bounded external
Lean 4 search; proof and downstream assurance gates remain open.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Space and dynamics | Probability space and ergodic measure-preserving `T` | Sigma-finite and non-ergodic variants excluded |
| Process | Integrable real `X_n`, `X_0 = 0` a.e., subadditive cocycle a.e. | Extended-real and two-parameter encodings excluded |
| Lower control | Finite uniform lower bound for `E[X_n]/n`, `n >= 1` | Exact minimal classical hypothesis awaits source audit |
| Conclusion | A.e. convergence of `X_n/n` to `inf_{n>=1} E[X_n]/n` | `L1` convergence is not claimed |
| Lean target | `Stage1Instances.THM_M_1057.KingmanTarget` | Elaborated statement only; no proof credit |
| Foundations | Lean kernel, pinned mathlib, classical measure theory | Environment and TCB fingerprints remain open |

The future architecture must cover probability/dynamics, measurability and integrability,
expectation subadditivity, maximal/ergodic estimates, a.e. convergence, invariance, and
ergodic constancy. These are scope nodes, not frozen obligations or proof credit.

## Current verdict

Lifecycle remains `planned`; provisional root vector remains `[H1, M3, R3]`.
The exact statement has been elaborated with a direct expansion, structural mutations,
and positive/zero-index boundary checks. The anchor audit found deterministic Fekete,
iterate-preservation, and ergodic-constancy support, but no terminal pinned-mathlib or
inspectable external Lean 4 Kingman theorem. Both phases await master acceptance. The
first open dependent gate is the obligation tree. The theorem is not complete.

## Validation

The intake checks remain in `validation.md`; exact Lean statement evidence is recorded
in `statement-validation.md` and `statement.json`. Anchor evidence is in
`anchor-audit.md`, `anchor-audit.json`, and `AnchorAudit.lean`.
