import Mathlib.GroupTheory.Sylow

/-!
# THM-M-0072 canonical Lean statement

This module freezes Thompson's printed 1968 Lemma 5.38(a)(i). It states only the target,
checked statement transport, mutation fixtures, and boundary facts; it does not prove the lemma.
-/

namespace Stage1Instances.THM_M_0072

universe u

/-- The source premise that the ambient group has no subgroup of index two. -/
def NoIndexTwoSubgroup (G : Type u) [Group G] : Prop :=
  forall H : Subgroup G, H.index != 2

/--
Thompson's transfer lemma, in the universal form printed as Lemma 5.38(a)(i): every involution
of a Sylow 2-subgroup has an ambient-group conjugate in each maximal subgroup of that Sylow
subgroup.
-/
def ThompsonTransferLemmaTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) -> NoIndexTwoSubgroup G ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        forall u : S, orderOf u = 2 ->
          exists m : M, IsConj (u : G) ((m : S) : G)

/-- The common modern formulation restricts the involution to the complement of `M`. -/
def OutsideMaximalTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) -> NoIndexTwoSubgroup G ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        forall u : S, u ∉ M -> orderOf u = 2 ->
          exists m : M, IsConj (u : G) ((m : S) : G)

/-- The same printed root with involution order measured after coercion to the ambient group. -/
def AmbientOrderTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) -> NoIndexTwoSubgroup G ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        forall u : S, orderOf (u : G) = 2 ->
          exists m : M, IsConj (u : G) ((m : S) : G)

/--
The printed universal form and the common outside-maximal form are equivalent: an involution
already in `M` is its own conjugate there.
-/
theorem thompsonTransferLemmaTarget_iff_outsideMaximalTarget :
    ThompsonTransferLemmaTarget.{u} <-> OutsideMaximalTarget.{u} := by
  constructor
  · intro h G _ _ hEven hIndex S M hM u _ hu
    exact h G hEven hIndex S M hM u hu
  · intro h G _ _ hEven hIndex S M hM u hu
    by_cases hum : u ∈ M
    · exact ⟨⟨u, hum⟩, IsConj.refl _⟩
    · exact h G hEven hIndex S M hM u hum hu

/-- The subgroup carrier does not change element order. -/
theorem thompsonTransferLemmaTarget_iff_ambientOrderTarget :
    ThompsonTransferLemmaTarget.{u} <-> AmbientOrderTarget.{u} := by
  simp only [ThompsonTransferLemmaTarget, AmbientOrderTarget, Subgroup.orderOf_coe]

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedNoIndexTwoHypothesis : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        forall u : S, orderOf u = 2 ->
          exists m : M, IsConj (u : G) ((m : S) : G)

def mutationChangedDomainToCommutativeGroups : Prop :=
  forall (G : Type u) [CommGroup G] [Finite G],
    Even (Nat.card G) -> NoIndexTwoSubgroup G ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        forall u : S, orderOf u = 2 ->
          exists m : M, IsConj (u : G) ((m : S) : G)

def mutationChangedBinderScope : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) -> NoIndexTwoSubgroup G ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        exists m : M, forall u : S, orderOf u = 2 ->
          IsConj (u : G) ((m : S) : G)

def mutationChangedOrderBoundary : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) -> NoIndexTwoSubgroup G ->
      forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
        forall u : S, orderOf u = 4 ->
          exists m : M, IsConj (u : G) ((m : S) : G)

variable
  (hRemoved : mutationRemovedNoIndexTwoHypothesis.{u})
  (hDomain : mutationChangedDomainToCommutativeGroups.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationChangedOrderBoundary.{u})

#check_failure (hRemoved : ThompsonTransferLemmaTarget.{u})
#check_failure (hDomain : ThompsonTransferLemmaTarget.{u})
#check_failure (hScope : ThompsonTransferLemmaTarget.{u})
#check_failure (hBoundary : ThompsonTransferLemmaTarget.{u})

/-- An involution already in `M` satisfies the printed conclusion without transfer theory. -/
theorem insideMaximal_hasConjugate
    {G : Type u} [Group G] {S : Sylow 2 G} (M : Subgroup S) (u : S) (hu : u ∈ M) :
    exists m : M, IsConj (u : G) ((m : S) : G) :=
  ⟨⟨u, hu⟩, IsConj.refl _⟩

#check thompsonTransferLemmaTarget_iff_outsideMaximalTarget
#check thompsonTransferLemmaTarget_iff_ambientOrderTarget
#print axioms thompsonTransferLemmaTarget_iff_outsideMaximalTarget
#print axioms thompsonTransferLemmaTarget_iff_ambientOrderTarget
#print axioms insideMaximal_hasConjugate

set_option pp.universes true in
set_option pp.explicit true in
#print ThompsonTransferLemmaTarget

end Stage1Instances.THM_M_0072
