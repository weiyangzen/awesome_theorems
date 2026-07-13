import Mathlib.Combinatorics.SetFamily.Intersecting
import Mathlib.Data.Finset.Slice

/-!
# THM-M-0822: Erdos-Ko-Rado maximum-size statement

This module freezes the standard uniform-family maximum-value form selected
from the repository gloss "maximum size of an intersecting family." It states
both attainability by a star and the universal sharp upper bound. It does not
classify all extremal families, especially at the boundary `n = 2 * r`.
-/

namespace Stage1Instances.THM_M_0822

open Finset

/-- The exact maximum-value form selected from the repository gloss.

For every positive rank `r` with `r <= n / 2`, some intersecting family of
`r`-subsets of `Fin n` has cardinality `choose (n - 1) (r - 1)`, and every
such family has at most that cardinality.
-/
def ErdosKoRadoMaximumTarget : Prop :=
  ∀ (n r : Nat), 1 ≤ r → r ≤ n / 2 →
    (∃ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting ∧
      (A : Set (Finset (Fin n))).Sized r ∧
      A.card = (n - 1).choose (r - 1)) ∧
    ∀ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting →
      (A : Set (Finset (Fin n))).Sized r →
      A.card ≤ (n - 1).choose (r - 1)

/-- The star of all `r`-subsets of `Fin n` containing `x`. -/
def erdosKoRadoStar (n r : Nat) (x : Fin n) : Finset (Finset (Fin n)) :=
  (powersetCard r Finset.univ).filter fun s => x ∈ s

/-- A star is the image of the `(r - 1)`-subsets avoiding its center. -/
theorem erdosKoRadoStar_eq_image (n r : Nat) (x : Fin n) (hr : 1 ≤ r) :
    erdosKoRadoStar n r x =
      (powersetCard (r - 1) (Finset.univ.erase x)).image (insert x) := by
  ext s
  simp only [erdosKoRadoStar, mem_filter, mem_powersetCard, mem_image]
  constructor
  · rintro ⟨⟨_hsub, hcard⟩, hxs⟩
    refine ⟨s.erase x, ⟨?_, ?_⟩, insert_erase hxs⟩
    · exact fun y hy => mem_erase.2 ⟨(mem_erase.1 hy).1, mem_univ y⟩
    · rw [card_erase_of_mem hxs, hcard]
  · rintro ⟨a, ⟨ha, hcard⟩, rfl⟩
    have hxa : x ∉ a := fun hx => (mem_erase.1 (ha hx)).1 rfl
    refine ⟨⟨fun _ _ => mem_univ _, ?_⟩, mem_insert_self ..⟩
    rw [card_insert_of_notMem hxa, hcard, Nat.sub_add_cancel hr]

/-- Every star is intersecting. -/
theorem erdosKoRadoStar_intersecting (n r : Nat) (x : Fin n) :
    (erdosKoRadoStar n r x : Set (Finset (Fin n))).Intersecting := by
  intro s hs t ht hDisjoint
  exact
    (Finset.disjoint_left.1 hDisjoint) (mem_filter.1 hs).2
      (mem_filter.1 ht).2

/-- Every member of an `r`-star has cardinality `r`. -/
theorem erdosKoRadoStar_sized (n r : Nat) (x : Fin n) :
    (erdosKoRadoStar n r x : Set (Finset (Fin n))).Sized r := by
  intro s hs
  exact (mem_powersetCard.1 (mem_filter.1 hs).1).2

/-- For positive uniform families, mathlib's self-pair intersecting predicate
agrees with the source convention that checks only distinct pairs. -/
theorem sized_intersecting_iff_pairwise {n r : Nat}
    {A : Finset (Finset (Fin n))} (hr : 1 ≤ r)
    (hSized : (A : Set (Finset (Fin n))).Sized r) :
    (A : Set (Finset (Fin n))).Intersecting ↔
      (A : Set (Finset (Fin n))).Pairwise fun s t => ¬Disjoint s t := by
  rw [Set.intersecting_iff_pairwise_not_disjoint]
  refine and_iff_left ?_
  intro hEq
  have hmemSet : (∅ : Finset (Fin n)) ∈ (A : Set (Finset (Fin n))) := by
    rw [hEq]
    exact Set.mem_singleton _
  have hzero : r = 0 := (hSized hmemSet).symm.trans Finset.card_empty
  omega

/-- A positive-rank star has the claimed extremal cardinality. -/
theorem card_erdosKoRadoStar (n r : Nat) (x : Fin n) (hr : 1 ≤ r) :
    (erdosKoRadoStar n r x).card = (n - 1).choose (r - 1) := by
  rw [erdosKoRadoStar_eq_image n r x hr, card_image_of_injOn]
  · rw [card_powersetCard, card_erase_of_mem (mem_univ x), card_univ,
      Fintype.card_fin]
  · intro a ha b hb hab
    have hxa : x ∉ a :=
      fun hx => (mem_erase.1 ((mem_powersetCard.1 ha).1 hx)).1 rfl
    have hxb : x ∉ b :=
      fun hx => (mem_erase.1 ((mem_powersetCard.1 hb).1 hx)).1 rfl
    simpa [hxa, hxb] using congrArg (erase · x) hab

/-- The parameter range supplies a ground element and hence an attaining star. -/
theorem erdosKoRadoStar_attains (n r : Nat) (hr : 1 ≤ r)
    (hhalf : r ≤ n / 2) :
    ∃ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting ∧
      (A : Set (Finset (Fin n))).Sized r ∧
      A.card = (n - 1).choose (r - 1) := by
  have hn2 : 0 < n / 2 := lt_of_lt_of_le Nat.zero_lt_one (hr.trans hhalf)
  let x : Fin n := ⟨0, Nat.pos_of_div_pos hn2⟩
  exact ⟨erdosKoRadoStar n r x, erdosKoRadoStar_intersecting n r x,
    erdosKoRadoStar_sized n r x, card_erdosKoRadoStar n r x hr⟩

