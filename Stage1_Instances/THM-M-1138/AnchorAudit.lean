import Mathlib.Analysis.InnerProductSpace.Harmonic.HarmonicContOnCl
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Topology.Order.Compact
import Mathlib.Analysis.Complex.AbsMax
import Mathlib.Analysis.Complex.Harmonic.MeanValue

/-!
# THM-M-1138 anchor-audit elaboration probes

This file checks the types of the closest declarations found at the pinned
mathlib revision. It deliberately contains no proof of the target.
-/

#check InnerProductSpace.HarmonicContOnCl
#check InnerProductSpace.HarmonicContOnCl.harmonicOnNhd
#check InnerProductSpace.HarmonicContOnCl.continuousOn
#check IsCompact.exists_isMaxOn
#check Complex.exists_mem_frontier_isMaxOn_norm
#check HarmonicContOnCl.circleAverage_eq

#print axioms InnerProductSpace.HarmonicContOnCl.continuousOn
#print axioms IsCompact.exists_isMaxOn
#print axioms Complex.exists_mem_frontier_isMaxOn_norm
#print axioms HarmonicContOnCl.circleAverage_eq
