import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0583 immutable anchor-audit probe

This file checks the type of the strongest usable local infrastructure at the
pinned mathlib revision.  The generalized Poincare declaration in the imported
source is a `proof_wanted` marker and is deliberately not referenced as a Lean
constant.
-/

noncomputable section

open Metric ContinuousMap
open scoped Manifold

namespace Stage1Instances.THM_M_0583.AnchorAudit

universe u

abbrev FourModel := EuclideanSpace ℝ (Fin 4)
abbrev FourSphere := sphere (0 : EuclideanSpace ℝ (Fin 5)) 1

/-- The exact audited candidate type, including the dossier's compactness binder. -/
def ExactCandidateType : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [CompactSpace M]
    [ChartedSpace FourModel M],
      M ≃ₕ FourSphere → Nonempty (M ≃ₜ FourSphere)

/-- A checked sanity endpoint, not a proof for arbitrary four-manifolds. -/
theorem fourSphere_self_homeomorph : Nonempty (FourSphere ≃ₜ FourSphere) :=
  ⟨Homeomorph.refl FourSphere⟩

theorem exactCandidateType_expands :
    ExactCandidateType.{u} ↔
      ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [CompactSpace M]
        [ChartedSpace (EuclideanSpace ℝ (Fin 4)) M],
          M ≃ₕ sphere (0 : EuclideanSpace ℝ (Fin 5)) 1 →
            Nonempty (M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 5)) 1) :=
  Iff.rfl

#check ExactCandidateType
#check fourSphere_self_homeomorph
#print axioms fourSphere_self_homeomorph

end Stage1Instances.THM_M_0583.AnchorAudit
