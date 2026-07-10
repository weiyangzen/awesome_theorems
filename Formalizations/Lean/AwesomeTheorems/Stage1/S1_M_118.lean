import Mathlib.Algebra.Homology.EulerCharacteristic
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.InnerProductSpace.Orientation
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Geometry.Manifold.ContMDiff.Basic
import Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary
import Mathlib.Geometry.Manifold.VectorBundle.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Typeclasses.Finite

/-!
# S1-M-118 / THM-M-0571: local index theorem

This Stage1 artifact records a conservative Lean statement-shape boundary for
the local index-density formula in index theory.

The pinned mathlib snapshot provides smooth-manifold, boundaryless-manifold,
vector-bundle, and homological Euler-characteristic substrates.  It does not
provide a terminal API for Fredholm/elliptic differential operators,
pseudodifferential symbols, characteristic forms/classes, integration of
differential forms over compact manifolds, or the local index-density theorem.

The declarations below therefore expose a precise abstract boundary plus
checked substrate wrappers only, without proof-placeholder declarations.
-/

noncomputable section

open scoped ContDiff Manifold MeasureTheory

universe uE uH uM uR uD uB uF uι

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_118

/--
Minimal smooth manifold boundary used by the local index theorem.

A terminal formalization should specialize this to compact, oriented,
boundaryless smooth manifolds of finite dimension, with the exact regularity and
orientation APIs needed by the chosen differential-form/integration substrate.
-/
structure SmoothManifoldBoundary
    (E : Type uE) (H : Type uH) (M : Type uM)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H) : Type (max uH uM) where
  chartedSpace : ChartedSpace H M
  smooth : @IsManifold ℝ _ E _ _ H _ I ∞ M _ chartedSpace
  boundaryless : @BoundarylessManifold ℝ _ E _ _ H _ I M _ chartedSpace

/--
Abstract data for the local index-density formula.

The fields deliberately keep the currently missing pieces explicit:
`Operator`, `IsElliptic`, `analyticIndex`, `indexDensity`,
`characteristicDensity`, and `integrateDensity` must eventually be replaced by
concrete mathlib or pinned-dependency APIs for elliptic operators, Fredholm
index, characteristic forms, and integration.
-/
structure LocalIndexTheoremData
    (M : Type uM) (R : Type uR)
    [TopologicalSpace M] [Ring R] :
    Type (max (max uM uR) (uD + 1)) where
  Operator : Type uD
  IsElliptic : Operator → Prop
  analyticIndex : Operator → ℤ
  indexDensity : Operator → M → R
  characteristicDensity : Operator → M → R
  integrateDensity : (M → R) → ℤ
  local_density_formula :
    ∀ (D : Operator) (x : M),
      IsElliptic D → indexDensity D x = characteristicDensity D x
  integrated_index_formula :
    ∀ D : Operator,
      IsElliptic D → analyticIndex D = integrateDensity (characteristicDensity D)

/--
Formula-level statement for the abstract local index theorem boundary.

For every elliptic operator, the index density agrees pointwise with the
characteristic density, and integrating the characteristic density recovers the
analytic index.
-/
def LocalIndexDensityFormula
    {M : Type uM} {R : Type uR}
    [TopologicalSpace M] [Ring R]
    (A : LocalIndexTheoremData.{uM, uR, uD} M R) : Prop :=
  (∀ (D : A.Operator) (x : M),
    A.IsElliptic D → A.indexDensity D x = A.characteristicDensity D x) ∧
  (∀ D : A.Operator,
    A.IsElliptic D → A.analyticIndex D = A.integrateDensity (A.characteristicDensity D))

/--
Stage1 statement-shape candidate for THM-M-0571.

The concrete hypotheses say that `M` is a boundaryless smooth real manifold in
mathlib's `ModelWithCorners` framework.  The theorem's analytic and
cohomological content is bundled in `LocalIndexTheoremData` because the current
repo-local dependency closure has no terminal Lean 4 proof of the local index
formula.
-/
def StatementShape
    (E : Type uE) (H : Type uH) (M : Type uM) (R : Type uR)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M] [Ring R]
    (I : ModelWithCorners ℝ E H) : Prop :=
  Nonempty (SmoothManifoldBoundary E H M I) →
    ∃ A : LocalIndexTheoremData.{uM, uR, uD} M R,
      LocalIndexDensityFormula A

/-- The statement shape unfolds to the abstract local-index formula package. -/
theorem statementShape_iff_exists_formula
    (E : Type uE) (H : Type uH) (M : Type uM) (R : Type uR)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M] [Ring R]
    (I : ModelWithCorners ℝ E H) :
    StatementShape.{uE, uH, uM, uR, uD} E H M R I ↔
      (Nonempty (SmoothManifoldBoundary E H M I) →
        ∃ A : LocalIndexTheoremData.{uM, uR, uD} M R,
          LocalIndexDensityFormula A) :=
  Iff.rfl

/-- A smooth manifold is also a topological (`C^0`) manifold in mathlib's hierarchy. -/
theorem smoothManifold_isManifold_zero
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H)
    [ChartedSpace H M] [IsManifold I ∞ M] :
    IsManifold I 0 M :=
  inferInstance

/-- The identity map on a smooth manifold is smooth. -/
theorem contMDiff_id_on_smooth_manifold
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H)
    [ChartedSpace H M] [IsManifold I ∞ M] :
    ContMDiff I I ∞ (fun x : M => x) := by
  exact contMDiff_id

/-- Local wrapper for mathlib's smooth vector-bundle predicate. -/
def SmoothVectorBundlePredicate
    (B : Type uB) (F : Type uF) (E : B → Type uι)
    [TopologicalSpace B]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [∀ x, AddCommMonoid (E x)] [∀ x, Module ℝ (E x)]
    [TopologicalSpace (Bundle.TotalSpace F E)]
    [∀ x, TopologicalSpace (E x)] [FiberBundle F E]
    [VectorBundle ℝ F E]
    {EB : Type uE} [NormedAddCommGroup EB] [NormedSpace ℝ EB]
    {HB : Type uH} [TopologicalSpace HB]
    (IB : ModelWithCorners ℝ EB HB)
    [ChartedSpace HB B] : Prop :=
  ContMDiffVectorBundle ∞ F E IB

/-- A checked wrapper around mathlib's Euler characteristic of a homological complex. -/
abbrev HomologicalComplexEulerChar
    (R : Type uR) [Ring R] {ι : Type uι} {c : ComplexShape ι}
    [c.EulerCharSigns] (C : HomologicalComplex (ModuleCat R) c) : ℤ :=
  HomologicalComplex.eulerChar C

structure MathlibAnchorAuditRow where
  moduleName : String
  declarationName : String
  sourceLocation : String
  repoLocalStatus : String
  localIndexRole : String
  blocker : String

/-- mathlib revision used for the `THM-M-0571.mathlib-anchor-audit` child task. -/
def mathlibAnchorAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Integration-ready public anchor table for the local-index Stage1 slot.

