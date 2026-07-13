import Mathlib.Data.Fintype.BigOperators
import Mathlib.InformationTheory.Hamming

/-!
# THM-M-1587 discovery-only intake probe

These checks authenticate pinned Hamming-space and finite-cardinality interfaces adjacent to a
possible future Singleton-bound encoding. They do not define a code or minimum distance, select a
general or linear Singleton proposition, define MDS, or prove THM-M-1587.
-/

#check hammingDist
#check hammingDist_eq_zero
#check hammingDist_le_card_fintype
#check hammingDist_comp_le_hammingDist
#check Fintype.card_fun
#check Fintype.card_le_of_injective
#check Fintype.card_congr
#check Finite.of_injective
