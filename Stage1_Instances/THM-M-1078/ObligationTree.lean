import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.Probability.Martingale.Basic

/-! Checked conditional composition for the frozen THM-M-1078 architecture.

This file repeats the already frozen target expression because the target dossier is outside the
Lake package and has no local olean. `target_iff_statement_target` is generated only for the
combined validation input, where `Statement.lean` text precedes this file's body.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace Stage1Instances.THM_M_1078.ObligationTree

universe u

def martingaleTransform {Omega : Type*} [MeasurableSpace Omega]
    (f v : Nat -> Omega -> Real) (n : Nat) : Omega -> Real :=
  fun omega => (Finset.range n).sum
    (fun k => v (k + 1) omega * (f (k + 1) omega - f k omega))

def MartingaleTransformTarget : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    exists C : Real, 0 <= C ∧
      forall (Omega : Type*) (m : MeasurableSpace Omega) (mu : Measure Omega)
        [IsProbabilityMeasure mu] (F : Filtration Nat m)
        (f v : Nat -> Omega -> Real) (n : Nat),
        Martingale f F mu -> IsPredictable F v ->
        (forall k omega, abs (v k omega) <= 1) -> MemLp (f n) p mu ->
        lpNorm (martingaleTransform f v n) p mu <= C * lpNorm (f n) p mu

/-- Earlier-time integrability interface, universe-polymorphic in the probability space. -/
def EarlierMemLpBridge : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    forall (Omega : Type u) (m : MeasurableSpace Omega) (mu : Measure Omega)
      [IsProbabilityMeasure mu] (F : Filtration Nat m)
      (f : Nat -> Omega -> Real) (n : Nat),
      Martingale f F mu -> MemLp (f n) p mu -> forall k, MemLp (f k) p mu

/-- Local interface expected after the external theorem and all representation bridges have been
integrated. It deliberately retains the candidate's stronger all-time `MemLp` premise. -/
def AllTimeMemLpTransformBound : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    exists C : Real, 0 <= C ∧
      forall (Omega : Type*) (m : MeasurableSpace Omega) (mu : Measure Omega)
        [IsProbabilityMeasure mu] (F : Filtration Nat m)
        (f v : Nat -> Omega -> Real) (n : Nat),
        Martingale f F mu ->
        IsPredictable F v ->
        (forall k omega, abs (v k omega) <= 1) ->
        (forall k, MemLp (f k) p mu) ->
        lpNorm (martingaleTransform f v n) p mu <= C * lpNorm (f n) p mu

/-- Checked final composition. Both arguments are open obligations: the integrated stronger body
and the terminal-to-all-time `MemLp` bridge. This theorem supplies no proof of either premise. -/
theorem root_of_allTimeMemLpTransformBound
    (body : AllTimeMemLpTransformBound.{u})
    (earlierMemLp : EarlierMemLpBridge.{u}) :
    MartingaleTransformTarget.{u} := by
  intro p hp hpinfty
  obtain ⟨C, hC, hbody⟩ := body p hp hpinfty
  refine ⟨C, hC, ?_⟩
  intro Omega m mu _ F f v n hmart hpredict hbound hterminal
  exact hbody Omega m mu F f v n hmart hpredict hbound
    (earlierMemLp p hp hpinfty Omega m mu F f n hmart hterminal)

#check root_of_allTimeMemLpTransformBound
#print axioms root_of_allTimeMemLpTransformBound

end Stage1Instances.THM_M_1078.ObligationTree
