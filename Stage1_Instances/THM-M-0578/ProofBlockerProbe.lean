import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0578 proof-boundary probes

These checks reject two invalid shortcuts. They do not construct an exotic
seven-sphere and therefore do not close the canonical target.
-/

namespace Stage1Instances.THM_M_0578.ProofBlockerProbe

open Lean Elab Command
open scoped Manifold ContDiff
open Metric (sphere)

noncomputable section

/-- The standard smooth sphere cannot witness the target: its identity map is
an infinity-smooth self-diffeomorphism. -/
theorem standardSphereSelfDiffeomorphNotEmpty :
    ¬ IsEmpty
      (Diffeomorph
        (modelWithCornersSelf ℝ (EuclideanSpace ℝ (Fin 7)))
        (modelWithCornersSelf ℝ (EuclideanSpace ℝ (Fin 7)))
        (sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)
        (sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)
        ∞) := by
  intro h
  exact h.false
    (Diffeomorph.refl
      (modelWithCornersSelf ℝ (EuclideanSpace ℝ (Fin 7)))
      (sphere (0 : EuclideanSpace ℝ (Fin 8)) 1) ∞)

#print axioms standardSphereSelfDiffeomorphNotEmpty

-- The exact mathlib signature is a discarded source marker, not a theorem.
#check_failure exists_homeomorph_isEmpty_diffeomorph_sphere_seven

run_cmd do
  let marker := `exists_homeomorph_isEmpty_diffeomorph_sphere_seven
  if (← getEnv).contains marker then
    throwError "discarded source marker unexpectedly retained: {marker}"

end
end Stage1Instances.THM_M_0578.ProofBlockerProbe
