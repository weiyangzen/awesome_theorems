import Mathlib.Analysis.Calculus.ContDiffHolder.Pointwise
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Function.ConvergenceInMeasure
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Function.UniformIntegrable

/-!
# S1-M-155 / THM-M-1224: Grillakis theorem, NLW regularity

This Stage1 artifact records a conservative Lean statement-shape boundary for a
Grillakis-type regularity theorem for nonlinear wave equations.

The pinned mathlib snapshot provides useful analysis substrates: `MemLp`,
`eLpNorm`, Frechet derivatives, pointwise Holder regularity, convergence in
measure, uniform integrability, Sobolev inequalities, and distribution/test
function APIs.  It does not provide a terminal nonlinear-wave-equation
regularity theorem.  The declarations below therefore keep the actual NLW
equation, weak/classical bridge, and compactness/finite-approximation argument
as explicit proposition fields while exposing the functional-analytic boundary
in concrete mathlib terms.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal Topology unitInterval

namespace AwesomeTheorems.Stage1.S1_M_155

universe u

/--
Abstract data needed to state an NLW regularity theorem.

The fields `classicalOrWeakNLWEquation`, `initialDataCompatibility`,
`nonlinearityRegularityPackage`, `energyEstimatePackage`, and
`compactnessOrFiniteApproximationPackage` are deliberately abstract: the
current repo-local Lean dependency closure has no canonical API for nonlinear
wave equations, finite-energy weak solutions, Strichartz/compactness machinery,
or the full Grillakis regularity theorem.
-/
structure NLWRegularityData
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] where
  timeInterval : Set ℝ
  spaceDomain : Set E
  spacetimeMeasure : Measure (ℝ × E)
  spaceMeasure : Measure E
  solution : ℝ × E → ℝ
  nonlinearity : ℝ → ℝ
  initialPosition : E → ℝ
  initialVelocity : E → ℝ
  regularityOrder : ℕ
  holderExponent : I
  timeInterval_isOpen : IsOpen timeInterval
  spaceDomain_isOpen : IsOpen spaceDomain
  solution_continuousOn :
    ContinuousOn solution (timeInterval ×ˢ spaceDomain)
  solution_memLp : MemLp solution 2 spacetimeMeasure
  initialPosition_memLp : MemLp initialPosition 2 spaceMeasure
  initialVelocity_memLp : MemLp initialVelocity 2 spaceMeasure
  classicalOrWeakNLWEquation : Prop
  initialDataCompatibility : Prop
  nonlinearityRegularityPackage : Prop
  energyEstimatePackage : Prop
  compactnessOrFiniteApproximationPackage : Prop

/--
A low-regularity energy bound that can be expressed directly with mathlib's
`eLpNorm` and classical Frechet derivative notation.
-/
def BasicEnergyBound
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (D : NLWRegularityData E) (C : ℝ≥0∞) : Prop :=
  eLpNorm D.solution 2 D.spacetimeMeasure ≤ C ∧
    eLpNorm (fun z => fderiv ℝ D.solution z) 2 D.spacetimeMeasure ≤ C

/-- The abstract PDE-side hypotheses that a terminal formalization must replace. -/
def RegularityHypotheses
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (D : NLWRegularityData E) : Prop :=
  D.classicalOrWeakNLWEquation ∧
    D.initialDataCompatibility ∧
      D.nonlinearityRegularityPackage ∧
        D.energyEstimatePackage ∧
          D.compactnessOrFiniteApproximationPackage

/--
The concrete regularity conclusion carried by this statement shape.

The target is intentionally local on the spacetime cylinder and expressed using
mathlib's pointwise Holder API rather than a not-yet-selected Sobolev/Hilbert
scale for NLW.
-/
def RegularityConclusion
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (D : NLWRegularityData E) : Prop :=
  ∀ z ∈ D.timeInterval ×ˢ D.spaceDomain,
    ContDiffPointwiseHolderAt D.regularityOrder D.holderExponent D.solution z

/--
Stage1 normalized statement shape for Grillakis' NLW regularity theorem.

