import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-0339 pinned anchor probes

These checks inventory mathlib infrastructure used by the frozen MSS Corollary 1.5 statement.
They do not assert the partition theorem.
-/

#check InnerProductSpace.rankOne
#check InnerProductSpace.rankOne_apply
#check InnerProductSpace.norm_rankOne
#check InnerProductSpace.isPositive_rankOne_self
#check OrthonormalBasis.sum_rankOne_eq_id
#check ContinuousLinearMap.id
#check Finset.sum_filter
#check Real.sqrt

