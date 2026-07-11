import Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems

/-!
# THM-M-0082: general adjoint functor theorem statement

This module freezes and tests the general right-adjoint statement selected at
intake. It does not prove that statement.
-/

open CategoryTheory CategoryTheory.Limits

namespace Stage1Instances.THM_M_0082

universe vC vD uC uD

/-- Freyd's general right adjoint functor theorem in the size convention of
the pinned mathlib API. The hypotheses are values so the complete and
limit-preserving structures remain visible in the serialized proposition. -/
def GeneralRightAdjointTarget : Prop :=
  ∀ (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D] (G : Functor D C),
      HasLimits D →
        PreservesLimitsOfSize.{vD, vD} G →
          SolutionSetCondition.{vD} G →
            G.IsRightAdjoint

/-- The typeclass-shaped form used by the pinned mathlib declaration. -/
def TypeclassGeneralRightAdjointTarget : Prop :=
  ∀ (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D] (G : Functor D C)
    [HasLimits D] [PreservesLimitsOfSize.{vD, vD} G],
      SolutionSetCondition.{vD} G → G.IsRightAdjoint

/-- Explicit hypotheses and the typeclass-shaped encoding are equivalent.
This is a statement transport only; neither direction invokes the adjoint
functor theorem. -/
theorem generalRightAdjointTarget_iff_typeclassTarget :
    GeneralRightAdjointTarget.{vC, vD, uC, uD} ↔
      TypeclassGeneralRightAdjointTarget.{vC, vD, uC, uD} := by
  constructor
  · intro h C _ D _ G _ _ hSolution
    exact h C D G inferInstance inferInstance hSolution
  · intro h C _ D _ G hLimits hPreserves hSolution
    letI := hLimits
    letI := hPreserves
    exact h C D G hSolution

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedCompleteness : Prop :=
  ∀ (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D] (G : Functor D C),
      PreservesLimitsOfSize.{vD, vD} G →
        SolutionSetCondition.{vD} G → G.IsRightAdjoint

def mutationRemovedSolutionSet : Prop :=
  ∀ (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D] (G : Functor D C),
      HasLimits D → PreservesLimitsOfSize.{vD, vD} G → G.IsRightAdjoint

def mutationChangedBinderScope : Prop :=
  ∀ (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D],
      HasLimits D →
        ∀ (G : Functor D C),
          PreservesLimitsOfSize.{vD, vD} G ∧
            SolutionSetCondition.{vD} G → G.IsRightAdjoint

/-- Adding object inhabitation would exclude the empty-category boundary at
the statement level, even though completeness is already an explicit premise. -/
def mutationExcludedEmptyDomain : Prop :=
  ∀ (C : Type uC) [Category.{vC} C]
    (D : Type uD) [Category.{vD} D] [Nonempty D] (G : Functor D C),
      HasLimits D →
        PreservesLimitsOfSize.{vD, vD} G →
          SolutionSetCondition.{vD} G → G.IsRightAdjoint

end Stage1Instances.THM_M_0082

set_option pp.explicit true in
#print Stage1Instances.THM_M_0082.GeneralRightAdjointTarget
