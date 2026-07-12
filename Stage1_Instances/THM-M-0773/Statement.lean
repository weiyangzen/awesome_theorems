import Mathlib.Order.TeichmullerTukey

/-!
# THM-M-0773: Teichmuller-Tukey statement

This module freezes the nonempty-family formulation selected at intake. It defines
and checks the proposition only; it does not prove the Teichmuller-Tukey lemma.
-/

open Set

universe u

namespace Stage1Instances.THM_M_0773

/-- A nonempty family of finite character has a member maximal under inclusion. -/
def TeichmullerTukeyTarget : Prop :=
  ∀ (alpha : Type u) (F : Set (Set alpha)),
    Order.IsOfFiniteCharacter F →
    F.Nonempty →
    ∃ m, Maximal (fun y ↦ y ∈ F) m

/-- The stronger pointed form exposed by the pinned mathlib API. -/
def PointedTarget : Prop :=
  ∀ (alpha : Type u) (F : Set (Set alpha)),
    Order.IsOfFiniteCharacter F →
    ∀ x ∈ F, ∃ m, x ⊆ m ∧ Maximal (fun y ↦ y ∈ F) m

/-- Forgetting the extension witness checks the pointed-to-unpointed transport. -/
theorem pointed_implies_unpointed :
    PointedTarget.{u} → TeichmullerTukeyTarget.{u} := by
  intro h alpha F hfinite hne
  obtain ⟨x, hx⟩ := hne
  obtain ⟨m, _hxm, hm⟩ := h alpha F hfinite x hx
  exact ⟨m, hm⟩

-- Structural mutations are elaborated and compared by `check_statement.py`.
def mutationRemovedNonempty : Prop :=
  ∀ (alpha : Type u) (F : Set (Set alpha)),
    Order.IsOfFiniteCharacter F →
    ∃ m, Maximal (fun y ↦ y ∈ F) m

def mutationChangedDomain : Prop :=
  ∀ (alpha : Type u) (F : Set (Finset alpha)),
    F.Nonempty → ∃ m, Maximal (fun y ↦ y ∈ F) m

def mutationChangedBinderScope : Prop :=
  ∀ (alpha : Type u),
    ∃ F : Set (Set alpha),
      Order.IsOfFiniteCharacter F ∧ F.Nonempty ∧
        ∃ m, Maximal (fun y ↦ y ∈ F) m

def mutationExcludedEmptyCarrier : Prop :=
  ∀ (alpha : Type u) [Nonempty alpha] (F : Set (Set alpha)),
    Order.IsOfFiniteCharacter F →
    F.Nonempty →
    ∃ m, Maximal (fun y ↦ y ∈ F) m

/-- The omitted nonemptiness hypothesis is genuinely invalid at the empty family. -/
theorem emptyFamily_boundary (alpha : Type u) :
    Order.IsOfFiniteCharacter (∅ : Set (Set alpha)) ∧
      ¬ ∃ m, Maximal (fun y ↦ y ∈ (∅ : Set (Set alpha))) m := by
  constructor
  · intro x
    constructor
    · intro hx
      exact False.elim hx
    · intro h
      exact False.elim (h ∅ (empty_subset x) finite_empty)
  · rintro ⟨m, hm⟩
    exact hm.1

/-- Empty carriers remain in scope: the singleton family containing `empty` has a maximal member. -/
theorem emptyCarrier_boundary :
    ∃ m, Maximal (fun y ↦ y ∈ ({∅} : Set (Set Empty))) m := by
  refine ⟨∅, mem_singleton ∅, ?_⟩
  intro b hb _hab
  simp at hb ⊢

end Stage1Instances.THM_M_0773

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0773.TeichmullerTukeyTarget
