import Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems
import Mathlib.CategoryTheory.Adjunction.Limits
import Mathlib.Algebra.Homology.HomologySequenceLemmas

/-!
# S1-M-135 / THM-M-0082: Adjoint functor theorem

This Stage1 artifact records checked Lean 4 wrappers around the pinned mathlib
adjoint-functor-theorem API.

The central category-theory part is already present in mathlib:

* `isRightAdjoint_of_preservesLimits_of_solutionSetCondition`, the general
  adjoint functor theorem;
* `isRightAdjoint_of_preservesLimits_of_isCoseparating`, the special adjoint
  functor theorem;
* `isLeftAdjoint_of_preservesColimits_of_isSeparating`, the dual special
  theorem.

The homological wrappers at the end are included only as Stage1 anchors for the
surrounding category/homological-algebra API mentioned in the queue item.  They
do not claim that every downstream derived-functor or long-exact-sequence branch
has been backfilled into the public blueprint surface.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

set_option linter.unusedSectionVars false

universe w v vC vD uC uD uI

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_135

section GeneralAdjointFunctorTheorem

variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/--
Statement shape for the general adjoint functor theorem: a limit-preserving
functor satisfying the solution-set condition is a right adjoint.
-/
def GeneralRightAdjointStatementShape : Prop :=
  ∀ {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D] (G : D ⥤ C),
      HasLimits D →
        PreservesLimitsOfSize.{vD, vD} G →
          SolutionSetCondition.{vD} G →
            G.IsRightAdjoint

/-- Checked wrapper around mathlib's general adjoint functor theorem. -/
theorem generalRightAdjoint_of_solutionSetCondition
    (G : D ⥤ C) [HasLimits D] [PreservesLimitsOfSize.{vD, vD} G]
    (hG : SolutionSetCondition.{vD} G) :
    G.IsRightAdjoint :=
  isRightAdjoint_of_preservesLimits_of_solutionSetCondition G hG

/-- The general statement shape is witnessed by the pinned mathlib theorem. -/
theorem generalRightAdjointStatementShape_checked :
    GeneralRightAdjointStatementShape := by
  intro C _ D _ G hLimits hPres hSolution
  letI := hLimits
  letI := hPres
  exact generalRightAdjoint_of_solutionSetCondition G hSolution

/-- Converse anchor: a right adjoint satisfies mathlib's solution-set condition. -/
theorem solutionSetCondition_of_rightAdjoint
    (G : D ⥤ C) [G.IsRightAdjoint] :
    SolutionSetCondition.{w} G :=
  solutionSetCondition_of_isRightAdjoint G

end GeneralAdjointFunctorTheorem

section SpecialAdjointFunctorTheorem

variable {C : Type uC} [Category.{v} C]
variable {D : Type uD} [Category.{v} D]

/--
Statement shape for the special adjoint functor theorem: a limit-preserving
functor out of a complete well-powered category with a small coseparating class
is a right adjoint.
-/
def SpecialRightAdjointStatementShape : Prop :=
  ∀ {C : Type uC} [Category.{v} C]
    {D : Type uD} [Category.{v} D]
    (P : ObjectProperty D),
      ObjectProperty.Small.{v} P →
        P.IsCoseparating →
          HasLimits D →
            WellPowered.{v} D →
              ∀ G : D ⥤ C, PreservesLimits G → G.IsRightAdjoint

/--
Dual special statement shape: a colimit-preserving functor out of a cocomplete
co-well-powered category with a small separating class is a left adjoint.
-/
def SpecialLeftAdjointStatementShape : Prop :=
  ∀ {C : Type uC} [Category.{v} C]
    {D : Type uD} [Category.{v} D]
    (P : ObjectProperty C),
      ObjectProperty.Small.{v} P →
        P.IsSeparating →
          HasColimits C →
            WellPowered.{v} Cᵒᵖ →
              ∀ F : C ⥤ D, PreservesColimits F → F.IsLeftAdjoint

