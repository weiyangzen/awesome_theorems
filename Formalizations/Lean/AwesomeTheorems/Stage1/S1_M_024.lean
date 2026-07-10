import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion
import Mathlib.AlgebraicGeometry.Morphisms.Descent
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.CategoryTheory.Sites.Descent.DescentData
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.RingTheory.Kaehler.Basic

/-!
# S1-M-024 / THM-M-0111: Kodaira embedding theorem

This Stage1 artifact records a conservative Lean 4 boundary for the theorem
that Hodge manifolds are projective.  The local dependency closure has useful
scheme, projective-spectrum, properness, and complex-manifold infrastructure,
but this file does not claim a proof of the analytic Kodaira embedding theorem.

The terminal statement is therefore represented as `StatementShape : Prop`
over explicit abstract predicates for the analytic Hodge-manifold hypotheses
and the resulting projective embedding.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace AwesomeTheorems.Stage1.S1_M_024

universe u v

/--
Statement-side analytic data for a compact Hodge manifold.

The fields are intentionally proposition-valued until a later pass pins the
precise mathlib APIs for compact complex manifolds, Kahler forms, integral
cohomology classes, and the Hodge condition.
-/
structure HodgeManifoldData where
  carrier : Type u
  topology : TopologicalSpace carrier
  compactComplexManifold : Prop
  kahlerManifold : Prop
  integralKahlerClass : Prop

/--
Statement-side output data: a holomorphic embedding into a finite-dimensional
complex projective space.

`ambientIsProjectiveSpace` and `holomorphicClosedEmbedding` are kept as explicit
predicates because this repair did not identify a repo-local API connecting
complex-analytic manifolds, line bundles, and projective-space embeddings.
-/
structure ProjectiveEmbeddingData (D : HodgeManifoldData.{u}) where
  ambient : Type u
  ambientTopology : TopologicalSpace ambient
  projectiveDimension : Nat
  ambientIsProjectiveSpace : Prop
  embedding : D.carrier → ambient
  holomorphicClosedEmbedding : Prop

/-- The normalized input predicate for the Kodaira embedding theorem. -/
def IsHodgeManifold (D : HodgeManifoldData.{u}) : Prop :=
  D.compactComplexManifold ∧ D.kahlerManifold ∧ D.integralKahlerClass

/-- The normalized projectivity conclusion as existence of a projective embedding. -/
def IsProjectiveManifold (D : HodgeManifoldData.{u}) : Prop :=
  Nonempty (ProjectiveEmbeddingData D)

/--
Fully unfolded public statement-normalization target for the Stage1 boundary.

Universe/object shape:
* one Lean universe `u`;
* one analytic carrier package `D : HodgeManifoldData.{u}`;
* `D.carrier : Type u` carries the statement-side topological space field.

Hypothesis shape:
`D.compactComplexManifold ∧ D.kahlerManifold ∧ D.integralKahlerClass`.

Conclusion shape:
there exists a `ProjectiveEmbeddingData D`, containing a finite natural
projective dimension, an ambient type in the same universe, and an abstract
holomorphic closed-embedding predicate into complex projective space.
-/
def NormalizedKodairaEmbeddingShape : Prop :=
  ∀ D : HodgeManifoldData.{u},
    D.compactComplexManifold ∧ D.kahlerManifold ∧ D.integralKahlerClass →
      Nonempty (ProjectiveEmbeddingData D)

/--
Stage1 statement shape for Kodaira embedding:
every compact complex Hodge manifold admits a projective embedding.
-/
def StatementShape : Prop :=
  ∀ D : HodgeManifoldData.{u}, IsHodgeManifold D → IsProjectiveManifold D

/-- The public `StatementShape` is definitionally the unfolded normalized shape. -/
theorem statementShape_eq_normalizedKodairaEmbeddingShape :
    StatementShape.{u} = NormalizedKodairaEmbeddingShape.{u} :=
  rfl

/-- Projection wrapper: a supplied embedding package proves the local conclusion. -/
theorem projective_of_embeddingData {D : HodgeManifoldData.{u}}
    (h : Nonempty (ProjectiveEmbeddingData D)) : IsProjectiveManifold D :=
  h

/--
Wrapper from a future terminal embedding theorem to the frozen Stage1 statement
shape.  This is checked, but it assumes the future theorem as an argument rather
than proving Kodaira embedding.
-/
theorem statementShape_of_projective_embedding
    (h : ∀ D : HodgeManifoldData.{u}, IsHodgeManifold D → Nonempty (ProjectiveEmbeddingData D)) :
    StatementShape.{u} := by
  intro D hD
  exact h D hD

/-! ## Complex/Kahler package frontier -/

/--
Complex/Kahler input package that a genuine formalization of Kodaira embedding
has to pin before the theorem can be stated with native analytic APIs.

The fields are proof obligations, not definitions supplied by this file.
They deliberately separate the complex manifold, Kahler form, integral class,
and Hermitian positive line-bundle layers because these are distinct API
families in the informal proof.
-/
structure KodairaComplexKahlerPackage (D : HodgeManifoldData.{u}) : Type (u + 1) where
  compactComplexChartsPinned : D.compactComplexManifold
  kahlerFormPinned : D.kahlerManifold
  integralClassPinned : D.integralKahlerClass
  hermitianLineBundlePinned : Prop
  positiveCurvatureRepresentsClass : Prop

/-! ## Positive line-bundle / integral Kahler bridge frontier -/

/--
P03 bridge package for the Kodaira proof tree.

This structure isolates the classical bridge from an integral positive Kahler
class to a holomorphic Hermitian line bundle with positive curvature.  The
fields are still proof obligations because the current local mathlib closure
does not expose the analytic Chern-class, holomorphic line-bundle, or
curvature-form APIs needed to prove them natively.
-/
structure PositiveLineBundleIntegralKahlerBridgePackage
    (D : HodgeManifoldData.{u}) : Type (u + 1) where
  compactComplexChartsPinned : D.compactComplexManifold
  kahlerFormPinned : D.kahlerManifold
  integralClassPinned : D.integralKahlerClass
  holomorphicHermitianLineBundlePinned : Prop
  firstChernClassMatchesIntegralKahlerClass : Prop
  curvatureFormRepresentsKahlerClass : Prop
  curvatureFormPositive : Prop
  tensorPowersRemainPositive : Prop
  positiveImpliesAmpleReductionTarget : Prop

/--
A P03 bridge package supplies the corresponding front half of the existing
Kodaira complex/Kahler frontier.  This is a checked package projection, not a
proof that such a bridge package exists.
-/
def complexKahlerPackage_of_positiveLineBundleBridge
    {D : HodgeManifoldData.{u}}
    (P : PositiveLineBundleIntegralKahlerBridgePackage D) :
    KodairaComplexKahlerPackage D where
  compactComplexChartsPinned := P.compactComplexChartsPinned
  kahlerFormPinned := P.kahlerFormPinned
  integralClassPinned := P.integralClassPinned
  hermitianLineBundlePinned := P.holomorphicHermitianLineBundlePinned
  positiveCurvatureRepresentsClass :=
    P.curvatureFormPositive ∧ P.curvatureFormRepresentsKahlerClass

/--
If the P03 bridge package is ever constructed, the normalized Hodge-manifold
input predicate follows immediately from its checked analytic fields.
-/
theorem isHodgeManifold_of_positiveLineBundleBridge
    {D : HodgeManifoldData.{u}}
    (P : PositiveLineBundleIntegralKahlerBridgePackage D) :
    IsHodgeManifold D := by
  exact ⟨P.compactComplexChartsPinned, P.kahlerFormPinned, P.integralClassPinned⟩

/--
Finite-dimensional holomorphic section package for the Kodaira map.

Informally this is where powers of a positive line bundle acquire enough
global sections to separate points and tangent vectors.
-/
structure KodairaSectionSeparationPackage (D : HodgeManifoldData.{u}) : Type (u + 1) where
  amplePowerGlobalSectionsPinned : Prop
  finiteDimensionalSectionSpace : Prop
  separatesPoints : Prop
  separatesTangentVectors : Prop

/--
Projective-map package for the final embedding construction.

