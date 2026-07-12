import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0990: Lyapunov central limit theorem statement

This module freezes the triangular-array proposition selected by the rev-5.6
intake. It elaborates the target and statement mutations, but does not prove
the Lyapunov central limit theorem.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped Real Topology ProbabilityTheory

namespace Stage1Instances.THM_M_0990

universe u v

/-- Sum of the variances of the first `n` variables in row `n`. -/
def rowVarianceSum {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real) (n : Nat) : Real :=
  ∑ k ∈ Finset.range n, variance (X n k) P

/-- The positive square-root normalization for row `n`. -/
def rowScale {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real) (n : Nat) : Real :=
  Real.sqrt (rowVarianceSum P X n)

/-- Entry `k` of row `n`, centered by its expectation. -/
def centered {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (n k : Nat) (omega : Omega) : Real :=
  X n k omega - ∫ x, X n k x ∂P

/-- The textbook Lyapunov ratio with exponent `2 + delta`. -/
def lyapunovRatio {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (delta : Real) (n : Nat) : Real :=
  (Real.rpow (rowScale P X n) (2 + delta))⁻¹ *
    ∑ k ∈ Finset.range n,
      ∫ omega, Real.rpow |centered P X n k omega| (2 + delta) ∂P

/-- The centered row sum divided by its row standard deviation. -/
def normalizedRowSum {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (n : Nat) (omega : Omega) : Real :=
  (rowScale P X n)⁻¹ * ∑ k ∈ Finset.range n, centered P X n k omega

/--
The exact Lean target for the Lyapunov central limit theorem. Rows use their
first `n` entries; independence is joint within each whole row and hence in
particular holds for that finite prefix. Positivity of the row variance scale
is required eventually, exactly where the asymptotic normalization is used.
-/
def StatementShape : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat -> Nat -> Omega -> Real) (Y : Omega' -> Real) (delta : Real),
    HasLaw Y (gaussianReal 0 1) P' ->
    0 < delta ->
    (∀ n k : Nat, Measurable (X n k)) ->
    (∀ n : Nat, iIndepFun (X n) P) ->
    (∀ n k : Nat, MemLp (X n k) 2 P) ->
    (∀ n k : Nat,
      Integrable (fun omega => Real.rpow |centered P X n k omega| (2 + delta)) P) ->
    (∀ᶠ n : Nat in atTop, 0 < rowVarianceSum P X n) ->
    Tendsto (lyapunovRatio P X delta) atTop (nhds 0) ->
    TendstoInDistribution
      (normalizedRowSum P X) atTop Y (fun _ : Nat => P) P'

/-! The mutations are unproved propositions used to make statement drift visible. -/

/-- Mutation: the Lyapunov condition is removed. -/
def mutationRemovedLyapunovCondition : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (X : Nat -> Nat -> Omega -> Real) (delta : Real),
    0 < delta ->
    (∀ n : Nat, iIndepFun (X n) P) ->
    (∀ᶠ n : Nat in atTop, 0 < rowVarianceSum P X n) ->
    True

/-- Mutation: the conclusion is normalized by the variance sum, not its square root. -/
def mutationVarianceNormalization : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat -> Nat -> Omega -> Real) (Y : Omega' -> Real),
    TendstoInDistribution
      (fun n omega => (rowVarianceSum P X n)⁻¹ *
        ∑ k ∈ Finset.range n, centered P X n k omega)
      atTop Y (fun _ : Nat => P) P'

/-- Mutation: independence is required only pairwise, not jointly. -/
def mutationPairwiseIndependence : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real),
    ∀ n i j : Nat, i ≠ j -> IndepFun (X n i) (X n j) P

#check StatementShape
#print StatementShape
#print mutationRemovedLyapunovCondition
#print mutationVarianceNormalization
#print mutationPairwiseIndependence

end Stage1Instances.THM_M_0990
