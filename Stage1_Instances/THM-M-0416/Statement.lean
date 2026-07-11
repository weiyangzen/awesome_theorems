import Mathlib.NumberTheory.NumberField.Units.DirichletTheorem

/-!
# THM-M-0416 exact statement boundary

This module freezes the Dirichlet unit theorem target selected at intake. It
contains statement transports and mutation probes, but claims no proof of the
target.
-/

open scoped NumberField

noncomputable section

namespace Stage1Instances.THM_M_0416

universe u

open NumberField NumberField.Units

/-- The additive quotient of the units of the ring of integers by torsion. -/
abbrev UnitsModTorsion (K : Type u) [Field K] [NumberField K] :=
  Additive ((𝓞 K)ˣ ⧸ NumberField.Units.torsion K)

/-- The exact target selected at intake for Dirichlet's unit theorem. -/
def DirichletUnitTheoremTarget : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Free ℤ (UnitsModTorsion K) ∧
      Module.Finite ℤ (UnitsModTorsion K) ∧
      Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K ∧
      (∀ x : (𝓞 K)ˣ,
        ∃! ζe : NumberField.Units.torsion K × (Fin (NumberField.Units.rank K) → ℤ),
          x = ζe.1 * ∏ i, (NumberField.Units.fundSystem K i) ^ (ζe.2 i))

/-- Direct local restatement of the historical candidate's `StatementShape`. -/
def PinnedCandidateSourceShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Free ℤ (UnitsModTorsion K) ∧
      Module.Finite ℤ (UnitsModTorsion K) ∧
      Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K ∧
      (∀ x : (𝓞 K)ˣ,
        ∃! ζe : NumberField.Units.torsion K × (Fin (NumberField.Units.rank K) → ℤ),
          x = ζe.1 * ∏ i, (NumberField.Units.fundSystem K i) ^ (ζe.2 i))

/-- Checked statement identity with the historical candidate shape. -/
theorem target_iff_pinnedCandidateSourceShape :
    DirichletUnitTheoremTarget.{u} ↔ PinnedCandidateSourceShape.{u} := by
  rfl

/- Structural mutations. The validator confirms that neither serializes to
the canonical target. -/

/-- Mutation specializing the arbitrary number field to `ℚ`. -/
def mutationChangedDomain : Prop :=
  letI : Module ℤ (UnitsModTorsion ℚ) := AddCommGroup.toIntModule (UnitsModTorsion ℚ)
  Module.Free ℤ (UnitsModTorsion ℚ) ∧
    Module.Finite ℤ (UnitsModTorsion ℚ) ∧
    Module.finrank ℤ (UnitsModTorsion ℚ) = NumberField.Units.rank ℚ ∧
    (∀ x : (𝓞 ℚ)ˣ,
      ∃! ζe : NumberField.Units.torsion ℚ × (Fin (NumberField.Units.rank ℚ) → ℤ),
        x = ζe.1 * ∏ i, (NumberField.Units.fundSystem ℚ i) ^ (ζe.2 i))

/-- Mutation changing the outer field binder from universal to existential. -/
def mutationChangedBinderScope : Prop :=
  ∃ (K : Type u), ∃ (_f : Field K), ∃ (_nf : NumberField K), True

/-- Boundary mutation excluding all unit-rank-zero number fields. -/
def mutationExcludesRankZero : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    0 < NumberField.Units.rank K ∧
      (letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
       Module.Free ℤ (UnitsModTorsion K) ∧
        Module.Finite ℤ (UnitsModTorsion K) ∧
        Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K)

/-- Rank-zero/empty-product boundary specialization. No exclusion is added. -/
def RationalBoundaryTarget : Prop := mutationChangedDomain

end Stage1Instances.THM_M_0416

set_option pp.explicit true in
#print Stage1Instances.THM_M_0416.DirichletUnitTheoremTarget
