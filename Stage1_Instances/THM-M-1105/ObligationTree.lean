import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Probability.Independence.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Haar.OfBasis

/-! Kernel-checked composition interfaces for the frozen THM-M-1105 proof architecture. -/

open Filter MeasureTheory Matrix ProbabilityTheory Set
open scoped BigOperators Topology

namespace Stage1.THM_M_1105.ObligationTree

noncomputable section

abbrev UpperTriangle (n : Nat) := {p : Fin n × Fin n // p.1 ≤ p.2}

def EmpiricalAverage
    {n : Nat} (H : Matrix (Fin (n + 1)) (Fin (n + 1)) Real)
    (hH : H.IsHermitian) (f : Real → Real) : Real :=
  (n + 1 : Real)⁻¹ * ∑ i : Fin (n + 1),
    f ((n + 1 : Real).sqrt⁻¹ * hH.eigenvalues i)

def SemicircleIntegral (f : Real → Real) : Real :=
  ∫ x in Icc (-2 : Real) 2,
    f x * ((2 * Real.pi)⁻¹ * Real.sqrt (4 - x ^ 2))

def SampleWeakConvergence
    {nΩ : Type*} [MeasurableSpace nΩ]
    (A : ∀ n : Nat, nΩ → Matrix (Fin (n + 1)) (Fin (n + 1)) Real)
    (hA_hermitian : ∀ n ω, (A n ω).IsHermitian) (ω : nΩ) : Prop :=
  ∀ f : Real → Real, Continuous f → Bornology.IsBounded (range f) →
    Tendsto (fun n ↦ EmpiricalAverage (A n ω) (hA_hermitian n ω) f)
      atTop (nhds (SemicircleIntegral f))

/-- The last analytic terminal packages the common-null-set conclusion. The argument is an open
registered obligation, not a proof of convergence. -/
theorem root_of_sample_weak_convergence
    {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ∀ n : Nat, Ω → Matrix (Fin (n + 1)) (Fin (n + 1)) Real)
    (hA_meas : ∀ n i j, Measurable (fun ω ↦ A n ω i j))
    (hA_hermitian : ∀ n ω, (A n ω).IsHermitian)
    (hA_indep : ∀ n,
      iIndepFun (fun p : UpperTriangle (n + 1) ↦ fun ω ↦ A n ω p.1.1 p.1.2) P)
    (hA_centered : ∀ n i j, ∫ ω, A n ω i j ∂P = 0)
    (hA_offdiag_variance : ∀ n (i j : Fin (n + 1)), i < j →
      ∫ ω, (A n ω i j) ^ 2 ∂P = 1)
    (hA_bounded : ∃ C : Real, 0 ≤ C ∧ ∀ n i j,
      ∀ᵐ ω ∂P, |A n ω i j| ≤ C)
    (terminal : ∀ᵐ ω ∂P, SampleWeakConvergence A hA_hermitian ω) :
    ∀ᵐ ω ∂P, ∀ f : Real → Real, Continuous f →
      Bornology.IsBounded (range f) →
      Tendsto
        (fun n : Nat ↦ (n + 1 : Real)⁻¹ * ∑ i : Fin (n + 1),
          f ((n + 1 : Real).sqrt⁻¹ * (hA_hermitian n ω).eigenvalues i))
        atTop
        (nhds (∫ x in Icc (-2 : Real) 2,
          f x * ((2 * Real.pi)⁻¹ * Real.sqrt (4 - x ^ 2)))) := by
  filter_upwards [terminal] with ω hω
  exact hω

#check root_of_sample_weak_convergence

end
end Stage1.THM_M_1105.ObligationTree
