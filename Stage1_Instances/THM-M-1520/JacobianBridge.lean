import Mathlib.MeasureTheory.Function.Jacobian

/-!
# THM-M-1520 Jacobian-to-measure bridge

This module implements the terminal change-of-variables step of `M1520-L-CHANGE` once the open
analytic subtree has supplied global differentiability, bijectivity, and determinant one for a
fixed time map.
-/

open MeasureTheory
open Set

noncomputable section

namespace Stage1.THM_M_1520

universe u

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
  [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]

/-- A differentiable bijection with unit Fréchet-Jacobian determinant preserves volume. -/
theorem measurePreserving_of_det_fderiv_eq_one
    {f : E → E} (hf : Differentiable Real f) (hbij : Function.Bijective f)
    (hdet : forall x, (fderiv Real f x).det = 1) :
    MeasurePreserving f volume volume := by
  refine ⟨hf.continuous.measurable, ?_⟩
  apply Measure.ext fun s hs => ?_
  rw [Measure.map_apply hf.continuous.measurable hs]
  have hchange := lintegral_abs_det_fderiv_eq_addHaar_image
    (μ := (volume : Measure E)) (hf.continuous.measurable hs)
    (s := f ⁻¹' s)
    (f := f) (f' := fun x => fderiv Real f x)
    (fun x _ => (hf x).hasFDerivAt.hasFDerivWithinAt)
    hbij.1.injOn
  simp only [hdet, abs_one, ENNReal.ofReal_one, setLIntegral_one] at hchange
  calc
    volume (f ⁻¹' s) = volume (f '' (f ⁻¹' s)) := hchange
    _ = volume s := by rw [hbij.2.image_preimage]

#print sorries measurePreserving_of_det_fderiv_eq_one
#print axioms measurePreserving_of_det_fderiv_eq_one

end Stage1.THM_M_1520
