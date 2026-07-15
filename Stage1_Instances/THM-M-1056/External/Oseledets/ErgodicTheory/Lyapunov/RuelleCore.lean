/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Topology.Algebra.Order.LiminfLimsup
import Mathlib.Order.Filter.AtTopBot.Basic

/-!
# Deterministic core of Ruelle's spectral upper bound

This file formalises, deterministically, the analytic heart of Ruelle's argument
(Publ. IHES 50, 1979, Lemma 1.4 / Prop 1.3) for the per-vector spectral upper bound

  `limsup (1/n) log ‖Mⁿ v‖ ≤ λ⁽ʳ⁾`   for `v` in the limit slow space.

We abstract the SVD data of a sequence of operators `f n : E →ₗ E` on a finite-dimensional
real inner product space `E` by:

* a per-time orthonormal right-singular basis `e n : OrthonormalBasis (Fin d) ℝ E`;
* per-time singular values `σ n : Fin d → ℝ` (`≥ 0`);
* the defining Parseval identity
    `‖f n u‖² = Σ_j (σ n j)² · ⟪e n j, u⟫²`.

From this single identity we derive both halves of Ruelle's one-step sandwich:

* `normSq_apply_le_of_mem_span` — restricted SVD upper bound on a "slow" right-singular span;
* `singularValue_norm_proj_le_norm_apply` — SVD lower bound via a "fast" right-singular projection.

The convention here matches Ruelle's (increasing): the index set is split by a *cut* into a
"slow / low" part (small indices, small singular values) and a "fast / high" part (large indices,
large singular values).

## Main results

* `oneStep_sandwich`: the one-step two-sided estimate.  For `u` in the slow span at time `n`,
  the fast projection of `f (n+1) u` decays at the full pairwise band gap
  (`t·‖fastProj‖ ≤ b·s·‖u‖`),
  combining the slow SVD upper bound at time `n` with the fast SVD lower bound at time `n+1` through
  the one-step operator bound `b`.
* The `k`-uniform forward leakage chain.  `geometric_recursion` solves the discrete linear
  recursion `a(i+1) ≤ q·a i + c i` exactly, the analytic engine of Ruelle's Lemma 1.4
  band-distance induction (his displayed geometric-series computation).
-/

open Filter Topology
open scoped RealInnerProductSpace BigOperators

noncomputable section

namespace ErgodicTheory.RuelleCofactor

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
variable {d : ℕ}

/-- **SVD data** for a sequence of operators on a finite-dimensional real inner product space.

`e n` is the time-`n` orthonormal right-singular basis, `σ n j ≥ 0` the `j`-th singular value, and
`apply n u = f n u` the image, satisfying the Parseval identity
`‖apply n u‖² = Σ_j (σ n j)² ⟪e n j, u⟫²`. -/
structure SVDData (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E] (d : ℕ) where
  /-- The (right-singular) orthonormal basis at time `n`. -/
  e : ℕ → OrthonormalBasis (Fin d) ℝ E
  /-- The singular values at time `n`. -/
  σ : ℕ → Fin d → ℝ
  /-- Singular values are nonnegative. -/
  σ_nonneg : ∀ n j, 0 ≤ σ n j
  /-- The image of `u` under the time-`n` operator. -/
  apply : ℕ → E → E
  /-- The Parseval / SVD identity for the squared norm of the image. -/
  normSq_apply : ∀ n u,
    ‖apply n u‖ ^ 2 = ∑ j, (σ n j) ^ 2 * ⟪e n j, u⟫ ^ 2

namespace SVDData

variable (S : SVDData E d)

/-- Parseval for the orthonormal basis: `‖u‖² = Σ_j ⟪e n j, u⟫²`. -/
lemma normSq_eq (n : ℕ) (u : E) : ‖u‖ ^ 2 = ∑ j, ⟪S.e n j, u⟫ ^ 2 := by
  have := (S.e n).sum_inner_mul_inner u u
  -- `(e n).sum_inner_mul_inner` : `∑ i, ⟪u, e i⟫ * ⟪e i, u⟫ = ⟪u, u⟫`
  rw [← real_inner_self_eq_norm_sq]
  rw [← (S.e n).sum_inner_mul_inner u u]
  apply Finset.sum_congr rfl
  intro j _
  rw [real_inner_comm (S.e n j) u]
  ring

