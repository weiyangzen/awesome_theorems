import Mathlib

/-!
Frozen provenance (not an active canonical import):
import FormalConjectures.ErdosProblems.1105
Erdos1105.erdos_1105.parts.ii

Audit surface for Master trust-zero replay.  It neither imports nor invokes the
provider theorem whose source proof contains `sorryAx`.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003691

open SimpleGraph

/-- Semantic-substitution mutation: an arbitrary altered output is not used. -/
theorem audit_exact_output
    (antiRamsey altered : ∀ {V : Type}, SimpleGraph V → ℕ → ℕ)
    (hFormula : ∀ (k n : ℕ), 5 ≤ k → k ≤ n →
      let ℓ := (k - 1) / 2
      let ε := if Odd k then 1 else 2
      antiRamsey (pathGraph k) n =
        max ((k - 2).choose 2 + 1)
          ((ℓ - 1).choose 2 + (ℓ - 1) * (n - ℓ + 1) + ε))
    (k n : ℕ) (hk : 5 ≤ k) (hkn : k ≤ n) :
    antiRamsey (pathGraph k) n =
      max ((k - 2).choose 2 + 1)
        ((((k - 1) / 2 - 1).choose 2) +
          ((k - 1) / 2 - 1) * (n - (k - 1) / 2 + 1) +
          (if Odd k then 1 else 2)) := by
  exact hFormula k n hk hkn

/-- Reverse audit transport, independently replayable from `Mathlib`. -/
theorem audit_reverse_transport
    (antiRamsey : ∀ {V : Type}, SimpleGraph V → ℕ → ℕ)
    (hNormalized : ∀ (k n : ℕ), 5 ≤ k → k ≤ n →
      antiRamsey (pathGraph k) n =
        max ((k - 2).choose 2 + 1)
          ((((k - 1) / 2 - 1).choose 2) +
            ((k - 1) / 2 - 1) * (n - (k - 1) / 2 + 1) +
            (if Odd k then 1 else 2))) :
    ∀ (k n : ℕ), 5 ≤ k → k ≤ n →
      let ℓ := (k - 1) / 2
      let ε := if Odd k then 1 else 2
      antiRamsey (pathGraph k) n =
        max ((k - 2).choose 2 + 1)
          ((ℓ - 1).choose 2 + (ℓ - 1) * (n - ℓ + 1) + ε) := by
  intro k n hk hkn
  exact hNormalized k n hk hkn

end AwesomeTheorems.Stage5.S5_CLM_00003691
