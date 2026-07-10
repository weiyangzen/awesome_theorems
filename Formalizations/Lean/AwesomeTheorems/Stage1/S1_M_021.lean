/-!
# S1-M-021 / THM-M-0412: Pierce/Nagell-Lutz branch-scope audit

This Stage1 repair artifact records a conservative Lean 4 statement shape for the
repository entry currently described as the Pierce conjecture on integer points
of certain cubic curves.

The child identity audit found that the local metadata naming Trygve Nagell and
plane cubics matches the Nagell-Lutz theorem lineage, not a distinct Pierce
conjecture.  Until the public blueprint is serially backfilled, this file keeps
the older namespace-compatible module path and records the corrected source
identity as audit data below.

The public blueprint has not yet merged the exact primary-source theorem
identity, equation family, or Lean 4 object model.  This file therefore does not
claim a proof of the mathematical theorem.  It freezes the accepted theorem
branch scope that a later integrator can specialize once the source equation
family and Lean 4 anchor are known.
-/

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_021

/-- Affine rational coordinates for a Weierstrass cubic. -/
abbrev RationalAffinePoint : Type :=
  Rat × Rat

/--
Data needed to state the accepted Nagell-Lutz branch for a resolved cubic.

The fields deliberately keep the equation, torsion predicate, and divisibility
conclusion abstract.  The public Stage1 entry still needs a serial backfill that
chooses the exact Weierstrass normalization and mathlib object model.
-/
structure NagellLutzBranchData where
  curveName : String
  sourceCitation : String
  shortWeierstrassA : Int
  shortWeierstrassB : Int
  discriminantNormalization : Int
  isNonsingularIntegralWeierstrassCubic : Prop
  equation : RationalAffinePoint → Prop
  finiteOrder : RationalAffinePoint → Prop
  isTwoTorsion : RationalAffinePoint → Prop
  hasIntegralCoordinates : RationalAffinePoint → Prop
  twoTorsionBranchConclusion : RationalAffinePoint → Prop
  yCoordinateSquareDividesDiscriminant : RationalAffinePoint → Prop
  sourceIdentityResolvedAsNagellLutz : Prop
  acceptedBranchScope : Prop
  mathlibObjectModelAudited : Prop
  arithmeticInfrastructure : Prop

/--
Legacy alias retained for namespace compatibility while the public title still
uses Pierce/Nagell wording.
-/
abbrev PierceCubicIntegralPointData : Type :=
  NagellLutzBranchData

/-- Affine integral coordinates for the accepted branch statement. -/
abbrev IntegralAffinePoint : Type :=
  Int × Int

/--
The accepted Nagell-Lutz branch scope:

* the curve is a nonsingular integral Weierstrass cubic;
* every finite-order affine point on it has integral coordinates;
* the two-torsion branch is separated from the non-two-torsion branch;
* the non-two-torsion branch carries the discriminant-divisibility conclusion.
-/
def NagellLutzAcceptedBranch (D : NagellLutzBranchData) : Prop :=
  D.isNonsingularIntegralWeierstrassCubic ∧
    ∀ P : RationalAffinePoint,
      D.equation P →
        D.finiteOrder P →
          D.hasIntegralCoordinates P ∧
            (D.isTwoTorsion P → D.twoTorsionBranchConclusion P) ∧
              (¬ D.isTwoTorsion P → D.yCoordinateSquareDividesDiscriminant P)

/--
Legacy name retained for earlier child-ledger references.  It now denotes the
Nagell-Lutz accepted branch, not a finite-list classification of all integral
points.
-/
def IntegralPointClassification (D : PierceCubicIntegralPointData) : Prop :=
  NagellLutzAcceptedBranch D

/--
The theorem-internal implication shape for the corrected Pierce/Nagell-Lutz
entry.

After public backfill, the later module should replace the abstract premises by
concrete mathlib or pinned external Lean 4 declarations for the selected
Weierstrass equation family.
-/
def NagellLutzTheorem (D : NagellLutzBranchData) : Prop :=
  D.sourceIdentityResolvedAsNagellLutz →
    D.acceptedBranchScope →
      D.mathlibObjectModelAudited →
      D.arithmeticInfrastructure →
        NagellLutzAcceptedBranch D

/-- Legacy name retained for the public slot's old Pierce/Nagell label. -/
def PierceNagellCubicTheorem (D : PierceCubicIntegralPointData) : Prop :=
  NagellLutzTheorem D

/--
Normalized Stage1 statement shape for THM-M-0412.

This is the single canonical replacement for the earlier private-ledger
conditional candidates.  It is intentionally a statement-shape predicate over a
theorem data package, not a repo-local proof of the underlying
arithmetic-geometric theorem.
-/
def StatementShape : Prop :=
  ∀ D : NagellLutzBranchData,
    D.sourceIdentityResolvedAsNagellLutz →
      D.acceptedBranchScope →
        D.mathlibObjectModelAudited →
          D.arithmeticInfrastructure →
            NagellLutzAcceptedBranch D

/-- The normalized statement unfolds to the explicit data-parametrized form. -/
theorem statementShape_iff :
    StatementShape ↔
      ∀ D : NagellLutzBranchData,
        D.sourceIdentityResolvedAsNagellLutz →
          D.acceptedBranchScope →
            D.mathlibObjectModelAudited →
            D.arithmeticInfrastructure →
              NagellLutzAcceptedBranch D :=
  Iff.rfl

/--
Compatibility check: the canonical `StatementShape` is propositionally the same
as the legacy Nagell-Lutz theorem-package wrapper, but it is no longer presented
as one of several conditional candidates.
-/
theorem statementShape_iff_legacyNagellLutzWrapper :
    StatementShape ↔ ∀ D : NagellLutzBranchData, NagellLutzTheorem D :=
  Iff.rfl

/--
Checked wrapper: a proof of the statement shape supplies the integral-point
branch result for any resolved cubic data package satisfying the audited source,
accepted branch, object-model, and infrastructure predicates.
-/
theorem acceptedBranch_of_statementShape
    (h : StatementShape) (D : NagellLutzBranchData)
    (hsource : D.sourceIdentityResolvedAsNagellLutz)
    (hbranch : D.acceptedBranchScope)
    (hmodel : D.mathlibObjectModelAudited)
    (hinfra : D.arithmeticInfrastructure) :
    NagellLutzAcceptedBranch D :=
  h D hsource hbranch hmodel hinfra

