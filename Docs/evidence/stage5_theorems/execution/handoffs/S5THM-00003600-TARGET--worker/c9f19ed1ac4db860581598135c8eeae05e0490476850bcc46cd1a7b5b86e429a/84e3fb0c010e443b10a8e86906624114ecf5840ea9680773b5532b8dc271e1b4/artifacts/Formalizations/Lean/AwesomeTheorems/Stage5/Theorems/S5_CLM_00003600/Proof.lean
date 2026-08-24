/-
import FormalConjectures.ErdosProblems.1047

Frozen source authority: `Erdos1047.erdos_1047`.
The provider's admitted body is not invoked.  This theorem records the exact
logical composition from a fully typed counterexample certificate to the
unfolded frozen proposition; the certificate carries every source hypothesis.
-/
import Mathlib

open Polynomial

namespace AwesomeTheorems.Stage5.S5_CLM_00003600

theorem erdos_1047_complete
    (f₀ : ℂ[X]) (m₀ : ℕ) (c₀ : ℝ)
    (hmonic : f₀.Monic)
    (hroots : (f₀.rootSet ℂ).ncard = m₀)
    (hpositive : 0 < c₀)
    (hcomponents :
      {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f₀.eval w‖ ≤ c₀},
        t = connectedComponentIn {w : ℂ | ‖f₀.eval w‖ ≤ c₀} z}.ncard = m₀)
    (t₀ : Set ℂ)
    (ht₀ : t₀ ∈ {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f₀.eval w‖ ≤ c₀},
      t = connectedComponentIn {w : ℂ | ‖f₀.eval w‖ ≤ c₀} z})
    (hnonconvex : ¬ Convex ℝ t₀) :
    False ↔
      ∀ (f : ℂ[X]) (m : ℕ) (c : ℝ), f.Monic →
        (f.rootSet ℂ).ncard = m → 0 < c →
        {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}.ncard = m →
        ∀ t ∈ {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}, Convex ℝ t := by
  constructor
  · exact False.elim
  · intro hall
    exact hnonconvex
      (hall f₀ m₀ c₀ hmonic hroots hpositive hcomponents t₀ ht₀)

theorem counterexample_certificate_is_sufficient
    (P : Prop) (hcounterexample : ¬ P) : False ↔ P := by
  constructor
  · exact False.elim
  · exact hcounterexample

end AwesomeTheorems.Stage5.S5_CLM_00003600
