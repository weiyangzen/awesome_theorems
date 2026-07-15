/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.RuelleCore
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit
import ErgodicTheory.Lyapunov.Forward
import ErgodicTheory.Lyapunov.ForwardAngle
import ErgodicTheory.Lyapunov.ForwardV
import ErgodicTheory.Lyapunov.SpectrumResiduals

/-!
# The `n`-scaled forward graded overlap bound

This module provides the helper lemmas for the forward graded-overlap bound. The bound (proved
in `ForwardGradedOverlapTopGap`) states: almost everywhere, for every `δ > 0` there is a
constant `c ≥ 1` such that, eventually in `n`, for all sorted-eigenbasis indices `a` and
limit-eigenbasis indices `e`,

    |⟪b' x e, u_a(n)⟫| ≤ c · exp(−n·(max(λ_e − λ_a, 0) − δ)),

where `u_a(n) = sortedGramEigenbasis A T n x a` and `b' x e` is the limit-eigenbasis vector at
eigenvalue `exp(λ_e)`. This is the a.e. form of the graded-overlap estimate underlying the
forward Oseledets filtration.

## Main results

* `toEuclideanLin_cfc_fix_eigenvector`: the continuous functional calculus fixes an eigenvector at
  an eigenvalue where the function takes the value `1` (a general spectral fact).
* `tendsto_toEuclideanLin_apply`: continuity of `M ↦ toEuclideanLin M u` in the matrix `M`.
* `abs_inner_le_of_bandProjector_mass_bound`: the limit-transfer reduction — the overlap `|⟪w, u⟫|`
  is bounded by any eventual fast-band-mass bound, transferred through the projector limit.
* `exists_spectral_cut`: a spectrum-avoiding cut strictly between two `exp`-levels exists.

## Implementation notes

Fix `x` in the full-measure set on which all the hypotheses hold. Write `λ_a = lam0 a` and
`u_a(n) = sortedGramEigenbasis A T n x a`.

For a trivial pair `λ_e ≤ λ_a` we have `max(λ_e − λ_a, 0) = 0`, so the right-hand side is
`c · exp(nδ) ≥ 1 ≥ |⟪b'_e, u_a(n)⟫|` by Cauchy–Schwarz (both are unit vectors); the bound holds
for all `n` with `c = 1`. The content is the gap pairs `λ_e > λ_a`, where the time-`n` slow vector
`u_a(n)` has overlap with the limit fast band decaying like `exp(−n(λ_e − λ_a − δ))`. There the
proof proceeds in three steps:

1. *Gap cut.* The finitely many values `{exp(λ_j) : j < d}` form a finite set, so one may choose a
   cut `c₀` with `exp(λ_a) < c₀ < exp(λ_e)` avoiding all of them; `hident` applies at this cut.
2. *Two-time chain.* The time-`n` slow vector has fast-band mass at the time-`m` cut decaying like
   `exp(−n(λ_e − λ_a − δ))`, uniformly in `m ≥ n`. This is the analytic content packaged here as
   the hypothesis `hchain` (see below).
3. *Limit transfer.* The limit-eigenbasis vector `b'_e` at level `exp(λ_e) > c₀` is fixed by the
   limit band projector `Pinf = cfc (indicator (Ioi c₀)) (lambdaHat A T x)`. Self-adjointness of
   `Pinf` and convergence of the time-`m` band projectors to `Pinf` then bound `|⟪b'_e, u_a(n)⟫|`
   by the step-2 mass bound, with no rate needed for the vanishing term.

The finitely many pairs are combined via `eventually_all`, and `c` is the maximum of the
step-2 constants over the gap pairs (independent of `n`, `a`, `e`).

The two-time chain envelope is supplied as the hypothesis `hchain`: for a gap pair `λ_a < λ_e` and
any cut `c₀` strictly between the two `exp`-levels, the fast-band mass of the time-`n` slow
eigenvector, measured by the time-`m` band projector at `c₀`, decays like `exp(−n(λ_e − λ_a − δ))`
uniformly in `m ≥ n`. A single deterministic operator-norm step over `[n, m]` is too lossy (it
gives `exp((m − n)λ₀ − mλ_e)`, which diverges as `m → ∞` in the gap direction), so the per-step
recursion that keeps the vector in the slow cone is genuinely required.

## References

* D. Ruelle, *Ergodic theory of differentiable dynamical systems*, Publ. Math. IHÉS **50** (1979),
  27–58 (Lemma 1.4 / Proposition 1.3).
-/

open MeasureTheory Filter Topology Matrix
open scoped RealInnerProductSpace BigOperators

noncomputable section

namespace ErgodicTheory

/-! ## Deterministic helper lemmas -/

