import Statement

/-!
# THM-M-0663 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the proved subsingleton-domain result directly against the frozen
statement interface. It does not prove the o-minimal monotonicity root or the
full frozen degenerate-branch obligation.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0663.Validation

universe u v w

variable {L : Language.{u, v}} {M : Type w}

theorem partitionOfSubsingletonDirect
    [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M]
    [TopologicalSpace M]
    {A : Set M} (f : M -> M) (hA : A.Subsingleton) :
    exists pieces : Finset (Set M),
      (forall p, p ∈ pieces ->
        p ⊆ A /\ p.OrdConnected /\ HasMonotoneBehavior f p) /\
      Set.PairwiseDisjoint (pieces : Set (Set M)) id /\
      A = ⋃₀ (pieces : Set (Set M)) := by
  classical
  rcases A.eq_empty_or_nonempty with rfl | hne
  · exact ⟨∅, by simp⟩
  · obtain ⟨a, ha⟩ := hne
    have hAeq : A = {a} := Set.eq_singleton_iff_unique_mem.mpr
      ⟨ha, fun x hx => hA hx ha⟩
    subst A
    refine ⟨{{a}}, ?_, ?_, ?_⟩
    · intro p hp
      have hpA : p = {a} := Finset.mem_singleton.mp hp
      subst p
      exact ⟨Subset.rfl, Set.ordConnected_singleton, Or.inl Set.subsingleton_singleton⟩
    · simpa using Set.pairwiseDisjoint_singleton ({a} : Set M) id
    · simp

theorem partitionEmptyDirect
    [L.IsOrdered] [L.Structure M] [LinearOrder M] [L.OrderedStructure M]
    [TopologicalSpace M] (f : M -> M) :
    exists pieces : Finset (Set M),
      (forall p, p ∈ pieces ->
        p ⊆ (∅ : Set M) /\ p.OrdConnected /\ HasMonotoneBehavior f p) /\
      Set.PairwiseDisjoint (pieces : Set (Set M)) id /\
      (∅ : Set M) = ⋃₀ (pieces : Set (Set M)) := by
  exact partitionOfSubsingletonDirect (L := L) f Set.subsingleton_empty

#print axioms partitionOfSubsingletonDirect
#print axioms partitionEmptyDirect

end Stage1Instances.THM_M_0663.Validation
