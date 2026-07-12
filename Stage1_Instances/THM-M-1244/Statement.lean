import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1244: exact Gaussian logarithmic Sobolev statement

This module freezes the finite-dimensional, standard-product-Gaussian form of
Gross's logarithmic Sobolev inequality. It does not prove the inequality.
-/

namespace Stage1Instances.THM_M_1244

open MeasureTheory ProbabilityTheory

/-- Euclidean space with its standard product measurable and normed structures. -/
abbrev Euclidean (n : Nat) := Fin n → ℝ

/-- The standard centered Gaussian probability measure with identity covariance. -/
noncomputable def standardGaussian (n : Nat) : Measure (Euclidean n) :=
  Measure.pi fun _ : Fin n ↦ gaussianReal 0 1

/-- The convention-safe integrand `s log s`, set to zero at `s = 0`. -/
noncomputable def xlogx (s : ℝ) : ℝ := if s = 0 then 0 else s * Real.log s

/-- Entropy of the square of a real function with respect to a measure. -/
noncomputable def entropySquare {n : Nat} (f : Euclidean n → ℝ)
    (μ : Measure (Euclidean n)) : ℝ :=
  ∫ x, xlogx (f x ^ 2) ∂μ - (∫ x, f x ^ 2 ∂μ) * Real.log (∫ x, f x ^ 2 ∂μ)

/-- The canonical finite-dimensional Gross Gaussian log-Sobolev target.

All integrability assumptions used by the displayed Bochner integrals are
explicit. `ContDiff ℝ 1` supplies the classical gradient through `fderiv`; no
positive-dimension restriction is imposed, so the zero-dimensional case is
part of the target.
-/
def GaussianLogSobolevTarget : Prop :=
  ∀ (n : Nat) (f : Euclidean n → ℝ),
    ContDiff ℝ 1 f →
    Integrable (fun x ↦ f x ^ 2) (standardGaussian n) →
    Integrable (fun x ↦ xlogx (f x ^ 2)) (standardGaussian n) →
    Integrable (fun x ↦ ‖fderiv ℝ f x‖ ^ 2) (standardGaussian n) →
    entropySquare f (standardGaussian n) ≤
      2 * ∫ x, ‖fderiv ℝ f x‖ ^ 2 ∂(standardGaussian n)

/-- Fully expanded encoding used to check the selected definitions. -/
def ExpandedTarget : Prop :=
  ∀ (n : Nat) (f : (Fin n → ℝ) → ℝ),
    ContDiff ℝ 1 f →
    Integrable (fun x ↦ f x ^ 2) (Measure.pi fun _ : Fin n ↦ gaussianReal 0 1) →
    Integrable
      (fun x ↦ if f x ^ 2 = 0 then 0 else f x ^ 2 * Real.log (f x ^ 2))
      (Measure.pi fun _ : Fin n ↦ gaussianReal 0 1) →
    Integrable (fun x ↦ ‖fderiv ℝ f x‖ ^ 2)
      (Measure.pi fun _ : Fin n ↦ gaussianReal 0 1) →
    (∫ x, (if f x ^ 2 = 0 then 0 else f x ^ 2 * Real.log (f x ^ 2))
          ∂(Measure.pi fun _ : Fin n ↦ gaussianReal 0 1)) -
        (∫ x, f x ^ 2 ∂(Measure.pi fun _ : Fin n ↦ gaussianReal 0 1)) *
          Real.log (∫ x, f x ^ 2 ∂(Measure.pi fun _ : Fin n ↦ gaussianReal 0 1)) ≤
      2 * ∫ x, ‖fderiv ℝ f x‖ ^ 2
        ∂(Measure.pi fun _ : Fin n ↦ gaussianReal 0 1)

/-- Checked definitional transport to the expanded encoding. -/
theorem gaussianLogSobolevTarget_iff_expandedTarget :
    GaussianLogSobolevTarget ↔ ExpandedTarget :=
  Iff.rfl

-- Structural mutations are elaborated and compared by `check_statement.py`.
def mutationPositiveDimensionOnly : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (f : Euclidean n → ℝ),
    ContDiff ℝ 1 f →
    Integrable (fun x ↦ f x ^ 2) (standardGaussian n) →
    Integrable (fun x ↦ xlogx (f x ^ 2)) (standardGaussian n) →
    Integrable (fun x ↦ ‖fderiv ℝ f x‖ ^ 2) (standardGaussian n) →
    entropySquare f (standardGaussian n) ≤
      2 * ∫ x, ‖fderiv ℝ f x‖ ^ 2 ∂(standardGaussian n)

def mutationRemovedEntropyIntegrability : Prop :=
  ∀ (n : Nat) (f : Euclidean n → ℝ),
    ContDiff ℝ 1 f →
    Integrable (fun x ↦ f x ^ 2) (standardGaussian n) →
    Integrable (fun x ↦ ‖fderiv ℝ f x‖ ^ 2) (standardGaussian n) →
    entropySquare f (standardGaussian n) ≤
      2 * ∫ x, ‖fderiv ℝ f x‖ ^ 2 ∂(standardGaussian n)

def mutationSharpConstantFour : Prop :=
  ∀ (n : Nat) (f : Euclidean n → ℝ),
    ContDiff ℝ 1 f →
    Integrable (fun x ↦ f x ^ 2) (standardGaussian n) →
    Integrable (fun x ↦ xlogx (f x ^ 2)) (standardGaussian n) →
    Integrable (fun x ↦ ‖fderiv ℝ f x‖ ^ 2) (standardGaussian n) →
    entropySquare f (standardGaussian n) ≤
      4 * ∫ x, ‖fderiv ℝ f x‖ ^ 2 ∂(standardGaussian n)

def mutationLebesgueMeasure : Prop :=
  ∀ (n : Nat) (f : Euclidean n → ℝ),
    ContDiff ℝ 1 f →
    Integrable (fun x ↦ f x ^ 2) volume →
    Integrable (fun x ↦ xlogx (f x ^ 2)) volume →
    Integrable (fun x ↦ ‖fderiv ℝ f x‖ ^ 2) volume →
    entropySquare f volume ≤ 2 * ∫ x, ‖fderiv ℝ f x‖ ^ 2

end Stage1Instances.THM_M_1244

set_option pp.explicit true in
#print Stage1Instances.THM_M_1244.GaussianLogSobolevTarget
