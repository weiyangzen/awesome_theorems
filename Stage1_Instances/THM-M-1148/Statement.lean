import Mathlib.Analysis.Complex.Harmonic.Poisson

/-!
# THM-M-1148: Poisson integral formula on a disk

This module freezes the exact rev-5.6 target. It contains no proof of the
Dirichlet existence theorem.
-/

noncomputable section

open InnerProductSpace Metric Real Set

namespace Stage1Instances.THM_M_1148

/--
For positive radius and continuous real boundary data, the Poisson integral
is represented by a harmonic function on the disk which extends continuously
to the closed disk and has the prescribed boundary trace.

`circleAverage` fixes the normalization: it is the average over the angular
parameter, so the displayed kernel needs no additional `2 * pi` factor.
-/
def PoissonIntegralFormula : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R →
      ∀ g : ℂ → ℝ,
        ContinuousOn g (sphere c R) →
          ∃ u : ℂ → ℝ,
            HarmonicOnNhd u (ball c R) ∧
              ContinuousOn u (closedBall c R) ∧
                EqOn u g (sphere c R) ∧
                  ∀ w : ℂ, w ∈ ball c R →
                    circleAverage (poissonKernel c w • g) c R = u w

-- Structural mutations are separately elaborated statement fixtures.
def mutationRemovedPositiveRadius : Prop :=
  ∀ (c : ℂ) (R : ℝ) (g : ℂ → ℝ),
    ContinuousOn g (sphere c R) →
      ∃ u : ℂ → ℝ,
        HarmonicOnNhd u (ball c R) ∧
          ContinuousOn u (closedBall c R) ∧
            EqOn u g (sphere c R) ∧
              ∀ w : ℂ, w ∈ ball c R →
                circleAverage (poissonKernel c w • g) c R = u w

def mutationChangedValueDomain : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R →
      ∀ g : ℂ → ℂ,
        ContinuousOn g (sphere c R) →
          ∃ u : ℂ → ℂ,
            HarmonicOnNhd u (ball c R) ∧
              ContinuousOn u (closedBall c R) ∧
                EqOn u g (sphere c R) ∧
                  ∀ w : ℂ, w ∈ ball c R →
                    circleAverage (poissonKernel c w • g) c R = u w

def mutationChangedBinderScope : Prop :=
  ∀ (c : ℂ) (R : ℝ) (g : ℂ → ℝ),
    0 < R ∧ ContinuousOn g (sphere c R) ∧
      ∃ u : ℂ → ℝ,
        HarmonicOnNhd u (ball c R) ∧
          ContinuousOn u (closedBall c R) ∧
            EqOn u g (sphere c R) ∧
              ∀ w : ℂ, w ∈ ball c R →
                circleAverage (poissonKernel c w • g) c R = u w

def mutationFormulaOnClosedDisk : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R →
      ∀ g : ℂ → ℝ,
        ContinuousOn g (sphere c R) →
          ∃ u : ℂ → ℝ,
            HarmonicOnNhd u (ball c R) ∧
              ContinuousOn u (closedBall c R) ∧
                EqOn u g (sphere c R) ∧
                  ∀ w : ℂ, w ∈ closedBall c R →
                    circleAverage (poissonKernel c w • g) c R = u w

def mutationRemovedBoundaryTrace : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R →
      ∀ g : ℂ → ℝ,
        ContinuousOn g (sphere c R) →
          ∃ u : ℂ → ℝ,
            HarmonicOnNhd u (ball c R) ∧
              ContinuousOn u (closedBall c R) ∧
                ∀ w : ℂ, w ∈ ball c R →
                  circleAverage (poissonKernel c w • g) c R = u w

end Stage1Instances.THM_M_1148

set_option pp.explicit true in
#print Stage1Instances.THM_M_1148.PoissonIntegralFormula