The `embeddingData` field is the first point at which the Stage1 boundary has
the exact local conclusion `ProjectiveEmbeddingData D`; earlier package fields
are kept separate so a future integrator can replace them one-by-one with
native mathlib or pinned external APIs.
-/
structure KodairaProjectiveMapPackage (D : HodgeManifoldData.{u}) : Type (u + 1) where
  complexProjectiveSpacePinned : Prop
  mapFromSectionsConstructed : Prop
  holomorphicMapProved : Prop
  closedEmbeddingProved : Prop
  embeddingData : ProjectiveEmbeddingData D

/--
Full proof-package frontier for Kodaira embedding.

A term of this structure is intentionally stronger than the current artifact:
it would contain the analytic/Kahler package, the section-separation package,
and the final projective-map package.  The current file only checks wrappers
around this frontier.
-/
structure KodairaEmbeddingProofPackage (D : HodgeManifoldData.{u}) : Type (u + 1) where
  complexKahler : KodairaComplexKahlerPackage D
  sectionSeparation : KodairaSectionSeparationPackage D
  projectiveMap : KodairaProjectiveMapPackage D

/-- A completed proof package supplies the local projective-manifold conclusion. -/
theorem projective_of_proofPackage {D : HodgeManifoldData.{u}}
    (h : Nonempty (KodairaEmbeddingProofPackage D)) : IsProjectiveManifold D := by
  rcases h with ⟨P⟩
  exact ⟨P.projectiveMap.embeddingData⟩

/--
Wrapper from future per-object proof packages to the frozen Stage1 statement
shape.  This is a checked frontier theorem only; it does not construct the
packages.
-/
theorem statementShape_of_proofPackages
    (h : ∀ D : HodgeManifoldData.{u},
      IsHodgeManifold D → Nonempty (KodairaEmbeddingProofPackage D)) :
    StatementShape.{u} := by
  intro D hD
  exact projective_of_proofPackage (h D hD)

/--
Scheme-side bridge target: a morphism factors through a closed immersion into an
ambient scheme proper over the base.  This is a common algebraic shadow of
projectivity used by nearby Stage1 algebraic-geometry modules.
-/
def SchemeProjectiveOverViaClosedImmersion
    (S X P : Scheme.{u}) (f : X ⟶ S) : Prop :=
  ∃ (p : P ⟶ S) (i : X ⟶ P), IsClosedImmersion i ∧ IsProper p ∧ i ≫ p = f

/-- Closed immersions are proper in the imported scheme-morphism API. -/
theorem closedImmersion_isProper {X P : Scheme.{u}} (i : X ⟶ P) [IsClosedImmersion i] :
    IsProper i :=
  inferInstance

/--
Checked scheme-side wrapper: a closed immersion into an ambient scheme proper
over the base gives a proper composite map to the base.
-/
theorem projectiveOverViaClosedImmersion_isProper
    {S X P : Scheme.{u}} {f : X ⟶ S} {p : P ⟶ S} {i : X ⟶ P}
    (hi : IsClosedImmersion i) (hp : IsProper p) (hfac : i ≫ p = f) :
    IsProper f := by
  haveI : IsClosedImmersion i := hi
  haveI : IsProper p := hp
  subst f
  infer_instance

/--
Pinned mathlib anchor: finite-type `Proj` is proper over its degree-zero base.
This is not Kodaira embedding, but it verifies projective-scheme infrastructure
needed on the algebraic side of a future integration.
-/
theorem projToSpecZero_isProper
    {A : Type u} {sigma : Type v} [CommRing A] [SetLike sigma A]
    [AddSubgroupClass sigma A] (Agraded : Nat → sigma) [GradedRing Agraded]
    [Algebra.FiniteType (Agraded 0) A] :
    IsProper (Proj.toSpecZero Agraded) := by
  infer_instance

/-- Statement shape for the checked `Proj.toSpecZero` properness anchor. -/
def ProjectiveSpectrumProperAnchorShape : Prop :=
  ∀ {A : Type u} {sigma : Type v} [CommRing A] [SetLike sigma A]
    [AddSubgroupClass sigma A] (Agraded : Nat → sigma) [GradedRing Agraded]
    [Algebra.FiniteType (Agraded 0) A], IsProper (Proj.toSpecZero Agraded)

/-- Audit shape for a possible exact external Lean 4 Kodaira embedding proof. -/
structure ExternalLeanAnchorAudit where
  exactKodairaEmbeddingTheoremFound : Prop
  importedIntoLakeClosure : Prop
  concreteIntegrationBlockerRecorded : Prop

/--
Repo-local integration-debt gate for exact external anchors.

If a future audit finds a complete external Lean 4 Kodaira embedding proof, this
Stage1 slot cannot be completed from an anchor alone: the proof must either be
pin/import/check integrated into this Lake closure or blocked by a concrete
dependency, license, or toolchain reason.
-/
def RepoLocalIntegrationDebtGate (A : ExternalLeanAnchorAudit) : Prop :=
  A.exactKodairaEmbeddingTheoremFound →
    A.importedIntoLakeClosure ∨ A.concreteIntegrationBlockerRecorded

