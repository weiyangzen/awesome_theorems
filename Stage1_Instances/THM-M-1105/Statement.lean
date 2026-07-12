import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Probability.Independence.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Haar.OfBasis

open Filter MeasureTheory Matrix ProbabilityTheory Set
open scoped BigOperators Topology

namespace Stage1.THM_M_1105

/-- The upper-triangular index set of an `n` by `n` symmetric matrix. -/
abbrev UpperTriangle (n : ℕ) := {p : Fin n × Fin n // p.1 ≤ p.2}

/-- A bounded-entry, real-symmetric Wigner semicircle-law target.

The matrices are unnormalised: their off-diagonal entries have variance one, and the
`1 / sqrt n` scaling is applied when their eigenvalues are sampled.  The conclusion is almost-sure
weak convergence, expressed against every bounded continuous real test function. -/
def WignerSemicircleLaw
    {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ∀ n : ℕ, Ω → Matrix (Fin (n + 1)) (Fin (n + 1)) ℝ)
    (hA_meas : ∀ n i j, Measurable (fun ω ↦ A n ω i j))
    (hA_hermitian : ∀ n ω, (A n ω).IsHermitian)
    (hA_indep : ∀ n,
      iIndepFun (fun p : UpperTriangle (n + 1) ↦ fun ω ↦ A n ω p.1.1 p.1.2) P)
    (hA_centered : ∀ n i j, ∫ ω, A n ω i j ∂P = 0)
    (hA_offdiag_variance : ∀ n (i j : Fin (n + 1)), i < j →
      ∫ ω, (A n ω i j) ^ 2 ∂P = 1)
    (hA_bounded : ∃ C : ℝ, 0 ≤ C ∧ ∀ n i j,
      ∀ᵐ ω ∂P, |A n ω i j| ≤ C) : Prop :=
    ∀ᵐ ω ∂P, ∀ f : ℝ → ℝ, Continuous f → Bornology.IsBounded (range f) →
      Tendsto
        (fun n : ℕ ↦ (n + 1 : ℝ)⁻¹ * ∑ i : Fin (n + 1),
          f ((n + 1 : ℝ).sqrt⁻¹ * (hA_hermitian n ω).eigenvalues i))
        atTop
        (𝓝 (∫ x in Set.Icc (-2 : ℝ) 2,
          f x * ((2 * Real.pi)⁻¹ * Real.sqrt (4 - x ^ 2))))

#check WignerSemicircleLaw

end Stage1.THM_M_1105
