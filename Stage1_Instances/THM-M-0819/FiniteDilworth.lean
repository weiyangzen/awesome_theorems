/-
Copyright (c) 2025 Vlad Tsyrklevich. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vlad Tsyrklevich
-/

/-
This is a current-pin port of `vlad902/misc-lean-proofs` commit
`f82f920f05a381bb1ce5e8903bde33e27f4365b6`, file
`MiscLeanProofs/Dilworth.lean` (upstream SHA-256
`4bc86897588087f472b358830bba157b92994e2b0dd44c66805f57c29211c985`).
The port changes only two Lean API sites: `IsChain.image` and a dependent rewrite
inside `overlap_top_encard_eq`. See `proof-receipt.json` for the exact boundary.
-/

import Mathlib.Data.ENat.Lattice
import Mathlib.Data.Finite.Card
import Mathlib.Data.Set.Card
import Mathlib.Data.Set.Subset
import Mathlib.Tactic.ENatToNat

/-!
# Dilworth's theorem

This file proves Dilworth's and Mirsky's theorems, along with the requisite definitions required to
state them.

## Definitions

* `chainHeight` / `antichainWidth`: The maximum size of any chain/antichain in a given order.
* `IsChainPartition` / `IsAntichainPartition`: A predicate for whether a given set of sets
   is a partition of the parent order into disjoint chains/antichains
* `minChainPartition` / `minAntiChainPartition`: The minimum size of a chain/antichain partition in
   a given order.

* `minChainPartition_eq_antichainWidth`: Dilworth's theorem for finite posets.
* `minAntichainPartition_eq_chainHeight`: Mirsky's theorem.
-/

section PR

open Function Set IsAntichain