/-- Legacy wrapper name for earlier ledgers. -/
theorem classification_of_statementShape
    (h : StatementShape) (D : PierceCubicIntegralPointData)
    (hsource : D.sourceIdentityResolvedAsNagellLutz)
    (hbranch : D.acceptedBranchScope)
    (hmodel : D.mathlibObjectModelAudited)
    (hinfra : D.arithmeticInfrastructure) :
    IntegralPointClassification D :=
  acceptedBranch_of_statementShape h D hsource hbranch hmodel hinfra

/-- Projection wrapper for the nonsingular integral Weierstrass support. -/
theorem nonsingularCubic_of_acceptedBranch {D : NagellLutzBranchData}
    (h : NagellLutzAcceptedBranch D) :
    D.isNonsingularIntegralWeierstrassCubic :=
  h.1

/-- Projection wrapper: finite-order affine points have integral coordinates. -/
theorem integralCoordinates_of_finiteOrder {D : NagellLutzBranchData}
    (h : NagellLutzAcceptedBranch D) {P : RationalAffinePoint}
    (heq : D.equation P) (htors : D.finiteOrder P) :
    D.hasIntegralCoordinates P :=
  ((h.2 P) heq htors).1

/-- Projection wrapper: the two-torsion case is an explicit branch. -/
theorem twoTorsionBranch_of_finiteOrder {D : NagellLutzBranchData}
    (h : NagellLutzAcceptedBranch D) {P : RationalAffinePoint}
    (heq : D.equation P) (htors : D.finiteOrder P)
    (h2 : D.isTwoTorsion P) :
    D.twoTorsionBranchConclusion P :=
  (((h.2 P) heq htors).2).1 h2

/-- Projection wrapper: non-two-torsion finite-order points satisfy divisibility. -/
theorem discriminantDivisibility_of_nonTwoTorsion {D : NagellLutzBranchData}
    (h : NagellLutzAcceptedBranch D) {P : RationalAffinePoint}
    (heq : D.equation P) (htors : D.finiteOrder P)
    (hnot2 : ¬ D.isTwoTorsion P) :
    D.yCoordinateSquareDividesDiscriminant P :=
  (((h.2 P) heq htors).2).2 hnot2

/-- Audit shape for a possible external Lean 4 theorem anchor. -/
structure ExternalLeanAnchorAudit where
  exactTheoremFound : Prop
  importedIntoLakeClosure : Prop
  concreteIntegrationBlockerRecorded : Prop

/--
Repo-local integration-debt gate: if an exact external Lean 4 proof is found,
it must either enter this Lake closure or be blocked by a concrete integration
reason.  Anchor-only evidence is not a completed state for this slot.
-/
def RepoLocalIntegrationDebtGate (A : ExternalLeanAnchorAudit) : Prop :=
  A.exactTheoremFound →
    A.importedIntoLakeClosure ∨ A.concreteIntegrationBlockerRecorded

/-- If no exact external anchor is found, the integration-debt gate is vacuous. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit) (h : ¬ A.exactTheoremFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/-- Mathlib areas that must be audited after the exact equation family is fixed. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Basic",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
  "Mathlib.AlgebraicGeometry.EllipticCurve.DivisionPolynomial.Basic",
  "Mathlib.AlgebraicGeometry.EllipticCurve.DivisionPolynomial.Degree",
  "Mathlib.Algebra.CubicDiscriminant",
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.NumberTheory.NumberField.ClassNumber",
  "Mathlib.NumberTheory.Padics.PadicIntegers",
  "Mathlib.RingTheory.DedekindDomain.Ideal.Basic",
  "Mathlib.RingTheory.Ideal.Norm.AbsNorm"
]

/--
Theorem-level mathlib audit row for the Stage1 public backfill.

`closureStatus` records whether the declaration is only reusable
infrastructure or a terminal theorem anchor for the Nagell-Lutz/Pierce slot.
-/
structure MathlibTheoremAuditRow where
  moduleName : String
  declarationName : String
  role : String
  closureStatus : String

/--
Mathlib theorem-level audit table for `S1-M-021-public-003`.

