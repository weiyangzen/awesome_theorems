import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Analysis.Asymptotics.AsymptoticEquivalent
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Filter Asymptotics

#check Nat.Partition
#synth Fintype (Nat.Partition 5)
#check Filter.atTop
#check Asymptotics.IsEquivalent
#check Real.exp
#check Real.pi
#check Real.sqrt

noncomputable def partitionCountProbe (n : ℕ) : ℝ :=
  Fintype.card (Nat.Partition n)

noncomputable def hardyRamanujanMainTermProbe (n : ℕ) : ℝ :=
  Real.exp (Real.pi * Real.sqrt (2 * (n : ℝ) / 3)) /
    (4 * (n : ℝ) * Real.sqrt 3)

#check Asymptotics.IsEquivalent Filter.atTop partitionCountProbe hardyRamanujanMainTermProbe
