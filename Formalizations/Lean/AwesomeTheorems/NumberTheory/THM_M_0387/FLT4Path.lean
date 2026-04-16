import Mathlib.NumberTheory.FLT.Four

namespace AwesomeTheorems.NumberTheory.THM_M_0387

/-- The machine-checked `n = 4` branch imported from `mathlib`. -/
theorem flt4Path : FermatLastTheoremFor 4 := fermatLastTheoremFour

/-- The same `n = 4` branch specialized to integer solutions. -/
theorem flt4IntPath : FermatLastTheoremWith ℤ 4 :=
  (fermatLastTheoremFor_iff_int).mp flt4Path

/-- Exponents divisible by `4` reduce to the `n = 4` branch. -/
theorem flt8ViaFlt4Path : FermatLastTheoremFor 8 :=
  FermatLastTheoremFor.mono (by decide : 4 ∣ 8) flt4Path

end AwesomeTheorems.NumberTheory.THM_M_0387
