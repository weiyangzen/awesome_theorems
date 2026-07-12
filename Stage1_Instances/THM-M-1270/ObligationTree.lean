import Mathlib.Topology.Semicontinuity.Basic

/-!
# THM-M-1270 obligation-tree composition boundary

This module checks only the child-to-root interface frozen by the obligation
registry.  `WitnessPackage` is an explicit premise; no Ekeland witness is
constructed in this phase.
-/

open Set

namespace Stage1Instances.THM_M_1270.ObligationTree

universe u

def ApproximateMinimizer {X : Type u} (f : X -> Real) (epsilon : Real) (x0 : X) : Prop :=
  forall x : X, f x0 <= f x + epsilon

def Root : Prop :=
  forall (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 : X),
    LowerSemicontinuous f -> BddBelow (range f) ->
      0 < epsilon -> 0 < lambda -> ApproximateMinimizer f epsilon x0 ->
        exists v : X, f v <= f x0 /\ dist v x0 <= lambda /\
          forall y : X, y ≠ v -> f v < f y + (epsilon / lambda) * dist v y

def ValueImprovement {X : Type u} (f : X -> Real) (x0 v : X) : Prop :=
  f v <= f x0

def Localization {X : Type u} [PseudoMetricSpace X]
    (lambda : Real) (x0 v : X) : Prop :=
  dist v x0 <= lambda

def StrictPenalizedMinimality {X : Type u} [PseudoMetricSpace X]
    (f : X -> Real) (epsilon lambda : Real) (v : X) : Prop :=
  forall y : X, y ≠ v -> f v < f y + (epsilon / lambda) * dist v y

/-- Exact output interface of the descent construction and limit argument. -/
def WitnessPackage {X : Type u} [MetricSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 : X) : Prop :=
  exists v : X,
    ValueImprovement f x0 v /\
      Localization lambda x0 v /\
        StrictPenalizedMinimality f epsilon lambda v

/-- Checked composition from the frozen hard-core interface to the exact root. -/
theorem root_compose
    (hardCore : forall (X : Type u) [MetricSpace X] [CompleteSpace X]
      (f : X -> Real) (epsilon lambda : Real) (x0 : X),
      LowerSemicontinuous f -> BddBelow (range f) ->
        0 < epsilon -> 0 < lambda -> ApproximateMinimizer f epsilon x0 ->
          WitnessPackage f epsilon lambda x0) : Root.{u} := by
  intro X _ _ f epsilon lambda x0 hlsc hbdd hepsilon hlambda happrox
  rcases hardCore X f epsilon lambda x0 hlsc hbdd hepsilon hlambda happrox with
    ⟨v, himprove, hlocal, hstrict⟩
  exact ⟨v, himprove, hlocal, hstrict⟩

end Stage1Instances.THM_M_1270.ObligationTree

#check LowerSemicontinuous
#check CauchySeq
#check CompleteSpace

#print axioms Stage1Instances.THM_M_1270.ObligationTree.root_compose
