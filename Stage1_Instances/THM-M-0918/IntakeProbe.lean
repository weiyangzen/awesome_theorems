import Mathlib.Combinatorics.Enumerative.Partition.Glaisher

/-!
# THM-M-0918 discovery-only intake probe

These checks authenticate pinned partition, restricted-partition, formal-power-series, infinite
sum, and infinite product interfaces adjacent to possible Rogers-Ramanujan encodings. They do not
define either Rogers-Ramanujan restriction, select the analytic or combinatorial pair as the root,
or prove either identity.
-/

#check Nat.Partition
#synth Fintype (Nat.Partition 5)
#check Nat.Partition.restricted
#check Nat.Partition.countRestricted
#check Nat.Partition.hasProd_powerSeriesMk_card_restricted
#check Nat.Partition.powerSeriesMk_card_restricted_eq_tprod
#check Nat.Partition.genFun
#check Nat.Partition.hasProd_genFun
#check PowerSeries.mk
#check PowerSeries.coeff
#check PowerSeries.X
#check PowerSeries.WithPiTopology.multipliable_one_sub_X_pow
#check HasSum
#check HasProd
#check tsum
#check tprod

#print axioms Nat.Partition.hasProd_powerSeriesMk_card_restricted
#print axioms Nat.Partition.powerSeriesMk_card_restricted_eq_tprod
#print axioms PowerSeries.WithPiTopology.multipliable_one_sub_X_pow
