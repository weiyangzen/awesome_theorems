import Mathlib.Combinatorics.Enumerative.InclusionExclusion
import Mathlib.Data.Finset.CastCard

/-!
# THM-M-0913 discovery-only intake probe

These commands authenticate the pinned finite-family inclusion-exclusion interfaces that are
adjacent to the catalog phrase "cardinality formula for the elements of a union". This file does
not select a canonical proposition, declare a theorem, or provide proof credit.
-/

#check Finset.indicator_biUnion_eq_sum_powerset
#check Finset.inclusion_exclusion_sum_biUnion
#check Finset.inclusion_exclusion_card_biUnion
#check Finset.inclusion_exclusion_sum_inf_compl
#check Finset.inclusion_exclusion_card_inf_compl
#check Finset.cast_card_union

#print axioms Finset.inclusion_exclusion_card_biUnion
#print axioms Finset.cast_card_union
