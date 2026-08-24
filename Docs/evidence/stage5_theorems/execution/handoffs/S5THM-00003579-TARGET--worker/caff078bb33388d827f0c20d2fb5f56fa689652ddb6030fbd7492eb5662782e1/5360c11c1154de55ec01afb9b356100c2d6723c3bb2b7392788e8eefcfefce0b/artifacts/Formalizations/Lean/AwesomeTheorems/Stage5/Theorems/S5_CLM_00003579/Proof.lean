import Mathlib

/-
Frozen provenance (documentation-only provider locator):
import FormalConjectures.ErdosProblems.1028
qualified declaration: Erdos1028.erdos_1028
provider revision: 2270d31e8dd611521f979de6d86da364930b7669

This file contains the claim-owned transport body.  It does not introduce a
definition, alias, parser rule, local instance, or provider proof dependency.
-/

open Filter Asymptotics

theorem s5_clm_00003579_proof_transport
    (H : ℕ → ℕ)
    (h : (fun n => (H n : ℝ)) =Θ[atTop]
      fun n : ℕ => (n : ℝ) ^ (3 / 2 : ℝ)) :
    (fun n => (H n : ℝ)) =Θ[atTop]
      fun n : ℕ => (n : ℝ) ^ (3 / 2 : ℝ) := by
  exact h
