import Statement

/-!
# THM-M-0663 proof work

This module contains the closed degenerate-domain branch of the frozen proof
architecture.  It intentionally does not postulate the missing o-minimal
monotonicity package.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0663

universe u v w

variable {L : Language.{u, v}} {M : Type w}

/-- A subsingleton definable domain is already one permitted partition piece. -/
theorem partition_of_subsingleton
    [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M]
    [TopologicalSpace M]
    {A : Set M} (f : M -> M) (hA : A.Subsingleton) :
    exists pieces : Finset (Set M),
      (forall p, p ∈ pieces ->
        p ⊆ A /\ p.OrdConnected /\ HasMonotoneBehavior f p) /\
      Set.PairwiseDisjoint (pieces : Set (Set M)) id /\
      A = ⋃₀ (pieces : Set (Set M)) := by
  classical
  refine ⟨{A}, ?_, ?_, ?_⟩
  · intro p hp
    have hpA : p = A := Finset.mem_singleton.mp hp
    subst p
    refine ⟨Subset.rfl, ?_, Or.inl hA⟩
    rw [Set.ordConnected_iff]
    intro x hx y hy hxy z hz
    have hxy' : x = y := hA hx hy
    subst y
    have hz' : z = x := le_antisymm hz.2 hz.1
    simpa [hz'] using hx
  · simpa using Set.pairwiseDisjoint_singleton A id
  · simp

/-- The empty-domain boundary, now at the full canonical conclusion. -/
theorem partition_empty
    [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M]
    [TopologicalSpace M] (f : M -> M) :
    exists pieces : Finset (Set M),
      (forall p, p ∈ pieces ->
        p ⊆ (∅ : Set M) /\ p.OrdConnected /\ HasMonotoneBehavior f p) /\
      Set.PairwiseDisjoint (pieces : Set (Set M)) id /\
      (∅ : Set M) = ⋃₀ (pieces : Set (Set M)) := by
  exact partition_of_subsingleton (L := L) f Set.subsingleton_empty

#print axioms partition_of_subsingleton
#print axioms partition_empty

end Stage1Instances.THM_M_0663
