import Statement

/-!
# THM-M-0786 conditional root composition

This module checks only the final binder-level composition selected by the
frozen architecture. The payoff solver remains an explicit premise, so this
file supplies no proof of Borel determinacy.
-/

namespace Stage1Instances.THM_M_0786.ObligationTree

open Stage1Instances.THM_M_0786

/-- The output interface of the still-open external-theorem adapter package. -/
def PayoffSolver : Prop :=
  ∀ payoff : Set Play, MeasurableSet payoff →
    (∃ first : Strategy, FirstWins payoff first) ∨
    (∃ second : Strategy, SecondWins payoff second)

/-- Checked final composition; `solve` is the entire substantive root premise. -/
theorem root_of_payoffSolver (solve : PayoffSolver) : BorelDeterminacyTarget := by
  exact solve

#print axioms root_of_payoffSolver

end Stage1Instances.THM_M_0786.ObligationTree