/-- If no exact external Lean 4 proof anchor is found, the gate is vacuous. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit)
    (h : ¬ A.exactKodairaEmbeddingTheoremFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/-! ## P08 repo-local wrapper/pin closure gate -/

/--
Allowed repo-local closure routes for the P08 completion gate.

All three routes require an actual local Lean validation run before any public
status upgrade.  The current file only records the gate; it does not provide
one of these closure routes for Kodaira embedding.
-/
inductive RepoLocalClosureRoute where
  | local_proof_body
  | local_wrapper_upstream_mathlib
  | external_upstream_pinned
  deriving DecidableEq, Repr

/--
P08 completion record.  A record satisfies `P08CompletionGate` only when a
machine closure is available, a repo-local closure route is selected, the local
validation command has passed, and public status upgrade is explicitly allowed.
-/
structure P08RepoLocalClosureRecord where
  machineClosureAvailable : Prop
  closureRoute : Option RepoLocalClosureRoute
  validationCommand : String
  validationPassed : Prop
  publicStatusUpgradeAllowed : Prop

/-- P08's required validation command for this Stage1 artifact. -/
def p08ValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_024.lean"

/-- The exact P08 completion gate: closure route plus local validation. -/
def P08CompletionGate (R : P08RepoLocalClosureRecord) : Prop :=
  R.machineClosureAvailable ∧
    R.closureRoute.isSome = true ∧
    R.validationCommand = p08ValidationCommand ∧
    R.validationPassed ∧
    R.publicStatusUpgradeAllowed

/--
Current P08 record for Kodaira embedding.

This deliberately records the absence of machine closure.  It therefore blocks
wrapper/pin completion and any public status upgrade while keeping the local
Lean artifact checkable.
-/
def p08CurrentClosureRecord : P08RepoLocalClosureRecord where
  machineClosureAvailable := False
  closureRoute := none
  validationCommand := p08ValidationCommand
  validationPassed := False
  publicStatusUpgradeAllowed := False

/-- Without machine closure, P08 cannot be completed. -/
theorem no_p08_completion_without_machine_closure
    (R : P08RepoLocalClosureRecord)
    (h : ¬ R.machineClosureAvailable) :
    ¬ P08CompletionGate R := by
  intro hgate
  exact h hgate.1

/-- The current Kodaira P08 record is intentionally not a completion record. -/
theorem p08_current_not_completed :
    ¬ P08CompletionGate p08CurrentClosureRecord := by
  exact no_p08_completion_without_machine_closure p08CurrentClosureRecord (by
    intro h
    exact h)

/-- Integration-ready P08 wrapper/pin plan for a later serial integrator. -/
def p08RepoLocalWrapperPinPlan : List String :=
  [ "Do not add a Kodaira wrapper until an exact Lean 4 theorem or local proof body exists.",
    "If the exact theorem lands in pinned mathlib, import its module and prove a local wrapper of StatementShape.",
    "If the exact theorem is in an external Lean 4 project, add a pinned Lake dependency or vendor the proof body before wrapping it.",
    "If pin/import/check fails, record the concrete dependency, license, or toolchain blocker and leave the slot open.",
    "After the wrapper or proof body is present, run p08ValidationCommand and only then propose a public status upgrade." ]

/-! ## External Lean 4 anchor audit for S1-M-024-P07 -/

/-- One primary-source row for the external Lean 4 anchor audit. -/
structure ExternalLeanAnchorAuditRow where
  repositoryUrl : String
  commit : String
  sourceOrQuery : String
  theoremNames : String
  exactKodairaEmbeddingStatus : String
  lakeIntegrationFeasibility : String
  blockerOrNextStep : String
  deriving Repr

/-- Date on which the external Lean 4 anchor audit rows were backfilled. -/
def externalLeanAnchorAuditDate : String :=
  "2026-05-01"

/--
Primary-source external Lean 4 audit for the exact Kodaira embedding anchor.

The rows deliberately distinguish adjacent imported infrastructure from an exact
Kodaira embedding theorem.  No row is counted as theorem completion.
-/
def externalLeanAnchorAuditRows : List ExternalLeanAnchorAuditRow := [
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    sourceOrQuery := "Mathlib/Geometry/Manifold/Complex.lean, local pinned checkout plus public upstream URL at the same commit",
    theoremNames := "MDifferentiable.isLocallyConstant; MDifferentiable.exists_eq_const_of_compactSpace",
    exactKodairaEmbeddingStatus := "not_exact; the source file explicitly lists holomorphic vector/line bundles and section theory as future TODOs",
    lakeIntegrationFeasibility := "already_pinned_and_import_checked_by_this_file via Mathlib.Geometry.Manifold.Complex",
    blockerOrNextStep := "This is complex-manifold infrastructure only; it does not provide compact Hodge manifolds, positive line bundles, very ampleness, or a projective embedding theorem."
  },
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    sourceOrQuery := "Mathlib/AlgebraicGeometry/ProjectiveSpectrum/Proper.lean",
    theoremNames := "AlgebraicGeometry.Proj.toSpecZero; instance IsProper (Proj.toSpecZero _)",
    exactKodairaEmbeddingStatus := "not_exact; algebraic Proj properness anchor only",
    lakeIntegrationFeasibility := "already_pinned_and_import_checked_by_this_file via Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper and projToSpecZero_isProper",
    blockerOrNextStep := "Useful for algebraic projective targets, but it does not construct a holomorphic map from a compact Hodge manifold."
  },
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    sourceOrQuery := "Mathlib/CategoryTheory/Sites/SheafCohomology/Basic.lean",
    theoremNames := "CategoryTheory.Sheaf.H; CategoryTheory.Sheaf.cohomologyPresheaf; CategoryTheory.Sheaf.H'",
    exactKodairaEmbeddingStatus := "not_exact; general abelian sheaf cohomology infrastructure only",
    lakeIntegrationFeasibility := "already_pinned_and_import_checked_by_this_file via Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
    blockerOrNextStep := "No coherent analytic sheaf, holomorphic line-bundle cohomology, Kodaira vanishing, or section-generation theorem is integrated."
  },
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    sourceOrQuery := "Mathlib/LinearAlgebra/Projectivization/Basic.lean",
    theoremNames := "Projectivization; Projectivization.mk; Projectivization.mk_eq_mk_iff; Projectivization.map; Projectivization.map_injective",
    exactKodairaEmbeddingStatus := "not_exact; linear-algebraic projectivization infrastructure only",
    lakeIntegrationFeasibility := "feasible_mathlib_import_if_needed; not imported by this file because it is not an exact Kodaira theorem",
    blockerOrNextStep := "Could support a future section-coordinate map, but lacks topology, complex-manifold structure, holomorphicity, and closed-embedding results."
  },
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    sourceOrQuery := "Mathlib/RingTheory/Kaehler/Basic.lean",
    theoremNames := "KaehlerDifferential; KaehlerDifferential.D; KaehlerDifferential.span_range_derivation",
    exactKodairaEmbeddingStatus := "not_exact; algebraic Kahler differentials, not analytic Kahler manifolds",
    lakeIntegrationFeasibility := "already_pinned_and_import_checked_by_this_file via Mathlib.RingTheory.Kaehler.Basic",
    blockerOrNextStep := "Does not supply Kahler metrics/forms, integral Kahler classes, curvature positivity, or Chern-class bridges."
  },
  {
    repositoryUrl := "https://github.com/leanprover-community/flt-regular",
    commit := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
    sourceOrQuery := "repo-local pinned package search over Lean sources for Kodaira, Hodge manifold, VeryAmple, and line-bundle terms",
    theoremNames := "none applicable to Kodaira embedding",
    exactKodairaEmbeddingStatus := "not_applicable; pinned package contains no exact Kodaira embedding anchor found by the local source search",
    lakeIntegrationFeasibility := "already_pinned_but_no_relevant_theorem_to_import",
    blockerOrNextStep := "No integration action for this theorem; keep the package out of the Kodaira completion claim."
  },
  {
    repositoryUrl := "https://github.com/search",
    commit := "not_available",
    sourceOrQuery := "Unauthenticated GitHub code-search/API queries for \"Kodaira embedding\", KodairaEmbedding, \"Hodge manifold\", and VeryAmple in Lean",
    theoremNames := "not_retrieved",
    exactKodairaEmbeddingStatus := "global_external_search_blocked; GitHub API returned rate-limit errors and browser search access timed out from this environment",
    lakeIntegrationFeasibility := "unknown_until_authenticated_primary_source_search_succeeds",
    blockerOrNextStep := "Run authenticated GitHub/source search; if an exact Lean 4 proof is found, pin/import/check it or record a concrete dependency, license, or toolchain blocker before any completion claim."
  }
]

/-- The P07 external-anchor audit currently records seven primary-source rows. -/
theorem externalLeanAnchorAuditRows_length :
    externalLeanAnchorAuditRows.length = 7 :=
  rfl

/-- P07 found no exact external Lean 4 Kodaira embedding proof inside the checked rows. -/
def externalLeanAnchorAuditConclusion : String :=
  "no_exact_external_lean4_kodaira_embedding_theorem_verified; adjacent mathlib anchors are pinned/import-checkable infrastructure only; global external search still needs authenticated source access"

/-- Mathlib modules audited as relevant anchors for this Stage1 boundary. -/
def mathlibAnchorModules : List String :=
  [ "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
    "Mathlib.AlgebraicGeometry.Morphisms.Descent",
    "Mathlib.Geometry.Manifold.Complex",
    "Mathlib.Geometry.Manifold.Riemannian.Basic",
    "Mathlib.RingTheory.Kaehler.Basic",
    "Mathlib.CategoryTheory.Sites.Descent.DescentData",
    "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
    "Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion",
    "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper" ]

/-! ## Public object-model audit for S1-M-024-P02 -/

/-- One row in the public-backfill object-model audit for Kodaira embedding. -/
structure KodairaObjectModelAuditRow where
  component : String
  mathlibSurface : String
  checkedAnchor : String
  repoLocalStatus : String
  kodairaRole : String
  blockerOrNextApi : String
  deriving Repr

/-- mathlib revision used by this Stage1 audit pass. -/
def objectModelAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Public-backfill-ready object-model table for the Kodaira embedding theorem.

