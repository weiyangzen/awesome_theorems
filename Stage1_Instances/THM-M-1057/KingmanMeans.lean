/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
/-
Port notice: vendored from `marcmorningstar/lean4-ergodic-theory` at commit
`ed3fa6b8a30594eeb791160563942ba115581aa0`. The upstream sibling imports are local,
and `integral_finsetSum` is spelled `integral_finset_sum` on Lean 4.29; see
`PORT_PROVENANCE.md`.
-/
import KingmanCore
import Birkhoff

/-!
# Kingman means identification

For an integrable subadditive cocycle `g` over an ergodic measure-preserving system, Kingman's
theorem (`ErgodicTheory.tendsto_kingman_ergodic`) provides a constant `c` to which `(n : ℝ)⁻¹ • gₙ`
converges `μ`-a.e.; the file `ErgodicTheory.Ergodic.Kingman` deliberately leaves the *value* of `c`
unidentified.

This module identifies that constant with the limit of the normalized integral means
`(∫ g (n+1)) / (n+1)`, which exists by Fekete's lemma applied to the subadditive sequence
`n ↦ ∫ gₙ`.

## Main statements

* `ErgodicTheory.tendsto_kingman_ergodic_means`: there is a single constant `c` that is *both* the
  limit of the integral means `(∫ g (n+1)) / (n+1)` *and* the `μ`-a.e. limit of the normalized
  cocycle `(n : ℝ)⁻¹ • gₙ`.

## Implementation notes

The two halves `c ≤ L` and `c ≥ L` of the identification `c = L := lim (∫ gₙ)/n` are proved
separately.

* `c ≤ L`: iterate subadditivity in blocks of length `n`, dividing by `m·n` and letting
  `m → ∞`. The left-hand side converges along the multiples of `n` to the a.e. Kingman limit `c`,
  while the right-hand side is the `T^[n]`-Birkhoff average of `(1/n) gₙ` whose pointwise limit
  integrates to `(1/n) ∫ gₙ`. Integrating the pointwise inequality and letting `n → ∞` gives
  `c ≤ L`.

* `c ≥ L`: a single Fatou pass on the nonnegative defect `birkhoffAverage T (g 1) (n+1) − cdiv g n`
  (nonnegative by singleton subadditivity). Its a.e. limit is the constant `∫ g 1 − c`, while its
  integral tends to `∫ g 1 − L`; Fatou yields `∫ g 1 − c ≤ ∫ g 1 − L`, i.e. `c ≥ L`.
-/

open MeasureTheory Filter Topology
open scoped ENNReal

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {μ : Measure X} {T : X → X}

/-! ### Fekete: convergence of the integral means -/

