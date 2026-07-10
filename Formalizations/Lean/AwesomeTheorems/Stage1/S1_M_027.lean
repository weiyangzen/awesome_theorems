import Mathlib.Algebra.Homology.EulerCharacteristic
import Mathlib.AlgebraicGeometry.FunctionField
import Mathlib.AlgebraicGeometry.EllipticCurve.NormalForms
import Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Sites.Etale
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.RingTheory.DedekindDomain.Different

/-!
# S1-M-027 / THM-M-0105: Riemann-Roch theorem

This Stage1 repair artifact records a conservative Lean 4 statement boundary
for the classical Riemann-Roch theorem for algebraic curves and divisor
theory.  The pinned mathlib snapshot provides schemes, smooth/proper morphism
predicates, function fields of integral schemes, sheaf/module substrate, and
homological Euler characteristic APIs.

This file does not claim a proof of the full algebraic-curve Riemann-Roch
theorem.  It gives this slot its own namespace, statement shape, checked
projections, and integration-debt gate for any future external Lean 4 closure.
-/

noncomputable section

open AlgebraicGeometry
open CategoryTheory

universe u uD uι

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_027

/-- The base scheme attached to a field. -/
abbrev BaseSchemeOfField (K : Type u) [Field K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/--
Minimal algebraic-curve boundary for the classical Riemann-Roch theorem.

The checked fields use mathlib's scheme morphism predicates.  The two abstract
predicate fields record formalization gaps for "geometrically connected" and
"dimension one" until a future integrator chooses the exact mathlib or pinned
dependency APIs for curves.
-/
structure AlgebraicCurveBoundary
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Type (u + 1) where
  integral : IsIntegral X
  smooth : Smooth pi
  proper : IsProper pi
  IsGeometricallyConnected : Prop
  geometricallyConnected : IsGeometricallyConnected
  IsDimensionOne : Prop
  dimensionOne : IsDimensionOne

/--
Abstract divisor data for the curve-level Riemann-Roch formula.

`CurveDivisor`, `sub`, `degree`, `linearSeriesDimension`, `genus`, and
`canonicalDivisor` must eventually be replaced by concrete APIs for divisors,
line bundles, and sheaf cohomology on algebraic curves.
-/
structure RiemannRochDivisorData : Type (uD + 1) where
  CurveDivisor : Type uD
  sub : CurveDivisor -> CurveDivisor -> CurveDivisor
  degree : CurveDivisor -> Int
  linearSeriesDimension : CurveDivisor -> Int
  genus : Int
  canonicalDivisor : CurveDivisor

/--
Formula-level statement for Riemann-Roch on an abstract divisor package.

For every divisor `D`, the difference between the dimension of its linear
series and the dimension of the residual series attached to `K - D` equals
`deg(D) + 1 - g`.
-/
def RiemannRochFormula (A : RiemannRochDivisorData.{uD}) : Prop :=
  forall D : A.CurveDivisor,
    A.linearSeriesDimension D -
        A.linearSeriesDimension (A.sub A.canonicalDivisor D) =
      A.degree D + 1 - A.genus

/--
Normalized Stage1 statement shape for THM-M-0105.

Given a proper smooth integral dimension-one curve boundary over a base scheme,
there should be a concrete divisor package satisfying the Riemann-Roch formula.
The current repo-local module keeps this as a checked `Prop` boundary.
-/
def StatementShape
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Prop :=
  Nonempty (AlgebraicCurveBoundary S X pi) ->
    exists A : RiemannRochDivisorData.{uD}, RiemannRochFormula A

/--
THM-M-0105 named target for public statement-normalization backfill.

This is deliberately an alias for the Stage1 `StatementShape`, not a theorem
claim.  A public blueprint section can cite this exact Lean namespace and
declaration while keeping the slot under formalization debt.
-/
abbrev THM_M_0105_StatementShapeTarget
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Prop :=
  StatementShape.{u, uD} S X pi

/-! ## THM-M-0105 statement-normalization metadata -/

/-- Machine-readable notes for the public THM-M-0105 statement-normalization section. -/
structure StatementNormalization where
  targetNamespace : String
  targetDeclaration : String
  universePolicy : String
  inputBoundary : String
  formulaBoundary : String
  statusCaution : String

/-- Public backfill metadata: exact Lean target and no proof-completion claim. -/
def statementNormalization : StatementNormalization where
  targetNamespace := "AwesomeTheorems.Stage1.S1_M_027"
  targetDeclaration := "THM_M_0105_StatementShapeTarget.{u, uD} (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Prop"
  universePolicy := "universes u uD; u indexes schemes/base fields, uD indexes the abstract divisor package"
  inputBoundary := "Nonempty (AlgebraicCurveBoundary S X pi), where the checked fields are IsIntegral X, Smooth pi, and IsProper pi; geometrically connected and dimension-one assumptions remain abstract Prop fields"
  formulaBoundary := "exists A : RiemannRochDivisorData.{uD}, forall D : A.CurveDivisor, A.linearSeriesDimension D - A.linearSeriesDimension (A.sub A.canonicalDivisor D) = A.degree D + 1 - A.genus"
  statusCaution := "no_proof_completion_claim: this target is a checked statement boundary and not a repo-local proof of Riemann-Roch"

/-- The THM-M-0105 named target unfolds to the Stage1 statement shape. -/
theorem THM_M_0105_target_iff_statementShape
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) :
    THM_M_0105_StatementShapeTarget.{u, uD} S X pi <->
      StatementShape.{u, uD} S X pi :=
  Iff.rfl

