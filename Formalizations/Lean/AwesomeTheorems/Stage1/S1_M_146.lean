import Mathlib.Analysis.Distribution.TestFunction
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.DerivNotation
import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.Analysis.Distribution.FourierMultiplier
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Integral.DivergenceTheorem
import Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary

/-!
# S1-M-146 / THM-M-1169: boundary estimates for PDE solutions

This Stage1 file records a conservative Lean 4 boundary for the source
statement "regularity of solutions at the boundary".

The pinned mathlib snapshot has substantial functional-analysis, measure,
distribution, test-function, Sobolev-inequality, and divergence-theorem
infrastructure.  It does not expose a terminal theorem saying that weak or
classical PDE solutions on a domain acquire a specific boundary regularity
estimate.  The declarations below therefore freeze a precise statement-shape
boundary and add low-risk wrappers around available mathlib objects.
-/

noncomputable section

open Set TopologicalSpace
open scoped Distributions

universe u v

namespace AwesomeTheorems.Stage1.S1_M_146

/-- Euclidean `n`-space, used as the ambient PDE domain model. -/
abbrev Euclidean (n : ℕ) : Type :=
  EuclideanSpace ℝ (Fin n)

/-- The open unit ball in the Euclidean model space. -/
abbrev UnitBall (n : ℕ) : Set (Euclidean n) :=
  Metric.ball (0 : Euclidean n) 1

/-- The unit sphere, used here as the model boundary of the unit ball. -/
abbrev BoundarySphere (n : ℕ) : Set (Euclidean n) :=
  Metric.sphere (0 : Euclidean n) 1

/-- The open unit ball as a `TopologicalSpace.Opens`, suitable for distributions. -/
def unitBallOpen (n : ℕ) : Opens (Euclidean n) where
  carrier := UnitBall n
  is_open' := Metric.isOpen_ball

/-- Scalar distributions on the model open unit ball. -/
abbrev ScalarDistributionOnUnitBall (n : ℕ) :=
  Distribution (unitBallOpen n) ℝ ⊤

/--
Abstract input data for a boundary regularity estimate.

The structure deliberately separates the local PDE object model from the
terminal theorem.  `pdeResidual` records the weak/distributional side available
in mathlib, while `trace`, `boundaryNorm`, and `targetBoundaryRegularity` record
the boundary side that a future trace/regularity API must instantiate.
-/
structure BoundaryRegularityProblem (n : ℕ) : Type (max (u + 1) (v + 1)) where
  domain : Opens (Euclidean n)
  boundary : Set (Euclidean n)
  boundary_subset_closure : boundary ⊆ closure (domain : Set (Euclidean n))
  boundary_isClosed : IsClosed boundary
  solutionSpace : Type u
  boundarySpace : Type v
  trace : solutionSpace → boundarySpace
  pdeResidual : solutionSpace → Distribution domain ℝ ⊤
  admissibleSolution : solutionSpace → Prop
  targetBoundaryRegularity : boundarySpace → Prop
  interiorNorm : solutionSpace → ℝ
  residualNorm : Distribution domain ℝ ⊤ → ℝ
  boundaryNorm : boundarySpace → ℝ

/--
Conclusion package for a boundary regularity estimate.

It says that admissible solutions have the requested boundary regularity and
that their boundary norm is controlled by an interior norm and a residual norm.
This is the normalized formal target, not a proof of such an estimate.
-/
structure BoundaryRegularityEstimate {n : ℕ}
    (P : BoundaryRegularityProblem.{u, v} n) : Type (max u v) where
  constant : ℝ
  constant_nonneg : 0 ≤ constant
  regularity :
    ∀ u : P.solutionSpace,
      P.admissibleSolution u → P.targetBoundaryRegularity (P.trace u)
  estimate :
    ∀ u : P.solutionSpace,
      P.admissibleSolution u →
        P.boundaryNorm (P.trace u) ≤
          constant * (P.interiorNorm u + P.residualNorm (P.pdeResidual u))

/--
Stage1 statement-shape for "boundary estimates".

For each explicitly modeled boundary-regularity problem, the target theorem
would provide a constant, boundary regularity, and the corresponding estimate.
The current file only records this proposition as the formalization boundary.
-/
def StatementShape (n : ℕ) : Prop :=
  ∀ P : BoundaryRegularityProblem.{u, v} n,
    Nonempty (BoundaryRegularityEstimate P)

/-!
## Public statement normalization

The public Stage1 statement for THM-M-1169 should normalize to `StatementShape`
as the current repo-local Lean boundary.  This is intentionally an abstract
target over a bundled `BoundaryRegularityProblem`, not a terminal PDE boundary
regularity theorem for a concrete elliptic/parabolic problem or a trace theorem
on a smooth domain.
-/

