import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0988: pinned anchor audit

This module independently restates the frozen target and checks its direct
bridge to the theorem in the pinned mathlib snapshot. It is audit evidence;
the later proof and validation nodes retain their own gates.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Filter Finset
open scoped Real Topology ProbabilityTheory

namespace Stage1Instances.THM_M_0988.AnchorAudit

universe u v

/-- An independently elaborated copy of the frozen statement. The audit
validator checks its material clauses against `Statement.lean`. -/
def AuditedStatementShape : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat -> Omega -> Real) (Y : Omega' -> Real),
    HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' ->
    MemLp (X 0) 2 P ->
    iIndepFun X P ->
    (forall i : Nat, IdentDistrib (X i) (X 0) P P) ->
    TendstoInDistribution
      (fun (n : Nat) (omega : Omega) =>
        (Real.sqrt (n : Real))⁻¹ *
          (∑ k ∈ Finset.range n, X k omega -
            (n : Real) * ∫ x, X 0 x ∂P))
      atTop Y (fun _ : Nat => P) P'

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check ProbabilityTheory.charFun_inv_sqrt_mul_sum
#check ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow

/-- The pinned mathlib declaration has exactly the strength required by the
frozen target, including the zero-variance branch. -/
theorem exactTarget_from_pinned_mathlib : AuditedStatementShape.{u, v} := by
  intro Omega _ Omega' _ P P' _ _ X Y hY hX hindep hident
  exact ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
    hY hX hindep hident

end Stage1Instances.THM_M_0988.AnchorAudit

#print axioms Stage1Instances.THM_M_0988.AnchorAudit.exactTarget_from_pinned_mathlib