These rows are positive substrate anchors only.  They do not close the local
index theorem because the Fredholm/elliptic-operator, characteristic-density,
and differential-form integration APIs remain outside the checked repo-local
boundary recorded by this file.
-/
def mathlibAnchorAuditTable : List MathlibAnchorAuditRow := [
  {
    moduleName := "Mathlib.Geometry.Manifold.IsManifold.Basic",
    declarationName := "IsManifold",
    sourceLocation := "Mathlib/Geometry/Manifold/IsManifold/Basic.lean:785",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localIndexRole := "Smooth-manifold typeclass over `ModelWithCorners`, used by `SmoothManifoldBoundary`.",
    blocker := "Does not provide elliptic operators, analytic index, index densities, or characteristic forms."
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary",
    declarationName := "BoundarylessManifold",
    sourceLocation := "Mathlib/Geometry/Manifold/IsManifold/InteriorBoundary.lean:164",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localIndexRole := "Boundaryless-manifold typeclass required by the Stage1 compact-boundaryless statement shape.",
    blocker := "Boundarylessness is substrate only; compactness, orientation, ellipticity, and integration remain uninstantiated."
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.ContMDiff.Defs",
    declarationName := "ContMDiff",
    sourceLocation := "Mathlib/Geometry/Manifold/ContMDiff/Defs.lean:192",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localIndexRole := "Smoothness predicate for maps between charted manifolds.",
    blocker := "Does not package differential operators, symbols, heat kernels, or local index-density proofs."
  },
  {
    moduleName := "Mathlib.Topology.VectorBundle.Basic",
    declarationName := "VectorBundle",
    sourceLocation := "Mathlib/Topology/VectorBundle/Basic.lean:361",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localIndexRole := "Topological vector-bundle substrate for operator domain/codomain bundles.",
    blocker := "No elliptic differential-operator API or analytic index is attached to this class."
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.VectorBundle.Basic",
    declarationName := "ContMDiffVectorBundle",
    sourceLocation := "Mathlib/Geometry/Manifold/VectorBundle/Basic.lean:280",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localIndexRole := "Smooth vector-bundle predicate used by `SmoothVectorBundlePredicate`.",
    blocker := "Smooth bundle transitions are available, but connections, symbols, characteristic densities, and index maps are not closed."
  },
  {
    moduleName := "Mathlib.Algebra.Homology.EulerCharacteristic",
    declarationName := "HomologicalComplex.eulerChar",
    sourceLocation := "Mathlib/Algebra/Homology/EulerCharacteristic.lean:147",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localIndexRole := "Homological Euler-characteristic substrate for index-style integer outputs.",
    blocker := "Euler characteristic alone is not a Fredholm index and is not connected to elliptic operator kernels/cokernels here."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularSet",
    declarationName := "TopCat.toSSet",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularSet.lean:54",
    repoLocalStatus := "upstream_anchor_checked",
    localIndexRole := "Singular simplicial-set bridge from topological spaces to simplicial sets.",
    blocker := "Substrate for homology only; no de Rham or characteristic-class comparison is supplied."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    declarationName := "AlgebraicTopology.SSet.singularChainComplexFunctor",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularHomology/Basic.lean:36",
    repoLocalStatus := "upstream_anchor_checked",
    localIndexRole := "Singular chain complex associated to a simplicial set with coefficients.",
    blocker := "Does not supply manifold de Rham forms or a local index density."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    declarationName := "AlgebraicTopology.singularChainComplexFunctor",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularHomology/Basic.lean:42",
    repoLocalStatus := "upstream_anchor_checked",
    localIndexRole := "TopCat singular chain complex functor with coefficients.",
    blocker := "Provides homology substrate only, not the analytic or characteristic-class sides of the local index theorem."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    declarationName := "AlgebraicTopology.singularHomologyFunctor",
    sourceLocation := "Mathlib/AlgebraicTopology/SingularHomology/Basic.lean:47",
    repoLocalStatus := "upstream_anchor_checked",
    localIndexRole := "Singular homology functor for topological spaces.",
    blocker := "No bridge is checked from singular homology to the local index theorem's analytic-density formula."
  }
]

/-- The C002 anchor table has one row for each requested substrate family. -/
theorem mathlibAnchorAuditTable_length :
    mathlibAnchorAuditTable.length = 10 :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.ChartedSpace",
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary",
  "Mathlib.Geometry.Manifold.ContMDiff.Basic",
  "Mathlib.Geometry.Manifold.ContMDiff.Defs",
  "Mathlib.Topology.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Bordism",
  "Mathlib.Algebra.Homology.EulerCharacteristic",
  "Mathlib.AlgebraicTopology.SingularSet",
  "Mathlib.AlgebraicTopology.SingularHomology.Basic"
]

/-- Checked declaration names from the C002 public anchor table. -/
def mathlibAnchorNames : List String :=
  mathlibAnchorAuditTable.map (fun row => row.declarationName)

/-- Search terms that did not locate a terminal local index theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Atiyah",
  "Singer",
  "IndexTheorem",
  "LocalIndex",
  "Dirac",
  "Fredholm",
  "EllipticOperator",
  "Pseudodifferential",
  "CharacteristicClass",
  "Chern",
  "Pontryagin",
  "Todd",
  "DifferentialForm",
  "de Rham",
  "index density",
  "heat kernel"
]

structure OperatorApiAuditRow where
  requestedApi : String
  checkedSurface : String
  evidence : String
  repoLocalStatus : String
  localIndexRole : String
  blocker : String

/--
Operator-side API audit for `THM-M-0571.operator-api-audit`.

This table records checked local dependency surfaces only.  The positive rows
are adjacent infrastructure, not a completed local-index theorem API.
-/
def operatorApiAuditTable : List OperatorApiAuditRow := [
  {
    requestedApi := "Fredholm operators",
    checkedSurface := "Mathlib.Analysis.Normed.Operator.FredholmAlternative; Mathlib.Analysis.Normed.Operator.Banach",
    evidence := "`IsCompactOperator.hasEigenvalue_or_mem_resolventSet` proves the Fredholm alternative for compact operators; `Banach.lean` has a TODO saying to generalize lemmas once mathlib has Fredholm operators.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Adjacent Banach-space spectral theory only.",
    blocker := "No checked `Fredholm` structure/class, Fredholm index, finite kernel/cokernel package, or elliptic-operator Fredholm theorem is present in the pinned repo-local dependency closure."
  },
  {
    requestedApi := "elliptic differential operators",
    checkedSurface := "Mathlib.Geometry.Manifold.*; Mathlib.Analysis.Normed.Operator.*",
    evidence := "Pinned mathlib provides smooth-manifold and continuous-linear-operator infrastructure, but no located declaration packages differential operators on vector bundles with an ellipticity predicate.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Would supply the operator object and ellipticity hypothesis of the local index theorem.",
    blocker := "`LocalIndexTheoremData.Operator` and `LocalIndexTheoremData.IsElliptic` remain abstract fields."
  },
  {
    requestedApi := "principal symbols",
    checkedSurface := "Repository-local search over pinned mathlib and `flt-regular`",
    evidence := "Searches for `principal symbol`, `PrincipalSymbol`, and `principalSymbol` did not locate a differential-operator symbol API; unrelated algebraic `Symbols` files are not applicable.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Would identify ellipticity and the symbol-side proof package.",
    blocker := "No repo-local principal-symbol type or theorem connects symbols to elliptic Fredholmness."
  },
  {
    requestedApi := "pseudodifferential operators",
    checkedSurface := "Repository-local search over pinned mathlib and `flt-regular`",
    evidence := "Searches for `Pseudodifferential`, `pseudodifferential`, and `pseudo-differential` found no terminal operator calculus.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Would support the parametrix and local symbol calculus branch.",
    blocker := "No pseudodifferential calculus, parametrix API, or index-density construction is available locally."
  },
  {
    requestedApi := "Dirac operators",
    checkedSurface := "Measure/distribution Dirac surfaces only",
    evidence := "Searches for `Dirac` locate Dirac measures and Dirac delta distributions, not geometric Dirac operators on Clifford modules or spin manifolds.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Would provide a key elliptic-operator family for index-theorem instances.",
    blocker := "No checked Dirac-operator declaration, Clifford-symbol package, or heat-kernel index proof was found locally."
  },
  {
    requestedApi := "kernels and cokernels",
    checkedSurface := "Mathlib.CategoryTheory.Limits.Shapes.Kernels; Mathlib.Algebra.Homology.ShortComplex.*",
    evidence := "Category-theoretic kernels/cokernels and homological kernels/cokernels are present in mathlib.",
    repoLocalStatus := "local_wrapper_upstream_mathlib_adjacent",
    localIndexRole := "Potential substrate for homological algebra bookkeeping.",
    blocker := "These categorical kernels/cokernels are not specialized to analytic Fredholm operators and are not connected to a finite-dimensional analytic index."
  },
  {
    requestedApi := "analytic index",
    checkedSurface := "Repository-local search over pinned mathlib and `flt-regular`",
    evidence := "Searches for `analytic index`, `analyticIndex`, `IndexTheorem`, `LocalIndex`, `Atiyah`, and `Singer` did not locate an analytic-index API or index theorem.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Would supply the integer target of the local index theorem.",
    blocker := "`LocalIndexTheoremData.analyticIndex` remains an abstract field, with no repo-local Fredholm-index definition behind it."
  },
  {
    requestedApi := "external Lean 4 operator package",
    checkedSurface := "Formalizations/Lean/lakefile.lean and lake-manifest.json",
    evidence := "The repo-local dependency closure contains pinned mathlib and `flt-regular`; no external Lean 4 analytic-index, elliptic-operator, or pseudodifferential package is pinned/imported.",
    repoLocalStatus := "not_repo_local_closed",
    localIndexRole := "Would be the path to `external_upstream_pinned` if a real external proof/API were found.",
    blocker := "No external proof/API is currently inside the repo-local Lake closure, so there is no repo-local integration-debt completion claim to discharge for this child."
  }
]

