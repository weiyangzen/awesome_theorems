import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic

/-!
# THM-M-1140: strong maximum principle for harmonic functions

This module freezes the exact Lean statement selected by the rev-5.6 intake.
It contains no proof of the strong maximum principle.
-/

open Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1140

/-- The finite-dimensional real Euclidean ambient space. -/
abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/-- Exact target selected at intake: a real-valued function harmonic on a
nonempty connected open Euclidean domain and attaining its maximum at a point
of the domain is constant there. -/
def HarmonicStrongMaximumPrinciple : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n → Real) (x0 : Space n),
    Omega.Nonempty → IsOpen Omega → IsConnected Omega → x0 ∈ Omega →
    HarmonicOnNhd u Omega →
    (∀ x ∈ Omega, u x ≤ u x0) →
    ∀ x ∈ Omega, u x = u x0

/-- Equivalent encoding with the maximizing point represented as a subtype,
matching the binder shape used in the intake record. -/
def SubtypeMaximizerEncoding : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n → Real) (x0 : Omega),
    Omega.Nonempty → IsOpen Omega → IsConnected Omega →
    HarmonicOnNhd u Omega →
    (∀ x : Omega, u x ≤ u x0) →
    ∀ x : Omega, u x = u x0

/-- Checked transport between ambient-point and subtype-point encodings. -/
theorem harmonicStrongMaximumPrinciple_iff_subtypeMaximizerEncoding :
    HarmonicStrongMaximumPrinciple ↔ SubtypeMaximizerEncoding := by
  constructor
  · intro h n Omega u x0 hne hopen hconn hharm hmax x
    exact h n Omega u x0 hne hopen hconn x0.property hharm
      (fun y hy ↦ hmax ⟨y, hy⟩) x x.property
  · intro h n Omega u x0 hne hopen hconn hx0 hharm hmax x hx
    exact h n Omega u ⟨x0, hx0⟩ hne hopen hconn hharm
      (fun y ↦ hmax y y.property) ⟨x, hx⟩

-- Separately elaborated structural mutations are not aliases of the root.
def mutationRemovedOpenness : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n → Real) (x0 : Space n),
    Omega.Nonempty → IsConnected Omega → x0 ∈ Omega →
    HarmonicOnNhd u Omega →
    (∀ x ∈ Omega, u x ≤ u x0) →
    ∀ x ∈ Omega, u x = u x0

def mutationRemovedConnectedness : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n → Real) (x0 : Space n),
    Omega.Nonempty → IsOpen Omega → x0 ∈ Omega →
    HarmonicOnNhd u Omega →
    (∀ x ∈ Omega, u x ≤ u x0) →
    ∀ x ∈ Omega, u x = u x0

def mutationRemovedHarmonicity : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n → Real) (x0 : Space n),
    Omega.Nonempty → IsOpen Omega → IsConnected Omega → x0 ∈ Omega →
    (∀ x ∈ Omega, u x ≤ u x0) →
    ∀ x ∈ Omega, u x = u x0

def mutationChangedExtremumToLocalNeighborhood : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n → Real) (x0 : Space n),
    Omega.Nonempty → IsOpen Omega → IsConnected Omega → x0 ∈ Omega →
    HarmonicOnNhd u Omega →
    (∃ r : Real, 0 < r ∧ ∀ x ∈ Omega, dist x x0 < r → u x ≤ u x0) →
    ∀ x ∈ Omega, u x = u x0

def mutationChangedCodomainToComplex : Prop :=
  ∀ (n : Nat) (Omega : Set (Space n)) (u : Space n → Complex) (x0 : Space n),
    Omega.Nonempty → IsOpen Omega → IsConnected Omega → x0 ∈ Omega →
    HarmonicOnNhd u Omega →
    (∀ x ∈ Omega, ‖u x‖ ≤ ‖u x0‖) →
    ∀ x ∈ Omega, u x = u x0

end Stage1Instances.THM_M_1140

set_option pp.explicit true in
#print Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple
