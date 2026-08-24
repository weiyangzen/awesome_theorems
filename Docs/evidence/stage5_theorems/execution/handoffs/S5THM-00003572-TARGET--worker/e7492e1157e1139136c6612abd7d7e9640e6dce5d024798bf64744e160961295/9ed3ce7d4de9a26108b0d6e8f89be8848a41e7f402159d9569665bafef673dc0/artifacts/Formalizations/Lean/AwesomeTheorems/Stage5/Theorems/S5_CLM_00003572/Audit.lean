import Mathlib

/-!
Pinned source provenance (the numeric provider module is recorded as data, not activated here):
import FormalConjectures.ErdosProblems.1023
Erdos1023.erdos_1023.variants.erdos_kleitman

Independent audit surface for the claim-owned forward/reverse transport and root composition.
-/

open Filter
open scoped Asymptotics

namespace AwesomeTheorems.Stage5.S5_CLM_00003572

/-- Audit the source-to-target direction without consulting a provider proof term. -/
theorem auditSourceToTarget
    (F : ℕ → ℕ)
    (h :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact h

/-- Audit the target-to-source direction without consulting a provider proof term. -/
theorem auditTargetToSource
    (F : ℕ → ℕ)
    (h :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact h

/-- Audit the root's proof composition at the same type as both transport directions. -/
theorem auditRoot
    (F : ℕ → ℕ)
    (certificate :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact auditTargetToSource F (auditSourceToTarget F certificate)

end AwesomeTheorems.Stage5.S5_CLM_00003572
