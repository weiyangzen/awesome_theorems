# THM-M-1033 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Ito isometry. It does not inherit proof
credit or accepted state from the legacy `S1_M_226.lean` statement-shape artifact.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Continuous-time real Brownian Ito isometry on a fixed finite horizon | Elaboration and expression fingerprint belong to the dependent statement phase |
| Probability model | Complete filtered probability space satisfying the usual conditions, carrying a standard Brownian motion | The exact Lean object model and completion conventions remain open |
| Integrand | Real predictable process with finite expected time integral of its square | Predictable versus progressively measurable encodings require checked comparison |
| Integral | Ito integral from time `0` to `T` | Construction, modification conventions, and terminal API are not credited at intake |
| Conclusion | `E[(integral_0^T H_t dW_t)^2] = E[integral_0^T H_t^2 dt]` | Extended/nonnegative versus Bochner integral representation remains to be frozen |
| Degenerate cases | `T = 0` and integrands equal almost everywhere | Boundary probes are mandatory; they are not proof credit |
| Foundations | Lean 4 kernel plus pinned mathlib and an accepted classical/choice/quotient policy | Exact toolchain, imports, dependency closure, and TCB fingerprint remain open |

The dossier deliberately excludes the stronger general square-integrable-martingale bracket
isometry and the weaker finite discrete predictable-sum theorem from the root. They are possible
generalization and approximation nodes, respectively, and cannot silently replace the Brownian
continuous-time claim. The legacy file's abstract propositions and discrete `Nat`-indexed model are
discovery inputs only.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the Lean statement gate: there is no elaborated canonical expression, environment fingerprint,
checked encoding transport, or mutation record. The theorem is not complete.

## Validation

On base revision `dbd29db42090d2fce49f69d84d4631769ef7e9c3`, the commands in `validation.md`
establish manifest membership, repository-standard consistency, JSON syntax, and dossier hygiene
only. No Lean proof or source acceptance is claimed.
