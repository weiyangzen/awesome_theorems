# THM-M-0536 rev-5.6 statement

This directory freezes and elaborates the exact Lean target for homotopy invariance of homology.
`Target.lean` says that the forward map of a chosen homotopy equivalence induces an isomorphism on
unreduced integral singular homology in every natural-number degree.

The conventions are mathlib's `singularHomologyFunctor`, coefficients given by `ℤ` as an object of
`ModuleCat ℤ`, natural-number grading, and `ContinuousMap.HomotopyEquiv`. Spaces are restricted to
Lean's base universe because the coefficient object `ℤ` is small and mathlib's functor requires the
coefficient category and spaces at the same universe. Empty spaces and degree zero remain included;
negative degrees are outside this natural grading.

This completes only statement elaboration. The provisional root vector remains `[H1, M4, R4]`:
the anchor audit, proof, and all completion gates remain open. Exact commands and environment pins
are in `statement-validation.md`; intake evidence remains in `validation.md`.
