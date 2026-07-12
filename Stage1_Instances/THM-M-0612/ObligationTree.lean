import Statement

/-!
# THM-M-0612 conditional obligation composition

This module checks only the final logical composition selected by the frozen
architecture.  The geometric radius-squared obstruction remains an explicit
premise; no nonsqueezing proof is asserted here.
-/

noncomputable section

namespace Stage1.THM_M_0612

universe u

/-- Output expected from the geometric/capacity branch of the architecture. -/
def RadiusSquaredObstruction : Prop :=
  forall (Q : Type u) [Fintype Q] (i : Q) (r R : Real),
    0 < r -> 0 < R ->
    forall f : PhaseSpace Q -> PhaseSpace Q,
      IsSymplecticEmbeddingOnBall r f ->
      Set.MapsTo f (ball r) (cylinder i R) ->
      r ^ 2 <= R ^ 2

/-- The elementary ordered-field transport from squared positive radii. -/
theorem radius_le_of_sq_le
    {r R : Real} (hr : 0 < r) (hR : 0 < R) (h : r ^ 2 <= R ^ 2) : r <= R := by
  nlinarith

/-- Checked conditional composition from the geometric package to the exact root. -/
theorem root_of_radiusSquaredObstruction
    (geometry : RadiusSquaredObstruction.{u}) : StatementShape.{u} := by
  intro Q _fintype i r R hr hR f hf hmaps
  exact radius_le_of_sq_le hr hR (geometry Q i r R hr hR f hf hmaps)

#print axioms radius_le_of_sq_le
#print axioms root_of_radiusSquaredObstruction

end Stage1.THM_M_0612
