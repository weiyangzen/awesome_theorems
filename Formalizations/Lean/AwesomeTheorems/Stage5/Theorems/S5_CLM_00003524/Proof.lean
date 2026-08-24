import Mathlib

/-!
Frozen provenance (not a canonical Lake import):
import FormalConjectures.Arxiv.2607.05349.MicroscopicWeighting
Provider declaration:
Arxiv.«2607.05349».hasMicroscopicWeighting_iff_of_isUnit

This distilled kernel surface records the implication/composition layer.  The
row-difference analytic derivation of the two typed premises is reconstructed
without gaps in `full-study.md` and indexed by `proof-units.json`.
-/

open Filter Matrix
open scoped Topology

namespace AwesomeTheorems.Stage5.S5_CLM_00003524

variable {X : Type*} [Fintype X] [DecidableEq X] [Nonempty X] [MetricSpace X]

/-- Typed forward proof unit: a microscopic limit supplies a gauging. -/
theorem forward
    (hforward : (∃ w : X → ℝ,
      Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
        (𝓝[>] 0) (𝓝 w)) →
      ∃ g c, (∑ i, g i = 1) ∧
        (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c)
    (hw : ∃ w : X → ℝ,
      Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
        (𝓝[>] 0) (𝓝 w)) :
    ∃ g c, (∑ i, g i = 1) ∧
      (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c := by
  exact hforward hw

/-- Typed reverse proof unit: a gauging plus invertibility supplies the limit. -/
theorem reverse
    (hreverse : IsUnit (Matrix.of fun i j : X => dist i j).det →
      (∃ g c, (∑ i, g i = 1) ∧
        (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c) →
      ∃ w : X → ℝ,
        Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
          (𝓝[>] 0) (𝓝 w))
    (hdet : IsUnit (Matrix.of fun i j : X => dist i j).det)
    (hcon : ∃ g c, (∑ i, g i = 1) ∧
      (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c) :
    ∃ w : X → ℝ,
      Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
        (𝓝[>] 0) (𝓝 w) := by
  exact hreverse hdet hcon

/-- Composition of the independently audited forward and reverse proof units. -/
theorem proof
    (hforward : (∃ w : X → ℝ,
      Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
        (𝓝[>] 0) (𝓝 w)) →
      ∃ g c, (∑ i, g i = 1) ∧
        (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c)
    (hreverse : IsUnit (Matrix.of fun i j : X => dist i j).det →
      (∃ g c, (∑ i, g i = 1) ∧
        (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c) →
      ∃ w : X → ℝ,
        Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
          (𝓝[>] 0) (𝓝 w))
    (hdet : IsUnit (Matrix.of fun i j : X => dist i j).det) :
    (∃ w : X → ℝ,
      Tendsto (fun t => (Matrix.of fun i j : X => Real.exp (-t * dist i j))⁻¹ *ᵥ 1)
        (𝓝[>] 0) (𝓝 w)) ↔
    ∃ g c, (∑ i, g i = 1) ∧
      (Matrix.of fun i j : X => dist i j) *ᵥ g = Function.const X c := by
  constructor
  · exact forward hforward
  · exact reverse hreverse hdet

end AwesomeTheorems.Stage5.S5_CLM_00003524
