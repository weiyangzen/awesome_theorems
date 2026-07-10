import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Distribution.FourierMultiplier
import Mathlib.Analysis.Fourier.Convolution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Topology.ContinuousMap.Basic

/-!
# S1-M-154 / THM-M-1216: Kenig-Ponce-Vega low-regularity theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Kenig-Ponce-Vega theorem family on low-regularity well-posedness for dispersive
equations.

The pinned mathlib snapshot has substantial adjacent analysis infrastructure:
Fourier transforms, Schwartz maps, tempered distributions, Fourier multipliers,
`Lp`/`MemLp`, continuity predicates, Frechet derivatives, and a
Gagliardo-Nirenberg-Sobolev inequality.  This audit did not find a terminal
Kenig-Ponce-Vega, KdV, Bourgain-space, or dispersive well-posedness theorem.

The declarations below therefore avoid proof placeholders and false completion
claims.  They normalize the expected well-posedness interface and include only
small checked wrappers around available mathlib facts.
-/

noncomputable section

open MeasureTheory
open scoped FourierTransform NNReal ENNReal SchwartzMap Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_154

universe u

/--
Abstract data for a low-regularity dispersive initial-value problem.

`Phase` should later be replaced by a concrete Sobolev or Bourgain-type phase
space.  The proposition-valued estimate fields mark the exact formalization
boundary: a terminal KPV formalization must provide the linear dispersive
estimate, nonlinear estimate, and fixed-point or compactness closure in concrete
mathlib objects rather than treating this structure as a completed theorem.
-/
structure KPVProblem (Phase : Type u) [TopologicalSpace Phase] : Type u where
  regularity : ℝ
  equationName : String
  timeDomain : Set ℝ
  dataSet : Set Phase
  solution : Phase → ℝ → Phase
  IsSolution : Phase → (ℝ → Phase) → Prop
  uniquenessClass : (ℝ → Phase) → Prop
  lowRegularityRegime : Prop
  linearDispersiveEstimate : Prop
  nonlinearEstimate : Prop
  contractionOrCompactnessClosure : Prop

/-- The solution-flow map associated to the abstract dispersive problem. -/
def FlowMap {Phase : Type u} [TopologicalSpace Phase] (P : KPVProblem Phase) :
    Phase → (ℝ → Phase) :=
  fun u0 t => P.solution u0 t

/-- Continuous dependence of the flow map on the initial data set. -/
def FlowMapContinuousOn {Phase : Type u} [TopologicalSpace Phase]
    (P : KPVProblem Phase) : Prop :=
  ContinuousOn (FlowMap P) P.dataSet

/--
Hadamard-style local well-posedness package for the abstract KPV boundary.

The statement records existence, uniqueness in the selected uniqueness class,
continuous dependence, and a separated persistence/a-priori branch.  It is not a
terminal proof of any specific dispersive PDE.
-/
structure LocalWellPosedData {Phase : Type u} [TopologicalSpace Phase]
    (P : KPVProblem Phase) : Prop where
  existence : ∀ u0 ∈ P.dataSet, P.IsSolution u0 (FlowMap P u0)
  uniqueness :
    ∀ u0 ∈ P.dataSet, ∀ v : ℝ → Phase,
      P.uniquenessClass v → P.IsSolution u0 v → v = FlowMap P u0
  continuousDependence : FlowMapContinuousOn P
  persistenceOrAPrioriBound : P.contractionOrCompactnessClosure

/--
Normalized Stage1 statement shape for the Kenig-Ponce-Vega low-regularity theorem family.

For every concrete phase space and dispersive problem, if the low-regularity
regime and the linear/nonlinear/closure packages have been supplied, then the
associated initial-value problem is locally well posed.  The hard KPV content is
kept as explicit hypotheses because no terminal Lean 4 proof of those estimates
was found in the local dependency closure.
-/
def StatementShape : Prop :=
  ∀ (Phase : Type u) [TopologicalSpace Phase] (P : KPVProblem Phase),
    P.lowRegularityRegime →
      P.linearDispersiveEstimate →
        P.nonlinearEstimate →
          P.contractionOrCompactnessClosure →
            LocalWellPosedData P

/--
The public Stage1 variant frozen by the child statement-normalization pass.

The selected reading is the real-line KdV local well-posedness theorem from
Kenig-Ponce-Vega's 1996 JAMS paper, "A bilinear estimate with applications to
the KdV equation": the equation is `u_t + u_xxx + u * u_x = 0`, the initial data
space is the inhomogeneous Sobolev scale `H^s(R)`, the threshold convention is
`s > -3 / 4`, the time interval is local and symmetric, and the conclusion is
Hadamard local well-posedness with the solution path in `C(I, H^s(R))` and
uniqueness/construction in a Bourgain `X^{s,b}` restriction class.

This Lean object deliberately records the public theorem boundary as metadata
and equalities against `KPVProblem`.  It is not a Sobolev-space definition, a
Bourgain-space API, or a proof of the KPV theorem.
-/
inductive FrozenKPVEquationVariant : Type
  | realLineKdV
deriving DecidableEq, Repr

/-- Initial-data space selected for the public KPV Stage1 statement. -/
inductive FrozenKPVDataSpace : Type
  | inhomogeneousSobolevHsRealLine
deriving DecidableEq, Repr

/-- Time-domain convention selected for the public KPV Stage1 statement. -/
inductive FrozenKPVTimeIntervalKind : Type
  | localSymmetricClosedInterval
deriving DecidableEq, Repr

/-- Conclusion type selected for the public KPV Stage1 statement. -/
inductive FrozenKPVConclusionKind : Type
  | localHadamardWellPosednessWithBourgainUniqueness
deriving DecidableEq, Repr

/-- Frozen equation variant: real-line KdV. -/
def selectedEquationVariant : FrozenKPVEquationVariant :=
  FrozenKPVEquationVariant.realLineKdV

/-- Frozen initial-data space: inhomogeneous Sobolev `H^s(R)`. -/
def selectedDataSpace : FrozenKPVDataSpace :=
  FrozenKPVDataSpace.inhomogeneousSobolevHsRealLine

/-- Frozen time-domain convention: a local symmetric interval `[-T, T]`. -/
def selectedTimeIntervalKind : FrozenKPVTimeIntervalKind :=
  FrozenKPVTimeIntervalKind.localSymmetricClosedInterval

/-- Frozen conclusion type: local Hadamard well-posedness with Bourgain-space uniqueness. -/
def selectedConclusionKind : FrozenKPVConclusionKind :=
  FrozenKPVConclusionKind.localHadamardWellPosednessWithBourgainUniqueness

/-- Human-readable equation label used to bind the abstract `KPVProblem` field. -/
def selectedEquationDescription : String :=
  "real-line KdV: u_t + u_xxx + u * u_x = 0"

/-- Human-readable data-space label used until a concrete Sobolev API is selected. -/
def selectedDataSpaceDescription : String :=
  "inhomogeneous Sobolev space H^s(R)"

/-- Human-readable conclusion label used until concrete Bourgain-space APIs are selected. -/
def selectedConclusionDescription : String :=
  "local Hadamard well-posedness in C([-T,T], H^s(R)) with Bourgain X^{s,b} uniqueness"

/-- KPV regularity threshold for the selected real-line KdV variant. -/
def selectedRegularityThreshold : ℝ :=
  -(3 / 4)

/-- Regularities covered by the selected public KPV variant. -/
def SelectedRegularity (s : ℝ) : Prop :=
  selectedRegularityThreshold < s

/-- The selected local symmetric time interval `[-T, T]`. -/
def selectedLocalTimeInterval (T : ℝ) : Set ℝ :=
  {t : ℝ | -T ≤ t ∧ t ≤ T}

/--
Checked record tying an abstract `KPVProblem` to the frozen public KPV variant.

`dataSet` is the intended `H^s(R)` subset of the eventual phase-space model.  It
remains abstract because the current repo-local dependency closure does not yet
provide the Sobolev/Bourgain APIs needed for a terminal KPV statement.
-/
structure FrozenKPVVariant (Phase : Type u) [TopologicalSpace Phase] : Type u where
  s : ℝ
  T : ℝ
  T_pos : 0 < T
  dataSet : Set Phase
  problem : KPVProblem Phase
  regularityRange : SelectedRegularity s
  equationVariant : FrozenKPVEquationVariant
  equationVariant_eq : equationVariant = selectedEquationVariant
  dataSpace : FrozenKPVDataSpace
  dataSpace_eq : dataSpace = selectedDataSpace
  timeIntervalKind : FrozenKPVTimeIntervalKind
  timeIntervalKind_eq : timeIntervalKind = selectedTimeIntervalKind
  conclusionKind : FrozenKPVConclusionKind
  conclusionKind_eq : conclusionKind = selectedConclusionKind
  problemRegularity : problem.regularity = s
  problemEquation : problem.equationName = selectedEquationDescription
  problemTimeDomain : problem.timeDomain = selectedLocalTimeInterval T
  problemDataSet : problem.dataSet = dataSet
  problemLowRegularityRegime : problem.lowRegularityRegime = SelectedRegularity s

