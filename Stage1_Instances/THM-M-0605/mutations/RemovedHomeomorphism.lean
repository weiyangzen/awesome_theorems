import Mathlib.Geometry.Manifold.Instances.Sphere

noncomputable section
open Metric
open scoped ContDiff Manifold

namespace Stage1.THM_M_0605.Mutation

abbrev S7 := sphere (0 : EuclideanSpace ℝ (Fin 8)) 1

structure M7 where
  Carrier : Type
  topology : TopologicalSpace Carrier
  chartedSpace : ChartedSpace (EuclideanSpace ℝ (Fin 7)) Carrier
  isManifold : letI := topology; letI := chartedSpace; IsManifold (𝓡 7) ω Carrier

def exact : Prop := ∃ M : M7, letI := M.topology; letI := M.chartedSpace
  Nonempty (M.Carrier ≃ₜ S7) ∧ IsEmpty (M.Carrier ≃ₘ⟮𝓡 7, 𝓡 7⟯ S7)

def removedHomeomorphism : Prop := ∃ M : M7, letI := M.topology; letI := M.chartedSpace
  IsEmpty (M.Carrier ≃ₘ⟮𝓡 7, 𝓡 7⟯ S7)

example : exact = removedHomeomorphism := by rfl

end Stage1.THM_M_0605.Mutation
