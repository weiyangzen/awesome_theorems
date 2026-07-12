import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0987 pinned anchor audit

This file checks the exact mathlib candidate selected by the statement phase.
It is candidate evidence only; the canonical target remains unproved until the
separate proof and validation phases accept a wrapper and its trust closure.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Finset
open scoped Real Topology

namespace Stage1Instances.THM_M_0987.AnchorAudit

universe uOmega uOmega'

/-- An exact-type audit probe for the pinned mathlib CLT declaration. -/
theorem pinnedMathlibCandidate
    (Omega : Type uOmega) (Omega' : Type uOmega')
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat -> Omega -> Real) (Y : Omega' -> Real)
    (hY : HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P')
    (hX : MemLp (X 0) 2 P)
    (hindep : iIndepFun X P)
    (hident : forall i : Nat, IdentDistrib (X i) (X 0) P P) :
    TendstoInDistribution
      (fun (n : Nat) omega =>
        (Real.sqrt (n : Real))⁻¹ *
          ((∑ k ∈ Finset.range n, X k omega) - (n : Real) * P[X 0]))
      atTop Y (fun _ : Nat => P) P' := by
  exact ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
    hY hX hindep hident

end Stage1Instances.THM_M_0987.AnchorAudit

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.charFun_inv_sqrt_mul_sum
#check ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow
#check MeasureTheory.taylor_charFun_two
#check MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun
#check ProbabilityTheory.charFun_gaussianReal

#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#print axioms Stage1Instances.THM_M_0987.AnchorAudit.pinnedMathlibCandidate