/-- Checked wrapper around mathlib's special adjoint functor theorem. -/
theorem specialRightAdjoint_of_coseparating
    [HasLimits D] [WellPowered.{v} D]
    {P : ObjectProperty D} [ObjectProperty.Small.{v} P]
    (hP : P.IsCoseparating) (G : D ⥤ C) [PreservesLimits G] :
    G.IsRightAdjoint :=
  isRightAdjoint_of_preservesLimits_of_isCoseparating hP G

/-- Checked wrapper around the dual special adjoint functor theorem. -/
theorem specialLeftAdjoint_of_separating
    [HasColimits C] [WellPowered.{v} Cᵒᵖ]
    {P : ObjectProperty C} [ObjectProperty.Small.{v} P]
    (hP : P.IsSeparating) (F : C ⥤ D) [PreservesColimits F] :
    F.IsLeftAdjoint :=
  isLeftAdjoint_of_preservesColimits_of_isSeparating hP F

/-- The special right-adjoint statement shape is witnessed by mathlib. -/
theorem specialRightAdjointStatementShape_checked :
    SpecialRightAdjointStatementShape := by
  intro C _ D _ P hSmall hCoseparating hLimits hWellPowered G hPres
  letI := hSmall
  letI := hLimits
  letI := hWellPowered
  letI := hPres
  exact specialRightAdjoint_of_coseparating hCoseparating G

/-- The dual special left-adjoint statement shape is witnessed by mathlib. -/
theorem specialLeftAdjointStatementShape_checked :
    SpecialLeftAdjointStatementShape := by
  intro C _ D _ P hSmall hSeparating hColimits hWellPowered F hPres
  letI := hSmall
  letI := hColimits
  letI := hWellPowered
  letI := hPres
  exact specialLeftAdjoint_of_separating hSeparating F

end SpecialAdjointFunctorTheorem

section PreservationAnchors

variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]
variable {F : C ⥤ D} {G : D ⥤ C}

/-- Checked anchor: left adjoints preserve colimits. -/
theorem leftAdjoint_preservesColimitsOfSize
    (adj : F ⊣ G) :
    PreservesColimitsOfSize.{v, uI} F :=
  adj.leftAdjoint_preservesColimits

/-- Checked anchor: right adjoints preserve limits. -/
theorem rightAdjoint_preservesLimitsOfSize
    (adj : F ⊣ G) :
    PreservesLimitsOfSize.{v, uI} G :=
  adj.rightAdjoint_preservesLimits

end PreservationAnchors

section HomologicalAnchors

/-- Statement shape for the long exact homology sequence of a short exact complex. -/
def HomologyLongExactStatement
    (A : Type uC) [Category.{vC} A] [Abelian A] {ι : Type uI}
    (c : ComplexShape ι) : Prop :=
  ∀ (S : ShortComplex (HomologicalComplex A c)) (hS : S.ShortExact)
    (i j : ι) (hij : c.Rel i j),
      (HomologicalComplex.HomologySequence.composableArrows₅ hS i j hij).Exact

/-- Checked wrapper around mathlib's long exact homology-sequence exactness theorem. -/
theorem homologyLongExactStatement_checked
    (A : Type uC) [Category.{vC} A] [Abelian A] {ι : Type uI}
    (c : ComplexShape ι) :
    HomologyLongExactStatement A c := by
  intro S hS i j hij
  exact HomologicalComplex.HomologySequence.composableArrows₅_exact hS i j hij

/-- Checked naturality square for connecting morphisms in the long exact sequence. -/
theorem homologyConnecting_naturality
    {A : Type uC} [Category.{vC} A] [Abelian A] {ι : Type uI} {c : ComplexShape ι}
    {S₁ S₂ : ShortComplex (HomologicalComplex A c)}
    (φ : S₁ ⟶ S₂) (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i j : ι) (hij : c.Rel i j) :
    hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ _ =
      HomologicalComplex.homologyMap φ.τ₃ _ ≫ hS₂.δ i j hij :=
  HomologicalComplex.HomologySequence.δ_naturality φ hS₁ hS₂ i j hij

end HomologicalAnchors

