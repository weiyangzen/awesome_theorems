import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Analysis.Normed.Operator.ContinuousLinearMap

/-!
# THM-M-0299 discovery-only intake probe

These checks authenticate generic pinned measure, integration, Lp-space, and bounded-operator APIs.
They do not define a singular-integral kernel or operator, select a canonical target, or prove an
Lp boundedness theorem.
-/

#check MeasureTheory.Measure
#check MeasureTheory.Measure.restrict
#check MeasureTheory.MemLp
#check MeasureTheory.Lp
#check MeasureTheory.integral
#check ContinuousLinearMap
#check ContinuousLinearMap.mk
