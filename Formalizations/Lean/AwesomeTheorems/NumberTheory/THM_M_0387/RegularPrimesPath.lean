import Mathlib.NumberTheory.FLT.Basic
import Mathlib.Data.Nat.Prime.Basic

namespace AwesomeTheorems.NumberTheory.THM_M_0387

/--
The shape of the regular-primes route: an upstream regularity predicate on odd primes
should imply `FermatLastTheoremFor p`.

This repository does not vendor `flt-regular` yet, so we record the statement shape
and upstream module anchors here without introducing a new dependency.
-/
def regularPrimesStatementShape (IsRegularPrime : ℕ → Prop) : Prop :=
  ∀ {p : ℕ}, Nat.Prime p → IsRegularPrime p → FermatLastTheoremFor p

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
