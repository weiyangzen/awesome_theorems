import Mathlib.Order.TeichmullerTukey

/-!
# THM-M-0773 pinned anchor probe

This narrow wrapper checks that the pinned mathlib declaration closes the exact
statement frozen in `Statement.lean`. It adds no proof body beyond selecting a
member of the nonempty family and forgetting the extension witness.
-/

open Set

universe u

namespace Stage1Instances.THM_M_0773

/-- Exact-root wrapper around the pinned pointed Teichmuller-Tukey theorem. -/
theorem target_of_mathlib :
    ∀ (alpha : Type u) (F : Set (Set alpha)),
      Order.IsOfFiniteCharacter F →
      F.Nonempty →
      ∃ m, Maximal (fun y ↦ y ∈ F) m := by
  intro alpha F hfinite hne
  obtain ⟨x, hx⟩ := hne
  obtain ⟨m, _hxm, hm⟩ := hfinite.exists_maximal hx
  exact ⟨m, hm⟩

end Stage1Instances.THM_M_0773

#check Order.IsOfFiniteCharacter.exists_maximal
#check Stage1Instances.THM_M_0773.target_of_mathlib
#print axioms Order.IsOfFiniteCharacter.exists_maximal
#print axioms Stage1Instances.THM_M_0773.target_of_mathlib
