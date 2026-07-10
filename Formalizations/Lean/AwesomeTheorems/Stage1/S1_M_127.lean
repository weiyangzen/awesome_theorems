import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Geometry.Manifold.MFDeriv.SpecificFunctions
import Mathlib.Geometry.Manifold.VectorBundle.SmoothSection
import Mathlib.Geometry.Manifold.VectorBundle.Tangent

/-!
# S1-M-127 / THM-M-0173: Atiyah-Singer index theorem

This Stage1 artifact records a conservative Lean boundary for the
Atiyah-Singer index theorem: the analytic index of an elliptic operator equals
its topological index.

The pinned mathlib snapshot has smooth-manifold, tangent-bundle, vector-bundle,
smooth-section, and compact-operator spectral substrate.  The declarations
below therefore model the operator carrier as a map between bundled smooth
sections of smooth vector bundles.  The audit did not locate native APIs for
finite-jet differential operators, principal symbols, ellipticity, Fredholm
index, K-theoretic pushforward, characteristic classes, or the Atiyah-Singer
index formula, so those layers remain explicit blockers rather than theorem
claims.
-/

noncomputable section

open scoped Manifold Topology ContDiff

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_127

universe uM uS uK u𝕜 uE uH uF₁ uF₂ uV₁ uV₂ uX

/--
Concrete Stage1 carrier for a differential operator between smooth sections of
two smooth vector bundles over the same smooth real manifold.

The `toFun` field is no longer an abstract `Operator : Type`: it is a genuine
Lean function from `C^∞` sections of the source bundle to `C^∞` sections of the
target bundle, using mathlib's `ContMDiffSection`.  The final two proposition
fields record the exact remaining mathlib gap: this pinned dependency closure
does not provide a native finite-jet/differential-operator API or a principal
symbol API that could make ellipticity a checked, non-abstract predicate.
-/
structure SmoothSectionDifferentialOperator
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
    {H : Type uH} [TopologicalSpace H]
    (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace Real F₁]
    (V₁ : M -> Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module Real (V₁ x)]
    [VectorBundle Real F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace Real F₂]
    (V₂ : M -> Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module Real (V₂ x)]
    [VectorBundle Real F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I] where
  order : ℕ
  toFun : ContMDiffSection I F₁ ∞ V₁ -> ContMDiffSection I F₂ ∞ V₂
  locallyFiniteJetDetermined : Prop
  principalSymbolObjectAvailable : Prop