The table is intentionally data-only: it records checked local mathlib
declarations and their roles, but it does not assert that mathlib already
contains the Nagell-Lutz theorem or the repository's older Pierce-labelled
integer-point theorem.
-/
def mathlibTheoremLevelAudit : List MathlibTheoremAuditRow := [
  {
    moduleName := "Mathlib.Algebra.CubicDiscriminant",
    declarationName := "Cubic",
    role := "cubic-polynomial object for the two-torsion polynomial and discriminant vocabulary",
    closureStatus := "infrastructure_only; no terminal Pierce/Nagell-Lutz integer-point theorem"
  },
  {
    moduleName := "Mathlib.Algebra.CubicDiscriminant",
    declarationName := "Cubic.discr",
    role := "discriminant expression for cubic polynomials",
    closureStatus := "infrastructure_only; supports discriminant normalization audit"
  },
  {
    moduleName := "Mathlib.Algebra.CubicDiscriminant",
    declarationName := "Cubic.discr_ne_zero_iff_roots_nodup",
    role := "nonsingularity-style bridge from nonzero cubic discriminant to distinct roots",
    closureStatus := "supporting_lemma_only; not an integral-point or torsion classification"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    declarationName := "WeierstrassCurve",
    role := "candidate object model for the resolved integral Weierstrass cubic",
    closureStatus := "object_model_available; exact statement still not repo-local closed"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    declarationName := "WeierstrassCurve.Δ",
    role := "Weierstrass discriminant used by the accepted Nagell-Lutz divisibility conclusion",
    closureStatus := "infrastructure_only; divisibility theorem not found"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    declarationName := "WeierstrassCurve.IsElliptic",
    role := "nonzero or unit discriminant hypothesis for elliptic Weierstrass curves",
    closureStatus := "hypothesis_api_available; terminal theorem absent"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    declarationName := "WeierstrassCurve.twoTorsionPolynomial",
    role := "2-torsion polynomial whose roots describe nonzero 2-torsion x-coordinates",
    closureStatus := "two_torsion_infrastructure_only"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    declarationName := "WeierstrassCurve.twoTorsionPolynomial_discr",
    role := "relates the two-torsion polynomial discriminant to the Weierstrass discriminant",
    closureStatus := "supporting_lemma_only; no finite-order integral-coordinate closure"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
    declarationName := "WeierstrassCurve.Affine.Point",
    role := "affine point type for the future rational/integral coordinate bridge",
    closureStatus := "point_api_available; exact integral-coordinate predicate still local"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
    declarationName := "WeierstrassCurve.Affine.Point.instAddCommGroup",
    role := "group law on nonsingular affine points over a field",
    closureStatus := "group_law_available; no Nagell-Lutz torsion theorem found"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
    declarationName := "WeierstrassCurve.Affine.Point.toClass",
    role := "bridge from affine points to the coordinate-ring class group",
    closureStatus := "adjacent_infrastructure_only; not a terminal anchor"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point",
    declarationName := "WeierstrassCurve.Projective.Point",
    role := "projective nonsingular point type and alternate group-law surface",
    closureStatus := "point_api_available; not selected as terminal statement yet"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point",
    declarationName := "WeierstrassCurve.Projective.Point.toAffineAddEquiv",
    role := "additive equivalence from projective points to affine points over a field",
    closureStatus := "bridge_available; no integral Nagell-Lutz closure"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
    declarationName := "WeierstrassCurve.IsIntegral",
    role := "integral model hypothesis for Weierstrass curves over fraction fields",
    closureStatus := "model_infrastructure_only"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
    declarationName := "WeierstrassCurve.integralModel",
    role := "constructs an integral Weierstrass model from an integral hypothesis",
    closureStatus := "model_infrastructure_only; no torsion-point divisibility result"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
    declarationName := "WeierstrassCurve.exists_isIntegral",
    role := "existence of an integral model after variable change",
    closureStatus := "supporting_theorem_only"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
    declarationName := "WeierstrassCurve.exists_isMinimal",
    role := "existence of a minimal integral model for reduction arguments",
    closureStatus := "supporting_theorem_only; terminal theorem still formalization_debt"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
    declarationName := "WeierstrassCurve.HasGoodReduction",
    role := "local reduction predicate likely needed by a proof package",
    closureStatus := "local_reduction_infrastructure_only"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.DivisionPolynomial.Basic",
    declarationName := "WeierstrassCurve.Ψ₂Sq_eq",
    role := "connects the second division polynomial square with the two-torsion polynomial",
    closureStatus := "division_polynomial_infrastructure_only"
  },
  {
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.DivisionPolynomial.Basic",
    declarationName := "WeierstrassCurve.map_Ψ",
    role := "base-map compatibility for division polynomials",
    closureStatus := "supporting_lemma_only; no exact finite-order point theorem"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.Basic",
    declarationName := "NumberField",
    role := "number-field context for any descent, valuation, or ideal-theoretic proof branch",
    closureStatus := "ambient_infrastructure_only"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.ClassNumber",
    declarationName := "NumberField.classNumber",
    role := "class-number API for possible ideal-class arguments",
    closureStatus := "ambient_infrastructure_only"
  },
  {
    moduleName := "Mathlib.NumberTheory.Padics.PadicIntegers",
    declarationName := "PadicInt",
    role := "p-adic integer API adjacent to Lutz-style local arguments",
    closureStatus := "ambient_infrastructure_only; no Lutz theorem anchor found"
  },
  {
    moduleName := "Mathlib.RingTheory.DedekindDomain.Ideal.Basic",
    declarationName := "IsDedekindDomain",
    role := "Dedekind-domain ideal infrastructure for arithmetic reductions",
    closureStatus := "ambient_infrastructure_only"
  },
  {
    moduleName := "Mathlib.RingTheory.Ideal.Norm.AbsNorm",
    declarationName := "Ideal.absNorm",
    role := "ideal norm infrastructure for possible local/global arithmetic branches",
    closureStatus := "ambient_infrastructure_only"
  },
  {
    moduleName := "pinned local mathlib source tree",
    declarationName := "Pierce / Nagell / Nagell-Lutz terminal theorem",
    role := "exact theorem anchor search by public title and accepted theorem identity",
    closureStatus := "not_found_locally; current status remains not_repo_local_closed"
  }
]

/-- External search terms retained for the later primary-source anchor pass. -/
def externalAnchorSearchTerms : List String := [
  "Nagell Lutz theorem Lean 4",
  "Lutz Nagell theorem torsion elliptic curve Lean",
  "finite order rational point integral coordinates elliptic curve Lean",
  "y^2 divides discriminant torsion point Lean",
  "Pierce conjecture integer points cubic curves Lean 4",
  "Pierce Nagell conjecture cubic curve integral points Lean",
  "Trygve Nagell 1948 cubic curves integer points",
  "Trygve Nagell 1935 cubiques planes premier genre Lean",
  "Pierce conjecture Diophantine equation cubic curve",
  "integral points cubic curves Lean mathlib"
]

/-- External Lean project search row for `S1-M-021-public-004`. -/
structure ExternalLeanProjectSearchRow where
  searchDate : String
  query : String
  searchSurface : String
  url : String
  commit : String
  moduleName : String
  theoremName : String
  lakeCompatibility : String
  resultStatus : String

/--
External Lean 4 project audit for the exact Nagell-Lutz/Pierce equation family.

No row below is a proof anchor.  The table records that the checked external
surfaces did not expose a Lean 4 theorem named for Nagell-Lutz/Lutz-Nagell or
for the exact torsion-point discriminant-divisibility family.
-/
def externalLeanProjectAudit : List ExternalLeanProjectSearchRow := [
  {
    searchDate := "2026-05-01",
    query := "\"Nagell-Lutz\" language:Lean",
    searchSurface := "GitHub web code search",
    url := "https://github.com/search?q=%22Nagell-Lutz%22+language%3ALean&type=code",
    commit := "not_applicable_no_result",
    moduleName := "not_applicable_no_result",
    theoremName := "not_applicable_no_result",
    lakeCompatibility := "not_applicable_no_result",
    resultStatus := "result_count_0; no external Lean 4 theorem anchor found"
  },
  {
    searchDate := "2026-05-01",
    query := "\"Lutz-Nagell\" language:Lean",
    searchSurface := "GitHub web code search",
    url := "https://github.com/search?q=%22Lutz-Nagell%22+language%3ALean&type=code",
    commit := "not_applicable_no_result",
    moduleName := "not_applicable_no_result",
    theoremName := "not_applicable_no_result",
    lakeCompatibility := "not_applicable_no_result",
    resultStatus := "result_count_0; no external Lean 4 theorem anchor found"
  },
  {
    searchDate := "2026-05-01",
    query := "\"Nagell\" \"WeierstrassCurve\"",
    searchSurface := "GitHub web code search",
    url := "https://github.com/search?q=%22Nagell%22+%22WeierstrassCurve%22&type=code",
    commit := "not_applicable_no_result",
    moduleName := "not_applicable_no_result",
    theoremName := "not_applicable_no_result",
    lakeCompatibility := "not_applicable_no_result",
    resultStatus := "result_count_0; no external Lean 4 theorem anchor found"
  },
  {
    searchDate := "2026-05-01",
    query := "Nagell|Lutz|torsion.*integral|integral.*torsion|y.*divides.*discriminant|discriminant.*torsion",
    searchSurface := "repo-local pinned mathlib source rg",
    url := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    moduleName := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    theoremName := "none_terminal_for_Nagell_Lutz",
    lakeCompatibility := "compatible_with_current_lake_manifest_mathlib_pin",
    resultStatus := "only infrastructure hits; no exact finite-order rational point integrality or y^2-discriminant divisibility theorem"
  },
  {
    searchDate := "2026-05-01",
    query := "Nagell / Lutz package search",
    searchSurface := "Reservoir package endpoint probe",
    url := "https://reservoir.lean-lang.org/",
    commit := "not_applicable_no_result",
    moduleName := "not_applicable_no_result",
    theoremName := "not_applicable_no_result",
    lakeCompatibility := "not_applicable_no_result",
    resultStatus := "no package endpoint result exposing a candidate external Lean 4 project"
  }
]

