/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.Forward
import ErgodicTheory.Lyapunov.Filtration
import ErgodicTheory.Lyapunov.GrowthFunction

/-!
# Block-rate overlap bounds against sorted Gram singular directions

This file proves the block-specific overlap decay rate consumed by the spectral split of the
Oseledets multiplicative ergodic theorem: writing `A⁽ⁿ⁾ = cocycle A T n x`,

    limsup_n (1/n) · log |⟪v, uⱼ(n)⟫| ≤ λᵢ − λ_l,

where `v` is a *slow* vector (upper Lyapunov growth `lambdaBar A T x v ≤ λᵢ`) and
`uⱼ(n) = sortedGramEigenbasis A T n x j` is a sorted Gram singular vector whose singular value
`σⱼ(n)` has exponent `λ_l`. For a fast direction (`λ_l > λᵢ`) the rate is the full multi-gap
difference `λᵢ − λ_l`, the sum of all adjacent spectral gaps between the two exponents.

Eigenvector-perturbation arguments (Davis–Kahan / sin-Θ bounds) only reach the nearest
adjacent gap, because the residual leak at a nested cut is cut-invariant. The proof here
instead goes through the sharp Gram-eigenvector cross bound
`|⟪uⱼ(n), v⟫| ≤ ‖A⁽ⁿ⁾ v‖ / σⱼ(n)`. The required slow-growth input
`limsup (1/n) log ‖A⁽ⁿ⁾ v‖ ≤ λᵢ` is not an output of the spectral split it feeds: it is the
inequality `lambdaBar A T x v ≤ λᵢ`, the defining property of membership in the limsup flag
`ErgodicTheory.vflag`, which is established strictly upstream of the overlap split. No circularity
arises.

## Main results

* `abs_inner_gramEig_le_norm_div_singularValue`: for a linear map `f` on a finite-dimensional
  real inner product space and a unit eigenvector `u` of the Gram operator `adjoint f ∘ₗ f`
  with eigenvalue `μ > 0`, every vector `v` satisfies `|⟪u, v⟫| ≤ ‖f v‖ / √μ`.
* `abs_inner_sortedGramEigenbasis_le_cocycle`: the cocycle instance
  `|⟪uⱼ(n), v⟫| ≤ ‖A⁽ⁿ⁾ v‖ / σⱼ(n)`.
* `limsup_log_div_le_of_limsup_le_of_tendsto`: if `aₙ ≤ pₙ / qₙ` eventually (all three
  sequences eventually positive), `limsup (1/n) log pₙ ≤ P`, and `(1/n) log qₙ → Q`, then
  `limsup (1/n) log aₙ ≤ P − Q`.
* `overlap_limsup_le_of_slow_growth`: the block-rate overlap bound, with the slow-growth
  hypothesis stated as a `limsup` bound.
-/

open MeasureTheory Filter Topology
open scoped Matrix InnerProductSpace Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-! ## The abstract Gram-eigenvector cross bound -/

/-- Let `f : E →ₗ[ℝ] E` be a linear map on a finite-dimensional real inner product space and
`u` a unit eigenvector of the Gram operator `adjoint f ∘ₗ f` with eigenvalue `μ > 0`
(`adjoint f (f u) = μ • u`). Then every vector `v` satisfies

    |⟪u, v⟫| ≤ ‖f v‖ / √μ.