/--
Frozen public statement boundary for this Stage1 slot.

The low-regularity regime is supplied by the checked frozen-variant witness
`V.regularityRange`, so this statement no longer treats that field as an
independent proposition-valued hypothesis.  The hard linear, nonlinear, and
closure packages remain explicit hypotheses recorded inside `KPVProblem`; this
therefore supports statement normalization only, not a completion claim.
-/
def FrozenVariantStatement : Prop :=
  ∀ (Phase : Type u) [TopologicalSpace Phase] (V : FrozenKPVVariant Phase),
    V.problem.linearDispersiveEstimate →
      V.problem.nonlinearEstimate →
        V.problem.contractionOrCompactnessClosure →
          LocalWellPosedData V.problem

/-- Current public Stage1 theorem variant selected for THM-M-1216. -/
def FrozenTheoremVariant : Prop :=
  FrozenVariantStatement.{u}

/--
Formalization route selected by the target-decision pass.

The choices distinguish a Sobolev-only Hadamard statement, a Bourgain
restriction-space proof target with a Sobolev trace conclusion, and a wrapper
around a pinned upstream development.  The current local dependency closure does
not provide a pinned upstream KPV theorem, so the selected target is the
Bourgain route rather than an upstream wrapper.
-/
inductive FormalTargetRoute : Type
  | sobolevSpaceHadamardOnly
  | bourgainXsbLocalWellPosedness
  | pinnedUpstreamAbstractWrapper
deriving DecidableEq, Repr

/--
Selected formal target for the KPV Stage1 slot.

The intended terminal statement should construct/control the solution in a
Bourgain `X^{s,b}` restriction class and then expose the Sobolev
`C([-T,T], H^s(R))` well-posedness conclusion.  The existing `KPVProblem`
wrapper remains an interim statement boundary, not a completion route.
-/
def selectedFormalTargetRoute : FormalTargetRoute :=
  FormalTargetRoute.bourgainXsbLocalWellPosedness

/-- Machine-readable route decision status for the child C002 pass. -/
def selectedFormalTargetRouteStatus : String :=
  "selected_bourgain_xsb_local_well_posedness_with_sobolev_trace_conclusion"

/-- Reasons for rejecting a Sobolev-only formal target as the terminal KPV route. -/
def sobolevOnlyTargetRejectionReasons : List String := [
  "KPV low-regularity KdV proof route uses Bourgain restriction-space estimates below classical energy regularity.",
  "A Sobolev-only statement would hide the uniqueness/contraction class needed by the selected theorem boundary.",
  "The current repo-local dependency closure has no concrete Sobolev-space well-posedness theorem proving the KPV result."
]

/-- Reasons for rejecting a pinned-upstream wrapper as the current formal target. -/
def pinnedUpstreamWrapperRejectionReasons : List String := [
  "No pinned/imported/checked upstream Lean 4 KPV theorem is present in this repository.",
  "The local artifact records adjacent mathlib Fourier/Sobolev/distribution anchors only.",
  "An anchor-only upstream note would be repo_local_integration_debt and cannot support completion."
]

/-- Concrete blockers before the selected Bourgain route can become a terminal proof. -/
def selectedBourgainTargetBlockers : List String := [
  "Define or import a concrete Bourgain X^{s,b} restriction-space API for the Airy/KdV phase.",
  "Define the inhomogeneous Sobolev H^s(R) data/trace object used by the final conclusion.",
  "Provide the Airy propagator Fourier-multiplier representation.",
  "Provide the linear dispersive/smoothing estimates and the KPV bilinear estimate at s > -3/4.",
  "Replace the proposition-valued KPVProblem estimate fields by concrete imported theorem hypotheses or local proof bodies."
]

/-- Machine-status bucket for the C003 Sobolev/Bourgain API audit. -/
inductive APIAuditMachineStatus : Type
  | repoLocalPinnedChecked
  | externalAnchorOnlyNotPinned
  | irrelevantNameCollision
  | missingTerminalKPVAPI
deriving DecidableEq, Repr

/--
One row in the C003 audit of Sobolev/Bourgain-space Lean 4 APIs.

External rows are deliberately metadata only.  They are not imported by this
repository and therefore cannot close the parent KPV theorem.
-/
structure LeanAPIAuditEntry : Type where
  repositoryURL : String
  commitSHA : String
  toolchain : String
  modules : List String
  declarationNames : List String
  placeholderStatus : String
  relevanceToKPV : String
  machineStatus : APIAuditMachineStatus
deriving Repr

/-- mathlib row for the C003 Sobolev/Bourgain API audit. -/
def mathlibSobolevBourgainAPIAuditEntry : LeanAPIAuditEntry where
  repositoryURL := "https://github.com/leanprover-community/mathlib4"
  commitSHA := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  toolchain := "leanprover/lean4:v4.29.0"
  modules := [
    "Mathlib.MeasureTheory.Function.LpSeminorm.Defs",
    "Mathlib.MeasureTheory.Function.LpSpace.Basic",
    "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
    "Mathlib.Analysis.Fourier.FourierTransform",
    "Mathlib.Analysis.Fourier.Convolution",
    "Mathlib.Analysis.Distribution.FourierMultiplier",
    "Mathlib.Analysis.Distribution.TemperedDistribution",
    "Mathlib.Analysis.Distribution.SchwartzSpace.Fourier"
  ]
  declarationNames := [
    "MeasureTheory.MemLp",
    "MeasureTheory.Lp",
    "MeasureTheory.eLpNorm",
    "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
    "Lp.fourierTransform",
    "Lp.fourierTransformCLM",
    "SchwartzMap.fourier_convolution",
    "TemperedDistribution",
    "TemperedDistribution.fourierMultiplierCLM",
    "TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM",
    "TemperedDistribution.laplacian_eq_fourierMultiplierCLM"
  ]
  placeholderStatus :=
    "repo-local pinned mathlib dependency; selected wrappers compile; no Lean proof-placeholder tokens introduced here"
  relevanceToKPV :=
    "Provides adjacent Lp, Fourier, tempered-distribution, Fourier-multiplier, and Gagliardo-Nirenberg-Sobolev anchors; does not provide H^s(R), Bourgain X^{s,b}, KdV, or KPV well-posedness APIs."
  machineStatus := APIAuditMachineStatus.repoLocalPinnedChecked

/--
External Lean 4 candidate with concrete Fourier-side Sobolev infrastructure.

This is useful as an API reconnaissance result, but it is on `T^2`, is not
imported by this repository, and does not state the real-line KPV theorem.
-/
def sqgFourierSobolevAPIAuditEntry : LeanAPIAuditEntry where
  repositoryURL := "https://github.com/Brsanch/sqg-lean-proofs-fourier"
  commitSHA := "ce02796e3d3ba91101fa86629c73d35ee7056ccf"
  toolchain := "leanprover/lean4:v4.29.0; mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95"
  modules := [
    "FourierAnalysis.LittlewoodPaley.Dyadic",
    "FourierAnalysis.LittlewoodPaley.Bernstein",
    "FourierAnalysis.Paraproduct.Defs",
    "FourierAnalysis.KatoPonce.SobolevEmbedding",
    "FourierAnalysis.KatoPonce.Product",
    "FourierAnalysis.KatoPonce.Commutator"
  ]
  declarationNames := [
    "hsSeminormSq",
    "lpProjector",
    "lpPartialSum",
    "bony_partial",
    "norm_lpPartialSum_le",
    "norm_lpProjector_le",
    "norm_le_tsum_mFourierCoeff",
    "norm_partialCommutator_le_hs_uniform",
    "norm_partialCommutator_le_hs_fully_uniform"
  ]
  placeholderStatus :=
    "external archive scan found no Lean proof-placeholder tokens; not pinned/imported/checked in this repository"
  relevanceToKPV :=
    "Concrete Fourier-side homogeneous Sobolev and Kato-Ponce style infrastructure on T^2; not real-line H^s(R), not Bourgain X^{s,b}, and not the KdV/KPV theorem."
  machineStatus := APIAuditMachineStatus.externalAnchorOnlyNotPinned

