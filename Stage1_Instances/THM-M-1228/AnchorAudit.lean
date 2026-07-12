import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Measure.Hausdorff

/-!
# THM-M-1228: pinned anchor probes

These declarations are adjacent analysis infrastructure. In particular,
`hausdorffMeasure` uses the ambient metric and is not by itself the parabolic
Hausdorff construction required by the CKN target.
-/

#check MeasureTheory.Measure.hausdorffMeasure
#check MeasureTheory.Measure.hausdorffMeasure_apply
#check Distribution
#check TestFunction
#check ContDiffAt
#check ContDiff
#check MeasureTheory.eLpNorm
#check MeasureTheory.MemLp
#check MeasureTheory.Lp
