import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Normed.Operator.FredholmAlternative

/-!
# THM-M-1161: pinned anchor probes

These probes check the operator-level declarations retained by the anchor
audit. They do not prove the integral-equation target.
-/

#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet
#check IsCompactOperator.hasEigenvalue_iff_mem_spectrum
#check ContinuousLinearMap.orthogonal_ker
#check ContinuousLinearMap.orthogonal_range
#check ContinuousLinearMap.adjoint
#check ContinuousLinearMap.isUnit_iff_bijective
#check spectrum.mem_resolventSet_iff

namespace AwesomeTheorems.Stage1.THM_M_1161.AnchorAudit

open Module End

/-- Checked wrapper around the closest pinned mathlib theorem. Its conclusion
is strictly operator-spectral and does not include the integral realization or
the adjoint solvability equivalence of the canonical target. -/
theorem compactOperatorFredholmAnchor
    {K E : Type*} [NontriviallyNormedField K]
    [NormedAddCommGroup E] [NormedSpace K E] [CompleteSpace E]
    {T : E →L[K] E} {mu : K} (hT : IsCompactOperator T) (hmu : mu ≠ 0) :
    HasEigenvalue (T : End K E) mu ∨ mu ∈ resolventSet K T :=
  IsCompactOperator.hasEigenvalue_or_mem_resolventSet hT hmu

end AwesomeTheorems.Stage1.THM_M_1161.AnchorAudit
