import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1141: Harnack's inequality

This module freezes the statement selected from Axler, Bourdon, and Ramey,
*Harmonic Function Theory*, second edition, Theorem 3.6. It contains no proof
of Harnack's inequality.
-/

open Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1141

abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/-- On every compact subset of a connected open Euclidean domain, all values
of every positive harmonic function are comparable by one constant depending
only on the domain and compact set. -/
def HarnackInequality : Prop :=
  ∀ (n : Nat) (Ω K : Set (Space n)),
    IsOpen Ω → IsConnected Ω → IsCompact K → K ⊆ Ω →
    ∃ C : Real, 1 < C ∧
      ∀ (u : Space n → Real), HarmonicOnNhd u Ω →
        (∀ z ∈ Ω, 0 < u z) →
        ∀ x ∈ K, ∀ y ∈ K, 1 / C ≤ u y / u x ∧ u y / u x ≤ C

-- Structural mutations elaborate independently and document statement sensitivity.
def mutationRemovedConnectedness : Prop :=
  ∀ (n : Nat) (Ω K : Set (Space n)),
    IsOpen Ω → IsCompact K → K ⊆ Ω →
    ∃ C : Real, 1 < C ∧
      ∀ (u : Space n → Real), HarmonicOnNhd u Ω →
        (∀ z ∈ Ω, 0 < u z) →
        ∀ x ∈ K, ∀ y ∈ K, 1 / C ≤ u y / u x ∧ u y / u x ≤ C

def mutationRemovedCompactness : Prop :=
  ∀ (n : Nat) (Ω K : Set (Space n)),
    IsOpen Ω → IsConnected Ω → K ⊆ Ω →
    ∃ C : Real, 1 < C ∧
      ∀ (u : Space n → Real), HarmonicOnNhd u Ω →
        (∀ z ∈ Ω, 0 < u z) →
        ∀ x ∈ K, ∀ y ∈ K, 1 / C ≤ u y / u x ∧ u y / u x ≤ C

def mutationNonnegativeFunctions : Prop :=
  ∀ (n : Nat) (Ω K : Set (Space n)),
    IsOpen Ω → IsConnected Ω → IsCompact K → K ⊆ Ω →
    ∃ C : Real, 1 < C ∧
      ∀ (u : Space n → Real), HarmonicOnNhd u Ω →
        (∀ z ∈ Ω, 0 ≤ u z) →
        ∀ x ∈ K, ∀ y ∈ K, 1 / C ≤ u y / u x ∧ u y / u x ≤ C

def mutationConstantDependsOnFunction : Prop :=
  ∀ (n : Nat) (Ω K : Set (Space n)) (u : Space n → Real),
    IsOpen Ω → IsConnected Ω → IsCompact K → K ⊆ Ω →
    HarmonicOnNhd u Ω → (∀ z ∈ Ω, 0 < u z) →
    ∃ C : Real, 1 < C ∧
      ∀ x ∈ K, ∀ y ∈ K, 1 / C ≤ u y / u x ∧ u y / u x ≤ C

end Stage1Instances.THM_M_1141

set_option pp.explicit true in
#print Stage1Instances.THM_M_1141.HarnackInequality
