import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.Probability.Martingale.Basic

/-!
# THM-M-1078: pinned mathlib anchor probes

These declarations are the closest support in the pinned mathlib revision.  In
particular, the `Submartingale.sum_mul_sub'` conclusion is a submartingale
closure result, not the target `L^p` estimate.
-/

open MeasureTheory

#check IsPredictable
#check IsPredictable.measurable_add_one
#check isPredictable_iff_measurable_add_one
#check Martingale
#check Submartingale.sum_mul_sub'
#check MemLp
#check lpNorm

