import Mathlib.Algebra.Homology.EulerCharacteristic
import Mathlib.AlgebraicGeometry.FunctionField
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
# S1-M-124 / THM-M-0175: Riemann-Roch theorem for algebraic curves

This Stage1 artifact records a conservative Lean statement-shape boundary for
the classical Riemann-Roch formula on algebraic curves:

`ell(D) - ell(K - D) = deg(D) + 1 - g`.

The pinned mathlib snapshot provides schemes, proper and smooth morphism
properties, sheaf/module substrate, function fields of integral schemes, and
homological Euler characteristic.  It does not provide a terminal API for
Cartier/Weil divisors on curves, line bundles associated to divisors, sheaf
cohomology dimensions on proper smooth curves, genus, canonical divisors, or
the Riemann-Roch theorem for algebraic curves.

The declarations below therefore expose the formula boundary and low-risk
mathlib wrappers only, without proof-placeholder declarations.
-/

noncomputable section

open AlgebraicGeometry

universe u uD uι

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_124

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
line bundles and sheaf cohomology on algebraic curves.
-/
structure RiemannRochDivisorData : Type (uD + 1) where
  CurveDivisor : Type uD
  sub : CurveDivisor -> CurveDivisor -> CurveDivisor
  degree : CurveDivisor -> Int
  linearSeriesDimension : CurveDivisor -> Int
  genus : Int
  canonicalDivisor : CurveDivisor

/--
Divisor object-model choices considered for the curve-level Riemann-Roch
statement.

The selected Stage1 path is `abstractCartierLineBundleBridge`: keep the current
repo-local divisor package abstract, but require its eventual concrete backend
to be Cartier-facing so that `O(D)`, global sections, and the cohomology model
can be attached directly.  Weil/valuation data remains a bridge target for
smooth regular curves, not the selected local object model.
-/
inductive CurveDivisorObjectModel where
  | cartierDivisors
  | weilDivisors
  | abstractCartierLineBundleBridge
  | pinnedExternalProjectiveCurveDivisors
  deriving DecidableEq, Repr

/-- Repo-local record of the S1-M-124 divisor object-model decision. -/
structure DivisorObjectModelDecision where
  selectedModel : CurveDivisorObjectModel
  selectedModelName : String
  rejectedDirectModels : List String
  rationale : List String
  requiredBridgeApis : List String
  repoLocalCompletionStatus : String

/--
Divisor model decision for THM-M-0175.

The pinned mathlib snapshot does not expose a terminal algebraic-curve
Cartier/Weil divisor API.  Since the Riemann-Roch formula must compare
`H^0(X, O(D))` and `H^0(X, O(K-D))`, the safest local object model is an
abstract Cartier-facing package: it preserves the line-bundle/cohomology shape
without pretending that a concrete divisor API or Weil-Cartier equivalence is
already available in this Lake closure.
-/
def selectedDivisorObjectModelDecision : DivisorObjectModelDecision where
  selectedModel := CurveDivisorObjectModel.abstractCartierLineBundleBridge
  selectedModelName := "abstract_cartier_line_bundle_bridge"
  rejectedDirectModels := [
    "direct_cartier_divisors: no concrete algebraic-curve Cartier divisor API was located in the pinned mathlib snapshot",
    "direct_weil_divisors: no concrete algebraic-curve Weil divisor API was located in the pinned mathlib snapshot",
    "pinned_external_projective_curve_divisors: no terminal external projective-curve divisor dependency is repo-local pinned/imported/checked"
  ]
  rationale := [
    "Riemann-Roch needs the divisor-to-line-bundle map D ↦ O(D) before ell(D) can be modeled as a finite-dimensional global-section dimension",
    "Cartier-facing semantics align with line bundles and sheaf cohomology; Weil/valuation divisors can later feed this model through a smooth-regular-curve equivalence",
    "The current abstract RiemannRochDivisorData remains a statement-shape boundary and does not claim a concrete divisor implementation"
  ]
  requiredBridgeApis := [
    "curve regularity bridge from smooth dimension-one schemes to the Cartier-Weil equivalence",
    "Cartier divisor group, subtraction, canonical divisor, and degree on proper smooth curves",
    "divisor-to-line-bundle construction O(D) with compatibility for K-D",
    "finite-dimensional H^0 model over the base field for ell(D) and ell(K-D)",
    "replacement theorem connecting RiemannRochDivisorData to the chosen concrete divisor API"
  ]
  repoLocalCompletionStatus := "not_repo_local_closed"

