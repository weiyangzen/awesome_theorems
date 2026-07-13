import Mathlib.Combinatorics.SetFamily.LYM

/-!
# THM-M-0821 anchor-audit candidate

This module checks the exact frozen maximum-value claim through the pinned
mathlib upper bound and the lower-middle-layer witness. The theorem is
candidate evidence for the anchor-audit node. It is not an accepted proof-phase
declaration or a theorem-completion receipt.
-/

namespace Stage1Instances.THM_M_0821

universe u

def IsSpernerFamily {alpha : Type u} (A : Finset (Finset alpha)) : Prop :=
  IsAntichain (fun x y : Finset alpha => x ⊆ y) (A : Set (Finset alpha))

def SpernerMaximumTarget : Prop :=
  ∀ (alpha : Type u) [Fintype alpha],
    (∃ A : Finset (Finset alpha),
      IsSpernerFamily A ∧
        A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)) ∧
      ∀ A : Finset (Finset alpha),
        IsSpernerFamily A →
          A.card ≤ Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-! The two declarations above are a standalone literal fixture for the
statement-phase declarations. The checker requires the serialized expression
to equal the frozen statement fingerprint. The dossier path cannot be imported
as a Lean module because its directory name contains hyphens. -/

/-- Exact pinned-mathlib candidate for the full attainability-plus-bound target. -/
theorem spernerMaximum_mathlib_candidate : SpernerMaximumTarget.{u} := by
  intro alpha _
  let middle : Finset (Finset alpha) :=
    Finset.powersetCard (Fintype.card alpha / 2) Finset.univ
  refine ⟨⟨middle, ?_, ?_⟩, ?_⟩
  · simp [IsSpernerFamily, middle]
    exact
      (Set.sized_powersetCard (Finset.univ : Finset alpha)
        (Fintype.card alpha / 2)).isAntichain
  · simp [middle, Finset.card_powersetCard]
  · intro A hA
    exact hA.sperner

#check IsAntichain.sperner
#check Set.sized_powersetCard
#check Set.Sized.isAntichain
#check Finset.card_powersetCard

#print IsAntichain.sperner
#print axioms IsAntichain.sperner
#print axioms Set.Sized.isAntichain
#print axioms Finset.card_powersetCard
#print axioms spernerMaximum_mathlib_candidate

set_option pp.explicit true in
set_option pp.universes true in
#print SpernerMaximumTarget

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0821.spernerMaximum_mathlib_candidate

end Stage1Instances.THM_M_0821