/--
External Lean 4 candidate with concrete `H1`/`H2` Sobolev infrastructure.

This records a useful Sobolev-space API candidate, but it targets
Rellich-Kondrachov compactness rather than dispersive KdV well-posedness.
-/
def rellichKondrachovSobolevAPIAuditEntry : LeanAPIAuditEntry where
  repositoryURL := "https://github.com/abenenson/rellich-kondrachov"
  commitSHA := "85f2c2e943404e5ba92911346874d8961e137b60"
  toolchain := "leanprover/lean4:v4.29.0-rc7; mathlib c5edb8d3738a5abd7da7f34d5bcb27f632a1ecca"
  modules := [
    "RellichKondrachov.Analysis.FunctionalSpaces.Sobolev.Euclidean.H1",
    "RellichKondrachov.Analysis.FunctionalSpaces.Sobolev.Euclidean.H2",
    "RellichKondrachov.Analysis.FunctionalSpaces.Sobolev.Euclidean.TranslationEstimateH1",
    "RellichKondrachov.Geometry.Manifold.Sobolev.H1",
    "RellichKondrachov.Geometry.Manifold.Sobolev.EmbeddingL2",
    "RellichKondrachov.Geometry.Manifold.Sobolev.RellichKondrachov",
    "RellichKondrachov.Geometry.Manifold.Sobolev.RellichKondrachovRiemannian.Global"
  ]
  declarationNames := [
    "C1c",
    "C2c",
    "h1",
    "h2",
    "isClosed_h1",
    "isClosed_h2",
    "h1ToL2",
    "h2ToL2",
    "norm_translateL2_sub_h1ToL2_le",
    "isCompactOperator_h1ToL2_of_summands",
    "isCompactOperator_h1ToL2_riemannianVolume"
  ]
  placeholderStatus :=
    "external archive scan found no Lean proof-placeholder tokens; not pinned/imported/checked in this repository"
  relevanceToKPV :=
    "Concrete H1/H2 Sobolev and compact-embedding infrastructure over Euclidean/manifold settings; not the inhomogeneous real-line H^s(R) scale for arbitrary real s, not Bourgain X^{s,b}, and not KdV/KPV."
  machineStatus := APIAuditMachineStatus.externalAnchorOnlyNotPinned

/--
External Lean 4 project whose name contains Bourgain but not the PDE
restriction-space API needed for KPV.
-/
def leanBourgainNameCollisionAuditEntry : LeanAPIAuditEntry where
  repositoryURL := "https://github.com/Command-Master/lean-bourgain"
  commitSHA := "07fe8b2feac3e72d4f0bd1c8d094e1ebd0a02ffb"
  toolchain := "leanprover/lean4:v4.7.0; mathlib 154a87cdc796f476922d458f987f6f4d1709ed8c"
  modules := [
    "Pseudorandom.Bourgain",
    "Pseudorandom.LpLemmas",
    "Pseudorandom.XorLemma",
    "Pseudorandom.Incidence.Incidence"
  ]
  declarationNames := [
    "bourgain_extractor_final",
    "bourgain_extractor",
    "line_point_large_l2",
    "l1Norm_le_sqrt_card_mul_l2Norm",
    "lpNorm_eq_card_rpow_mul_nlpNorm"
  ]
  placeholderStatus :=
    "external archive scan found no Lean proof-placeholder tokens; not pinned/imported/checked in this repository"
  relevanceToKPV :=
    "Finite-field pseudorandom extractor project; Bourgain name collision only, with no Sobolev/Bourgain X^{s,b}, KdV, or KPV API."
  machineStatus := APIAuditMachineStatus.irrelevantNameCollision

/-- C003 audit rows for concrete Sobolev/Bourgain-space API reconnaissance. -/
def concreteSobolevBourgainAPIAuditEntries : List LeanAPIAuditEntry := [
  mathlibSobolevBourgainAPIAuditEntry,
  sqgFourierSobolevAPIAuditEntry,
  rellichKondrachovSobolevAPIAuditEntry,
  leanBourgainNameCollisionAuditEntry
]

/-- C003 terminal API diagnosis: no repo-local KPV-ready Sobolev/Bourgain API was found. -/
def concreteSobolevBourgainAPIAuditConclusion : String :=
  "No repo-local or pinned external Lean 4 API currently supplies the full KPV target stack: inhomogeneous H^s(R), Bourgain X^{s,b} for the Airy/KdV phase, KdV linear propagator, KPV bilinear estimate, and local well-posedness theorem."

/-- The C003 audit records exactly the four rows above. -/
theorem concreteSobolevBourgainAPIAuditEntries_length :
    concreteSobolevBourgainAPIAuditEntries.length = 4 :=
  rfl

/-- The C003 audit keeps external candidates out of the repo-local completion bucket. -/
theorem sqgFourierSobolevAPIAuditEntry_not_repoLocalPinned :
    sqgFourierSobolevAPIAuditEntry.machineStatus ≠
      APIAuditMachineStatus.repoLocalPinnedChecked := by
  decide

/-- The Rellich-Kondrachov Sobolev candidate is not repo-local pinned here. -/
theorem rellichKondrachovSobolevAPIAuditEntry_not_repoLocalPinned :
    rellichKondrachovSobolevAPIAuditEntry.machineStatus ≠
      APIAuditMachineStatus.repoLocalPinnedChecked := by
  decide

/-- The Bourgain extractor name collision is not a KPV Bourgain-space API. -/
theorem leanBourgainNameCollisionAuditEntry_status :
    leanBourgainNameCollisionAuditEntry.machineStatus =
      APIAuditMachineStatus.irrelevantNameCollision :=
  rfl

/--
Fourier-side profiles for the local Airy/KdV linear propagator API.

This is deliberately the transform-side scalar profile `ξ ↦ û(ξ)`.  It is not
a physical-space Sobolev or Bourgain-space object.
-/
abbrev AiryKdVFourierProfile : Type :=
  ℝ → ℂ

/--
The mathlib Fourier-convention symbol of the third spatial derivative.

With mathlib's `2 * π * I` derivative convention, the linear KdV/Airy equation
`u_t + u_xxx = 0` has transform-side generator
`(2π i ξ)^3`.
-/
def mathlibAiryKdVGeneratorSymbol (ξ : ℝ) : ℂ :=
  (2 * (Real.pi : ℂ) * Complex.I * (ξ : ℂ)) ^ 3

/--
Fourier multiplier for the Airy/KdV linear propagator under the selected
equation convention `u_t + u_xxx = 0`.
-/
def airyKdVLinearMultiplier (t ξ : ℝ) : ℂ :=
  Complex.exp (-(t : ℂ) * mathlibAiryKdVGeneratorSymbol ξ)

/--
Concrete Fourier-side Airy/KdV linear propagator.

The action is multiplication of the Fourier profile by the checked multiplier
`exp (-t * (2π i ξ)^3)`.
-/
def airyKdVLinearPropagatorFourier
    (t : ℝ) (uHat : AiryKdVFourierProfile) : AiryKdVFourierProfile :=
  fun ξ => airyKdVLinearMultiplier t ξ * uHat ξ

/--
C004 closure status for the Airy/KdV linear propagator leaf.

Only the local Fourier-side multiplier API is checked here.  The inverse
Fourier bridge, Sobolev/Bourgain mapping properties, and KPV estimates remain
separate formalization debt.
-/
inductive AiryKdVPropagatorClosureStatus : Type
  | localFourierSideMultiplierChecked
  | physicalSpaceBridgeMissing
  | estimateLayerMissing
deriving DecidableEq, Repr

/-- Current C004 status: a checked local Fourier-side multiplier API only. -/
def airyKdVPropagatorClosureStatus : AiryKdVPropagatorClosureStatus :=
  AiryKdVPropagatorClosureStatus.localFourierSideMultiplierChecked

/-- C004 diagnosis for the checked Airy/KdV propagator API. -/
def airyKdVLinearPropagatorAPIConclusion : String :=
  "Repo-local Lean now has a checked Fourier-side Airy/KdV multiplier API for u_t + u_xxx = 0, but no physical-space Sobolev/Bourgain propagator, no mapping estimates, and no KPV well-posedness closure."

/-- The selected Airy/KdV generator symbol is the cube of the mathlib derivative multiplier. -/
theorem mathlibAiryKdVGeneratorSymbol_eq (ξ : ℝ) :
    mathlibAiryKdVGeneratorSymbol ξ =
      (2 * (Real.pi : ℂ) * Complex.I * (ξ : ℂ)) ^ 3 :=
  rfl

