import Mathlib.MeasureTheory.Constructions.Polish.Basic
import Mathlib.MeasureTheory.Function.AEEqFun
import Mathlib.MeasureTheory.Measure.RegularityCompacts

/-!
# THM-M-0287 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for relative continuity, measurability,
compact inner regularity, continuous maps, and a distinct topology-refinement theorem. They do not
state or prove the measure-theoretic Lusin theorem.
-/

#check ContinuousOn
#check Continuous.measurable
#check MeasurableSet.exists_isCompact_diff_lt
#check MeasureTheory.innerRegular_isCompact_isClosed_measurableSet_of_finite
#check Measurable.exists_continuous
#check ContinuousMap.toAEEqFun