/-- Preconditions for creating a terminal repo-local wrapper theorem. -/
structure RepoLocalWrapperReadiness where
  exactConcreteStatementKnown : Prop
  exactMachineAnchorKnown : Prop
  anchorImportedIntoLakeOrBlocked : Prop
  publicBackfillSeriallyMerged : Prop
  theoremTreeBudgetChecked : Prop

/--
Gate for `S1-M-021-public-005`: a terminal repo-local proof wrapper may only be
created after the concrete statement, exact machine anchor, integration status,
public backfill, and theorem-tree budget are all known.

The existing declarations in this file are statement/projection wrappers over
abstract data.  They are not terminal wrappers around a mathlib or external Lean
proof of Nagell-Lutz.
-/
def RepoLocalWrapperCreationGate (R : RepoLocalWrapperReadiness) : Prop :=
  R.exactConcreteStatementKnown ∧
    R.exactMachineAnchorKnown ∧
      R.anchorImportedIntoLakeOrBlocked ∧
        R.publicBackfillSeriallyMerged ∧
          R.theoremTreeBudgetChecked

/-- Missing a concrete source statement blocks terminal wrapper creation. -/
theorem not_wrapperCreationGate_without_concrete_statement
    (R : RepoLocalWrapperReadiness) (h : ¬ R.exactConcreteStatementKnown) :
    ¬ RepoLocalWrapperCreationGate R := by
  intro hgate
  exact h hgate.1

/-- Missing an exact machine anchor blocks terminal wrapper creation. -/
theorem not_wrapperCreationGate_without_machine_anchor
    (R : RepoLocalWrapperReadiness) (h : ¬ R.exactMachineAnchorKnown) :
    ¬ RepoLocalWrapperCreationGate R := by
  intro hgate
  exact h hgate.2.1

/-- Current C005 wrapper gate audit for the public-doc integrator. -/
def repoLocalWrapperGateAudit : List String := [
  "S1-M-021-public-005 is blocked for terminal wrapper creation",
  "reason-001: the checked StatementShape is still abstract over NagellLutzBranchData, not a concrete mathlib Weierstrass object model",
  "reason-002: C004 found no exact external Lean 4 proof anchor with URL, commit, module, theorem name, and Lake compatibility",
  "reason-003: no mathlib terminal theorem for the Nagell-Lutz finite-order integrality and discriminant-divisibility branch is known",
  "safe-local-progress: keep only checked statement/projection wrappers and explicit wrapper-readiness gates",
  "completion-boundary: do not mark S1-M-021-public-005 complete until a concrete statement and exact machine anchor are imported or a concrete blocker is recorded"
]

/--
Integration status for `S1-M-021-public-006`.

This is deliberately separate from the wrapper gate: an exact external proof, if
one is later found, must either be pinned/imported/checked in this repository or
blocked by a concrete integration reason.  A bare URL/theorem-name anchor is not
a completed repo-local state.
-/
structure ExternalProofIntegrationStatus where
  exactExternalProofExists : Prop
  pinnedIntoLakeClosure : Prop
  importedAndCheckedLocally : Prop
  concreteIntegrationBlocker : Prop

/--
C006 integration gate.  If an exact external proof exists, the repository must
either have it in the local Lake closure with a local check, or record a concrete
blocker.
-/
def ExternalProofIntegrationGate (S : ExternalProofIntegrationStatus) : Prop :=
  S.exactExternalProofExists →
    (S.pinnedIntoLakeClosure ∧ S.importedAndCheckedLocally) ∨
      S.concreteIntegrationBlocker

/-- If no exact external proof exists, C006 has no external proof to integrate. -/
theorem externalProofIntegrationGate_of_no_external_proof
    (S : ExternalProofIntegrationStatus) (h : ¬ S.exactExternalProofExists) :
    ExternalProofIntegrationGate S := by
  intro hfound
  exact False.elim (h hfound)

/--
Anchor-only evidence fails the C006 gate whenever an external proof exists but
is neither pinned into the Lake closure nor blocked by a concrete reason.
-/
theorem not_externalProofIntegrationGate_with_anchor_only
    (S : ExternalProofIntegrationStatus)
    (hexists : S.exactExternalProofExists)
    (hnotPinned : ¬ S.pinnedIntoLakeClosure)
    (hnotBlocked : ¬ S.concreteIntegrationBlocker) :
    ¬ ExternalProofIntegrationGate S := by
  intro hgate
  cases hgate hexists with
  | inl hlocal =>
      exact hnotPinned hlocal.1
  | inr hblocker =>
      exact hnotBlocked hblocker

/-- Current C006 external-proof integration audit for the public-doc integrator. -/
def externalProofIntegrationAuditC006 : List String := [
  "S1-M-021-public-006 is an external-proof integration gate, not a theorem-completion claim",
  "current-result: no exact external Lean 4 proof exists in the C004/C006 audit, so there is no URL/commit/module/theorem candidate to pin or import",
  "web-search-2026-05-01: Nagell-Lutz, Lutz-Nagell, Nagell plus WeierstrassCurve, and torsion-discriminant Lean searches found no exact Lean 4 proof anchor",
  "repo-local-result: local pinned mathlib has elliptic-curve, Weierstrass, cubic-discriminant, reduction, and division-polynomial infrastructure, but no terminal Nagell-Lutz proof theorem",
  "integration-action: no external dependency was added because no exact external proof candidate was identified",
  "blocker-if-later-found: an exact external candidate must provide URL, revision, module, theorem name, license compatibility, Lake/toolchain compatibility, and a placeholder-free local check path",
  "completion-boundary: anchor-only evidence must remain open; no completed state may retain repo_local_integration_debt"
]

