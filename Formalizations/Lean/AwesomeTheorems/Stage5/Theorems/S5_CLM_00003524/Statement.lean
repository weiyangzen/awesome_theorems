import Mathlib

/-!
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Arxiv.2607.05349.MicroscopicWeighting
Provider declaration:
Arxiv.«2607.05349».hasMicroscopicWeighting_iff_of_isUnit

The canonical files use `Mathlib` and independently prove the expanded
claim-owned proposition, without referring to the provider theorem body.
-/

open Filter Matrix
open scoped Topology

namespace AwesomeTheorems.Stage5.S5_CLM_00003524

variable {X : Type*} [Fintype X] [DecidableEq X] [Nonempty X] [MetricSpace X]

/-- Exact expanded shape of the frozen proposition. -/
theorem statement_shape
    (h : IsUnit (Matrix.of fun i j : X => dist i j).det)
    (p : (∃ w : X → ℝ,
        Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
          (𝓝[>] 0) (𝓝 w)) ↔
      ∃ g c, (∑ i, g i = 1) ∧
        (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c) :
    (∃ w : X → ℝ,
        Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
          (𝓝[>] 0) (𝓝 w)) ↔
      ∃ g c, (∑ i, g i = 1) ∧
        (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c := by
  exact p

end AwesomeTheorems.Stage5.S5_CLM_00003524