/--
Checked projection: the concrete operator carrier sends smooth sections to
smooth sections by construction.
-/
theorem smoothSectionDifferentialOperator_maps_smooth_sections
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners Real E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace Real F₁]
    {V₁ : M -> Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module Real (V₁ x)]
    [VectorBundle Real F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace Real F₂]
    {V₂ : M -> Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module Real (V₂ x)]
    [VectorBundle Real F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (P : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂)
    (s : ContMDiffSection I F₁ ∞ V₁) :
    CMDiff ∞ (T% fun x => P.toFun s x) :=
  (P.toFun s).contMDiff

/--
Data needed to state the Atiyah-Singer index theorem on a compact smooth
manifold after replacing the old abstract `Operator : Type` boundary.

`SymbolClass` and `KTheoryClass` remain abstract because the pinned mathlib
closure still lacks the principal-symbol/K-theory pushforward API needed for a
native topological index.
-/
structure AtiyahSingerIndexData
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
    {H : Type uH} [TopologicalSpace H]
    (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace Real F₁]
    (V₁ : M -> Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module Real (V₁ x)]
    [VectorBundle Real F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace Real F₂]
    (V₂ : M -> Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module Real (V₂ x)]
    [VectorBundle Real F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I] where
  SymbolClass : Type uS
  KTheoryClass : Type uK
  analyticIndex : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Int
  topologicalIndex : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Int
  principalSymbol : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> SymbolClass
  symbolKClass : SymbolClass -> KTheoryClass
  isElliptic : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Prop
  isFredholm : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Prop
  symbolClassInvertibleOffZeroSection :
    SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Prop
  topologicalPushforwardDefined :
    SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Prop
  analyticIndexAgreesWithFredholmIndex :
    SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Prop
  topologicalIndexAgreesWithSymbolPushforward :
    SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂ -> Prop

/--
Single-operator formula shape for Atiyah-Singer.

The hypotheses split the analytic Fredholm branch from the symbol/K-theory
branch.  The conclusion is the expected equality between the analytic and
topological indices.
-/
def AtiyahSingerIndexFormula
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners Real E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace Real F₁]
    {V₁ : M -> Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module Real (V₁ x)]
    [VectorBundle Real F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace Real F₂]
    {V₂ : M -> Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module Real (V₂ x)]
    [VectorBundle Real F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (D : AtiyahSingerIndexData I M F₁ V₁ F₂ V₂)
    (P : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂) : Prop :=
  D.isElliptic P ->
    D.isFredholm P ->
      D.symbolClassInvertibleOffZeroSection P ->
        D.topologicalPushforwardDefined P ->
          D.analyticIndexAgreesWithFredholmIndex P ->
            D.topologicalIndexAgreesWithSymbolPushforward P ->
              D.analyticIndex P = D.topologicalIndex P

/--
Stage1 normalized statement-shape candidate for the Atiyah-Singer index
theorem over a compact smooth real manifold.

The compact smooth manifold hypotheses are concrete mathlib hypotheses.  The
operator carrier is now a concrete map between smooth vector bundle sections.
The finite-jet/principal-symbol witness, ellipticity, Fredholm index, symbol
class, K-theory class, and topological index remain explicit formalization
boundaries because no terminal repo-local or pinned mathlib theorem was located
for the full theorem.
-/
def StatementShape
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [CompactSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace Real F₁]
    (V₁ : M -> Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module Real (V₁ x)]
    [VectorBundle Real F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace Real F₂]
    (V₂ : M -> Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module Real (V₂ x)]
    [VectorBundle Real F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (D : AtiyahSingerIndexData I M F₁ V₁ F₂ V₂) : Prop :=
  forall P : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂,
    D.isElliptic P -> AtiyahSingerIndexFormula D P

/-- The normalized statement shape unfolds to the per-operator formula. -/
theorem statementShape_iff_forall_operator
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [CompactSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace Real F₁]
    (V₁ : M -> Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module Real (V₁ x)]
    [VectorBundle Real F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace Real F₂]
    (V₂ : M -> Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module Real (V₂ x)]
    [VectorBundle Real F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (D : AtiyahSingerIndexData I M F₁ V₁ F₂ V₂) :
    StatementShape E H I M F₁ V₁ F₂ V₂ D <->
      forall P : SmoothSectionDifferentialOperator I M F₁ V₁ F₂ V₂,
        D.isElliptic P -> AtiyahSingerIndexFormula D P :=
  Iff.rfl

/--
The five formal theorem variants considered for the Atiyah-Singer Stage1 slot.

This is a statement-normalization choice, not a proof of any branch.
-/
inductive AtiyahSingerFormalVariant where
  | generalEllipticComplex
  | singleEllipticOperator
  | diracTypeOperator
  | heatKernelLocalIndexTheorem
  | kTheoreticTopologicalIndex
deriving Repr, DecidableEq

/-- The complete C006 candidate list, kept as checked data. -/
def atiyahSingerFormalVariantCandidates : List AtiyahSingerFormalVariant := [
  .generalEllipticComplex,
  .singleEllipticOperator,
  .diracTypeOperator,
  .heatKernelLocalIndexTheorem,
  .kTheoreticTopologicalIndex
]

/--
Decision record for child task S1-M-127-C006.

The selected Stage1 variant is the single elliptic operator theorem: an
elliptic differential operator between smooth vector-bundle sections on a
compact smooth manifold has equal analytic and topological indices.  The other
variants remain future refinements or proof-method branches.
-/
structure AtiyahSingerVariantDecision where
  childTask : String
  chosenVariant : AtiyahSingerFormalVariant
  leanStatementBoundary : String
  generalEllipticComplexStatus : String
  diracTypeOperatorStatus : String
  heatKernelLocalIndexStatus : String
  kTheoreticTopologicalIndexStatus : String
  completionClaimAllowed : Bool
  repoLocalIntegrationDebtRetained : Bool
deriving Repr

/-- C006 decision: use the single elliptic operator formulation as the canonical Stage1 target. -/
def intendedFormalVariantDecision : AtiyahSingerVariantDecision := {
  childTask := "S1-M-127-C006",
  chosenVariant := .singleEllipticOperator,
  leanStatementBoundary :=
    "AwesomeTheorems.Stage1.S1_M_127.StatementShape",
  generalEllipticComplexStatus :=
    "not selected for Stage1; requires a chain-complex/elliptic-complex API over smooth vector bundle sections",
  diracTypeOperatorStatus :=
    "not selected as the canonical parent theorem; future specialization after Clifford/Dirac operator APIs exist",
  heatKernelLocalIndexStatus :=
    "not selected as the canonical parent theorem; future proof-method branch requiring heat kernels and local index density",
  kTheoreticTopologicalIndexStatus :=
    "not selected as a standalone theorem; kept as the topological-index branch inside the single-operator formula",
  completionClaimAllowed := false,
  repoLocalIntegrationDebtRetained := false
}

/-- C006 considered exactly the five requested formal theorem variants. -/
theorem atiyahSingerFormalVariantCandidates_length :
    atiyahSingerFormalVariantCandidates.length = 5 :=
  rfl

/-- C006 freezes the Stage1 target as the single elliptic operator variant. -/
theorem intendedFormalVariantDecision_chosen :
    intendedFormalVariantDecision.chosenVariant =
      AtiyahSingerFormalVariant.singleEllipticOperator :=
  rfl

/-- C006 is not a theorem-completion claim. -/
theorem intendedFormalVariantDecision_no_completion :
    intendedFormalVariantDecision.completionClaimAllowed = false :=
  rfl

/--
C006 does not leave a completed state with repo-local integration debt.

No external terminal Lean 4 Atiyah-Singer proof was selected by this variant
decision, and the parent remains open formalization debt rather than an
anchor-only completion.
-/
theorem intendedFormalVariantDecision_no_repo_local_integration_debt :
    intendedFormalVariantDecision.repoLocalIntegrationDebtRetained = false :=
  rfl

/-- Checked wrapper: the identity map on a charted manifold is smooth to any order. -/
theorem contMDiff_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {n : WithTop ℕ∞} :
    ContMDiff I I n (id : M -> M) :=
  contMDiff_id

/-- Checked wrapper: the tangent map of the identity is the identity on the tangent bundle. -/
theorem tangentMap_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] :
    tangentMap I I (id : M -> M) = id :=
  tangentMap_id

/-- Checked wrapper: the manifold derivative of the identity is the identity on each tangent space. -/
theorem mfderiv_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] (x : M) :
    mfderiv I I (id : M -> M) x = ContinuousLinearMap.id 𝕜 (TangentSpace I x) :=
  mfderiv_id

/--
Checked wrapper for mathlib's Fredholm alternative for compact operators.

This is an analytic substrate only; it is not a Fredholm-index theorem for
elliptic differential operators.
-/
theorem compact_operator_fredholm_alternative_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X] [CompleteSpace X]
    {T : X →L[𝕜] X} {μ : 𝕜}
    (hT : IsCompactOperator (T : X -> X)) (hμ : μ ≠ 0) :
    Module.End.HasEigenvalue (T : Module.End 𝕜 X) μ ∨ μ ∈ resolventSet 𝕜 T :=
  IsCompactOperator.hasEigenvalue_or_mem_resolventSet hT hμ