Indeed `μ · ⟪u, v⟫ = ⟪adjoint f (f u), v⟫ = ⟪f u, f v⟫`, so Cauchy–Schwarz gives
`|⟪u, v⟫| ≤ ‖f u‖ · ‖f v‖ / μ`, and `‖f u‖² = ⟪adjoint f (f u), u⟫ = μ` for unit `u`,
so `‖f u‖ = √μ`. Pure linear algebra: no perturbation theory and no symmetry of `f` is
used. -/
theorem abs_inner_gramEig_le_norm_div_singularValue
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (f : E →ₗ[ℝ] E) {u v : E} (hu : ‖u‖ = 1) {μ : ℝ} (hμ : 0 < μ)
    (heig : (LinearMap.adjoint f) (f u) = μ • u) :
    |(inner ℝ u v : ℝ)| ≤ ‖f v‖ / Real.sqrt μ := by
  have hfu_sq : ‖f u‖ ^ 2 = μ := by
    have h1 : (inner ℝ (f u) (f u) : ℝ) = inner ℝ ((LinearMap.adjoint f) (f u)) u := by
      rw [LinearMap.adjoint_inner_left]
    rw [real_inner_self_eq_norm_sq] at h1
    rw [h1, heig, real_inner_smul_left, real_inner_self_eq_norm_sq, hu]; ring
  have hfu_nonneg : 0 ≤ ‖f u‖ := norm_nonneg _
  have hfu : ‖f u‖ = Real.sqrt μ := by
    rw [← hfu_sq, Real.sqrt_sq hfu_nonneg]
  have hsqrt_pos : 0 < Real.sqrt μ := Real.sqrt_pos.mpr hμ
  have hkey : μ * (inner ℝ u v : ℝ) = (inner ℝ (f u) (f v) : ℝ) := by
    have h1 : (inner ℝ (f u) (f v) : ℝ) = inner ℝ ((LinearMap.adjoint f) (f u)) v := by
      rw [LinearMap.adjoint_inner_left]
    rw [h1, heig, real_inner_smul_left]
  have habs : |(inner ℝ u v : ℝ)| = |(inner ℝ (f u) (f v) : ℝ)| / μ := by
    rw [eq_div_iff (ne_of_gt hμ), ← abs_of_pos hμ, ← abs_mul, mul_comm, hkey]
  rw [habs]
  have hcs : |(inner ℝ (f u) (f v) : ℝ)| ≤ ‖f u‖ * ‖f v‖ :=
    abs_real_inner_le_norm (f u) (f v)
  have hμsqrt : Real.sqrt μ * Real.sqrt μ = μ := Real.mul_self_sqrt (le_of_lt hμ)
  calc |(inner ℝ (f u) (f v) : ℝ)| / μ ≤ (‖f u‖ * ‖f v‖) / μ := by gcongr
    _ = (Real.sqrt μ * ‖f v‖) / μ := by rw [hfu]
    _ = ‖f v‖ / Real.sqrt μ := by
        rw [div_eq_div_iff (ne_of_gt hμ) (ne_of_gt hsqrt_pos)]
        nlinarith [hμsqrt, norm_nonneg (f v)]

/-! ## The per-`n` cocycle overlap bound -/

/-- For the sorted Gram singular vector `uⱼ(n) = sortedGramEigenbasis A T n x j` and any fixed
vector `v`:

    |⟪uⱼ(n), v⟫| ≤ ‖A⁽ⁿ⁾ · v‖ / σⱼ(n),

where `σⱼ(n) = (toEuclideanLin (cocycle A T n x)).singularValues j` is the `j`-th singular
value of `A⁽ⁿ⁾` and `‖A⁽ⁿ⁾ · v‖` the cocycle growth of the fixed `v`. This instantiates
`abs_inner_gramEig_le_norm_div_singularValue` at the Gram eigenvalue
`μⱼ(n) = eigenvalues₀ (gram) j = σⱼ(n)²`, so that `√(μⱼ(n)) = σⱼ(n)`. -/
theorem abs_inner_sortedGramEigenbasis_le_cocycle [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X)
    (j : Fin (Fintype.card (Fin d))) (v : EuclideanSpace ℝ (Fin d))
    (hσpos : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j) :
    |(inner ℝ (sortedGramEigenbasis A T n x j) v : ℝ)|
      ≤ ‖Matrix.toEuclideanLin (cocycle A T n x) v‖
        / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j := by
  set f := Matrix.toEuclideanLin (cocycle A T n x) with hf
  set u := sortedGramEigenbasis A T n x j with hu
  set μ := (gram_posSemidef A T n x).isHermitian.eigenvalues₀ j with hμ
  -- `μ = σⱼ²` and `√μ = σⱼ`.
  have hμsq : μ = f.singularValues j ^ 2 := by
    rw [hμ, hf]; exact gram_eigenvalues₀_eq_sq_singularValues A T n x j
  have hμpos : 0 < μ := by rw [hμsq]; positivity
  have hsqrtμ : Real.sqrt μ = f.singularValues j := by
    rw [hμsq, Real.sqrt_sq (le_of_lt hσpos)]
  -- the gram eigenpair: `adjoint f (f u) = μ • u`.
  have hadj : LinearMap.adjoint f = Matrix.toEuclideanLin (cocycle A T n x)ᵀ := by
    rw [hf]
    have h := Matrix.toEuclideanLin_conjTranspose_eq_adjoint (cocycle A T n x)
    rw [Matrix.conjTranspose_eq_transpose_of_trivial] at h
    exact h.symm
  have hgram : (LinearMap.adjoint f) ∘ₗ f = Matrix.toEuclideanLin (gram A T n x) := by
    rw [hadj, hf, gram]
    exact (Matrix.toLpLin_mul_same 2 _ _).symm
  have heig : (LinearMap.adjoint f) (f u) = μ • u := by
    have h := sortedGramEigenbasis_eigenpair A T n x j
    rw [← hgram] at h
    simpa [LinearMap.comp_apply] using h
  have hunorm : ‖u‖ = 1 := by rw [hu]; exact (sortedGramEigenbasis A T n x).orthonormal.1 j
  have hbnd := abs_inner_gramEig_le_norm_div_singularValue f (u := u) (v := v) hunorm hμpos heig
  rwa [hsqrtμ] at hbnd

