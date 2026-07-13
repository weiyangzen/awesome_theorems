import Mathlib.Data.Finset.Slice

/-!
# THM-M-0821: Sperner maximum-size statement

This module freezes the literal catalog claim: the maximum cardinality of an
antichain in a finite Boolean lattice. It states both attainability and the
universal sharp upper bound. The stronger classification of every equality
case in Sperner's 1928 paper is deliberately not added to this target.
-/

namespace Stage1Instances.THM_M_0821

universe u

/-- A finite family of finite subsets in which distinct members are
incomparable under inclusion. -/
def IsSpernerFamily {alpha : Type u} (A : Finset (Finset alpha)) : Prop :=
  IsAntichain (fun x y : Finset alpha => x ⊆ y) (A : Set (Finset alpha))

/-- The lower middle layer of the finite Boolean lattice on `alpha`. -/
def middleLayer (alpha : Type u) [Fintype alpha] : Finset (Finset alpha) :=
  Finset.powersetCard (Fintype.card alpha / 2) Finset.univ

/-- The exact maximum-value form selected from the repository gloss.

For every finite ground type, an antichain of middle-binomial cardinality
exists, and every antichain has at most that cardinality.
-/
def SpernerMaximumTarget : Prop :=
  ∀ (alpha : Type u) [Fintype alpha],
    (∃ A : Finset (Finset alpha),
      IsSpernerFamily A ∧
        A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)) ∧
      ∀ A : Finset (Finset alpha),
        IsSpernerFamily A →
          A.card ≤ Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-- Equivalent concrete-witness form using the lower middle layer. -/
def MiddleLayerMaximumTarget : Prop :=
  ∀ (alpha : Type u) [Fintype alpha],
    IsSpernerFamily (middleLayer alpha) ∧
      (middleLayer alpha).card =
        Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2) ∧
      ∀ A : Finset (Finset alpha),
        IsSpernerFamily A →
          A.card ≤ Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-- The existential maximum-value target and the concrete lower-middle-layer
form are equivalent without importing a proof of Sperner's upper bound. -/
theorem spernerMaximumTarget_iff_middleLayerMaximumTarget :
    SpernerMaximumTarget.{u} ↔ MiddleLayerMaximumTarget.{u} := by
  constructor
  · intro h alpha
    refine ⟨?_, ?_, (h alpha).2⟩
    · simp [IsSpernerFamily, middleLayer]
      exact
        (Set.sized_powersetCard (Finset.univ : Finset alpha)
          (Fintype.card alpha / 2)).isAntichain
    · simp [middleLayer, Finset.card_powersetCard]
  · intro h alpha
    refine ⟨⟨middleLayer alpha, (h alpha).1, (h alpha).2.1⟩, (h alpha).2.2⟩

/-- The selected lower-middle witness includes the empty ground-set case. -/
theorem middleLayer_fin_zero : middleLayer (Fin 0) = {∅} := by
  simp [middleLayer]

/-- For a singleton ground set, the selected lower middle layer has rank zero. -/
theorem middleLayer_fin_one : middleLayer (Fin 1) = {∅} := by
  simp [middleLayer]

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removed-hypothesis mutation: the universal bound no longer assumes the
family is an antichain. -/
def mutationRemovedAntichainHypothesis : Prop :=
  ∀ (alpha : Type u) [Fintype alpha],
    (∃ A : Finset (Finset alpha),
      IsSpernerFamily A ∧
        A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)) ∧
      ∀ A : Finset (Finset alpha),
        A.card ≤ Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-- Changed-domain mutation: family members are `Set alpha` rather than
`Finset alpha`. -/
def mutationChangedSubsetDomain : Prop :=
  ∀ (alpha : Type u) [Fintype alpha],
    (∃ A : Finset (Set alpha),
      IsAntichain (fun x y : Set alpha => x ⊆ y) (A : Set (Set alpha)) ∧
        A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)) ∧
      ∀ A : Finset (Set alpha),
        IsAntichain (fun x y : Set alpha => x ⊆ y) (A : Set (Set alpha)) →
          A.card ≤ Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

/-- Changed-scope mutation: the family binder is existential throughout, so
the conclusion no longer bounds every antichain. -/
def mutationChangedFamilyBinderScope : Prop :=
  ∀ (alpha : Type u) [Fintype alpha],
    ∃ A : Finset (Finset alpha),
      IsSpernerFamily A ∧
        A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2) ∧
          (IsSpernerFamily A →
            A.card ≤ Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2))

/-- Boundary mutation: finite types with no elements are excluded. -/
def mutationExcludesEmptyGroundSet : Prop :=
  ∀ (alpha : Type u) [Fintype alpha],
    0 < Fintype.card alpha →
      (∃ A : Finset (Finset alpha),
        IsSpernerFamily A ∧
          A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)) ∧
        ∀ A : Finset (Finset alpha),
          IsSpernerFamily A →
            A.card ≤ Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2)

#check_failure
  (rfl : SpernerMaximumTarget.{u} = mutationRemovedAntichainHypothesis.{u})
#check_failure
  (rfl : SpernerMaximumTarget.{u} = mutationChangedSubsetDomain.{u})
#check_failure
  (rfl : SpernerMaximumTarget.{u} = mutationChangedFamilyBinderScope.{u})
#check_failure
  (rfl : SpernerMaximumTarget.{u} = mutationExcludesEmptyGroundSet.{u})

#print axioms spernerMaximumTarget_iff_middleLayerMaximumTarget

end Stage1Instances.THM_M_0821

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0821.SpernerMaximumTarget
