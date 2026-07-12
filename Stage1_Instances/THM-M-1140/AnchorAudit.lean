import Mathlib.Analysis.Complex.AbsMax
import Mathlib.Analysis.Complex.Harmonic.MeanValue
import Mathlib.Analysis.InnerProductSpace.Harmonic.HarmonicContOnCl

/-!
# THM-M-1140 anchor-audit probes

These checks pin the types and trust reports of the closest mathlib declarations
found by the bounded anchor search. They do not prove the target.
-/

#check InnerProductSpace.HarmonicOnNhd.continuousOn
#check InnerProductSpace.HarmonicOnNhd.neg
#check HarmonicOnNhd.circleAverage_eq
#check HarmonicContOnCl.circleAverage_eq
#check Complex.norm_eqOn_of_isPreconnected_of_isMaxOn
#check Complex.eqOn_of_isPreconnected_of_isMaxOn_norm

#print axioms InnerProductSpace.HarmonicOnNhd.continuousOn
#print axioms InnerProductSpace.HarmonicOnNhd.neg
#print axioms HarmonicOnNhd.circleAverage_eq
#print axioms HarmonicContOnCl.circleAverage_eq
#print axioms Complex.norm_eqOn_of_isPreconnected_of_isMaxOn
#print axioms Complex.eqOn_of_isPreconnected_of_isMaxOn_norm
