import «Stage1_Instances».«THM-M-0082».Statement

/-!
# THM-M-0082 independent validation probe

This module reconstructs the exact frozen target directly from the pinned
mathlib declaration. It does not import or reuse the proof-phase wrapper or
the obligation-tree composition theorem.
-/

open CategoryTheory CategoryTheory.Limits

namespace Stage1Instances.THM_M_0082.Validation

open Stage1Instances.THM_M_0082

universe vC vD uC uD

/-- Independent exact-root reconstruction using the pinned terminal body. -/
theorem independentGeneralRightAdjointTarget :
    GeneralRightAdjointTarget.{vC, vD, uC, uD} := by
  intro C _ D _ G hLimits hPreserves hSolution
  letI := hLimits
  letI := hPreserves
  exact
    CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition
      G hSolution

#check independentGeneralRightAdjointTarget
#print axioms independentGeneralRightAdjointTarget

end Stage1Instances.THM_M_0082.Validation
