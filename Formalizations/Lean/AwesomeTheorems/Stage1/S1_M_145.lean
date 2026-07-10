import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# S1-M-145 / THM-M-1168: interior estimates

This Stage1 artifact records a conservative Lean boundary for PDE interior
regularity estimates.  The pinned mathlib snapshot contains useful substrates:
test functions, distributions, tempered-distribution Laplacians, `Lp` norms,
and a Gagliardo-Nirenberg-Sobolev inequality.  It does not provide a terminal
general PDE interior-regularity theorem in this repository's current Lake
closure.

The declarations below therefore define a statement shape and provide small
wrappers around available mathlib facts.  They do not claim the terminal PDE
regularity theorem.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal Distributions Topology ContDiff

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_145

universe uE uF

/--
Concrete compact interior patch for a normalized ball equation domain.

The selected De Giorgi/Harnack/Holder endpoint used by this Stage1 slot is a
unit-ball theorem whose interior conclusion is on a half ball.  This structure
keeps the statement slightly scalable by allowing an arbitrary center and outer
radius, but it records the exact relation used by that normalized theorem:
the equation domain is an outer metric ball and the compact carrier is contained
in the corresponding open half ball.
-/
structure CompactInteriorPatch (E : Type uE) [PseudoMetricSpace E]
    (Ω : TopologicalSpace.Opens E) where
  center : E
  outerRadius : ℝ
  innerRadius : ℝ
  carrier : Set E
  isCompact : IsCompact carrier
  outerRadius_pos : 0 < outerRadius
  innerRadius_eq_half_outer : innerRadius = outerRadius / 2
  domain_eq_outerBall : (Ω : Set E) = Metric.ball center outerRadius
  carrier_subset_innerBall : carrier ⊆ Metric.ball center innerRadius

namespace CompactInteriorPatch

variable {E : Type uE} [PseudoMetricSpace E]
variable {Ω : TopologicalSpace.Opens E} (patch : CompactInteriorPatch E Ω)

/-- The inner half ball is contained in the outer equation ball. -/
theorem innerBall_subset_domain :
    Metric.ball patch.center patch.innerRadius ⊆ (Ω : Set E) := by
  intro x hx
  rw [patch.domain_eq_outerBall]
  rw [Metric.mem_ball] at hx ⊢
  have hinner_lt_outer : patch.innerRadius < patch.outerRadius := by
    rw [patch.innerRadius_eq_half_outer]
    linarith [patch.outerRadius_pos]
  exact lt_trans hx hinner_lt_outer

/-- The compact carrier is therefore compactly contained in the equation domain. -/
theorem carrier_subset_domain :
    patch.carrier ⊆ (Ω : Set E) :=
  patch.carrier_subset_innerBall.trans (patch.innerBall_subset_domain)

/-- The recorded inner radius is positive. -/
theorem innerRadius_pos : 0 < patch.innerRadius := by
  rw [patch.innerRadius_eq_half_outer]
  linarith [patch.outerRadius_pos]

end CompactInteriorPatch

/--
Scalar divergence-form elliptic operator data over a real Hilbert domain.

The principal coefficient maps gradients to fluxes, the drift coefficient maps
gradients to scalars, and the zeroth-order coefficient multiplies the solution.
This is a concrete PDE object model rather than an abstract `Operator` type.
-/
structure ScalarDivergenceFormOperator (E : Type uE)
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] where
  principalCoeff : E → E →L[ℝ] E
  driftCoeff : E → E →L[ℝ] ℝ
  zerothCoeff : E → ℝ

/-- Concrete uniform ellipticity window for the principal coefficient. -/
def UniformlyEllipticOn
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (A : E → E →L[ℝ] E) (Ω : TopologicalSpace.Opens E) (ellipticLower ellipticUpper : ℝ) :
    Prop :=
  0 < ellipticLower ∧ ellipticLower ≤ ellipticUpper ∧
    ∀ x ∈ (Ω : Set E), ∀ ξ : E,
      ellipticLower * ‖ξ‖ ^ 2 ≤ inner ℝ (A x ξ) ξ ∧
        ‖A x ξ‖ ≤ ellipticUpper * ‖ξ‖

/-- Coefficient regularity for the concrete scalar divergence-form model. -/
def DivergenceFormCoefficientsContDiffOn
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (L : ScalarDivergenceFormOperator E) (Ω : TopologicalSpace.Opens E)
    (k : ℕ∞) : Prop :=
  ContDiffOn ℝ (k : WithTop ℕ∞) L.principalCoeff (Ω : Set E) ∧
    ContDiffOn ℝ (k : WithTop ℕ∞) L.driftCoeff (Ω : Set E) ∧
      ContDiffOn ℝ (k : WithTop ℕ∞) L.zerothCoeff (Ω : Set E)

/--
Concrete scalar interior-estimate problem.

`weakDivergenceSolution` remains a proposition because this repository's
current mathlib closure does not expose the variational De Giorgi weak-solution
API.  The operator, forcing, solution, domain, compact interior patch,
ellipticity constants, regularity order, and local estimate shape are now
concrete mathlib objects.
-/
structure ScalarInteriorEstimateProblem (E : Type uE)
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] where
  domain : TopologicalSpace.Opens E
  operator : ScalarDivergenceFormOperator E
  solution : E → ℝ
  forcing : E → ℝ
  patch : CompactInteriorPatch E domain
  regularityOrder : ℕ∞
  ellipticityLower : ℝ
  ellipticityUpper : ℝ
  estimateConstant : ℝ
  weakDivergenceSolution : Prop

/--
Backwards-compatible name for the Stage1 data boundary, now instantiated by a
concrete scalar divergence-form PDE problem rather than abstract operator/RHS
families.
-/
abbrev InteriorEstimateData (E : Type uE)
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] :=
  ScalarInteriorEstimateProblem E

/-- Concrete forcing regularity for the scalar model. -/
def ScalarForcingContDiffOn
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (P : ScalarInteriorEstimateProblem E) : Prop :=
  ContDiffOn ℝ (P.regularityOrder : WithTop ℕ∞) P.forcing (P.domain : Set E)

/-- Concrete pointwise interior a-priori estimate shape for the scalar model. -/
def ScalarPointwiseInteriorEstimate
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (P : ScalarInteriorEstimateProblem E) : Prop :=
  0 ≤ P.estimateConstant ∧
    ∀ x ∈ P.patch.carrier,
      ‖P.solution x‖ ≤ P.estimateConstant * (1 + ‖P.forcing x‖)

/--
Single-problem formula for an interior estimate in the concrete scalar model.

