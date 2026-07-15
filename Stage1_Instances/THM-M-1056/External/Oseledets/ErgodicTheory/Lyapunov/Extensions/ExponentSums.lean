/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.Extensions.Spectrum

/-!
# Sums of Lyapunov exponents, sign/vanishing, and the telescoping identity

This module is purely *additive* on top of the spectrum object
`ErgodicTheory.exponents : Fin d → ℝ` (defined in `ErgodicTheory/Lyapunov/Spectrum.lean`) — the
sorted, antitone, with-multiplicity Lyapunov spectrum of an ergodic, invertible,
log-integrable matrix cocycle (standing hypotheses `hT : Ergodic T μ`,
`hA : ∀ x, (A x).det ≠ 0`, `hAmeas : Measurable A`, `hint : IntegrableLogNorm A μ`,
`hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ`, together with `[IsProbabilityMeasure μ]`).

It records three things requested as additive extensions:

* **Exponent sums** (`sumPosExp`, `sumNonnegExp`, `sumNegExp`, `sumAllExp`): the sums of the
  strictly positive / non-negative / strictly negative / all exponents, counted with
  multiplicity. These are plain real numbers. Because `exponents` is deterministic (it does
  not depend on the point `x`), these sums are deterministic constants; in particular they
  are trivially almost-everywhere constant, so no further ergodic argument is needed to
  identify them as a.e.-limits.
* **Sign and vanishing characterizations** (`sumPosExp_nonneg`, `sumPosExp_eq_zero_iff`,
  `sumPosExp_pos_iff`, and the dual statements for `sumNegExp`): immediate consequences of
  the definitions and the sign of the filtered summands.
* **The telescoping identity** (`gammaK_eq_sum_top_exponents`): the genuine ergodic growth
  rate `Γ_k = lim (1/n) log sprod_k` of the product of the top-`k` singular values equals the
  sum `∑_{i<k} exponents i` of the top-`k` exponents. This is the shared foundation for the
  exterior characterization and the determinant identity.

## Main definitions

* `ErgodicTheory.sumPosExp` — sum of the strictly positive exponents (with multiplicity).
* `ErgodicTheory.sumNonnegExp` — sum of the non-negative exponents (with multiplicity).
* `ErgodicTheory.sumNegExp` — sum of the strictly negative exponents (with multiplicity).
* `ErgodicTheory.sumAllExp` — sum of all exponents (with multiplicity).
* `ErgodicTheory.gammaK` — the genuine ergodic growth rate `Γ_k`, the a.e.-constant limit of
  `(1/n) log sprod_k`, packaged as a plain real via `Classical.choose`.

## Main results

* `ErgodicTheory.sumPosExp_nonneg`, `ErgodicTheory.sumPosExp_eq_zero_iff`,
  `ErgodicTheory.sumPosExp_pos_iff` — sign/vanishing for the positive-exponent sum.
* `ErgodicTheory.sumNegExp_nonpos`, `ErgodicTheory.sumNegExp_eq_zero_iff`,
  `ErgodicTheory.sumNegExp_neg_iff` — the dual contraction statements.
* `ErgodicTheory.gammaK_tendsto` — `gammaK k` is the a.e. limit of `(1/n) log sprod_k`.
* `ErgodicTheory.gammaK_eq_sum_top_exponents` — the telescoping identity
  `Γ_k = ∑_{i<k} exponents i`.

## References

* M. Viana, *Lectures on Lyapunov Exponents*, Cambridge Studies in Adv. Math. **145** (2014).
-/

open MeasureTheory Filter Topology

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]
variable {μ : Measure X} {T : X → X}

section Sums

variable [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)

