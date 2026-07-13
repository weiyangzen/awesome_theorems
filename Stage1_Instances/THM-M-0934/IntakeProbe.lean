import Mathlib.Combinatorics.Additive.SubsetSum
import Mathlib.Combinatorics.Additive.CauchyDavenport

/- Discovery-only checks for subset-sum vocabulary and an unrestricted neighboring theorem. -/
#check Finset.subsetSum
#check Finset.mem_subsetSum_iff
#check Finset.product
#check Finset.filter
#check Finset.image
#check Finset.image₂
#check ZMod.cauchy_davenport
#check cauchy_davenport_minOrder_add
#print axioms ZMod.cauchy_davenport
