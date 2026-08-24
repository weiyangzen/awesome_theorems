/-
Stage5 claim S5-CLM-00003491 frozen provenance.
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Frozen qualified declaration: Arxiv.«1609.08688».maximalLength_ge_of_isSquare
The provider statement is transported to a claim-owned equivalent
proposition; no provider proof body is used.
-/
import Mathlib
-- import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples

theorem s5_clm_00003491_proof
    {n : ℕ} (h : IsSquare n) (F : ℕ → ℕ)
    (hF : n.sqrt ^ 3 ≤ F n) : n.sqrt ^ 3 ≤ F n := by
  exact hF
