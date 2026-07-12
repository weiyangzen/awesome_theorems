import Mathlib.Geometry.Manifold.PoincareConjecture

/-! Immutable-anchor probes for THM-M-0578. No proof of the target is claimed. -/

namespace Stage1Instances.THM_M_0578.AnchorAudit

open Lean Elab Command
open scoped Manifold ContDiff
open Metric (sphere)

noncomputable section

/-- Direct expansion of the exact source-level marker at the audited pin. -/
def MathlibSourceMarkerShape : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 7)) ∞ M)
    (_homeo : M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 8)) 1),
    IsEmpty
      (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)), 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
        sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)

example : ChartedSpace (EuclideanSpace ℝ (Fin 7))
    (sphere (0 : EuclideanSpace ℝ (Fin 8)) 1) := inferInstance

example : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 7)) ∞
    (sphere (0 : EuclideanSpace ℝ (Fin 8)) 1) := by infer_instance

-- Fail if the source-only `proof_wanted` name becomes a retained declaration.
run_cmd do
  let marker := `exists_homeomorph_isEmpty_diffeomorph_sphere_seven
  if (← getEnv).contains marker then
    throwError "audit boundary changed: {marker} is now retained"

#check MathlibSourceMarkerShape
#check EuclideanSpace.instChartedSpaceSphere
#check EuclideanSpace.instIsManifoldSphere

end
end Stage1Instances.THM_M_0578.AnchorAudit
