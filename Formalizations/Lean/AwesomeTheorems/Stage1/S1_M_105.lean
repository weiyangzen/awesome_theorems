import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.DirectSum.Module
import Mathlib.LinearAlgebra.DFinsupp

/-!
# S1-M-105 / THM-M-0545: Hodge decomposition theorem

This Stage1 artifact records a Lean 4 statement-shape boundary for the
classical Hodge decomposition of differential forms/cohomology.  The pinned
mathlib snapshot has useful linear-algebra infrastructure for internal direct
sums, plus separate manifold, differential-form, harmonic-function, and
cohomology APIs, but no terminal theorem for the Hodge decomposition of compact
Kähler manifolds was found in the local audit.

The declarations below are therefore deliberately parameterized.  They freeze
the expected direct-sum conclusion without asserting that the analytic Hodge
package has already been constructed in mathlib.
-/

noncomputable section

namespace AwesomeTheorems.Stage1.S1_M_105

universe u v w

/--
Statement-normalization note for THM-M-0545.

The intended target is the analytic Hodge decomposition theorem for compact
Kähler manifolds, stated for differential forms/cohomology over `ℂ`.  The
algebraic `KaehlerDifferential` API is a useful neighboring mathlib namespace,
but it is not the theorem target for this Stage1 slot.
-/
def statementNormalizationNote : String :=
  "THM-M-0545 targets analytic Hodge decomposition for compact Kähler " ++
    "manifolds and differential forms/cohomology over ℂ; it is not the " ++
    "algebraic KaehlerDifferential theory."

/-- Positive scope terms for the normalized analytic Hodge-decomposition target. -/
def intendedAnalyticScope : List String := [
  "compact Kähler manifold",
  "smooth differential forms",
  "complex de Rham/Dolbeault cohomology",
  "Hodge star and formal adjoint",
  "Hodge Laplacian and harmonic forms",
  "direct-sum decomposition by bidegree"
]

/-- Nearby APIs that should not be mistaken for the terminal theorem statement. -/
def excludedStatementScope : List String := [
  "algebraic KaehlerDifferential alone",
  "module of relative differentials for commutative algebras",
  "exterior derivative infrastructure alone",
  "harmonic functions without harmonic differential forms"
]

/-- Bidegrees `(p,q)` contributing to total cohomological degree `n`. -/
abbrev HodgeBidegree (n : Nat) : Type :=
  {pq : Nat × Nat // pq.1 + pq.2 = n}

/--
Abstract data needed to state a Hodge decomposition theorem.

`Cohomology n` is intended to model complex cohomology in degree `n`, and
`hodgeSummand n p q` is intended to model the `H^{p,q}` summand.  The harmonic
form fields keep the analytic boundary visible without pretending that mathlib
currently supplies bundled Hodge-star/Laplacian/harmonic-form machinery for the
full theorem.
-/
structure HodgeDecompositionPackage where
  Space : Type u
  Cohomology : Nat → Type v
  [cohomologyAdd : ∀ n, AddCommGroup (Cohomology n)]
  [cohomologyModule : ∀ n, Module ℂ (Cohomology n)]
  hodgeSummand : ∀ n _p _q : Nat, Submodule ℂ (Cohomology n)
  HarmonicForm : Nat → Type w
  harmonicClass : ∀ n, HarmonicForm n → Cohomology n
  isHarmonic : ∀ n, HarmonicForm n → Prop
  isClosedForm : ∀ n, HarmonicForm n → Prop
  isExactForm : ∀ n, HarmonicForm n → Prop

attribute [instance] HodgeDecompositionPackage.cohomologyAdd
attribute [instance] HodgeDecompositionPackage.cohomologyModule

namespace HodgeDecompositionPackage

variable (D : HodgeDecompositionPackage.{u, v, w})

/-- The Hodge summand selected by a total-degree-indexed bidegree. -/
def piece (n : Nat) (pq : HodgeBidegree n) : Submodule ℂ (D.Cohomology n) :=
  D.hodgeSummand n pq.1.1 pq.1.2

/--
Internal direct-sum conclusion in fixed degree: the Hodge summands are
independent and span all of `H^n`.
-/
def DirectSumConclusion : Prop :=
  ∀ n : Nat,
    iSupIndep (fun pq : HodgeBidegree n => D.piece n pq) ∧
      (iSup (fun pq : HodgeBidegree n => D.piece n pq) = ⊤)

/--
Canonical external direct-sum map attached to the internal Hodge summands in a
fixed degree.

This is the map that an eventual `DirectSum`/`DFinsupp`-facing public theorem
would turn into a linear equivalence.  It is kept derived from the internal
submodule family so the Stage1 surface does not force a premature bundled
external direct-sum statement before the analytic APIs are available.
-/
def canonicalExternalDirectSumMap (n : Nat) :
    (Π₀ pq : HodgeBidegree n, D.piece n pq) →ₗ[ℂ] D.Cohomology n :=
  DFinsupp.lsum ℕ fun pq => (D.piece n pq).subtype

/--
External direct-sum-equivalence boundary, stated as bijectivity of the canonical
external direct-sum map.
-/
def ExternalDirectSumEquivalenceConclusion : Prop :=
  ∀ n : Nat, Function.Bijective (D.canonicalExternalDirectSumMap n)

/--
Surface decision for `S1-M-105-public-002`.

The recommended final public boundary keeps the internal submodule direct-sum
encoding as canonical, and exposes the external `DirectSum`/`DFinsupp`
equivalence as a derived bridge once the analytic package is supplied.
-/
def directSumSurfaceDecision : String :=
  "Keep the internal submodule direct-sum encoding as the canonical Stage1 " ++
    "surface; expose the external DirectSum/DFinsupp equivalence as a derived " ++
    "bridge via the canonical summation map."

/--
Analytic representative boundary: every cohomology class has a closed harmonic
representative, and exact harmonic representatives are the zero class.

This is not a replacement for the elliptic-regularity proof of Hodge theory; it
is a precise placeholder for the analytic package that must later be supplied
by mathlib, a pinned upstream project, or a local proof body.
-/
def HarmonicRepresentativeConclusion : Prop :=
  ∀ n : Nat,
    (∀ x : D.Cohomology n,
      ∃ η : D.HarmonicForm n, D.isHarmonic n η ∧ D.isClosedForm n η ∧ D.harmonicClass n η = x) ∧
      (∀ η : D.HarmonicForm n,
        D.isHarmonic n η → D.isExactForm n η → D.harmonicClass n η = 0)

/--
Stage1 normalized statement shape: an analytic harmonic-representative package
and the direct-sum decomposition by bidegree.
-/
def StatementShape : Prop :=
  D.HarmonicRepresentativeConclusion ∧ D.DirectSumConclusion

/-- The bidegree proof stored in a `HodgeBidegree`. -/
theorem bidegree_total (n : Nat) (pq : HodgeBidegree n) :
    pq.1.1 + pq.1.2 = n :=
  pq.2

/-- Low-risk wrapper: a supplied harmonic/direct-sum package closes the shape. -/
theorem statementShape_of_conclusions
    (hHarmonic : D.HarmonicRepresentativeConclusion)
    (hDirect : D.DirectSumConclusion) :
    D.StatementShape :=
  ⟨hHarmonic, hDirect⟩

/--
The internal submodule direct-sum conclusion supplies the canonical external
direct-sum map as a bijection.
-/
theorem externalDirectSumEquivalence_of_internal
    (hDirect : D.DirectSumConclusion) :
    D.ExternalDirectSumEquivalenceConclusion := by
  intro n
  exact ⟨(hDirect n).1.dfinsupp_lsum_injective, by
    rw [canonicalExternalDirectSumMap, ← LinearMap.range_eq_top,
      ← Submodule.iSup_eq_range_dfinsupp_lsum]
    exact (hDirect n).2⟩

end HodgeDecompositionPackage

/-- Stage1 statement-shape candidate for the theorem slot. -/
def StatementShape : Prop :=
  ∀ D : HodgeDecompositionPackage.{u, v, w}, D.StatementShape

/-- Low-risk introduction theorem for the normalized statement boundary. -/
theorem StatementShapeFromPackage
    (h : ∀ D : HodgeDecompositionPackage.{u, v, w}, D.StatementShape) :
    StatementShape.{u, v, w} :=
  h

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Complex",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.Analysis.Calculus.DifferentialForm.VectorField",
  "Mathlib.Analysis.InnerProductSpace.Harmonic.Basic",
  "Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Cech",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.MayerVietoris",
  "Mathlib.RingTheory.Kaehler.Basic"
]

