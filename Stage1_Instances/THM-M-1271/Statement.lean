import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Topology.MetricSpace.Sequences

/-!
# THM-M-1271: mountain pass theorem statement

This module freezes the classical Ambrosetti-Rabinowitz mountain-pass target.
It contains statement-level definitions and checks only, not a proof of the theorem.
-/

namespace Stage1Instances.THM_M_1271

open Filter Set

universe u

variable {X : Type u} [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]

/-- Sequential Palais-Smale compactness for a continuously differentiable real functional. -/
def PalaisSmale (Phi : X → ℝ) : Prop :=
  ∀ x : ℕ → X,
    Bornology.IsBounded (range (fun n ↦ Phi (x n))) →
    Tendsto (fun n ↦ ‖fderiv ℝ Phi (x n)‖) atTop (nhds 0) →
    ∃ a : X, ∃ k : ℕ → ℕ, StrictMono k ∧ Tendsto (x ∘ k) atTop (nhds a)

/-- Continuous paths from the origin to `e`, represented on the closed unit interval. -/
def IsAdmissiblePath (e : X) (gamma : ℝ → X) : Prop :=
  ContinuousOn gamma (Icc 0 1) ∧ gamma 0 = 0 ∧ gamma 1 = e

/-- The maximum-height surrogate attached to a path. For an admissible path this is the
actual maximum, since its image under a `C^1` functional is compact. -/
noncomputable def PathHeight (Phi : X → ℝ) (gamma : ℝ → X) : ℝ :=
  sSup {r : ℝ | ∃ t ∈ Icc (0 : ℝ) 1, r = Phi (gamma t)}

/-- The mountain-pass minimax level for paths from the origin to `e`. -/
noncomputable def MountainPassLevel (Phi : X → ℝ) (e : X) : ℝ :=
  sInf {c : ℝ | ∃ gamma : ℝ → X, IsAdmissiblePath e gamma ∧ c = PathHeight Phi gamma}

/-- The exact classical mountain-pass target: mountain-pass geometry plus the Palais-Smale
condition gives a critical point at the minimax level, above the spherical barrier. -/
def MountainPassTarget : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (Phi : X → ℝ) (rho alpha : ℝ) (e : X),
    ContDiff ℝ 1 Phi →
    PalaisSmale Phi →
    Phi 0 = 0 →
    0 < rho →
    0 < alpha →
    (∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) →
    rho < ‖e‖ →
    Phi e ≤ 0 →
    ∃ x : X,
      fderiv ℝ Phi x = 0 ∧
      Phi x = MountainPassLevel Phi e ∧
      alpha ≤ MountainPassLevel Phi e

/-- A direct expansion used to check that the named predicates do not hide a changed theorem. -/
def ExpandedMountainPassTarget : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (Phi : X → ℝ) (rho alpha : ℝ) (e : X),
    ContDiff ℝ 1 Phi →
    (∀ x : ℕ → X,
      Bornology.IsBounded (range (fun n ↦ Phi (x n))) →
      Tendsto (fun n ↦ ‖fderiv ℝ Phi (x n)‖) atTop (nhds 0) →
      ∃ a : X, ∃ k : ℕ → ℕ, StrictMono k ∧ Tendsto (x ∘ k) atTop (nhds a)) →
    Phi 0 = 0 → 0 < rho → 0 < alpha →
    (∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) → rho < ‖e‖ → Phi e ≤ 0 →
    ∃ x : X, fderiv ℝ Phi x = 0 ∧
      Phi x = sInf {c : ℝ | ∃ gamma : ℝ → X,
        (ContinuousOn gamma (Icc 0 1) ∧ gamma 0 = 0 ∧ gamma 1 = e) ∧
        c = sSup {r : ℝ | ∃ t ∈ Icc (0 : ℝ) 1, r = Phi (gamma t)}} ∧
      alpha ≤ sInf {c : ℝ | ∃ gamma : ℝ → X,
        (ContinuousOn gamma (Icc 0 1) ∧ gamma 0 = 0 ∧ gamma 1 = e) ∧
        c = sSup {r : ℝ | ∃ t ∈ Icc (0 : ℝ) 1, r = Phi (gamma t)}}

/-- Kernel-checked identity between the canonical named target and its direct expansion. -/
theorem mountainPassTarget_iff_expanded :
    MountainPassTarget.{u} ↔ ExpandedMountainPassTarget.{u} := by
  rfl

-- Separately elaborated mutations; the statement validator requires distinct expressions.
def mutationWithoutPalaisSmale : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (Phi : X → ℝ) (rho alpha : ℝ) (e : X),
    ContDiff ℝ 1 Phi → Phi 0 = 0 → 0 < rho → 0 < alpha →
    (∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) → rho < ‖e‖ → Phi e ≤ 0 →
    ∃ x : X, fderiv ℝ Phi x = 0 ∧ Phi x = MountainPassLevel Phi e

def mutationFiniteDimensional : Prop :=
  ∀ (n : ℕ) (Phi : (Fin n → ℝ) → ℝ) (rho alpha : ℝ) (e : Fin n → ℝ),
    ContDiff ℝ 1 Phi → PalaisSmale Phi → Phi 0 = 0 → 0 < rho → 0 < alpha →
    (∀ x, ‖x‖ = rho → alpha ≤ Phi x) → rho < ‖e‖ → Phi e ≤ 0 →
    ∃ x, fderiv ℝ Phi x = 0 ∧ Phi x = MountainPassLevel Phi e

def mutationApproximateConclusion : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (Phi : X → ℝ) (rho alpha : ℝ) (e : X),
    ContDiff ℝ 1 Phi → PalaisSmale Phi → Phi 0 = 0 → 0 < rho → 0 < alpha →
    (∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) → rho < ‖e‖ → Phi e ≤ 0 →
    ∀ epsilon > 0, ∃ x : X, ‖fderiv ℝ Phi x‖ < epsilon

end Stage1Instances.THM_M_1271

set_option pp.explicit true in
#print Stage1Instances.THM_M_1271.MountainPassTarget
