import Mathlib.Geometry.Manifold.PoincareConjecture

/-! Immutable-anchor probes for THM-M-0605. This file contains no proof of the target. -/

noncomputable section

open Metric
open scoped ContDiff Manifold

namespace Stage1.THM_M_0605

-- Re-elaborated verbatim from `Statement.lean`; that standalone file is not a Lake module.
abbrev StandardSevenSphere := sphere (0 : EuclideanSpace ℝ (Fin 8)) 1

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

namespace AnchorAudit

open Lean Elab Command

/-- Direct expansion of mathlib's source-only exotic-sphere marker. -/
def MathlibMarkerShape : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold (𝓡 7) ω M)
    (_homeo : M ≃ₜ StandardSevenSphere),
    IsEmpty (M ≃ₘ⟮𝓡 7, 𝓡 7⟯ StandardSevenSphere)

/-- The audited marker has exactly the canonical meaning after packaging its instances. -/
theorem exoticSevenSphereExists_iff_mathlibMarkerShape :
    ExoticSevenSphereExists ↔ MathlibMarkerShape := by
  constructor
  · rintro ⟨M, hhomeo, hdiff⟩
    exact ⟨M.Carrier, M.topology, M.chartedSpace, M.isManifold, hhomeo.some, hdiff⟩
  · rintro ⟨M, topology, chartedSpace, isManifold, homeo, hdiff⟩
    let witness : SmoothSevenManifold := ⟨M, topology, chartedSpace, isManifold⟩
    exact ⟨witness, ⟨homeo⟩, hdiff⟩

-- Fail if the source-only `proof_wanted` marker becomes a retained declaration.
run_cmd do
  let marker := `exists_homeomorph_isEmpty_diffeomorph_sphere_seven
  if (← getEnv).contains marker then
    throwError "audit boundary changed: {marker} is now retained"

#check MathlibMarkerShape
#check exoticSevenSphereExists_iff_mathlibMarkerShape

end AnchorAudit
end Stage1.THM_M_0605