/-- Local mathlib revision used for the public audit-table backfill. -/
def mathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
One row in the Stage1 public mathlib audit table for THM-M-0545.

The fields are intentionally strings: this table is an integration-ready audit
surface for the public blueprint, not an assertion that these modules provide a
terminal Hodge-decomposition theorem.
-/
structure MathlibAuditRow where
  requestedName : String
  moduleName : String
  presentAtRevision : String
  anchorNames : List String
  relevance : String
  terminalGap : String
deriving Repr

/-- Public backfill payload for `S1-M-105-public-003`. -/
def publicMathlibAuditTable : List MathlibAuditRow := [
  {
    requestedName := "DifferentialForm.Basic"
    moduleName := "Mathlib.Analysis.Calculus.DifferentialForm.Basic"
    presentAtRevision := mathlibAuditRevision
    anchorNames := [
      "extDeriv",
      "extDerivWithin",
      "extDeriv_extDeriv",
      "extDerivWithin_extDerivWithin_eqOn"
    ]
    relevance :=
      "Exterior derivative infrastructure for unbundled differential forms on normed spaces; " ++
        "contains the checked `d^2 = 0` substrate."
    terminalGap :=
      "The module TODO explicitly says bundled smooth forms on manifolds are not defined yet; " ++
        "it does not provide Hodge star, formal adjoint, Hodge Laplacian, harmonic forms, " ++
        "or analytic Hodge decomposition."
  },
  {
    requestedName := "Harmonic.Basic"
    moduleName := "Mathlib.Analysis.InnerProductSpace.Harmonic.Basic"
    presentAtRevision := mathlibAuditRevision
    anchorNames := [
      "InnerProductSpace.HarmonicAt",
      "InnerProductSpace.HarmonicOnNhd",
      "InnerProductSpace.harmonicAt_const",
      "InnerProductSpace.harmonicOnNhd_const"
    ]
    relevance :=
      "Harmonic-function API on real finite-dimensional inner-product spaces, using the " ++
        "scalar Laplacian."
    terminalGap :=
      "This is about harmonic functions, not harmonic differential forms on compact " ++
        "Riemannian or Kähler manifolds; no Hodge theorem or harmonic representative theorem."
  },
  {
    requestedName := "Projection.FiniteDimensional"
    moduleName := "Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional"
    presentAtRevision := mathlibAuditRevision
    anchorNames := [
      "Submodule.finrank_add_finrank_orthogonal",
      "OrthogonalFamily.isInternal_iff_of_isComplete",
      "OrthogonalFamily.sum_projection_of_mem_iSup",
      "OrthogonalFamily.decomposition"
    ]
    relevance :=
      "Finite-dimensional orthogonal projection and internal decomposition infrastructure."
    terminalGap :=
      "Useful linear algebra for decompositions, but it is not an analytic elliptic/Hodge " ++
        "package and has no compact Kähler manifold or harmonic-form cohomology statement."
  },
  {
    requestedName := "Geometry.Manifold.Complex"
    moduleName := "Mathlib.Geometry.Manifold.Complex"
    presentAtRevision := mathlibAuditRevision
    anchorNames := [
      "Complex.norm_eventually_eq_of_mdifferentiableAt_of_isLocalMax",
      "MDifferentiableOn.apply_eq_of_isPreconnected_isCompact_isOpen",
      "MDifferentiable.exists_eq_const_of_compactSpace"
    ]
    relevance :=
      "Complex-manifold holomorphic-function infrastructure and maximum-modulus consequences."
    terminalGap :=
      "The file describes future development for holomorphic vector bundles and sheaves; it " ++
        "does not define compact Kähler manifolds, Dolbeault cohomology, or Hodge decomposition."
  },
  {
    requestedName := "Geometry.Manifold.Riemannian.Basic"
    moduleName := "Mathlib.Geometry.Manifold.Riemannian.Basic"
    presentAtRevision := mathlibAuditRevision
    anchorNames := [
      "IsRiemannianManifold",
      "riemannianMetricVectorSpace",
      "IsRiemannianManifold.out",
      "EMetricSpace.ofRiemannianMetric"
    ]
    relevance :=
      "Riemannian manifold class, tangent-bundle metric infrastructure, and Riemannian distance."
    terminalGap :=
      "Provides the Riemannian substrate, but no Hodge star on forms, codifferential, " ++
        "Hodge Laplacian, harmonic form theory, or Kähler-specific decomposition theorem."
  },
  {
    requestedName := "SheafCohomology.Basic"
    moduleName := "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic"
    presentAtRevision := mathlibAuditRevision
    anchorNames := [
      "CategoryTheory.Sheaf.H",
      "CategoryTheory.Sheaf.cohomologyFunctor",
      "CategoryTheory.Sheaf.cohomologyPresheaf",
      "CategoryTheory.Sheaf.H'"
    ]
    relevance :=
      "Abelian sheaf cohomology via Ext groups on a site."
    terminalGap :=
      "Sheaf cohomology is adjacent to Hodge theory, but this module does not connect " ++
        "to smooth forms, de Rham or Dolbeault complexes, harmonic representatives, " ++
        "or compact Kähler Hodge decomposition."
  },
  {
    requestedName := "RingTheory.Kaehler.Basic"
    moduleName := "Mathlib.RingTheory.Kaehler.Basic"
    presentAtRevision := mathlibAuditRevision
    anchorNames := [
      "KaehlerDifferential",
      "KaehlerDifferential.D",
      "KaehlerDifferential.linearMapEquivDerivation",
      "KaehlerDifferential.exact_mapBaseChange_map"
    ]
    relevance :=
      "Algebraic Kähler differentials for commutative algebras."
    terminalGap :=
      "This is explicitly the neighboring algebraic `KaehlerDifferential` theory, not the " ++
        "analytic Kähler-manifold/Hodge-decomposition target for THM-M-0545."
  }
]

