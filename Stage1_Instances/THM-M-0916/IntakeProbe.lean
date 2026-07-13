import Mathlib.Combinatorics.Enumerative.Partition.GenFun

/-!
# THM-M-0916 discovery-only intake probe

These checks authenticate adjacent pinned partition and power-series APIs. They do not state
Euler's pentagonal number theorem, select a source formula, or supply proof credit.
-/

#synth Fintype (Nat.Partition 5)
#check Fintype.card (Nat.Partition 5)
#check Nat.Partition.genFun
#check Nat.Partition.coeff_genFun
#check Nat.Partition.hasProd_genFun
#check Nat.Partition.genFun_eq_tprod
#check PowerSeries.mk
#check PowerSeries.coeff
