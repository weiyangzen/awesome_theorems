import Mathlib.AlgebraicGeometry.ZariskisMainTheorem
import Mathlib.AlgebraicGeometry.RationalMap

/-!
# S1-M-031 / THM-M-0107: Zariski's main theorem

This Stage1 artifact records the repo-local statement shape for the
Grothendieck reformulation of Zariski's main theorem already available in the
pinned mathlib dependency.
-/

open CategoryTheory Limits

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_031

open AlgebraicGeometry

universe u

variable {X Y : Scheme.{u}} (f : X ⟶ Y)

/-- Statement shape: for a separated finite-type morphism, the quasi-finite
locus is exactly the preimage of an open in the relative normalization on which
the normalization map is an isomorphism. -/
def StatementShape [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f] : Prop :=
  ∃ U : f.normalization.Opens, IsIso (f.toNormalization ∣_ U) ∧
    (f.toNormalization ⁻¹ᵁ U).1 = { x | f.QuasiFiniteAt x }

/-- Repo-local wrapper for mathlib's Grothendieck form of Zariski's main theorem. -/
theorem zariskiMain_mathlib_wrapper
    [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f] :
    StatementShape f :=
  AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization f

/-- Corollary wrapper: the quasi-finite locus of a finite-type morphism is open. -/
theorem quasiFiniteLocus_open_mathlib_wrapper [LocallyOfFiniteType f] :
    IsOpen { x | f.QuasiFiniteAt x } :=
  AlgebraicGeometry.Scheme.Hom.isOpen_quasiFiniteAt f

/-- Corollary wrapper: the quasi-finite locus maps by an open immersion to the
relative normalization under the separated finite-type quasi-compact hypotheses. -/
theorem quasiFiniteLocus_toNormalization_openImmersion_mathlib_wrapper
    [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f] :
    IsOpenImmersion (f.quasiFiniteLocus.ι ≫ f.toNormalization) :=
  inferInstance

/-- Corollary wrapper: a proper locally quasi-finite morphism is finite. -/
theorem finite_of_proper_of_locallyQuasiFinite_mathlib_wrapper
    [IsProper f] [LocallyQuasiFinite f] :
    IsFinite f :=
  IsFinite.of_isProper_of_locallyQuasiFinite f

/-- Corollary wrapper: finiteness is equivalent to properness plus local
quasi-finiteness for scheme morphisms. -/
theorem finite_iff_proper_and_locallyQuasiFinite_mathlib_wrapper :
    IsFinite f ↔ IsProper f ∧ LocallyQuasiFinite f :=
  AlgebraicGeometry.IsFinite.iff_isProper_and_locallyQuasiFinite f

/--
Checked rational-map substrate available in pinned mathlib.

This is deliberately only an API anchor: it does not assert a selected
birational-equivalence predicate for Zariski's main theorem.
-/
def RationalMapDomainDenseStatement : Prop :=
  ∀ (X Y : Scheme.{u}) (φ : X ⤏ Y), Dense (X := X) φ.domain

/-- Every mathlib scheme rational map has a dense domain of definition. -/
theorem rationalMapDomainDense_mathlib_anchor : RationalMapDomainDenseStatement := by
  intro X Y φ
  exact Scheme.RationalMap.dense_domain φ