/-- The Airy/KdV multiplier is definitionally the exponential multiplier above. -/
theorem airyKdVLinearMultiplier_eq (t ξ : ℝ) :
    airyKdVLinearMultiplier t ξ =
      Complex.exp (-(t : ℂ) * mathlibAiryKdVGeneratorSymbol ξ) :=
  rfl

/--
Checked Fourier-multiplier representation of the local Airy/KdV propagator.

This is the C004 checked API leaf: the transform-side propagator is exactly
pointwise multiplication by `exp (-t * (2π i ξ)^3)`.
-/
theorem airyKdVLinearPropagatorFourier_representation
    (t : ℝ) (uHat : AiryKdVFourierProfile) :
    airyKdVLinearPropagatorFourier t uHat =
      fun ξ => airyKdVLinearMultiplier t ξ * uHat ξ :=
  rfl

/-- Pointwise form of the checked Fourier-multiplier representation. -/
theorem airyKdVLinearPropagatorFourier_apply
    (t ξ : ℝ) (uHat : AiryKdVFourierProfile) :
    airyKdVLinearPropagatorFourier t uHat ξ =
      airyKdVLinearMultiplier t ξ * uHat ξ :=
  rfl

/-- At time zero the Airy/KdV multiplier is `1`. -/
theorem airyKdVLinearMultiplier_zero (ξ : ℝ) :
    airyKdVLinearMultiplier 0 ξ = 1 := by
  simp [airyKdVLinearMultiplier]

/-- At time zero the Fourier-side Airy/KdV propagator is the identity. -/
theorem airyKdVLinearPropagatorFourier_zero
    (uHat : AiryKdVFourierProfile) :
    airyKdVLinearPropagatorFourier 0 uHat = uHat := by
  funext ξ
  simp [airyKdVLinearPropagatorFourier, airyKdVLinearMultiplier]

/-- The C004 status records only local Fourier-side multiplier closure. -/
theorem airyKdVPropagatorClosureStatus_eq :
    airyKdVPropagatorClosureStatus =
      AiryKdVPropagatorClosureStatus.localFourierSideMultiplierChecked :=
  rfl

/--
Linear estimate families needed after the C004 Airy/KdV multiplier API.

These are statement-level requirements for the selected Bourgain route, not
proved estimates.  A terminal KPV formalization must replace them with concrete
normed-space statements over `H^s(ℝ)` and Airy-adapted `X^{s,b}` spaces.
-/
inductive KPVLinearEstimateKind : Type
  | homogeneousBourgainEvolution
  | inhomogeneousDuhamelBourgain
  | timeLocalizedCutoff
  | airySmoothingOrMaximalControl
deriving DecidableEq, Repr

/-- Repo-local status for a required KPV linear estimate family. -/
inductive KPVLinearEstimateStatus : Type
  | missingConcreteBourgainAPI
  | missingConcreteSobolevTraceAPI
  | missingRepoLocalProof
  | externalTerminalProofNotFound
deriving DecidableEq, Repr

/--
One C005 requirement row for the linear dispersive/smoothing layer.

The row records what the selected KPV route needs before the proposition-valued
`KPVProblem.linearDispersiveEstimate` field can be replaced by checked theorem
hypotheses or local proof bodies.
-/
structure KPVLinearEstimateRequirement : Type where
  requirementID : String
  kind : KPVLinearEstimateKind
  humanStatement : String
  proofRouteUse : String
  repoLocalStatus : KPVLinearEstimateStatus
  blocker : String
deriving Repr

/-- Homogeneous Airy evolution estimate required by the selected Bourgain route. -/
def homogeneousBourgainEvolutionRequirement : KPVLinearEstimateRequirement where
  requirementID := "KPV-LIN-001"
  kind := KPVLinearEstimateKind.homogeneousBourgainEvolution
  humanStatement :=
    "Bound the time-localized Airy evolution of initial data in the Airy-adapted Bourgain X^{s,b} norm by the H^s(R) norm of the data."
  proofRouteUse :=
    "Seeds the contraction space from initial data via the C004 Fourier-side Airy multiplier."
  repoLocalStatus := KPVLinearEstimateStatus.missingConcreteBourgainAPI
  blocker :=
    "No repo-local concrete X^{s,b} space or H^s(R) trace norm exists to state this estimate as a Lean theorem."

/-- Inhomogeneous Duhamel estimate required by the selected Bourgain route. -/
def inhomogeneousDuhamelBourgainRequirement : KPVLinearEstimateRequirement where
  requirementID := "KPV-LIN-002"
  kind := KPVLinearEstimateKind.inhomogeneousDuhamelBourgain
  humanStatement :=
    "Bound the time-localized Airy Duhamel integral in X^{s,b} by the forcing term in the lower b-index Bourgain norm."
  proofRouteUse :=
    "Turns the nonlinear forcing estimate into a contraction estimate for the integral equation."
  repoLocalStatus := KPVLinearEstimateStatus.missingConcreteBourgainAPI
  blocker :=
    "The repository has no concrete Duhamel operator over the physical-space Airy propagator and no X^{s,b-1} API."

/-- Time-localization estimate required by the selected Bourgain route. -/
def timeLocalizedCutoffRequirement : KPVLinearEstimateRequirement where
  requirementID := "KPV-LIN-003"
  kind := KPVLinearEstimateKind.timeLocalizedCutoff
  humanStatement :=
    "Control multiplication by a smooth time cutoff between the Bourgain norms used for the local-in-time argument."
  proofRouteUse :=
    "Provides the small-time factor and localizes the fixed-point problem to [-T,T]."
  repoLocalStatus := KPVLinearEstimateStatus.missingRepoLocalProof
  blocker :=
    "Pinned mathlib has smooth functions and Fourier infrastructure, but no checked Airy X^{s,b} cutoff lemma in this repository."

/-- Smoothing or maximal-function control required by the selected KPV route. -/
def airySmoothingOrMaximalControlRequirement : KPVLinearEstimateRequirement where
  requirementID := "KPV-LIN-004"
  kind := KPVLinearEstimateKind.airySmoothingOrMaximalControl
  humanStatement :=
    "Provide the Airy/KdV linear smoothing or maximal-function control used to connect the Bourgain contraction class with the Sobolev well-posedness conclusion."
  proofRouteUse :=
    "Supplies the linear regularity/control input needed before the nonlinear bilinear estimate can close the KPV theorem."
  repoLocalStatus := KPVLinearEstimateStatus.externalTerminalProofNotFound
  blocker :=
    "Local mathlib search and public GitHub repository queries found no importable Lean 4 Airy/KdV smoothing or dispersive estimate theorem."

/-- C005 requirement rows for the selected KPV linear estimate package. -/
def kpvLinearEstimateRequirements : List KPVLinearEstimateRequirement := [
  homogeneousBourgainEvolutionRequirement,
  inhomogeneousDuhamelBourgainRequirement,
  timeLocalizedCutoffRequirement,
  airySmoothingOrMaximalControlRequirement
]

/-- C005 integration gate for the required linear dispersive/smoothing estimates. -/
structure KPVLinearEstimateIntegrationGate : Type where
  childID : String
  c004FourierMultiplierAvailable : Bool
  concreteBourgainAPIAvailable : Bool
  concreteSobolevTraceAPIAvailable : Bool
  repoLocalLinearEstimatesChecked : Bool
  externalTerminalEstimateProofPinned : Bool
  mayReplaceKPVProblemLinearField : Bool
deriving Repr

/--
Current C005 gate.

The C004 multiplier is available, but the concrete normed-space APIs and
linear-estimate proofs are not.  Therefore `KPVProblem.linearDispersiveEstimate`
must remain an explicit hypothesis and the parent theorem remains open.
-/
def kpvLinearEstimateIntegrationGate : KPVLinearEstimateIntegrationGate where
  childID := "S1-M-154-C005"
  c004FourierMultiplierAvailable := true
  concreteBourgainAPIAvailable := false
  concreteSobolevTraceAPIAvailable := false
  repoLocalLinearEstimatesChecked := false
  externalTerminalEstimateProofPinned := false
  mayReplaceKPVProblemLinearField := false

/-- C005 terminal diagnosis for the linear dispersive/smoothing estimate layer. -/
def kpvLinearEstimateAuditConclusion : String :=
  "C005 records the selected KPV linear-estimate package but does not close it: the C004 Fourier-side Airy multiplier is checked, while concrete H^s(R), X^{s,b}, Duhamel, cutoff, and smoothing/maximal estimate theorems are not present in the repo-local Lean closure."

