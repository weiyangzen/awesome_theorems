import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0646 pinned anchor audit

The declarations below are checked against the repository's pinned mathlib revision.  The first
two are exact or stronger upward anchors.  The final declaration is a downward theorem and is
checked only to make the direction boundary explicit.
-/

namespace Stage1Instances.THM_M_0646

open Cardinal FirstOrder

universe u v w w'

#check FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge
#check FirstOrder.Language.exists_elementaryEmbedding_card_eq
#check FirstOrder.Language.exists_elementarilyEquivalent_card_eq
#check FirstOrder.Language.exists_elementarySubstructure_card_eq

/-- Exact-type audit witness from the pinned mathlib consequence to the frozen target expression. -/
theorem pinned_exact_candidate :
    forall (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
      (kappa : Cardinal.{w}),
        aleph0 <= kappa ->
        Cardinal.lift.{w} L.card <= Cardinal.lift.{max u v} kappa ->
        Cardinal.lift.{w} #M <= Cardinal.lift.{w'} kappa ->
        exists N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = kappa := by
  intro L M _ _ kappa h0 hL _hM
  exact L.exists_elementarilyEquivalent_card_eq M kappa h0 hL

/-- The stronger elementary-extension candidate also implies the frozen target. -/
theorem pinned_extension_candidate
    (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
    (kappa : Cardinal.{w})
    (hL : Cardinal.lift.{w} L.card <= Cardinal.lift.{max u v} kappa)
    (hM : Cardinal.lift.{w} #M <= Cardinal.lift.{w'} kappa) :
    exists N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = kappa := by
  obtain ⟨N, hMN, hcard⟩ := L.exists_elementaryEmbedding_card_eq_of_ge M kappa hL hM
  exact ⟨N, hMN.some.elementarilyEquivalent, hcard⟩

end Stage1Instances.THM_M_0646

#print axioms FirstOrder.Language.exists_elementarilyEquivalent_card_eq
#print axioms FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge
#print axioms Stage1Instances.THM_M_0646.pinned_exact_candidate
#print axioms Stage1Instances.THM_M_0646.pinned_extension_candidate
