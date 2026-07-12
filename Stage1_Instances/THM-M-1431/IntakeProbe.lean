import Mathlib.Analysis.Complex.Basic
import Mathlib.Logic.Function.Iterate
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Topology.Separation.Connected

/-! Discovery-only API checks for a later source-frozen Mandelbrot-set statement. -/

#check Complex
#check Nat.iterate
#check Function.iterate_succ_apply
#check Set.range
#check Bornology.IsBounded
#check Metric.isBounded_iff_subset_closedBall
#check IsConnected
#check IsPreconnected
#check IsCompact
