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

At intake, lifecycle was `planned` and the provisional root vector was `[H1, M3, R3]`; the first
failed theorem gate was the exact Lean statement gate. The provisional statement result below now
addresses that node, but does not change authoritative state before master acceptance. No theorem
completion is claimed.

## Provisional statement result

The statement-phase artifacts now freeze and elaborate
`Stage1Instances.THM_M_1019.Statement` from the single direct import
`Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`. A kernel-checked `iff` connects it
to the expanded real integral form. The statement receipt remains provisional until master
acceptance; the anchor audit and every proof and release gate remain open.

## Validation

The commands and results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier hygiene only. Master acceptance and all dependent phases
remain outstanding.
