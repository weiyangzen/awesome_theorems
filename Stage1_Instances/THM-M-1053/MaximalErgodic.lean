/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
/-
Port note: this file is modified from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
The sole compatibility change is the pinned-mathlib spelling
`integrable_finset_sum`; see `PORT_PROVENANCE.md`.
-/
import Mathlib.Dynamics.BirkhoffSum.Average
import Mathlib.Dynamics.Ergodic.MeasurePreserving
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Order.Lattice
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order

/-!
# The maximal ergodic inequality (Hopf/Garsia)

For an integrable `f` and a measure-preserving `T`, on the set where some forward
Birkhoff sum is positive the integral of `f` is nonnegative:
`0 ≤ ∫_{ {x | ∃ n, 0 < birkhoffSum T f (n+1) x} } f dμ`. This inequality is the
analytic gateway to the pointwise (Birkhoff) ergodic theorem.

The proof follows Garsia's short combinatorial argument. We introduce the
*maximal function* `maxBirkhoff T g N x = max_{0 ≤ k ≤ N} birkhoffSum T g k x`
for a measurable representative `g` of `f`, establish the pointwise Garsia
inequality `maxBirkhoff … x - maxBirkhoff … (T x) ≤ g x` on the set where the
maximal function is positive, integrate it, pass to the limit `N → ∞`, and
transfer back from `g` to `f`.

## Main results

* `ErgodicTheory.maxBirkhoff`: Garsia's maximal function
  `maxBirkhoff T g N x = max_{0 ≤ k ≤ N} birkhoffSum T g k x`.
* `ErgodicTheory.maxBirkhoff_le_add`: Garsia's pointwise inequality
  `maxBirkhoff T g N x ≤ g x + maxBirkhoff T g N (T x)` on the set where the maximal
  function is positive.
* `ErgodicTheory.setIntegral_maxBirkhoff_pos_nonneg`: Garsia's inequality at a fixed
  level `N`.
* `ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg`: the maximal ergodic inequality.

## References

* A. M. Garsia, *A simple proof of E. Hopf's maximal ergodic theorem*,
  J. Math. Mech. 14 (1965), 381–382.
-/

open MeasureTheory Filter Finset Topology

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {μ : Measure X} {T : X → X}

/-- Garsia's maximal function: `maxBirkhoff T g N x = max_{0 ≤ k ≤ N} birkhoffSum T g k x`.
Because the `k = 0` term equals `birkhoffSum T g 0 x = 0`, this quantity is always `≥ 0`.
The nonemptiness witness is the literal `Finset.nonempty_range_add_one`, matching
`Finset.measurable_range_sup''`. -/
noncomputable def maxBirkhoff (T : X → X) (g : X → ℝ) (N : ℕ) (x : X) : ℝ :=
  (Finset.range (N + 1)).sup' Finset.nonempty_range_add_one
    (fun k => birkhoffSum T g k x)

omit [MeasurableSpace X] in
/-- The `k = 0` term of `maxBirkhoff` is `birkhoffSum T g 0 x = 0`, so the maximal
function is nonnegative everywhere. -/
theorem maxBirkhoff_nonneg (g : X → ℝ) (N : ℕ) (x : X) : 0 ≤ maxBirkhoff T g N x := by
  refine le_trans (le_of_eq (birkhoffSum_zero T g x).symm) ?_
  exact Finset.le_sup' (fun k => birkhoffSum T g k x) (Finset.mem_range.2 (Nat.succ_pos N))

