/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
/-
Port notice: vendored from `marcmorningstar/lean4-ergodic-theory` at commit
`ed3fa6b8a30594eeb791160563942ba115581aa0`. The upstream sibling import is local,
and `integral_finsetSum` is spelled `integral_finset_sum` on Lean 4.29; see
`PORT_PROVENANCE.md`.
-/
import KingmanFekete

/-!
# The Derriennic "leaders" route and the maximal inequality

The Derriennic / Karlsson route towards `limsup ≤ liminf` almost everywhere: the "leaders"
construction and Derriennic's maximal inequality (Karlsson, *A proof of the subadditive ergodic
theorem*, Lemma 3.4 / Prop 3.5).

Internal infrastructure for Kingman's theorem (the `ErgodicTheory.Kingman` namespace); the public
statement is in `ErgodicTheory.Ergodic.Kingman.Core`.
-/

open MeasureTheory Filter Topology
open scoped ENNReal

namespace ErgodicTheory.Kingman

variable {X : Type*} [MeasurableSpace X] {μ : Measure X} {T : X → X}

/-! ### The Derriennic "leaders" route to `limsup ≤ liminf` a.e.

We follow Karlsson, *A proof of the subadditive ergodic theorem* (Riesz/Derriennic route).
The four ingredients are:

* `sum_leaders_nonpos`: Riesz's combinatorial "leader" lemma (Karlsson Lemma 3.2),
  pure finite induction, no measure theory.
* `sum_bcoc_telescope`: the telescoping identity
  `a n x − a (n−k) (T^[k] x) = ∑ bₙ₋ᵢ(T^[i]x)`.
* `limsup_setIntegral_div_nonpos`: Derriennic's maximal inequality (Karlsson Lemma 3.4 /
  Prop 3.5): for a `T`-invariant set `B` on which `liminf (aₙ/n) < α`, one has
  `limsup (1/n) ∫_B aₙ ≤ α·μ(B)`.
* the `E_{α,β}` two-bound contradiction (Karlsson §3.3), mirroring the additive
  `measure_setOf_lt_limsup_eq_zero` in `Birkhoff.lean`. -/

open Classical in
/-- The set of leaders of length `n` for partial sums `S`. -/
noncomputable def leaderSet (S : ℕ → ℝ) (n : ℕ) : Finset ℕ :=
  (Finset.range n).filter (fun u => ∃ j, u < j ∧ j ≤ n ∧ S j < S u)

/-- A leader `u ≥ s` of length `n` (with `s ≤ n`) is, after shifting indices down by `s`, a
leader of the shifted partial sums `S (· + s)` of length `n − s`, and conversely. (The leader
condition only inspects partial sums strictly after `u`, so dropping the prefix `[0, s)` is
harmless.) This is the reindexing engine of the leader-lemma induction. -/
theorem mem_leaderSet_shift (S : ℕ → ℝ) (s n u : ℕ) (hsn : s ≤ n) :
    (u + s ∈ leaderSet S n ∧ s ≤ u + s) ↔ u ∈ leaderSet (fun j => S (j + s)) (n - s) := by
  classical
  simp only [leaderSet, Finset.mem_filter, Finset.mem_range]
  constructor
  · rintro ⟨⟨_, j, hj1, hj2, hj3⟩, _⟩
    refine ⟨by omega, j - s, by omega, by omega, ?_⟩
    rwa [Nat.sub_add_cancel (by omega)]
  · rintro ⟨hu, j, hj1, hj2, hj3⟩
    refine ⟨⟨by omega, j + s, by omega, by omega, hj3⟩, by omega⟩

