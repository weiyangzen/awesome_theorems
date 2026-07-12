import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.Topology.Semicontinuity.Hemicontinuity

/-!
# THM-M-0320: Kakutani fixed-point theorem statement

This module freezes the finite-dimensional Euclidean target corresponding to
Kakutani's 1941 theorem. It intentionally contains no proof of that theorem.
-/

namespace Stage1Instances.THM_M_0320

open Set

/-- Kakutani's fixed-point theorem in the source's closed, bounded Euclidean
form: an upper-hemicontinuous correspondence with nonempty closed convex
values contained in the domain has a fixed point. -/
def KakutaniFixedPointTarget : Prop :=
  forall (n : Nat) (K : Set (EuclideanSpace Real (Fin n)))
      (F : EuclideanSpace Real (Fin n) -> Set (EuclideanSpace Real (Fin n))),
    K.Nonempty ->
    IsClosed K ->
    Bornology.IsBounded K ->
    Convex Real K ->
    (forall x, x ∈ K -> (F x).Nonempty) ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    (forall x, x ∈ K -> Convex Real (F x)) ->
    (forall x, x ∈ K -> F x ⊆ K) ->
    UpperHemicontinuousOn F K ->
    exists x, x ∈ K ∧ x ∈ F x

-- Independently elaborated statement mutations. They receive no proof credit.
def MutationAllowsEmptyDomain : Prop :=
  forall (n : Nat) (K : Set (EuclideanSpace Real (Fin n)))
      (F : EuclideanSpace Real (Fin n) -> Set (EuclideanSpace Real (Fin n))),
    IsClosed K -> Bornology.IsBounded K -> Convex Real K ->
    (forall x, x ∈ K -> (F x).Nonempty) ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    (forall x, x ∈ K -> Convex Real (F x)) ->
    (forall x, x ∈ K -> F x ⊆ K) ->
    UpperHemicontinuousOn F K ->
    exists x, x ∈ K ∧ x ∈ F x

def MutationAllowsEmptyValues : Prop :=
  forall (n : Nat) (K : Set (EuclideanSpace Real (Fin n)))
      (F : EuclideanSpace Real (Fin n) -> Set (EuclideanSpace Real (Fin n))),
    K.Nonempty -> IsClosed K -> Bornology.IsBounded K -> Convex Real K ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    (forall x, x ∈ K -> Convex Real (F x)) ->
    (forall x, x ∈ K -> F x ⊆ K) ->
    UpperHemicontinuousOn F K ->
    exists x, x ∈ K ∧ x ∈ F x

def MutationDropsValueContainment : Prop :=
  forall (n : Nat) (K : Set (EuclideanSpace Real (Fin n)))
      (F : EuclideanSpace Real (Fin n) -> Set (EuclideanSpace Real (Fin n))),
    K.Nonempty -> IsClosed K -> Bornology.IsBounded K -> Convex Real K ->
    (forall x, x ∈ K -> (F x).Nonempty) ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    (forall x, x ∈ K -> Convex Real (F x)) ->
    UpperHemicontinuousOn F K ->
    exists x, x ∈ K ∧ x ∈ F x

def MutationWeakensFixedPoint : Prop :=
  forall (n : Nat) (K : Set (EuclideanSpace Real (Fin n)))
      (F : EuclideanSpace Real (Fin n) -> Set (EuclideanSpace Real (Fin n))),
    K.Nonempty -> IsClosed K -> Bornology.IsBounded K -> Convex Real K ->
    (forall x, x ∈ K -> (F x).Nonempty) ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    (forall x, x ∈ K -> Convex Real (F x)) ->
    (forall x, x ∈ K -> F x ⊆ K) ->
    UpperHemicontinuousOn F K ->
    exists x, x ∈ K

end Stage1Instances.THM_M_0320

set_option pp.explicit true in
#print Stage1Instances.THM_M_0320.KakutaniFixedPointTarget
