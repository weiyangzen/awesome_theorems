import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic

open Laplacian Topology

namespace THMM1136StatementProbe

open InnerProductSpace

variable
  {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
  (f : E → F) (x : E) (s : Set E)

/-- The exact type supplied by mathlib for its pointwise-neighborhood notion of harmonicity. -/
example : HarmonicAt f x ↔ ContDiffAt ℝ 2 f x ∧ (Δ f =ᶠ[𝓝 x] 0) := Iff.rfl

/-- The corresponding setwise target is only pointwise quantification of `HarmonicAt`. -/
example : HarmonicOnNhd f s ↔ ∀ y ∈ s, HarmonicAt f y := Iff.rfl

end THMM1136StatementProbe
