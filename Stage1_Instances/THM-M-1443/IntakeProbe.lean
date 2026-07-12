import Mathlib.Dynamics.FixedPoints.Topology
import Mathlib.Topology.MetricSpace.Contracting

/-!
# THM-M-1443 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to possible future fixed-point iteration
statements. They do not select a catalog proposition, connect an equation root to a fixed point, or
prove THM-M-1443.
-/

#check Function.iterate_succ_apply
#check Function.IsFixedPt
#check isFixedPt_of_tendsto_iterate
#check ContractingWith
#check ContractingWith.exists_fixedPoint
#check ContractingWith.fixedPoint_isFixedPt
#check ContractingWith.tendsto_iterate_fixedPoint
#check ContractingWith.apriori_dist_iterate_fixedPoint_le
#check ContractingWith.aposteriori_dist_iterate_fixedPoint_le
