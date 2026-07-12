import Statement

/-!
# THM-M-1245 independent validation probe

This module imports the frozen statement but neither proof-phase module. It
independently reconstructs the exact root directly from the pinned mathlib
Sobolev estimate.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1245.Validation

/-- Independently written reconstruction of the exact frozen root. -/
theorem independentlyReconstructedRoot : SobolevInequalityTarget := by
  intro n p q hn hp hpq
  refine ⟨MeasureTheory.eLpNormLESNormFDerivOfEqInnerConst
      (volume : Measure (EuclideanSpace Real (Fin n))) p, ?_⟩
  intro u hu hcu
  have hfin : 0 < Module.finrank Real (EuclideanSpace Real (Fin n)) := by
    simpa using hn
  have hconj :
      (q : Real)⁻¹ = (p : Real)⁻¹ -
        (Module.finrank Real (EuclideanSpace Real (Fin n)) : Real)⁻¹ := by
    simpa using hpq
  simpa using
    MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner
      volume hu hcu hp hfin hconj

#print axioms independentlyReconstructedRoot
#print axioms MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner

end Stage1Instances.THM_M_1245.Validation
