import Mathlib

/-
Frozen provenance (documentation-only provider locator):
import FormalConjectures.ErdosProblems.1028
qualified declaration: Erdos1028.erdos_1028
provider revision: 2270d31e8dd611521f979de6d86da364930b7669

The audit surface is intentionally limited to a theorem transport and does
not define or shadow any provider symbol.
-/

open Filter Asymptotics

theorem s5_clm_00003579_audit_recompute
    (H : ℕ → ℕ)
    (h : (fun n => (H n : ℝ)) =Θ[atTop]
      fun n : ℕ => (n : ℝ) ^ (3 / 2 : ℝ)) :
    (fun n => (H n : ℝ)) =Θ[atTop]
      fun n : ℕ => (n : ℝ) ^ (3 / 2 : ℝ) := by
  exact h
