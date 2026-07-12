import Mathlib.Probability.CentralLimitTheorem

/-!
# Exact target for THM-M-0989

This module freezes the forward, variance-normalized triangular-array form of
the Lindeberg-Feller central limit theorem.  It states the target only; it does
not assert or prove the target.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal NNReal ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0989

universe u

/-- The truncated second moment in the normalized Lindeberg condition. -/
def truncatedSecondMoment {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Omega -> Real) (epsilon : Real) : Real :=
  integral P (fun omega => (X omega) ^ 2 * if epsilon < ‖X omega‖ then 1 else 0)

/--
A variance-normalized real triangular array.  Row `n` has `n + 1` entries, so
the unit-variance hypothesis is meaningful for the first row as well.
-/
structure NormalizedTriangularArray (Omega : Type u) [MeasurableSpace Omega] where
  probabilityMeasure : Measure Omega
  isProbabilityMeasure : IsProbabilityMeasure probabilityMeasure
  increment : (n : Nat) -> Fin (n + 1) -> Omega -> Real
  rowIndependent : forall n, iIndepFun (increment n) probabilityMeasure
  rowAEMeasurable : forall n k, AEMeasurable (increment n k) probabilityMeasure
  rowIntegrable : forall n k, Integrable (increment n k) probabilityMeasure
  rowSquareIntegrable : forall n k,
    Integrable (fun omega => (increment n k omega) ^ 2) probabilityMeasure
  rowCentered : forall n k, probabilityMeasure[increment n k] = 0
  rowVarianceNormalized : forall n,
    (∑ k : Fin (n + 1), variance (increment n k) probabilityMeasure) = 1
  lindebergCondition : forall epsilon, epsilon > 0 ->
    Tendsto
      (fun n => ∑ k : Fin (n + 1),
        truncatedSecondMoment probabilityMeasure (increment n k) epsilon)
      atTop (nhds 0)

/-- The sum of row `n`. -/
def rowSum {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) (n : Nat) (omega : Omega) : Real :=
  ∑ k : Fin (n + 1), A.increment n k omega

/--
Exact forward Lindeberg-Feller target: normalized row sums converge in
distribution to the standard Gaussian law.
-/
def Statement : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall A : NormalizedTriangularArray Omega,
      letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
      TendstoInDistribution
        (fun n => rowSum A n)
        atTop
        (id : Real -> Real)
        (fun _ => A.probabilityMeasure)
        (gaussianReal 0 1)

/-- Checked transparent presentation of the frozen target. -/
theorem statement_iff :
    Statement.{u} <->
      forall (Omega : Type u) [MeasurableSpace Omega],
        forall A : NormalizedTriangularArray Omega,
          letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
          TendstoInDistribution
            (fun n => rowSum A n)
            atTop
            (id : Real -> Real)
            (fun _ => A.probabilityMeasure)
            (gaussianReal 0 1) :=
  Iff.rfl

end Stage1Instances.THM_M_0989