omit [MeasurableSpace X] in
/-- The recursion `maxBirkhoff T g (N+1) x = birkhoffSum T g (N+1) x ⊔ maxBirkhoff T g N x`,
from `range (N+2) = insert (N+1) (range (N+1))`. -/
theorem maxBirkhoff_succ (g : X → ℝ) (N : ℕ) (x : X) :
    maxBirkhoff T g (N + 1) x =
      birkhoffSum T g (N + 1) x ⊔ maxBirkhoff T g N x := by
  unfold maxBirkhoff
  apply le_antisymm
  · refine Finset.sup'_le _ _ (fun k hk => ?_)
    rw [Finset.mem_range, Nat.lt_succ_iff, Nat.le_succ_iff] at hk
    rcases hk with hk | hk
    · exact le_sup_of_le_right
        (Finset.le_sup' (fun k => birkhoffSum T g k x) (Finset.mem_range.2 (Nat.lt_succ_of_le hk)))
    · subst hk; exact le_sup_left
  · apply sup_le
    · exact Finset.le_sup' (fun k => birkhoffSum T g k x)
        (Finset.mem_range.2 (Nat.lt_succ_self (N + 1)))
    · refine Finset.sup'_le _ _ (fun k hk => ?_)
      rw [Finset.mem_range] at hk
      exact Finset.le_sup' (fun k => birkhoffSum T g k x)
        (Finset.mem_range.2 (Nat.lt_succ_of_lt hk))

/-- Each Birkhoff partial sum `x ↦ birkhoffSum T g k x` is measurable when `g` is
measurable and `T` is measurable. -/
theorem measurable_birkhoffSum (hT : Measurable T) {g : X → ℝ} (hg : Measurable g) (k : ℕ) :
    Measurable (fun x => birkhoffSum T g k x) := by
  simp only [birkhoffSum]
  exact Finset.measurable_sum _ (fun j _ => hg.comp (hT.iterate j))

/-- The maximal function `maxBirkhoff T g N` is measurable when `g` and `T` are. -/
theorem measurable_maxBirkhoff (hT : Measurable T) {g : X → ℝ} (hg : Measurable g) (N : ℕ) :
    Measurable (maxBirkhoff T g N) :=
  Finset.measurable_range_sup'' (fun k _ => measurable_birkhoffSum hT hg k)

/-- Each Birkhoff partial sum `x ↦ birkhoffSum T g k x` is integrable when `g` is
integrable and `T` is measure-preserving. -/
theorem integrable_birkhoffSum (hT : MeasurePreserving T μ μ) {g : X → ℝ}
    (hg : Integrable g μ) (k : ℕ) : Integrable (fun x => birkhoffSum T g k x) μ := by
  simp only [birkhoffSum]
  refine integrable_finset_sum _ (fun j _ => ?_)
  have : Integrable (g ∘ T^[j]) μ := (hT.iterate j).integrable_comp_of_integrable hg
  exact this

/-- The maximal function `maxBirkhoff T g N` is integrable when `g` is integrable
and `T` is measure-preserving. -/
theorem integrable_maxBirkhoff (hT : MeasurePreserving T μ μ) {g : X → ℝ}
    (hg : Integrable g μ) (N : ℕ) : Integrable (maxBirkhoff T g N) μ := by
  induction N with
  | zero =>
      have : maxBirkhoff T g 0 = fun x => birkhoffSum T g 0 x := by
        funext x; simp only [maxBirkhoff]; rw [Finset.sup'_eq_of_forall]
        intro k hk; rw [Finset.mem_range, Nat.lt_one_iff] at hk; subst hk; rfl
      rw [this]; exact integrable_birkhoffSum hT hg 0
  | succ N ih =>
      have hrec : maxBirkhoff T g (N + 1) =
          fun x => birkhoffSum T g (N + 1) x ⊔ maxBirkhoff T g N x := by
        funext x; exact maxBirkhoff_succ g N x
      rw [hrec]
      exact (integrable_birkhoffSum hT hg (N + 1)).sup ih

omit [MeasurableSpace X] in
/-- A real constant can be pulled inside a nonempty `Finset.sup'`:
`c + s.sup' H f = s.sup' H (fun b => c + f b)`. (Mathlib has no `Finset.sup'_add`,
so we prove it directly by `le_antisymm`.) -/
theorem add_sup'_eq {ι : Type*} (s : Finset ι) (H : s.Nonempty) (c : ℝ) (f : ι → ℝ) :
    c + s.sup' H f = s.sup' H (fun b => c + f b) := by
  apply le_antisymm
  · obtain ⟨b, hb, hbeq⟩ := Finset.exists_mem_eq_sup' H f
    rw [hbeq]
    exact Finset.le_sup' (fun b => c + f b) hb
  · refine Finset.sup'_le _ _ (fun b hb => ?_)
    have := Finset.le_sup' f hb
    linarith

omit [MeasurableSpace X] in
/-- **Garsia's pointwise inequality.** On the set where `maxBirkhoff T g N` is
positive, `maxBirkhoff T g N x ≤ g x + maxBirkhoff T g N (T x)`.

Key identity: pulling the constant `g x` through the `sup'` and applying
`birkhoffSum_succ'` shows `g x + maxBirkhoff T g N (T x)` is the maximum of the
*shifted* partial sums `birkhoffSum T g (k+1) x` over `k ≤ N`. Since the maximum
defining `maxBirkhoff T g N x` is positive it is attained at some index `k₀ ≥ 1`
(the index `0` gives `birkhoffSum T g 0 x = 0`), and `birkhoffSum T g k₀ x` is one
of the shifted sums, hence `≤` the shifted maximum. -/
theorem maxBirkhoff_le_add (g : X → ℝ) (N : ℕ) (x : X)
    (hx : 0 < maxBirkhoff T g N x) :
    maxBirkhoff T g N x ≤ g x + maxBirkhoff T g N (T x) := by
  -- Rewrite the RHS as a sup' of shifted Birkhoff sums.
  have hrhs : g x + maxBirkhoff T g N (T x)
      = (Finset.range (N + 1)).sup' Finset.nonempty_range_add_one
          (fun k => birkhoffSum T g (k + 1) x) := by
    unfold maxBirkhoff
    rw [add_sup'_eq]
    refine Finset.sup'_congr _ rfl (fun k _ => ?_)
    rw [birkhoffSum_succ']
  rw [hrhs]
  -- The maximum defining the LHS is attained at some k₀ ∈ range (N+1).
  have hk₀eq' :
      maxBirkhoff T g N x
        = (Finset.range (N + 1)).sup' Finset.nonempty_range_add_one
            (fun k => birkhoffSum T g k x) := rfl
  obtain ⟨k₀, hk₀mem, hk₀eq⟩ :=
    Finset.exists_mem_eq_sup' (Finset.nonempty_range_add_one (n := N))
      (fun k => birkhoffSum T g k x)
  rw [hk₀eq'.trans hk₀eq] at hx ⊢
  -- k₀ ≠ 0, since birkhoffSum T g 0 x = 0 < birkhoffSum T g k₀ x.
  have hk₀pos : 0 < k₀ := by
    rcases Nat.eq_zero_or_pos k₀ with h | h
    · exfalso
      subst h
      rw [birkhoffSum_zero] at hx
      exact lt_irrefl 0 hx
    · exact h
  -- Write k₀ = (k₀ - 1) + 1, with k₀ - 1 ∈ range (N+1).
  obtain ⟨m, rfl⟩ : ∃ m, k₀ = m + 1 := ⟨k₀ - 1, by omega⟩
  refine Finset.le_sup' (fun k => birkhoffSum T g (k + 1) x) ?_
  rw [Finset.mem_range] at hk₀mem ⊢
  omega

/-- If `f =ᵐ[μ] g` and `T` is measure-preserving, then the Birkhoff sums agree a.e.:
`birkhoffSum T f n =ᵐ[μ] birkhoffSum T g n`. Each summand `f ∘ T^[k] =ᵐ[μ] g ∘ T^[k]`
because `T^[k]` is measure-preserving, and a finite a.e.-equal sum is a.e.-equal. -/
theorem birkhoffSum_congr_ae (hT : MeasurePreserving T μ μ) {f g : X → ℝ}
    (hfg : f =ᵐ[μ] g) (n : ℕ) :
    (fun x => birkhoffSum T f n x) =ᵐ[μ] (fun x => birkhoffSum T g n x) := by
  -- For each k, the composite with T^[k] is a.e. equal.
  have hcomp : ∀ k : ℕ, (f ∘ T^[k]) =ᵐ[μ] (g ∘ T^[k]) := fun k =>
    ((hT.iterate k).quasiMeasurePreserving).ae_eq_comp hfg
  -- Collect over the (finitely many, hence countably many) indices.
  have hall : ∀ᵐ x ∂μ, ∀ k : ℕ, (f ∘ T^[k]) x = (g ∘ T^[k]) x :=
    (ae_all_iff).2 hcomp
  filter_upwards [hall] with x hx
  simp only [birkhoffSum]
  exact Finset.sum_congr rfl (fun k _ => hx k)

/-- **Garsia's inequality for a fixed level `N`.** For a measurable integrable `g`,
the integral of `g` over the set `{x | 0 < maxBirkhoff T g N x}` is nonnegative.

This is the heart of the maximal ergodic inequality. We integrate the pointwise
Garsia inequality `maxBirkhoff T g N x - maxBirkhoff T g N (T x) ≤ g x` over the
level set `E N`, then use measure-preservation
(`∫ maxBirkhoff∘T = ∫ maxBirkhoff`) and the fact that `maxBirkhoff` vanishes off
`E N` to cancel the two maximal-function integrals. -/
theorem setIntegral_maxBirkhoff_pos_nonneg (hT : MeasurePreserving T μ μ) {g : X → ℝ}
    (hg : Integrable g μ) (hgm : Measurable g) (N : ℕ) :
    0 ≤ ∫ x in {x | 0 < maxBirkhoff T g N x}, g x ∂μ := by
  set E : Set X := {x | 0 < maxBirkhoff T g N x} with hE
  have hEmeas : MeasurableSet E :=
    measurableSet_lt measurable_const (measurable_maxBirkhoff hT.measurable hgm N)
  -- Integrability of the maximal function and its composition with T.
  have hMint : Integrable (maxBirkhoff T g N) μ := integrable_maxBirkhoff hT hg N
  have hMTint : Integrable (fun x => maxBirkhoff T g N (T x)) μ :=
    hT.integrable_comp_of_integrable hMint
  -- Step (★): integrate the pointwise Garsia inequality over E.
  have hstep : ∫ x in E, (maxBirkhoff T g N x - maxBirkhoff T g N (T x)) ∂μ
      ≤ ∫ x in E, g x ∂μ := by
    refine setIntegral_mono_on (hMint.sub hMTint).integrableOn hg.integrableOn hEmeas ?_
    intro x hx
    have := maxBirkhoff_le_add g N x hx
    linarith
  -- Split the LHS integral.
  have hsplit : ∫ x in E, (maxBirkhoff T g N x - maxBirkhoff T g N (T x)) ∂μ
      = (∫ x in E, maxBirkhoff T g N x ∂μ)
          - ∫ x in E, maxBirkhoff T g N (T x) ∂μ :=
    integral_sub hMint.integrableOn hMTint.integrableOn
  -- (a) ∫_E maxBirkhoff∘T ≤ ∫_X maxBirkhoff∘T.
  have ha : ∫ x in E, maxBirkhoff T g N (T x) ∂μ
      ≤ ∫ x, maxBirkhoff T g N (T x) ∂μ :=
    setIntegral_le_integral hMTint
      (Eventually.of_forall (fun x => maxBirkhoff_nonneg g N (T x)))
  -- (b) ∫_X maxBirkhoff∘T = ∫_X maxBirkhoff, by measure-preservation.
  have hb : ∫ x, maxBirkhoff T g N (T x) ∂μ = ∫ x, maxBirkhoff T g N x ∂μ := by
    have haem : AEMeasurable T μ := hT.measurable.aemeasurable
    have hmap := integral_map (μ := μ) (φ := T) haem
      (f := maxBirkhoff T g N)
      ((measurable_maxBirkhoff hT.measurable hgm N).aestronglyMeasurable)
    rw [hT.map_eq] at hmap
    exact hmap.symm
  -- (c) ∫_X maxBirkhoff = ∫_E maxBirkhoff, since maxBirkhoff = 0 off E.
  have hc : ∫ x, maxBirkhoff T g N x ∂μ = ∫ x in E, maxBirkhoff T g N x ∂μ := by
    rw [← integral_add_compl hEmeas hMint]
    have hzero : ∫ x in Eᶜ, maxBirkhoff T g N x ∂μ = 0 := by
      refine setIntegral_eq_zero_of_forall_eq_zero (fun x hx => ?_)
      have hxnotpos : ¬ 0 < maxBirkhoff T g N x := by
        simp only [hE, Set.mem_compl_iff, Set.mem_setOf_eq] at hx; exact hx
      have hxnonneg : 0 ≤ maxBirkhoff T g N x := maxBirkhoff_nonneg g N x
      have hxle : maxBirkhoff T g N x ≤ 0 := not_lt.1 hxnotpos
      linarith
    rw [hzero, add_zero]
  -- Chain everything together.
  have key : 0 ≤ ∫ x in E, (maxBirkhoff T g N x - maxBirkhoff T g N (T x)) ∂μ := by
    rw [hsplit]
    have : ∫ x in E, maxBirkhoff T g N (T x) ∂μ ≤ ∫ x in E, maxBirkhoff T g N x ∂μ := by
      calc ∫ x in E, maxBirkhoff T g N (T x) ∂μ
          ≤ ∫ x, maxBirkhoff T g N (T x) ∂μ := ha
        _ = ∫ x, maxBirkhoff T g N x ∂μ := hb
        _ = ∫ x in E, maxBirkhoff T g N x ∂μ := hc
    linarith
  linarith [hstep, key]

omit [MeasurableSpace X] in
/-- The level sets `{x | 0 < maxBirkhoff T g N x}` are monotone in `N`, because
`maxBirkhoff T g N` is monotone in `N` (the `sup'` is over a larger range). -/
theorem monotone_setOf_maxBirkhoff_pos (g : X → ℝ) :
    Monotone (fun N => {x | 0 < maxBirkhoff T g N x}) := by
  intro N M hNM x hx
  simp only [Set.mem_setOf_eq] at hx ⊢
  refine lt_of_lt_of_le hx ?_
  unfold maxBirkhoff
  exact Finset.sup'_mono _ (by
    intro k hk; rw [Finset.mem_range] at hk ⊢; omega) Finset.nonempty_range_add_one

omit [MeasurableSpace X] in
/-- The union of the level sets `{x | 0 < maxBirkhoff T g N x}` over all `N` is exactly
the target set `{x | ∃ n, 0 < birkhoffSum T g (n+1) x}`. -/
theorem iUnion_setOf_maxBirkhoff_pos (g : X → ℝ) :
    ⋃ N, {x | 0 < maxBirkhoff T g N x}
      = {x | ∃ n : ℕ, 0 < birkhoffSum T g (n + 1) x} := by
  ext x
  simp only [Set.mem_iUnion, Set.mem_setOf_eq]
  constructor
  · rintro ⟨N, hN⟩
    -- 0 < maxBirkhoff means some birkhoffSum T g k x > 0 with k ≤ N, and k ≠ 0.
    unfold maxBirkhoff at hN
    rw [Finset.lt_sup'_iff] at hN
    obtain ⟨k, hkmem, hkpos⟩ := hN
    rw [Finset.mem_range] at hkmem
    rcases Nat.eq_zero_or_pos k with hk0 | hk0
    · rw [hk0, birkhoffSum_zero] at hkpos; exact absurd hkpos (lt_irrefl 0)
    · obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
      exact ⟨m, hkpos⟩
  · rintro ⟨n, hn⟩
    refine ⟨n + 1, ?_⟩
    unfold maxBirkhoff
    rw [Finset.lt_sup'_iff]
    exact ⟨n + 1, Finset.mem_range.2 (by omega), hn⟩

/-- **Maximal ergodic inequality, measurable version.** For a measurable integrable `g`
and measure-preserving `T`, the integral of `g` over the set where some forward Birkhoff
partial sum is positive is nonnegative. The general (only a.e. measurable) case is
obtained by passing to a measurable representative. -/
theorem setIntegral_birkhoffSum_pos_nonneg_of_measurable (hT : MeasurePreserving T μ μ)
    {g : X → ℝ} (hg : Integrable g μ) (hgm : Measurable g) :
    0 ≤ ∫ x in {x | ∃ n : ℕ, 0 < birkhoffSum T g (n + 1) x}, g x ∂μ := by
  have hmono : Monotone (fun N => {x | 0 < maxBirkhoff T g N x}) :=
    monotone_setOf_maxBirkhoff_pos g
  have hmeas : ∀ N, MeasurableSet {x | 0 < maxBirkhoff T g N x} := fun N =>
    measurableSet_lt measurable_const (measurable_maxBirkhoff hT.measurable hgm N)
  have hunion := iUnion_setOf_maxBirkhoff_pos (T := T) g
  -- The integrand g is integrable on the union (= target set).
  have hgU : IntegrableOn g (⋃ N, {x | 0 < maxBirkhoff T g N x}) μ := hg.integrableOn
  -- ∫_{E N} g → ∫_{⋃ E N} g.
  have htend :
      Tendsto (fun N => ∫ x in {x | 0 < maxBirkhoff T g N x}, g x ∂μ) atTop
        (𝓝 (∫ x in ⋃ N, {x | 0 < maxBirkhoff T g N x}, g x ∂μ)) :=
    tendsto_setIntegral_of_monotone hmeas hmono hgU
  -- Each term is ≥ 0; the limit is ≥ 0.
  have hlim : 0 ≤ ∫ x in ⋃ N, {x | 0 < maxBirkhoff T g N x}, g x ∂μ :=
    ge_of_tendsto' htend (fun N => setIntegral_maxBirkhoff_pos_nonneg hT hg hgm N)
  rwa [hunion] at hlim

/-- **Maximal ergodic inequality** (Hopf/Garsia). For a measure-preserving `T` and an
integrable `f`, the integral of `f` over the set where some forward Birkhoff partial
sum is positive is nonnegative.

The proof reduces to the measurable case
`setIntegral_birkhoffSum_pos_nonneg_of_measurable` by passing to the measurable
representative `g = hf.1.mk f` and transferring both the target set (the two sets
agree a.e. since the Birkhoff sums agree a.e.) and the integrand (`f =ᵐ[μ] g`). -/
theorem setIntegral_birkhoffSum_pos_nonneg
    (hT : MeasurePreserving T μ μ) {f : X → ℝ} (hf : Integrable f μ) :
    0 ≤ ∫ x in {x | ∃ n : ℕ, 0 < birkhoffSum T f (n + 1) x}, f x ∂μ := by
  -- The measurable representative of f.
  set g : X → ℝ := hf.1.mk f with hg_def
  have hgm : Measurable g := hf.1.measurable_mk
  have hfg : f =ᵐ[μ] g := hf.1.ae_eq_mk
  have hgi : Integrable g μ := hf.congr hfg
  -- Notation for the two target sets.
  set Sf : Set X := {x | ∃ n : ℕ, 0 < birkhoffSum T f (n + 1) x} with hSf
  set Sg : Set X := {x | ∃ n : ℕ, 0 < birkhoffSum T g (n + 1) x} with hSg
  -- The two target sets agree a.e. (Birkhoff sums of f and g agree a.e.).
  have hsets : Sf =ᵐ[μ] Sg := by
    rw [Filter.eventuallyEq_set]
    have hbk : ∀ᵐ x ∂μ, ∀ n : ℕ,
        birkhoffSum T f (n + 1) x = birkhoffSum T g (n + 1) x := by
      rw [ae_all_iff]
      exact fun n => birkhoffSum_congr_ae hT hfg (n + 1)
    filter_upwards [hbk] with x hx
    simp only [hSf, hSg, Set.mem_setOf_eq]
    constructor
    · rintro ⟨n, hn⟩; exact ⟨n, by rw [← hx n]; exact hn⟩
    · rintro ⟨n, hn⟩; exact ⟨n, by rw [hx n]; exact hn⟩
  -- Sg is measurable, hence Sf is a null-measurable set.
  have hSgmeas : MeasurableSet Sg := by
    rw [hSg, ← iUnion_setOf_maxBirkhoff_pos (T := T) g]
    exact MeasurableSet.iUnion (fun N =>
      measurableSet_lt measurable_const (measurable_maxBirkhoff hT.measurable hgm N))
  have hSfnull : NullMeasurableSet Sf μ :=
    (hSgmeas.nullMeasurableSet).congr hsets.symm
  -- Transfer the set Sf ↝ Sg and the integrand g ↝ f.
  calc 0 ≤ ∫ x in Sg, g x ∂μ :=
        hSg ▸ setIntegral_birkhoffSum_pos_nonneg_of_measurable hT hgi hgm
    _ = ∫ x in Sf, g x ∂μ := (setIntegral_congr_set hsets).symm
    _ = ∫ x in Sf, f x ∂μ :=
        setIntegral_congr_ae₀ hSfnull (hfg.mono (fun x hx _ => hx.symm))

end ErgodicTheory
