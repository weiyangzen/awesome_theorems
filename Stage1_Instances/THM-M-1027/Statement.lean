import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Independence.Process.HasIndepIncrements

/-!
# THM-M-1027: exact Wiener-process existence statement

This module freezes and tests the statement boundary only. It does not construct
a Wiener process.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal

namespace Stage1Instances.THM_M_1027

universe u

/-- The one-sided time domain of a standard Wiener process. -/
abbrev Time := NNReal

/-- A real-valued stochastic process indexed by nonnegative real time. -/
abbrev RealProcess (Omega : Type u) := Time -> Omega -> Real

/-- The nonnegative variance of an increment over ordered times. -/
def IncrementVariance (s t : Time) (hst : s <= t) : NNReal :=
  ⟨(t : Real) - (s : Real), sub_nonneg.mpr (by exact_mod_cast hst)⟩

/-- The standard Wiener laws on a fixed probability space. -/
structure IsWienerProcess (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) (W : RealProcess Omega) : Prop where
  measurable : forall t : Time, Measurable (W t)
  startsAtZero : Filter.Eventually (fun omega => W 0 omega = 0) (ae P)
  incrementLaw : forall {s t : Time}, (hst : s <= t) ->
    HasLaw (fun omega => W t omega - W s omega)
      (gaussianReal 0 (IncrementVariance s t hst)) P
  independentIncrements : HasIndepIncrements W P
  continuousPaths :
    Filter.Eventually (fun omega => Continuous (fun t : Time => W t omega)) (ae P)

/-- The exact intake-selected existence claim for a standard Wiener process. -/
def WienerExistenceTarget : Prop :=
  Exists fun (Omega : Type u) =>
    Exists fun (_m : MeasurableSpace Omega) =>
      Exists fun (P : Measure Omega) =>
        Exists fun (W : RealProcess Omega) =>
          IsProbabilityMeasure P /\ IsWienerProcess Omega P W

/-- Direct expansion of the intake's canonical formal claim. -/
def PinnedIntakeSourceShape : Prop :=
  Exists fun (Omega : Type u) =>
    Exists fun (_m : MeasurableSpace Omega) =>
      Exists fun (P : Measure Omega) =>
        Exists fun (W : Time -> Omega -> Real) =>
          IsProbabilityMeasure P /\
          (forall t : Time, Measurable (W t)) /\
          Filter.Eventually (fun omega => W 0 omega = 0) (ae P) /\
          (forall {s t : Time}, (hst : s <= t) ->
            HasLaw (fun omega => W t omega - W s omega)
              (gaussianReal 0 (IncrementVariance s t hst)) P) /\
          HasIndepIncrements W P /\
          Filter.Eventually
            (fun omega => Continuous (fun t : Time => W t omega)) (ae P)

/-- Checked transport between the structured target and its direct intake expansion. -/
theorem wienerExistenceTarget_iff_pinnedIntakeSourceShape :
    WienerExistenceTarget.{u} <-> PinnedIntakeSourceShape.{u} := by
  constructor
  · rintro ⟨Omega, m, P, W, hP, hW⟩
    exact ⟨Omega, m, P, W, hP, hW.measurable, hW.startsAtZero,
      hW.incrementLaw, hW.independentIncrements, hW.continuousPaths⟩
  · rintro ⟨Omega, m, P, W, hP, hmeas, hzero, hlaw, hindep, hcont⟩
    exact ⟨Omega, m, P, W, hP, ⟨hmeas, hzero, hlaw, hindep, hcont⟩⟩

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationTwoSidedTime : Prop :=
  Exists fun (Omega : Type u) =>
    Exists fun (_m : MeasurableSpace Omega) =>
      Exists fun (P : Measure Omega) => Exists fun (_W : Real -> Omega -> Real) =>
        IsProbabilityMeasure P

def mutationRemovedContinuity : Prop :=
  Exists fun (Omega : Type u) =>
    Exists fun (_m : MeasurableSpace Omega) =>
      Exists fun (P : Measure Omega) => Exists fun (W : RealProcess Omega) =>
        IsProbabilityMeasure P /\
        (forall t : Time, Measurable (W t)) /\
        Filter.Eventually (fun omega => W 0 omega = 0) (ae P) /\
        (forall {s t : Time}, (hst : s <= t) ->
          HasLaw (fun omega => W t omega - W s omega)
            (gaussianReal 0 (IncrementVariance s t hst)) P) /\
        HasIndepIncrements W P

def mutationRemovedIndependentIncrements : Prop :=
  Exists fun (Omega : Type u) =>
    Exists fun (_m : MeasurableSpace Omega) =>
      Exists fun (P : Measure Omega) => Exists fun (W : RealProcess Omega) =>
        IsProbabilityMeasure P /\
        (forall t : Time, Measurable (W t)) /\
        Filter.Eventually (fun omega => W 0 omega = 0) (ae P) /\
        (forall {s t : Time}, (hst : s <= t) ->
          HasLaw (fun omega => W t omega - W s omega)
            (gaussianReal 0 (IncrementVariance s t hst)) P) /\
        Filter.Eventually
          (fun omega => Continuous (fun t : Time => W t omega)) (ae P)

def mutationUnitVarianceAtEveryIncrement : Prop :=
  Exists fun (Omega : Type u) =>
    Exists fun (_m : MeasurableSpace Omega) =>
      Exists fun (P : Measure Omega) => Exists fun (W : RealProcess Omega) =>
        IsProbabilityMeasure P /\
        forall {s t : Time}, s <= t ->
          HasLaw (fun omega => W t omega - W s omega) (gaussianReal 0 1) P

/-- Equal times have zero increment variance. -/
theorem incrementVariance_self (t : Time) : IncrementVariance t t le_rfl = 0 := by
  apply NNReal.eq
  change (t : Real) - (t : Real) = 0
  exact sub_self _

end Stage1Instances.THM_M_1027

set_option pp.explicit true in
#print Stage1Instances.THM_M_1027.WienerExistenceTarget
