import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-1063 validation probes

These declarations independently reconstruct the two scalar proof-phase results without importing
`Proof.lean`. They are same-worker differential probes, not a Donsker proof and not the distinct
runner required by the rev-5.6 independent-verification gate.
-/

open Filter Finset MeasureTheory ProbabilityTheory Set
open scoped Real Topology

namespace AwesomeTheorems.Stage1.THM_M_1063.Validation

noncomputable section

universe u

def normalizedIncrement {Omega : Type u} (X : Nat -> Omega -> Real) (sigma : Real) :
    Nat -> Omega -> Real :=
  fun i omega => sigma⁻¹ * X i omega

theorem independentlyStandardized
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
    (forall i, AEMeasurable (normalizedIncrement X sigma i) P) /\
      iIndepFun (normalizedIncrement X sigma) P /\
      (forall i, IdentDistrib (normalizedIncrement X sigma i)
        (normalizedIncrement X sigma 0) P P) /\
      MemLp (normalizedIncrement X sigma 0) 2 P /\
      (∫ omega, normalizedIncrement X sigma 0 omega ∂P) = 0 /\
      variance (normalizedIncrement X sigma 0) P = 1 := by
  have hsigma_ne : sigma ≠ 0 := ne_of_gt hsigma
  have hMeasNorm : forall i, AEMeasurable (normalizedIncrement X sigma i) P := by
    intro i
    exact (hMeas i).const_mul sigma⁻¹
  have hIndepNorm : iIndepFun (normalizedIncrement X sigma) P := by
    simpa only [normalizedIncrement, Function.comp_def] using
      hIndep.comp (fun _ x => sigma⁻¹ * x) (fun _ => by fun_prop)
  have hIdentNorm : forall i, IdentDistrib (normalizedIncrement X sigma i)
      (normalizedIncrement X sigma 0) P P := by
    intro i
    simpa only [normalizedIncrement] using (hIdent i).const_mul sigma⁻¹
  have hLpNorm : MemLp (normalizedIncrement X sigma 0) 2 P := hLp.const_mul sigma⁻¹
  have hMeanNorm : (∫ omega, normalizedIncrement X sigma 0 omega ∂P) = 0 := by
    simp only [normalizedIncrement]
    rw [integral_const_mul, hMean, mul_zero]
  have hVarNorm : variance (normalizedIncrement X sigma 0) P = 1 := by
    unfold normalizedIncrement
    rw [variance_const_mul, hVar]
    rw [← mul_pow, inv_mul_cancel₀ hsigma_ne, one_pow]
  exact ⟨hMeasNorm, hIndepNorm, hIdentNorm, hLpNorm, hMeanNorm, hVarNorm⟩

theorem independentlyReplayedScalarCLT
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
        (Real.sqrt n)⁻¹ * ∑ i ∈ range n, normalizedIncrement X sigma i omega)
      atTop id (fun _ => P) (gaussianReal 0 1) := by
  rcases independentlyStandardized P X sigma hsigma hMeas hIndep hIdent hLp hMean hVar with
    ⟨_hMeasNorm, hIndepNorm, hIdentNorm, hLpNorm, hMeanNorm, hVarNorm⟩
  have hSecondMoment :
      (∫ omega, normalizedIncrement X sigma 0 omega ^ 2 ∂P) = 1 := by
    have hVarianceIdentity := variance_eq_integral hLpNorm.aemeasurable
    rw [hMeanNorm] at hVarianceIdentity
    simpa only [sub_zero] using hVarianceIdentity.symm.trans hVarNorm
  exact tendstoInDistribution_inv_sqrt_mul_sum
    HasLaw.id hMeanNorm hSecondMoment hIndepNorm hIdentNorm

#print axioms independentlyStandardized
#print axioms independentlyReplayedScalarCLT

end

end AwesomeTheorems.Stage1.THM_M_1063.Validation