For every normed real spatial model and every data package satisfying the
abstract NLW equation, initial-data, nonlinearity, energy, and compactness
packages, the solution has the stated local pointwise Holder regularity on the
spacetime cylinder.
-/
def StatementShape
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] :
    Prop :=
  ∀ D : NLWRegularityData E,
    RegularityHypotheses D → RegularityConclusion D

/-- The statement shape unfolds to the expected implication over all data packages. -/
theorem statementShape_iff_forall_data
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] :
    StatementShape E ↔
      ∀ D : NLWRegularityData E,
        RegularityHypotheses D → RegularityConclusion D :=
  Iff.rfl

/-- The energy bound exposes the solution's `L^2` control. -/
theorem BasicEnergyBound.solution_eLpNorm_le
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    {D : NLWRegularityData E} {C : ℝ≥0∞}
    (h : BasicEnergyBound D C) :
    eLpNorm D.solution 2 D.spacetimeMeasure ≤ C :=
  h.1

/-- The energy bound exposes the derivative's `L^2` control. -/
theorem BasicEnergyBound.fderiv_eLpNorm_le
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    {D : NLWRegularityData E} {C : ℝ≥0∞}
    (h : BasicEnergyBound D C) :
    eLpNorm (fun z => fderiv ℝ D.solution z) 2 D.spacetimeMeasure ≤ C :=
  h.2

/--
If a later proof already has sufficiently high classical `ContDiffAt`
regularity on the spacetime cylinder, mathlib supplies the requested pointwise
Holder regularity.
-/
theorem regularityConclusion_of_contDiffAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    (D : NLWRegularityData E) {n : WithTop ℕ∞}
    (hu : ∀ z ∈ D.timeInterval ×ˢ D.spaceDomain, ContDiffAt ℝ n D.solution z)
    (hk : D.regularityOrder < n) :
    RegularityConclusion D := by
  intro z hz
  exact (hu z hz).contDiffPointwiseHolderAt hk D.holderExponent

/-- The PDE-side hypotheses project to the abstract NLW equation field. -/
theorem RegularityHypotheses.classicalOrWeakNLWEquation
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    {D : NLWRegularityData E}
    (h : RegularityHypotheses D) :
    D.classicalOrWeakNLWEquation :=
  h.1

/-- The PDE-side hypotheses project to the initial-data compatibility field. -/
theorem RegularityHypotheses.initialDataCompatibility
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    {D : NLWRegularityData E}
    (h : RegularityHypotheses D) :
    D.initialDataCompatibility :=
  h.2.1

/-- The PDE-side hypotheses project to the nonlinearity regularity field. -/
theorem RegularityHypotheses.nonlinearityRegularityPackage
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    {D : NLWRegularityData E}
    (h : RegularityHypotheses D) :
    D.nonlinearityRegularityPackage :=
  h.2.2.1

/-- The PDE-side hypotheses project to the energy-estimate field. -/
theorem RegularityHypotheses.energyEstimatePackage
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    {D : NLWRegularityData E}
    (h : RegularityHypotheses D) :
    D.energyEstimatePackage :=
  h.2.2.2.1

/-- The PDE-side hypotheses project to the compactness/approximation field. -/
theorem RegularityHypotheses.compactnessOrFiniteApproximationPackage
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    {D : NLWRegularityData E}
    (h : RegularityHypotheses D) :
    D.compactnessOrFiniteApproximationPackage :=
  h.2.2.2.2

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.MeasureTheory.Function.UniformIntegrable",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Calculus.ContDiffHolder.Pointwise",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Deriv"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.TendstoInMeasure",
  "MeasureTheory.UnifIntegrable",
  "MeasureTheory.UniformIntegrable",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "ContDiffPointwiseHolderAt",
  "ContDiffAt.contDiffPointwiseHolderAt",
  "Distribution",
  "fderiv"
]

/--
The mathlib revision used by the Stage1 audit that produced this statement
shape.
-/
def checkedMathlibRevision : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Machine-status metadata for this file.  This is intentionally weaker than a
terminal Grillakis/NLW theorem proof.
-/
def repoLocalMachineStatus : String := "statement_shape_local_checked"

