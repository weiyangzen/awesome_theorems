import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0579: immutable anchor probes

These probes check nearby APIs in the pinned mathlib snapshot. The source
module contains only a discarded `proof_wanted` signature for the terminal
three-dimensional theorem, so none of these declarations closes the target.
-/

open scoped Manifold

namespace Stage1Instances.THMM0579.AnchorAudit

abbrev ModelSpace3 : Type := EuclideanSpace ℝ (Fin 3)
abbrev Sphere3 : Type := Metric.sphere (0 : EuclideanSpace ℝ (Fin 4)) (1 : ℝ)

/-- The target sphere has the object-model instances expected by the statement. -/
def SphereObjectModel : Prop :=
  Nonempty (ChartedSpace ModelSpace3 Sphere3) ∧ CompactSpace Sphere3

theorem sphere_object_model : SphereObjectModel := by
  exact ⟨⟨inferInstance⟩, inferInstance⟩

/-- Simple connectedness supplies the connectedness implicit in the human claim. -/
theorem simplyConnected_implies_pathConnected
    (M : Type*) [TopologicalSpace M] [SimplyConnectedSpace M] :
    PathConnectedSpace M := by
  infer_instance

#check EuclideanSpace.instChartedSpaceSphere
#check EuclideanSpace.instIsManifoldSphere
#check SimplyConnectedSpace.equiv_unit
#check SimplyConnectedSpace.paths_homotopic
#check simplyConnectedSpace_iff
#check sphere_object_model
#check simplyConnected_implies_pathConnected

end Stage1Instances.THMM0579.AnchorAudit