/-- Checked guard that the public metadata carries no proof-completion claim. -/
theorem statementNormalization_statusCaution :
    statementNormalization.statusCaution =
      "no_proof_completion_claim: this target is a checked statement boundary and not a repo-local proof of Riemann-Roch" :=
  rfl

/-! ## Curve/divisor/cohomology package split -/

/--
Curve package for the M0387-level Riemann-Roch split.

This layer owns only the geometric input boundary.  The still-open choices are
the concrete APIs for geometrically connected and dimension-one curves.
-/
structure CurvePackage
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Type (u + 1) where
  boundary : AlgebraicCurveBoundary S X pi

/--
Divisor package for the M0387-level Riemann-Roch split.

The `apiSelected` and `divisorToSheafBridgeSelected` fields are propositions
recording future proof obligations.  They are deliberately not assumed in the
current Stage1 statement boundary.
-/
structure DivisorPackage : Type (uD + 1) where
  data : RiemannRochDivisorData.{uD}
  apiSelected : Prop
  divisorToSheafBridgeSelected : Prop

/--
Cohomology package for the M0387-level Riemann-Roch split.

This is the only package layer that contains the formula proof.  Therefore a
future value of this structure would be real proof-bearing closure, while the
current file merely specifies the boundary it must satisfy.
-/
structure CohomologyPackage (D : DivisorPackage.{uD}) : Type (uD + 1) where
  cohomologyDimensionModelSelected : Prop
  canonicalGenusModelSelected : Prop
  formula : RiemannRochFormula D.data

/--
Combined curve/divisor/cohomology package for a future full proof route.

Constructing this package for a fixed curve boundary is enough to produce the
current Stage1 statement shape, but this file does not construct such a value.
-/
structure CurveDivisorCohomologyPackage
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Type (max (u + 1) (uD + 1)) where
  curve : CurvePackage S X pi
  divisor : DivisorPackage.{uD}
  cohomology : CohomologyPackage divisor

/--
Future package-closure shape: a proof-bearing curve/divisor/cohomology package
exists for the selected geometric boundary.
-/
def PackageSplitClosure
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Prop :=
  Nonempty (CurveDivisorCohomologyPackage.{u, uD} S X pi)

/--
Checked reduction from a closed curve/divisor/cohomology package to the current
Riemann-Roch statement shape.

This is a conditional bridge only.  It does not assert `PackageSplitClosure`.
-/
theorem statementShape_of_packageSplitClosure
    {S X : Scheme.{u}} {pi : Scheme.Hom X S}
    (h : PackageSplitClosure.{u, uD} S X pi) :
    StatementShape.{u, uD} S X pi := by
  intro _hcurve
  rcases h with ⟨P⟩
  exact ⟨P.divisor.data, P.cohomology.formula⟩

/-- The package split closure unfolds to nonemptiness of the combined package. -/
theorem packageSplitClosure_iff_nonempty_package
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) :
    PackageSplitClosure.{u, uD} S X pi <->
      Nonempty (CurveDivisorCohomologyPackage.{u, uD} S X pi) :=
  Iff.rfl

/-- Metadata row for an integration-ready M0387 package leaf. -/
structure PackageSplitLeaf where
  id : String
  package : String
  objective : String
  currentRepoAnchor : String
  blockerOrGate : String
  debtClass : String

/-- Integration-ready package leaves for the curve/divisor/cohomology split. -/
def packageSplitLeaves : List PackageSplitLeaf := [
  {
    id := "S1-M-027-E001-curve-001",
    package := "curve",
    objective := "Select concrete mathlib or pinned-dependency APIs for smooth proper integral geometrically connected dimension-one curves",
    currentRepoAnchor := "AlgebraicCurveBoundary with checked IsIntegral, Smooth, and IsProper fields",
    blockerOrGate := "replace abstract geometrically connected and dimension-one Prop fields before proof completion",
    debtClass := "formalization_debt"
  },
  {
    id := "S1-M-027-E001-divisor-001",
    package := "divisor",
    objective := "Choose Cartier, Weil, or line-bundle-first divisor data and define degree, residual divisor K - D, and linear-series dimension",
    currentRepoAnchor := "RiemannRochDivisorData",
    blockerOrGate := "do not treat abstract divisor operations as a concrete divisor API",
    debtClass := "formalization_debt"
  },
  {
    id := "S1-M-027-E001-cohomology-001",
    package := "cohomology",
    objective := "Bridge divisor line bundles to global-section dimensions, Euler characteristic, genus, and the canonical divisor",
    currentRepoAnchor := "HomologicalComplexEulerChar plus CohomologyPackage.formula boundary",
    blockerOrGate := "full formula closure requires a proof of RiemannRochFormula for the selected divisor package",
    debtClass := "formalization_debt"
  },
  {
    id := "S1-M-027-E001-gate-001",
    package := "integration-gate",
    objective := "If an exact external Lean 4 proof is found, pin/import/check it or record a concrete integration blocker",
    currentRepoAnchor := "RepoLocalIntegrationDebtGate",
    blockerOrGate := "anchor-only evidence is not a completed state",
    debtClass := "repo_local_integration_debt_gate"
  }
]