/-- Checked wrapper: nonzero spectral points of a compact operator are eigenvalues. -/
theorem compact_operator_hasEigenvalue_iff_mem_spectrum_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X] [CompleteSpace X]
    {T : X →L[𝕜] X} {μ : 𝕜}
    (hT : IsCompactOperator (T : X -> X)) (hμ : μ ≠ 0) :
    Module.End.HasEigenvalue (T : Module.End 𝕜 X) μ <-> μ ∈ spectrum 𝕜 T :=
  IsCompactOperator.hasEigenvalue_iff_mem_spectrum hT hμ

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.MFDeriv.SpecificFunctions",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Bordism",
  "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
  "Mathlib.Analysis.Normed.Operator.Compact",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.AlgebraicTopology.SingularHomology.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ContMDiff",
  "ContMDiffSection",
  "ContMDiffVectorBundle",
  "Bundle.TotalSpace",
  "contMDiff_id",
  "tangentMap",
  "tangentMap_id",
  "mfderiv",
  "mfderiv_id",
  "TangentSpace",
  "IsCompactOperator",
  "IsCompactOperator.hasEigenvalue_or_mem_resolventSet",
  "IsCompactOperator.hasEigenvalue_iff_mem_spectrum",
  "resolventSet",
  "spectrum"
]

/-- Search terms that did not locate a terminal Atiyah-Singer theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Atiyah",
  "Singer",
  "Atiyah-Singer",
  "AtiyahSinger",
  "index theorem",
  "IndexTheorem",
  "elliptic operator",
  "Dirac operator",
  "Fredholm operator",
  "Fredholm index",
  "finite jet",
  "jet bundle",
  "principal symbol",
  "Chern character",
  "Todd class",
  "A-hat class",
  "KTheory"
]

/-- Pinned mathlib revision used for the Stage1 machine audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
One row of the machine audit table for the Atiyah-Singer Stage1 substrate.

The fields are strings because this table records module-level audit evidence
and negative API search results, while theorem-level claims are represented
separately by checked wrappers above.
-/
structure MathlibMachineAuditRow where
  moduleName : String
  auditedSubstrate : String
  checkedAnchors : List String
  repoLocalEvidence : String
  machineStatus : String
  debtClass : String
deriving Repr

/--
Machine audit table for the mathlib manifold/vector-bundle/Fredholm substrate
at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Rows marked `local_wrapper_upstream_mathlib` have a wrapper theorem in this
file.  Rows marked `imported_or_audited_substrate_only` are usable substrate
or documented gaps, not terminal Atiyah-Singer proof bodies.
-/
def mathlibMachineAuditTable : List MathlibMachineAuditRow := [
  {
    moduleName := "Mathlib.Geometry.Manifold.MFDeriv.SpecificFunctions",
    auditedSubstrate := "smooth manifold identity/tangent/mfderiv API",
    checkedAnchors := [
      "contMDiff_id",
      "tangentMap_id",
      "mfderiv_id"
    ],
    repoLocalEvidence :=
      "wrapped by contMDiff_id_mathlib_wrapper, tangentMap_id_mathlib_wrapper, and mfderiv_id_mathlib_wrapper",
    machineStatus := "local_wrapper_upstream_mathlib",
    debtClass := "none_for_this_substrate"
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
    auditedSubstrate := "smooth vector-bundle sections",
    checkedAnchors := [
      "ContMDiffSection",
      "ContMDiffSection.contMDiff"
    ],
    repoLocalEvidence :=
      "SmoothSectionDifferentialOperator.toFun maps ContMDiffSection to ContMDiffSection; smoothSectionDifferentialOperator_maps_smooth_sections checks the smoothness projection",
    machineStatus := "local_proof_body_for_statement_shape",
    debtClass := "formalization_debt_for_finite_jet_differential_operator_layer"
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
    auditedSubstrate := "tangent bundle and tangent-space API",
    checkedAnchors := [
      "tangentMap",
      "TangentSpace",
      "ContinuousLinearMap.id"
    ],
    repoLocalEvidence :=
      "used by tangentMap_id_mathlib_wrapper and mfderiv_id_mathlib_wrapper",
    machineStatus := "local_wrapper_upstream_mathlib",
    debtClass := "none_for_this_substrate"
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
    auditedSubstrate := "covariant derivative and documented 1-jet boundary",
    checkedAnchors := [
      "CovariantDerivative",
      "documented TODO: dependence only via the 1-jet"
    ],
    repoLocalEvidence :=
      "audited as substrate only; no repo-local Atiyah-Singer wrapper depends on it",
    machineStatus := "imported_or_audited_substrate_only",
    debtClass := "formalization_debt_for_native_finite_jet_api"
  },
  {
    moduleName := "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
    auditedSubstrate := "compact-operator Fredholm alternative and spectral anchors",
    checkedAnchors := [
      "IsCompactOperator.hasEigenvalue_or_mem_resolventSet",
      "IsCompactOperator.hasEigenvalue_iff_mem_spectrum",
      "resolventSet",
      "spectrum"
    ],
    repoLocalEvidence :=
      "wrapped by compact_operator_fredholm_alternative_mathlib_wrapper and compact_operator_hasEigenvalue_iff_mem_spectrum_mathlib_wrapper",
    machineStatus := "local_wrapper_upstream_mathlib",
    debtClass := "formalization_debt_for_Fredholm_operator_index_API"
  },
  {
    moduleName := "pinned mathlib global search",
    auditedSubstrate := "terminal Atiyah-Singer/Fredholm-index/K-theory-index APIs",
    checkedAnchors := absentTerminalSearchTerms,
    repoLocalEvidence :=
      "no repo-local importable theorem or definition was located for AtiyahSinger, FredholmIndex, EllipticOperator, AnalyticIndex, TopologicalIndex, principal symbol, or K-theory topological pushforward",
    machineStatus := "not_repo_local_closed",
    debtClass := "formalization_debt"
  }
]

