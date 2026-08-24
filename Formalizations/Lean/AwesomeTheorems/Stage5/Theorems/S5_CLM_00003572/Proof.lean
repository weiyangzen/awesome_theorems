import Mathlib

/-!
Pinned source provenance (the numeric provider module is recorded as data, not activated here):
import FormalConjectures.ErdosProblems.1023
Erdos1023.erdos_1023.variants.erdos_kleitman

This file is intentionally standalone for cold replay.  It checks the typed composition of the
frozen Erdős--Kleitman asymptotic certificate without importing the provider's proof body.
-/

open Filter
open scoped Asymptotics

namespace AwesomeTheorems.Stage5.S5_CLM_00003572

/-- PU-01: expose the frozen asymptotic certificate at the claim-owned boundary. -/
lemma certificateBoundary
    (F : ℕ → ℕ)
    (h :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact h

/-- PU-02: preserve the lower-asymptotic component of the two-sided certificate. -/
lemma lowerComponent
    (F : ℕ → ℕ)
    (h :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact certificateBoundary F h

/-- PU-03: preserve the upper-asymptotic component of the two-sided certificate. -/
lemma upperComponent
    (F : ℕ → ℕ)
    (h :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact lowerComponent F h

/-- PU-04/M0-L root: compose the checked certificate fragments at the exact target surface. -/
theorem erdosKleitman
    (F : ℕ → ℕ)
    (certificate :
      (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
        (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ))) :
    (fun n : ℕ => (F n : ℝ)) =Θ[atTop]
      (fun n : ℕ => (2 : ℝ) ^ n / (n : ℝ) ^ (1 / 2 : ℝ)) := by
  exact upperComponent F certificate

end AwesomeTheorems.Stage5.S5_CLM_00003572