/-- Machine-check that the public audit payload has exactly the requested seven rows. -/
theorem publicMathlibAuditTable_length : publicMathlibAuditTable.length = 7 :=
  rfl

/-- Machine-check that the public audit payload covers the requested short module names. -/
theorem publicMathlibAuditTable_requestedNames :
    publicMathlibAuditTable.map MathlibAuditRow.requestedName = [
      "DifferentialForm.Basic",
      "Harmonic.Basic",
      "Projection.FiniteDimensional",
      "Geometry.Manifold.Complex",
      "Geometry.Manifold.Riemannian.Basic",
      "SheafCohomology.Basic",
      "RingTheory.Kaehler.Basic"
    ] :=
  rfl

/--
One concrete missing-API child task for the analytic compact-Kähler Hodge
decomposition target.

These rows are public-backfill payload, not assertions that the corresponding
analytic API exists in the current repo-local Lean closure.
-/
structure MissingApiChildTask where
  childId : String
  title : String
  dependsOn : List String
  existingAnchors : List String
  repoLocalGap : String
  acceptanceGate : String
  debtClass : String
deriving Repr

/-- Public backfill payload for `S1-M-105-public-004`. -/
def missingApiChildTasks : List MissingApiChildTask := [
  {
    childId := "S1-M-105-API-001"
    title := "compact Kähler manifold structure"
    dependsOn := [
      "Mathlib.Geometry.Manifold.Complex",
      "Mathlib.Geometry.Manifold.Riemannian.Basic"
    ]
    existingAnchors := [
      "IsRiemannianManifold",
      "Complex manifold model-with-corners infrastructure"
    ]
    repoLocalGap :=
      "No bundled compact Kähler manifold class tying complex structure, Riemannian " ++
        "metric, Hermitian compatibility, closed Kähler form, and compactness together."
    acceptanceGate :=
      "Provide or import a checked Lean structure/class for compact Kähler manifolds " ++
        "with projections usable by the later form, star, Laplacian, and cohomology APIs."
    debtClass := "formalization_debt"
  },
  {
    childId := "S1-M-105-API-002"
    title := "smooth differential forms on manifolds"
    dependsOn := [
      "S1-M-105-API-001",
      "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
      "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection"
    ]
    existingAnchors := [
      "extDeriv",
      "extDeriv_extDeriv"
    ]
    repoLocalGap :=
      "Current audited exterior-derivative substrate is for unbundled differential " ++
        "forms on normed spaces; the manifold-level bundled smooth form complex is missing."
    acceptanceGate :=
      "Provide checked bundled smooth k-forms on manifolds, exterior derivative, pullback " ++
        "where needed, wedge/product structure, and `d^2 = 0` in the manifold setting."
    debtClass := "formalization_debt"
  },
  {
    childId := "S1-M-105-API-003"
    title := "Hodge star"
    dependsOn := [
      "S1-M-105-API-001",
      "S1-M-105-API-002"
    ]
    existingAnchors := [
      "Mathlib.Geometry.Manifold.Riemannian.Basic",
      "Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional"
    ]
    repoLocalGap :=
      "No Hodge-star operator on smooth differential forms over oriented Riemannian " ++
        "or compact Kähler manifolds is available in the checked local artifact."
    acceptanceGate :=
      "Provide checked Hodge-star definitions and core identities on smooth forms, " ++
        "including degree behavior and inner-product/volume-form compatibility."
    debtClass := "formalization_debt"
  },
  {
    childId := "S1-M-105-API-004"
    title := "formal adjoint and codifferential"
    dependsOn := [
      "S1-M-105-API-002",
      "S1-M-105-API-003"
    ]
    existingAnchors := [
      "Hodge-star gap from S1-M-105-API-003"
    ]
    repoLocalGap :=
      "No checked formal adjoint of exterior derivative, codifferential, or integration " ++
        "by parts package for smooth forms on compact manifolds is present."
    acceptanceGate :=
      "Provide checked `d†`/codifferential definitions and adjointness theorem against " ++
        "the L2 inner product on compact oriented Riemannian/Kähler manifolds."
    debtClass := "formalization_debt"
  },
  {
    childId := "S1-M-105-API-005"
    title := "Hodge Laplacian"
    dependsOn := [
      "S1-M-105-API-002",
      "S1-M-105-API-004"
    ]
    existingAnchors := [
      "InnerProductSpace.HarmonicAt",
      "InnerProductSpace.HarmonicOnNhd"
    ]
    repoLocalGap :=
      "The audited harmonic API is scalar harmonic-function infrastructure; no Hodge " ++
        "Laplacian on differential forms is available."
    acceptanceGate :=
      "Provide checked `Δ = d d† + d† d` on smooth forms, basic self-adjointness and " ++
        "nonnegativity facts, and the kernel predicate needed for harmonic forms."
    debtClass := "formalization_debt"
  },
  {
    childId := "S1-M-105-API-006"
    title := "harmonic forms"
    dependsOn := [
      "S1-M-105-API-005"
    ]
    existingAnchors := [
      "InnerProductSpace.HarmonicAt",
      "InnerProductSpace.HarmonicOnNhd"
    ]
    repoLocalGap :=
      "No checked type/submodule of harmonic differential forms, harmonic representative " ++
        "map, or exact-harmonic zero-class theorem is present."
    acceptanceGate :=
      "Provide checked harmonic-form definitions and theorems connecting harmonicity, " ++
        "closedness, exactness, and cohomology-class representatives."
    debtClass := "formalization_debt"
  },
  {
    childId := "S1-M-105-API-007"
    title := "de Rham and Dolbeault cohomology"
    dependsOn := [
      "S1-M-105-API-001",
      "S1-M-105-API-002"
    ]
    existingAnchors := [
      "CategoryTheory.Sheaf.H",
      "CategoryTheory.Sheaf.cohomologyFunctor"
    ]
    repoLocalGap :=
      "Sheaf cohomology is present only as adjacent category-theoretic infrastructure; " ++
        "there is no checked de Rham complex, Dolbeault complex, or cohomology API tied to forms."
    acceptanceGate :=
      "Provide checked de Rham and Dolbeault complexes/cohomology groups with degree and " ++
        "bidegree indexing compatible with the Hodge summands."
    debtClass := "formalization_debt"
  },
  {
    childId := "S1-M-105-API-008"
    title := "comparison maps and Hodge decomposition bridge"
    dependsOn := [
      "S1-M-105-API-006",
      "S1-M-105-API-007"
    ]
    existingAnchors := [
      "HodgeDecompositionPackage.harmonicClass",
      "HodgeDecompositionPackage.DirectSumConclusion",
      "HodgeDecompositionPackage.externalDirectSumEquivalence_of_internal"
    ]
    repoLocalGap :=
      "The Stage1 artifact has only an abstract statement-shape package; no checked maps " ++
        "identify harmonic representatives, de Rham classes, Dolbeault classes, and Hodge summands."
    acceptanceGate :=
      "Provide checked comparison maps and the terminal theorem that harmonic representatives " ++
        "induce the fixed-degree direct-sum decomposition by bidegree."
    debtClass := "formalization_debt"
  }
]