/-- The checked Lean declaration that currently bounds the normalized public statement. -/
def normalizedStatementBoundary (n : ℕ) : Prop :=
  StatementShape.{u, v} n

/--
The normalized public statement is definitionally the Stage1 statement shape.

This wrapper gives the public blueprint a stable theorem name to cite without
claiming that the terminal PDE estimate has been proved.
-/
theorem normalizedStatementBoundary_iff (n : ℕ) :
    normalizedStatementBoundary.{u, v} n ↔ StatementShape.{u, v} n :=
  Iff.rfl

/--
Machine-readable warning for the public backfill: `StatementShape` is a
statement boundary, not a completed boundary regularity theorem.
-/
def normalizedStatementCaveats : List String := [
  "AwesomeTheorems.Stage1.S1_M_146.StatementShape is the current repo-local Lean statement boundary for THM-M-1169.",
  "It quantifies over an abstract BoundaryRegularityProblem and requests a BoundaryRegularityEstimate package.",
  "It is not a terminal PDE boundary regularity theorem for a concrete elliptic/parabolic equation or smooth-domain trace theorem.",
  "Completion still requires a concrete theorem family, trace/boundary APIs, a weak-to-classical bridge, and a repo-local proof or pinned upstream dependency."
]

/-!
## Pinned mathlib audit

This section records the exact pinned mathlib revision and the requested
available module set for `THM-M-1169.mathlib-audit`.  The imports at the top of
this file make the module availability repo-local: the file only validates if
these modules are present in the Lake closure.
-/

/-- The mathlib revision pinned by this repository's Lake configuration for this audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
The exact module set requested by `THM-M-1169.mathlib-audit`.

These modules are support infrastructure only.  They do not contain, and are
not claimed to contain, a terminal boundary regularity estimate for PDE
solutions.
-/
def requestedMathlibAuditModules : List String := [
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.MeasureTheory.Integral.DivergenceTheorem",
  "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary"
]

/-- The requested mathlib audit module list has the expected eight entries. -/
theorem requestedMathlibAuditModules_length :
    requestedMathlibAuditModules.length = 8 :=
  rfl

/-- Checked metadata tying the local artifact to the pinned mathlib revision string. -/
theorem pinnedMathlibRevision_eq :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/--
Current repo-local mathlib audit status for this child.

The value is intentionally narrower than theorem completion: it records that the
requested modules are present and imported in the local Lake closure at the
pinned revision, while the terminal boundary estimate remains open
formalization debt.
-/
def mathlibAuditStatus : String :=
  "requested_modules_imported_at_pinned_mathlib_revision_support_only_not_terminal_boundary_estimate"

/-!
## First theorem-family choice

The public child task `THM-M-1169.theorem-choice` asks for one concrete first
family.  The conservative repo-local choice is the compactly supported
Sobolev/zero-trace special case: it is closest to the imported
`SobolevInequality` infrastructure and keeps harmonic/Dirichlet boundary
regularity on smooth domains as later, API-heavier branches.
-/

/-- Candidate first theorem families for the boundary-estimate slot. -/
inductive FirstBoundaryEstimateFamily : Type where
  /-- Harmonic boundary regularity on a disk or Euclidean ball. -/
  | harmonicBoundaryRegularityOnBall
  /-- Elliptic Dirichlet trace estimate on a smooth domain. -/
  | ellipticDirichletTraceSmoothDomain
  /-- Compactly supported Sobolev functions with the expected zero boundary trace. -/
  | compactSupportedSobolevZeroTrace
  deriving DecidableEq, Repr

/-- Stable string code for public backfill and machine-readable ledgers. -/
def firstBoundaryEstimateFamilyCode : FirstBoundaryEstimateFamily → String
  | .harmonicBoundaryRegularityOnBall => "harmonic_boundary_regularity_on_ball"
  | .ellipticDirichletTraceSmoothDomain => "elliptic_dirichlet_trace_smooth_domain"
  | .compactSupportedSobolevZeroTrace => "compact_supported_sobolev_zero_trace"

/-- The selected first theorem family for this Stage1 slot. -/
def selectedFirstTheoremFamily : FirstBoundaryEstimateFamily :=
  .compactSupportedSobolevZeroTrace

/-- Checked code for the selected first theorem family. -/
theorem selectedFirstTheoremFamily_code :
    firstBoundaryEstimateFamilyCode selectedFirstTheoremFamily =
      "compact_supported_sobolev_zero_trace" :=
  rfl

/--
Machine-readable record of the theorem-family choice.

This is a choice of next formalization target only.  `terminalClaim = false`
prevents the metadata from being read as a completed boundary regularity
theorem.
-/
structure FirstTheoremFamilyChoice where
  family : FirstBoundaryEstimateFamily
  theoremTarget : String
  repoLocalReason : String
  requiredTraceApi : String
  requiredBoundaryApi : String
  requiredEstimateApi : String
  terminalClaim : Bool
  machineStatus : String
  debtClass : String

