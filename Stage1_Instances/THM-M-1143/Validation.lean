import Proof

/-!
# THM-M-1143 validation probes

This module adds no proof of the open interior gradient estimate. It independently restates two
already implemented elementary proof steps over the imported interfaces and checks the exact
canonical target and conditional composition declarations. These are same-workspace,
import-dependent probes, not an independent release verifier.
-/

open Bornology Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1143.Validation

open Stage1Instances.THM_M_1143

/-- A second implementation of the bounded-range normalization used by the proof phase. -/
theorem uniformAbsBoundDirect {n : Nat} {f : Space n -> Real}
    (hb : IsBounded (range f)) :
    exists C : Real, forall x, |f x| <= C := by
  rw [isBounded_iff_forall_norm_le] at hb
  obtain ⟨C, hC⟩ := hb
  refine ⟨C, fun x => ?_⟩
  simpa only [Real.norm_eq_abs] using hC (f x) ⟨x, rfl⟩

/-- A second proof that reciprocal-radius domination forces a continuous linear map to vanish. -/
theorem continuousLinearMapEqZeroDirect
    {E F : Type*} [NormedAddCommGroup E] [NormedSpace Real E]
    [NormedAddCommGroup F] [NormedSpace Real F]
    (L : E →L[Real] F) (A : Real) (hA : 0 <= A)
    (hbound : forall R : Real, 0 < R -> ‖L‖ <= A / R) :
    L = 0 := by
  by_contra hL
  have hnorm : 0 < ‖L‖ := norm_pos_iff.mpr hL
  let R : Real := A / ‖L‖ + 1
  have hR : 0 < R := by
    dsimp [R]
    positivity
  have hle := hbound R hR
  have hlt : A / R < ‖L‖ := by
    rw [div_lt_iff₀ hR]
    dsimp [R]
    rw [mul_add, mul_div_cancel₀ A hnorm.ne']
    linarith
  exact (not_lt_of_ge hle) hlt

#check BoundedHarmonicIsConstant
#check InteriorGradientEstimatePackage
#check root_of_interiorGradientEstimate

#print axioms uniformAbsBoundDirect
#print axioms continuousLinearMapEqZeroDirect
#print axioms root_of_interiorGradientEstimate

end Stage1Instances.THM_M_1143.Validation
