/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.LimitSlowSpaceSpectralBound

/-!
# The fast-index spectral envelope from the graded overlap bound

This module proves `vslow_bridge_bound_of_forward_graded`, which discharges the `hbridge`
hypothesis of `ErgodicTheory.limsup_le_of_mem_vslow`
(see `ErgodicTheory/Lyapunov/LimitSlowSpaceSpectralBound.lean`), instantiated at `lam := lam0`,
`g := fun x e ↦ lam0 (e : ℕ)`, `b' := b'`.

The proof consumes:
* `hslowperp` — slow orthogonality of `b'` against `vslow`;
* `hfwdN` — the `n`-scaled forward graded overlap bound;
* `hlam0` — per-index singular-exponent convergence;
* `hrev` — Ruelle's reverse cofactor bound.

It produces the fast-index `specTerm` envelope outright; the reverse-bound premise inside the
`hbridge` conclusion is introduced and ignored.

## Main results

* `ErgodicTheory.vslow_bridge_bound_of_forward_graded`: for a.e. `x`, every nonzero vector `v`
  of the
  slow subspace `vslow A T (Real.exp t) x` and every fast index `j` (one with `t < lam0 j`) satisfy
  the eventual spectral-term bound `specTerm T A n x v j ≤ Real.exp (n * (2 * t + ε))`.

## References

The reverse cofactor bound consumed as the `hrev` premise is the reverse side of Lemma 1.4 in
D. Ruelle, *Ergodic theory of differentiable dynamical systems*, Publ. Math. IHÉS 50 (1979),
27–58.
-/

open MeasureTheory Filter Topology Matrix
open scoped RealInnerProductSpace BigOperators Matrix

noncomputable section

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {μ : MeasureTheory.Measure X}
variable {d : ℕ} {T : X → X}