/-- Public Lean 4 repository search terms required by child task S1-M-127-C003. -/
def externalLeanAuditSearchTerms : List String := [
  "AtiyahSinger",
  "Atiyah-Singer",
  "IndexTheorem",
  "FredholmIndex",
  "EllipticOperator",
  "TopologicalIndex",
  "AnalyticIndex"
]

/--
One row of the child-task public Lean 4 repository audit.

String fields are used because the negative audit evidence records repository
search metadata and integration feasibility, not theorem-level declarations.
-/
structure ExternalLeanRepositoryAuditRow where
  searchTerm : String
  repositoryURL : String
  commit : String
  modulePath : String
  theoremNames : List String
  lakeCompatibility : String
  auditResult : String
deriving Repr

/--
External public Lean 4 audit for child task S1-M-127-C003 on 2026-05-01.

Available authenticated GitHub code search was blocked because `gh auth status`
reported no logged-in GitHub host and the REST code-search endpoint returned
`Requires authentication`.  Unauthenticated GitHub repository search and public
Reservoir/web searches did not identify a terminal Lean 4 Atiyah-Singer proof
for the required exact terms.  Therefore this table records no external
upstream proof body and intentionally introduces no `external_upstream_anchor_only`
completion claim.
-/
def externalLeanRepositoryAuditTable : List ExternalLeanRepositoryAuditRow := [
  {
    searchTerm := "AtiyahSinger",
    repositoryURL := "none located by available unauthenticated public repository/search audit",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    lakeCompatibility := "not applicable; no candidate Lean 4 package located",
    auditResult := "no terminal public Lean 4 Atiyah-Singer theorem candidate found"
  },
  {
    searchTerm := "Atiyah-Singer",
    repositoryURL := "none located by available unauthenticated public repository/search audit",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    lakeCompatibility := "not applicable; no candidate Lean 4 package located",
    auditResult := "no terminal public Lean 4 Atiyah-Singer theorem candidate found"
  },
  {
    searchTerm := "IndexTheorem",
    repositoryURL := "none located by available unauthenticated public repository/search audit",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    lakeCompatibility := "not applicable; no candidate Lean 4 package located",
    auditResult := "no terminal public Lean 4 index theorem candidate for Atiyah-Singer found"
  },
  {
    searchTerm := "FredholmIndex",
    repositoryURL := "none located by available unauthenticated public repository/search audit",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    lakeCompatibility := "not applicable; no candidate Lean 4 package located",
    auditResult := "no terminal public Lean 4 Fredholm-index API/proof candidate for elliptic operators found"
  },
  {
    searchTerm := "EllipticOperator",
    repositoryURL := "none located by available unauthenticated public repository/search audit",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    lakeCompatibility := "not applicable; no candidate Lean 4 package located",
    auditResult := "no terminal public Lean 4 elliptic-operator API/proof candidate found"
  },
  {
    searchTerm := "TopologicalIndex",
    repositoryURL := "none located by available unauthenticated public repository/search audit",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    lakeCompatibility := "not applicable; no candidate Lean 4 package located",
    auditResult := "no terminal public Lean 4 topological-index candidate found"
  },
  {
    searchTerm := "AnalyticIndex",
    repositoryURL := "none located by available unauthenticated public repository/search audit",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    lakeCompatibility := "not applicable; no candidate Lean 4 package located",
    auditResult := "no terminal public Lean 4 analytic-index candidate found"
  }
]

/--
Repo-local integration gate for child task S1-M-127-C004.

This records whether an external Lean 4 proof candidate has actually reached
the threshold where the repository must pin/import/check it or record a concrete
integration blocker.  The current audit found no such candidate, so the gate is
open as formalization debt rather than completed from anchor-only evidence.
-/
structure ExternalProofIntegrationGate where
  childTask : String
  externalProofFound : Bool
  candidateRepositoryURL : String
  candidateCommit : String
  candidateModulePath : String
  candidateTheoremNames : List String
  repoLocalAction : String
  integrationBlocker : String
  gateResult : String
  completionClaimAllowed : Bool
