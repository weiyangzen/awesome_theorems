import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension
import Mathlib.MeasureTheory.Integral.Bochner.Set

/-!
# THM-M-1200 anchor audit

This module checks the precise mathlib declarations selected as supporting
infrastructure.  It intentionally does not prove the frozen target.
-/

#check ContDiffBump
#check ContDiffBump.contDiff
#check ContDiffBump.hasCompactSupport
#check ContDiffBump.one_of_mem_closedBall
#check ContDiffBump.nonneg
#check Continuous.integral_pos_of_hasCompactSupport_nonneg_nonzero
#check MeasureTheory.integral_congr_ae
