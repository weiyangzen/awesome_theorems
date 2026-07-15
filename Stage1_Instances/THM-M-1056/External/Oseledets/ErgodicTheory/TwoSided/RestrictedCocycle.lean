/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.TwoSided.Invertible
import ErgodicTheory.TwoSided.KingmanMeans
import ErgodicTheory.Lyapunov.MeasurableSubspace
import ErgodicTheory.Cocycle.FurstenbergKesten
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit

/-!
# The backward-orbit restricted envelope

For a fixed measurable family of subspaces `V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))`
this module builds the **restricted cocycle** used in the transversality crux of the
two-sided multiplicative ergodic theorem. The restricted generator is
`restGen A V x = A x * orthProjMatrix (V x)` and the restricted log-norm cocycle is

```
restLog A V T n x = Real.log (‖cocycle (restGen A V) T n x‖ ⊔ sFloor A T n x)
```

where `sFloor A T n x = ∏_{j<n} (‖(A (T^[j] x))⁻¹‖)⁻¹` is a strictly-positive *floor*.

The floor is the key device: plain `log ‖cocycle (A·P)‖` fails to be subadditive at the
"junk" points where the restricted product collapses to the zero matrix (`log 0 = 0`). The
`⊔`-floor makes the floored quantity *everywhere* strictly positive, so
`restLog` is subadditive over `T` for *all* `m, n, x` — exactly the everywhere hypothesis
Kingman's theorem needs. On a biinvariant conull *good* set (flag equivariance along the
orbit plus `V ≠ ⊥`) the floor is absorbed and `restLog n x = log ‖A⁽ⁿ⁾(x)·P_{V(x)}‖`.

## Main definitions

* `ErgodicTheory.restGen`: the restricted generator `x ↦ A x * orthProjMatrix (V x)`.
* `ErgodicTheory.sFloor`: the strictly-positive floor `∏_{j<n} (‖(A (T^[j] x))⁻¹‖)⁻¹`.
* `ErgodicTheory.restLog`: the floored restricted log-norm cocycle.

## Main results

* `ErgodicTheory.sFloor_pos`, `ErgodicTheory.sFloor_mul`: positivity and multiplicativity of the
  floor.
* `ErgodicTheory.isSubadditiveCocycle_restLog`: `restLog` is an *everywhere* subadditive
  cocycle over `T`.
* `ErgodicTheory.measurable_restLog`, `ErgodicTheory.integrable_restLog`: measurability and
  integrability of each level.
* `ErgodicTheory.restLog_eq_on_good`: on the good set the floor is absorbed,
  `restLog n y = log ‖A⁽ⁿ⁾(y)·P_{V(y)}‖`.
* `ErgodicTheory.restLog_kingman`: Kingman over `T` for `restLog` with the constant identified
  as the limit of the integral means (via `tendsto_kingman_ergodic_means`).
* `ErgodicTheory.restLog_backward_kingman`: the backward transfer — `restLog ∘ (T.symm)^[·]`
  is subadditive over `T.symm` with the *same* constant.
-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} {d : ℕ}

/-! ### The restricted generator and the floor -/

/-- The **restricted generator** `x ↦ A x * orthProjMatrix (V x)`: the forward generator
post-composed (on the right) with the orthogonal projection onto `V x`. -/
noncomputable def restGen (A : X → Matrix (Fin d) (Fin d) ℝ)
    (V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))) : X → Matrix (Fin d) (Fin d) ℝ :=
  fun x => A x * orthProjMatrix (V x)

/-- The strictly-positive **floor** `∏_{j<n} (‖(A (T^[j] x))⁻¹‖)⁻¹`. Multiplicative along the
orbit; bounded below the cocycle norm on the good set. -/
noncomputable def sFloor (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) : ℝ :=
  ∏ j ∈ Finset.range n, (‖(A (T^[j] x))⁻¹‖)⁻¹

/-- The floored restricted log-norm cocycle
`restLog A V T n x = log (‖cocycle (restGen A V) T n x‖ ⊔ sFloor A T n x)`. -/
noncomputable def restLog (A : X → Matrix (Fin d) (Fin d) ℝ)
    (V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))) (T : X → X) (n : ℕ) (x : X) : ℝ :=
  Real.log (‖cocycle (restGen A V) T n x‖ ⊔ sFloor A T n x)

/-- For nonnegative reals, `max (a*b) (c*d) ≤ max a c * max b d`. -/
theorem max_mul_le_mul_max {a b c e : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (he : 0 ≤ e) : a * b ⊔ c * e ≤ (a ⊔ c) * (b ⊔ e) := by
  refine max_le ?_ ?_
  · exact mul_le_mul (le_max_left a c) (le_max_left b e) hb (le_trans ha (le_max_left a c))
  · exact mul_le_mul (le_max_right a c) (le_max_right b e) he (le_trans hc (le_max_right a c))

/-! ### Positivity and multiplicativity of the floor -/

/-- Each floor factor `(‖(A y)⁻¹‖)⁻¹` is strictly positive for an invertible generator. -/
theorem sFloor_factor_pos {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0)
    [NeZero d] (y : X) : 0 < (‖(A y)⁻¹‖)⁻¹ := by
  have hpos : 0 < ‖(A y)⁻¹‖ := by
    rw [norm_pos_iff]
    intro h
    have hdet : (A y)⁻¹.det ≠ 0 := by
      rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA y)
    exact hdet (by rw [h, Matrix.det_zero]; exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩⟩)
  positivity