/--
This artifact does not claim completion of Grillakis' nonlinear-wave-equation
regularity theorem.
-/
def terminalGrillakisTheoremCompleted : Bool := false

/--
Search terms that did not locate a terminal Grillakis/NLW theorem in pinned
mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Grillakis",
  "nonlinear wave",
  "wave equation",
  "WaveEquation",
  "NLW",
  "Strichartz",
  "Shatah",
  "Struwe",
  "KleinGordon",
  "critical wave"
]

/--
C004 public-blocker payload for the later serialized blueprint/todo backfill.

This is deliberately metadata, not terminal theorem evidence.  The current
Stage1 pass found no pinned mathlib theorem and no external Lean 4 theorem
closing Grillakis' nonlinear-wave-equation regularity theorem, so the
repo-local completion gate remains closed.
-/
def c004PublicBlocker : String :=
  "no pinned mathlib or external Lean 4 theorem for Grillakis' nonlinear-wave-equation regularity theorem was found in this pass"

/--
C004 machine-debt classification.

No external Lean 4 proof body was identified, so there is no known upstream
machine theorem left as anchor-only `repo_local_integration_debt`.  The terminal
PDE theorem remains formalization debt, while this file is only a checked
statement-shape artifact.
-/
def c004MachineDebtClassification : List String := [
  "formalization_debt: terminal Grillakis/NLW regularity theorem is not repo-local closed",
  "not_repo_local_closed: this file is a statement-shape artifact plus checked adjacent mathlib anchors",
  "repo_local_integration_debt_gate: passed only as a non-completion finding because no external Lean 4 closure was found"
]

/-- C004 exact blocker text is fixed for public-doc integration. -/
theorem c004PublicBlocker_eq :
    c004PublicBlocker =
      "no pinned mathlib or external Lean 4 theorem for Grillakis' nonlinear-wave-equation regularity theorem was found in this pass" :=
  rfl

/--
C005 theorem-tree leaf inventory for the later serialized public blueprint
backfill.  These strings are metadata only: checked leaves name locally
validated statement-shape or anchor-budget work, while unchecked leaves are
future terminal PDE/integration obligations.
-/
def c005TheoremTreeLeaves : List String := [
  "G-NLW-L001 [checked] A1: explicit universe and spatial model selected; local steps: 6",
  "G-NLW-L002 [checked] A2: spacetime cylinder represented as R x E and timeInterval x spaceDomain; local steps: 8",
  "G-NLW-L003 [checked] A3: solution, nonlinearity, and initial data represented as concrete functions; local steps: 8",
  "G-NLW-L004 [checked] A4: MemLp fields and BasicEnergyBound with eLpNorm defined; local steps: 16",
  "G-NLW-L005 [checked] A5: RegularityConclusion uses ContDiffPointwiseHolderAt; local steps: 8",
  "G-NLW-L006 [checked] B1: local probes validated MeasureTheory.MemLp and MeasureTheory.eLpNorm; local steps: 4",
  "G-NLW-L007 [checked] B2: local artifact validates fderiv in BasicEnergyBound; Sobolev inequality module imported; local steps: 10",
  "G-NLW-L008 [checked] B3: local probes validated MeasureTheory.TendstoInMeasure and MeasureTheory.UniformIntegrable; local steps: 6",
  "G-NLW-L009 [checked] B4: local probe validated Distribution; distribution modules audited; local steps: 6",
  "G-NLW-L010 [unchecked] B5: complete authenticated external Lean 4 source search for Grillakis/NLW terminal theorem; estimated local steps: 30",
  "G-NLW-L011 [unchecked] C1: choose and define the exact NLW equation variant and nonlinearity class; estimated local steps: 80",
  "G-NLW-L012 [unchecked] C2: define finite-energy weak solution and distribution/weak derivative formulation; estimated local steps: 95",
  "G-NLW-L013 [unchecked] C3: prove weak/classical formulation bridge under adequate regularity; estimated local steps: 90",
  "G-NLW-L014 [unchecked] C4: encode initial data and boundary/domain conditions precisely; estimated local steps: 70",
  "G-NLW-L015 [unchecked] D1: formalize local energy inequality or conservation package; estimated local steps: 90",
  "G-NLW-L016 [unchecked] D2: formalize finite-dimensional approximation or compactness branch; estimated local steps: 95",
  "G-NLW-L017 [unchecked] D3: formalize nonlinear estimate package; estimated local steps: 95",
  "G-NLW-L018 [unchecked] D4: terminal Grillakis regularity upgrade wrapper; estimated local steps: 70 after C/D prerequisites",
  "G-NLW-L019 [checked] E1: validate repo-local statement-shape artifact; local steps: 5",
  "G-NLW-L020 [unchecked] E2: pin/import/check any future external Lean proof or record concrete blocker; estimated local steps: 40",
  "G-NLW-L021 [unchecked] E3: public blueprint/todo/README synchronization by later integrator; estimated local steps: 30"
]