/-- The selected local divisor model is the abstract Cartier-facing bridge. -/
theorem selectedDivisorObjectModelDecision_model :
    selectedDivisorObjectModelDecision.selectedModel =
      CurveDivisorObjectModel.abstractCartierLineBundleBridge :=
  rfl

/-- The divisor model decision does not close the terminal Riemann-Roch theorem. -/
theorem selectedDivisorObjectModelDecision_not_closed :
    selectedDivisorObjectModelDecision.repoLocalCompletionStatus =
      "not_repo_local_closed" :=
  rfl

/--
Abstract finite-dimensional `H^0` model for `ell(D)`.

This is still a bridge record rather than a concrete sheaf-cohomology API: a
future proof must replace `H0` by global sections of the line bundle `O(D)`.
The checked content here is the finite-dimensional vector-space shape used to
interpret the integer-valued `linearSeriesDimension` field.
-/
structure RiemannRochFiniteH0Model
    (k : Type u) [Field k] (A : RiemannRochDivisorData.{uD}) :
    Type (max u uD + 1) where
  H0 : A.CurveDivisor -> Type (max u uD)
  addCommGroup : forall D, AddCommGroup (H0 D)
  module : forall D, Module k (H0 D)
  finiteDimensional :
    forall D, @FiniteDimensional k (H0 D) _ (addCommGroup D) (module D)
  ell_eq_finrank :
    forall D, A.linearSeriesDimension D =
      Int.ofNat (@Module.finrank k (H0 D) _ _ (module D))

/--
Cohomology model choices considered for `ell(D)` and `ell(K-D)`.

The selected Stage1 path is `abstractFiniteDimensionalH0Bridge`: model both
terms as finite-dimensional global-section spaces of the Cartier-facing line
bundles `O(D)` and `O(K-D)`, while recording that the concrete sheaf
cohomology and Serre-duality APIs are not yet repo-local closed.
-/
inductive CurveCohomologyObjectModel where
  | abstractFiniteDimensionalH0Bridge
  | concreteSheafCohomologyDimensions
  | eulerCharacteristicWithSerreDuality
  | pinnedExternalProjectiveCurveCohomology
  deriving DecidableEq, Repr

/-- Repo-local record of the S1-M-124 cohomology model decision. -/
structure CohomologyObjectModelDecision where
  selectedModel : CurveCohomologyObjectModel
  selectedModelName : String
  ellDInterpretation : String
  ellKMinusDInterpretation : String
  finiteDimensionalityRequirement : String
  rejectedDirectModels : List String
  rationale : List String
  requiredBridgeApis : List String
  repoLocalCompletionStatus : String

/--
Cohomology model decision for THM-M-0175.

