import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1143: Liouville theorem for bounded harmonic functions

This module freezes the canonical proposition. It does not prove it.
-/

open Bornology Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1143

/-- Real Euclidean `n`-space, with its mathlib inner-product structure. -/
abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/--
Every bounded real-valued harmonic function on a positive-dimensional Euclidean space is
constant. Harmonicity is required at every point of the whole space, and boundedness applies to
the entire range.
-/
def BoundedHarmonicIsConstant : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    0 < n ->
    HarmonicOnNhd f univ ->
    IsBounded (range f) ->
    forall x y, f x = f y

-- Structural mutations used to ensure the frozen clauses remain distinguishable.
def mutationRemovedBoundedness : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    0 < n -> HarmonicOnNhd f univ -> forall x y, f x = f y

def mutationRemovedHarmonicity : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    0 < n -> IsBounded (range f) -> forall x y, f x = f y

def mutationChangedDomainToPlane : Prop :=
  forall (f : Space 2 -> Real),
    HarmonicOnNhd f univ -> IsBounded (range f) -> forall x y, f x = f y

def mutationAllowedZeroDimension : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    HarmonicOnNhd f univ -> IsBounded (range f) -> forall x y, f x = f y

def mutationOneSidedBound : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    0 < n -> HarmonicOnNhd f univ ->
    (exists C : Real, forall x, f x <= C) -> forall x y, f x = f y

end Stage1Instances.THM_M_1143

set_option pp.explicit true in
#print Stage1Instances.THM_M_1143.BoundedHarmonicIsConstant
