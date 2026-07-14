import Statement
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1088 same-worker separate-module validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It replays the proof phase's
four partial arguments in a separate module namespace. The bodies intentionally follow the same
route and therefore provide no implementation-diversity or independent-verifier credit. The
process-level result retains the sharp centered-supremum MGF estimate as an explicit premise, so it
is not a proof of Borell--TIS or of any frozen obligation.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal

namespace Stage1Instances.THM_M_1088.Validation

/-- Separate-module replay of the exact coordinate sub-Gaussian MGF fact. -/
theorem coordinate_hasSubgaussianMGF
    {Omega T : Type*} [MeasurableSpace Omega] [Nonempty T]
    (P : Measure Omega) (X : T -> Omega -> Real)
    (hGaussian : ProbabilityTheory.IsGaussianProcess X P)
    (hCentered : forall t, ∫ omega, X t omega ∂P = 0)
    (t : T) :
    ProbabilityTheory.HasSubgaussianMGF (X t)
      (Real.toNNReal (ProbabilityTheory.variance (X t) P)) P := by
  have hLaw := hGaussian.hasGaussianLaw_eval t
  have hMap : P.map (X t) = ProbabilityTheory.gaussianReal 0
      (Real.toNNReal (ProbabilityTheory.variance (X t) P)) := by
    rw [hLaw.isGaussian_map.eq_gaussianReal]
    congr
    · rw [integral_map]
      · simpa using hCentered t
      · exact hLaw.aemeasurable
      · exact aestronglyMeasurable_id
    · rw [ProbabilityTheory.variance_id_map hLaw.aemeasurable]
  constructor
  · intro l
    have hInt : Integrable (fun x : Real => Real.exp (l * x))
        (ProbabilityTheory.gaussianReal 0
          (Real.toNNReal (ProbabilityTheory.variance (X t) P))) :=
      ProbabilityTheory.integrable_exp_mul_gaussianReal l
    rw [<- hMap] at hInt
    exact hInt.comp_aemeasurable hLaw.aemeasurable
  · intro l
    rw [ProbabilityTheory.mgf_gaussianReal hMap]
    simp

/-- Separate-module replay of the exact strict-event `u = 0` bound. -/
theorem zeroTailBound_of_isGaussianProcess
    {Omega T : Type*} [MeasurableSpace Omega] [Nonempty T]
    (P : Measure Omega) (X : T -> Omega -> Real) (S : Omega -> Real) (sigma2 : Real)
    (hGaussian : ProbabilityTheory.IsGaussianProcess X P) :
    P {omega | (0 : Real) < S omega - ∫ x, S x ∂P} <=
      ENNReal.ofReal (Real.exp (-((0 : Real) ^ 2) / (2 * sigma2))) := by
  letI : IsProbabilityMeasure P := hGaussian.isProbabilityMeasure
  calc
    P {omega | (0 : Real) < S omega - ∫ x, S x ∂P} <= P Set.univ :=
      measure_mono (Set.subset_univ _)
    _ = 1 := measure_univ
    _ = ENNReal.ofReal (Real.exp (-((0 : Real) ^ 2) / (2 * sigma2))) := by simp

/-- Separate-module replay of the generic MGF-to-strict-tail conversion. -/
theorem strictUpperTail_of_hasSubgaussianMGF
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

/-- Same-worker duplicate-route process adapter. The missing sharp supremum MGF remains an explicit
premise and therefore receives no Borell--TIS, frozen-obligation, or independent-verifier credit. -/
theorem processUpperTail_of_supremumMGF
    {Omega T : Type*} [MeasurableSpace Omega] [Nonempty T]
    (P : Measure Omega) (X : T -> Omega -> Real) (S : Omega -> Real) (sigma2 : Real)
    (hGaussian : ProbabilityTheory.IsGaussianProcess X P)
    (hsigma2 : 0 < sigma2)
    (hmgf : ProbabilityTheory.HasSubgaussianMGF
      (fun omega => S omega - ∫ x, S x ∂P) (Real.toNNReal sigma2) P) :
    forall u : Real, 0 <= u ->
      P {omega | u < S omega - ∫ x, S x ∂P} <=
        ENNReal.ofReal (Real.exp (-(u ^ 2) / (2 * sigma2))) := by
  letI : IsProbabilityMeasure P := hGaussian.isProbabilityMeasure
  intro u hu
  rcases hu.eq_or_lt with rfl | hu
  · exact zeroTailBound_of_isGaussianProcess P X S sigma2 hGaussian
  · simpa [Real.coe_toNNReal sigma2 hsigma2.le] using
      strictUpperTail_of_hasSubgaussianMGF P S (Real.toNNReal sigma2) hmgf u hu.le

assert_no_sorry coordinate_hasSubgaussianMGF
assert_no_sorry zeroTailBound_of_isGaussianProcess
assert_no_sorry strictUpperTail_of_hasSubgaussianMGF
assert_no_sorry processUpperTail_of_supremumMGF
#print sorries coordinate_hasSubgaussianMGF
#print sorries zeroTailBound_of_isGaussianProcess
#print sorries strictUpperTail_of_hasSubgaussianMGF
#print sorries processUpperTail_of_supremumMGF
#print axioms coordinate_hasSubgaussianMGF
#print axioms zeroTailBound_of_isGaussianProcess
#print axioms strictUpperTail_of_hasSubgaussianMGF
#print axioms processUpperTail_of_supremumMGF

end Stage1Instances.THM_M_1088.Validation
