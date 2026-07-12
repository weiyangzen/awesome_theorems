import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.FDeriv.Bilinear
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

/-!
# THM-M-0158 anchor audit probes

This module checks the pinned mathlib APIs that can support a local proof of the frozen
Weingarten-equations statement. It deliberately does not assert the target theorem.
-/

namespace Stage1Instances.THM_M_0158.AnchorCandidates

#check ContDiffOn.differentiableOn
#check ContDiffWithinAt.fderivWithin_right_apply
#check ContinuousLinearMap.hasFDerivWithinAt_of_bilinear
#check ContinuousLinearMap.fderivWithin_of_bilinear
#check Matrix.mul_nonsing_inv
#check Matrix.nonsing_inv_mul

/-- A determinant hypothesis in the frozen target supplies the two-sided matrix inverse API. -/
theorem gram_inverse_probe (A : Matrix (Fin 2) (Fin 2) Real) (hA : Matrix.det A ≠ 0) :
    A * A⁻¹ = 1 ∧ A⁻¹ * A = 1 := by
  have hunit : IsUnit A.det := isUnit_iff_ne_zero.mpr hA
  exact ⟨Matrix.mul_nonsing_inv A hunit, Matrix.nonsing_inv_mul A hunit⟩

end Stage1Instances.THM_M_0158.AnchorCandidates