/-- The C005 audit records exactly four linear estimate requirements. -/
theorem kpvLinearEstimateRequirements_length :
    kpvLinearEstimateRequirements.length = 4 :=
  rfl

/-- The C005 gate records the already checked C004 Fourier-side multiplier as available. -/
theorem kpvLinearEstimateGate_c004_available :
    kpvLinearEstimateIntegrationGate.c004FourierMultiplierAvailable = true :=
  rfl

/-- The C005 gate blocks replacement of the abstract linear estimate field. -/
theorem kpvLinearEstimateGate_blocks_replacement :
    kpvLinearEstimateIntegrationGate.mayReplaceKPVProblemLinearField = false :=
  rfl

/-- The C005 gate has no pinned external terminal estimate proof. -/
theorem kpvLinearEstimateGate_no_external_pin :
    kpvLinearEstimateIntegrationGate.externalTerminalEstimateProofPinned = false :=
  rfl

/--
Nonlinear estimate families needed for the selected low-regularity KPV route.

These are statement-level requirements for the KPV bilinear estimate layer, not
proved estimates.  A terminal formalization must state them over concrete
Airy-adapted `X^{s,b}` and Sobolev trace spaces.
-/
inductive KPVNonlinearEstimateKind : Type
  | coreBilinearDerivativeEstimate
  | timeLocalizedNonlinearForcing
  | contractionDifferenceEstimate
  | lowRegularityThresholdCompatibility
deriving DecidableEq, Repr

/-- Repo-local status for a required KPV nonlinear estimate family. -/
inductive KPVNonlinearEstimateStatus : Type
  | missingConcreteBourgainAPI
  | missingSpatialDerivativeOperator
  | missingRepoLocalProof
  | externalTerminalProofNotFound
deriving DecidableEq, Repr

/--
One C006 requirement row for the bilinear/multilinear nonlinear estimate layer.

The rows record what is still needed before `KPVProblem.nonlinearEstimate` can
be replaced by concrete checked theorem hypotheses or local proof bodies.
-/
structure KPVNonlinearEstimateRequirement : Type where
  requirementID : String
  kind : KPVNonlinearEstimateKind
  humanStatement : String
  proofRouteUse : String
  repoLocalStatus : KPVNonlinearEstimateStatus
  blocker : String
deriving Repr

/-- Human-readable shape of the core KPV bilinear derivative estimate. -/
def selectedKPVBilinearEstimateDescription : String :=
  "For s > -3/4, prove a Bourgain-space bilinear estimate of the form ||partial_x (u * v)||_{X^{s,b-1}} <= C ||u||_{X^{s,b}} ||v||_{X^{s,b}} for the Airy/KdV phase, with the exact b-exponents fixed by the final KPV route."

/-- The selected bilinear-estimate threshold is the same `s > -3/4` threshold. -/
def selectedKPVBilinearEstimateThreshold : ℝ :=
  selectedRegularityThreshold

/-- Core bilinear derivative estimate required at the selected KPV threshold. -/
def coreBilinearDerivativeRequirement : KPVNonlinearEstimateRequirement where
  requirementID := "KPV-NL-001"
  kind := KPVNonlinearEstimateKind.coreBilinearDerivativeEstimate
  humanStatement := selectedKPVBilinearEstimateDescription
  proofRouteUse :=
    "Controls the KdV nonlinearity u * u_x, equivalently partial_x (u^2), inside the Bourgain contraction argument at s > -3/4."
  repoLocalStatus := KPVNonlinearEstimateStatus.missingConcreteBourgainAPI
  blocker :=
    "No repo-local concrete Airy X^{s,b} norm, spatial derivative operator between Bourgain spaces, or bilinear KPV theorem exists."

/-- Time-localized nonlinear forcing estimate needed for the local problem. -/
def timeLocalizedNonlinearForcingRequirement : KPVNonlinearEstimateRequirement where
  requirementID := "KPV-NL-002"
  kind := KPVNonlinearEstimateKind.timeLocalizedNonlinearForcing
  humanStatement :=
    "Combine the bilinear derivative estimate with the local time cutoff so that the nonlinear forcing term lies in the Duhamel input Bourgain space."
  proofRouteUse :=
    "Turns the global bilinear estimate into the local-in-time nonlinear bound used by the integral equation on [-T,T]."
  repoLocalStatus := KPVNonlinearEstimateStatus.missingRepoLocalProof
  blocker :=
    "C005 leaves the time-cutoff and Duhamel Bourgain estimates open, so the localized nonlinear forcing theorem cannot yet be stated concretely."

/-- Difference estimate needed for contraction and uniqueness. -/
def contractionDifferenceRequirement : KPVNonlinearEstimateRequirement where
  requirementID := "KPV-NL-003"
  kind := KPVNonlinearEstimateKind.contractionDifferenceEstimate
  humanStatement :=
    "Prove the Lipschitz bilinear difference bound for partial_x (u^2 - v^2) in the lower Bourgain norm."
  proofRouteUse :=
    "Provides the contraction and uniqueness estimate after the nonlinear map is localized in time."
  repoLocalStatus := KPVNonlinearEstimateStatus.missingRepoLocalProof
  blocker :=
    "The algebraic polarization step is elementary, but the normed-space bilinear estimate and Bourgain APIs are absent from the repo-local closure."

/-- Threshold-compatibility requirement for the low-regularity branch. -/
def lowRegularityThresholdCompatibilityRequirement : KPVNonlinearEstimateRequirement where
  requirementID := "KPV-NL-004"
  kind := KPVNonlinearEstimateKind.lowRegularityThresholdCompatibility
  humanStatement :=
    "Record and check that the nonlinear estimate package is stated only for the selected KPV range s > -3/4, with endpoint behavior left outside this Stage1 claim."
  proofRouteUse :=
    "Prevents silently upgrading the statement to the endpoint s = -3/4 or to regularities below the selected KPV theorem variant."
  repoLocalStatus := KPVNonlinearEstimateStatus.externalTerminalProofNotFound
  blocker :=
    "No pinned external Lean 4 theorem was found for the KPV bilinear estimate at the selected threshold, endpoint, or below-threshold variants."

/-- C006 requirement rows for the selected KPV nonlinear estimate package. -/
def kpvNonlinearEstimateRequirements : List KPVNonlinearEstimateRequirement := [
  coreBilinearDerivativeRequirement,
  timeLocalizedNonlinearForcingRequirement,
  contractionDifferenceRequirement,
  lowRegularityThresholdCompatibilityRequirement
]

/-- C006 integration gate for the bilinear/multilinear nonlinear estimates. -/
structure KPVNonlinearEstimateIntegrationGate : Type where
  childID : String
  selectedThresholdPinned : Bool
  c004FourierMultiplierAvailable : Bool
  linearEstimateGateClosed : Bool
  concreteBourgainAPIAvailable : Bool
  repoLocalBilinearEstimateChecked : Bool
  externalTerminalBilinearProofPinned : Bool
  mayReplaceKPVProblemNonlinearField : Bool
deriving Repr

/--
Current C006 gate.

The low-regularity threshold and C004 multiplier are recorded, but the concrete
Bourgain API, linear estimate package, and bilinear proof are missing.
Therefore `KPVProblem.nonlinearEstimate` must remain an explicit hypothesis.
-/
def kpvNonlinearEstimateIntegrationGate : KPVNonlinearEstimateIntegrationGate where
  childID := "S1-M-154-C006"
  selectedThresholdPinned := true
  c004FourierMultiplierAvailable := true
  linearEstimateGateClosed := false
  concreteBourgainAPIAvailable := false
  repoLocalBilinearEstimateChecked := false
  externalTerminalBilinearProofPinned := false
  mayReplaceKPVProblemNonlinearField := false

/-- C006 terminal diagnosis for the bilinear/multilinear nonlinear estimate layer. -/
def kpvNonlinearEstimateAuditConclusion : String :=
  "C006 records the selected KPV nonlinear-estimate package but does not close it: the threshold s > -3/4 and the expected bilinear derivative estimate are pinned as statement requirements, while concrete Airy X^{s,b} spaces, localized nonlinear forcing bounds, contraction difference estimates, and any repo-local or pinned external bilinear proof are absent."

/-- The C006 audit records exactly four nonlinear estimate requirements. -/
theorem kpvNonlinearEstimateRequirements_length :
    kpvNonlinearEstimateRequirements.length = 4 :=
  rfl

/-- The selected C006 bilinear-estimate threshold is the frozen KPV threshold. -/
theorem selectedKPVBilinearEstimateThreshold_eq :
    selectedKPVBilinearEstimateThreshold = selectedRegularityThreshold :=
  rfl

