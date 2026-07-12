import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0646: obligation-tree composition probe

This module checks the exact root composition from the pinned elementary-equivalence interface.
The interface remains a premise here, so this is architecture evidence rather than proof closure.
-/

namespace Stage1Instances.THM_M_0646.ObligationTree

open Cardinal FirstOrder

universe u v w w'

def Root : Prop :=
  ∀ (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
    (κ : Cardinal.{w}),
      ℵ₀ ≤ κ →
      Cardinal.lift.{w} L.card ≤ Cardinal.lift.{max u v} κ →
      Cardinal.lift.{w} #M ≤ Cardinal.lift.{w'} κ →
      ∃ N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = κ

def PinnedEquivalenceInterface : Prop :=
  ∀ (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
    (κ : Cardinal.{w}),
      ℵ₀ ≤ κ →
      Cardinal.lift.{w} L.card ≤ Cardinal.lift.{max u v} κ →
      ∃ N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = κ

/-- Checked child-to-parent composition. The source-cardinality hypothesis is deliberately
stronger than the pinned equivalence interface requires. -/
theorem root_compose (candidate : PinnedEquivalenceInterface.{u, v, w, w'}) :
    Root.{u, v, w, w'} := by
  intro L M _ _ κ h0 hL _hM
  exact candidate L M κ h0 hL

#check FirstOrder.Language.exists_elementarilyEquivalent_card_eq
#check FirstOrder.Language.exists_elementaryEmbedding_card_eq
#check FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_le
#check FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge
#check FirstOrder.Language.exists_elementarySubstructure_card_eq
#check FirstOrder.Language.Theory.exists_large_model_of_infinite_model
#check FirstOrder.Language.ElementaryEmbedding.ofModelsElementaryDiagram
#print axioms root_compose

end Stage1Instances.THM_M_0646.ObligationTree
