import Statement

/-!
# THM-M-0086 proof execution

This module installs the three exact terminal bodies identified by the pinned-anchor audit and
composes them into the canonical three-branch target frozen in `Statement.lean`.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits
open CategoryTheory.Abelian

universe v u

namespace Stage1Instances.THM_M_0086.Proof

open Stage1Instances.THM_M_0086

/-- The pinned Freyd-Mitchell terminal theorem at the frozen embedding interface. -/
theorem embeddingBranch
    (C : Type u) [Category.{v} C] [Abelian C] : EmbeddingBranch C := by
  exact CategoryTheory.Abelian.freyd_mitchell C

/-- The pinned injective-coseparator theorem at the frozen universally quantified interface. -/
theorem injectiveBranch
    (C : Type u) [Category.{v} C] [Abelian C] : InjectiveBranch C := by
  intro _ _ G hG
  exact CategoryTheory.Abelian.has_injective_coseparator G hG

/-- The pinned opposite-category dual theorem at the frozen projective interface. -/
theorem projectiveBranch
    (C : Type u) [Category.{v} C] [Abelian C] : ProjectiveBranch C := by
  intro _ _ G hG
  exact CategoryTheory.Abelian.has_projective_separator G hG

/-- The exact canonical package, with all three frozen branch obligations composed. -/
theorem freydTheoremPackage : CanonicalStatement.{v, u} := by
  intro C _ _
  exact ⟨embeddingBranch C, injectiveBranch C, projectiveBranch C⟩

#print axioms embeddingBranch
#print axioms injectiveBranch
#print axioms projectiveBranch
#print axioms freydTheoremPackage

end Stage1Instances.THM_M_0086.Proof