Rows marked `local_wrapper_upstream_mathlib` or `checked_import_surface` are
locally import-checked infrastructure only. Rows marked `missing_terminal_api`
remain open formalization debt and must not be treated as theorem completion.
-/
def kodairaObjectModelAuditTable : List KodairaObjectModelAuditRow := [
  {
    component := "Complex manifolds and holomorphic maps",
    mathlibSurface := "Mathlib.Geometry.Manifold.Complex",
    checkedAnchor := "ModelWithCorners; IsManifold; MDifferentiable.isLocallyConstant; MDifferentiable.exists_eq_const_of_compactSpace",
    repoLocalStatus := "checked_import_surface",
    kodairaRole := "Supplies the complex-manifold differentiability substrate for analytic source objects and holomorphic maps.",
    blockerOrNextApi := "No compact complex Hodge-manifold object is selected; holomorphic vector/line bundles are explicitly listed as TODOs in this mathlib module."
  },
  {
    component := "Projective spectrum / Proj",
    mathlibSurface := "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper",
    checkedAnchor := "AlgebraicGeometry.Proj.toSpecZero; projToSpecZero_isProper",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    kodairaRole := "Provides checked algebraic projective-scheme infrastructure for finite-type Proj proper over its degree-zero base.",
    blockerOrNextApi := "This is scheme-side projective infrastructure only; it is not a complex projective-space embedding API for Kodaira."
  },
  {
    component := "Proper morphisms and closed immersions",
    mathlibSurface := "Mathlib.AlgebraicGeometry.Morphisms.Proper; Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion",
    checkedAnchor := "AlgebraicGeometry.IsProper; AlgebraicGeometry.IsClosedImmersion; closedImmersion_isProper; projectiveOverViaClosedImmersion_isProper",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    kodairaRole := "Supports the algebraic shadow that a closed immersion into a proper ambient scheme gives a proper structural morphism.",
    blockerOrNextApi := "Does not construct the analytic Kodaira map or identify its target with algebraic projective space."
  },
  {
    component := "Abelian sheaf cohomology",
    mathlibSurface := "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
    checkedAnchor := "CategoryTheory.Sheaf.H; CategoryTheory.Sheaf.cohomologyPresheaf; CategoryTheory.Sheaf.H'",
    repoLocalStatus := "checked_import_surface",
    kodairaRole := "Provides general Grothendieck-site abelian sheaf cohomology names that could host future vanishing statements.",
    blockerOrNextApi := "No coherent analytic sheaf, holomorphic line-bundle sheaf, or Kodaira/Serre vanishing theorem is pinned here."
  },
  {
    component := "Descent and local-to-global transport",
    mathlibSurface := "Mathlib.CategoryTheory.Sites.Descent.DescentData; Mathlib.AlgebraicGeometry.Morphisms.Descent",
    checkedAnchor := "CategoryTheory.Pseudofunctor.DescentData; AlgebraicGeometry.IsZariskiLocalAtTarget.descendsAlong",
    repoLocalStatus := "checked_import_surface",
    kodairaRole := "Records available categorical and algebraic-geometry descent infrastructure for later gluing/local-to-global proof packages.",
    blockerOrNextApi := "No descent theorem for holomorphic line bundles, global section generation, or analytic-to-algebraic comparison is selected."
  },
  {
    component := "Kahler differentials versus analytic Kahler geometry",
    mathlibSurface := "Mathlib.RingTheory.Kaehler.Basic; Mathlib.Geometry.Manifold.Riemannian.Basic",
    checkedAnchor := "KaehlerDifferential; IsRiemannianManifold; RiemannianBundle",
    repoLocalStatus := "checked_import_surface",
    kodairaRole := "Documents that the imported algebraic Kahler-differential API and Riemannian metric API are adjacent but not the integral Kahler-class package.",
    blockerOrNextApi := "Need a native Kahler form/metric plus integral cohomology-class interface for compact complex manifolds."
  },
  {
    component := "Line bundles, positivity, and very ampleness",
    mathlibSurface := "not located in the checked repo-local mathlib closure",
    checkedAnchor := "KodairaComplexKahlerPackage.hermitianLineBundlePinned; KodairaSectionSeparationPackage.amplePowerGlobalSectionsPinned",
    repoLocalStatus := "missing_terminal_api",
    kodairaRole := "Central API family for the positive line bundle, high tensor powers, generated sections, very ampleness, and the final projective embedding.",
    blockerOrNextApi := "Pin or implement holomorphic Hermitian line bundles, tensor powers, positivity/curvature, finite-dimensional global sections, and very-ample/projective-map APIs before any terminal proof claim."
  }
]

/-- The P02 object-model table covers the seven required audit components. -/
theorem kodairaObjectModelAuditTable_length :
    kodairaObjectModelAuditTable.length = 7 :=
  rfl

/-! ## Public proof-tree package for S1-M-024-P03 -/

/-- One node in the P03 positive-line-bundle bridge proof tree. -/
structure PositiveLineBundleBridgeProofTreeNode where
  nodeId : String
  parentId : String
  theoremTarget : String
  dependencySurface : String
  repoLocalStatus : String
  leafBudget : String
  blockerOrNextApi : String
  deriving Repr

/--
Public-backfill-ready proof tree for the positive line-bundle / integral
Kahler-class bridge.

Rows marked `checked_package_projection` are local wrappers over abstract
package data. Rows marked `unchecked_formalization_debt` are classical analytic
obligations that still need native or pinned upstream APIs before they can be
counted as completed leaves.
-/
def positiveLineBundleBridgeProofTree :
    List PositiveLineBundleBridgeProofTreeNode := [
  {
    nodeId := "KOD-P03",
    parentId := "KOD-ROOT",
    theoremTarget := "Build a positive holomorphic Hermitian line-bundle package from the integral Kahler-class hypothesis.",
    dependencySurface := "PositiveLineBundleIntegralKahlerBridgePackage; KodairaComplexKahlerPackage",
    repoLocalStatus := "package_frontier_checked_not_constructed",
    leafBudget := "unchecked package root; split into KOD-P03-L013 through KOD-P03-L018",
    blockerOrNextApi := "Needs native compact complex Kahler class, integral cohomology, holomorphic Hermitian line-bundle, curvature, Chern-class, and positivity APIs."
  },
  {
    nodeId := "KOD-P03-L013",
    parentId := "KOD-P03",
    theoremTarget := "Define the positive holomorphic Hermitian line-bundle interface over the compact complex source.",
    dependencySurface := "PositiveLineBundleIntegralKahlerBridgePackage.holomorphicHermitianLineBundlePinned",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 60",
    blockerOrNextApi := "Pin or implement a holomorphic Hermitian line-bundle object over compact complex manifolds."
  },
  {
    nodeId := "KOD-P03-L014",
    parentId := "KOD-P03",
    theoremTarget := "Connect the integral Kahler class to the first Chern class of the selected line bundle.",
    dependencySurface := "PositiveLineBundleIntegralKahlerBridgePackage.firstChernClassMatchesIntegralKahlerClass",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Pin integral cohomology and first-Chern-class APIs for holomorphic line bundles."
  },
  {
    nodeId := "KOD-P03-L015",
    parentId := "KOD-P03",
    theoremTarget := "Choose a Hermitian metric whose curvature form represents the integral Kahler class.",
    dependencySurface := "PositiveLineBundleIntegralKahlerBridgePackage.curvatureFormRepresentsKahlerClass",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Pin Chern connection, curvature-form, and de Rham/cohomology comparison APIs."
  },
  {
    nodeId := "KOD-P03-L016",
    parentId := "KOD-P03",
    theoremTarget := "Prove the curvature representative is positive in the analytic line-bundle sense.",
    dependencySurface := "PositiveLineBundleIntegralKahlerBridgePackage.curvatureFormPositive",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 60",
    blockerOrNextApi := "Pin positivity conventions relating Kahler forms and Hermitian line-bundle curvature."
  },
  {
    nodeId := "KOD-P03-L017",
    parentId := "KOD-P03",
    theoremTarget := "Record stability of positivity under tensor powers and the ampleness reduction target.",
    dependencySurface := "PositiveLineBundleIntegralKahlerBridgePackage.tensorPowersRemainPositive; PositiveLineBundleIntegralKahlerBridgePackage.positiveImpliesAmpleReductionTarget",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Pin tensor powers of holomorphic line bundles and the positive-to-ample or positive-to-very-ample bridge used downstream."
  },
  {
    nodeId := "KOD-P03-L018",
    parentId := "KOD-P03",
    theoremTarget := "Export the P03 bridge package into the existing Kodaira complex/Kahler frontier.",
    dependencySurface := "complexKahlerPackage_of_positiveLineBundleBridge; isHodgeManifold_of_positiveLineBundleBridge",
    repoLocalStatus := "checked_package_projection",
    leafBudget := "<= 20 checked",
    blockerOrNextApi := "Projection is checked, but it depends on an unconstructed bridge package and therefore is not theorem completion."
  }
]

/-- The P03 proof-tree package contains one root row and six leaf rows. -/
theorem positiveLineBundleBridgeProofTree_length :
    positiveLineBundleBridgeProofTree.length = 7 :=
  rfl

