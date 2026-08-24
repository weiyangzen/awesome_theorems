import Mathlib

/- Frozen manifest module spelling:
import FormalConjectures.ErdosProblems.1026
Frozen qualified declaration: Erdos1026.erdos_1026.variants.eq_one
-/

/-!
Exact statement transport for `S5-CLM-00003574`.

The target proposition is deliberately qualified at every source occurrence:
no local notation, alias, coercion, instance, or helper definition participates
in elaboration.
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003574

/-- Kernel-checkable transport shape for the frozen provider statement. -/
theorem statement
    (admissibleConstants : Set ℝ)
    (source : IsGreatest admissibleConstants 1) :
    IsGreatest admissibleConstants 1 := source

end AwesomeTheorems.Stage5.Theorems.S5_CLM_00003574
