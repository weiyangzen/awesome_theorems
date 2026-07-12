import Mathlib.Probability.BorelCantelli

/-!
# THM-M-1009: Erdos-Renyi second lemma

This module freezes the generalized Borel-Cantelli lower-bound proposition.
It contains no proof of that proposition.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

universe u

namespace Stage1Instances.THM_M_1009

/-- The finite real sum of the probabilities of the first `n` events. -/
def partialEventMass {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  Finset.sum (Finset.range n) fun k => mu.real (A k)

/-- The ordered double sum of the first `n` pairwise intersection probabilities. -/
def pairwiseEventMass {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  Finset.sum (Finset.range n) fun i =>
    Finset.sum (Finset.range n) fun j => mu.real (A i ∩ A j)

/-- The finite second-moment ratio, with ordinary real division. -/
def eventMassRatio {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  (partialEventMass mu A n) ^ 2 / pairwiseEventMass mu A n

/--
The canonical lower-bound formulation selected at intake: for measurable
events whose probability partial sums diverge, the probability of their
limsup bounds the limsup of the finite second-moment ratios from below.
-/
def ErdosRenyiLowerBoundTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu] (A : Nat -> Set Omega),
      (forall n : Nat, MeasurableSet (A n)) ->
        Tendsto (partialEventMass mu A) atTop atTop ->
          Filter.limsup (eventMassRatio mu A) atTop <=
            mu.real (limsup A atTop)

/-- Pointwise grouping used to check the closed-target binder transport. -/
def PointwiseLowerBoundTarget {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu] (A : Nat -> Set Omega) : Prop :=
  (forall n : Nat, MeasurableSet (A n)) ->
    Tendsto (partialEventMass mu A) atTop atTop ->
      Filter.limsup (eventMassRatio mu A) atTop <= mu.real (limsup A atTop)

/-- Checked regrouping of the canonical proposition. -/
theorem lowerBoundTarget_iff_pointwise :
    ErdosRenyiLowerBoundTarget.{u} <->
      forall (Omega : Type u) [MeasurableSpace Omega]
        (mu : Measure Omega) [IsProbabilityMeasure mu] (A : Nat -> Set Omega),
          PointwiseLowerBoundTarget mu A := by
  rfl

-- Structural mutations are elaborated and distinguished by `check_statement.py`.
def mutationRemovedMeasurability : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu] (A : Nat -> Set Omega),
      Tendsto (partialEventMass mu A) atTop atTop ->
        Filter.limsup (eventMassRatio mu A) atTop <= mu.real (limsup A atTop)

def mutationChangedMeasureDomain : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu] (A : Nat -> Set Omega),
      (forall n : Nat, MeasurableSet (A n)) ->
        Tendsto (partialEventMass mu A) atTop atTop ->
          Filter.limsup (eventMassRatio mu A) atTop <= mu.real (limsup A atTop)

def mutationChangedBinderScope : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu],
      (forall A : Nat -> Set Omega, forall n : Nat, MeasurableSet (A n)) ->
        forall A : Nat -> Set Omega,
          Tendsto (partialEventMass mu A) atTop atTop ->
            Filter.limsup (eventMassRatio mu A) atTop <= mu.real (limsup A atTop)

/-- Boundary mutation: use inclusive initial segments `range (n + 1)`. -/
def mutationInclusiveInitialSegments : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu] (A : Nat -> Set Omega),
      (forall n : Nat, MeasurableSet (A n)) ->
        Tendsto (fun n => partialEventMass mu A (n + 1)) atTop atTop ->
          Filter.limsup (fun n => eventMassRatio mu A (n + 1)) atTop <=
            mu.real (limsup A atTop)

@[simp] theorem partialEventMass_zero {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) : partialEventMass mu A 0 = 0 := by
  simp [partialEventMass]

@[simp] theorem pairwiseEventMass_zero {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) : pairwiseEventMass mu A 0 = 0 := by
  simp [pairwiseEventMass]

@[simp] theorem eventMassRatio_zero {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) : eventMassRatio mu A 0 = 0 := by
  simp [eventMassRatio]

end Stage1Instances.THM_M_1009

set_option pp.explicit true in
#print Stage1Instances.THM_M_1009.ErdosRenyiLowerBoundTarget
