import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0988 independent validation probe

This module does not import `Proof.lean` or `ObligationTree.lean`. It independently
reconstructs the frozen statement root from the pinned mathlib declaration.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Filter Finset
open scoped Real Topology ProbabilityTheory

namespace Stage1Instances.THM_M_0988.Validation

universe u v

/-- An independently written direct reconstruction of the exact frozen root. -/
theorem independentlyReconstructedRoot :
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
            ((∑ k ∈ Finset.range n, X k omega) -
              (n : Real) * ∫ x, X 0 x ∂P))
        atTop Y (fun _ : Nat => P) P' := by
  intro Omega _ Omega' _ P P' _ _ X Y hLaw hMoment hIndependent hIdentDistrib
  exact ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
    hLaw hMoment hIndependent hIdentDistrib

#print axioms independentlyReconstructedRoot
#print axioms ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub

end Stage1Instances.THM_M_0988.Validation
