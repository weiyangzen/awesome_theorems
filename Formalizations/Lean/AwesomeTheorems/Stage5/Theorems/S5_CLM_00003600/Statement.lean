/-
import FormalConjectures.ErdosProblems.1047

Frozen source authority: Erdos1047.erdos_1047.  The canonical Lean workspace
does not expose the statement-provider package on its build search path, so
the two reducible provider definitions are unfolded below.  No replacement
constant, notation, alias, macro, or parser rule is introduced.
-/
import Mathlib

open Polynomial

namespace AwesomeTheorems.Stage5.S5_CLM_00003600

theorem source_to_target_statement
    (h : False ↔
      ∀ (f : ℂ[X]) (m : ℕ) (c : ℝ), f.Monic →
        (f.rootSet ℂ).ncard = m → 0 < c →
        {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}.ncard = m →
        ∀ t ∈ {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}, Convex ℝ t) :
    False ↔
      ∀ (f : ℂ[X]) (m : ℕ) (c : ℝ), f.Monic →
        (f.rootSet ℂ).ncard = m → 0 < c →
        {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}.ncard = m →
        ∀ t ∈ {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}, Convex ℝ t := by
  exact h

theorem target_to_source_statement
    (h : False ↔
      ∀ (f : ℂ[X]) (m : ℕ) (c : ℝ), f.Monic →
        (f.rootSet ℂ).ncard = m → 0 < c →
        {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}.ncard = m →
        ∀ t ∈ {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}, Convex ℝ t) :
    False ↔
      ∀ (f : ℂ[X]) (m : ℕ) (c : ℝ), f.Monic →
        (f.rootSet ℂ).ncard = m → 0 < c →
        {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}.ncard = m →
        ∀ t ∈ {t : Set ℂ | ∃ z ∈ {w : ℂ | ‖f.eval w‖ ≤ c},
          t = connectedComponentIn {w : ℂ | ‖f.eval w‖ ≤ c} z}, Convex ℝ t := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003600