The pinned mathlib snapshot exposes homological Euler-characteristic substrate,
but not a terminal algebraic-curve sheaf-cohomology dimension API specialized
to divisor line bundles.  The safest local model is therefore a finite `H^0`
bridge: `ell(D)` and `ell(K-D)` are dimensions of finite-dimensional global
section spaces, and the Euler-characteristic/Serre-duality route remains a
future proof bridge rather than a completed local theorem.
-/
def selectedCohomologyObjectModelDecision : CohomologyObjectModelDecision where
  selectedModel := CurveCohomologyObjectModel.abstractFiniteDimensionalH0Bridge
  selectedModelName := "abstract_finite_dimensional_H0_bridge"
  ellDInterpretation := "finrank over the base field of H^0(X, O(D))"
  ellKMinusDInterpretation := "finrank over the base field of H^0(X, O(K-D))"
  finiteDimensionalityRequirement :=
    "H^0(X, O(D)) and H^0(X, O(K-D)) must be finite-dimensional vector spaces before ell is identified with finrank"
  rejectedDirectModels := [
    "direct_concrete_sheaf_cohomology_dimensions: no terminal curve-divisor line-bundle cohomology API is available in the pinned mathlib snapshot",
    "euler_characteristic_with_serre_duality_as_selected_model: useful proof route, but it still needs concrete H^0/H^1 finiteness and duality APIs before it can define ell",
    "pinned_external_projective_curve_cohomology: no external terminal cohomology package is pinned/imported/checked in this Lake closure"
  ]
  rationale := [
    "The formula uses ell(D) and ell(K-D), so the model must expose finite-dimensional H^0 spaces for both O(D) and O(K-D)",
    "A finite H^0 bridge is compatible with the selected abstract Cartier line-bundle divisor model",
    "Euler characteristic can later connect H^0 and H^1, but choosing it as the immediate ell model would hide the required finite-dimensional global-section interface"
  ]
  requiredBridgeApis := [
    "divisor-to-line-bundle construction D -> O(D) and residual construction K-D",
    "global section functor H^0 for line bundles on proper smooth curves",
    "finite-dimensionality of H^0(X, O(D)) and H^0(X, O(K-D)) over the base field",
    "identification of ell(D) and ell(K-D) with the corresponding finranks",
    "H^1/cohomological Euler characteristic and Serre-duality bridge for the eventual proof of the formula"
  ]
  repoLocalCompletionStatus := "not_repo_local_closed"

/-- The selected local cohomology model is the abstract finite-dimensional `H^0` bridge. -/
theorem selectedCohomologyObjectModelDecision_model :
    selectedCohomologyObjectModelDecision.selectedModel =
      CurveCohomologyObjectModel.abstractFiniteDimensionalH0Bridge :=
  rfl

/-- The cohomology model decision does not close the terminal Riemann-Roch theorem. -/
theorem selectedCohomologyObjectModelDecision_not_closed :
    selectedCohomologyObjectModelDecision.repoLocalCompletionStatus =
      "not_repo_local_closed" :=
  rfl

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
Stage1 statement-shape candidate for THM-M-0175.

Given a proper smooth integral dimension-one curve boundary over a base scheme,
there should be a concrete divisor package satisfying the Riemann-Roch formula.
The current local artifact does not prove that existence.
-/
def StatementShape
    (S X : Scheme.{u}) (pi : Scheme.Hom X S) : Prop :=
  Nonempty (AlgebraicCurveBoundary S X pi) ->
    exists A : RiemannRochDivisorData.{uD}, RiemannRochFormula A

/-- The statement shape unfolds to the intended curve-boundary to formula-package form. -/
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

/-- A proper scheme morphism is locally of finite type in mathlib's current API. -/
theorem properMorphism_locallyOfFiniteType
    {S X : Scheme.{u}} {pi : Scheme.Hom X S}
    (hpi : IsProper pi) : LocallyOfFiniteType pi := by
  letI : IsProper pi := hpi
  infer_instance

/-- An integral scheme is irreducible in mathlib's scheme hierarchy. -/
theorem integralScheme_irreducibleSpace
    {X : Scheme.{u}} (hX : IsIntegral X) : IrreducibleSpace X := by
  letI : IsIntegral X := hX
  infer_instance

/-- The function field of an integral scheme is a field in mathlib. -/
@[reducible]
def integralScheme_functionField_field
    {X : Scheme.{u}} (hX : IsIntegral X) : Field X.functionField := by
  letI : IsIntegral X := hX
  infer_instance

/-- The function field of an integral scheme as a checked local abbreviation. -/
abbrev FunctionFieldOfIntegralScheme
    (X : Scheme.{u}) [IsIntegral X] : CommRingCat :=
  X.functionField

/-- A checked wrapper around mathlib's Euler characteristic of a homological complex. -/
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

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.FunctionField",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Morphisms.FiniteType",
  "Mathlib.AlgebraicGeometry.Morphisms.Separated",
  "Mathlib.AlgebraicGeometry.Modules.Sheaf",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Scheme",
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

/-- Repo-local record for the pinned mathlib anchor audit. -/
structure MathlibAnchorAuditNote where
  pinnedRevision : String
  checkedSubstrateModules : List String
  absentTerminalTheoremSearchTerms : List String
  terminalAlgebraicCurveRiemannRochFound : Bool
  repoLocalCompletionStatus : String

