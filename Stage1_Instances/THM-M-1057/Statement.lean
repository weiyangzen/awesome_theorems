import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
The statement-only, ergodic real-valued form of Kingman's subadditive ergodic
theorem selected by the rev-5.6 intake.  This file contains no proof of the
target.
-/

noncomputable section

open Filter Function MeasureTheory Set
open scoped MeasureTheory Topology

namespace Stage1Instances.THM_M_1057

universe u

structure KingmanData (Omega : Type u) [MeasurableSpace Omega] where
  measure : Measure Omega
  transformation : Omega -> Omega
  process : Nat -> Omega -> Real
  isProbability : IsProbabilityMeasure measure
  isErgodic : Ergodic transformation measure
  integrable : forall n, Integrable (process n) measure
  zero : process 0 =ᵐ[measure] fun _ => 0
  subadditive : forall m n,
    process (m + n) ≤ᵐ[measure]
      fun omega => process m omega + process n ((transformation^[m]) omega)
  normalizedExpectationsBoundedBelow : exists C : Real, forall n,
    n ≠ 0 -> C ≤ (∫ omega, process n omega ∂measure) / (n : Real)

def normalizedProcess {Omega : Type u} [MeasurableSpace Omega]
    (P : KingmanData Omega) (n : Nat) (omega : Omega) : Real :=
  P.process n omega / (n : Real)

def expectedAverage {Omega : Type u} [MeasurableSpace Omega]
    (P : KingmanData Omega) (n : Nat) : Real :=
  (∫ omega, P.process n omega ∂P.measure) / (n : Real)

def kingmanValue {Omega : Type u} [MeasurableSpace Omega]
    (P : KingmanData Omega) : Real :=
  sInf (expectedAverage P '' Ici 1)

def KingmanTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : KingmanData Omega),
    ∀ᵐ omega ∂P.measure,
      Tendsto (fun n => normalizedProcess P n omega) atTop (𝓝 (kingmanValue P))

-- A fully expanded encoding used to kernel-check the selected packaging.
def ExpandedSourceShape : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : KingmanData Omega),
    ∀ᵐ omega ∂P.measure,
      Tendsto
        (fun n : Nat => P.process n omega / (n : Real))
        atTop
        (𝓝 (sInf ((fun n : Nat =>
          (∫ omega, P.process n omega ∂P.measure) / (n : Real)) '' Ici 1)))

theorem kingmanTarget_iff_expandedSourceShape :
    KingmanTarget.{u} <-> ExpandedSourceShape.{u} := by
  rfl

-- Structural mutations.  The statement validator requires distinct elaborated types.
def mutationRemovedLowerBound : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
      (measure : Measure Omega) (transformation : Omega -> Omega)
      (process : Nat -> Omega -> Real),
    IsProbabilityMeasure measure ->
    Ergodic transformation measure ->
    (forall n, Integrable (process n) measure) ->
    process 0 =ᵐ[measure] (fun _ => 0) ->
    (forall m n, process (m + n) ≤ᵐ[measure]
      fun omega => process m omega + process n ((transformation^[m]) omega)) ->
    ∀ᵐ omega ∂measure,
      Tendsto (fun n => process n omega / (n : Real)) atTop
        (𝓝 (sInf ((fun n : Nat => (∫ omega, process n omega ∂measure) / (n : Real)) '' Ici 1)))

def mutationChangedDomainToRat : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    (Nat -> Omega -> Rat) -> True

def mutationChangedBinderScope : Prop :=
  exists Omega : Type u, Nonempty (MeasurableSpace Omega)

def mutationIncludesZeroInInfimum : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : KingmanData Omega),
    ∀ᵐ omega ∂P.measure,
      Tendsto (fun n => normalizedProcess P n omega) atTop
        (𝓝 (sInf (range (expectedAverage P))))

theorem zeroIndexNormalizationBoundary {Omega : Type u} [MeasurableSpace Omega]
    (P : KingmanData Omega) (omega : Omega) :
    normalizedProcess P 0 omega = 0 := by
  simp [normalizedProcess]

theorem positiveIndexMembershipBoundary {Omega : Type u} [MeasurableSpace Omega]
    (P : KingmanData Omega) : expectedAverage P 1 ∈ expectedAverage P '' Ici 1 := by
  exact ⟨1, by simp, rfl⟩

#print Stage1Instances.THM_M_1057.KingmanTarget

end Stage1Instances.THM_M_1057