/-- The floor is strictly positive. -/
theorem sFloor_pos {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    [NeZero d] (n : ℕ) (x : X) : 0 < sFloor A T n x :=
  Finset.prod_pos fun j _ => sFloor_factor_pos hA (T^[j] x)

/-- **Floor multiplicativity.** `sFloor (m + n) x = sFloor m x * sFloor n (T^[m] x)`. -/
theorem sFloor_mul {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} (m n : ℕ) (x : X) :
    sFloor A T (m + n) x = sFloor A T m x * sFloor A T n (T^[m] x) := by
  unfold sFloor
  rw [Finset.prod_range_add]
  congr 1
  refine Finset.prod_congr rfl (fun j _ => ?_)
  rw [← Function.iterate_add_apply, Nat.add_comm m j]

/-! ### Everywhere subadditivity of the floored restricted log cocycle -/

/-- **Everywhere subadditivity.** `restLog A V T` is a subadditive cocycle over `T` for *all*
`m, n, x` (no a.e. caveat): the floor `sFloor` is strictly positive, so the `⊔` is always
positive and `Real.log` is monotone with `Real.log_mul` available. This is precisely the
everywhere hypothesis Kingman's theorem requires; plain `log ‖cocycle (A·P)‖` fails to be
subadditive at the junk points where the restricted product vanishes. -/
theorem isSubadditiveCocycle_restLog {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] :
    IsSubadditiveCocycle T (restLog A V T) := by
  refine ⟨fun m n x => ?_⟩
  set G := restGen A V with hG
  -- Shorthand for the four nonnegative quantities.
  set a : ℝ := ‖cocycle G T n (T^[m] x)‖ with ha
  set b : ℝ := ‖cocycle G T m x‖ with hb
  set a' : ℝ := sFloor A T n (T^[m] x) with ha'
  set b' : ℝ := sFloor A T m x with hb'
  have hann : 0 ≤ a := norm_nonneg _
  have hbnn : 0 ≤ b := norm_nonneg _
  have ha'pos : 0 < a' := sFloor_pos hA n _
  have hb'pos : 0 < b' := sFloor_pos hA m x
  -- The maxes are strictly positive (the floor pins them up).
  have hmaxa : 0 < a ⊔ a' := lt_of_lt_of_le ha'pos (le_max_right a a')
  have hmaxb : 0 < b ⊔ b' := lt_of_lt_of_le hb'pos (le_max_right b b')
  -- Factorization of the `(m+n)`-level via the cocycle identity and floor multiplicativity.
  have hcocfac : cocycle G T (m + n) x = cocycle G T n (T^[m] x) * cocycle G T m x := by
    rw [Nat.add_comm m n]; exact cocycle_add G T n m x
  have hsubmul : ‖cocycle G T (m + n) x‖ ≤ a * b := by
    rw [hcocfac]; exact Matrix.l2_opNorm_mul _ _
  have hfloorfac : sFloor A T (m + n) x = b' * a' := by
    rw [sFloor_mul]
  -- `max (‖coc‖) (sFloor) ≤ max a a' * max b b'`.
  have hkey : ‖cocycle G T (m + n) x‖ ⊔ sFloor A T (m + n) x ≤ (a ⊔ a') * (b ⊔ b') := by
    have hle : ‖cocycle G T (m + n) x‖ ⊔ sFloor A T (m + n) x ≤ a * b ⊔ a' * b' := by
      rw [hfloorfac, mul_comm b' a']
      exact max_le_max hsubmul (le_refl _)
    exact le_trans hle (max_mul_le_mul_max hann hbnn ha'pos.le hb'pos.le)
  -- Take logs.
  have hpos : 0 < ‖cocycle G T (m + n) x‖ ⊔ sFloor A T (m + n) x :=
    lt_of_lt_of_le (sFloor_pos hA (m + n) x) (le_max_right _ _)
  calc restLog A V T (m + n) x
      = Real.log (‖cocycle G T (m + n) x‖ ⊔ sFloor A T (m + n) x) := rfl
    _ ≤ Real.log ((a ⊔ a') * (b ⊔ b')) := Real.log_le_log hpos hkey
    _ = Real.log (a ⊔ a') + Real.log (b ⊔ b') :=
        Real.log_mul (ne_of_gt hmaxa) (ne_of_gt hmaxb)
    _ = restLog A V T m x + restLog A V T n (T^[m] x) := by
        rw [restLog, restLog, ha, hb, ha', hb']; ring

/-! ### Elementary norm facts feeding the integrability sandwich -/

/-- `‖restGen A V x‖ ≤ ‖A x‖`: the projection is a contraction. -/
theorem norm_restGen_le {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (x : X) :
    ‖restGen A V x‖ ≤ ‖A x‖ := by
  have hP : ‖orthProjMatrix (V x)‖ ≤ 1 := by
    rw [← Matrix.l2_opNorm_toEuclideanCLM, orthProjMatrix, StarAlgEquiv.apply_symm_apply]
    exact Submodule.starProjection_norm_le _
  calc ‖restGen A V x‖ ≤ ‖A x‖ * ‖orthProjMatrix (V x)‖ := Matrix.l2_opNorm_mul _ _
    _ ≤ ‖A x‖ * 1 := by gcongr
    _ = ‖A x‖ := mul_one _

/-- `‖cocycle (restGen A V) T n x‖ ≤ ∏_{j<n} ‖A (T^[j] x)‖`. -/
theorem norm_cocycle_restGen_le_prod {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} (n : ℕ) (x : X) :
    ‖cocycle (restGen A V) T n x‖ ≤ ∏ j ∈ Finset.range n, ‖A (T^[j] x)‖ := by
  induction n generalizing x with
  | zero =>
    simp only [cocycle_zero, Finset.range_zero, Finset.prod_empty]
    rw [← Matrix.l2_opNorm_toEuclideanCLM, map_one]
    exact ContinuousLinearMap.norm_id_le
  | succ n ih =>
    rw [cocycle_succ (restGen A V) T n x, Finset.prod_range_succ']
    calc ‖cocycle (restGen A V) T n (T x) * restGen A V x‖
        ≤ ‖cocycle (restGen A V) T n (T x)‖ * ‖restGen A V x‖ := Matrix.l2_opNorm_mul _ _
      _ ≤ (∏ j ∈ Finset.range n, ‖A (T^[j] (T x))‖) * ‖A x‖ :=
          mul_le_mul (ih (T x)) (norm_restGen_le _) (norm_nonneg _) (Finset.prod_nonneg
            (fun j _ => norm_nonneg _))
      _ = (∏ j ∈ Finset.range n, ‖A (T^[(j + 1)] x)‖) * ‖A (T^[0] x)‖ := by
          simp only [Function.iterate_succ_apply, Function.iterate_zero_apply]

/-- `(‖M⁻¹‖)⁻¹ ≤ ‖M‖` for an invertible matrix. -/
theorem inv_norm_inv_le_norm {M : Matrix (Fin d) (Fin d) ℝ} [NeZero d] (hM : M.det ≠ 0) :
    (‖M⁻¹‖)⁻¹ ≤ ‖M‖ := by
  have hmulinv : M * M⁻¹ = 1 := Matrix.mul_nonsing_inv _ (Ne.isUnit hM)
  have h1 : (1 : ℝ) ≤ ‖M‖ * ‖M⁻¹‖ := by
    have := Matrix.l2_opNorm_mul M M⁻¹
    rw [hmulinv, norm_one_matrix] at this; exact this
  have hinvpos : 0 < ‖M⁻¹‖ := by
    rw [norm_pos_iff]; intro h
    have hdet : (M⁻¹).det ≠ 0 := by
      rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero hM
    exact hdet (by rw [h, Matrix.det_zero]; exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩⟩)
  rw [inv_le_iff_one_le_mul₀ hinvpos]; linarith

/-- `Real.posLog t = Real.log (t ⊔ 1)` for `t ≥ 0`. -/
theorem posLog_eq_log_max_one {t : ℝ} (ht : 0 ≤ t) : Real.posLog t = Real.log (t ⊔ 1) := by
  rw [Real.posLog_def]
  rcases le_total t 1 with h | h
  · rw [max_eq_right h, Real.log_one, max_eq_left (Real.log_nonpos ht h)]
  · rw [max_eq_left h, max_eq_right (Real.log_nonneg h)]

/-! ### The sandwich bounds -/

/-- **Lower sandwich.** `restLog n x ≥ log (sFloor n x) = -∑ log‖(A∘T^[j])⁻¹‖`. -/
theorem log_sFloor_le_restLog {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    [NeZero d] (n : ℕ) (x : X) :
    Real.log (sFloor A T n x) ≤ restLog A V T n x :=
  Real.log_le_log (sFloor_pos hA n x) (le_max_right _ _)

/-- `log (sFloor n x) = - birkhoffSum T (log‖A⁻¹‖) n x`. -/
theorem log_sFloor_eq {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] (n : ℕ) (x : X) :
    Real.log (sFloor A T n x)
      = - birkhoffSum T (fun y => Real.log ‖(A y)⁻¹‖) n x := by
  unfold sFloor
  rw [Real.log_prod (fun j _ => ne_of_gt (sFloor_factor_pos hA (T^[j] x)))]
  rw [birkhoffSum, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl (fun j _ => ?_)
  rw [Real.log_inv]

/-- **Upper sandwich.** `restLog n x ≤ birkhoffSum T (log⁺‖A‖) n x`. The `⊔` is dominated by
`∏ (‖A∘T^[j]‖ ⊔ 1)`, whose log is the positive-log Birkhoff sum. -/
theorem restLog_le_birkhoffSum {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    [NeZero d] (n : ℕ) (x : X) :
    restLog A V T n x ≤ birkhoffSum T (fun y => Real.posLog ‖A y‖) n x := by
  set cap : ℕ → ℝ := fun j => ‖A (T^[j] x)‖ ⊔ 1 with hcap
  have hcap_pos : ∀ j, 0 < cap j := fun j => lt_of_lt_of_le one_pos (le_max_right _ _)
  -- `P ≤ ∏ cap` and `F ≤ ∏ cap`.
  have hPle : ‖cocycle (restGen A V) T n x‖ ≤ ∏ j ∈ Finset.range n, cap j := by
    refine le_trans (norm_cocycle_restGen_le_prod n x) ?_
    exact Finset.prod_le_prod (fun j _ => norm_nonneg _) (fun j _ => le_max_left _ _)
  have hFle : sFloor A T n x ≤ ∏ j ∈ Finset.range n, cap j := by
    unfold sFloor
    refine Finset.prod_le_prod (fun j _ => le_of_lt (sFloor_factor_pos hA (T^[j] x))) ?_
    intro j _
    exact le_trans (inv_norm_inv_le_norm (hA (T^[j] x))) (le_max_left _ _)
  have hmaxle : ‖cocycle (restGen A V) T n x‖ ⊔ sFloor A T n x ≤ ∏ j ∈ Finset.range n, cap j :=
    max_le hPle hFle
  have hprodpos : 0 < ∏ j ∈ Finset.range n, cap j := Finset.prod_pos fun j _ => hcap_pos j
  calc restLog A V T n x
      ≤ Real.log (∏ j ∈ Finset.range n, cap j) := Real.log_le_log
        (lt_of_lt_of_le (sFloor_pos hA n x) (le_max_right _ _)) hmaxle
    _ = ∑ j ∈ Finset.range n, Real.log (cap j) :=
        Real.log_prod (fun j _ => ne_of_gt (hcap_pos j))
    _ = birkhoffSum T (fun y => Real.posLog ‖A y‖) n x := by
        rw [birkhoffSum]
        refine Finset.sum_congr rfl (fun j _ => ?_)
        rw [hcap, posLog_eq_log_max_one (norm_nonneg _)]

/-! ### Measurability and integrability of each level -/

section Measurability

variable [MeasurableSpace X]

/-- The restricted generator is measurable when `A` and the subspace family are. -/
theorem measurable_restGen {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hAmeas : Measurable A)
    (hV : MeasurableSubspace V) : Measurable (restGen A V) :=
  hAmeas.mul hV

/-- The floor is measurable. -/
theorem measurable_sFloor {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hAmeas : Measurable A) (hTmeas : Measurable T) (n : ℕ) :
    Measurable (fun x => sFloor A T n x) := by
  unfold sFloor
  refine Finset.measurable_prod _ (fun j _ => ?_)
  have hAj : Measurable fun x => A (T^[j] x) := hAmeas.comp (hTmeas.iterate j)
  exact ((measurable_l2_opNorm.comp (measurable_inv_matrix.comp hAj)).inv)

/-- Each level `restLog n` is measurable. -/
theorem measurable_restLog {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} (hAmeas : Measurable A)
    (hV : MeasurableSubspace V) (hTmeas : Measurable T) (n : ℕ) :
    Measurable (fun x => restLog A V T n x) := by
  unfold restLog
  refine Real.measurable_log.comp ?_
  refine Measurable.max ?_ (measurable_sFloor hAmeas hTmeas n)
  exact measurable_l2_opNorm.comp (measurable_cocycle (measurable_restGen hAmeas hV) hTmeas n)

variable {μ : Measure X}

/-- **Integrability of each level.** Each `restLog n` is integrable, via the sandwich
`-(birkhoffSum log⁺‖A‖ + birkhoffSum log⁺‖A⁻¹‖) ≤ restLog n ≤ birkhoffSum log⁺‖A‖` whose
endpoints are integrable (mirroring `integrable_logNorm_cocycle`). -/
theorem integrable_restLog {T : X → X} (hT : MeasurePreserving T μ μ) [IsFiniteMeasure μ]
    {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hA : ∀ x, (A x).det ≠ 0) [NeZero d]
    (hAmeas : Measurable A) (hV : MeasurableSubspace V) (hTmeas : Measurable T)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (n : ℕ) : Integrable (fun x => restLog A V T n x) μ := by
  have hBp_int : Integrable
      (fun x => birkhoffSum T (fun y => Real.posLog ‖A y‖) n x) μ :=
    integrable_birkhoffSum hT hint n
  have hBm_int : Integrable
      (fun x => birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x) μ :=
    integrable_birkhoffSum hT hint' n
  refine Integrable.mono' (hBp_int.add hBm_int)
    (measurable_restLog hAmeas hV hTmeas n).aestronglyMeasurable
    (Filter.Eventually.of_forall fun x => ?_)
  -- Sandwich `|restLog n x| ≤ birkhoffSum log⁺‖A‖ + birkhoffSum log⁺‖A⁻¹‖`.
  have hub : restLog A V T n x ≤ birkhoffSum T (fun y => Real.posLog ‖A y‖) n x :=
    restLog_le_birkhoffSum hA n x
  have hlb' : - birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x ≤ restLog A V T n x := by
    refine le_trans ?_ (log_sFloor_le_restLog hA n x)
    rw [log_sFloor_eq hA n x]
    have hmono : birkhoffSum T (fun y => Real.log ‖(A y)⁻¹‖) n x
        ≤ birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x := by
      unfold birkhoffSum
      refine Finset.sum_le_sum (fun j _ => ?_)
      simp only
      rw [Real.posLog_def]; exact le_max_right _ _
    linarith
  have hBp_nonneg : 0 ≤ birkhoffSum T (fun y => Real.posLog ‖A y‖) n x :=
    Finset.sum_nonneg fun k _ => Real.posLog_nonneg
  have hBm_nonneg : 0 ≤ birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x :=
    Finset.sum_nonneg fun k _ => Real.posLog_nonneg
  rw [Real.norm_eq_abs, abs_le]
  exact ⟨by simp only [Pi.add_apply]; linarith, by simp only [Pi.add_apply]; linarith⟩

end Measurability

/-! ### The good set: floor absorption and the unrestricted form -/

/-- The orthogonal-projection matrix is idempotent. -/
theorem orthProjMatrix_idem (K : Submodule ℝ (EuclideanSpace ℝ (Fin d))) :
    orthProjMatrix K * orthProjMatrix K = orthProjMatrix K := by
  have hinj : Function.Injective (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)) :=
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)).injective
  apply hinj
  rw [map_mul, orthProjMatrix, StarAlgEquiv.apply_symm_apply]
  refine ContinuousLinearMap.ext (fun v => ?_)
  rw [ContinuousLinearMap.mul_apply]
  exact Submodule.starProjection_eq_self_iff.mpr (K.starProjection_apply_mem v)

/-- **Multi-step flag equivariance.** Given the one-step equivariance
`P(T z) · A z · P z = A z · P z` along the orbit, the projection `P(T^[m] y)` fixes
`A⁽ᵐ⁾(y) · P y`. -/
theorem restEquivariant_iterate {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} {y : X}
    (hequiv : ∀ k : ℕ, orthProjMatrix (V (T (T^[k] y))) * A (T^[k] y) * orthProjMatrix (V (T^[k] y))
      = A (T^[k] y) * orthProjMatrix (V (T^[k] y))) (m : ℕ) :
    orthProjMatrix (V (T^[m] y)) * cocycle A T m y * orthProjMatrix (V y)
      = cocycle A T m y * orthProjMatrix (V y) := by
  induction m with
  | zero => simp only [Function.iterate_zero_apply, cocycle_zero, one_mul, mul_one,
      orthProjMatrix_idem]
  | succ m ih =>
    rw [cocycle_succ' A T m y, Function.iterate_succ_apply']
    have hstep := hequiv m
    -- Insert `P(T^[m] y)` via the IH, apply one-step equivariance, then peel it back off.
    calc orthProjMatrix (V (T (T^[m] y))) * (A (T^[m] y) * cocycle A T m y)
            * orthProjMatrix (V y)
        = orthProjMatrix (V (T (T^[m] y))) * A (T^[m] y)
            * (cocycle A T m y * orthProjMatrix (V y)) := by noncomm_ring
      _ = orthProjMatrix (V (T (T^[m] y))) * A (T^[m] y)
            * (orthProjMatrix (V (T^[m] y)) * cocycle A T m y * orthProjMatrix (V y)) := by
          rw [ih]
      _ = orthProjMatrix (V (T (T^[m] y))) * A (T^[m] y) * orthProjMatrix (V (T^[m] y))
            * (cocycle A T m y * orthProjMatrix (V y)) := by noncomm_ring
      _ = A (T^[m] y) * orthProjMatrix (V (T^[m] y))
            * (cocycle A T m y * orthProjMatrix (V y)) := by
          rw [hstep]
      _ = A (T^[m] y)
            * (orthProjMatrix (V (T^[m] y)) * cocycle A T m y * orthProjMatrix (V y)) := by
          noncomm_ring
      _ = A (T^[m] y) * (cocycle A T m y * orthProjMatrix (V y)) := by rw [ih]
      _ = A (T^[m] y) * cocycle A T m y * orthProjMatrix (V y) := by noncomm_ring

/-- **The restricted matrix identity on the good set** (levels `≥ 1`). With the one-step flag
equivariance along the orbit, `cocycle (restGen A V) T (n+1) y = cocycle A T (n+1) y · P_{V y}`.
(At `n = 0` the identity reads `1 = P_{V y}`, which fails unless `V y = ⊤`; hence the `n+1`.) -/
theorem cocycle_restGen_eq {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} {y : X}
    (hequiv : ∀ k : ℕ, orthProjMatrix (V (T (T^[k] y))) * A (T^[k] y) * orthProjMatrix (V (T^[k] y))
      = A (T^[k] y) * orthProjMatrix (V (T^[k] y))) (n : ℕ) :
    cocycle (restGen A V) T (n + 1) y
      = cocycle A T (n + 1) y * orthProjMatrix (V y) := by
  induction n with
  | zero =>
    rw [cocycle_one, cocycle_one, restGen]
  | succ n ih =>
    rw [cocycle_succ' (restGen A V) T (n + 1) y, ih, cocycle_succ' A T (n + 1) y]
    have hfix := restEquivariant_iterate hequiv (n + 1)
    calc restGen A V (T^[n + 1] y) * (cocycle A T (n + 1) y * orthProjMatrix (V y))
        = A (T^[n + 1] y) * (orthProjMatrix (V (T^[n + 1] y))
            * cocycle A T (n + 1) y * orthProjMatrix (V y)) := by
          rw [restGen]; noncomm_ring
      _ = A (T^[n + 1] y) * (cocycle A T (n + 1) y * orthProjMatrix (V y)) := by rw [hfix]
      _ = A (T^[n + 1] y) * cocycle A T (n + 1) y * orthProjMatrix (V y) := by noncomm_ring

/-- `‖(cocycle A T n y)⁻¹‖ ≤ ∏_{j<n} ‖(A (T^[j] y))⁻¹‖` (submultiplicativity of the inverse
cocycle norm). -/
theorem norm_inv_cocycle_le_prod {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (n : ℕ) (y : X) :
    ‖(cocycle A T n y)⁻¹‖ ≤ ∏ j ∈ Finset.range n, ‖(A (T^[j] y))⁻¹‖ := by
  induction n generalizing y with
  | zero =>
    simp only [cocycle_zero, Finset.range_zero, Finset.prod_empty, inv_one]
    rw [← Matrix.l2_opNorm_toEuclideanCLM, map_one]
    exact ContinuousLinearMap.norm_id_le
  | succ n ih =>
    rw [cocycle_succ A T n y, Matrix.mul_inv_rev, Finset.prod_range_succ']
    calc ‖(A y)⁻¹ * (cocycle A T n (T y))⁻¹‖
        ≤ ‖(A y)⁻¹‖ * ‖(cocycle A T n (T y))⁻¹‖ := Matrix.l2_opNorm_mul _ _
      _ ≤ ‖(A y)⁻¹‖ * ∏ j ∈ Finset.range n, ‖(A (T^[j] (T y)))⁻¹‖ :=
          mul_le_mul_of_nonneg_left (ih (T y)) (norm_nonneg _)
      _ = (∏ j ∈ Finset.range n, ‖(A (T^[(j + 1)] y))⁻¹‖) * ‖(A (T^[0] y))⁻¹‖ := by
          rw [mul_comm]
          simp only [Function.iterate_succ_apply, Function.iterate_zero_apply]

/-- **Floor absorption.** On the good set (`V y ≠ ⊥`), the floor is below the restricted
cocycle norm: `sFloor A T n y ≤ ‖cocycle A T n y · P_{V y}‖`. (A unit vector `v ∈ V y` is fixed
by the projection, so `‖A⁽ⁿ⁾ v‖ ≥ ‖(A⁽ⁿ⁾)⁻¹‖⁻¹ ≥ sFloor`.) -/
theorem sFloor_le_norm_cocycle_mul_proj [MeasurableSpace X] {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    [NeZero d] {y : X} (hVy : V y ≠ ⊥) (n : ℕ) :
    sFloor A T n y ≤ ‖cocycle A T n y * orthProjMatrix (V y)‖ := by
  -- Pick a unit vector in `V y`.
  obtain ⟨w, hwK, hw0⟩ := (V y).exists_mem_ne_zero_of_ne_bot hVy
  set v : EuclideanSpace ℝ (Fin d) := (‖w‖)⁻¹ • w with hv
  have hvmem : v ∈ V y := (V y).smul_mem _ hwK
  have hvnorm : ‖v‖ = 1 := by
    rw [hv, norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ (by simpa using hw0)]
  -- `(A⁽ⁿ⁾ · P) v = A⁽ⁿ⁾ v` and its norm bounds `‖A⁽ⁿ⁾ · P‖`.
  set N : Matrix (Fin d) (Fin d) ℝ := cocycle A T n y * orthProjMatrix (V y) with hN
  have happ : Matrix.toEuclideanCLM (𝕜 := ℝ) N v
      = Matrix.toEuclideanLin (cocycle A T n y) v := by
    rw [hN, map_mul]
    simp only [ContinuousLinearMap.mul_apply]
    have hPv : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix (V y)) v = v := by
      rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
      exact Submodule.starProjection_eq_self_iff.mpr hvmem
    rw [hPv]
    rfl
  have hNlb : ‖Matrix.toEuclideanLin (cocycle A T n y) v‖ ≤ ‖N‖ := by
    have hle := (Matrix.toEuclideanCLM (𝕜 := ℝ) N).le_opNorm v
    rw [Matrix.l2_opNorm_toEuclideanCLM, hvnorm, mul_one, happ] at hle
    exact hle
  -- `‖A⁽ⁿ⁾ v‖ ≥ ‖(A⁽ⁿ⁾)⁻¹‖⁻¹`.
  have hgrow : (‖(cocycle A T n y)⁻¹‖)⁻¹ ≤ ‖Matrix.toEuclideanLin (cocycle A T n y) v‖ := by
    have hsand := norm_le_norm_inv_mul_norm_cocycle_apply (T := T) hA n y v
    rw [hvnorm] at hsand
    have hinvpos : 0 < ‖(cocycle A T n y)⁻¹‖ := norm_inv_cocycle_pos hA n y
    rw [inv_le_iff_one_le_mul₀ hinvpos, mul_comm]
    linarith
  -- `sFloor ≤ ‖(A⁽ⁿ⁾)⁻¹‖⁻¹`.
  have hfloor : sFloor A T n y ≤ (‖(cocycle A T n y)⁻¹‖)⁻¹ := by
    have hprodeq : sFloor A T n y = (∏ j ∈ Finset.range n, ‖(A (T^[j] y))⁻¹‖)⁻¹ := by
      unfold sFloor; rw [Finset.prod_inv_distrib]
    rw [hprodeq]
    have hinvpos : 0 < ‖(cocycle A T n y)⁻¹‖ := norm_inv_cocycle_pos hA n y
    have hprodpos : 0 < ∏ j ∈ Finset.range n, ‖(A (T^[j] y))⁻¹‖ :=
      Finset.prod_pos fun j _ => by
        have := sFloor_factor_pos hA (T^[j] y)
        rw [inv_pos] at this; exact this
    rw [inv_le_inv₀ hprodpos hinvpos]
    exact norm_inv_cocycle_le_prod n y
  calc sFloor A T n y ≤ (‖(cocycle A T n y)⁻¹‖)⁻¹ := hfloor
    _ ≤ ‖Matrix.toEuclideanLin (cocycle A T n y) v‖ := hgrow
    _ ≤ ‖N‖ := hNlb

/-- **The unrestricted form on the good set.** With one-step flag equivariance along the orbit
and `V y ≠ ⊥`, for `n ≥ 1` the floor is absorbed and
`restLog A V T n y = log ‖A⁽ⁿ⁾(y) · P_{V y}‖`. (This is the form consumed by the restricted
exponent computation; the `⊔`-floor was needed only for the everywhere-subadditivity feeding
Kingman.) -/
theorem restLog_eq_on_good [MeasurableSpace X] {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    [NeZero d] {y : X}
    (hequiv : ∀ k : ℕ, orthProjMatrix (V (T (T^[k] y))) * A (T^[k] y) * orthProjMatrix (V (T^[k] y))
      = A (T^[k] y) * orthProjMatrix (V (T^[k] y)))
    (hVy : V y ≠ ⊥) (n : ℕ) :
    restLog A V T (n + 1) y
      = Real.log ‖cocycle A T (n + 1) y * orthProjMatrix (V y)‖ := by
  unfold restLog
  rw [cocycle_restGen_eq hequiv n]
  congr 1
  exact max_eq_left (sFloor_le_norm_cocycle_mul_proj hA hVy (n + 1))

/-! ### Kingman over `T` and the means identification -/

section Kingman

variable [MeasurableSpace X] {μ : Measure X}

/-- The bounded-below proviso for `restLog`: each normalized integral mean is
`≥ - ∫ log⁺‖A⁻¹‖`. From the lower sandwich `restLog n ≥ - birkhoffSum (log⁺‖A⁻¹‖) n`. -/
theorem bddBelow_restLog_means {T : X → X} (hT : MeasurePreserving T μ μ)
    [IsFiniteMeasure μ] {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hA : ∀ x, (A x).det ≠ 0) [NeZero d]
    (hAmeas : Measurable A) (hV : MeasurableSubspace V) (hTmeas : Measurable T)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    BddBelow (Set.range fun n : ℕ => (∫ x, restLog A V T (n + 1) x ∂μ) / (n + 1)) := by
  refine ⟨- ∫ x, Real.posLog ‖(A x)⁻¹‖ ∂μ, ?_⟩
  rintro _ ⟨n, rfl⟩
  have hpos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
  rw [le_div_iff₀ hpos]
  -- `restLog (n+1) ≥ - birkhoffSum (log⁺‖A⁻¹‖) (n+1)`.
  have hlb : ∀ x, - birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) (n + 1) x
      ≤ restLog A V T (n + 1) x := by
    intro x
    refine le_trans ?_ (log_sFloor_le_restLog (V := V) hA (n + 1) x)
    rw [log_sFloor_eq hA (n + 1) x]
    have hmono : birkhoffSum T (fun y => Real.log ‖(A y)⁻¹‖) (n + 1) x
        ≤ birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) (n + 1) x := by
      unfold birkhoffSum
      refine Finset.sum_le_sum (fun j _ => ?_)
      simp only
      rw [Real.posLog_def]; exact le_max_right _ _
    linarith
  have hmono : - ∫ x, birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) (n + 1) x ∂μ ≤
      ∫ x, restLog A V T (n + 1) x ∂μ := by
    rw [← integral_neg]
    exact integral_mono ((integrable_birkhoffSum hT hint' (n + 1)).neg)
      (integrable_restLog hT hA hAmeas hV hTmeas hint hint' (n + 1)) hlb
  rw [integral_birkhoffSum hT hint' (n + 1), nsmul_eq_mul] at hmono
  push_cast at hmono ⊢
  nlinarith [hmono]

/-- **Kingman over `T` with identified means.** Under ergodicity, there is a constant `χ_V`
that is *both* the limit of the integral means `(∫ restLog (n+1)) / (n+1)` and the `μ`-a.e.
limit of `(n : ℝ)⁻¹ • restLog n`. The means identification (`tendsto_kingman_ergodic_means`)
is what lets the backward transfer pin down the same constant. -/
theorem restLog_kingman [IsProbabilityMeasure μ] {T : X → X} (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hA : ∀ x, (A x).det ≠ 0) [NeZero d]
    (hAmeas : Measurable A) (hV : MeasurableSubspace V)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ c : ℝ,
      Tendsto (fun n : ℕ => (∫ x, restLog A V T (n + 1) x ∂μ) / (n + 1)) atTop (𝓝 c) ∧
      ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * restLog A V T n x) atTop (𝓝 c) := by
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  have hTmeas : Measurable T := hmp.measurable
  exact tendsto_kingman_ergodic_means hT (isSubadditiveCocycle_restLog (V := V) hA)
    (fun n => integrable_restLog hmp hA hAmeas hV hTmeas hint hint' n)
    (bddBelow_restLog_means hmp hA hAmeas hV hTmeas hint hint')

/-! ### Backward transfer: Kingman over `T.symm` with the same constant -/

/-- The backward-shifted cocycle `hₙ x = restLog A V T n (T.symm^[n] x)` is subadditive over
`T.symm`. The index juggle uses `T^[n] ∘ T.symm^[m+n] = T.symm^[m]` and the everywhere
subadditivity of `restLog`. -/
theorem isSubadditiveCocycle_restLog_backward {T : X ≃ᵐ X}
    {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hA : ∀ x, (A x).det ≠ 0) [NeZero d] :
    IsSubadditiveCocycle (⇑T.symm)
      (fun n x => restLog A V (⇑T) n ((⇑T.symm)^[n] x)) := by
  have hsub := isSubadditiveCocycle_restLog (T := (⇑T)) (V := V) hA
  refine ⟨fun m n x => ?_⟩
  -- `restLog` subadditivity at `(n, m, S^[m+n] x)`.
  have hstep := hsub.apply_add_le n m ((⇑T.symm)^[m + n] x)
  rw [Nat.add_comm n m] at hstep
  -- Rewrite the two shifted arguments.
  have h1 : (⇑T)^[n] ((⇑T.symm)^[m + n] x) = (⇑T.symm)^[m] x := by
    rw [show m + n = n + m by ring, Function.iterate_add_apply (⇑T.symm) n m]
    exact (Function.LeftInverse.iterate (fun y => T.apply_symm_apply y) n) ((⇑T.symm)^[m] x)
  have h2 : (⇑T.symm)^[m + n] x = (⇑T.symm)^[n] ((⇑T.symm)^[m] x) := by
    rw [show m + n = n + m by ring, Function.iterate_add_apply]
  rw [h1] at hstep
  -- `hstep : restLog (m+n) (S^[m+n]x) ≤ restLog n (S^[m+n]x) + restLog m (S^[m]x)`.
  calc restLog A V (⇑T) (m + n) ((⇑T.symm)^[m + n] x)
      ≤ restLog A V (⇑T) n ((⇑T.symm)^[m + n] x) + restLog A V (⇑T) m ((⇑T.symm)^[m] x) := hstep
    _ = restLog A V (⇑T) m ((⇑T.symm)^[m] x)
          + restLog A V (⇑T) n ((⇑T.symm)^[n] ((⇑T.symm)^[m] x)) := by rw [h2]; ring

/-- The integral of the backward-shifted cocycle equals the integral of `restLog`:
`∫ restLog n (T.symm^[n] x) ∂μ = ∫ restLog n x ∂μ` (measure preservation of `T.symm^[n]`). -/
theorem integral_restLog_backward {T : X ≃ᵐ X} (hT : MeasurePreserving T μ μ)
    [IsFiniteMeasure μ] {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hA : ∀ x, (A x).det ≠ 0) [NeZero d]
    (hAmeas : Measurable A) (hV : MeasurableSubspace V)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) (n : ℕ) :
    ∫ x, restLog A V (⇑T) n ((⇑T.symm)^[n] x) ∂μ = ∫ x, restLog A V (⇑T) n x ∂μ := by
  have hf : Integrable (fun x => restLog A V (⇑T) n x) μ :=
    integrable_restLog hT hA hAmeas hV hT.measurable hint hint' n
  have hmp : MeasurePreserving ((⇑T.symm)^[n]) μ μ := (hT.symm T).iterate n
  have haesm : AEStronglyMeasurable (fun x => restLog A V (⇑T) n x)
      (Measure.map ((⇑T.symm)^[n]) μ) := by
    rw [hmp.map_eq]; exact hf.aestronglyMeasurable
  have hmap := integral_map (μ := μ) (φ := (⇑T.symm)^[n]) hmp.aemeasurable
    (f := fun x => restLog A V (⇑T) n x) haesm
  rw [hmp.map_eq] at hmap
  exact hmap.symm

/-- **Backward transfer with the shared constant.** There is a single constant `χ_V` such that
the forward integral means converge to it, the forward normalized cocycle `(1/n) restLog n`
converges to it `μ`-a.e. (over `T`), *and* the backward normalized cocycle
`(1/n) restLog n (T.symm^[n] x)` converges to it `μ`-a.e. (over `T.symm`). The backward limit
shares the forward constant precisely because the integral means of the two cocycles coincide
(`integral_restLog_backward`) and Fekete limits are unique — this is where the means
identification `integral_restLog_backward` is essential. -/
theorem restLog_backward_kingman [IsProbabilityMeasure μ] {T : X ≃ᵐ X} (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hA : ∀ x, (A x).det ≠ 0) [NeZero d]
    (hAmeas : Measurable A) (hV : MeasurableSubspace V)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ c : ℝ,
      Tendsto (fun n : ℕ => (∫ x, restLog A V (⇑T) (n + 1) x ∂μ) / (n + 1)) atTop (𝓝 c) ∧
      (∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * restLog A V (⇑T) n x) atTop (𝓝 c)) ∧
      ∀ᵐ x ∂μ, Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ * restLog A V (⇑T) n ((⇑T.symm)^[n] x)) atTop (𝓝 c) := by
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  -- Forward Kingman with identified means: constant `c`.
  obtain ⟨c, hcmean, hcfwd⟩ := restLog_kingman hT hA hAmeas hV hint hint'
  refine ⟨c, hcmean, hcfwd, ?_⟩
  -- Backward Kingman over `T.symm`, constant `c'`.
  have hSerg : Ergodic (⇑T.symm) μ := hT.symm
  have hSmp : MeasurePreserving (⇑T.symm) μ μ := hmp.symm T
  obtain ⟨c', hc'mean, hc'bwd⟩ :=
    tendsto_kingman_ergodic_means hSerg
      (isSubadditiveCocycle_restLog_backward (T := T) (V := V) hA)
      (fun n => by
        have hf : Integrable (fun x => restLog A V (⇑T) n x) μ :=
          integrable_restLog hmp hA hAmeas hV hmp.measurable hint hint' n
        exact ((hSmp.iterate n).integrable_comp_of_integrable hf))
      (by
        -- The backward means are termwise equal to the forward means, hence bounded below.
        obtain ⟨lb, hlb⟩ := bddBelow_restLog_means (V := V) hmp hA hAmeas hV hmp.measurable
          hint hint'
        refine ⟨lb, ?_⟩
        rintro _ ⟨n, rfl⟩
        change lb ≤ (∫ x, restLog A V (⇑T) (n + 1) ((⇑T.symm)^[n + 1] x) ∂μ) / (n + 1)
        rw [integral_restLog_backward hmp hA hAmeas hV hint hint' (n + 1)]
        exact hlb ⟨n, rfl⟩)
  -- The two means sequences are termwise equal, so `c' = c`.
  have hmean_eq : (fun n : ℕ => (∫ x, restLog A V (⇑T) (n + 1) ((⇑T.symm)^[n + 1] x) ∂μ) / (n + 1))
      = fun n : ℕ => (∫ x, restLog A V (⇑T) (n + 1) x ∂μ) / (n + 1) := by
    funext n
    rw [integral_restLog_backward hmp hA hAmeas hV hint hint' (n + 1)]
  rw [hmean_eq] at hc'mean
  have hcc : c' = c := tendsto_nhds_unique hc'mean hcmean
  rw [← hcc]
  exact hc'bwd

end Kingman

end ErgodicTheory
