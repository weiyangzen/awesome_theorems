import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
Trust-zero rejection of the standard-sphere shortcut. The standard sphere has
an infinity-smooth identity diffeomorphism, so it cannot satisfy the target's
`IsEmpty` comparison certificate. This is blocker evidence, not a root proof.
-/

noncomputable section

open Metric
open scoped ContDiff Manifold

namespace Stage1.THM_M_0605.Probes

abbrev StandardSevenSphere :=
  sphere (0 : EuclideanSpace ℝ (Fin 8)) 1

theorem standardSevenSphere_self_diffeomorph_not_isEmpty :
    ¬ IsEmpty
      (StandardSevenSphere ≃ₘ⟮𝓡 7, 𝓡 7⟯ StandardSevenSphere) := by
  intro h
  exact h.false (Diffeomorph.refl (𝓡 7) StandardSevenSphere ∞)

#print axioms standardSevenSphere_self_diffeomorph_not_isEmpty

end Stage1.THM_M_0605.Probes
