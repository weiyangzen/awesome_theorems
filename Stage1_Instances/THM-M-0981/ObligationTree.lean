import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# THM-M-0981 conditional obligation composition

This module checks the child-to-root composition selected by the frozen
architecture. The three Kolmogorov clauses remain explicit premises, so this
file does not claim that the canonical theorem has been proved.
-/

open Function MeasureTheory Set

namespace Stage1Instances.THM_M_0981.ObligationTree

universe u

def CanonicalRoot (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, IsProbabilityMeasure P ->
    P (∅ : Set Omega) = 0 /\ P univ = 1 /\
      forall A : Nat -> Set Omega,
        (forall n, MeasurableSet (A n)) -> Pairwise (Disjoint on A) ->
          P (iUnion A) = tsum (fun n => P (A n))

def EmptyEventPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : Measure Omega),
    P (∅ : Set Omega) = 0

def UnitMassPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : Measure Omega),
    IsProbabilityMeasure P -> P univ = 1

def CountableAdditivityPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : Measure Omega)
    (A : Nat -> Set Omega),
      (forall n, MeasurableSet (A n)) -> Pairwise (Disjoint on A) ->
        P (iUnion A) = tsum (fun n => P (A n))

/-- Exact conditional composition. Each clause package is consumed, and no
measure-theory theorem is invoked inside this composition certificate. -/
theorem root_compose
    (emptyEvent : EmptyEventPackage.{u})
    (unitMass : UnitMassPackage.{u})
    (countableAdditivity : CountableAdditivityPackage.{u}) :
    forall (Omega : Type u) [MeasurableSpace Omega],
      CanonicalRoot Omega := by
  intro Omega _ P hP
  refine And.intro (emptyEvent Omega P) (And.intro (unitMass Omega P hP) ?_)
  intro A hmeas hdisjoint
  exact countableAdditivity Omega P A hmeas hdisjoint

#check measure_empty
#check IsProbabilityMeasure.measure_univ
#check measure_iUnion
#print axioms root_compose

end Stage1Instances.THM_M_0981.ObligationTree
