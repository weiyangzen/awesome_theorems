import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0646 independent validation probe

This module intentionally does not import the local statement or proof modules. It reconstructs
the frozen root type and closes it directly with the pinned mathlib declaration, providing a
second elaboration route for narrow validation. It is not a distinct-runner attestation.
-/

namespace Stage1Instances.THM_M_0646.Validation

open Cardinal FirstOrder

universe u v w w'

def Root : Prop :=
  ∀ (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
    (κ : Cardinal.{w}),
      ℵ₀ ≤ κ →
      Cardinal.lift.{w} L.card ≤ Cardinal.lift.{max u v} κ →
      Cardinal.lift.{w} #M ≤ Cardinal.lift.{w'} κ →
      ∃ N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = κ

theorem independentRoot : Root.{u, v, w, w'} := by
  intro L M _ _ κ hInfiniteCardinal hLanguageCardinal _hSourceCardinal
  exact L.exists_elementarilyEquivalent_card_eq M κ
    hInfiniteCardinal hLanguageCardinal

theorem independentRootExactType :
    ∀ (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
      (κ : Cardinal.{w}),
        ℵ₀ ≤ κ →
        Cardinal.lift.{w} L.card ≤ Cardinal.lift.{max u v} κ →
        Cardinal.lift.{w} #M ≤ Cardinal.lift.{w'} κ →
        ∃ N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = κ :=
  independentRoot

#check FirstOrder.Language.exists_elementarilyEquivalent_card_eq
#print axioms FirstOrder.Language.exists_elementarilyEquivalent_card_eq
#print axioms independentRoot

end Stage1Instances.THM_M_0646.Validation
