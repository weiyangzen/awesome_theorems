import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Distribution.FourierMultiplier
import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# S1-M-207 / THM-M-1548: Korteweg-de Vries equation

This Stage1 artifact records a conservative Lean 4 boundary for the
Korteweg-de Vries equation, normalized as the one-dimensional nonlinear
dispersive PDE

`u_t + 6 * u * u_x + u_xxx = 0`.

The pinned mathlib snapshot has classical derivatives, `ContDiff`, Lp-space
predicates, Schwartz-space derivative operators, tempered distributions, and
Fourier-multiplier anchors.  This file does not claim a terminal theorem for
KdV well-posedness, soliton construction, inverse scattering, Lax pairs, or
conservation-law closure.
-/

noncomputable section

open scoped ENNReal NNReal SchwartzMap Topology

open MeasureTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_207

/-- Space-time for the classical one-dimensional KdV equation. -/
abbrev SpaceTime : Type :=
  ℝ × ℝ

/-- A scalar KdV field `u(t, x)`. -/
abbrev ScalarField : Type :=
  SpaceTime → ℝ

/-- The selected classical KdV domain: all real time-space. -/
def classicalKdVDomain : Set SpaceTime :=
  Set.univ

/-- A fixed-time spatial slice of a scalar KdV field. -/
def timeSlice (u : ScalarField) (t : ℝ) : ℝ → ℝ :=
  fun x => u (t, x)

/-- Formal time derivative `u_t`. -/
def temporalDerivative (u : ScalarField) : ScalarField :=
  fun z => deriv (fun t : ℝ => u (t, z.2)) z.1

/-- Formal space derivative `u_x`. -/
def spatialDerivative (u : ScalarField) : ScalarField :=
  fun z => deriv (fun x : ℝ => u (z.1, x)) z.2

/-- Formal second space derivative `u_xx`. -/
def secondSpatialDerivative (u : ScalarField) : ScalarField :=
  spatialDerivative (spatialDerivative u)

/-- Formal third space derivative `u_xxx`. -/
def thirdSpatialDerivative (u : ScalarField) : ScalarField :=
  spatialDerivative (secondSpatialDerivative u)

/--
Formal KdV residual with nonlinear coefficient `c`.

The standard KdV normalization is `c = 6`; keeping the coefficient explicit
also records the statement-shape boundary for later rescaled variants.
-/
def kdvResidual (c : ℝ) (u : ScalarField) : ScalarField :=
  fun z => temporalDerivative u z + c * u z * spatialDerivative u z +
    thirdSpatialDerivative u z

/-- The KdV residual unfolds to `u_t + c * u * u_x + u_xxx`. -/
theorem kdvResidual_apply (c : ℝ) (u : ScalarField) (z : SpaceTime) :
    kdvResidual c u z =
      temporalDerivative u z + c * u z * spatialDerivative u z +
        thirdSpatialDerivative u z :=
  rfl

/-- The standard KdV equation in the normalization `u_t + 6*u*u_x + u_xxx = 0`. -/
def SolvesClassicalKdV (u : ScalarField) (domain : Set SpaceTime) : Prop :=
  ∀ z ∈ domain, kdvResidual 6 u z = 0

/-- The classical solution class used by this Stage1 statement boundary. -/
def ClassicalKdVSolutionClass (u : ScalarField) (domain : Set SpaceTime) : Prop :=
  ContDiffOn ℝ 3 u domain

/-- The pointwise residual interpretation used by this Stage1 statement boundary. -/
def KdVResidualInterpretation (u : ScalarField) (domain : Set SpaceTime) : Prop :=
  SolvesClassicalKdV u domain

/-- Initial trace of a KdV field at time `0`. -/
def KdVInitialTrace (u : ScalarField) (u₀ : ℝ → ℝ) : Prop :=
  timeSlice u 0 = u₀

/-- Signed mass functional for a spatial KdV profile. -/
def kdvMass (v : ℝ → ℝ) : ℝ :=
  ∫ x, v x

/-- Quadratic momentum functional for a spatial KdV profile. -/
def kdvMomentum (v : ℝ → ℝ) : ℝ :=
  ∫ x, (v x) ^ 2

/-- Classical KdV Hamiltonian density in the `u_t + 6*u*u_x + u_xxx = 0` normalization. -/
def kdvEnergyDensity (v : ℝ → ℝ) (x : ℝ) : ℝ :=
  (deriv v x) ^ 2 - 2 * (v x) ^ 3

/-- Classical KdV energy functional for a spatial profile. -/
def kdvEnergy (v : ℝ → ℝ) : ℝ :=
  ∫ x, kdvEnergyDensity v x

/-- Conservation of the signed mass functional along the time evolution. -/
def KdVMassConservationTarget (u : ScalarField) (_domain : Set SpaceTime) : Prop :=
  ∀ t : ℝ, kdvMass (timeSlice u t) = kdvMass (timeSlice u 0)

/-- Conservation of the quadratic momentum functional along the time evolution. -/
def KdVMomentumConservationTarget (u : ScalarField) (_domain : Set SpaceTime) : Prop :=
  ∀ t : ℝ, kdvMomentum (timeSlice u t) = kdvMomentum (timeSlice u 0)

/-- Conservation of the classical KdV energy functional along the time evolution. -/
def KdVEnergyConservationTarget (u : ScalarField) (_domain : Set SpaceTime) : Prop :=
  ∀ t : ℝ, kdvEnergy (timeSlice u t) = kdvEnergy (timeSlice u 0)

/-- Concrete conservation-law target package for this Stage1 KdV boundary. -/
structure KdVConservationTarget (u : ScalarField) (domain : Set SpaceTime) : Prop where
  mass : KdVMassConservationTarget u domain
  momentum : KdVMomentumConservationTarget u domain
  energy : KdVEnergyConservationTarget u domain

