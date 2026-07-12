import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# THM-M-1080 proof bodies

This module closes the zero-threshold boundary and the finite telescoping identity used by the
frozen obligation graph.  The positive-threshold package remains open: the pinned mathlib Azuma
theorem assumes `StandardBorelSpace` and conditional sub-Gaussian increments, neither of which is
available from the exact target without a new conditional Hoeffding development.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1080.Proof

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

/-- The martingale increments telescope to the endpoint difference. -/
theorem sum_increment_eq_sub (X : Nat -> Omega -> Real) (n : Nat) (omega : Omega) :
    (∑ k ∈ Finset.range n, (X (k + 1) omega - X k omega)) = X n omega - X 0 omega := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Finset.sum_range_succ, ih]
      ring

/-- The included `t = 0` branch follows solely from the probability-measure bound. -/
theorem zeroThreshold
    (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (G : Filtration Nat mOmega) (X : Nat -> Omega -> Real)
    (c : Nat -> NNReal) (hMart : Martingale X G mu) (n : Nat)
    (hBound : forall k, k < n -> ∀ᵐ omega ∂mu,
      |X (k + 1) omega - X k omega| <= (c (k + 1) : Real)) :
    mu.real {omega | (0 : Real) <= X n omega - X 0 omega} <=
      Real.exp (-((0 : Real) ^ 2) / (2 * squaredBoundSum c n)) := by
  simpa using (measureReal_le_one : mu.real {omega | (0 : Real) <= X n omega - X 0 omega} <= 1)

/-- Once the still-open positive branch is supplied, the exact frozen target follows. -/
theorem azumaUpperTail_of_positive (positive : PositiveThresholdPackage.{u}) :
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
  · exact zeroThreshold Omega mu G X c hMart n hBound
  · exact positive Omega mu G X c hMart n hBound t ht

#print axioms sum_increment_eq_sub
#print axioms zeroThreshold
#print axioms azumaUpperTail_of_positive

end Stage1Instances.THM_M_1080.Proof
