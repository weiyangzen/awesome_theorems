import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Periodic

/-!
# THM-M-0245 discovery-only intake probe

These checks authenticate pinned APIs adjacent to the unit disc, holomorphic functions, radial
parameterization, one-sided limits, and almost-everywhere boundary statements. They do not choose
a bounded or Hardy-class hypothesis, define the exact boundary measure, state Fatou's theorem, or
provide proof credit.
-/

namespace Stage1Instances.THM_M_0245

#check Complex.UnitDisc
#check Complex.UnitDisc.norm_lt_one
#check AnalyticOnNhd
#check circleMap
#check range_circleMap
#check continuous_circleMap
#check Filter.Tendsto
#check nhdsWithin
#check MeasureTheory.ae
#check AddCircle.measure_univ

end Stage1Instances.THM_M_0245