/-- **Sum of the strictly positive Lyapunov exponents** (counted with multiplicity). It is a
plain real number; since `exponents` is deterministic this sum does not depend on the point
`x`, hence is trivially almost-everywhere constant. -/
noncomputable def sumPosExp : ℝ :=
  ∑ i ∈ Finset.univ.filter (fun i => 0 < exponents hT hA hAmeas hint hint' i),
    exponents hT hA hAmeas hint hint' i

/-- **Sum of the non-negative Lyapunov exponents** (counted with multiplicity). It is a plain
real number; since `exponents` is deterministic this sum does not depend on the point `x`,
hence is trivially almost-everywhere constant. -/
noncomputable def sumNonnegExp : ℝ :=
  ∑ i ∈ Finset.univ.filter (fun i => 0 ≤ exponents hT hA hAmeas hint hint' i),
    exponents hT hA hAmeas hint hint' i

/-- **Sum of the strictly negative Lyapunov exponents** (counted with multiplicity). It is a
plain real number; since `exponents` is deterministic this sum does not depend on the point
`x`, hence is trivially almost-everywhere constant. -/
noncomputable def sumNegExp : ℝ :=
  ∑ i ∈ Finset.univ.filter (fun i => exponents hT hA hAmeas hint hint' i < 0),
    exponents hT hA hAmeas hint hint' i

/-- **Sum of all Lyapunov exponents** (counted with multiplicity). It is a plain real number;
since `exponents` is deterministic this sum does not depend on the point `x`, hence is
trivially almost-everywhere constant. -/
noncomputable def sumAllExp : ℝ := ∑ i, exponents hT hA hAmeas hint hint' i

end Sums

/-! ## Sign and vanishing characterizations -/

section Signs

variable [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)

/-- **The positive-exponent sum is non-negative.** Every summand is strictly positive on the
filter, so the sum is `≥ 0`. -/
theorem sumPosExp_nonneg : 0 ≤ sumPosExp hT hA hAmeas hint hint' := by
  refine Finset.sum_nonneg (fun i hi => ?_)
  exact le_of_lt (Finset.mem_filter.mp hi).2

/-- **Vanishing of the positive-exponent sum.** The sum of the strictly positive exponents is
zero iff there is no positive exponent, i.e. the cocycle is non-expanding (all exponents are
`≤ 0`). -/
theorem sumPosExp_eq_zero_iff :
    sumPosExp hT hA hAmeas hint hint' = 0
      ↔ ∀ i, exponents hT hA hAmeas hint hint' i ≤ 0 := by
  rw [sumPosExp,
    Finset.sum_eq_zero_iff_of_nonneg (fun i hi => le_of_lt (Finset.mem_filter.mp hi).2)]
  constructor
  · intro h i
    by_contra hi
    exact absurd (h i (Finset.mem_filter.mpr ⟨Finset.mem_univ i, not_le.mp hi⟩))
      (ne_of_gt (not_le.mp hi))
  · intro h i hi
    exact absurd (Finset.mem_filter.mp hi).2 (not_lt.mpr (h i))

/-- **Positivity of the positive-exponent sum.** The sum of the strictly positive exponents is
strictly positive iff at least one exponent is positive. -/
theorem sumPosExp_pos_iff :
    0 < sumPosExp hT hA hAmeas hint hint'
      ↔ ∃ i, 0 < exponents hT hA hAmeas hint hint' i := by
  rw [lt_iff_le_and_ne, and_iff_right (sumPosExp_nonneg hT hA hAmeas hint hint'), ne_comm, ne_eq,
    not_iff_comm, sumPosExp_eq_zero_iff]
  simp only [not_exists, not_lt]

/-- **The negative-exponent sum is non-positive.** Every summand is strictly negative on the
filter, so the sum is `≤ 0`. -/
theorem sumNegExp_nonpos : sumNegExp hT hA hAmeas hint hint' ≤ 0 := by
  refine Finset.sum_nonpos (fun i hi => ?_)
  exact le_of_lt (Finset.mem_filter.mp hi).2

/-- **Vanishing of the negative-exponent sum.** The sum of the strictly negative exponents is
zero iff there is no negative exponent, i.e. the cocycle is non-contracting (all exponents are
`≥ 0`). -/
theorem sumNegExp_eq_zero_iff :
    sumNegExp hT hA hAmeas hint hint' = 0
      ↔ ∀ i, 0 ≤ exponents hT hA hAmeas hint hint' i := by
  rw [sumNegExp, ← neg_eq_zero, ← Finset.sum_neg_distrib,
    Finset.sum_eq_zero_iff_of_nonneg
      (fun i hi => le_of_lt (neg_pos.mpr (Finset.mem_filter.mp hi).2))]
  constructor
  · intro h i
    by_contra hi
    exact absurd (h i (Finset.mem_filter.mpr ⟨Finset.mem_univ i, not_le.mp hi⟩))
      (by simpa using ne_of_lt (not_le.mp hi))
  · intro h i hi
    exact absurd (Finset.mem_filter.mp hi).2 (not_lt.mpr (h i))

/-- **Positive-exponent sum = full exponent sum, under a nonnegative spectrum.** If every Lyapunov
exponent is nonnegative, the positive-exponent sum equals the full exponent sum: the extra
`univ`-summands (exponent `≤ 0`, hence `= 0` here) vanish.

This is a purely spectral fact about `sumPosExp`/`sumAllExp`. It generalizes the expanding case
`sumPosExp_eq_sumAllExp_of_expanding` (all exponents strictly positive) to a merely nonnegative
spectrum, and it is the step that specializes the SRB reverse inequality to the volume case
(`hspec` = nonnegative spectrum). -/
theorem sumPosExp_eq_sumAllExp_of_nonneg
    (hnn : ∀ i, 0 ≤ exponents hT hA hAmeas hint hint' i) :
    sumPosExp hT hA hAmeas hint hint' = sumAllExp hT hA hAmeas hint hint' := by
  rw [sumPosExp, sumAllExp]
  refine Finset.sum_subset (Finset.filter_subset _ _) (fun i _ hi => ?_)
  have hle : exponents hT hA hAmeas hint hint' i ≤ 0 := by
    by_contra h
    exact hi (Finset.mem_filter.mpr ⟨Finset.mem_univ i, not_le.mp h⟩)
  exact le_antisymm hle (hnn i)

/-- **Negativity of the negative-exponent sum.** The sum of the strictly negative exponents is
strictly negative iff at least one exponent is negative. -/
theorem sumNegExp_neg_iff :
    sumNegExp hT hA hAmeas hint hint' < 0
      ↔ ∃ i, exponents hT hA hAmeas hint hint' i < 0 := by
  rw [lt_iff_le_and_ne, and_iff_right (sumNegExp_nonpos hT hA hAmeas hint hint'), ne_eq,
    not_iff_comm, sumNegExp_eq_zero_iff]
  simp only [not_exists, not_lt]

end Signs

/-! ## The telescoping identity `Γ_k = ∑_{i<k} exponents i` -/

section Telescoping

variable [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)

/-- The genuine ergodic growth rate `Γ_k`, the `μ`-a.e.-constant limit of
`(1/n) log sprod_k` (the product of the top-`k` singular values), packaged as a plain real
via `Classical.choose` of `tendsto_gammaK_of_integrableLogNorm`. Defined for `k ≤ d`. -/
noncomputable def gammaK {k : ℕ} (hk : k ≤ d) : ℝ :=
  Classical.choose (tendsto_gammaK_of_integrableLogNorm hT hA hAmeas hint hint' hk)

/-- The defining a.e. limit of `gammaK`: `(1/n) log sprod_k → Γ_k` for `μ`-a.e. `x`. -/
theorem gammaK_tendsto {k : ℕ} (hk : k ≤ d) :
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T k n x)) atTop
      (𝓝 (gammaK hT hA hAmeas hint hint' hk)) :=
  Classical.choose_spec (tendsto_gammaK_of_integrableLogNorm hT hA hAmeas hint hint' hk)

/-- **The telescoping identity.** The genuine ergodic growth rate `Γ_k` of the product of the
top-`k` singular values equals the sum of the top-`k` Lyapunov exponents (with multiplicity):
`Γ_k = ∑_{i<k} exponents i`. The top-`k` indices are realized as `Fin.castLE hk : Fin k → Fin d`.

Proof: `(1/n) log sprod_k = ∑_{i<k} (1/n) log σᵢ` (since `sprod_k = ∏_{i<k} σᵢ`, by
`Real.log_prod` on the positive singular values), each term converges to `exponents i` by
`exponents_tendsto_log_singularValue`, the finite sum of convergents converges to the sum of
the limits (`tendsto_finset_sum`), and the limit is identified with `Γ_k` by uniqueness of
limits against `gammaK_tendsto`. -/
theorem gammaK_eq_sum_top_exponents {k : ℕ} (hk : k ≤ d) :
    gammaK hT hA hAmeas hint hint' hk
      = ∑ i : Fin k, exponents hT hA hAmeas hint hint' (Fin.castLE hk i) := by
  -- a.e., `(1/n) log sprod_k → ∑_{i<k} exponents i`.
  have hsum : ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T k n x)) atTop
      (𝓝 (∑ i : Fin k, exponents hT hA hAmeas hint hint' (Fin.castLE hk i))) := by
    -- the per-index σ-limits, gathered over the finite index set `Fin k`
    have hσ : ∀ᵐ x ∂μ, ∀ i : Fin k, Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues (i : ℕ))) atTop
        (𝓝 (exponents hT hA hAmeas hint hint' (Fin.castLE hk i))) := by
      rw [ae_all_iff]
      intro i
      exact exponents_tendsto_log_singularValue hT hA hAmeas hint hint' (Fin.castLE hk i)
    filter_upwards [hσ] with x hx
    -- rewrite `(1/n) log sprod_k` as a finite sum of `(1/n) log σᵢ`
    have hrw : ∀ n : ℕ, (n : ℝ)⁻¹ * Real.log (sprod A T k n x)
        = ∑ i : Fin k, (n : ℝ)⁻¹ *
            Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues (i : ℕ)) := by
      intro n
      rw [sprod, Real.log_prod (fun i hi => ne_of_gt
          (singularValues_cocycle_pos hA n x (lt_of_lt_of_le (Finset.mem_range.mp hi) hk))),
        Finset.mul_sum, Finset.sum_range fun i =>
          (n : ℝ)⁻¹ * Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)]
    exact (tendsto_finset_sum Finset.univ (fun i _ => hx i)).congr (fun n => (hrw n).symm)
  obtain ⟨x, hx, hxsum⟩ := (Filter.Eventually.and (gammaK_tendsto hT hA hAmeas hint hint' hk)
    hsum).exists
  exact tendsto_nhds_unique hx hxsum

end Telescoping

end ErgodicTheory
