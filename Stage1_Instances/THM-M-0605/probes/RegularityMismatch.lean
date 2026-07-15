import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
Trust-zero proof-phase probes for the regularity mismatch in the frozen
THM-M-0605 target. These checks establish a blocker; they do not prove the
existence of an exotic seven-sphere.
-/

noncomputable section

open scoped ContDiff Manifold

namespace Stage1.THM_M_0605.Probes

/-- The frozen target's `omega` regularity is not mathlib's infinity-smooth
regularity used by the pinned source marker. -/
theorem analyticOrder_ne_smoothOrder :
    (ω : WithTop ENat) ≠ ∞ := by
  decide

#print axioms analyticOrder_ne_smoothOrder

section RegularityDirections

variable (M : Type) [TopologicalSpace M]
  [ChartedSpace (EuclideanSpace ℝ (Fin 7)) M]

/-- An analytic manifold supplies the weaker infinity-smooth instance. -/
example [IsManifold (𝓡 7) ω M] : IsManifold (𝓡 7) ∞ M := by
  infer_instance

end RegularityDirections

-- Batteries' `proof_wanted` marker is source-only and is discarded on import.
#check_failure exists_homeomorph_isEmpty_diffeomorph_sphere_seven

end Stage1.THM_M_0605.Probes