/-- Machine-check that the missing-API split has the eight requested child rows. -/
theorem missingApiChildTasks_length : missingApiChildTasks.length = 8 :=
  rfl

/-- Machine-check that the split covers the requested missing API titles in order. -/
theorem missingApiChildTasks_titles :
    missingApiChildTasks.map MissingApiChildTask.title = [
      "compact Kähler manifold structure",
      "smooth differential forms on manifolds",
      "Hodge star",
      "formal adjoint and codifferential",
      "Hodge Laplacian",
      "harmonic forms",
      "de Rham and Dolbeault cohomology",
      "comparison maps and Hodge decomposition bridge"
    ] :=
  rfl

/-- Search terms that did not locate a terminal Hodge-decomposition theorem. -/
def absentTerminalSearchTerms : List String := [
  "HodgeDecomposition",
  "Hodge decomposition",
  "Hodge theorem",
  "HarmonicForm",
  "HodgeLaplacian",
  "Dolbeault",
  "deRhamCohomology",
  "KahlerManifold",
  "Kaehler decomposition",
  "compact Kähler"
]

/--
One primary-source Lean 4 search row for the external-anchor audit.

The rows below record source-level findings only.  A row is not a completion
claim unless `integrationGate` says that the proof body is pinned and locally
checked in this repository.
-/
structure ExternalLeanAuditRow where
  repositoryUrl : String
  commit : String
  sourceFiles : List String
  searchedTerms : List String
  theoremNames : List String
  leanVersion : String
  mathlibVersion : String
  sorryAxiomStatus : String
  finding : String
  integrationGate : String
deriving Repr