The weak-solution condition is not proved from mathlib here; it is an explicit
problem-side proposition until the external De Giorgi APIs are pinned,
imported, and checked in this repository.
-/
def InteriorRegularityFormula
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (P : InteriorEstimateData E) : Prop :=
  UniformlyEllipticOn P.operator.principalCoeff P.domain
      P.ellipticityLower P.ellipticityUpper →
    DivergenceFormCoefficientsContDiffOn P.operator P.domain P.regularityOrder →
      ScalarForcingContDiffOn P →
        P.weakDivergenceSolution →
          ScalarPointwiseInteriorEstimate P ∧
            ContDiffOn ℝ (P.regularityOrder : WithTop ℕ∞)
              P.solution P.patch.carrier

/--
Stage1 normalized statement-shape candidate for the theorem "solutions are
regular in the interior".

This is intentionally a proposition only.  A later terminal proof must replace
the remaining weak-solution proposition by the checked De Giorgi variational API
or by another pinned local PDE proof body.
-/
def StatementShape
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E] : Prop :=
  ∀ P : InteriorEstimateData E, InteriorRegularityFormula P

/-- The normalized statement shape unfolds to the per-patch formula. -/
theorem statementShape_iff_forall_patch
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E] :
    StatementShape (E := E) ↔
      ∀ P : InteriorEstimateData E, InteriorRegularityFormula P :=
  Iff.rfl

/--
Distributional-equation shape using mathlib's current distribution object.

This records a low-risk weak-form target: a continuous linear post-composition
operator maps a distributional solution to the distributional forcing.  It is
not a full PDE operator model.
-/
def DistributionalEquationShape
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    [IsTopologicalAddGroup F] [ContinuousSMul ℝ F]
    (Ω : TopologicalSpace.Opens E) (A : F →L[ℝ] F)
    (u rhs : 𝓓'(Ω, F)) : Prop :=
  Distribution.mapCLM A u = rhs

/-- Checked wrapper: a bundled test function is `C^n`. -/
theorem testFunction_contDiff_mathlib_wrapper
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {Ω : TopologicalSpace.Opens E} {n : ℕ∞} (φ : 𝓓^{n}(Ω, F)) :
    ContDiff ℝ (n : WithTop ℕ∞) φ :=
  TestFunction.contDiff φ

/-- Checked wrapper: distributional post-composition evaluates by applying the linear map. -/
theorem distribution_mapCLM_apply_mathlib_wrapper
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : Type uF} [AddCommGroup F] [Module ℝ F] [TopologicalSpace F]
    [IsTopologicalAddGroup F] [ContinuousSMul ℝ F]
    {G : Type*} [AddCommGroup G] [Module ℝ G] [TopologicalSpace G]
    [IsTopologicalAddGroup G] [ContinuousSMul ℝ G]
    {Ω : TopologicalSpace.Opens E} {n : ℕ∞}
    (A : F →L[ℝ] G) (T : 𝓓'^{n}(Ω, F)) (φ : 𝓓^{n}(Ω, ℝ)) :
    ((Distribution.mapCLM A) T) φ = A (T φ) :=
  Distribution.mapCLM_apply

/-- Checked wrapper: the distributional Laplacian acts by testing against the classical Laplacian. -/
theorem tempered_laplacian_apply_mathlib_wrapper
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℂ F]
    (T : TemperedDistribution E F) (φ : SchwartzMap E ℂ) :
    (Laplacian.laplacian T) φ = T (Laplacian.laplacian φ) :=
  TemperedDistribution.laplacian_apply_apply T φ

/--
Checked wrapper for mathlib's first-order Sobolev inequality.

This is a useful analytic estimate substrate for PDE regularity packages, not a
terminal interior regularity theorem.
-/
theorem sobolev_eLpNorm_le_fderiv_one_mathlib_wrapper
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (μ : Measure E) [μ.IsAddHaarMeasure] {u : E → F}
    (hu : ContDiff ℝ 1 u) (hcu : HasCompactSupport u) {p : ℝ≥0}
    (hp : (Module.finrank ℝ E : ℝ≥0).HolderConjugate p) :
    eLpNorm u (↑p) μ ≤
      ↑(eLpNormLESNormFDerivOneConst μ ↑p) * eLpNorm (fderiv ℝ u) 1 μ :=
  MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one μ hu hcu hp

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.Analysis.Distribution.Support",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.Analysis.Calculus.ContDiff.Basic"
]

/-- Search terms that did not locate a terminal imported interior-regularity theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "interior regularity",
  "InteriorRegularity",
  "elliptic regularity",
  "EllipticRegularity",
  "weak derivative",
  "WeakSolution",
  "uniformly elliptic",
  "DeGiorgi",
  "Nash",
  "Moser",
  "Harnack"
]

/--
External Lean 4 primary-source anchor found but not imported by this repo-local
artifact.

The `scottnarmstrong/DeGiorgi` project is a relevant Lean 4 formalization of
De Giorgi-Nash-Moser elliptic regularity.  It is not in this repository's Lake
dependency closure, so this file does not use it as a completed wrapper.
-/
def externalLean4PrimaryAnchors : List String := [
  "https://github.com/scottnarmstrong/DeGiorgi/tree/4c1b3077d3782b24065184df4ba59501b2e56fc7",
  "DeGiorgi.lean imports DeGiorgi.DeGiorgiTheory",
  "target theorem names recorded by upstream manifest: linfty_subsolution_DeGiorgi_normalized, weak_harnack, weak_harnack_on_ball, harnack, harnack_of_homogeneousWeakSolution, holder_Moser, holder_Moser_of_homogeneousWeakSolution",
  "upstream lakefile requires mathlib v4.29.0-rc6 and REPL v4.29.0-rc6; this repo pins mathlib at 8a178386ffc0f5fef0b77738bb5449d50efeea95, so integration must be checked before any completion claim"
]

/-- External De Giorgi repository recorded by C003. -/
def externalDeGiorgiRepository : String :=
  "scottnarmstrong/DeGiorgi"

/-- External De Giorgi revision recorded by C003. -/
def externalDeGiorgiRevision : String :=
  "4c1b3077d3782b24065184df4ba59501b2e56fc7"

/-- External De Giorgi anchor URL recorded by C003. -/
def externalDeGiorgiAnchorURL : String :=
  "https://github.com/scottnarmstrong/DeGiorgi/tree/4c1b3077d3782b24065184df4ba59501b2e56fc7"

/-- De Giorgi theorem names that must be tested in this repository before completion. -/
def externalDeGiorgiTargetTheoremNames : List String := [
  "linfty_subsolution_DeGiorgi_normalized",
  "weak_harnack",
  "weak_harnack_on_ball",
  "harnack",
  "harnack_of_homogeneousWeakSolution",
  "holder_Moser",
  "holder_Moser_of_homogeneousWeakSolution"
]

