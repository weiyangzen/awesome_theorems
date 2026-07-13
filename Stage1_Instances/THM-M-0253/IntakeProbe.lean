import Mathlib.Analysis.Complex.CanonicalDecomposition
import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Topology.MetricSpace.Bounded

/-!
# THM-M-0253 discovery-only intake probe

These checks authenticate generic pinned APIs adjacent to a possible unit-disc bounded-analytic
interpolation encoding. They do not define a Hardy space, an interpolating sequence, a Carleson
condition, a canonical target, or a proof.
-/

#check Complex.UnitDisc
#check Complex.UnitDisc.norm_lt_one
#check AnalyticOnNhd
#check Bornology.IsBounded
#check Metric.isBounded_range_iff
#check Function.Injective
#check (fun _sequence : ℕ → Complex.UnitDisc => _sequence)
#check Complex.canonicalFactor
#check Complex.analyticOnNhd_canonicalFactor
