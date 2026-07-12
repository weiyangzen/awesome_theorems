import Mathlib.Data.Fintype.BigOperators
import Mathlib.InformationTheory.Hamming

/-!
# THM-M-1588 discovery-only intake probe

These checks authenticate pinned finite Hamming-space and cardinality interfaces adjacent to a
possible future Gilbert-Varshamov encoding. They do not define a code-size extremal function,
select a finite, linear, or asymptotic catalog proposition, or prove THM-M-1588.
-/

#check hammingDist
#check hammingDist_triangle
#check hammingDist_le_card_fintype
#check Hamming
#check Hamming.dist_eq_hammingDist
#check Fintype.card_fun
#check Nat.choose
#check Finset.exists_max_image