deriving Repr

/--
Child S1-M-127-C004 integration gate.

No external Lean 4 Atiyah-Singer proof body was located by the available audit,
so there is nothing to pin/import/check in this child.  This is not a completion
claim for the parent theorem.
-/
def externalProofIntegrationGate : ExternalProofIntegrationGate := {
  childTask := "S1-M-127-C004",
  externalProofFound := false,
  candidateRepositoryURL := "none located by available unauthenticated public repository/search audit",
  candidateCommit := "not applicable",
  candidateModulePath := "not applicable",
  candidateTheoremNames := [],
  repoLocalAction := "no pin/import/check action is available because no external Lean 4 proof candidate was found",
  integrationBlocker :=
    "authenticated GitHub code search remains an audit-coverage blocker; if a later authenticated pass finds a terminal proof, this repository must pin/import/check it locally or record a concrete incompatibility before any completion claim",
  gateResult :=
    "open_not_completed; formalization_debt remains, but no completed repo_local_integration_debt state is introduced",
  completionClaimAllowed := false
}

/--
One terminal subleaf in the C005 split of unchecked parent leaves
`AS-L010` through `AS-L027`.

The row is process metadata: it records an independent future proof obligation
with an explicit local proof-step budget.  A row marked `unchecked` is not
completion evidence for the Atiyah-Singer theorem.
-/
structure AtiyahSingerUncheckedLeafSubledgerRow where
  parentLeafId : String
  terminalLeafId : String
  packageId : String
  obligation : String
  localStepBudget : Nat
  status : String
  repoLocalClosed : Bool
  debtClass : String
  blocker : String
deriving Repr

/-- Parent leaves split by child task S1-M-127-C005. -/
def asUncheckedParentLeafIds : List String := [
  "AS-L010", "AS-L011", "AS-L012", "AS-L013", "AS-L014", "AS-L015",
  "AS-L016", "AS-L017", "AS-L018", "AS-L019", "AS-L020", "AS-L021",
  "AS-L022", "AS-L023", "AS-L024", "AS-L025", "AS-L026", "AS-L027"
]

/--
C005 sub-ledger for unchecked Atiyah-Singer leaves `AS-L010` through `AS-L027`.