/-! ## Public proof-tree package for S1-M-024-P04 -/

/--
P04 cohomology-vanishing and section-generation package for the Kodaira proof
tree.

The fields are still proof obligations.  They isolate the analytic/coherent
sheaf layer that should sit between the positive line-bundle bridge and the
later point/tangent separation package: high tensor powers of the positive line
bundle, coherent sheaf cohomology, Kodaira-type vanishing, finite-dimensional
global sections, and finite-jet evaluation surjectivity.
-/
structure CohomologyVanishingSectionGenerationPackage
    (D : HodgeManifoldData.{u}) : Type (u + 1) where
  positiveLineBundleBridge : PositiveLineBundleIntegralKahlerBridgePackage D
  coherentSheafForTensorPowersPinned : Prop
  highTensorPowerCohomologyPinned : Prop
  kodairaVanishingForPositivePowers : Prop
  finiteDimensionalGlobalSections : Prop
  evaluationMapAtFiniteJetsPinned : Prop
  evaluationMapSurjectiveForHighPowers : Prop
  globallyGeneratedForHighPowers : Prop

/--
Checked projection: a P04 package supplies the pre-separation section data that
the existing `KodairaSectionSeparationPackage` frontier needs before the P05
point/tangent-separation proofs can be attempted.
-/
def SectionGenerationPrerequisites
    (D : HodgeManifoldData.{u}) : Prop :=
  ∃ _P : CohomologyVanishingSectionGenerationPackage D,
    True

/--
The P04 package projection is local and checked.  It only records that a package
term would provide the section-generation prerequisites; it does not construct
cohomology, prove vanishing, or prove separation.
-/
theorem sectionGenerationPrerequisites_of_cohomologyPackage
    {D : HodgeManifoldData.{u}}
    (P : CohomologyVanishingSectionGenerationPackage D) :
    SectionGenerationPrerequisites D := by
  exact ⟨P, True.intro⟩

/--
A P04 package also carries forward the P03 positive line-bundle bridge.  This
keeps the proof-tree dependency explicit for later public backfill.
-/
def positiveLineBundleBridge_of_cohomologyPackage
    {D : HodgeManifoldData.{u}}
    (P : CohomologyVanishingSectionGenerationPackage D) :
    PositiveLineBundleIntegralKahlerBridgePackage D :=
  P.positiveLineBundleBridge

/-- One node in the P04 cohomology-vanishing/section-generation proof tree. -/
structure CohomologyVanishingSectionProofTreeNode where
  nodeId : String
  parentId : String
  theoremTarget : String
  dependencySurface : String
  repoLocalStatus : String
  leafBudget : String
  blockerOrNextApi : String
  deriving Repr

/--
Public-backfill-ready proof tree for the cohomology vanishing and section
generation package.

Rows marked `checked_package_projection` are local projections out of abstract
package data. Rows marked `unchecked_formalization_debt` are classical analytic
or sheaf-cohomological obligations that still need native or pinned upstream
APIs before they can be counted as completed leaves.
-/
def cohomologyVanishingSectionGenerationProofTree :
    List CohomologyVanishingSectionProofTreeNode := [
  {
    nodeId := "KOD-P04",
    parentId := "KOD-ROOT",
    theoremTarget := "From a positive line-bundle bridge, build the cohomology-vanishing and section-generation package for high tensor powers.",
    dependencySurface := "PositiveLineBundleIntegralKahlerBridgePackage; CohomologyVanishingSectionGenerationPackage; CategoryTheory.Sheaf.H",
    repoLocalStatus := "package_frontier_checked_not_constructed",
    leafBudget := "unchecked package root; split into KOD-P04-L017 through KOD-P04-L023",
    blockerOrNextApi := "Needs coherent analytic sheaves, holomorphic line-bundle tensor powers, sheaf cohomology over compact complex manifolds, Kodaira/Serre vanishing, and finite-jet evaluation APIs."
  },
  {
    nodeId := "KOD-P04-L017",
    parentId := "KOD-P04",
    theoremTarget := "Pin the coherent analytic sheaf attached to each high tensor power of the positive line bundle.",
    dependencySurface := "CohomologyVanishingSectionGenerationPackage.coherentSheafForTensorPowersPinned",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 70",
    blockerOrNextApi := "Pin or implement coherent analytic sheaves associated to holomorphic line-bundle tensor powers."
  },
  {
    nodeId := "KOD-P04-L018",
    parentId := "KOD-P04",
    theoremTarget := "State the sheaf-cohomology objects for those tensor-power sheaves.",
    dependencySurface := "CohomologyVanishingSectionGenerationPackage.highTensorPowerCohomologyPinned; CategoryTheory.Sheaf.H",
    repoLocalStatus := "checked_import_surface_plus_unchecked_formalization_debt",
    leafBudget := "<= 70",
    blockerOrNextApi := "General sheaf cohomology imports check, but the analytic coherent sheaf instance and target site are not pinned."
  },
  {
    nodeId := "KOD-P04-L019",
    parentId := "KOD-P04",
    theoremTarget := "Prove Kodaira-type vanishing for positive high tensor powers in the required cohomological degrees.",
    dependencySurface := "CohomologyVanishingSectionGenerationPackage.kodairaVanishingForPositivePowers",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 90",
    blockerOrNextApi := "No repo-local or pinned upstream Kodaira vanishing theorem for compact complex manifolds is integrated."
  },
  {
    nodeId := "KOD-P04-L020",
    parentId := "KOD-P04",
    theoremTarget := "Derive finite-dimensionality of the relevant global holomorphic section spaces.",
    dependencySurface := "CohomologyVanishingSectionGenerationPackage.finiteDimensionalGlobalSections",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 70",
    blockerOrNextApi := "Needs finite-dimensionality theorem for global sections of coherent sheaves on compact complex manifolds or an algebraic comparison route."
  },
  {
    nodeId := "KOD-P04-L021",
    parentId := "KOD-P04",
    theoremTarget := "Pin finite-jet evaluation maps from global sections to local quotient or jet targets.",
    dependencySurface := "CohomologyVanishingSectionGenerationPackage.evaluationMapAtFiniteJetsPinned",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Pin local analytic stalk/jet/ideal-quotient APIs for evaluating sections at points and first-order tangent data."
  },
  {
    nodeId := "KOD-P04-L022",
    parentId := "KOD-P04",
    theoremTarget := "Use vanishing to prove finite-jet evaluation maps are surjective for sufficiently high tensor powers.",
    dependencySurface := "CohomologyVanishingSectionGenerationPackage.evaluationMapSurjectiveForHighPowers",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 90",
    blockerOrNextApi := "Needs exact-sequence cohomology, ideal sheaves for finite subschemes or analytic jets, and the vanishing theorem from KOD-P04-L019."
  },
  {
    nodeId := "KOD-P04-L023",
    parentId := "KOD-P04",
    theoremTarget := "Package global generation of high tensor powers as the input for later point/tangent separation.",
    dependencySurface := "CohomologyVanishingSectionGenerationPackage.globallyGeneratedForHighPowers; sectionGenerationPrerequisites_of_cohomologyPackage",
    repoLocalStatus := "checked_package_projection",
    leafBudget := "<= 20 checked",
    blockerOrNextApi := "Projection is checked, but it depends on an unconstructed cohomology-vanishing package and therefore is not theorem completion."
  }
]

/-- The P04 proof-tree package contains one root row and seven leaf rows. -/
theorem cohomologyVanishingSectionGenerationProofTree_length :
    cohomologyVanishingSectionGenerationProofTree.length = 8 :=
  rfl

/-! ## Public proof-tree package for S1-M-024-P05 -/

/--
P05 point/tangent separation package for the Kodaira proof tree.

The fields are still proof obligations.  They isolate the geometric step that
turns the P04 section-generation package into the two local conditions used by
the final Kodaira map: distinct points are separated by global sections, and
nonzero tangent directions are separated by first jets of global sections.
-/
structure PointTangentSeparationPackage
    (D : HodgeManifoldData.{u}) : Type (u + 1) where
  sectionGeneration : SectionGenerationPrerequisites D
  highPowerGlobalSectionsPinned : Prop
  finiteDimensionalSectionSpace : Prop
  pointEvaluationMapsPinned : Prop
  pointPairEvaluationSurjective : Prop
  separatesDistinctPoints : Prop
  tangentJetEvaluationMapsPinned : Prop
  tangentJetEvaluationSurjective : Prop
  separatesTangentVectors : Prop
  separationImpliesEmbeddingCriterion : Prop

