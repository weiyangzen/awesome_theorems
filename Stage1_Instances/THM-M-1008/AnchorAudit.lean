import Mathlib.Probability.Independence.ZeroOne
import Mathlib.Probability.IdentDistribIndep

/-!
# THM-M-1008 anchor-audit probes

The declarations below are checked proof-route anchors. None states the
finite-permutation-invariant iid root frozen in `Statement.lean`.
-/

open MeasureTheory ProbabilityTheory

#check ProbabilityTheory.iIndepFun.precomp
#check ProbabilityTheory.IdentDistrib.pi
#check ProbabilityTheory.IdentDistrib.measure_preimage_eq
#check ProbabilityTheory.measure_eq_zero_or_one_of_indepSet_self
#check ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop

#print axioms ProbabilityTheory.IdentDistrib.pi
#print axioms ProbabilityTheory.IdentDistrib.measure_preimage_eq
#print axioms ProbabilityTheory.measure_eq_zero_or_one_of_indepSet_self
#print axioms ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop
