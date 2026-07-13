import Mathlib.Data.Finset.Max
import Mathlib.Dynamics.FixedPoints.Topology
import Mathlib.Topology.MetricSpace.Contracting

/-!
# THM-M-1483 discovery-only intake probe

These checks authenticate pinned finite-minimum, fixed-point, and contraction-iteration interfaces
adjacent to possible particle-swarm models. They do not define a particle, swarm, velocity update,
personal or neighborhood best, random model, objective, PSO algorithm, or PSO theorem.
-/

#check Finset.exists_min_image
#check Function.IsFixedPt
#check isFixedPt_of_tendsto_iterate
#check ContractingWith.fixedPoint_isFixedPt
#check ContractingWith.tendsto_iterate_fixedPoint

#print axioms Finset.exists_min_image
#print axioms isFixedPt_of_tendsto_iterate
#print axioms ContractingWith.tendsto_iterate_fixedPoint
