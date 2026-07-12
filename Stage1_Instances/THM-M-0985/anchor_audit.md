# Anchor audit

The immutable in-environment candidate is
`ProbabilityTheory.strong_law_ae` from `Mathlib.Probability.StrongLaw` at
mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The repository manifest pins
that exact commit and the audit reused its existing checkout without changing
`.lake`.

## Candidate crosswalk

| Frozen target surface | Pinned candidate surface | Audit result |
|---|---|---|
| `X : Nat -> Omega -> Real` | Banach-valued `X`, specialized to `Real` | exact specialization |
| mutual `iIndepFun X mu` | pairwise `IndepFun` on `X` | checked by `pairwise_of_iIndepFun` |
| `IdentDistrib (X n) (X 0) mu mu` | identical binder and measures | direct |
| `Integrable (X 0) mu` | identical premise | direct |
| inverse times sum over `range n` | inverse scalar action on the same sum | `simpa [smul_eq_mul]` |
| almost-everywhere `Tendsto` to integral | identical conclusion | direct |

`AnchorAudit.lean` provides a kernel-checked witness of the complete frozen
expanded target expression. The target's explicit measurability and
probability-measure assumptions are conservative extra premises: the pinned
theorem derives sufficient measurability from integrability and handles the
probability-space boundary internally. They are not removed from or changed
in the checked witness.

The adjacent `strong_law_ae_real` is also exact up to the routine identity
`sum / n = n^-1 * sum`. `strong_law_Lp` is not a root candidate because its
convergence mode and moment premises differ. A search of every pre-existing
pinned Lean package and repo-local Lean file found no independent external
terminal implementation; local hits are wrappers or unrelated Kolmogorov
theorems. A supplementary public code-index query returned HTTP 503 and is
recorded only as a search limitation, not evidence.

Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for both
audit declarations, with no `sorryAx`. This is candidate evidence, not proof-
phase or theorem-completion credit. Human-source pinpointing remains `H1`, the
root vector remains `[H1, M3, R3]`, and master acceptance is still required.
