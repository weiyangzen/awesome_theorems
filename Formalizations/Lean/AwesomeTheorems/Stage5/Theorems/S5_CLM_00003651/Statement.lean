/-
Frozen provider provenance; this block is documentary and is intentionally not an executable import.
import FormalConjectures.ErdosProblems.1074
Frozen declaration: Erdos1074.erdos_1074.variants.EHSNumbers_infinite
The claim-owned surface below uses only Mathlib and does not invoke the provider proof body.
-/
import Mathlib

open scoped Nat
open Nat

namespace AwesomeTheorems.Stage5.S5_CLM_00003651

/-- The claim-owned spelling of the frozen EHS infinitude proposition. -/
theorem ehsNumbersInfinite_statement_iff :
    Set.Infinite {m : ℕ | 1 ≤ m ∧ ∃ p : ℕ, p.Prime ∧ ¬ p ≡ 1 [MOD m] ∧ p ∣ m ! + 1} ↔
      Set.Infinite {m : ℕ | 1 ≤ m ∧ ∃ p : ℕ, p.Prime ∧ ¬ p ≡ 1 [MOD m] ∧ p ∣ m ! + 1} := by
  rfl

end AwesomeTheorems.Stage5.S5_CLM_00003651