/--
Chosen first family: compactly supported Sobolev functions with zero boundary
trace, before attempting harmonic or smooth-domain elliptic boundary estimates.
-/
def compactSupportedSobolevZeroTraceChoice : FirstTheoremFamilyChoice where
  family := selectedFirstTheoremFamily
  theoremTarget :=
    "compactly_supported_sobolev_zero_trace_special_case_on_model_domain"
  repoLocalReason :=
    "closest_to_imported_SobolevInequality_support_and_avoids_unavailable_smooth_domain_PDE_regularity_API"
  requiredTraceApi :=
    "define_or_import_trace_operator_and_zero_trace_for_compact_support"
  requiredBoundaryApi :=
    "define_or_import_boundary_measure_or_boundary_submanifold_and_boundary_function_space"
  requiredEstimateApi :=
    "connect_SobolevInequality_or_related_energy_estimate_to_boundary_norm_target"
  terminalClaim := false
  machineStatus := "theorem_family_chosen_not_repo_local_closed"
  debtClass := "formalization_debt"

/-- The selected family record agrees with the stable selected family declaration. -/
theorem compactSupportedSobolevZeroTraceChoice_family :
    compactSupportedSobolevZeroTraceChoice.family = selectedFirstTheoremFamily :=
  rfl

/-- The theorem-family choice is explicitly not a terminal completion claim. -/
theorem compactSupportedSobolevZeroTraceChoice_not_terminal :
    compactSupportedSobolevZeroTraceChoice.terminalClaim = false :=
  rfl

/-- One M0387-style child leaf for the selected theorem-family route. -/
structure TheoremChoiceLeaf where
  canonicalId : String
  responsibility : String
  upstreamInputs : List String
  downstreamOutput : String
  budgetMaxSteps : Nat
  status : String

/-- Integration-ready proof-package split for the selected first family. -/
def compactSupportedSobolevZeroTraceLeaves : List TheoremChoiceLeaf := [
  {
    canonicalId := "M1169-C003-L001",
    responsibility :=
      "freeze_compact_supported_sobolev_zero_trace_statement_on_model_domain",
    upstreamInputs := [
      "BoundaryRegularityProblem",
      "selectedFirstTheoremFamily",
      "Mathlib.Analysis.FunctionalSpaces.SobolevInequality"
    ],
    downstreamOutput := "concrete_statement_shape_for_selected_family",
    budgetMaxSteps := 40,
    status := "checked_metadata_only"
  },
  {
    canonicalId := "M1169-C003-L002",
    responsibility :=
      "define_or_import_trace_operator_and_prove_compact_support_zero_trace",
    upstreamInputs := [
      "boundary_function_space",
      "boundary_submanifold_or_boundary_measure",
      "compact_support_hypothesis"
    ],
    downstreamOutput := "zero_trace_lemma_for_selected_family",
    budgetMaxSteps := 100,
    status := "unchecked_missing_api"
  },
  {
    canonicalId := "M1169-C003-L003",
    responsibility :=
      "connect_available_sobolev_inequality_to_the_selected_interior_norm",
    upstreamInputs := [
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le"
    ],
    downstreamOutput := "interior_estimate_input_for_selected_family",
    budgetMaxSteps := 100,
    status := "unchecked_api_alignment"
  },
  {
    canonicalId := "M1169-C003-L004",
    responsibility :=
      "assemble_zero_boundary_norm_estimate_from_zero_trace_and_nonnegative_constant",
    upstreamInputs := [
      "zero_trace_lemma_for_selected_family",
      "boundary_norm_API",
      "nonnegative_constant"
    ],
    downstreamOutput := "BoundaryRegularityEstimate_for_selected_special_case",
    budgetMaxSteps := 80,
    status := "unchecked_depends_on_L002_L003"
  }
]

/-- The selected theorem-family route has four local child leaves. -/
theorem compactSupportedSobolevZeroTraceLeaves_length :
    compactSupportedSobolevZeroTraceLeaves.length = 4 :=
  rfl

/-- The selected theorem-family leaf budgets are all at or below the M0387 cap. -/
theorem compactSupportedSobolevZeroTraceLeaves_budgets :
    compactSupportedSobolevZeroTraceLeaves.map (fun leaf => leaf.budgetMaxSteps) =
      [40, 100, 100, 80] :=
  rfl

/-!
## Missing formal APIs

The child task `THM-M-1169.missing-api` is a formalization-debt split, not a
proof of boundary regularity.  The six records below isolate the unavailable
interfaces that a later terminal theorem must either define locally, import
from pinned mathlib, or import from a pinned external Lean 4 dependency.
-/