/-- Combined Stage1 statement shape for this slot's checked category-level anchors. -/
def StatementShape : Prop :=
  GeneralRightAdjointStatementShape.{uC, vC, uD, vD} ∧
    SpecialRightAdjointStatementShape.{v, uC, uD} ∧
      SpecialLeftAdjointStatementShape.{v, uC, uD}

/-- Checked combined wrapper for the currently available mathlib adjoint-functor API. -/
theorem statementShape_checked : StatementShape :=
  ⟨generalRightAdjointStatementShape_checked,
    specialRightAdjointStatementShape_checked,
    specialLeftAdjointStatementShape_checked⟩

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems",
  "Mathlib.CategoryTheory.Adjunction.Basic",
  "Mathlib.CategoryTheory.Adjunction.Limits",
  "Mathlib.CategoryTheory.Comma.StructuredArrow.Small",
  "Mathlib.CategoryTheory.Limits.Constructions.WeaklyInitial",
  "Mathlib.CategoryTheory.Subobject.Comma",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas"
]

/-- Principal declarations used by this Stage1 wrapper. -/
def mathlibAnchorNames : List String := [
  "CategoryTheory.SolutionSetCondition",
  "CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition",
  "CategoryTheory.solutionSetCondition_of_isRightAdjoint",
  "CategoryTheory.isRightAdjoint_of_preservesLimits_of_isCoseparating",
  "CategoryTheory.isLeftAdjoint_of_preservesColimits_of_isSeparating",
  "CategoryTheory.Adjunction.leftAdjoint_preservesColimits",
  "CategoryTheory.Adjunction.rightAdjoint_preservesLimits",
  "HomologicalComplex.HomologySequence.composableArrows₅_exact",
  "HomologicalComplex.HomologySequence.δ_naturality"
]

/-- Pinned mathlib revision used for the adjoint-functor-theorem anchor audit. -/
def adjointFunctorTheoremsMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Pinned mathlib module containing the adjoint-functor-theorem API. -/
def adjointFunctorTheoremsMathlibModule : String :=
  "Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems"

/-- Public machine-status wording justified for the core category-level AFT wrappers. -/
def coreCategoryAFTMachineStatus : String :=
  "local_wrapper_upstream_mathlib"

/--
Public-status boundary for this Stage1 slot.

The category-level adjoint functor theorem wrappers are locally checked against
pinned mathlib.  The homological declarations in this file are adjacent anchors
only and should remain partial in public status text unless separately proved.
-/
def publicStatusBoundary : String :=
  "core category-level AFT local_wrapper_upstream_mathlib; homological add-ons partial"

/--
Public caution prepared for `THM-M-0082.homological-branch-boundary`.

The checked homology-sequence declarations below are adjacent API anchors for
the Stage1 profile.  They are not a repo-local proof of every derived-object,
derived-functor, or spectral-sequence specialization that may be mentioned in
the broader human-readable profile.
-/
def homologicalBranchBoundaryCaution : String :=
  "The homology-sequence wrappers in S1_M_135.lean are adjacent checked API anchors only; they do not prove every derived-object, derived-functor, or spectral-sequence specialization in the Stage1 profile."

/--
Public anchor table for the pinned mathlib adjoint-functor-theorem API.

Each row is `(module, declaration, source line, role, repo-local status)`, with
line numbers taken from the checked-out mathlib revision recorded above.
-/
def publicAdjointFunctorTheoremsAnchorTable :
    List (String × String × Nat × String × String) := [
  (adjointFunctorTheoremsMathlibModule,
    "CategoryTheory.SolutionSetCondition",
    62,
    "solution-set hypothesis for the general adjoint functor theorem",
    "pinned_mathlib_imported_and_wrapped"),
  (adjointFunctorTheoremsMathlibModule,
    "CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition",
    85,
    "general adjoint functor theorem: limit-preserving functor plus solution-set condition",
    "pinned_mathlib_imported_and_wrapped"),
  (adjointFunctorTheoremsMathlibModule,
    "CategoryTheory.isRightAdjoint_of_preservesLimits_of_isCoseparating",
    108,
    "special adjoint functor theorem from small coseparating class and well-powered domain",
    "pinned_mathlib_imported_and_wrapped"),
  (adjointFunctorTheoremsMathlibModule,
    "CategoryTheory.isLeftAdjoint_of_preservesColimits_of_isSeparating",
    119,
    "dual special adjoint functor theorem from small separating class and co-well-powered source",
    "pinned_mathlib_imported_and_wrapped")
]