/-- Current machine-proof debt classification for this repaired Stage1 module. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: source identity and accepted branch are recorded only at documentation/audit level",
  "not_repo_local_closed: this module is a checked statement shape and projection-wrapper package only",
  "repo_local_integration_debt is not asserted because no exact external Lean 4 proof anchor has been imported or identified",
  "external_upstream_anchor_only is not present for S1-M-021-public-004 because the external search found no URL/commit/module/theorem Lake candidate",
  "S1-M-021-public-005 remains blocked for terminal repo-local wrapper creation until the concrete statement and exact machine anchor are known",
  "S1-M-021-public-006 has no external proof to pin/import/check; if one appears, anchor-only evidence must be replaced by a local Lake check or a concrete integration blocker"
]

/-- Primary-source identity audit for the Stage1 public backfill. -/
def primarySourceIdentityAudit : List String := [
  "public-title-conflict: Pierce conjecture is not supported by the inspected cubic-curve sources",
  "resolved-title: Nagell-Lutz theorem, rooted in Nagell's theorem on arithmetic of plane cubics of genus one",
  "primary-source: Trygve Nagell, Solution de quelques problemes dans la theorie arithmetique des cubiques planes du premier genre, Skrifter Norske Videnskaps-Akademi i Oslo, 1935, no. 1",
  "independent-source: Elisabeth Lutz, Sur l'equation y^2 = x^3 - A x - B dans les corps p-adiques, Journal fur die reine und angewandte Mathematik 177, 1937",
  "equation-family: nonsingular integral Weierstrass cubic y^2 = x^3 + a*x^2 + b*x + c, often specialized to y^2 = x^3 + A*x + B or y^2 = x^3 - A*x - B",
  "accepted-branch: rational finite-order affine points on the selected curve",
  "two-torsion-branch: order-two points are separated before divisibility is asserted",
  "non-two-torsion-branch: a finite-order point has integral affine coordinates and its y-coordinate square divides the discriminant normalization of the cubic",
  "repo-action: backfill public docs as Nagell-Lutz theorem or mark the existing Pierce title as a source-identity error before any completion claim"
]

/-- Current accepted branch scope for the public-doc integrator. -/
def acceptedBranchScopeAudit : List String := [
  "not-conjecture-only: after identity correction, the accepted branch is the classical Nagell-Lutz theorem",
  "not-completed: no repo-local proof body, mathlib theorem wrapper, or pinned external proof is present",
  "statement-root: nonsingular integral Weierstrass cubic over Q with integer coefficients",
  "input-branch: affine rational finite-order point satisfying the selected cubic equation",
  "branch-001: coordinate integrality for every finite-order affine point",
  "branch-002: two-torsion points are handled separately, conventionally by y = 0 in short Weierstrass form",
  "branch-003: non-two-torsion points satisfy y^2 divisibility by the selected discriminant normalization",
  "blocker-if-unresolved: if public docs do not accept the Nagell-Lutz identity correction, this slot remains a source-identity blocker rather than a completion task"
]

/-- One M0387-level theorem-tree leaf budget row for the C007 public task. -/
structure TheoremTreeLeafBudgetRow where
  leafId : String
  parentNode : String
  obligation : String
  requiredInput : String
  outputInterface : String
  declaredMaxLocalSteps : Nat
  status : String

/--
C007 theorem-tree expansion.