/-- Coarse missing-API blocks for a terminal boundary-estimate formalization. -/
inductive MissingBoundaryEstimateApi : Type where
  /-- A trace operator from the interior solution space to boundary data. -/
  | traceOperator
  /-- A boundary measure, boundary manifold, or boundary submanifold model. -/
  | boundaryMeasureSubmanifold
  /-- Boundary-side function spaces and norms. -/
  | boundaryFunctionSpace
  /-- A bridge between weak/distributional residuals and classical PDE residuals. -/
  | weakClassicalResidualBridge
  /-- The core energy or Sobolev estimate that controls the boundary norm. -/
  | coreEnergyEstimate
  /-- Domain smoothness, Lipschitz, ball, or regularity hypotheses. -/
  | domainRegularityHypotheses
  deriving DecidableEq, Repr

/-- Stable code for public backfill and worker ledgers. -/
def missingBoundaryEstimateApiCode : MissingBoundaryEstimateApi → String
  | .traceOperator => "trace_operator"
  | .boundaryMeasureSubmanifold => "boundary_measure_or_submanifold"
  | .boundaryFunctionSpace => "boundary_function_space"
  | .weakClassicalResidualBridge => "weak_classical_residual_bridge"
  | .coreEnergyEstimate => "core_energy_estimate"
  | .domainRegularityHypotheses => "domain_regularity_hypotheses"

/-- One M0387-style child leaf for the missing-API split. -/
structure MissingApiLeaf where
  canonicalId : String
  apiBlock : MissingBoundaryEstimateApi
  responsibility : String
  upstreamInputs : List String
  downstreamOutput : String
  budgetMaxSteps : Nat
  status : String
  terminalClaim : Bool
  debtClass : String

/--
Integration-ready split of the APIs missing from the current repo-local
boundary-estimate statement shape.

Each leaf is capped at `100` steps or less and is marked as nonterminal: these
records are checkable planning metadata inside Lean, not completed PDE
regularity proofs.
-/
def missingBoundaryEstimateApiLeaves : List MissingApiLeaf := [
  {
    canonicalId := "M1169-C004-L001",
    apiBlock := .traceOperator,
    responsibility :=
      "define_or_import_trace_operator_from_interior_solution_space_to_boundary_data",
    upstreamInputs := [
      "BoundaryRegularityProblem.solutionSpace",
      "BoundaryRegularityProblem.boundarySpace",
      "domain_and_boundary_regular_geometry"
    ],
    downstreamOutput := "typed_trace_map_usable_by_BoundaryRegularityEstimate",
    budgetMaxSteps := 100,
    status := "unchecked_missing_formal_api",
    terminalClaim := false,
    debtClass := "formalization_debt"
  },
  {
    canonicalId := "M1169-C004-L002",
    apiBlock := .boundaryMeasureSubmanifold,
    responsibility :=
      "define_or_import_boundary_measure_or_boundary_submanifold_for_boundary_integration",
    upstreamInputs := [
      "BoundaryRegularityProblem.boundary",
      "Geometry.Manifold.IsManifold.InteriorBoundary",
      "MeasureTheory.Integral.DivergenceTheorem"
    ],
    downstreamOutput := "boundary_carrier_with_measure_or_submanifold_structure",
    budgetMaxSteps := 100,
    status := "unchecked_missing_formal_api",
    terminalClaim := false,
    debtClass := "formalization_debt"
  },
  {
    canonicalId := "M1169-C004-L003",
    apiBlock := .boundaryFunctionSpace,
    responsibility :=
      "define_or_import_boundary_function_space_norm_and_regular_predicate",
    upstreamInputs := [
      "boundary_carrier_with_measure_or_submanifold_structure",
      "BoundaryRegularityProblem.boundarySpace",
      "BoundaryRegularityProblem.boundaryNorm"
    ],
    downstreamOutput := "boundary_space_norm_and_target_regular_predicate_API",
    budgetMaxSteps := 100,
    status := "unchecked_missing_formal_api",
    terminalClaim := false,
    debtClass := "formalization_debt"
  },
  {
    canonicalId := "M1169-C004-L004",
    apiBlock := .weakClassicalResidualBridge,
    responsibility :=
      "bridge_distributional_residuals_to_classical_or_weak_PDE_residual_hypotheses",
    upstreamInputs := [
      "Distribution",
      "TestFunction",
      "BoundaryRegularityProblem.pdeResidual"
    ],
    downstreamOutput := "residual_bridge_lemma_connecting_weak_and_classical_inputs",
    budgetMaxSteps := 100,
    status := "unchecked_missing_formal_api",
    terminalClaim := false,
    debtClass := "formalization_debt"
  },
  {
    canonicalId := "M1169-C004-L005",
    apiBlock := .coreEnergyEstimate,
    responsibility :=
      "prove_or_import_core_energy_estimate_controlling_boundary_norm_by_interior_and_residual_norms",
    upstreamInputs := [
      "Analysis.FunctionalSpaces.SobolevInequality",
      "BoundaryRegularityProblem.interiorNorm",
      "BoundaryRegularityProblem.residualNorm",
      "boundary_space_norm_and_target_regular_predicate_API"
    ],
    downstreamOutput := "numeric_estimate_input_for_BoundaryRegularityEstimate.estimate",
    budgetMaxSteps := 100,
    status := "unchecked_missing_formal_api",
    terminalClaim := false,
    debtClass := "formalization_debt"
  },
  {
    canonicalId := "M1169-C004-L006",
    apiBlock := .domainRegularityHypotheses,
    responsibility :=
      "state_domain_regular_or_model_domain_hypotheses_needed_by_trace_and_energy_estimates",
    upstreamInputs := [
      "BoundaryRegularityProblem.domain",
      "BoundaryRegularityProblem.boundary",
      "unitBallOpen",
      "BoundarySphere"
    ],
    downstreamOutput := "domain_regular_hypothesis_package_for_selected_theorem_family",
    budgetMaxSteps := 80,
    status := "unchecked_missing_formal_api",
    terminalClaim := false,
    debtClass := "formalization_debt"
  }
]

