import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.SpecialFunctions.Gamma.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1288: Talenti's sharp Sobolev inequality

This module freezes the inequality-only target selected by the intake. It does
not prove the inequality.
-/

noncomputable section

open MeasureTheory
open scoped ContDiff Gradient

namespace Stage1Instances.THM_M_1288

/-- Euclidean `n`-space with its standard inner product and volume measure. -/
abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/-- The real-valued `L^p` expression used in the classical statement. -/
def lpNorm {n : Nat} (p : Real) (f : Space n -> Real) : Real :=
  (integral volume (fun x => ‖f x‖ ^ p)) ^ (1 / p)

/-- The corresponding `L^p` expression for a Euclidean-vector-valued map. -/
def vectorLpNorm {n : Nat} (p : Real) (f : Space n -> Space n) : Real :=
  (integral volume (fun x => ‖f x‖ ^ p)) ^ (1 / p)

/-- The Sobolev conjugate `np/(n-p)`. -/
def sobolevConjugate (n : Nat) (p : Real) : Real :=
  (n : Real) * p / ((n : Real) - p)

/-- Talenti's explicit optimal constant in the normalization
`‖u‖_(np/(n-p)) <= C(n,p) ‖gradient u‖_p`. -/
def talentiConstant (n : Nat) (p : Real) : Real :=
  Real.pi ^ (-1 / 2 : Real) *
    (n : Real) ^ (-1 / p) *
    ((p - 1) / ((n : Real) - p)) ^ (1 - 1 / p) *
    (Real.Gamma (1 + (n : Real) / 2) * Real.Gamma n /
      (Real.Gamma ((n : Real) / p) *
        Real.Gamma (1 + (n : Real) - (n : Real) / p))) ^ (1 / (n : Real))

/-- An admissible Sobolev constant for smooth compactly supported scalar
functions on Euclidean `n`-space. -/
def IsAdmissibleConstant (n : Nat) (p C : Real) : Prop :=
  forall u : Space n -> Real,
    ContDiff Real ∞ u ->
    HasCompactSupport u ->
    lpNorm (sobolevConjugate n p) u <= C * vectorLpNorm p (gradient u)

/-- Canonical statement of Talenti's sharp first-order Sobolev inequality.
The second conjunct records sharpness: the displayed constant is least among
all constants valid on the same test-function class. -/
def TalentiSharpSobolevTarget : Prop :=
  forall (n : Nat) (p : Real),
    1 < p -> p < (n : Real) ->
      IsAdmissibleConstant n p (talentiConstant n p) /\
      forall C : Real, IsAdmissibleConstant n p C -> talentiConstant n p <= C

-- Structural mutations are separately elaborated and inspected by the receipt.
def mutationRemovedLowerBound : Prop :=
  forall (n : Nat) (p : Real), p < (n : Real) ->
    IsAdmissibleConstant n p (talentiConstant n p)

def mutationRemovedSharpness : Prop :=
  forall (n : Nat) (p : Real),
    1 < p -> p < (n : Real) -> IsAdmissibleConstant n p (talentiConstant n p)

def mutationChangedTestClass : Prop :=
  forall (n : Nat) (p : Real), 1 < p -> p < (n : Real) ->
    forall u : Space n -> Real,
      lpNorm (sobolevConjugate n p) u <=
        talentiConstant n p * vectorLpNorm p (gradient u)

end Stage1Instances.THM_M_1288

set_option pp.explicit true in
#print Stage1Instances.THM_M_1288.TalentiSharpSobolevTarget
