/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.Extensions.ExponentSums
import ErgodicTheory.Ergodic.Birkhoff

/-!
# The trace/determinant identity: sum of all Lyapunov exponents = ∫ log|det|

This module is purely *additive* on top of the spectrum object
`ErgodicTheory.exponents : Fin d → ℝ` and the telescoping growth rate `ErgodicTheory.gammaK`
(both in `ErgodicTheory/Lyapunov/Extensions/ExponentSums.lean` / `Spectrum.lean`). It proves the
classical
**determinant identity** of multiplicative ergodic theory: under the standing hypotheses
(`hT : Ergodic T μ`, `hA : ∀ x, (A x).det ≠ 0`, `hAmeas : Measurable A`,
`hint : IntegrableLogNorm A μ`, `hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ`, together
with `[IsProbabilityMeasure μ]`), the **sum of all Lyapunov exponents** (counted with
multiplicity) equals the **integral of `log|det|` of the generator**:

`∑ i, exponents i = ∫ x, log |(A x).det| ∂μ`.

The proof is the standard composition:

1. **Volume = product of all singular values.** The product of *all* `d` singular values of
   a matrix equals the absolute value of its determinant: `sprod A T d n x = |det(A⁽ⁿ⁾)|`.
   This is proved via the squared-singular-value/Gram-eigenvalue bridge
   (`sq_singularValues_eq_gram_eigenvalue`) and `det = ∏ eigenvalues` for the symmetric Gram
   operator (`LinearMap.IsSymmetric.det_eq_prod_eigenvalues`): `sprod_d² = det(MᵀM) =
   (det M)²`, hence `sprod_d = |det M|`.
2. **`log|det|` is an additive (Birkhoff) cocycle.** Because `det` is multiplicative
   (`Matrix.det_mul`), `log|det(A⁽ⁿ⁾)| = ∑_{k<n} log|det(A(Tᵏx))|`, i.e. the *exact* Birkhoff
   sum of `log|det A|` (the equality analogue of the submultiplicative log-norm sandwich).
3. **Birkhoff ergodic theorem.** `(1/n) log|det(A⁽ⁿ⁾)| → ∫ log|det A|` `μ`-a.e., using that
   `log|det A|` is integrable (it equals `log sprod_d` at `n = 1`, integrable by
   `integrable_logSprod`).
4. **Telescoping at `k = d`.** The same normalized quantity also converges to `Γ_d = ∑ i,
   exponents i` (`gammaK_eq_sum_top_exponents`). Uniqueness of limits gives the identity.

## Main results

* `ErgodicTheory.sprod_d_eq_abs_det` — product of all singular values = `|det|`.
* `ErgodicTheory.integrable_log_abs_det` — `log|det A| ∈ L¹(μ)`.
* `ErgodicTheory.log_abs_det_cocycle_eq_birkhoffSum` — `log|det(A⁽ⁿ⁾)|` is the Birkhoff sum of
  `log|det A|`.
* `ErgodicTheory.tendsto_log_abs_det_cocycle` — `(1/n) log|det(A⁽ⁿ⁾)| → ∑ i, exponents i` a.e.
* `ErgodicTheory.sumAllExp_eq_integral_log_abs_det` — the determinant identity
  `∑ i, exponents i = ∫ x, log |(A x).det| ∂μ`.
* `ErgodicTheory.tendsto_abs_det_cocycle_atTop_zero` — volume contraction: if the sum of all
  exponents is negative, then `|det(A⁽ⁿ⁾)| → 0` `μ`-a.e.

## References

* D. Ruelle, *Ergodic theory of differentiable dynamical systems*,
  Publ. Math. IHÉS **50** (1979), 27–58.
* M. Viana, *Lectures on Lyapunov Exponents*, Cambridge Studies in Adv. Math. **145** (2014).
-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]
variable {μ : Measure X} {T : X → X}

/-! ## Step 1: the product of all singular values is the absolute determinant -/

omit [MeasurableSpace X] [NeZero d] in
/-- **The determinant as a linear map equals the matrix determinant** for `toEuclideanLin`.
`toEuclideanLin` is `Matrix.toLin` for the standard orthonormal basis, so the determinant of
the associated endomorphism is the matrix determinant (`LinearMap.det_toLin`). -/
theorem det_toEuclideanLin (M : Matrix (Fin d) (Fin d) ℝ) :
    LinearMap.det (Matrix.toEuclideanLin M) = M.det := by
  rw [Matrix.toEuclideanLin_eq_toLin_orthonormal, LinearMap.det_toLin]

