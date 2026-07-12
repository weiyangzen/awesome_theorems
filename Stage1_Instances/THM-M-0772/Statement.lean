import Mathlib.Order.Preorder.Chain

/-!
# THM-M-0772: Hausdorff maximal principle statement

This module freezes the exact partial-order existence claim. It contains no
proof of Hausdorff's maximal principle.
-/

namespace Stage1Instances.THM_M_0772

universe u

/-- A partially ordered type has an inclusion-maximal chain. -/
def HausdorffMaximalPrinciple : Prop :=
  ∀ (P : Type u) [PartialOrder P], ∃ c : Set P, IsMaxChain (· ≤ ·) c

/-- The same target with `IsMaxChain` expanded at the statement boundary. -/
def ExpandedHausdorffMaximalPrinciple : Prop :=
  ∀ (P : Type u) [PartialOrder P], ∃ c : Set P,
    IsChain (· ≤ ·) c ∧
      ∀ ⦃t : Set P⦄, IsChain (· ≤ ·) t → c ⊆ t → c = t

/-- The expanded encoding is definitionally faithful to the canonical target. -/
theorem hausdorffMaximalPrinciple_iff_expanded :
    HausdorffMaximalPrinciple.{u} ↔ ExpandedHausdorffMaximalPrinciple.{u} := by
  rfl

/- Structural mutations. The checker requires their elaborated expressions to
be different from the canonical expression; none receives proof credit. -/

/-- Removes the partial-order hypothesis and silently fixes equality as the relation. -/
def mutationRemovedPartialOrder : Prop :=
  ∀ (P : Type u), ∃ c : Set P, IsMaxChain (· = ·) c

/-- Changes the arbitrary carrier to the single fixed carrier `Nat`. -/
def mutationChangedDomain : Prop :=
  ∃ c : Set Nat, IsMaxChain (· ≤ ·) c

/-- Moves the carrier from universal to existential binder scope. -/
def mutationChangedBinderScope : Prop :=
  ∃ (P : Type u), ∃ _order : PartialOrder P,
    ∃ c : Set P, @IsMaxChain P _order.le c

/-- Excludes the empty carrier by adding an unnecessary hypothesis. -/
def mutationExcludedEmptyBoundary : Prop :=
  ∀ (P : Type u) [PartialOrder P] [Nonempty P],
    ∃ c : Set P, IsMaxChain (· ≤ ·) c

/-- The canonical target includes the empty partially ordered carrier. -/
theorem emptyBoundary :
    ∃ c : Set Empty, IsMaxChain (· ≤ ·) c := by
  refine ⟨∅, IsChain.empty, ?_⟩
  intro t _ht _hsub
  apply Set.Subset.antisymm
  · exact Set.empty_subset t
  · intro x _hx
    nomatch x

/-- The canonical target includes a singleton partially ordered carrier. -/
theorem singletonBoundary :
    ∃ c : Set Unit, IsMaxChain (· ≤ ·) c := by
  refine ⟨Set.univ, Set.subsingleton_univ.isChain, ?_⟩
  intro t _ht hsub
  exact Set.Subset.antisymm hsub (Set.subset_univ t)

end Stage1Instances.THM_M_0772

set_option pp.explicit true in
#print Stage1Instances.THM_M_0772.HausdorffMaximalPrinciple
