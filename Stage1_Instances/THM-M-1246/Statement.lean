import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

/-!
# THM-M-1246: exact Euclidean L2 Hardy inequality statement

This module freezes the differential Hardy inequality selected by the intake.
It elaborates only the proposition and structural statement checks; it supplies
no proof of the inequality.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1246

abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/--
The sharp Euclidean `L2` Hardy inequality for smooth compactly supported real
functions in dimension at least three. Lean's totalized division fixes the
singular integrand to zero at the origin. The operator norm of the Frechet
derivative is the Euclidean norm of the scalar-valued gradient.
-/
def HardyInequalityTarget : Prop :=
  forall (n : Nat), 3 <= n ->
    forall u : Space n -> Real,
      ContDiff Real ⊤ u ->
      HasCompactSupport u ->
      (∫ x, |u x| ^ 2 / ‖x‖ ^ 2) <=
        (2 / ((n : Real) - 2)) ^ 2 * ∫ x, ‖fderiv Real u x‖ ^ 2

/-- Checked expansion fixes all binders, hypotheses, measures, and constants. -/
theorem hardyInequalityTarget_iff_expanded :
    HardyInequalityTarget <->
      forall (n : Nat), 3 <= n ->
        forall u : Space n -> Real,
          ContDiff Real ⊤ u ->
          HasCompactSupport u ->
          (∫ x, |u x| ^ 2 / ‖x‖ ^ 2) <=
            (2 / ((n : Real) - 2)) ^ 2 * ∫ x, ‖fderiv Real u x‖ ^ 2 :=
  Iff.rfl

-- These altered propositions elaborate but are not definitionally the root.
example : True := by
  fail_if_success
    exact (Iff.rfl : HardyInequalityTarget <->
      forall (n : Nat), 2 <= n ->
        forall u : Space n -> Real,
          ContDiff Real ⊤ u -> HasCompactSupport u ->
          (∫ x, |u x| ^ 2 / ‖x‖ ^ 2) <=
            (2 / ((n : Real) - 2)) ^ 2 * ∫ x, ‖fderiv Real u x‖ ^ 2)
  trivial

example : True := by
  fail_if_success
    exact (Iff.rfl : HardyInequalityTarget <->
      forall (n : Nat), 3 <= n ->
        forall u : Space n -> Real,
          ContDiff Real ⊤ u ->
          (∫ x, |u x| ^ 2 / ‖x‖ ^ 2) <=
            (2 / ((n : Real) - 2)) ^ 2 * ∫ x, ‖fderiv Real u x‖ ^ 2)
  trivial

example : True := by
  fail_if_success
    exact (Iff.rfl : HardyInequalityTarget <->
      forall (n : Nat), 3 <= n ->
        forall u : Space n -> Real,
          ContDiff Real ⊤ u -> HasCompactSupport u ->
          (∫ x, |u x| ^ 2 / ‖x‖ ^ 2) >=
            (2 / ((n : Real) - 2)) ^ 2 * ∫ x, ‖fderiv Real u x‖ ^ 2)
  trivial

end Stage1Instances.THM_M_1246

set_option pp.explicit true in
#print Stage1Instances.THM_M_1246.HardyInequalityTarget