/-- Search terms used to distinguish checked anchors from broader absent APIs. -/
def anchorAuditSearchTerms : List String := [
  "AdjointFunctorTheorems",
  "SolutionSetCondition",
  "isRightAdjoint_of_preservesLimits_of_solutionSetCondition",
  "isRightAdjoint_of_preservesLimits_of_isCoseparating",
  "isLeftAdjoint_of_preservesColimits_of_isSeparating",
  "WellPowered",
  "IsCoseparating",
  "IsSeparating",
  "left adjoint preserves colimits",
  "right adjoint preserves limits",
  "HomologySequence.δ_naturality"
]

/-- Search terms prepared for the optional non-mathlib external Lean audit. -/
def externalHomologicalAFTAuditSearchTerms : List String := [
  "adjoint functor theorem homological algebra",
  "homological adjoint functor theorem",
  "derived functor adjoint functor theorem",
  "spectral sequence adjoint functor theorem",
  "Brown representability",
  "well generated triangulated category",
  "derived category adjoint functor",
  "Lean AdjointFunctorTheorem",
  "Lean BrownRepresentability",
  "Lean derived functor adjoint"
]

/--
Authenticated external-audit status for `THM-M-0082.external-audit`.

The local process was not logged in to GitHub on 2026-05-01, so authenticated
GitHub code search could not be run here.  No non-mathlib stronger homological
AFT specialization is imported, pinned, or claimed as completion evidence by
this repo-local artifact.
-/
def externalHomologicalAFTAuditStatus : String :=
  "blocked_no_authenticated_github_code_search_2026-05-01; no external completion claim"

/--
Repo-local completion gate for the optional external audit.

URL-only or unauthenticated search findings must not be counted as completion.
A future positive result needs a concrete repository, commit, theorem/module
name, Lake integration feasibility check, and local import/check result.
-/
def externalHomologicalAFTRepoLocalGate : String :=
  "no completed state from external audit until a non-mathlib Lean proof is pinned/imported/checked or a concrete integration blocker is recorded"

/-- Public theorem-tree package row prepared for serial Stage1 backfill. -/
structure M0082TheoremTreePackage where
  code : String
  title : String
  scope : String
  leafRange : String
  status : String
  deriving Repr

/-- Public theorem-tree leaf row prepared for serial Stage1 backfill. -/
structure M0082TheoremTreeLeaf where
  code : String
  packageCode : String
  task : String
  localArtifact : String
  budget : String
  status : String
  deriving Repr

/--
Package split for `THM-M-0082.theorem-tree`.

