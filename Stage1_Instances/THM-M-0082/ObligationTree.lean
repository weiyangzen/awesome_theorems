import «Stage1_Instances».«THM-M-0082».Statement

/-!
# THM-M-0082: obligation-tree composition harness

This module checks only the child-to-root composition frozen by the obligation
registry.  The central bridge remains an explicit premise; this file does not
invoke or prove the adjoint functor theorem.
-/

open CategoryTheory CategoryTheory.Limits

namespace Stage1Instances.THM_M_0082.ObligationTree

universe vC vD uC uD

/-- Exact type of the external bridge isolated by the frozen architecture. -/
def GeneralRightAdjointBridge : Prop :=
  ∀ (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D] (G : Functor D C)
    [HasLimits D] [PreservesLimitsOfSize.{vD, vD} G],
      SolutionSetCondition.{vD} G → G.IsRightAdjoint

/-- Checked composition from the exact bridge interface to the explicit-value
canonical root.  The bridge is deliberately consumed as a hypothesis. -/
theorem root_of_bridge
    (hBridge : GeneralRightAdjointBridge.{vC, vD, uC, uD}) :
    GeneralRightAdjointTarget.{vC, vD, uC, uD} := by
  intro C _ D _ G hLimits hPreserves hSolution
  letI := hLimits
  letI := hPreserves
  exact hBridge C D G hSolution

end Stage1Instances.THM_M_0082.ObligationTree

#print axioms Stage1Instances.THM_M_0082.ObligationTree.root_of_bridge
