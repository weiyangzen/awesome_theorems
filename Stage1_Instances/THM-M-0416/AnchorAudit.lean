import Mathlib.NumberTheory.NumberField.Units.DirichletTheorem

/-!
# THM-M-0416 pinned mathlib anchor

This module checks an exact candidate for the frozen target. It is audit
evidence only; promotion and proof credit belong to later rev-5.6 phases.
-/

open scoped NumberField

noncomputable section

namespace Stage1Instances.THM_M_0416.AnchorAudit

universe u

open NumberField NumberField.Units

abbrev UnitsModTorsion (K : Type u) [Field K] [NumberField K] :=
  Additive ((𝓞 K)ˣ ⧸ NumberField.Units.torsion K)

/-- Exact mathlib-backed candidate for the canonical statement. -/
theorem dirichletUnitTheorem_mathlib_candidate :
    ∀ (K : Type u) [Field K] [NumberField K],
      letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
      Module.Free ℤ (UnitsModTorsion K) ∧
        Module.Finite ℤ (UnitsModTorsion K) ∧
        Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K ∧
        (∀ x : (𝓞 K)ˣ,
          ∃! ζe : NumberField.Units.torsion K × (Fin (NumberField.Units.rank K) → ℤ),
            x = ζe.1 * ∏ i, (NumberField.Units.fundSystem K i) ^ (ζe.2 i)) := by
  intro K _ _
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact ⟨inferInstance, inferInstance, NumberField.Units.rank_modTorsion K,
    NumberField.Units.exist_unique_eq_mul_prod K⟩

#check NumberField.Units.rank_modTorsion
#check NumberField.Units.exist_unique_eq_mul_prod
#print axioms NumberField.Units.rank_modTorsion
#print axioms NumberField.Units.exist_unique_eq_mul_prod
#print axioms dirichletUnitTheorem_mathlib_candidate

end Stage1Instances.THM_M_0416.AnchorAudit
