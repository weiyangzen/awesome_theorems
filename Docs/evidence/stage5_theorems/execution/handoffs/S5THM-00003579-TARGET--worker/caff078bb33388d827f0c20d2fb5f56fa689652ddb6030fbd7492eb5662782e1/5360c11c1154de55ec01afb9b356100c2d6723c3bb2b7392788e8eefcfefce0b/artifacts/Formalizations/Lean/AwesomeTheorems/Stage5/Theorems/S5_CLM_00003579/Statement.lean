import Mathlib

/-
Frozen provenance (the numeric module path is intentionally documentation-only):
import FormalConjectures.ErdosProblems.1028
qualified declaration: Erdos1028.erdos_1028
provider revision: 2270d31e8dd611521f979de6d86da364930b7669

The claim-owned surface below states the transport proposition with its
mathematical function supplied explicitly.  No local helper, alias, parser
extension, or provider proof body is introduced.
-/

open Filter Asymptotics

theorem s5_clm_00003579_statement_transport
    (H : ℕ → ℕ)
    (h : (fun n => (H n : ℝ)) =Θ[atTop]
      fun n : ℕ => (n : ℝ) ^ (3 / 2 : ℝ)) :
    (fun n => (H n : ℝ)) =Θ[atTop]
      fun n : ℕ => (n : ℝ) ^ (3 / 2 : ℝ) := by
  exact h