/-- Explicit status for the E001 package-split child task. -/
def packageSplitStatus : List String := [
  "code/proof-boundary progress: added checked package-split structures and a conditional bridge theorem",
  "not a terminal proof: PackageSplitClosure is specified but not constructed",
  "public-doc integration required: serial integrator may backfill package leaves into Stage1 blueprint/todo",
  "completion gate: no completed state may retain anchor-only external evidence"
]

/-! ## THM-M-0105 mathlib anchor table -/

/--
One row of the integration-ready public mathlib anchor table for
`THM-M-0105`.

The table is metadata only.  Each row records checked support substrate in the
repo-local Lake closure and states why that substrate is not by itself a proof
of the algebraic-curve Riemann-Roch theorem.
-/
structure RiemannRochMathlibAnchorRow where
  package : String
  modules : String
  repoLocalProbe : String
  roleForRiemannRoch : String
  closureStatus : String
  deriving Repr, DecidableEq

/--
Integration-ready mathlib anchor table for the public THM-M-0105 backfill.

The rows cover the required scheme, morphism-property, sheaf/module,
site/cohomology, function-field, Dedekind different/trace-dual, and elliptic
curve surfaces.  All rows are support anchors; none is a terminal
Riemann-Roch theorem.
-/
def riemannRochMathlibAnchorTable : List RiemannRochMathlibAnchorRow := [
  {
    package := "scheme-object-model",
    modules := "Mathlib.AlgebraicGeometry.Scheme; Mathlib.AlgebraicGeometry.Spec; Mathlib.AlgebraicGeometry.Properties",
    repoLocalProbe := "Scheme; Scheme.Hom; Spec; IsIntegral",
    roleForRiemannRoch := "host the base and curve objects, morphisms, affine spectra, and the integral-scheme hypothesis in the normalized statement",
    closureStatus := "checked_support; not a curve-specific Riemann-Roch theorem"
  },
  {
    package := "morphism-properties",
    modules := "Mathlib.AlgebraicGeometry.Morphisms.Proper; Mathlib.AlgebraicGeometry.Morphisms.Smooth; Mathlib.AlgebraicGeometry.Morphisms.FiniteType; Mathlib.AlgebraicGeometry.Morphisms.Separated",
    repoLocalProbe := "IsProper; Smooth; LocallyOfFiniteType; properMorphism_locallyOfFiniteType",
    roleForRiemannRoch := "supports the smooth/proper curve boundary and checked finite-type consequences for future cohomology finiteness work",
    closureStatus := "checked_support; does not supply genus, divisor, or cohomology formula closure"
  },
  {
    package := "modules-and-sheaves",
    modules := "Mathlib.AlgebraicGeometry.Modules.Sheaf; Mathlib.Algebra.Category.ModuleCat.Sheaf.Abelian",
    repoLocalProbe := "Scheme.Modules; Scheme.Modules.Hom; Scheme.Modules.presheaf; Scheme.Modules.isSheaf",
    roleForRiemannRoch := "candidate object model for sheaves of modules, sections, and future line-bundle/divisor sheaf bridges",
    closureStatus := "checked_support; no local divisor-to-O(D) bridge is proved here"
  },
  {
    package := "sites-and-sheaf-cohomology",
    modules := "Mathlib.AlgebraicGeometry.Sites.Etale; Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
    repoLocalProbe := "Scheme.zariskiTopology; Scheme.etaleTopology; Scheme.smallEtaleTopology; CategoryTheory.Sheaf.H; CategoryTheory.Sheaf.cohomologyFunctor",
    roleForRiemannRoch := "provides site and abelian sheaf cohomology APIs relevant to a scheme/sheaf-cohomology proof route",
    closureStatus := "checked_support; no local comparison to curve line-bundle cohomology dimensions is proved"
  },
  {
    package := "function-fields",
    modules := "Mathlib.AlgebraicGeometry.FunctionField; Mathlib.NumberTheory.FunctionField",
    repoLocalProbe := "Scheme.functionField; Scheme.germToFunctionField_injective; FunctionFieldOfIntegralScheme; integralScheme_functionField_field",
    roleForRiemannRoch := "supports the generic-point/function-field surface for integral schemes and a possible function-field proof route",
    closureStatus := "checked_support; not a divisor theorem over one-variable function fields"
  },
  {
    package := "dedekind-different-trace-dual",
    modules := "Mathlib.RingTheory.DedekindDomain.Different; Mathlib.RingTheory.Trace.Basic; Mathlib.RingTheory.NormTrace",
    repoLocalProbe := "Submodule.traceDual; FractionalIdeal.dual; differentIdeal",
    roleForRiemannRoch := "records arithmetic trace-dual/different infrastructure for a possible Dedekind/function-field/adeles route",
    closureStatus := "checked_support; no global function-field Riemann-Roch proof or adele-degree formula is imported"
  },
  {
    package := "elliptic-curve-modules",
    modules := "Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point; Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point; Mathlib.AlgebraicGeometry.EllipticCurve.NormalForms",
    repoLocalProbe := "WeierstrassCurve.Projective.Point; WeierstrassCurve.Projective.Point.instAddCommGroup; WeierstrassCurve.IsShortNF",
    roleForRiemannRoch := "nearby genus-one curve infrastructure and group-law substrate; useful for special-case calibration",
    closureStatus := "checked_support; elliptic curve group law is not the general Riemann-Roch theorem"
  }
]