/-- Equivalent form that chooses a concrete star as the attaining family. -/
def ConcreteStarMaximumTarget : Prop :=
  ∀ (n r : Nat), 1 ≤ r → r ≤ n / 2 →
    (∃ x : Fin n,
      (erdosKoRadoStar n r x : Set (Finset (Fin n))).Intersecting ∧
      (erdosKoRadoStar n r x : Set (Finset (Fin n))).Sized r ∧
      (erdosKoRadoStar n r x).card = (n - 1).choose (r - 1)) ∧
    ∀ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting →
      (A : Set (Finset (Fin n))).Sized r →
      A.card ≤ (n - 1).choose (r - 1)

/-- The existential maximum target and concrete-star form are equivalent
without importing the proof-bearing EKR module. -/
theorem erdosKoRadoMaximumTarget_iff_concreteStarMaximumTarget :
    ErdosKoRadoMaximumTarget ↔ ConcreteStarMaximumTarget := by
  constructor
  · intro h n r hr hhalf
    have hn2 : 0 < n / 2 := lt_of_lt_of_le Nat.zero_lt_one (hr.trans hhalf)
    let x : Fin n := ⟨0, Nat.pos_of_div_pos hn2⟩
    exact ⟨⟨x, erdosKoRadoStar_intersecting n r x,
      erdosKoRadoStar_sized n r x, card_erdosKoRadoStar n r x hr⟩,
      (h n r hr hhalf).2⟩
  · intro h n r hr hhalf
    exact ⟨erdosKoRadoStar_attains n r hr hhalf, (h n r hr hhalf).2⟩

/-! Kernel-checked parameter boundaries. -/

/-- No positive rank is admissible for an empty ground set. -/
theorem no_admissible_rank_fin_zero : ∀ r : Nat, 1 ≤ r → ¬r ≤ 0 / 2 := by
  omega

/-- No positive rank is admissible for a singleton ground set. -/
theorem no_admissible_rank_fin_one : ∀ r : Nat, 1 ≤ r → ¬r ≤ 1 / 2 := by
  omega

/-- The equality boundary `n = 2 * r` is included and attained. -/
theorem star_attains_equality_boundary :
    ∃ A : Finset (Finset (Fin 4)),
      (A : Set (Finset (Fin 4))).Intersecting ∧
      (A : Set (Finset (Fin 4))).Sized 2 ∧
      A.card = (4 - 1).choose (2 - 1) := by
  exact erdosKoRadoStar_attains 4 2 (by decide) (by decide)

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removed-hypothesis mutation: the universal bound no longer requires
the family to be intersecting. -/
def mutationRemovedIntersectingHypothesis : Prop :=
  ∀ (n r : Nat), 1 ≤ r → r ≤ n / 2 →
    (∃ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting ∧
      (A : Set (Finset (Fin n))).Sized r ∧
      A.card = (n - 1).choose (r - 1)) ∧
    ∀ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Sized r →
      A.card ≤ (n - 1).choose (r - 1)

/-- Changed-domain mutation: family members are `Set (Fin n)` instead of
`Finset (Fin n)`, while the mathematical predicate shape is retained. -/
def mutationChangedSubsetDomain : Prop :=
  ∀ (n r : Nat), 1 ≤ r → r ≤ n / 2 →
    (∃ A : Finset (Set (Fin n)),
      (A : Set (Set (Fin n))).Intersecting ∧
      (∀ s ∈ A, ∃ t : Finset (Fin n), (t : Set (Fin n)) = s ∧ t.card = r) ∧
      A.card = (n - 1).choose (r - 1)) ∧
    ∀ A : Finset (Set (Fin n)),
      (A : Set (Set (Fin n))).Intersecting →
      (∀ s ∈ A, ∃ t : Finset (Fin n), (t : Set (Fin n)) = s ∧ t.card = r) →
      A.card ≤ (n - 1).choose (r - 1)

/-- Changed-scope mutation: only one attaining family is bounded, rather than
every intersecting uniform family. -/
def mutationChangedFamilyBinderScope : Prop :=
  ∀ (n r : Nat), 1 ≤ r → r ≤ n / 2 →
    ∃ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting ∧
      (A : Set (Finset (Fin n))).Sized r ∧
      A.card = (n - 1).choose (r - 1) ∧
      A.card ≤ (n - 1).choose (r - 1)

/-- Boundary mutation: equality `r = n / 2` is excluded. -/
def mutationExcludesEqualityBoundary : Prop :=
  ∀ (n r : Nat), 1 ≤ r → r < n / 2 →
    (∃ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting ∧
      (A : Set (Finset (Fin n))).Sized r ∧
      A.card = (n - 1).choose (r - 1)) ∧
    ∀ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting →
      (A : Set (Finset (Fin n))).Sized r →
      A.card ≤ (n - 1).choose (r - 1)

#check_failure
  (rfl : ErdosKoRadoMaximumTarget = mutationRemovedIntersectingHypothesis)
#check_failure
  (rfl : ErdosKoRadoMaximumTarget = mutationChangedSubsetDomain)
#check_failure
  (rfl : ErdosKoRadoMaximumTarget = mutationChangedFamilyBinderScope)
#check_failure
  (rfl : ErdosKoRadoMaximumTarget = mutationExcludesEqualityBoundary)

#print axioms erdosKoRadoMaximumTarget_iff_concreteStarMaximumTarget
#print axioms star_attains_equality_boundary

end Stage1Instances.THM_M_0822

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget
