import Mathlib.Topology.Algebra.Module.LinearPMap
import Mathlib.Analysis.Normed.Operator.Basic

/-!
# THM-M-1041: contraction Hille--Yosida statement

This module freezes the contraction-semigroup form of Hille--Yosida over a real
Banach space. It elaborates the statement only and contains no proof of it.
-/

noncomputable section

open Filter Topology
open scoped Topology NNReal

namespace Stage1Instances.THM_M_1041

universe u

variable {X : Type u} [NormedAddCommGroup X] [NormedSpace ℝ X]

/-- A bounded-operator family on nonnegative time is a strongly continuous
contraction semigroup. -/
def IsC0ContractionSemigroup (T : ℝ≥0 → X →L[ℝ] X) : Prop :=
  T 0 = ContinuousLinearMap.id ℝ X ∧
  (∀ s t, T (s + t) = (T s).comp (T t)) ∧
  (∀ x, Continuous fun t => T t x) ∧
  ∀ t x, ‖T t x‖ ≤ ‖x‖

/-- `A` is the infinitesimal generator of `T`, expressed as equality of its
graph with the strong right derivative of `T` at zero. -/
def IsGenerator (A : X →ₗ.[ℝ] X) (T : ℝ≥0 → X →L[ℝ] X) : Prop :=
  ∀ x y, (∃ hx : x ∈ A.domain, A ⟨x, hx⟩ = y) ↔
    Tendsto
      (fun t : ℝ≥0 => ((t : ℝ)⁻¹) • (T t x - x))
      (nhdsWithin (0 : ℝ≥0) (Set.Ioi 0)) (nhds y)

/-- A bounded inverse for `lambda I - A`, including both inverse equations and
the contraction-form resolvent estimate. -/
def IsContractiveResolvent (A : X →ₗ.[ℝ] X) (a : ℝ) (R : X →L[ℝ] X) : Prop :=
  (∀ y, ∃ hRy : R y ∈ A.domain, a • R y - A ⟨R y, hRy⟩ = y) ∧
  (∀ x (hx : x ∈ A.domain), R (a • x - A ⟨x, hx⟩) = x) ∧
  ∀ y, ‖R y‖ ≤ a⁻¹ * ‖y‖

/-- The exact contraction Hille--Yosida target: a partially defined real-linear
operator generates a strongly continuous contraction semigroup iff it is
closed, densely defined, and has the standard positive-axis resolvent bound. -/
def HilleYosidaContractionTarget : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (A : X →ₗ.[ℝ] X),
    (∃ T : ℝ≥0 → X →L[ℝ] X, IsC0ContractionSemigroup T ∧ IsGenerator A T) ↔
      Dense (A.domain : Set X) ∧ A.IsClosed ∧
        ∀ a : ℝ, 0 < a → ∃ R : X →L[ℝ] X, IsContractiveResolvent A a R

/-- A logically identical parenthesization used as a checked transport. -/
def ExpandedTarget : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X],
    ∀ A : X →ₗ.[ℝ] X,
      (∃ T : ℝ≥0 → X →L[ℝ] X, IsC0ContractionSemigroup T ∧ IsGenerator A T) ↔
        (Dense (A.domain : Set X) ∧ A.IsClosed ∧
          ∀ a : ℝ, a > 0 → ∃ R : X →L[ℝ] X, IsContractiveResolvent A a R)

theorem target_iff_expanded : HilleYosidaContractionTarget.{u} ↔ ExpandedTarget.{u} :=
  Iff.rfl

-- Structural mutations elaborated separately by the statement checker.
def mutationNoDenseDomain : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (A : X →ₗ.[ℝ] X),
    (∃ T : ℝ≥0 → X →L[ℝ] X, IsC0ContractionSemigroup T ∧ IsGenerator A T) ↔
      A.IsClosed ∧ ∀ a : ℝ, 0 < a → ∃ R : X →L[ℝ] X, IsContractiveResolvent A a R

def mutationNonnegativeResolventAxis : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (A : X →ₗ.[ℝ] X),
    (∃ T : ℝ≥0 → X →L[ℝ] X, IsC0ContractionSemigroup T ∧ IsGenerator A T) ↔
      Dense (A.domain : Set X) ∧ A.IsClosed ∧
        ∀ a : ℝ, 0 ≤ a → ∃ R : X →L[ℝ] X, IsContractiveResolvent A a R

def mutationChangedTimeDomain : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X],
    ∀ T : ℝ → X →L[ℝ] X, Continuous T

end Stage1Instances.THM_M_1041

set_option pp.explicit true in
#print Stage1Instances.THM_M_1041.HilleYosidaContractionTarget
