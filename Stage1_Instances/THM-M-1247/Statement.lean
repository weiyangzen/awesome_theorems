import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# THM-M-1247: exact Rellich inequality statement

This module freezes the classical sharp second-order `L2` inequality on
Euclidean space. It contains no proof of the inequality.
-/

namespace Stage1Instances.THM_M_1247

open MeasureTheory

/-- Euclidean space in dimension `n`, with its standard Pi norm. -/
abbrev Euclidean (n : Nat) := Fin n → ℝ

/-- The Euclidean Laplacian, defined as the standard-coordinate trace of the
second Frechet derivative. -/
noncomputable def laplacian {n : Nat} (u : Euclidean n → ℝ) (x : Euclidean n) : ℝ :=
  ∑ i : Fin n,
    (fderiv ℝ (fun y ↦ fderiv ℝ u y) x) (Pi.single i 1) (Pi.single i 1)

/-- The canonical sharp Rellich inequality target.

The support conditions encode `u ∈ C_c^∞ (ℝ^n \ {0})`: `u` is smooth,
compactly supported, and its topological support does not contain the origin.
-/
def RellichInequalityTarget : Prop :=
  ∀ (n : Nat), 5 ≤ n → ∀ u : Euclidean n → ℝ,
    ContDiff ℝ ⊤ u → HasCompactSupport u → (0 : Euclidean n) ∉ tsupport u →
      (((n : ℝ) * ((n : ℝ) - 4)) / 4) ^ 2 *
          ∫ x, (u x) ^ 2 / ‖x‖ ^ 4 ≤
        ∫ x, (laplacian u x) ^ 2

/-- Fully expanded spelling of the canonical target. -/
def ExpandedTarget : Prop :=
  ∀ (n : Nat), 5 ≤ n → ∀ u : (Fin n → ℝ) → ℝ,
    ContDiff ℝ ⊤ u → HasCompactSupport u → (0 : Fin n → ℝ) ∉ tsupport u →
      (((n : ℝ) * ((n : ℝ) - 4)) / 4) ^ 2 *
          ∫ x, (u x) ^ 2 / ‖x‖ ^ 4 ≤
        ∫ x,
          (∑ i : Fin n,
            (fderiv ℝ (fun y ↦ fderiv ℝ u y) x)
              (Pi.single i 1) (Pi.single i 1)) ^ 2

/-- Checked definitional transport to the expanded encoding. -/
theorem rellichInequalityTarget_iff_expandedTarget :
    RellichInequalityTarget ↔ ExpandedTarget :=
  Iff.rfl

-- Structural mutations are elaborated and fingerprinted separately.
def mutationRemovedSupportAvoidance : Prop :=
  ∀ (n : Nat), 5 ≤ n → ∀ u : Euclidean n → ℝ,
    ContDiff ℝ ⊤ u → HasCompactSupport u →
      (((n : ℝ) * ((n : ℝ) - 4)) / 4) ^ 2 *
          ∫ x, (u x) ^ 2 / ‖x‖ ^ 4 ≤
        ∫ x, (laplacian u x) ^ 2

def mutationChangedDomainToOneDimension : Prop :=
  ∀ u : Euclidean 1 → ℝ,
    ContDiff ℝ ⊤ u → HasCompactSupport u → (0 : Euclidean 1) ∉ tsupport u →
      ((1 : ℝ) * (1 - 4) / 4) ^ 2 * ∫ x, (u x) ^ 2 / ‖x‖ ^ 4 ≤
        ∫ x, (laplacian u x) ^ 2

def mutationExistentialFunction : Prop :=
  ∀ (n : Nat), 5 ≤ n → ∃ u : Euclidean n → ℝ,
    ContDiff ℝ ⊤ u ∧ HasCompactSupport u ∧ (0 : Euclidean n) ∉ tsupport u ∧
      (((n : ℝ) * ((n : ℝ) - 4)) / 4) ^ 2 *
          ∫ x, (u x) ^ 2 / ‖x‖ ^ 4 ≤
        ∫ x, (laplacian u x) ^ 2

def mutationIncludesDimensionFour : Prop :=
  ∀ (n : Nat), 4 ≤ n → ∀ u : Euclidean n → ℝ,
    ContDiff ℝ ⊤ u → HasCompactSupport u → (0 : Euclidean n) ∉ tsupport u →
      (((n : ℝ) * ((n : ℝ) - 4)) / 4) ^ 2 *
          ∫ x, (u x) ^ 2 / ‖x‖ ^ 4 ≤
        ∫ x, (laplacian u x) ^ 2

end Stage1Instances.THM_M_1247

set_option pp.explicit true in
#print Stage1Instances.THM_M_1247.RellichInequalityTarget
