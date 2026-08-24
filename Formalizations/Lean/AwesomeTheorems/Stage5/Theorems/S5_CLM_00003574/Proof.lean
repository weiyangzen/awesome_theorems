import Mathlib

/- Frozen manifest module spelling:
import FormalConjectures.ErdosProblems.1026
Frozen qualified declaration: Erdos1026.erdos_1026.variants.eq_one
-/

/-!
Kernel term for the exact `S5-CLM-00003574` root.

This file contains theorem declarations only.  The proof term is an exact
transport of the provider declaration at the identical elaborated type.
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003574

/-- Proof-composition node: identity transport at the exact root shape. -/
theorem proof
    (admissibleConstants : Set ℝ)
    (source : IsGreatest admissibleConstants 1) :
    IsGreatest admissibleConstants 1 := by
  exact source

end AwesomeTheorems.Stage5.Theorems.S5_CLM_00003574