Each terminal row is independently budgeted at at most 100 local proof steps,
but every row remains `unchecked` and `repoLocalClosed = false` until a real
Lean API or pinned proof dependency supplies the corresponding proof body.
-/
def asUncheckedLeafSubledger : List AtiyahSingerUncheckedLeafSubledgerRow := [
  {
    parentLeafId := "AS-L010",
    terminalLeafId := "AS-L010-a",
    packageId := "AS-P02-smooth-manifold-vector-bundle-substrate",
    obligation := "instantiate concrete source and target smooth vector bundle section spaces",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires finalized ContMDiffSection carrier and bundle hypotheses for the selected theorem variant"
  },
  {
    parentLeafId := "AS-L010",
    terminalLeafId := "AS-L010-b",
    packageId := "AS-P02-smooth-manifold-vector-bundle-substrate",
    obligation := "prove required smooth vector bundle instance plumbing for both section bundles",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires stable local-frame and smooth-vector-bundle API targets"
  },
  {
    parentLeafId := "AS-L010",
    terminalLeafId := "AS-L010-c",
    packageId := "AS-P02-smooth-manifold-vector-bundle-substrate",
    obligation := "expose source-target section map interface used by later operator leaves",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires downstream agreement on single-operator versus complex variant"
  },
  {
    parentLeafId := "AS-L011",
    terminalLeafId := "AS-L011-a",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "define finite-jet dependency for a differential operator over smooth sections",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "no native finite-jet bundle or DifferentialOperator API in the pinned closure"
  },
  {
    parentLeafId := "AS-L011",
    terminalLeafId := "AS-L011-b",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "record local-coordinate expression law for the differential operator",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires finite-jet/local-coordinate operator API"
  },
  {
    parentLeafId := "AS-L011",
    terminalLeafId := "AS-L011-c",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "prove restriction and composition compatibility for differential operators",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires sheaf/locality interface for smooth-section operators"
  },
  {
    parentLeafId := "AS-L012",
    terminalLeafId := "AS-L012-a",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "construct the cotangent-symbol bundle target for the principal symbol",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "no principal-symbol object for section differential operators is available locally"
  },
  {
    parentLeafId := "AS-L012",
    terminalLeafId := "AS-L012-b",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "define the homogeneous top-order symbol map",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires top-order finite-jet extraction"
  },
  {
    parentLeafId := "AS-L012",
    terminalLeafId := "AS-L012-c",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "prove coordinate invariance of the principal symbol",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires chart-change law for differential-operator coefficients"
  },
  {
    parentLeafId := "AS-L013",
    terminalLeafId := "AS-L013-a",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "define the zero-section complement predicate in the cotangent bundle",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires selected cotangent-bundle/symbol-bundle model"
  },
  {
    parentLeafId := "AS-L013",
    terminalLeafId := "AS-L013-b",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "define fiberwise invertibility of the principal symbol off the zero section",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires principal-symbol API and bundle morphism invertibility"
  },
  {
    parentLeafId := "AS-L013",
    terminalLeafId := "AS-L013-c",
    packageId := "AS-P03-elliptic-operator-model",
    obligation := "prove ellipticity is stable under coordinate changes and bundle trivializations",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires symbol coordinate-invariance leaf AS-L012-c"
  },
  {
    parentLeafId := "AS-L014",
    terminalLeafId := "AS-L014-a",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "define Sobolev completions of source and target section spaces",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "no Sobolev-space API for vector-bundle sections is available locally"
  },
  {
    parentLeafId := "AS-L014",
    terminalLeafId := "AS-L014-b",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "prove inclusion, trace, and density facts needed for completed section spaces",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires Sobolev section-space model"
  },
  {
    parentLeafId := "AS-L014",
    terminalLeafId := "AS-L014-c",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "extend elliptic differential operators to continuous maps between Sobolev spaces",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires differential-operator and Sobolev APIs"
  },
  {
    parentLeafId := "AS-L015",
    terminalLeafId := "AS-L015-a",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "state weak-solution equation in the completed section-space model",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires Sobolev extension leaf AS-L014-c"
  },
  {
    parentLeafId := "AS-L015",
    terminalLeafId := "AS-L015-b",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "prove the local elliptic estimate used for regularity",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires elliptic PDE estimates not present in pinned mathlib"
  },
  {
    parentLeafId := "AS-L015",
    terminalLeafId := "AS-L015-c",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "upgrade weak solutions to smooth sections by bootstrapping",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires local elliptic estimate and Sobolev regularity machinery"
  },
  {
    parentLeafId := "AS-L016",
    terminalLeafId := "AS-L016-a",
    packageId := "AS-P06-local-to-global-bridge",
    obligation := "construct local parametrix symbol data for an elliptic operator",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires pseudo-differential or symbol-calculus API"
  },
  {
    parentLeafId := "AS-L016",
    terminalLeafId := "AS-L016-b",
    packageId := "AS-P06-local-to-global-bridge",
    obligation := "prove the parametrix remainder is smoothing or compact",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires compactness theorem for smoothing remainders"
  },
  {
    parentLeafId := "AS-L016",
    terminalLeafId := "AS-L016-c",
    packageId := "AS-P06-local-to-global-bridge",
    obligation := "assemble local parametrices into a global compact-error identity",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires partition-of-unity and compact manifold patching leaves"
  },
  {
    parentLeafId := "AS-L017",
    terminalLeafId := "AS-L017-a",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "derive Fredholmness from a two-sided parametrix modulo compact maps",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "mathlib lacks Fredholm-operator/Fredholm-index API in this closure"
  },
  {
    parentLeafId := "AS-L017",
    terminalLeafId := "AS-L017-b",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "establish closed range and index setup for the completed operator",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires Fredholm operator infrastructure"
  },
  {
    parentLeafId := "AS-L017",
    terminalLeafId := "AS-L017-c",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "specialize Fredholmness to elliptic operators on compact manifolds",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires global parametrix leaf AS-L016-c"
  },
  {
    parentLeafId := "AS-L018",
    terminalLeafId := "AS-L018-a",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "identify the analytic kernel as a solution subspace",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires completed operator model"
  },
  {
    parentLeafId := "AS-L018",
    terminalLeafId := "AS-L018-b",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "prove finite dimensionality of the kernel from Fredholmness or elliptic regularity",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires Fredholmness or elliptic regularity closure"
  },
  {
    parentLeafId := "AS-L018",
    terminalLeafId := "AS-L018-c",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "bridge Sobolev-kernel elements back to smooth-section kernel elements",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires elliptic regularity leaf AS-L015-c"
  },
  {
    parentLeafId := "AS-L019",
    terminalLeafId := "AS-L019-a",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "model the cokernel as quotient or adjoint-kernel data",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires chosen functional-analytic cokernel API"
  },
  {
    parentLeafId := "AS-L019",
    terminalLeafId := "AS-L019-b",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "prove finite dimensionality of the cokernel",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires Fredholm operator infrastructure"
  },
  {
    parentLeafId := "AS-L019",
    terminalLeafId := "AS-L019-c",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "prove equivalence between quotient cokernel and adjoint-kernel descriptions",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires adjoint operator and Hilbert/Sobolev model choices"
  },
  {
    parentLeafId := "AS-L020",
    terminalLeafId := "AS-L020-a",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "define analytic index as integer-valued dimension difference",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires finite-dimensional kernel and cokernel leaves"
  },
  {
    parentLeafId := "AS-L020",
    terminalLeafId := "AS-L020-b",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "prove kernel-cokernel dimension subtraction is well typed and invariant",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires dimension API for selected scalar field"
  },
  {
    parentLeafId := "AS-L020",
    terminalLeafId := "AS-L020-c",
    packageId := "AS-P04-analytic-fredholm-index",
    obligation := "connect the analytic index definition to the future FredholmIndex API",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "no FredholmIndex API located in pinned mathlib"
  },
  {
    parentLeafId := "AS-L021",
    terminalLeafId := "AS-L021-a",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "define or import K-theory carrier for symbol classes",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "no terminal KTheory symbol-class API located locally"
  },
  {
    parentLeafId := "AS-L021",
    terminalLeafId := "AS-L021-b",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "prove homotopy invariance of the symbol K-class",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires K-theory object model"
  },
  {
    parentLeafId := "AS-L021",
    terminalLeafId := "AS-L021-c",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "connect elliptic symbols to the relevant exact-sequence boundary class",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires symbol and K-theory exact-sequence APIs"
  },
  {
    parentLeafId := "AS-L022",
    terminalLeafId := "AS-L022-a",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "define Thom or Bott orientation for the cotangent-bundle symbol class",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires K-theory orientation/Bott periodicity API"
  },
  {
    parentLeafId := "AS-L022",
    terminalLeafId := "AS-L022-b",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "construct the cotangent-bundle topological pushforward",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "no K-theory topological-index pushforward API is available locally"
  },
  {
    parentLeafId := "AS-L022",
    terminalLeafId := "AS-L022-c",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "prove functoriality and naturality properties of the pushforward",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires pushforward construction leaf AS-L022-b"
  },
  {
    parentLeafId := "AS-L023",
    terminalLeafId := "AS-L023-a",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "define the characteristic-class objects required by the selected theorem variant",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires deciding Chern/Todd/A-hat route and available characteristic-class APIs"
  },
  {
    parentLeafId := "AS-L023",
    terminalLeafId := "AS-L023-b",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "state and prove the index-integrand formula in cohomology or K-theory",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires characteristic classes and cohomological pairing APIs"
  },
  {
    parentLeafId := "AS-L023",
    terminalLeafId := "AS-L023-c",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "normalize signs, gradings, and real/complex conventions for the chosen variant",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires formal theorem variant decision"
  },
  {
    parentLeafId := "AS-L024",
    terminalLeafId := "AS-L024-a",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "define the topological index map from symbol data",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires K-theory pushforward or characteristic-class formula"
  },
  {
    parentLeafId := "AS-L024",
    terminalLeafId := "AS-L024-b",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "prove the topological index lands in the integer target",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires integrality theorem for selected topological-index model"
  },
  {
    parentLeafId := "AS-L024",
    terminalLeafId := "AS-L024-c",
    packageId := "AS-P05-symbol-k-theory-topological-index",
    obligation := "bridge topological pushforward evaluation to the declared topological index",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires topological pushforward construction"
  },
  {
    parentLeafId := "AS-L025",
    terminalLeafId := "AS-L025-a",
    packageId := "AS-P07-terminal-index-equality",
    obligation := "state local heat-kernel or local index density contribution",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires chosen proof route and heat-kernel/local-density APIs if that route is used"
  },
  {
    parentLeafId := "AS-L025",
    terminalLeafId := "AS-L025-b",
    packageId := "AS-P07-terminal-index-equality",
    obligation := "formalize deformation, cobordism, or K-theoretic invariance argument",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires selected terminal proof variant"
  },
  {
    parentLeafId := "AS-L025",
    terminalLeafId := "AS-L025-c",
    packageId := "AS-P07-terminal-index-equality",
    obligation := "bridge local density or deformation output to the topological index package",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires AS-L024 topological-index closure"
  },
  {
    parentLeafId := "AS-L026",
    terminalLeafId := "AS-L026-a",
    packageId := "AS-P06-local-to-global-bridge",
    obligation := "construct the partition-of-unity data needed for global patching",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires smooth partition-of-unity APIs for the selected bundles"
  },
  {
    parentLeafId := "AS-L026",
    terminalLeafId := "AS-L026-b",
    packageId := "AS-P06-local-to-global-bridge",
    obligation := "prove compatibility of local coordinate computations on overlaps",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires coordinate-invariance leaves for operators and symbols"
  },
  {
    parentLeafId := "AS-L026",
    terminalLeafId := "AS-L026-c",
    packageId := "AS-P06-local-to-global-bridge",
    obligation := "use compactness to pass from finite local cover data to global identities",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires compact manifold cover and global assembly APIs"
  },
  {
    parentLeafId := "AS-L027",
    terminalLeafId := "AS-L027-a",
    packageId := "AS-P07-terminal-index-equality",
    obligation := "state the bridge theorem equating analytic and topological index constructions",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires AS-L020 analytic index and AS-L024 topological index"
  },
  {
    parentLeafId := "AS-L027",
    terminalLeafId := "AS-L027-b",
    packageId := "AS-P07-terminal-index-equality",
    obligation := "assemble analytic, symbol, topological, and local-to-global branches into the equality proof",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires closure of AS-L010 through AS-L026"
  },
  {
    parentLeafId := "AS-L027",
    terminalLeafId := "AS-L027-c",
    packageId := "AS-P07-terminal-index-equality",
    obligation := "discharge the normalized StatementShape theorem from the terminal equality",
    localStepBudget := 100,
    status := "unchecked",
    repoLocalClosed := false,
    debtClass := "formalization_debt",
    blocker := "requires terminal equality and public theorem variant freeze"
  }
]