/--
Pinned mathlib audit note for THM-M-0175.

This records the checked substrate available at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and the negative terminal-theorem
search result inside the local Lake closure.  The `false` terminal-theorem
field is part of the non-completion boundary for this Stage1 artifact.
-/
def pinnedMathlibAnchorAuditNote : MathlibAnchorAuditNote where
  pinnedRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  checkedSubstrateModules := mathlibAnchorModules
  absentTerminalTheoremSearchTerms := absentTerminalSearchTerms
  terminalAlgebraicCurveRiemannRochFound := false
  repoLocalCompletionStatus := "not_repo_local_closed"

/-- The pinned mathlib audit note is tied to the Lake-pinned mathlib revision. -/
theorem pinnedMathlibAnchorAuditNote_revision :
    pinnedMathlibAnchorAuditNote.pinnedRevision =
      "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- The pinned mathlib audit note does not claim a terminal curve Riemann-Roch theorem. -/
theorem pinnedMathlibAnchorAuditNote_terminal_not_found :
    pinnedMathlibAnchorAuditNote.terminalAlgebraicCurveRiemannRochFound = false :=
  rfl

/-- Repo-local record for an external GitHub/Reservoir audit candidate. -/
structure ExternalLeanAuditCandidate where
  repositoryUrl : String
  observedBranch : String
  observedToolchain : String
  observedMathlibRevision : String
  reservoirPackageObserved : Bool
  candidateDeclarations : List String
  terminalProofFound : Bool
  completionAssessment : String
  integrationBlocker : String

/--
External audit note for `cguth7/roch-riemann-refactor`.

The repository is relevant primary-source evidence for a Lean 4 Riemann-Roch
attempt, but it is not a repo-local completion anchor for THM-M-0175.  Its own
README and final report describe the general theorem as conditional on
project-specific hypotheses and blocked by affine-only place infrastructure.
-/
def cguthRochRiemannRefactorAudit : ExternalLeanAuditCandidate where
  repositoryUrl := "https://github.com/cguth7/roch-riemann-refactor"
  observedBranch := "main"
  observedToolchain := "leanprover/lean4:v4.27.0-rc1"
  observedMathlibRevision := "fe3134f0c3508d2fd6394307be226ffa9b8cb4ba"
  reservoirPackageObserved := false
  candidateDeclarations := [
    "RiemannRochV2.riemann_roch_from_euler",
    "RiemannRochV2.riemann_roch_full",
    "RiemannRochV2.euler_characteristic",
    "RiemannRochV2.PairingNondegenerate.serre_duality_finrank"
  ]
  terminalProofFound := false
  completionAssessment :=
    "external_conditional_attempt_not_terminal_for_algebraic_curve_RR"
  integrationBlocker :=
    "Lean 4.27/mathlib-fe3134f0c project; reported conditional/typeclass hypotheses, affine-only place obstruction, non-critical sorries, and no repo-local pin/import/check in this Lake closure"

/-- The audited external candidate is not recorded as a terminal proof. -/
theorem cguthRochRiemannRefactorAudit_terminal_not_found :
    cguthRochRiemannRefactorAudit.terminalProofFound = false :=
  rfl

/--
External-anchor gate for the audited candidate: because no terminal proof was
found, the repo-local integration-debt gate is vacuous for this candidate.
-/
def cguthRochRiemannRefactorAnchorAudit : ExternalLeanAnchorAudit where
  exactTheoremFound := False
  importedIntoLakeClosure := False
  concreteIntegrationBlockerRecorded := True

/-- The audited external candidate satisfies the local integration-debt gate. -/
theorem cguthRochRiemannRefactor_integrationDebtGate :
    RepoLocalIntegrationDebtGate cguthRochRiemannRefactorAnchorAudit :=
  repoLocalIntegrationDebtGate_of_no_external_anchor
    cguthRochRiemannRefactorAnchorAudit not_false

/-- Current machine-proof debt classification for this repaired Stage1 module. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: full algebraic-curve Riemann-Roch proof is not repo-local closed",
  "not_repo_local_closed: this file is a statement-shape wrapper plus checked substrate anchors",
  "repo_local_integration_debt_gate: no completion claim may retain anchor-only external evidence"
]

