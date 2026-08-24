import Mathlib

/-
Frozen provider provenance (text only; the numeric module is not a canonical import):
import FormalConjectures.ErdosProblems.107
Erdos107.variants.ersz_bounds
Provider revision: 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003643

/-- The claim-owned surface records the exact logical normalization used by the
Erdős--Szekeres bounds statement.  The function argument is the transported
meaning of the frozen provider's `Erdos107.f`; the semantic crosswalk binds it
to that source constant before this normalization is used. -/
theorem erdosSzekeresBounds_statement_equivalence (f : ℕ → ℕ) :
    (∀ n : ℕ, 3 ≤ n →
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) ↔
    (∀ n ≥ 3,
      2 ^ (n - 2) + 1 ≤ f n ∧
      f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1) := by
  rfl

end AwesomeTheorems.Stage5.S5_CLM_00003643
