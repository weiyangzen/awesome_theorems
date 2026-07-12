import Mathlib.Data.Finset.Pairwise
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Nat.ModEq

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0898 catalog wording.

These declarations do not define a Steiner triple system, a resolution, or a Kirkman schedule and
do not state any existence theorem. They supply no statement or proof credit.
-/

#check Finset.powersetCard
#check Finset.mem_powersetCard
#check Finset.card_powersetCard
#check Set.Pairwise
#check Set.PairwiseDisjoint
#check Finset.card
#check Nat.ModEq