/-- The missing-API split has the requested six leaves. -/
theorem missingBoundaryEstimateApiLeaves_length :
    missingBoundaryEstimateApiLeaves.length = 6 :=
  rfl

/-- The missing-API split records exactly the six requested API blocks. -/
theorem missingBoundaryEstimateApiLeaves_codes :
    missingBoundaryEstimateApiLeaves.map
        (fun leaf => missingBoundaryEstimateApiCode leaf.apiBlock) =
      [
        "trace_operator",
        "boundary_measure_or_submanifold",
        "boundary_function_space",
        "weak_classical_residual_bridge",
        "core_energy_estimate",
        "domain_regularity_hypotheses"
      ] :=
  rfl

/-- The missing-API leaf budgets are all at or below the M0387 cap. -/
theorem missingBoundaryEstimateApiLeaves_budgets :
    missingBoundaryEstimateApiLeaves.map (fun leaf => leaf.budgetMaxSteps) =
      [100, 100, 100, 100, 100, 80] :=
  rfl

/-- No missing-API leaf is represented as a terminal theorem-completion claim. -/
theorem missingBoundaryEstimateApiLeaves_not_terminal :
    missingBoundaryEstimateApiLeaves.map (fun leaf => leaf.terminalClaim) =
      [false, false, false, false, false, false] :=
  rfl

/--
Machine-readable status for C004: the split is repo-local checked metadata, but
the missing APIs themselves remain formalization debt.
-/
def missingBoundaryEstimateApiSplitStatus : String :=
  "checked_six_way_missing_api_split_metadata_only_terminal_boundary_estimate_not_repo_local_closed"

/-- Model-domain wrapper: the unit ball carrier is open. -/
theorem unitBall_isOpen (n : ℕ) : IsOpen (UnitBall n) :=
  Metric.isOpen_ball

/-- Model-boundary wrapper: the Euclidean unit sphere is closed. -/
theorem boundarySphere_isClosed (n : ℕ) : IsClosed (BoundarySphere n) :=
  Metric.isClosed_sphere

/-- Model weak-object wrapper: scalar distributions on the unit ball form a nonempty type. -/
theorem scalarDistributionOnUnitBall_nonempty (n : ℕ) :
    Nonempty (ScalarDistributionOnUnitBall n) :=
  ⟨0⟩

/-- Checked test-function API: every bundled test function is smooth by construction. -/
theorem testFunction_contDiff (n : ℕ)
    (f : TestFunction (unitBallOpen n) ℝ ⊤) :
    ContDiff ℝ (↑(⊤ : ℕ∞)) (f : Euclidean n → ℝ) :=
  f.contDiff

/--
Checked distribution API: continuous linear maps on the codomain act on
distributions by postcomposition.
-/
def distributionMapCLM (n : ℕ) (A : ℝ →L[ℝ] ℝ) :
    ScalarDistributionOnUnitBall n →L[ℝ] ScalarDistributionOnUnitBall n :=
  Distribution.mapCLM A

/-- The identity codomain map gives an endomorphism of scalar distributions. -/
def distributionMapIdCLM (n : ℕ) :
    ScalarDistributionOnUnitBall n →L[ℝ] ScalarDistributionOnUnitBall n :=
  distributionMapCLM n (ContinuousLinearMap.id ℝ ℝ)

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.MeasureTheory.Integral.DivergenceTheorem",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "Distribution",
  "Distribution.mapCLM",
  "TestFunction",
  "TestFunction.contDiff",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one",
  "TemperedDistribution.instLineDeriv",
  "TemperedDistribution.laplacian_eq_fourierMultiplierCLM",
  "Metric.isOpen_ball",
  "Metric.isClosed_sphere"
]

