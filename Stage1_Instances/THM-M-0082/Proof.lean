import «Stage1_Instances».«THM-M-0082».ObligationTree

/-!
# THM-M-0082: proof of the general right adjoint functor theorem target

This module integrates the terminal proof body from the pinned mathlib
`AdjointFunctorTheorems` module.  It first checks the exact typeclass-shaped
bridge frozen by the obligation registry, then uses the separately checked
explicit-hypothesis transport to prove the canonical target.
-/

open CategoryTheory CategoryTheory.Limits

namespace Stage1Instances.THM_M_0082.Proof

open Stage1Instances.THM_M_0082
open Stage1Instances.THM_M_0082.ObligationTree

universe vC vD uC uD

/-- The pinned mathlib terminal body at the exact bridge interface. -/
theorem generalRightAdjointBridge :
    GeneralRightAdjointBridge.{vC, vD, uC, uD} := by
  intro C _ D _ G _ _ hSolution
  exact
    CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition
      G hSolution

/-- The exact frozen root, obtained by composing the pinned terminal body with
the checked explicit-value to typeclass transport. -/
theorem generalRightAdjointTarget :
    GeneralRightAdjointTarget.{vC, vD, uC, uD} :=
  root_of_bridge generalRightAdjointBridge

#print axioms generalRightAdjointBridge
#print axioms generalRightAdjointTarget

end Stage1Instances.THM_M_0082.Proof