/-- C005 leaves that must remain unchecked in the public backfill. -/
def c005UncheckedTerminalLeaves : List String := [
  "G-NLW-L010",
  "G-NLW-L011",
  "G-NLW-L012",
  "G-NLW-L013",
  "G-NLW-L014",
  "G-NLW-L015",
  "G-NLW-L016",
  "G-NLW-L017",
  "G-NLW-L018",
  "G-NLW-L020",
  "G-NLW-L021"
]

/-- C005 exact unchecked-leaf set for public-doc integration. -/
theorem c005UncheckedTerminalLeaves_eq :
    c005UncheckedTerminalLeaves =
      ["G-NLW-L010",
        "G-NLW-L011",
        "G-NLW-L012",
        "G-NLW-L013",
        "G-NLW-L014",
        "G-NLW-L015",
        "G-NLW-L016",
        "G-NLW-L017",
        "G-NLW-L018",
        "G-NLW-L020",
        "G-NLW-L021"] :=
  rfl

/--
C006 requested external-audit query terms.

The authenticated GitHub code-search gate is an external process requirement,
not proof evidence.  These terms are kept in Lean only as serialized metadata
for the later public backfill.
-/
def c006RequestedAuditTerms : List String := [
  "Grillakis",
  "nonlinear wave",
  "wave equation",
  "WaveEquation",
  "NLW",
  "Strichartz",
  "Shatah",
  "Struwe",
  "KleinGordon",
  "critical wave"
]

/--
C006 audit execution status.

On 2026-05-01, `gh auth status` reported that no GitHub host was logged in and
no `GH_TOKEN`/`GITHUB_TOKEN` environment credential was available.  The
authenticated primary-source GitHub code-search gate therefore remains open.
-/
def c006AuthenticatedGitHubAuditStatus : String :=
  "blocked: gh auth status reported no logged-in GitHub host and no GH_TOKEN/GITHUB_TOKEN credential was available on 2026-05-01"

/--
C006 fallback source-audit summary.

Fallback checks found no candidate terminal Lean 4 proof: local `rg` over the
pinned mathlib checkout matched the requested PDE terms only in this Stage1
artifact, and unauthenticated GitHub repository searches for the requested
terms plus Lean found no plausible Lean theorem project.  GitHub code search
was not authenticated and then hit the unauthenticated API rate limit, so this
is not a completed authenticated audit.
-/
def c006FallbackAuditSummary : String :=
  "fallback only: no candidate terminal Lean 4 proof found in pinned mathlib or unauthenticated GitHub repository metadata; authenticated GitHub code search still required"

/--
C006 repo-local integration-debt gate.

No external Lean 4 proof body was identified by the fallback search, so this
pass did not create a concrete `repo_local_integration_debt` item.  Because the
authenticated GitHub code-search gate did not run, the child remains blocked
rather than completed.
-/
def c006RepoLocalIntegrationDebtGate : String :=
  "open: no external proof was identified by fallback search, but authenticated GitHub code search was blocked; do not mark completed"

/-- C006 exact authentication-blocker text for public-doc integration. -/
theorem c006AuthenticatedGitHubAuditStatus_eq :
    c006AuthenticatedGitHubAuditStatus =
      "blocked: gh auth status reported no logged-in GitHub host and no GH_TOKEN/GITHUB_TOKEN credential was available on 2026-05-01" :=
  rfl

/-!
## C007 variant decision

