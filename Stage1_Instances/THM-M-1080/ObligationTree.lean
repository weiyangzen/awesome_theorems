import Mathlib.Probability.Martingale.Basic

/-!
# THM-M-1080 conditional obligation composition

This file checks only the final case recomposition for the frozen Azuma
architecture.  The positive-threshold and zero-threshold packages are explicit
open hypotheses; neither is implemented here.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1080.ObligationTree

universe u

def squaredBoundSum (c : Nat -> NNReal) (n : Nat) : Real :=
  ∑ k ∈ Finset.range n, (c (k + 1) : Real) ^ 2

def PositiveThresholdPackage : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal),
      Martingale X G mu ->
      forall n : Nat,
        (forall k, k < n -> ∀ᵐ omega ∂mu,
          |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
        forall t : Real, 0 < t ->
          mu.real {omega | t <= X n omega - X 0 omega} <=
            Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n))

def ZeroThresholdPackage : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal),
      Martingale X G mu ->
      forall n : Nat,
        (forall k, k < n -> ∀ᵐ omega ∂mu,
          |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
        mu.real {omega | (0 : Real) <= X n omega - X 0 omega} <=
          Real.exp (-((0 : Real) ^ 2) / (2 * squaredBoundSum c n))

/-- Exact recomposition of the two threshold branches into the frozen target. -/
theorem azumaUpperTail_of_threshold_packages
    (positive : PositiveThresholdPackage.{u})
    (zero : ZeroThresholdPackage.{u}) :
    forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
      [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
      (c : Nat -> NNReal),
        Martingale X G mu ->
        forall n : Nat,
          (forall k, k < n -> ∀ᵐ omega ∂mu,
            |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) ->
          forall t : Real, 0 <= t ->
            mu.real {omega | t <= X n omega - X 0 omega} <=
              Real.exp (-(t ^ 2) / (2 * squaredBoundSum c n)) := by
  intro Omega mOmega mu hmu G X c hMart n hBound t ht
  rcases ht.eq_or_lt with rfl | ht
  · exact zero Omega mu G X c hMart n hBound
  · exact positive Omega mu G X c hMart n hBound t ht

#print axioms azumaUpperTail_of_threshold_packages

end Stage1Instances.THM_M_1080.ObligationTree