/-- Uniqueness target among classical solutions with the same trace and conservation package. -/
def KdVUniquenessTarget
    (u₀ : ℝ → ℝ) (u : ScalarField) (domain : Set SpaceTime) : Prop :=
  ∀ v : ScalarField,
    ClassicalKdVSolutionClass v domain →
      KdVResidualInterpretation v domain →
        KdVInitialTrace v u₀ →
          KdVConservationTarget v domain →
            ∀ z ∈ domain, v z = u z

/-- The chosen domain is all real time-space. -/
theorem classicalKdVDomain_eq_univ :
    classicalKdVDomain = Set.univ :=
  rfl

/-- On the chosen domain, every space-time point is included. -/
theorem mem_classicalKdVDomain (z : SpaceTime) :
    z ∈ classicalKdVDomain := by
  simp [classicalKdVDomain]

/-- The initial-trace predicate unfolds to equality of the zero-time slice. -/
theorem kdvInitialTrace_apply {u : ScalarField} {u₀ : ℝ → ℝ}
    (h : KdVInitialTrace u u₀) (x : ℝ) :
    u (0, x) = u₀ x := by
  exact congrFun h x

/-- Public terminal-branch options for the broad KdV Stage1 slot. -/
inductive KdVTerminalBranch : Type where
  | oneSolitonVerification
  | restrictedClassicalConservationLaws
  | localOrGlobalWellPosedness
  | laxIsospectrality
  | inverseScatteringTheorem
  deriving DecidableEq

/--
Stage1 child decision for THM-M-1548.

The selected public branch is the restricted one-soliton verification target:
prove directly that the explicit `sech^2` travelling wave satisfies the
classical KdV residual.  This is intentionally narrower than well-posedness,
Lax isospectrality, or inverse scattering.
-/
def selectedTerminalBranch : KdVTerminalBranch :=
  KdVTerminalBranch.oneSolitonVerification

/-- The public branch decision is definitionally the one-soliton target. -/
theorem selectedTerminalBranch_eq :
    selectedTerminalBranch = KdVTerminalBranch.oneSolitonVerification :=
  rfl

/-- Hyperbolic secant, used to state the standard one-soliton profile. -/
def sech (y : ℝ) : ℝ :=
  (Real.cosh y)⁻¹

/-- Parameters for the positive-speed one-soliton family. -/
structure OneSolitonParameters : Type where
  speed : ℝ
  center : ℝ
  positiveSpeed : 0 < speed

/-- Travelling-wave phase `sqrt(c)/2 * (x - c*t - x₀)`. -/
def oneSolitonPhase (speed center : ℝ) (z : SpaceTime) : ℝ :=
  (Real.sqrt speed / 2) * (z.2 - speed * z.1 - center)

/-- Standard KdV one-soliton profile `(c/2) * sech^2(sqrt(c)/2 * (x - c*t - x₀))`. -/
def oneSolitonProfile (speed center : ℝ) : ScalarField :=
  fun z => (speed / 2) * (sech (oneSolitonPhase speed center z)) ^ 2

/--
Concrete terminal theorem target for the selected public branch.

This is a statement boundary only: the residual calculation remains a future
formalization leaf, and no theorem in this file proves the target.
-/
def OneSolitonVerificationTarget (p : OneSolitonParameters) : Prop :=
  SolvesClassicalKdV (oneSolitonProfile p.speed p.center) Set.univ

/-- The one-soliton branch target is exactly vanishing KdV residual everywhere. -/
theorem oneSolitonVerificationTarget_iff_residual
    (p : OneSolitonParameters) :
    OneSolitonVerificationTarget p ↔
      ∀ z : SpaceTime, kdvResidual 6 (oneSolitonProfile p.speed p.center) z = 0 := by
  unfold OneSolitonVerificationTarget SolvesClassicalKdV
  simp

/-- Concrete decaying-boundary reading for the classical real-line KdV statement. -/
def KdVSchwartzInitialBoundary (u₀ : ℝ → ℝ) : Prop :=
  ∃ f : 𝓢(ℝ, ℝ), (fun x : ℝ => f x) = u₀

/-- Concrete admissibility gate for the statement-boundary initial data. -/
def KdVAdmissibleForFlow (u₀ : ℝ → ℝ) : Prop :=
  ContDiff ℝ ⊤ u₀ ∧
    MeasureTheory.MemLp u₀ (2 : ℝ≥0∞) ∧
      KdVSchwartzInitialBoundary u₀

/-- Initial data package for a future full KdV theorem. -/
structure KdVInitialData (u₀ : ℝ → ℝ) : Type where
  initialRegularity : ContDiff ℝ ⊤ u₀
  initialMemLpTwo : MeasureTheory.MemLp u₀ (2 : ℝ≥0∞)
  decayOrPeriodicBoundary : KdVSchwartzInitialBoundary u₀
  admissibleForKdVFlow : KdVAdmissibleForFlow u₀

/--
Global classical KdV solution package.

The hard PDE components are explicit target predicates: all real time-space as
domain, `ContDiffOn ℝ 3` as the classical solution class, pointwise residual
zero, zero-time initial trace, the three standard conservation functionals, and
uniqueness within the same classical/conservation class.
-/
structure KdVGlobalSolution (u₀ : ℝ → ℝ) (I : KdVInitialData u₀) : Type where
  u : ScalarField
  solutionRegularity : ClassicalKdVSolutionClass u classicalKdVDomain
  solvesKdV : KdVResidualInterpretation u classicalKdVDomain
  initialTrace : KdVInitialTrace u u₀
  conservationTarget : KdVConservationTarget u classicalKdVDomain
  uniquenessInAdmissibleClass : KdVUniquenessTarget u₀ u classicalKdVDomain

/--
Normalized Stage1 statement shape for THM-M-1548.

For every admissible initial profile, the expected terminal theorem should
produce a nonnegative-time classical KdV solution satisfying the PDE, initial
trace, conservation laws, and uniqueness in the chosen admissible class.  This
is only a statement boundary until the analytic KdV proof packages are supplied
by local Lean code or a pinned external Lean 4 dependency.
-/
def StatementShape : Prop :=
  ∀ (u₀ : ℝ → ℝ) (I : KdVInitialData u₀),
    KdVSchwartzInitialBoundary u₀ →
      KdVAdmissibleForFlow u₀ →
        Nonempty (KdVGlobalSolution u₀ I)