/-- The C006 gate records the already checked C004 Fourier-side multiplier as available. -/
theorem kpvNonlinearEstimateGate_c004_available :
    kpvNonlinearEstimateIntegrationGate.c004FourierMultiplierAvailable = true :=
  rfl

/-- The C006 gate blocks replacement of the abstract nonlinear estimate field. -/
theorem kpvNonlinearEstimateGate_blocks_replacement :
    kpvNonlinearEstimateIntegrationGate.mayReplaceKPVProblemNonlinearField = false :=
  rfl

/-- The C006 gate has no pinned external terminal bilinear estimate proof. -/
theorem kpvNonlinearEstimateGate_no_external_pin :
    kpvNonlinearEstimateIntegrationGate.externalTerminalBilinearProofPinned = false :=
  rfl

/--
C007 status categories for replacing a proposition-valued `KPVProblem` field.

Only `localProofBodyChecked` and `importedTheoremChecked` can support a terminal
completion claim.  The current slot has one checked local replacement for the
frozen low-regularity regime and open formalization debt for the remaining hard
analysis fields.
-/
inductive KPVProblemFieldReplacementStatus : Type
  | localProofBodyChecked
  | importedTheoremChecked
  | blockedByMissingConcreteAPI
  | blockedByOpenEstimateGate
  | blockedByMissingClosureProof
  | externalTerminalProofNotFound
deriving DecidableEq, Repr

/-- Proposition-valued fields in `KPVProblem` audited by the C007 pass. -/
inductive KPVProblemFieldReplacementKind : Type
  | lowRegularityRegime
  | linearDispersiveEstimate
  | nonlinearEstimate
  | contractionOrCompactnessClosure
deriving DecidableEq, Repr

/-- One C007 row describing whether a `KPVProblem` proof field can be replaced. -/
structure KPVProblemFieldReplacementRequirement : Type where
  fieldName : String
  kind : KPVProblemFieldReplacementKind
  replacementTarget : String
  currentEvidence : String
  repoLocalStatus : KPVProblemFieldReplacementStatus
  blocker : String
deriving Repr

/-- C007 row for the low-regularity regime field. -/
def lowRegularityRegimeReplacementRequirement :
    KPVProblemFieldReplacementRequirement where
  fieldName := "KPVProblem.lowRegularityRegime"
  kind := KPVProblemFieldReplacementKind.lowRegularityRegime
  replacementTarget := "FrozenKPVVariant.regularityRange : SelectedRegularity s"
  currentEvidence :=
    "The frozen variant stores `regularityRange : SelectedRegularity s` and `problemLowRegularityRegime : problem.lowRegularityRegime = SelectedRegularity s`."
  repoLocalStatus := KPVProblemFieldReplacementStatus.localProofBodyChecked
  blocker :=
    "No blocker for the frozen-variant low-regularity branch; the generic `KPVProblem` field remains abstract for non-frozen problems."

/-- C007 row for the linear dispersive/smoothing estimate field. -/
def linearDispersiveEstimateReplacementRequirement :
    KPVProblemFieldReplacementRequirement where
  fieldName := "KPVProblem.linearDispersiveEstimate"
  kind := KPVProblemFieldReplacementKind.linearDispersiveEstimate
  replacementTarget :=
    "Concrete imported theorem hypotheses or local proof bodies for the C005 homogeneous Airy, Duhamel, cutoff, and smoothing/maximal estimates."
  currentEvidence :=
    "C005 records `kpvLinearEstimateRequirements` and the gate `kpvLinearEstimateGate_blocks_replacement`."
  repoLocalStatus := KPVProblemFieldReplacementStatus.blockedByOpenEstimateGate
  blocker :=
    "Concrete H^s(R), Airy X^{s,b}, Duhamel, cutoff, and smoothing/maximal theorem APIs are not present in the repo-local Lean closure."

/-- C007 row for the bilinear/multilinear nonlinear estimate field. -/
def nonlinearEstimateReplacementRequirement :
    KPVProblemFieldReplacementRequirement where
  fieldName := "KPVProblem.nonlinearEstimate"
  kind := KPVProblemFieldReplacementKind.nonlinearEstimate
  replacementTarget :=
    "Concrete imported theorem hypotheses or local proof bodies for the C006 KPV bilinear derivative, localized forcing, and contraction-difference estimates."
  currentEvidence :=
    "C006 records `kpvNonlinearEstimateRequirements` and the gate `kpvNonlinearEstimateGate_blocks_replacement`."
  repoLocalStatus := KPVProblemFieldReplacementStatus.blockedByOpenEstimateGate
  blocker :=
    "Concrete Airy X^{s,b} spaces, a spatial derivative operator between Bourgain norms, and a checked KPV bilinear theorem are absent."

/-- C007 row for the fixed-point/compactness closure field. -/
def contractionOrCompactnessClosureReplacementRequirement :
    KPVProblemFieldReplacementRequirement where
  fieldName := "KPVProblem.contractionOrCompactnessClosure"
  kind := KPVProblemFieldReplacementKind.contractionOrCompactnessClosure
  replacementTarget :=
    "A local proof body or imported theorem assembling the checked linear and nonlinear estimates into `LocalWellPosedData` by contraction or compactness."
  currentEvidence :=
    "Only the abstract `LocalWellPosedData` interface and small continuity wrapper lemmas are present."
  repoLocalStatus := KPVProblemFieldReplacementStatus.blockedByMissingClosureProof
  blocker :=
    "The closure proof cannot be stated concretely until the C005 linear and C006 nonlinear estimate gates close."

/-- C007 replacement rows for the proposition-valued `KPVProblem` proof fields. -/
def kpvProblemFieldReplacementRequirements :
    List KPVProblemFieldReplacementRequirement := [
  lowRegularityRegimeReplacementRequirement,
  linearDispersiveEstimateReplacementRequirement,
  nonlinearEstimateReplacementRequirement,
  contractionOrCompactnessClosureReplacementRequirement
]

/-- C007 integration gate for replacing all proposition-valued `KPVProblem` fields. -/
structure KPVProblemFieldReplacementGate : Type where
  childID : String
  frozenLowRegularityFieldReplaced : Bool
  linearFieldConcrete : Bool
  nonlinearFieldConcrete : Bool
  closureFieldConcrete : Bool
  externalTerminalKPVProofPinned : Bool
  mayReplaceAllKPVProblemPropFields : Bool
  mayClaimTerminalKPVCompletion : Bool
deriving Repr

/--
Current C007 gate.

The frozen low-regularity branch is locally tied to `SelectedRegularity s`.
The hard linear, nonlinear, and closure fields are not yet concrete imported
theorem hypotheses or local proof bodies, so the terminal KPV completion gate is
closed.
-/
def kpvProblemFieldReplacementGate : KPVProblemFieldReplacementGate where
  childID := "S1-M-154-C007"
  frozenLowRegularityFieldReplaced := true
  linearFieldConcrete := false
  nonlinearFieldConcrete := false
  closureFieldConcrete := false
  externalTerminalKPVProofPinned := false
  mayReplaceAllKPVProblemPropFields := false
  mayClaimTerminalKPVCompletion := false

/-- C007 terminal diagnosis for the proposition-valued field replacement task. -/
def kpvProblemFieldReplacementAuditConclusion : String :=
  "C007 replaces the frozen low-regularity hypothesis by checked local evidence through `FrozenKPVVariant.regularityRange` and `problemLowRegularityRegime`, but the linear, nonlinear, and closure fields remain formalization debt because no concrete Airy H^s(R)/X^{s,b} APIs, KPV estimates, fixed-point proof, or pinned external terminal theorem are available in the repo-local Lean closure."

/-- The C007 audit records exactly four proposition-valued field rows. -/
theorem kpvProblemFieldReplacementRequirements_length :
    kpvProblemFieldReplacementRequirements.length = 4 :=
  rfl

/-- The C007 gate records the frozen low-regularity field as locally replaced. -/
theorem kpvProblemFieldReplacementGate_lowRegularity_replaced :
    kpvProblemFieldReplacementGate.frozenLowRegularityFieldReplaced = true :=
  rfl

/-- The C007 gate blocks replacing every proposition-valued field at once. -/
theorem kpvProblemFieldReplacementGate_blocks_all_replacement :
    kpvProblemFieldReplacementGate.mayReplaceAllKPVProblemPropFields = false :=
  rfl

/-- The C007 gate blocks a terminal KPV completion claim. -/
theorem kpvProblemFieldReplacementGate_blocks_completion :
    kpvProblemFieldReplacementGate.mayClaimTerminalKPVCompletion = false :=
  rfl

