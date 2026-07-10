import Mathlib.NumberTheory.FLT.Basic
import AwesomeTheorems.NumberTheory.THM_M_0387.StatementAndReductionPath
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path
import AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath
import AwesomeTheorems.NumberTheory.THM_M_0387.SmallExponentsPath
import AwesomeTheorems.NumberTheory.THM_M_0387.InternalCoveragePath

open AwesomeTheorems.NumberTheory.THM_M_0387

example : fermatLastTheoremRootStatement ↔ FermatLastTheorem :=
  fermatLastTheoremRootStatement_iff

example {n : ℕ} : FermatLastTheoremFor n ↔ FermatLastTheoremForCoprime n :=
  fermatLastTheoremFor_iff_coprime

example : FermatLastTheoremFor 0 := fltExponentZeroPath

example : ¬ FermatLastTheoremFor 1 := notFltExponentOnePath

example : ¬ FermatLastTheoremFor 2 := notFltExponentTwoPath

example : FermatLastTheoremFor 4 := flt4Path

example : FermatLastTheoremFor 3 := flt3Path

example : FermatLastTheoremWith ℤ 4 := flt4IntPath

example : FermatLastTheoremFor 8 := flt8ViaFlt4Path

example : FermatLastTheoremFor 5 := flt5Path

example : FermatLastTheoremFor 7 := flt7Path

example : FermatLastTheoremFor 11 := flt11Path

example : FermatLastTheoremFor 13 := flt13Path

example {n : ℕ} (hn : n ∈ Finset.Icc 3 16) : FermatLastTheoremFor n :=
  fltSmallExponentsPath hn

example {p : ℕ} [Fact p.Prime] (hreg : IsRegularPrime p) (hodd : p ≠ 2) :
    FermatLastTheoremFor p :=
  regularPrimesPath hreg hodd

example
    (hodd : ∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p) :
    FermatLastTheorem :=
  FermatLastTheorem.of_odd_primes hodd