/-- Low-risk introduction wrapper for the normalized KdV statement shape. -/
theorem StatementShape.intro
    (h : ∀ (u₀ : ℝ → ℝ) (I : KdVInitialData u₀),
      KdVSchwartzInitialBoundary u₀ →
        KdVAdmissibleForFlow u₀ →
          Nonempty (KdVGlobalSolution u₀ I)) :
    StatementShape :=
  h

/-- The initial `L^2` hypothesis projects from the initial-data package. -/
theorem initial_memLp_two {u₀ : ℝ → ℝ} (I : KdVInitialData u₀) :
    MeasureTheory.MemLp u₀ (2 : ℝ≥0∞) :=
  I.initialMemLpTwo

/-- The initial-data package exposes the concrete admissibility target. -/
theorem initial_admissible_for_flow {u₀ : ℝ → ℝ} (I : KdVInitialData u₀) :
    KdVAdmissibleForFlow u₀ :=
  I.admissibleForKdVFlow

/-- A KdV solution package exposes the classical KdV equation on its domain. -/
theorem solution_solves_kdv {u₀ : ℝ → ℝ} {I : KdVInitialData u₀}
    (S : KdVGlobalSolution u₀ I) :
    SolvesClassicalKdV S.u classicalKdVDomain :=
  S.solvesKdV

/-- A KdV solution package exposes its initial trace. -/
theorem solution_initial_trace {u₀ : ℝ → ℝ} {I : KdVInitialData u₀}
    (S : KdVGlobalSolution u₀ I) (x : ℝ) :
    S.u (0, x) = u₀ x :=
  kdvInitialTrace_apply S.initialTrace x

/-- The selected KdV domain covers each nonnegative time slice. -/
theorem nonnegative_time_slice_mem {u₀ : ℝ → ℝ} {I : KdVInitialData u₀}
    (_S : KdVGlobalSolution u₀ I) {t : ℝ} (_ht : 0 ≤ t) (x : ℝ) :
    (t, x) ∈ classicalKdVDomain := by
  exact mem_classicalKdVDomain (t, x)

/-- A KdV solution package exposes conservation of the mass invariant. -/
theorem solution_mass_conserved {u₀ : ℝ → ℝ} {I : KdVInitialData u₀}
    (S : KdVGlobalSolution u₀ I) :
    KdVMassConservationTarget S.u classicalKdVDomain :=
  S.conservationTarget.mass

/-- A KdV solution package exposes conservation of the momentum invariant. -/
theorem solution_momentum_conserved {u₀ : ℝ → ℝ} {I : KdVInitialData u₀}
    (S : KdVGlobalSolution u₀ I) :
    KdVMomentumConservationTarget S.u classicalKdVDomain :=
  S.conservationTarget.momentum

/-- A KdV solution package exposes conservation of the energy invariant. -/
theorem solution_energy_conserved {u₀ : ℝ → ℝ} {I : KdVInitialData u₀}
    (S : KdVGlobalSolution u₀ I) :
    KdVEnergyConservationTarget S.u classicalKdVDomain :=
  S.conservationTarget.energy

/-- A KdV solution package exposes the selected uniqueness target. -/
theorem solution_uniqueness_target {u₀ : ℝ → ℝ} {I : KdVInitialData u₀}
    (S : KdVGlobalSolution u₀ I) :
    KdVUniquenessTarget u₀ S.u classicalKdVDomain :=
  S.uniquenessInAdmissibleClass

/-- Checked mathlib anchor: derivatives of Schwartz maps are available as continuous maps. -/
theorem schwartz_derivCLM_apply_anchor (f : 𝓢(ℝ, ℝ)) (x : ℝ) :
    SchwartzMap.derivCLM ℝ ℝ f x = deriv f x :=
  SchwartzMap.derivCLM_apply ℝ f x

/--
Checked mathlib anchor: the third derivative on one-dimensional Schwartz maps
can be expressed by iterating the continuous derivative map.
-/
def schwartzThirdDerivative : 𝓢(ℝ, ℝ) →L[ℝ] 𝓢(ℝ, ℝ) :=
  (SchwartzMap.derivCLM ℝ ℝ).comp
    ((SchwartzMap.derivCLM ℝ ℝ).comp (SchwartzMap.derivCLM ℝ ℝ))

/-- The third-derivative anchor unfolds to three applications of `derivCLM`. -/
theorem schwartzThirdDerivative_apply (f : 𝓢(ℝ, ℝ)) :
    schwartzThirdDerivative f =
      SchwartzMap.derivCLM ℝ ℝ (SchwartzMap.derivCLM ℝ ℝ (SchwartzMap.derivCLM ℝ ℝ f)) :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this KdV slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Deriv",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Fourier",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic"
]

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "ContDiff",
  "ContDiffOn",
  "MeasureTheory.MemLp",
  "MeasureTheory.integral",
  "MeasureTheory.eLpNorm",
  "Real.cosh",
  "Real.sqrt",
  "Real.deriv_cosh",
  "SchwartzMap.derivCLM",
  "SchwartzMap.derivCLM_apply",
  "SchwartzMap.lineDerivOp_apply",
  "SchwartzMap.fourier_lineDerivOp_eq",
  "SchwartzMap.lineDeriv_eq_fourierMultiplierCLM",
  "TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM",
  "TemperedDistribution.fourierMultiplierCLM"
]

/--
Search terms that did not locate a terminal KdV theorem in the pinned local
mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "Korteweg",
  "KdV",
  "de Vries",
  "soliton",
  "Soliton",
  "Lax pair",
  "Airy",
  "inverse scattering",
  "u_xxx",
  "dispersive PDE",
  "Airy equation",
  "Korteweg-de Vries"
]

/-- Machine status vocabulary for the C002 external-anchor audit. -/
inductive ExternalAnchorAuditStatus : Type where
  | repoLocalPinnedAdjacent
  | externalAnchorOnlyNotPinned
  | irrelevantNameCollision
  | authenticatedSearchBlocked
  | noTerminalLean4ProofVerified
  deriving DecidableEq