/-- **Riesz's leader lemma** (Karlsson, Lemma 3.2), in partial-sum form. Given a
sequence of partial sums `S : ℕ → ℝ` (think `S j = c 0 + … + c (j−1)`, `S 0 = 0`), call an
index `u < n` a *leader* (of length `n`) if some later partial sum drops strictly below `S u`,
i.e. `∃ j, u < j ≤ n ∧ S j < S u`. (This matches Karlsson's "a forward partial sum
`c u + … + c (j−1) = S j − S u` is negative".) Then the sum of the increments `S (u+1) − S u`
over the leaders is non-positive. Strong induction on `n`. -/
theorem sum_leaders_nonpos :
    ∀ (n : ℕ) (S : ℕ → ℝ), ∑ u ∈ leaderSet S n, (S (u + 1) - S u) ≤ 0 := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro S
    match n with
    | 0 => simp [leaderSet]
    | (n + 1) =>
      classical
      by_cases h0 : (0 : ℕ) ∈ leaderSet S (n + 1)
      · -- `0` is a leader: take the least partial-sum index `k` with `S k < S 0`.
        simp only [leaderSet, Finset.mem_filter, Finset.mem_range] at h0
        obtain ⟨_, j0, hj01, hj02, hj03⟩ := h0
        set P : ℕ → Prop := fun j => j ≤ n + 1 ∧ S j < S 0 with hP
        have hPex : ∃ j, P j := ⟨j0, hj02, hj03⟩
        set k : ℕ := Nat.find hPex with hk
        have hkP : P k := Nat.find_spec hPex
        have hk0 : 0 < k := by
          rcases Nat.eq_zero_or_pos k with h | h
          · exfalso; rw [h] at hkP; exact lt_irrefl _ hkP.2
          · exact h
        have hkle : k ≤ n + 1 := hkP.1
        have hkmin : ∀ m, m < k → ¬ P m := fun m hm => Nat.find_min hPex hm
        -- For each `i < k`, `S k < S i`: `S i ≥ S 0` (minimality) and `S k < S 0`.
        have hbeat : ∀ i, i < k → S k < S i := by
          intro i hik
          rcases Nat.eq_zero_or_pos i with hi0 | _
          · subst hi0; exact hkP.2
          · have hSi : S 0 ≤ S i := by
              by_contra hlt; rw [not_le] at hlt; exact hkmin i hik ⟨by omega, hlt⟩
            linarith [hkP.2]
        -- Split the leader set as the prefix `range k` together with the leaders `≥ k`.
        have hprefix : ∀ i, i < k → i ∈ leaderSet S (n + 1) := by
          intro i hik
          simp only [leaderSet, Finset.mem_filter, Finset.mem_range]
          exact ⟨by omega, k, hik, hkle, hbeat i hik⟩
        -- Split the leader sum into the prefix `{u < k}` and the tail `{¬ u < k}`.
        rw [← Finset.sum_filter_add_sum_filter_not (leaderSet S (n + 1)) (fun u => u < k)
          (fun u => S (u + 1) - S u)]
        -- The prefix filter is exactly `range k`; its increment sum telescopes to `S k - S 0 < 0`.
        have hpref_eq : (leaderSet S (n + 1)).filter (fun u => u < k) = Finset.range k := by
          ext u
          simp only [Finset.mem_filter, Finset.mem_range, and_iff_right_iff_imp]
          intro hu; exact hprefix u hu
        rw [hpref_eq, Finset.sum_range_sub S k]
        -- The tail filter reindexes to the leaders of the shifted partial sums of length `n+1-k`.
        have htail : ∑ u ∈ (leaderSet S (n + 1)).filter (fun u => ¬ u < k), (S (u + 1) - S u)
            ≤ 0 := by
          set S' : ℕ → ℝ := fun j => S (j + k) with hS'
          have hmap : (leaderSet S (n + 1)).filter (fun u ↦ ¬ u < k)
              = (leaderSet S' (n + 1 - k)).map
                  ⟨fun u ↦ u + k, fun a b h ↦ Nat.add_right_cancel h⟩ := by
            ext u
            simp only [Finset.mem_filter, Finset.mem_map, Function.Embedding.coeFn_mk, not_lt]
            constructor
            · rintro ⟨hmem, hku⟩
              refine ⟨u - k, ?_, by omega⟩
              have := (mem_leaderSet_shift S k (n + 1) (u - k) hkle).1
              rw [Nat.sub_add_cancel hku] at this
              exact (this ⟨hmem, by omega⟩)
            · rintro ⟨v, hv, rfl⟩
              refine ⟨?_, by omega⟩
              exact ((mem_leaderSet_shift S k (n + 1) v hkle).2 hv).1
          rw [hmap, Finset.sum_map]
          simp only [Function.Embedding.coeFn_mk]
          have hval : ∀ v, S (v + k + 1) - S (v + k) = S' (v + 1) - S' v := by
            intro v; simp only [hS']; ring_nf
          simp_rw [hval]
          exact ih (n + 1 - k) (by omega) S'
        have := hkP.2; linarith [htail]
      · -- `0` is not a leader: every leader lies in `{1,…,n}`; shift down by 1 and apply IH.
        set S' : ℕ → ℝ := fun j => S (j + 1) with hS'
        have hmap : leaderSet S (n + 1)
            = (leaderSet S' n).map ⟨fun u => u + 1, fun a b h => Nat.add_right_cancel h⟩ := by
          ext u
          simp only [Finset.mem_map, Function.Embedding.coeFn_mk]
          constructor
          · intro hmem
            have hu0 : u ≠ 0 := by rintro rfl; exact h0 hmem
            refine ⟨u - 1, ?_, by omega⟩
            have := (mem_leaderSet_shift S 1 (n + 1) (u - 1) (by omega)).1
            rw [Nat.sub_add_cancel (by omega)] at this
            exact this ⟨hmem, by omega⟩
          · rintro ⟨v, hv, rfl⟩
            exact ((mem_leaderSet_shift S 1 (n + 1) v (by omega)).2 hv).1
        rw [hmap, Finset.sum_map]
        simp only [Function.Embedding.coeFn_mk]
        have hval : ∀ v, S (v + 1 + 1) - S (v + 1) = S' (v + 1) - S' v := fun v => rfl
        simp_rw [hval]
        exact ih n (by omega) S'

omit [MeasurableSpace X] in
/-- **Leader inequality for the cocycle** (Karlsson, §3.2, the pointwise input of his
Lemma 3.4). Fix `x` and length `n`, and consider the partial sums
`S j := g n x − g (n−j) (T^[j] x)` (so `S 0 = 0`, and the increment `S (k+1) − S k` equals
`g (n−k) (T^[k] x) − g (n−k−1) (T^[k+1] x)`). With these partial sums an index `k` is a
*leader* exactly when `T^[k] x` lies in Karlsson's set `Λ_{n−k}`. The leader lemma
`sum_leaders_nonpos` then bounds the sum of the increments over the leaders by `0`. This is
the purely pointwise/combinatorial heart of Derriennic's maximal inequality (the measure
theory enters only when one integrates this inequality over a `T`-invariant set). -/
theorem sum_leaders_cocycle_nonpos (g : ℕ → X → ℝ) (n : ℕ) (x : X) :
    ∑ k ∈ leaderSet (fun j => g n x - g (n - j) (T^[j] x)) n,
        (g (n - k) (T^[k] x) - g (n - (k + 1)) (T^[k + 1] x)) ≤ 0 := by
  have h := sum_leaders_nonpos n (fun j => g n x - g (n - j) (T^[j] x))
  refine le_of_eq_of_le (Finset.sum_congr rfl (fun k _ => ?_)) h
  ring

/-! ### Derriennic's maximal inequality (Karlsson Lemma 3.4 / Prop 3.5)

Karlsson's Λ-set and A-set, and the integral telescoping of `sum_leaders_cocycle_nonpos`
over a `T`-invariant set `B`. -/

/-- The increment of the cocycle: `bcoc g i x = g i x − g (i−1) (T x)`. (Karlsson's `b_i`.) -/
def bcoc (g : ℕ → X → ℝ) (i : ℕ) (x : X) : ℝ := g i x - g (i - 1) (T x)

/-- Karlsson's set `Λ_m = {y | inf_{1≤k≤m} (g m y − g (m−k)(T^[k] y)) < 0}`. -/
def lambdaSet (g : ℕ → X → ℝ) (m : ℕ) : Set X :=
  {y | ∃ k, 1 ≤ k ∧ k ≤ m ∧ g m y - g (m - k) (T^[k] y) < 0}

/-- Karlsson's set `A_m = {y | inf_{1≤k≤m} g k y < 0} ⊆ Λ_m`. -/
def aSet (g : ℕ → X → ℝ) (m : ℕ) : Set X :=
  {y | ∃ k, 1 ≤ k ∧ k ≤ m ∧ g k y < 0}

omit [MeasurableSpace X] in
/-- `A_m ⊆ Λ_m` by subadditivity: `g m y ≤ g (m−k) y + g k (T^[m−k] y)`… actually the
inclusion uses `g m y ≤ g (m−k) (·)`; we prove it via `g m y − g (m−k)(T^[k] y) ≤ g k y` when
`k ≤ m`. Indeed `g m y = g (k + (m−k)) y ≤ g k y + g (m−k) (T^[k] y)`. -/
theorem aSet_subset_lambdaSet {g : ℕ → X → ℝ} (hsub : IsSubadditiveCocycle T g) (m : ℕ) :
    aSet g m ⊆ lambdaSet (T := T) g m := by
  rintro y ⟨k, hk1, hkm, hk⟩
  refine ⟨k, hk1, hkm, ?_⟩
  have hdecomp : g m y ≤ g k y + g (m - k) (T^[k] y) := by
    have := hsub.apply_add_le k (m - k) y
    rwa [Nat.add_sub_cancel' hkm] at this
  linarith

omit [MeasurableSpace X] in
/-- The leader-membership identification (Karlsson, §3.2): an index `k` is a leader of the
partial sums `S j = g n x − g (n−j)(T^[j] x)` of length `n` exactly when `k < n` and
`T^[k] x ∈ Λ_{n−k}`. -/
theorem mem_leaderSet_iff_mem_lambdaSet (g : ℕ → X → ℝ) (n k : ℕ) (x : X) :
    k ∈ leaderSet (fun j => g n x - g (n - j) (T^[j] x)) n ↔
      k < n ∧ T^[k] x ∈ lambdaSet (T := T) g (n - k) := by
  classical
  simp only [leaderSet, Finset.mem_filter, Finset.mem_range, lambdaSet, Set.mem_setOf_eq]
  constructor
  · rintro ⟨hkn, j, hkj, hjn, hlt⟩
    refine ⟨hkn, j - k, by omega, by omega, ?_⟩
    have h1 : T^[j - k] (T^[k] x) = T^[j] x := by
      rw [← Function.iterate_add_apply]; congr 1; omega
    have h2 : n - k - (j - k) = n - j := by omega
    rw [h1, h2]
    linarith
  · rintro ⟨hkn, m, hm1, hmnk, hlt⟩
    refine ⟨hkn, k + m, by omega, by omega, ?_⟩
    have h1 : T^[m] (T^[k] x) = T^[k + m] x := by
      rw [← Function.iterate_add_apply]; congr 1; omega
    have h2 : n - k - m = n - (k + m) := by omega
    rw [h1, h2] at hlt
    linarith

omit [MeasurableSpace X] in
/-- **Telescoping** (Karlsson §3.2): `∑_{k<n} bcoc g (n−k) (T^[k] x) = g n x − g 0 (T^[n] x)`. -/
theorem sum_bcoc_telescope (g : ℕ → X → ℝ) (n : ℕ) (x : X) :
    ∑ k ∈ Finset.range n, bcoc (T := T) g (n - k) (T^[k] x)
      = g n x - g 0 (T^[n] x) := by
  set h : ℕ → ℝ := fun k => g (n - k) (T^[k] x) with hh
  have hterm : ∀ k ∈ Finset.range n, bcoc (T := T) g (n - k) (T^[k] x) = h k - h (k + 1) := by
    intro k _
    simp only [hh, bcoc]
    rw [Function.iterate_succ_apply', show n - k - 1 = n - (k + 1) by omega]
  rw [Finset.sum_congr rfl hterm, Finset.sum_range_sub' h n]
  simp only [hh, Nat.sub_zero, Function.iterate_zero, id_eq, Nat.sub_self]

open Classical in
omit [MeasurableSpace X] in
/-- **Pointwise leader inequality, Λ-form.** Summing the increments `bcoc g (n−k)`
along the orbit over the indices `k < n` with `T^[k] x ∈ Λ_{n−k}` gives a non-positive number.
(Recast of `sum_leaders_cocycle_nonpos` via the membership identification.) -/
theorem sum_bcoc_lambda_nonpos (g : ℕ → X → ℝ) (n : ℕ) (x : X) :
    ∑ k ∈ (Finset.range n).filter (fun k => T^[k] x ∈ lambdaSet (T := T) g (n - k)),
        bcoc (T := T) g (n - k) (T^[k] x) ≤ 0 := by
  classical
  have hset : (Finset.range n).filter (fun k => T^[k] x ∈ lambdaSet (T := T) g (n - k))
      = leaderSet (fun j => g n x - g (n - j) (T^[j] x)) n := by
    ext k
    simp only [Finset.mem_filter, Finset.mem_range, mem_leaderSet_iff_mem_lambdaSet]
  rw [hset]
  refine le_of_eq_of_le (Finset.sum_congr rfl (fun k _ => ?_)) (sum_leaders_cocycle_nonpos g n x)
  simp only [bcoc]
  rw [Function.iterate_succ_apply', show n - k - 1 = n - (k + 1) by omega]

/-- Karlsson's localized increment `ψ_i = 1_{Λ_i} · bcoc g i`. -/
noncomputable def psiCoc (g : ℕ → X → ℝ) (i : ℕ) : X → ℝ :=
  (lambdaSet (T := T) g i).indicator (bcoc (T := T) g i)

open Classical in
omit [MeasurableSpace X] in
/-- **Indicator form of the pointwise leader inequality.** The full-range orbit sum of
the localized increments `ψ_{n−k} ∘ T^[k]` is non-positive (it equals the filtered leader sum
of `sum_bcoc_lambda_nonpos`, the extra terms being zero off `Λ`). -/
theorem sum_psiCoc_comp_nonpos (g : ℕ → X → ℝ) (n : ℕ) (x : X) :
    ∑ k ∈ Finset.range n, psiCoc (T := T) g (n - k) (T^[k] x) ≤ 0 := by
  classical
  have hrw : ∑ k ∈ Finset.range n, psiCoc (T := T) g (n - k) (T^[k] x)
      = ∑ k ∈ (Finset.range n).filter (fun k => T^[k] x ∈ lambdaSet (T := T) g (n - k)),
          bcoc (T := T) g (n - k) (T^[k] x) := by
    rw [Finset.sum_filter]
    refine Finset.sum_congr rfl (fun k _ => ?_)
    simp only [psiCoc, Set.indicator_apply]
  rw [hrw]
  exact sum_bcoc_lambda_nonpos g n x

/-- `bcoc g i = g i − g (i−1) ∘ T` is integrable. -/
theorem integrable_bcoc (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (i : ℕ) : Integrable (bcoc (T := T) g i) μ := by
  have hcomp : Integrable (fun x => g (i - 1) (T x)) μ :=
    hT.integrable_comp_of_integrable (hint (i - 1))
  exact (hint i).sub hcomp

/-- `lambdaSet g m` is null-measurable: a finite union over `1 ≤ k ≤ m` of the null-measurable
sets `{g m − g (m−k) ∘ T^[k] < 0}`. -/
theorem nullMeasurableSet_lambdaSet (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (m : ℕ) :
    NullMeasurableSet (lambdaSet (T := T) g m) μ := by
  classical
  have hrw : lambdaSet (T := T) g m
      = ⋃ k ∈ (Finset.Icc 1 m : Finset ℕ), {y | g m y - g (m - k) (T^[k] y) < 0} := by
    ext y
    simp only [lambdaSet, Set.mem_setOf_eq, Set.mem_iUnion, Finset.mem_Icc]
    constructor
    · rintro ⟨k, hk1, hkm, hlt⟩; exact ⟨k, ⟨hk1, hkm⟩, hlt⟩
    · rintro ⟨k, ⟨hk1, hkm⟩, hlt⟩; exact ⟨k, hk1, hkm, hlt⟩
  rw [hrw]
  refine NullMeasurableSet.biUnion (Finset.Icc 1 m).countable_toSet (fun k _ => ?_)
  have hg1 : AEMeasurable (g m) μ := (hint m).aemeasurable
  have hg2 : AEMeasurable (fun y => g (m - k) (T^[k] y)) μ :=
    (hT.iterate k).integrable_comp_of_integrable (hint (m - k)) |>.aemeasurable
  exact nullMeasurableSet_lt (hg1.sub hg2) aemeasurable_const

/-- `psiCoc g i` is integrable (indicator of a null-measurable set of an integrable function). -/
theorem integrable_psiCoc (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (i : ℕ) : Integrable (psiCoc (T := T) g i) μ :=
  (integrable_bcoc hT hint i).indicator₀ (nullMeasurableSet_lambdaSet hT hint i)

/-- Set-integral invariance under `T^[k]` for a measurable `T`-invariant set `s`:
`∫_s (h ∘ T^[k]) = ∫_s h`. -/
theorem setIntegral_comp_iterate_of_invariants
    (hT : MeasurePreserving T μ μ) {h : X → ℝ} (hh : AEStronglyMeasurable h μ)
    {s : Set X} (hs : MeasurableSet s) (hsinv : T ⁻¹' s = s) (k : ℕ) :
    ∫ x in s, h (T^[k] x) ∂μ = ∫ x in s, h x ∂μ := by
  have hmp : MeasurePreserving (T^[k]) μ μ := hT.iterate k
  have hsinvk : T^[k] ⁻¹' s = s := by
    clear hh hs hmp
    induction k with
    | zero => simp
    | succ k ih => rw [Function.iterate_succ', Set.preimage_comp, hsinv, ih]
  have hmap : Measure.map (T^[k]) μ = μ := hmp.map_eq
  have hhmap : AEStronglyMeasurable h (Measure.map (T^[k]) μ) := by rw [hmap]; exact hh
  calc ∫ x in s, h (T^[k] x) ∂μ
      = ∫ x in T^[k] ⁻¹' s, h (T^[k] x) ∂μ := by rw [hsinvk]
    _ = ∫ y in s, h y ∂(Measure.map (T^[k]) μ) := (setIntegral_map hs hhmap hmp.aemeasurable).symm
    _ = ∫ y in s, h y ∂μ := by rw [hmap]

/-- **Integrated leader inequality** (Karlsson Lemma 3.4, the telescoped integral). For a
measurable `T`-invariant set `B`, the partial sum of localized increment integrals is
non-positive: `∑_{i=1}^n ∫_{B} ψ_i ≤ 0`, where `ψ_i = 1_{Λ_i} bcoc g i`. -/
theorem sum_setIntegral_psiCoc_nonpos
    (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ} (hint : ∀ n, Integrable (g n) μ)
    {B : Set X} (hB : MeasurableSet B) (hBinv : T ⁻¹' B = B) (n : ℕ) :
    ∑ i ∈ Finset.Icc 1 n, ∫ x in B, psiCoc (T := T) g i x ∂μ ≤ 0 := by
  classical
  -- Integrate the pointwise inequality `∑_{k<n} ψ_{n-k}(T^[k] x) ≤ 0` over `B`.
  have hpt : ∫ x in B, (∑ k ∈ Finset.range n, psiCoc (T := T) g (n - k) (T^[k] x)) ∂μ ≤ 0 :=
    integral_nonpos_of_ae (Filter.Eventually.of_forall (fun x => sum_psiCoc_comp_nonpos g n x))
  -- Pull the finite sum out and apply the change of variables for `T^[k]`.
  rw [integral_finset_sum (μ := μ.restrict B) (Finset.range n)
    (f := fun k x => psiCoc (T := T) g (n - k) (T^[k] x))
    (fun k _ => ((hT.iterate k).integrable_comp_of_integrable
      (integrable_psiCoc hT hint (n - k))).restrict)] at hpt
  -- `∫_B ψ_{n-k} ∘ T^[k] = ∫_B ψ_{n-k}`.
  have hcv : ∀ k ∈ Finset.range n,
      ∫ x in B, psiCoc (T := T) g (n - k) (T^[k] x) ∂μ
        = ∫ x in B, psiCoc (T := T) g (n - k) x ∂μ := fun k _ =>
    setIntegral_comp_iterate_of_invariants hT
      (integrable_psiCoc hT hint (n - k)).aestronglyMeasurable hB hBinv k
  rw [Finset.sum_congr rfl hcv] at hpt
  -- Reindex `i = n - k` over `range n` to `Icc 1 n`.
  have hreindex : ∑ k ∈ Finset.range n, ∫ x in B, psiCoc (T := T) g (n - k) x ∂μ
      = ∑ i ∈ Finset.Icc 1 n, ∫ x in B, psiCoc (T := T) g i x ∂μ := by
    refine Finset.sum_nbij' (fun k => n - k) (fun i => n - i) ?_ ?_ ?_ ?_ ?_
    · intro k hk; simp only [Finset.mem_range] at hk; simp only [Finset.mem_Icc]; omega
    · intro i hi; simp only [Finset.mem_Icc] at hi; simp only [Finset.mem_range]; omega
    · intro k hk; simp only [Finset.mem_range] at hk; dsimp only; omega
    · intro i hi; simp only [Finset.mem_Icc] at hi; dsimp only; omega
    · intro k _; rfl
  rw [hreindex] at hpt
  exact hpt

/-- **Integrated telescoping** over an invariant set `B`:
`∑_{i=1}^m ∫_B bcoc g i = ∫_B g m − ∫_B g 0`. -/
theorem sum_setIntegral_bcoc_eq
    (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ} (hint : ∀ n, Integrable (g n) μ)
    {B : Set X} (hB : MeasurableSet B) (hBinv : T ⁻¹' B = B) (m : ℕ) :
    ∑ i ∈ Finset.Icc 1 m, ∫ x in B, bcoc (T := T) g i x ∂μ
      = (∫ x in B, g m x ∂μ) - ∫ x in B, g 0 x ∂μ := by
  classical
  have hcv : ∀ k ∈ Finset.range m,
      ∫ x in B, bcoc (T := T) g (m - k) (T^[k] x) ∂μ
        = ∫ x in B, bcoc (T := T) g (m - k) x ∂μ := fun k _ =>
    setIntegral_comp_iterate_of_invariants hT
      (integrable_bcoc hT hint (m - k)).aestronglyMeasurable hB hBinv k
  have hreindex : ∑ k ∈ Finset.range m, ∫ x in B, bcoc (T := T) g (m - k) x ∂μ
      = ∑ i ∈ Finset.Icc 1 m, ∫ x in B, bcoc (T := T) g i x ∂μ := by
    refine Finset.sum_nbij' (fun k => m - k) (fun i => m - i) ?_ ?_ ?_ ?_ ?_
    · intro k hk; simp only [Finset.mem_range] at hk; simp only [Finset.mem_Icc]; omega
    · intro i hi; simp only [Finset.mem_Icc] at hi; simp only [Finset.mem_range]; omega
    · intro k hk; simp only [Finset.mem_range] at hk; dsimp only; omega
    · intro i hi; simp only [Finset.mem_Icc] at hi; dsimp only; omega
    · intro k _; rfl
  calc ∑ i ∈ Finset.Icc 1 m, ∫ x in B, bcoc (T := T) g i x ∂μ
      = ∑ k ∈ Finset.range m, ∫ x in B, bcoc (T := T) g (m - k) x ∂μ := hreindex.symm
    _ = ∑ k ∈ Finset.range m, ∫ x in B, bcoc (T := T) g (m - k) (T^[k] x) ∂μ :=
        (Finset.sum_congr rfl hcv).symm
    _ = ∫ x in B, (∑ k ∈ Finset.range m, bcoc (T := T) g (m - k) (T^[k] x)) ∂μ :=
        (integral_finset_sum (μ := μ.restrict B) (Finset.range m)
          (f := fun k x => bcoc (T := T) g (m - k) (T^[k] x))
          (fun k _ => ((hT.iterate k).integrable_comp_of_integrable
            (integrable_bcoc hT hint (m - k))).restrict)).symm
    _ = ∫ x in B, (g m x - g 0 (T^[m] x)) ∂μ :=
        integral_congr_ae (Filter.Eventually.of_forall (fun x => sum_bcoc_telescope g m x))
    _ = (∫ x in B, g m x ∂μ) - ∫ x in B, g 0 (T^[m] x) ∂μ :=
        integral_sub (hint m).restrict
          ((hT.iterate m).integrable_comp_of_integrable (hint 0)).restrict
    _ = (∫ x in B, g m x ∂μ) - ∫ x in B, g 0 x ∂μ := by
        rw [setIntegral_comp_iterate_of_invariants hT (hint 0).aestronglyMeasurable hB hBinv m]

omit [MeasurableSpace X] in
/-- `aSet g` is monotone in the length. -/
theorem aSet_mono {g : ℕ → X → ℝ} : Monotone (aSet g) := by
  intro a b hab y hy
  obtain ⟨k, hk1, hka, hk⟩ := hy
  exact ⟨k, hk1, le_trans hka hab, hk⟩

/-- `aSet g m` is null-measurable. -/
theorem nullMeasurableSet_aSet {g : ℕ → X → ℝ} (hint : ∀ n, Integrable (g n) μ) (m : ℕ) :
    NullMeasurableSet (aSet g m) μ := by
  classical
  have hrw : aSet g m = ⋃ k ∈ (Finset.Icc 1 m : Finset ℕ), {y | g k y < 0} := by
    ext y; simp only [aSet, Set.mem_setOf_eq, Set.mem_iUnion, Finset.mem_Icc]
    constructor
    · rintro ⟨k, hk1, hkm, hlt⟩; exact ⟨k, ⟨hk1, hkm⟩, hlt⟩
    · rintro ⟨k, ⟨hk1, hkm⟩, hlt⟩; exact ⟨k, hk1, hkm, hlt⟩
  rw [hrw]
  exact NullMeasurableSet.biUnion (Finset.Icc 1 m).countable_toSet
    (fun k _ => nullMeasurableSet_lt (hint k).aemeasurable aemeasurable_const)

/-- Translation by a finite (real-coerced) constant is an order isomorphism of `EReal`. -/
noncomputable def erealAddCoeIso (c : ℝ) : EReal ≃o EReal where
  toFun y := y + (c : EReal)
  invFun y := y - (c : EReal)
  left_inv y := by simp only; rw [EReal.add_sub_cancel_right]
  right_inv y := by simp only; rw [EReal.sub_add_cancel]
  map_rel_iff' := by
    intro a b
    simp only [Equiv.coe_fn_mk]
    exact (EReal.addLECancellable_coe c).add_le_add_iff_right

omit [MeasurableSpace X] in
/-- **EReal `limsup` of a finite shift.** For a real sequence `u` and a real constant `c`,
`limsup (fun n => ↑(u n) + ↑c) = limsup (fun n => ↑(u n)) + ↑c`. Used to convert the shifted
maximal inequality (Prop 3.5) from the non-positive case. -/
theorem ereal_limsup_add_coe (u : ℕ → ℝ) (c : ℝ) :
    Filter.limsup (fun n => ((u n : ℝ) : EReal) + (c : EReal)) atTop
      = Filter.limsup (fun n => ((u n : ℝ) : EReal)) atTop + (c : EReal) := by
  have h := (erealAddCoeIso c).limsup_apply (u := fun n => ((u n : ℝ) : EReal))
    (f := atTop) (by isBoundedDefault) (by isBoundedDefault)
    (by isBoundedDefault) (by isBoundedDefault)
  simp only [erealAddCoeIso, RelIso.coe_fn_mk, Equiv.coe_fn_mk] at h
  exact h.symm

/-- **Derriennic's maximal inequality** (Karlsson Lemma 3.4). For a measurable
`T`-invariant set `B` on which (a.e.) `liminf (cdiv g · x) < 0`, the normalized integral
`(∫_B g (n+1))/(n+1)` has non-positive `limsup`. -/
theorem limsup_setIntegral_div_nonpos [IsFiniteMeasure μ]
    (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (hint : ∀ n, Integrable (g n) μ)
    {B : Set X} (hB : MeasurableSet B) (hBinv : T ⁻¹' B = B)
    (hBneg : ∀ᵐ x ∂μ, x ∈ B → ∃ k, g (k + 1) x < 0) :
    Filter.limsup
      (fun n : ℕ => (((∫ x in B, g (n + 1) x ∂μ) / (n + 1) : ℝ) : EReal)) atTop ≤ 0 := by
  classical
  -- The positive part `p := (g 1)⁺`, integrable and nonnegative.
  set p : X → ℝ := fun y => max (g 1 y) 0 with hpdef
  have hpint : Integrable p μ := (hint 1).pos_part
  have hpnn : ∀ y, 0 ≤ p y := fun y => le_max_right _ _
  -- The tail integrals `dseq i = ∫_{B \ A_i} p`.
  set dseq : ℕ → ℝ := fun i => ∫ x in B, ((aSet g i)ᶜ).indicator p x ∂μ with hdseqdef
  -- (1) `B ⊆ᵐ ⋃ A_i`: on `B`, some level is `< 0`.
  have hBsub : ∀ᵐ x ∂μ, x ∈ B → x ∈ ⋃ i, aSet g i := by
    filter_upwards [hBneg] with x hx hxB
    obtain ⟨k, hk⟩ := hx hxB
    refine Set.mem_iUnion.2 ⟨k + 1, ?_⟩
    exact ⟨k + 1, by omega, le_refl _, hk⟩
  -- (2) `dseq i → 0` by dominated convergence on the antitone indicators.
  have hdseq0 : Tendsto dseq atTop (𝓝 0) := by
    set F : ℕ → X → ℝ := fun i x => (B ∩ (aSet g i)ᶜ).indicator p x with hFdef
    have hFnm : ∀ i, NullMeasurableSet (B ∩ (aSet g i)ᶜ) μ := fun i =>
      hB.nullMeasurableSet.inter (nullMeasurableSet_aSet hint i).compl
    have hFint : ∀ i, ∫ a, F i a ∂μ = dseq i := by
      intro i
      simp only [hFdef, hdseqdef]
      rw [← Set.indicator_indicator, integral_indicator₀ hB.nullMeasurableSet]
    have hFm : ∀ i, AEStronglyMeasurable (F i) μ :=
      fun i => (hpint.aestronglyMeasurable.indicator₀ (hFnm i))
    have hbound : ∀ i, ∀ᵐ a ∂μ, ‖F i a‖ ≤ p a := by
      intro i
      filter_upwards with a
      simp only [hFdef, Set.indicator_apply, Real.norm_eq_abs]
      by_cases h : a ∈ B ∩ (aSet g i)ᶜ
      · simp only [h, if_true, abs_of_nonneg (hpnn a), le_refl]
      · simp only [h, if_false, abs_zero]; exact hpnn a
    have hlim : ∀ᵐ a ∂μ, Tendsto (fun i => F i a) atTop (𝓝 0) := by
      filter_upwards [hBsub] with a hBa
      by_cases haB : a ∈ B
      · obtain ⟨j, hj⟩ := Set.mem_iUnion.1 (hBa haB)
        refine Tendsto.congr' ?_ tendsto_const_nhds
        filter_upwards [eventually_ge_atTop j] with i hij
        simp only [hFdef, Set.indicator_apply]
        have : a ∈ aSet g i := aSet_mono hij hj
        simp only [Set.mem_inter_iff, Set.mem_compl_iff, this, not_true, and_false, if_false]
      · refine Tendsto.congr' ?_ tendsto_const_nhds
        filter_upwards with i
        simp only [hFdef, Set.indicator_apply]
        simp only [Set.mem_inter_iff, haB, false_and, if_false]
    have hconv : Tendsto (fun i => ∫ a, F i a ∂μ) atTop (𝓝 (∫ a, (0 : ℝ) ∂μ)) :=
      tendsto_integral_of_dominated_convergence p hFm hpint hbound hlim
    simp only [integral_zero] at hconv
    exact (funext hFint) ▸ hconv
  -- (3) Per-level bound: `∫_B bcoc g i ≤ ∫_B ψ_i + dseq i` for `i ≥ 1`.
  have hpoint : ∀ i, 1 ≤ i → ∀ x,
      bcoc (T := T) g i x - psiCoc (T := T) g i x ≤ ((aSet g i)ᶜ).indicator p x := by
    intro i hi1 x
    -- `bcoc g i x ≤ p x` by subadditivity (i ≥ 1).
    have hble : bcoc (T := T) g i x ≤ p x := by
      have hdec : g i x ≤ g 1 x + g (i - 1) (T x) := by
        have := hsub.apply_add_le 1 (i - 1) x
        rw [show 1 + (i - 1) = i by omega, Function.iterate_one] at this
        exact this
      simp only [bcoc, hpdef]
      have : g i x - g (i - 1) (T x) ≤ g 1 x := by linarith
      exact le_trans this (le_max_left _ _)
    by_cases hΛ : x ∈ lambdaSet (T := T) g i
    · -- on `Λ_i`: `psiCoc = bcoc`, so LHS = 0 ≤ RHS.
      simp only [psiCoc, Set.indicator_of_mem hΛ, sub_self]
      exact Set.indicator_nonneg (fun y _ => hpnn y) x
    · -- off `Λ_i` (⟹ off `A_i`): `psiCoc = 0`, LHS = bcoc ≤ p = RHS.
      have hA : x ∉ aSet g i := fun h => hΛ (aSet_subset_lambdaSet hsub i h)
      simp only [psiCoc, Set.indicator_of_notMem hΛ, sub_zero,
        Set.indicator_of_mem (Set.mem_compl hA)]
      exact hble
  -- (4) The main inequality: `∫_B g (n+1) ≤ ∫_B g 0 + ∑_{i∈Icc 1 (n+1)} dseq i`.
  have hmain : ∀ n : ℕ, ∫ x in B, g (n + 1) x ∂μ
      ≤ (∫ x in B, g 0 x ∂μ) + ∑ i ∈ Finset.Icc 1 (n + 1), dseq i := by
    intro n
    -- telescoping: `∫_B g(n+1) - ∫_B g 0 = ∑_{Icc 1 (n+1)} ∫_B bcoc g i`.
    have htel := sum_setIntegral_bcoc_eq hT hint hB hBinv (n + 1)
    -- per-level: `∫_B bcoc g i ≤ ∫_B ψ_i + dseq i`.
    have hlevel : ∀ i ∈ Finset.Icc 1 (n + 1),
        ∫ x in B, bcoc (T := T) g i x ∂μ
          ≤ (∫ x in B, psiCoc (T := T) g i x ∂μ) + dseq i := by
      intro i hi
      simp only [Finset.mem_Icc] at hi
      have hsub_int : ∫ x in B, (bcoc (T := T) g i x - psiCoc (T := T) g i x) ∂μ ≤ dseq i := by
        rw [hdseqdef]
        refine setIntegral_mono_on ?_ ?_ hB (fun x _ => hpoint i hi.1 x)
        · exact ((integrable_bcoc hT hint i).sub (integrable_psiCoc hT hint i)).restrict
        · exact (hpint.indicator₀ (nullMeasurableSet_aSet hint i).compl).restrict
      rw [integral_sub (integrable_bcoc hT hint i).restrict
        (integrable_psiCoc hT hint i).restrict] at hsub_int
      linarith
    -- sum the per-level bounds; use `sum_setIntegral_psiCoc_nonpos` for `∑ ∫_B ψ_i ≤ 0`.
    have hsumlevel : ∑ i ∈ Finset.Icc 1 (n + 1), ∫ x in B, bcoc (T := T) g i x ∂μ
        ≤ (∑ i ∈ Finset.Icc 1 (n + 1), ∫ x in B, psiCoc (T := T) g i x ∂μ)
          + ∑ i ∈ Finset.Icc 1 (n + 1), dseq i := by
      rw [← Finset.sum_add_distrib]
      exact Finset.sum_le_sum hlevel
    have hstar := sum_setIntegral_psiCoc_nonpos hT hint hB hBinv (n + 1)
    have : ∑ i ∈ Finset.Icc 1 (n + 1), ∫ x in B, bcoc (T := T) g i x ∂μ
        ≤ ∑ i ∈ Finset.Icc 1 (n + 1), dseq i := by linarith
    rw [htel] at this
    linarith
  -- (5) Conclude: `(∫_B g(n+1))/(n+1) ≤ r n → 0`, so the EReal limsup is `≤ 0`.
  set r : ℕ → ℝ := fun n =>
    (∫ x in B, g 0 x ∂μ) / (n + 1) + (∑ i ∈ Finset.Icc 1 (n + 1), dseq i) / (n + 1) with hrdef
  -- `∑_{Icc 1 (n+1)} dseq = ∑_{range (n+1)} dseq (·+1)`.
  have hIccrange : ∀ n : ℕ, ∑ i ∈ Finset.Icc 1 (n + 1), dseq i
      = ∑ j ∈ Finset.range (n + 1), dseq (j + 1) := by
    intro n
    refine Finset.sum_nbij' (fun i => i - 1) (fun j => j + 1) ?_ ?_ ?_ ?_ ?_
    · intro i hi; simp only [Finset.mem_Icc] at hi; simp only [Finset.mem_range]; omega
    · intro j hj; simp only [Finset.mem_range] at hj; simp only [Finset.mem_Icc]; omega
    · intro i hi; simp only [Finset.mem_Icc] at hi; dsimp only; omega
    · intro j hj; dsimp only; omega
    · intro i hi; simp only [Finset.mem_Icc] at hi; dsimp only; congr 1; omega
  have hle : ∀ n : ℕ, (∫ x in B, g (n + 1) x ∂μ) / (n + 1) ≤ r n := by
    intro n
    rw [hrdef]
    simp only
    rw [← add_div]
    have hpos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
    exact (div_le_div_iff_of_pos_right hpos).2 (hmain n)
  have hr0 : Tendsto r atTop (𝓝 0) := by
    rw [hrdef]
    have h1 : Tendsto (fun n : ℕ => (∫ x in B, g 0 x ∂μ) / (n + 1)) atTop (𝓝 0) := by
      simp only [div_eq_mul_inv]
      have : Tendsto (fun n : ℕ => ((n : ℝ) + 1)⁻¹) atTop (𝓝 0) :=
        tendsto_inv_atTop_zero.comp (tendsto_atTop_add_const_right _ 1 tendsto_natCast_atTop_atTop)
      simpa using this.const_mul (∫ x in B, g 0 x ∂μ)
    have h2 : Tendsto (fun n : ℕ ↦ (∑ i ∈ Finset.Icc 1 (n + 1), dseq i) / (n + 1)) atTop
        (𝓝 0) := by
      -- Cesàro: `(m⁻¹) ∑_{j<m} dseq (j+1) → 0`, evaluated at `m = n+1`.
      have hces : Tendsto (fun m : ℕ => ((m : ℝ))⁻¹ * ∑ j ∈ Finset.range m, dseq (j + 1))
          atTop (𝓝 0) := Filter.Tendsto.cesaro (hdseq0.comp (tendsto_add_atTop_nat 1))
      have hshift := hces.comp (tendsto_add_atTop_nat 1)
      refine hshift.congr (fun n => ?_)
      simp only [Function.comp]
      rw [hIccrange n, div_eq_inv_mul,
        show ((n : ℝ) + 1) = (((n + 1 : ℕ)) : ℝ) by push_cast; ring]
    simpa using h1.add h2
  -- limsup in EReal of a sequence dominated by `r → 0`.
  have hcoe : Tendsto (fun n : ℕ => ((r n : ℝ) : EReal)) atTop (𝓝 ((0 : ℝ) : EReal)) :=
    (continuous_coe_real_ereal.tendsto _).comp hr0
  calc Filter.limsup
        (fun n : ℕ => (((∫ x in B, g (n + 1) x ∂μ) / (n + 1) : ℝ) : EReal)) atTop
      ≤ Filter.limsup (fun n : ℕ => ((r n : ℝ) : EReal)) atTop := by
        refine Filter.limsup_le_limsup ?_ ?_ ?_
        · filter_upwards with n; exact EReal.coe_le_coe_iff.2 (hle n)
        · exact Filter.isCobounded_le_of_bot
        · exact Filter.isBounded_le_of_top
    _ = ((0 : ℝ) : EReal) := hcoe.limsup_eq
    _ = 0 := by norm_num

/-- **The `β`-version of the maximal inequality** (Karlsson Prop 3.5). For a measurable
`T`-invariant set `B` on which (a.e.) `liminf (cdiv a · x) < β`, the normalized integral
`(∫_B a(n+1))/(n+1)` has `EReal` `limsup ≤ β · (μ B).toReal`. Proved by applying
`limsup_setIntegral_div_nonpos` to the shifted subadditive cocycle `a'(n) x := a n x − n·β`
(subtracting the additive `n·β` preserves subadditivity), then undoing the constant shift. -/
theorem setIntegral_div_le_level [IsFiniteMeasure μ]
    (hT : MeasurePreserving T μ μ) {a : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T a) (hint : ∀ n, Integrable (a n) μ)
    {B : Set X} (hB : MeasurableSet B) (hBinv : T ⁻¹' B = B) (β : ℝ)
    (hBneg : ∀ᵐ x ∂μ, x ∈ B → ∃ k, a (k + 1) x < (k + 1) * β) :
    Filter.limsup
      (fun n : ℕ => (((∫ x in B, a (n + 1) x ∂μ) / (n + 1) : ℝ) : EReal)) atTop
      ≤ ((β * (μ B).toReal : ℝ) : EReal) := by
  classical
  -- Shifted cocycle `a'(n) x := a n x − n·β`.
  set a' : ℕ → X → ℝ := fun n x => a n x - n * β with ha'def
  have ha'sub : IsSubadditiveCocycle T a' := by
    refine ⟨fun m n x => ?_⟩
    simp only [ha'def]
    have := hsub.apply_add_le m n x
    push_cast
    ring_nf
    ring_nf at this
    linarith
  have ha'int : ∀ n, Integrable (a' n) μ := by
    intro n
    simp only [ha'def]
    exact (hint n).sub (integrable_const _)
  -- `hBneg` for `a'`: `a(k+1)x < (k+1)β ⟺ a'(k+1)x < 0`.
  have hBneg' : ∀ᵐ x ∂μ, x ∈ B → ∃ k, a' (k + 1) x < 0 := by
    filter_upwards [hBneg] with x hx hxB
    obtain ⟨k, hk⟩ := hx hxB
    refine ⟨k, ?_⟩
    simp only [ha'def]
    push_cast
    linarith
  -- The maximal inequality for `a'`.
  have hLC := limsup_setIntegral_div_nonpos hT ha'sub ha'int hB hBinv hBneg'
  -- Integral identity: `(∫_B a'(n+1))/(n+1) = (∫_B a(n+1))/(n+1) − β·(μ B).toReal`.
  have hident : ∀ n : ℕ, (∫ x in B, a' (n + 1) x ∂μ) / (n + 1)
      = (∫ x in B, a (n + 1) x ∂μ) / (n + 1) - β * (μ B).toReal := by
    intro n
    have hconst : ∫ _x in B, (((n : ℕ) + 1 : ℕ) : ℝ) * β ∂μ
        = (((n : ℕ) + 1 : ℕ) : ℝ) * β * (μ B).toReal := by
      rw [setIntegral_const, smul_eq_mul, mul_comm]
      rfl
    have hsplit : ∫ x in B, a' (n + 1) x ∂μ
        = (∫ x in B, a (n + 1) x ∂μ) - (((n : ℕ) + 1 : ℕ) : ℝ) * β * (μ B).toReal := by
      simp only [ha'def]
      rw [integral_sub (hint (n + 1)).restrict ((integrable_const _).restrict), hconst]
    rw [hsplit, sub_div]
    congr 1
    have hpos : (0 : ℝ) < (((n : ℕ) + 1 : ℕ) : ℝ) := by positivity
    rw [show ((n : ℝ) + 1) = (((n : ℕ) + 1 : ℕ) : ℝ) by push_cast; ring]
    field_simp
  -- Rewrite the maximal-inequality limsup using the identity, then undo the shift.
  have hcongr : (fun n : ℕ => (((∫ x in B, a' (n + 1) x ∂μ) / (n + 1) : ℝ) : EReal))
      = fun n : ℕ => (((∫ x in B, a (n + 1) x ∂μ) / (n + 1) : ℝ) : EReal)
          + ((-(β * (μ B).toReal) : ℝ) : EReal) := by
    funext n
    rw [hident n, sub_eq_add_neg, EReal.coe_add, EReal.coe_neg]
  rw [hcongr, ereal_limsup_add_coe] at hLC
  -- `limsup (↑X) + ↑(−c) ≤ 0  ⟹  limsup (↑X) ≤ ↑c`.
  have hstep := add_le_add_left hLC ((β * (μ B).toReal : ℝ) : EReal)
  rw [zero_add] at hstep
  set L : EReal := Filter.limsup
    (fun n : ℕ => (((∫ x in B, a (n + 1) x ∂μ) / (n + 1) : ℝ) : EReal)) atTop with hLdef
  have hcz : ((-(β * (μ B).toReal) : ℝ) : EReal) + ((β * (μ B).toReal : ℝ) : EReal) = 0 := by
    rw [← EReal.coe_add, neg_add_cancel, EReal.coe_zero]
  have hid : L + ((-(β * (μ B).toReal) : ℝ) : EReal) + ((β * (μ B).toReal : ℝ) : EReal) = L := by
    rw [add_assoc, hcz, add_zero]
  rw [hid] at hstep
  exact hstep


end ErgodicTheory.Kingman