/-! ## The rate-assembly lemma -/

/-- The `limsup` arithmetic behind the block rate. If `aₙ ≤ pₙ / qₙ` eventually (with
`aₙ, pₙ, qₙ` eventually positive), `limsup (1/n) log pₙ ≤ P`, and `(1/n) log qₙ → Q`, then
`limsup (1/n) log aₙ ≤ P − Q`.

Mechanism: `(1/n) log aₙ ≤ (1/n) log pₙ − (1/n) log qₙ` eventually; the `limsup` of the
right-hand side is `≤ limsup (1/n) log pₙ + limsup (−(1/n) log qₙ) = P + (−Q)` (the second
`limsup` is `−Q` since `(1/n) log qₙ → Q`). -/
theorem limsup_log_div_le_of_limsup_le_of_tendsto
    {a p q : ℕ → ℝ} {P Q : ℝ}
    (hbound : ∀ᶠ n : ℕ in atTop, a n ≤ p n / q n)
    (hapos : ∀ᶠ n : ℕ in atTop, 0 < a n)
    (hppos : ∀ᶠ n : ℕ in atTop, 0 < p n)
    (hqpos : ∀ᶠ n : ℕ in atTop, 0 < q n)
    (hPlim : limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (p n)) atTop ≤ P)
    (hPbdd : IsBoundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (p n)))
    (hPcob : IsCoboundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (p n)))
    (hQtend : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (q n)) atTop (𝓝 Q))
    (hacob : IsCoboundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (a n))) :
    limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (a n)) atTop ≤ P - Q := by
  set la : ℕ → ℝ := fun n => (n : ℝ)⁻¹ * Real.log (a n) with hla
  set lp : ℕ → ℝ := fun n => (n : ℝ)⁻¹ * Real.log (p n) with hlp
  set lq : ℕ → ℝ := fun n => (n : ℝ)⁻¹ * Real.log (q n) with hlq
  -- `la n ≤ lp n - lq n` eventually.
  have hev : la ≤ᶠ[atTop] (fun n => lp n - lq n) := by
    filter_upwards [hbound, hapos, hppos, hqpos, eventually_ge_atTop 1] with n hb ha hp hq hn1
    have hninv : (0 : ℝ) ≤ (n : ℝ)⁻¹ := by positivity
    have hlogle : Real.log (a n) ≤ Real.log (p n) - Real.log (q n) := by
      have : Real.log (a n) ≤ Real.log (p n / q n) := Real.log_le_log ha hb
      rwa [Real.log_div (ne_of_gt hp) (ne_of_gt hq)] at this
    calc la n = (n : ℝ)⁻¹ * Real.log (a n) := rfl
      _ ≤ (n : ℝ)⁻¹ * (Real.log (p n) - Real.log (q n)) :=
          mul_le_mul_of_nonneg_left hlogle hninv
      _ = lp n - lq n := by rw [mul_sub]
  -- We avoid any lower bound on `lp` by an `ε`-argument: for every `ε > 0`, eventually
  -- `lq n > Q - ε`, hence `la n ≤ lp n - lq n < lp n - (Q - ε) = lp n + (ε - Q)`, and
  -- `limsup (lp + const) = limsup lp + const ≤ P + (ε - Q)`. Then `ε → 0` gives
  -- `limsup la ≤ P - Q`.
  rw [show P - Q = P + (- Q) by ring]
  refine le_of_forall_pos_le_add (fun ε hε => ?_)
  -- eventually `la n ≤ lp n + (ε - Q)`.
  have hqlow : ∀ᶠ n : ℕ in atTop, Q - ε ≤ lq n :=
    hQtend.eventually (eventually_ge_nhds (show Q - ε < Q by linarith))
  have hev2 : la ≤ᶠ[atTop] (fun n => lp n + (ε - Q)) := by
    filter_upwards [hev, hqlow] with n hn hq
    calc la n ≤ lp n - lq n := hn
      _ ≤ lp n - (Q - ε) := by linarith
      _ = lp n + (ε - Q) := by ring
  -- limsup of `lp + const`.
  have hbdd_const : IsBoundedUnder (· ≤ ·) atTop (fun n => lp n + (ε - Q)) := by
    obtain ⟨B, hB⟩ := hPbdd
    rw [eventually_map] at hB
    exact ⟨B + (ε - Q), eventually_map.mpr (by
      filter_upwards [hB] with n hn using by linarith)⟩
  have hlimsup_const : limsup (fun n => lp n + (ε - Q)) atTop = limsup lp atTop + (ε - Q) :=
    limsup_add_const atTop lp (ε - Q) hPbdd hPcob
  calc limsup la atTop ≤ limsup (fun n => lp n + (ε - Q)) atTop :=
        limsup_le_limsup hev2 hacob hbdd_const
    _ = limsup lp atTop + (ε - Q) := hlimsup_const
    _ ≤ P + (ε - Q) := by gcongr
    _ = P + (- Q) + ε := by ring