/--
Checked projection: a P05 point/tangent package supplies the existing
`KodairaSectionSeparationPackage` frontier.  This is only a package projection;
it does not construct the global sections or prove either separation theorem.
-/
def kodairaSectionSeparationPackage_of_pointTangentSeparationPackage
    {D : HodgeManifoldData.{u}}
    (P : PointTangentSeparationPackage D) :
    KodairaSectionSeparationPackage D where
  amplePowerGlobalSectionsPinned := P.highPowerGlobalSectionsPinned
  finiteDimensionalSectionSpace := P.finiteDimensionalSectionSpace
  separatesPoints := P.separatesDistinctPoints
  separatesTangentVectors := P.separatesTangentVectors

/--
A P05 package carries the P04 section-generation prerequisite forward.  Keeping
this projection checked prevents the public proof tree from hiding its
dependency on cohomology vanishing and finite-jet generation.
-/
theorem sectionGenerationPrerequisites_of_pointTangentSeparationPackage
    {D : HodgeManifoldData.{u}}
    (P : PointTangentSeparationPackage D) :
    SectionGenerationPrerequisites D :=
  P.sectionGeneration

/--
If a P05 package is constructed, it supplies the full section-separation
frontier required by the global Kodaira proof package.
-/
theorem sectionSeparationFrontier_of_pointTangentSeparationPackage
    {D : HodgeManifoldData.{u}}
    (P : PointTangentSeparationPackage D) :
    Nonempty (KodairaSectionSeparationPackage D) :=
  ⟨kodairaSectionSeparationPackage_of_pointTangentSeparationPackage P⟩

/-- One node in the P05 point/tangent separation proof tree. -/
structure PointTangentSeparationProofTreeNode where
  nodeId : String
  parentId : String
  theoremTarget : String
  dependencySurface : String
  repoLocalStatus : String
  leafBudget : String
  blockerOrNextApi : String
  deriving Repr

/--
Public-backfill-ready proof tree for separating points and tangent vectors.

Rows marked `checked_package_projection` are local projections out of abstract
package data. Rows marked `unchecked_formalization_debt` are analytic or
sheaf-theoretic obligations that still need native or pinned upstream APIs
before they can be counted as completed leaves.
-/
def pointTangentSeparationProofTree :
    List PointTangentSeparationProofTreeNode := [
  {
    nodeId := "KOD-P05",
    parentId := "KOD-ROOT",
    theoremTarget := "Use high tensor-power global sections to separate distinct points and nonzero tangent vectors.",
    dependencySurface := "SectionGenerationPrerequisites; PointTangentSeparationPackage; KodairaSectionSeparationPackage",
    repoLocalStatus := "package_frontier_checked_not_constructed",
    leafBudget := "unchecked package root; split into KOD-P05-L024 through KOD-P05-L031",
    blockerOrNextApi := "Needs point evaluation maps, first-jet/tangent evaluation maps, surjectivity from P04 finite-jet generation, and a native embedding criterion for the complete linear system."
  },
  {
    nodeId := "KOD-P05-L024",
    parentId := "KOD-P05",
    theoremTarget := "Carry the P04 section-generation prerequisites into the point/tangent separation step.",
    dependencySurface := "PointTangentSeparationPackage.sectionGeneration; sectionGenerationPrerequisites_of_pointTangentSeparationPackage",
    repoLocalStatus := "checked_package_projection",
    leafBudget := "<= 20 checked",
    blockerOrNextApi := "Projection is checked, but it depends on an unconstructed P05 package and therefore is not theorem completion."
  },
  {
    nodeId := "KOD-P05-L025",
    parentId := "KOD-P05",
    theoremTarget := "Pin finite-dimensional global section spaces for the high tensor power used by the complete linear system.",
    dependencySurface := "PointTangentSeparationPackage.highPowerGlobalSectionsPinned; PointTangentSeparationPackage.finiteDimensionalSectionSpace",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 60",
    blockerOrNextApi := "Needs a concrete global-section vector-space API for high tensor powers of the positive line bundle."
  },
  {
    nodeId := "KOD-P05-L026",
    parentId := "KOD-P05",
    theoremTarget := "Pin point-evaluation maps at ordered pairs of distinct source points.",
    dependencySurface := "PointTangentSeparationPackage.pointEvaluationMapsPinned",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 70",
    blockerOrNextApi := "Needs point evaluation of holomorphic line-bundle sections and a selected representation of distinct point pairs."
  },
  {
    nodeId := "KOD-P05-L027",
    parentId := "KOD-P05",
    theoremTarget := "Use finite-jet generation to prove pairwise point-evaluation surjectivity.",
    dependencySurface := "PointTangentSeparationPackage.pointPairEvaluationSurjective; CohomologyVanishingSectionGenerationPackage.evaluationMapSurjectiveForHighPowers",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 90",
    blockerOrNextApi := "Needs the P04 evaluation-surjectivity theorem specialized to length-two point subschemes or analytic point pairs."
  },
  {
    nodeId := "KOD-P05-L028",
    parentId := "KOD-P05",
    theoremTarget := "Deduce that global sections separate distinct points.",
    dependencySurface := "PointTangentSeparationPackage.separatesDistinctPoints",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Needs a local nonvanishing/ratio argument that turns point-pair surjectivity into separation by one section or by the projective section tuple."
  },
  {
    nodeId := "KOD-P05-L029",
    parentId := "KOD-P05",
    theoremTarget := "Pin first-jet or tangent-evaluation maps for sections at each source point.",
    dependencySurface := "PointTangentSeparationPackage.tangentJetEvaluationMapsPinned",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Needs tangent spaces, first jets or maximal-ideal-square quotients, and section differentials for holomorphic line bundles."
  },
  {
    nodeId := "KOD-P05-L030",
    parentId := "KOD-P05",
    theoremTarget := "Use finite-jet generation to prove tangent-jet evaluation surjectivity and tangent-vector separation.",
    dependencySurface := "PointTangentSeparationPackage.tangentJetEvaluationSurjective; PointTangentSeparationPackage.separatesTangentVectors",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 90",
    blockerOrNextApi := "Needs the P04 finite-jet surjectivity theorem specialized to first-order tangent jets and a proof that nonzero tangent directions are detected."
  },
  {
    nodeId := "KOD-P05-L031",
    parentId := "KOD-P05",
    theoremTarget := "Export point and tangent separation into the existing Kodaira section-separation frontier.",
    dependencySurface := "kodairaSectionSeparationPackage_of_pointTangentSeparationPackage; sectionSeparationFrontier_of_pointTangentSeparationPackage",
    repoLocalStatus := "checked_package_projection",
    leafBudget := "<= 20 checked",
    blockerOrNextApi := "Projection is checked, but it depends on an unconstructed point/tangent separation package and therefore is not theorem completion."
  }
]

/-- The P05 proof-tree package contains one root row and eight leaf rows. -/
theorem pointTangentSeparationProofTree_length :
    pointTangentSeparationProofTree.length = 9 :=
  rfl

/-! ## Public proof-tree package for S1-M-024-P06 -/

/--
P06 projective-embedding construction package for the Kodaira proof tree.

The fields are still proof obligations.  They isolate the final geometric step:
choose a finite section basis, construct the complete-linear-system map to
complex projective space, prove well-definedness and holomorphicity, deduce
injectivity and immersion from P05 separation, and combine those conditions
with compactness to obtain the `ProjectiveEmbeddingData` used by the Stage1
statement boundary.
-/
structure ProjectiveEmbeddingConstructionPackage
    (D : HodgeManifoldData.{u}) : Type (u + 1) where
  pointTangentSeparation : PointTangentSeparationPackage D
  sectionSeparation : KodairaSectionSeparationPackage D
  completeLinearSystemPinned : Prop
  finiteCoordinateSectionsPinned : Prop
  basepointFreeFromSectionGeneration : Prop
  nonzeroSectionTupleAtEveryPoint : Prop
  complexProjectiveSpaceTargetPinned : Prop
  mapFromSectionTupleConstructed : Prop
  wellDefinedModuloScalarChoices : Prop
  independentOfBasisChoice : Prop
  holomorphicMapFromSections : Prop
  injectiveFromPointSeparation : Prop
  immersionFromTangentSeparation : Prop
  compactToClosedEmbeddingCriterionPinned : Prop
  closedEmbeddingFromInjectiveImmersion : Prop
  embeddingData : ProjectiveEmbeddingData D

