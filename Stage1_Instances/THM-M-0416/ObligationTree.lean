import Statement

/-!
# THM-M-0416 conditional obligation composition

This module checks only the composition interfaces frozen by the obligation
registry. The package premises are intentionally not proved in this phase.
-/

open scoped NumberField

noncomputable section

namespace Stage1Instances.THM_M_0416.ObligationTree

universe u

open NumberField NumberField.Units

def FreePackage : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
      AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
    Module.Free ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K)

def FinitePackage : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
      AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
    Module.Finite ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K)

def RankPackage : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
      AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
    Module.finrank ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) = NumberField.Units.rank K

def CoordinatesPackage : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (x : (NumberField.RingOfIntegers K)ˣ),
    ∃! ζe : NumberField.Units.torsion K × (Fin (NumberField.Units.rank K) → ℤ),
      x = ζe.1 * ∏ i, (NumberField.Units.fundSystem K i) ^ (ζe.2 i)

/-- Checked child-to-parent composition. This is conditional, not root closure. -/
theorem root_of_packages
    (hFree : FreePackage.{u}) (hFinite : FinitePackage.{u})
    (hRank : RankPackage.{u}) (hCoordinates : CoordinatesPackage.{u}) :
    DirichletUnitTheoremTarget.{u} := by
  intro K _ _
  letI : Module ℤ (Stage1Instances.THM_M_0416.UnitsModTorsion K) :=
    AddCommGroup.toIntModule (Stage1Instances.THM_M_0416.UnitsModTorsion K)
  exact ⟨hFree K, hFinite K, hRank K, hCoordinates K⟩

#print axioms root_of_packages

end Stage1Instances.THM_M_0416.ObligationTree
