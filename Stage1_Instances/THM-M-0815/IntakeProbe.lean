import Mathlib.Combinatorics.SimpleGraph.Hall

/-!
# THM-M-0815 discovery-only intake probe

These checks authenticate pinned Hall-marriage interfaces in indexed-family, relation, and
bipartite-graph forms. This file does not select a canonical proposition or prove a new target.
In particular, the graph-wide perfect-matching interface has a stronger, differently scoped
neighborhood premise than the standard condition for a matching saturating one bipartition.
-/

#check Finset.all_card_le_biUnion_card_iff_existsInjective'
#check Finset.all_card_le_biUnion_card_iff_exists_injective
#check Fintype.all_card_le_rel_image_card_iff_exists_injective
#check Fintype.all_card_le_filter_rel_iff_exists_injective
#check SimpleGraph.exists_isMatching_of_forall_ncard_le
#check SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
#print SimpleGraph.IsBipartiteWith
#check SimpleGraph.Subgraph.isPerfectMatching_iff
#check Set.Infinite.ncard

#print axioms Finset.all_card_le_biUnion_card_iff_existsInjective'
#print axioms Finset.all_card_le_biUnion_card_iff_exists_injective
#print axioms SimpleGraph.exists_isMatching_of_forall_ncard_le
#print axioms SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
