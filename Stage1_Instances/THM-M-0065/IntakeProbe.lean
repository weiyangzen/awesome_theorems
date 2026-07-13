import Mathlib.Order.JordanHolder

/-!
# THM-M-0065 discovery-only intake probe

These checks authenticate the pinned abstract Jordan-Holder API and a generic use. They do not
define group composition series, provide a subgroup instance, freeze the canonical group target,
or prove a repo-local THM-M-0065 wrapper.
-/

#check JordanHolderLattice
#check CompositionSeries
#check CompositionSeries.Equivalent
#check CompositionSeries.Equivalent.length_eq
#check CompositionSeries.jordan_holder

#print axioms CompositionSeries.jordan_holder

section

variable {X : Type*} [Lattice X] [JordanHolderLattice X]

example (s₁ s₂ : CompositionSeries X) (hb : s₁.head = s₂.head)
    (ht : s₁.last = s₂.last) : s₁.Equivalent s₂ :=
  CompositionSeries.jordan_holder s₁ s₂ hb ht

end
