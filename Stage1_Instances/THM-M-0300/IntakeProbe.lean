import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Haar.Unique

/-!
# THM-M-0300 intake API probe

This file deliberately declares no Hardy-space atomic-decomposition target. It checks only generic
interfaces that may be adjacent to a future source-faithful encoding. None defines a real Hardy
space, an atom predicate, or the requested decomposition theorem.
-/

open MeasureTheory

#check MeasureTheory.Lp
#check MeasureTheory.MemLp
#check MeasureTheory.Integrable
#check MeasureTheory.integral
#check MeasureTheory.volume
#check Filter.Tendsto
#check Summable
