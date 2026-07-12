import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.Probability.Martingale.Basic

/-!
# THM-M-1078: exact martingale-transform statement

This module freezes the finite-horizon, discrete-time qualitative martingale-transform inequality.
It contains no proof of that inequality.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace Stage1Instances.THM_M_1078

universe u

/-- The transform through time `n`.  The multiplier at time `k + 1` is measurable at time `k`
because the whole multiplier process is predictable. -/
def martingaleTransform {Omega : Type*} [MeasurableSpace Omega]
    (f v : Nat -> Omega -> Real) (n : Nat) : Omega -> Real :=
  fun omega => (Finset.range n).sum
    (fun k => v (k + 1) omega * (f (k + 1) omega - f k omega))

/-- For every non-endpoint exponent there is a finite constant, depending only on the exponent,
which bounds every finite predictable scalar transform of every real martingale. -/
def MartingaleTransformTarget : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    exists C : Real, 0 <= C ∧
      forall (Omega : Type*) (m : MeasurableSpace Omega) (mu : Measure Omega)
        [IsProbabilityMeasure mu] (F : Filtration Nat m)
        (f v : Nat -> Omega -> Real) (n : Nat),
        Martingale f F mu ->
        IsPredictable F v ->
        (forall k omega, abs (v k omega) <= 1) ->
        MemLp (f n) p mu ->
        lpNorm (martingaleTransform f v n) p mu <= C * lpNorm (f n) p mu

/-- Direct expansion used to ensure that the named target hides no weaker conclusion. -/
def ExpandedSourceShape : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    exists C : Real, 0 <= C ∧
      forall (Omega : Type*) (m : MeasurableSpace Omega) (mu : Measure Omega)
        [IsProbabilityMeasure mu] (F : Filtration Nat m)
        (f v : Nat -> Omega -> Real) (n : Nat),
        Martingale f F mu ->
        IsPredictable F v ->
        (forall k omega, abs (v k omega) <= 1) ->
        MemLp (f n) p mu ->
        lpNorm
          (fun omega => (Finset.range n).sum
            (fun k => v (k + 1) omega * (f (k + 1) omega - f k omega)))
          p mu <= C * lpNorm (f n) p mu

theorem target_iff_expandedSourceShape :
    MartingaleTransformTarget.{u} <-> ExpandedSourceShape.{u} := by
  change ExpandedSourceShape.{u} <-> ExpandedSourceShape.{u}
  rfl

-- Deliberately changed statements, separately elaborated as boundary checks.
def mutationRemovedPredictability : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    exists C : Real, forall (Omega : Type*) (m : MeasurableSpace Omega) (mu : Measure Omega)
      [IsProbabilityMeasure mu] (F : Filtration Nat m) (f v : Nat -> Omega -> Real) (n : Nat),
      Martingale f F mu -> MemLp (f n) p mu ->
      lpNorm (martingaleTransform f v n) p mu <= C * lpNorm (f n) p mu

def mutationFixedExponentTwo : Prop :=
  exists C : Real, forall (Omega : Type*) (m : MeasurableSpace Omega) (mu : Measure Omega)
    [IsProbabilityMeasure mu] (F : Filtration Nat m) (f v : Nat -> Omega -> Real) (n : Nat),
    Martingale f F mu -> IsPredictable F v -> (forall k omega, abs (v k omega) <= 1) ->
    MemLp (f n) 2 mu ->
    lpNorm (martingaleTransform f v n) 2 mu <= C * lpNorm (f n) 2 mu

def mutationAssumedBound : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    exists C : Real, MartingaleTransformTarget.{u} -> 0 <= C

end Stage1Instances.THM_M_1078

set_option pp.explicit true in
#print Stage1Instances.THM_M_1078.MartingaleTransformTarget