variable {α β : Type*} {r r₁ r₂ : α → α → Prop} {r' : β → β → Prop} {s t : Set α} {a b : α}

-- #29992

theorem IsChain.exists_isTop {α : Type*} [Preorder α] (s : Set α) (h : s.Nonempty) (hf : s.Finite)
    (hs : IsChain (· ≤ ·) s) : ∃ x : s, IsTop x := by
  obtain ⟨x, hx₁, hx₂⟩ := hf.exists_maximal h
  refine ⟨⟨x, hx₁⟩, fun a ↦ ?_⟩
  by_cases h' : x = a.1
  · simp [h']
  · rcases hs hx₁ a.2 h' with h'' | h''
    · exact hx₂ a.2 h''
    · exact h''

theorem IsChain.exists_isBot {α : Type*} [Preorder α] (s : Set α) (h : s.Nonempty) (hf : s.Finite)
    (hs : IsChain (· ≤ ·) s) : ∃ x : s, IsBot x :=
  hs.symm.exists_isTop (α := αᵒᵈ) s h hf

theorem IsMaxChain.exists_isMax {α : Type*} [Preorder α] {s : Set α} (h : s.Nonempty) (hf : s.Finite)
    (hs : IsMaxChain (· ≤ ·) s) : ∃ x : α, x ∈ s ∧ IsMax x := by
  by_contra! hh
  obtain ⟨x, hx₁, hx₂⟩ := hf.exists_maximal h
  have := hh x hx₁
  simp only [IsMax, not_forall] at this
  obtain ⟨z, hz₁, hz₂⟩ := this
  have : IsChain (· ≤ ·) (s ∪ {z}) := by
    refine isChain_union.mpr ⟨hs.isChain, IsChain.singleton, fun a ha₁ ↦ ?_⟩
    by_cases h' : x = a
    · grind
    · rcases hs.1 hx₁ ha₁ h' with h'' | h'' <;> grind [le_trans]
  refine hz₂ (hx₂ ?_ hz₁)
  rw [hs.2 this (by simp)]
  simp

theorem IsMaxChain.exists_isMin {α : Type*} [Preorder α] (s : Set α) (h : s.Nonempty) (hf : s.Finite)
    (hs : IsMaxChain (· ≤ ·) s) : ∃ x : α, x ∈ s ∧ IsMin x :=
  hs.symm.exists_isMax (α := αᵒᵈ) h hf

end PR

section height

open ENat

variable (α : Type*) (r : α → α → Prop)

noncomputable def chainHeight : ℕ∞ := ⨆ s : {s : Set α // IsChain r s}, s.val.encard

theorem chainHeight_eq_biInf :
  chainHeight α r = ⨆ s : {s : Set α // IsChain r s}, s.val.encard := rfl

theorem chainHeight_le_card : chainHeight α r ≤ ENat.card α := by
  simp [chainHeight_eq_biInf, Set.encard_le_card]

theorem chainHeight_ne_top_of_finite [Finite α] : chainHeight α r ≠ ⊤ := by
  obtain ⟨n, hn₁, hn₂⟩ := le_coe_iff.mp <| card_eq_coe_natCard α ▸ (chainHeight_le_card α r)
  simp [hn₁]

theorem chainHeight_eq_zero_iff : chainHeight α r = 0 ↔ IsEmpty α := by
  constructor
  · intro h
    by_contra! hh
    obtain ⟨x⟩ := hh
    simp only [chainHeight, iSup_eq_zero, Set.encard_eq_zero, Subtype.forall] at h
    have := h {x}
    simp at this
  · simp_all [chainHeight, Set.eq_empty_of_isEmpty]

theorem exists_isChain_of_le_chainHeight (n : ℕ) (h : n ≤ chainHeight α r) :
    ∃ s : Set α, s.encard = n ∧ IsChain r s := by
  by_cases h' : n = 0
  · exact ⟨∅, by simp [h']⟩
  · have : ∃ s : Set α, IsChain r s ∧ n ≤ s.encard := by
      contrapose! h
      refine iSup_lt_iff.mpr ⟨n - 1, ?_, fun s ↦ ?_⟩
      · enat_to_nat
        exact Nat.sub_one_lt h'
      · exact ENat.le_sub_one_of_lt <| h s.1 s.2
    obtain ⟨s, hs₁, hs₂⟩ := this
    obtain ⟨t, ht₁, ht₂⟩ := Set.exists_subset_encard_eq hs₂
    exact ⟨t, ht₂, hs₁.mono ht₁⟩

theorem exists_of_chainHeight_ne_top (h : chainHeight α r ≠ ⊤) :
    ∃ s : Set α, s.encard = chainHeight α r ∧ IsChain r s := by
  have : Nonempty { s // IsChain r s } := ⟨∅, by simp⟩
  obtain ⟨s, hs⟩ := exists_eq_iSup_of_lt_top (by rwa [← chainHeight_eq_biInf, lt_top_iff_ne_top])
  exact ⟨s.1, hs, s.2⟩

theorem exists_eq_chainHeight_of_finite [Finite α] :
    ∃ s : Set α, s.encard = chainHeight α r ∧ IsChain r s :=
  exists_of_chainHeight_ne_top α r (chainHeight_ne_top_of_finite α r)

variable {α β : Type*} {r : α → α → Prop} {r' : β → β → Prop}

theorem encard_le_chainHeight {s : Set α} (h : IsChain r s) : s.encard ≤ chainHeight α r :=
  le_iSup_iff.mpr fun _ a ↦ a ⟨s, h⟩

theorem finite_of_chainHeight_ne_top {s : Set α} (h₁ : IsChain r s) (h₂ : chainHeight α r ≠ ⊤) :
    s.Finite :=
  Set.encard_ne_top_iff.mp <| ne_top_of_le_ne_top h₂ <| encard_le_chainHeight h₁

theorem encard_lt_chainHeight_of_not_isMaxChain {s : Set α} [Finite s] (h₁ : IsChain r s)
    (h₂ : ¬IsMaxChain r s) : s.encard < chainHeight α r := by
  contrapose! h₂
  refine ⟨h₁, fun t ht₁ ht₂ ↦ ?_⟩
  by_contra! hh
  have := Set.Finite.encard_lt_encard (by assumption) ⟨ht₂, by grind⟩
  have := lt_of_lt_of_le (lt_of_le_of_lt h₂ this) (encard_le_chainHeight ht₁)
  simp at this

theorem chainHeight_le_of_relEmbedding (e : r ↪r r') :
    chainHeight α r ≤ chainHeight β r' := by
  refine forall_natCast_le_iff_le.mp fun n hn ↦ ?_
  obtain ⟨a, ha₁, ha₂⟩ := exists_isChain_of_le_chainHeight α r n hn
  have : (e '' a).encard = n := by rw [Function.Injective.encard_image e.injective, ha₁]
  exact this ▸ encard_le_chainHeight (s := e '' a) <| IsChain.image_relEmbedding_iff.mpr ha₂

theorem chainHeight_eq_of_relIso (e : r ≃r r') :
    chainHeight α r = chainHeight β r' :=
  le_antisymm (chainHeight_le_of_relEmbedding e) (chainHeight_le_of_relEmbedding e.symm)

theorem chainHeight_coe_univ :
    chainHeight ↑Set.univ (r ·.val ·.val) = chainHeight α r :=
  chainHeight_eq_of_relIso { toEquiv := Equiv.Set.univ α, map_rel_iff' := by simp }

theorem chainHeight_subset (s t : Set α) (h : s ⊆ t) :
    chainHeight s (r · ·) ≤ chainHeight t (r · ·) :=
  chainHeight_le_of_relEmbedding (Subrel.inclusionEmbedding r h)

end height

section width

open ENat

variable (α : Type*) (r : α → α → Prop)

noncomputable def antichainWidth : ℕ∞ := ⨆ s : {s : Set α // IsAntichain r s}, s.val.encard

theorem antichainWidth_eq_biInf :
  antichainWidth α r = ⨆ s : {s : Set α // IsAntichain r s}, s.val.encard := rfl

theorem antichainWidth_le_card : antichainWidth α r ≤ ENat.card α := by
  simp [antichainWidth_eq_biInf, Set.encard_le_card]

theorem antichainWidth_ne_top_of_finite [Finite α] : antichainWidth α r ≠ ⊤ := by
  obtain ⟨n, hn₁, hn₂⟩ := le_coe_iff.mp <| card_eq_coe_natCard α ▸ (antichainWidth_le_card α r)
  simp [hn₁]

theorem antichainWidth_eq_zero_iff : antichainWidth α r = 0 ↔ IsEmpty α := by
  constructor
  · intro h
    by_contra! hh
    obtain ⟨x⟩ := hh
    simp only [antichainWidth, iSup_eq_zero, Set.encard_eq_zero, Subtype.forall] at h
    have := h {x}
    simp at this
  · simp_all [antichainWidth, Set.eq_empty_of_isEmpty]

theorem exists_of_le_antichainWidth (n : ℕ) (h : n ≤ antichainWidth α r) :
    ∃ s : Set α, s.encard = n ∧ IsAntichain r s := by
  by_cases h' : n = 0
  · exact ⟨∅, by simp [h']⟩
  · have : ∃ s : Set α, IsAntichain r s ∧ n ≤ s.encard := by
      contrapose! h
      refine iSup_lt_iff.mpr ⟨n - 1, ?_, fun s ↦ ?_⟩
      · enat_to_nat
        exact Nat.sub_one_lt h'
      · exact ENat.le_sub_one_of_lt <| h s.1 s.2
    obtain ⟨s, hs₁, hs₂⟩ := this
    obtain ⟨t, ht₁, ht₂⟩ := Set.exists_subset_encard_eq hs₂
    exact ⟨t, ht₂, hs₁.subset ht₁⟩

theorem exists_of_antichainWidth_ne_top (h : antichainWidth α r ≠ ⊤) :
    ∃ s : Set α, s.encard = antichainWidth α r ∧ IsAntichain r s := by
  have : Nonempty { s // IsAntichain r s } := ⟨∅, by simp⟩
  obtain ⟨s, hs⟩ := exists_eq_iSup_of_lt_top (by rwa [← antichainWidth_eq_biInf, lt_top_iff_ne_top])
  exact ⟨s.1, hs, s.2⟩

theorem exists_eq_antichainWidth_of_finite [Finite α] :
    ∃ s : Set α, s.encard = antichainWidth α r ∧ IsAntichain r s :=
  exists_of_antichainWidth_ne_top α r (antichainWidth_ne_top_of_finite α r)

variable {α β : Type*} {r : α → α → Prop} {r' : β → β → Prop}

theorem encard_le_antichainWidth {s : Set α} (h : IsAntichain r s) :
    s.encard ≤ antichainWidth α r :=
  le_iSup_iff.mpr fun _ a ↦ a ⟨s, h⟩

theorem finite_of_antichainWidth_ne_top {s : Set α} (h₁ : IsAntichain r s)
    (h₂ : antichainWidth α r ≠ ⊤) : s.Finite :=
  Set.encard_ne_top_iff.mp <| ne_top_of_le_ne_top h₂ <| encard_le_antichainWidth h₁

theorem encard_lt_antichainWidth_of_not_isMaxAntichain {s : Set α} [Finite s] (h₁ : IsAntichain r s)
    (h₂ : ¬IsMaxAntichain r s) : s.encard < antichainWidth α r := by
  contrapose! h₂
  refine ⟨h₁, fun t ht₁ ht₂ ↦ ?_⟩
  by_contra! hh
  have := Set.Finite.encard_lt_encard (by assumption) ⟨ht₂, by grind⟩
  have := lt_of_lt_of_le (lt_of_le_of_lt h₂ this) (encard_le_antichainWidth ht₁)
  simp at this

theorem antichainWidth_le_of_relEmbedding (e : r ↪r r') :
    antichainWidth α r ≤ antichainWidth β r' := by
  refine forall_natCast_le_iff_le.mp fun n hn ↦ ?_
  obtain ⟨a, ha₁, ha₂⟩ := exists_of_le_antichainWidth α r n hn
  have : (e '' a).encard = n := by rw [Function.Injective.encard_image e.injective, ha₁]
  exact this ▸ encard_le_antichainWidth (s := e '' a) <| IsAntichain.image_relEmbedding_iff.mpr ha₂

theorem antichainWidth_eq_of_relIso (e : r ≃r r') :
    antichainWidth α r = antichainWidth β r' :=
  le_antisymm (antichainWidth_le_of_relEmbedding e) (antichainWidth_le_of_relEmbedding e.symm)

theorem antichainWidth_coe_univ :
    antichainWidth ↑Set.univ (r ·.val ·.val) = antichainWidth α r :=
  antichainWidth_eq_of_relIso { toEquiv := Equiv.Set.univ α, map_rel_iff' := by simp }

theorem antichainWidth_subset (s t : Set α) (h : s ⊆ t) :
    antichainWidth s (r · ·) ≤ antichainWidth t (r · ·) :=
  antichainWidth_le_of_relEmbedding (Subrel.inclusionEmbedding r h)

end width

section ChainPartition

variable (α : Type*) (r : α → α → Prop)

def IsChainPartition (S : Set (Set α)) :=
  (∀ x : α, ∃! s ∈ S, x ∈ s) ∧ (∀ s ∈ S, IsChain r s)

theorem exists_IsChainPartition :
    ∃ s : Set (Set α), IsChainPartition α r s ∧ s.encard = ENat.card α := by
  refine ⟨Set.range ({·}), ⟨fun a ↦ ⟨{a}, by simp⟩, by simp [IsChain.singleton]⟩, ?_⟩
  rw [← @Set.image_univ, ← Set.encard_univ α]
  exact Function.Injective.encard_image Set.singleton_injective Set.univ

noncomputable def minChainPartition : ℕ∞ :=
  ⨅ s : {s : Set (Set α) // IsChainPartition α r s}, s.val.encard

theorem minChainPartition_eq_biSup :
  minChainPartition α r =
    ⨅ s : {s : Set (Set α) // IsChainPartition α r s}, s.val.encard := rfl

theorem minChainPartition_eq_zero_iff : minChainPartition α r = 0 ↔ IsEmpty α := by
  simp [isEmpty_iff, minChainPartition, IsChainPartition]

theorem one_le_minChainPartition_iff : 1 ≤ minChainPartition α r ↔ Nonempty α := by
  refine ⟨fun h ↦ ?_, fun h ↦ ?_⟩
  · contrapose! h
    grind [minChainPartition_eq_zero_iff, not_nonempty_iff, ENat.lt_one_iff_eq_zero]
  · by_contra! hh
    grind [minChainPartition_eq_zero_iff, not_nonempty_iff, ENat.lt_one_iff_eq_zero]

theorem minChainPartition_le_card : minChainPartition α r ≤ ENat.card α := by
  obtain ⟨s, hs₁, hs₂⟩ := exists_IsChainPartition α r
  refine iInf_le_iff.mpr fun b hb ↦ ?_
  grw [hb ⟨s, hs₁⟩, hs₂]

theorem minChainPartition_ne_top_of_finite [Finite α] : minChainPartition α r ≠ ⊤ := by
  have := minChainPartition_le_card α r
  rw [ENat.card_eq_coe_natCard, ENat.le_coe_iff] at this
  obtain ⟨n, hn, _⟩ := this
  simp [hn]

theorem minChainPartition_le_encard (S : Set (Set α)) (h : IsChainPartition α r S) :
    minChainPartition α r ≤ S.encard :=
  iInf_le_iff.mpr fun _ hx ↦ hx ⟨S, h⟩

theorem minChainPartition_exists :
    ∃ (S : Set (Set α)), S.encard = minChainPartition α r ∧ IsChainPartition α r S := by
  have : Nonempty ({s : Set (Set α) // IsChainPartition α r s}) := by
    obtain ⟨s, hs, _⟩ := exists_IsChainPartition α r
    exact ⟨s, hs⟩
  obtain ⟨s, hs⟩ := @ENat.exists_eq_iInf _ this (·.val.encard)
  exact ⟨s.val, hs, s.property⟩

end ChainPartition

section AntichainPartition

variable (α : Type*) (r : α → α → Prop)

def IsAntichainPartition (S : Set (Set α)) :=
  (∀ x : α, ∃! s ∈ S, x ∈ s) ∧ (∀ s ∈ S, IsAntichain r s)

theorem exists_IsAntichainPartition :
    ∃ s : Set (Set α), IsAntichainPartition α r s ∧ s.encard = ENat.card α := by
  refine ⟨Set.range ({·}), ⟨fun a ↦ ⟨{a}, by simp⟩, by simp⟩, ?_⟩
  rw [← @Set.image_univ, ← Set.encard_univ α]
  exact Function.Injective.encard_image Set.singleton_injective Set.univ

noncomputable def minAntichainPartition : ℕ∞ :=
  ⨅ s : {s : Set (Set α) // IsAntichainPartition α r s}, s.val.encard

theorem minAntichainPartition_eq_biSup :
  minAntichainPartition α r =
    ⨅ s : {s : Set (Set α) // IsAntichainPartition α r s}, s.val.encard := rfl

theorem minAntichainPartition_eq_zero_iff : minAntichainPartition α r = 0 ↔ IsEmpty α := by
  simp [isEmpty_iff, minAntichainPartition, IsAntichainPartition]

theorem one_le_minAntichainPartition_iff : 1 ≤ minAntichainPartition α r ↔ Nonempty α := by
  refine ⟨fun h ↦ ?_, fun h ↦ ?_⟩
  · contrapose! h
    grind [minAntichainPartition_eq_zero_iff, not_nonempty_iff, ENat.lt_one_iff_eq_zero]
  · by_contra! hh
    grind [minAntichainPartition_eq_zero_iff, not_nonempty_iff, ENat.lt_one_iff_eq_zero]

theorem minAntichainPartition_le_card : minAntichainPartition α r ≤ ENat.card α := by
  obtain ⟨s, hs₁, hs₂⟩ := exists_IsAntichainPartition α r
  refine iInf_le_iff.mpr fun b hb ↦ ?_
  grw [hb ⟨s, hs₁⟩, hs₂]

theorem minAntichainPartition_ne_top_of_finite [Finite α] : minAntichainPartition α r ≠ ⊤ := by
  have := minAntichainPartition_le_card α r
  rw [ENat.card_eq_coe_natCard, ENat.le_coe_iff] at this
  obtain ⟨n, hn, _⟩ := this
  simp [hn]

theorem minAntichainPartition_le_encard (S : Set (Set α)) (h : IsAntichainPartition α r S) :
    minAntichainPartition α r ≤ S.encard :=
  iInf_le_iff.mpr fun _ hx ↦ hx ⟨S, h⟩

theorem minAntichainPartition_exists :
    ∃ (S : Set (Set α)), S.encard = minAntichainPartition α r ∧ IsAntichainPartition α r S := by
  have : Nonempty ({s : Set (Set α) // IsAntichainPartition α r s}) := by
    obtain ⟨s, hs, _⟩ := exists_IsAntichainPartition α r
    exact ⟨s, hs⟩
  obtain ⟨s, hs⟩ := @ENat.exists_eq_iInf _ this (·.val.encard)
  exact ⟨s.val, hs, s.property⟩

end AntichainPartition

section mirsky

variable (α : Type*) (r : α → α → Prop)

theorem le_minAntichainPartition_of_isChain {α} {r} {s : Set α} (h : IsChain r s) :
    s.encard ≤ minAntichainPartition α r := by
  by_contra! hh
  obtain ⟨t, ht₁, ht₂⟩ := minAntichainPartition_exists α r
  have (a : α) (ha : a ∈ s) := Classical.choose_spec (ht₂.1 a) |>.1.1
  obtain ⟨x, hx, y, hy, hxy, _⟩ := Set.exists_ne_map_eq_of_encard_lt_of_maps_to (ht₁ ▸ hh) this
  have cc := Classical.choose_spec (ht₂.1 x)
  have := Classical.choose_spec (ht₂.1 y)
  have := (ht₂.2 _ cc.1.1) cc.1.2 (by grind) hxy
  have := (ht₂.2 _ cc.1.1) (by grind) cc.1.2 hxy.symm
  rcases h hx hy hxy <;> contradiction

theorem chainHeight_le_minAntichainPartition : chainHeight α r ≤ minAntichainPartition α r := by
  refine ENat.forall_natCast_le_iff_le.mp fun m h ↦ ?_
  obtain ⟨s, hs₁, hs₂⟩ := exists_isChain_of_le_chainHeight α r m (by simp_all)
  exact hs₁ ▸ le_minAntichainPartition_of_isChain hs₂

theorem maximal_inter_nonempty {α} [Preorder α] [Nonempty α] (hc : chainHeight α (· ≤ ·) ≠ ⊤)
    {s : Set α} (hs : IsMaxChain (· ≤ ·) s) : ({x | Maximal ⊤ x} ∩ s).Nonempty := by
  have : Finite s := finite_of_chainHeight_ne_top hs.isChain hc
  obtain ⟨k, hk₁, hk₂⟩ := hs.exists_isMax (hs.nonempty_iff.mp (by assumption)) (Set.toFinite _)
  exact ⟨k, Set.mem_inter (by simp [Pi.top_def, hk₂]) hk₁⟩

theorem chainHeight_sdiff_add_one_le {α} {r} (hc : chainHeight α r ≠ ⊤) {s : Set α}
    (hs : ∀ {t : Set α}, IsMaxChain r t → (s ∩ t).Nonempty) :
    chainHeight ↑(Set.univ \ s) (r ·.val ·) + 1 ≤ chainHeight α r := by
  have := chainHeight_subset (r := r) (Set.univ \ s) Set.univ (by simp)
  have hhc := lt_top_iff_ne_top.mp <| lt_of_le_of_lt
    (chainHeight_coe_univ ▸ this) (lt_top_iff_ne_top.mpr hc)
  obtain ⟨c, hc₁, hc₂⟩ := exists_of_chainHeight_ne_top _ _ hhc
  obtain ⟨d, hd₁, hd₂⟩ := exists_of_chainHeight_ne_top α _ hc
  let e₁ : Set α := Subtype.val '' c
  let e₂ : IsChain _ e₁ :=
    hc₂.image_of_map_rel _ _ Subtype.val (fun _ _ x ↦ x)
  have : Finite e₁ := finite_of_chainHeight_ne_top e₂ hc
  have tt := encard_lt_chainHeight_of_not_isMaxChain e₂
    (by grind [Set.inter_nonempty_iff_exists_right])
  have : c.encard = e₁.encard := by simp [e₁, Function.Injective.encard_image]
  grw [← hc₁, this, Order.add_one_le_of_lt tt]

theorem minAntichainPartition_le_sdiff_add_one {s : Set α} (hs : IsAntichain r s) :
    minAntichainPartition α r ≤
      minAntichainPartition ↑(Set.univ \ s) (r · ·) + 1 := by
  obtain ⟨S, hS₁, hS₂⟩ := minAntichainPartition_exists ↑(Set.univ \ s) (r · ·)
  let T : Set (Set α) := { s } ∪ ((Subtype.val '' ·) '' S)
  have hT : T.encard ≤ minAntichainPartition ↑(Set.univ \ s) (r · ·) + 1 := by
    simp only [Set.singleton_union, ← hS₁, T]
    grw [Set.encard_insert_le]
    rw [Function.Injective.encard_image Set.image_val_injective]
  have : IsAntichainPartition α r T := by
    simp only [IsAntichainPartition, Set.singleton_union, Set.mem_insert_iff,
      Set.mem_image, forall_eq_or_imp, hs, forall_exists_index, and_imp,
      forall_apply_eq_imp_iff₂, true_and, T]
    refine ⟨fun x ↦ ?_, fun a ha b hb c hc hbc ↦ ?_⟩
    · by_cases h' : x ∈ Set.univ \ s
      · obtain ⟨u, _, _⟩ := hS₂.1 ⟨x, h'⟩
        exact ⟨u, by grind⟩
      · exact ⟨s, by grind⟩
    · have := @hS₂.2 _ ha ⟨b, by grind⟩ (by grind) ⟨c, by grind⟩ (by grind) (by simp [hbc])
      simpa using this
  grw [minAntichainPartition_le_encard α r T this, hT]

theorem minAntichainPartition_eq_chainHeight [PartialOrder α] :
    minAntichainPartition α (· ≤ ·) = chainHeight α (· ≤ ·) := by
  refine ENat.eq_of_forall_natCast_le_iff fun m ↦
    ⟨fun h ↦ ?_, fun h ↦ le_trans h <| chainHeight_le_minAntichainPartition _ _⟩
  induction m generalizing α with
  | zero => simp
  | succ n ih =>
    by_cases h' : Nonempty α
    · by_cases hc : chainHeight α (· ≤ ·) = ⊤
      · simp [hc]
      · simp only [Nat.cast_add, Nat.cast_one]
        have := minAntichainPartition_le_sdiff_add_one α _ <| setOf_maximal_antichain ⊤
        have := ih _ <| ENat.addLECancellable_coe 1 |>.add_le_add_iff_right.mp <| le_trans h this
        grw [add_le_add_left this 1]
        have := chainHeight_sdiff_add_one_le hc (maximal_inter_nonempty hc)
        simpa using chainHeight_sdiff_add_one_le hc (maximal_inter_nonempty hc)
    · grind [not_isEmpty_iff, chainHeight_eq_zero_iff, minAntichainPartition_eq_zero_iff]

#print axioms minAntichainPartition_eq_chainHeight

end mirsky

section dilworth

variable (α : Type*) (r : α → α → Prop)

theorem le_minChainPartition_of_isAntichain {α} {r} {s : Set α} (h : IsAntichain r s) :
    s.encard ≤ minChainPartition α r := by
  by_contra! hh
  obtain ⟨t, ht₁, ht₂⟩ := minChainPartition_exists α r
  have (a : α) (ha : a ∈ s) := Classical.choose_spec (ht₂.1 a) |>.1.1
  obtain ⟨x, hx, y, hy, hxy, _⟩ := Set.exists_ne_map_eq_of_encard_lt_of_maps_to (ht₁ ▸ hh) this
  have := Classical.choose_spec (ht₂.1 y)
  have := Classical.choose_spec (ht₂.1 x)
  have := (ht₂.2 _ this.1.1) this.1.2 (by grind) hxy
  have t1 := h hx hy hxy
  have t2 := h hy hx hxy.symm
  simp only [Pi.compl_apply, compl_iff_not] at t1 t2 this
  rcases this with h' | h' <;> simp [t1, t2] at h'

theorem antichainWidth_le_minChainPartition : antichainWidth α r ≤ minChainPartition α r := by
  refine ENat.forall_natCast_le_iff_le.mp fun m h ↦ ?_
  obtain ⟨s, hs₁, hs₂⟩ := exists_of_le_antichainWidth α r m (by simp_all)
  exact hs₁ ▸ le_minChainPartition_of_isAntichain hs₂

theorem minChainPartition_le_sdiff_add_one [LE α] {s : Set α} (hs : IsChain (· ≤ ·) s) :
    minChainPartition α (· ≤ ·) ≤ minChainPartition ↑(Set.univ \ s) (· ≤ ·) + 1 := by
  obtain ⟨S, hS₁, hS₂⟩ := minChainPartition_exists ↑(Set.univ \ s) (· ≤ ·)
  let T : Set (Set α) := {s} ∪ ((Subtype.val '' ·) '' S)
  have hT : T.encard ≤ minChainPartition ↑(Set.univ \ s) (· ≤ ·) + 1 := by
    simp only [Set.singleton_union, ← hS₁, T]
    grw [Set.encard_insert_le]
    rw [Function.Injective.encard_image Set.image_val_injective]
  have : IsChainPartition α (· ≤ ·) T := by
    simp only [IsChainPartition, Set.singleton_union, Set.mem_insert_iff, Set.mem_image,
      forall_eq_or_imp, hs, forall_exists_index, and_imp, forall_apply_eq_imp_iff₂, true_and, T]
    refine ⟨fun x ↦ ?_, fun a ha b hb c hc hbc ↦ ?_⟩
    · by_cases h' : x ∈ Set.univ \ s
      · obtain ⟨u, _, _⟩ := hS₂.1 ⟨x, h'⟩
        exact ⟨u, by grind⟩
      · exact ⟨s, by grind⟩
    · have := @hS₂.2 _ ha ⟨b, by grind⟩ (by grind) ⟨c, by grind⟩ (by grind) (by simp [hbc])
      simpa using this
  grw [minChainPartition_le_encard α (· ≤ ·) T this, hT]

theorem pigeonhole_inter_eq {α} {r} {S : Set (Set α)} [Finite S]
    (hS : IsChainPartition α r S) {a : Set α} (ha₁ : a.encard = S.encard) (ha₂ : IsAntichain r a) :
    ∀ s ∈ S, ∃ x : α, (a ∩ s) = {x} := by
  intro s hs
  apply Set.ncard_eq_one.mp
  suffices (a ∩ s).encard ≠ 0 by
    have h := Set.encard_le_coe_iff_finite_ncard_le.mp <| Set.encard_le_one_iff_subsingleton.mpr <|
      inter_subsingleton_of_isAntichain_of_isChain ha₂ (hS.2 s hs)
    have := Set.Nonempty.ncard_pos h.1 (Set.encard_ne_zero.mp this)
    grind
  by_contra hh
  rw [Set.encard_eq_zero] at hh
  have hmap : Set.MapsTo (fun x ↦ Classical.choose (hS.1 x)) a (S \ {s}) := by
    grind [Set.MapsTo, Classical.choose_spec, Disjoint.notMem_of_mem_left,
      =_ Set.disjoint_iff_inter_eq_empty]
  have := Set.exists_ne_map_eq_of_encard_lt_of_maps_to (t := (S \ {s})) (s := a) ?_ hmap
  · obtain ⟨x, hx, y, hy, hxy, _⟩ := this
    have h₁ := ha₂ hx hy hxy
    have h₂ := ha₂ hy hx hxy.symm
    have := Classical.choose_spec (hS.1 y)
    have := Classical.choose_spec (hS.1 x)
    have := (hS.2 _ this.1.1) this.1.2 (by grind) hxy
    simp only [Pi.compl_apply, compl_iff_not] at h₁ h₂ this
    grind
  · rw [ha₁, Set.encard_diff_singleton_of_mem hs, ← Set.Finite.cast_ncard_eq S.toFinite]
    enat_to_nat
    exact Nat.sub_one_lt_of_lt <| Set.Nonempty.ncard_pos S.toFinite <| Set.nonempty_of_mem hs

theorem pigeonhole_delete_largest {α} {r} {C : Set (Set α)} (hC₁ : IsChainPartition α r C)
    (hS₂ : C.encard = antichainWidth α r) (hnetop : antichainWidth α r ≠ ⊤)
    (c d : Set α) (hd : IsChain r d) (hc : c ∈ C)
    (h : ∀ x ∈ c, ∀ a : Set α, IsAntichain r a → a.encard = antichainWidth α r → x ∈ a → x ∈ d) :
    antichainWidth α r = antichainWidth ↑(Set.univ \ d) (r · ·) + 1 := by
  refine ENat.eq_of_forall_natCast_le_iff fun n ↦ ⟨fun hn ↦ ?_, fun hn ↦ ?_⟩
  · obtain ⟨b, hb₁, hb₂⟩ := exists_of_antichainWidth_ne_top α r hnetop
    let n : Set ↑(Set.univ \ d) := ((fun x ↦ ⟨x.1, by grind⟩) '' (@Set.univ ↑(b \ d)))
    have hna : @IsAntichain ↑(Set.univ \ d) (r · ·) n :=
      IsAntichain.image (isAntichain_coe_univ_iff.mpr hb₂.diff) _ (fun _ _ a ↦ a)
    have hbne : b.encard ≤ n.encard + 1 := by
      rw [Function.Injective.encard_image <| Set.inclusion_injective (by grind)]
      simp only [← Set.encard_diff_add_encard_of_subset (by grind : (b \ d) ⊆ b),
        sdiff_sdiff_right_self, Set.inf_eq_inter, Set.encard_univ, add_comm (b ∩ d).encard]
      refine add_le_add_right (Set.encard_le_one_iff_subsingleton.mpr ?_) (b \ d).encard
      exact inter_subsingleton_of_isAntichain_of_isChain hb₂ hd
    grw [hn, ← hb₁, hbne, encard_le_antichainWidth hna]
  · grw [hn]
    have := antichainWidth_coe_univ ▸ @antichainWidth_subset α r ↑(Set.univ \ d) Set.univ (by simp)
    refine Order.add_one_le_of_lt <| lt_of_le_of_ne this ?_
    by_contra! hh
    obtain ⟨a, ha₁, ha₂⟩ := exists_of_le_antichainWidth ↑(Set.univ \ d) (r · ·)
      (antichainWidth ↑(Set.univ \ d) (r · ·)).toNat (by simp [ENat.coe_toNat_le_self])
    rw [hh, ENat.coe_toNat hnetop] at ha₁
    have hnew : @IsAntichain α r a := ha₂.image Subtype.val (by simp)
    have : Finite C := by grind [Set.Finite.to_subtype, Set.encard_ne_top_iff]
    obtain ⟨x, hx⟩ := pigeonhole_inter_eq hC₁
      (by grind [Function.Injective.encard_image, Subtype.val_injective]) hnew c hc
    rw [Set.eq_singleton_iff_unique_mem] at hx
    grind [Function.Injective.encard_image, Subtype.val_injective]

abbrev overlap_antichain {α : Type*} [LE α] (C : Set (Set α)) (c : C) :=
  { x ∈ c.1 | ∃ s : Set α, x ∈ s ∧ IsAntichain (· ≤ ·) s ∧ s.encard = C.encard }

def overlap_top {α : Type*} [LE α] (C : Set (Set α)) :=
  { x | ∃ c hx, @IsTop (overlap_antichain C c) _ ⟨x, hx⟩ }

theorem isAntichain_overlap_top {α} [PartialOrder α] {C : Set (Set α)} [Finite C]
    (hC : IsChainPartition α (· ≤ ·) C) :
    IsAntichain (· ≤ ·) (overlap_top C) := by
  intro c hc d hd hne
  simp only [overlap_top, Set.coe_setOf, Set.mem_setOf_eq, Subtype.exists] at hc hd
  obtain ⟨c₀, hc₀, hc₀mem, hc₀top⟩ := hc
  obtain ⟨d₀, hd₀, hd₀mem, hd₀top⟩ := hd
  by_cases h' : c₀ = d₀
  · subst h'
    have := Subtype.mk_eq_mk.mp <| le_antisymm (hd₀top ⟨c, hc₀mem⟩) (hc₀top ⟨d, hd₀mem⟩)
    contradiction
  · obtain ⟨j, hj1, hj2, hj3⟩ := hd₀mem.2
    obtain ⟨y, hy⟩ := pigeonhole_inter_eq hC hj3 hj2 c₀ hc₀
    rw [Set.eq_singleton_iff_unique_mem] at hy
    have sm : ¬y ≤ d := by
      by_cases h'' : y = d
      · obtain ⟨z, hz₁, hz₂⟩ := hC.1 y
        grind
      · exact hj2 (by grind) hj1 h''
    have ss : y ≤ c := hc₀top ⟨y, by grind⟩
    grw [ss] at sm
    exact sm

theorem overlap_top_encard_eq {α} [Finite α] [PartialOrder α] {C : Set (Set α)}
    (hC : IsChainPartition α (· ≤ ·) C) {A : Set α} (hA₁ : A.encard = C.encard)
    (hA₂ : IsAntichain (· ≤ ·) A) :
    (overlap_top C).encard = C.encard := by
  simp only [Subtype.exists, overlap_top]
  refine Set.encard_congr <| Equiv.ofBijective (fun b ↦ ⟨Classical.choose b.2, ?_⟩) ⟨?_, ?_⟩
  · grind [Classical.choose_spec]
  · intro b c heq
    have heq' : Classical.choose b.2 = Classical.choose c.2 :=
      congrArg Subtype.val heq
    obtain ⟨sb, hsb₁, hsb₂⟩ := Classical.choose_spec b.2
    obtain ⟨sc, hsc₁, hsc₂⟩ := Classical.choose_spec c.2
    obtain ⟨hbs, hbA⟩ := hsb₁
    obtain ⟨hcs, hcA⟩ := hsc₁
    have hbs' : b.1 ∈ Classical.choose c.2 := by
      rw [← heq']
      exact hbs
    have hcs' : c.1 ∈ Classical.choose b.2 := by
      rw [heq']
      exact hcs
    have hsb₁' : b.1 ∈ overlap_antichain C ⟨Classical.choose c.2, sc⟩ :=
      ⟨hbs', hbA⟩
    have hsc₁' : c.1 ∈ overlap_antichain C ⟨Classical.choose b.2, sb⟩ :=
      ⟨hcs', hcA⟩
    exact SetCoe.ext <| le_antisymm (hsc₂ ⟨b, hsb₁'⟩) (hsb₂ ⟨c, hsc₁'⟩)
  · intro b
    have (c : C) : (overlap_antichain C c).Nonempty := by
      apply Set.nonempty_coe_sort.mp
      simp only [Set.coe_setOf, nonempty_subtype]
      obtain ⟨b, hb⟩ := pigeonhole_inter_eq hC hA₁ hA₂ c.1 c.2
      rw [Set.eq_singleton_iff_unique_mem] at hb
      exact ⟨b, by grind, ⟨A, by grind, hA₂, hA₁⟩⟩
    obtain ⟨i, hi⟩ := hC.2 b.1 b.2 |>.mono (by grind) |>.exists_isTop _ (this b) (Set.toFinite _)
    use ⟨i.1, by grind⟩
    obtain ⟨d, hd₁, hd₂⟩ := hC.1 i
    grind [Classical.choose_spec]

theorem minChainPartition_eq_antichainWidth [PartialOrder α] [Finite α] :
    minChainPartition α (· ≤ ·) = antichainWidth α (· ≤ ·) := by
  have (eq := hcard) card := Nat.card α
  induction card using Nat.case_strong_induction_on generalizing α with
  | hz =>
    have := Finite.card_eq_zero_iff.mp hcard.symm
    rw [antichainWidth_eq_zero_iff α _ |>.mpr this, minChainPartition_eq_zero_iff α _ |>.mpr this]
  | hi n ih =>
    refine ENat.eq_of_forall_natCast_le_iff fun m ↦ ⟨fun hm ↦ ?_,
      fun hm ↦ le_trans hm (antichainWidth_le_minChainPartition _ _)⟩
    have : Nonempty α := Nat.card_pos_iff.mp (by grind) |>.1
    obtain ⟨a, ha⟩ := (@Set.univ α).toFinite.exists_maximal (Set.nonempty_iff_univ_nonempty.mp this)
    have heq := ih n (le_refl _) ↑(Set.univ \ {a}) (by simp [hcard.symm])
    obtain ⟨C, hC₁, hC₂⟩ := minChainPartition_exists ↑(Set.univ \ {a}) (· ≤ ·)
    obtain ⟨A, hA₁, hA₂⟩ := exists_eq_antichainWidth_of_finite ↑(Set.univ \ {a}) (· ≤ ·)
    let S : Set ↑(Set.univ \ {a}) := overlap_top C
    have Santi : IsAntichain (· ≤ ·) S := isAntichain_overlap_top hC₂
    by_cases h' : ∃ x : S, x.1 ≤ a
    · obtain ⟨x, hx⟩ := h'
      obtain ⟨t, ht, _⟩ := hC₂.1 x
      let Z := {z ∈ t | z ≤ x}
      have Zchain : IsChain (· ≤ ·) Z := hC₂.2 t ht.1 |>.mono (by simp [Z])
      let K := Subtype.val '' Z ∪ {a}
      have Kchain : IsChain (· ≤ ·) K := by
        refine isChain_union.mpr ⟨?_, IsChain.singleton, ?_⟩
        · exact Monotone.isChain_image (Subtype.mono_coe _) Zchain
        · simp only [Set.mem_image, Set.mem_setOf_eq, Subtype.exists, Set.mem_diff, Set.mem_univ,
            Set.mem_singleton_iff, true_and, exists_and_right, exists_eq_right, ne_eq, forall_eq,
            forall_exists_index, and_imp, Z]
          exact fun _ _ _ hle _ ↦ Or.inl <| le_trans (Subtype.coe_le_coe.mp hle) hx
      have Keq₁ := ih (n + 1 - K.ncard) (by simp [K, Set.one_le_ncard_insert a]) ↑(Set.univ \ K)
        (by simp [hcard, Set.ncard_diff (s := K)])
      have Keq₂ : antichainWidth ↑(Set.univ \ K) (· ≤ ·) + 1 = A.encard:= by
        have : antichainWidth ↑(Set.univ \ K) (· ≤ ·) = antichainWidth ↑(Set.univ \ Z) (· ≤ ·) := by
          refine antichainWidth_eq_of_relIso (e := { toEquiv := ?_, map_rel_iff' := ?_ })
          · refine Equiv.ofBijective (fun x ↦ ⟨⟨x.1, by grind⟩, by grind⟩) ?_
            exact Function.bijective_iff_has_inverse.mpr ⟨fun x ↦ ⟨x.1, by grind⟩,
              by grind [Function.leftInverse_iff_comp, Function.rightInverse_iff_comp]⟩
          · simp
        have hpg := pigeonhole_delete_largest hC₂ (by grind)
          (antichainWidth_ne_top_of_finite _ _) t Z Zchain ht.1 (fun y hy s _ _ _ ↦ by
            have := x.2
            simp only [Set.coe_setOf, Set.mem_setOf_eq, Subtype.exists, overlap_top, S] at this
            obtain ⟨l, _, _, hl⟩ := this
            simpa [Z, hy] using hl ⟨y, by grind, ⟨s, by grind⟩⟩
          )
        simp [hA₁, this, hpg]
      grw [hm, minChainPartition_le_sdiff_add_one α Kchain]
      rw [Keq₁, Keq₂, hA₁]
      exact antichainWidth_coe_univ (α := α) ▸ antichainWidth_subset _ _ (by simp)
    · have hia : IsAntichain (· ≤ ·) (Subtype.val '' (overlap_top C) ∪ {a}) := by
        refine isAntichain_union.mpr ⟨Santi.image _ (by simp), IsAntichain.singleton, ?_⟩
        simp only [Subtype.exists, Pi.compl_apply, compl_iff_not] at ⊢ h'
        grind [Maximal]
      have hCencard : C.encard + 1 = (Subtype.val '' S ∪ {a}).encard := by
        rw [Set.encard_union_eq (by simp), Function.Injective.encard_image (by simp)]
        simp [S, overlap_top_encard_eq hC₂ (hC₁ ▸ heq ▸ hA₁) hA₂]
      grw [hm, minChainPartition_le_sdiff_add_one α (s := {a}) (by simp),
        minChainPartition_le_encard _ _ _ hC₂, hCencard, encard_le_antichainWidth hia]

#print axioms minChainPartition_eq_antichainWidth

end dilworth
