import Mathlib

/-!
Frozen provenance (not an active canonical import):
import FormalConjectures.ErdosProblems.1105
Erdos1105.erdos_1105.parts.ii

This file deliberately repeats the small claim-owned closure rather than
importing another generated file, allowing independent cold elaboration.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003691

open SimpleGraph

/-- Forward readable unit: specialize the supplied exact formula. -/
theorem specialize_path_formula
    (antiRamsey : ∀ {V : Type}, SimpleGraph V → ℕ → ℕ)
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

/-- Reverse transport: package pointwise normalized evidence as the let form. -/
theorem package_path_formula
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

/-- Exact bidirectional equivalence used by the semantic crosswalk. -/
theorem path_formula_iff
    (antiRamsey : ∀ {V : Type}, SimpleGraph V → ℕ → ℕ) :
    (∀ (k n : ℕ), 5 ≤ k → k ≤ n →
      let ℓ := (k - 1) / 2
      let ε := if Odd k then 1 else 2
      antiRamsey (pathGraph k) n =
        max ((k - 2).choose 2 + 1)
          ((ℓ - 1).choose 2 + (ℓ - 1) * (n - ℓ + 1) + ε)) ↔
    (∀ (k n : ℕ), 5 ≤ k → k ≤ n →
      antiRamsey (pathGraph k) n =
        max ((k - 2).choose 2 + 1)
          ((((k - 1) / 2 - 1).choose 2) +
            ((k - 1) / 2 - 1) * (n - (k - 1) / 2 + 1) +
            (if Odd k then 1 else 2))) := by
  constructor
  · exact specialize_path_formula antiRamsey
  · exact package_path_formula antiRamsey

end AwesomeTheorems.Stage5.S5_CLM_00003691
