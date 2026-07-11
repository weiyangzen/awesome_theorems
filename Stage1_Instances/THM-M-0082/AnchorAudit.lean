import Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems

/-!
# THM-M-0082: pinned anchor audit

This module checks the type boundary of the pinned mathlib candidate. It is
audit evidence only; the proof node remains downstream.
-/

open CategoryTheory CategoryTheory.Limits

namespace Stage1Instances.THM_M_0082.AnchorAudit

universe vC vD uC uD

#check CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition
#print axioms CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition

/-- The pinned candidate accepts exactly the hypotheses frozen by
`GeneralRightAdjointTarget`, including the `vD` solution-set index. -/
example (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D] (G : Functor D C)
    [HasLimits D] [PreservesLimitsOfSize.{vD, vD} G]
    (hG : SolutionSetCondition.{vD} G) : G.IsRightAdjoint :=
  CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition G hG

end Stage1Instances.THM_M_0082.AnchorAudit
