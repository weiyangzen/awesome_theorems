import Statement

/-!
# THM-M-1041 conditional obligation composition

This module checks only the composition of separately exposed forward and
converse packages into the frozen Hille--Yosida equivalence. Neither package
is inhabited here.
-/

noncomputable section

open scoped NNReal

namespace Stage1Instances.THM_M_1041

universe u

/-- The complete generation-to-resolvent direction required by the root. -/
def ForwardPackage : Prop :=
  forall (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X]
    [CompleteSpace X] (A : X →ₗ.[ℝ] X),
    (∃ T : ℝ≥0 → X →L[ℝ] X,
      IsC0ContractionSemigroup T /\ IsGenerator A T) ->
      Dense (A.domain : Set X) /\ A.IsClosed /\
        forall a : ℝ, 0 < a -> ∃ R : X →L[ℝ] X,
          IsContractiveResolvent A a R

/-- The complete resolvent-to-generation direction required by the root. -/
def ConversePackage : Prop :=
  forall (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X]
    [CompleteSpace X] (A : X →ₗ.[ℝ] X),
    (Dense (A.domain : Set X) /\ A.IsClosed /\
      forall a : ℝ, 0 < a -> ∃ R : X →L[ℝ] X,
        IsContractiveResolvent A a R) ->
      ∃ T : ℝ≥0 → X →L[ℝ] X,
        IsC0ContractionSemigroup T /\ IsGenerator A T

/-- Kernel-checked final assembly, conditional on both substantive directions. -/
theorem root_of_directionPackages
    (forward : ForwardPackage.{u}) (converse : ConversePackage.{u}) :
    HilleYosidaContractionTarget.{u} := by
  intro X _ _ _ A
  constructor
  · exact forward X A
  · exact converse X A

#print axioms root_of_directionPackages

end Stage1Instances.THM_M_1041
