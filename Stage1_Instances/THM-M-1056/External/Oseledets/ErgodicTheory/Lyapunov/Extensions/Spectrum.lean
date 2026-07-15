/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit
import ErgodicTheory.Lyapunov.Extensions.Corollaries

/-!
# The full Lyapunov spectrum as a consumable object

This module packages the deterministic Lyapunov spectrum produced by
`ErgodicTheory.exists_lam_tendsto_singularValue` into a single, directly usable term: the
**sorted, with-multiplicity** exponent vector

`exponents A T hT hA hAmeas hint hint' : Fin d → ℝ`.

For an ergodic, invertible, log-integrable matrix cocycle (the standing hypotheses
`hT : Ergodic T μ`, `hA : ∀ x, (A x).det ≠ 0`, `hAmeas : Measurable A`,
`hint : IntegrableLogNorm A μ`, `hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ`,
together with `[IsProbabilityMeasure μ]`), `exponents` is the antitone `Fin d → ℝ` whose
`i`-th entry is the deterministic limit of `(1/n) log σᵢ(A⁽ⁿ⁾)`. It is the canonical
spectrum object that downstream consumers (exponent sums, the determinant identity, the
exterior characterization, …) build on, so all later statements funnel through this one
definition.

## Main definitions

* `ErgodicTheory.exponents` — the sorted, with-multiplicity Lyapunov spectrum, as a total
  `Fin d → ℝ`, obtained by `Classical.choose`-ing the `lam : ℕ → ℝ` of
  `exists_lam_tendsto_singularValue` and restricting it to `Fin d`.
* `ErgodicTheory.topExponent` — the largest exponent `exponents … 0`.

## Main results

* `ErgodicTheory.exponents_antitone` — the spectrum is antitone (largest first).
* `ErgodicTheory.exponents_tendsto_log_singularValue` — for each `i`, a.e. `x`, the normalized
  log of the `i`-th singular value of `A⁽ⁿ⁾` converges to `exponents … i`.
* `ErgodicTheory.exp_exponents_eq_eigenvalues₀_oseledetsLimit` — the eigenvalue tie:
  a.e. `x`, for every sorted index `i`, `exp (exponents … i)` is the `i`-th sorted
  eigenvalue of the Oseledets limit `Λ x`.

## References

* M. Viana, *Lectures on Lyapunov Exponents*, Cambridge Studies in Adv. Math. **145** (2014).
-/

open MeasureTheory Filter Topology

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]
variable {μ : Measure X} {T : X → X}

section Spectrum

variable [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)

/-- The chosen deterministic exponent sequence `lam : ℕ → ℝ` underlying the spectrum,
extracted from `exists_lam_tendsto_singularValue` via `Classical.choose`. It is antitone on
`[0, d)` and gives the a.e. σ-limits; both properties are recorded as `chosenLam_antitone`
and `chosenLam_tendsto`. Use `exponents` (the `Fin d → ℝ` restriction) as the public
object. -/
noncomputable def chosenLam : ℕ → ℝ :=
  Classical.choose (exists_lam_tendsto_singularValue hT hA hAmeas hint hint')

/-- The defining specification of `chosenLam`: antitonicity on `[0, d)` and the a.e.
per-singular-value σ-limit. -/
theorem chosenLam_spec :
    (∀ a b : ℕ, a ≤ b → b < d → chosenLam hT hA hAmeas hint hint' b
        ≤ chosenLam hT hA hAmeas hint hint' a) ∧
      ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
        atTop (𝓝 (chosenLam hT hA hAmeas hint hint' i)) :=
  Classical.choose_spec (exists_lam_tendsto_singularValue hT hA hAmeas hint hint')

/-- **The full sorted Lyapunov spectrum, with multiplicity, as a total `Fin d → ℝ`.**
Its `i`-th entry is the deterministic limit of `(1/n) log σᵢ(A⁽ⁿ⁾)`; the entries are
sorted in non-increasing order (largest exponent first) and each distinct exponent is
repeated according to its multiplicity. This is the canonical spectrum object. -/
noncomputable def exponents : Fin d → ℝ :=
  fun i => chosenLam hT hA hAmeas hint hint' (i : ℕ)

/-- **The spectrum is antitone**: `exponents` lists the Lyapunov exponents in
non-increasing order (largest first), counted with multiplicity. -/
theorem exponents_antitone : Antitone (exponents hT hA hAmeas hint hint') := by
  intro i j hij
  exact (chosenLam_spec hT hA hAmeas hint hint').1 (i : ℕ) (j : ℕ)
    (by exact_mod_cast hij) j.isLt

/-- **The defining σ-limit of the spectrum.** For each sorted index `i` and `μ`-a.e. `x`,
the normalized log of the `i`-th singular value of the cocycle iterate `A⁽ⁿ⁾` converges to
`exponents … i`. -/
theorem exponents_tendsto_log_singularValue (i : Fin d) :
    ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues (i : ℕ)))
      atTop (𝓝 (exponents hT hA hAmeas hint hint' i)) :=
  (chosenLam_spec hT hA hAmeas hint hint').2 (i : ℕ) i.isLt

/-- The top (largest) Lyapunov exponent, `exponents … 0`. Requires `d ≠ 0` (the index `0`
is `⟨0, _⟩ : Fin d`), which is available from `[NeZero d]`. -/
noncomputable def topExponent : ℝ :=
  exponents hT hA hAmeas hint hint' ⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩

/-- **The eigenvalue tie.** For `μ`-a.e. `x` and every sorted index `i`, the exponential
of the `i`-th Lyapunov exponent is the `i`-th sorted eigenvalue of the Oseledets limit
matrix `Λ x`: `exp (exponents … i) = eigenvalues₀ (Λ x) i`.

This couples the deterministic spectrum to the (per-point) spectral data of the Oseledets
limit, combining `oseledetsLimit_eigenvalues₀_eq` (eigenvalues of `Λ` are `e^{lamSing}`)
with the identification `lamSing A T x i = exponents … i` valid a.e. -/
theorem exp_exponents_eq_eigenvalues₀_oseledetsLimit :
    ∀ᵐ x ∂μ, ∀ (hH : (oseledetsLimit A T x).IsHermitian) (i : Fin (Fintype.card (Fin d))),
      Real.exp (exponents hT hA hAmeas hint hint'
          ⟨(i : ℕ), lt_of_lt_of_eq i.isLt (Fintype.card_fin d)⟩)
        = hH.eigenvalues₀ i := by
  -- a.e., the σ-limit holds at every index, so `lamSing A T x i = exponents … i`
  have hlam : ∀ᵐ x ∂μ, ∀ i : Fin d,
      lamSing A T x (i : ℕ) = exponents hT hA hAmeas hint hint' i := by
    rw [ae_all_iff]
    intro i
    filter_upwards [exponents_tendsto_log_singularValue hT hA hAmeas hint hint' i] with x hx
    exact lamSing_eq_of_tendsto hx
  filter_upwards [oseledetsLimit_eigenvalues₀_eq hT hA hAmeas hint hint', hlam]
    with x hx hlamx
  intro hH i
  have hid : (i : ℕ) < d := lt_of_lt_of_eq i.isLt (Fintype.card_fin d)
  rw [← hlamx ⟨(i : ℕ), hid⟩, ← hx hH i]

end Spectrum

end ErgodicTheory
