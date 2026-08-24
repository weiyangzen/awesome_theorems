/-
Frozen provenance: the provider module string is `FormalConjectures.ErdosProblems.107`.
Frozen qualified declaration: `Erdos107.variants.su_bound`.
import FormalConjectures.ErdosProblems.107
Erdos107.variants.su_bound
The numeric module path is retained as provenance only; this claim-owned file
uses the pinned Mathlib environment and does not substitute a local provider.
-/
import Mathlib

open Filter

namespace S5_CLM_00003645

theorem audit_transport (f : ℕ → ℕ) (h :
    ∃ r : ℕ → ℝ, r =o[atTop] (fun n => (n : ℝ)) ∧
      ∀ n ≥ 3, (f n : ℝ) ≤ 2^(n + r n)) :
    ∃ r : ℕ → ℝ, r =o[atTop] (fun n => (n : ℝ)) ∧
      ∀ n ≥ 3, (f n : ℝ) ≤ 2^(n + r n) := by
  exact h

end S5_CLM_00003645