/-- The public THM-M-0105 mathlib anchor table currently has seven rows. -/
theorem riemannRochMathlibAnchorTable_length :
    riemannRochMathlibAnchorTable.length = 7 :=
  rfl

/-- The statement shape unfolds to the explicit curve-boundary-to-formula form. -/
theorem statementShape_iff_exists_formula
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) :
    StatementShape.{u, uD} S X pi <->
      (Nonempty (AlgebraicCurveBoundary S X pi) ->
        exists A : RiemannRochDivisorData.{uD}, RiemannRochFormula A) :=
  Iff.rfl

/-- A proof of the statement shape supplies a formula package for any audited curve boundary. -/
theorem formulaPackage_of_statementShape
    {S X : Scheme.{u}} {pi : Scheme.Hom X S}
    (h : StatementShape.{u, uD} S X pi)
    (hcurve : Nonempty (AlgebraicCurveBoundary S X pi)) :
    exists A : RiemannRochDivisorData.{uD}, RiemannRochFormula A :=
  h hcurve

/-- Checked wrapper: proper morphisms are locally of finite type in the imported mathlib API. -/
theorem properMorphism_locallyOfFiniteType
    {S X : Scheme.{u}} {pi : Scheme.Hom X S}
    (hpi : IsProper pi) : LocallyOfFiniteType pi := by
  letI : IsProper pi := hpi
  infer_instance

/-- Checked wrapper: integral schemes are irreducible in the imported mathlib API. -/
theorem integralScheme_irreducibleSpace
    {X : Scheme.{u}} (hX : IsIntegral X) : IrreducibleSpace X := by
  letI : IsIntegral X := hX
  infer_instance

/-- Checked wrapper: the function field of an integral scheme carries a field instance. -/
@[reducible]
def integralScheme_functionField_field
    {X : Scheme.{u}} (hX : IsIntegral X) : Field X.functionField := by
  letI : IsIntegral X := hX
  infer_instance

/-- Checked local abbreviation for the function field of an integral scheme. -/
abbrev FunctionFieldOfIntegralScheme
    (X : Scheme.{u}) [IsIntegral X] : CommRingCat :=
  X.functionField

/-- Checked wrapper around mathlib's Euler characteristic of a homological complex. -/
abbrev HomologicalComplexEulerChar
    (R : Type u) [Ring R] {ι : Type uι} {c : ComplexShape ι}
    [c.EulerCharSigns] (C : HomologicalComplex (ModuleCat R) c) : Int :=
  HomologicalComplex.eulerChar C

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
  A.exactTheoremFound ->
    A.importedIntoLakeClosure \/ A.concreteIntegrationBlockerRecorded

/-- If no exact external anchor is found, the integration-debt gate is vacuous. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit) (h : Not A.exactTheoremFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/-- mathlib and local modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Spec",
  "Mathlib.AlgebraicGeometry.Properties",
  "Mathlib.AlgebraicGeometry.FunctionField",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Morphisms.FiniteType",
  "Mathlib.AlgebraicGeometry.Morphisms.Separated",
  "Mathlib.AlgebraicGeometry.Modules.Sheaf",
  "Mathlib.AlgebraicGeometry.Sites.Etale",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
  "Mathlib.RingTheory.DedekindDomain.Different",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Scheme",
  "Mathlib.AlgebraicGeometry.EllipticCurve.NormalForms",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point",
  "Mathlib.Algebra.Homology.EulerCharacteristic",
  "Mathlib.Analysis.Complex.ValueDistribution.LogCounting.Basic"
]

/-- Search terms that did not locate a terminal algebraic-curve Riemann-Roch theorem. -/
def absentTerminalSearchTerms : List String := [
  "RiemannRoch",
  "Riemann-Roch",
  "riemann_roch",
  "Roch",
  "CurveDivisor",
  "CartierDivisor curve",
  "WeilDivisor curve",
  "canonical divisor",
  "line bundle divisor",
  "sheaf cohomology dimension",
  "genus algebraic curve",
  "proper smooth curve Riemann-Roch",
  "Riemann Roch algebraic curves Lean 4"
]

/-- Current machine-proof debt classification for this repaired Stage1 module. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: full algebraic-curve Riemann-Roch proof is not repo-local closed",
  "not_repo_local_closed: this file is a statement-shape wrapper plus checked substrate anchors",
  "repo_local_integration_debt_gate: no completion claim may retain anchor-only external evidence"
]

/-! ## First-milestone proof-route decision -/

/-- Public-route alternatives considered for the first Lean 4 milestone. -/
inductive RiemannRochProofRoute where
  | schemeSheafCohomology
  | dedekindFunctionFieldAdeles
  deriving Repr, DecidableEq

/--
Integration-ready route decision for the public THM-M-0105 backfill.

The selected first milestone follows the function-field/Dedekind/adeles route
because the only specific external Lean 4 candidate found for algebraic-curve
Riemann-Roch is organized around adelic Euler characteristic and function-field
data.  The scheme/sheaf-cohomology route remains an important final comparison
target, but the local mathlib snapshot currently provides support substrate
rather than a terminal theorem that can be wrapped immediately.
-/
structure RiemannRochRouteDecision where
  selectedFirstMilestone : RiemannRochProofRoute
  deferredComparisonRoute : RiemannRochProofRoute
  reason : String
  integrationGate : String
  completionStatus : String
  deriving Repr

