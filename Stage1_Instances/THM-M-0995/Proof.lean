import ObligationTree
import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0995 proof execution

This module contains the proof bodies closed during the proof phase.  The
remaining analytic MGF leaf is recorded in `proof-validation.md`; no theorem
below assumes the canonical Bernstein conclusion.
-/

noncomputable section

open Finset MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0995.Proof

open Stage1Instances.THM_M_0995
open Stage1Instances.THM_M_0995.ObligationTree

universe u

/-- Chernoff's inequality specialized to the exact finite sum interface. -/
theorem chernoffPackage : ChernoffPackage.{u} := by
  intro Omega _ P s t hs
  letI : IsProbabilityMeasure P.mu := P.isProbability
  have hsum_meas : AEMeasurable (partialSum P.n P.X) P.mu := by
    unfold partialSum
    exact Finset.aemeasurable_fun_sum (range P.n) fun i hi =>
      P.aemeasurable i (Finset.mem_range.mp hi)
  have hsum_bound : ∀ᵐ omega ∂P.mu,
      |partialSum P.n P.X omega| <= P.n * P.bound := by
    have hall : ∀ᵐ omega ∂P.mu, ∀ i ∈ range P.n, |P.X i omega| <= P.bound := by
      rw [Finset.eventually_all]
      intro i hi
      exact P.abs_bound_ae i (Finset.mem_range.mp hi)
    filter_upwards [hall] with omega homega
    calc
      |partialSum P.n P.X omega| <= ∑ i ∈ range P.n, |P.X i omega| := by
        simpa [partialSum] using
          (Finset.abs_sum_le_sum_abs (s := range P.n) (f := fun i => P.X i omega))
      _ <= ∑ _i ∈ range P.n, P.bound := by
        exact Finset.sum_le_sum fun i hi => homega i hi
      _ = P.n * P.bound := by simp
  have hInt : Integrable
      (fun omega => Real.exp (s * partialSum P.n P.X omega)) P.mu := by
    apply (integrable_const (Real.exp (|s| * (P.n * P.bound)))).mono
    · exact hsum_meas.const_mul s |>.exp.aestronglyMeasurable
    filter_upwards [hsum_bound] with omega homega
    simp only [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    exact Real.exp_le_exp.mpr <| calc
      s * partialSum P.n P.X omega
          <= |s * partialSum P.n P.X omega| := le_abs_self _
      _ = |s| * |partialSum P.n P.X omega| := abs_mul _ _
      _ <= |s| * (P.n * P.bound) :=
        mul_le_mul_of_nonneg_left homega (abs_nonneg s)
  simpa [ProbabilityTheory.mgf] using
    (ProbabilityTheory.measure_ge_le_exp_mul_mgf
      (μ := P.mu) (X := partialSum P.n P.X) t hs hInt)

/-- The zero-denominator branch follows from the probability-measure bound. -/
theorem zeroDenominatorPackage : ZeroDenominatorPackage.{u} := by
  intro Omega _ P t ht hden
  letI : IsProbabilityMeasure P.mu := P.isProbability
  rw [hden]
  simp only [mul_zero, div_zero, Real.exp_zero]
  exact measureReal_le_one

/-- The frozen optimizer interface is inconsistent at `v = 0, b = 1, t = 1`. -/
theorem not_optimizeExponentPackage : Not OptimizeExponentPackage := by
  intro h
  have hcase := h 0 1 1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  norm_num at hcase

/-- Compose the tail, sum-MGF, optimization, and zero-denominator branches. -/
theorem assemblyPackage : AssemblyPackage.{u} := by
  intro _hIndividual hSum hChernoff hOptimize hZero
  intro Omega _ P t ht
  let d := P.varianceBudget + P.bound * t / 3
  by_cases hd : d = 0
  · exact hZero Omega P t ht hd
  have hdpos : 0 < d := lt_of_le_of_ne
    (add_nonneg P.varianceBudget_nonneg
      (div_nonneg (mul_nonneg P.bound_nonneg ht) (by norm_num)))
    (Ne.symm hd)
  let s := t / d
  obtain ⟨hs0, hsb, hopt⟩ :=
    hOptimize P.varianceBudget P.bound t P.varianceBudget_nonneg P.bound_nonneg ht hdpos
  calc
    P.mu.real {omega | t <= partialSum P.n P.X omega}
        <= Real.exp (-s * t) *
          (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu) :=
      hChernoff Omega P s t hs0
    _ <= Real.exp (-s * t) *
          Real.exp (s ^ 2 * P.varianceBudget /
            (2 * (1 - s * P.bound / 3))) := by
      gcongr
      exact hSum Omega P s hs0 hsb
    _ <= Real.exp (-(t ^ 2) /
          (2 * (P.varianceBudget + P.bound * t / 3))) := hopt

end Stage1Instances.THM_M_0995.Proof

#check Stage1Instances.THM_M_0995.Proof.zeroDenominatorPackage
#check Stage1Instances.THM_M_0995.Proof.chernoffPackage
#check Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage
#check Stage1Instances.THM_M_0995.Proof.assemblyPackage
#print axioms Stage1Instances.THM_M_0995.Proof.zeroDenominatorPackage
#print axioms Stage1Instances.THM_M_0995.Proof.chernoffPackage
#print axioms Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage
#print axioms Stage1Instances.THM_M_0995.Proof.assemblyPackage
