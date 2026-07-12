import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Integral
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Constructions.Pi

/-!
# THM-M-1248: Caffarelli-Kohn-Nirenberg statement

This module freezes the sufficiency direction of the theorem on pages 259-260
of Caffarelli, Kohn, and Nirenberg (1984). It contains no proof of the
inequality.
-/

namespace Stage1Instances.THM_M_1248

open MeasureTheory

/-- The explicit weighted real `L^p` quantity used in the source statement.
The source permits `p < 1` for the target quantity, so this is not expressed
through mathlib's normed `Lp` space. -/
noncomputable def weightedLp {n : Nat} (p weight : Real)
    (u : EuclideanSpace Real (Fin n) -> Real) : Real :=
  (∫ x, (‖x‖ ^ weight * |u (WithLp.toLp 2 x)|) ^ p) ^ (p⁻¹)

/-- The weighted `L^p` quantity of the first derivative. For a scalar-valued
function the operator norm of `fderiv` is the Euclidean norm of its gradient. -/
noncomputable def weightedDerivativeLp {n : Nat} (p weight : Real)
    (u : EuclideanSpace Real (Fin n) -> Real) : Real :=
  (∫ x, (‖x‖ ^ weight * ‖fderiv Real u (WithLp.toLp 2 x)‖) ^ p) ^ (p⁻¹)

/-- Equations (1.1)-(1.3), (1.5), and the two conditional restrictions on
pages 259-260 of the primary paper. -/
def AdmissibleParameters (n : Nat)
    (p q r alpha beta gamma sigma a : Real) : Prop :=
  0 < n ∧
  1 ≤ p ∧ 1 ≤ q ∧ 0 < r ∧ 0 ≤ a ∧ a ≤ 1 ∧
  0 < p⁻¹ + alpha / n ∧
  0 < q⁻¹ + beta / n ∧
  0 < r⁻¹ + gamma / n ∧
  gamma = a * sigma + (1 - a) * beta ∧
  r⁻¹ + gamma / n =
    a * (p⁻¹ + (alpha - 1) / n) + (1 - a) * (q⁻¹ + beta / n) ∧
  (0 < a -> 0 ≤ alpha - sigma) ∧
  (0 < a ->
    p⁻¹ + (alpha - 1) / n = r⁻¹ + gamma / n ->
    alpha - sigma ≤ 1)

/-- The exact weighted interpolation estimate selected at intake. The source's
`C_c^infinity (R^n)` is represented by `ContDiff Real infinity` together with
compact support. -/
def CaffarelliKohnNirenbergTarget : Prop :=
  ∀ (n : Nat) (p q r alpha beta gamma sigma a : Real),
    AdmissibleParameters n p q r alpha beta gamma sigma a ->
    ∃ C : Real, 0 < C ∧
      ∀ u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma u ≤
          C * (weightedDerivativeLp p alpha u) ^ a *
            (weightedLp q beta u) ^ (1 - a)

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedCriticalRestriction : Prop :=
  ∀ (n : Nat) (p q r alpha beta gamma sigma a : Real),
    (AdmissibleParameters n p q r alpha beta gamma sigma a ∨ alpha - sigma > 1) ->
    ∃ C : Real, 0 < C ∧
      ∀ u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma u ≤
          C * (weightedDerivativeLp p alpha u) ^ a *
            (weightedLp q beta u) ^ (1 - a)

def mutationChangedDomain : Prop :=
  ∀ (p q r alpha beta gamma sigma a : Real),
    AdmissibleParameters 1 p q r alpha beta gamma sigma a ->
    ∃ C : Real, 0 < C ∧
      ∀ u : Real -> Real, ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma (fun x : EuclideanSpace Real (Fin 1) => u (x 0)) ≤ C

def mutationChangedBinderScope : Prop :=
  ∃ C : Real, 0 < C ∧
    ∀ (n : Nat) (p q r alpha beta gamma sigma a : Real),
      AdmissibleParameters n p q r alpha beta gamma sigma a ->
      ∀ u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma u ≤
          C * (weightedDerivativeLp p alpha u) ^ a *
            (weightedLp q beta u) ^ (1 - a)

def mutationIncludesZeroDimension : Prop :=
  ∀ (n : Nat) (p q r alpha beta gamma sigma a : Real),
    (AdmissibleParameters n p q r alpha beta gamma sigma a ∨ n = 0) ->
    ∃ C : Real, 0 < C ∧
      ∀ u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma u ≤ C

end Stage1Instances.THM_M_1248

set_option pp.explicit true in
#print Stage1Instances.THM_M_1248.CaffarelliKohnNirenbergTarget
