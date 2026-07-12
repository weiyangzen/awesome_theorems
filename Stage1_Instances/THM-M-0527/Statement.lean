import Mathlib.Topology.Homotopy.Lifting

/-!
# THM-M-0527: classification of connected pointed covering spaces

This module freezes the statement boundary. It does not prove the classification theorem.
-/

namespace Stage1Instances.THM_M_0527

universe u

noncomputable section

/-- Every point has an open neighborhood whose based loops become trivial in the ambient space. -/
def SemilocallySimplyConnected (X : Type u) [TopologicalSpace X] : Prop :=
  ∀ x : X, ∃ U : Set X, IsOpen U ∧ x ∈ U ∧
    ∀ (u : U) (g : FundamentalGroup U u),
      FundamentalGroup.map
        (⟨Subtype.val, continuous_subtype_val⟩ : C(U, X)) u g = 1

/-- A based, path-connected covering of `(X, x₀)`. All total spaces live in the same
universe as the base; the universe choice is part of the frozen target. -/
structure PointedConnectedCover (X : Type u) [TopologicalSpace X] (x₀ : X) where
  E : Type u
  topology : TopologicalSpace E
  e₀ : E
  p : E → X
  continuous_p : @Continuous E X topology _ p
  covering_p : @IsCoveringMap E X topology _ p
  connected_E : @PathConnectedSpace E topology
  map_basepoint : p e₀ = x₀

namespace PointedConnectedCover

instance {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P : PointedConnectedCover X x₀) : TopologicalSpace P.E := P.topology

instance {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P : PointedConnectedCover X x₀) : PathConnectedSpace P.E := P.connected_E

def continuousMap {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P : PointedConnectedCover X x₀) : C(P.E, X) :=
  ⟨P.p, P.continuous_p⟩

/-- The subgroup assigned to a pointed cover by the induced map on fundamental groups. -/
def inducedSubgroup {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P : PointedConnectedCover X x₀) : Subgroup (FundamentalGroup X x₀) :=
  (FundamentalGroup.mapOfEq P.continuousMap P.map_basepoint).range

/-- Pointed covering isomorphism: a homeomorphism of total spaces over `X` preserving the
chosen lift of `x₀`. -/
def Isomorphic {X : Type u} [TopologicalSpace X] {x₀ : X}
    (P Q : PointedConnectedCover X x₀) : Prop :=
  ∃ h : P.E ≃ₜ Q.E, h P.e₀ = Q.e₀ ∧ ∀ e : P.E, Q.p (h e) = P.p e

end PointedConnectedCover

/-- Exact pointed classification target. The fixed induced-subgroup assignment is onto, and two
pointed connected covers have the same assigned subgroup exactly when they are pointed-isomorphic.
This is the quotient-free expression of a bijection on pointed isomorphism classes. -/
def CoveringSpaceClassificationTarget : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] [PathConnectedSpace X] [LocPathConnectedSpace X]
    (x₀ : X),
    SemilocallySimplyConnected X →
      Function.Surjective
        (PointedConnectedCover.inducedSubgroup (x₀ := x₀)) ∧
      ∀ P Q : PointedConnectedCover X x₀,
        PointedConnectedCover.inducedSubgroup P =
            PointedConnectedCover.inducedSubgroup Q ↔
          PointedConnectedCover.Isomorphic P Q

-- Structural mutations are elaborated separately for statement-boundary comparison.
def mutationRemovedSemilocalHypothesis : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] [PathConnectedSpace X] [LocPathConnectedSpace X]
    (x₀ : X),
      Function.Surjective
        (PointedConnectedCover.inducedSubgroup (x₀ := x₀)) ∧
      ∀ P Q : PointedConnectedCover X x₀,
        PointedConnectedCover.inducedSubgroup P =
            PointedConnectedCover.inducedSubgroup Q ↔
          PointedConnectedCover.Isomorphic P Q

def mutationRemovedLocalPathConnectedness : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] [PathConnectedSpace X] (x₀ : X),
    SemilocallySimplyConnected X →
      Function.Surjective
        (PointedConnectedCover.inducedSubgroup (x₀ := x₀)) ∧
      ∀ P Q : PointedConnectedCover X x₀,
        PointedConnectedCover.inducedSubgroup P =
            PointedConnectedCover.inducedSubgroup Q ↔
          PointedConnectedCover.Isomorphic P Q

def mutationExistenceOnly : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] [PathConnectedSpace X] [LocPathConnectedSpace X]
    (x₀ : X), SemilocallySimplyConnected X →
      Function.Surjective
        (PointedConnectedCover.inducedSubgroup (x₀ := x₀))

end

end Stage1Instances.THM_M_0527

set_option pp.explicit true in
#print Stage1Instances.THM_M_0527.CoveringSpaceClassificationTarget
