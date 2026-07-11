import Statement

/-!
# THM-M-0416 independent kernel-validation probe

This module reconstructs the exact frozen root directly from the pinned
mathlib declarations.  It deliberately does not import `Proof.lean` or
`ObligationTree.lean`.
-/

open scoped NumberField

noncomputable section

namespace Stage1Instances.THM_M_0416.Validation

universe u

open NumberField NumberField.Units

/-- An independently implemented proof of the exact frozen target. -/
theorem independentDirichletUnitTheorem :
    Stage1Instances.THM_M_0416.DirichletUnitTheoremTarget.{u} := by
  intro K _ _
  letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
    AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
  exact ⟨inferInstance, inferInstance, NumberField.Units.rank_modTorsion K,
    NumberField.Units.exist_unique_eq_mul_prod K⟩

#check independentDirichletUnitTheorem
#print axioms independentDirichletUnitTheorem

end Stage1Instances.THM_M_0416.Validation