/-- C005 records exactly the eighteen parent unchecked leaves requested. -/
theorem asUncheckedParentLeafIds_length :
    asUncheckedParentLeafIds.length = 18 :=
  rfl

/-- C005 splits the eighteen unchecked parent leaves into fifty-four terminal rows. -/
theorem asUncheckedLeafSubledger_length :
    asUncheckedLeafSubledger.length = 54 :=
  rfl

/-- Every terminal C005 row has an independent local proof-step budget `<= 100`. -/
def asUncheckedLeafSubledgerBudgetsLE100 : Bool :=
  asUncheckedLeafSubledger.all (fun row => row.localStepBudget <= 100)

/-- The C005 sub-ledger is a budget split only; no terminal row is repo-locally closed. -/
def asUncheckedLeafSubledgerNoRepoLocalClosure : Bool :=
  asUncheckedLeafSubledger.all (fun row => !row.repoLocalClosed)

/-- C005 preserves all split leaves as unchecked future formalization debt. -/
def asUncheckedLeafSubledgerStatus : String :=
  "all_terminal_rows_unchecked_formalization_debt"

/-- The checked budget gate evaluates to true for the C005 sub-ledger. -/
theorem asUncheckedLeafSubledgerBudgetsLE100_eq_true :
    asUncheckedLeafSubledgerBudgetsLE100 = true :=
  rfl

