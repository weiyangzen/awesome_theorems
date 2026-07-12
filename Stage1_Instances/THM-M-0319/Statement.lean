import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-0319: exact Brouwer fixed-point statement

This module freezes the finite-dimensional compact-convex statement only. It
contains no proof of Brouwer's fixed-point theorem.
-/

namespace Stage1Instances.THM_M_0319

/-- Real Euclidean `n`-space, including the zero-dimensional case. -/
abbrev RealEuclideanSpace (n : Nat) := EuclideanSpace Real (Fin n)

/-- The exact ambient-map formulation selected for Brouwer's fixed-point theorem. -/
def BrouwerFixedPointTarget : Prop :=
  forall (n : Nat) (K : Set (RealEuclideanSpace n))
    (f : RealEuclideanSpace n -> RealEuclideanSpace n),
    K.Nonempty ->
    IsCompact K ->
    Convex Real K ->
    ContinuousOn f K ->
    Set.MapsTo f K K ->
    exists x, x ∈ K ∧ f x = x

-- Structural mutations elaborate separately; the statement checker requires
-- their explicit expressions to differ from the canonical target.
def mutationRemovedNonempty : Prop :=
  forall (n : Nat) (K : Set (RealEuclideanSpace n))
    (f : RealEuclideanSpace n -> RealEuclideanSpace n),
    IsCompact K -> Convex Real K -> ContinuousOn f K -> Set.MapsTo f K K ->
    exists x, x ∈ K ∧ f x = x

def mutationRemovedMapsTo : Prop :=
  forall (n : Nat) (K : Set (RealEuclideanSpace n))
    (f : RealEuclideanSpace n -> RealEuclideanSpace n),
    K.Nonempty -> IsCompact K -> Convex Real K -> ContinuousOn f K ->
    exists x, x ∈ K ∧ f x = x

def mutationChangedContinuity : Prop :=
  forall (n : Nat) (K : Set (RealEuclideanSpace n))
    (f : RealEuclideanSpace n -> RealEuclideanSpace n),
    K.Nonempty -> IsCompact K -> Convex Real K -> Continuous f ->
    Set.MapsTo f K K -> exists x, x ∈ K ∧ f x = x

def mutationChangedBinderScope : Prop :=
  forall (n : Nat) (K : Set (RealEuclideanSpace n)),
    K.Nonempty -> IsCompact K -> Convex Real K ->
    (forall f : RealEuclideanSpace n -> RealEuclideanSpace n, ContinuousOn f K) ->
    forall f : RealEuclideanSpace n -> RealEuclideanSpace n,
      Set.MapsTo f K K -> exists x, x ∈ K ∧ f x = x

def mutationFixedDimensionThree : Prop :=
  forall (K : Set (RealEuclideanSpace 3))
    (f : RealEuclideanSpace 3 -> RealEuclideanSpace 3),
    K.Nonempty -> IsCompact K -> Convex Real K -> ContinuousOn f K ->
    Set.MapsTo f K K -> exists x, x ∈ K ∧ f x = x

/-- Nonemptiness is sufficient to close the selected target's `n = 0` boundary. -/
theorem zeroDimensionalBoundary (K : Set (RealEuclideanSpace 0))
    (f : RealEuclideanSpace 0 -> RealEuclideanSpace 0) (hK : K.Nonempty) :
    exists x, x ∈ K ∧ f x = x := by
  obtain ⟨x, hx⟩ := hK
  refine ⟨x, hx, ?_⟩
  ext i
  exact Fin.elim0 i

end Stage1Instances.THM_M_0319

set_option pp.explicit true in
#print Stage1Instances.THM_M_0319.BrouwerFixedPointTarget
