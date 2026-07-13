import Mathlib.Analysis.Complex.Liouville
import Mathlib.Analysis.Complex.OpenMapping
import Mathlib.Analysis.Complex.ValueDistribution.FirstMainTheorem
import Mathlib.Data.Set.Card

/-!
# THM-M-0228 discovery-only intake probe

These checks authenticate adjacent pinned complex-analysis, value-distribution, and set-cardinality
interfaces. They neither select the canonical Little Picard encoding nor state or prove the target.
-/

open Set

#check Differentiable
#check AnalyticOnNhd
#check Function.const
#check Function.Surjective
#check Set.range
#check Set.Subsingleton
#check Set.encard_le_one_iff_subsingleton
#check Differentiable.exists_const_forall_eq_of_bounded
#check AnalyticOnNhd.is_constant_or_isOpenMap
#check Meromorphic
#check ValueDistribution.characteristic
#check ValueDistribution.isBigO_characteristic_sub_characteristic_shift
#check Complex.differentiable_exp
#check Complex.range_exp
