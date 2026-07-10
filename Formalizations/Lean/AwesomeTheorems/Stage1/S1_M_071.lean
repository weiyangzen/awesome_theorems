import Mathlib.NumberTheory.NumberField.Units.DirichletTheorem

/-!
# S1-M-071 / THM-M-0416: Dirichlet's unit theorem

This Stage1 artifact records a repo-local Lean 4 wrapper for the pinned mathlib
formalization of Dirichlet's unit theorem for number fields.

The proof body is supplied by
`Mathlib.NumberTheory.NumberField.Units.DirichletTheorem`.
-/

open scoped NumberField

noncomputable section

namespace AwesomeTheorems.Stage1.S1_M_071

universe u

open NumberField NumberField.Units

/-- Audit identifier for the source theorem. -/
def theoremUID : String := "THM-M-0416"

/-- Current repo-local machine state for this Stage1 artifact. -/
def machineProofStatus : String := "local_wrapper_upstream_mathlib"

/--
Current machine-proof debt classification for this Stage1 artifact.

The terminal proof body is supplied by pinned mathlib; this local module
checks wrappers and the normalized `StatementShape` against that dependency.
-/
def machineProofDebt : String := "none_for_checked_mathlib_wrapper"

/-- This artifact retains no repo-local integration debt. -/
def repoLocalIntegrationDebtRetained : Bool := false

/-- The additive quotient of the unit group by its torsion subgroup. -/
abbrev UnitsModTorsion (K : Type u) [Field K] [NumberField K] :=
  Additive ((𝓞 K)ˣ ⧸ NumberField.Units.torsion K)

/--
Stage1 normalized statement shape for Dirichlet's unit theorem.

For every number field `K`, the quotient of the unit group of `𝓞 K` by torsion
is a finite free `ℤ`-module of rank `# InfinitePlace K - 1`, and every unit has
a unique expression as a torsion unit times powers of a chosen fundamental
system of units.
-/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Free ℤ (UnitsModTorsion K) ∧
      Module.Finite ℤ (UnitsModTorsion K) ∧
      Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K ∧
      (∀ x : (𝓞 K)ˣ,
        ∃! ζe : NumberField.Units.torsion K × (Fin (NumberField.Units.rank K) → ℤ),
          x = ζe.1 * ∏ i, (NumberField.Units.fundSystem K i) ^ (ζe.2 i))

/-- mathlib wrapper: the unit group modulo torsion is free over `ℤ`. -/
theorem units_mod_torsion_free (K : Type u) [Field K] [NumberField K] :
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Free ℤ (UnitsModTorsion K) := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact inferInstance

/-- mathlib wrapper: the unit group modulo torsion is finite over `ℤ`. -/
theorem units_mod_torsion_finite (K : Type u) [Field K] [NumberField K] :
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Finite ℤ (UnitsModTorsion K) := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact inferInstance

/-- mathlib wrapper: the rank of units modulo torsion is `# InfinitePlace K - 1`. -/
theorem units_rank_modTorsion (K : Type u) [Field K] [NumberField K] :
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact NumberField.Units.rank_modTorsion K

namespace P3

/--
Public theorem-tree child `S1-M-071.P3.free_rank_quotient`: the quotient of
the unit group by torsion is a finite free `ℤ`-module of rank
`NumberField.Units.rank K`.
-/
theorem free_rank_quotient (K : Type u) [Field K] [NumberField K] :
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Free ℤ (UnitsModTorsion K) ∧
      Module.Finite ℤ (UnitsModTorsion K) ∧
      Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact ⟨units_mod_torsion_free K, units_mod_torsion_finite K,
    units_rank_modTorsion K⟩

end P3

/--
mathlib wrapper: each unit is uniquely a torsion unit times powers of the
fundamental system of units.
-/
theorem dirichletUnitTheorem_decomposition (K : Type u) [Field K] [NumberField K]
    (x : (𝓞 K)ˣ) :
    ∃! ζe : NumberField.Units.torsion K × (Fin (NumberField.Units.rank K) → ℤ),
      x = ζe.1 * ∏ i, (NumberField.Units.fundSystem K i) ^ (ζe.2 i) :=
  NumberField.Units.exist_unique_eq_mul_prod K x

