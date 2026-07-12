import Mathlib.ModelTheory.Definability
import Mathlib.ModelTheory.Order
import Mathlib.Topology.Order.Basic

/-!
# THM-M-0663: o-minimal monotonicity statement

This module freezes the unary monotonicity theorem selected by the intake.  It
contains definitions of the required statement interface, but no proof of the
monotonicity theorem.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0663

universe u v w

variable {L : Language.{u, v}} {M : Type w}

/-- A structure is o-minimal when every unary set definable with parameters is
a finite union of order-convex sets.  Empty and singleton components are
allowed and can be deleted or merged without changing the condition. -/
def IsOMinimal [L.IsOrdered] [L.Structure M] [LinearOrder M]
    [L.OrderedStructure M] : Prop :=
  forall s : Set M, (Set.univ : Set M).Definable₁ L s ->
    exists pieces : Finset (Set M),
      (forall p, p ∈ pieces -> p.OrdConnected) /\
      s = ⋃₀ (pieces : Set (Set M))

/-- The graph of `f` restricted to its intended domain. -/
def restrictedGraph (A : Set M) (f : M -> M) : Set (Fin 2 -> M) :=
  {p | p 0 ∈ A /\ p 1 = f (p 0)}

/-- The permitted behavior of a unary function on one partition piece. -/
def HasMonotoneBehavior [LinearOrder M] [TopologicalSpace M]
    (f : M -> M) (p : Set M) : Prop :=
  p.Subsingleton \/
    (ContinuousOn f p /\
      ((exists c : M, EqOn f (fun _ => c) p) \/
        StrictMonoOn f p \/ StrictAntiOn f p))

/--
Unary monotonicity for o-minimal structures: a definable unary function on a
definable domain has a finite partition into points and order-convex pieces on
which it is continuous and constant, strictly increasing, or strictly
decreasing.
-/
def OMinimalMonotonicity : Prop :=
  forall (L : Language.{u, v}) (M : Type w)
    [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M]
    [DenselyOrdered M] [NoMinOrder M] [NoMaxOrder M]
    [TopologicalSpace M] [OrderTopology M],
    IsOMinimal (L := L) (M := M) ->
    forall (A : Set M) (f : M -> M),
      (Set.univ : Set M).Definable₁ L A ->
      (Set.univ : Set M).Definable L (restrictedGraph A f) ->
      exists pieces : Finset (Set M),
        (forall p, p ∈ pieces -> p ⊆ A /\ p.OrdConnected /\ HasMonotoneBehavior f p) /\
        Set.PairwiseDisjoint (pieces : Set (Set M)) id /\
        A = ⋃₀ (pieces : Set (Set M))

/-- A direct expansion used to check binder order and scope. -/
theorem oMinimalMonotonicity_iff : OMinimalMonotonicity.{u, v, w} <->
    forall (L : Language.{u, v}) (M : Type w)
      [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M]
      [DenselyOrdered M] [NoMinOrder M] [NoMaxOrder M]
      [TopologicalSpace M] [OrderTopology M],
      IsOMinimal (L := L) (M := M) ->
      forall (A : Set M) (f : M -> M),
        (Set.univ : Set M).Definable₁ L A ->
        (Set.univ : Set M).Definable L (restrictedGraph A f) ->
        exists pieces : Finset (Set M),
          (forall p, p ∈ pieces -> p ⊆ A /\ p.OrdConnected /\ HasMonotoneBehavior f p) /\
          Set.PairwiseDisjoint (pieces : Set (Set M)) id /\
          A = ⋃₀ (pieces : Set (Set M)) := by
  unfold OMinimalMonotonicity
  rfl

-- Structural mutations elaborate as distinct propositions for fingerprinting.
def mutationRemovedOMinimality : Prop :=
  forall (L : Language.{u, v}) (M : Type w)
    [L.Structure M] [LinearOrder M] [TopologicalSpace M] [OrderTopology M]
    (A : Set M) (f : M -> M),
    (Set.univ : Set M).Definable₁ L A ->
    (Set.univ : Set M).Definable L (restrictedGraph A f) ->
    exists pieces : Finset (Set M), A = ⋃₀ (pieces : Set (Set M))

def mutationChangedDomain : Prop :=
  forall (L : Language.{u, v}) (M : Type w)
    [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M],
    IsOMinimal (L := L) (M := M) ->
    forall f : M -> M, exists pieces : Finset (Set M),
      Set.univ = ⋃₀ (pieces : Set (Set M))

def mutationChangedBinderScope : Prop :=
  exists pieces : Finset (Set Nat), forall A : Set Nat,
    A = ⋃₀ (pieces : Set (Set Nat))

def mutationWeakenedConclusion : Prop :=
  forall (L : Language.{u, v}) (M : Type w)
    [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M],
    IsOMinimal (L := L) (M := M) ->
    forall (A : Set M) (f : M -> M), exists pieces : Finset (Set M),
      A = ⋃₀ (pieces : Set (Set M))

/-- The empty domain is intentionally included by the selected statement. -/
theorem emptyDomainPartition :
    exists pieces : Finset (Set M),
      (forall p, p ∈ pieces -> p ⊆ (∅ : Set M)) /\
      Set.PairwiseDisjoint (pieces : Set (Set M)) id /\
      (∅ : Set M) = ⋃₀ (pieces : Set (Set M)) := by
  exact ⟨∅, by simp⟩

end Stage1Instances.THM_M_0663

set_option pp.explicit true in
#print Stage1Instances.THM_M_0663.OMinimalMonotonicity
