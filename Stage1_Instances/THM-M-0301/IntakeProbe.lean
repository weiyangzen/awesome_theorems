import Mathlib.Analysis.Distribution.SchwartzSpace.Basic
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-0301 intake API probe

This file deliberately declares no BMO duality target. It checks only generic
interfaces adjacent to a future source-faithful formalization. In particular,
none of these declarations defines Euclidean BMO, the real Hardy space, or
their duality theorem.
-/

#check MeasureTheory.LocallyIntegrable
#check MeasureTheory.MemLp
#check MeasureTheory.Lp
#check MeasureTheory.integral
#check SchwartzMap
#check SchwartzMap.integralCLM
#check ContinuousLinearMap