omit [MeasurableSpace X] in
/-- **Product of all singular values = `|det|`** (deterministic, every `n`, `x`).
The product of *all* `d` singular values of the cocycle iterate equals the absolute value of
its determinant. Proof: square it, use `σᵢ² = eigenvalue_i(MᵀM)`
(`sq_singularValues_eq_gram_eigenvalue`) and `det = ∏ eigenvalues` for the symmetric Gram
operator, giving `sprod_d² = det(MᵀM) = (det M)²`; then take the (nonnegative) square root.
No invertibility is required: the identity holds for every matrix (both sides are
nonnegative and have equal squares). -/
theorem sprod_d_eq_abs_det {A : X → Matrix (Fin d) (Fin d) ℝ}
    (n : ℕ) (x : X) :
    sprod A T d n x = |(cocycle A T n x).det| := by
  set M := cocycle A T n x with hM
  have hfin : Module.finrank ℝ (EuclideanSpace ℝ (Fin d)) = d := finrank_euclideanSpace_fin
  -- `sprod_d²` over `range d` rewritten as a `Fin d` product of squared singular values.
  have hsq : (sprod A T d n x) ^ 2
      = ∏ i : Fin d, (Matrix.toEuclideanLin M).singularValues (i : ℕ) ^ 2 := by
    rw [sprod, ← Finset.prod_pow]
    rw [Finset.prod_range fun i =>
      (Matrix.toEuclideanLin M).singularValues i ^ 2]
  -- Each squared singular value is the corresponding Gram eigenvalue.
  have heig : ∏ i : Fin d, (Matrix.toEuclideanLin M).singularValues (i : ℕ) ^ 2
      = ∏ i : Fin d,
          (Matrix.toEuclideanLin M).isSymmetric_adjoint_comp_self.eigenvalues hfin i := by
    refine Finset.prod_congr rfl (fun i _ => ?_)
    exact sq_singularValues_eq_gram_eigenvalue M hfin i
  -- The product of eigenvalues of the symmetric Gram operator is its determinant.
  have hdet : ∏ i : Fin d,
        (Matrix.toEuclideanLin M).isSymmetric_adjoint_comp_self.eigenvalues hfin i
      = LinearMap.det ((Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M)) := by
    let L := (Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M)
    let hL := (Matrix.toEuclideanLin M).isSymmetric_adjoint_comp_self
    let b := (hL.eigenvectorBasis hfin).toBasis
    have hdiag : L.toMatrix b b = Matrix.diagonal (hL.eigenvalues hfin) := by
      ext i j
      simp [L, b, LinearMap.toMatrix_apply, Matrix.diagonal_apply,
        hL.apply_eigenvectorBasis hfin]
      split <;> simp_all
    calc
      ∏ i : Fin d, hL.eigenvalues hfin i
          = (Matrix.diagonal (hL.eigenvalues hfin)).det := by simp
      _ = (L.toMatrix b b).det := by rw [hdiag]
      _ = LinearMap.det L := LinearMap.det_toMatrix b L
  -- The Gram operator is `toEuclideanLin (MᵀM)`, whose determinant is `(det M)²`.
  have hgram : LinearMap.det
        ((Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M))
      = (M.det) ^ 2 := by
    rw [adjoint_comp_self_eq_gram, det_toEuclideanLin, Matrix.det_mul, Matrix.det_transpose, sq]
  -- Assemble: `sprod_d² = (det M)²`.
  have hkey : (sprod A T d n x) ^ 2 = (M.det) ^ 2 := by
    rw [hsq, heig, hdet, hgram]
  -- `sprod_d ≥ 0`, so take the square root.
  have hnn : 0 ≤ sprod A T d n x :=
    Finset.prod_nonneg (fun i _ => (Matrix.toEuclideanLin M).singularValues_nonneg i)
  have habs : |sprod A T d n x| = |M.det| := by
    rw [← Real.sqrt_sq_eq_abs, ← Real.sqrt_sq_eq_abs, hkey]
  rwa [abs_of_nonneg hnn] at habs

/-! ## Step 2: `log|det(A⁽ⁿ⁾)|` is the Birkhoff sum of `log|det A|` -/

