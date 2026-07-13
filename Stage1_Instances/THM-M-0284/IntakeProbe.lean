import Mathlib.Probability.Independence.ZeroOne

/-!
# THM-M-0284 discovery-only intake probe

These checks authenticate the pinned ordinary-measure Kolmogorov zero-one declaration and its
immediate tail-sigma-algebra route. They do not select a canonical source statement, add a wrapper,
or transfer proof credit to THM-M-0284.
-/

open MeasureTheory MeasurableSpace
open scoped MeasureTheory ENNReal

#check ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop
#check ProbabilityTheory.Kernel.measure_zero_or_one_of_measurableSet_limsup_atTop
#check ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atBot
#check ProbabilityTheory.indep_limsup_atTop_self
#check ProbabilityTheory.measure_eq_zero_or_one_of_indepSet_self
#check ProbabilityTheory.iIndep
#check MeasurableSet
#check Filter.limsup