/-- Audit row for external or repo-local Lean sources inspected for KdV anchors. -/
structure ExternalAnchorAuditEntry : Type where
  repositoryURL : String
  commitSHA : String
  queryTerms : List String
  modulesOrFiles : List String
  declarationNames : List String
  placeholderStatus : String
  relevanceToKdV : String
  machineStatus : ExternalAnchorAuditStatus

/-- Requested C002 external-search terms. -/
def requestedExternalAuditTerms : List String := [
  "Korteweg",
  "KdV",
  "Soliton",
  "Lax pair",
  "Airy",
  "inverse scattering",
  "u_xxx"
]

/-- C002 authentication status for GitHub code search in this environment. -/
def authenticatedGithubAuditStatus : String :=
  "gh auth status reported no logged-in GitHub host on 2026-05-01; unauthenticated GitHub REST code search was rate-limited, so no authenticated GitHub code-search completion is claimed by this artifact."

/-- Repo-local pinned mathlib audit row: adjacent analysis anchors only, no terminal KdV proof. -/
def mathlibKdVExternalAuditEntry : ExternalAnchorAuditEntry where
  repositoryURL := "https://github.com/leanprover-community/mathlib4"
  commitSHA := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  queryTerms := requestedExternalAuditTerms
  modulesOrFiles := mathlibAnchorModules
  declarationNames := mathlibAnchorNames
  placeholderStatus :=
    "repo-local pinned dependency; local wrappers compile; no terminal KdV theorem and no placeholder-based completion claim"
  relevanceToKdV :=
    "Provides deriv, ContDiff, MemLp, Schwartz derivative, tempered-distribution, Fourier-multiplier, hyperbolic-function, and Sobolev-adjacent anchors; no Korteweg-de Vries, soliton, Lax-pair, inverse-scattering, or u_xxx terminal theorem was found in the pinned local mathlib snapshot."
  machineStatus := ExternalAnchorAuditStatus.repoLocalPinnedAdjacent