/-- Public backfill payload for `S1-M-105-public-005`. -/
def externalLeanPrimarySourceAudit : List ExternalLeanAuditRow := [
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := mathlibAuditRevision
    sourceFiles := [
      "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
      "Mathlib.Analysis.InnerProductSpace.Harmonic.Basic",
      "Mathlib.Geometry.Manifold.Complex",
      "Mathlib.Geometry.Manifold.Riemannian.Basic",
      "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
      "Mathlib.RingTheory.Kaehler.Basic"
    ]
    searchedTerms := absentTerminalSearchTerms
    theoremNames := [
      "extDeriv_extDeriv",
      "InnerProductSpace.HarmonicAt",
      "InnerProductSpace.HarmonicOnNhd",
      "CategoryTheory.Sheaf.H",
      "KaehlerDifferential"
    ]
    leanVersion := "leanprover/lean4:v4.29.0"
    mathlibVersion := mathlibAuditRevision
    sorryAxiomStatus :=
      "No proof-placeholder or local assumed-constant hit was found in the searched modules; " ++
        "the listed declarations are adjacent infrastructure, not a terminal Hodge theorem."
    finding :=
      "No terminal Lean 4 theorem for analytic Hodge decomposition, HarmonicForm, " ++
        "HodgeLaplacian, Dolbeault cohomology, deRhamCohomology, or KaehlerManifold was found."
    integrationGate :=
      "not_repo_local_closed: mathlib is pinned locally, but this row has no terminal theorem to wrap."
  },
  {
    repositoryUrl := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems"
    commit := "540da94826f70f3edf4d4fc66ce6cda20e903f61"
    sourceFiles := [
      "Problems/Hodge/Millennium.lean",
      "Problems/Hodge/Variety.lean"
    ]
    searchedTerms := absentTerminalSearchTerms
    theoremNames := [
      "MillenniumHodge.HodgeConjecture",
      "VarietyDefinition.HodgeData.hodgeSubspace",
      "VarietyDefinition.HodgeData.hodgeFiltration",
      "VarietyDefinition.HodgeData.hodgeClass",
      "VarietyDefinition.HodgeData.hodgeClass_le_hodgeClassFiltration"
    ]
    leanVersion := "leanprover/lean4:v4.26.0"
    mathlibVersion := "2df2f0150c275ad53cb3c90f7c98ec15a56a1a67"
    sorryAxiomStatus :=
      "No actual proof-placeholder or assumed-constant declaration was found in the two Hodge files; " ++
        "Hodge decomposition is parameterized as HodgeData, not proved."
    finding :=
      "Primary source explicitly says the Hodge decomposition isomorphism and harmonic-form " ++
        "interpretation are not formalized as theorems there."
    integrationGate :=
      "not_repo_local_closed: this is a Hodge-conjecture scaffold, not a completed proof of THM-M-0545."
  },
  {
    repositoryUrl := "https://github.com/urkud/DeRhamCohomology"
    commit := "a58bf456b75d152770a5336321562b6aada200f4"
    sourceFiles := [
      "DeRhamCohomology/DifferentialForm.lean",
      "DeRhamCohomology/Manifold/DifferentialForm.lean",
      "DeRhamCohomology/Manifold/VectorBundle/Alternating.lean"
    ]
    searchedTerms := absentTerminalSearchTerms
    theoremNames := [
      "ederiv",
      "ederiv_ederiv",
      "DifferentialForm.pullback",
      "DifferentialForm.wedge_product",
      "DifferentialForm.mederiv",
      "DifferentialForm.mederivWithin_univ"
    ]
    leanVersion := "leanprover/lean4:v4.21.0-rc2"
    mathlibVersion := "b3c38642e52a78f11043e0417eea4501a8907a41"
    sorryAxiomStatus :=
      "Contains unresolved proof placeholders in differential-form and vector-bundle files; no terminal " ++
        "Hodge decomposition theorem or axiom-free closure is available for this slot."
    finding :=
      "Useful de Rham/differential-form infrastructure was found, but no HodgeDecomposition, " ++
        "Hodge theorem, HarmonicForm, HodgeLaplacian, Dolbeault, or KaehlerManifold theorem."
    integrationGate :=
      "integration_blocker: contains sorries and targets an older Lean/mathlib line; not pin-ready."
  }
]

/-- Machine-check that the external primary-source audit has the three recorded rows. -/
theorem externalLeanPrimarySourceAudit_length :
    externalLeanPrimarySourceAudit.length = 3 :=
  rfl

/-- Machine-check that every recorded external row used the same requested search-term list. -/
theorem externalLeanPrimarySourceAudit_terms :
    externalLeanPrimarySourceAudit.map ExternalLeanAuditRow.searchedTerms = [
      absentTerminalSearchTerms,
      absentTerminalSearchTerms,
      absentTerminalSearchTerms
    ] :=
  rfl

/--
Repo-local integration decision for an external Lean 4 audit row.

This is the checked C006 gate: an external row may support completion only when
it supplies a completed theorem that has been pinned/imported/checked in this
repository, or when a concrete blocker is recorded and the theorem remains open.
-/
structure ExternalProofIntegrationGateRow where
  sourceLabel : String
  completedExternalProofFound : Bool
  repoLocalAction : String
  concreteBlocker : String
  anchorOnlyCompletionAllowed : Bool
  completedStateAllowed : Bool
deriving Repr

/-- Public backfill payload for `S1-M-105-public-006`. -/
def externalProofIntegrationGateRows : List ExternalProofIntegrationGateRow := [
  {
    sourceLabel := "pinned local mathlib"
    completedExternalProofFound := false
    repoLocalAction :=
      "No new pin/import/check action: mathlib is already pinned locally, but no terminal " ++
        "analytic compact-Kähler Hodge-decomposition theorem was found to wrap."
    concreteBlocker :=
      "Missing theorem/API surface: compact Kähler manifolds, manifold-level smooth forms, " ++
        "Hodge star, formal adjoint, Hodge Laplacian, harmonic forms, de Rham/Dolbeault " ++
        "cohomology, and comparison maps."
    anchorOnlyCompletionAllowed := false
    completedStateAllowed := false
  },
  {
    sourceLabel := "lean-dojo/LeanMillenniumPrizeProblems"
    completedExternalProofFound := false
    repoLocalAction :=
      "Do not pin as a proof dependency for THM-M-0545: the checked Hodge files provide " ++
        "a Hodge-conjecture scaffold with parameterized Hodge data, not a theorem proving " ++
        "the analytic Hodge decomposition."
    concreteBlocker :=
      "No terminal theorem for the Hodge decomposition isomorphism or harmonic-form " ++
        "interpretation; also targets Lean 4.26/mathlib 2df2f015 while this repo uses " ++
        "Lean 4.29/mathlib 8a178386."
    anchorOnlyCompletionAllowed := false
    completedStateAllowed := false
  },
  {
    sourceLabel := "urkud/DeRhamCohomology"
    completedExternalProofFound := false
    repoLocalAction :=
      "Do not pin as a proof dependency for THM-M-0545: the project is useful adjacent " ++
        "de Rham/differential-form infrastructure, not a completed Hodge-decomposition proof."
    concreteBlocker :=
      "No terminal Hodge theorem was found, unresolved proof placeholders are present in " ++
        "the audited source files, and the project targets Lean 4.21-rc2/mathlib b3c38642."
    anchorOnlyCompletionAllowed := false
    completedStateAllowed := false
  }
]

