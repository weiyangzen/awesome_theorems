import Statement
import FiniteDilworth
import Mathlib.Combinatorics.Compactness
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0819: proof of Dilworth's primary finite-width theorem

The finite core is the locally ported finite Dilworth theorem. For an arbitrary
finite-width poset, every finite set is enlarged by the fixed maximum
antichain, colored by the finite theorem, and the local colorings are stitched
together by Rado selection. The global color fibers are the required chains.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0819_Proof

open Stage1Instances.THM_M_0819

universe u

noncomputable section

private theorem hasExactly_encard {α : Type u} {n : Nat} {s : Set α}
    (h : HasExactly n s) : s.encard = n := by
  obtain ⟨e⟩ := h
  simpa using ENat.card_congr e

private theorem isAntichain_subtype {α : Type u} [PartialOrder α] {s t : Set α}
    (hs : IsAntichain (fun x y : α => x ≤ y) s) :
    IsAntichain (fun x y : t => x ≤ y) {x | x.1 ∈ s} := by
  intro x hx y hy hxy
  exact hs hx hy (fun h => hxy (Subtype.ext h))

private theorem dependent_of_subtype_dependent
    {α : Type u} [PartialOrder α] {t : Set α} {s : Set t}
    (h : IsDependent s) : IsDependent (Subtype.val '' s : Set α) := by
  obtain ⟨x, hx, y, hy, hxy, hcomp⟩ := h
  exact ⟨x, ⟨x, hx, rfl⟩, y, ⟨y, hy, rfl⟩,
    fun heq => hxy (Subtype.ext heq), hcomp⟩

private theorem finite_width_le {α : Type u} [PartialOrder α] (k : Nat)
    (hdep : ∀ s : Set α, HasExactly (k + 1) s → IsDependent s)
    (t : Set α) (s : Set t) (hs : IsAntichain (fun x y : t => x ≤ y) s) :
    s.encard ≤ k := by
  by_contra hnot
  have hk1 : (k + 1 : ENat) ≤ s.encard := by
    exact Order.add_one_le_of_lt (lt_of_not_ge hnot)
  obtain ⟨r, hrs, hrcard⟩ := Set.exists_subset_encard_eq hk1
  have hrAnti : IsAntichain (fun x y : t => x ≤ y) r := hs.subset hrs
  let image : Set α := Subtype.val '' r
  have himageCard : image.encard = k + 1 := by
    rw [Function.Injective.encard_image Subtype.val_injective, hrcard]
  have himageExact : HasExactly (k + 1) image := by
    have himageFinite : image.Finite := Set.finite_of_encard_eq_coe himageCard
    letI : Finite image := himageFinite.to_subtype
    let e : image ≃ Fin (k + 1) := Finite.equivFinOfCardEq
      (α := image) (by
        rw [Nat.card_coe_set_eq]
        exact_mod_cast (himageFinite.cast_ncard_eq.trans himageCard))
    exact ⟨e⟩
  obtain ⟨x, hx, y, hy, hxy, hcomp⟩ := hdep image himageExact
  obtain ⟨x', hx', rfl⟩ := hx
  obtain ⟨y', hy', heq⟩ := hy
  subst heq
  rcases hcomp with hle | hge
  · exact hrAnti hx' hy' (fun h => hxy (congrArg Subtype.val h)) hle
  · exact hrAnti hy' hx' (fun h => hxy (congrArg Subtype.val h).symm) hge

