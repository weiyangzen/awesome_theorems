import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1023: infinitely divisible distributions

This module freezes the real-line Levy-Khinchin statement using the truncation
`x * 1_{|x| <= 1}` and mathlib's positive-sign characteristic function.
It contains definitions and statement checks only, not a proof of the theorem.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal MeasureTheory

namespace Stage1Instances.THM_M_1023

/-- The `n`-fold additive convolution power, with the zeroth power equal to
the Dirac mass at zero. -/
def convolutionPower (mu : Measure Real) : Nat -> Measure Real
  | 0 => Measure.dirac 0
  | n + 1 => mu ∗ convolutionPower mu n

/-- A probability measure is infinitely divisible when it has a probability
convolution root of every strictly positive natural order. -/
def IsInfinitelyDivisible (mu : Measure Real) : Prop :=
  IsProbabilityMeasure mu /\
    forall n : Nat, 0 < n ->
      exists root : Measure Real,
        IsProbabilityMeasure root /\ convolutionPower root n = mu

/-- Levy-Khinchin data for the truncation `x * 1_{|x| <= 1}`. The jump
measure has no atom at zero and integrates `min 1 x^2`. -/
structure LevyKhintchineData where
  drift : Real
  gaussianVariance : NNReal
  jumpMeasure : Measure Real
  noAtomAtZero : jumpMeasure {0} = 0
  integrableMinOneSq :
    (∫⁻ x, ENNReal.ofReal (min 1 (x ^ 2)) ∂jumpMeasure) < ∞

/-- The characteristic exponent in the selected convention. -/
def LevyKhintchineData.exponent (d : LevyKhintchineData) (t : Real) : Complex :=
  Complex.I * (d.drift * t) - (d.gaussianVariance : Real) * t ^ 2 / 2 +
    ∫ x, (Complex.exp (Complex.I * (t * x)) - 1 -
      if |x| <= 1 then Complex.I * (t * x) else 0) ∂d.jumpMeasure

/-- The selected data represent `mu`. -/
def Represents (mu : Measure Real) (d : LevyKhintchineData) : Prop :=
  forall t : Real, charFun mu t = Complex.exp (d.exponent t)

/-- A measure has the selected Levy-Khinchin representation. -/
def HasLevyKhintchineRepresentation (mu : Measure Real) : Prop :=
  exists d : LevyKhintchineData,
    Represents mu d /\
      forall e : LevyKhintchineData, Represents mu e -> e = d

/-- Exact selected target: the real-line Levy-Khinchin characterization. -/
def InfinitelyDivisibleIffLevyKhintchine : Prop :=
  forall mu : Measure Real,
    IsInfinitelyDivisible mu <-> HasLevyKhintchineRepresentation mu

/-- Direct expansion used as a checked transport for the target boundary. -/
def ExpandedTarget : Prop :=
  forall mu : Measure Real,
    (IsProbabilityMeasure mu /\
      forall n : Nat, 0 < n ->
        exists root : Measure Real,
          IsProbabilityMeasure root /\ convolutionPower root n = mu) <->
    exists d : LevyKhintchineData,
      Represents mu d /\
        forall e : LevyKhintchineData, Represents mu e -> e = d

theorem target_iff_expanded :
    InfinitelyDivisibleIffLevyKhintchine <-> ExpandedTarget := by
  rfl

-- Deliberately non-equivalent mutations, elaborated separately.
def mutationRemovedProbabilityHypothesis : Prop :=
  forall mu : Measure Real,
    (forall n : Nat, 0 < n ->
      exists root : Measure Real,
        IsProbabilityMeasure root /\ convolutionPower root n = mu) <->
    HasLevyKhintchineRepresentation mu

def mutationAllowsZeroOrder : Prop :=
  forall mu : Measure Real,
    (IsProbabilityMeasure mu /\
      forall n : Nat, exists root : Measure Real,
        IsProbabilityMeasure root /\ convolutionPower root n = mu) <->
    HasLevyKhintchineRepresentation mu

def mutationChangedDomainToComplex : Prop :=
  forall mu : Measure Complex, IsProbabilityMeasure mu -> True

def mutationDroppedConverse : Prop :=
  forall mu : Measure Real,
    IsInfinitelyDivisible mu -> HasLevyKhintchineRepresentation mu

def mutationExcludesZeroGaussianPart : Prop :=
  forall mu : Measure Real,
    IsInfinitelyDivisible mu <->
      exists d : LevyKhintchineData, 0 < d.gaussianVariance /\
        Represents mu d /\
          forall e : LevyKhintchineData, Represents mu e -> e = d

end Stage1Instances.THM_M_1023

set_option pp.explicit true in
#print Stage1Instances.THM_M_1023.InfinitelyDivisibleIffLevyKhintchine
