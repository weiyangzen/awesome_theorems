import FlowAlgebra
import JacobianBridge

/-!
# THM-M-1520 fixed-time change of variables

This module composes the frozen flow-algebra and Jacobian-to-measure subbranches. The remaining
analytic work must still prove spatial differentiability and determinant one for every time map.
-/

open MeasureTheory

noncomputable section

namespace Stage1.THM_M_1520

/-- A time map preserves volume once the open analytic subtree supplies spatial differentiability
and unit Frechet-Jacobian determinant. Bijectivity is derived from the stated two-sided flow laws. -/
theorem timeMap_measurePreserving_of_differentiable_det_eq_one
    {n : Nat} {Phi : Real -> PhaseSpace n -> PhaseSpace n}
    (hzero : forall z, Phi 0 z = z)
    (hflow : forall s t z, Phi (s + t) z = Phi s (Phi t z))
    (t : Real) (hdiff : Differentiable Real (Phi t))
    (hdet : forall z, (fderiv Real (Phi t) z).det = 1) :
    MeasurePreserving (Phi t) volume volume := by
  exact measurePreserving_of_det_fderiv_eq_one hdiff
    (timeMap_bijective hzero hflow t) hdet

/-- Uniform fixed-time composition. This is not the missing analytic package: differentiability
and determinant one remain explicit premises for every time. -/
theorem allTimeMaps_measurePreserving_of_differentiable_det_eq_one
    {n : Nat} {Phi : Real -> PhaseSpace n -> PhaseSpace n}
    (hzero : forall z, Phi 0 z = z)
    (hflow : forall s t z, Phi (s + t) z = Phi s (Phi t z))
    (hdiff : forall t, Differentiable Real (Phi t))
    (hdet : forall t z, (fderiv Real (Phi t) z).det = 1) :
    forall t, MeasurePreserving (Phi t) volume volume := by
  intro t
  exact timeMap_measurePreserving_of_differentiable_det_eq_one hzero hflow t (hdiff t) (hdet t)

#print sorries timeMap_measurePreserving_of_differentiable_det_eq_one
#print axioms timeMap_measurePreserving_of_differentiable_det_eq_one
#print sorries allTimeMaps_measurePreserving_of_differentiable_det_eq_one
#print axioms allTimeMaps_measurePreserving_of_differentiable_det_eq_one

end Stage1.THM_M_1520
