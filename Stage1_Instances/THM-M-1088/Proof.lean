import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-1088 proof work

This module implements the tail-conversion part of the frozen Borell--TIS architecture.  The
remaining open analytic obligation is to prove the centered supremum has the sharp sub-Gaussian
MGF parameter.  That implication is not assumed here to be a consequence of the Gaussian-process
hypotheses.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal

namespace Stage1Instances.THM_M_1088.Proof

/-- A sub-Gaussian MGF bound for the centered supremum implies the exact strict-event `ENNReal`
tail bound used by the canonical target.  This covers both `u = 0` and positive `u`; the passage
from `<` to `<=` is by event inclusion, not by changing the public statement. -/
theorem upperTailBound_of_hasSubgaussianMGF
    {Omega : Type*} [MeasurableSpace Omega] (P : Measure Omega) [IsFiniteMeasure P]
    (S : Omega -> Real) (c : NNReal)
    (hmgf : ProbabilityTheory.HasSubgaussianMGF
      (fun omega => S omega - ∫ x, S x ∂P) c P) :
    forall u : Real, 0 <= u ->
      P {omega | u < S omega - ∫ x, S x ∂P} <=
        ENNReal.ofReal (Real.exp (-(u ^ 2) / (2 * (c : Real)))) := by
  intro u hu
  calc
    P {omega | u < S omega - ∫ x, S x ∂P}
        <= P {omega | u <= S omega - ∫ x, S x ∂P} := by
          apply measure_mono
          intro omega homega
          change u < S omega - ∫ x, S x ∂P at homega
          change u <= S omega - ∫ x, S x ∂P
          exact homega.le
    _ = ENNReal.ofReal (P.real {omega | u <= S omega - ∫ x, S x ∂P}) := by
          exact (ENNReal.ofReal_toReal (measure_ne_top P _)).symm
    _ <= ENNReal.ofReal (Real.exp (-(u ^ 2) / (2 * (c : Real)))) := by
          exact ENNReal.ofReal_le_ofReal (hmgf.measure_ge_le hu)

#print axioms Stage1Instances.THM_M_1088.Proof.upperTailBound_of_hasSubgaussianMGF

end Stage1Instances.THM_M_1088.Proof