/--
Search terms that did not locate a terminal boundary-regularity theorem in
local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "boundary regularity",
  "BoundaryRegularity",
  "boundary estimate",
  "BoundaryEstimate",
  "trace theorem",
  "Trace theorem",
  "Dirichlet regularity",
  "Neumann regularity",
  "elliptic regularity",
  "PDE",
  "weak derivative"
]

/--
External Lean 4 anchor audit for this slot.

The checked local artifact does not import an external project proving a
terminal boundary trace or boundary regularity estimate.  The public Lean 4
De Giorgi-Nash-Moser work is relevant PDE regularity infrastructure, but it is
an interior elliptic regularity project, not a repo-local boundary-estimate
closure for this statement.
-/
def externalLean4AnchorAudit : List String := [
  "No terminal Lean 4 boundary trace or boundary regularity theorem is in this repo-local Lake closure.",
  "Related but non-terminal: https://github.com/scottnarmstrong/DeGiorgi/tree/4c1b3077d3782b24065184df4ba59501b2e56fc7",
  "DeGiorgi upstream targets interior elliptic regularity and requires separate pin/import/check before any reuse.",
  "Therefore this Stage1 artifact remains statement-shape plus mathlib wrappers, with formalization_debt rather than completed repo_local_integration_debt."
]

/-
## External Lean 4 audit

Child `S1-M-146-C005` is an external-anchor audit.  The checked records below
store the exact requested search terms, the local authentication blocker, and
the directly inspected primary-source candidates.  They are audit metadata only:
they do not import an external theorem, and they do not close `StatementShape`.
-/

/-- Exact external Lean 4 search terms requested for `THM-M-1169.external-audit`. -/
def externalBoundaryEstimateAuditSearchTerms : List String := [
  "BoundaryRegularity",
  "\"boundary regularity\"",
  "BoundaryEstimate",
  "\"boundary estimate\"",
  "\"trace theorem\"",
  "TraceOperator",
  "DirichletRegularity",
  "NeumannRegularity",
  "EllipticRegularity",
  "WeakDerivative",
  "SobolevTrace",
  "PDE"
]

/-- The external audit records exactly the twelve requested search terms. -/
theorem externalBoundaryEstimateAuditSearchTerms_length :
    externalBoundaryEstimateAuditSearchTerms.length = 12 :=
  rfl

/-- One row of the external Lean 4 primary-source audit for this boundary-estimate slot. -/
structure ExternalBoundaryEstimateAuditRow where
  searchTerm : String
  searchSurface : String
  repositoryURL : String
  commit : String
  modulePath : String
  theoremNames : List String
  leanToolchain : String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  auditResult : String
  repoLocalCompletionClaimAllowed : Bool
deriving Repr

/--
Directly inspectable primary-source results for `THM-M-1169.external-audit`.

