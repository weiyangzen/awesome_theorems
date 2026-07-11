# THM-M-1019 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the uniqueness theorem for
characteristic functions. The Stage0 label `已验证` is discovery metadata only and
supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact human root | Equality of characteristic functions of two real-valued probability laws at every real argument implies equality of those laws | Lean elaboration and the choice of the canonical measure-level API belong to the statement phase |
| Random-variable form | Real-valued random variables have equal pushforward laws when their characteristic functions agree | A transport from random variables to probability measures must be checked, not assumed |
| Measure form | Borel probability measures on `Real`; characteristic function `t \mapsto \int x, exp (I * t * x) \partial\mu` | Measurability, integrability, scalar coercions, and Fourier-transform convention must be frozen later |
| Equality notion | Equality of Borel probability measures, equivalently equality in distribution | Pointwise equality, almost-everywhere equality, and equality only near zero are excluded from the root |
| Degenerate cases | Dirac and other atomic laws remain included; no moment or density hypothesis is permitted | Boundary mutations are statement-phase work |
| Foundations | Lean 4 kernel and pinned mathlib with an audited classical/choice policy | Toolchain, imports, TCB, and environment fingerprint remain open |

The intended theorem is the classical uniqueness theorem, not the neighboring inversion
formula, continuity theorem, Bochner theorem, or moment-determinacy result. Those may later
be dependencies but are not substitutes for the root.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem
gate is the exact Lean statement gate: there is not yet a selected and elaborated declaration,
normalized expression hash, environment fingerprint, or checked random-variable/measure
transport. No theorem completion is claimed.

## Validation

The commands and results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier hygiene only. Master acceptance and all dependent phases
remain outstanding.
