import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.IntegrableOn
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar

/-!
# THM-M-1177: Alexandrov-Bakelman-Pucci statement

This module freezes the classical, drift-free, determinant-weighted upper
estimate selected at intake. It states the target proposition but does not
prove the ABP estimate.
-/

noncomputable section

open scoped BigOperators
open MeasureTheory

namespace Stage1Instances.THM_M_1177

/-- Euclidean space of dimension `n`, in the coordinate model used by the
coefficient matrices and Hessian below. -/
abbrev Euclidean (n : Nat) := Fin n → ℝ

/-- The coordinate Hessian obtained from the second Frechet derivative. -/
def hessian {n : Nat} (u : Euclidean n → ℝ) (x : Euclidean n) :
    Matrix (Fin n) (Fin n) ℝ :=
  fun i j => fderiv ℝ (fderiv ℝ u) x (Pi.single i 1) (Pi.single j 1)

/-- Pointwise symmetry and strict positive definiteness of a coefficient
matrix. This explicit predicate fixes the convention without relying on an
alternate matrix-order encoding. -/
def IsSymmetricPositiveDefinite {n : Nat}
    (A : Matrix (Fin n) (Fin n) ℝ) : Prop :=
  A.transpose = A ∧
    ∀ v : Euclidean n, v ≠ 0 →
      0 < ∑ i : Fin n, v i * (A.mulVec v) i

/-- Points where an affine function touching `u` from above at `x` dominates
`u` throughout the domain. -/
def upperContactSet {n : Nat} (Ω : Set (Euclidean n))
    (u : Euclidean n → ℝ) : Set (Euclidean n) :=
  {x | x ∈ Ω ∧ ∃ p : Euclidean n, ∀ y ∈ Ω,
    u y ≤ u x + ∑ i : Fin n, p i * (y i - x i)}

/-- The determinant-weighted `L^n` quantity over the upper contact set. -/
def weightedNegativeNorm {n : Nat} (Ω : Set (Euclidean n))
    (u f : Euclidean n → ℝ)
    (A : Euclidean n → Matrix (Fin n) (Fin n) ℝ) : ℝ :=
  Real.rpow
    (∫ x in upperContactSet Ω u,
      (max (-f x) 0) ^ n / Matrix.det (A x))
    (1 / (n : ℝ))

/-- The exact classical ABP target selected at intake.

For each positive dimension there is a dimensional constant which works for
every bounded open preconnected domain, classical subsolution, and measurable
strictly positive-definite coefficient field. -/
def AlexandrovBakelmanPucciTarget : Prop :=
  ∀ n : Nat, 1 ≤ n → ∃ Cn : ℝ, 0 ≤ Cn ∧
    ∀ (Ω : Set (Euclidean n))
      (u f : Euclidean n → ℝ)
      (A : Euclidean n → Matrix (Fin n) (Fin n) ℝ),
      IsOpen Ω → IsPreconnected Ω → Bornology.IsBounded Ω →
      ContinuousOn u (closure Ω) → ContDiffOn ℝ 2 u Ω →
      Measurable f →
      (∀ i j, Measurable fun x => A x i j) →
      (∀ x ∈ Ω, IsSymmetricPositiveDefinite (A x)) →
      (∀ x ∈ Ω,
        Matrix.trace (A x * hessian u x) ≥ f x) →
      (∀ x ∈ frontier Ω, u x ≤ 0) →
      IntegrableOn
        (fun x => (max (-f x) 0) ^ n / Matrix.det (A x))
        (upperContactSet Ω u) →
      sSup (u '' Ω) ≤
        Cn * Metric.diam Ω * weightedNegativeNorm Ω u f A

-- Separately elaborated mutations used by `check_statement.py`.
def mutationAllowsDimensionZero : Prop :=
  ∀ n : Nat, ∃ Cn : ℝ, 0 ≤ Cn ∧
    ∀ (Ω : Set (Euclidean n)) (u f : Euclidean n → ℝ)
      (A : Euclidean n → Matrix (Fin n) (Fin n) ℝ), True

def mutationDropsBoundaryCondition : Prop :=
  ∀ n : Nat, 1 ≤ n → ∃ Cn : ℝ, 0 ≤ Cn ∧
    ∀ (Ω : Set (Euclidean n)) (u : Euclidean n → ℝ),
      sSup (u '' Ω) ≤ Cn * Metric.diam Ω

def mutationUsesWholeDomain : Prop :=
  ∀ n : Nat, 1 ≤ n → ∃ Cn : ℝ, 0 ≤ Cn ∧
    ∀ (Ω : Set (Euclidean n))
      (u f : Euclidean n → ℝ)
      (A : Euclidean n → Matrix (Fin n) (Fin n) ℝ),
      sSup (u '' Ω) ≤ Cn * Metric.diam Ω *
        Real.rpow (∫ x in Ω, (max (-f x) 0) ^ n / Matrix.det (A x))
          (1 / (n : ℝ))

def mutationReversesOperatorSign : Prop :=
  ∀ n : Nat, 1 ≤ n → ∀ (Ω : Set (Euclidean n))
    (u f : Euclidean n → ℝ)
    (A : Euclidean n → Matrix (Fin n) (Fin n) ℝ),
    (∀ x ∈ Ω, Matrix.trace (A x * hessian u x) ≤ f x) → True

end Stage1Instances.THM_M_1177

set_option pp.explicit true in
#print Stage1Instances.THM_M_1177.AlexandrovBakelmanPucciTarget