/-- The C003 operator API audit covers each requested operator-side family. -/
theorem operatorApiAuditTable_length :
    operatorApiAuditTable.length = 8 :=
  rfl

/-- Search strings used for the operator API audit. -/
def operatorApiAuditSearchTerms : List String := [
  "Fredholm",
  "fredholm",
  "EllipticOperator",
  "elliptic differential operator",
  "PrincipalSymbol",
  "principal symbol",
  "Pseudodifferential",
  "pseudodifferential",
  "DiracOperator",
  "Dirac operator",
  "analyticIndex",
  "analytic index",
  "AtiyahSinger",
  "Atiyah_Singer",
  "IndexTheorem",
  "LocalIndex",
  "heatKernel",
  "heat kernel"
]

/--
Machine-readable gate result for C003.

No external Lean 4 proof/API for the local index theorem was found inside the
repo-local Lake closure.  Therefore this child leaves formalization debt, not a
completed state with unresolved repo-local integration debt.
-/
def operatorApiAuditRepoLocalIntegrationDebtGate : String :=
  "pass: no completed claim and no external operator/index proof or API is present in the repo-local Lake closure; remaining debt is formalization_debt/not_repo_local_closed."

/--
Local alias for mathlib's current unbundled differential-form substrate on a
normed space.

This is intentionally not a manifold de Rham form API: pinned mathlib represents
an `n`-form on a normed space as a function into continuous alternating maps.
-/
abbrev NormedSpaceDifferentialForm
    (𝕜 E F : Type*) [NontriviallyNormedField 𝕜]
    [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    [NormedAddCommGroup F] [NormedSpace 𝕜 F] (n : ℕ) : Type _ :=
  E → E [⋀^Fin n]→L[𝕜] F

structure CharacteristicClassApiAuditRow where
  requestedApi : String
  checkedSurface : String
  evidence : String
  repoLocalStatus : String
  localIndexRole : String
  blocker : String

/--
Characteristic-class-side API audit for
`THM-M-0571.characteristic-class-api-audit`.

The positive differential-form row is only a normed-space exterior-derivative
substrate.  The rows for de Rham cohomology, Chern/Pontryagin/Todd/A-hat
classes, top-degree manifold forms, and characteristic-density normalization
remain formalization debt in this Lake closure.
-/
def characteristicClassApiAuditTable : List CharacteristicClassApiAuditRow := [
  {
    requestedApi := "differential forms",
    checkedSurface := "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
    evidence := "Pinned mathlib defines unbundled normed-space differential forms as `E -> E [⋀^Fin n]->L[𝕜] F`, with `extDeriv`, `extDerivWithin`, pullback lemmas, and second-exterior-derivative-zero lemmas under smoothness hypotheses.",
    repoLocalStatus := "local_wrapper_upstream_mathlib_partial_anchor",
    localIndexRole := "Provides adjacent exterior-calculus substrate for local density expressions in coordinate/normed-space form.",
    blocker := "The source TODO says bundled smooth `n`-forms on normed spaces and manifolds are not yet defined; no manifold de Rham complex or integration-ready top-degree form API is supplied by this row."
  },
  {
    requestedApi := "de Rham cohomology",
    checkedSurface := "Repository-local search over pinned mathlib and `flt-regular`",
    evidence := "Searches for `deRham`, `de Rham`, and `Rham` found only unrelated period-ring text and a comment about future de Rham cohomologies; no manifold de Rham cochain complex or cohomology object was located.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Would host characteristic classes and identify closed characteristic forms modulo exact forms.",
    blocker := "No repo-local de Rham cohomology API is available to receive characteristic classes or prove density representatives independent of choices."
  },
  {
    requestedApi := "Chern classes and Chern character",
    checkedSurface := "Repository-local search over pinned mathlib, `flt-regular`, and adjacent Stage1 HRR/index artifacts",
    evidence := "Searches for `Chern`, `Chern class`, and `Chern character` found no Lean declarations in the repo-local dependency closure; adjacent S1_M_125 and S1_M_113 artifacts also record Chern-character absence.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Needed for the vector-bundle characteristic factor in index-density formulas.",
    blocker := "No checked Chern class, Chern-Weil representative, or Chern character API is pinned or locally proved."
  },
  {
    requestedApi := "Pontryagin classes",
    checkedSurface := "Mathlib.Topology.Algebra.PontryaginDual and finite Fourier Pontryagin-duality files; repository-local search",
    evidence := "`PontryaginDual` and finite Pontryagin duality are present, but they concern duality of topological/finite abelian groups, not Pontryagin characteristic classes of real vector bundles.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Needed for the tangent-bundle characteristic factor in L-class/A-hat style index densities.",
    blocker := "No checked Pontryagin class or Chern-Weil Pontryagin-form API for real vector bundles is present."
  },
  {
    requestedApi := "Todd class",
    checkedSurface := "Repository-local search over pinned mathlib, `flt-regular`, and adjacent HRR artifact",
    evidence := "Searches for `Todd` and `Todd class` found no Lean declaration in the current Lake closure; the HRR Stage1 artifact keeps `toddClassTangent` abstract for the same reason.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Needed for Dolbeault/Hirzebruch-Riemann-Roch variants of the index theorem.",
    blocker := "No checked Todd class, power-series normalization, or multiplicative-sequence package is available locally."
  },
  {
    requestedApi := "A-hat class",
    checkedSurface := "Repository-local search over pinned mathlib, `flt-regular`, and adjacent index artifacts",
    evidence := "Searches for `Ahat`, `A-hat`, `A hat`, and `Â` found no A-hat class declaration or spin Dirac characteristic-class package.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Needed for spin Dirac index-density formulas.",
    blocker := "No checked A-hat class, Pontryagin-polynomial definition, or normalization theorem is present."
  },
  {
    requestedApi := "top-degree differential forms on manifolds",
    checkedSurface := "Mathlib.Analysis.Calculus.DifferentialForm.Basic plus Mathlib.Geometry.Manifold.*",
    evidence := "Mathlib has unbundled normed-space forms and smooth-manifold substrates, but no located bundled smooth manifold `n`-form API tying form degree to `finrank`, orientation, compact support, or manifold integration.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Would provide the precise type of the characteristic density to integrate over a compact oriented smooth manifold.",
    blocker := "`LocalIndexTheoremData.characteristicDensity` and `integrateDensity` remain scalar-function abstractions rather than top-degree-form/integration APIs."
  },
  {
    requestedApi := "characteristic-density normalization",
    checkedSurface := "Repository-local search over pinned mathlib and Stage1 local-index artifacts",
    evidence := "No checked declaration fixes the local index density normalization, such as `(2*pi*I)^(-n/2)`, Chern-Weil sign conventions, A-hat/Todd power series, or heat-kernel supertrace constants.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "Needed to state and prove the exact equality between analytic local density and characteristic-form representative.",
    blocker := "The theorem cannot be completed until a concrete normalization convention is selected and connected to both the analytic and characteristic-class sides."
  },
  {
    requestedApi := "external Lean 4 characteristic-class package",
    checkedSurface := "Formalizations/Lean/lakefile.lean and lake-manifest.json",
    evidence := "The repo-local dependency closure contains pinned mathlib and `flt-regular`; no external Lean 4 package for de Rham cohomology, Chern-Weil theory, characteristic classes, or local index density is pinned/imported.",
    repoLocalStatus := "not_repo_local_closed",
    localIndexRole := "Would be the path to `external_upstream_pinned` if a real characteristic-class/index-density package were found.",
    blocker := "No external characteristic-class proof/API is currently inside the repo-local Lake closure, so this child records formalization blockers rather than completed repo-local integration debt."
  }
]

/-- The C004 characteristic-class API audit covers each requested characteristic-side family. -/
theorem characteristicClassApiAuditTable_length :
    characteristicClassApiAuditTable.length = 9 :=
  rfl

/-- Search strings used for the characteristic-class API audit. -/
def characteristicClassApiAuditSearchTerms : List String := [
  "DifferentialForm",
  "extDeriv",
  "deRham",
  "de Rham",
  "Chern",
  "Chern character",
  "Pontryagin",
  "Pontryagin class",
  "Todd",
  "Todd class",
  "Ahat",
  "A-hat",
  "A hat",
  "Â",
  "top-degree differential form",
  "characteristic density",
  "index density"
]

/--
Machine-readable gate result for C004.

The checked differential-form substrate is partial and adjacent only.  No
external Lean 4 proof/API for the local index theorem's characteristic-class
side is pinned in the repo-local Lake closure, so the remaining state is
formalization debt rather than completed repo-local integration debt.
-/
def characteristicClassApiRepoLocalIntegrationDebtGate : String :=
  "pass: no completed claim and no external de Rham/characteristic-class/index-density proof or API is present in the repo-local Lake closure; remaining debt is formalization_debt/not_repo_local_closed."

structure IntegrationApiAuditRow where
  requestedApi : String
  checkedSurface : String
  evidence : String
  repoLocalStatus : String
  localIndexRole : String
  blocker : String

/--
Interim scalar-density integration functional chosen for the C005 audit.

This is the strongest repo-local integration API available in the pinned Lake
closure: integrate an `F`-valued density over an explicit finite measure using
mathlib's Bochner integral.  It is not, by itself, integration of top-degree
differential forms on manifolds.
-/
abbrev ScalarDensityIntegrationFunctional
    (M F : Type*) [MeasurableSpace M]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (_μ : MeasureTheory.Measure M) : Type _ :=
  (M → F) → F

/-- Chosen repo-local scalar-density integration implementation. -/
noncomputable def scalarDensityIntegral
    (M F : Type*) [MeasurableSpace M]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (μ : MeasureTheory.Measure M) :
    ScalarDensityIntegrationFunctional M F μ :=
  fun f => ∫ x, f x ∂μ

/-- The chosen scalar-density integration API is exactly mathlib's Bochner integral. -/
theorem scalarDensityIntegral_apply
    (M F : Type*) [MeasurableSpace M]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (μ : MeasureTheory.Measure M) (f : M → F) :
    scalarDensityIntegral M F μ f = ∫ x, f x ∂μ :=
  rfl

/--
Compact scalar integration boundary for the local-index Stage1 slot.

This structure intentionally uses an explicit finite measure.  A future
top-degree-form API should replace `density` by a bundled smooth top-degree
form and construct `μ` canonically from the oriented smooth manifold data.
-/
structure CompactScalarIntegrationBoundary
    (M : Type uM) [TopologicalSpace M] [CompactSpace M] [MeasurableSpace M] where
  measure : MeasureTheory.Measure M
  finiteMeasure : MeasureTheory.IsFiniteMeasure measure

/-- Scalar-density integral attached to a compact finite-measure boundary. -/
noncomputable def CompactScalarIntegrationBoundary.integrate
    {M : Type uM} [TopologicalSpace M] [CompactSpace M] [MeasurableSpace M]
    (B : CompactScalarIntegrationBoundary M) (f : M → ℝ) : ℝ := by
  letI := B.finiteMeasure
  exact scalarDensityIntegral M ℝ B.measure f

/-- The compact scalar boundary integrates by the selected Bochner API. -/
theorem compactScalarIntegrationBoundary_integrate_eq_integral
    {M : Type uM} [TopologicalSpace M] [CompactSpace M] [MeasurableSpace M]
    (B : CompactScalarIntegrationBoundary M) (f : M → ℝ) :
    B.integrate f = ∫ x, f x ∂B.measure := by
  rfl

/-- Top-degree alternating-form type on the model vector space side. -/
abbrev ModelTopDegreeAlternatingForm
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (n : ℕ) [Fact (Module.finrank ℝ E = n)] : Type uE :=
  E [⋀^Fin n]→ₗ[ℝ] ℝ

/--
Checked model-space orientation anchor.

Mathlib provides a top-degree volume form on an oriented finite-dimensional real
inner product space.  The audit keeps this separate from manifold form
integration because the pinned dependency closure does not provide a bundled
oriented-manifold top-degree form integration API.
-/
noncomputable def modelOrientationVolumeForm
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (n : ℕ) [Fact (Module.finrank ℝ E = n)]
    (o : Orientation ℝ E (Fin n)) :
    ModelTopDegreeAlternatingForm E n :=
  o.volumeForm

/-- The model orientation anchor is exactly mathlib's `Orientation.volumeForm`. -/
theorem modelOrientationVolumeForm_eq
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (n : ℕ) [Fact (Module.finrank ℝ E = n)]
    (o : Orientation ℝ E (Fin n)) :
    modelOrientationVolumeForm E n o = o.volumeForm :=
  rfl

/--
Integration-side API audit for `THM-M-0571.integration-api-audit`.

The selected repo-local bridge is scalar Bochner integration over an explicit
finite measure.  Compactness, model-space orientation, and model volume forms
are checked adjacent anchors, but no terminal compact oriented smooth manifold
top-degree differential-form integration API is available in the current Lake
closure.
-/
def integrationApiAuditTable : List IntegrationApiAuditRow := [
  {
    requestedApi := "compact oriented smooth manifold integration target",
    checkedSurface := "`CompactSpace M`, `MeasurableSpace M`, explicit `MeasureTheory.Measure M`, and `MeasureTheory.IsFiniteMeasure μ`",
    evidence := "`CompactScalarIntegrationBoundary` validates a compact finite-measure scalar integration boundary, and `compactScalarIntegrationBoundary_integrate_eq_integral` checks that it reduces to mathlib's Bochner integral.",
    repoLocalStatus := "local_wrapper_upstream_mathlib_partial_anchor",
    localIndexRole := "Selected interim integration API for scalar densities extracted from a future top-degree form.",
    blocker := "No canonical orientation-derived manifold measure, density bundle, or top-degree smooth manifold form integration API is present locally."
  },
  {
    requestedApi := "Bochner integration of scalar densities",
    checkedSurface := "Mathlib.MeasureTheory.Integral.Bochner.Basic",
    evidence := "`scalarDensityIntegral_apply` checks the chosen implementation against `MeasureTheory.integral`, notation `∫ x, f x ∂μ`.",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localIndexRole := "Can integrate a real-valued characteristic-density function once a concrete finite measure is supplied.",
    blocker := "This integrates scalar functions, not differential forms; top-degree-form-to-density conversion is not supplied."
  },
  {
    requestedApi := "compactness and finite-measure control",
    checkedSurface := "Mathlib.Topology compactness plus Mathlib.MeasureTheory finite-measure typeclasses",
    evidence := "`CompactScalarIntegrationBoundary` requires `[CompactSpace M]` and stores an explicit `MeasureTheory.IsFiniteMeasure measure` witness.",
    repoLocalStatus := "local_wrapper_upstream_mathlib_partial_anchor",
    localIndexRole := "Captures the compactness/finite-volume side needed for integrating local index densities.",
    blocker := "Compactness does not by itself produce the geometric measure or orientation-normalized density required by the local index theorem."
  },
  {
    requestedApi := "orientation and top-degree model forms",
    checkedSurface := "Mathlib.LinearAlgebra.Orientation and Mathlib.Analysis.InnerProductSpace.Orientation",
    evidence := "`modelOrientationVolumeForm_eq` checks `Orientation.volumeForm : E [⋀^Fin n]→ₗ[ℝ] ℝ` for an oriented finite-dimensional real inner product model space.",
    repoLocalStatus := "local_wrapper_upstream_mathlib_partial_anchor",
    localIndexRole := "Provides model-vector-space orientation and a top-degree alternating form anchor.",
    blocker := "This is not a manifold orientation sheaf/atlas compatibility API and is not connected to differential-form integration over `M`."
  },
  {
    requestedApi := "top-degree differential forms on compact oriented manifolds",
    checkedSurface := "Mathlib.Analysis.Calculus.DifferentialForm.Basic plus manifold and measure-theory searches",
    evidence := "`DifferentialForm.Basic` represents unbundled normed-space forms and its TODO says bundled smooth forms on normed spaces and manifolds are not yet defined; no located declaration integrates manifold top-degree forms.",
    repoLocalStatus := "formalization_debt",
    localIndexRole := "This is the terminal API needed for the local index theorem's characteristic-density side.",
    blocker := "Need a bundled smooth manifold `n`-form API, orientation/volume-density bridge, compact-support or compact-manifold integration, and Stokes/de Rham compatibility."
  },
  {
    requestedApi := "external Lean 4 integration/top-degree-form package",
    checkedSurface := "Formalizations/Lean/lakefile.lean and lake-manifest.json",
    evidence := "The repo-local dependency closure contains pinned mathlib and `flt-regular`; no external Lean 4 package for oriented-manifold top-degree-form integration or local index density is pinned/imported.",
    repoLocalStatus := "not_repo_local_closed",
    localIndexRole := "Would be the path to `external_upstream_pinned` if a real integration API/proof were found.",
    blocker := "No external top-degree-form integration proof/API is currently inside the repo-local Lake closure, so this child records formalization blockers rather than completed repo-local integration debt."
  }
]

/-- The C005 integration API audit covers each requested integration-side family. -/
theorem integrationApiAuditTable_length :
    integrationApiAuditTable.length = 6 :=
  rfl

/-- Search strings used for the integration API audit. -/
def integrationApiAuditSearchTerms : List String := [
  "MeasureTheory.integral",
  "Bochner integral",
  "CompactSpace",
  "IsFiniteMeasure",
  "Orientation",
  "Orientation.volumeForm",
  "Module.Oriented",
  "manifold orientation",
  "oriented manifold",
  "volume form",
  "top-degree differential form",
  "integral differential form"
]

/--
Machine-readable gate result for C005.

The chosen repo-local bridge is validated only for scalar densities over an
explicit finite measure.  There is no completed external Lean 4 proof/API for
compact oriented smooth manifold top-degree-form integration inside the
repo-local Lake closure, so no completed state retains repo-local integration
debt.
-/
def integrationApiRepoLocalIntegrationDebtGate : String :=
  "pass: selected scalar-density Bochner integration as a checked partial bridge; no completed theorem claim and no external top-degree-form manifold integration proof/API is present in the repo-local Lake closure; remaining debt is formalization_debt/not_repo_local_closed."

structure ExternalProofSearchAuditRow where
  searchSurface : String
  searchTerms : List String
  evidence : String
  candidateRepository : String
  candidateCommit : String
  candidateModulePath : String
  candidateTheoremNames : List String
  repoLocalAction : String
  blocker : String

/-- Exact C006 external-proof-search terms requested for THM-M-0571. -/
def externalProofSearchRequestedTerms : List String := [
  "AtiyahSinger",
  "Atiyah_Singer",
  "IndexTheorem",
  "LocalIndexTheorem",
  "DiracOperator",
  "Fredholm",
  "EllipticOperator",
  "Pseudodifferential",
  "Ahat",
  "Pontryagin",
  "ChernCharacter",
  "indexDensity",
  "heatKernel"
]

/--
External proof-search audit for `THM-M-0571.external-proof-search`.

The authenticated GitHub code-search requirement is not closed in this local
process: `gh auth status` reports no logged-in host and `GH_TOKEN` /
`GITHUB_TOKEN` are unset.  Public fallback searches and the repo-local Lake
closure did not locate a terminal Lean 4 local index theorem proof body.  The
one concrete external `heatKernel` candidate below proves only the one
dimensional heat equation for a scalar kernel, so it is not a pin/import/check
candidate for the local index theorem.
-/
def externalProofSearchAuditTable : List ExternalProofSearchAuditRow := [
  {
    searchSurface := "repo-local Lake dependency closure",
    searchTerms := externalProofSearchRequestedTerms,
    evidence := "Search over the pinned Lake closure, including mathlib @ 8a178386ffc0f5fef0b77738bb5449d50efeea95 and flt-regular @ 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27, found no terminal local index theorem proof body.",
    candidateRepository := "not applicable",
    candidateCommit := "not applicable",
    candidateModulePath := "not applicable",
    candidateTheoremNames := [],
    repoLocalAction := "nothing to pin/import/check",
    blocker := "LocalIndexTheoremData remains abstract; no external upstream proof body is already in the repo-local closure."
  },
  {
    searchSurface := "authenticated GitHub code search",
    searchTerms := externalProofSearchRequestedTerms,
    evidence := "`gh auth status` reports no logged-in GitHub host; `GH_TOKEN` and `GITHUB_TOKEN` are unset; an unauthenticated REST code-search probe cannot satisfy the authenticated-search gate.",
    candidateRepository := "not accepted from this blocked authenticated surface",
    candidateCommit := "not applicable",
    candidateModulePath := "not applicable",
    candidateTheoremNames := [],
    repoLocalAction := "do not pin/import/check from this blocked surface",
    blocker := "Rerun GitHub code search after `gh auth login` or a valid token, then inspect any hits for non-placeholder Lean proof bodies before any completion claim."
  },
  {
    searchSurface := "public GitHub/web fallback search",
    searchTerms := externalProofSearchRequestedTerms,
    evidence := "Public web/repository searches for the exact local-index terms did not locate a terminal Lean 4 proof body for the local index theorem.",
    candidateRepository := "none located",
    candidateCommit := "not applicable",
    candidateModulePath := "not applicable",
    candidateTheoremNames := [],
    repoLocalAction := "nothing to pin/import/check",
    blocker := "Fallback public search is not a substitute for the authenticated GitHub gate and found no terminal proof candidate."
  },
  {
    searchSurface := "Reservoir package search surface",
    searchTerms := externalProofSearchRequestedTerms,
    evidence := "Reservoir package-page/public search checks did not identify a Lean package advertising a terminal local index theorem, Atiyah-Singer proof, elliptic Fredholm index package, or characteristic-density theorem for these exact terms.",
    candidateRepository := "none located",
    candidateCommit := "not applicable",
    candidateModulePath := "not applicable",
    candidateTheoremNames := [],
    repoLocalAction := "nothing to pin/import/check",
    blocker := "No Reservoir package candidate was available for Lake integration in this pass."
  },
  {
    searchSurface := "external heat-kernel candidate audit",
    searchTerms := ["heatKernel"],
    evidence := "weiran-sun/pde documents `Heat.heatKernel_solves_heat_eq` for the one-dimensional scalar heat equation.",
    candidateRepository := "https://github.com/weiran-sun/pde",
    candidateCommit := "0b37f095c5ac3571084f5ea47f0435884452d86a",
    candidateModulePath := "PDE/Basics/Heat/HeatKernel.lean",
    candidateTheoremNames := [
      "Heat.heatKernel",
      "Heat.integral_heatKernel_one_gaussian",
      "Heat.heatKernel_solves_heat_eq"
    ],
    repoLocalAction := "not pinned: adjacent heat-equation evidence only",
    blocker := "This package has no elliptic operator, Dirac operator, Fredholm index, characteristic density, or local index theorem statement, so it is not a real proof body for THM-M-0571."
  }
]

/-- The C006 external proof search records the five available audit surfaces. -/
theorem externalProofSearchAuditTable_length :
    externalProofSearchAuditTable.length = 5 :=
  rfl

structure ExternalProofSearchGate where
  authenticatedGitHubCodeSearchRan : Bool
  publicFallbackSearchRan : Bool
  reservoirSearchRan : Bool
  verifiedExternalLean4ClosureFound : Bool
  closurePinnedOrVendored : Bool
  closureImportedInRepo : Bool
  repoLocalValidationPassedForClosure : Bool
  completedStateHasRepoLocalIntegrationDebt : Bool
  publicCompletionAllowed : Bool
  terminalMachineStatus : String
  terminalDebtClass : String
  integrationBlocker : String

/--
C006 M0387 integration gate for external local-index proof bodies.

No external Lean 4 local index theorem proof body is accepted in this pass, and
the authenticated GitHub search gate is still open.  Therefore there is no
repo-local integration-debt completion claim to discharge, and the parent item
must remain open under formalization debt / not repo-local closed.
-/
def externalProofSearchGate : ExternalProofSearchGate where
  authenticatedGitHubCodeSearchRan := false
  publicFallbackSearchRan := true
  reservoirSearchRan := true
  verifiedExternalLean4ClosureFound := false
  closurePinnedOrVendored := false
  closureImportedInRepo := false
  repoLocalValidationPassedForClosure := false
  completedStateHasRepoLocalIntegrationDebt := false
  publicCompletionAllowed := false
  terminalMachineStatus := "not_repo_local_closed"
  terminalDebtClass := "formalization_debt"
  integrationBlocker :=
    "authenticated GitHub code search is blocked by missing credentials; rerun with `gh auth login` or a valid token, and if a real proof body is found then pin/import/check it or record a concrete toolchain/license/dependency blocker."

/-- C006 does not permit completion from anchor-only or blocked-search evidence. -/
theorem externalProofSearchGate_noCompletion :
    externalProofSearchGate.verifiedExternalLean4ClosureFound = false ∧
      externalProofSearchGate.closurePinnedOrVendored = false ∧
      externalProofSearchGate.repoLocalValidationPassedForClosure = false ∧
      externalProofSearchGate.completedStateHasRepoLocalIntegrationDebt = false ∧
      externalProofSearchGate.publicCompletionAllowed = false := by
  exact ⟨rfl, rfl, rfl, rfl, rfl⟩

inductive LocalIndexProofBranch where
  | manifoldVectorBundleSubstrate
  | operatorFredholmIndexPackage
  | characteristicDensityPackage
  | integrationBridge
  | localHeatKernelOrSymbolProof
  | repoLocalClosureGate
  deriving DecidableEq, Repr

namespace LocalIndexProofBranch

/-- Stable branch labels for the C007 proof-tree backfill. -/
def label : LocalIndexProofBranch → String
  | manifoldVectorBundleSubstrate => "manifold/vector-bundle substrate"
  | operatorFredholmIndexPackage => "operator/Fredholm-index package"
  | characteristicDensityPackage => "characteristic-density package"
  | integrationBridge => "integration bridge"
  | localHeatKernelOrSymbolProof => "local heat-kernel or symbol proof"
  | repoLocalClosureGate => "repo-local closure gate"

end LocalIndexProofBranch

structure LocalIndexProofLeafLedger where
  branch : LocalIndexProofBranch
  leafId : String
  task : String
  budget : ℕ
  budget_le_100 : budget ≤ 100
  repoLocalStatus : String
  machineAnchor : String
  blocker : String
  terminalLocalIndexCompletionClaim : Bool

/-- Manifold and vector-bundle substrate branch ledger for C007. -/
def localIndexManifoldVectorBundleSubstrateLedger :
    List LocalIndexProofLeafLedger := [
  {
    branch := LocalIndexProofBranch.manifoldVectorBundleSubstrate
    leafId := "M0571-P01-L001"
    task := "Package boundaryless smooth manifold assumptions over ModelWithCorners, ChartedSpace, and IsManifold infinity"
    budget := 45
    budget_le_100 := by decide
    repoLocalStatus := "checked local wrapper over pinned mathlib substrate"
    machineAnchor := "SmoothManifoldBoundary"
    blocker := "Compactness, finite dimension, orientation, and analytic operator data are not supplied by this substrate leaf."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.manifoldVectorBundleSubstrate
    leafId := "M0571-P01-L002"
    task := "Record checked smooth-map and smooth-vector-bundle predicates needed by future operator bundles"
    budget := 55
    budget_le_100 := by decide
    repoLocalStatus := "checked local wrapper over pinned mathlib substrate"
    machineAnchor := "smoothManifold_isManifold_zero; contMDiff_id_on_smooth_manifold; SmoothVectorBundlePredicate"
    blocker := "No connection, differential operator, principal symbol, Clifford module, or elliptic bundle map is constructed."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.manifoldVectorBundleSubstrate
    leafId := "M0571-P01-L003"
    task := "Record homological Euler-characteristic and singular-homology anchors as adjacent topological substrate"
    budget := 60
    budget_le_100 := by decide
    repoLocalStatus := "checked local wrapper over pinned mathlib substrate"
    machineAnchor := "HomologicalComplexEulerChar; mathlibAnchorAuditTable"
    blocker := "These anchors do not identify Fredholm kernels/cokernels or the analytic index of an elliptic operator."
    terminalLocalIndexCompletionClaim := false
  }
]

/-- Operator and Fredholm-index package branch ledger for C007. -/
def localIndexOperatorFredholmIndexLedger :
    List LocalIndexProofLeafLedger := [
  {
    branch := LocalIndexProofBranch.operatorFredholmIndexPackage
    leafId := "M0571-P02-L001"
    task := "Keep the operator, ellipticity predicate, and analytic index behind explicit abstract fields"
    budget := 45
    budget_le_100 := by decide
    repoLocalStatus := "checked statement-shape boundary; formalization_debt for concrete operator APIs"
    machineAnchor := "LocalIndexTheoremData.Operator; LocalIndexTheoremData.IsElliptic; LocalIndexTheoremData.analyticIndex"
    blocker := "No repo-local elliptic differential operator, Fredholm operator structure, or analytic-index construction is available."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.operatorFredholmIndexPackage
    leafId := "M0571-P02-L002"
    task := "Audit Fredholm, principal-symbol, pseudodifferential, Dirac, kernel/cokernel, and analytic-index surfaces"
    budget := 80
    budget_le_100 := by decide
    repoLocalStatus := "checked audit table; mostly formalization_debt"
    machineAnchor := "operatorApiAuditTable; operatorApiAuditTable_length"
    blocker := "Positive kernel/cokernel and Fredholm-alternative anchors remain adjacent only and do not close the elliptic Fredholm index theorem."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.operatorFredholmIndexPackage
    leafId := "M0571-P02-L003"
    task := "Gate operator-side completion against repo-local dependency closure"
    budget := 35
    budget_le_100 := by decide
    repoLocalStatus := "checked non-completion gate"
    machineAnchor := "operatorApiAuditRepoLocalIntegrationDebtGate"
    blocker := "A future concrete operator package must be locally proved or pinned/imported/checked before this branch can close."
    terminalLocalIndexCompletionClaim := false
  }
]

/-- Characteristic-density package branch ledger for C007. -/
def localIndexCharacteristicDensityLedger :
    List LocalIndexProofLeafLedger := [
  {
    branch := LocalIndexProofBranch.characteristicDensityPackage
    leafId := "M0571-P03-L001"
    task := "Keep index density and characteristic density as explicit abstract fields in the statement-shape boundary"
    budget := 40
    budget_le_100 := by decide
    repoLocalStatus := "checked statement-shape boundary; formalization_debt for concrete characteristic densities"
    machineAnchor := "LocalIndexTheoremData.indexDensity; LocalIndexTheoremData.characteristicDensity"
    blocker := "No Chern-Weil, Chern character, Todd, A-hat, Pontryagin, or normalization theorem is constructed."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.characteristicDensityPackage
    leafId := "M0571-P03-L002"
    task := "Audit differential forms, de Rham cohomology, characteristic classes, top-degree forms, and normalization surfaces"
    budget := 90
    budget_le_100 := by decide
    repoLocalStatus := "checked audit table; partial differential-form anchor only"
    machineAnchor := "NormedSpaceDifferentialForm; characteristicClassApiAuditTable; characteristicClassApiAuditTable_length"
    blocker := "The available differential-form substrate is normed-space local calculus, not a manifold de Rham/characteristic-class density package."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.characteristicDensityPackage
    leafId := "M0571-P03-L003"
    task := "Gate characteristic-side completion against repo-local dependency closure"
    budget := 35
    budget_le_100 := by decide
    repoLocalStatus := "checked non-completion gate"
    machineAnchor := "characteristicClassApiRepoLocalIntegrationDebtGate"
    blocker := "A future characteristic-class density package must be locally proved or pinned/imported/checked before this branch can close."
    terminalLocalIndexCompletionClaim := false
  }
]

/-- Integration bridge branch ledger for C007. -/
def localIndexIntegrationBridgeLedger :
    List LocalIndexProofLeafLedger := [
  {
    branch := LocalIndexProofBranch.integrationBridge
    leafId := "M0571-P04-L001"
    task := "Select and validate scalar-density Bochner integration over an explicit finite measure as the interim bridge"
    budget := 55
    budget_le_100 := by decide
    repoLocalStatus := "checked local wrapper over pinned mathlib integration"
    machineAnchor := "ScalarDensityIntegrationFunctional; scalarDensityIntegral; scalarDensityIntegral_apply"
    blocker := "This integrates scalar functions, not top-degree differential forms on compact oriented smooth manifolds."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.integrationBridge
    leafId := "M0571-P04-L002"
    task := "Record compact finite-measure and model-orientation anchors for future top-degree-form integration"
    budget := 70
    budget_le_100 := by decide
    repoLocalStatus := "checked partial integration/orientation anchors"
    machineAnchor := "CompactScalarIntegrationBoundary; compactScalarIntegrationBoundary_integrate_eq_integral; modelOrientationVolumeForm_eq"
    blocker := "No canonical orientation-derived manifold measure, density bundle, or Stokes/de Rham compatible integration API is constructed."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.integrationBridge
    leafId := "M0571-P04-L003"
    task := "Gate integration-side completion against repo-local dependency closure"
    budget := 35
    budget_le_100 := by decide
    repoLocalStatus := "checked non-completion gate"
    machineAnchor := "integrationApiRepoLocalIntegrationDebtGate"
    blocker := "A future compact oriented manifold top-degree-form integration package must be locally proved or pinned/imported/checked before this branch can close."
    terminalLocalIndexCompletionClaim := false
  }
]

/-- Local heat-kernel or symbol proof branch ledger for C007. -/
def localIndexHeatKernelOrSymbolProofLedger :
    List LocalIndexProofLeafLedger := [
  {
    branch := LocalIndexProofBranch.localHeatKernelOrSymbolProof
    leafId := "M0571-P05-L001"
    task := "State the required local analytic proof route as either heat-kernel asymptotics or symbol/parametrix calculus"
    budget := 75
    budget_le_100 := by decide
    repoLocalStatus := "unchecked formalization_debt recorded by checked ledger"
    machineAnchor := "absentTerminalSearchTerms; externalProofSearchRequestedTerms"
    blocker := "No heat-kernel asymptotic expansion, supertrace local density theorem, pseudodifferential parametrix, or symbol-index proof is present locally."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.localHeatKernelOrSymbolProof
    leafId := "M0571-P05-L002"
    task := "Reject adjacent scalar heat-equation evidence as a local index theorem proof body"
    budget := 55
    budget_le_100 := by decide
    repoLocalStatus := "checked external-candidate non-closure audit"
    machineAnchor := "externalProofSearchAuditTable; externalProofSearchAuditTable_length"
    blocker := "The inspected `heatKernel` candidate proves a scalar heat-equation fact, not an elliptic operator index-density theorem."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.localHeatKernelOrSymbolProof
    leafId := "M0571-P05-L003"
    task := "Keep the pointwise density formula as data until the analytic proof package exists"
    budget := 45
    budget_le_100 := by decide
    repoLocalStatus := "checked statement-shape boundary; formalization_debt for proof body"
    machineAnchor := "LocalIndexTheoremData.local_density_formula; LocalIndexDensityFormula"
    blocker := "The equality is an abstract field in this Stage1 boundary, not a derived heat-kernel or symbol-calculus theorem."
    terminalLocalIndexCompletionClaim := false
  }
]

/-- Repo-local closure gate branch ledger for C007. -/
def localIndexRepoLocalClosureGateLedger :
    List LocalIndexProofLeafLedger := [
  {
    branch := LocalIndexProofBranch.repoLocalClosureGate
    leafId := "M0571-P06-L001"
    task := "Record that blocked or negative external-search evidence is not a completion source"
    budget := 45
    budget_le_100 := by decide
    repoLocalStatus := "checked non-completion gate"
    machineAnchor := "externalProofSearchGate; externalProofSearchGate_noCompletion"
    blocker := "Authenticated GitHub code search remains blocked by missing credentials, and no accepted external Lean 4 proof body is pinned."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.repoLocalClosureGate
    leafId := "M0571-P06-L002"
    task := "Require any future external proof body to be pinned or vendored, imported, and repo-locally validated"
    budget := 50
    budget_le_100 := by decide
    repoLocalStatus := "checked process gate"
    machineAnchor := "ExternalProofSearchGate.closurePinnedOrVendored; ExternalProofSearchGate.repoLocalValidationPassedForClosure"
    blocker := "No external upstream local index theorem proof body is currently in the Lake closure."
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.repoLocalClosureGate
    leafId := "M0571-P06-L003"
    task := "Close the terminal theorem only by local proof body, pinned mathlib wrapper, or pinned/imported external dependency"
    budget := 100
    budget_le_100 := by decide
    repoLocalStatus := "unchecked formalization_debt recorded by checked ledger"
    machineAnchor := "StatementShape; LocalIndexDensityFormula"
    blocker := "The terminal local index theorem remains not_repo_local_closed; this proof-tree backfill does not prove it."
    terminalLocalIndexCompletionClaim := false
  }
]

structure LocalIndexProofBranchLedger where
  branch : LocalIndexProofBranch
  branchSummary : String
  leaves : List LocalIndexProofLeafLedger
  independentLeafLedger : Bool
  terminalLocalIndexCompletionClaim : Bool

/--
C007 proof-tree backfill split for `THM-M-0571.proof-tree-backfill`.

This is a checked process surface only.  It records the required six branches
and `<=100` leaf budgets, while explicitly preserving the non-completion
boundary for the terminal local index theorem.
-/
def localIndexProofTreeBackfill : List LocalIndexProofBranchLedger := [
  {
    branch := LocalIndexProofBranch.manifoldVectorBundleSubstrate
    branchSummary := "manifold/vector-bundle substrate"
    leaves := localIndexManifoldVectorBundleSubstrateLedger
    independentLeafLedger := true
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.operatorFredholmIndexPackage
    branchSummary := "operator/Fredholm-index package"
    leaves := localIndexOperatorFredholmIndexLedger
    independentLeafLedger := true
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.characteristicDensityPackage
    branchSummary := "characteristic-density package"
    leaves := localIndexCharacteristicDensityLedger
    independentLeafLedger := true
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.integrationBridge
    branchSummary := "integration bridge"
    leaves := localIndexIntegrationBridgeLedger
    independentLeafLedger := true
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.localHeatKernelOrSymbolProof
    branchSummary := "local heat-kernel or symbol proof"
    leaves := localIndexHeatKernelOrSymbolProofLedger
    independentLeafLedger := true
    terminalLocalIndexCompletionClaim := false
  },
  {
    branch := LocalIndexProofBranch.repoLocalClosureGate
    branchSummary := "repo-local closure gate"
    leaves := localIndexRepoLocalClosureGateLedger
    independentLeafLedger := true
    terminalLocalIndexCompletionClaim := false
  }
]

/-- The C007 split has exactly the six branches requested by the child task. -/
theorem localIndexProofTreeBackfill_length :
    localIndexProofTreeBackfill.length = 6 :=
  rfl

/--
C007 non-completion gate: proof-tree backfill exists, but it does not claim the
terminal local index theorem.
-/
def localIndexProofTreeBackfillClaimsTerminalCompletion : Bool :=
  localIndexProofTreeBackfill.any
    (fun branch => branch.terminalLocalIndexCompletionClaim)

/--
M0387 repo-local integration-debt gate for C007.  The proof-tree split records
open formalization debt; it does not leave anchor-only external evidence in a
completed state.
-/
def localIndexProofTreeRepoLocalIntegrationDebtRetainedInCompletedState :
    Bool :=
  false

/-- Checked C007 non-completion result. -/
theorem localIndexProofTreeBackfillClaimsTerminalCompletion_eq_false :
    localIndexProofTreeBackfillClaimsTerminalCompletion = false :=
  rfl

/-- Checked C007 repo-local integration-debt gate. -/
theorem localIndexProofTreeRepoLocalIntegrationDebtRetained_eq_false :
    localIndexProofTreeRepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-! ## Audit probes -/

#check IsManifold
#check BoundarylessManifold
#check ContMDiff
#check VectorBundle
#check ContMDiffVectorBundle
#check HomologicalComplex.eulerChar
#check TopCat.toSSet
#check AlgebraicTopology.SSet.singularChainComplexFunctor
#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor
#check mathlibAnchorAuditRevision
#check mathlibAnchorAuditTable
#check mathlibAnchorAuditTable_length
#check StatementShape
#check IsCompactOperator
#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet
#check CategoryTheory.Limits.HasKernel
#check CategoryTheory.Limits.HasCokernel
#check CategoryTheory.Limits.kernel
#check CategoryTheory.Limits.cokernel
#check operatorApiAuditTable
#check operatorApiAuditTable_length
#check operatorApiAuditRepoLocalIntegrationDebtGate
#check extDeriv
#check extDerivWithin
#check extDeriv_apply
#check extDerivWithin_extDerivWithin_apply
#check NormedSpaceDifferentialForm
#check characteristicClassApiAuditTable
#check characteristicClassApiAuditTable_length
#check characteristicClassApiRepoLocalIntegrationDebtGate
#check MeasureTheory.integral
#check CompactSpace
#check MeasureTheory.IsFiniteMeasure
#check Orientation
#check Orientation.volumeForm
#check ScalarDensityIntegrationFunctional
#check scalarDensityIntegral
#check scalarDensityIntegral_apply
#check CompactScalarIntegrationBoundary
#check CompactScalarIntegrationBoundary.integrate
#check compactScalarIntegrationBoundary_integrate_eq_integral
#check ModelTopDegreeAlternatingForm
#check modelOrientationVolumeForm
#check modelOrientationVolumeForm_eq
#check integrationApiAuditTable
#check integrationApiAuditTable_length
#check integrationApiRepoLocalIntegrationDebtGate
#check externalProofSearchRequestedTerms
#check externalProofSearchAuditTable
#check externalProofSearchAuditTable_length
#check externalProofSearchGate
#check externalProofSearchGate_noCompletion
#check LocalIndexProofBranch
#check LocalIndexProofLeafLedger
#check localIndexProofTreeBackfill
#check localIndexProofTreeBackfill_length
#check localIndexProofTreeBackfillClaimsTerminalCompletion_eq_false
#check localIndexProofTreeRepoLocalIntegrationDebtRetained_eq_false

end S1_M_118
end Stage1
end AwesomeTheorems
