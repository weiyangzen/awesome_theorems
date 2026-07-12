# THM-M-1056 rev-5.6 intake

This is the `planned` instance for the Oseledets multiplicative ergodic theorem. The legacy gloss
"Lyapunov exponents of random matrices" does not fix a unique variant. This intake selects the
classical finite-dimensional invertible ergodic cocycle variant. The statement phase freezes its
exact Lean encoding in `Statement.lean` and `statement.json`.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Base | invertible ergodic probability-preserving `T` | measurable-space assumptions unfrozen |
| Cocycle | strongly measurable `A : Omega -> (E ≃L[Real] E)` and left-to-right forward action | proof properties open |
| Hypotheses | integrable `log+ ||A||` and `log+ ||A^-1||` | source-equivalence audit open |
| Conclusion | a.e. finite Lyapunov spectrum and invariant measurable splitting with vector growth rates | filtration-only/noninvertible variants excluded |
| Formal system | Lean 4 plus pinned mathlib | target elaborated; proof and downstream gates open |

See `intake.json` and `source_statement_crosswalk.md`. The source label `已验证` provides no proof
credit.

## Verdict and task DAG

Lifecycle remains `planned`, with root vector `[H1, M4, R3]`. The exact statement is self-tested
and pending master acceptance; the theorem is not proved or complete.

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Intake and statement have worker self-tests; master acceptance and all later nodes remain open.