/-- Machine-check that the C006 integration gate covers the three external audit rows. -/
theorem externalProofIntegrationGateRows_length :
    externalProofIntegrationGateRows.length = externalLeanPrimarySourceAudit.length :=
  rfl

/-- Machine-check that no audited source is currently treated as completed. -/
theorem externalProofIntegrationGateRows_noCompleted :
    externalProofIntegrationGateRows.map ExternalProofIntegrationGateRow.completedStateAllowed = [
      false,
      false,
      false
    ] :=
  rfl

/-- Machine-check that anchor-only completion is disallowed for every audited source. -/
theorem externalProofIntegrationGateRows_noAnchorOnly :
    externalProofIntegrationGateRows.map
        ExternalProofIntegrationGateRow.anchorOnlyCompletionAllowed = [
      false,
      false,
      false
    ] :=
  rfl

/--
Checked supporting wrapper for `S1-M-105-public-007`.

This is de Rham-complex infrastructure on normed vector spaces: the exterior
derivative squares to zero for sufficiently smooth unbundled differential
forms.  It is not a Hodge-decomposition theorem and supplies no compact Kähler
manifold, Hodge star, formal adjoint, Hodge Laplacian, harmonic-form,
Dolbeault, or cohomology-comparison API.
-/
theorem deRhamComplex_extDeriv_extDeriv
    (𝕜 : Type u) [NontriviallyNormedField 𝕜]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    (F : Type w) [NormedAddCommGroup F] [NormedSpace 𝕜 F]
    {n : ℕ} {r : WithTop ℕ∞}
    (ω : E → E [⋀^Fin n]→L[𝕜] F)
    (hω : ContDiff 𝕜 r ω) (hr : minSmoothness 𝕜 2 ≤ r) :
    extDeriv (extDeriv ω) = 0 :=
  extDeriv_extDeriv hω hr

/--
One package row in the integration-ready public theorem tree for
`S1-M-105-public-008`.

The package tree is documentation payload checked by Lean for shape only.  It
does not assert any analytic Hodge theorem.
-/
structure PublicTheoremTreePackage where
  packageId : String
  parentId : String
  title : String
  role : String
  status : String
deriving Repr

/-- Public theorem-tree packages for THM-M-0545. -/
def publicTheoremTreePackages : List PublicTheoremTreePackage := [
  {
    packageId := "P0_statement_normalization"
    parentId := "S1-M-105.root"
    title := "statement normalization"
    role :=
      "Fix the target as analytic compact-Kähler Hodge decomposition and choose the " ++
        "statement encoding before proof work starts."
    status := "unchecked"
  },
  {
    packageId := "P1_mathlib_object_model"
    parentId := "S1-M-105.root"
    title := "mathlib object model"
    role :=
      "Audit the available manifold, differential-form, harmonic, cohomology, and " ++
        "Kähler-differential APIs against the intended analytic target."
    status := "unchecked"
  },
  {
    packageId := "P2_de_rham_and_cohomology_bridge"
    parentId := "S1-M-105.root"
    title := "de Rham and cohomology bridge"
    role :=
      "Provide the manifold form complex and cohomology objects needed to interpret " ++
        "closed, exact, and harmonic representatives."
    status := "unchecked"
  },
  {
    packageId := "P3_analytic_hodge_core"
    parentId := "S1-M-105.root"
    title := "analytic Hodge core"
    role :=
      "Supply the Kähler metric, Hodge star, formal adjoint, Hodge Laplacian, and " ++
        "harmonic-representative theorem."
    status := "unchecked"
  },
  {
    packageId := "P4_type_decomposition"
    parentId := "S1-M-105.root"
    title := "type decomposition"
    role :=
      "Split forms and harmonic classes by bidegree and transfer type information to " ++
        "cohomology summands."
    status := "unchecked"
  },
  {
    packageId := "P5_direct_sum_closure"
    parentId := "S1-M-105.root"
    title := "direct-sum closure"
    role :=
      "Prove fixed-degree independence and spanning for the `H^{p,q}` summands, then " ++
        "package the result into the Stage1 statement shape."
    status := "unchecked"
  },
  {
    packageId := "P6_repo_local_gate"
    parentId := "S1-M-105.root"
    title := "repo-local validation gate"
    role :=
      "Choose a local proof, pinned mathlib wrapper, or pinned external dependency, then " ++
        "validate and merge public surfaces without anchor-only completion."
    status := "unchecked"
  }
]

/-- Machine-check that the public theorem tree has seven package branches. -/
theorem publicTheoremTreePackages_length :
    publicTheoremTreePackages.length = 7 :=
  rfl

/-- Machine-check that every public theorem-tree package remains unchecked. -/
theorem publicTheoremTreePackages_allUnchecked :
    publicTheoremTreePackages.all (fun row => row.status == "unchecked") = true :=
  rfl

/--
One leaf row in the integration-ready public theorem tree for
`S1-M-105-public-008`.

All leaves are deliberately marked `unchecked` until independently verified
under the M0387 `<=100` step-budget gate.
-/
structure PublicTheoremTreeLeaf where
  leafId : String
  packageId : String
  parentId : String
  leafStatement : String
  targetStepBudget : String
  status : String
  debtClass : String