/--
Checked projection: a P06 construction package supplies the existing
`KodairaProjectiveMapPackage` frontier.  This does not build a section basis or
prove any analytic embedding theorem; it only records the final package shape
that a later native or pinned formalization must satisfy.
-/
def kodairaProjectiveMapPackage_of_projectiveEmbeddingConstructionPackage
    {D : HodgeManifoldData.{u}}
    (P : ProjectiveEmbeddingConstructionPackage D) :
    KodairaProjectiveMapPackage D where
  complexProjectiveSpacePinned := P.complexProjectiveSpaceTargetPinned
  mapFromSectionsConstructed := P.mapFromSectionTupleConstructed
  holomorphicMapProved := P.holomorphicMapFromSections
  closedEmbeddingProved := P.closedEmbeddingFromInjectiveImmersion
  embeddingData := P.embeddingData

/--
A P06 package carries the P05 section-separation frontier forward.  Keeping
this projection checked makes the dependency on point and tangent separation
explicit in the public proof tree.
-/
def sectionSeparation_of_projectiveEmbeddingConstructionPackage
    {D : HodgeManifoldData.{u}}
    (P : ProjectiveEmbeddingConstructionPackage D) :
    KodairaSectionSeparationPackage D :=
  P.sectionSeparation

/--
If a P06 construction package is available, it supplies the exact local
projectivity conclusion used by the normalized Kodaira statement.
-/
theorem projective_of_projectiveEmbeddingConstructionPackage
    {D : HodgeManifoldData.{u}}
    (P : ProjectiveEmbeddingConstructionPackage D) :
    IsProjectiveManifold D :=
  ⟨P.embeddingData⟩

/--
If the earlier complex/Kahler and P06 projective construction packages are both
available, they assemble into the existing global proof-package frontier.
-/
theorem proofPackage_of_projectiveEmbeddingConstructionPackage
    {D : HodgeManifoldData.{u}}
    (K : KodairaComplexKahlerPackage D)
    (P : ProjectiveEmbeddingConstructionPackage D) :
    Nonempty (KodairaEmbeddingProofPackage D) :=
  ⟨{
    complexKahler := K
    sectionSeparation := P.sectionSeparation
    projectiveMap :=
      kodairaProjectiveMapPackage_of_projectiveEmbeddingConstructionPackage P
  }⟩

/-- One node in the P06 projective-embedding construction proof tree. -/
structure ProjectiveEmbeddingConstructionProofTreeNode where
  nodeId : String
  parentId : String
  theoremTarget : String
  dependencySurface : String
  repoLocalStatus : String
  leafBudget : String
  blockerOrNextApi : String
  deriving Repr

/--
Public-backfill-ready proof tree for constructing and proving the projective
embedding from the separated global sections.

Rows marked `checked_package_projection` are local projections out of abstract
package data. Rows marked `unchecked_formalization_debt` are analytic,
linear-system, or projective-space obligations that still need native or pinned
upstream APIs before they can be counted as completed leaves.
-/
def projectiveEmbeddingConstructionProofTree :
    List ProjectiveEmbeddingConstructionProofTreeNode := [
  {
    nodeId := "KOD-P06",
    parentId := "KOD-ROOT",
    theoremTarget := "Construct the complete-linear-system map to complex projective space and prove it is a holomorphic closed embedding.",
    dependencySurface := "PointTangentSeparationPackage; KodairaSectionSeparationPackage; ProjectiveEmbeddingConstructionPackage; ProjectiveEmbeddingData",
    repoLocalStatus := "package_frontier_checked_not_constructed",
    leafBudget := "unchecked package root; split into KOD-P06-L032 through KOD-P06-L041",
    blockerOrNextApi := "Needs finite global-section bases, complete linear systems, complex projective-space targets, holomorphic map construction from sections, and a closed-embedding criterion for compact complex manifolds."
  },
  {
    nodeId := "KOD-P06-L032",
    parentId := "KOD-P06",
    theoremTarget := "Carry the P05 point/tangent separation package and section-separation frontier into the projective-map step.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.pointTangentSeparation; ProjectiveEmbeddingConstructionPackage.sectionSeparation; sectionSeparation_of_projectiveEmbeddingConstructionPackage",
    repoLocalStatus := "checked_package_projection",
    leafBudget := "<= 20 checked",
    blockerOrNextApi := "Projection is checked, but it depends on an unconstructed P06 package and therefore is not theorem completion."
  },
  {
    nodeId := "KOD-P06-L033",
    parentId := "KOD-P06",
    theoremTarget := "Pin the complete linear system and a finite coordinate-section family for the high tensor power.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.completeLinearSystemPinned; ProjectiveEmbeddingConstructionPackage.finiteCoordinateSectionsPinned",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 70",
    blockerOrNextApi := "Needs a concrete finite-dimensional global-section vector space, basis/coordinate APIs, and the line-bundle tensor power selected by P04/P05."
  },
  {
    nodeId := "KOD-P06-L034",
    parentId := "KOD-P06",
    theoremTarget := "Prove basepoint freeness and the nonzero section tuple at every source point.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.basepointFreeFromSectionGeneration; ProjectiveEmbeddingConstructionPackage.nonzeroSectionTupleAtEveryPoint",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Needs global generation from P04 plus evaluation of the selected coordinate sections at each point."
  },
  {
    nodeId := "KOD-P06-L035",
    parentId := "KOD-P06",
    theoremTarget := "Pin the complex projective-space target associated to the finite section coordinate family.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.complexProjectiveSpaceTargetPinned; ProjectiveEmbeddingData.ambientIsProjectiveSpace",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 60",
    blockerOrNextApi := "Needs the chosen Lean API for finite-dimensional complex projective space and its topology/complex-manifold structure."
  },
  {
    nodeId := "KOD-P06-L036",
    parentId := "KOD-P06",
    theoremTarget := "Construct the map from the nonzero section tuple and prove scalar and basis-choice well-definedness.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.mapFromSectionTupleConstructed; ProjectiveEmbeddingConstructionPackage.wellDefinedModuloScalarChoices; ProjectiveEmbeddingConstructionPackage.independentOfBasisChoice",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Needs quotient/projectivization APIs for nonzero coordinate vectors and basis-change compatibility for complete linear systems."
  },
  {
    nodeId := "KOD-P06-L037",
    parentId := "KOD-P06",
    theoremTarget := "Prove that the constructed projective-space map is holomorphic.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.holomorphicMapFromSections; KodairaProjectiveMapPackage.holomorphicMapProved",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Needs holomorphicity of section coordinate functions and the projective-space chart criterion for holomorphic maps."
  },
  {
    nodeId := "KOD-P06-L038",
    parentId := "KOD-P06",
    theoremTarget := "Deduce injectivity of the projective map from point separation.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.injectiveFromPointSeparation; PointTangentSeparationPackage.separatesDistinctPoints",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Needs the ratio/coordinate argument turning separated point values into distinct projective points."
  },
  {
    nodeId := "KOD-P06-L039",
    parentId := "KOD-P06",
    theoremTarget := "Deduce immersion of the projective map from tangent-vector separation.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.immersionFromTangentSeparation; PointTangentSeparationPackage.separatesTangentVectors",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 80",
    blockerOrNextApi := "Needs differential of the projective section map and the tangent-space criterion detected by first jets."
  },
  {
    nodeId := "KOD-P06-L040",
    parentId := "KOD-P06",
    theoremTarget := "Combine compactness, injective immersion, and target separation/Hausdorffness into a closed embedding criterion.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.compactToClosedEmbeddingCriterionPinned; ProjectiveEmbeddingConstructionPackage.closedEmbeddingFromInjectiveImmersion",
    repoLocalStatus := "unchecked_formalization_debt",
    leafBudget := "<= 90",
    blockerOrNextApi := "Needs a native holomorphic closed-embedding predicate and a theorem that compact-source injective immersions into the selected projective target give embeddings in the required sense."
  },
  {
    nodeId := "KOD-P06-L041",
    parentId := "KOD-P06",
    theoremTarget := "Export the constructed closed embedding into `ProjectiveEmbeddingData`, `KodairaProjectiveMapPackage`, and the local projectivity conclusion.",
    dependencySurface := "ProjectiveEmbeddingConstructionPackage.embeddingData; kodairaProjectiveMapPackage_of_projectiveEmbeddingConstructionPackage; projective_of_projectiveEmbeddingConstructionPackage",
    repoLocalStatus := "checked_package_projection",
    leafBudget := "<= 25 checked",
    blockerOrNextApi := "Projection is checked, but it depends on an unconstructed projective-embedding construction package and therefore is not theorem completion."
  }
]