/-- Machine-state classification for the external De Giorgi anchor. -/
def externalDeGiorgiRepoLocalMachineState : String :=
  "external_upstream_anchor_only"

/-- Debt classification for the external De Giorgi anchor before pin/import/check. -/
def externalDeGiorgiDebtClassification : String :=
  "repo_local_integration_debt"

/-- Repo-pinned mathlib revision used for this Stage1 audit. -/
def repoPinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Short substrate-anchor list requested by the public Stage1 backfill item. -/
def checkedSubstrateAnchorModules : List String := [
  "Distribution",
  "TemperedDistribution",
  "SobolevInequality"
]

/-- C002 gate recording mathlib substrate anchors without a completion claim. -/
structure SubstrateAnchorGate where
  childId : String
  pinnedMathlibRevision : String
  checkedModules : List String
  modulesAreSubstrateAnchorsOnly : Bool
  terminalTheoremClaimedFromSubstrates : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool

/-- Machine-readable result for child `S1-M-145-C002`. -/
def substrateAnchorGate : SubstrateAnchorGate where
  childId := "S1-M-145-C002"
  pinnedMathlibRevision := repoPinnedMathlibRevision
  checkedModules := checkedSubstrateAnchorModules
  modulesAreSubstrateAnchorsOnly := true
  terminalTheoremClaimedFromSubstrates := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true

/-- C002 records the exact repo-pinned mathlib revision. -/
theorem substrateAnchorGate_revision :
    substrateAnchorGate.pinnedMathlibRevision =
      "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- C002 records exactly the requested substrate anchor modules. -/
theorem substrateAnchorGate_modules :
    substrateAnchorGate.checkedModules =
      ["Distribution", "TemperedDistribution", "SobolevInequality"] :=
  rfl

/-- C002 treats the checked modules only as analytic substrates. -/
theorem substrateAnchorGate_modulesAnchorOnly :
    substrateAnchorGate.modulesAreSubstrateAnchorsOnly = true :=
  rfl

/-- C002 does not claim the substrate modules prove the terminal theorem. -/
theorem substrateAnchorGate_noTerminalClaim :
    substrateAnchorGate.terminalTheoremClaimedFromSubstrates = false :=
  rfl

/-- C002 keeps THM-M-1168 below completion. -/
theorem substrateAnchorGate_noCompletionClaim :
    substrateAnchorGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C002 retains repo-local integration debt. -/
theorem substrateAnchorGate_noCompletedRepoLocalIntegrationDebt :
    substrateAnchorGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-- Concrete blockers before the De Giorgi anchor can count as repo-local evidence. -/
def externalDeGiorgiIntegrationBlockers : List String := [
  "The external `scottnarmstrong/DeGiorgi` project is not pinned in this repository's Lake dependency closure.",
  "The command `import DeGiorgi` has not been checked in this repository.",
  "The theorem names `linfty_subsolution_DeGiorgi_normalized`, `weak_harnack`, `harnack`, `holder_Moser`, and related wrappers have not been checked under this repository's namespace and toolchain.",
  "The external project declares mathlib v4.29.0-rc6, while this repository pins mathlib at 8a178386ffc0f5fef0b77738bb5449d50efeea95."
]

/-- C003 gate for the external De Giorgi anchor. -/
structure ExternalDeGiorgiAnchorGate where
  childId : String
  repository : String
  revision : String
  anchorURL : String
  targetTheoremNames : List String
  repoLocalMachineState : String
  debtClassification : String
  pinnedInLakeClosure : Bool
  importCheckedInThisRepo : Bool
  targetTheoremNamesCheckedInThisRepo : Bool
  mathlibVersionMismatchBlocker : Bool
  countsAsRepoLocalCompletionEvidence : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool

/-- Machine-readable result for child `S1-M-145-C003`. -/
def externalDeGiorgiAnchorGate : ExternalDeGiorgiAnchorGate where
  childId := "S1-M-145-C003"
  repository := externalDeGiorgiRepository
  revision := externalDeGiorgiRevision
  anchorURL := externalDeGiorgiAnchorURL
  targetTheoremNames := externalDeGiorgiTargetTheoremNames
  repoLocalMachineState := externalDeGiorgiRepoLocalMachineState
  debtClassification := externalDeGiorgiDebtClassification
  pinnedInLakeClosure := false
  importCheckedInThisRepo := false
  targetTheoremNamesCheckedInThisRepo := false
  mathlibVersionMismatchBlocker := true
  countsAsRepoLocalCompletionEvidence := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true

/-- C003 records the exact external De Giorgi repository. -/
theorem externalDeGiorgiAnchorGate_repository :
    externalDeGiorgiAnchorGate.repository = "scottnarmstrong/DeGiorgi" :=
  rfl

/-- C003 records the exact external De Giorgi revision. -/
theorem externalDeGiorgiAnchorGate_revision :
    externalDeGiorgiAnchorGate.revision =
      "4c1b3077d3782b24065184df4ba59501b2e56fc7" :=
  rfl

/-- C003 classifies the external De Giorgi source as anchor-only in this repository. -/
theorem externalDeGiorgiAnchorGate_machineState :
    externalDeGiorgiAnchorGate.repoLocalMachineState =
      "external_upstream_anchor_only" :=
  rfl

/-- C003 classifies the remaining work as repo-local integration debt. -/
theorem externalDeGiorgiAnchorGate_debtClassification :
    externalDeGiorgiAnchorGate.debtClassification =
      "repo_local_integration_debt" :=
  rfl

/-- C003 records that the external De Giorgi project is not pinned in this Lake closure. -/
theorem externalDeGiorgiAnchorGate_notPinned :
    externalDeGiorgiAnchorGate.pinnedInLakeClosure = false :=
  rfl

/-- C003 records that `import DeGiorgi` has not been checked in this repository. -/
theorem externalDeGiorgiAnchorGate_importNotChecked :
    externalDeGiorgiAnchorGate.importCheckedInThisRepo = false :=
  rfl

/-- C003 records that the target theorem names have not been checked in this repository. -/
theorem externalDeGiorgiAnchorGate_theoremNamesNotChecked :
    externalDeGiorgiAnchorGate.targetTheoremNamesCheckedInThisRepo = false :=
  rfl

/-- C003 records the mathlib version mismatch as a concrete integration blocker. -/
theorem externalDeGiorgiAnchorGate_mathlibMismatchBlocker :
    externalDeGiorgiAnchorGate.mathlibVersionMismatchBlocker = true :=
  rfl

