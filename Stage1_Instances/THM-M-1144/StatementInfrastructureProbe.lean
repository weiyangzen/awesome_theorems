import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic

/-!
This probe checks only the pinned Lean substrate relevant to a future exact statement. It does not
select a gradient-estimate variant and is not the canonical target for `THM-M-1144`.
-/

#check InnerProductSpace.HarmonicAt
#check InnerProductSpace.HarmonicOnNhd
#check InnerProductSpace.HarmonicOnNhd.contDiffOn
#check fderiv
#check Metric.ball
