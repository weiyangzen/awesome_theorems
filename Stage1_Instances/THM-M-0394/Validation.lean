import «Stage1_Instances».«THM-M-0394».ObligationTree

/-!
# THM-M-0394 independent validation probes

This module rechecks the two proof-phase logical obligations without importing
`Proof.lean`. It does not provide either open arithmetic finiteness branch and
therefore cannot prove the canonical Siegel statement on its own.
-/

noncomputable section

open Stage1Rev56.THMM0394

universe u v

namespace Stage1Rev56.THMM0394.Validation

/-- Local factorization of the compatibility hypotheses, independently defined
for the validation probe. -/
def ModelCompatibility {K : Type u} [Field K] [NumberField K]
    (C : CurveModel.{u, v} K) : Prop :=
  C.dimensionOne ∧ C.genusModelsCompletion ∧ C.boundaryModelsComplement ∧
    C.coordinatesModelAffineEmbedding

/-- Independent reconstruction of the exact genus branch expansion. -/
theorem independent_isSiegelCurve_branch_iff
    {K : Type u} [Field K] [NumberField K]
    (C : CurveModel.{u, v} K) :
    IsSiegelCurve C ↔
      (ModelCompatibility C ∧ 0 < C.genus) ∨
      (ModelCompatibility C ∧ C.genus = 0 ∧ 3 ≤ C.boundaryPoints.card) := by
  simp only [IsSiegelCurve, ModelCompatibility]
  constructor
  · rintro ⟨hdim, hgenus, hboundary, hcoordinates, hpositive | hzero⟩
    · exact Or.inl ⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hpositive⟩
    · exact Or.inr ⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hzero⟩
  · rintro (⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hpositive⟩ |
      ⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hzero⟩)
    · exact ⟨hdim, hgenus, hboundary, hcoordinates, Or.inl hpositive⟩
    · exact ⟨hdim, hgenus, hboundary, hcoordinates, Or.inr hzero⟩

/-- Independent child-to-parent composition. The two substantive branch
proofs remain explicit premises rather than hidden assertions. -/
theorem independent_statement_of_branches
    (positive : ObligationTree.PositiveGenusBranch.{u, v})
    (genusZero : ObligationTree.GenusZeroBranch.{u, v}) : Statement.{u, v} := by
  intro K _ _ S C hC
  obtain hPositive | ⟨hZero, hBoundary⟩ := hC.2.2.2.2
  · exact positive K S C hC hPositive
  · exact genusZero K S C hC hZero hBoundary

#print axioms independent_isSiegelCurve_branch_iff
#print axioms independent_statement_of_branches

end Stage1Rev56.THMM0394.Validation