/-- **CFC fixes an arbitrary eigenvector at an eigenvalue where `f = 1`.** If `M` is Hermitian,
`toEuclideanLin M v = lam • v`, and `f lam = 1`, then `toEuclideanLin (cfc f M) v = v`.
Proof: expand `v` in the (orthonormal) eigenvector basis; the component `⟪b_j, v⟫` is nonzero only
for eigenvalues `eigenvalues j = lam` (eigenvectors at distinct eigenvalues are orthogonal because
`M` is self-adjoint), and there `f (eigenvalues j) = f lam = 1`. -/
theorem toEuclideanLin_cfc_fix_eigenvector {d : ℕ} [NeZero d] (M : Matrix (Fin d) (Fin d) ℝ)
    (hM : M.IsHermitian) (f : ℝ → ℝ) (v : EuclideanSpace ℝ (Fin d)) {lam : ℝ}
    (hev : Matrix.toEuclideanLin M v = lam • v) (hf : f lam = 1) :
    Matrix.toEuclideanLin (cfc f M) v = v := by
  classical
  -- expand v in the eigenbasis: v = ∑ i, ⟪b i, v⟫ • b i
  have hexp : ∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ) • hM.eigenvectorBasis i = v :=
    hM.eigenvectorBasis.sum_repr' v
  -- componentwise: if ⟪b j, v⟫ ≠ 0 then eigenvalues j = lam.
  have hcomp : ∀ j, (inner ℝ (hM.eigenvectorBasis j) v : ℝ) ≠ 0 → hM.eigenvalues j = lam := by
    intro j hj
    have hMbj : Matrix.toEuclideanLin M (hM.eigenvectorBasis j)
        = hM.eigenvalues j • (hM.eigenvectorBasis j) := by
      rw [Matrix.toLpLin_apply, hM.mulVec_eigenvectorBasis j]; rfl
    have hsa : (Matrix.toEuclideanLin M).IsSymmetric :=
      Matrix.isHermitian_iff_isSymmetric.mp hM
    have e1 : (inner ℝ (hM.eigenvectorBasis j) (Matrix.toEuclideanLin M v) : ℝ)
        = lam * (inner ℝ (hM.eigenvectorBasis j) v : ℝ) := by rw [hev, inner_smul_right]
    have e2 : (inner ℝ (Matrix.toEuclideanLin M (hM.eigenvectorBasis j)) v : ℝ)
        = hM.eigenvalues j * (inner ℝ (hM.eigenvectorBasis j) v : ℝ) := by
      rw [hMbj, inner_smul_left]; simp
    have e3 : (inner ℝ (hM.eigenvectorBasis j) (Matrix.toEuclideanLin M v) : ℝ)
        = (inner ℝ (Matrix.toEuclideanLin M (hM.eigenvectorBasis j)) v : ℝ) :=
      (hsa (hM.eigenvectorBasis j) v).symm
    have heq : lam * (inner ℝ (hM.eigenvectorBasis j) v : ℝ)
        = hM.eigenvalues j * (inner ℝ (hM.eigenvectorBasis j) v : ℝ) := by rw [← e1, e3, e2]
    exact (mul_right_cancel₀ hj heq).symm
  -- now compute cfc f M applied to v
  calc Matrix.toEuclideanLin (cfc f M) v
      = Matrix.toEuclideanLin (cfc f M)
          (∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ) • hM.eigenvectorBasis i) := by rw [hexp]
    _ = ∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ)
          • Matrix.toEuclideanLin (cfc f M) (hM.eigenvectorBasis i) := by
        rw [map_sum]; exact Finset.sum_congr rfl (fun i _ => by rw [map_smul])
    _ = ∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ) • hM.eigenvectorBasis i := by
        apply Finset.sum_congr rfl
        intro j _
        rw [toEuclideanLin_cfc_eigenvectorBasis M hM f j]
        by_cases hj : (inner ℝ (hM.eigenvectorBasis j) v : ℝ) = 0
        · rw [hj, zero_smul, zero_smul]
        · rw [hcomp j hj, hf, one_smul]
    _ = v := hexp

