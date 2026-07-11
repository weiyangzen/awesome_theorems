import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.RingTheory.Algebraic.Defs
import Mathlib.Topology.Instances.Irrational

/-!
# THM-M-0399: canonical statement

This module elaborates only the statement of Roth's theorem. It intentionally contains no
declaration of a proof of `RothStatement`.
-/

noncomputable section

namespace Stage1Instances.THM_M_0399

/-- Rationals approximating `alpha` beyond exponent `2 + epsilon`, using the positive reduced
denominator supplied by `Rat.den`. -/
def exceptionalRationals (alpha epsilon : ℝ) : Set ℚ :=
  {x | |alpha - (x : ℝ)| < Real.rpow (x.den : ℝ) (-(2 + epsilon))}

/-- Roth's theorem in its exponent-`2 + epsilon`, constant-one formulation. -/
def RothStatement : Prop :=
  ∀ (alpha : ℝ), IsAlgebraic ℚ alpha → Irrational alpha →
    ∀ (epsilon : ℝ), 0 < epsilon → (exceptionalRationals alpha epsilon).Finite

-- These separately elaborated mutations are fingerprint fixtures for the statement validator.
def mutationRemovedIrrationality : Prop :=
  ∀ (alpha : ℝ), IsAlgebraic ℚ alpha →
    ∀ (epsilon : ℝ), 0 < epsilon → (exceptionalRationals alpha epsilon).Finite

def mutationChangedDomain : Prop :=
  ∀ (alpha : ℚ),
    ∀ (epsilon : ℝ), 0 < epsilon → (exceptionalRationals (alpha : ℝ) epsilon).Finite

def mutationChangedBinderScope : Prop :=
  ∀ (epsilon : ℝ), 0 < epsilon →
    ∀ (alpha : ℝ), IsAlgebraic ℚ alpha → Irrational alpha →
      (exceptionalRationals alpha epsilon).Finite

def mutationEpsilonBoundary : Prop :=
  ∀ (alpha : ℝ), IsAlgebraic ℚ alpha → Irrational alpha →
    (exceptionalRationals alpha 0).Finite

end Stage1Instances.THM_M_0399

set_option pp.explicit true in
#print Stage1Instances.THM_M_0399.RothStatement
