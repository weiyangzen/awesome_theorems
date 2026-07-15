/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.TwoSided.Invertible
import ErgodicTheory.TwoSided.StrongExport
import ErgodicTheory.Lyapunov.Extensions.DetIdentity
import ErgodicTheory.Ergodic.Birkhoff

/-!
# Exponent reflection for the two-sided Oseledets theorem

This module establishes the **exponent
reflection** principle: the backward singular spectrum is the reflected negation of the
forward one.

The argument has two unconditional analytic inputs and one self-contained combinatorial
core:

* **Determinant identity (forward).** For any deterministic exponent sequence `lam0`
  realizing the a.e. per-index singular-value limits, the sum of the first `d` values
  equals the integral of `log|det A|`:
  `∑_{j<d} lam0 j = ∫ x, log |(A x).det| ∂μ`.  This is `sum_lam0_eq_integral_log_abs_det`,
  obtained from `ErgodicTheory.sumAllExp_eq_integral_log_abs_det` of `DetIdentity.lean` by
  identifying the limit values via uniqueness of a.e. limits.
* **Determinant identity (backward).** Applying the same to the backward system
  `(⇑T.symm, backwardGen A T)` and changing variables (`MeasurePreserving.integral_comp'`,
  `Matrix.det_nonsing_inv`, `Real.log_inv`) gives
  `∑_{j<d} mu0 j = − ∑_{j<d} lam0 j` (`sum_mu0_eq_neg_sum_lam0`).
* **Reflection combinatorics.** A pure order/counting argument
  (`reflect_of_counting_and_sum`): two antitone tuples `p, q : ℕ → ℝ` on `[0,d)` with a
  *counting bound* (`∀ a b, a + b < 0 → #{p ≤ a} + #{q ≤ b} ≤ d`) and equal-opposite sums
  (`∑ q = − ∑ p`) satisfy `q j = − p (d−1−j)` pointwise.  The counting bound is supplied
  by `ae_counting`; here every reflection corollary takes it as a
  hypothesis, so this module does **not** depend on `ae_counting`.

## Main results

* `ErgodicTheory.sum_lam0_eq_integral_log_abs_det` — forward determinant sum identity.
* `ErgodicTheory.sum_mu0_eq_neg_sum_lam0` — backward sum is the negation of the forward sum.
* `ErgodicTheory.reflect_of_counting_and_sum` — pure combinatorial reflection lemma.
* `ErgodicTheory.numExp_eq_of_counting`, `ErgodicTheory.expEnum_eq_neg_rev_of_counting` — the
  reflection corollaries (number of distinct exponents, reflected-negated enumeration), each
  consuming the counting bound as a hypothesis.
-/

open MeasureTheory Filter Topology

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-! ## The forward and backward determinant sum identities -/

section DetSum

variable [NeZero d] {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}

/-- **Forward determinant sum identity.** Any deterministic exponent sequence `lam0` that
realizes the a.e. per-index singular-value limits (e.g. the one produced by
`exists_lam_tendsto_singularValue`, exposed by `oseledets_filtration_dims`) satisfies
`∑_{j<d} lam0 j = ∫ x, log |(A x).det| ∂μ`.