omit [MeasurableSpace X] [NeZero d] in
/-- **`log|det(A⁽ⁿ⁾)|` is an additive (Birkhoff) cocycle.** Since `det` is multiplicative
(`Matrix.det_mul`), the log of the absolute determinant of the cocycle iterate is *exactly*
the Birkhoff sum of `log|det A|` (the equality analogue of the submultiplicative log-norm
sandwich `logNorm_cocycle_le_birkhoffSum`). -/
theorem log_abs_det_cocycle_eq_birkhoffSum {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (n : ℕ) (x : X) :
    Real.log |(cocycle A T n x).det|
      = birkhoffSum T (fun y => Real.log |(A y).det|) n x := by
  induction n generalizing x with
  | zero => simp
  | succ n ih =>
    rw [cocycle_succ, Matrix.det_mul, abs_mul,
      Real.log_mul (abs_ne_zero.mpr (det_cocycle_ne_zero hA n (T x)))
        (abs_ne_zero.mpr (hA x)),
      birkhoffSum_succ', ih (T x)]
    ring

/-! ## Step 3: integrability of `log|det A|` -/

/-- **`log|det A| ∈ L¹(μ)`.** Identifying `|det A|` with the product of all singular values of
`A` (`sprod A T d 1 = |det(A⁽¹⁾)| = |det A|`), integrability follows from the integrability of
`log sprod_d` (`integrable_logSprod` at `k = d`, `n = 1`), which is dominated by the two
Furstenberg–Kesten log-norm cocycles `d·(log⁺‖A‖ + log⁺‖A⁻¹‖)`. -/
theorem integrable_log_abs_det (hT : MeasurePreserving T μ μ) [IsFiniteMeasure μ]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    Integrable (fun x => Real.log |(A x).det|) μ := by
  have hTmeas : Measurable T := hT.measurable
  have heq : (fun x => Real.log (sprod A T d 1 x))
      = fun x => Real.log |(A x).det| := by
    funext x
    rw [sprod_d_eq_abs_det 1 x, cocycle_one]
  rw [← heq]
  exact integrable_logSprod hT hA hAmeas hTmeas hint hint' (le_refl d) 1

/-! ## Step 4: the a.e. growth limit and the determinant identity -/

section Identity

variable [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)

/-- The `Fin d → Fin d` reindexing `Fin.castLE (le_refl d)` is the identity, so summing
`exponents ∘ Fin.castLE (le_refl d)` over `Fin d` is just `sumAllExp`. -/
private theorem gammaK_d_eq_sumAllExp :
    gammaK hT hA hAmeas hint hint' (le_refl d) = sumAllExp hT hA hAmeas hint hint' := by
  rw [gammaK_eq_sum_top_exponents hT hA hAmeas hint hint' (le_refl d), sumAllExp]
  exact Finset.sum_congr rfl (fun i _ => by rw [Fin.castLE_rfl, id])

/-- **The a.e. determinant growth limit.** For `μ`-a.e. `x`, the normalized log absolute
determinant of the cocycle iterate converges to the sum of all Lyapunov exponents:
`(1/n) log|det(A⁽ⁿ⁾)| → ∑ i, exponents i`. Two ingredients: the Birkhoff a.e. limit of the
additive cocycle `log|det A|` (which is `∫ log|det A|`) and the telescoping growth rate
`Γ_d = ∑ i, exponents i` (`gammaK`), tied together via `sprod_d = |det|`. This route
identifies the *limit* as the exponent sum; the *value* `∫ log|det A|` is recorded in
`sumAllExp_eq_integral_log_abs_det`. -/
theorem tendsto_log_abs_det_cocycle :
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log |(cocycle A T n x).det|) atTop
      (𝓝 (sumAllExp hT hA hAmeas hint hint')) := by
  -- The normalized `log|det(A⁽ⁿ⁾)|` equals the normalized `log sprod_d`.
  have hrw : ∀ x, (fun n : ℕ => (n : ℝ)⁻¹ * Real.log |(cocycle A T n x).det|)
      = fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T d n x) := by
    intro x
    funext n
    rw [sprod_d_eq_abs_det n x]
  filter_upwards [gammaK_tendsto hT hA hAmeas hint hint' (le_refl d)] with x hx
  rw [hrw x, ← gammaK_d_eq_sumAllExp hT hA hAmeas hint hint']
  exact hx

/-- **The determinant identity.** The sum of all Lyapunov exponents (counted with
multiplicity) equals the integral of `log|det|` of the generator:
`∑ i, exponents i = ∫ x, log |(A x).det| ∂μ`. Proved by identifying the two a.e. limits of
`(1/n) log|det(A⁽ⁿ⁾)|`: the Birkhoff limit `∫ log|det A|` (via `log_abs_det_cocycle_eq_
birkhoffSum` + the ergodic Birkhoff theorem) and the exponent sum (`tendsto_log_abs_det_
cocycle`); uniqueness of limits closes the identity. -/
theorem sumAllExp_eq_integral_log_abs_det :
    sumAllExp hT hA hAmeas hint hint' = ∫ x, Real.log |(A x).det| ∂μ := by
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  have hLint : Integrable (fun x => Real.log |(A x).det|) μ :=
    integrable_log_abs_det hmp hA hAmeas hint hint'
  -- Birkhoff a.e.: the average of the additive cocycle tends to `∫ log|det A|`.
  have hbirk : ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log |(cocycle A T n x).det|) atTop
      (𝓝 (∫ y, Real.log |(A y).det| ∂μ)) := by
    filter_upwards [tendsto_birkhoffAverage_ae_integral hT hLint] with x hx
    -- rewrite the cocycle log|det| as the Birkhoff average of `log|det A|`.
    have hcongr : ∀ n : ℕ, birkhoffAverage ℝ T (fun y => Real.log |(A y).det|) n x
        = (n : ℝ)⁻¹ * Real.log |(cocycle A T n x).det| := by
      intro n
      rw [birkhoffAverage, log_abs_det_cocycle_eq_birkhoffSum hA n x, smul_eq_mul]
    exact hx.congr hcongr
  -- Both a.e. limits exist; uniqueness gives the identity.
  obtain ⟨x, hx1, hx2⟩ :=
    (Filter.Eventually.and (tendsto_log_abs_det_cocycle hT hA hAmeas hint hint') hbirk).exists
  exact tendsto_nhds_unique hx1 hx2

/-! ## Volume contraction corollary -/

/-- **Volume contraction.** If the sum of all Lyapunov exponents is negative, then for
`μ`-a.e. `x` the absolute determinant (the volume-scaling factor) of the cocycle iterate
tends to `0`: `|det(A⁽ⁿ⁾)| → 0`. Since `(1/n) log|det(A⁽ⁿ⁾)| → ∑ exp < 0`, the log absolute
determinant tends to `-∞`, so its exponential tends to `0`. -/
theorem tendsto_abs_det_cocycle_atTop_zero
    (hneg : sumAllExp hT hA hAmeas hint hint' < 0) :
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => |(cocycle A T n x).det|) atTop (𝓝 0) := by
  filter_upwards [tendsto_log_abs_det_cocycle hT hA hAmeas hint hint'] with x hx
  -- `log|det(A⁽ⁿ⁾)| = ((1/n) log|det(A⁽ⁿ⁾)|) · n → -∞`, since the average tends to `S < 0`.
  have hprod : Tendsto
      (fun n : ℕ => ((n : ℝ)⁻¹ * Real.log |(cocycle A T n x).det|) * (n : ℝ)) atTop atBot :=
    hx.neg_mul_atTop hneg tendsto_natCast_atTop_atTop
  -- For `n ≥ 1`, the product equals `log|det(A⁽ⁿ⁾)|`.
  have hlog : Tendsto (fun n : ℕ => Real.log |(cocycle A T n x).det|) atTop atBot := by
    refine hprod.congr' ?_
    filter_upwards [eventually_ge_atTop 1] with n hn
    have hn0 : (n : ℝ) ≠ 0 := by positivity
    field_simp
  -- `|det(A⁽ⁿ⁾)| = exp (log|det(A⁽ⁿ⁾)|) → exp(-∞) = 0`.
  have hpos : ∀ n : ℕ, 0 < |(cocycle A T n x).det| :=
    fun n => abs_pos.mpr (det_cocycle_ne_zero hA n x)
  have hcongr : (fun n : ℕ => |(cocycle A T n x).det|)
      = fun n : ℕ => Real.exp (Real.log |(cocycle A T n x).det|) := by
    funext n; rw [Real.exp_log (hpos n)]
  rw [hcongr]
  exact Real.tendsto_exp_atBot.comp hlog

end Identity

end ErgodicTheory