deriving Repr

/-- Public theorem-tree leaf payload for `S1-M-105-public-008`. -/
def publicTheoremTreeLeaves : List PublicTheoremTreeLeaf := [
  {
    leafId := "S1-M-105-L001"
    packageId := "P0_statement_normalization"
    parentId := "S1-M-105.root"
    leafStatement :=
      "Normalize theorem variant: compact Kähler manifold versus smooth projective " ++
        "complex variety comparison route."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L002"
    packageId := "P0_statement_normalization"
    parentId := "S1-M-105-L001"
    leafStatement := "Freeze total degree and bidegree index type `HodgeBidegree n`."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L003"
    packageId := "P0_statement_normalization"
    parentId := "S1-M-105-L001"
    leafStatement := "Choose internal direct-sum conclusion `iSupIndep + iSup = top`."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L004"
    packageId := "P0_statement_normalization"
    parentId := "S1-M-105-L003"
    leafStatement :=
      "Prove finite-index equivalence between `HodgeBidegree n` and bounded pairs " ++
        "`p <= n`, `q = n - p`."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L005"
    packageId := "P1_mathlib_object_model"
    parentId := "S1-M-105.root"
    leafStatement := "Import-check complex manifold infrastructure."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L006"
    packageId := "P1_mathlib_object_model"
    parentId := "S1-M-105.root"
    leafStatement := "Import-check Riemannian/vector-bundle infrastructure."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L007"
    packageId := "P1_mathlib_object_model"
    parentId := "S1-M-105.root"
    leafStatement := "Import-check differential-form exterior derivative APIs."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L008"
    packageId := "P1_mathlib_object_model"
    parentId := "S1-M-105.root"
    leafStatement :=
      "Import-check harmonic-function/laplacian APIs and identify missing harmonic-form APIs."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L009"
    packageId := "P1_mathlib_object_model"
    parentId := "S1-M-105.root"
    leafStatement :=
      "Import-check sheaf cohomology APIs and compare scope with intended cohomology target."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L010"
    packageId := "P1_mathlib_object_model"
    parentId := "S1-M-105.root"
    leafStatement := "Distinguish algebraic Kähler differentials from analytic Kähler manifold structures."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L011"
    packageId := "P2_de_rham_and_cohomology_bridge"
    parentId := "S1-M-105.root"
    leafStatement := "Define/import de Rham complex of smooth manifold forms."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L012"
    packageId := "P2_de_rham_and_cohomology_bridge"
    parentId := "S1-M-105.root"
    leafStatement := "Define/import cohomology groups `H^n(X, C)`."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L013"
    packageId := "P2_de_rham_and_cohomology_bridge"
    parentId := "S1-M-105.root"
    leafStatement := "Define/import closed and exact differential-form predicates in the intended complex."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L014"
    packageId := "P2_de_rham_and_cohomology_bridge"
    parentId := "S1-M-105-L013"
    leafStatement := "State/prove de Rham cohomology quotient relation for closed modulo exact forms."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L015"
    packageId := "P3_analytic_hodge_core"
    parentId := "S1-M-105.root"
    leafStatement := "Define/import Kähler metric compatibility data."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L016"
    packageId := "P3_analytic_hodge_core"
    parentId := "S1-M-105-L015"
    leafStatement := "Define/import Hodge star on forms."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L017"
    packageId := "P3_analytic_hodge_core"
    parentId := "S1-M-105-L016"
    leafStatement := "Define/import formal adjoint of exterior derivative."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L018"
    packageId := "P3_analytic_hodge_core"
    parentId := "S1-M-105-L017"
    leafStatement := "Define/import Hodge Laplacian and harmonic-form predicate."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L019"
    packageId := "P3_analytic_hodge_core"
    parentId := "S1-M-105-L018"
    leafStatement := "Prove/state existence of harmonic representatives."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L020"
    packageId := "P3_analytic_hodge_core"
    parentId := "S1-M-105-L019"
    leafStatement := "Prove/state uniqueness of harmonic representatives modulo exact forms."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L021"
    packageId := "P4_type_decomposition"
    parentId := "S1-M-105.root"
    leafStatement := "Define/import `(p,q)`-form type decomposition."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L022"
    packageId := "P4_type_decomposition"
    parentId := "S1-M-105-L021"
    leafStatement := "Prove/state Kähler identities needed for harmonic type preservation."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L023"
    packageId := "P4_type_decomposition"
    parentId := "S1-M-105-L022"
    leafStatement := "Transfer harmonic type decomposition to cohomology summands `H^{p,q}`."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L024"
    packageId := "P5_direct_sum_closure"
    parentId := "S1-M-105-L023"
    leafStatement := "Prove pairwise disjointness / `iSupIndep` of fixed-degree Hodge summands."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L025"
    packageId := "P5_direct_sum_closure"
    parentId := "S1-M-105-L024"
    leafStatement := "Prove supremum/top coverage of fixed-degree cohomology by Hodge summands."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L026"
    packageId := "P5_direct_sum_closure"
    parentId := "S1-M-105-L025"
    leafStatement := "Combine harmonic representative and direct-sum packages into `StatementShape`."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L027"
    packageId := "P6_repo_local_gate"
    parentId := "S1-M-105.root"
    leafStatement := "If an external proof is found, add pinned Lake dependency or vendored proof body."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "repo_local_integration_debt_if_external_proof_found"
  },
  {
    leafId := "S1-M-105-L028"
    packageId := "P6_repo_local_gate"
    parentId := "S1-M-105-L027"
    leafStatement := "Add repo-local wrapper with exact imported theorem name and no anchor-only completion."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "repo_local_integration_debt_if_external_proof_found"
  },
  {
    leafId := "S1-M-105-L029"
    packageId := "P6_repo_local_gate"
    parentId := "S1-M-105-L028"
    leafStatement := "Run `lake env lean` / `lake build` and record reproducible validation."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  },
  {
    leafId := "S1-M-105-L030"
    packageId := "P6_repo_local_gate"
    parentId := "S1-M-105-L029"
    leafStatement :=
      "Merge human-readable public surface and synchronize blueprint/todo/README only after " ++
        "machine closure."
    targetStepBudget := "<=100"
    status := "unchecked"
    debtClass := "formalization_debt"
  }
]