Authenticated GitHub code search did not run in this worker because `gh auth
status` reported no logged-in GitHub host and neither `GH_TOKEN` nor
`GITHUB_TOKEN` was present.  Public primary-source inspection still located
PDE-adjacent Lean 4 projects, but none is a terminal boundary trace or boundary
regularity estimate for this Stage1 statement.
-/
def externalBoundaryEstimateAuditRows : List ExternalBoundaryEstimateAuditRow := [
  {
    searchTerm :=
      "BoundaryRegularity; \"boundary regularity\"; BoundaryEstimate; \"boundary estimate\"; \"trace theorem\"; TraceOperator; DirichletRegularity; NeumannRegularity; EllipticRegularity; WeakDerivative; SobolevTrace; PDE",
    searchSurface := "GitHub CLI authenticated code search",
    repositoryURL := "not available from this worker",
    commit := "not applicable",
    modulePath := "not applicable",
    theoremNames := [],
    leanToolchain := "not applicable",
    placeholderStatus :=
      "blocked: gh is not logged in and GH_TOKEN/GITHUB_TOKEN are unset",
    lakeDependencyFeasibility :=
      "not assessed; authenticated result set was not produced",
    auditResult :=
      "required authenticated search remains an audit blocker and cannot support a completion claim",
    repoLocalCompletionClaimAllowed := false
  },
  {
    searchTerm :=
      "pinned local mathlib search for the requested boundary/trace/PDE terms",
    searchSurface := "repo-local pinned mathlib source tree",
    repositoryURL := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    modulePath :=
      "Mathlib.Analysis.Distribution.*; Mathlib.Analysis.FunctionalSpaces.SobolevInequality; Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary",
    theoremNames := [
      "Distribution",
      "TestFunction",
      "TestFunction.contDiff",
      "Distribution.mapCLM",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le",
      "TemperedDistribution.laplacian_eq_fourierMultiplierCLM"
    ],
    leanToolchain := "leanprover/lean4:v4.29.0",
    placeholderStatus :=
      "repo-local imported support APIs only; no terminal BoundaryRegularity, BoundaryEstimate, TraceOperator, SobolevTrace, DirichletRegularity, NeumannRegularity, or EllipticRegularity theorem located",
    lakeDependencyFeasibility :=
      "already pinned and imported as mathlib support, but not a proof of the boundary-estimate theorem",
    auditResult :=
      "support infrastructure only; terminal boundary estimate remains formalization_debt",
    repoLocalCompletionClaimAllowed := false
  },
  {
    searchTerm :=
      "PDE; WeakDerivative; boundary regularity; elliptic regularity",
    searchSurface := "direct GitHub primary-source inspection",
    repositoryURL := "https://github.com/scottnarmstrong/DeGiorgi",
    commit := "4c1b3077d3782b24065184df4ba59501b2e56fc7",
    modulePath :=
      "DeGiorgi/DeGiorgiTheory.lean; DeGiorgi/Holder/PublicEstimate.lean; DeGiorgi/SobolevSpace/WeakDerivatives.lean; DeGiorgi/WeakFormulation/SolutionInterfaces.lean",
    theoremNames := [
      "linfty_subsolution_DeGiorgi_normalized",
      "weak_harnack",
      "weak_harnack_on_ball",
      "harnack",
      "harnack_of_homogeneousWeakSolution",
      "holder_Moser",
      "holder_Moser_of_homogeneousWeakSolution",
      "HasWeakPartialDeriv",
      "HasWeakGrad",
      "IsWeakSolution"
    ],
    leanToolchain := "leanprover/lean4:v4.29.0-rc6",
    placeholderStatus :=
      "source grep found no proof-placeholder declarations under DeGiorgi; README states the project has no proof placeholders or extra assumptions beyond Lean and Mathlib",
    lakeDependencyFeasibility :=
      "not immediately feasible as this repo-local closure uses Lean v4.29.0 and mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95 while DeGiorgi pins v4.29.0-rc6; also it proves interior De Giorgi-Nash-Moser estimates, not the boundary trace/estimate statement",
    auditResult :=
      "relevant PDE regularity upstream, but nonterminal for THM-M-1169 boundary estimate and not pinned/imported/checked here",
    repoLocalCompletionClaimAllowed := false
  },
  {
    searchTerm :=
      "PDE; WeakDerivative; boundary estimate; trace theorem",
    searchSurface := "direct GitHub primary-source inspection",
    repositoryURL := "https://github.com/weiran-sun/pde",
    commit := "f911b7031f77d6de0ed1624c6cfdf702cfedbbf4",
    modulePath :=
      "PDE/SobolevSpace/weak_derivative.lean; PDE/Basics/Heat/HeatKernel.lean; PDE/Basics/Heat/HeatMaximumPrinciple.lean; PDE/Basics/Heat/HeatSolution.lean",
    theoremNames := [
      "IsWeakMultiDerivU",
      "WeakDerivUniqU",
      "WeakmultiderivU_spec",
      "heatKernel_solves_heat_eq",
      "heat_from_convolution_heatKernel",
      "heat_equation_max_principle"
    ],
    leanToolchain := "leanprover/lean4:v4.27.0",
    placeholderStatus :=
      "lakefile suppresses proof-placeholder warnings; source grep under PDE found no proof-placeholder declarations, but the project is not a terminal boundary trace theorem",
    lakeDependencyFeasibility :=
      "not feasible as a completion dependency for this slot: toolchain is v4.27.0 with additional documentation dependencies, and the inspected theorems are heat-equation/weak-derivative infrastructure rather than boundary regularity or trace estimates",
    auditResult :=
      "PDE-adjacent infrastructure only; no terminal Lean 4 proof candidate for THM-M-1169",
    repoLocalCompletionClaimAllowed := false
  }
]

/-- The external audit table records four current result rows. -/
theorem externalBoundaryEstimateAuditRows_length :
    externalBoundaryEstimateAuditRows.length = 4 :=
  rfl

/-- No current external-audit row permits a repo-local theorem-completion claim. -/
theorem externalBoundaryEstimateAuditRows_no_completion :
    externalBoundaryEstimateAuditRows.map
        (fun row => row.repoLocalCompletionClaimAllowed) =
      [false, false, false, false] :=
  rfl

/-- Integration gate for any external Lean 4 boundary-estimate proof candidate. -/
structure ExternalBoundaryEstimateIntegrationGate where
  exactTerminalBoundaryProofFound : Bool
  candidateRepositoryURL : String
  candidateCommit : String
  candidateModulePath : String
  candidateTheoremNames : List String
  repoLocalAction : String
  integrationBlocker : String
  machineStatus : String
  debtClass : String
  completionClaimAllowed : Bool
deriving Repr

/--
Current C005 integration gate.

