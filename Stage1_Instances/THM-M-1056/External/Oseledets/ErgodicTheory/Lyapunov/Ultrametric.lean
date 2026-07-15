/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.LinearIndependent.Lemmas
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Lattice.Fold

/-!
# Ultrametric growth functions

Pure finite-dimensional linear algebra underlying the Lyapunov→Oseledets arc: the
**ultrametric growth function** abstraction that forces the Lyapunov spectrum to be finite
(at most `d = finrank ℝ E` values) and its sublevel sets to be subspaces.

A real-valued function `g` on the *nonzero* vectors of a real vector space `E` is an
**ultrametric growth function** (`IsUltrametricGrowth`) when it is scaling-invariant
(`g (c • v) = g v` for `c ≠ 0`) and non-Archimedean (`g (v + w) ≤ max (g v) (g w)`).
`g 0` is never referenced; the `v ≠ 0` side conditions are carried explicitly to avoid
`WithBot ℝ` arithmetic.

The main results:

* `IsUltrametricGrowth.add_eq_max_of_ne` — the ultrametric inequality is an equality when
  the two values differ;
* `IsUltrametricGrowth.linearIndependent_of_injOn` — vectors with pairwise-distinct values
  are linearly independent;
* `IsUltrametricGrowth.finite_range` — the set of realized values is finite;
* `IsUltrametricGrowth.sublevel` — each sublevel set `{v | v = 0 ∨ g v ≤ t}` is a submodule;
* `IsUltrametricGrowth.sublevel_mono` — these sublevel submodules are monotone in `t`.

Reference: Oseledets multiplicative ergodic theorem, ultrametric growth function.
-/

namespace ErgodicTheory

variable {E : Type*} [AddCommGroup E] [Module ℝ E]

/-- A real-valued function on the nonzero vectors of `E` is an **ultrametric growth
function** if it is scaling-invariant and non-Archimedean. (`g 0` is never referenced;
`v ≠ 0` side conditions are carried.) -/
structure IsUltrametricGrowth (g : E → ℝ) : Prop where
  /-- `g` is invariant under nonzero scaling. -/
  scaling : ∀ (c : ℝ) (v : E), c ≠ 0 → g (c • v) = g v
  /-- `g` satisfies the strong (non-Archimedean) triangle inequality. -/
  ultra : ∀ v w : E, v ≠ 0 → w ≠ 0 → v + w ≠ 0 → g (v + w) ≤ max (g v) (g w)

namespace IsUltrametricGrowth

variable {g : E → ℝ}

/-- The value at `-v` equals the value at `v` (scaling by `c = -1`). -/
theorem neg (h : IsUltrametricGrowth g) (v : E) : g (-v) = g v := by
  have := h.scaling (-1) v (by norm_num)
  simpa using this