/-! ## The block-rate overlap bound from the slow-growth limsup -/

/-- The block-rate overlap bound. For the sorted Gram singular vector
`uⱼ(n) = sortedGramEigenbasis A T n x j` and a slow vector `v`, with:

* the **slow growth** `limsup (1/n) log ‖A⁽ⁿ⁾ v‖ ≤ λᵢ` — this is `lambdaBar A T x v ≤ λᵢ`,
  the defining property of `v` being slow, supplied by the limsup-flag filtration
  (`ErgodicTheory/Lyapunov/Filtration.lean`), which is strictly upstream of the overlap split;
* the **singular exponent** `(1/n) log σⱼ(n) → λ_l` (see `tendsto_log_singularValue`);

the overlap exponent obeys the block rate

    limsup (1/n) log |⟪v, uⱼ(n)⟫| ≤ λᵢ − λ_l.

The per-`n` input is `abs_inner_sortedGramEigenbasis_le_cocycle`
(`|⟪uⱼ, v⟫| ≤ ‖A⁽ⁿ⁾ v‖ / σⱼ`, sharp); the rate is assembled by
`limsup_log_div_le_of_limsup_le_of_tendsto`. -/
theorem overlap_limsup_le_of_slow_growth [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X)
    (j : Fin (Fintype.card (Fin d))) {v : EuclideanSpace ℝ (Fin d)} {lamI lamL : ℝ}
    (hσpos : ∀ᶠ n : ℕ in atTop, 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j)
    (hslow : limsup (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop ≤ lamI)
    (hslowbdd : IsBoundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖))
    (hslowcob : IsCoboundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖))
    (hsing : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j)) atTop (𝓝 lamL))
    (hvgrowpos : ∀ᶠ n : ℕ in atTop, 0 < ‖Matrix.toEuclideanLin (cocycle A T n x) v‖)
    (hovpos : ∀ᶠ n : ℕ in atTop,
      0 < |(inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)|)
    (hovcob : IsCoboundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log |(inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)|)) :
    limsup (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log |(inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)|) atTop
      ≤ lamI - lamL := by
  -- the per-`n` bound `|⟪v, uⱼ⟫| ≤ ‖A⁽ⁿ⁾v‖ / σⱼ`.
  have hbound : ∀ᶠ n : ℕ in atTop,
      |(inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)|
        ≤ ‖Matrix.toEuclideanLin (cocycle A T n x) v‖
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j := by
    filter_upwards [hσpos] with n hn
    rw [real_inner_comm]
    exact abs_inner_sortedGramEigenbasis_le_cocycle A T n x j v hn
  exact limsup_log_div_le_of_limsup_le_of_tendsto hbound hovpos hvgrowpos hσpos
    hslow hslowbdd hslowcob hsing hovcob

/-! ## The `lambdaBar` form

The slow-growth `limsup` hypothesis of `overlap_limsup_le_of_slow_growth` is, up to the
`toEuclideanCLM`/`toEuclideanLin` coercion, exactly `lambdaBar A T x v`
(`lambdaBar_eq_limsup_growthSeq` in `ErgodicTheory/Lyapunov/GrowthFunction.lean`). The connector
below restates the overlap bound with the filtration's native slow-vector hypothesis
`lambdaBar A T x v ≤ λᵢ`, making explicit that the slow growth is supplied by
`ErgodicTheory/Lyapunov/Filtration.lean` (`lambdaBar_eq_on_stratum` / `mem_vflag`), strictly
upstream of the overlap split — not by the spectral split it feeds. -/

omit [MeasurableSpace X] in
/-- The `lambdaBar` form of the slow-growth `limsup`: the cocycle map's `toEuclideanLin` and
`toEuclideanCLM` agree, so `limsup (1/n) log ‖toEuclideanLin (cocycle) v‖ = lambdaBar A T x v`. -/
theorem limsup_log_norm_cocycle_eq_lambdaBar
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    limsup (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop
      = lambdaBar A T x v := by
  rw [lambdaBar]
  have hpt : ∀ n : ℕ, Matrix.toEuclideanLin (cocycle A T n x) v
      = Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v := by
    intro n
    rw [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]; rfl
  simp_rw [hpt]

end ErgodicTheory
