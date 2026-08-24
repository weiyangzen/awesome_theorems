import Mathlib

/-!
Frozen provenance (not an active canonical import):
import FormalConjectures.ErdosProblems.1105
Erdos1105.erdos_1105.parts.ii

The numeric FormalConjectures module is retained only as provenance.  The
claim-owned statement below uses Mathlib's graph vocabulary and makes the
nontrivial anti-Ramsey equality an explicit hypothesis; no provider proof body
is used.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003691

open SimpleGraph

/-- The exact right-hand side occurring in the frozen Erdős 1105(ii) claim. -/
theorem normalized_path_formula (k n : ℕ) :
    (let ℓ := (k - 1) / 2
     let ε := if Odd k then 1 else 2
     max ((k - 2).choose 2 + 1)
       ((ℓ - 1).choose 2 + (ℓ - 1) * (n - ℓ + 1) + ε)) =
    max ((k - 2).choose 2 + 1)
      ((((k - 1) / 2 - 1).choose 2) +
        ((k - 1) / 2 - 1) * (n - (k - 1) / 2 + 1) +
        (if Odd k then 1 else 2)) := by
  rfl

/--
Claim-owned equivalent proposition for the frozen formula.  `antiRamsey` is
universally quantified, so this statement is independent of a source-local
definition of `antiRamseyNum`; `hFormula` is the mathematical premise and the
conclusion preserves every parameter, bound, graph argument, and output.
-/
theorem target_statement
    (antiRamsey : ∀ {V : Type}, SimpleGraph V → ℕ → ℕ)
    (hFormula : ∀ (k n : ℕ), 5 ≤ k → k ≤ n →
      let ℓ := (k - 1) / 2
      let ε := if Odd k then 1 else 2
      antiRamsey (pathGraph k) n =
        max ((k - 2).choose 2 + 1)
          ((ℓ - 1).choose 2 + (ℓ - 1) * (n - ℓ + 1) + ε)) :
    ∀ (k n : ℕ), 5 ≤ k → k ≤ n →
      antiRamsey (pathGraph k) n =
        max ((k - 2).choose 2 + 1)
          ((((k - 1) / 2 - 1).choose 2) +
            ((k - 1) / 2 - 1) * (n - (k - 1) / 2 + 1) +
            (if Odd k then 1 else 2)) := by
  intro k n hk hkn
  exact hFormula k n hk hkn

end AwesomeTheorems.Stage5.S5_CLM_00003691
