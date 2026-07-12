import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

/-!
# THM-M-1129 conditional root composition

This file checks only the final composition interface. `PoissonAnalyticPackage` is an explicit
premise representing the still-open analytic obligation tree; it is not evidence for that package.
-/

open scoped RealInnerProductSpace
open MeasureTheory Metric Set

namespace Stage1.THM_M_1129

/- The statement-shaped definitions below are deliberately repeated because this dossier is not a
Lake source module. Their exact correspondence is checked by source hashes and by elaborating both
files under the same imports; they are not credited as an alternate transport. -/
abbrev Plane := EuclideanSpace Real (Fin 2)

noncomputable def poissonDiskTerm (c t : Real) (h : Plane -> Real) (x : Plane) : Real :=
  (t / (2 * Real.pi)) *
    ∫ z in closedBall (0 : Plane) 1,
      h (x + (c * t) • z) / Real.sqrt (1 - norm z ^ 2)

def IsClassicalWaveSolution (c : Real) (f g : Plane -> Real) (u : Plane -> Real -> Real) : Prop :=
  (forall t, ContDiff Real 2 (fun x => u x t)) ∧
  (forall x t, HasDerivAt (fun s => u x s) (deriv (fun s => u x s) t) t) ∧
  (forall x t, HasDerivAt (deriv (fun s => u x s))
      (c ^ 2 * Laplacian.laplacian (fun y => u y t) x) t) ∧
  (forall x, u x 0 = f x) ∧
  (forall x, deriv (fun s => u x s) 0 = g x) ∧
  (forall t, HasCompactSupport (fun x => u x t))

def PoissonFormulaTarget : Prop :=
  forall (c : Real) (f g : Plane -> Real) (u : Plane -> Real -> Real),
    0 < c -> ContDiff Real 3 f -> ContDiff Real 2 g -> HasCompactSupport f ->
    HasCompactSupport g -> IsClassicalWaveSolution c f g u ->
    forall (x : Plane) (t : Real), 0 < t ->
      u x t = deriv (fun s => poissonDiskTerm c s f x) t + poissonDiskTerm c t g x

/-- The exact result that the analytic subtree must deliver. This abbreviation neither weakens nor
proves the canonical target. -/
def PoissonAnalyticPackage : Prop := PoissonFormulaTarget

/-- Kernel-checked conditional composition from the analytic package to the exact public root. -/
theorem poissonFormulaTarget_of_analyticPackage
    (analytic : PoissonAnalyticPackage) : PoissonFormulaTarget := by
  exact analytic

#print axioms poissonFormulaTarget_of_analyticPackage

end Stage1.THM_M_1129
