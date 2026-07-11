# THM-M-1330 rev-5.6 intake

This is a `planned` instance for the Donnelly-Li theorem. Repository metadata supplies only the
phrase "spectrum of negatively curved manifolds"; it is too broad to serve as an exact theorem.
The 1979 Donnelly-Li paper identified in the crosswalk supplies the provisional intended scope.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Geometry | complete, noncompact Riemannian manifold | dimension, connectedness, boundary, and curvature convention await exact source transcription |
| Asymptotic hypothesis | sectional curvature tends to minus infinity at infinity | quantifier/uniformity and exhaustion formulation are not yet frozen |
| Operator | Laplace-Beltrami operator on functions | sign and self-adjoint realization/domain await source and Lean design |
| Conclusion | pure point/discrete spectrum | the exact compact-resolvent/eigenbasis equivalence is not yet selected |
| Formal foundations | manifolds, curvature, Hilbert spaces, unbounded spectral theory | no Lean declaration or import is credited |

Later phases must not broaden this into every theorem about negative curvature, nor weaken the
asymptotic curvature hypothesis to constant negative curvature. The statement phase must first
obtain and hash the primary text, transcribe its numbered theorem and assumptions, then assess
whether mathlib can express the required unbounded-operator spectrum.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source statement identification: bibliographic identity is strong, but theorem/page, exact premises,
and errata are not accepted. Consequently no canonical Lean expression exists and the theorem is
not complete.

Validation commands and their limits are recorded in `validation.md`.
