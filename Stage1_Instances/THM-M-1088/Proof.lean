import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
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

/-- Each centered coordinate has the exact coordinate variance as its sub-Gaussian MGF parameter.
This is finite-dimensional substrate only: sub-Gaussianity is not preserved by a pointwise maximum
through any theorem used here. -/
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
    rw [← hMap] at hInt
    exact hInt.comp_aemeasurable hLaw.aemeasurable
  · intro l
    rw [ProbabilityTheory.mgf_gaussianReal hMap]
    simp

/-- The `u = 0` branch of the canonical strict-event tail bound follows directly from the
probability normalization forced by a nonempty Gaussian process.  It does not depend on the open
Gaussian-concentration/MGF package. -/
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

/-- Process-level composition of the two implemented tail branches.  This exposes the exact open
analytic premise: a sharp sub-Gaussian MGF bound for the centered supremum with parameter `sigma2`.
The premise is not inferred from `hGaussian` here. -/
theorem upperTailBound_of_process_hasSubgaussianMGF
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
      upperTailBound_of_hasSubgaussianMGF P S (Real.toNNReal sigma2) hmgf u hu.le

#print axioms Stage1Instances.THM_M_1088.Proof.upperTailBound_of_hasSubgaussianMGF
#print axioms Stage1Instances.THM_M_1088.Proof.zeroTailBound_of_isGaussianProcess
#print axioms Stage1Instances.THM_M_1088.Proof.upperTailBound_of_process_hasSubgaussianMGF
#print axioms Stage1Instances.THM_M_1088.Proof.coordinate_hasSubgaussianMGF

end Stage1Instances.THM_M_1088.Proof
