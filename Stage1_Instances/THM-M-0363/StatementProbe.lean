import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-0363 statement-infrastructure probe

This file deliberately does not declare the BMO duality target. It only checks
the generic pinned interfaces that a source-faithful statement would have to
build on. The concrete BMO and real Hardy-space interfaces are absent.
-/

#check MeasureTheory.LocallyIntegrable
#check MeasureTheory.MemLp
#check MeasureTheory.integral
#check SchwartzMap
#check ContinuousLinearMap
