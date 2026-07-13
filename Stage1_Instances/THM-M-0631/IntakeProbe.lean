import Mathlib.Topology.Baire.CompleteMetrizable

/-!
# THM-M-0631 discovery-only intake probe

These checks authenticate pinned complete-metrizability and Baire-category interfaces. They do not
select a canonical interpretation of "second category", establish a source transport, or prove the
repository target.
-/

#check BaireSpace
#check BaireSpace.baire_property
#check BaireSpace.of_completelyPseudoMetrizable
#check TopologicalSpace.IsCompletelyPseudoMetrizableSpace
#check TopologicalSpace.IsCompletelyMetrizableSpace
#check dense_iInter_of_isOpen_nat
#check not_isMeagre_of_isOpen
#check IsMeagre
#check IsMeagre.empty
#check isMeagre_iff_countable_union_isNowhereDense
#check nonempty_of_not_isMeagre

#synth BaireSpace Empty
example : IsMeagre (Set.univ : Set Empty) := by
  rw [Set.univ_eq_empty_iff.mpr inferInstance]
  exact IsMeagre.empty

#print axioms BaireSpace.of_completelyPseudoMetrizable
