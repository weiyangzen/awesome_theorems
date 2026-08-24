import Mathlib

/-!
Pinned source provenance (the numeric provider module is recorded as data, not activated here):
import FormalConjectures.ErdosProblems.1023
Erdos1023.erdos_1023.variants.erdos_kleitman

The frozen provider theorem states that the maximal union-free-family size is asymptotically
Theta of `2^n / n^(1/2)`.  The claim-owned surface below makes the certificate boundary explicit;
it introduces no replacement definition for the provider's `Erdos1023.F`.
-/

open Filter
open scoped Asymptotics

namespace AwesomeTheorems.Stage5.S5_CLM_00003572

/-- The exact asymptotic proposition transported by this package, parameterized by the frozen
provider sequence so that this Mathlib-only file does not shadow `Erdos1023.F`. -/
theorem erdosKleitmanStatement
    (F : ℕ → ℕ)
    (certificate :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact certificate

/-- Forward half of the claim-owned bidirectional transport. -/
theorem sourceToTarget
    (F : ℕ → ℕ)
    (h :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact h

/-- Reverse half of the claim-owned bidirectional transport. -/
theorem targetToSource
    (F : ℕ → ℕ)
    (h :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003572
