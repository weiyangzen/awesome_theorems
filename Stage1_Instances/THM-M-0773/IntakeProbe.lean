import Mathlib.Order.TeichmullerTukey

open Set

#check Order.IsOfFiniteCharacter
#check Order.IsOfFiniteCharacter.exists_maximal

-- The omitted nonempty premise cannot be dismissed: the empty family has finite character.
theorem emptyFamily_isOfFiniteCharacter {alpha : Type*} :
    Order.IsOfFiniteCharacter (∅ : Set (Set alpha)) := by
  intro x
  constructor
  · intro hx
    exact False.elim hx
  · intro h
    exact False.elim (h (∅ : Set alpha) (empty_subset x) Set.finite_empty)
