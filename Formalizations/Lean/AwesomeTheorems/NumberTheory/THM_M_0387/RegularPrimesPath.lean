import FltRegular.FltRegular

namespace AwesomeTheorems.NumberTheory.THM_M_0387

/-- The exact statement shape supplied by the pinned `flt-regular` terminal theorem. -/
def regularPrimesStatementShape : Prop :=
  ∀ {p : ℕ} [Fact p.Prime], IsRegularPrime p → p ≠ 2 → FermatLastTheoremFor p

/--
The machine-checked regular-primes branch imported from the pinned
`leanprover-community/flt-regular` dependency.
-/
theorem regularPrimesPath {p : ℕ} [Fact p.Prime] (hreg : IsRegularPrime p) (hodd : p ≠ 2) :
    FermatLastTheoremFor p :=
  flt_regular hreg hodd

/-- Upstream modules that realize the regular-primes branch in `flt-regular`. -/
def regularPrimesPathModules : List String := [
  "FltRegular/NumberTheory/RegularPrimes.lean",
  "FltRegular/MayAssume/Lemmas.lean",
  "FltRegular/CaseI/Statement.lean",
  "FltRegular/CaseII/Statement.lean",
  "FltRegular/CaseII/InductionStep.lean",
  "FltRegular/FltRegular.lean"
]

/-- Terminal upstream declaration name for the regular-primes branch. -/
def regularPrimesPathTerminalTheorem : String := "flt_regular"

end AwesomeTheorems.NumberTheory.THM_M_0387