The rows are checked as repo-local metadata for the public theorem-tree merge.
Rows marked `checked_wrapper` refer only to declarations already validated in
this file; the public merge row remains integrator-pending.
-/
def theoremTreePackages : List M0082TheoremTreePackage := [
  {
    code := "P01",
    title := "statement-boundary-and-import-surface",
    scope := "imports pinned AFT and homological modules; fixes the Stage1 namespace and combined statement shape",
    leafRange := "M0082-L001",
    status := "checked_metadata"
  },
  {
    code := "P02",
    title := "general-adjoint-functor-theorem",
    scope := "solution-set condition plus limit preservation implies right adjoint",
    leafRange := "M0082-L002 through M0082-L004",
    status := "checked_wrapper"
  },
  {
    code := "P03",
    title := "right-adjoint-solution-set-converse",
    scope := "right adjoints satisfy mathlib's solution-set condition",
    leafRange := "M0082-L005",
    status := "checked_anchor"
  },
  {
    code := "P04",
    title := "special-right-adjoint-functor-theorem",
    scope := "well-powered complete domain with a small coseparating class",
    leafRange := "M0082-L006 and M0082-L008 and M0082-L010",
    status := "checked_wrapper"
  },
  {
    code := "P05",
    title := "dual-special-left-adjoint-functor-theorem",
    scope := "co-well-powered cocomplete source with a small separating class",
    leafRange := "M0082-L007 and M0082-L009 and M0082-L011",
    status := "checked_wrapper"
  },
  {
    code := "P06",
    title := "adjunction-preservation-support",
    scope := "left adjoints preserve colimits and right adjoints preserve limits",
    leafRange := "M0082-L012 through M0082-L013",
    status := "checked_anchor"
  },
  {
    code := "P07",
    title := "combined-status-and-pinned-anchor-table",
    scope := "combined statement shape, pinned mathlib revision, module list, declaration list, and public anchor table",
    leafRange := "M0082-L014 through M0082-L017",
    status := "checked_metadata"
  },
  {
    code := "P08",
    title := "homological-adjacent-anchor-boundary",
    scope := "long exact homology sequence and connecting morphism naturality anchors, explicitly nonterminal for broader homological add-ons",
    leafRange := "M0082-L018 through M0082-L019",
    status := "checked_adjacent_anchor_only"
  },
  {
    code := "P09",
    title := "public-merge-and-completion-gate",
    scope := "serial public theorem-tree merge, aggregator policy, and no residual repo-local integration debt before completion language",
    leafRange := "M0082-L020",
    status := "public_merge_pending"
  }
]

/-- The `THM-M-0082` public theorem-tree package split has exactly P01 through P09. -/
theorem theoremTreePackages_length : theoremTreePackages.length = 9 := rfl

/--
M0387-level leaf ledger for `THM-M-0082.theorem-tree`.