Every row declares the local proof-process budget expected of the eventual
leaf.  The current rows are intentionally `unchecked`: the exact concrete
statement and terminal machine anchor are still not known, so this child pass
may expand and typecheck the budget ledger but may not mark any leaf closed.
-/
def theoremTreeBudgetC007 : List TheoremTreeLeafBudgetRow := [
  {
    leafId := "S1-M-021-C007-L001",
    parentNode := "root.identity",
    obligation := "Serially merge the Nagell-Lutz identity correction into the public blueprint before any theorem-completion checkbox is changed.",
    requiredInput := "primary-source citation and accepted replacement title",
    outputInterface := "public statement identity accepted by integrator",
    declaredMaxLocalSteps := 100,
    status := "unchecked_public_backfill_required"
  },
  {
    leafId := "S1-M-021-C007-L002",
    parentNode := "root.statement",
    obligation := "Freeze the exact integral Weierstrass equation family, including coefficient domain and normalization.",
    requiredInput := "source theorem equation family",
    outputInterface := "concrete equation predicate replacing the abstract equation field",
    declaredMaxLocalSteps := 100,
    status := "unchecked_exact_statement_missing"
  },
  {
    leafId := "S1-M-021-C007-L003",
    parentNode := "root.statement",
    obligation := "Freeze the nonsingularity and discriminant-normalization hypotheses in the same vocabulary as the selected equation family.",
    requiredInput := "source discriminant convention and mathlib discriminant API",
    outputInterface := "checked nonsingular integral Weierstrass hypothesis",
    declaredMaxLocalSteps := 100,
    status := "unchecked_exact_statement_missing"
  },
  {
    leafId := "S1-M-021-C007-L004",
    parentNode := "root.statement",
    obligation := "Specify the rational affine point type and the integral-coordinate predicate used by the theorem conclusion.",
    requiredInput := "source convention for affine rational points and integral coordinates",
    outputInterface := "coordinate-integrality predicate compatible with mathlib points",
    declaredMaxLocalSteps := 100,
    status := "unchecked_object_model_missing"
  },
  {
    leafId := "S1-M-021-C007-L005",
    parentNode := "root.statement",
    obligation := "Specify the finite-order or torsion predicate and its connection to the selected curve group law.",
    requiredInput := "mathlib affine/projective group-law surface",
    outputInterface := "finite-order predicate for points on the selected curve",
    declaredMaxLocalSteps := 100,
    status := "unchecked_object_model_missing"
  },
  {
    leafId := "S1-M-021-C007-L006",
    parentNode := "branch.two_torsion",
    obligation := "Separate the two-torsion branch before asserting the non-two-torsion divisibility conclusion.",
    requiredInput := "two-torsion predicate and source branch convention",
    outputInterface := "two-torsion branch theorem obligation",
    declaredMaxLocalSteps := 100,
    status := "unchecked_statement_branch_missing"
  },
  {
    leafId := "S1-M-021-C007-L007",
    parentNode := "branch.non_two_torsion",
    obligation := "State the non-two-torsion y-coordinate-square divisibility conclusion using the selected discriminant normalization.",
    requiredInput := "source divisibility statement and discriminant convention",
    outputInterface := "non-two-torsion divisibility theorem obligation",
    declaredMaxLocalSteps := 100,
    status := "unchecked_statement_branch_missing"
  },
  {
    leafId := "S1-M-021-C007-L008",
    parentNode := "mathlib.object_model",
    obligation := "Audit whether the terminal statement should use WeierstrassCurve, affine points, projective points, or a custom source-family wrapper.",
    requiredInput := "exact source statement and pinned mathlib elliptic-curve API",
    outputInterface := "selected Lean object model with import list",
    declaredMaxLocalSteps := 100,
    status := "unchecked_anchor_missing"
  },
  {
    leafId := "S1-M-021-C007-L009",
    parentNode := "mathlib.object_model",
    obligation := "Bridge source coordinates to the selected mathlib curve equation.",
    requiredInput := "selected object model and equation predicate",
    outputInterface := "coordinate equation equivalence lemma obligation",
    declaredMaxLocalSteps := 100,
    status := "unchecked_anchor_missing"
  },
  {
    leafId := "S1-M-021-C007-L010",
    parentNode := "mathlib.object_model",
    obligation := "Bridge integral coefficients and rational coordinates through the selected algebra-map or coercion conventions.",
    requiredInput := "coefficient domain and mathlib coercion API",
    outputInterface := "integer-to-rational coefficient bridge obligation",
    declaredMaxLocalSteps := 100,
    status := "unchecked_anchor_missing"
  },
  {
    leafId := "S1-M-021-C007-L011",
    parentNode := "proof.infrastructure",
    obligation := "Audit which height, local-field, p-adic, or reduction APIs are required by a future Nagell-Lutz proof package.",
    requiredInput := "exact proof source or terminal machine anchor",
    outputInterface := "infrastructure dependency table",
    declaredMaxLocalSteps := 100,
    status := "unchecked_proof_source_missing"
  },
  {
    leafId := "S1-M-021-C007-L012",
    parentNode := "proof.infrastructure",
    obligation := "Split the local bad-prime or valuation branch if the selected proof source uses it.",
    requiredInput := "proof source local argument",
    outputInterface := "local valuation branch obligations",
    declaredMaxLocalSteps := 100,
    status := "unchecked_proof_source_missing"
  },
  {
    leafId := "S1-M-021-C007-L013",
    parentNode := "proof.infrastructure",
    obligation := "Split the minimal-model or variable-change branch if required by the selected theorem statement.",
    requiredInput := "proof source model-normalization argument",
    outputInterface := "minimal-model or variable-change obligations",
    declaredMaxLocalSteps := 100,
    status := "unchecked_proof_source_missing"
  },
  {
    leafId := "S1-M-021-C007-L014",
    parentNode := "proof.infrastructure",
    obligation := "Split the torsion-integrality argument into coordinate integrality and divisibility subgoals.",
    requiredInput := "proof source torsion argument",
    outputInterface := "coordinate-integrality and divisibility obligations",
    declaredMaxLocalSteps := 100,
    status := "unchecked_proof_source_missing"
  },
  {
    leafId := "S1-M-021-C007-L015",
    parentNode := "machine_anchor.mathlib",
    obligation := "Confirm that pinned mathlib has no terminal Nagell-Lutz theorem before treating the item as formalization debt.",
    requiredInput := "pinned mathlib source and exact theorem search terms",
    outputInterface := "mathlib theorem-level audit row",
    declaredMaxLocalSteps := 100,
    status := "unchecked_exact_statement_missing_for_final_search"
  },
  {
    leafId := "S1-M-021-C007-L016",
    parentNode := "machine_anchor.external",
    obligation := "Search external Lean 4 projects by the exact equation family and terminal theorem conclusion.",
    requiredInput := "exact equation family and conclusion",
    outputInterface := "URL, commit, module, theorem name, and Lake compatibility, or no-result row",
    declaredMaxLocalSteps := 100,
    status := "unchecked_exact_statement_missing_for_final_search"
  },
  {
    leafId := "S1-M-021-C007-L017",
    parentNode := "repo_local.integration",
    obligation := "If an external proof exists, pin/import/check it in the local Lake closure or record a concrete integration blocker.",
    requiredInput := "external proof URL, commit, module, theorem name, and toolchain",
    outputInterface := "external_upstream_pinned, local wrapper, or concrete blocker",
    declaredMaxLocalSteps := 100,
    status := "unchecked_no_external_anchor_found"
  },
  {
    leafId := "S1-M-021-C007-L018",
    parentNode := "repo_local.wrapper",
    obligation := "Create a terminal repo-local wrapper only after the concrete statement and exact machine anchor are known.",
    requiredInput := "concrete statement plus mathlib or pinned external anchor",
    outputInterface := "checked terminal wrapper theorem",
    declaredMaxLocalSteps := 100,
    status := "unchecked_wrapper_gate_blocked"
  },
  {
    leafId := "S1-M-021-C007-L019",
    parentNode := "repo_local.wrapper",
    obligation := "Keep the existing abstract StatementShape/projection wrappers separate from any future terminal theorem wrapper.",
    requiredInput := "current checked statement-shape module",
    outputInterface := "no false completion claim from abstract wrappers",
    declaredMaxLocalSteps := 100,
    status := "unchecked_terminal_wrapper_absent"
  },
  {
    leafId := "S1-M-021-C007-L020",
    parentNode := "validation",
    obligation := "Run the theorem-specific Lean check after each scoped Lean edit.",
    requiredInput := "owned Stage1 Lean module",
    outputInterface := "lake env lean validation result",
    declaredMaxLocalSteps := 100,
    status := "checked_for_this_child_artifact_only"
  },
  {
    leafId := "S1-M-021-C007-L021",
    parentNode := "public.merge_gate",
    obligation := "Backfill the public blueprint only through a serial integrator merge, not from this child worker.",
    requiredInput := "child ledger and checked Lean audit data",
    outputInterface := "public backfill proposal",
    declaredMaxLocalSteps := 100,
    status := "unchecked_public_backfill_required"
  },
  {
    leafId := "S1-M-021-C007-L022",
    parentNode := "public.merge_gate",
    obligation := "Keep public completion checkboxes open until exact statement, anchor audit, integration gate, and leaf-budget gate all close.",
    requiredInput := "M0387 completion gates",
    outputInterface := "no premature public completion state",
    declaredMaxLocalSteps := 100,
    status := "unchecked_completion_blocked"
  },
  {
    leafId := "S1-M-021-C007-L023",
    parentNode := "debt.classification",
    obligation := "Classify current debt as formalization debt/not_repo_local_closed rather than repo-local integration debt in a completed state.",
    requiredInput := "C004/C006 no-anchor result",
    outputInterface := "machine-proof debt classification",
    declaredMaxLocalSteps := 100,
    status := "checked_for_current_no_anchor_diagnosis"
  },
  {
    leafId := "S1-M-021-C007-L024",
    parentNode := "debt.classification",
    obligation := "If a later exact external Lean proof is found, reopen the repo-local integration gate immediately.",
    requiredInput := "future external proof candidate",
    outputInterface := "pin/import/check action or concrete integration blocker",
    declaredMaxLocalSteps := 100,
    status := "unchecked_future_contingency"
  }
]

