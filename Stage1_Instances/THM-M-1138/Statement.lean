import Mathlib.Analysis.InnerProductSpace.Harmonic.HarmonicContOnCl
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1138: weak maximum principle for harmonic functions

This module freezes the exact statement selected by the rev-5.6 intake. It
contains no proof of the maximum principle.
-/

open Set Topology
open InnerProductSpace

namespace Stage1Instances.THM_M_1138

/-- The finite-dimensional real Euclidean ambient space. -/
abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/-- Exact target selected at intake: a real-valued harmonic function,
continuous on the closure of a nonempty bounded connected open Euclidean
domain of positive dimension, has a boundary point dominating every value on
the closure. -/
def HarmonicWeakMaximumPrinciple : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (u : Space n → Real),
    0 < n → U.Nonempty → IsOpen U → IsConnected U → Bornology.IsBounded U →
    HarmonicContOnCl u U →
    ∃ y ∈ frontier U, ∀ x ∈ closure U, u x ≤ u y

-- Separately elaborated structural mutations are not aliases of the root.
def mutationRemovedBoundedness : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (u : Space n → Real),
    0 < n → U.Nonempty → IsOpen U → IsConnected U →
    HarmonicContOnCl u U →
    ∃ y ∈ frontier U, ∀ x ∈ closure U, u x ≤ u y

def mutationRemovedContinuityOnClosure : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (u : Space n → Real),
    0 < n → U.Nonempty → IsOpen U → IsConnected U → Bornology.IsBounded U →
    HarmonicOnNhd u U →
    ∃ y ∈ frontier U, ∀ x ∈ closure U, u x ≤ u y

def mutationRemovedHarmonicity : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (u : Space n → Real),
    0 < n → U.Nonempty → IsOpen U → IsConnected U → Bornology.IsBounded U →
    ContinuousOn u (closure U) →
    ∃ y ∈ frontier U, ∀ x ∈ closure U, u x ≤ u y

def mutationAllowedZeroDimension : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (u : Space n → Real),
    U.Nonempty → IsOpen U → IsConnected U → Bornology.IsBounded U →
    HarmonicContOnCl u U →
    ∃ y ∈ frontier U, ∀ x ∈ closure U, u x ≤ u y

def mutationChangedBinderScope : Prop :=
  ∀ (n : Nat) (U : Set (Space n)),
    0 < n → U.Nonempty → IsOpen U → IsConnected U → Bornology.IsBounded U →
    ∀ u : Space n → Real,
      HarmonicContOnCl u U ∧
      ∃ y ∈ frontier U, ∀ x ∈ closure U, u x ≤ u y

end Stage1Instances.THM_M_1138

set_option pp.explicit true in
#print Stage1Instances.THM_M_1138.HarmonicWeakMaximumPrinciple