set_option maxHeartbeats 800000 in -- heavy elaboration; exceeds the default budget
-- the five-step assembly elaborates many `EuclideanSpace ℝ (Fin d)` inner products and
-- `sortedGramEigenbasis` index casts inside nested `filter_upwards`/`calc` blocks
/-- The `hbridge` hypothesis of `limsup_le_of_mem_vslow`, derived from the `n`-scaled forward
graded overlap bound, slow orthogonality, singular-exponent convergence, and Ruelle's reverse
cofactor bound. -/
theorem vslow_bridge_bound_of_forward_graded [MeasureTheory.IsProbabilityMeasure μ] [NeZero d]
    {A : X → Matrix (Fin d) (Fin d) ℝ}
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i)))
    (b' : X → OrthonormalBasis (Fin d) ℝ (EuclideanSpace ℝ (Fin d)))
    (hslowperp : ∀ᵐ x ∂μ, ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, ∀ e : Fin d,
      t < lam0 (e : ℕ) → inner ℝ (b' x e) v = 0)
    (hfwdN : ∀ᵐ x ∂μ, ∀ δ : ℝ, 0 < δ →
      ∃ c : ℝ, 1 ≤ c ∧ ∀ᶠ n : ℕ in Filter.atTop,
      ∀ a e : Fin d,
        |(inner ℝ (b' x e) (sortedGramEigenbasis A T n x
            ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩) : ℝ)|
          ≤ c * Real.exp (-(n : ℝ) * (max (lam0 (e : ℕ) - lam0 (a : ℕ)) 0 - δ)))
    (hrev : ∀ (S : Matrix (Fin d) (Fin d) ℝ), S * Sᵀ = 1 →
      ∀ (g : Fin d → ℝ) (c : ℝ), 1 ≤ c →
      (∀ a b : Fin d, |S a b| ≤ c * Real.exp (-(max (g b - g a) 0))) →
      ∀ i j : Fin d, |S i j| ≤ (d - 1).factorial * c ^ (d - 1) * Real.exp (-(g i - g j))) :
    ∀ᵐ x ∂μ, ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, v ≠ 0 →
      (∃ c : ℝ, 1 ≤ c ∧ ∀ᶠ n : ℕ in Filter.atTop, ∀ i e : Fin d,
        |(inner ℝ (b' x e)
            (sortedGramEigenbasis A T n x
              ⟨(i : ℕ), lt_of_lt_of_eq i.isLt (Fintype.card_fin d).symm⟩) : ℝ)|
          ≤ (d - 1).factorial * c ^ (d - 1) * Real.exp (-(lam0 (i : ℕ) - lam0 (e : ℕ)))) →
        ∀ j : Fin (Fintype.card (Fin d)), t < lam0 (j : ℕ) → ∀ ε : ℝ, 0 < ε →
          ∀ᶠ n : ℕ in Filter.atTop,
          specTerm T A n x v j ≤ Real.exp ((n : ℝ) * (2 * t + ε)) := by
  have hcard : Fintype.card (Fin d) = d := Fintype.card_fin d
  -- Intersect the (finitely many) per-index singular-limit a.e. sets.
  have hallσ : ∀ᵐ x ∂μ, ∀ j : Fin (Fintype.card (Fin d)), Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      atTop (𝓝 (lam0 (j : ℕ))) := by
    rw [MeasureTheory.ae_all_iff]
    intro j
    exact hlam0 (j : ℕ) (lt_of_lt_of_eq j.2 hcard)
  filter_upwards [hallσ, hslowperp, hfwdN] with x hσx hperpx hfwdNx
  intro t v hvmem hv _hrevconst j hjfast ε hε
  -- Choose the gradings.
  set δ : ℝ := ε / (8 * d) with hδdef
  have hdpos : (0 : ℝ) < d := by exact_mod_cast Nat.pos_of_ne_zero (NeZero.ne d)
  have hδpos : 0 < δ := by rw [hδdef]; positivity
  set δ' : ℝ := ε / 8 with hδ'def
  have hδ'pos : 0 < δ' := by rw [hδ'def]; positivity
  ------------------------------------------------------------------
  -- STEP 1: n-scaled reverse graded bound via `hrev` + packaging.
  ------------------------------------------------------------------
  obtain ⟨c, hc, hfwdn⟩ := hfwdNx δ hδpos
  -- For every eventual `n`, the reverse bound at grading `n·lam0`.
  have hrevN : ∀ᶠ n : ℕ in atTop, ∀ i e : Fin d,
      |(inner ℝ (b' x e) (sortedGramEigenbasis A T n x
          ⟨(i : ℕ), lt_of_lt_of_eq i.isLt (Fintype.card_fin d).symm⟩) : ℝ)|
        ≤ (d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1)
            * Real.exp (-((n : ℝ) * lam0 (i : ℕ) - (n : ℝ) * lam0 (e : ℕ))) := by
    filter_upwards [hfwdn, eventually_ge_atTop 1] with n hn hn1
    have hnpos : (0 : ℝ) ≤ (n : ℝ) := by positivity
    -- The time-`n` Gram eigenbasis, reindexed to `Fin d`.
    set bn : OrthonormalBasis (Fin d) ℝ (EuclideanSpace ℝ (Fin d)) :=
      (sortedGramEigenbasis A T n x).reindex (finCongr hcard) with hbn
    have hbneq : ∀ a : Fin d, bn a = sortedGramEigenbasis A T n x
        ⟨(a : ℕ), lt_of_lt_of_eq a.2 (Fintype.card_fin d).symm⟩ := by
      intro a; rw [hbn, OrthonormalBasis.reindex_apply]; congr 1
    -- The scaled grading and constant.
    set gN : Fin d → ℝ := fun e => (n : ℝ) * lam0 (e : ℕ) with hgN
    set cN : ℝ := c * Real.exp ((n : ℝ) * δ) with hcN
    have hcN1 : 1 ≤ cN := by
      rw [hcN]
      have : (1 : ℝ) ≤ Real.exp ((n : ℝ) * δ) :=
        Real.one_le_exp (by positivity)
      nlinarith [hc, this]
    -- The forward graded bound at grading `gN`, constant `cN`.
    have hfwdgN : ∀ a e : Fin d, |(inner ℝ (b' x e) (bn a) : ℝ)|
        ≤ cN * Real.exp (-(max (gN e - gN a) 0)) := by
      intro a e
      rw [hbneq a]
      refine (hn a e).trans ?_
      -- `c·exp(-n(max(lam0 e - lam0 a, 0) - δ)) ≤ cN·exp(-max(gN e - gN a, 0))`.
      rw [hcN]
      have hmaxscale : (n : ℝ) * max (lam0 (e : ℕ) - lam0 (a : ℕ)) 0
          = max (gN e - gN a) 0 := by
        rw [mul_max_of_nonneg _ _ hnpos, mul_zero, hgN]
        congr 1
        ring
      rw [mul_assoc, ← Real.exp_add]
      apply mul_le_mul_of_nonneg_left _ (le_of_lt (lt_of_lt_of_le zero_lt_one hc))
      apply Real.exp_le_exp.mpr
      have heq : -(n : ℝ) * (max (lam0 (e : ℕ) - lam0 (a : ℕ)) 0 - δ)
          = (n : ℝ) * δ + -(max (gN e - gN a) 0) := by
        rw [← hmaxscale]; ring
      linarith [heq.le, heq.ge]
    -- Apply the packaging lemma.
    have hpack := reverse_graded_overlap_bound (d := d) hrev
      (b := bn) (b' := b' x) (g := gN) cN hcN1 hfwdgN
    intro i e
    have hie := hpack i e
    rw [hbneq i] at hie
    -- Rewrite the grading difference to the n-scaled form.
    have hgdiff : gN i - gN e = (n : ℝ) * lam0 (i : ℕ) - (n : ℝ) * lam0 (e : ℕ) := by
      rw [hgN]
    rw [hcN, hgdiff] at hie
    exact hie
  ------------------------------------------------------------------
  -- STEP 2: expand `v` via Parseval, drop slow indices, bound fast.
  ------------------------------------------------------------------
  -- `t < lam0 j`, `(j : ℕ) < d`.
  have hjd : (j : ℕ) < d := lt_of_lt_of_eq j.2 hcard
  -- The overlap of `v` with the `j`-th sorted Gram eigenvector.
  have hovbound : ∀ᶠ n : ℕ in atTop,
      |(inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)|
        ≤ (d : ℝ) * ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1))
            * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) := by
    filter_upwards [hrevN] with n hrevNn
    -- Parseval expansion: `u_j(n) = Σ_e ⟪b' x e, u_j(n)⟫ • b' x e` so
    -- `⟪v, u_j(n)⟫ = Σ_e ⟪v, b' x e⟫ ⟪b' x e, u_j(n)⟫`.
    have hpars : (inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)
        = ∑ e : Fin d, (inner ℝ v (b' x e) : ℝ)
            * (inner ℝ (b' x e) (sortedGramEigenbasis A T n x j) : ℝ) :=
      ((b' x).sum_inner_mul_inner v (sortedGramEigenbasis A T n x j)).symm
    -- The `j`-index of `sortedGramEigenbasis` as a `Fin d` index.
    set jd : Fin d := ⟨(j : ℕ), hjd⟩ with hjddef
    have hju : (sortedGramEigenbasis A T n x ⟨(jd : ℕ),
        lt_of_lt_of_eq jd.isLt (Fintype.card_fin d).symm⟩)
        = sortedGramEigenbasis A T n x j := by
      congr 1
    -- Per-term bound.
    have hterm : ∀ e : Fin d, |(inner ℝ v (b' x e) : ℝ)
        * (inner ℝ (b' x e) (sortedGramEigenbasis A T n x j) : ℝ)|
          ≤ ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1))
              * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) := by
      intro e
      rw [abs_mul]
      by_cases hslow : t < lam0 (e : ℕ)
      · -- slow index: the `v`-factor vanishes.
        have hperp : (inner ℝ (b' x e) v : ℝ) = 0 := hperpx t v hvmem e hslow
        have hvperp : (inner ℝ v (b' x e) : ℝ) = 0 := by
          rw [real_inner_comm]; exact hperp
        rw [hvperp, abs_zero, zero_mul]
        positivity
      · -- fast/equal index: `lam0 e ≤ t`.
        have hle : lam0 (e : ℕ) ≤ t := not_lt.mp hslow
        have hvf : |(inner ℝ v (b' x e) : ℝ)| ≤ ‖v‖ := by
          have hcs := abs_real_inner_le_norm v (b' x e)
          rwa [(b' x).orthonormal.1 e, mul_one] at hcs
        -- the reverse bound for the eigenbasis factor (use `jd` as the `i`-index).
        have hrf := hrevNn jd e
        rw [hju] at hrf
        -- monotone in the exponent: `lam0 j - lam0 e ≥ lam0 j - t`.
        have hexpmono : Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * lam0 (e : ℕ)))
            ≤ Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) := by
          apply Real.exp_le_exp.mpr
          have hnpos : (0 : ℝ) ≤ (n : ℝ) := by positivity
          have : (n : ℝ) * lam0 (e : ℕ) ≤ (n : ℝ) * t :=
            mul_le_mul_of_nonneg_left hle hnpos
          linarith
        have hCnn :
            (0 : ℝ) ≤ (d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1) := by
          have : (0 : ℝ) ≤ c := le_of_lt (lt_of_lt_of_le zero_lt_one hc)
          positivity
        calc |(inner ℝ v (b' x e) : ℝ)|
                * |(inner ℝ (b' x e) (sortedGramEigenbasis A T n x j) : ℝ)|
            ≤ ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1)
                * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * lam0 (e : ℕ)))) := by
              apply mul_le_mul hvf hrf (abs_nonneg _) (norm_nonneg _)
          _ ≤ ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1)
                * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t))) := by
              apply mul_le_mul_of_nonneg_left _ (norm_nonneg _)
              exact mul_le_mul_of_nonneg_left hexpmono hCnn
          _ = ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1))
                * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) := by ring
    -- Sum the per-term bounds.
    rw [hpars]
    calc |∑ e : Fin d, (inner ℝ v (b' x e) : ℝ)
            * (inner ℝ (b' x e) (sortedGramEigenbasis A T n x j) : ℝ)|
        ≤ ∑ e : Fin d, |(inner ℝ v (b' x e) : ℝ)
            * (inner ℝ (b' x e) (sortedGramEigenbasis A T n x j) : ℝ)| :=
          Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ _e : Fin d,
            ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1))
              * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) :=
          Finset.sum_le_sum (fun e _ => hterm e)
      _ = (d : ℝ) * ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1))
              * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) := by
          have hcu : (Finset.univ : Finset (Fin d)).card = d := Finset.card_fin d
          rw [Finset.sum_const, nsmul_eq_mul, hcu]
          ring
  ------------------------------------------------------------------
  -- STEP 3: singular value asymptotics (no `hA`, via nonneg case split).
  ------------------------------------------------------------------
  have hσenv : ∀ᶠ n : ℕ in atTop,
      ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j) ^ 2
        ≤ Real.exp ((n : ℝ) * (2 * lam0 (j : ℕ) + 2 * δ')) := by
    have hev := (hσx j).eventually
      (gt_mem_nhds (show lam0 (j : ℕ) < lam0 (j : ℕ) + δ' by linarith))
    filter_upwards [hev, eventually_ge_atTop 1] with n hn hn1
    have hnpos : (0 : ℝ) < (n : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hn1
    set σ := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j with hσdef
    have hσnn : 0 ≤ σ := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg j
    rcases eq_or_lt_of_le hσnn with hσ0 | hσp
    · -- σ = 0: trivial.
      rw [← hσ0]; simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow]
      exact Real.exp_nonneg _
    · -- σ > 0.
      have hloglt : Real.log σ < (n : ℝ) * (lam0 (j : ℕ) + δ') := by
        have hmul : (n : ℝ) * ((n : ℝ)⁻¹ * Real.log σ)
            < (n : ℝ) * (lam0 (j : ℕ) + δ') := mul_lt_mul_of_pos_left hn hnpos
        rwa [← mul_assoc, mul_inv_cancel₀ (ne_of_gt hnpos), one_mul] at hmul
      have hσsq : σ ^ 2 = Real.exp (2 * Real.log σ) := by
        rw [mul_comm, Real.exp_mul, Real.exp_log hσp]; norm_num
      rw [hσsq]
      apply Real.exp_le_exp.mpr
      nlinarith [hloglt]
  ------------------------------------------------------------------
  -- STEP 4: assemble the envelope.
  ------------------------------------------------------------------
  -- The combined constant `K := (d·‖v‖·(d-1)!)²` (the `c^{d-1}` factor is folded in).
  -- We absorb everything with `eventually_const_le_exp` for `K·c^{2(d-1)}` against `exp(nε/4)`.
  -- First, a clean per-`n` algebraic bound from steps 2,3.
  have hcombined : ∀ᶠ n : ℕ in atTop,
      specTerm T A n x v j
        ≤ ((d : ℝ) * ‖v‖ * (d - 1).factorial * c ^ (d - 1)) ^ 2
            * Real.exp ((n : ℝ) * (2 * t + 2 * δ' + 2 * (d - 1) * δ)) := by
    filter_upwards [hovbound, hσenv] with n hov hσ
    rw [specTerm]
    -- Bound `⟪v,u_j⟫² ≤ (RHS of hov)²`.
    set σ := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j with hσdef
    set Bn : ℝ :=
      (d : ℝ) * ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1))
        * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) with hBn
    have hBnn : 0 ≤ Bn := by
      have hcnn : (0 : ℝ) ≤ c := le_of_lt (lt_of_lt_of_le zero_lt_one hc)
      rw [hBn]; positivity
    have hovsq : (inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ) ^ 2 ≤ Bn ^ 2 := by
      have habs : |(inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)| ≤ Bn := hov
      have h1 : (inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ) ^ 2
          = |(inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ)| ^ 2 := (sq_abs _).symm
      rw [h1]
      exact pow_le_pow_left₀ (abs_nonneg _) habs 2
    have hσnn2 : (0 : ℝ) ≤ σ ^ 2 := by positivity
    -- `specTerm = σ² · ⟪v,u_j⟫² ≤ exp(...)·Bn²`.
    have hstep : σ ^ 2 * (inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ) ^ 2
        ≤ Real.exp ((n : ℝ) * (2 * lam0 (j : ℕ) + 2 * δ')) * Bn ^ 2 := by
      apply mul_le_mul hσ hovsq (sq_nonneg _) (Real.exp_nonneg _)
    refine hstep.trans ?_
    -- Now collapse `exp(...)·Bn²` into `K·exp(n(2t+2δ'+2(d-1)δ))`.
    rw [hBn]
    -- Expand Bn².
    have hcnn : (0 : ℝ) ≤ c := le_of_lt (lt_of_lt_of_le zero_lt_one hc)
    set D : ℝ := (d : ℝ) * ‖v‖ * (d - 1).factorial * c ^ (d - 1) with hD
    have hpow : (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1)
        = c ^ (d - 1) * Real.exp ((n : ℝ) * δ * ((d : ℝ) - 1)) := by
      rw [mul_pow, ← Real.exp_nat_mul]
      congr 1
      have hd1 : (1 : ℝ) ≤ (d : ℝ) := by
        exact_mod_cast Nat.one_le_iff_ne_zero.mpr (NeZero.ne d)
      have : ((d - 1 : ℕ) : ℝ) = (d : ℝ) - 1 := by
        have : (1 : ℕ) ≤ d := Nat.one_le_iff_ne_zero.mpr (NeZero.ne d)
        push_cast [this]; ring
      rw [this]; ring_nf
    -- Rewrite the squared envelope as `D² · exp(...)`.
    have hsq :
        ((d : ℝ) * ‖v‖ * ((d - 1).factorial * (c * Real.exp ((n : ℝ) * δ)) ^ (d - 1))
            * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t))) ^ 2
        = D ^ 2 * Real.exp ((n : ℝ) * δ * ((d : ℝ) - 1) * 2
            + -((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t) * 2) := by
      rw [hpow]
      rw [show (d : ℝ) * ‖v‖ * ((d - 1).factorial * (c ^ (d - 1)
            * Real.exp ((n : ℝ) * δ * ((d : ℝ) - 1))))
            * Real.exp (-((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t))
          = D * Real.exp ((n : ℝ) * δ * ((d : ℝ) - 1)
              + -((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t)) by rw [hD, Real.exp_add]; ring]
      rw [mul_pow, ← Real.exp_nat_mul]
      congr 1
      push_cast
      ring_nf
    rw [hsq]
    rw [show Real.exp ((n : ℝ) * (2 * lam0 (j : ℕ) + 2 * δ'))
          * (D ^ 2 * Real.exp ((n : ℝ) * δ * ((d : ℝ) - 1) * 2
              + -((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t) * 2))
        = D ^ 2 * (Real.exp ((n : ℝ) * (2 * lam0 (j : ℕ) + 2 * δ'))
            * Real.exp ((n : ℝ) * δ * ((d : ℝ) - 1) * 2
              + -((n : ℝ) * lam0 (j : ℕ) - (n : ℝ) * t) * 2)) by ring]
    rw [← Real.exp_add]
    rw [show ((d : ℝ) * ‖v‖ * (d - 1).factorial * c ^ (d - 1)) ^ 2 = D ^ 2 by rw [hD]]
    apply le_of_eq
    congr 1
    apply Real.exp_eq_exp.mpr
    ring
  ------------------------------------------------------------------
  -- STEP 5: absorb the constant and the residual exponent slack into `exp(n(2t+ε))`.
  ------------------------------------------------------------------
  -- `2δ' + 2(d-1)δ ≤ ε/2`:  2δ' = ε/4;  2(d-1)δ = 2(d-1)·ε/(8d) ≤ ε/4.
  have hslack : 2 * δ' + 2 * (d - 1) * δ ≤ ε / 2 := by
    have hδ'val : 2 * δ' = ε / 4 := by rw [hδ'def]; ring
    have hδval : (2 : ℝ) * (d - 1) * δ ≤ ε / 4 := by
      rw [hδdef]
      have hd1 : (d : ℝ) - 1 ≤ (d : ℝ) := by linarith
      have hd1nn : (0 : ℝ) ≤ (d : ℝ) - 1 := by
        have : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr (NeZero.ne d)
        linarith
      rw [div_eq_mul_inv, div_eq_mul_inv]
      rw [show (2 : ℝ) * ((d : ℝ) - 1) * (ε * (8 * (d : ℝ))⁻¹)
          = (((d : ℝ) - 1) / (d : ℝ)) * (ε * (1 / 4)) by
        field_simp
        ring]
      have hfrac : ((d : ℝ) - 1) / (d : ℝ) ≤ 1 := by
        rw [div_le_one hdpos]; exact hd1
      have hεq : ε * (1 / 4) = ε / 4 := by ring
      rw [hεq]
      have : (((d : ℝ) - 1) / (d : ℝ)) * (ε / 4) ≤ 1 * (ε / 4) :=
        mul_le_mul_of_nonneg_right hfrac (by positivity)
      linarith [this]
    linarith [hδ'val, hδval]
  -- The constant `K := (d·‖v‖·(d-1)!·c^{d-1})²` is eventually ≤ `exp(nε/2)`.
  have hKenv := eventually_const_le_exp
    (((d : ℝ) * ‖v‖ * (d - 1).factorial * c ^ (d - 1)) ^ 2) (sq_nonneg _)
    (show (0 : ℝ) < ε / 2 by linarith)
  filter_upwards [hcombined, hKenv] with n hcomb hKn
  refine hcomb.trans ?_
  have hnpos : (0 : ℝ) ≤ (n : ℝ) := by positivity
  calc ((d : ℝ) * ‖v‖ * (d - 1).factorial * c ^ (d - 1)) ^ 2
          * Real.exp ((n : ℝ) * (2 * t + 2 * δ' + 2 * (d - 1) * δ))
      ≤ Real.exp ((n : ℝ) * (ε / 2))
          * Real.exp ((n : ℝ) * (2 * t + 2 * δ' + 2 * (d - 1) * δ)) := by
        apply mul_le_mul_of_nonneg_right hKn (Real.exp_nonneg _)
    _ = Real.exp ((n : ℝ) * (ε / 2) + (n : ℝ) * (2 * t + 2 * δ' + 2 * (d - 1) * δ)) := by
        rw [← Real.exp_add]
    _ ≤ Real.exp ((n : ℝ) * (2 * t + ε)) := by
        apply Real.exp_le_exp.mpr
        have hcoef : (ε / 2) + (2 * t + 2 * δ' + 2 * (d - 1) * δ) ≤ 2 * t + ε := by
          linarith [hslack]
        nlinarith [hcoef, hnpos]

end ErgodicTheory