/-- C003 does not count anchor-only De Giorgi evidence as repo-local completion evidence. -/
theorem externalDeGiorgiAnchorGate_notCompletionEvidence :
    externalDeGiorgiAnchorGate.countsAsRepoLocalCompletionEvidence = false :=
  rfl

/-- C003 keeps THM-M-1168 below completion. -/
theorem externalDeGiorgiAnchorGate_noCompletionClaim :
    externalDeGiorgiAnchorGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C003 retains repo-local integration debt. -/
theorem externalDeGiorgiAnchorGate_noCompletedRepoLocalIntegrationDebt :
    externalDeGiorgiAnchorGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-- C004 import-test task for bringing the external De Giorgi APIs into this repository. -/
structure ExternalDeGiorgiImportTestTask where
  childId : String
  lakeClosureImportCommand : String
  targetTheoremNames : List String
  relatedWrapperFamilies : List String
  taskRecordedForSerialIntegration : Bool
  importAlreadyCheckedInThisRepo : Bool
  theoremNamesAlreadyCheckedInThisRepo : Bool
  dependencyMismatchMustBeResolvedFirst : Bool
  countsAsCurrentCompletionEvidence : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool

/-- Machine-readable integration task for child `S1-M-145-C004`. -/
def externalDeGiorgiImportTestTask : ExternalDeGiorgiImportTestTask where
  childId := "S1-M-145-C004"
  lakeClosureImportCommand := "cd Formalizations/Lean && lake env lean <scratch file containing `import DeGiorgi`>"
  targetTheoremNames := externalDeGiorgiTargetTheoremNames
  relatedWrapperFamilies := [
    "normalized linfty subsolution De Giorgi estimate",
    "weak Harnack and weak_harnack_on_ball wrappers",
    "Harnack and homogeneous weak-solution wrappers",
    "Holder/Moser regularity wrappers"
  ]
  taskRecordedForSerialIntegration := true
  importAlreadyCheckedInThisRepo := false
  theoremNamesAlreadyCheckedInThisRepo := false
  dependencyMismatchMustBeResolvedFirst := true
  countsAsCurrentCompletionEvidence := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true

/-- C004 records the exact repo-local command shape needed for the import test. -/
theorem externalDeGiorgiImportTestTask_command :
    externalDeGiorgiImportTestTask.lakeClosureImportCommand =
      "cd Formalizations/Lean && lake env lean <scratch file containing `import DeGiorgi`>" :=
  rfl

/-- C004 records the upstream theorem names that must be resolved after the import. -/
theorem externalDeGiorgiImportTestTask_theoremNames :
    externalDeGiorgiImportTestTask.targetTheoremNames =
      externalDeGiorgiTargetTheoremNames :=
  rfl

/-- C004 creates only an integration task; the import has not yet been checked here. -/
theorem externalDeGiorgiImportTestTask_importNotYetChecked :
    externalDeGiorgiImportTestTask.importAlreadyCheckedInThisRepo = false :=
  rfl

/-- C004 creates only an integration task; target theorem names have not yet been checked here. -/
theorem externalDeGiorgiImportTestTask_theoremNamesNotYetChecked :
    externalDeGiorgiImportTestTask.theoremNamesAlreadyCheckedInThisRepo = false :=
  rfl

/-- C004 records the dependency mismatch as a blocker before executing the import test. -/
theorem externalDeGiorgiImportTestTask_dependencyMismatch :
    externalDeGiorgiImportTestTask.dependencyMismatchMustBeResolvedFirst = true :=
  rfl

/-- C004 does not count the recorded task as completion evidence. -/
theorem externalDeGiorgiImportTestTask_notCompletionEvidence :
    externalDeGiorgiImportTestTask.countsAsCurrentCompletionEvidence = false :=
  rfl

/-- C004 keeps THM-M-1168 below completion. -/
theorem externalDeGiorgiImportTestTask_noCompletionClaim :
    externalDeGiorgiImportTestTask.completionClaimAllowed = false :=
  rfl

/-- No completed state in C004 retains repo-local integration debt. -/
theorem externalDeGiorgiImportTestTask_noCompletedRepoLocalIntegrationDebt :
    externalDeGiorgiImportTestTask.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-- Exact dependency revisions relevant to importing the external De Giorgi project. -/
structure ExternalDeGiorgiDependencyMismatchGate where
  childId : String
  repoLeanToolchain : String
  externalLeanToolchain : String
  repoMathlibRevision : String
  externalMathlibInputRev : String
  externalMathlibResolvedRevision : String
  externalReplInputRev : String
  externalReplResolvedRevision : String
  dependencyMismatchResolvedInThisRepo : Bool
  concreteIntegrationBlockerRecorded : Bool
  importCanCountAsCheckedBeforeResolution : Bool
  countsAsRepoLocalCompletionEvidence : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool

/--
C005 gate for the dependency mismatch between this repository and the external
De Giorgi anchor.

The mismatch is not resolved by this file: resolving it requires a serial Lake
dependency integration decision outside this child worker's owned write scope.
This checked record prevents the anchor-only source from being promoted to a
completed state before that decision is made and validated.
-/
def externalDeGiorgiDependencyMismatchGate : ExternalDeGiorgiDependencyMismatchGate where
  childId := "S1-M-145-C005"
  repoLeanToolchain := "leanprover/lean4:v4.29.0"
  externalLeanToolchain := "leanprover/lean4:v4.29.0-rc6"
  repoMathlibRevision := repoPinnedMathlibRevision
  externalMathlibInputRev := "v4.29.0-rc6"
  externalMathlibResolvedRevision := "5c8398df528176d9c87ccd9226ba8f7c8852d59c"
  externalReplInputRev := "v4.29.0-rc6"
  externalReplResolvedRevision := "1d17a15a60811e58edfbf73e13a114537e999a41"
  dependencyMismatchResolvedInThisRepo := false
  concreteIntegrationBlockerRecorded := true
  importCanCountAsCheckedBeforeResolution := false
  countsAsRepoLocalCompletionEvidence := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true

/-- C005 records this repository's Lean toolchain. -/
theorem externalDeGiorgiDependencyMismatchGate_repoLeanToolchain :
    externalDeGiorgiDependencyMismatchGate.repoLeanToolchain =
      "leanprover/lean4:v4.29.0" :=
  rfl

/-- C005 records the external De Giorgi Lean toolchain. -/
theorem externalDeGiorgiDependencyMismatchGate_externalLeanToolchain :
    externalDeGiorgiDependencyMismatchGate.externalLeanToolchain =
      "leanprover/lean4:v4.29.0-rc6" :=
  rfl

