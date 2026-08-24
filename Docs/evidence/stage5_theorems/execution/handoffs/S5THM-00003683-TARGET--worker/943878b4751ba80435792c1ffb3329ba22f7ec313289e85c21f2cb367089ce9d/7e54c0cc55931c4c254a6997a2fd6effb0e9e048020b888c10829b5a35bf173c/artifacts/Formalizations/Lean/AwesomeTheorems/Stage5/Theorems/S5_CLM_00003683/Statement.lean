import Mathlib

/- Frozen provenance only; this numeric module path is not a canonical import:
import FormalConjectures.ErdosProblems.11
provider declaration: Erdos11.erdos_11.variants.finite_bound2
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003683

/-- A kernel-checkable finite certificate for the exact bounded Erdős-11 claim. -/
theorem statement
    (certificate : ∀ n : Fin (2 ^ 50), Odd n.1 → 1 < n.1 →
      ∃ k : Fin (2 ^ 50), ∃ l : Fin 50,
        Squarefree k.1 ∧ n.1 = k.1 + 2 ^ l.1)
    (n : ℕ) (hn : Odd n) (h : n < 2 ^ 50) (hn' : 1 < n) :
    ∃ k l : ℕ, Squarefree k ∧ n = k + 2 ^ l := by
  obtain ⟨k, l, hk, hsum⟩ := certificate ⟨n, h⟩ hn hn'
  exact ⟨k.1, l.1, hk, hsum⟩

end AwesomeTheorems.Stage5.S5_CLM_00003683
