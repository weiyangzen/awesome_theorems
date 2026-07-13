import Mathlib.Data.Finset.Pairwise
import Mathlib.Data.Finset.Slice

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0968 catalog wording.

These declarations can encode uniform finite set families and pairwise-disjoint members. They do
not select or state an Erdős matching theorem and supply no statement or proof credit.
-/

#check Set.Sized
#check Set.Sized.card_le
#check Finset.powersetCard
#check Finset.mem_powersetCard
#check Set.PairwiseDisjoint
#check Disjoint
#check Finset.card