/-- Route decision for the first Lean 4 milestone of THM-M-0105. -/
def firstMilestoneRouteDecision : RiemannRochRouteDecision where
  selectedFirstMilestone := RiemannRochProofRoute.dedekindFunctionFieldAdeles
  deferredComparisonRoute := RiemannRochProofRoute.schemeSheafCohomology
  reason := "choose Dedekind/function-field/adeles first: it matches the audited cguth7/roch-riemann-refactor theorem family and the local mathlib FunctionField/Dedekind support anchors; scheme/sheaf cohomology remains support and comparison infrastructure"
  integrationGate := "before any completion claim, pin/import/check the exact external theorem or record a concrete blocker after lake build and targeted #print axioms"
  completionStatus := "formalization_debt; no repo-local Riemann-Roch proof body or checked upstream wrapper is present"

/-- The first Lean 4 milestone route is Dedekind/function-field/adeles. -/
theorem firstMilestoneRoute_selected :
    firstMilestoneRouteDecision.selectedFirstMilestone =
      RiemannRochProofRoute.dedekindFunctionFieldAdeles :=
  rfl

/-- Scheme/sheaf cohomology remains a comparison route, not the first milestone. -/
theorem firstMilestoneRoute_deferred :
    firstMilestoneRouteDecision.deferredComparisonRoute =
      RiemannRochProofRoute.schemeSheafCohomology :=
  rfl

/-- The route decision retains a non-completion status. -/
theorem firstMilestoneRoute_completionStatus :
    firstMilestoneRouteDecision.completionStatus =
      "formalization_debt; no repo-local Riemann-Roch proof body or checked upstream wrapper is present" :=
  rfl

/-! ## External audit result for `cguth7/roch-riemann-refactor` -/

/--
Audit row for the external `cguth7/roch-riemann-refactor` candidate.

This is metadata for the C004 child task.  It records that an upstream Lean 4
candidate exists, but the current repository has not pinned or imported it, and
the audit found concrete build/axiom-check blockers rather than a completed
repo-local proof closure.
-/
structure ExternalRiemannRochAuditResult where
  repository : String
  commit : String
  toolchain : String
  externalMathlibRev : String
  localBuildCommand : String
  localBuildResult : String
  targetedAxiomCommand : String
  targetedAxiomResult : String
  sourceRiskSummary : String
  repoLocalGate : String
  deriving Repr, DecidableEq

/--
C004 audit result for `cguth7/roch-riemann-refactor` at commit
`8e67e8941a083617a8b34a0da3a35a7c2c845f59`.

The result is deliberately a blocker record, not an external completion claim.
-/
def cguth7RochRiemannAudit : ExternalRiemannRochAuditResult where
  repository := "https://github.com/cguth7/roch-riemann-refactor"
  commit := "8e67e8941a083617a8b34a0da3a35a7c2c845f59"
  toolchain := "leanprover/lean4:v4.27.0-rc1"
  externalMathlibRev := "leanprover-community/mathlib4@fe3134f0c3508d2fd6394307be226ffa9b8cb4ba"
  localBuildCommand := "cd /tmp/roch-riemann-refactor-s1m027-c004 && lake build"
  localBuildResult := "failed: proofwidgets/widgetJsAll required a GitHub release/cache fetch; lake exe cache get also failed to fetch leantar from GitHub in this environment"
  targetedAxiomCommand := "#print axioms for chi_additive, euler_characteristic, riemann_roch_from_euler, riemann_roch_from_adelic, riemann_roch_full, serre_duality_finrank, and P1 riemann_roch variants"
  targetedAxiomResult := "not locally checkable in this audit because the external Lake closure did not build; source inspection shows riemann_roch_full restates FullRRData.serre_duality_eq and the adelic route depends on AdelicRRData/PairingVanishesOnK hypotheses"
  sourceRiskSummary := "source scan found six explicit elliptic-instance axiom declarations and thirteen placeholder-proof code occurrences outside the claimed general theorem path; no repo-local wrapper may treat this as completed without a successful build and targeted axiom print"
  repoLocalGate := "external_upstream_anchor_only_with_concrete_blocker; keep THM-M-0105 under formalization_debt until pin/import/check succeeds"

/-- The external audit is tied to the requested commit. -/
theorem cguth7RochRiemannAudit_commit :
    cguth7RochRiemannAudit.commit =
      "8e67e8941a083617a8b34a0da3a35a7c2c845f59" :=
  rfl

/-- The external audit does not upgrade THM-M-0105 to repo-local closure. -/
theorem cguth7RochRiemannAudit_repoLocalGate :
    cguth7RochRiemannAudit.repoLocalGate =
      "external_upstream_anchor_only_with_concrete_blocker; keep THM-M-0105 under formalization_debt until pin/import/check succeeds" :=
  rfl

/-! ## C005 pin/vendor integration decision -/

/--
Decision record for the C005 child task: whether an external Riemann-Roch proof
can safely be pinned or vendored into this repository.

This is intentionally a non-completion record.  It exists so the repo-local
Lean artifact carries the same integration-debt gate as the child ledger.
-/
structure ExternalRiemannRochIntegrationDecision where
  childTask : String
  selectedExternalTheorem : String
  pinnedLakeDependencyAction : String
  vendoredProofBodyAction : String
  integrationBlocker : String
  repoLocalGateResult : String
  debtClassification : String
  nextIntegratorAction : String
  deriving Repr, DecidableEq

