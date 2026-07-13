import Mathlib.Combinatorics.Enumerative.Partition.GenFun
import Mathlib.Data.Nat.ModEq

/-!
# THM-M-0920 discovery-only intake probe

These checks authenticate adjacent pinned integer-partition, restricted-partition,
generating-function, and congruence APIs. They do not identify the catalog's "Andrews splitting
theorem," encode the 1974 Andrews identity, or state or prove THM-M-0920.
-/

#check Nat.Partition
#synth Fintype (Nat.Partition 5)
#check Nat.Partition.restricted
#check Nat.Partition.genFun
#check Nat.Partition.coeff_genFun
#check Nat.Partition.hasProd_genFun
#check Nat.ModEq
