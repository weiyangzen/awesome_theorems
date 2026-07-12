import Mathlib.Data.Complex.Basic
import Mathlib.Logic.Function.Iterate
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Analysis.Normed.Field.Basic

/-! Discovery-only API checks for a later source-corrected Mandelbrot-set statement. -/

#check Complex
#check (fun c z : ℂ => z ^ 2 + c)
#check (fun (f : ℂ → ℂ) (n : ℕ) (z : ℂ) => f^[n] z)
#check Function.iterate_zero_apply
#check Function.iterate_succ_apply
#check Set.range
#check Bornology.IsBounded
#check Metric.isBounded_iff_subset_closedBall
#check norm