/-- The C007 gate has no pinned external terminal KPV proof. -/
theorem kpvProblemFieldReplacementGate_no_external_terminal_pin :
    kpvProblemFieldReplacementGate.externalTerminalKPVProofPinned = false :=
  rfl

/--
C008 repo-local completion gate for the public Stage1 checklist item.

The public item may close only after this local artifact validates a concrete
wrapper/proof and the completed state has no repo-local integration debt.
-/
structure KPVRepoLocalCompletionGate : Type where
  childID : String
  leanArtifactHasBeenValidated : Bool
  concreteWrapperOrProofValidated : Bool
  externalTerminalKPVProofFound : Bool
  externalTerminalKPVProofPinnedOrBlocked : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  publicStage1ItemMayClose : Bool
deriving Repr

/--
Current C008 gate.

This file validates statement-shape wrappers and audit data, but not a concrete
KPV proof or imported terminal wrapper.  No external terminal Lean 4 proof has
been found, so there is no anchor-only proof being counted as completed-state
evidence.  The public Stage1 item must remain open.
-/
def kpvRepoLocalCompletionGate : KPVRepoLocalCompletionGate where
  childID := "S1-M-154-C008"
  leanArtifactHasBeenValidated := true
  concreteWrapperOrProofValidated := false
  externalTerminalKPVProofFound := false
  externalTerminalKPVProofPinnedOrBlocked := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  publicStage1ItemMayClose := false

/-- C008 terminal diagnosis for the repo-local completion gate. -/
def kpvRepoLocalCompletionAuditConclusion : String :=
  "C008 keeps the public Stage1 item open: the repo-local Lean artifact validates audit scaffolding, but no concrete KPV wrapper/proof or pinned external terminal theorem is present, and no completed-state repo_local_integration_debt is being retained."

/-- The C008 gate records that this child is the repo-local completion gate. -/
theorem kpvRepoLocalCompletionGate_child :
    kpvRepoLocalCompletionGate.childID = "S1-M-154-C008" :=
  rfl

/-- The C008 gate does not validate a concrete terminal KPV wrapper/proof. -/
theorem kpvRepoLocalCompletionGate_no_concrete_wrapper :
    kpvRepoLocalCompletionGate.concreteWrapperOrProofValidated = false :=
  rfl

/-- The C008 gate records no anchor-only terminal KPV proof as completed debt. -/
theorem kpvRepoLocalCompletionGate_no_completed_integration_debt :
    kpvRepoLocalCompletionGate.repoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-- The public Stage1 item must remain open under the current C008 gate. -/
theorem kpvRepoLocalCompletionGate_keeps_public_item_open :
    kpvRepoLocalCompletionGate.publicStage1ItemMayClose = false :=
  rfl

/-- The C002 target decision selects the Bourgain route. -/
theorem selectedFormalTargetRoute_eq :
    selectedFormalTargetRoute = FormalTargetRoute.bourgainXsbLocalWellPosedness :=
  rfl

/-- C002 did not select the Sobolev-only route. -/
theorem selectedFormalTargetRoute_ne_sobolevOnly :
    selectedFormalTargetRoute ≠ FormalTargetRoute.sobolevSpaceHadamardOnly := by
  decide

/-- C002 did not select an anchor-only or pinned-upstream wrapper route. -/
theorem selectedFormalTargetRoute_ne_pinnedUpstreamWrapper :
    selectedFormalTargetRoute ≠ FormalTargetRoute.pinnedUpstreamAbstractWrapper := by
  decide

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Phase : Type u) [TopologicalSpace Phase] (P : KPVProblem Phase),
      P.lowRegularityRegime →
        P.linearDispersiveEstimate →
          P.nonlinearEstimate →
            P.contractionOrCompactnessClosure →
              LocalWellPosedData P) :
    StatementShape.{u} :=
  h

/-- Low-risk introduction wrapper for the frozen public KPV variant. -/
theorem FrozenTheoremVariant.intro
    (h : ∀ (Phase : Type u) [TopologicalSpace Phase] (V : FrozenKPVVariant Phase),
      V.problem.linearDispersiveEstimate →
        V.problem.nonlinearEstimate →
          V.problem.contractionOrCompactnessClosure →
            LocalWellPosedData V.problem) :
    FrozenTheoremVariant.{u} :=
  h

/--
Specialize the generic statement shape to the frozen public KPV variant.

The low-regularity hypothesis required by `StatementShape` is discharged from
`FrozenKPVVariant.problem_lowRegularityRegime`, not from a fresh external
proposition-valued hypothesis.
-/
theorem FrozenTheoremVariant.of_statementShape (h : StatementShape.{u}) :
    FrozenTheoremVariant.{u} := by
  intro Phase _ V hLinear hNonlinear hClosure
  apply h Phase V.problem
  · rw [V.problemLowRegularityRegime]
    exact V.regularityRange
  · exact hLinear
  · exact hNonlinear
  · exact hClosure

/-- The frozen theorem variant unfolds to the frozen-variant statement boundary. -/
theorem frozenTheoremVariant_iff :
    FrozenTheoremVariant.{u} ↔ FrozenVariantStatement.{u} :=
  Iff.rfl

/-- The selected regularity condition is exactly `s > -3 / 4`. -/
theorem selectedRegularity_iff (s : ℝ) :
    SelectedRegularity s ↔ selectedRegularityThreshold < s :=
  Iff.rfl

/-- The center point belongs to every selected symmetric interval with nonnegative radius. -/
theorem zero_mem_selectedLocalTimeInterval {T : ℝ} (hT : 0 ≤ T) :
    0 ∈ selectedLocalTimeInterval T :=
  ⟨neg_nonpos.mpr hT, hT⟩

/-- Extract the frozen regularity range from a selected KPV variant. -/
theorem FrozenKPVVariant.selected_regularity
    {Phase : Type u} [TopologicalSpace Phase] (V : FrozenKPVVariant Phase) :
    SelectedRegularity V.s :=
  V.regularityRange

/-- Extract the abstract problem bound to a selected KPV variant. -/
theorem FrozenKPVVariant.problem_regularity
    {Phase : Type u} [TopologicalSpace Phase] (V : FrozenKPVVariant Phase) :
    V.problem.regularity = V.s :=
  V.problemRegularity

/-- The frozen low-regularity field is supplied by the concrete selected range. -/
theorem FrozenKPVVariant.problem_lowRegularityRegime
    {Phase : Type u} [TopologicalSpace Phase] (V : FrozenKPVVariant Phase) :
    V.problem.lowRegularityRegime := by
  rw [V.problemLowRegularityRegime]
  exact V.regularityRange

/-- Extract the frozen equation label from a selected KPV variant. -/
theorem FrozenKPVVariant.problem_equation
    {Phase : Type u} [TopologicalSpace Phase] (V : FrozenKPVVariant Phase) :
    V.problem.equationName = selectedEquationDescription :=
  V.problemEquation

/-- Extract the frozen local time interval from a selected KPV variant. -/
theorem FrozenKPVVariant.problem_timeDomain
    {Phase : Type u} [TopologicalSpace Phase] (V : FrozenKPVVariant Phase) :
    V.problem.timeDomain = selectedLocalTimeInterval V.T :=
  V.problemTimeDomain

/-- A global continuous flow map gives continuous dependence on the data set. -/
theorem flowMapContinuousOn_of_continuous {Phase : Type u} [TopologicalSpace Phase]
    (P : KPVProblem Phase) (h : Continuous (FlowMap P)) :
    FlowMapContinuousOn P :=
  h.continuousOn

/-- Continuous dependence restricts to any smaller initial-data set. -/
theorem flowMapContinuousOn_mono {Phase : Type u} [TopologicalSpace Phase]
    (P : KPVProblem Phase) {s : Set Phase}
    (h : FlowMapContinuousOn P) (hs : s ⊆ P.dataSet) :
    ContinuousOn (FlowMap P) s :=
  h.mono hs

/-- Extract the continuous-dependence component from the local well-posedness package. -/
theorem LocalWellPosedData.continuous_dependence {Phase : Type u} [TopologicalSpace Phase]
    {P : KPVProblem Phase} (H : LocalWellPosedData P) :
    FlowMapContinuousOn P :=
  H.continuousDependence

/-- Extract existence of the selected solution path from the local well-posedness package. -/
theorem LocalWellPosedData.exists_solution {Phase : Type u} [TopologicalSpace Phase]
    {P : KPVProblem Phase} (H : LocalWellPosedData P)
    {u0 : Phase} (hu0 : u0 ∈ P.dataSet) :
    P.IsSolution u0 (FlowMap P u0) :=
  H.existence u0 hu0