/-- **Strict ultrametric: equality when the two values differ.** -/
theorem add_eq_max_of_ne (h : IsUltrametricGrowth g)
    {v w : E} (hv : v ≠ 0) (hw : w ≠ 0) (hvw : v + w ≠ 0) (hne : g v ≠ g w) :
    g (v + w) = max (g v) (g w) := by
  -- It suffices to prove the statement when `g v < g w`; the other case is symmetric
  -- via `v + w = w + v`.
  wlog hlt : g v < g w generalizing v w
  · have hwv : w + v ≠ 0 := by rwa [add_comm] at hvw
    have := this hw hv hwv (Ne.symm hne) (by
      rcases lt_or_gt_of_ne hne with h' | h'
      · exact absurd h' hlt
      · exact h')
    rwa [add_comm, max_comm] at this
  -- Now `g v < g w`, so `max (g v) (g w) = g w`.
  have hmax : max (g v) (g w) = g w := max_eq_right hlt.le
  rw [hmax]
  -- Upper bound: `g (v + w) ≤ max (g v) (g w) = g w`.
  have hle : g (v + w) ≤ g w := (h.ultra v w hv hw hvw).trans (le_of_eq hmax)
  -- Lower bound: `g w = g ((v + w) + (-v)) ≤ max (g (v+w)) (g (-v)) = max (g (v+w)) (g v)`.
  have hnegv : (-v) ≠ 0 := neg_ne_zero.mpr hv
  have hsum : (v + w) + (-v) = w := by abel
  have key : g w ≤ max (g (v + w)) (g v) := by
    have := h.ultra (v + w) (-v) hvw hnegv (by rw [hsum]; exact hw)
    rw [hsum, h.neg v] at this
    exact this
  -- If `g (v + w) < g w`, then `max (g (v+w)) (g v) < g w` since `g v < g w` too —
  -- contradicting `key`. Hence `g w ≤ g (v + w)`, and with `hle` we get equality.
  rcases le_or_gt (g w) (g (v + w)) with hge | hlt'
  · exact le_antisymm hle hge
  · exfalso
    have : max (g (v + w)) (g v) < g w := max_lt hlt' hlt
    exact (not_lt.mpr key) this

/-- A sum over a nonempty finset of nonzero vectors with pairwise-distinct `g`-values is
nonzero, and its `g`-value equals the maximum of the individual `g`-values. This iterated
`add_eq_max_of_ne` is the engine of ultrametric independence; the two conclusions are
proved together because each induction step needs the tail subsum to be nonzero. -/
theorem sum_ne_zero_and_g_eq_sup' (h : IsUltrametricGrowth g) {ι : Type*}
    {s : Finset ι} (hs : s.Nonempty) {v : ι → E}
    (hv : ∀ i ∈ s, v i ≠ 0)
    (hinj : Set.InjOn (g ∘ v) s) :
    (∑ i ∈ s, v i) ≠ 0 ∧ g (∑ i ∈ s, v i) = s.sup' hs fun i => g (v i) := by
  classical
  induction s using Finset.strongInduction with
  | _ s ih =>
    obtain ⟨t, a, hat, rfl⟩ := hs.exists_cons_eq
    -- `s = cons a t hat`, `a ∉ t`.
    rcases t.eq_empty_or_nonempty with rfl | ht
    · -- Singleton case.
      refine ⟨?_, ?_⟩ <;> simp [hv a (by simp)]
    · -- `t` is nonempty.
      have hsub : t ⊆ Finset.cons a t hat := Finset.subset_cons hat
      have hvt : ∀ i ∈ t, v i ≠ 0 := fun i hi => hv i (hsub hi)
      have hinjt : Set.InjOn (g ∘ v) t :=
        hinj.mono (by exact_mod_cast hsub)
      -- Inductive hypothesis on the tail.
      obtain ⟨hsumt, htail⟩ :=
        ih t (Finset.ssubset_cons hat) ht hvt hinjt
      have hva : v a ≠ 0 := hv a (by simp)
      -- `g (∑ t) = g (v b)` for some `b ∈ t`.
      obtain ⟨b, hb, hbval⟩ := Finset.exists_mem_eq_sup' ht (fun i => g (v i))
      -- `a ≠ b`, so `g (v a) ≠ g (v b)` by injectivity of `g ∘ v` on `s`.
      have hab : a ≠ b := fun hab => hat (hab ▸ hb)
      have hamem : a ∈ Finset.cons a t hat := Finset.mem_cons_self a t
      have hbmem : b ∈ Finset.cons a t hat := hsub hb
      have hne_val : g (v a) ≠ g (v b) := fun heq => hab (hinj hamem hbmem heq)
      have hgne : g (v a) ≠ g (∑ i ∈ t, v i) := by rw [htail, hbval]; exact hne_val
      -- The full sum is nonzero: otherwise `v a = -(∑ t)` would force equal `g`-values.
      have hfull : v a + ∑ i ∈ t, v i ≠ 0 := by
        intro hz
        have : v a = -(∑ i ∈ t, v i) := by
          rw [eq_neg_iff_add_eq_zero]; exact hz
        rw [this, h.neg] at hgne
        exact hgne rfl
      rw [Finset.sum_cons]
      refine ⟨hfull, ?_⟩
      rw [h.add_eq_max_of_ne hva hsumt hfull hgne, htail, Finset.sup'_cons]

/-- **Vectors of distinct values are linearly independent.** -/
theorem linearIndependent_of_injOn (h : IsUltrametricGrowth g) {ι : Type*} {v : ι → E}
    (hv : ∀ i, v i ≠ 0) (hinj : Function.Injective (g ∘ v)) :
    LinearIndependent ℝ v := by
  classical
  rw [linearIndependent_iff']
  intro s c hsum i hi
  -- Suppose some coefficient is nonzero; derive a contradiction from the support sum.
  by_contra hci
  -- The support `t` of the nonzero coefficients on `s` is nonempty (it contains `i`).
  set t := s.filter (fun j => c j ≠ 0) with ht_def
  have hit : i ∈ t := Finset.mem_filter.mpr ⟨hi, hci⟩
  have htne : t.Nonempty := ⟨i, hit⟩
  -- On the support, `∑ c j • v j = ∑_{all s} c j • v j = 0`.
  have hsum' : (∑ j ∈ t, c j • v j) = 0 := by
    rw [← hsum]
    apply Finset.sum_subset (Finset.filter_subset _ _)
    intro j hjs hjt
    have : c j = 0 := by
      by_contra hcj
      exact hjt (Finset.mem_filter.mpr ⟨hjs, hcj⟩)
    rw [this, zero_smul]
  -- The vectors `w j = c j • v j` are nonzero on `t`, with `g ∘ w` injective on `t`.
  have hwne : ∀ j ∈ t, c j • v j ≠ 0 := by
    intro j hj
    have hcj : c j ≠ 0 := (Finset.mem_filter.mp hj).2
    exact smul_ne_zero hcj (hv j)
  have hginj : Set.InjOn (g ∘ fun j => c j • v j) t := by
    intro x hx y hy hxy
    have hcx : c x ≠ 0 := (Finset.mem_filter.mp hx).2
    have hcy : c y ≠ 0 := (Finset.mem_filter.mp hy).2
    simp only [Function.comp_apply] at hxy
    rw [h.scaling (c x) (v x) hcx, h.scaling (c y) (v y) hcy] at hxy
    exact hinj hxy
  -- The support sum is nonzero by the engine lemma — contradiction with `hsum'`.
  obtain ⟨hne0, _⟩ := h.sum_ne_zero_and_g_eq_sup' htne hwne hginj
  exact hne0 hsum'

/-- The set of values is **finite** (the Lyapunov spectrum has at most `d = finrank ℝ E`
elements). -/
theorem finite_range [FiniteDimensional ℝ E] (h : IsUltrametricGrowth g) :
    (Set.range fun v : {v : E // v ≠ 0} => g v).Finite := by
  classical
  -- If the range were infinite, an injection `ℕ ↪ range` yields infinitely many distinct
  -- values, hence (restricting to `finrank + 1` of them) too many independent vectors.
  by_contra hinf
  rw [Set.not_finite] at hinf
  set S := Set.range fun v : {v : E // v ≠ 0} => g v with hS
  -- For each point of `S` choose a witnessing nonzero vector.
  have hwit : ∀ r : S, ∃ w : E, w ≠ 0 ∧ g w = r := by
    rintro ⟨r, hr⟩
    obtain ⟨v, hv⟩ := hr
    exact ⟨v.1, v.2, hv⟩
  choose w hw hwval using hwit
  -- An injection `ℕ ↪ S`, then restrict to `Fin (finrank + 1)`.
  set e : ℕ ↪ S := hinf.natEmbedding S with he
  set d := Module.finrank ℝ E with hd
  -- The vectors `u k = w (e k)` for `k : Fin (d + 1)`.
  set u : Fin (d + 1) → E := fun k => w (e k) with hu
  have hune : ∀ k, u k ≠ 0 := fun k => hw (e k)
  -- `g ∘ u` is injective: distinct `k` give distinct values via `e` and the witness values.
  have huinj : Function.Injective (g ∘ u) := by
    intro k₁ k₂ hk
    simp only [Function.comp_apply, hu] at hk
    rw [hwval (e k₁), hwval (e k₂)] at hk
    -- `(e k₁ : ℝ) = (e k₂ : ℝ)` forces `e k₁ = e k₂`, hence `k₁ = k₂`.
    have hee : e (k₁ : ℕ) = e (k₂ : ℕ) := Subtype.ext hk
    exact Fin.val_injective (e.injective hee)
  -- Linear independence of `d + 1` vectors contradicts `finrank = d`.
  have hli : LinearIndependent ℝ u := h.linearIndependent_of_injOn hune huinj
  have hcard : Fintype.card (Fin (d + 1)) ≤ d := by
    have := hli.fintype_card_le_finrank
    rwa [← hd] at this
  simp only [Fintype.card_fin] at hcard
  omega

/-- The **sublevel set** `{v | v = 0 ∨ g v ≤ t}` is a submodule of `E`. Closure under
addition is the non-Archimedean inequality, closure under scaling is scaling-invariance,
and `0` lies in it via the left disjunct. -/
def sublevel (h : IsUltrametricGrowth g) (t : ℝ) : Submodule ℝ E where
  carrier := {v | v = 0 ∨ g v ≤ t}
  zero_mem' := Or.inl rfl
  add_mem' := by
    intro v w hv hw
    -- `hv : v = 0 ∨ g v ≤ t`, `hw : w = 0 ∨ g w ≤ t`; goal `v + w = 0 ∨ g (v+w) ≤ t`.
    rcases hv with rfl | hv
    · -- `v = 0`: `0 + w = w ∈ carrier`.
      simpa using hw
    · rcases hw with rfl | hw
      · -- `w = 0`: `v + 0 = v ∈ carrier`.
        simpa using Or.inr hv
      · -- Both nonzero with `g ≤ t`.
        by_cases hvw : v + w = 0
        · exact Or.inl hvw
        · by_cases hv0 : v = 0
          · subst hv0; right; simpa using hw
          · by_cases hw0 : w = 0
            · subst hw0; right; simpa using hv
            · exact Or.inr ((h.ultra v w hv0 hw0 hvw).trans (max_le hv hw))
  smul_mem' := by
    intro c v hv
    rcases hv with rfl | hv
    · left; simp
    · by_cases hc : c = 0
      · left; simp [hc]
      · right; rw [h.scaling c v hc]; exact hv

@[simp]
theorem mem_sublevel (h : IsUltrametricGrowth g) (t : ℝ) (v : E) :
    v ∈ h.sublevel t ↔ v = 0 ∨ g v ≤ t := Iff.rfl

/-- `sublevel` is **monotone** in the threshold `t`. -/
theorem sublevel_mono (h : IsUltrametricGrowth g) : Monotone h.sublevel := by
  intro t₁ t₂ hle v hv
  rw [mem_sublevel] at hv ⊢
  rcases hv with rfl | hv
  · exact Or.inl rfl
  · exact Or.inr (hv.trans hle)

end IsUltrametricGrowth

end ErgodicTheory
