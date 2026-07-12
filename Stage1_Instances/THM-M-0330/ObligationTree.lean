import Statement

/-!
# THM-M-0330 conditional obligation composition

This module checks only the final logical composition selected by the frozen
obligation architecture.  The two mathematical directions remain explicit
premises and receive no proof credit from this adapter.
-/

namespace Stage1Instances.THM_M_0330

open scoped NNReal

universe u

/-- Exact forward-direction package, with no hidden change of target. -/
def ForwardPackage : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (A : X →ₗ.[ℝ] X),
    (∃ T : ℝ≥0 → X →L[ℝ] X, IsC0ContractionSemigroup T ∧ IsGenerator A T) →
      Dense (A.domain : Set X) ∧ A.IsClosed ∧
        ∀ a : ℝ, 0 < a → ∃ R : X →L[ℝ] X, IsContractiveResolvent A a R

/-- Exact converse-direction package, with no hidden change of target. -/
def ConversePackage : Prop :=
  ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
    (A : X →ₗ.[ℝ] X),
    (Dense (A.domain : Set X) ∧ A.IsClosed ∧
      ∀ a : ℝ, 0 < a → ∃ R : X →L[ℝ] X, IsContractiveResolvent A a R) →
      ∃ T : ℝ≥0 → X →L[ℝ] X, IsC0ContractionSemigroup T ∧ IsGenerator A T

/-- Kernel-checked composition of the two exact directional packages. -/
theorem root_of_direction_packages
    (forward : ForwardPackage.{u}) (converse : ConversePackage.{u}) :
    HilleYosidaContractionTarget.{u} := by
  intro X _ _ _ A
  exact ⟨forward X A, converse X A⟩

#print axioms root_of_direction_packages

end Stage1Instances.THM_M_0330
