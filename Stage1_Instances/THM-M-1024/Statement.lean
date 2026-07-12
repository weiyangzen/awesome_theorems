import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1024: Levy-Khintchine representation statement

This module freezes the statement boundary only. It does not prove the
Levy-Khintchine theorem.
-/

namespace Stage1Instances.THM_M_1024

open scoped MeasureTheory
open MeasureTheory Set

abbrev Space (d : Nat) := EuclideanSpace Real (Fin d)

/-- Probability-law predicate, kept as data rather than a typeclass so that
convolution roots can be quantified without synthesizing local instances. -/
def IsProbabilityLaw {E : Type*} [MeasurableSpace E] (mu : Measure E) : Prop :=
  mu univ = 1

/-- The `n`-fold additive convolution, with the zeroth power the point mass at
zero. Only positive powers occur in `InfinitelyDivisible`. -/
noncomputable def convolutionPow {E : Type*} [MeasurableSpace E] [AddMonoid E]
    (mu : Measure E) : Nat -> Measure E
  | 0 => Measure.dirac 0
  | n + 1 => convolutionPow mu n ∗ mu

/-- A probability law has a probability convolution root of every positive
integer order. -/
def InfinitelyDivisible {E : Type*} [MeasurableSpace E] [AddMonoid E]
    (mu : Measure E) : Prop :=
  IsProbabilityLaw mu ∧
    ∀ n : Nat, 0 < n -> ∃ root : Measure E,
      IsProbabilityLaw root ∧ convolutionPow root n = mu

/-- Drift, Gaussian covariance operator, and jump measure. -/
structure LevyTriplet (d : Nat) where
  drift : Space d
  covariance : Space d →L[Real] Space d
  jumps : Measure (Space d)

/-- The Levy measure conditions, with the value at the origin stated
separately and the usual truncated second moment encoded by integrability. -/
def IsLevyMeasure {d : Nat} (nu : Measure (Space d)) : Prop :=
  nu {0} = 0 ∧
    Integrable (fun x : Space d => min 1 (‖x‖ ^ 2)) nu

/-- Symmetry and positive semidefiniteness of the Gaussian covariance. -/
def IsCovariance {d : Nat} (Q : Space d →L[Real] Space d) : Prop :=
  (∀ x y, @inner Real _ _ (Q x) y = @inner Real _ _ x (Q y)) ∧
    ∀ x, 0 ≤ @inner Real _ _ x (Q x)

/-- Levy-Khintchine exponent with Fourier sign `+i`, Gaussian coefficient
`-1/2`, and closed-unit-ball compensation. -/
noncomputable def levyExponent {d : Nat} (data : LevyTriplet d) (u : Space d) : Complex :=
  Complex.I * ((@inner Real _ _ data.drift u : Real) : Complex)
    - (1 / 2 : Complex) * ((@inner Real _ _ u (data.covariance u) : Real) : Complex)
    + ∫ x : Space d,
        (Complex.exp (Complex.I * ((@inner Real _ _ u x : Real) : Complex)) - 1
          - Complex.I * ((@inner Real _ _ u x : Real) : Complex) * if ‖x‖ ≤ 1 then 1 else 0) ∂data.jumps

/-- Valid representation data for `mu` under the frozen convention. -/
def Represents {d : Nat} (mu : Measure (Space d)) (data : LevyTriplet d) : Prop :=
  IsCovariance data.covariance ∧
    IsLevyMeasure data.jumps ∧
    ∀ u : Space d, charFun mu u = Complex.exp (levyExponent data u)

/-- Exact target: infinite divisibility is equivalent to existence and
convention-relative uniqueness of Levy-Khintchine representation data. -/
def LevyKhintchineTarget : Prop :=
  ∀ (d : Nat) (mu : Measure (Space d)),
    InfinitelyDivisible mu ↔ ∃! data : LevyTriplet d, Represents mu data

-- Structural mutations elaborated separately for statement discrimination.
def mutationNoUniqueness : Prop :=
  ∀ (d : Nat) (mu : Measure (Space d)),
    InfinitelyDivisible mu ↔ ∃ data : LevyTriplet d, Represents mu data

def mutationDimensionOne : Prop :=
  ∀ mu : Measure (Space 1),
    InfinitelyDivisible mu ↔ ∃! data : LevyTriplet 1, Represents mu data

def mutationNoAtomCondition {d : Nat} (nu : Measure (Space d)) : Prop :=
  Integrable (fun x : Space d => min 1 (‖x‖ ^ 2)) nu

noncomputable def mutationOpenBallExponent {d : Nat} (data : LevyTriplet d)
    (u : Space d) : Complex :=
  Complex.I * ((@inner Real _ _ data.drift u : Real) : Complex)
    - (1 / 2 : Complex) * ((@inner Real _ _ u (data.covariance u) : Real) : Complex)
    + ∫ x : Space d,
        (Complex.exp (Complex.I * ((@inner Real _ _ u x : Real) : Complex)) - 1
          - Complex.I * ((@inner Real _ _ u x : Real) : Complex) * if ‖x‖ < 1 then 1 else 0) ∂data.jumps

/-- Dimension zero remains in the target and its space is inhabited. -/
example : Nonempty (Space 0) := inferInstance

end Stage1Instances.THM_M_1024

set_option pp.explicit true in
#print Stage1Instances.THM_M_1024.LevyKhintchineTarget