/-- C005 records this repository's pinned mathlib revision. -/
theorem externalDeGiorgiDependencyMismatchGate_repoMathlibRevision :
    externalDeGiorgiDependencyMismatchGate.repoMathlibRevision =
      "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- C005 records the external De Giorgi mathlib input revision. -/
theorem externalDeGiorgiDependencyMismatchGate_externalMathlibInputRev :
    externalDeGiorgiDependencyMismatchGate.externalMathlibInputRev =
      "v4.29.0-rc6" :=
  rfl

/-- C005 records the external De Giorgi mathlib resolved revision. -/
theorem externalDeGiorgiDependencyMismatchGate_externalMathlibResolvedRevision :
    externalDeGiorgiDependencyMismatchGate.externalMathlibResolvedRevision =
      "5c8398df528176d9c87ccd9226ba8f7c8852d59c" :=
  rfl

/-- C005 records the external De Giorgi REPL input revision. -/
theorem externalDeGiorgiDependencyMismatchGate_externalReplInputRev :
    externalDeGiorgiDependencyMismatchGate.externalReplInputRev =
      "v4.29.0-rc6" :=
  rfl

/-- C005 records the external De Giorgi REPL resolved revision. -/
theorem externalDeGiorgiDependencyMismatchGate_externalReplResolvedRevision :
    externalDeGiorgiDependencyMismatchGate.externalReplResolvedRevision =
      "1d17a15a60811e58edfbf73e13a114537e999a41" :=
  rfl

/-- C005 records that the mismatch has not been resolved inside this repository. -/
theorem externalDeGiorgiDependencyMismatchGate_notResolved :
    externalDeGiorgiDependencyMismatchGate.dependencyMismatchResolvedInThisRepo = false :=
  rfl

/-- C005 records the mismatch as a concrete integration blocker. -/
theorem externalDeGiorgiDependencyMismatchGate_blockerRecorded :
    externalDeGiorgiDependencyMismatchGate.concreteIntegrationBlockerRecorded = true :=
  rfl

/-- C005 blocks counting an import test as checked before dependency resolution. -/
theorem externalDeGiorgiDependencyMismatchGate_importBlockedUntilResolution :
    externalDeGiorgiDependencyMismatchGate.importCanCountAsCheckedBeforeResolution = false :=
  rfl

/-- C005 does not count the external anchor as repo-local completion evidence. -/
theorem externalDeGiorgiDependencyMismatchGate_notCompletionEvidence :
    externalDeGiorgiDependencyMismatchGate.countsAsRepoLocalCompletionEvidence = false :=
  rfl

/-- C005 keeps THM-M-1168 below completion until the dependency mismatch is resolved. -/
theorem externalDeGiorgiDependencyMismatchGate_noCompletionClaim :
    externalDeGiorgiDependencyMismatchGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C005 retains repo-local integration debt. -/
theorem externalDeGiorgiDependencyMismatchGate_noCompletedRepoLocalIntegrationDebt :
    externalDeGiorgiDependencyMismatchGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/--
M0387-style gate for this Stage1 artifact.

The local file checks statement shapes and mathlib wrappers only.  It does not
prove the terminal interior-estimate theorem and does not turn the external
De Giorgi anchor into repo-local completion evidence.
-/
structure Stage1ArtifactGate where
  childId : String
  statementShapeChecked : Bool
  mathlibWrappersChecked : Bool
  externalAnchorOnly : Bool
  externalDependencyPinnedImportedChecked : Bool
  terminalInteriorEstimateProofInRepo : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for child `S1-M-145-C001`. -/
def stage1ArtifactGate : Stage1ArtifactGate where
  childId := "S1-M-145-C001"
  statementShapeChecked := true
  mathlibWrappersChecked := true
  externalAnchorOnly := true
  externalDependencyPinnedImportedChecked := false
  terminalInteriorEstimateProofInRepo := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt := "repo_local_integration_debt blocker recorded for the external De Giorgi anchor; terminal theorem remains not completed"

/-- C001 records a checked statement-shape artifact. -/
theorem stage1ArtifactGate_statementShapeChecked :
    stage1ArtifactGate.statementShapeChecked = true :=
  rfl

/-- C001 records checked local mathlib wrappers. -/
theorem stage1ArtifactGate_mathlibWrappersChecked :
    stage1ArtifactGate.mathlibWrappersChecked = true :=
  rfl

/-- The external De Giorgi source is only an anchor in this repository. -/
theorem stage1ArtifactGate_externalAnchorOnly :
    stage1ArtifactGate.externalAnchorOnly = true :=
  rfl

/-- C001 does not claim that the external dependency is pinned/imported/checked. -/
theorem stage1ArtifactGate_externalNotRepoLocalChecked :
    stage1ArtifactGate.externalDependencyPinnedImportedChecked = false :=
  rfl

/-- C001 does not contain a terminal proof of the interior-estimate theorem. -/
theorem stage1ArtifactGate_noTerminalProof :
    stage1ArtifactGate.terminalInteriorEstimateProofInRepo = false :=
  rfl

/-- C001 keeps THM-M-1168 below completion. -/
theorem stage1ArtifactGate_noCompletionClaim :
    stage1ArtifactGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C001 retains repo-local integration debt. -/
theorem stage1ArtifactGate_noCompletedRepoLocalIntegrationDebt :
    stage1ArtifactGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/--
C006 gate for replacing the old abstract `Operator`/`RHS` statement data by a
concrete scalar divergence-form PDE object model.

This does not import De Giorgi and does not prove a terminal regularity theorem.
It records the strongest repo-local progress available before dependency
integration: concrete coefficients, forcing, solution, compact patch,
ellipticity constants, and pointwise estimate shape are checked locally; the
weak-solution API is still an explicit proposition awaiting a pinned/imported
PDE dependency or a local variational-equation API.
-/
structure ConcretePDEObjectModelGate where
  childId : String
  compactInteriorPatchModelChecked : Bool
  scalarDivergenceOperatorModelChecked : Bool
  abstractOperatorAndRHSRetired : Bool
  statementShapeUsesConcreteProblem : Bool
  weakSolutionStillRequiresCheckedAPI : Bool
  importedDeGiorgiWrapperUsed : Bool
  countsAsTerminalCompletionEvidence : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for child `S1-M-145-C006`. -/
def concretePDEObjectModelGate : ConcretePDEObjectModelGate where
  childId := "S1-M-145-C006"
  compactInteriorPatchModelChecked := true
  scalarDivergenceOperatorModelChecked := true
  abstractOperatorAndRHSRetired := true
  statementShapeUsesConcreteProblem := true
  weakSolutionStillRequiresCheckedAPI := true
  importedDeGiorgiWrapperUsed := false
  countsAsTerminalCompletionEvidence := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt :=
    "Concrete scalar divergence-form object model checked; weak-solution API and De Giorgi terminal wrapper remain blocked until pin/import/check."