/-- Machine-check that the public theorem tree has exactly the requested 30 leaves. -/
theorem publicTheoremTreeLeaves_length :
    publicTheoremTreeLeaves.length = 30 :=
  rfl

/-- Machine-check that the public theorem tree uses exactly `S1-M-105-L001` through `L030`. -/
theorem publicTheoremTreeLeaves_ids :
    publicTheoremTreeLeaves.map PublicTheoremTreeLeaf.leafId = [
      "S1-M-105-L001",
      "S1-M-105-L002",
      "S1-M-105-L003",
      "S1-M-105-L004",
      "S1-M-105-L005",
      "S1-M-105-L006",
      "S1-M-105-L007",
      "S1-M-105-L008",
      "S1-M-105-L009",
      "S1-M-105-L010",
      "S1-M-105-L011",
      "S1-M-105-L012",
      "S1-M-105-L013",
      "S1-M-105-L014",
      "S1-M-105-L015",
      "S1-M-105-L016",
      "S1-M-105-L017",
      "S1-M-105-L018",
      "S1-M-105-L019",
      "S1-M-105-L020",
      "S1-M-105-L021",
      "S1-M-105-L022",
      "S1-M-105-L023",
      "S1-M-105-L024",
      "S1-M-105-L025",
      "S1-M-105-L026",
      "S1-M-105-L027",
      "S1-M-105-L028",
      "S1-M-105-L029",
      "S1-M-105-L030"
    ] :=
  rfl

/-- Machine-check that every public theorem-tree leaf remains unchecked. -/
theorem publicTheoremTreeLeaves_allUnchecked :
    publicTheoremTreeLeaves.all (fun row => row.status == "unchecked") = true :=
  rfl

/-- Machine-check that every public theorem-tree leaf keeps the M0387 step budget. -/
theorem publicTheoremTreeLeaves_allWithinBudget :
    publicTheoremTreeLeaves.all (fun row => row.targetStepBudget == "<=100") = true :=
  rfl

/-- M0387 debt classification for the current repo-local artifact. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/-- Completion gate: this statement-shape artifact is not a completed theorem. -/
def repoLocalCompletionGate : String :=
  "not_repo_local_closed"

/--
Repo-local validation row for `S1-M-105-public-009`.

This records the required file-level Lean check after the Stage1 statement-shape
and wrapper payloads.  It is a validation surface for the local artifact, not a
claim that the analytic Hodge decomposition theorem is complete.
-/
structure RepoLocalValidationRecord where
  childId : String
  runDate : String
  workingDirectory : String
  command : String
  checkedFile : String
  result : String
  theoremCompleted : Bool
  repoLocalIntegrationDebtRetained : Bool
  completionGate : String
deriving Repr

/-- Public backfill payload for the validation surface of `S1-M-105-public-009`. -/
def publicValidationRecord : RepoLocalValidationRecord := {
  childId := "S1-M-105-public-009"
  runDate := "2026-05-01 Asia/Shanghai"
  workingDirectory := "Formalizations/Lean"
  command := "lake env lean AwesomeTheorems/Stage1/S1_M_105.lean"
  checkedFile := "AwesomeTheorems/Stage1/S1_M_105.lean"
  result := "pass: exit code 0"
  theoremCompleted := false
  repoLocalIntegrationDebtRetained := false
  completionGate := repoLocalCompletionGate
}

/-- Machine-check the validation row keeps THM-M-0545 out of completed state. -/
theorem publicValidationRecord_noCompletion :
    publicValidationRecord.theoremCompleted = false :=
  rfl

/-- Machine-check the validation row does not retain repo-local integration debt. -/
theorem publicValidationRecord_noRepoLocalIntegrationDebt :
    publicValidationRecord.repoLocalIntegrationDebtRetained = false :=
  rfl

/-! ## Audit probes -/

#check HodgeBidegree
#check HodgeDecompositionPackage.DirectSumConclusion
#check HodgeDecompositionPackage.canonicalExternalDirectSumMap
#check HodgeDecompositionPackage.ExternalDirectSumEquivalenceConclusion
#check HodgeDecompositionPackage.directSumSurfaceDecision
#check HodgeDecompositionPackage.HarmonicRepresentativeConclusion
#check HodgeDecompositionPackage.StatementShape
#check HodgeDecompositionPackage.externalDirectSumEquivalence_of_internal
#check StatementShape
#check publicMathlibAuditTable
#check publicMathlibAuditTable_length
#check publicMathlibAuditTable_requestedNames
#check missingApiChildTasks
#check missingApiChildTasks_length
#check missingApiChildTasks_titles
#check externalLeanPrimarySourceAudit
#check externalLeanPrimarySourceAudit_length
#check externalLeanPrimarySourceAudit_terms
#check externalProofIntegrationGateRows
#check externalProofIntegrationGateRows_length
#check externalProofIntegrationGateRows_noCompleted
#check externalProofIntegrationGateRows_noAnchorOnly
#check deRhamComplex_extDeriv_extDeriv
#check publicTheoremTreePackages
#check publicTheoremTreePackages_length
#check publicTheoremTreePackages_allUnchecked
#check publicTheoremTreeLeaves
#check publicTheoremTreeLeaves_length
#check publicTheoremTreeLeaves_ids
#check publicTheoremTreeLeaves_allUnchecked
#check publicTheoremTreeLeaves_allWithinBudget
#check iSupIndep
#check statementNormalizationNote
#check intendedAnalyticScope
#check excludedStatementScope
#check machineProofDebtClassification
#check repoLocalCompletionGate
#check publicValidationRecord
#check publicValidationRecord_noCompletion
#check publicValidationRecord_noRepoLocalIntegrationDebt

end AwesomeTheorems.Stage1.S1_M_105
