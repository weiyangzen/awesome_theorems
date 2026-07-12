import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0578: exact Milnor exotic seven-sphere statement

This module freezes and checks the statement boundary only. It does not prove
the existence of an exotic sphere.
-/

namespace Stage1Instances.THM_M_0578

open scoped Manifold ContDiff

open Metric (sphere)

/-- The exact seven-dimensional exotic-sphere existence target selected from
the repository's two source records and Milnor's historical result. -/
def MilnorExoticSphereTarget : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 7)) ∞ M)
    (_homeo : M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 8)) 1),
    IsEmpty
      (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)), 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
        sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)

/-- Direct local expansion of the historical seven-sphere claim and of
mathlib's statement candidate. -/
def PinnedCandidateSourceShape : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 7)) ∞ M)
    (_homeo : M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 8)) 1),
    IsEmpty
      (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)), 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
        sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)

/-- Checked identity with the directly expanded source shape. -/
theorem milnorExoticSphereTarget_iff_pinnedCandidateSourceShape :
    MilnorExoticSphereTarget ↔ PinnedCandidateSourceShape := by
  rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationChangedDimension : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 6)) M)
    (_ : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 6)) ∞ M)
    (_homeo : M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 7)) 1),
    IsEmpty
      (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 6)), 𝓘(ℝ, EuclideanSpace ℝ (Fin 6))⟯
        sphere (0 : EuclideanSpace ℝ (Fin 7)) 1)

def mutationRemovedHomeomorphism : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 7)) ∞ M),
    IsEmpty
      (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)), 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
        sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)

def mutationRemovedSmoothManifold : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_homeo : M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 8)) 1),
    IsEmpty
      (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)), 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
        sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)

def mutationAllowsDiffeomorphism : Prop :=
  ∃ (M : Type) (_ : TopologicalSpace M)
    (_ : ChartedSpace (EuclideanSpace ℝ (Fin 7)) M)
    (_ : IsManifold 𝓘(ℝ, EuclideanSpace ℝ (Fin 7)) ∞ M)
    (_homeo : M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 8)) 1),
    Nonempty
      (M ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)), 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
        sphere (0 : EuclideanSpace ℝ (Fin 8)) 1)

end Stage1Instances.THM_M_0578

set_option pp.explicit true in
#print Stage1Instances.THM_M_0578.MilnorExoticSphereTarget
