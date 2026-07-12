import Mathlib.Probability.Martingale.Basic

/-!
# THM-M-1080: Azuma's inequality statement

This module freezes the finite-horizon, one-sided Azuma bound for a real-valued martingale with
deterministic almost-sure absolute increment bounds. It supplies no proof of the inequality.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1080

universe u

/-- The sum of the squared increment bounds at steps `1, ..., n`. -/
def squaredBoundSum (c : Nat -> NNReal) (n : Nat) : Real :=
  ∑ k ∈ Finset.range n, (c (k + 1) : Real) ^ 2

/--
The canonical upper-tail Azuma inequality. The horizon includes times `0, ..., n`; its increment
hypothesis covers exactly the transitions `k -> k+1` for `k < n`.
-/
def AzumaUpperTail : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal),
      Martingale X G mu ->
      forall n : Nat,
        (forall k, k < n -> ∀ᵐ omega ∂mu,
          |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
        forall t : Real, 0 <= t ->
          mu.real {omega | t <= X n omega - X 0 omega} <=
            Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n))

/-- Public canonical target for the statement phase. -/
abbrev Statement : Prop := AzumaUpperTail.{u}

/-- Direct expansion, used to check that the public abbreviation hides no stronger hypothesis. -/
def ExpandedSourceShape : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal),
      Martingale X G mu ->
      forall n : Nat,
        (forall k, k < n -> ∀ᵐ omega ∂mu,
          |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
        forall t : Real, 0 <= t ->
          mu.real {omega | t <= X n omega - X 0 omega} <=
            Real.exp (-(t ^ 2) /
              (2 * ∑ k ∈ Finset.range n, (c (k + 1) : Real) ^ 2))

theorem statement_iff_expandedSourceShape :
    AzumaUpperTail.{u} ↔ ExpandedSourceShape.{u} := by
  simp only [AzumaUpperTail, ExpandedSourceShape, squaredBoundSum]

-- Deliberately non-equivalent statement mutations retained as boundary checks.
def MutationRemovedMartingale : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (X : Nat -> Omega -> Real) (c : Nat -> NNReal) (n : Nat),
      (forall k, k < n -> ∀ᵐ omega ∂mu,
        |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
      forall t : Real, 0 <= t ->
        mu.real {omega | t <= X n omega - X 0 omega} <=
          Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n))

def MutationChangedDomain : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Int)
    (c : Nat -> NNReal), StronglyAdapted G X -> True

def MutationUniformBinderScope : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real) (c : NNReal),
      Martingale X G mu -> forall n : Nat,
        (forall k, k < n -> ∀ᵐ omega ∂mu,
          |X (k + 1) omega - X k omega| <= (c : Real)) ->
        forall t : Real, 0 <= t -> True

def MutationPositiveThresholdOnly : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal), Martingale X G mu -> forall n : Nat,
      (forall k, k < n -> ∀ᵐ omega ∂mu,
        |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
      forall t : Real, 0 < t ->
        mu.real {omega | t <= X n omega - X 0 omega} <=
          Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n))

#print AzumaUpperTail
#print ExpandedSourceShape
#print MutationRemovedMartingale
#print MutationChangedDomain
#print MutationUniformBinderScope
#print MutationPositiveThresholdOnly

end Stage1Instances.THM_M_1080
