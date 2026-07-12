import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Analysis.Calculus.ContDiff.Basic

/-!
# THM-M-1518: stationary action implies the Euler-Lagrange equation

This module freezes the statement selected by the rev-5.6 intake. It deliberately
states stationarity rather than a universal least-action claim and contains no
proof of the variational theorem.
-/

noncomputable section

open Set MeasureTheory

namespace Stage1Instances.THM_M_1518

/-- Euclidean configuration space of dimension `n`. -/
abbrev Configuration (n : Nat) := Fin n → ℝ

/-- A time-parametrized path in configuration space. -/
abbrev Path (n : Nat) := ℝ → Configuration n

/-- Fixed endpoint data on a nondegenerate compact time interval. -/
structure BoundaryData (n : Nat) where
  initialTime : ℝ
  finalTime : ℝ
  initialPosition : Configuration n
  finalPosition : Configuration n
  timeOrder : initialTime < finalTime

/-- The action of a path for a time-dependent Lagrangian. -/
def Action {n : Nat} (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n) : ℝ :=
  ∫ t in B.initialTime..B.finalTime, L (t, q t, deriv q t)

/-- A variation is admissible when it is continuously differentiable and
vanishes at both endpoints. -/
def AdmissibleVariation {n : Nat} (B : BoundaryData n) (η : Path n) : Prop :=
  ContDiff ℝ 1 η ∧ η B.initialTime = 0 ∧ η B.finalTime = 0

/-- The path obtained by varying `q` in direction `η` by parameter `ε`. -/
def VariedPath {n : Nat} (q η : Path n) (ε : ℝ) : Path n :=
  fun t => q t + ε • η t

/-- First variation of the action in an admissible direction. -/
def FirstVariation {n : Nat} (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q η : Path n) : ℝ :=
  deriv (fun ε : ℝ => Action L B (VariedPath q η ε)) 0

/-- Stationarity with respect to every continuously differentiable,
endpoint-fixing variation. -/
def StationaryAction {n : Nat} (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n) : Prop :=
  ∀ η : Path n, AdmissibleVariation B η → FirstVariation L B q η = 0

/-- Partial derivative of `L` with respect to position. -/
def PositionDerivative {n : Nat}
    (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (t : ℝ) (x v : Configuration n) : Configuration n →L[ℝ] ℝ :=
  fderiv ℝ (fun y => L (t, y, v)) x

/-- Partial derivative of `L` with respect to velocity. -/
def VelocityDerivative {n : Nat}
    (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (t : ℝ) (x v : Configuration n) : Configuration n →L[ℝ] ℝ :=
  fderiv ℝ (fun w => L (t, x, w)) v

/-- Pointwise Euler-Lagrange equation on the open time interval. -/
def EulerLagrangeEquation {n : Nat}
    (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n) : Prop :=
  ∀ t ∈ Ioo B.initialTime B.finalTime,
    HasDerivAt
      (fun τ => VelocityDerivative L τ (q τ) (deriv q τ))
      (PositionDerivative L t (q t) (deriv q t)) t

/-- The exact target selected at intake: fixed-endpoint stationary action
implies the interior Euler-Lagrange equation. -/
def StationaryActionEulerLagrangeTarget : Prop :=
  ∀ (n : Nat) (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n),
      ContDiff ℝ 2 L →
        ContDiff ℝ 2 q →
          q B.initialTime = B.initialPosition →
            q B.finalTime = B.finalPosition →
              StationaryAction L B q → EulerLagrangeEquation L B q

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationReversedImplication : Prop :=
  ∀ (n : Nat) (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n),
      ContDiff ℝ 2 L → ContDiff ℝ 2 q →
        q B.initialTime = B.initialPosition → q B.finalTime = B.finalPosition →
          EulerLagrangeEquation L B q → StationaryAction L B q

def mutationRemovedEndpointConditions : Prop :=
  ∀ (n : Nat) (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n),
      ContDiff ℝ 2 L → ContDiff ℝ 2 q →
        StationaryAction L B q → EulerLagrangeEquation L B q

def mutationAutonomousLagrangian : Prop :=
  ∀ (n : Nat) (L : Configuration n × Configuration n → ℝ)
    (B : BoundaryData n) (q : Path n),
      ContDiff ℝ 2 L → ContDiff ℝ 2 q →
        q B.initialTime = B.initialPosition → q B.finalTime = B.finalPosition →
          StationaryAction (fun z => L z.2) B q →
            EulerLagrangeEquation (fun z => L z.2) B q

def mutationLocalMinimumPremise : Prop :=
  ∀ (n : Nat) (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n),
      ContDiff ℝ 2 L → ContDiff ℝ 2 q →
        q B.initialTime = B.initialPosition → q B.finalTime = B.finalPosition →
          (∀ r : Path n, Action L B q ≤ Action L B r) → EulerLagrangeEquation L B q

/-- The zero variation satisfies the endpoint conditions. -/
theorem zero_admissibleVariation (n : Nat) (B : BoundaryData n) :
    AdmissibleVariation B (fun _ => (0 : Configuration n)) := by
  exact ⟨contDiff_const, rfl, rfl⟩

/-- A nondegenerate interval has no point simultaneously at both endpoints. -/
theorem endpoints_distinct (n : Nat) (B : BoundaryData n) :
    B.initialTime ≠ B.finalTime :=
  ne_of_lt B.timeOrder

end Stage1Instances.THM_M_1518

set_option pp.explicit true in
#print Stage1Instances.THM_M_1518.StationaryActionEulerLagrangeTarget
