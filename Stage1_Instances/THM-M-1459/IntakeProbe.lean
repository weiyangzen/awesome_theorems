import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Analysis.SpecialFunctions.Complex.LogBounds

/-!
# THM-M-1459 discovery-only intake probe

These checks authenticate pinned finite-sum, norm, geometric-series, and complex-number interfaces.
They do not select a kernel, define a particle hierarchy or multipole expansion, specify a cost
model, or prove a fast multipole correctness, error, or complexity theorem.
-/

#check norm_sum_le
#check summable_geometric_of_norm_lt_one
#check tsum_geometric_of_norm_lt_one
#check tsum_geometric_le_of_norm_lt_one
#check Complex.norm_mul
#check norm_inv
#check Complex.hasSum_taylorSeries_neg_log
#check Complex.norm_log_sub_logTaylor_le
#check Complex.norm_log_one_sub_inv_add_logTaylor_neg_le

#print axioms norm_sum_le
#print axioms tsum_geometric_of_norm_lt_one
#print axioms Complex.norm_log_one_sub_inv_add_logTaylor_neg_le