/-- The checked non-closure gate evaluates to true for the C005 sub-ledger. -/
theorem asUncheckedLeafSubledgerNoRepoLocalClosure_eq_true :
    asUncheckedLeafSubledgerNoRepoLocalClosure = true :=
  rfl

/-- The audit table records exactly the requested pinned mathlib revision. -/
theorem pinnedMathlibRevision_eq_requested :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- The Stage1 audit table currently has six machine-audit rows. -/
theorem mathlibMachineAuditTable_length :
    mathlibMachineAuditTable.length = 6 :=
  rfl

/-- The child external repository audit records exactly the seven required search terms. -/
theorem externalLeanAuditSearchTerms_length :
    externalLeanAuditSearchTerms.length = 7 :=
  rfl

/-- The child external repository audit currently has one row for each required term. -/
theorem externalLeanRepositoryAuditTable_length :
    externalLeanRepositoryAuditTable.length = 7 :=
  rfl

/-- C004 does not permit a parent-theorem completion claim. -/
theorem externalProofIntegrationGate_no_completion :
    externalProofIntegrationGate.completionClaimAllowed = false :=
  rfl

/--
Serial public-surface merge gate for child task S1-M-127-C007.

This is checked metadata for the integrator handoff only.  It records that the
validated statement shape and audit boundary may be merged into public Stage1
surfaces only in a serial public-doc pass, with blueprint/todo status kept open
and without turning the current statement-shape artifact into a theorem
completion claim.
-/
structure PublicStage1SurfaceMergeGate where
  childTask : String
  publicBlueprintLine : String
  leanStatementBoundary : String
  leanAuditBoundary : String
  requiredValidationCommand : String
  validationRequiredBeforePublicMerge : Bool
  publicDocsEditedByChild : Bool
  integratorMustSynchronizeBlueprintAndTodo : Bool
  completionClaimAllowed : Bool
  repoLocalIntegrationDebtRetained : Bool
  mergeStatus : String
  remainingDebtClass : String
deriving Repr

/--
C007 handoff gate.

The current local artifact is ready to be cited by a serial integrator, but this
child does not edit `Docs/Stage1_Blueprint.md`, `Docs/todos_20260430.md`,
`README.md`, Lean import aggregators, or Lake configuration.
-/
def publicStage1SurfaceMergeGate : PublicStage1SurfaceMergeGate := {
  childTask := "S1-M-127-C007",
  publicBlueprintLine := "Docs/Stage1_Blueprint.md:1748",
  leanStatementBoundary :=
    "AwesomeTheorems.Stage1.S1_M_127.StatementShape",
  leanAuditBoundary :=
    "SmoothSectionDifferentialOperator, AtiyahSingerIndexData, mathlibMachineAuditTable, externalLeanRepositoryAuditTable, externalProofIntegrationGate, asUncheckedLeafSubledger, intendedFormalVariantDecision",
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_127.lean",
  validationRequiredBeforePublicMerge := true,
  publicDocsEditedByChild := false,
  integratorMustSynchronizeBlueprintAndTodo := true,
  completionClaimAllowed := false,
  repoLocalIntegrationDebtRetained := false,
  mergeStatus :=
    "integration_ready_for_serial_public_backfill_only; parent remains open",
  remainingDebtClass :=
    "formalization_debt_not_repo_local_integration_debt"
}

/-- C007 did not edit public documents directly. -/
theorem publicStage1SurfaceMergeGate_no_public_doc_edit :
    publicStage1SurfaceMergeGate.publicDocsEditedByChild = false :=
  rfl

/-- C007 requires serial blueprint/todo synchronization by an integrator. -/
theorem publicStage1SurfaceMergeGate_requires_status_sync :
    publicStage1SurfaceMergeGate.integratorMustSynchronizeBlueprintAndTodo = true :=
  rfl

/-- C007 is not a parent-theorem completion claim. -/
theorem publicStage1SurfaceMergeGate_no_completion :
    publicStage1SurfaceMergeGate.completionClaimAllowed = false :=
  rfl

/-- C007 does not retain completed-state repo-local integration debt. -/
theorem publicStage1SurfaceMergeGate_no_repo_local_integration_debt :
    publicStage1SurfaceMergeGate.repoLocalIntegrationDebtRetained = false :=
  rfl

/--
Exact blocker for upgrading this Stage1 statement boundary to a native
Atiyah-Singer theorem statement in the current pinned mathlib closure.
-/
def concreteOperatorModelBlocker : String :=
  "mathlib provides ContMDiffSection for smooth vector-bundle sections, so the local operator carrier is now a map between smooth section spaces; however this pinned closure has no native finite-jet bundle or DifferentialOperator API, no principal-symbol object for such operators, no ellipticity predicate as symbol invertibility off the zero section, no Fredholm-index API for elliptic operators, and no K-theory topological-index pushforward."

end S1_M_127
end Stage1
end AwesomeTheorems
