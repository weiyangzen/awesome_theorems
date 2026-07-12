import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.InnerProductSpace.Laplacian

/-!
# THM-M-1289: Aubin-Talenti functions

This module freezes the PDE-normalized positive critical bubble and its sharp
homogeneous Sobolev equality property. It contains no proof of those facts.
-/

namespace Stage1Instances.THM_M_1289

open scoped ENNReal RealInnerProductSpace
open MeasureTheory

abbrev Euclidean (n : Nat) := EuclideanSpace ℝ (Fin n)

/-- The critical Sobolev exponent `2n / (n - 2)`, represented for `eLpNorm`. -/
noncomputable def criticalExponent (n : Nat) : ENNReal :=
  ENNReal.ofReal (2 * (n : ℝ) / ((n : ℝ) - 2))

/-- The PDE-normalized Aubin-Talenti bubble with center `a` and scale `lambda`. -/
noncomputable def bubble (n : Nat) (a : Euclidean n) (lambda : ℝ) : Euclidean n → ℝ :=
  fun x ↦
    Real.rpow ((n : ℝ) * ((n : ℝ) - 2)) (((n : ℝ) - 2) / 4) *
      Real.rpow (lambda / (lambda ^ 2 + ‖x - a‖ ^ 2)) (((n : ℝ) - 2) / 2)

/-- The `L^2` seminorm of the Frechet gradient. -/
noncomputable def gradientNorm {n : Nat} (f : Euclidean n → ℝ) : ENNReal :=
  eLpNorm (fun x ↦ ‖fderiv ℝ f x‖) (ENNReal.ofReal 2)
    (volume : Measure (Euclidean n))

/-- `C` is the least constant in the critical homogeneous Sobolev inequality.
The test class is smooth compactly supported real functions on `R^n`. -/
def IsSharpSobolevConstant (n : Nat) (C : ℝ) : Prop :=
  0 < C ∧
  (∀ f : Euclidean n → ℝ, ContDiff ℝ ⊤ f → HasCompactSupport f →
    eLpNorm f (criticalExponent n) (volume : Measure (Euclidean n)) ≤
      ENNReal.ofReal C * gradientNorm f) ∧
  ∀ C' : ℝ, 0 ≤ C' → C' < C →
    ∃ f : Euclidean n → ℝ, ContDiff ℝ ⊤ f ∧ HasCompactSupport f ∧
      ENNReal.ofReal C' * gradientNorm f <
        eLpNorm f (criticalExponent n) (volume : Measure (Euclidean n))

/-- The exact target selected at intake: every positive-scale normalized bubble
is positive and smooth, solves the pointwise critical PDE, lies in the
homogeneous Sobolev class, and realizes the sharp Sobolev constant. -/
def AubinTalentiTarget : Prop :=
  ∀ (n : Nat), 3 ≤ n → ∀ (a : Euclidean n) (lambda : ℝ), 0 < lambda →
    let U := bubble n a lambda
    (∀ x, 0 < U x) ∧
    ContDiff ℝ ⊤ U ∧
    (∀ x, -Laplacian.laplacian U x =
      Real.rpow (U x) (((n : ℝ) + 2) / ((n : ℝ) - 2))) ∧
    eLpNorm U (criticalExponent n) (volume : Measure (Euclidean n)) < ⊤ ∧
    gradientNorm U < ⊤ ∧
    ∃ C : ℝ, IsSharpSobolevConstant n C ∧
      eLpNorm U (criticalExponent n) (volume : Measure (Euclidean n)) =
        ENNReal.ofReal C * gradientNorm U

-- Independently elaborated structural mutations for the statement gate.
def mutationRemovedDimensionBound : Prop :=
  ∀ (n : Nat) (a : Euclidean n) (lambda : ℝ), 0 < lambda →
    ∀ x, 0 < bubble n a lambda x

def mutationNonnegativeScale : Prop :=
  ∀ (n : Nat), 3 ≤ n → ∀ (a : Euclidean n) (lambda : ℝ), 0 ≤ lambda →
    ∀ x, 0 < bubble n a lambda x

def mutationChangedDomain : Prop :=
  ∀ (n : Nat), 3 ≤ n → ∀ (a : (Fin n → ℚ)) (lambda : ℚ), 0 < lambda → a = a

def mutationClassification : Prop :=
  ∀ (n : Nat), 3 ≤ n → ∀ f : Euclidean n → ℝ,
    (∃ C : ℝ, IsSharpSobolevConstant n C ∧
      eLpNorm f (criticalExponent n) (volume : Measure (Euclidean n)) =
        ENNReal.ofReal C * gradientNorm f) →
    ∃ (a : Euclidean n) (lambda : ℝ), 0 < lambda ∧ f = bubble n a lambda

#check_failure (rfl : AubinTalentiTarget = mutationRemovedDimensionBound)
#check_failure (rfl : AubinTalentiTarget = mutationNonnegativeScale)
#check_failure (rfl : AubinTalentiTarget = mutationChangedDomain)
#check_failure (rfl : AubinTalentiTarget = mutationClassification)

end Stage1Instances.THM_M_1289

set_option pp.explicit true in
#print Stage1Instances.THM_M_1289.AubinTalentiTarget