The Stage1 source phrase `NLW的正则性` is too broad for a terminal Lean target.
For this Grillakis slot, C007 fixes the canonical variant to the three-dimensional
defocusing energy-critical quintic wave equation.  This is still metadata: the
repo has no local nonlinear-wave-equation API or proof of the PDE theorem.
-/

/-- C007 metadata record for the selected Grillakis/NLW theorem variant. -/
structure NLWVariantDecision where
  spatialDimension : Nat
  spacetimeDimension : Nat
  equation : String
  nonlinearityPower : Nat
  nonlinearityClass : String
  criticalRegime : String
  initialDataSpace : String
  solutionNotion : String
  targetRegularity : String
  excludedVariants : List String
  sourceBasis : List String
  formalizationStatus : String

/--
C007 canonical variant behind `NLW的正则性`.

The chosen target is Grillakis' smooth/global-regularity theorem for the
defocusing energy-critical quintic wave equation in `3 + 1` dimensions.  Later
energy-class well-posedness/scattering extensions are recorded as adjacent
context, not as this child task's theorem variant.
-/
def c007CanonicalVariant : NLWVariantDecision where
  spatialDimension := 3
  spacetimeDimension := 4
  equation := "partial_t^2 u - Delta u + u^5 = 0 on R x R^3"
  nonlinearityPower := 5
  nonlinearityClass := "pure defocusing quintic power nonlinearity f(u) = u^5"
  criticalRegime :=
    "energy-critical in dimension 3; scaling-critical Sobolev exponent s_c = 1; not subcritical"
  initialDataSpace :=
    "smooth Cauchy data in the classical finite-energy/compact-support formulation used for global smooth solutions; energy-class Hdot^1 x L^2 is an adjacent later extension, not this C007 target"
  solutionNotion :=
    "global classical smooth solution; finite-energy weak-solution and weak/classical bridge remain future formalization debt"
  targetRegularity :=
    "global-in-time C_infty regularity/persistence of smoothness for the solution"
  excludedVariants := [
    "general nonlinearities f(u)",
    "subcritical powers 1 < p < 5",
    "supercritical powers p > 5",
    "bounded-domain or obstacle variants",
    "radial-only variants",
    "energy-class scattering theorem as the primary statement"
  ]
  sourceBasis := [
    "Annals of Mathematics 132(3), 485-509, 1990: Grillakis, Regularity and asymptotic behavior of the wave equation with a critical nonlinearity",
    "Communications on Pure and Applied Mathematics 45(6), 749-774, 1992: Grillakis, Regularity for the wave equation with a critical nonlinearity",
    "Tao 2006 arXiv:math/0601164 identifies the established energy-critical NLW as Box u = u^5 in R^{1+3}",
    "Roy, Global existence of smooth solutions of a 3D log-log energy-supercritical wave equation, introduction: p = 5 gives s_c = 1 and Grillakis established global smooth regularity for the 3D energy-critical equation"
  ]
  formalizationStatus :=
    "variant_decision_metadata_only: no terminal repo-local Lean proof; no completed state may be claimed"

/-- C007 public-doc status for the variant decision. -/
def c007VariantDecisionStatus : String :=
  "decided: target the 3D defocusing energy-critical quintic NLW smooth/global-regularity theorem; terminal Lean proof remains formalization_debt"

/-- C007 repo-local integration-debt gate for the variant decision. -/
def c007RepoLocalIntegrationDebtGate : String :=
  "passed as non-completion metadata: no external Lean proof was identified or left anchor-only completed; terminal theorem remains not_repo_local_closed"

/-- C007 pins the selected spatial dimension. -/
theorem c007CanonicalVariant_spatialDimension_eq :
    c007CanonicalVariant.spatialDimension = 3 :=
  rfl

/-- C007 pins the selected nonlinearity power. -/
theorem c007CanonicalVariant_nonlinearityPower_eq :
    c007CanonicalVariant.nonlinearityPower = 5 :=
  rfl

/-- C007 pins the nonterminal status text. -/
theorem c007VariantDecisionStatus_eq :
    c007VariantDecisionStatus =
      "decided: target the 3D defocusing energy-critical quintic NLW smooth/global-regularity theorem; terminal Lean proof remains formalization_debt" :=
  rfl