Proof: the chosen spectrum `exponents` of `Spectrum.lean` realizes the same a.e. limits
(`exponents_tendsto_log_singularValue`); uniqueness of a.e. limits at a common conull
point forces `lam0 j = exponents j` for every `j < d`, so `∑_{j<d} lam0 j = sumAllExp`,
which equals the integral by `sumAllExp_eq_integral_log_abs_det`. -/
theorem sum_lam0_eq_integral_log_abs_det
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      atTop (𝓝 (lam0 i))) :
    ∑ j ∈ Finset.range d, lam0 j = ∫ x, Real.log |(A x).det| ∂μ := by
  -- Identify `lam0 j = exponents j` for each `j < d` via uniqueness of a.e. limits.
  have hpoint : ∀ j : ℕ, (hj : j < d) →
      lam0 j = exponents hT hA hAmeas hint hint' ⟨j, hj⟩ := by
    intro j hj
    obtain ⟨x, hx1, hx2⟩ :=
      (Filter.Eventually.and (hlam0 j hj)
        (exponents_tendsto_log_singularValue hT hA hAmeas hint hint' ⟨j, hj⟩)).exists
    exact tendsto_nhds_unique hx1 hx2
  -- Rewrite the range sum as a `Fin d` sum and conclude via the determinant identity.
  rw [← sumAllExp_eq_integral_log_abs_det hT hA hAmeas hint hint', sumAllExp]
  rw [Finset.sum_range fun j => lam0 j]
  exact Finset.sum_congr rfl fun i _ => hpoint (i : ℕ) i.isLt

end DetSum

section BackwardSum

variable [NeZero d] {μ : Measure X} [IsProbabilityMeasure μ] {T : X ≃ᵐ X}
    {A : X → Matrix (Fin d) (Fin d) ℝ}

omit [NeZero d] [IsProbabilityMeasure μ] in
/-- The pointwise identity `log |det (backwardGen A T x)| = − log |det (A (T.symm x))|`,
from `det (M⁻¹) = (det M)⁻¹` and `log |r⁻¹| = − log |r|`. -/
theorem log_abs_det_backwardGen (x : X) :
    Real.log |(backwardGen A T x).det| = - Real.log |(A (T.symm x)).det| := by
  rw [backwardGen, Matrix.det_nonsing_inv, Ring.inverse_eq_inv', abs_inv, Real.log_inv]

omit [NeZero d] [IsProbabilityMeasure μ] in
/-- **Backward determinant integral identity.**
`∫ x, log |det (backwardGen A T x)| ∂μ = − ∫ x, log |(A x).det| ∂μ`, via the pointwise
inverse-determinant identity and the change of variables along the measure-preserving
`T.symm`. -/
theorem integral_log_abs_det_backwardGen_eq_neg (hT : Ergodic T μ) :
    ∫ x, Real.log |(backwardGen A T x).det| ∂μ = - ∫ x, Real.log |(A x).det| ∂μ := by
  have hTm : MeasurePreserving T μ μ := hT.toMeasurePreserving
  have hS : MeasurePreserving T.symm μ μ := hTm.symm T
  calc ∫ x, Real.log |(backwardGen A T x).det| ∂μ
      = ∫ x, - Real.log |(A (T.symm x)).det| ∂μ := by
        simp_rw [log_abs_det_backwardGen]
    _ = - ∫ x, Real.log |(A (T.symm x)).det| ∂μ := integral_neg _
    _ = - ∫ y, Real.log |(A y).det| ∂μ := by
        rw [hS.integral_comp' (fun y => Real.log |(A y).det|)]

/-- **Backward determinant sum identity.** For any backward exponent sequence `mu0`
realizing the a.e. per-index singular-value limits of the *backward* cocycle
`cocycle (backwardGen A T) (⇑T.symm)`, the sum of its first `d` values is the negation of
the forward sum:
`∑_{j<d} mu0 j = − ∑_{j<d} lam0 j`. -/
theorem sum_mu0_eq_neg_sum_lam0
    (hT : Ergodic T μ) (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 mu0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      atTop (𝓝 (lam0 i)))
    (hmu0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin
          (cocycle (backwardGen A T) (⇑T.symm) n x)).singularValues i))
      atTop (𝓝 (mu0 i))) :
    ∑ j ∈ Finset.range d, mu0 j = - ∑ j ∈ Finset.range d, lam0 j := by
  have hTm : MeasurePreserving T μ μ := hT.toMeasurePreserving
  have hbd : BackwardData μ A T := backwardData_of hA hAmeas hTm hint hint'
  -- Backward sum identity from the general forward identity applied to the backward system.
  have hback : ∑ j ∈ Finset.range d, mu0 j
      = ∫ x, Real.log |(backwardGen A T x).det| ∂μ :=
    sum_lam0_eq_integral_log_abs_det (T := ⇑T.symm) hT.symm
      hbd.det_ne_zero hbd.measurable hbd.integrableLogNorm hbd.integrableLogNorm_inv mu0 hmu0
  -- Forward sum identity.
  have hfwd : ∑ j ∈ Finset.range d, lam0 j = ∫ x, Real.log |(A x).det| ∂μ :=
    sum_lam0_eq_integral_log_abs_det hT hA hAmeas hint hint' lam0 hlam0
  rw [hback, integral_log_abs_det_backwardGen_eq_neg (A := A) hT, hfwd]

end BackwardSum

/-! ## The pure combinatorial reflection lemma -/

section Combinatorics

/-- The sublevel count `#{j < d | p j ≤ a}` of a sequence `p` on `[0, d)`. -/
private noncomputable def countLe (p : ℕ → ℝ) (d : ℕ) (a : ℝ) : ℕ :=
  ((Finset.range d).filter (fun j => p j ≤ a)).card

/-- **Lower bound on the sublevel count for an antitone sequence.** If `p` is antitone on
`[0, d)` and `p k ≤ c` with `k < d`, then every index in `[k, d)` is in the sublevel set,
so the count is at least `d − k`. -/
private theorem le_countLe_of_antitone {p : ℕ → ℝ} {d : ℕ}
    (hp : ∀ a b : ℕ, a ≤ b → b < d → p b ≤ p a)
    {c : ℝ} {k : ℕ} (hpk : p k ≤ c) :
    d - k ≤ countLe p d c := by
  have hsub : Finset.Ico k d ⊆ (Finset.range d).filter (fun j => p j ≤ c) := by
    intro i hi
    rw [Finset.mem_Ico] at hi
    rw [Finset.mem_filter, Finset.mem_range]
    exact ⟨hi.2, le_trans (hp k i hi.1 hi.2) hpk⟩
  calc d - k = (Finset.Ico k d).card := (Nat.card_Ico k d).symm
    _ ≤ _ := Finset.card_le_card hsub

/-- **Sorted domination from the counting bound.** Given antitone `p, q` on `[0, d)`, the
counting bound `∀ a b, a + b < 0 → countLe p a + countLe q b ≤ d`, and an index `j < d`,
we have `−p (d − 1 − j) ≤ q j`.

If not, then `p (d − 1 − j) + q j < 0`; applying the bound at `a := p (d − 1 − j)`,
`b := q j` gives `countLe p a + countLe q b ≤ d`, while the antitone lower bounds give
`countLe p a ≥ j + 1` (indices `[d − 1 − j, d)`) and `countLe q b ≥ d − j`
(indices `[j, d)`), summing to `d + 1` — a contradiction. -/
private theorem neg_p_rev_le_q {p q : ℕ → ℝ} {d : ℕ}
    (hp : ∀ a b : ℕ, a ≤ b → b < d → p b ≤ p a)
    (hq : ∀ a b : ℕ, a ≤ b → b < d → q b ≤ q a)
    (hcount : ∀ a b : ℝ, a + b < 0 → countLe p d a + countLe q d b ≤ d)
    {j : ℕ} (hj : j < d) :
    - p (d - 1 - j) ≤ q j := by
  by_contra hlt
  rw [not_le] at hlt
  -- `hlt : q j < - p (d - 1 - j)`, i.e. `p (d-1-j) + q j < 0`.
  have hkrev : d - 1 - j < d := by omega
  have hsum : p (d - 1 - j) + q j < 0 := by linarith
  have hb := hcount (p (d - 1 - j)) (q j) hsum
  -- `countLe p (p (d-1-j)) ≥ d - (d-1-j) = j + 1`.
  have hp1 : d - (d - 1 - j) ≤ countLe p d (p (d - 1 - j)) :=
    le_countLe_of_antitone hp le_rfl
  -- `countLe q (q j) ≥ d - j`.
  have hq1 : d - j ≤ countLe q d (q j) :=
    le_countLe_of_antitone hq le_rfl
  -- `(d - (d-1-j)) + (d - j) = (j+1) + (d-j) = d+1 > d`, contradiction.
  omega

/-- **Reflection from counting bound and sum.** Let `p, q : ℕ → ℝ` be antitone on `[0, d)`.
If the counting bound `∀ a b, a + b < 0 → #{j < d | p j ≤ a} + #{j < d | q j ≤ b} ≤ d`
holds and the sums are opposite, `∑_{j<d} q j = − ∑_{j<d} p j`, then `q` is the reflected
negation of `p`: `q j = − p (d − 1 − j)` for every `j < d`.

Proof: the counting bound yields the pointwise lower bound `q j ≥ − p (d − 1 − j)`
(`neg_p_rev_le_q`); summing these and reindexing `j ↦ d − 1 − j` shows the sum of the
lower bounds equals `− ∑ p = ∑ q`, so the nonnegative slacks sum to zero, forcing equality
at every index (`Finset.sum_eq_zero_iff_of_nonneg`). -/
theorem reflect_of_counting_and_sum {p q : ℕ → ℝ} {d : ℕ}
    (hp : ∀ a b : ℕ, a ≤ b → b < d → p b ≤ p a)
    (hq : ∀ a b : ℕ, a ≤ b → b < d → q b ≤ q a)
    (hcount : ∀ a b : ℝ, a + b < 0 →
      ((Finset.range d).filter (fun j => p j ≤ a)).card
        + ((Finset.range d).filter (fun j => q j ≤ b)).card ≤ d)
    (hsum : ∑ j ∈ Finset.range d, q j = - ∑ j ∈ Finset.range d, p j) :
    ∀ j : ℕ, j < d → q j = - p (d - 1 - j) := by
  -- The pointwise lower bound.
  have hle : ∀ j ∈ Finset.range d, - p (d - 1 - j) ≤ q j := by
    intro j hj
    exact neg_p_rev_le_q hp hq hcount (Finset.mem_range.mp hj)
  -- The sum of the lower bounds equals `∑ q` (via reindexing `j ↦ d - 1 - j`).
  have hreindex : ∑ j ∈ Finset.range d, (- p (d - 1 - j)) = - ∑ j ∈ Finset.range d, p j := by
    rw [Finset.sum_range_reflect (fun j => - p j) d, ← Finset.sum_neg_distrib]
  have hsumeq : ∑ j ∈ Finset.range d, (- p (d - 1 - j)) = ∑ j ∈ Finset.range d, q j := by
    rw [hreindex, ← hsum]
  -- The slacks `q j - (- p (d-1-j)) ≥ 0` sum to zero, hence each is zero.
  have hslack : ∀ j ∈ Finset.range d, 0 ≤ q j - (- p (d - 1 - j)) :=
    fun j hj => by linarith [hle j hj]
  have hslacksum : ∑ j ∈ Finset.range d, (q j - (- p (d - 1 - j))) = 0 := by
    rw [Finset.sum_sub_distrib, hsumeq, sub_self]
  have hzero := (Finset.sum_eq_zero_iff_of_nonneg hslack).mp hslacksum
  intro j hj
  have := hzero j (Finset.mem_range.mpr hj)
  linarith

end Combinatorics

/-! ## Reflection corollaries: distinct-exponent count, enumeration, dimension formula -/

section Corollaries

/-- **Distinct backward exponents are the negated forward ones.** If `q j = − p (d − 1 − j)`
for all `j < d`, then the set of distinct values of `q` on `[0, d)` is the negation of the
set of distinct values of `p`. -/
private theorem distinctExp_eq_image_neg {p q : ℕ → ℝ} {d : ℕ}
    (hrefl : ∀ j : ℕ, j < d → q j = - p (d - 1 - j)) :
    distinctExp q d = (distinctExp p d).image Neg.neg := by
  ext r
  simp only [mem_distinctExp, Finset.mem_image]
  constructor
  · rintro ⟨j, hj, rfl⟩
    exact ⟨p (d - 1 - j), ⟨d - 1 - j, by omega, rfl⟩, by rw [hrefl j hj]⟩
  · rintro ⟨s, ⟨i, hi, rfl⟩, rfl⟩
    refine ⟨d - 1 - i, by omega, ?_⟩
    have hidx : d - 1 - (d - 1 - i) = i := by omega
    rw [hrefl (d - 1 - i) (by omega), hidx]

/-- **The number of distinct exponents is reflection-invariant.** -/
theorem numExp_eq_of_counting {p q : ℕ → ℝ} {d : ℕ}
    (hrefl : ∀ j : ℕ, j < d → q j = - p (d - 1 - j)) :
    numExp q d = numExp p d := by
  rw [numExp, numExp, distinctExp_eq_image_neg hrefl,
    Finset.card_image_of_injective _ neg_injective]

/-- **The backward distinct-exponent enumeration is the reflected negation of the forward
one.** With `q j = − p (d − 1 − j)`, the descending enumeration of `q`'s distinct values at
index `a` equals the negation of the descending enumeration of `p`'s distinct values at the
reversed index: `expEnum q d a = − expEnum p d (a.rev')`, where the index `a.rev'` lives in
`Fin (numExp p d)` after transporting along `numExp q d = numExp p d`. -/
theorem expEnum_eq_neg_rev_of_counting {p q : ℕ → ℝ} {d : ℕ}
    (hrefl : ∀ j : ℕ, j < d → q j = - p (d - 1 - j))
    (a : Fin (numExp q d)) :
    expEnum q d a
      = - expEnum p d (Fin.cast (numExp_eq_of_counting hrefl) a.rev) := by
  have hset : distinctExp q d = (distinctExp p d).image Neg.neg :=
    distinctExp_eq_image_neg hrefl
  have hcard : numExp q d = numExp p d := numExp_eq_of_counting hrefl
  -- The candidate strictly monotone enumeration of `distinctExp q d`.
  set g : Fin (numExp q d) → ℝ :=
    fun i => - (distinctExp p d).orderEmbOfFin rfl (Fin.cast hcard i).rev with hg
  -- `g` is strictly monotone.
  have hmono : StrictMono g := by
    intro x y hxy
    simp only [hg]
    rw [neg_lt_neg_iff]
    exact ((distinctExp p d).orderEmbOfFin rfl).strictMono
      (Fin.rev_lt_rev.mpr (by rwa [Fin.cast_lt_cast]))
  -- `g` lands in `distinctExp q d`.
  have hrange : ∀ i, g i ∈ distinctExp q d := by
    intro i
    rw [hset, Finset.mem_image, hg]
    exact ⟨(distinctExp p d).orderEmbOfFin rfl (Fin.cast hcard i).rev,
      (distinctExp p d).orderEmbOfFin_mem rfl _, rfl⟩
  -- Hence `g` is the ascending enumeration of `distinctExp q d`.
  have huniq : g = (distinctExp q d).orderEmbOfFin rfl :=
    Finset.orderEmbOfFin_unique rfl hrange hmono
  -- Read off both sides as evaluations of `orderEmbOfFin`.
  rw [expEnum, expEnum, ← huniq, hg]

/-- **Backward sublevel count = forward strict-superlevel count.** With the reflection
`q j = − p (d − 1 − j)`, for any threshold `t` the number of backward exponents at or below
`−t` equals the number of forward exponents at or above `t`, which is `d` minus the number
of forward exponents strictly below `t`:
`#{j < d | q j ≤ −t} = d − #{j < d | p j < t}`. -/
theorem backward_count_eq_of_counting {p q : ℕ → ℝ} {d : ℕ}
    (hrefl : ∀ j : ℕ, j < d → q j = - p (d - 1 - j)) (t : ℝ) :
    ((Finset.range d).filter (fun j => q j ≤ - t)).card
      = d - ((Finset.range d).filter (fun j => p j < t)).card := by
  -- `q j ≤ -t ↔ t ≤ p (d-1-j)`; reindex `j ↦ d-1-j` to a forward superlevel count.
  have hsuper : ((Finset.range d).filter (fun j => q j ≤ - t)).card
      = ((Finset.range d).filter (fun i => t ≤ p i)).card := by
    apply Finset.card_nbij' (fun j => d - 1 - j) (fun i => d - 1 - i)
    · intro j hj
      simp only [Finset.coe_filter, Finset.mem_range, Set.mem_setOf_eq] at hj ⊢
      refine ⟨by omega, ?_⟩
      have hq : q j ≤ -t := hj.2
      rw [hrefl j hj.1] at hq; linarith
    · intro i hi
      simp only [Finset.coe_filter, Finset.mem_range, Set.mem_setOf_eq] at hi ⊢
      refine ⟨by omega, ?_⟩
      have hidx : d - 1 - (d - 1 - i) = i := by omega
      rw [hrefl (d - 1 - i) (by omega), hidx, neg_le_neg_iff]; exact hi.2
    · intro j hj
      simp only [Finset.coe_filter, Finset.mem_range, Set.mem_setOf_eq] at hj
      change d - 1 - (d - 1 - j) = j; omega
    · intro i hi
      simp only [Finset.coe_filter, Finset.mem_range, Set.mem_setOf_eq] at hi
      change d - 1 - (d - 1 - i) = i; omega
  -- Superlevel = complement of strict sublevel within `range d`.
  rw [hsuper]
  have hcompl : (Finset.range d).filter (fun i => t ≤ p i)
      = (Finset.range d) \ (Finset.range d).filter (fun i => p i < t) := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_sdiff, Finset.mem_range, not_and, not_lt]
    constructor
    · rintro ⟨hi, hti⟩; exact ⟨hi, fun _ => hti⟩
    · rintro ⟨hi, h⟩; exact ⟨hi, h hi⟩
  rw [hcompl, Finset.card_sdiff_of_subset (Finset.filter_subset _ _), Finset.card_range]

/-- **Consecutive-exponent gap.** For consecutive distinct forward exponents
`λᵢ = expEnum p d i` and `λ_{i+1} = expEnum p d i.succ`, the forward exponents strictly
below `λᵢ` are exactly those at or below `λ_{i+1}` (no distinct value lies strictly between
two consecutive ones):
`#{j < d | p j < λᵢ} = #{j < d | p j ≤ λ_{i+1}}`. -/
theorem forward_strict_count_eq_succ {p : ℕ → ℝ} {d : ℕ}
    (i : Fin (numExp p d)) (hi : (i : ℕ) + 1 < numExp p d) :
    ((Finset.range d).filter (fun j => p j < expEnum p d i)).card
      = ((Finset.range d).filter (fun j => p j ≤ expEnum p d ⟨(i : ℕ) + 1, hi⟩)).card := by
  congr 1
  ext j
  simp only [Finset.mem_filter, Finset.mem_range, and_congr_right_iff]
  intro hj
  constructor
  · intro hlt
    -- `p j` is a distinct value `< λᵢ`, so `p j ≤ λ_{i+1}` (the largest distinct below `λᵢ`).
    obtain ⟨k, hk⟩ := exists_expEnum_eq p hj
    rw [← hk] at hlt ⊢
    -- `expEnum p d k < expEnum p d i` ⟹ `i < k` (strict antitone) ⟹ `i+1 ≤ k`
    -- ⟹ `expEnum p d k ≤ expEnum p d (i+1)` (antitone).
    have hik : i < k := by
      by_contra hle
      rw [not_lt] at hle
      exact absurd ((expEnum_strictAnti p d).antitone hle) (not_le.mpr hlt)
    have : (⟨(i : ℕ) + 1, hi⟩ : Fin (numExp p d)) ≤ k := by
      rw [Fin.le_def]; simp only; omega
    exact (expEnum_strictAnti p d).antitone this
  · intro hle
    -- `p j ≤ λ_{i+1} < λᵢ`.
    exact lt_of_le_of_lt hle (expEnum_strictAnti p d (by rw [Fin.lt_def]; simp))

end Corollaries

end ErgodicTheory
