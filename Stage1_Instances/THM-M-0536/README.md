# THM-M-0536 rev-5.6 dossier

This directory freezes and elaborates the exact Lean target for homotopy invariance of homology.
`Target.lean` says that the forward map of a chosen homotopy equivalence induces an isomorphism on
unreduced integral singular homology in every natural-number degree.

The conventions are mathlib's `singularHomologyFunctor`, coefficients given by `ℤ` as an object of
`ModuleCat ℤ`, natural-number grading, and `ContinuousMap.HomotopyEquiv`. Spaces are restricted to
Lean's base universe because the coefficient object `ℤ` is small and mathlib's functor requires the
coefficient category and spaces at the same universe. Empty spaces and degree zero remain included;
negative degrees are outside this natural grading.

The bounded anchor audit selected
`TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor` from pinned mathlib and composed it
with the two fields of `ContinuousMap.HomotopyEquiv` in `AnchorAudit.lean`. The exact candidate
elaborates and has only `propext`, `Classical.choice`, and `Quot.sound` in its reported axiom
set. Candidate inventory, immutable revisions, external discovery limits, and commands are in
`anchor-audit.md`.

`Proof.lean` now gives a placeholder-free proof of the exact target. It separately checks both
induced inverse laws and installs the inverse map in `IsIso`; `proof-receipt.json` and
`proof-validation.md` record the provisional proof-node evidence. This closes the local machine
root for the proof phase pending master acceptance, but it does not claim theorem completion:
source/readability acceptance, hermetic validation, independent verification, and release remain
open. Intake and statement receipts remain in `validation.md` and `statement-validation.md`.