/--
External Fourier/Sobolev-adjacent candidate inherited from the local Stage1 KPV
audit.  It is useful reconnaissance only and is not a KdV terminal theorem.
-/
def sqgFourierKdVAdjacentAuditEntry : ExternalAnchorAuditEntry where
  repositoryURL := "https://github.com/Brsanch/sqg-lean-proofs-fourier"
  commitSHA := "ce02796e3d3ba91101fa86629c73d35ee7056ccf"
  queryTerms := ["Airy", "KdV", "Sobolev", "Kato-Ponce"]
  modulesOrFiles := [
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
    "prior local archive audit reported no Lean proof-placeholder tokens; not pinned, imported, or checked in this repository"
  relevanceToKdV :=
    "Concrete Fourier-side homogeneous Sobolev and Kato-Ponce infrastructure on T^2; not Korteweg-de Vries, not Airy/KdV real-line propagation, not soliton/Lax/inverse-scattering closure."
  machineStatus := ExternalAnchorAuditStatus.externalAnchorOnlyNotPinned

/--
External Sobolev-adjacent candidate inherited from the local Stage1 KPV audit.
It is compactness infrastructure, not a KdV theorem.
-/
def rellichKondrachovKdVAdjacentAuditEntry : ExternalAnchorAuditEntry where
  repositoryURL := "https://github.com/abenenson/rellich-kondrachov"
  commitSHA := "85f2c2e943404e5ba92911346874d8961e137b60"
  queryTerms := ["KdV", "Airy", "Sobolev"]
  modulesOrFiles := [
    "RellichKondrachov.Analysis.FunctionalSpaces.Sobolev.Euclidean.H1",
    "RellichKondrachov.Analysis.FunctionalSpaces.Sobolev.Euclidean.H2",
    "RellichKondrachov.Geometry.Manifold.Sobolev.RellichKondrachov"
  ]
  declarationNames := [
    "C1c",
    "C2c",
    "h1",
    "h2",
    "h1ToL2",
    "h2ToL2",
    "isCompactOperator_h1ToL2_riemannianVolume"
  ]
  placeholderStatus :=
    "prior local archive audit reported no Lean proof-placeholder tokens; not pinned, imported, or checked in this repository"
  relevanceToKdV :=
    "Concrete H1/H2 and compact-embedding infrastructure; not a Korteweg-de Vries, Airy propagator, soliton, Lax-pair, or inverse-scattering theorem."
  machineStatus := ExternalAnchorAuditStatus.externalAnchorOnlyNotPinned

/-- External Bourgain-name candidate that is irrelevant to the KdV PDE branch. -/
def leanBourgainNameCollisionAuditEntry : ExternalAnchorAuditEntry where
  repositoryURL := "https://github.com/Command-Master/lean-bourgain"
  commitSHA := "07fe8b2feac3e72d4f0bd1c8d094e1ebd0a02ffb"
  queryTerms := ["KdV", "Airy", "Bourgain"]
  modulesOrFiles := [
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
    "prior local archive audit reported no Lean proof-placeholder tokens; not pinned, imported, or checked in this repository"
  relevanceToKdV :=
    "Finite-field pseudorandom extractor project; Bourgain-name collision only, with no KdV, Airy, soliton, Lax-pair, inverse-scattering, or u_xxx API."
  machineStatus := ExternalAnchorAuditStatus.irrelevantNameCollision

/-- C002 audit rows available without claiming authenticated GitHub search closure. -/
def externalKdVAuditEntries : List ExternalAnchorAuditEntry := [
  mathlibKdVExternalAuditEntry,
  sqgFourierKdVAdjacentAuditEntry,
  rellichKondrachovKdVAdjacentAuditEntry,
  leanBourgainNameCollisionAuditEntry
]

/-- C002 conclusion: no external terminal Lean 4 KdV proof was verified or pinned. -/
def externalKdVAuditConclusion : String :=
  "No external Lean 4 terminal KdV proof was verified, imported, or pinned in this pass; parent THM-M-1548 remains not_repo_local_closed/formalization_debt, and the authenticated GitHub search leaf must remain open until credentials allow code search or a concrete integration blocker is recorded."

/-- C003 decision vocabulary for the external-proof integration gate. -/
inductive ExternalKdVProofIntegrationDecision : Type where
  | noExternalTerminalProofVerified
  | pinExternalDependencyRequired
  | vendorProofBodyRequired
  | concreteIntegrationBlocked
  deriving DecidableEq

/--
C003 integration decision.

No external terminal Lean 4 KdV proof was verified in this repo-local pass, so
there is currently no proof body to pin or vendor.  This is not a completion
claim for THM-M-1548.
-/
def c003IntegrationDecision : ExternalKdVProofIntegrationDecision :=
  ExternalKdVProofIntegrationDecision.noExternalTerminalProofVerified

/-- C003 source-search evidence that affects the pin/vendor decision. -/
def c003ExternalProofSearchEvidence : List String := [
  "gh auth status reported no logged-in GitHub host on 2026-05-01",
  "gh search code KdV --language Lean could not run without GitHub authentication",
  "GitHub REST code search for KdV language:Lean was rate-limited",
  "GitHub REST repository search for KdV Lean returned total_count = 0",
  "GitHub REST repository search for Korteweg-de Vries Lean returned total_count = 0",
  "pinned local mathlib search found adjacent analysis APIs but no terminal KdV theorem"
]

/-- C003 repo-local integration-debt gate for this non-completed pass. -/
def c003RepoLocalIntegrationDebtGate : String :=
  "Gate passes only in the non-completion sense: no verified external terminal Lean 4 KdV proof was left as anchor-only completed evidence.  THM-M-1548 remains not_repo_local_closed/formalization_debt until a proof body is locally proved, pinned, or vendored and checked."

/-- The C003 decision is definitionally the no-external-proof-found branch. -/
theorem c003IntegrationDecision_eq :
    c003IntegrationDecision =
      ExternalKdVProofIntegrationDecision.noExternalTerminalProofVerified :=
  rfl

/-- The C002 audit table records exactly the four rows above. -/
theorem externalKdVAuditEntries_length :
    externalKdVAuditEntries.length = 4 :=
  rfl

/-- The SQG Fourier candidate is not repo-local pinned for this KdV slot. -/
theorem sqgFourierKdVAdjacentAuditEntry_not_repoLocalPinned :
    sqgFourierKdVAdjacentAuditEntry.machineStatus ≠
      ExternalAnchorAuditStatus.repoLocalPinnedAdjacent := by
  decide

/-- The Rellich-Kondrachov candidate is not repo-local pinned for this KdV slot. -/
theorem rellichKondrachovKdVAdjacentAuditEntry_not_repoLocalPinned :
    rellichKondrachovKdVAdjacentAuditEntry.machineStatus ≠
      ExternalAnchorAuditStatus.repoLocalPinnedAdjacent := by
  decide

/-- Repo-local status vocabulary for expanded M1548 unchecked child leaves. -/
inductive M1548LeafStatus : Type where
  | checkedStatementBoundary
  | uncheckedSubledgerOpen
  | integrationBlocked
  deriving DecidableEq

/--
Independent `<=100`-step subledger for a single unchecked M1548 leaf.

These rows are process/checklist data, not terminal KdV proof claims.
-/
structure M1548LeafSubledger : Type where
  leafId : String
  packageId : String
  objective : String
  prerequisites : List String
  substeps : List String
  maxProofSteps : Nat
  status : M1548LeafStatus
  completionGate : String

/-- The local budget gate attached to each expanded child leaf. -/
def M1548LeafSubledger.budgetWithinM0387 (s : M1548LeafSubledger) : Prop :=
  s.maxProofSteps ≤ 100

/-- Expanded C005 subledger for `M1548-L020`: weak-residual API audit. -/
def M1548_L020_subledger : M1548LeafSubledger where
  leafId := "M1548-L020"
  packageId := "P1.mathlib_object_model"
  objective := "Audit Fourier multiplier and tempered-distribution APIs for a weak KdV residual."
  prerequisites := [
    "Pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "Checked local anchors SchwartzMap.derivCLM and TemperedDistribution.fourierMultiplierCLM"
  ]
  substeps := [
    "List the exact derivative, Schwartz, Fourier, and tempered-distribution modules used by the residual model.",
    "Check whether mathlib exposes a third line-derivative operator suitable for u_xxx.",
    "Check whether products of distributions or Schwartz/test functions are available for the nonlinear u*u_x term.",
    "Record missing nonlinear weak-product infrastructure as formalization debt, not as a completed weak KdV residual."
  ]
  maxProofSteps := 45
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "May close only after exact module/theorem anchors are recorded and the nonlinear weak-product blocker is either proved locally or explicitly scoped out."

/-- Expanded C005 subledger for `M1548-L021`: selected solution API and domain. -/
def M1548_L021_subledger : M1548LeafSubledger where
  leafId := "M1548-L021"
  packageId := "P2.classical_pde_bridge"
  objective := "Choose classical versus weak solution API and domain: whole line, torus, or interval."
  prerequisites := [
    "selectedTerminalBranch = oneSolitonVerification",
    "classicalKdVDomain = Set.univ"
  ]
  substeps := [
    "Use the one-soliton branch as the current public terminal branch.",
    "Keep the initial repo-local domain as all real time-space rather than a torus or bounded interval.",
    "State that the current solution API is classical pointwise residual, not weak distributional residual.",
    "Record that alternative weak, periodic, and well-posedness domains remain separate branches."
  ]
  maxProofSteps := 35
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "May close publicly only when the blueprint records the one-soliton/all-real-line/classical-pointwise choice."

/-- Expanded C005 subledger for `M1548-L022`: pointwise-to-weak bridge. -/
def M1548_L022_subledger : M1548LeafSubledger where
  leafId := "M1548-L022"
  packageId := "P2.classical_pde_bridge"
  objective := "Bridge pointwise kdvResidual 6 u = 0 to a distribution/test-function formulation."
  prerequisites := [
    "ClassicalKdVSolutionClass u classicalKdVDomain",
    "KdVResidualInterpretation u classicalKdVDomain"
  ]
  substeps := [
    "Define the test-function pairing intended for the selected weak residual.",
    "Prove or import integration-by-parts lemmas for temporal and third spatial derivatives.",
    "Prove that the nonlinear classical product u*u_x is integrable against each selected test function.",
    "Conclude the weak residual vanishes from pointwise vanishing only after the previous analytic lemmas are checked."
  ]
  maxProofSteps := 90
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until the pairing, integration-by-parts, and nonlinear integrability lemmas compile locally."

/-- Expanded C005 subledger for `M1548-L023`: derivative regularity. -/
def M1548_L023_subledger : M1548LeafSubledger where
  leafId := "M1548-L023"
  packageId := "P2.classical_pde_bridge"
  objective := "Prove derivative regularity lemmas required for u*u_x and u_xxx in the chosen class."
  prerequisites := [
    "ContDiffOn ℝ 3 u classicalKdVDomain",
    "temporalDerivative, spatialDerivative, and thirdSpatialDerivative definitions"
  ]
  substeps := [
    "Extract first spatial differentiability from ContDiffOn ℝ 3.",
    "Extract third spatial differentiability from ContDiffOn ℝ 3.",
    "Establish regularity of the pointwise product u * spatialDerivative u on the chosen domain.",
    "Package these facts as reusable hypotheses for residual and conservation calculations."
  ]
  maxProofSteps := 85
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until the ContDiffOn projection and product-regularity lemmas are local Lean theorems."

/-- Expanded C005 subledger for `M1548-L024`: mass functional. -/
def M1548_L024_subledger : M1548LeafSubledger where
  leafId := "M1548-L024"
  packageId := "P3.conservation_laws"
  objective := "Define the selected mass functional."
  prerequisites := [
    "timeSlice",
    "kdvMass"
  ]
  substeps := [
    "Use the signed real-line mass kdvMass v = integral v.",
    "Specify the decay or integrability hypothesis under which the integral is meaningful.",
    "Add projection lemmas connecting KdVMassConservationTarget to timeSlice.",
    "Avoid claiming conservation until the derivative and boundary-term proof is checked."
  ]
  maxProofSteps := 40
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "May close after the public surface records kdvMass and the required integrability side conditions."

/-- Expanded C005 subledger for `M1548-L025`: momentum functional. -/
def M1548_L025_subledger : M1548LeafSubledger where
  leafId := "M1548-L025"
  packageId := "P3.conservation_laws"
  objective := "Define the selected momentum functional."
  prerequisites := [
    "timeSlice",
    "kdvMomentum"
  ]
  substeps := [
    "Use the quadratic real-line momentum kdvMomentum v = integral (v^2).",
    "Specify L2 or stronger side conditions for the quadratic integral.",
    "Add projection lemmas connecting KdVMomentumConservationTarget to timeSlice.",
    "Avoid claiming conservation until the formal time-derivative calculation is checked."
  ]
  maxProofSteps := 40
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "May close after the public surface records kdvMomentum and the required L2/integrability side conditions."

/-- Expanded C005 subledger for `M1548-L026`: energy functional. -/
def M1548_L026_subledger : M1548LeafSubledger where
  leafId := "M1548-L026"
  packageId := "P3.conservation_laws"
  objective := "Define the selected KdV energy/Hamiltonian functional."
  prerequisites := [
    "kdvEnergyDensity",
    "kdvEnergy"
  ]
  substeps := [
    "Use the classical density (deriv v)^2 - 2*v^3 in the current normalization.",
    "Specify differentiability and integrability side conditions for both density terms.",
    "Add projection lemmas connecting KdVEnergyConservationTarget to timeSlice.",
    "Keep boundary-term cancellation as a later proof leaf."
  ]
  maxProofSteps := 45
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "May close after the public surface records kdvEnergy and the required differentiability/integrability side conditions."

/-- Expanded C005 subledger for `M1548-L027`: mass conservation. -/
def M1548_L027_subledger : M1548LeafSubledger where
  leafId := "M1548-L027"
  packageId := "P3.conservation_laws"
  objective := "Prove mass conservation for smooth decaying or periodic classical solutions."
  prerequisites := [
    "SolvesClassicalKdV u classicalKdVDomain",
    "Boundary or periodic cancellation hypothesis for spatial total derivatives"
  ]
  substeps := [
    "Differentiate the mass integral with respect to time under the integral sign.",
    "Substitute u_t = -6*u*u_x - u_xxx from the KdV residual.",
    "Rewrite 6*u*u_x and u_xxx as spatial total derivatives.",
    "Use decay or periodic boundary cancellation to show the derivative of mass is zero.",
    "Integrate the zero time derivative to get equality with the initial mass."
  ]
  maxProofSteps := 95
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until differentiation-under-integral and boundary-cancellation lemmas compile locally."

/-- Expanded C005 subledger for `M1548-L028`: momentum conservation. -/
def M1548_L028_subledger : M1548LeafSubledger where
  leafId := "M1548-L028"
  packageId := "P3.conservation_laws"
  objective := "Prove momentum conservation for smooth decaying or periodic classical solutions."
  prerequisites := [
    "SolvesClassicalKdV u classicalKdVDomain",
    "Product and integration-by-parts lemmas for u^2"
  ]
  substeps := [
    "Differentiate the quadratic momentum integral under the integral sign.",
    "Apply the chain rule to obtain the integral of 2*u*u_t.",
    "Substitute the KdV residual expression for u_t.",
    "Rewrite the resulting nonlinear and third-derivative terms as spatial total derivatives.",
    "Use decay or periodic boundary cancellation to conclude conservation."
  ]
  maxProofSteps := 95
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until chain-rule, integration-by-parts, and boundary-cancellation lemmas compile locally."

/-- Expanded C005 subledger for `M1548-L029`: energy conservation. -/
def M1548_L029_subledger : M1548LeafSubledger where
  leafId := "M1548-L029"
  packageId := "P3.conservation_laws"
  objective := "Prove energy/Hamiltonian conservation for smooth decaying or periodic classical solutions."
  prerequisites := [
    "SolvesClassicalKdV u classicalKdVDomain",
    "Regularity sufficient for differentiating deriv (timeSlice u t)",
    "Boundary or periodic cancellation hypothesis"
  ]
  substeps := [
    "Differentiate the energy integral under the integral sign.",
    "Apply product and chain rules to the derivative-square and cubic terms.",
    "Substitute the KdV residual expression for u_t.",
    "Use integration by parts to convert the remaining expression to boundary terms.",
    "Apply decay or periodic cancellation to obtain zero time derivative and conservation."
  ]
  maxProofSteps := 100
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until higher-regularity, differentiation-under-integral, and boundary-cancellation lemmas compile locally."

/-- Expanded C005 subledger for `M1548-L030`: one-soliton verification. -/
def M1548_L030_subledger : M1548LeafSubledger where
  leafId := "M1548-L030"
  packageId := "P4.well_posedness_or_soliton_branch"
  objective := "Verify a one-soliton closed-form solution satisfies the KdV residual under explicit parameter constraints."
  prerequisites := [
    "selectedTerminalBranch = oneSolitonVerification",
    "OneSolitonParameters with 0 < speed",
    "oneSolitonProfile"
  ]
  substeps := [
    "Prove the needed derivatives of sech y = (Real.cosh y)^-1.",
    "Differentiate the phase (sqrt speed / 2) * (x - speed*t - center) in t and x.",
    "Compute u_t, u_x, and u_xxx for oneSolitonProfile.",
    "Use positivity of speed to simplify sqrt speed identities.",
    "Normalize the polynomial/hyperbolic expression and prove kdvResidual 6 equals zero."
  ]
  maxProofSteps := 100
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until the complete residual calculation is a placeholder-free local Lean theorem."

/-- Expanded C005 subledger for `M1548-L031`: restricted well-posedness alternative. -/
def M1548_L031_subledger : M1548LeafSubledger where
  leafId := "M1548-L031"
  packageId := "P4.well_posedness_or_soliton_branch"
  objective := "Formalize local well-posedness statement in a deliberately restricted smooth class, if chosen instead of soliton verification."
  prerequisites := [
    "A future branch decision that supersedes oneSolitonVerification",
    "Explicit Banach/Sobolev solution space"
  ]
  substeps := [
    "State the chosen restricted smooth or Sobolev class.",
    "State existence, uniqueness, and continuous-dependence components separately.",
    "Identify the contraction, semigroup, or energy-estimate theorem intended to prove existence.",
    "Mark this branch inactive while selectedTerminalBranch remains oneSolitonVerification."
  ]
  maxProofSteps := 70
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Cannot close for completion while the public branch remains one-soliton verification; if branch changes, it needs a separate proof package."

/-- Expanded C005 subledger for `M1548-L032`: uniqueness target. -/
def M1548_L032_subledger : M1548LeafSubledger where
  leafId := "M1548-L032"
  packageId := "P4.well_posedness_or_soliton_branch"
  objective := "Prove uniqueness in the selected admissible class or mark the exact missing estimate."
  prerequisites := [
    "KdVUniquenessTarget",
    "Chosen solution class and admissibility hypotheses"
  ]
  substeps := [
    "Define the difference w = v - u for two candidate solutions.",
    "Derive the evolution equation satisfied by w.",
    "State the energy or Gronwall estimate needed to force w = 0.",
    "Record the exact missing estimate if it is unavailable in mathlib or local code."
  ]
  maxProofSteps := 90
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until the difference-equation estimate is proved locally or listed as a concrete blocker."

/-- Expanded C005 subledger for `M1548-L033`: Lax operator definition. -/
def M1548_L033_subledger : M1548LeafSubledger where
  leafId := "M1548-L033"
  packageId := "P5.lax_spectral_or_variational_branch"
  objective := "Define the KdV Lax operator in the selected function-space model."
  prerequisites := [
    "A selected spectral function-space model",
    "Second derivative and multiplication-by-u operator APIs"
  ]
  substeps := [
    "Choose whether the Lax operator acts on Schwartz functions, L2, or a Sobolev domain.",
    "Define the negative second derivative component.",
    "Define the multiplication-by-u potential component.",
    "State domain and self-adjointness side conditions separately."
  ]
  maxProofSteps := 80
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until the operator model and domain side conditions are Lean definitions, not prose."

/-- Expanded C005 subledger for `M1548-L034`: Lax equation bridge. -/
def M1548_L034_subledger : M1548LeafSubledger where
  leafId := "M1548-L034"
  packageId := "P5.lax_spectral_or_variational_branch"
  objective := "State/prove the Lax equation bridge or mark unavailable spectral prerequisites."
  prerequisites := [
    "M1548-L033 Lax operator model",
    "A commutator API for the chosen operator class"
  ]
  substeps := [
    "Define the auxiliary operator P used in the KdV Lax pair.",
    "Define the commutator [P, L] in the chosen operator model.",
    "Show that dL/dt = [P, L] is equivalent to the KdV residual under regularity hypotheses.",
    "If unbounded-operator APIs are missing, record the exact missing mathlib abstraction."
  ]
  maxProofSteps := 95
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Remains open until the commutator equation compiles or an exact unbounded-operator blocker is recorded."

/-- Expanded C005 subledger for `M1548-L035`: spectral API audit. -/
def M1548_L035_subledger : M1548LeafSubledger where
  leafId := "M1548-L035"
  packageId := "P5.lax_spectral_or_variational_branch"
  objective := "Audit mathlib spectral APIs for unbounded Schrodinger operators; if unavailable, record concrete blocker."
  prerequisites := [
    "mathlib spectral/operator theory modules at the pinned revision",
    "M1548-L033 intended Lax operator model"
  ]
  substeps := [
    "Search pinned mathlib for unbounded self-adjoint operator and spectrum APIs.",
    "Search for Schrodinger operator, Sturm-Liouville, or second-derivative spectral anchors.",
    "Record exact modules and declaration names when present.",
    "If the APIs are absent, classify the Lax/ispectral branch as formalization debt rather than completed."
  ]
  maxProofSteps := 60
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "May close as an audit leaf only with exact module/theorem names or a concrete API-absence blocker."

/-- Expanded C005 subledger for `M1548-L036`: repo-local proof/dependency gate. -/
def M1548_L036_subledger : M1548LeafSubledger where
  leafId := "M1548-L036"
  packageId := "P6.repo_local_gate"
  objective := "Repo-local wrapper imports exactly the selected proof body/dependency and validates with lake env lean; no placeholder declarations."
  prerequisites := [
    "Selected terminal branch",
    "Local proof body or pinned external dependency",
    "Placeholder scan"
  ]
  substeps := [
    "If no external proof exists, keep the status not_repo_local_closed/formalization_debt.",
    "If an external Lean 4 proof exists, pin it as a Lake dependency or vendor the proof body.",
    "Add a local wrapper theorem only after the proof body is in the repo-local verification closure.",
    "Run lake env lean on the owned Stage1 artifact and run the placeholder scan."
  ]
  maxProofSteps := 55
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Cannot close completed with external_upstream_anchor_only; must be local_proof_body, local_wrapper_upstream_mathlib, external_upstream_pinned, or a concrete blocker."

/-- Expanded C005 subledger for `M1548-L037`: public merge gate. -/
def M1548_L037_subledger : M1548LeafSubledger where
  leafId := "M1548-L037"
  packageId := "P6.repo_local_gate"
  objective := "Public blueprint/todo/README status is updated only after machine anchor, local validation, and human-readable tree are consistent."
  prerequisites := [
    "Machine anchor or explicit non-completion debt classification",
    "Local validation command result",
    "Human-readable theorem-tree subledger"
  ]
  substeps := [
    "Merge the subledger text into the authoritative public Stage1 surface serially.",
    "Keep public checklist items unchecked unless the local machine gate is satisfied.",
    "Ensure README, todo, and blueprint summaries do not conflict about completion status.",
    "Record validation date, command, and result in the public backfill."
  ]
  maxProofSteps := 45
  status := M1548LeafStatus.uncheckedSubledgerOpen
  completionGate := "Public backfill may merge these subledgers, but completion remains blocked until M0387 machine and integration gates are satisfied."

/-- C005 expansion of unchecked leaves `M1548-L020` through `M1548-L037`. -/
def M1548_C005_expandedSubledgers : List M1548LeafSubledger := [
  M1548_L020_subledger,
  M1548_L021_subledger,
  M1548_L022_subledger,
  M1548_L023_subledger,
  M1548_L024_subledger,
  M1548_L025_subledger,
  M1548_L026_subledger,
  M1548_L027_subledger,
  M1548_L028_subledger,
  M1548_L029_subledger,
  M1548_L030_subledger,
  M1548_L031_subledger,
  M1548_L032_subledger,
  M1548_L033_subledger,
  M1548_L034_subledger,
  M1548_L035_subledger,
  M1548_L036_subledger,
  M1548_L037_subledger
]

/-- The C005 subledger expansion covers exactly the requested 18 leaves. -/
theorem M1548_C005_expandedSubledgers_length :
    M1548_C005_expandedSubledgers.length = 18 :=
  rfl

/-- Every C005 expanded leaf keeps an M0387 `<=100` proof-step budget. -/
theorem M1548_C005_expandedSubledgers_budget_gate :
    M1548_C005_expandedSubledgers.all
      (fun s => decide (s.maxProofSteps ≤ 100)) = true :=
  rfl

/-- The C005 expansion is a process ledger, not a terminal KdV completion claim. -/
def M1548_C005_completionBoundary : String :=
  "M1548-L020 through M1548-L037 are expanded into independent <=100-step subledgers, but all remain non-completion process leaves until local Lean proof bodies or concrete integration blockers satisfy the M0387 machine gates."

/-! ## Audit probes -/

#check StatementShape
#check selectedTerminalBranch
#check OneSolitonParameters
#check oneSolitonProfile
#check OneSolitonVerificationTarget
#check KdVInitialData
#check KdVGlobalSolution
#check classicalKdVDomain
#check ClassicalKdVSolutionClass
#check KdVResidualInterpretation
#check KdVInitialTrace
#check KdVSchwartzInitialBoundary
#check KdVAdmissibleForFlow
#check kdvMass
#check kdvMomentum
#check kdvEnergy
#check KdVConservationTarget
#check KdVUniquenessTarget
#check kdvResidual
#check SolvesClassicalKdV
#check initial_memLp_two
#check initial_admissible_for_flow
#check solution_solves_kdv
#check solution_initial_trace
#check solution_mass_conserved
#check solution_momentum_conserved
#check solution_energy_conserved
#check solution_uniqueness_target
#check schwartz_derivCLM_apply_anchor
#check schwartzThirdDerivative
#check deriv
#check ContDiff
#check ContDiffOn
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
#check Real.cosh
#check Real.sqrt
#check Real.deriv_cosh
#check SchwartzMap.derivCLM
#check SchwartzMap.derivCLM_apply
#check TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM
#check TemperedDistribution.fourierMultiplierCLM
#check requestedExternalAuditTerms
#check authenticatedGithubAuditStatus
#check externalKdVAuditEntries
#check externalKdVAuditConclusion
#check c003IntegrationDecision
#check c003ExternalProofSearchEvidence
#check c003RepoLocalIntegrationDebtGate
#check c003IntegrationDecision_eq
#check externalKdVAuditEntries_length
#check M1548LeafSubledger
#check M1548_C005_expandedSubledgers
#check M1548_C005_expandedSubledgers_length
#check M1548_C005_expandedSubledgers_budget_gate
#check M1548_C005_completionBoundary

end S1_M_207
end Stage1
end AwesomeTheorems