/-- The P06 proof-tree package contains one root row and ten leaf rows. -/
theorem projectiveEmbeddingConstructionProofTree_length :
    projectiveEmbeddingConstructionProofTree.length = 11 :=
  rfl

/-- M0387-level formalization package split for the Kodaira embedding frontier. -/
def formalizationPackageSplit : List String :=
  [ "complex-manifold package: compact complex analytic spaces/manifolds, holomorphic maps, and closed embeddings",
    "Kahler package: Kahler forms or metrics and the integral cohomology-class hypothesis",
    "positive-line-bundle package: Hermitian holomorphic line bundles whose curvature represents the integral Kahler class",
    "section-separation package: finite-dimensional spaces of global holomorphic sections of high tensor powers that separate points and tangent vectors",
    "projective-map package: construct the map to complex projective space from sections and prove it is a holomorphic closed embedding",
    "scheme/projectivity bridge package: relate the analytic embedding target to checked scheme-side closed-immersion/properness infrastructure when an algebraic target is selected" ]

/-- Search markers for the missing terminal theorem/API family. -/
def absentTerminalSearchTerms : List String :=
  [ "KodairaEmbedding",
    "Kodaira embedding",
    "Hodge manifold projective",
    "Kahler integral class",
    "positive line bundle very ample" ]

/-- Integration-ready statement-normalization notes for later public backfill. -/
def publicStatementNormalizationNotes : List String :=
  [ "Universe: one universe u; HodgeManifoldData.carrier : Type u; embedding ambient : Type u.",
    "Object: a compact complex Hodge manifold is represented by HodgeManifoldData with proposition-valued analytic predicates.",
    "Hypotheses: compactComplexManifold, kahlerManifold, and integralKahlerClass, combined by IsHodgeManifold.",
    "Conclusion: Nonempty (ProjectiveEmbeddingData D), i.e. finite-dimensional complex-projective ambient data plus a holomorphic closed embedding.",
    "Boundary: this is a statement-shape artifact only; it is not a proof of Kodaira embedding." ]

/-- Remaining theorem-internal leaves before this slot can be considered closed. -/
def theoremInternalChildLeaves : List String :=
  [ "S1-M-024-leaf-001 pin native compact complex manifold and holomorphic map APIs",
    "S1-M-024-leaf-002 pin Kahler form/metric and integral cohomology class APIs",
    "S1-M-024-leaf-003 pin positive Hermitian holomorphic line bundle and curvature-class bridge",
    "S1-M-024-leaf-004 formalize finite-dimensional global section spaces for high tensor powers",
    "S1-M-024-leaf-005 prove global sections separate points",
    "S1-M-024-leaf-006 prove global sections separate tangent vectors",
    "S1-M-024-leaf-007 construct the projective-space map from a basis of sections using the P06 complete-linear-system package",
    "S1-M-024-leaf-008 prove the constructed map is holomorphic, injective, immersive, and a closed embedding",
    "S1-M-024-leaf-009 pin/import/check any exact external Lean 4 proof or record a concrete integration blocker",
    "S1-M-024-leaf-010 replace the statement-shape wrapper by a repo-local wrapper or local proof body only after every package leaf has a <=100-step ledger" ]

/-- Current machine-proof debt classification for this theorem slot. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/-- Completion gate: anchor-only evidence cannot close this Stage1 item. -/
def repoLocalIntegrationDebtGate : String :=
  "not_completed_no_repo_local_integration_debt_retained"

#check HodgeManifoldData
#check ProjectiveEmbeddingData
#check NormalizedKodairaEmbeddingShape
#check StatementShape
#check statementShape_eq_normalizedKodairaEmbeddingShape
#check projective_of_embeddingData
#check statementShape_of_projective_embedding
#check KodairaComplexKahlerPackage
#check PositiveLineBundleIntegralKahlerBridgePackage
#check complexKahlerPackage_of_positiveLineBundleBridge
#check isHodgeManifold_of_positiveLineBundleBridge
#check KodairaSectionSeparationPackage
#check KodairaProjectiveMapPackage
#check KodairaEmbeddingProofPackage
#check projective_of_proofPackage
#check statementShape_of_proofPackages
#check SchemeProjectiveOverViaClosedImmersion
#check closedImmersion_isProper
#check projectiveOverViaClosedImmersion_isProper
#check projToSpecZero_isProper
#check ExternalLeanAnchorAudit
#check RepoLocalIntegrationDebtGate
#check repoLocalIntegrationDebtGate_of_no_external_anchor
#check RepoLocalClosureRoute
#check P08RepoLocalClosureRecord
#check p08ValidationCommand
#check P08CompletionGate
#check p08CurrentClosureRecord
#check no_p08_completion_without_machine_closure
#check p08_current_not_completed
#check p08RepoLocalWrapperPinPlan
#check ExternalLeanAnchorAuditRow
#check externalLeanAnchorAuditDate
#check externalLeanAnchorAuditRows
#check externalLeanAnchorAuditRows_length
#check externalLeanAnchorAuditConclusion
#check KodairaObjectModelAuditRow
#check objectModelAuditRevision
#check kodairaObjectModelAuditTable
#check kodairaObjectModelAuditTable_length
#check PositiveLineBundleBridgeProofTreeNode
#check positiveLineBundleBridgeProofTree
#check positiveLineBundleBridgeProofTree_length
#check CohomologyVanishingSectionGenerationPackage
#check SectionGenerationPrerequisites
#check sectionGenerationPrerequisites_of_cohomologyPackage
#check positiveLineBundleBridge_of_cohomologyPackage
#check CohomologyVanishingSectionProofTreeNode
#check cohomologyVanishingSectionGenerationProofTree
#check cohomologyVanishingSectionGenerationProofTree_length
#check PointTangentSeparationPackage
#check kodairaSectionSeparationPackage_of_pointTangentSeparationPackage
#check sectionGenerationPrerequisites_of_pointTangentSeparationPackage
#check sectionSeparationFrontier_of_pointTangentSeparationPackage
#check PointTangentSeparationProofTreeNode
#check pointTangentSeparationProofTree
#check pointTangentSeparationProofTree_length
#check ProjectiveEmbeddingConstructionPackage
#check kodairaProjectiveMapPackage_of_projectiveEmbeddingConstructionPackage
#check sectionSeparation_of_projectiveEmbeddingConstructionPackage
#check projective_of_projectiveEmbeddingConstructionPackage
#check proofPackage_of_projectiveEmbeddingConstructionPackage
#check ProjectiveEmbeddingConstructionProofTreeNode
#check projectiveEmbeddingConstructionProofTree
#check projectiveEmbeddingConstructionProofTree_length
#check MDifferentiable.isLocallyConstant
#check MDifferentiable.exists_eq_const_of_compactSpace
#check CategoryTheory.Sheaf.H
#check CategoryTheory.Sheaf.cohomologyPresheaf
#check CategoryTheory.Pseudofunctor.DescentData
#check AlgebraicGeometry.IsZariskiLocalAtTarget.descendsAlong
#check formalizationPackageSplit
#check theoremInternalChildLeaves
#check KaehlerDifferential
#check IsRiemannianManifold

end AwesomeTheorems.Stage1.S1_M_024