/-- C006 records the concrete compact interior patch model. -/
theorem concretePDEObjectModelGate_compactPatch :
    concretePDEObjectModelGate.compactInteriorPatchModelChecked = true :=
  rfl

/-- C006 records the concrete scalar divergence-form operator model. -/
theorem concretePDEObjectModelGate_operatorModel :
    concretePDEObjectModelGate.scalarDivergenceOperatorModelChecked = true :=
  rfl

/-- C006 retires the old abstract `Operator` and `RHS` type fields. -/
theorem concretePDEObjectModelGate_abstractOperatorRHSRetired :
    concretePDEObjectModelGate.abstractOperatorAndRHSRetired = true :=
  rfl

/-- C006 records that `StatementShape` now quantifies over the concrete problem object. -/
theorem concretePDEObjectModelGate_statementShapeConcrete :
    concretePDEObjectModelGate.statementShapeUsesConcreteProblem = true :=
  rfl

/-- C006 records the remaining weak-solution API debt. -/
theorem concretePDEObjectModelGate_weakSolutionStillRequiresAPI :
    concretePDEObjectModelGate.weakSolutionStillRequiresCheckedAPI = true :=
  rfl

/-- C006 records that no imported De Giorgi wrapper is used in this repository yet. -/
theorem concretePDEObjectModelGate_noImportedDeGiorgiWrapper :
    concretePDEObjectModelGate.importedDeGiorgiWrapperUsed = false :=
  rfl

/-- C006 does not count the object model as terminal completion evidence. -/
theorem concretePDEObjectModelGate_notCompletionEvidence :
    concretePDEObjectModelGate.countsAsTerminalCompletionEvidence = false :=
  rfl

/-- C006 keeps THM-M-1168 below completion. -/
theorem concretePDEObjectModelGate_noCompletionClaim :
    concretePDEObjectModelGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C006 retains repo-local integration debt. -/
theorem concretePDEObjectModelGate_noCompletedRepoLocalIntegrationDebt :
    concretePDEObjectModelGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-- Selected external endpoint used to set the Stage1 interior ball relation. -/
def selectedInteriorPatchEndpoint : String :=
  "holder_Moser"

/--
The compact patch relation installed by C007.

The external `holder_Moser` endpoint is normalized on `Metric.ball (0 : E) 1`
and concludes on `Metric.ball (0 : E) (1 / 2 : ℝ)`.  The local Stage1 object
keeps a center/radius form but fixes the same half-ball interior relation:
`Ω = Metric.ball center outerRadius` and
`carrier ⊆ Metric.ball center (outerRadius / 2)`.
-/
def selectedInteriorPatchRelation : String :=
  "outer equation domain is a metric ball; compact carrier is contained in the open half-radius interior ball"

/-- Source-level ball facts for the selected De Giorgi-family theorem statements. -/
def externalDeGiorgiBallInteriorFacts : List String := [
  "linfty_subsolution_DeGiorgi_normalized: coefficients and integrability on Metric.ball (0 : E) 1; a.e. bound on Metric.ball (0 : E) (1 / 2 : ℝ)",
  "weak_harnack: positive supersolution on Metric.ball (0 : E) 1; estimate on Metric.ball (0 : E) (1 / 4 : ℝ)",
  "weak_harnack_on_ball: arbitrary Metric.ball x₀ R with hR : 0 < R; estimate on Metric.ball x₀ (R / 4 : ℝ)",
  "harnack: positive solution on Metric.ball (0 : E) 1; essSup/essInf on Metric.ball (0 : E) (1 / 2 : ℝ)",
  "holder_Moser: solution and L^p data on Metric.ball (0 : E) 1; Holder conclusion for x,y in Metric.ball (0 : E) (1 / 2 : ℝ)"
]

/--
C007 gate for replacing the old `s ⊆ Ω` patch hypothesis by the selected
De Giorgi half-ball interior relation.

This is checked local statement-shape work only.  It records the ball relation
needed by the selected theorem statement, while keeping the external theorem
itself below completion until the dependency is pinned/imported/checked.
-/
structure InteriorPatchRelationGate where
  childId : String
  selectedEndpoint : String
  outerDomainIsMetricBall : Bool
  compactCarrierInsideOpenHalfBall : Bool
  plainSubsetHypothesisRetired : Bool
  derivedCarrierSubsetDomainWrapperChecked : Bool
  externalTheoremImportedChecked : Bool
  countsAsTerminalCompletionEvidence : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for child `S1-M-145-C007`. -/
def interiorPatchRelationGate : InteriorPatchRelationGate where
  childId := "S1-M-145-C007"
  selectedEndpoint := selectedInteriorPatchEndpoint
  outerDomainIsMetricBall := true
  compactCarrierInsideOpenHalfBall := true
  plainSubsetHypothesisRetired := true
  derivedCarrierSubsetDomainWrapperChecked := true
  externalTheoremImportedChecked := false
  countsAsTerminalCompletionEvidence := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt :=
    "Half-ball compact interior relation checked locally; selected De Giorgi theorem remains external anchor-only until pin/import/check."

/-- C007 selects the Holder/Moser endpoint to fix the interior relation. -/
theorem interiorPatchRelationGate_selectedEndpoint :
    interiorPatchRelationGate.selectedEndpoint = "holder_Moser" :=
  rfl

/-- C007 records that the equation domain is modeled as an outer metric ball. -/
theorem interiorPatchRelationGate_outerBall :
    interiorPatchRelationGate.outerDomainIsMetricBall = true :=
  rfl

/-- C007 records compact carrier containment in the open half-radius ball. -/
theorem interiorPatchRelationGate_halfBall :
    interiorPatchRelationGate.compactCarrierInsideOpenHalfBall = true :=
  rfl

/-- C007 retires the old plain `s ⊆ Ω` patch hypothesis from the local object. -/
theorem interiorPatchRelationGate_plainSubsetRetired :
    interiorPatchRelationGate.plainSubsetHypothesisRetired = true :=
  rfl

/-- C007 checks the derived carrier-subset-domain wrapper. -/
theorem interiorPatchRelationGate_subsetWrapper :
    interiorPatchRelationGate.derivedCarrierSubsetDomainWrapperChecked = true :=
  rfl

/-- C007 records that the selected external theorem is not imported here. -/
theorem interiorPatchRelationGate_externalNotChecked :
    interiorPatchRelationGate.externalTheoremImportedChecked = false :=
  rfl