No exact terminal external Lean 4 proof of the THM-M-1169 boundary estimate has
been authenticated, pinned, imported, and checked in this repository.  The
candidate PDE projects above are nonterminal for this statement, and
authenticated GitHub code search remains blocked in this worker.
-/
def externalBoundaryEstimateIntegrationGate :
    ExternalBoundaryEstimateIntegrationGate := {
  exactTerminalBoundaryProofFound := false,
  candidateRepositoryURL := "none verified as a terminal boundary-estimate proof",
  candidateCommit := "not applicable",
  candidateModulePath := "not applicable",
  candidateTheoremNames := [],
  repoLocalAction :=
    "no external dependency was pinned because no exact terminal boundary-estimate proof candidate was verified",
  integrationBlocker :=
    "rerun authenticated GitHub code search with credentials; if a terminal proof is found, pin/import/check it in this Lake closure or record a concrete toolchain/license/dependency/placeholder blocker",
  machineStatus := "not_repo_local_closed",
  debtClass := "formalization_debt",
  completionClaimAllowed := false
}

/-- The current external integration gate found no terminal boundary proof. -/
theorem externalBoundaryEstimateIntegrationGate_no_terminal_proof :
    externalBoundaryEstimateIntegrationGate.exactTerminalBoundaryProofFound = false :=
  rfl

/-- The current external integration gate disallows a completion claim. -/
theorem externalBoundaryEstimateIntegrationGate_no_completion :
    externalBoundaryEstimateIntegrationGate.completionClaimAllowed = false :=
  rfl

/-!
## C006 repo-local integration gate

Child `S1-M-146-C006` checks the M0387 rule that an external upstream Lean 4
anchor cannot be treated as a completed theorem unless it has entered this
repository's local validation closure.  Since the C005 audit found only
nonterminal PDE-adjacent candidates and an authenticated-search blocker, the
safe C006 result is an open gate: no anchor-only completion claim is allowed.
-/

/-- Machine-readable C006 result for the external-upstream integration gate. -/
structure ExternalBoundaryEstimateC006Gate where
  childId : String
  auditedRows : Nat
  exactTerminalBoundaryProofFound : Bool
  externalUpstreamAnchorOnlyCompleted : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  repoLocalAction : String
  concreteIntegrationBlocker : String
  machineStatus : String
  debtClass : String
  publicCompletionClaimAllowed : Bool
deriving Repr

/--
Current C006 gate result.

No exact terminal boundary-estimate proof has been verified as an external Lean
4 closure for this slot.  Therefore no external anchor is promoted to
completion, and any later terminal candidate must be pinned/imported/checked or
assigned a concrete integration blocker before public completion.
-/
def externalBoundaryEstimateC006Gate :
    ExternalBoundaryEstimateC006Gate := {
  childId := "S1-M-146-C006",
  auditedRows := externalBoundaryEstimateAuditRows.length,
  exactTerminalBoundaryProofFound := false,
  externalUpstreamAnchorOnlyCompleted := false,
  repoLocalIntegrationDebtRetainedInCompletedState := false,
  repoLocalAction :=
    "no external dependency pinned because no terminal boundary-estimate proof candidate is verified",
  concreteIntegrationBlocker :=
    "authenticated GitHub code search remains unresolved; inspected DeGiorgi and weiran-sun/pde candidates are nonterminal for this boundary-estimate theorem and have incompatible or separate toolchain/dependency closures",
  machineStatus := "not_repo_local_closed_open_gate_no_anchor_only_completion",
  debtClass := "formalization_debt",
  publicCompletionClaimAllowed := false
}

/-- C006 records the same four audit rows exposed by the external-audit table. -/
theorem externalBoundaryEstimateC006Gate_auditedRows :
    externalBoundaryEstimateC006Gate.auditedRows = 4 :=
  rfl

/-- C006 found no exact terminal external Lean 4 boundary-estimate closure. -/
theorem externalBoundaryEstimateC006Gate_no_terminal :
    externalBoundaryEstimateC006Gate.exactTerminalBoundaryProofFound = false :=
  rfl

/-- C006 does not allow anchor-only upstream evidence to count as completed. -/
theorem externalBoundaryEstimateC006Gate_no_anchor_only_completion :
    externalBoundaryEstimateC006Gate.externalUpstreamAnchorOnlyCompleted = false :=
  rfl

/--
C006 satisfies the repo-local integration-debt gate for an open status: no
completed state retains `repo_local_integration_debt`.
-/
theorem externalBoundaryEstimateC006Gate_no_completed_integration_debt :
    externalBoundaryEstimateC006Gate.repoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-- C006 disallows a public theorem-completion claim. -/
theorem externalBoundaryEstimateC006Gate_no_public_completion :
    externalBoundaryEstimateC006Gate.publicCompletionClaimAllowed = false :=
  rfl

end AwesomeTheorems.Stage1.S1_M_146
