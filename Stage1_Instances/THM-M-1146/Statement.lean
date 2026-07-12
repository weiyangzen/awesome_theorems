import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.LinearAlgebra.Complex.FiniteDimensional

/-!
# THM-M-1146: Schwarz reflection principle

This module freezes the harmonic, zero-boundary, odd-reflection target selected by the intake.
It declares a proposition only; it does not prove the reflection principle.
-/

namespace Stage1Instances.THM_M_1146

open Complex InnerProductSpace
open scoped ComplexConjugate

noncomputable section

/-- The part of `V` strictly above the real axis. -/
def upperPart (V : Set ℂ) : Set ℂ :=
  {z | z ∈ V ∧ 0 < z.im}

/-- The part of the real axis which lies in `V`. -/
def reflectingPart (V : Set ℂ) : Set ℂ :=
  {z | z ∈ V ∧ z.im = 0}

/-- Odd reflection across the real axis, with the original value selected on the axis. -/
def oddReflection (u : ℂ → ℝ) (z : ℂ) : ℝ :=
  if 0 ≤ z.im then u z else -u (starRingEnd ℂ z)

/-- Exact Lean target for the harmonic zero-boundary Schwarz reflection principle. -/
def SchwarzReflectionTarget : Prop :=
  ∀ (V : Set ℂ) (u : ℂ → ℝ),
    IsOpen V →
    (∀ z, z ∈ V ↔ starRingEnd ℂ z ∈ V) →
    HarmonicOnNhd u (upperPart V) →
    ContinuousOn u (upperPart V ∪ reflectingPart V) →
    (∀ z ∈ reflectingPart V, u z = 0) →
    HarmonicOnNhd (oddReflection u) V ∧
      ∀ z ∈ upperPart V, oddReflection u z = u z

/- Structural mutations used only to check that each frozen hypothesis and the odd sign are
distinguishable from the canonical target. -/
def mutationRemovedOpenness : Prop :=
  ∀ (V : Set ℂ) (u : ℂ → ℝ),
    (∀ z, z ∈ V ↔ starRingEnd ℂ z ∈ V) →
    HarmonicOnNhd u (upperPart V) →
    ContinuousOn u (upperPart V ∪ reflectingPart V) →
    (∀ z ∈ reflectingPart V, u z = 0) →
    HarmonicOnNhd (oddReflection u) V ∧
      ∀ z ∈ upperPart V, oddReflection u z = u z

def mutationRemovedSymmetry : Prop :=
  ∀ (V : Set ℂ) (u : ℂ → ℝ),
    IsOpen V →
    HarmonicOnNhd u (upperPart V) →
    ContinuousOn u (upperPart V ∪ reflectingPart V) →
    (∀ z ∈ reflectingPart V, u z = 0) →
    HarmonicOnNhd (oddReflection u) V ∧
      ∀ z ∈ upperPart V, oddReflection u z = u z

def mutationRemovedContinuity : Prop :=
  ∀ (V : Set ℂ) (u : ℂ → ℝ),
    IsOpen V →
    (∀ z, z ∈ V ↔ starRingEnd ℂ z ∈ V) →
    HarmonicOnNhd u (upperPart V) →
    (∀ z ∈ reflectingPart V, u z = 0) →
    HarmonicOnNhd (oddReflection u) V ∧
      ∀ z ∈ upperPart V, oddReflection u z = u z

def mutationRemovedBoundaryVanishing : Prop :=
  ∀ (V : Set ℂ) (u : ℂ → ℝ),
    IsOpen V →
    (∀ z, z ∈ V ↔ starRingEnd ℂ z ∈ V) →
    HarmonicOnNhd u (upperPart V) →
    ContinuousOn u (upperPart V ∪ reflectingPart V) →
    HarmonicOnNhd (oddReflection u) V ∧
      ∀ z ∈ upperPart V, oddReflection u z = u z

def evenReflection (u : ℂ → ℝ) (z : ℂ) : ℝ :=
  if 0 ≤ z.im then u z else u (starRingEnd ℂ z)

def mutationChangedOddSign : Prop :=
  ∀ (V : Set ℂ) (u : ℂ → ℝ),
    IsOpen V →
    (∀ z, z ∈ V ↔ starRingEnd ℂ z ∈ V) →
    HarmonicOnNhd u (upperPart V) →
    ContinuousOn u (upperPart V ∪ reflectingPart V) →
    (∀ z ∈ reflectingPart V, u z = 0) →
    HarmonicOnNhd (evenReflection u) V ∧
      ∀ z ∈ upperPart V, evenReflection u z = u z

/-- The branch convention agrees with `u` throughout the closed upper half-plane. -/
theorem oddReflection_eq_of_nonnegative_imaginary
    (u : ℂ → ℝ) (z : ℂ) (hz : 0 ≤ z.im) : oddReflection u z = u z := by
  simp [oddReflection, hz]

/-- The lower branch has the essential minus sign. -/
theorem oddReflection_eq_of_negative_imaginary
    (u : ℂ → ℝ) (z : ℂ) (hz : z.im < 0) :
    oddReflection u z = -u (starRingEnd ℂ z) := by
  simp [oddReflection, not_le.mpr hz]

set_option pp.explicit true in
#print SchwarzReflectionTarget

end
end Stage1Instances.THM_M_1146