/-- Number of C007 theorem-tree leaves currently recorded in the checked module. -/
def theoremTreeBudgetC007LeafCount : Nat :=
  theoremTreeBudgetC007.length

/-- The C007 expansion stays below the public `<=100` leaf-count ceiling. -/
theorem theoremTreeBudgetC007_leafCount_eq :
    theoremTreeBudgetC007LeafCount = 24 :=
  rfl

/-- The C007 expansion has fewer than or equal to 100 theorem-tree leaves. -/
theorem theoremTreeBudgetC007_leafCount_le_100 :
    theoremTreeBudgetC007LeafCount ≤ 100 := by
  native_decide

/-- Gate record for changing C007 or parent public completion state. -/
structure TheoremTreeBudgetCompletionStatus where
  exactStatementKnown : Prop
  concreteMachineAnchorKnown : Prop
  leavesExpanded : Prop
  leavesCheckedWithin100 : Prop
  publicBackfillMerged : Prop

/--
C007 completion gate.  Expansion alone is not enough: the leaves must be checked
within the local budget after the exact statement and machine anchor are known,
and the public merge-back must be serially completed.
-/
def TheoremTreeBudgetCompletionGate
    (B : TheoremTreeBudgetCompletionStatus) : Prop :=
  B.exactStatementKnown ∧
    B.concreteMachineAnchorKnown ∧
      B.leavesExpanded ∧
        B.leavesCheckedWithin100 ∧
          B.publicBackfillMerged

/-- Missing exact statement identity blocks the C007 completion gate. -/
theorem not_theoremTreeBudgetCompletionGate_without_exact_statement
    (B : TheoremTreeBudgetCompletionStatus)
    (h : ¬ B.exactStatementKnown) :
    ¬ TheoremTreeBudgetCompletionGate B := by
  intro hgate
  exact h hgate.1

/-- Missing checked `<=100` leaves blocks the C007 completion gate. -/
theorem not_theoremTreeBudgetCompletionGate_without_checked_leaves
    (B : TheoremTreeBudgetCompletionStatus)
    (h : ¬ B.leavesCheckedWithin100) :
    ¬ TheoremTreeBudgetCompletionGate B := by
  intro hgate
  exact h hgate.2.2.2.1

/-- Missing serial public backfill blocks the C007 completion gate. -/
theorem not_theoremTreeBudgetCompletionGate_without_public_backfill
    (B : TheoremTreeBudgetCompletionStatus)
    (h : ¬ B.publicBackfillMerged) :
    ¬ TheoremTreeBudgetCompletionGate B := by
  intro hgate
  exact h hgate.2.2.2.2

/-- C007 audit summary for the public-doc integrator. -/
def theoremTreeBudgetAuditC007 : List String := [
  "S1-M-021-public-007 expanded to 24 theorem-tree leaf budget rows in the checked Lean artifact",
  "leaf-count-gate: 24 <= 100 is locally checked by theoremTreeBudgetC007_leafCount_le_100",
  "leaf-closure-boundary: only artifact-validation and current debt-diagnosis rows are checked for this child pass; theorem proof leaves remain unchecked",
  "completion-blocker-001: exact concrete statement is still not merged into the public blueprint",
  "completion-blocker-002: no terminal mathlib or external Lean 4 theorem anchor is known",
  "completion-blocker-003: no repo-local terminal wrapper theorem exists",
  "completion-blocker-004: public backfill must be serially merged by an integrator",
  "repo-local-integration-debt-gate: no completed state is claimed; if a later external proof exists, pin/import/check or concrete blocker is mandatory"
]

/-- M0387-level theorem-internal child leaves for the next integrator pass. -/
def theoremInternalChildLeaves : List String := [
  "S1-M-021-C007-L001 root.identity serial public Nagell-Lutz identity backfill",
  "S1-M-021-C007-L002 root.statement exact integral Weierstrass equation family",
  "S1-M-021-C007-L003 root.statement nonsingularity and discriminant normalization",
  "S1-M-021-C007-L004 root.statement rational affine point and integral-coordinate predicate",
  "S1-M-021-C007-L005 root.statement finite-order or torsion predicate",
  "S1-M-021-C007-L006 branch.two_torsion explicit two-torsion split",
  "S1-M-021-C007-L007 branch.non_two_torsion y-coordinate-square discriminant divisibility",
  "S1-M-021-C007-L008 mathlib.object_model selected Lean object model and imports",
  "S1-M-021-C007-L009 mathlib.object_model source equation to mathlib curve equation bridge",
  "S1-M-021-C007-L010 mathlib.object_model integer-to-rational coefficient bridge",
  "S1-M-021-C007-L011 proof.infrastructure height/local-field/reduction API audit",
  "S1-M-021-C007-L012 proof.infrastructure bad-prime or valuation branch split",
  "S1-M-021-C007-L013 proof.infrastructure minimal-model or variable-change branch split",
  "S1-M-021-C007-L014 proof.infrastructure torsion-integrality argument split",
  "S1-M-021-C007-L015 machine_anchor.mathlib final mathlib terminal-theorem search",
  "S1-M-021-C007-L016 machine_anchor.external exact external Lean project search",
  "S1-M-021-C007-L017 repo_local.integration external proof pin/import/check or blocker",
  "S1-M-021-C007-L018 repo_local.wrapper terminal repo-local wrapper",
  "S1-M-021-C007-L019 repo_local.wrapper abstract-wrapper versus terminal-wrapper boundary",
  "S1-M-021-C007-L020 validation theorem-specific Lean check",
  "S1-M-021-C007-L021 public.merge_gate serial public blueprint backfill",
  "S1-M-021-C007-L022 public.merge_gate public completion checkbox remains open",
  "S1-M-021-C007-L023 debt.classification current formalization-debt/no-anchor diagnosis",
  "S1-M-021-C007-L024 debt.classification future external-proof integration contingency"
]

