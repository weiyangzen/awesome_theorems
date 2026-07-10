import FltRegular.SmallNumbers.SmallNumbers

namespace AwesomeTheorems.NumberTheory.THM_M_0387

/-- The machine-checked `n = 5` branch imported from `flt-regular`. -/
theorem flt5Path : FermatLastTheoremFor 5 :=
  fermatLastTheoremFive

/-- The machine-checked `n = 7` branch imported from `flt-regular`. -/
theorem flt7Path : FermatLastTheoremFor 7 :=
  fermatLastTheoremSeven

/-- The machine-checked `n = 11` branch imported from `flt-regular`. -/
theorem flt11Path : FermatLastTheoremFor 11 :=
  fermatLastTheoremEleven

/-- The machine-checked `n = 13` branch imported from `flt-regular`. -/
theorem flt13Path : FermatLastTheoremFor 13 :=
  fermatLastTheoremThirteen

/-- The machine-checked family of exponents from `3` through `16`. -/
theorem fltSmallExponentsPath {n : ℕ} (hn : n ∈ Finset.Icc 3 16) :
    FermatLastTheoremFor n :=
  FLT_small hn

end AwesomeTheorems.NumberTheory.THM_M_0387
