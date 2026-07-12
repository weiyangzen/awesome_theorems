import Mathlib.Probability.Process.Kolmogorov
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability
import Mathlib.Topology.MetricSpace.Holder

/-! Conditional composition harness for the frozen THM-M-1083 obligation tree. -/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1083.ObligationTree

universe u

abbrev TimeInterval (T : Real) := Set.Icc (0 : Real) T
abbrev RealProcess (T : Real) (Omega : Type u) := TimeInterval T -> Omega -> Real

def IsModification {T : Real} {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X Y : RealProcess T Omega) : Prop :=
  forall t, X t =ᵐ[P] Y t

def HasHolderPath {T : Real} {Omega : Type u} (Y : RealProcess T Omega)
    (gamma : NNReal) (omega : Omega) : Prop :=
  exists K : NNReal, HolderWith K gamma (fun t => Y t omega)

def KolmogorovContinuity : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : Measure Omega) [IsProbabilityMeasure P]
      (T alpha beta : Real) (C : NNReal) (X : RealProcess T Omega),
    0 < T ->
    0 < alpha ->
    0 < beta ->
    (forall t, Measurable (X t)) ->
    (forall s t,
      ∫⁻ omega, edist (X s omega) (X t omega) ^ alpha ∂P <=
        (C : ENNReal) * edist s t ^ (1 + beta)) ->
    exists Y : RealProcess T Omega,
      IsModification P X Y ∧
        forall gamma : NNReal,
          0 < gamma ->
          (gamma : Real) < beta / alpha ->
          ∀ᵐ omega ∂P, HasHolderPath Y gamma omega

/-- Exact final composition. `engine` is the open registered proof package, not a proof body. -/
theorem kolmogorovContinuity_of_engine
    (engine :
      forall (Omega : Type u) [MeasurableSpace Omega] (P : Measure Omega)
          [IsProbabilityMeasure P] (T alpha beta : Real) (C : NNReal)
          (X : RealProcess T Omega),
        0 < T -> 0 < alpha -> 0 < beta ->
        (forall t, Measurable (X t)) ->
        (forall s t,
          ∫⁻ omega, edist (X s omega) (X t omega) ^ alpha ∂P <=
            (C : ENNReal) * edist s t ^ (1 + beta)) ->
        exists Y : RealProcess T Omega,
          IsModification P X Y ∧
            forall gamma : NNReal, 0 < gamma -> (gamma : Real) < beta / alpha ->
              ∀ᵐ omega ∂P, HasHolderPath Y gamma omega) :
    KolmogorovContinuity.{u} := by
  intro Omega _ P _ T alpha beta C X hT ha hb hmeas hmoment
  exact engine Omega P T alpha beta C X hT ha hb hmeas hmoment

#check kolmogorovContinuity_of_engine

end Stage1Instances.THM_M_1083.ObligationTree
