import Mathlib.Data.Fintype.Pigeonhole

/-!
# THM-M-0914 discovery-only intake probe

These checks authenticate pinned finite-cardinality and pigeonhole interfaces adjacent to the
catalog claim. They do not select the canonical source encoding, freeze the dependent statement
node, audit terminal proof bodies, or prove THM-M-0914.
-/

#check Fintype.card_fin
#check Fintype.card_le_of_injective
#check Fintype.not_injective_of_card_lt
#check Fintype.exists_ne_map_eq_of_card_lt
#check Function.Embedding.isEmpty_of_card_lt

#print axioms Fintype.exists_ne_map_eq_of_card_lt