/-- Extract uniqueness in the selected uniqueness class. -/
theorem LocalWellPosedData.unique_solution {Phase : Type u} [TopologicalSpace Phase]
    {P : KPVProblem Phase} (H : LocalWellPosedData P)
    {u0 : Phase} (hu0 : u0 ∈ P.dataSet) {v : ℝ → Phase}
    (hvClass : P.uniquenessClass v) (hvSol : P.IsSolution u0 v) :
    v = FlowMap P u0 :=
  H.uniqueness u0 hu0 v hvClass hvSol

/--
Checked mathlib anchor: the finite-dimensional Gagliardo-Nirenberg-Sobolev inequality
available in the pinned local mathlib snapshot.
-/
theorem sobolev_eLpNorm_fderiv_anchor
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
    (μ : Measure E) [μ.IsAddHaarMeasure] [FiniteDimensional ℝ F]
    {u : E → F} {s : Set E} (hu : ContDiff ℝ 1 u)
    (h2u : Function.support u ⊆ s) {p : ℝ≥0}
    (hp : 1 ≤ p) (h2p : p < Module.finrank ℝ E)
    (hs : Bornology.IsBounded s) :
    eLpNorm u (p : ℝ≥0∞) μ ≤
      (eLpNormLESNormFDerivOfLeConst F μ s p p : ℝ≥0∞) *
        eLpNorm (fderiv ℝ u) (p : ℝ≥0∞) μ :=
  MeasureTheory.eLpNorm_le_eLpNorm_fderiv μ hu h2u hp h2p hs

/--
Checked mathlib anchor: distributional directional derivative as a Fourier multiplier
on tempered distributions.
-/
theorem tempered_lineDeriv_fourierMultiplier_anchor
    {E F : Type*} [NormedAddCommGroup E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ E] [NormedSpace ℂ F] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (m : E) (f : TemperedDistribution E F) :
    LineDeriv.lineDerivOp m f =
      (2 * (Real.pi : ℂ) * Complex.I) •
        (TemperedDistribution.fourierMultiplierCLM F fun x => (inner ℝ x m : ℂ)) f :=
  TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM m f

/--
Checked mathlib anchor: the distributional Laplacian as a Fourier multiplier on
tempered distributions.
-/
theorem tempered_laplacian_fourierMultiplier_anchor
    {E F : Type*} [NormedAddCommGroup E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ E] [NormedSpace ℂ F] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (f : TemperedDistribution E F) :
    Laplacian.laplacian f =
      -((2 * Real.pi : ℝ) ^ 2) •
        (TemperedDistribution.fourierMultiplierCLM F fun x => ((‖x‖ ^ 2 : ℝ) : ℂ)) f :=
  TemperedDistribution.laplacian_eq_fourierMultiplierCLM f

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Fourier.FourierTransform",
  "Mathlib.Analysis.Fourier.Convolution",
  "Mathlib.Analysis.Fourier.LpSpace",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Fourier",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic"
]

/-- Checked declaration names used as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "Continuous",
  "ContinuousOn",
  "MeasureTheory.MemLp",
  "MeasureTheory.Lp",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "VectorFourier.fourierIntegral",
  "FourierTransform.fourier",
  "SchwartzMap",
  "TemperedDistribution",
  "TemperedDistribution.fourierMultiplierCLM",
  "TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM",
  "TemperedDistribution.laplacian_eq_fourierMultiplierCLM",
  "SchwartzMap.fourier_convolution"
]

/-- Search terms that did not locate a terminal KPV theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Kenig",
  "Ponce",
  "Vega",
  "Kenig-Ponce-Vega",
  "KdV",
  "Korteweg",
  "Korteweg-de Vries",
  "Bourgain space",
  "Xsb",
  "KPV bilinear estimate",
  "bilinear Bourgain estimate",
  "multilinear nonlinear estimate",
  "Airy smoothing estimate",
  "linear dispersive estimate",
  "Duhamel Bourgain estimate",
  "dispersive well-posedness",
  "low regularity"
]

/-! ## Audit probes -/

#check KPVProblem
#check FlowMap
#check FlowMapContinuousOn
#check LocalWellPosedData
#check StatementShape
#check FrozenKPVVariant
#check FrozenVariantStatement
#check FrozenTheoremVariant
#check FormalTargetRoute
#check selectedFormalTargetRoute
#check selectedFormalTargetRoute_eq
#check selectedFormalTargetRoute_ne_sobolevOnly
#check selectedFormalTargetRoute_ne_pinnedUpstreamWrapper
#check APIAuditMachineStatus
#check LeanAPIAuditEntry
#check concreteSobolevBourgainAPIAuditEntries
#check concreteSobolevBourgainAPIAuditEntries_length
#check sqgFourierSobolevAPIAuditEntry_not_repoLocalPinned
#check rellichKondrachovSobolevAPIAuditEntry_not_repoLocalPinned
#check leanBourgainNameCollisionAuditEntry_status
#check AiryKdVFourierProfile
#check mathlibAiryKdVGeneratorSymbol
#check airyKdVLinearMultiplier
#check airyKdVLinearPropagatorFourier
#check AiryKdVPropagatorClosureStatus
#check airyKdVLinearPropagatorAPIConclusion
#check mathlibAiryKdVGeneratorSymbol_eq
#check airyKdVLinearMultiplier_eq
#check airyKdVLinearPropagatorFourier_representation
#check airyKdVLinearPropagatorFourier_apply
#check airyKdVLinearMultiplier_zero
#check airyKdVLinearPropagatorFourier_zero
#check airyKdVPropagatorClosureStatus_eq
#check KPVLinearEstimateKind
#check KPVLinearEstimateStatus
#check KPVLinearEstimateRequirement
#check kpvLinearEstimateRequirements
#check KPVLinearEstimateIntegrationGate
#check kpvLinearEstimateIntegrationGate
#check kpvLinearEstimateAuditConclusion
#check kpvLinearEstimateRequirements_length
#check kpvLinearEstimateGate_c004_available
#check kpvLinearEstimateGate_blocks_replacement
#check kpvLinearEstimateGate_no_external_pin
#check KPVNonlinearEstimateKind
#check KPVNonlinearEstimateStatus
#check KPVNonlinearEstimateRequirement
#check selectedKPVBilinearEstimateDescription
#check selectedKPVBilinearEstimateThreshold
#check kpvNonlinearEstimateRequirements
#check KPVNonlinearEstimateIntegrationGate
#check kpvNonlinearEstimateIntegrationGate
#check kpvNonlinearEstimateAuditConclusion
#check kpvNonlinearEstimateRequirements_length
#check selectedKPVBilinearEstimateThreshold_eq
#check kpvNonlinearEstimateGate_c004_available
#check kpvNonlinearEstimateGate_blocks_replacement
#check kpvNonlinearEstimateGate_no_external_pin
#check KPVProblemFieldReplacementStatus
#check KPVProblemFieldReplacementKind
#check KPVProblemFieldReplacementRequirement
#check kpvProblemFieldReplacementRequirements
#check KPVProblemFieldReplacementGate
#check kpvProblemFieldReplacementGate
#check kpvProblemFieldReplacementAuditConclusion
#check kpvProblemFieldReplacementRequirements_length
#check kpvProblemFieldReplacementGate_lowRegularity_replaced
#check kpvProblemFieldReplacementGate_blocks_all_replacement
#check kpvProblemFieldReplacementGate_blocks_completion
#check kpvProblemFieldReplacementGate_no_external_terminal_pin
#check KPVRepoLocalCompletionGate
#check kpvRepoLocalCompletionGate
#check kpvRepoLocalCompletionAuditConclusion
#check kpvRepoLocalCompletionGate_child
#check kpvRepoLocalCompletionGate_no_concrete_wrapper
#check kpvRepoLocalCompletionGate_no_completed_integration_debt
#check kpvRepoLocalCompletionGate_keeps_public_item_open
#check FrozenTheoremVariant.of_statementShape
#check flowMapContinuousOn_of_continuous
#check flowMapContinuousOn_mono
#check selectedRegularity_iff
#check zero_mem_selectedLocalTimeInterval
#check FrozenKPVVariant.problem_lowRegularityRegime
#check frozenTheoremVariant_iff
#check sobolev_eLpNorm_fderiv_anchor
#check tempered_lineDeriv_fourierMultiplier_anchor
#check tempered_laplacian_fourierMultiplier_anchor

end S1_M_154
end Stage1
end AwesomeTheorems