Every row is scoped to a local artifact already present in this file or to the
single public merge gate.  The homological leaves are deliberately marked as
adjacent anchors rather than terminal proofs of derived or spectral-sequence
specializations.
-/
def theoremTreeLeafLedger : List M0082TheoremTreeLeaf := [
  {
    code := "M0082-L001",
    packageCode := "P01",
    task := "record imports, namespace, universes, and Stage1 statement-boundary surface",
    localArtifact := "imports; namespace AwesomeTheorems.Stage1.S1_M_135; StatementShape",
    budget := "<=100",
    status := "checked_metadata"
  },
  {
    code := "M0082-L002",
    packageCode := "P02",
    task := "state the general right-adjoint theorem shape using `SolutionSetCondition`",
    localArtifact := "GeneralRightAdjointStatementShape",
    budget := "<=100",
    status := "checked_statement_shape"
  },
  {
    code := "M0082-L003",
    packageCode := "P02",
    task := "wrap mathlib's general AFT declaration",
    localArtifact := "generalRightAdjoint_of_solutionSetCondition",
    budget := "<=100",
    status := "checked_wrapper"
  },
  {
    code := "M0082-L004",
    packageCode := "P02",
    task := "witness the general statement shape from the local wrapper",
    localArtifact := "generalRightAdjointStatementShape_checked",
    budget := "<=100",
    status := "checked_wrapper"
  },
  {
    code := "M0082-L005",
    packageCode := "P03",
    task := "record the converse solution-set-condition anchor for right adjoints",
    localArtifact := "solutionSetCondition_of_rightAdjoint",
    budget := "<=100",
    status := "checked_anchor"
  },
  {
    code := "M0082-L006",
    packageCode := "P04",
    task := "state the special right-adjoint theorem shape",
    localArtifact := "SpecialRightAdjointStatementShape",
    budget := "<=100",
    status := "checked_statement_shape"
  },
  {
    code := "M0082-L007",
    packageCode := "P05",
    task := "state the dual special left-adjoint theorem shape",
    localArtifact := "SpecialLeftAdjointStatementShape",
    budget := "<=100",
    status := "checked_statement_shape"
  },
  {
    code := "M0082-L008",
    packageCode := "P04",
    task := "wrap the small-coseparating-class special AFT",
    localArtifact := "specialRightAdjoint_of_coseparating",
    budget := "<=100",
    status := "checked_wrapper"
  },
  {
    code := "M0082-L009",
    packageCode := "P05",
    task := "wrap the small-separating-class dual special AFT",
    localArtifact := "specialLeftAdjoint_of_separating",
    budget := "<=100",
    status := "checked_wrapper"
  },
  {
    code := "M0082-L010",
    packageCode := "P04",
    task := "witness the special right-adjoint statement shape from mathlib",
    localArtifact := "specialRightAdjointStatementShape_checked",
    budget := "<=100",
    status := "checked_wrapper"
  },
  {
    code := "M0082-L011",
    packageCode := "P05",
    task := "witness the dual special left-adjoint statement shape from mathlib",
    localArtifact := "specialLeftAdjointStatementShape_checked",
    budget := "<=100",
    status := "checked_wrapper"
  },
  {
    code := "M0082-L012",
    packageCode := "P06",
    task := "record preservation of colimits by left adjoints",
    localArtifact := "leftAdjoint_preservesColimitsOfSize",
    budget := "<=100",
    status := "checked_anchor"
  },
  {
    code := "M0082-L013",
    packageCode := "P06",
    task := "record preservation of limits by right adjoints",
    localArtifact := "rightAdjoint_preservesLimitsOfSize",
    budget := "<=100",
    status := "checked_anchor"
  },
  {
    code := "M0082-L014",
    packageCode := "P07",
    task := "combine the checked category-level AFT statement shapes",
    localArtifact := "statementShape_checked",
    budget := "<=100",
    status := "checked_wrapper"
  },
  {
    code := "M0082-L015",
    packageCode := "P07",
    task := "record audited mathlib modules and declaration names",
    localArtifact := "mathlibAnchorModules; mathlibAnchorNames; anchorAuditSearchTerms",
    budget := "<=100",
    status := "checked_metadata"
  },
  {
    code := "M0082-L016",
    packageCode := "P07",
    task := "record pinned revision, module, and public anchor table",
    localArtifact := "adjointFunctorTheoremsMathlibRevision; adjointFunctorTheoremsMathlibModule; publicAdjointFunctorTheoremsAnchorTable",
    budget := "<=100",
    status := "checked_metadata"
  },
  {
    code := "M0082-L017",
    packageCode := "P07",
    task := "record machine-status wording and the homological boundary note",
    localArtifact := "coreCategoryAFTMachineStatus; publicStatusBoundary",
    budget := "<=100",
    status := "checked_metadata"
  },
  {
    code := "M0082-L018",
    packageCode := "P08",
    task := "wrap long exact homology-sequence exactness as an adjacent API anchor",
    localArtifact := "HomologyLongExactStatement; homologyLongExactStatement_checked",
    budget := "<=100",
    status := "checked_adjacent_anchor_only"
  },
  {
    code := "M0082-L019",
    packageCode := "P08",
    task := "wrap connecting-morphism naturality as an adjacent API anchor",
    localArtifact := "homologyConnecting_naturality",
    budget := "<=100",
    status := "checked_adjacent_anchor_only"
  },
  {
    code := "M0082-L020",
    packageCode := "P09",
    task := "merge P01-P09 and M0082-L001-M0082-L020 into the public Stage1 theorem-tree surface",
    localArtifact := "this ledger plus theoremTreePackages and theoremTreeLeafLedger",
    budget := "<=100",
    status := "public_merge_pending"
  }
]

/-- The `THM-M-0082` public theorem-tree leaf ledger has exactly L001 through L020. -/
theorem theoremTreeLeafLedger_length : theoremTreeLeafLedger.length = 20 := rfl

/--
Completion gate for the theorem-tree child.

This child prepares checked repo-local package and leaf metadata.  It does not
edit public docs, does not expose a shared Lean aggregator, and therefore does
not by itself claim public theorem-tree completion.
-/
def theoremTreePublicMergeGate : String :=
  "P01-P09 and M0082-L001-M0082-L020 are repo-local checked metadata; serial public-doc merge remains pending"

end S1_M_135
end Stage1
end AwesomeTheorems