/--
Checked function-field/rational-map bridge available in pinned mathlib for an
integral source and a locally finite-type target over a base.
-/
def FunctionFieldRationalMapBridgeStatement : Prop :=
  ∀ {S X Y : Scheme.{u}} (sX : X ⟶ S) (sY : Y ⟶ S)
    [IsIntegral X] [LocallyOfFiniteType sY],
      Nonempty ({ g : Spec X.functionField ⟶ Y //
          g ≫ sY = X.fromSpecStalk _ ≫ sX } ≃
        { g : X ⤏ Y // g.compHom sY = sX.toRationalMap })

/-- Local anchor for mathlib's function-field/rational-map equivalence. -/
theorem functionFieldRationalMapBridge_mathlib_anchor :
    FunctionFieldRationalMapBridgeStatement := by
  intro S X Y sX sY _ _
  exact ⟨Scheme.RationalMap.equivFunctionField sX sY⟩

/-- Machine-checkable audit rows for the "birational morphism property" phrase. -/
structure BirationalPhraseAudit where
  code : String
  checkedAnchor : String
  importModule : String
  stage1Decision : String
  repoLocalClosed : Bool

/--
Decision for `S1-M-031-C003`.

The Stage1 wrapper should represent THM-M-0107's phrase about properties of
birational morphisms by the checked ZMT/normalization theorem and its
quasi-finite/proper-finite corollaries.  Pinned mathlib has rational-map and
function-field infrastructure, checked above, but this audit found no selected
`IsBirational`/`Birational` theorem family in the local mathlib source to wrap
as an additional ZMT corollary.  Adding a standalone pair of rational maps here
would be only statement-shape support, not a repo-local closed theorem about
Zariski's main theorem.
-/
def birationalPhraseAudit : List BirationalPhraseAudit := [
  {
    code := "ZMT-BIR-01"
    checkedAnchor :=
      "Scheme.Hom.exists_isIso_morphismRestrict_toNormalization"
    importModule := "Mathlib.AlgebraicGeometry.ZariskisMainTheorem"
    stage1Decision :=
      "Use the Grothendieck relative-normalization ZMT wrapper as the checked birational-morphism-property content."
    repoLocalClosed := true
  },
  {
    code := "ZMT-BIR-02"
    checkedAnchor :=
      "Scheme.Hom.isOpen_quasiFiniteAt; IsOpenImmersion (f.quasiFiniteLocus.ι ≫ f.toNormalization)"
    importModule := "Mathlib.AlgebraicGeometry.ZariskisMainTheorem"
    stage1Decision :=
      "Use quasi-finite locus openness and the open-immersion normalization corollary as checked consequences."
    repoLocalClosed := true
  },
  {
    code := "ZMT-BIR-03"
    checkedAnchor :=
      "IsFinite.of_isProper_of_locallyQuasiFinite; IsFinite.iff_isProper_and_locallyQuasiFinite"
    importModule := "Mathlib.AlgebraicGeometry.ZariskisMainTheorem"
    stage1Decision :=
      "Use the proper plus locally-quasi-finite implies finite corollary as checked ZMT consequence."
    repoLocalClosed := true
  },
  {
    code := "ZMT-BIR-04"
    checkedAnchor :=
      "Scheme.RationalMap; Scheme.RationalMap.equivFunctionField"
    importModule := "Mathlib.AlgebraicGeometry.RationalMap"
    stage1Decision :=
      "Do not add an explicit IsBirational/RationalMap ZMT theorem for this slot without a selected birational-equivalence predicate and proof."
    repoLocalClosed := false
  }
]

/-- The birational-phrase audit has the four rows needed by `S1-M-031-C003`. -/
theorem birationalPhraseAudit_length : birationalPhraseAudit.length = 4 :=
  rfl

/-- Only the ZMT/corollary rows are repo-local closed theorem wrappers. -/
theorem birationalPhraseAudit_closed_rows :
    birationalPhraseAudit.map BirationalPhraseAudit.repoLocalClosed =
      [true, true, true, false] :=
  rfl

/-- Stable row codes for public backfill of the birational-phrase decision. -/
theorem birationalPhraseAudit_codes :
    birationalPhraseAudit.map BirationalPhraseAudit.code =
      ["ZMT-BIR-01", "ZMT-BIR-02", "ZMT-BIR-03", "ZMT-BIR-04"] :=
  rfl

/-! ## Explicit birational-statement source audit for `S1-M-031-C004`. -/

/-- Machine-checkable rows for the explicit-birational-statement audit. -/
structure ExplicitBirationalSourceAudit where
  code : String
  requestedSurface : String
  primarySourceResult : String
  localCheck : String
  c004Decision : String
  repoLocalClosed : Bool

/--
Decision for `S1-M-031-C004`.

The current Stage1 wrapper does not require an additional explicit
`IsBirational`/`RationalMap` theorem.  The checked local progress is the
Grothendieck normalization theorem and its corollaries, plus checked
rational-map/function-field substrate anchors.  The concrete integration
blocker for any future explicit birational branch is the absence, in the
pinned mathlib source, of a selected algebraic-geometry `Birational` or
`IsBirational` predicate/theorem family together with a ZMT bridge theorem.
-/
def explicitBirationalSourceAudit : List ExplicitBirationalSourceAudit := [
  {
    code := "ZMT-EXPL-BIR-01"
    requestedSurface := "Birational / IsBirational"
    primarySourceResult :=
      "No matching algebraic-geometry Birational or IsBirational symbol was found in the pinned mathlib source tree."
    localCheck :=
      "Local source audit against Formalizations/Lean/.lake/packages/mathlib/Mathlib returned no matches."
    c004Decision :=
      "Concrete integration blocker: select or define a birational-equivalence predicate and prove or import a ZMT bridge before marking an explicit birational statement complete."
    repoLocalClosed := false
  },
  {
    code := "ZMT-EXPL-BIR-02"
    requestedSurface := "RationalMap"
    primarySourceResult :=
      "Mathlib.AlgebraicGeometry.RationalMap defines Scheme.RationalMap, notation X ⤏ Y, RationalMap.IsOver, and RationalMap.dense_domain."
    localCheck :=
      "Imported Mathlib.AlgebraicGeometry.RationalMap and checked Scheme.RationalMap.dense_domain."
    c004Decision :=
      "Use as checked substrate only; do not promote a bare rational-map pair to an explicit ZMT birational theorem."
    repoLocalClosed := true
  },
  {
    code := "ZMT-EXPL-BIR-03"
    requestedSurface := "FunctionField"
    primarySourceResult :=
      "Mathlib.AlgebraicGeometry.FunctionField defines Scheme.functionField and RationalMap.equivFunctionField bridges function-field morphisms to rational maps."
    localCheck :=
      "Checked Scheme.RationalMap.equivFunctionField through functionFieldRationalMapBridge_mathlib_anchor."
    c004Decision :=
      "Use as checked rational-map/function-field substrate, not as a completed ZMT birational-property theorem."
    repoLocalClosed := true
  },
  {
    code := "ZMT-EXPL-BIR-04"
    requestedSurface := "toNormalization"
    primarySourceResult :=
      "Mathlib.AlgebraicGeometry.Normalization defines Scheme.Hom.toNormalization; Mathlib.AlgebraicGeometry.ZariskisMainTheorem proves exists_isIso_morphismRestrict_toNormalization."
    localCheck :=
      "Wrapped Scheme.Hom.exists_isIso_morphismRestrict_toNormalization as zariskiMain_mathlib_wrapper."
    c004Decision :=
      "This is the repo-local closed Grothendieck ZMT statement for the current Stage1 artifact."
    repoLocalClosed := true
  },
  {
    code := "ZMT-EXPL-BIR-05"
    requestedSurface := "open-immersion/isomorphism corollaries"
    primarySourceResult :=
      "Mathlib proves isOpen_quasiFiniteAt, the quasiFiniteLocus-to-normalization open-immersion instance, and proper plus locally-quasi-finite implies finite."
    localCheck :=
      "Wrapped quasiFiniteLocus_open_mathlib_wrapper, quasiFiniteLocus_toNormalization_openImmersion_mathlib_wrapper, and finite_of_proper_of_locallyQuasiFinite_mathlib_wrapper."
    c004Decision :=
      "These corollaries are repo-local closed wrappers and are the checked replacement for a currently unselected explicit birational theorem."
    repoLocalClosed := true
  }
]

/-- The explicit birational source audit has the five source surfaces requested by C004. -/
theorem explicitBirationalSourceAudit_length :
    explicitBirationalSourceAudit.length = 5 :=
  rfl

/--
Only the absent explicit `Birational`/`IsBirational` row is not repo-local
closed; it is deliberately recorded as a blocker rather than a completion.
-/
theorem explicitBirationalSourceAudit_closed_rows :
    explicitBirationalSourceAudit.map ExplicitBirationalSourceAudit.repoLocalClosed =
      [false, true, true, true, true] :=
  rfl

/-- The current wrapper does not require an additional explicit birational theorem. -/
def explicitBirationalStatementRequiredForCurrentWrapper : Bool := false

theorem explicitBirationalStatementRequiredForCurrentWrapper_eq_false :
    explicitBirationalStatementRequiredForCurrentWrapper = false :=
  rfl

/-! ## Theorem-tree leaf ledger for `S1-M-031-C005`. -/

/-- Machine-checkable rows for the public theorem-tree expansion of the ZMT nodes. -/
structure ZMTTheoremTreeLeaf where
  code : String
  upstreamNode : String
  sourceRange : String
  leafSummary : String
  budgetLe100 : Bool
  repoLocalAnchor : String

/--
`S1-M-031-C005` expansion of the upstream mathlib theorem-tree nodes.

The rows are source-aligned to
`Mathlib.AlgebraicGeometry.ZariskisMainTheorem` at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.  They are public-ledger leaves:
each row is a local proof-budget unit, not a new proof obligation beyond the
checked upstream theorem wrappers in this file.
-/
def zmtTheoremTreeLeaves : List ZMTTheoremTreeLeaf := [
  {
    code := "ZMT-TREE-01"
    upstreamNode := "exists_etale_isCompl_of_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:53-58"
    leafSummary :=
      "Choose affine neighborhoods around the base point and source point, restrict f to the affine chart, and expose the finite-type algebra map."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.exists_etale_isCompl_of_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-02"
    upstreamNode := "exists_etale_isCompl_of_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:59-68"
    leafSummary :=
      "Identify the prime of the source chart as lying over the base prime and transfer QuasiFiniteAt to Algebra.QuasiFiniteAt on coordinate rings."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.exists_etale_isCompl_of_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-03"
    upstreamNode := "exists_etale_isCompl_of_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:69-75"
    leafSummary :=
      "Apply the ring-theoretic etale quasi-finite theorem to obtain the etale algebra neighborhood and the distinguished idempotent element."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.exists_etale_isCompl_of_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-04"
    upstreamNode := "exists_etale_isCompl_of_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:76-85"
    leafSummary :=
      "Build the Spec pullback comparison map from the tensor-product affine chart to the geometric pullback."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.exists_etale_isCompl_of_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-05"
    upstreamNode := "exists_etale_isCompl_of_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:86-100"
    leafSummary :=
      "Define the finite open component W1 by the basic open and prove the restricted projection is finite."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.exists_etale_isCompl_of_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-06"
    upstreamNode := "exists_etale_isCompl_of_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:101-114"
    leafSummary :=
      "Take the open complement W2, prove IsCompl V W, and return the point witness mapping back to x."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.exists_etale_isCompl_of_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-07"
    upstreamNode := "exists_mem_and_isIso_morphismRestrict_toNormalization"
    sourceRange := "ZariskisMainTheorem.lean:122-138"
    leafSummary :=
      "Invoke the etale/complement construction at a quasi-finite point and set up the normalization over the complementary cover."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization"
  },
  {
    code := "ZMT-TREE-08"
    upstreamNode := "exists_mem_and_isIso_morphismRestrict_toNormalization"
    sourceRange := "ZariskisMainTheorem.lean:139-161"
    leafSummary :=
      "Use the coproduct normalization decomposition over the complementary opens to prove the local restricted normalization map is an isomorphism."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization"
  },
  {
    code := "ZMT-TREE-09"
    upstreamNode := "exists_mem_and_isIso_morphismRestrict_toNormalization"
    sourceRange := "ZariskisMainTheorem.lean:162-188"
    leafSummary :=
      "Push the local isomorphism from the etale pullback to f.normalization and descend isomorphy along a surjective flat locally finite-presentation morphism."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization"
  },
  {
    code := "ZMT-TREE-10"
    upstreamNode := "exists_isIso_morphismRestrict_toNormalization"
    sourceRange := "ZariskisMainTheorem.lean:209-219"
    leafSummary :=
      "Choose a local normalization-isomorphism open around every quasi-finite point and glue these opens by the iSup open cover."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization"
  },
  {
    code := "ZMT-TREE-11"
    upstreamNode := "exists_isIso_morphismRestrict_toNormalization"
    sourceRange := "ZariskisMainTheorem.lean:220-250"
    leafSummary :=
      "For a point in the chosen open, find affine/basic-open data inside the normalization open and reduce to an affine chart."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization"
  },
  {
    code := "ZMT-TREE-12"
    upstreamNode := "exists_isIso_morphismRestrict_toNormalization"
    sourceRange := "ZariskisMainTheorem.lean:251-288"
    leafSummary :=
      "Use the basic-open isomorphism with integral normalization and finite-type hypotheses to prove the original point is quasi-finite."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization"
  },
  {
    code := "ZMT-TREE-13"
    upstreamNode := "isOpen_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:292-309"
    leafSummary :=
      "Reduce openness to affine charts and transport QuasiFiniteAt through restrictions and open immersions."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.isOpen_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-14"
    upstreamNode := "isOpen_quasiFiniteAt"
    sourceRange := "ZariskisMainTheorem.lean:310-311"
    leafSummary :=
      "In the affine branch, obtain the ZMT normalization open and rewrite the quasi-finite locus as the preimage of that open."
    budgetLe100 := true
    repoLocalAnchor := "AlgebraicGeometry.Scheme.Hom.isOpen_quasiFiniteAt"
  },
  {
    code := "ZMT-TREE-15"
    upstreamNode := "quasiFiniteLocus-to-normalization open immersion instance"
    sourceRange := "ZariskisMainTheorem.lean:322-327"
    leafSummary :=
      "Convert the quasiFiniteLocus inclusion to the ZMT open using the locus equality and infer the open immersion to normalization."
    budgetLe100 := true
    repoLocalAnchor := "quasiFiniteLocus_toNormalization_openImmersion_mathlib_wrapper"
  }
]

/-- The C005 theorem-tree expansion has fifteen public budget leaves. -/
theorem zmtTheoremTreeLeaves_length : zmtTheoremTreeLeaves.length = 15 :=
  rfl

/-- Every C005 theorem-tree leaf is recorded as a `<=100`-step public budget unit. -/
theorem zmtTheoremTreeLeaves_all_budgeted :
    zmtTheoremTreeLeaves.map ZMTTheoremTreeLeaf.budgetLe100 =
      [true, true, true, true, true, true, true, true, true, true, true, true,
        true, true, true] :=
  rfl

/-- Stable row codes for public backfill of the C005 theorem-tree expansion. -/
theorem zmtTheoremTreeLeaves_codes :
    zmtTheoremTreeLeaves.map ZMTTheoremTreeLeaf.code =
      ["ZMT-TREE-01", "ZMT-TREE-02", "ZMT-TREE-03", "ZMT-TREE-04",
        "ZMT-TREE-05", "ZMT-TREE-06", "ZMT-TREE-07", "ZMT-TREE-08",
        "ZMT-TREE-09", "ZMT-TREE-10", "ZMT-TREE-11", "ZMT-TREE-12",
        "ZMT-TREE-13", "ZMT-TREE-14", "ZMT-TREE-15"] :=
  rfl

/-! ## Public-status integration gate for `S1-M-031-C006`. -/

/-- Machine-checkable rows for the C006 public merge-back/status gate. -/
structure PublicStatusGateRow where
  code : String
  surface : String
  gateResult : String
  publicStatusUpdateAllowedNow : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool

/--
Decision for `S1-M-031-C006`.

This worker cannot edit the authoritative public Stage1 checklist directly.
The local status is therefore integration-ready but not publicly completed in
`Docs/Stage1_Blueprint.md` until a serial integrator merges the ledger rows
back.  No row below treats `repo_local_integration_debt` as a completed state:
the ZMT wrappers are local wrappers over pinned mathlib, while the unselected
explicit birational branch remains a blocker rather than completion evidence.
-/
def publicStatusGateRows : List PublicStatusGateRow := [
  {
    code := "ZMT-STATUS-01"
    surface := "Docs/Stage1_Blueprint.md authoritative checklist"
    gateResult :=
      "Public status update is blocked for this child worker until serial public merge-back."
    publicStatusUpdateAllowedNow := false
    completedStateRetainsRepoLocalIntegrationDebt := false
  },
  {
    code := "ZMT-STATUS-02"
    surface := "Grothendieck normalization ZMT wrapper"
    gateResult :=
      "Repo-local closure is local_wrapper_upstream_mathlib via zariskiMain_mathlib_wrapper."
    publicStatusUpdateAllowedNow := false
    completedStateRetainsRepoLocalIntegrationDebt := false
  },
  {
    code := "ZMT-STATUS-03"
    surface := "quasi-finite/proper-finite corollary wrappers"
    gateResult :=
      "Repo-local closure is local_wrapper_upstream_mathlib via checked corollary wrappers."
    publicStatusUpdateAllowedNow := false
    completedStateRetainsRepoLocalIntegrationDebt := false
  },
  {
    code := "ZMT-STATUS-04"
    surface := "explicit IsBirational/RationalMap branch"
    gateResult :=
      "Not completed; concrete blocker is absence of a selected birational predicate and ZMT bridge theorem in the local pinned source audit."
    publicStatusUpdateAllowedNow := false
    completedStateRetainsRepoLocalIntegrationDebt := false
  }
]

/-- The C006 public-status gate records four status rows. -/
theorem publicStatusGateRows_length : publicStatusGateRows.length = 4 :=
  rfl

/-- C006 does not permit this child worker to update public status directly. -/
theorem publicStatusGateRows_no_public_update_now :
    publicStatusGateRows.map PublicStatusGateRow.publicStatusUpdateAllowedNow =
      [false, false, false, false] :=
  rfl

/-- No C006 row leaves `repo_local_integration_debt` in a completed state. -/
theorem publicStatusGateRows_no_completed_repo_local_integration_debt :
    publicStatusGateRows.map
        PublicStatusGateRow.completedStateRetainsRepoLocalIntegrationDebt =
      [false, false, false, false] :=
  rfl

/-- Stable row codes for public backfill of the C006 status gate. -/
theorem publicStatusGateRows_codes :
    publicStatusGateRows.map PublicStatusGateRow.code =
      ["ZMT-STATUS-01", "ZMT-STATUS-02", "ZMT-STATUS-03", "ZMT-STATUS-04"] :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check AlgebraicGeometry.Scheme.Hom.exists_isIso_morphismRestrict_toNormalization
#check AlgebraicGeometry.exists_etale_isCompl_of_quasiFiniteAt
#check AlgebraicGeometry.Scheme.Hom.isOpen_quasiFiniteAt
#check AlgebraicGeometry.IsFinite.iff_isProper_and_locallyQuasiFinite
#check Scheme.RationalMap
#check Scheme.RationalMap.equivFunctionField
#check Scheme.functionField
#check AlgebraicGeometry.Scheme.Hom.toNormalization
#check rationalMapDomainDense_mathlib_anchor
#check functionFieldRationalMapBridge_mathlib_anchor
#check birationalPhraseAudit
#check birationalPhraseAudit_length
#check birationalPhraseAudit_closed_rows
#check explicitBirationalSourceAudit
#check explicitBirationalSourceAudit_closed_rows
#check explicitBirationalStatementRequiredForCurrentWrapper_eq_false
#check zmtTheoremTreeLeaves
#check zmtTheoremTreeLeaves_all_budgeted
#check zmtTheoremTreeLeaves_codes
#check publicStatusGateRows
#check publicStatusGateRows_no_public_update_now
#check publicStatusGateRows_no_completed_repo_local_integration_debt

end S1_M_031
end Stage1
end AwesomeTheorems
