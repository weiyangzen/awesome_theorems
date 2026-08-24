/-
Frozen source provenance (the numeric module is retained as an immutable
provenance string; canonical replay imports Mathlib and independently checks
the claim-owned transport):
import FormalConjectures.ErdosProblems.119
qualified declaration: Erdos119.erdos_119.parts.ii
source revision: 2270d31e8dd611521f979de6d86da364930b7669
source declaration sha256: 8ea100413f1086916458a58df7de0d20381312c1127ea38648ffa314023d3b85
source type sha256: 985c6e7afd38b23c7e717b861fede9149c638be51cdf0fcb8e79f2985e3c919a

Frozen declaration type:
answer(True) ↔ ∀ (z : ℕ → ℂ) (hz : ∀ i : ℕ, ‖z i‖ = 1),
  ∃ (c : ℝ) (hc : c > 0), Infinite {n : ℕ | M z n > n ^ c}
-/
import Mathlib

/-- Claim-owned kernel transport anchor; the canonical Master recomputes the
    elaborated source and target roots during the trust-zero replay. -/
theorem s5_clm_00003735_statement : True := by
  trivial
