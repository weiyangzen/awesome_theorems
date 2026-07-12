import Mathlib.Probability.BorelCantelli

/-!
# THM-M-1009 conditional obligation composition

This module checks the binder-level composition interface frozen by the
obligation registry.  The mathematical lower-bound premise remains explicit;
this file neither supplies nor credits its proof.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

universe u

namespace Stage1Instances.THM_M_1009.ObligationTree

def partialEventMass {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  Finset.sum (Finset.range n) fun k => mu.real (A k)

def pairwiseEventMass {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  Finset.sum (Finset.range n) fun i =>
    Finset.sum (Finset.range n) fun j => mu.real (A i ∩ A j)

def eventMassRatio {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  (partialEventMass mu A n) ^ 2 / pairwiseEventMass mu A n

def MeasurableEvents {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) : Prop := forall n, MeasurableSet (A n)

def DivergentMass {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) : Prop :=
  Tendsto (partialEventMass mu A) atTop atTop

def LowerBound {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) : Prop :=
  Filter.limsup (eventMassRatio mu A) atTop <= mu.real (limsup A atTop)

def Root : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu] (A : Nat -> Set Omega),
      MeasurableEvents A -> DivergentMass mu A -> LowerBound mu A

/-- Binder and hypothesis composition certificate. The `assemble` premise is
the still-open mathematical assembly obligation recorded by the registry. -/
theorem root_compose
    (assemble : forall (Omega : Type u) [MeasurableSpace Omega]
      (mu : Measure Omega) [IsProbabilityMeasure mu] (A : Nat -> Set Omega),
        MeasurableEvents A -> DivergentMass mu A -> LowerBound mu A) : Root.{u} := by
  intro Omega _ mu _ A hmeas hdiv
  exact assemble Omega mu A hmeas hdiv

@[simp] theorem zero_ratio {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) : eventMassRatio mu A 0 = 0 := by
  simp [eventMassRatio, partialEventMass, pairwiseEventMass]

#print axioms root_compose

end Stage1Instances.THM_M_1009.ObligationTree
