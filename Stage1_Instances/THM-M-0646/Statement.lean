import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0646: exact upward Loewenheim-Skolem statement

This module freezes the repository's elementary-equivalence wording. It states a proposition and
checks its relationship to the pinned mathlib declaration; it does not claim a new proof body.
-/

namespace Stage1Instances.THM_M_0646

open Cardinal FirstOrder

universe u v w w'

/--
Every infinite structure for `L` has an elementarily equivalent model of every infinite cardinal
large enough to carry the language. This is the direct formal reading of "infinite models have
arbitrarily large elementarily equivalent models".
-/
def LoewenheimSkolemTarget : Prop :=
  ∀ (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
    (κ : Cardinal.{w}),
      ℵ₀ ≤ κ →
      Cardinal.lift.{w} L.card ≤ Cardinal.lift.{max u v} κ →
      Cardinal.lift.{w} #M ≤ Cardinal.lift.{w'} κ →
      ∃ N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = κ

/-- Checked implication from mathlib's direct equivalence theorem to the upward target. -/
theorem pinned_mathlib_implies_target : LoewenheimSkolemTarget.{u, v, w, w'} := by
  intro L M _ _ κ h0 hL _hM
  exact L.exists_elementarilyEquivalent_card_eq M κ h0 hL

/-- Checked implication from mathlib's stronger upward elementary-embedding form. -/
theorem elementaryExtension_implies_target
    (L : Language.{u, v}) (M : Type w') [L.Structure M] [Infinite M]
    (κ : Cardinal.{w})
    (hL : Cardinal.lift.{w} L.card ≤ Cardinal.lift.{max u v} κ)
    (hM : Cardinal.lift.{w} #M ≤ Cardinal.lift.{w'} κ) :
    ∃ N : CategoryTheory.Bundled L.Structure, (M ≅[L] N) ∧ #N = κ := by
  obtain ⟨N, hMN, hcard⟩ := L.exists_elementaryEmbedding_card_eq_of_ge M κ hL hM
  exact ⟨N, hMN.some.elementarilyEquivalent, hcard⟩

end Stage1Instances.THM_M_0646

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0646.LoewenheimSkolemTarget
