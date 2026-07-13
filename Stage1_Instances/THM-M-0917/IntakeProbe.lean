import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Combinatorics.Enumerative.Partition.GenFun

/-!
# THM-M-0917 discovery-only intake probe

These checks authenticate adjacent pinned integer-partition and generic generating-function APIs.
They do not select a truth-valued interpretation of the catalog gloss or state THM-M-0917.
-/

#check Nat.Partition
#synth Fintype (Nat.Partition 5)
#synth Unique (Nat.Partition 0)
#synth Unique (Nat.Partition 1)
#check Fintype.card (Nat.Partition 5)
#check Nat.Partition.genFun
#check Nat.Partition.coeff_genFun
#check Nat.Partition.hasProd_genFun