/-- **SVD upper bound on a slow span.**  If `u` lies in the span of the right-singular vectors
`e n j` with `j` in `lo` (the "slow / low" indices), and every such singular value is `≤ s`, then
`‖f n u‖ ≤ s · ‖u‖`.  Pure SVD: in the Parseval sum only the `lo`-terms survive, each bounded by
`s² ⟪e n j, u⟫²`. -/
lemma normSq_apply_le_of_mem_span (n : ℕ) (lo : Finset (Fin d)) (s : ℝ) (hs : 0 ≤ s)
    (hσ : ∀ j ∈ lo, S.σ n j ≤ s) (u : E)
    (hu : u ∈ Submodule.span ℝ (Set.range (fun j : lo => S.e n (j : Fin d)))) :
    ‖S.apply n u‖ ^ 2 ≤ s ^ 2 * ‖u‖ ^ 2 := by
  -- Components outside `lo` vanish.
  have hzero : ∀ j ∉ lo, ⟪S.e n j, u⟫ = 0 := by
    intro j hj
    -- `u` is in the span of `e n i, i ∈ lo`; `e n j` is orthogonal to each.
    refine Submodule.span_induction
      (p := fun w _ => ⟪S.e n j, w⟫ = 0) ?_ ?_ ?_ ?_ hu
    · rintro _ ⟨i, rfl⟩
      have hij : (i : Fin d) ≠ j := by
        rintro rfl; exact hj i.2
      exact (S.e n).orthonormal.2 (by simpa using hij.symm)
    · simp
    · intro x y _ _ hx hy; rw [inner_add_right, hx, hy, add_zero]
    · intro a x _ hx; rw [inner_smul_right, hx, mul_zero]
  rw [S.normSq_apply, S.normSq_eq n u]
  rw [Finset.mul_sum]
  -- Split the LHS sum over `lo` and its complement; complement terms are 0.
  have hsplit : ∑ j, (S.σ n j) ^ 2 * ⟪S.e n j, u⟫ ^ 2
      = ∑ j ∈ lo, (S.σ n j) ^ 2 * ⟪S.e n j, u⟫ ^ 2 := by
    rw [← Finset.sum_filter_add_sum_filter_not Finset.univ (· ∈ lo)]
    have : ∑ j ∈ Finset.univ.filter (fun j => j ∉ lo),
        (S.σ n j) ^ 2 * ⟪S.e n j, u⟫ ^ 2 = 0 := by
      apply Finset.sum_eq_zero
      intro j hj
      simp only [Finset.mem_filter] at hj
      rw [hzero j hj.2]; ring
    rw [this, add_zero]
    apply Finset.sum_congr _ (fun _ _ => rfl)
    ext j; simp
  rw [hsplit]
  -- Bound each `lo`-term, and embed RHS over univ ⊇ lo.
  have hsub : ∑ j ∈ lo, (S.σ n j) ^ 2 * ⟪S.e n j, u⟫ ^ 2
      ≤ ∑ j ∈ lo, s ^ 2 * ⟪S.e n j, u⟫ ^ 2 := by
    apply Finset.sum_le_sum
    intro j hj
    apply mul_le_mul_of_nonneg_right _ (sq_nonneg _)
    apply sq_le_sq'
    · linarith [S.σ_nonneg n j, hσ j hj, hs]
    · exact hσ j hj
  refine hsub.trans ?_
  apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ lo)
  intro j _ _
  positivity

/-- **SVD lower bound via a fast projection.**  Fix a "fast / high" index set `hi` with every
singular value there `≥ t ≥ 0`.  Let `w = Σ_{j ∈ hi} ⟪e n j, u⟫ • e n j` be the orthogonal
projection of `u` onto the fast span.  Then `t · ‖w‖ ≤ ‖f n u‖`. -/
lemma singularValue_norm_proj_le_norm_apply (n : ℕ) (hi : Finset (Fin d)) (t : ℝ) (ht : 0 ≤ t)
    (hσ : ∀ j ∈ hi, t ≤ S.σ n j) (u : E) :
    (t * ‖∑ j ∈ hi, ⟪S.e n j, u⟫ • S.e n j‖) ^ 2 ≤ ‖S.apply n u‖ ^ 2 := by
  -- `‖w‖² = Σ_{j ∈ hi} ⟪e n j, u⟫²` (orthonormality).
  have hwSq : ‖∑ j ∈ hi, ⟪S.e n j, u⟫ • S.e n j‖ ^ 2
      = ∑ j ∈ hi, ⟪S.e n j, u⟫ ^ 2 := by
    rw [← real_inner_self_eq_norm_sq, sum_inner]
    apply Finset.sum_congr rfl
    intro i hi'
    rw [inner_sum]
    rw [Finset.sum_eq_single i]
    · rw [real_inner_smul_left, real_inner_smul_right,
        real_inner_self_eq_norm_sq, (S.e n).orthonormal.1 i]
      ring
    · intro j hj hji
      rw [real_inner_smul_left, real_inner_smul_right,
        (S.e n).orthonormal.2 (by simpa using hji.symm)]
      ring
    · intro h; exact absurd hi' h
  -- Bound `t² ‖w‖²` against the `hi`-part of the Parseval sum, which is ≤ the full sum.
  rw [mul_pow, hwSq, S.normSq_apply]
  rw [Finset.mul_sum]
  calc ∑ j ∈ hi, t ^ 2 * ⟪S.e n j, u⟫ ^ 2
      ≤ ∑ j ∈ hi, (S.σ n j) ^ 2 * ⟪S.e n j, u⟫ ^ 2 := by
        apply Finset.sum_le_sum
        intro j hj
        apply mul_le_mul_of_nonneg_right _ (sq_nonneg _)
        apply sq_le_sq'
        · linarith [hσ j hj, ht]
        · exact hσ j hj
    _ ≤ ∑ j, (S.σ n j) ^ 2 * ⟪S.e n j, u⟫ ^ 2 := by
        apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ hi)
        intro j _ _; positivity

