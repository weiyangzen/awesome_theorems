import «Stage1_Instances».«THM-M-0394».ObligationTree

/-!
# THM-M-0394 proof execution

This module contains the proof bodies that can be closed against the frozen
interfaces.  It proves the exact logical branch split and recomposition, but
does not postulate either arithmetic-geometric finiteness branch and therefore
does not declare the still-open Siegel root.
-/

noncomputable section

open Stage1Rev56.THMM0394

universe u v

namespace Stage1Rev56.THMM0394.Proof

/-- The common semantic compatibility hypotheses preceding the genus split. -/
def ModelCompatibility {K : Type u} [Field K] [NumberField K]
    (C : CurveModel.{u, v} K) : Prop :=
  C.dimensionOne ∧ C.genusModelsCompletion ∧ C.boundaryModelsComplement ∧
    C.coordinatesModelAffineEmbedding

/-- Exact disjunctive expansion of the branch split in `IsSiegelCurve`.
This closes frozen obligation `M0394-S3`; it proves no finiteness claim. -/
theorem isSiegelCurve_branch_iff
    {K : Type u} [Field K] [NumberField K]
    (C : CurveModel.{u, v} K) :
    IsSiegelCurve C ↔
      (ModelCompatibility C ∧ 0 < C.genus) ∨
      (ModelCompatibility C ∧ C.genus = 0 ∧ 3 ≤ C.boundaryPoints.card) := by
  constructor
  · rintro ⟨hdim, hgenus, hboundary, hcoordinates, hpositive | hzero⟩
    · exact Or.inl ⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hpositive⟩
    · exact Or.inr ⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hzero⟩
  · rintro (⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hpositive⟩ |
      ⟨⟨hdim, hgenus, hboundary, hcoordinates⟩, hzero⟩)
    · exact ⟨hdim, hgenus, hboundary, hcoordinates, Or.inl hpositive⟩
    · exact ⟨hdim, hgenus, hboundary, hcoordinates, Or.inr hzero⟩

/-- Proof-phase copy of the checked child-to-parent rule for frozen obligation
`M0394-B`.  Its two premises are intentionally explicit and unasserted. -/
theorem statement_of_branches
    (positive : ObligationTree.PositiveGenusBranch.{u, v})
    (genusZero : ObligationTree.GenusZeroBranch.{u, v}) : Statement.{u, v} :=
  ObligationTree.branch_composition positive genusZero

#print axioms isSiegelCurve_branch_iff
#print axioms statement_of_branches

end Stage1Rev56.THMM0394.Proof
