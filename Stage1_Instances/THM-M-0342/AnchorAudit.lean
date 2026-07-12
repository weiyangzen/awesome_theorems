import Mathlib.Analysis.Fourier.LpSpace

/-!
# THM-M-0342 anchor audit

This probe checks the pinned mathlib declarations against the frozen target shape. It is candidate
evidence only: the assigned phase does not promote the target or install a proof artifact.
-/

open MeasureTheory
open scoped FourierTransform ENNReal

namespace Stage1Instances.THM_M_0342.AnchorAudit

abbrev Domain (n : Nat) := EuclideanSpace Real (Fin n)

#check MeasureTheory.Lp.fourierTransformₗᵢ
#check MeasureTheory.Lp.norm_fourier_eq
#check MeasureTheory.Lp.inner_fourier_eq

/-- Exact-type probe for the norm-preservation candidate used by the frozen statement. -/
example :
    forall (n : Nat) (f : Domain n -> Complex),
      forall hf : MemLp f 2 (volume : Measure (Domain n)),
        ‖𝓕 (hf.toLp f)‖ = ‖hf.toLp f‖ := by
  intro n f hf
  exact MeasureTheory.Lp.norm_fourier_eq (hf.toLp f)

/-- The stronger inner-product API also specializes to the frozen domain. -/
example (n : Nat) (f g : Lp (α := Domain n) Complex 2) :
    @inner Complex _ _ (𝓕 f) (𝓕 g) = @inner Complex _ _ f g := by
  exact MeasureTheory.Lp.inner_fourier_eq f g

end Stage1Instances.THM_M_0342.AnchorAudit

#print axioms MeasureTheory.Lp.fourierTransformₗᵢ
#print axioms MeasureTheory.Lp.norm_fourier_eq
#print axioms MeasureTheory.Lp.inner_fourier_eq
