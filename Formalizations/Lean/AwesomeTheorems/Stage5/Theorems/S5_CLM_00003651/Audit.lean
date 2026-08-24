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

/-- The reverse leg records that the claim-owned proposition is unchanged. -/
theorem ehsNumbersInfinite_round_trip
    (h : Set.Infinite {m : ℕ | 1 ≤ m ∧ ∃ p : ℕ, p.Prime ∧ ¬ p ≡ 1 [MOD m] ∧ p ∣ m ! + 1}) :
    Set.Infinite {m : ℕ | 1 ≤ m ∧ ∃ p : ℕ, p.Prime ∧ ¬ p ≡ 1 [MOD m] ∧ p ∣ m ! + 1} := by
  simpa using h

end AwesomeTheorems.Stage5.S5_CLM_00003651