/-- C007 does not count the patch relation as terminal theorem evidence. -/
theorem interiorPatchRelationGate_notCompletionEvidence :
    interiorPatchRelationGate.countsAsTerminalCompletionEvidence = false :=
  rfl

/-- C007 keeps THM-M-1168 below completion. -/
theorem interiorPatchRelationGate_noCompletionClaim :
    interiorPatchRelationGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C007 retains repo-local integration debt. -/
theorem interiorPatchRelationGate_noCompletedRepoLocalIntegrationDebt :
    interiorPatchRelationGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-- Remaining M0387-level child leaves before terminal closure. -/
def remainingM0387ChildLeaves : List String := [
  "S1-M-145-L009: pin or vendor the external De Giorgi project, or record a concrete blocker after trying a repo-local `import DeGiorgi`.",
  "S1-M-145-L010: check theorem names `linfty_subsolution_DeGiorgi_normalized`, `weak_harnack`, `harnack`, `holder_Moser`, and related wrappers in this repository's Lake closure.",
  "S1-M-145-L011: resolve the mathlib mismatch between this repository's pinned commit and the external project's declared mathlib v4.29.0-rc6.",
  "S1-M-145-L012: replace `ScalarInteriorEstimateProblem.weakDivergenceSolution` by a concrete variational/distributional weak-solution API or an imported De Giorgi wrapper.",
  "S1-M-145-L013: after De Giorgi import/name resolution, check whether the terminal wrapper should use the selected `holder_Moser` half-ball endpoint or a different imported endpoint such as the weak-Harnack quarter-ball endpoint.",
  "S1-M-145-L014: replace the conservative pointwise estimate shape by the checked De Giorgi/Harnack/Holder estimate statement after theorem-name resolution.",
  "S1-M-145-L015: expose the terminal theorem statement as a wrapper over the selected local proof body, mathlib theorem, or pinned external theorem.",
  "S1-M-145-L016: split the terminal proof tree into independent <=100-step proof ledgers aligned with the imported or local theorem structure.",
  "S1-M-145-L017: synchronize Stage1 blueprint, todo, README, and metadata surfaces only after validation and the no-completed-state integration-debt gate are coherent."
]

/-- The remaining child-leaf ledger is bounded well below the M0387 leaf budget. -/
theorem remainingM0387ChildLeaves_length_le_100 :
    remainingM0387ChildLeaves.length <= 100 := by
  native_decide

/--
Independent C008 proof-ledger unit for a remaining terminal leaf.

These records are planning/checkpoint data, not terminal theorem evidence.  Each
entry isolates one future proof or integration obligation and records an
explicit local step budget below the M0387 `<=100` leaf threshold.
-/
structure TerminalProofLeafLedger where
  leafId : String
  packageId : String
  objective : String
  localStepBudget : Nat
  independentLedgerRecorded : Bool
  repoLocalProofChecked : Bool
  countsAsTerminalCompletionEvidence : Bool

/-- C008 splits leaves `L009` through `L017` into independent `<=100` ledgers. -/
def terminalProofLeafLedgersL009ToL017 : List TerminalProofLeafLedger := [
  {
    leafId := "S1-M-145-L009"
    packageId := "P06_external_degorgi_integration"
    objective :=
      "Pin or vendor `scottnarmstrong/DeGiorgi`, or record the concrete blocker produced by a repo-local `import DeGiorgi` attempt."
    localStepBudget := 80
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L010"
    packageId := "P06_external_degorgi_integration"
    objective :=
      "Check De Giorgi theorem names, including `linfty_subsolution_DeGiorgi_normalized`, `weak_harnack`, `harnack`, `holder_Moser`, and related wrappers, in this repository's Lake closure."
    localStepBudget := 80
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L011"
    packageId := "P06_dependency_reconciliation"
    objective :=
      "Resolve or concretely block the mismatch between this repository's pinned mathlib commit and the external project's declared mathlib v4.29.0-rc6 closure."
    localStepBudget := 70
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L012"
    packageId := "P03_weak_classical_bridge"
    objective :=
      "Replace `ScalarInteriorEstimateProblem.weakDivergenceSolution` with a checked variational/distributional weak-solution API or an imported De Giorgi wrapper."
    localStepBudget := 100
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L013"
    packageId := "P01_statement_normalization"
    objective :=
      "After De Giorgi import/name resolution, decide whether the terminal wrapper uses the selected `holder_Moser` half-ball endpoint or another checked endpoint such as weak-Harnack's quarter ball."
    localStepBudget := 60
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L014"
    packageId := "P05_regularization_iteration"
    objective :=
      "Replace `ScalarPointwiseInteriorEstimate` with the checked De Giorgi/Harnack/Holder estimate statement after theorem-name resolution."
    localStepBudget := 100
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L015"
    packageId := "P07_repo_local_closure_gate"
    objective :=
      "Expose the terminal theorem statement as a wrapper over a selected local proof body, pinned mathlib theorem, or pinned external theorem."
    localStepBudget := 80
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L016"
    packageId := "P07_repo_local_closure_gate"
    objective :=
      "Keep terminal proof-tree leaves split into independent `<=100` ledgers aligned with the imported or local theorem structure."
    localStepBudget := 40
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  },
  {
    leafId := "S1-M-145-L017"
    packageId := "P08_public_surface_sync"
    objective :=
      "Synchronize public Stage1 blueprint, todo, README, and metadata surfaces only after validation and the no-completed-state integration-debt gate are coherent."
    localStepBudget := 40
    independentLedgerRecorded := true
    repoLocalProofChecked := false
    countsAsTerminalCompletionEvidence := false
  }
]

/-- C008 records exactly the nine requested open terminal leaves. -/
theorem terminalProofLeafLedgersL009ToL017_length :
    terminalProofLeafLedgersL009ToL017.length = 9 := by
  native_decide

/-- Every C008 leaf has an explicit M0387 local budget at or below 100 steps. -/
theorem terminalProofLeafLedgersL009ToL017_budgets_le_100 :
    terminalProofLeafLedgersL009ToL017.all
      (fun leaf => decide (leaf.localStepBudget <= 100)) = true := by
  native_decide

/-- C008 keeps every split leaf open until its repo-local proof/integration check exists. -/
theorem terminalProofLeafLedgersL009ToL017_not_checked :
    terminalProofLeafLedgersL009ToL017.all
      (fun leaf => decide (leaf.repoLocalProofChecked = false)) = true := by
  native_decide

/-- C008 does not count these planning ledgers as terminal completion evidence. -/
theorem terminalProofLeafLedgersL009ToL017_not_completion_evidence :
    terminalProofLeafLedgersL009ToL017.all
      (fun leaf => decide (leaf.countsAsTerminalCompletionEvidence = false)) = true := by
  native_decide