/-- C008 child status for validation plus serial public merge-back. -/
structure PublicBackfillValidationStatus where
  localLeanValidationPassed : Prop
  publicBackfillProposalPrepared : Prop
  childEditedPublicDocs : Prop
  theoremCompletionClaimed : Prop
  repoLocalIntegrationDebtRetainedInCompletedState : Prop

/--
C008 closure gate.

This child can close only as a validation and merge-back-preparation task: the
Lean file must validate locally, this private ledger must contain a public
backfill proposal, and public blueprint/README/meta surfaces must remain for a
serial integrator.  The gate also forbids theorem-completion claims and forbids
any completed state that retains repo-local integration debt.
-/
def PublicBackfillValidationGate
    (S : PublicBackfillValidationStatus) : Prop :=
  S.localLeanValidationPassed ∧
    S.publicBackfillProposalPrepared ∧
      ¬ S.childEditedPublicDocs ∧
        ¬ S.theoremCompletionClaimed ∧
          ¬ S.repoLocalIntegrationDebtRetainedInCompletedState

/-- Missing local Lean validation blocks C008 closure. -/
theorem not_publicBackfillValidationGate_without_local_validation
    (S : PublicBackfillValidationStatus)
    (h : ¬ S.localLeanValidationPassed) :
    ¬ PublicBackfillValidationGate S := by
  intro hgate
  exact h hgate.1

/-- Direct child edits to public docs block C008 closure. -/
theorem not_publicBackfillValidationGate_with_public_doc_edit
    (S : PublicBackfillValidationStatus)
    (h : S.childEditedPublicDocs) :
    ¬ PublicBackfillValidationGate S := by
  intro hgate
  exact hgate.2.2.1 h

/-- A theorem-completion claim blocks C008 closure for this validation child. -/
theorem not_publicBackfillValidationGate_with_completion_claim
    (S : PublicBackfillValidationStatus)
    (h : S.theoremCompletionClaimed) :
    ¬ PublicBackfillValidationGate S := by
  intro hgate
  exact hgate.2.2.2.1 h

/-- Repo-local integration debt cannot remain in a completed C008 state. -/
theorem not_publicBackfillValidationGate_with_repo_local_integration_debt
    (S : PublicBackfillValidationStatus)
    (h : S.repoLocalIntegrationDebtRetainedInCompletedState) :
    ¬ PublicBackfillValidationGate S := by
  intro hgate
  exact hgate.2.2.2.2 h

/-- C008 audit summary for the serial public-doc integrator. -/
def publicBackfillValidationAuditC008 : List String := [
  "S1-M-021-public-008 is validation plus serial merge-back preparation, not public-doc editing by this child",
  "local-validation-command: cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_021.lean",
  "local-validation-scope: checks the owned Stage1 statement-shape, audit rows, integration gates, C007 leaf budget, and C008 merge-back gate",
  "public-doc-boundary: Docs/Stage1_Blueprint.md, Docs/todos_20260430.md, README.md, README/meta surfaces, and Lean aggregators remain integrator-owned",
  "completion-boundary: do not mark S1-M-021 completed; exact concrete statement, terminal machine anchor, repo-local wrapper or pinned dependency, checked theorem leaves, and serial public merge-back remain open",
  "repo-local-integration-debt-gate: no external proof anchor was identified; if one is later found, anchor-only evidence must be replaced by pin/import/check or a concrete integration blocker"
]

/-- C008 remaining child leaves for validation and serial public merge-back. -/
def publicBackfillValidationLeavesC008 : List String := [
  "S1-M-021-C008-L001 validation rerun theorem-specific lake env lean command after the C008 gate edit",
  "S1-M-021-C008-L002 private ledger records exact validation result and child scope",
  "S1-M-021-C008-L003 private ledger proposes public blueprint/todo backfill text for a serial integrator",
  "S1-M-021-C008-L004 public README/meta/blueprint updates remain blocked on integrator merge-back",
  "S1-M-021-C008-L005 parent theorem completion remains blocked until M0387 gates close"
]

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check statementShape_iff_legacyNagellLutzWrapper
#check NagellLutzTheorem
#check NagellLutzAcceptedBranch
#check PierceNagellCubicTheorem
#check IntegralPointClassification
#check acceptedBranch_of_statementShape
#check classification_of_statementShape
#check integralCoordinates_of_finiteOrder
#check twoTorsionBranch_of_finiteOrder
#check discriminantDivisibility_of_nonTwoTorsion
#check RepoLocalIntegrationDebtGate
#check repoLocalIntegrationDebtGate_of_no_external_anchor
#check primarySourceIdentityAudit
#check acceptedBranchScopeAudit
#check mathlibTheoremLevelAudit
#check externalLeanProjectAudit
#check RepoLocalWrapperCreationGate
#check not_wrapperCreationGate_without_concrete_statement
#check not_wrapperCreationGate_without_machine_anchor
#check repoLocalWrapperGateAudit
#check ExternalProofIntegrationGate
#check externalProofIntegrationGate_of_no_external_proof
#check not_externalProofIntegrationGate_with_anchor_only
#check externalProofIntegrationAuditC006
#check theoremTreeBudgetC007
#check theoremTreeBudgetC007_leafCount_eq
#check theoremTreeBudgetC007_leafCount_le_100
#check TheoremTreeBudgetCompletionGate
#check not_theoremTreeBudgetCompletionGate_without_exact_statement
#check not_theoremTreeBudgetCompletionGate_without_checked_leaves
#check not_theoremTreeBudgetCompletionGate_without_public_backfill
#check theoremTreeBudgetAuditC007
#check theoremInternalChildLeaves
#check PublicBackfillValidationGate
#check not_publicBackfillValidationGate_without_local_validation
#check not_publicBackfillValidationGate_with_public_doc_edit
#check not_publicBackfillValidationGate_with_completion_claim
#check not_publicBackfillValidationGate_with_repo_local_integration_debt
#check publicBackfillValidationAuditC008
#check publicBackfillValidationLeavesC008

end S1_M_021
end Stage1
end AwesomeTheorems