/-! ## C008 shared aggregator import decision -/

/--
C008 metadata for the later serialized decision about shared Lean aggregators.

This worker is not allowed to edit `AwesomeTheorems.lean`, `lakefile.lean`, or
any other shared import surface.  The record therefore stores the exact import
line and the gate a later integrator must satisfy before changing the default
build surface.
-/
structure SharedAggregatorDecision where
  candidateImportLine : String
  addInThisWorkerPatch : Bool
  recommendedSerializedAction : String
  directValidationCommand : String
  aggregateValidationCommand : String
  completionBoundary : String

/--
C008 decision payload.

The S1-M-155 artifact is import-ready as an individual Lean module, but the
shared aggregator should be changed only by a serialized integrator patch that
also reruns the aggregate check and updates public planning surfaces.
-/
def c008SharedAggregatorDecision : SharedAggregatorDecision where
  candidateImportLine := "import AwesomeTheorems.Stage1.S1_M_155"
  addInThisWorkerPatch := false
  recommendedSerializedAction :=
    "defer shared aggregator edit to a serialized integrator patch; add the candidate import only if Stage1 artifacts are intentionally adopted into the default AwesomeTheorems build surface"
  directValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_155.lean"
  aggregateValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems.lean"
  completionBoundary :=
    "aggregator decision metadata only; does not prove the terminal Grillakis/NLW regularity theorem and does not close S1-M-155"

/-- C008 pins the exact candidate import line for later integrator use. -/
theorem c008SharedAggregatorDecision_candidateImportLine_eq :
    c008SharedAggregatorDecision.candidateImportLine =
      "import AwesomeTheorems.Stage1.S1_M_155" :=
  rfl

/-- C008 records that this worker patch must not edit the shared aggregator. -/
theorem c008SharedAggregatorDecision_addInThisWorkerPatch_eq :
    c008SharedAggregatorDecision.addInThisWorkerPatch = false :=
  rfl

/-- C008 pins the non-completion boundary for the aggregator decision. -/
theorem c008SharedAggregatorDecision_completionBoundary_eq :
    c008SharedAggregatorDecision.completionBoundary =
      "aggregator decision metadata only; does not prove the terminal Grillakis/NLW regularity theorem and does not close S1-M-155" :=
  rfl

/-! ## Audit probes -/

#check NLWRegularityData
#check BasicEnergyBound
#check RegularityHypotheses
#check RegularityConclusion
#check StatementShape
#check regularityConclusion_of_contDiffAt
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
#check fderiv
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check MeasureTheory.TendstoInMeasure
#check MeasureTheory.UniformIntegrable
#check ContDiffPointwiseHolderAt
#check ContDiffAt.contDiffPointwiseHolderAt
#check Distribution
#check checkedMathlibRevision
#check repoLocalMachineStatus
#check terminalGrillakisTheoremCompleted
#check c004PublicBlocker
#check c004MachineDebtClassification
#check c004PublicBlocker_eq
#check c005TheoremTreeLeaves
#check c005UncheckedTerminalLeaves
#check c005UncheckedTerminalLeaves_eq
#check c006RequestedAuditTerms
#check c006AuthenticatedGitHubAuditStatus
#check c006FallbackAuditSummary
#check c006RepoLocalIntegrationDebtGate
#check c006AuthenticatedGitHubAuditStatus_eq
#check NLWVariantDecision
#check c007CanonicalVariant
#check c007VariantDecisionStatus
#check c007RepoLocalIntegrationDebtGate
#check c007CanonicalVariant_spatialDimension_eq
#check c007CanonicalVariant_nonlinearityPower_eq
#check c007VariantDecisionStatus_eq
#check SharedAggregatorDecision
#check c008SharedAggregatorDecision
#check c008SharedAggregatorDecision_candidateImportLine_eq
#check c008SharedAggregatorDecision_addInThisWorkerPatch_eq
#check c008SharedAggregatorDecision_completionBoundary_eq

end AwesomeTheorems.Stage1.S1_M_155
