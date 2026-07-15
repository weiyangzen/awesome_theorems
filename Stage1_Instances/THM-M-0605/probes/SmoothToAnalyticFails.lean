import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
Expected-negative probe: an infinity-smooth `IsManifold` instance does not
synthesize the analytic instance demanded by the frozen THM-M-0605 target.
-/

noncomputable section

open scoped ContDiff Manifold

namespace Stage1.THM_M_0605.Probes

variable (M : Type) [TopologicalSpace M]
  [ChartedSpace (EuclideanSpace ℝ (Fin 7)) M]
  [IsManifold (𝓡 7) ∞ M]

#synth IsManifold (𝓡 7) ω M

end Stage1.THM_M_0605.Probes