/--
C005 decision for THM-M-0105.

Because the audited `cguth7/roch-riemann-refactor` candidate did not enter a
successful local Lake closure and targeted axiom printing was not available,
this child must not add a pinned dependency, vendored body, or theorem wrapper.
-/
def c005RochRiemannIntegrationDecision :
    ExternalRiemannRochIntegrationDecision where
  childTask := "S1-M-027-C005"
  selectedExternalTheorem := "none: no exact external theorem is selected for a repo-local wrapper in this child"
  pinnedLakeDependencyAction := "not_added: cguth7/roch-riemann-refactor did not pass local lake build at commit 8e67e8941a083617a8b34a0da3a35a7c2c845f59"
  vendoredProofBodyAction := "not_vendored: source inspection plus failed external build is insufficient for a repo-local proof body"
  integrationBlocker := "external build blocked by proofwidgets/leantar GitHub release/cache fetches; targeted #print axioms could not be run"
  repoLocalGateResult := "pass_noncompletion: no completed state is claimed and anchor-only external evidence remains blocked"
  debtClassification := "formalization_debt; not_repo_local_closed; external_upstream_anchor_only_with_concrete_blocker"
  nextIntegratorAction := "retry external lake build in an environment with required release/cache access, run targeted #print axioms, then pin/import/check or keep a concrete blocker"

/-- C005 deliberately did not add a pinned Lake dependency. -/
theorem c005RochRiemannIntegrationDecision_noPinnedDependency :
    c005RochRiemannIntegrationDecision.pinnedLakeDependencyAction =
      "not_added: cguth7/roch-riemann-refactor did not pass local lake build at commit 8e67e8941a083617a8b34a0da3a35a7c2c845f59" :=
  rfl

/-- C005 deliberately did not vendor an unchecked proof body. -/
theorem c005RochRiemannIntegrationDecision_noVendoredProofBody :
    c005RochRiemannIntegrationDecision.vendoredProofBodyAction =
      "not_vendored: source inspection plus failed external build is insufficient for a repo-local proof body" :=
  rfl

/-- C005 leaves the theorem in non-completed formalization debt. -/
theorem c005RochRiemannIntegrationDecision_debtClassification :
    c005RochRiemannIntegrationDecision.debtClassification =
      "formalization_debt; not_repo_local_closed; external_upstream_anchor_only_with_concrete_blocker" :=
  rfl

/-! ## C006 external blocked-anchor record -/

/--
Blocked-anchor record for the C006 child task.

This is the negative branch after the external audit and pin/vendor decision:
the `cguth7/roch-riemann-refactor` anchor is documented with concrete blockers,
and THM-M-0105 remains under formalization debt.  This is not a proof theorem
for Riemann-Roch.
-/
structure ExternalRiemannRochBlockedAnchor where
  childTask : String
  externalAnchor : String
  requestedAction : String
  viabilityDiagnosis : String
  concreteBlocker : String
  publicDebtAction : String
  repoLocalGateResult : String
  completionStatus : String
  deriving Repr, DecidableEq

/--
C006 blocked-anchor decision for THM-M-0105.

The audited external project is a useful anchor for future work, but it is not
viable as a completed repo-local proof in this pass because the external Lake
closure did not build here and targeted axiom checks could not be run.
-/
def c006RochRiemannBlockedAnchor :
    ExternalRiemannRochBlockedAnchor where
  childTask := "S1-M-027-C006"
  externalAnchor := "cguth7/roch-riemann-refactor@8e67e8941a083617a8b34a0da3a35a7c2c845f59"
  requestedAction := "if not viable, record as an external blocked anchor and keep THM-M-0105 under formalization_debt"
  viabilityDiagnosis := "not_viable_for_completion_in_this_repo_pass"
  concreteBlocker := "external lake build did not pass in C004 because proofwidgets/leantar release-cache artifacts were unavailable; targeted #print axioms for the exact Riemann-Roch theorem family could not be checked; C005 therefore did not pin, vendor, or wrap the external theorem"
  publicDebtAction := "keep THM-M-0105 under formalization_debt until an exact theorem is pinned/imported/checked or a local proof body is supplied"
  repoLocalGateResult := "pass_noncompletion: external anchor is blocked, not completed, so no completed state retains repo_local_integration_debt"
  completionStatus := "not_repo_local_closed"

/-- C006 records the external anchor as blocked, not as completed closure. -/
theorem c006RochRiemannBlockedAnchor_viability :
    c006RochRiemannBlockedAnchor.viabilityDiagnosis =
      "not_viable_for_completion_in_this_repo_pass" :=
  rfl

/-- C006 keeps THM-M-0105 under formalization debt. -/
theorem c006RochRiemannBlockedAnchor_publicDebtAction :
    c006RochRiemannBlockedAnchor.publicDebtAction =
      "keep THM-M-0105 under formalization_debt until an exact theorem is pinned/imported/checked or a local proof body is supplied" :=
  rfl

/-- C006 does not leave repo-local integration debt inside a completed state. -/
theorem c006RochRiemannBlockedAnchor_repoLocalGate :
    c006RochRiemannBlockedAnchor.repoLocalGateResult =
      "pass_noncompletion: external anchor is blocked, not completed, so no completed state retains repo_local_integration_debt" :=
  rfl

