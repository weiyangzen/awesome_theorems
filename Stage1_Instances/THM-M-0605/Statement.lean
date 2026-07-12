import Mathlib.Geometry.Manifold.Instances.Sphere

noncomputable section

open Metric
open scoped ContDiff Manifold

namespace Stage1.THM_M_0605

/-- The standard smooth seven-sphere, realized as the unit sphere in `R^8`. -/
abbrev StandardSevenSphere :=
  sphere (0 : EuclideanSpace ℝ (Fin 8)) 1

/-- An abstract smooth real seven-manifold, including its chosen smooth structure. -/
structure SmoothSevenManifold where
  Carrier : Type
  topology : TopologicalSpace Carrier
  chartedSpace : ChartedSpace (EuclideanSpace ℝ (Fin 7)) Carrier
  isManifold :
    letI := topology
    letI := chartedSpace
    IsManifold (𝓡 7) ω Carrier

/-- The exact proposition that a smooth exotic seven-sphere exists. -/
def ExoticSevenSphereExists : Prop :=
  ∃ M : SmoothSevenManifold,
    letI := M.topology
    letI := M.chartedSpace
    letI := M.isManifold
    Nonempty (M.Carrier ≃ₜ StandardSevenSphere) ∧
      IsEmpty (M.Carrier ≃ₘ⟮𝓡 7, 𝓡 7⟯ StandardSevenSphere)

end Stage1.THM_M_0605

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1.THM_M_0605.ExoticSevenSphereExists
