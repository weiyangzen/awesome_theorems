import Mathlib.Analysis.Complex.Basic
import Mathlib.Logic.Function.Iterate
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Topology.Separation.Connected

/-! Discovery-only API checks for a later source-frozen Mandelbrot-set statement. -/

#check Complex
#check (fun c z : Complex => z ^ 2 + c)
#check (fun (c : Complex) (n : Nat) => (fun z : Complex => z ^ 2 + c)^[n] 0)
#check Function.iterate_zero_apply
#check Function.iterate_succ_apply
#check Set.range
#check Bornology.IsBounded
#check Metric.isBounded_iff_subset_closedBall
#check IsConnected
#check IsPreconnected
#check IsCompact