private theorem finite_chain_partition {α : Type u} [PartialOrder α] (k : Nat)
    (hdep : ∀ s : Set α, HasExactly (k + 1) s → IsDependent s)
    (A : Set α) (hAexact : HasExactly k A)
    (hAanti : IsAntichain (fun x y : α => x ≤ y) A)
    (s : Set α) (hs : s.Finite) :
    ∃ color : s → Fin k, ∀ x y : s, color x = color y → x ≠ y → x ≤ y ∨ y ≤ x := by
  let t : Set α := s ∪ A
  have hAfin : A.Finite := Set.finite_of_encard_eq_coe (hasExactly_encard hAexact)
  have htfin : t.Finite := hs.union hAfin
  letI : Finite t := htfin.to_subtype
  let At : Set t := {x | x.1 ∈ A}
  have hAtAnti : IsAntichain (fun x y : t => x ≤ y) At :=
    isAntichain_subtype hAanti
  have hAtCard : At.encard = k := by
    let e : At ≃ A :=
      { toFun := fun x => ⟨x.1.1, x.2⟩
        invFun := fun x => ⟨⟨x.1, Or.inr x.2⟩, x.2⟩
        left_inv := fun x => by ext; rfl
        right_inv := fun x => by ext; rfl }
    exact (Set.encard_congr e).trans (hasExactly_encard hAexact)
  have hWidthLe : antichainWidth t (fun x y : t => x ≤ y) ≤ k := by
    refine ENat.forall_natCast_le_iff_le.mp (fun n hn => ?_)
    obtain ⟨a, haCard, haAnti⟩ := exists_of_le_antichainWidth t
      (fun x y : t => x ≤ y) n hn
    exact haCard ▸ finite_width_le k hdep t a haAnti
  have hkLeWidth : (k : ENat) ≤ antichainWidth t (fun x y : t => x ≤ y) :=
    hAtCard ▸ encard_le_antichainWidth hAtAnti
  have hWidth : antichainWidth t (fun x y : t => x ≤ y) = k :=
    le_antisymm hWidthLe hkLeWidth
  obtain ⟨P, hPcard, hP⟩ := minChainPartition_exists t (fun x y : t => x ≤ y)
  have hPcardK : P.encard = k := by
    rw [hPcard, minChainPartition_eq_antichainWidth, hWidth]
  have hPfinite : P.Finite := Set.finite_of_encard_eq_coe hPcardK
  letI : Finite P := hPfinite.to_subtype
  let index : P ≃ Fin k := Finite.equivFinOfCardEq
    (α := P) (by
      rw [Nat.card_coe_set_eq]
      exact_mod_cast (hPfinite.cast_ncard_eq.trans hPcardK))
  let member (x : t) : P :=
    ⟨Classical.choose (hP.1 x), (Classical.choose_spec (hP.1 x)).1.1⟩
  let colorT (x : t) : Fin k := index (member x)
  have hsame (x y : t) (hcolor : colorT x = colorT y) (hxy : x ≠ y) :
      x ≤ y ∨ y ≤ x := by
    have hmember : member x = member y := index.injective hcolor
    have hxmem : x ∈ (member x).1 := (Classical.choose_spec (hP.1 x)).1.2
    have hymem : y ∈ (member y).1 := (Classical.choose_spec (hP.1 y)).1.2
    have hchain := hP.2 (member x).1 (member x).2
    exact hchain hxmem (hmember ▸ hymem) hxy
  let embedS : s → t := fun x => ⟨x.1, Or.inl x.2⟩
  exact ⟨fun x => colorT (embedS x), fun x y hcolor hxy =>
    hsame (embedS x) (embedS y) hcolor
      (fun h => hxy (Subtype.ext (congrArg (fun z : t => z.1) h)))⟩

private theorem positiveWidth :
    ∀ (α : Type u) [PartialOrder α] (k : Nat), 0 < k →
      (∀ s : Set α, HasExactly (k + 1) s → IsDependent s) →
      (∃ s : Set α, HasExactly k s ∧ IsAntichain (fun x y : α => x ≤ y) s) →
      ∃ C : Fin k → Set α, IsDisjointChainDecomposition k C := by
  intro α _ k _hk hdep hindependent
  obtain ⟨A, hAexact, hAanti⟩ := hindependent
  let coloring (s : Set α) (hs : s.Finite) : s → Fin k :=
    Classical.choose (finite_chain_partition k hdep A hAexact hAanti s hs)
  have hlocal (s : Set α) (hs : s.Finite) :
      ∀ x y : s, coloring s hs x = coloring s hs y → x ≠ y → x ≤ y ∨ y ≤ x :=
    Classical.choose_spec (finite_chain_partition k hdep A hAexact hAanti s hs)
  obtain ⟨global, hglobal⟩ := Set.Finite.rado_selection_subtype
    (β := fun _ : α => Fin k) coloring
  let C : Fin k → Set α := fun i => {x | global x = i}
  refine ⟨C, ?_⟩
  constructor
  · intro i x hx y hy hxy
    let pair : Set α := {x, y}
    have hpair : pair.Finite := Set.toFinite pair
    obtain ⟨t, ht, hsub, hagree⟩ := hglobal pair hpair
    have hxt : x ∈ t := hsub (by simp [pair])
    have hyt : y ∈ t := hsub (by simp [pair])
    have hxagree : global x = coloring t ht ⟨x, hxt⟩ :=
      hagree ⟨x, by simp [pair]⟩
    have hyagree : global y = coloring t ht ⟨y, hyt⟩ :=
      hagree ⟨y, by simp [pair]⟩
    apply hlocal t ht ⟨x, hxt⟩ ⟨y, hyt⟩
    · exact hxagree.symm.trans (hx.trans (hy.symm.trans hyagree))
    · exact fun h => hxy (congrArg Subtype.val h)
  · intro x
    refine ⟨global x, rfl, ?_⟩
    intro i hi
    exact hi.symm

/-- Dilworth's Theorem 1.1 for arbitrary partial orders of attained finite width. -/
theorem dilworthPrimary : DilworthPrimaryTarget.{u} := by
  intro α _ k hdep hindependent
  rcases Nat.eq_zero_or_pos k with rfl | hk
  · letI : IsEmpty α := zeroWidth_forces_isEmpty α hdep
    exact zeroWidth_decomposition α
  · exact positiveWidth α k hk hdep hindependent

#check dilworthPrimary
assert_no_sorry dilworthPrimary
#print sorries dilworthPrimary
#print axioms dilworthPrimary

end

end Stage1Instances.THM_M_0819_Proof