/-! ## The one-step two-sided sandwich -/

/-- The orthogonal projection of `u` onto the span of the time-`n` right-singular vectors with
index in `hi` (the "fast" band at time `n`):  `Σ_{j ∈ hi} ⟪e n j, u⟫ • e n j`. -/
def fastProj (n : ℕ) (hi : Finset (Fin d)) (u : E) : E :=
  ∑ j ∈ hi, ⟪S.e n j, u⟫ • S.e n j

/-- `‖fastProj n hi u‖² = Σ_{j ∈ hi} ⟪e n j, u⟫²` (orthonormality of `e n`). -/
lemma normSq_fastProj (n : ℕ) (hi : Finset (Fin d)) (u : E) :
    ‖S.fastProj n hi u‖ ^ 2 = ∑ j ∈ hi, ⟪S.e n j, u⟫ ^ 2 := by
  rw [fastProj, ← real_inner_self_eq_norm_sq, sum_inner]
  apply Finset.sum_congr rfl
  intro i hi'
  rw [inner_sum, Finset.sum_eq_single i]
  · rw [real_inner_smul_left, real_inner_smul_right,
      real_inner_self_eq_norm_sq, (S.e n).orthonormal.1 i]
    ring
  · intro j hj hji
    rw [real_inner_smul_left, real_inner_smul_right,
      (S.e n).orthonormal.2 (by simpa using hji.symm)]
    ring
  · intro h; exact absurd hi' h

/-- Restated lower bound in terms of `fastProj`:  `t · ‖fastProj n hi u‖ ≤ ‖f n u‖`. -/
lemma singularValue_norm_fastProj_le_norm_apply (n : ℕ) (hi : Finset (Fin d)) (t : ℝ) (ht : 0 ≤ t)
    (hσ : ∀ j ∈ hi, t ≤ S.σ n j) (u : E) :
    (t * ‖S.fastProj n hi u‖) ^ 2 ≤ ‖S.apply n u‖ ^ 2 :=
  S.singularValue_norm_proj_le_norm_apply n hi t ht hσ u

/-- **Ruelle's one-step two-sided SVD sandwich.**

Fix consecutive times `n, n+1`.  Let `u` lie in the time-`n` *slow* span (indices `lo`, each
singular value `≤ s`), and let `hi` be a *fast* band at time `n+1` (each singular value `≥ t > 0`).
Suppose the one-step operator bound `‖f (n+1) u‖ ≤ b · ‖f n u‖` holds with `b ≥ 0`.  Then the
time-`(n+1)` fast projection of `u` satisfies

    t · ‖fastProj (n+1) hi u‖  ≤  b · s · ‖u‖ .

