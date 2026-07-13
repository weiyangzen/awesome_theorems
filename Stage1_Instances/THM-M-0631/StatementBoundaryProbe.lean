import Mathlib.Topology.Baire.CompleteMetrizable

/-!
# THM-M-0631 statement-boundary probe

This file checks the empty-space distinction that blocks selection of the canonical statement.
It does not select a target, certify minimal imports for a target, or supply theorem proof credit.
-/

open Set

#check BaireSpace.of_completelyPseudoMetrizable
#check BaireSpace.baire_property
#check not_isMeagre_of_isOpen
#check IsMeagre.empty
#check nonempty_of_not_isMeagre

#synth MetricSpace Empty
#synth CompleteSpace Empty
#synth TopologicalSpace.IsCompletelyMetrizableSpace Empty
#synth BaireSpace Empty

example : IsMeagre (univ : Set Empty) := by
  rw [univ_eq_empty_iff.mpr inferInstance]
  exact IsMeagre.empty

example {X : Type*} [MetricSpace X] [CompleteSpace X] :
    Not (IsMeagre (univ : Set X)) ↔ Nonempty X := by
  constructor
  · intro h
    rcases nonempty_of_not_isMeagre h with ⟨x, _⟩
    exact ⟨x⟩
  · intro h
    letI : Nonempty X := h
    exact not_isMeagre_of_isOpen isOpen_univ univ_nonempty
