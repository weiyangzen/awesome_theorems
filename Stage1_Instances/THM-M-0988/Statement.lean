import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0988: Lindeberg-Levy central limit theorem statement

This module freezes the exact one-dimensional iid central limit theorem target
exposed by the pinned mathlib snapshot. It contains the proposition and
statement-mutation probes, not a proof of the proposition.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Filter Finset
open scoped Real Topology ProbabilityTheory

namespace Stage1Instances.THM_M_0988

universe u v

/--
The exact Lean target for the one-dimensional Lindeberg-Levy central limit
theorem, including the degenerate zero-variance case.
-/
def StatementShape : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat → Omega → Real) (Y : Omega' → Real),
    HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' →
    MemLp (X 0) 2 P →
    iIndepFun X P →
    (∀ i : Nat, IdentDistrib (X i) (X 0) P P) →
    TendstoInDistribution
      (fun (n : Nat) (omega : Omega) ↦
        (Real.sqrt (n : Real))⁻¹ *
          (∑ k ∈ Finset.range n, X k omega -
            (n : Real) * ∫ x, X 0 x ∂P))
      atTop Y (fun _ : Nat ↦ P) P'

/-! Mutation probes are intentionally proposition-valued and remain unproved. -/

/-- Mutation: omit the finite-second-moment premise. -/
def mutationRemovedSecondMoment : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat → Omega → Real) (Y : Omega' → Real),
    HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' →
    iIndepFun X P →
    (∀ i : Nat, IdentDistrib (X i) (X 0) P P) →
    TendstoInDistribution
      (fun (n : Nat) (omega : Omega) ↦
        (Real.sqrt (n : Real))⁻¹ *
          (∑ k ∈ Finset.range n, X k omega -
            (n : Real) * ∫ x, X 0 x ∂P))
      atTop Y (fun _ : Nat ↦ P) P'

/-- Mutation: require identical distribution only for the first ten coordinates. -/
def mutationFiniteIdentDistribScope : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat → Omega → Real) (Y : Omega' → Real),
    HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' →
    MemLp (X 0) 2 P →
    iIndepFun X P →
    (∀ i : Fin 10, IdentDistrib (X i) (X 0) P P) →
    TendstoInDistribution
      (fun (n : Nat) (omega : Omega) ↦
        (Real.sqrt (n : Real))⁻¹ *
          (∑ k ∈ Finset.range n, X k omega -
            (n : Real) * ∫ x, X 0 x ∂P))
      atTop Y (fun _ : Nat ↦ P) P'

/-- Mutation: silently exclude the zero-variance boundary case. -/
def mutationExcludedZeroVariance : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat → Omega → Real) (Y : Omega' → Real),
    variance (X 0) P ≠ 0 →
    HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' →
    MemLp (X 0) 2 P →
    iIndepFun X P →
    (∀ i : Nat, IdentDistrib (X i) (X 0) P P) →
    TendstoInDistribution
      (fun (n : Nat) (omega : Omega) ↦
        (Real.sqrt (n : Real))⁻¹ *
          (∑ k ∈ Finset.range n, X k omega -
            (n : Real) * ∫ x, X 0 x ∂P))
      atTop Y (fun _ : Nat ↦ P) P'

/-- Mutation: shift the square-root normalization from `n` to `n + 1`. -/
def mutationShiftedNormalization : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat → Omega → Real) (Y : Omega' → Real),
    HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P' →
    MemLp (X 0) 2 P →
    iIndepFun X P →
    (∀ i : Nat, IdentDistrib (X i) (X 0) P P) →
    TendstoInDistribution
      (fun (n : Nat) (omega : Omega) ↦
        (Real.sqrt ((n : Real) + 1))⁻¹ *
          (∑ k ∈ Finset.range n, X k omega -
            (n : Real) * ∫ x, X 0 x ∂P))
      atTop Y (fun _ : Nat ↦ P) P'

#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check StatementShape
#print StatementShape
#print mutationRemovedSecondMoment
#print mutationFiniteIdentDistribScope
#print mutationExcludedZeroVariance
#print mutationShiftedNormalization

end Stage1Instances.THM_M_0988
