import Mathlib.NumberTheory.ModularForms.Basic

/-!
# THM-M-0436 statement-gate audit

This module does not state or prove Shimura lifting. It kernel-checks the
reason that the legacy proposition-field candidate cannot be frozen as the
canonical target.
-/

namespace Stage1Instances.THM_M_0436

open Complex UpperHalfPlane Matrix.SpecialLinearGroup
open scoped MatrixGroups ModularForm

noncomputable section

universe u

/-- Exact local mirror of the legacy source record fields relevant to its
`StatementShape`. The historical module is separately elaborated intact. -/
structure LegacySource where
  level : ℕ
  weightIndex : ℕ
  characterTag : Type u
  sourceSpaceTag : Type u
  toFun : ℍ → ℂ
  qCoeff : ℕ → ℂ
  halfIntegralSlashLaw : Prop
  cuspCondition : Prop
  kohnenPlusCondition : Prop
  heckeEigenAwayFromLevel : Prop

/-- Exact local mirror of the legacy target record. -/
structure LegacyTarget (input : LegacySource.{u}) where
  targetLevel : ℕ
  targetWeight : ℤ
  targetGroup : Subgroup (GL (Fin 2) ℝ)
  targetForm : CuspForm targetGroup targetWeight
  targetCoeff : ℕ → ℂ
  coefficientFormula : Prop
  heckeCompatibilityAwayFromLevel : Prop
  lFunctionCompatibility : Prop

/-- Exact local expansion of the historical `StatementShape`. -/
def LegacyStatementShape : Prop :=
  ∀ input : LegacySource.{u},
    input.halfIntegralSlashLaw →
      input.cuspCondition →
        input.kohnenPlusCondition →
          input.heckeEigenAwayFromLevel →
            Nonempty (LegacyTarget input)

/-- The legacy target can always be populated with the zero ordinary cusp
form and arbitrary proposition witnesses. This is a statement mutation test,
not a proof of the classical Shimura lift. -/
theorem legacyStatementShape_is_vacuous : LegacyStatementShape := by
  intro input _ _ _ _
  let targetGroup : Subgroup (GL (Fin 2) ℝ) := ⊤
  exact ⟨{
    targetLevel := 0
    targetWeight := 0
    targetGroup := targetGroup
    targetForm := 0
    targetCoeff := fun _ => 0
    coefficientFormula := True
    heckeCompatibilityAwayFromLevel := True
    lFunctionCompatibility := True
  }⟩

end

end Stage1Instances.THM_M_0436

#check Stage1Instances.THM_M_0436.legacyStatementShape_is_vacuous