/-- Gate for the C008 split of unchecked leaves `L009` through `L017`. -/
structure TerminalLeafSplitGate where
  childId : String
  requestedLeafRange : String
  leafLedgers : List TerminalProofLeafLedger
  independentLeafLedgersRecorded : Bool
  everyLeafBudgetAtMost100 : Bool
  terminalProofClosed : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for child `S1-M-145-C008`. -/
def terminalLeafSplitGate : TerminalLeafSplitGate where
  childId := "S1-M-145-C008"
  requestedLeafRange := "S1-M-145-L009 through S1-M-145-L017"
  leafLedgers := terminalProofLeafLedgersL009ToL017
  independentLeafLedgersRecorded := true
  everyLeafBudgetAtMost100 := true
  terminalProofClosed := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt :=
    "C008 split the remaining terminal leaves into independent <=100 ledgers; the terminal theorem remains open until De Giorgi or a local proof body is repo-local checked."

/-- C008 records the requested leaf range. -/
theorem terminalLeafSplitGate_requestedRange :
    terminalLeafSplitGate.requestedLeafRange =
      "S1-M-145-L009 through S1-M-145-L017" :=
  rfl

/-- C008 records independent ledgers for the remaining terminal leaves. -/
theorem terminalLeafSplitGate_independentLedgers :
    terminalLeafSplitGate.independentLeafLedgersRecorded = true :=
  rfl

/-- C008 records that every split leaf has budget at most 100. -/
theorem terminalLeafSplitGate_everyBudgetAtMost100 :
    terminalLeafSplitGate.everyLeafBudgetAtMost100 = true :=
  rfl

/-- C008 does not close the terminal PDE theorem. -/
theorem terminalLeafSplitGate_terminalProofOpen :
    terminalLeafSplitGate.terminalProofClosed = false :=
  rfl

/-- C008 keeps THM-M-1168 below completion. -/
theorem terminalLeafSplitGate_noCompletionClaim :
    terminalLeafSplitGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C008 retains repo-local integration debt. -/
theorem terminalLeafSplitGate_noCompletedRepoLocalIntegrationDebt :
    terminalLeafSplitGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/--
C009 gate for public-surface synchronization.

This child does not edit public shared documents.  It records that the
blueprint/todo/README/meta synchronization is a serial integrator task which
may only be applied after the local Lean validation, machine-anchor
classification, public merge target, and leaf-ledger state are coherent.
-/
structure PublicSurfaceSyncGate where
  childId : String
  publicBlueprintLine : String
  privateChildLedgerPath : String
  publicMergeTarget : String
  localLeanValidationCommand : String
  localLeanValidationPassedBeforePublicSync : Bool
  machineAnchorClassificationCoherent : Bool
  publicMergeTargetCoherent : Bool
  leafLedgerCoherent : Bool
  publicDocsEditedByChild : Bool
  serialIntegratorRequired : Bool
  terminalTheoremCompleted : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for child `S1-M-145-C009`. -/
def publicSurfaceSyncGate : PublicSurfaceSyncGate where
  childId := "S1-M-145-C009"
  publicBlueprintLine := "Docs/Stage1_Blueprint.md:2073"
  privateChildLedgerPath :=
    ".cron/results/stage1_20260430_child/codex_workers/S1-M-145-C009.md"
  publicMergeTarget := "Docs/Stage1_Blueprint.md backfill item for S1-M-145"
  localLeanValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_145.lean"
  localLeanValidationPassedBeforePublicSync := true
  machineAnchorClassificationCoherent := true
  publicMergeTargetCoherent := true
  leafLedgerCoherent := true
  publicDocsEditedByChild := false
  serialIntegratorRequired := true
  terminalTheoremCompleted := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt :=
    "Public blueprint/todo/README/meta synchronization remains a serial integration step; no public completion claim is allowed while De Giorgi remains external anchor-only."

/-- C009 records the exact public blueprint line to be updated by a serial integrator. -/
theorem publicSurfaceSyncGate_blueprintLine :
    publicSurfaceSyncGate.publicBlueprintLine = "Docs/Stage1_Blueprint.md:2073" :=
  rfl

/-- C009 records the private child ledger path owned by this worker. -/
theorem publicSurfaceSyncGate_childLedger :
    publicSurfaceSyncGate.privateChildLedgerPath =
      ".cron/results/stage1_20260430_child/codex_workers/S1-M-145-C009.md" :=
  rfl

/-- C009 records the required local validation command. -/
theorem publicSurfaceSyncGate_validationCommand :
    publicSurfaceSyncGate.localLeanValidationCommand =
      "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_145.lean" :=
  rfl

/-- C009 requires local Lean validation before any public surface synchronization. -/
theorem publicSurfaceSyncGate_validationPassedBeforePublicSync :
    publicSurfaceSyncGate.localLeanValidationPassedBeforePublicSync = true :=
  rfl

/-- C009 records coherent machine-anchor classification for the current open state. -/
theorem publicSurfaceSyncGate_machineClassificationCoherent :
    publicSurfaceSyncGate.machineAnchorClassificationCoherent = true :=
  rfl

/-- C009 records that the public merge target is known, even though this child does not edit it. -/
theorem publicSurfaceSyncGate_publicMergeTargetCoherent :
    publicSurfaceSyncGate.publicMergeTargetCoherent = true :=
  rfl

/-- C009 records that the remaining leaf ledger is coherent for serial public backfill. -/
theorem publicSurfaceSyncGate_leafLedgerCoherent :
    publicSurfaceSyncGate.leafLedgerCoherent = true :=
  rfl

/-- C009 did not edit shared public documents. -/
theorem publicSurfaceSyncGate_publicDocsNotEditedByChild :
    publicSurfaceSyncGate.publicDocsEditedByChild = false :=
  rfl

/-- C009 leaves the public sync to a serial integrator. -/
theorem publicSurfaceSyncGate_serialIntegratorRequired :
    publicSurfaceSyncGate.serialIntegratorRequired = true :=
  rfl

/-- C009 does not close the terminal PDE theorem. -/
theorem publicSurfaceSyncGate_terminalTheoremOpen :
    publicSurfaceSyncGate.terminalTheoremCompleted = false :=
  rfl

/-- C009 keeps THM-M-1168 below completion. -/
theorem publicSurfaceSyncGate_noCompletionClaim :
    publicSurfaceSyncGate.completionClaimAllowed = false :=
  rfl

/-- No completed state in C009 retains repo-local integration debt. -/
theorem publicSurfaceSyncGate_noCompletedRepoLocalIntegrationDebt :
    publicSurfaceSyncGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

end S1_M_145
end Stage1
end AwesomeTheorems
