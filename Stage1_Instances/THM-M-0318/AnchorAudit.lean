import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.Topology.Order.IntermediateValue

/-!
# THM-M-0318 anchor audit probes

These commands check the strongest nearby declarations found in the pinned
mathlib revision. Both require materially stronger or narrower hypotheses than
the frozen Schauder target, so neither is root proof evidence.
-/

#check ContractingWith.exists_fixedPoint'
#check exists_mem_Icc_isFixedPt_of_mapsTo

#print axioms ContractingWith.exists_fixedPoint'
#print axioms exists_mem_Icc_isFixedPt_of_mapsTo