/-- Theorem-internal child leaves for the next M0387-level module split. -/
def theoremInternalChildLeaves : List String := [
  "S1-M-124-leaf-001 statement normalization and notation freeze",
  "S1-M-124-leaf-002 concrete curve object model: smooth proper geometrically connected dimension-one schemes",
  "S1-M-124-leaf-003 divisor API selection: Cartier/Weil divisors and linear equivalence",
  "S1-M-124-leaf-004 sheaf bridge: divisor line bundles and global sections",
  "S1-M-124-leaf-005 cohomology dimensions, Euler characteristic, genus, and canonical divisor",
  "S1-M-124-leaf-006 low-dimensional or special-base sanity wrappers",
  "S1-M-124-leaf-007 mathlib and external Lean 4 terminal theorem audit",
  "S1-M-124-leaf-008 pin/import/check or integration-blocker handling for any external closure",
  "S1-M-124-leaf-009 replacement of StatementShape by local proof body or checked upstream wrapper"
]

/--
Concrete M0387-level split for the formerly unchecked leaves `M0175-L013`
through `M0175-L021`.

These records are execution targets, not proof claims.  A leaf remains open
until its target Lean surface has a local proof body, a pinned checked upstream
wrapper, or a concrete integration blocker when an external proof is found.
-/
structure M0175ConcreteLeafSplit where
  leafId : String
  packageName : String
  localTask : String
  concreteInputs : List String
  targetLeanSurface : List String
  acceptanceGate : List String
  budgetBound : Nat
  currentStatus : String

