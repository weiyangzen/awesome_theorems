import ObligationTree

/-!
# THM-M-0416 proof integration

This module integrates the four frozen mathematical packages from the pinned
mathlib Dirichlet-unit-theorem surface and composes them into the exact root.
-/

open scoped NumberField

noncomputable section

namespace Stage1Instances.THM_M_0416.Proof

universe u

open NumberField NumberField.Units
open Stage1Instances.THM_M_0416.ObligationTree

/-- The pinned quotient-freeness instance closes `M0416-I-FREE`. -/
theorem freePackage_proof : FreePackage.{u} := by
  intro K _ _
  letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
    AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
  infer_instance

/-- The pinned quotient-finiteness instance closes `M0416-I-FINITE`. -/
theorem finitePackage_proof : FinitePackage.{u} := by
  intro K _ _
  letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
    AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
  infer_instance

/-- The pinned quotient-rank theorem closes `M0416-T-RANK`. -/
theorem rankPackage_proof : RankPackage.{u} := by
  intro K _ _
  letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
    AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
  exact NumberField.Units.rank_modTorsion K

/-- The pinned unique-coordinate theorem closes `M0416-T-COORDINATES`. -/
theorem coordinatesPackage_proof : CoordinatesPackage.{u} := by
  intro K _ _ x
  exact NumberField.Units.exist_unique_eq_mul_prod K x

/-- Exact proof of the frozen Dirichlet unit theorem target. -/
theorem dirichletUnitTheorem : DirichletUnitTheoremTarget.{u} :=
  root_of_packages freePackage_proof finitePackage_proof rankPackage_proof
    coordinatesPackage_proof

#print axioms freePackage_proof
#print axioms finitePackage_proof
#print axioms rankPackage_proof
#print axioms coordinatesPackage_proof
#print axioms dirichletUnitTheorem

end Stage1Instances.THM_M_0416.Proof
