import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-1063 proof-phase kernel lemmas

This module implements two exact components of the frozen Donsker architecture. It standardizes
the increments by the positive scale and then applies the pinned scalar central limit theorem to
the normalized partial sums. These are substantive local proof bodies, but scalar time-one
convergence is strictly weaker than convergence of the polygonal processes in continuous path
space. No path measurability, tightness, limit-identification, or Donsker root closure is claimed.
-/

open Filter Finset MeasureTheory ProbabilityTheory Set
open scoped Real Topology

namespace AwesomeTheorems.Stage1.THM_M_1063.Proof

noncomputable section

universe u

/-- The variance-one increments obtained by dividing by the frozen positive standard deviation. -/
def standardizedIncrement {Omega : Type u} (X : Nat -> Omega -> Real) (sigma : Real) :
    Nat -> Omega -> Real :=
  fun i omega => sigma⁻¹ * X i omega

/-- Positive scaling transports all hypotheses needed by the scalar CLT to the standardized
increments. This is an exact checked contribution toward `M1063-N-STANDARDIZE`. -/
theorem standardizedIncrement_package
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (X : Nat -> Omega -> Real) (sigma : Real)
    (hsigma : 0 < sigma)
    (hMeas : forall i, AEMeasurable (X i) P)
    (hIndep : iIndepFun X P)
    (hIdent : forall i, IdentDistrib (X i) (X 0) P P)
    (hLp : MemLp (X 0) 2 P)
    (hMean : (∫ omega, X 0 omega ∂P) = 0)
    (hVar : variance (X 0) P = sigma ^ 2) :
    (forall i, AEMeasurable (standardizedIncrement X sigma i) P) /\
      iIndepFun (standardizedIncrement X sigma) P /\
      (forall i, IdentDistrib (standardizedIncrement X sigma i)
        (standardizedIncrement X sigma 0) P P) /\
      MemLp (standardizedIncrement X sigma 0) 2 P /\
      (∫ omega, standardizedIncrement X sigma 0 omega ∂P) = 0 /\
      variance (standardizedIncrement X sigma 0) P = 1 := by
  have hsigma_ne : sigma ≠ 0 := ne_of_gt hsigma
  have hMeasStd : forall i, AEMeasurable (standardizedIncrement X sigma i) P := by
    intro i
    exact (hMeas i).const_mul sigma⁻¹
  have hIndepStd : iIndepFun (standardizedIncrement X sigma) P := by
    simpa only [standardizedIncrement, Function.comp_def] using
      hIndep.comp (fun _ x => sigma⁻¹ * x) (fun _ => by fun_prop)
  have hIdentStd : forall i, IdentDistrib (standardizedIncrement X sigma i)
      (standardizedIncrement X sigma 0) P P := by
    intro i
    simpa only [standardizedIncrement] using (hIdent i).const_mul sigma⁻¹
  have hLpStd : MemLp (standardizedIncrement X sigma 0) 2 P := by
    exact hLp.const_mul sigma⁻¹
  have hMeanStd : (∫ omega, standardizedIncrement X sigma 0 omega ∂P) = 0 := by
    simp only [standardizedIncrement]
    rw [integral_const_mul, hMean, mul_zero]
  have hVarStd : variance (standardizedIncrement X sigma 0) P = 1 := by
    unfold standardizedIncrement
    rw [variance_const_mul, hVar]
    rw [← mul_pow, inv_mul_cancel₀ hsigma_ne, one_pow]
  exact ⟨hMeasStd, hIndepStd, hIdentStd, hLpStd, hMeanStd, hVarStd⟩

/-- The pinned scalar CLT provides a checked contribution toward the time-one scalar support node.
It does not establish finite-dimensional or continuous-path convergence. -/
theorem scalarPartialSums_tendstoInDistribution
    {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (X : Nat -> Omega -> Real) (sigma : Real)
    (hsigma : 0 < sigma)
    (hMeas : forall i, AEMeasurable (X i) P)
    (hIndep : iIndepFun X P)
    (hIdent : forall i, IdentDistrib (X i) (X 0) P P)
    (hLp : MemLp (X 0) 2 P)
    (hMean : (∫ omega, X 0 omega ∂P) = 0)
    (hVar : variance (X 0) P = sigma ^ 2) :
    TendstoInDistribution
      (fun (n : Nat) omega =>
        (Real.sqrt n)⁻¹ * ∑ i ∈ range n, standardizedIncrement X sigma i omega)
      atTop id (fun _ => P) (gaussianReal 0 1) := by
  rcases standardizedIncrement_package P X sigma hsigma hMeas hIndep hIdent hLp hMean hVar with
    ⟨_hMeasStd, hIndepStd, hIdentStd, hLpStd, hMeanStd, hVarStd⟩
  have hSecondMoment :
      (∫ omega, standardizedIncrement X sigma 0 omega ^ 2 ∂P) = 1 := by
    have hVarianceIdentity := variance_eq_integral hLpStd.aemeasurable
    rw [hMeanStd] at hVarianceIdentity
    simpa only [sub_zero] using hVarianceIdentity.symm.trans hVarStd
  exact tendstoInDistribution_inv_sqrt_mul_sum
    HasLaw.id hMeanStd hSecondMoment hIndepStd hIdentStd

#check standardizedIncrement_package
#check scalarPartialSums_tendstoInDistribution

#print axioms standardizedIncrement_package
#print axioms scalarPartialSums_tendstoInDistribution

end

end AwesomeTheorems.Stage1.THM_M_1063.Proof