namespace P4

/--
Public theorem-tree child `S1-M-071.P4.unique_decomposition`: each unit is
uniquely a torsion unit times integral powers of the fundamental system of
units.
-/
theorem unique_decomposition (K : Type u) [Field K] [NumberField K] (x : (𝓞 K)ˣ) :
    ∃! ζe : NumberField.Units.torsion K × (Fin (NumberField.Units.rank K) → ℤ),
      x = ζe.1 * ∏ i, (NumberField.Units.fundSystem K i) ^ (ζe.2 i) :=
  dirichletUnitTheorem_decomposition K x

end P4

/-- mathlib wrapper: the full unit group is finitely generated as a monoid. -/
theorem units_monoid_fg (K : Type u) [Field K] [NumberField K] : Monoid.FG (𝓞 K)ˣ :=
  inferInstance

/-- mathlib wrapper: the torsion subgroup of units is cyclic. -/
theorem torsion_cyclic (K : Type u) [Field K] [NumberField K] :
    IsCyclic (NumberField.Units.torsion K) :=
  inferInstance

/--
mathlib wrapper: the fundamental system of units together with torsion generates
the full unit group.
-/
theorem closure_fundSystem_sup_torsion_eq_top (K : Type u) [Field K] [NumberField K] :
    Subgroup.closure (Set.range (NumberField.Units.fundSystem K)) ⊔
        NumberField.Units.torsion K = ⊤ :=
  NumberField.Units.closure_fundSystem_sup_torsion_eq_top K

namespace P5

/--
Public theorem-tree child `S1-M-071.P5.group_generation_and_torsion`: the unit
group is finitely generated, its torsion subgroup is cyclic, and the
fundamental system of units together with torsion generates the full unit group.
-/
theorem group_generation_and_torsion (K : Type u) [Field K] [NumberField K] :
    Monoid.FG (𝓞 K)ˣ ∧
      IsCyclic (NumberField.Units.torsion K) ∧
      Subgroup.closure (Set.range (NumberField.Units.fundSystem K)) ⊔
        NumberField.Units.torsion K = ⊤ := by
  exact ⟨units_monoid_fg K, torsion_cyclic K,
    closure_fundSystem_sup_torsion_eq_top K⟩

end P5

/-- mathlib modules checked for the repo-local Dirichlet-unit-theorem wrapper. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.NumberField.Units.DirichletTheorem"
]

/-- Pinned mathlib declarations used by the checked wrappers in this file. -/
def mathlibAnchorNames : List String := [
  "NumberField.Units.torsion",
  "NumberField.Units.rank",
  "NumberField.Units.fundSystem",
  "NumberField.Units.rank_modTorsion",
  "NumberField.Units.exist_unique_eq_mul_prod",
  "NumberField.Units.closure_fundSystem_sup_torsion_eq_top",
  "Monoid.FG (𝓞 K)ˣ",
  "IsCyclic (NumberField.Units.torsion K)"
]

/-- Lake-pinned mathlib revision observed by the 2026-04-30 repair pass. -/
def pinnedMathlibRevision : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- The Stage1 statement shape is closed by pinned mathlib. -/
theorem statementShape_mathlib : StatementShape := by
  intro K _ _
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact ⟨units_mod_torsion_free K, units_mod_torsion_finite K,
    units_rank_modTorsion K, dirichletUnitTheorem_decomposition K⟩

/-! ## Audit probes -/

#check NumberField.Units.torsion
#check NumberField.Units.rank
#check NumberField.Units.fundSystem
#check NumberField.Units.rank_modTorsion
#check NumberField.Units.exist_unique_eq_mul_prod
#check NumberField.Units.closure_fundSystem_sup_torsion_eq_top
#check units_mod_torsion_free
#check units_rank_modTorsion
#check P3.free_rank_quotient
#check dirichletUnitTheorem_decomposition
#check P4.unique_decomposition
#check P5.group_generation_and_torsion
#check statementShape_mathlib

end AwesomeTheorems.Stage1.S1_M_071