/-- Concrete split of `M0175-L013` through `M0175-L021` into local proof tasks. -/
def m0175ConcreteLeafSplits : List M0175ConcreteLeafSplit := [
  {
    leafId := "M0175-L013",
    packageName := "P02.divisor_model",
    localTask :=
      "Select the concrete divisor object model for curves and expose its equivalence boundary",
    concreteInputs := [
      "AlgebraicCurveBoundary",
      "selectedDivisorObjectModelDecision",
      "pinnedMathlibAnchorAuditNote"
    ],
    targetLeanSurface := [
      "replacement or refinement of RiemannRochDivisorData.CurveDivisor",
      "checked bridge from the selected Cartier-facing model to any Weil/projective-curve backend",
      "proof that the chosen model is not an anchor-only external dependency"
    ],
    acceptanceGate := [
      "Cartier, Weil, or pinned projective-curve divisor API is available in the local Lake closure",
      "model choice is represented by checked declarations, not prose only",
      "no proof-placeholder tactic or new primitive assumption is introduced"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L014",
    packageName := "P02.divisor_model",
    localTask :=
      "Define divisor degree and its compatibility obligations for subtraction and linear equivalence",
    concreteInputs := [
      "M0175-L013 selected divisor object model",
      "RiemannRochDivisorData.degree",
      "RiemannRochDivisorData.sub"
    ],
    targetLeanSurface := [
      "degree function on the concrete divisor type",
      "subtraction compatibility lemmas required for K-D",
      "linear-equivalence invariance statement for degree if the chosen API exposes linear equivalence"
    ],
    acceptanceGate := [
      "degree target compiles against the selected divisor API",
      "compatibility lemmas are theorem statements with local proofs or pinned checked wrappers",
      "leaf proof budget remains at most 100 local steps"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L015",
    packageName := "P03.line_bundle_bridge",
    localTask :=
      "Construct or import the divisor-to-line-bundle bridge D -> O(D)",
    concreteInputs := [
      "M0175-L013 selected divisor object model",
      "M0175-L014 divisor subtraction and degree surfaces",
      "Mathlib.AlgebraicGeometry.Modules.Sheaf"
    ],
    targetLeanSurface := [
      "line bundle or invertible sheaf associated to a divisor",
      "compatibility surface for O(K-D)",
      "bridge theorem from the concrete line-bundle API back to RiemannRochDivisorData"
    ],
    acceptanceGate := [
      "O(D) and O(K-D) are represented by checked Lean declarations",
      "the bridge is local or pinned/imported/checked",
      "no anchor-only external line-bundle evidence is treated as complete"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L016",
    packageName := "P04.cohomology_dimension_model",
    localTask :=
      "Define ell(D) as the finite dimension of global sections of O(D)",
    concreteInputs := [
      "RiemannRochFiniteH0Model",
      "selectedCohomologyObjectModelDecision",
      "M0175-L015 divisor-to-line-bundle bridge"
    ],
    targetLeanSurface := [
      "global-section vector space H0(X, O(D))",
      "ell(D) equals finrank over the base field",
      "corresponding statement for ell(K-D)"
    ],
    acceptanceGate := [
      "H0 spaces have AddCommGroup and Module instances over the base field",
      "ell-to-finrank equalities are checked theorem statements",
      "integer coercions in the final formula are fixed locally"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L017",
    packageName := "P04.cohomology_dimension_model",
    localTask :=
      "Prove finite-dimensionality of the relevant H0 spaces on proper curves",
    concreteInputs := [
      "M0175-L016 global-section model",
      "AlgebraicCurveBoundary.proper",
      "selectedCohomologyObjectModelDecision"
    ],
    targetLeanSurface := [
      "FiniteDimensional k H0(X, O(D))",
      "FiniteDimensional k H0(X, O(K-D))",
      "finite-dimensionality bridge accepted by RiemannRochFiniteH0Model"
    ],
    acceptanceGate := [
      "finite-dimensionality proof is local or comes from a pinned checked upstream theorem",
      "properness/coherence hypotheses are explicit",
      "no untracked project-specific primitive assumption supplies finiteness"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L018",
    packageName := "P05.genus_canonical_model",
    localTask :=
      "Define genus and canonical divisor and prove their convention bridge",
    concreteInputs := [
      "M0175-L013 selected divisor object model",
      "M0175-L016 cohomology dimension model",
      "HomologicalComplexEulerChar"
    ],
    targetLeanSurface := [
      "genus definition compatible with the curve API",
      "canonical divisor or canonical line bundle surface",
      "convention bridge aligning genus, degree K, and Euler characteristic signs"
    ],
    acceptanceGate := [
      "genus and canonical object definitions are checked in Lean",
      "K-D in the formula matches the selected subtraction/line-bundle convention",
      "Euler-characteristic sign convention is recorded by checked declarations"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L019",
    packageName := "P06.riemann_roch_core",
    localTask :=
      "Prove or import the Euler-characteristic Riemann-Roch identity for line bundles on curves",
    concreteInputs := [
      "M0175-L015 line-bundle bridge",
      "M0175-L017 finite-dimensional H0/H1 infrastructure",
      "M0175-L018 genus and canonical convention bridge"
    ],
    targetLeanSurface := [
      "chi(O(D)) = deg(D) + 1 - g for divisor line bundles",
      "Serre-duality or residual-series bridge for H1 and H0(K-D)",
      "theorem-level audit row for any imported upstream identity"
    ],
    acceptanceGate := [
      "core identity has a local proof body or pinned checked upstream wrapper",
      "external conditional attempts with placeholder assumptions are not marked complete",
      "repo_local_integration_debt is discharged or blocked concretely"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L020",
    packageName := "P06.riemann_roch_core",
    localTask :=
      "Derive the divisor-dimension formula from the cohomological statement",
    concreteInputs := [
      "M0175-L016 ell-as-finrank bridge",
      "M0175-L018 canonical divisor convention",
      "M0175-L019 Euler-characteristic Riemann-Roch identity"
    ],
    targetLeanSurface := [
      "checked theorem deriving RiemannRochFormula for the concrete divisor package",
      "coercion lemmas from Nat finrank to Int formula terms",
      "replacement theorem connecting concrete APIs to StatementShape"
    ],
    acceptanceGate := [
      "final formula compiles without abstract placeholder assumptions",
      "the local theorem proves the same D, K-D, degree, and genus convention as StatementShape",
      "public completion remains unchecked until this proof or a pinned equivalent validates"
    ],
    budgetBound := 100,
    currentStatus := "split_concrete_unchecked_formalization_debt"
  },
  {
    leafId := "M0175-L021",
    packageName := "P07.repo_local_closure_gate",
    localTask :=
      "Re-run local validation after any local proof, wrapper, or dependency pin/import",
    concreteInputs := [
      "M0175-L013 through M0175-L020",
      "RepoLocalIntegrationDebtGate",
      "cguthRochRiemannRefactorAnchorAudit"
    ],
    targetLeanSurface := [
      "lake env lean AwesomeTheorems/Stage1/S1_M_124.lean passes",
      "any new dependency is pinned in the project and checked locally",
      "completion status distinguishes local_proof_body, local_wrapper_upstream_mathlib, external_upstream_pinned, and not_repo_local_closed"
    ],
    acceptanceGate := [
      "validation command exits with code 0",
      "text audit finds no proof-placeholder tactic or new primitive assumption declaration",
      "no completed state retains repo_local_integration_debt"
    ],
    budgetBound := 30,
    currentStatus := "split_concrete_unchecked_closure_gate"
  }
]

/-- The concrete split covers exactly the nine requested formerly unchecked leaves. -/
def m0175ConcreteLeafSplitIds : List String :=
  m0175ConcreteLeafSplits.map (fun leaf => leaf.leafId)

/-- The requested leaf range has been split into `M0175-L013` through `M0175-L021`. -/
theorem m0175ConcreteLeafSplitIds_eq :
    m0175ConcreteLeafSplitIds = [
      "M0175-L013",
      "M0175-L014",
      "M0175-L015",
      "M0175-L016",
      "M0175-L017",
      "M0175-L018",
      "M0175-L019",
      "M0175-L020",
      "M0175-L021"
    ] :=
  rfl

/-- There are nine concrete child leaves in the `M0175-L013` through `M0175-L021` split. -/
theorem m0175ConcreteLeafSplits_length :
    m0175ConcreteLeafSplits.length = 9 :=
  rfl

/--
Completion status for the concrete split itself.

The split is checked local documentation-as-data, but the terminal
Riemann-Roch theorem remains formalization debt until the target surfaces above
are replaced by local proof bodies or pinned checked upstream wrappers.
-/
def m0175ConcreteLeafSplitCompletionStatus : String :=
  "split_complete_but_theorem_not_repo_local_closed"

/-- The concrete split does not close the terminal Riemann-Roch theorem. -/
theorem m0175ConcreteLeafSplitCompletionStatus_not_closed :
    m0175ConcreteLeafSplitCompletionStatus =
      "split_complete_but_theorem_not_repo_local_closed" :=
  rfl

/--
Repo-local closure statuses accepted by the Stage1 completion gate for
THM-M-0175.

`externalUpstreamAnchorOnly` is represented so that audits can classify it
explicitly, but it is not a completion state under the M0387 rules.
-/
inductive RepoLocalClosureStatus where
  | notRepoLocalClosed
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  deriving DecidableEq, Repr

/--
Checked public-completion gate for this Stage1 artifact.

The booleans are intentionally redundant audit flags: a serial integrator can
read the record without inferring from prose whether public completion may be
checked.
-/
structure PublicCompletionGateReport where
  currentStatus : RepoLocalClosureStatus
  terminalLocalProofBodyPresent : Bool
  pinnedExternalDependencyChecked : Bool
  anchorOnlyEvidenceCountedAsCompletion : Bool
  publicCompletionAllowed : Bool
  rationale : List String

/-- Closure statuses that may support a public completion checkmark. -/
def RepoLocalClosureStatus.isCompletionStatus :
    RepoLocalClosureStatus -> Bool
  | RepoLocalClosureStatus.localProofBody => true
  | RepoLocalClosureStatus.localWrapperUpstreamMathlib => true
  | RepoLocalClosureStatus.externalUpstreamPinned => true
  | RepoLocalClosureStatus.notRepoLocalClosed => false
  | RepoLocalClosureStatus.externalUpstreamAnchorOnly => false

/--
Predicate for a report that is strong enough to allow public completion.

This combines the status enum with the concrete proof-body/dependency flags and
forbids treating anchor-only external evidence as completion.
-/
def PublicCompletionGateReport.allowsCompletion
    (R : PublicCompletionGateReport) : Prop :=
  R.publicCompletionAllowed = true /\
    R.currentStatus.isCompletionStatus = true /\
    (R.terminalLocalProofBodyPresent = true \/
      R.pinnedExternalDependencyChecked = true) /\
    R.anchorOnlyEvidenceCountedAsCompletion = false

/--
Current public-completion gate for THM-M-0175.

The current artifact has checked statement-shape/audit data only.  It has no
local proof body for the algebraic-curve Riemann-Roch theorem and no external
proof dependency pinned into this Lake closure, so public completion must remain
unchecked.
-/
def currentPublicCompletionGateReport : PublicCompletionGateReport where
  currentStatus := RepoLocalClosureStatus.notRepoLocalClosed
  terminalLocalProofBodyPresent := false
  pinnedExternalDependencyChecked := false
  anchorOnlyEvidenceCountedAsCompletion := false
  publicCompletionAllowed := false
  rationale := [
    "statement-shape and audit declarations compile, but no terminal algebraic-curve Riemann-Roch proof body is present",
    "no external Lean 4 proof dependency has been pinned/imported/checked in this Lake closure",
    "anchor-only evidence is not counted as completion under the repo-local integration-debt gate"
  ]

/-- The current completion status is explicitly not repo-local closed. -/
theorem currentPublicCompletionGateReport_status :
    currentPublicCompletionGateReport.currentStatus =
      RepoLocalClosureStatus.notRepoLocalClosed :=
  rfl

/-- Public completion is currently not allowed for THM-M-0175. -/
theorem currentPublicCompletionGateReport_unchecked :
    currentPublicCompletionGateReport.publicCompletionAllowed = false :=
  rfl

/-- The current gate does not retain anchor-only evidence as completion. -/
theorem currentPublicCompletionGateReport_no_anchor_only_completion :
    currentPublicCompletionGateReport.anchorOnlyEvidenceCountedAsCompletion =
      false :=
  rfl

/-- The current report cannot satisfy the public-completion predicate. -/
theorem currentPublicCompletionGateReport_not_allowsCompletion :
    Not currentPublicCompletionGateReport.allowsCompletion := by
  intro h
  exact Bool.false_ne_true h.1

/-! ## Audit probes -/

#check Scheme
#check Scheme.Hom
#check Spec
#check IsIntegral
#check Smooth
#check IsProper
#check LocallyOfFiniteType
#check Scheme.functionField
#check HomologicalComplex.eulerChar
#check StatementShape
#check formulaPackage_of_statementShape
#check properMorphism_locallyOfFiniteType
#check integralScheme_irreducibleSpace
#check RepoLocalIntegrationDebtGate
#check MathlibAnchorAuditNote
#check pinnedMathlibAnchorAuditNote
#check pinnedMathlibAnchorAuditNote_revision
#check pinnedMathlibAnchorAuditNote_terminal_not_found
#check CurveDivisorObjectModel
#check DivisorObjectModelDecision
#check selectedDivisorObjectModelDecision
#check selectedDivisorObjectModelDecision_model
#check selectedDivisorObjectModelDecision_not_closed
#check RiemannRochFiniteH0Model
#check CurveCohomologyObjectModel
#check CohomologyObjectModelDecision
#check selectedCohomologyObjectModelDecision
#check selectedCohomologyObjectModelDecision_model
#check selectedCohomologyObjectModelDecision_not_closed
#check cguthRochRiemannRefactorAudit
#check cguthRochRiemannRefactorAudit_terminal_not_found
#check cguthRochRiemannRefactorAnchorAudit
#check cguthRochRiemannRefactor_integrationDebtGate
#check M0175ConcreteLeafSplit
#check m0175ConcreteLeafSplits
#check m0175ConcreteLeafSplitIds_eq
#check m0175ConcreteLeafSplits_length
#check m0175ConcreteLeafSplitCompletionStatus_not_closed
#check RepoLocalClosureStatus
#check PublicCompletionGateReport
#check PublicCompletionGateReport.allowsCompletion
#check currentPublicCompletionGateReport
#check currentPublicCompletionGateReport_status
#check currentPublicCompletionGateReport_unchecked
#check currentPublicCompletionGateReport_no_anchor_only_completion
#check currentPublicCompletionGateReport_not_allowsCompletion

end S1_M_124
end Stage1
end AwesomeTheorems
