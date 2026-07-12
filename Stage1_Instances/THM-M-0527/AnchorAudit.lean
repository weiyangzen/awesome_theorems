import Mathlib.Topology.Covering.Quotient
import Mathlib.Topology.Homotopy.Lifting

/-!
# THM-M-0527 anchor-audit smoke test

This file checks the pinned mathlib declarations that are closest to the frozen classification
target. None has the type of the target itself.
-/

#check IsCoveringMap.monodromyFunctor
#check IsCoveringMap.injective_path_homotopic_map
#check IsCoveringMap.existsUnique_continuousMap_lifts_of_range_le
#check Subgroup.isQuotientCoveringMap

#print axioms IsCoveringMap.monodromyFunctor
#print axioms IsCoveringMap.injective_path_homotopic_map
#print axioms IsCoveringMap.existsUnique_continuousMap_lifts_of_range_le
#print axioms Subgroup.isQuotientCoveringMap
