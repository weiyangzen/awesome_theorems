import Mathlib.NumberTheory.FLT.Basic
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path
import AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath

open AwesomeTheorems.NumberTheory.THM_M_0387

example : FermatLastTheoremFor 4 := flt4Path

example : FermatLastTheoremFor 3 := flt3Path

example : FermatLastTheoremWith ℤ 4 := flt4IntPath

example : FermatLastTheoremFor 8 := flt8ViaFlt4Path

example
    (hodd : ∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p) :
    FermatLastTheorem :=
  FermatLastTheorem.of_odd_primes hodd
