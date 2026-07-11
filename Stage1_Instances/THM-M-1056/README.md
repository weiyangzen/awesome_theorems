# THM-M-1056 rev-5.6 intake

This is the `planned` instance for the Oseledets multiplicative ergodic theorem. The legacy gloss
"Lyapunov exponents of random matrices" does not fix a unique variant. This intake selects the
classical finite-dimensional invertible ergodic cocycle variant; exact encoding is deferred.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Base | invertible ergodic probability-preserving `T` | measurable-space assumptions unfrozen |
| Cocycle | measurable `A : Omega -> GL(d, R)` and forward products | product convention unfrozen |
| Hypotheses | integrable `log+ ||A||` and `log+ ||A^-1||` | exact Lean integrability encoding open |
| Conclusion | a.e. finite Lyapunov spectrum and invariant measurable splitting with vector growth rates | filtration-only/noninvertible variants excluded |
| Formal system | Lean 4 plus pinned mathlib | imports, toolchain, and expression fingerprint open |

See `intake.json` and `source_statement_crosswalk.md`. The source label `已验证` provides no proof
credit.

## Verdict and task DAG

Lifecycle is `planned`, with provisional root vector `[H1, M4, R3]`. The exact-statement gate is
open; the theorem is not complete.

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only intake is self-tested; all dependent nodes and master acceptance remain open.

