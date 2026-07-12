import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

open scoped RealInnerProductSpace
open MeasureTheory Metric Set

namespace Stage1.THM_M_1129

abbrev Plane := EuclideanSpace ℝ (Fin 2)

/-- The unit-disk version of the Poisson integral.  Keeping the disk fixed makes the
change of variables, including its `t / (2 * pi)` normalization, explicit. -/
noncomputable def poissonDiskTerm (c t : ℝ) (h : Plane → ℝ) (x : Plane) : ℝ :=
  (t / (2 * Real.pi)) *
    ∫ z in closedBall (0 : Plane) 1,
      h (x + (c * t) • z) / Real.sqrt (1 - ‖z‖ ^ 2)

/-- A classical solution of the homogeneous two-dimensional wave Cauchy problem.
The compact-support clause fixes the uniqueness class used by the statement. -/
def IsClassicalWaveSolution (c : ℝ) (f g : Plane → ℝ) (u : Plane → ℝ → ℝ) : Prop :=
  (∀ t, ContDiff ℝ 2 (fun x => u x t)) ∧
  (∀ x t, HasDerivAt (fun s => u x s) (deriv (fun s => u x s) t) t) ∧
  (∀ x t, HasDerivAt (deriv (fun s => u x s))
      (c ^ 2 * Laplacian.laplacian (fun y => u y t) x) t) ∧
  (∀ x, u x 0 = f x) ∧
  (∀ x, deriv (fun s => u x s) 0 = g x) ∧
  (∀ t, HasCompactSupport (fun x => u x t))

/-- Exact formal target for Poisson's formula for the two-dimensional wave equation.
The data regularity/support hypotheses follow the classical compactly-supported formulation;
the conclusion is asserted only for positive time, since `t = 0` is recovered by the initial
conditions rather than substitution into the singular kernel. -/
def PoissonFormulaTarget : Prop :=
  ∀ (c : ℝ) (f g : Plane → ℝ) (u : Plane → ℝ → ℝ),
    0 < c →
    ContDiff ℝ 3 f →
    ContDiff ℝ 2 g →
    HasCompactSupport f →
    HasCompactSupport g →
    IsClassicalWaveSolution c f g u →
    ∀ (x : Plane) (t : ℝ), 0 < t →
      u x t = deriv (fun s => poissonDiskTerm c s f x) t + poissonDiskTerm c t g x

#check PoissonFormulaTarget
#print PoissonFormulaTarget

namespace MutationTests

def RemovedPositiveSpeed : Prop :=
  ∀ (c : ℝ) (f g : Plane → ℝ) (u : Plane → ℝ → ℝ),
    ContDiff ℝ 3 f → ContDiff ℝ 2 g → HasCompactSupport f → HasCompactSupport g →
    IsClassicalWaveSolution c f g u →
    ∀ x t, 0 < t →
      u x t = deriv (fun s => poissonDiskTerm c s f x) t + poissonDiskTerm c t g x

abbrev Space3 := EuclideanSpace ℝ (Fin 3)

def ChangedDomain : Prop :=
  ∀ (c : ℝ) (f g : Space3 → ℝ) (_u : Space3 → ℝ → ℝ), 0 < c →
    ContDiff ℝ 3 f → ContDiff ℝ 2 g → HasCompactSupport f → HasCompactSupport g → True

def ChangedBinderScope : Prop :=
  ∀ (c : ℝ) (f g : Plane → ℝ) (u : Plane → ℝ → ℝ), 0 < c →
    ContDiff ℝ 3 f → ContDiff ℝ 2 g → HasCompactSupport f → HasCompactSupport g →
    IsClassicalWaveSolution c f g u →
    (∀ x, ∃ t, 0 < t ∧
      u x t = deriv (fun s => poissonDiskTerm c s f x) t + poissonDiskTerm c t g x)

def IncludedBoundary : Prop :=
  ∀ (c : ℝ) (f g : Plane → ℝ) (u : Plane → ℝ → ℝ), 0 < c →
    ContDiff ℝ 3 f → ContDiff ℝ 2 g → HasCompactSupport f → HasCompactSupport g →
    IsClassicalWaveSolution c f g u →
    ∀ x t, 0 ≤ t →
      u x t = deriv (fun s => poissonDiskTerm c s f x) t + poissonDiskTerm c t g x

#check_failure (rfl : PoissonFormulaTarget = RemovedPositiveSpeed)
#check_failure (rfl : PoissonFormulaTarget = ChangedDomain)
#check_failure (rfl : PoissonFormulaTarget = ChangedBinderScope)
#check_failure (rfl : PoissonFormulaTarget = IncludedBoundary)

end MutationTests

end Stage1.THM_M_1129
