import Mathlib.Order.OrderIsoNat

/-!
# THM-M-0818 discovery-only intake probe

These checks authenticate the pinned infinitary Erdos-Szekeres candidate and its index-selection
APIs. They do not choose it over the finite sharp theorem, freeze a canonical target, audit the
terminal proof body, or prove THM-M-0818.
-/

#check exists_increasing_or_nonincreasing_subseq'
#check exists_increasing_or_nonincreasing_subseq
#check Nat.orderEmbeddingOfSet
#check RelEmbedding.natLT
#check OrderEmbedding.lt_iff_lt
