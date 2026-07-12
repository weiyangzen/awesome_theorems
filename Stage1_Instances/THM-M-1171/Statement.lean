import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# THM-M-1171: exact Calderon-Zygmund estimate statement

This module freezes the whole-space, scalar, compactly-supported smooth-function
form of the estimate. It contains no proof of the estimate.
-/

namespace Stage1Instances.THM_M_1171

open scoped ENNReal
open MeasureTheory

/-- Euclidean space in dimension `n`, represented with its standard Pi norm. -/
abbrev Euclidean (n : Nat) := Fin n → ℝ

/-- The second Frechet derivative, viewed as a bilinear map by currying. -/
noncomputable def hessian {n : Nat} (u : Euclidean n → ℝ) (x : Euclidean n) :
    Euclidean n →L[ℝ] Euclidean n →L[ℝ] ℝ :=
  fderiv ℝ (fun y ↦ fderiv ℝ u y) x

/-- The trace of the Hessian in the standard coordinates. -/
noncomputable def laplacian {n : Nat} (u : Euclidean n → ℝ) (x : Euclidean n) : ℝ :=
  ∑ i : Fin n, hessian u x (Pi.single i 1) (Pi.single i 1)

/-- The canonical whole-space Calderon-Zygmund target.

The exponent uses `ENNReal`, matching mathlib's `eLpNorm`. The hypotheses
`1 < p` and `p < ∞` state exactly the strong-type range. The constant is
nonnegative and may depend on `n` and `p`, but not on `u`.
-/
def CalderonZygmundEstimateTarget : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (p : ENNReal), 1 < p → p < ∞ →
    ∃ C : ℝ, 0 ≤ C ∧ ∀ u : Euclidean n → ℝ,
      ContDiff ℝ ⊤ u → HasCompactSupport u →
        eLpNorm (fun x ↦ ‖hessian u x‖) p (volume : Measure (Euclidean n)) ≤
          ENNReal.ofReal C * eLpNorm (laplacian u) p (volume : Measure (Euclidean n))

/-- An explicitly expanded spelling used to check the chosen binder order and
the strict upper endpoint. -/
def ExpandedTarget : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (p : ENNReal), 1 < p → p < ∞ →
    ∃ C : ℝ, 0 ≤ C ∧ ∀ u : (Fin n → ℝ) → ℝ,
      ContDiff ℝ ⊤ u → HasCompactSupport u →
        eLpNorm
            (fun x ↦ ‖fderiv ℝ (fun y ↦ fderiv ℝ u y) x‖) p
              (volume : Measure (Fin n → ℝ)) ≤
          ENNReal.ofReal C * eLpNorm
            (fun x ↦ ∑ i : Fin n,
              (fderiv ℝ (fun y ↦ fderiv ℝ u y) x)
                (Pi.single i 1) (Pi.single i 1)) p (volume : Measure (Fin n → ℝ))

/-- Checked definitional transport to the expanded encoding. -/
theorem calderonZygmundEstimateTarget_iff_expandedTarget :
    CalderonZygmundEstimateTarget ↔ ExpandedTarget :=
  Iff.rfl

-- Structural mutations, elaborated separately and compared by the validator.
def mutationIncludesDimensionZero : Prop :=
  ∀ (n : Nat) (p : ENNReal), 1 < p → p < ∞ →
    ∃ C : ℝ, 0 ≤ C ∧ ∀ u : Euclidean n → ℝ,
      ContDiff ℝ ⊤ u → HasCompactSupport u →
        eLpNorm (fun x ↦ ‖hessian u x‖) p (volume : Measure (Euclidean n)) ≤
          ENNReal.ofReal C * eLpNorm (laplacian u) p (volume : Measure (Euclidean n))

def mutationIncludesEndpointOne : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (p : ENNReal), 1 ≤ p → p < ∞ →
    ∃ C : ℝ, 0 ≤ C ∧ ∀ u : Euclidean n → ℝ,
      ContDiff ℝ ⊤ u → HasCompactSupport u →
        eLpNorm (fun x ↦ ‖hessian u x‖) p (volume : Measure (Euclidean n)) ≤
          ENNReal.ofReal C * eLpNorm (laplacian u) p (volume : Measure (Euclidean n))

def mutationConstantDependsOnFunction : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (p : ENNReal), 1 < p → p < ∞ →
    ∀ u : Euclidean n → ℝ, ContDiff ℝ ⊤ u → HasCompactSupport u →
      ∃ C : ℝ, 0 ≤ C ∧
        eLpNorm (fun x ↦ ‖hessian u x‖) p (volume : Measure (Euclidean n)) ≤
          ENNReal.ofReal C * eLpNorm (laplacian u) p (volume : Measure (Euclidean n))

def mutationReversedEstimate : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (p : ENNReal), 1 < p → p < ∞ →
    ∃ C : ℝ, 0 ≤ C ∧ ∀ u : Euclidean n → ℝ,
      ContDiff ℝ ⊤ u → HasCompactSupport u →
        eLpNorm (laplacian u) p (volume : Measure (Euclidean n)) ≤
          ENNReal.ofReal C * eLpNorm (fun x ↦ ‖hessian u x‖) p
            (volume : Measure (Euclidean n))

end Stage1Instances.THM_M_1171

set_option pp.explicit true in
#print Stage1Instances.THM_M_1171.CalderonZygmundEstimateTarget
