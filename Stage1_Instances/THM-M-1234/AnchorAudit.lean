import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
Elaboration witnesses for the mathlib surfaces found by the THM-M-1234 anchor
audit.  These are object-model anchors only; none proves Yudovich existence.
-/

open MeasureTheory

#check EuclideanSpace
#check MeasureTheory.volume
#check AEStronglyMeasurable
#check MemLp
#check ContDiff
#check HasCompactSupport
#check fderiv
#check MeasureTheory.Integrable

