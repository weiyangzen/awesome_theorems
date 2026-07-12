import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Analytic.Basic
import Mathlib.Topology.MetricSpace.Bounded

/-!
# THM-M-0373: Carleson's corona theorem statement

This module freezes the classical finite-generator Bezout formulation on the
open complex unit disc. It elaborates the statement only and contains no proof
of the corona theorem.
-/

namespace Stage1Instances.THM_M_0373

open Metric Set

/-- The open complex unit disc, as an ambient subset of `ℂ`. -/
def unitDisc : Set ℂ := ball 0 1

/-- A complex function is in `H∞` on the open unit disc when it is analytic
there and its range on the disc is bounded. -/
def InHInfinity (f : ℂ → ℂ) : Prop :=
  AnalyticOnNhd ℂ f unitDisc ∧ Bornology.IsBounded (f '' unitDisc)

/-- Canonical rev-5.6 target: the finite-generator Bezout form of Carleson's
corona theorem on the open unit disc. -/
def CoronaTheoremTarget : Prop :=
  ∀ (ι : Type) [Fintype ι] [Nonempty ι]
    (f : ι → ℂ → ℂ) (δ : ℝ),
      (∀ i, InHInfinity (f i)) →
      0 < δ →
      (∀ z ∈ unitDisc, δ ≤ ∑ i, ‖f i z‖) →
      ∃ g : ι → ℂ → ℂ,
        (∀ i, InHInfinity (g i)) ∧
        ∀ z ∈ unitDisc, ∑ i, f i z * g i z = 1

/-- Fully expanded form used to check the local `H∞` and disc abbreviations. -/
def ExpandedCoronaTheoremTarget : Prop :=
  ∀ (ι : Type) [Fintype ι] [Nonempty ι]
    (f : ι → ℂ → ℂ) (δ : ℝ),
      (∀ i, AnalyticOnNhd ℂ (f i) (ball 0 1) ∧
        Bornology.IsBounded (f i '' ball 0 1)) →
      0 < δ →
      (∀ z ∈ ball (0 : ℂ) 1, δ ≤ ∑ i, ‖f i z‖) →
      ∃ g : ι → ℂ → ℂ,
        (∀ i, AnalyticOnNhd ℂ (g i) (ball 0 1) ∧
          Bornology.IsBounded (g i '' ball 0 1)) ∧
        ∀ z ∈ ball (0 : ℂ) 1, ∑ i, f i z * g i z = 1

/-- Checked transport between the named canonical target and its direct
expansion. -/
theorem coronaTheoremTarget_iff_expanded :
    CoronaTheoremTarget ↔ ExpandedCoronaTheoremTarget := by
  rfl

-- Structural mutations are separately elaborated and compared by the checker.
def mutationAllowsEmptyFamily : Prop :=
  ∀ (ι : Type) [Fintype ι]
    (f : ι → ℂ → ℂ) (δ : ℝ),
      (∀ i, InHInfinity (f i)) →
      0 < δ →
      (∀ z ∈ unitDisc, δ ≤ ∑ i, ‖f i z‖) →
      ∃ g : ι → ℂ → ℂ,
        (∀ i, InHInfinity (g i)) ∧
        ∀ z ∈ unitDisc, ∑ i, f i z * g i z = 1

def mutationDropsPositiveDelta : Prop :=
  ∀ (ι : Type) [Fintype ι] [Nonempty ι]
    (f : ι → ℂ → ℂ) (δ : ℝ),
      (∀ i, InHInfinity (f i)) →
      (∀ z ∈ unitDisc, δ ≤ ∑ i, ‖f i z‖) →
      ∃ g : ι → ℂ → ℂ,
        (∀ i, InHInfinity (g i)) ∧
        ∀ z ∈ unitDisc, ∑ i, f i z * g i z = 1

def mutationUsesSumOfSquaredNorms : Prop :=
  ∀ (ι : Type) [Fintype ι] [Nonempty ι]
    (f : ι → ℂ → ℂ) (δ : ℝ),
      (∀ i, InHInfinity (f i)) →
      0 < δ →
      (∀ z ∈ unitDisc, δ ≤ ∑ i, ‖f i z‖ ^ 2) →
      ∃ g : ι → ℂ → ℂ,
        (∀ i, InHInfinity (g i)) ∧
        ∀ z ∈ unitDisc, ∑ i, f i z * g i z = 1

def mutationIncludesBoundaryCircle : Prop :=
  ∀ (ι : Type) [Fintype ι] [Nonempty ι]
    (f : ι → ℂ → ℂ) (δ : ℝ),
      (∀ i, AnalyticOnNhd ℂ (f i) (closedBall 0 1) ∧
        Bornology.IsBounded (f i '' closedBall 0 1)) →
      0 < δ →
      (∀ z ∈ closedBall (0 : ℂ) 1, δ ≤ ∑ i, ‖f i z‖) →
      ∃ g : ι → ℂ → ℂ,
        (∀ i, AnalyticOnNhd ℂ (g i) (closedBall 0 1) ∧
          Bornology.IsBounded (g i '' closedBall 0 1)) ∧
        ∀ z ∈ closedBall (0 : ℂ) 1, ∑ i, f i z * g i z = 1

end Stage1Instances.THM_M_0373

set_option pp.explicit true in
#print Stage1Instances.THM_M_0373.CoronaTheoremTarget
