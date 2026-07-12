import Mathlib.Geometry.Manifold.Instances.Sphere

/-! Checked composition interface for the frozen THM-M-0605 architecture. -/

noncomputable section

open Metric
open scoped ContDiff Manifold

namespace Stage1.THM_M_0605

abbrev StandardSevenSphere :=
  sphere (0 : EuclideanSpace ℝ (Fin 8)) 1

structure SmoothSevenManifold where
  Carrier : Type
  topology : TopologicalSpace Carrier
  chartedSpace : ChartedSpace (EuclideanSpace ℝ (Fin 7)) Carrier
  isManifold :
    letI := topology
    letI := chartedSpace
    IsManifold (𝓡 7) ω Carrier

def ExoticSevenSphereExists : Prop :=
  ∃ M : SmoothSevenManifold,
    letI := M.topology
    letI := M.chartedSpace
    letI := M.isManifold
    Nonempty (M.Carrier ≃ₜ StandardSevenSphere) ∧
      IsEmpty (M.Carrier ≃ₘ⟮𝓡 7, 𝓡 7⟯ StandardSevenSphere)

/-- The terminal assembly consumes the constructed manifold and both exact comparison
certificates. It does not construct any of these three inputs. -/
theorem exoticSevenSphereExists_of_witness
    (M : SmoothSevenManifold)
    (hHome :
      letI := M.topology
      Nonempty (M.Carrier ≃ₜ StandardSevenSphere))
    (hNotDiff :
      letI := M.topology
      letI := M.chartedSpace
      letI := M.isManifold
      IsEmpty (M.Carrier ≃ₘ⟮𝓡 7, 𝓡 7⟯ StandardSevenSphere)) :
    ExoticSevenSphereExists := by
  refine ⟨M, ?_⟩
  exact ⟨hHome, hNotDiff⟩

#check exoticSevenSphereExists_of_witness
#print axioms exoticSevenSphereExists_of_witness

end Stage1.THM_M_0605