This is the leakage at the full pairwise band gap: combining the SVD lower bound at time `n+1`
(`fastProj` term) with the SVD upper bound on the slow span at time `n` (`s‖u‖`) through the
one-step step bound `b`. -/
theorem oneStep_sandwich (n : ℕ) (lo hi : Finset (Fin d)) (s t b : ℝ)
    (hs : 0 ≤ s) (ht : 0 ≤ t) (hb : 0 ≤ b)
    (hσlo : ∀ j ∈ lo, S.σ n j ≤ s) (hσhi : ∀ j ∈ hi, t ≤ S.σ (n + 1) j)
    (u : E) (hu : u ∈ Submodule.span ℝ (Set.range (fun j : lo => S.e n (j : Fin d))))
    (hstep : ‖S.apply (n + 1) u‖ ≤ b * ‖S.apply n u‖) :
    t * ‖S.fastProj (n + 1) hi u‖ ≤ b * s * ‖u‖ := by
  -- The chain of squared inequalities:
  --   (t‖w‖)² ≤ ‖f(n+1)u‖² ≤ (b‖f n u‖)² ≤ (b·s·‖u‖)².
  have hlower : (t * ‖S.fastProj (n + 1) hi u‖) ^ 2 ≤ ‖S.apply (n + 1) u‖ ^ 2 :=
    S.singularValue_norm_fastProj_le_norm_apply (n + 1) hi t ht hσhi u
  have hstep2 : ‖S.apply (n + 1) u‖ ^ 2 ≤ (b * ‖S.apply n u‖) ^ 2 := by
    apply sq_le_sq'
    · nlinarith [norm_nonneg (S.apply (n + 1) u), norm_nonneg (S.apply n u), hstep]
    · exact hstep
  have hupper : ‖S.apply n u‖ ^ 2 ≤ s ^ 2 * ‖u‖ ^ 2 :=
    S.normSq_apply_le_of_mem_span n lo s hs hσlo u hu
  have hchain : (t * ‖S.fastProj (n + 1) hi u‖) ^ 2 ≤ (b * s * ‖u‖) ^ 2 := by
    refine hlower.trans (hstep2.trans ?_)
    have : (b * ‖S.apply n u‖) ^ 2 = b ^ 2 * ‖S.apply n u‖ ^ 2 := by ring
    rw [this]
    calc b ^ 2 * ‖S.apply n u‖ ^ 2
        ≤ b ^ 2 * (s ^ 2 * ‖u‖ ^ 2) := by
          apply mul_le_mul_of_nonneg_left hupper (sq_nonneg b)
      _ = (b * s * ‖u‖) ^ 2 := by ring
  -- Take square roots: both sides nonneg.
  have hL : 0 ≤ t * ‖S.fastProj (n + 1) hi u‖ := by positivity
  have hR : 0 ≤ b * s * ‖u‖ := by positivity
  nlinarith [hchain, hL, hR]

/-! ## The `k`-uniform forward chain (geometric recursion)

Ruelle's Lemma 1.4 controls the leakage of *slow* mass into the *fast* bands accumulated over the
window `n, n+1, …, n+k`.  Iterating the one-step sandwich along the window produces, for the
mass arriving in a fixed fast band, a *discrete linear recursion*

    a (i+1)  ≤  q · a i  +  R · ρ^i ,

whose solution is the geometric envelope below.  Here `a i` is the band-leakage budget at time
`n+i`, `q ∈ [0,1)` the one-step survival/decay factor of the gap, `R·ρ^i` the fresh mass injected at
step `i` (itself decaying at the source rate `ρ`).  This is the core analytic engine of Lemma 1.4:
the band-distance induction reduces to iterating exactly this recursion, and the resulting
geometric sum is Ruelle's displayed computation.  It is stated and proved abstractly so it can be
driven by the sandwich factors at each step. -/

/-- **Discrete geometric recursion (Grönwall-type).**  If `a (i+1) ≤ q · a i + c i` for all `i`,
with `0 ≤ q`, then for every `k`,

    a k  ≤  q^k · a 0  +  Σ_{i<k} q^{k-1-i} · c i .

This is the exact solution of Ruelle's per-step leakage recursion; the second term is the
accumulated freshly-injected mass, each contribution surviving `k-1-i` further steps at factor
`q`. -/
theorem geometric_recursion (a c : ℕ → ℝ) (q : ℝ) (hq : 0 ≤ q)
    (hrec : ∀ i, a (i + 1) ≤ q * a i + c i) (k : ℕ) :
    a k ≤ q ^ k * a 0 + ∑ i ∈ Finset.range k, q ^ (k - 1 - i) * c i := by
  induction k with
  | zero => simp
  | succ k ih =>
    -- a (k+1) ≤ q·a k + c k ≤ q·(envelope k) + c k = envelope (k+1).
    refine (hrec k).trans ?_
    have hstep : q * a k + c k
        ≤ q * (q ^ k * a 0 + ∑ i ∈ Finset.range k, q ^ (k - 1 - i) * c i) + c k := by
      have := mul_le_mul_of_nonneg_left ih hq
      linarith
    refine hstep.trans (le_of_eq ?_)
    rw [Finset.sum_range_succ]
    -- Reindex the surviving terms: each `q^{k-1-i}` gains one factor of `q`, becoming
    -- `q^{(k+1)-1-i}`.
    have hpow : ∀ i ∈ Finset.range k,
        q * (q ^ (k - 1 - i) * c i) = q ^ (k + 1 - 1 - i) * c i := by
      intro i hi
      rw [Finset.mem_range] at hi
      have : k + 1 - 1 - i = (k - 1 - i) + 1 := by omega
      rw [this, pow_succ]; ring
    rw [mul_add, Finset.mul_sum, Finset.sum_congr rfl hpow]
    have hck : q ^ (k + 1 - 1 - k) * c k = c k := by
      have : k + 1 - 1 - k = 0 := by omega
      rw [this, pow_zero, one_mul]
    rw [hck]
    ring

end SVDData

end ErgodicTheory.RuelleCofactor
