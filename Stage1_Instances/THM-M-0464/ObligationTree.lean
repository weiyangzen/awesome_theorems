/-!
# THM-M-0464 obligation interfaces

This source fragment is elaborated immediately after `Statement.lean`; the dossier lives outside
the Lake module root. It checks the exact root boundary and the final counting conclusion, but does
not postulate or prove any open Pila-Wilkie package recorded in the obligation registry.
-/

namespace AwesomeTheorems.THM_M_0464.ObligationTree

open Set

/-- The conclusion delivered for one fixed definable set and positive exponent. -/
def CountingConclusion (n : ℕ) (X : Set (Fin n → ℝ)) (epsilon : ℝ) : Prop :=
  ∃ c : ℝ, ∀ T : ℕ, 1 ≤ T →
    (rationalPoints (X \ algebraicPart X) T).Finite ∧
      ((rationalPoints (X \ algebraicPart X) T).ncard : ℝ) ≤ c * (T : ℝ) ^ epsilon

/-- Exact definitional unfolding of the frozen root into its terminal counting interface.
This consumes the complete terminal conclusion as a hypothesis; it supplies no proof of it. -/
theorem root_from_terminal_counting
    (terminal : ∀ (S : OMinimalStructure) (n : ℕ), 1 ≤ n →
      ∀ (X : Set (Fin n → ℝ)), S.definable n X →
      ∀ epsilon : ℝ, 0 < epsilon → CountingConclusion n X epsilon) :
    PilaWilkieStatement := by
  intro S n hn X hX epsilon hepsilon
  exact terminal S n hn X hX epsilon hepsilon

#check CountingConclusion
#check root_from_terminal_counting
#print axioms root_from_terminal_counting

end AwesomeTheorems.THM_M_0464.ObligationTree