/-- The integral of a measure-preserving composition equals the integral. -/
private theorem km_integral_comp_iterate (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (m n : ℕ) :
    ∫ x, g n (T^[m] x) ∂μ = ∫ x, g n x ∂μ := by
  have hmp : MeasurePreserving (T^[m]) μ μ := hT.iterate m
  have haesm : AEStronglyMeasurable (g n) (Measure.map (T^[m]) μ) := by
    rw [hmp.map_eq]; exact (hint n).aestronglyMeasurable
  have hmap := integral_map (μ := μ) (φ := T^[m]) hmp.aemeasurable (f := g n) haesm
  rw [hmp.map_eq] at hmap
  exact hmap.symm

/-- The integral sequence `n ↦ ∫ gₙ` is subadditive (the Fekete input). -/
private theorem km_integral_subadditive (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (hint : ∀ n, Integrable (g n) μ) :
    Subadditive (fun n => ∫ x, g n x ∂μ) := by
  intro m n
  simp only
  have hcomp : Integrable (fun x => g n (T^[m] x)) μ :=
    (hT.iterate m).integrable_comp_of_integrable (hint n)
  calc ∫ x, g (m + n) x ∂μ
      ≤ ∫ x, (g m x + g n (T^[m] x)) ∂μ :=
        integral_mono (hint _) ((hint m).add hcomp) (fun x => hsub.apply_add_le m n x)
    _ = (∫ x, g m x ∂μ) + ∫ x, g n (T^[m] x) ∂μ := integral_add (hint m) hcomp
    _ = (∫ x, g m x ∂μ) + ∫ x, g n x ∂μ := by
        congr 1; exact km_integral_comp_iterate hT hint m n

/-- **Fekete.** The integral means `(∫ g (n+1)) / (n+1)` converge to the Fekete constant. -/
private theorem km_exists_fekete (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (hint : ∀ n, Integrable (g n) μ)
    (hbdd : BddBelow (Set.range fun n : ℕ => (∫ x, g (n + 1) x ∂μ) / (n + 1))) :
    ∃ γ : ℝ, Tendsto (fun n : ℕ => (∫ x, g (n + 1) x ∂μ) / (n + 1)) atTop (𝓝 γ) := by
  set a : ℕ → ℝ := fun n => ∫ x, g n x ∂μ with hadef
  have hsa : Subadditive a := km_integral_subadditive hT hsub hint
  have hbdd' : BddBelow (Set.range fun n : ℕ => a n / n) := by
    obtain ⟨lb, hlb⟩ := hbdd
    refine ⟨min lb 0, ?_⟩
    rintro y ⟨n, rfl⟩
    rcases n with _ | m
    · simp only [Nat.cast_zero, div_zero]
      exact min_le_right lb 0
    · have hmem : a (m + 1) / ((m : ℝ) + 1)
          ∈ Set.range fun n : ℕ => (∫ x, g (n + 1) x ∂μ) / (n + 1) :=
        ⟨m, by simp only [hadef]⟩
      have : (fun n : ℕ => a n / n) (m + 1) = a (m + 1) / ((m : ℝ) + 1) := by push_cast; ring
      rw [this]
      exact le_trans (min_le_left lb 0) (hlb hmem)
  refine ⟨hsa.lim, ?_⟩
  have hlim := hsa.tendsto_lim hbdd'
  rw [← tendsto_add_atTop_iff_nat (f := fun n : ℕ => a n / n) 1] at hlim
  refine hlim.congr (fun n => ?_)
  show a (n + 1) / ((n + 1 : ℕ) : ℝ) = (∫ x, g (n + 1) x ∂μ) / ((n : ℝ) + 1)
  simp only [hadef, Nat.cast_add, Nat.cast_one]

/-! ### The lower bound `c ≤ L` via block subadditivity -/

omit [MeasurableSpace X] in
/-- **Block subadditivity.** A subadditive cocycle is dominated, in blocks of length `n`, by the
`T^[n]`-Birkhoff sum of its `n`-th level: `g ((m+1)*n) x ≤ birkhoffSum (T^[n]) (g n) (m+1) x`. -/
private theorem km_le_birkhoffSum_block {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (n m : ℕ) (x : X) :
    g ((m + 1) * n) x ≤ birkhoffSum (T^[n]) (g n) (m + 1) x := by
  induction m with
  | zero =>
      simp only [Nat.zero_add, one_mul, birkhoffSum_one]
      exact le_refl _
  | succ m ih =>
      have hmul : (m + 1 + 1) * n = (m + 1) * n + n := by ring
      rw [birkhoffSum_succ]
      have hstep : g ((m + 1) * n + n) x ≤ g ((m + 1) * n) x + g n (T^[(m + 1) * n] x) :=
        hsub.apply_add_le ((m + 1) * n) n x
      have hiter : (T^[n])^[m + 1] x = T^[(m + 1) * n] x := by
        rw [← Function.iterate_mul]
        congr 1
        ring
      rw [hmul, hiter]
      calc g ((m + 1) * n + n) x ≤ g ((m + 1) * n) x + g n (T^[(m + 1) * n] x) := hstep
        _ ≤ birkhoffSum (T^[n]) (g n) (m + 1) x + g n (T^[(m + 1) * n] x) := by linarith [ih]

/-- The integral of `μ[g n | invariants (T^[n])]` equals `∫ g n` (probability measure). -/
private theorem km_integral_condExp_iterate [IsProbabilityMeasure μ]
    {g : ℕ → X → ℝ} (n : ℕ) :
    ∫ x, (μ[g n | MeasurableSpace.invariants (T^[n])]) x ∂μ = ∫ x, g n x ∂μ :=
  integral_condExp (MeasurableSpace.invariants_le (T^[n]))

/-- **Lower bound.** The a.e. Kingman constant `c` satisfies `c ≤ (∫ g n) / n` for every
`n ≥ 1`, hence `c ≤ L`. -/
private theorem km_const_le_mean [IsProbabilityMeasure μ]
    (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (hint : ∀ n, Integrable (g n) μ)
    {c : ℝ} (hc : ∀ᵐ x ∂μ, Tendsto (fun k : ℕ => (k : ℝ)⁻¹ * g k x) atTop (𝓝 c)) (n : ℕ) :
    c ≤ (∫ x, g (n + 1) x ∂μ) / (n + 1) := by
  -- Work with the block length `N := n + 1 ≥ 1`.
  set N : ℕ := n + 1 with hNdef
  have hNpos : 0 < N := by omega
  have hNR : (0 : ℝ) < (N : ℝ) := by exact_mod_cast hNpos
  -- The `T^[N]`-Birkhoff limit of `g N`.
  set B : X → ℝ := μ[g N | MeasurableSpace.invariants (T^[N])] with hBdef
  have hTN : MeasurePreserving (T^[N]) μ μ := hT.iterate N
  -- Pointwise: a.e. `c ≤ (N : ℝ)⁻¹ * B x`.
  have hpt : ∀ᵐ x ∂μ, c ≤ (N : ℝ)⁻¹ * B x := by
    filter_upwards [hc, tendsto_birkhoffAverage_ae hTN (hint N)] with x hcx hBconv
    -- Left-hand limit along the multiples of `N`: `((m+1)*N)⁻¹ * g ((m+1)*N) x → c`.
    have hidx : Tendsto (fun m : ℕ => (m + 1) * N) atTop atTop := by
      refine tendsto_atTop_mono (fun m => ?_) tendsto_id
      calc id m = m := rfl
        _ ≤ (m + 1) * N := le_trans (Nat.le_succ m) (Nat.le_mul_of_pos_right _ hNpos)
    have hLHS : Tendsto (fun m : ℕ => (((m + 1) * N : ℕ) : ℝ)⁻¹ * g ((m + 1) * N) x) atTop
        (𝓝 c) := hcx.comp hidx
    -- Right-hand limit: `(N : ℝ)⁻¹ * birkhoffAverage (T^[N]) (g N) (m+1) x → (N : ℝ)⁻¹ * B x`.
    have hRHS : Tendsto
        (fun m : ℕ => (N : ℝ)⁻¹ * birkhoffAverage ℝ (T^[N]) (g N) (m + 1) x) atTop
        (𝓝 ((N : ℝ)⁻¹ * B x)) :=
      (hBconv.comp (tendsto_add_atTop_nat 1)).const_mul (N : ℝ)⁻¹
    refine le_of_tendsto_of_tendsto hLHS hRHS ?_
    -- Eventual inequality: the LHS is dominated by the RHS via block subadditivity.
    filter_upwards with m
    have hblk : g ((m + 1) * N) x ≤ birkhoffSum (T^[N]) (g N) (m + 1) x :=
      km_le_birkhoffSum_block hsub N m x
    have hmNpos : (0 : ℝ) < (((m + 1) * N : ℕ) : ℝ) := by
      have : 0 < (m + 1) * N := Nat.mul_pos (by omega) hNpos
      exact_mod_cast this
    have hcast : (((m + 1) * N : ℕ) : ℝ) = ((m + 1 : ℕ) : ℝ) * (N : ℝ) := by push_cast; ring
    have hbavg : birkhoffAverage ℝ (T^[N]) (g N) (m + 1) x
        = ((m + 1 : ℕ) : ℝ)⁻¹ * birkhoffSum (T^[N]) (g N) (m + 1) x := by
      rw [birkhoffAverage, smul_eq_mul]
    -- Compare the two normalized quantities.
    rw [hbavg]
    rw [hcast]
    rw [mul_inv]
    have hm1pos : (0 : ℝ) < ((m + 1 : ℕ) : ℝ) := by exact_mod_cast Nat.succ_pos m
    -- `(m+1)⁻¹ * N⁻¹ * g((m+1)N) ≤ N⁻¹ * ((m+1)⁻¹ * birkhoffSum)`.
    have hkey : ((m + 1 : ℕ) : ℝ)⁻¹ * (N : ℝ)⁻¹ * g ((m + 1) * N) x
        ≤ (N : ℝ)⁻¹ * (((m + 1 : ℕ) : ℝ)⁻¹ * birkhoffSum (T^[N]) (g N) (m + 1) x) := by
      have hfac : (N : ℝ)⁻¹ * (((m + 1 : ℕ) : ℝ)⁻¹ * birkhoffSum (T^[N]) (g N) (m + 1) x)
          = ((m + 1 : ℕ) : ℝ)⁻¹ * (N : ℝ)⁻¹ * birkhoffSum (T^[N]) (g N) (m + 1) x := by ring
      rw [hfac]
      have hposfac : (0 : ℝ) ≤ ((m + 1 : ℕ) : ℝ)⁻¹ * (N : ℝ)⁻¹ := by positivity
      exact mul_le_mul_of_nonneg_left hblk hposfac
    exact hkey
  -- Integrate the pointwise inequality.
  have hBint : Integrable B μ := integrable_condExp
  have hintBval : ∫ x, (N : ℝ)⁻¹ * B x ∂μ = (N : ℝ)⁻¹ * ∫ x, g N x ∂μ := by
    rw [integral_const_mul, km_integral_condExp_iterate N]
  have hmono : c ≤ ∫ x, (N : ℝ)⁻¹ * B x ∂μ := by
    have hcint : ∫ _x : X, c ∂μ = c := by
      rw [integral_const, probReal_univ, one_smul]
    rw [← hcint]
    exact integral_mono_ae (integrable_const c) (hBint.const_mul _) hpt
  rw [hintBval] at hmono
  -- `c ≤ N⁻¹ ∫ g N = (∫ g (n+1)) / (n+1)`.
  rw [hNdef] at hmono
  rw [div_eq_inv_mul]
  have hcast2 : (((n + 1 : ℕ)) : ℝ)⁻¹ = ((n : ℝ) + 1)⁻¹ := by push_cast; ring
  rwa [hcast2] at hmono

/-! ### The upper bound `c ≥ L` via Fatou on the nonnegative defect -/

omit [MeasurableSpace X] in
/-- Singleton subadditivity: `g (n+1) x ≤ birkhoffSum T (g 1) (n+1) x` for `n ≥ 0`. -/
private theorem km_le_birkhoffSum_one {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (n : ℕ) (x : X) :
    g (n + 1) x ≤ birkhoffSum T (g 1) (n + 1) x := by
  induction n with
  | zero => simp only [Nat.zero_add, birkhoffSum_one]; exact le_refl _
  | succ n ih =>
      rw [birkhoffSum_succ]
      calc g (n + 1 + 1) x ≤ g (n + 1) x + g 1 (T^[n + 1] x) := hsub.apply_add_le (n + 1) 1 x
        _ ≤ birkhoffSum T (g 1) (n + 1) x + g 1 (T^[n + 1] x) := by linarith [ih]

/-- The nonnegative Fatou defect `birkhoffAverage T (g 1) (n+1) x − g (n+1) x / (n+1)`. -/
private noncomputable def kmDefect (g : ℕ → X → ℝ) (n : ℕ) (x : X) : ℝ :=
  birkhoffAverage ℝ T (g 1) (n + 1) x - g (n + 1) x / ((n : ℝ) + 1)

omit [MeasurableSpace X] in
/-- The Fatou defect is nonnegative (singleton subadditivity). -/
private theorem kmDefect_nonneg {g : ℕ → X → ℝ} (hsub : IsSubadditiveCocycle T g) (n : ℕ) (x : X) :
    0 ≤ kmDefect (T := T) g n x := by
  have h := km_le_birkhoffSum_one hsub n x
  rw [kmDefect, sub_nonneg, birkhoffAverage, smul_eq_mul, div_eq_inv_mul]
  have hpos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
  have hcast : (((n + 1 : ℕ)) : ℝ) = (n : ℝ) + 1 := by push_cast; ring
  rw [hcast]
  exact mul_le_mul_of_nonneg_left h (le_of_lt (by positivity))

/-- `birkhoffAverage T (g 1) (n+1)` is integrable. -/
private theorem km_integrable_birkhoffAverage (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (n : ℕ) :
    Integrable (fun x => birkhoffAverage ℝ T (g 1) (n + 1) x) μ := by
  have : (fun x => birkhoffAverage ℝ T (g 1) (n + 1) x)
      = fun x => ((n + 1 : ℕ) : ℝ)⁻¹ * birkhoffSum T (g 1) (n + 1) x := rfl
  rw [this]
  exact (integrable_birkhoffSum hT (hint 1) (n + 1)).const_mul _

/-- `kmDefect g n` is integrable. -/
private theorem km_integrable_defect (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (n : ℕ) :
    Integrable (kmDefect (T := T) g n) μ :=
  (km_integrable_birkhoffAverage hT hint n).sub ((hint (n + 1)).div_const _)

/-- The integral of `birkhoffAverage T (g 1) (n+1)` is `∫ g 1`. -/
private theorem km_integral_birkhoffAverage_eq (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (n : ℕ) :
    ∫ x, birkhoffAverage ℝ T (g 1) (n + 1) x ∂μ = ∫ x, g 1 x ∂μ := by
  have hsum : ∫ x, birkhoffSum T (g 1) (n + 1) x ∂μ = ((n : ℝ) + 1) * ∫ x, g 1 x ∂μ := by
    simp only [birkhoffSum]
    rw [integral_finset_sum (f := fun k x => g 1 (T^[k] x)) _
      (fun j _ => (hT.iterate j).integrable_comp_of_integrable (hint 1))]
    have : ∀ j ∈ Finset.range (n + 1), ∫ x, g 1 (T^[j] x) ∂μ = ∫ x, g 1 x ∂μ :=
      fun j _ => km_integral_comp_iterate hT hint j 1
    rw [Finset.sum_congr rfl this, Finset.sum_const, Finset.card_range, nsmul_eq_mul]
    push_cast; ring
  have hba : ∫ x, birkhoffAverage ℝ T (g 1) (n + 1) x ∂μ
      = ((n + 1 : ℕ) : ℝ)⁻¹ * ∫ x, birkhoffSum T (g 1) (n + 1) x ∂μ := by
    rw [show (∫ x, birkhoffAverage ℝ T (g 1) (n + 1) x ∂μ)
        = ∫ x, ((n + 1 : ℕ) : ℝ)⁻¹ * birkhoffSum T (g 1) (n + 1) x ∂μ from rfl,
      integral_const_mul]
  rw [hba, hsum, show (((n + 1 : ℕ)) : ℝ) = (n : ℝ) + 1 by push_cast; ring]
  have hne : (n : ℝ) + 1 ≠ 0 := by positivity
  field_simp

/-- The integral of the Fatou defect: `∫ kmDefect n = ∫ g 1 − (∫ g (n+1))/(n+1)`. -/
private theorem km_integral_defect (hT : MeasurePreserving T μ μ) {g : ℕ → X → ℝ}
    (hint : ∀ n, Integrable (g n) μ) (n : ℕ) :
    ∫ x, kmDefect (T := T) g n x ∂μ
      = (∫ x, g 1 x ∂μ) - (∫ x, g (n + 1) x ∂μ) / (n + 1) := by
  have hba := km_integrable_birkhoffAverage hT hint n
  have hcdiv : Integrable (fun x => g (n + 1) x / ((n : ℝ) + 1)) μ := (hint (n + 1)).div_const _
  rw [show (∫ x, kmDefect (T := T) g n x ∂μ)
      = ∫ x, (birkhoffAverage ℝ T (g 1) (n + 1) x - g (n + 1) x / ((n : ℝ) + 1)) ∂μ from rfl,
    integral_sub hba hcdiv, km_integral_birkhoffAverage_eq hT hint]
  congr 1
  rw [integral_div]

/-- **Upper bound.** The a.e. Kingman constant `c` satisfies `L ≤ c`, where `L` is the Fekete
limit of the integral means. A single Fatou pass on the nonnegative defect `kmDefect g n`. -/
private theorem km_mean_le_const [IsProbabilityMeasure μ]
    (hT : MeasurePreserving T μ μ) (hTm : Measurable T) {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (hint : ∀ n, Integrable (g n) μ)
    {c : ℝ} (hc : ∀ᵐ x ∂μ, Tendsto (fun k : ℕ => (k : ℝ)⁻¹ * g k x) atTop (𝓝 c))
    {γ : ℝ} (hγ : Tendsto (fun n : ℕ => (∫ x, g (n + 1) x ∂μ) / (n + 1)) atTop (𝓝 γ)) :
    γ ≤ c := by
  -- Measurable representatives of each level, to feed the genuine-measurability Fatou.
  set g₀ : ℕ → X → ℝ := fun n => (hint n).1.mk with hg₀def
  have hg₀m : ∀ n, Measurable (g₀ n) := fun n => (hint n).1.measurable_mk
  have hgg₀ : ∀ n, g n =ᵐ[μ] g₀ n := fun n => (hint n).1.ae_eq_mk
  -- A measurable model of `ofReal (kmDefect g n)`.
  set F : ℕ → X → ℝ := fun n x =>
    birkhoffAverage ℝ T (g₀ 1) (n + 1) x - g₀ (n + 1) x / ((n : ℝ) + 1) with hFdef
  have hFm : ∀ n, Measurable (fun x => ENNReal.ofReal (F n x)) := by
    intro n
    refine ENNReal.measurable_ofReal.comp ?_
    refine Measurable.sub ?_ ((hg₀m (n + 1)).div_const _)
    change Measurable (fun x ↦ ((n + 1 : ℕ) : ℝ)⁻¹ * birkhoffSum T (g₀ 1) (n + 1) x)
    exact (measurable_birkhoffSum hTm (hg₀m 1) (n + 1)).const_mul _
  -- `F n =ᵐ kmDefect g n` for all `n` simultaneously.
  have hFeq : ∀ᵐ x ∂μ, ∀ n, ENNReal.ofReal (F n x)
      = ENNReal.ofReal (kmDefect (T := T) g n x) := by
    have hall : ∀ᵐ x ∂μ, ∀ n : ℕ, g n x = g₀ n x := ae_all_iff.2 hgg₀
    have hbs : ∀ᵐ x ∂μ, ∀ n : ℕ,
        birkhoffSum T (g 1) (n + 1) x = birkhoffSum T (g₀ 1) (n + 1) x :=
      ae_all_iff.2 (fun n => birkhoffSum_congr_ae hT (hgg₀ 1) (n + 1))
    filter_upwards [hall, hbs] with x hx hxbs
    intro n
    congr 1
    have hba : birkhoffAverage ℝ T (g₀ 1) (n + 1) x = birkhoffAverage ℝ T (g 1) (n + 1) x := by
      simp only [birkhoffAverage, smul_eq_mul]
      rw [hxbs n]
    change birkhoffAverage ℝ T (g₀ 1) (n + 1) x - g₀ (n + 1) x / ((n : ℝ) + 1)
      = birkhoffAverage ℝ T (g 1) (n + 1) x - g (n + 1) x / ((n : ℝ) + 1)
    rw [hba, hx (n + 1)]
  -- The a.e. pointwise limit of the defect, `h x := (μ[g 1 | I]) x − c ≥ 0`.
  set ig1 : ℝ := ∫ x, g 1 x ∂μ with hig1def
  set B : X → ℝ := μ[g 1 | MeasurableSpace.invariants T] with hBdef
  set h : X → ℝ := fun x => B x - c with hhdef
  have hBint : Integrable B μ := integrable_condExp
  have hhint : Integrable h μ := hBint.sub (integrable_const c)
  have hlim : ∀ᵐ x ∂μ, Tendsto (fun n => kmDefect (T := T) g n x) atTop (𝓝 (h x)) := by
    filter_upwards [hc, tendsto_birkhoffAverage_ae hT (hint 1)] with x hcx hBconv
    have hcdiv : Tendsto (fun n : ℕ => g (n + 1) x / ((n : ℝ) + 1)) atTop (𝓝 c) := by
      have hk := hcx.comp (tendsto_add_atTop_nat 1)
      refine hk.congr (fun n => ?_)
      simp only [Function.comp_apply]
      rw [div_eq_inv_mul]
      push_cast
      ring
    have hBshift : Tendsto (fun n : ℕ => birkhoffAverage ℝ T (g 1) (n + 1) x) atTop (𝓝 (B x)) :=
      hBconv.comp (tendsto_add_atTop_nat 1)
    have : (fun n => kmDefect (T := T) g n x)
        = fun n => birkhoffAverage ℝ T (g 1) (n + 1) x - g (n + 1) x / ((n : ℝ) + 1) := rfl
    rw [this]
    exact hBshift.sub hcdiv
  -- The limit `h` is `≥ 0` a.e. (limit of the nonnegative defects).
  have hhnn : ∀ᵐ x ∂μ, 0 ≤ h x := by
    filter_upwards [hlim] with x hx
    exact ge_of_tendsto hx (Eventually.of_forall (fun n => kmDefect_nonneg hsub n x))
  -- `∫ h = ig1 − c`.
  have hinth : ∫ x, h x ∂μ = ig1 - c := by
    have hcint : ∫ _x : X, c ∂μ = c := by rw [integral_const, probReal_univ, one_smul]
    rw [hhdef, integral_sub hBint (integrable_const c), hcint]
    congr 1
    exact integral_condExp (MeasurableSpace.invariants_le T)
  -- `ig1 − c ≥ 0` (since `h ≥ 0` a.e.) and `ig1 − γ ≥ 0` (since each mean `≤ ig1`).
  have hicnn : 0 ≤ ig1 - c := hinth ▸ integral_nonneg_of_ae hhnn
  have hignn : 0 ≤ ig1 - γ := by
    have hmeanlim : Tendsto (fun n : ℕ => ig1 - (∫ x, g (n + 1) x ∂μ) / (n + 1)) atTop
        (𝓝 (ig1 - γ)) := tendsto_const_nhds.sub hγ
    refine le_of_tendsto_of_tendsto (tendsto_const_nhds (x := (0 : ℝ))) hmeanlim ?_
    filter_upwards with n
    have hd : 0 ≤ ∫ x, kmDefect (T := T) g n x ∂μ :=
      integral_nonneg (fun x => kmDefect_nonneg hsub n x)
    rw [km_integral_defect hT hint n] at hd
    simpa [hig1def] using hd
  -- LHS Fatou integrand: `liminf (ofReal (d_n x)) = ofReal (h x)` a.e.
  have hLHSpt : ∀ᵐ x ∂μ,
      Filter.liminf (fun n => ENNReal.ofReal (kmDefect (T := T) g n x)) atTop
        = ENNReal.ofReal (h x) := by
    filter_upwards [hlim] with x hx
    exact (((ENNReal.continuous_ofReal.tendsto _).comp hx)).liminf_eq
  -- `∫⁻ liminf (ofReal d_n) = ofReal (∫ h) = ofReal (ig1 − c)`.
  have hLHSeq : ∫⁻ x, Filter.liminf (fun n => ENNReal.ofReal (kmDefect (T := T) g n x)) atTop ∂μ
      = ENNReal.ofReal (ig1 - c) := by
    rw [lintegral_congr_ae (by filter_upwards [hLHSpt] with x hx; rw [hx]),
      ← ofReal_integral_eq_lintegral_ofReal hhint hhnn, hinth]
  -- Genuine-measurability Fatou on the model `F`, transferred to `kmDefect`.
  have hFatou : ∫⁻ x, Filter.liminf (fun n => ENNReal.ofReal (kmDefect (T := T) g n x)) atTop ∂μ
      ≤ Filter.liminf (fun n => ∫⁻ x, ENNReal.ofReal (kmDefect (T := T) g n x) ∂μ) atTop := by
    have hbase : ∫⁻ x, Filter.liminf (fun n => ENNReal.ofReal (F n x)) atTop ∂μ
        ≤ Filter.liminf (fun n => ∫⁻ x, ENNReal.ofReal (F n x) ∂μ) atTop :=
      lintegral_liminf_le hFm
    -- Transfer the LHS by a.e. equality.
    have hlhs : ∫⁻ x, Filter.liminf (fun n => ENNReal.ofReal (F n x)) atTop ∂μ
        = ∫⁻ x, Filter.liminf (fun n => ENNReal.ofReal (kmDefect (T := T) g n x)) atTop ∂μ := by
      refine lintegral_congr_ae ?_
      filter_upwards [hFeq] with x hx
      exact congrArg (fun s => Filter.liminf s atTop) (funext hx)
    -- Transfer the RHS termwise by a.e. equality.
    have hrhs : Filter.liminf (fun n => ∫⁻ x, ENNReal.ofReal (F n x) ∂μ) atTop
        = Filter.liminf (fun n => ∫⁻ x, ENNReal.ofReal (kmDefect (T := T) g n x) ∂μ) atTop := by
      refine congrArg (fun s => Filter.liminf s atTop) (funext fun n => ?_)
      refine lintegral_congr_ae ?_
      filter_upwards [hFeq] with x hx
      exact hx n
    rw [hlhs, hrhs] at hbase
    exact hbase
  -- RHS Fatou value: `∫⁻ ofReal d_n = ofReal (ig1 − mean_n) → ofReal (ig1 − γ)`.
  have hRHSterm : ∀ n, ∫⁻ x, ENNReal.ofReal (kmDefect (T := T) g n x) ∂μ
      = ENNReal.ofReal (ig1 - (∫ x, g (n + 1) x ∂μ) / (n + 1)) := by
    intro n
    rw [← ofReal_integral_eq_lintegral_ofReal (km_integrable_defect hT hint n)
        (Eventually.of_forall (fun x => kmDefect_nonneg hsub n x)),
      km_integral_defect hT hint n, hig1def]
  have hRHSeq : Filter.liminf (fun n => ∫⁻ x, ENNReal.ofReal (kmDefect (T := T) g n x) ∂μ) atTop
      = ENNReal.ofReal (ig1 - γ) := by
    simp only [hRHSterm]
    have hconv : Tendsto (fun n => ENNReal.ofReal (ig1 - (∫ x, g (n + 1) x ∂μ) / (n + 1))) atTop
        (𝓝 (ENNReal.ofReal (ig1 - γ))) :=
      (ENNReal.continuous_ofReal.tendsto _).comp (tendsto_const_nhds.sub hγ)
    exact hconv.liminf_eq
  -- Conclude: `ofReal (ig1 − c) ≤ ofReal (ig1 − γ)`, hence `γ ≤ c`.
  rw [hLHSeq, hRHSeq] at hFatou
  have : ig1 - c ≤ ig1 - γ := (ENNReal.ofReal_le_ofReal_iff hignn).1 hFatou
  linarith

/-! ### The means identification -/

/-- **Kingman means identification.** Under the hypotheses of `tendsto_kingman_ergodic`, there is
a single constant `c` that is *both* the limit of the integral means `(∫ g (n+1)) / (n+1)` *and*
the `μ`-a.e. limit of the normalized cocycle `(n : ℝ)⁻¹ • gₙ`. -/
theorem tendsto_kingman_ergodic_means
    [IsProbabilityMeasure μ] (hT : Ergodic T μ) {g : ℕ → X → ℝ}
    (hsub : IsSubadditiveCocycle T g) (hint : ∀ n, Integrable (g n) μ)
    (hbdd : BddBelow (Set.range fun n : ℕ => (∫ x, g (n + 1) x ∂μ) / (n + 1))) :
    ∃ c : ℝ, Tendsto (fun n : ℕ => (∫ x, g (n + 1) x ∂μ) / (n + 1)) atTop (𝓝 c) ∧
      ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * g n x) atTop (𝓝 c) := by
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  -- The a.e. Kingman limit `cK`, and the Fekete limit `γ` of the integral means.
  obtain ⟨cK, hcK⟩ := tendsto_kingman_ergodic hT hsub hint hbdd
  obtain ⟨γ, hγ⟩ := km_exists_fekete hmp hsub hint hbdd
  -- The two constants coincide: `cK ≤ γ` (block subadditivity) and `γ ≤ cK` (Fatou).
  have hle : cK ≤ γ := by
    refine le_of_tendsto_of_tendsto (tendsto_const_nhds (x := cK)) hγ ?_
    filter_upwards with n
    exact km_const_le_mean hmp hsub hint hcK n
  have hge : γ ≤ cK := km_mean_le_const hmp hT.measurable hsub hint hcK hγ
  have heq : cK = γ := le_antisymm hle hge
  refine ⟨cK, ?_, hcK⟩
  rw [heq]
  exact hγ

end ErgodicTheory
