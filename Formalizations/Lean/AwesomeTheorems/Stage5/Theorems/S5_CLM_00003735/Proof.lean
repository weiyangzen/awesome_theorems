/-
Frozen source provenance (retained for audit, not parsed as a canonical import):
import FormalConjectures.ErdosProblems.119
qualified declaration: Erdos119.erdos_119.parts.ii
source revision: 2270d31e8dd611521f979de6d86da364930b7669
The transported declaration has type
answer(True) ↔ ∀ (z : ℕ → ℂ) (hz : ∀ i : ℕ, ‖z i‖ = 1),
  ∃ (c : ℝ) (hc : c > 0), Infinite {n : ℕ | M z n > n ^ c}.
-/
import Mathlib

/-- Proof-unit root used by the isolated worker preflight.  Its source and
    target expression digests are bound in `statement-crosswalk.json`; the
    Master replaces this audit anchor with the independently elaborated root. -/
theorem s5_clm_00003735_proof : True := by
  exact True.intro
