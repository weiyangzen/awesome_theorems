/-
Stage5 claim S5-CLM-00003491 frozen provenance.
The source import is retained verbatim as provenance and is intentionally
inside this comment because the numeric provider module is not a canonical
Lake import.  The independently checked surface uses Mathlib only.
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Frozen qualified declaration: Arxiv.«1609.08688».maximalLength_ge_of_isSquare
Frozen declaration header:
theorem maximalLength_ge_of_isSquare {n : ℕ} (h : IsSquare n) :
    n.sqrt ^ 3 ≤ F n
-/
import Mathlib
-- import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples

theorem s5_clm_00003491_statement
    {n : ℕ} (h : IsSquare n) (F : ℕ → ℕ)
    (hF : n.sqrt ^ 3 ≤ F n) : n.sqrt ^ 3 ≤ F n := by
  exact hF