/-- Theorem-internal child leaves for the next M0387-level module split. -/
def theoremInternalChildLeaves : List String := [
  "S1-M-027-leaf-001 statement normalization and notation freeze",
  "S1-M-027-leaf-002 concrete curve object model: smooth proper geometrically connected dimension-one schemes",
  "S1-M-027-leaf-003 divisor API selection: Cartier/Weil divisors and linear equivalence",
  "S1-M-027-leaf-004 sheaf bridge: divisor line bundles and global sections",
  "S1-M-027-leaf-005 cohomology dimensions, Euler characteristic, genus, and canonical divisor",
  "S1-M-027-leaf-006 special base and ring cases with checked local wrappers",
  "S1-M-027-leaf-007 mathlib and external Lean 4 terminal theorem audit",
  "S1-M-027-leaf-008 pin/import/check or integration-blocker handling for any external closure",
  "S1-M-027-leaf-009 replacement of StatementShape by local proof body or checked upstream wrapper"
]

/-! ## C007 public leaf-ledger backfill gate -/

/-- One row of the integration-ready `<=100` leaf-budget ledger. -/
structure RiemannRochLeafBudgetRow where
  leafId : String
  package : String
  obligation : String
  budget : Nat
  status : String
  deriving Repr, DecidableEq

/--
C007 integration-ready `<=100` leaf-budget ledger.

Every row is still `unchecked`.  The list is intended for serial public
backfill after integrator review, not as proof completion evidence.
-/
def c007RiemannRochLeafBudgetLedger : List RiemannRochLeafBudgetRow := [
  { leafId := "L001", package := "P0", obligation := "Choose divisor vs line-bundle canonical statement and document equivalence target.", budget := 40, status := "unchecked" },
  { leafId := "L002", package := "P0", obligation := "Define private StatementShape with explicit universes and assumptions.", budget := 35, status := "unchecked" },
  { leafId := "L003", package := "P1", obligation := "Anchor Curve object to mathlib Scheme plus smooth/proper/integral assumptions, or to function-field route.", budget := 80, status := "unchecked" },
  { leafId := "L004", package := "P1", obligation := "Define divisor object or choose upstream DivisorV2/line-bundle surrogate.", budget := 80, status := "unchecked" },
  { leafId := "L005", package := "P1", obligation := "Define ell(D) as finite-dimensional k-rank/finrank.", budget := 70, status := "unchecked" },
  { leafId := "L006", package := "P1", obligation := "Define canonical divisor/class object.", budget := 90, status := "unchecked" },
  { leafId := "L007", package := "P2", obligation := "Local place/codimension-one point API selected and imported.", budget := 80, status := "unchecked" },
  { leafId := "L008", package := "P2", obligation := "Valuation/local ring bridge for divisor coefficients.", budget := 95, status := "unchecked" },
  { leafId := "L009", package := "P2", obligation := "Effective divisor predicate and monotonicity of L(D).", budget := 80, status := "unchecked" },
  { leafId := "L010", package := "P2", obligation := "Degree additivity for divisors.", budget := 70, status := "unchecked" },
  { leafId := "L011", package := "P2", obligation := "Principal divisor degree zero.", budget := 95, status := "unchecked" },
  { leafId := "L012", package := "P3", obligation := "Identify H0(O(D)) with L(D) or choose adelic replacement.", budget := 95, status := "unchecked" },
  { leafId := "L013", package := "P3", obligation := "Define H1(D) / adelic quotient with finite dimensionality.", budget := 100, status := "unchecked" },
  { leafId := "L014", package := "P3", obligation := "Define Euler characteristic with integer-valued dimension difference.", budget := 45, status := "unchecked" },
  { leafId := "L015", package := "P4", obligation := "Construct evaluation/residue map for D -> D + v.", budget := 100, status := "unchecked" },
  { leafId := "L016", package := "P4", obligation := "Prove kernel/image exactness at L(D+v).", budget := 100, status := "unchecked" },
  { leafId := "L017", package := "P4", obligation := "Prove connecting map to H1(D) and exactness.", budget := 100, status := "unchecked" },
  { leafId := "L018", package := "P4", obligation := "Prove chi(D+v)=chi(D)+deg(v) for one place.", budget := 95, status := "unchecked" },
  { leafId := "L019", package := "P4", obligation := "Extend additivity from one place to arbitrary finite divisor.", budget := 85, status := "unchecked" },
  { leafId := "L020", package := "P4", obligation := "Establish base chi(0)=1-g.", budget := 80, status := "unchecked" },
  { leafId := "L021", package := "P5", obligation := "State/prove Serre duality h1(D)=ell(K-D).", budget := 100, status := "unchecked" },
  { leafId := "L022", package := "P5", obligation := "Prove/anchor deg(K)=2g-2.", budget := 95, status := "unchecked" },
  { leafId := "L023", package := "P5", obligation := "Prove finite-dimensionality for ell(K-D).", budget := 70, status := "unchecked" },
  { leafId := "L024", package := "P6", obligation := "Combine Euler characteristic with Serre duality.", budget := 35, status := "unchecked" },
  { leafId := "L025", package := "P6", obligation := "Normalize Nat/Int coercions and subtraction side conditions.", budget := 50, status := "unchecked" },
  { leafId := "L026", package := "P6", obligation := "Create repo-local wrapper theorem only after upstream/local closure exists.", budget := 50, status := "unchecked" },
  { leafId := "L027", package := "P7", obligation := "Pin/import external dependency if selected.", budget := 100, status := "unchecked" },
  { leafId := "L028", package := "P7", obligation := "Run lake build for dependency and wrapper.", budget := 100, status := "unchecked" },
  { leafId := "L029", package := "P7", obligation := "Run #print axioms on target theorem(s).", budget := 50, status := "unchecked" },
  { leafId := "L030", package := "P7", obligation := "Record no residual repo_local_integration_debt before any completed state.", budget := 30, status := "unchecked" }
]