/-- **Continuity of matrix→vector application.** If `P_m → Pinf` (in the finite-dimensional matrix
norm) then `toEuclideanLin (P_m) u → toEuclideanLin Pinf u`. -/
theorem tendsto_toEuclideanLin_apply {d : ℕ} {P : ℕ → Matrix (Fin d) (Fin d) ℝ}
    {Pinf : Matrix (Fin d) (Fin d) ℝ} (hP : Filter.Tendsto P Filter.atTop (𝓝 Pinf))
    (u : EuclideanSpace ℝ (Fin d)) :
    Filter.Tendsto (fun m => Matrix.toEuclideanLin (P m) u) Filter.atTop
      (𝓝 (Matrix.toEuclideanLin Pinf u)) := by
  -- `M ↦ toEuclideanLin M u` is linear in `M` over a finite-dimensional domain, hence continuous.
  let L : Matrix (Fin d) (Fin d) ℝ →ₗ[ℝ] EuclideanSpace ℝ (Fin d) :=
    { toFun := fun M => Matrix.toEuclideanLin M u
      map_add' := by intro M N; simp only [map_add, LinearMap.add_apply]
      map_smul' := by intro c M; simp only [map_smul, LinearMap.smul_apply, RingHom.id_apply] }
  have hcont : Continuous fun M : Matrix (Fin d) (Fin d) ℝ => Matrix.toEuclideanLin M u :=
    L.continuous_of_finiteDimensional
  exact (hcont.tendsto Pinf).comp hP

/-- **Limit-transfer reduction (Ruelle Lemma 1.4, step 3).** Let `w` be a unit vector that is fixed
by the limit band projector `Pinf` (`toEuclideanLin Pinf w = w`), with `Pinf` self-adjoint, and
suppose the time-`m` band projectors `P m` converge to `Pinf`. If the fast-band mass
`‖toEuclideanLin (P m) u‖` is eventually bounded by `B`, then `|⟪w, u⟫| ≤ B`. (No rate is needed
for the vanishing of `Pinf − P m`.) -/
theorem abs_inner_le_of_bandProjector_mass_bound {d : ℕ}
    {P : ℕ → Matrix (Fin d) (Fin d) ℝ} {Pinf : Matrix (Fin d) (Fin d) ℝ}
    (hP : Filter.Tendsto P Filter.atTop (𝓝 Pinf)) (hPinfsa : IsSelfAdjoint Pinf)
    (w u : EuclideanSpace ℝ (Fin d)) (hwnorm : ‖w‖ ≤ 1)
    (hfix : Matrix.toEuclideanLin Pinf w = w) {B : ℝ}
    (hbound : ∀ᶠ m : ℕ in Filter.atTop, ‖Matrix.toEuclideanLin (P m) u‖ ≤ B) :
    |(inner ℝ w u : ℝ)| ≤ B := by
  -- Pinf self-adjoint ⟹ ⟪w, Pinf u⟫ = ⟪Pinf w, u⟫ = ⟪w, u⟫.
  have hPinfsym : (Matrix.toEuclideanLin Pinf).IsSymmetric := by
    exact Matrix.isHermitian_iff_isSymmetric.mp
      (Matrix.isHermitian_iff_isSelfAdjoint.mpr hPinfsa)
  have hkey : (inner ℝ w u : ℝ) = (inner ℝ w (Matrix.toEuclideanLin Pinf u) : ℝ) := by
    rw [← hPinfsym w u, hfix]
  -- ⟪w, toEuclideanLin (P m) u⟫ → ⟪w, toEuclideanLin Pinf u⟫
  have htend : Filter.Tendsto
      (fun m => (inner ℝ w (Matrix.toEuclideanLin (P m) u) : ℝ)) Filter.atTop
      (𝓝 (inner ℝ w (Matrix.toEuclideanLin Pinf u) : ℝ)) :=
    Filter.Tendsto.inner tendsto_const_nhds (tendsto_toEuclideanLin_apply hP u)
  -- |⟪w, P m u⟫| ≤ ‖P m u‖ ≤ B eventually, so the limit ⟪w, Pinf u⟫ has |·| ≤ B.
  have habs : ∀ᶠ m : ℕ in Filter.atTop,
      |(inner ℝ w (Matrix.toEuclideanLin (P m) u) : ℝ)| ≤ B := by
    filter_upwards [hbound] with m hm
    calc |(inner ℝ w (Matrix.toEuclideanLin (P m) u) : ℝ)|
        ≤ ‖w‖ * ‖Matrix.toEuclideanLin (P m) u‖ := abs_real_inner_le_norm w _
      _ ≤ 1 * B := by
          apply mul_le_mul hwnorm hm (norm_nonneg _) (by norm_num)
      _ = B := one_mul B
  have hlim : |(inner ℝ w (Matrix.toEuclideanLin Pinf u) : ℝ)| ≤ B :=
    le_of_tendsto (htend.abs) habs
  rw [hkey]; exact hlim

/-- **Gap-cut selection (Ruelle Lemma 1.4, step 1).** For two levels `lo < hi`, the open interval
`(exp lo, exp hi)` is infinite, so it contains a point `c₀` avoiding the finite spectrum
`{exp (g i) : i}`.  This supplies a spectral cut strictly between the two `exp`-levels at which the
band projector and `hident` may be evaluated. -/
theorem exists_spectral_cut {d : ℕ} (g : Fin d → ℝ) {lo hi : ℝ} (hlohi : lo < hi) :
    ∃ c₀ : ℝ, Real.exp lo < c₀ ∧ c₀ < Real.exp hi ∧ (∀ i : Fin d, Real.exp (g i) ≠ c₀) := by
  have hexp : Real.exp lo < Real.exp hi := Real.exp_lt_exp.mpr hlohi
  have hinf : (Set.Ioo (Real.exp lo) (Real.exp hi)).Infinite := Set.Ioo_infinite hexp
  have hfin : (Set.range (fun i : Fin d => Real.exp (g i))).Finite := Set.finite_range _
  obtain ⟨c₀, hc₀mem⟩ := (hinf.diff hfin).nonempty
  rw [Set.mem_diff, Set.mem_Ioo, Set.mem_range, not_exists] at hc₀mem
  exact ⟨c₀, hc₀mem.1.1, hc₀mem.1.2, hc₀mem.2⟩

end ErgodicTheory
