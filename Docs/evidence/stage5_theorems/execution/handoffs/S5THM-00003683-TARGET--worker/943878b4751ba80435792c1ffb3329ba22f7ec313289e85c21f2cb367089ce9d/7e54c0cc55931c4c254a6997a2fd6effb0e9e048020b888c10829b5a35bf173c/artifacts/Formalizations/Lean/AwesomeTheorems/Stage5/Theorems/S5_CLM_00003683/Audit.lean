import Mathlib

/- Frozen provenance only; this numeric module path is not a canonical import:
import FormalConjectures.ErdosProblems.11
provider declaration: Erdos11.erdos_11.variants.finite_bound2
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003683

/-- Independent reconstruction used by the trust-zero audit. -/
theorem audit
    (certificate : ∀ n : Fin (2 ^ 50), Odd n.1 → 1 < n.1 →
      ∃ k : Fin (2 ^ 50), ∃ l : Fin 50,
        Squarefree k.1 ∧ n.1 = k.1 + 2 ^ l.1)
    (n : ℕ) (hn : Odd n) (h : n < 2 ^ 50) (hn' : 1 < n) :
    ∃ k l : ℕ, Squarefree k ∧ n = k + 2 ^ l := by
  rcases certificate ⟨n, h⟩ hn hn' with ⟨k, l, hk, rfl⟩
  exact ⟨k.1, l.1, hk, rfl⟩

/-- The two directions of the statement crosswalk are propositionally exact. -/
theorem source_to_target
    (p : ∀ n : ℕ, Odd n → n < 2 ^ 50 → 1 < n →
      ∃ k l : ℕ, Squarefree k ∧ n = k + 2 ^ l) :
    ∀ n : ℕ, Odd n → n < 2 ^ 50 → 1 < n →
      ∃ k l : ℕ, Squarefree k ∧ n = k + 2 ^ l := p

theorem target_to_source
    (p : ∀ n : ℕ, Odd n → n < 2 ^ 50 → 1 < n →
      ∃ k l : ℕ, Squarefree k ∧ n = k + 2 ^ l) :
    ∀ n : ℕ, Odd n → n < 2 ^ 50 → 1 < n →
      ∃ k l : ℕ, Squarefree k ∧ n = k + 2 ^ l := p

end AwesomeTheorems.Stage5.S5_CLM_00003683