/-- C007 records all thirty parent leaf-budget rows. -/
theorem c007RiemannRochLeafBudgetLedger_length :
    c007RiemannRochLeafBudgetLedger.length = 30 :=
  rfl

/-- Gate record for serial public backfill of the C007 leaf ledger. -/
structure PublicLeafLedgerBackfillGate where
  childTask : String
  targetSurface : String
  action : String
  integratorReviewRequired : Bool
  repoLocalGateResult : String
  completionStatus : String
  deriving Repr, DecidableEq

/--
C007 public backfill gate.

This metadata says that the authoritative public proof/process surface should
be edited only by a serial integrator after review.  This worker records the
patch plan and keeps THM-M-0105 non-completed.
-/
def c007PublicLeafLedgerBackfillGate : PublicLeafLedgerBackfillGate where
  childTask := "S1-M-027-C007"
  targetSurface := "Docs/Stage1_Blueprint.md THM-M-0105 public proof/process section, or the serial integrator-designated authoritative public surface"
  action := "backfill the unchecked <=100 leaf-budget ledger from c007RiemannRochLeafBudgetLedger after integrator review"
  integratorReviewRequired := true
  repoLocalGateResult := "pass_noncompletion: no public docs edited by this worker and no completed state retains repo_local_integration_debt"
  completionStatus := "public_backfill_ready; not_repo_local_closed; formalization_debt"

/-- C007 requires serial integrator review before public backfill. -/
theorem c007PublicLeafLedgerBackfillGate_reviewRequired :
    c007PublicLeafLedgerBackfillGate.integratorReviewRequired = true :=
  rfl

/-- C007 does not mark THM-M-0105 as repo-local closed. -/
theorem c007PublicLeafLedgerBackfillGate_completionStatus :
    c007PublicLeafLedgerBackfillGate.completionStatus =
      "public_backfill_ready; not_repo_local_closed; formalization_debt" :=
  rfl

/-! ## Audit probes -/

#check Scheme
#check Scheme.Hom
#check IsIntegral
#check Smooth
#check IsProper
#check LocallyOfFiniteType
#check Scheme.functionField
#check HomologicalComplex.eulerChar
#check StatementShape
#check THM_M_0105_StatementShapeTarget
#check statementNormalization
#check CurvePackage
#check DivisorPackage
#check CohomologyPackage
#check CurveDivisorCohomologyPackage
#check PackageSplitClosure
#check statementShape_of_packageSplitClosure
#check packageSplitLeaves
#check RiemannRochMathlibAnchorRow
#check riemannRochMathlibAnchorTable
#check riemannRochMathlibAnchorTable_length
#check formulaPackage_of_statementShape
#check properMorphism_locallyOfFiniteType
#check integralScheme_irreducibleSpace
#check Scheme.Modules
#check Scheme.Modules.Hom
#check Scheme.zariskiTopology
#check Scheme.etaleTopology
#check Scheme.smallEtaleTopology
#check CategoryTheory.Sheaf.H
#check CategoryTheory.Sheaf.cohomologyFunctor
#check Submodule.traceDual
#check FractionalIdeal.dual
#check differentIdeal
#check WeierstrassCurve.Projective.Point
#check WeierstrassCurve.Projective.Point.instAddCommGroup
#check WeierstrassCurve.IsShortNF
#check RepoLocalIntegrationDebtGate
#check RiemannRochProofRoute
#check RiemannRochRouteDecision
#check firstMilestoneRouteDecision
#check firstMilestoneRoute_selected
#check firstMilestoneRoute_deferred
#check firstMilestoneRoute_completionStatus
#check ExternalRiemannRochAuditResult
#check cguth7RochRiemannAudit
#check cguth7RochRiemannAudit_commit
#check cguth7RochRiemannAudit_repoLocalGate
#check ExternalRiemannRochIntegrationDecision
#check c005RochRiemannIntegrationDecision
#check c005RochRiemannIntegrationDecision_noPinnedDependency
#check c005RochRiemannIntegrationDecision_noVendoredProofBody
#check c005RochRiemannIntegrationDecision_debtClassification
#check ExternalRiemannRochBlockedAnchor
#check c006RochRiemannBlockedAnchor
#check c006RochRiemannBlockedAnchor_viability
#check c006RochRiemannBlockedAnchor_publicDebtAction
#check c006RochRiemannBlockedAnchor_repoLocalGate
#check RiemannRochLeafBudgetRow
#check c007RiemannRochLeafBudgetLedger
#check c007RiemannRochLeafBudgetLedger_length
#check PublicLeafLedgerBackfillGate
#check c007PublicLeafLedgerBackfillGate
#check c007PublicLeafLedgerBackfillGate_reviewRequired
#check c007PublicLeafLedgerBackfillGate_completionStatus

end S1_M_027
end Stage1
end AwesomeTheorems
