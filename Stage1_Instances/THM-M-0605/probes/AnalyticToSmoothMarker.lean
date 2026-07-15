import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
Trust-zero proof-phase probe for the only valid direction between the frozen
analytic target and the infinity-smooth shape of mathlib's source marker.
This implication is diagnostic evidence only; it does not prove either
existence statement.
-/

noncomputable section

open Metric
open scoped ContDiff Manifold

namespace Stage1.THM_M_0605.Probes

abbrev StandardSevenSphere :=
  sphere (0 : EuclideanSpace ℝ (Fin 8)) 1

structure AnalyticSevenManifold where
  Carrier : Type
  topology : TopologicalSpace Carrier
  chartedSpace : ChartedSpace (EuclideanSpace ℝ (Fin 7)) Carrier
  isManifold :
    letI := topology
    letI := chartedSpace
    IsManifold (𝓡 7) ω Carrier

def FrozenAnalyticTarget : Prop :=
  ∃ M : AnalyticSevenManifold,
    letI := M.topology
    letI := M.chartedSpace
    letI := M.isManifold
    Nonempty (M.Carrier ≃ₜ StandardSevenSphere) ∧
      IsEmpty (M.Carrier ≃ₘ⟮𝓡 7, 𝓡 7⟯ StandardSevenSphere)

def ActualSmoothMarkerShape : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold (𝓡 7) ∞ M)
    (_homeo : M ≃ₜ StandardSevenSphere),
    IsEmpty (M ≃ₘ⟮𝓡 7, 𝓡 7⟯ StandardSevenSphere)

/-- Analytic manifolds are smooth, so the stronger frozen shape implies the
actual infinity-smooth marker shape. No reverse instance is available. -/
theorem frozenAnalyticTarget_implies_actualSmoothMarkerShape :
    FrozenAnalyticTarget → ActualSmoothMarkerShape := by
  rintro ⟨M, hHome, hNotDiff⟩
  letI : TopologicalSpace M.Carrier := M.topology
  letI : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M.Carrier := M.chartedSpace
  letI : IsManifold (𝓡 7) ω M.Carrier := M.isManifold
  let smooth : IsManifold (𝓡 7) ∞ M.Carrier := inferInstance
  exact ⟨M.Carrier, M.topology, M.chartedSpace, smooth, hHome.some, hNotDiff⟩

#print axioms frozenAnalyticTarget_implies_actualSmoothMarkerShape

end Stage1.THM_M_0605.Probes
