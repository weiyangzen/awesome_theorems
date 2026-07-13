import Mathlib.Combinatorics.Additive.CauchyDavenport
import Mathlib.Combinatorics.Additive.SubsetSum
import Mathlib.Data.Finset.Powerset

/-!
# THM-M-0935 discovery-only intake probe

These checks authenticate pinned APIs adjacent to a possible restricted fixed-cardinality sumset
encoding. They do not select the general h-fold theorem or its h = 2 specialization, define the
canonical target, or prove the Dias da Silva-Hamidoune theorem.
-/

#check Finset.powersetCard
#check Finset.mem_powersetCard
#check Finset.card_powersetCard
#check Finset.sum
#check Finset.image
#check Finset.card_image_le
#check Finset.subsetSum
#check Finset.mem_subsetSum_iff
#check ZMod
#check ZMod.cauchy_davenport
