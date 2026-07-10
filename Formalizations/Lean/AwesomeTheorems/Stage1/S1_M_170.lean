import Mathlib.Analysis.Convex.Function
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.Normed.Operator.Compact
import Mathlib.MeasureTheory.Function.UnifTight
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Topology.Compactness.Compact
import Mathlib.Topology.Separation.Basic

/-!
# S1-M-170 / THM-M-1205: compensated compactness

This Stage1 artifact records a conservative Lean 4 statement boundary for a
Tartar-Murat/Kruzkov-style compensated compactness method for conservation laws.

The pinned mathlib snapshot has useful substrates for distributions, `L^p`
convergence, uniform integrability/tightness, topological compactness, and
convex entropy functions.  This audit did not find a terminal compensated
compactness, div-curl, Young-measure reduction, or conservation-law entropy
compactness theorem in the local dependency closure.

The declarations below therefore keep the hard PDE compactness mechanism as
explicit proposition-valued hypotheses and expose only checked wrappers around
available mathlib convergence and compactness anchors.
-/

noncomputable section

open Filter MeasureTheory Set Topology
open scoped BigOperators ENNReal NNReal Topology Distributions MeasureTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_170

universe u

/-- Space-time model for a scalar conservation law over a finite-dimensional spatial index set. -/
abbrev SpaceTime (ι : Type u) : Type u :=
  ℝ × (ι → ℝ)

/-- A scalar space-time field. -/
abbrev ScalarField (ι : Type u) : Type u :=
  SpaceTime ι → ℝ

/-- A flux depending on the scalar state and returning a spatial vector. -/
abbrev Flux (ι : Type u) : Type u :=
  ℝ → ι → ℝ

/-- The time coordinate direction in `SpaceTime ι`. -/
def timeDirection (ι : Type u) : SpaceTime ι :=
  (1, 0)

/-- The `i`-th spatial coordinate direction in `SpaceTime ι`. -/
def spatialDirection (ι : Type u) (i : ι) : SpaceTime ι := by
  classical
  exact (0, fun j => if j = i then 1 else 0)

/--
Entropy/entropy-flux pair for a scalar conservation law.

The convexity of the scalar entropy is represented concretely.  The legacy
field `compatibilityWithFlux` is retained as a hook for solution classes, while
`EntropyFluxCompatible` below gives the checked pointwise derivative statement
`qᵢ' = eta' fᵢ'`.
-/
structure EntropyPair (ι : Type u) : Type u where
  entropy : ℝ → ℝ
  entropyFlux : ℝ → ι → ℝ
  entropy_convex : ConvexOn ℝ univ entropy
  compatibilityWithFlux : Flux ι → Prop

/--
Pointwise scalar entropy-pair compatibility at state `a`.

For every spatial coordinate `i`, this encodes the formal identity
`d/du qᵢ(u) = eta'(u) * d/du fᵢ(u)` using Frechet derivatives on `ℝ`.
-/
def EntropyFluxCompatibilityAt
    {ι : Type u} (pair : EntropyPair ι) (flux : Flux ι) (a : ℝ) : Prop :=
  ∀ i : ι,
    fderiv ℝ (fun s : ℝ => pair.entropyFlux s i) a 1 =
      fderiv ℝ pair.entropy a 1 *
        fderiv ℝ (fun s : ℝ => flux s i) a 1

/-- Concrete entropy-pair compatibility for a scalar flux: `q' = eta' f'` at every state. -/
def EntropyFluxCompatible
    {ι : Type u} (pair : EntropyPair ι) (flux : Flux ι) : Prop :=
  ∀ a : ℝ, EntropyFluxCompatibilityAt pair flux a

/-- Scalar distributions on an open space-time domain. -/
abbrev ScalarDistributionOn
    (ι : Type u) [Fintype ι] (Ω : TopologicalSpace.Opens (SpaceTime ι))
    (n : ℕ∞ := ⊤) : Type u :=
  Distribution Ω ℝ n

/-- Entropy-production distributions on an open space-time domain. -/
abbrev EntropyProductionDistributionOn
    (ι : Type u) [Fintype ι] (Ω : TopologicalSpace.Opens (SpaceTime ι))
    (n : ℕ∞ := ⊤) : Type u :=
  ScalarDistributionOn ι Ω n

/-- Smooth compactly supported test functions on a space-time domain. -/
abbrev SpaceTimeTestFunction
    (ι : Type u) [Fintype ι] (Ω : TopologicalSpace.Opens (SpaceTime ι)) : Type u :=
  TestFunction Ω ℝ ⊤

/--
The scalar integrand appearing in the distributional weak formulation of
`∂t u + div f(u) = 0`.

For a compactly supported smooth test function `φ`, this is
`u ∂t φ + Σᵢ fᵢ(u) ∂ᵢ φ`.  The zero integral of this expression is the
distributional conservation-law identity after integration by parts.
-/
def conservationLawWeakIntegrand
    {ι : Type u} [Fintype ι]
    {Ω : TopologicalSpace.Opens (SpaceTime ι)}
    (u : ScalarField ι) (flux : Flux ι) (φ : SpaceTimeTestFunction ι Ω)
    (z : SpaceTime ι) : ℝ := by
  classical
  exact
    u z * fderiv ℝ (φ : SpaceTime ι → ℝ) z (timeDirection ι) +
      ∑ i : ι, flux (u z) i *
        fderiv ℝ (φ : SpaceTime ι → ℝ) z (spatialDirection ι i)

/--
The scalar integrand whose negative integral is the action of the entropy
production distribution `∂t eta(u) + div q(u)` on a test function.
-/
def entropyProductionWeakIntegrand
    {ι : Type u} [Fintype ι]
    {Ω : TopologicalSpace.Opens (SpaceTime ι)}
    (u : ScalarField ι) (pair : EntropyPair ι) (φ : SpaceTimeTestFunction ι Ω)
    (z : SpaceTime ι) : ℝ := by
  classical
  exact
    pair.entropy (u z) * fderiv ℝ (φ : SpaceTime ι → ℝ) z (timeDirection ι) +
      ∑ i : ι, pair.entropyFlux (u z) i *
        fderiv ℝ (φ : SpaceTime ι → ℝ) z (spatialDirection ι i)

/--
Concrete test-function action for an entropy-production distribution.

Mathematically this states
`⟨∂t eta(u) + div q(u), φ⟩ =
  - ∫ (eta(u) ∂t φ + Σᵢ qᵢ(u) ∂ᵢ φ)`.
The integrability condition is explicit because the current Stage1 boundary has
no solution-class API deriving it.
-/
def EntropyProductionDistributionAction
    {ι : Type u} [Fintype ι]
    {Ω : TopologicalSpace.Opens (SpaceTime ι)}
    (μ : Measure (SpaceTime ι)) (u : ScalarField ι) (pair : EntropyPair ι)
    (T : EntropyProductionDistributionOn ι Ω) : Prop :=
  ∀ φ : SpaceTimeTestFunction ι Ω,
    Integrable (fun z => entropyProductionWeakIntegrand u pair φ z) μ ∧
      T φ = -MeasureTheory.integral μ
        (fun z => entropyProductionWeakIntegrand u pair φ z)

/--
Concrete distributional formulation of the scalar conservation law
`∂t u + div f(u) = 0` over `SpaceTime ι`.

This is intentionally a weak identity against all bundled mathlib test
functions on the open domain.  Integrability is kept explicit because the
current Stage1 boundary has no solution-class API that would derive it.
-/
def DistributionalConservationLaw
    {ι : Type u} [Fintype ι]
    (Ω : TopologicalSpace.Opens (SpaceTime ι)) (μ : Measure (SpaceTime ι))
    (u : ScalarField ι) (flux : Flux ι) : Prop :=
  ∀ φ : SpaceTimeTestFunction ι Ω,
    Integrable (fun z => conservationLawWeakIntegrand u flux φ z) μ ∧
      MeasureTheory.integral μ (fun z => conservationLawWeakIntegrand u flux φ z) = 0

/--
Normalized input data for a compensated compactness theorem for scalar
conservation laws.

The concrete fields use current mathlib objects.  The proposition-valued fields
mark the missing PDE infrastructure after the distributional conservation-law
identity: entropy-production compactness in a negative Sobolev/distribution
topology, div-curl or Young-measure reduction, and the genuine-nonlinearity
closure.
-/
structure ConservationLawCompactnessData (ι : Type u) [Fintype ι] : Type u where
  domain : TopologicalSpace.Opens (SpaceTime ι)
  measure : Measure (SpaceTime ι)
  exponent : ℝ≥0∞
  sequence : ℕ → ScalarField ι
  limit : ScalarField ι
  flux : Flux ι
  entropyProduction : EntropyPair ι → ℕ → EntropyProductionDistributionOn ι domain
  entropyPairCompatibility :
    ∀ pair : EntropyPair ι, pair.compatibilityWithFlux flux ↔
      EntropyFluxCompatible pair flux
  entropyProduction_action :
    ∀ (pair : EntropyPair ι) (n : ℕ),
      pair.compatibilityWithFlux flux →
        EntropyProductionDistributionAction measure (sequence n) pair
          (entropyProduction pair n)
  boundaryOrInitialConditions : Prop
  uniformRangeBound : Prop
  entropyProductionCompact : Prop
  divCurlOrYoungMeasureReduction : Prop
  genuineNonlinearity : Prop

/-- The concrete weak conservation-law proposition attached to the compactness data. -/
def ConservationLawCompactnessData.distributionalConservationLaw
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Prop :=
  ∀ n, DistributionalConservationLaw D.domain D.measure (D.sequence n) D.flux

/-- Convert the data-level compatibility hook into the concrete derivative condition. -/
theorem ConservationLawCompactnessData.entropyFluxCompatible
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι)
    {pair : EntropyPair ι} (h : pair.compatibilityWithFlux D.flux) :
    EntropyFluxCompatible pair D.flux :=
  (D.entropyPairCompatibility pair).mp h

/-- Extract the checked entropy-production distribution action for a compatible pair. -/
theorem ConservationLawCompactnessData.entropyProductionAction
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι)
    (pair : EntropyPair ι) (n : ℕ) (h : pair.compatibilityWithFlux D.flux) :
    EntropyProductionDistributionAction D.measure (D.sequence n) pair
      (D.entropyProduction pair n) :=
  D.entropyProduction_action pair n h

/--
The PDE-side hypotheses for the compensated compactness method.

This bundle is deliberately weaker than a terminal theorem: it records exactly
the hard formalization boundary that future work must replace with concrete
distributional inequalities and compactness proofs.
-/
def CompensatedCompactnessHypotheses
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Prop :=
  D.distributionalConservationLaw ∧
    D.boundaryOrInitialConditions ∧
      D.uniformRangeBound ∧
        D.entropyProductionCompact ∧
          D.divCurlOrYoungMeasureReduction ∧
            D.genuineNonlinearity

/-- Full strong `L^p` convergence of the approximating sequence to the selected limit. -/
def StrongLpConvergence
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Prop :=
  Tendsto
    (fun n => eLpNorm (D.sequence n - D.limit) D.exponent D.measure)
    atTop (𝓝 0)

/-- Subsequence strong `L^p` compactness, the usual compensated-compactness output shape. -/
structure StrongSubsequenceCompactness
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Type u where
  subsequence : ℕ → ℕ
  strictMono_subsequence : StrictMono subsequence
  strongLp_subsequence :
    Tendsto
      (fun k => eLpNorm (D.sequence (subsequence k) - D.limit) D.exponent D.measure)
      atTop (𝓝 0)

/--
Downstream hypotheses under which mathlib's Vitali convergence theorem already
turns convergence in measure plus uniform integrability/tightness into strong
`L^p` convergence.

The compensated-compactness proof is expected to provide these hypotheses, or a
subsequence version of them, from entropy-production compactness and the
Young-measure/div-curl reduction.
-/
structure VitaliReadyHypotheses
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Prop where
  exponent_ge_one : 1 ≤ D.exponent
  exponent_ne_top : D.exponent ≠ ∞
  sequence_memLp : ∀ n, MemLp (D.sequence n) D.exponent D.measure
  limit_memLp : MemLp D.limit D.exponent D.measure
  tendstoInMeasure : TendstoInMeasure D.measure D.sequence atTop D.limit
  uniformIntegrable : UnifIntegrable D.sequence D.exponent D.measure
  uniformTight : UnifTight D.sequence D.exponent D.measure

/--
Subsequence form of the Vitali-ready hypotheses.

This is the compactness-output shape usually expected from the PDE side:
entropy compactness and the div-curl/Young-measure reduction first select a
strictly increasing subsequence, and that reindexed sequence is then
Vitali-ready.
-/
structure VitaliReadySubsequenceHypotheses
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) where
  subsequence : ℕ → ℕ
  strictMono_subsequence : StrictMono subsequence
  exponent_ge_one : 1 ≤ D.exponent
  exponent_ne_top : D.exponent ≠ ∞
  sequence_memLp : ∀ k, MemLp (D.sequence (subsequence k)) D.exponent D.measure
  limit_memLp : MemLp D.limit D.exponent D.measure
  tendstoInMeasure :
    TendstoInMeasure D.measure (fun k => D.sequence (subsequence k)) atTop D.limit
  uniformIntegrable :
    UnifIntegrable (fun k => D.sequence (subsequence k)) D.exponent D.measure
  uniformTight :
    UnifTight (fun k => D.sequence (subsequence k)) D.exponent D.measure

/--
Normalized Stage1 statement shape for compensated compactness.

For every finite-dimensional scalar conservation-law datum, the PDE-side
compensated-compactness hypotheses should produce a strongly convergent
subsequence.  This is a proposition only; no terminal PDE proof is claimed.
-/
def StatementShape : Prop :=
  ∀ (ι : Type u) [Fintype ι] (D : ConservationLawCompactnessData ι),
    CompensatedCompactnessHypotheses D →
      Nonempty (StrongSubsequenceCompactness D)

/-- The statement shape unfolds to the expected quantified compactness assertion. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ (ι : Type u) [Fintype ι] (D : ConservationLawCompactnessData ι),
        CompensatedCompactnessHypotheses D →
          Nonempty (StrongSubsequenceCompactness D) :=
  Iff.rfl

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (ι : Type u) [Fintype ι] (D : ConservationLawCompactnessData ι),
      CompensatedCompactnessHypotheses D →
        Nonempty (StrongSubsequenceCompactness D)) :
    StatementShape.{u} :=
  h

/-! ## Public statement normalization -/

/--
Public statement-normalization boundary for `THM-M-1205`.

This deliberately aliases `AwesomeTheorems.Stage1.S1_M_170.StatementShape`.
It is the current repo-local Lean statement boundary for compensated
compactness, not a terminal Tartar-Murat/Kruzkov compactness theorem.
-/
abbrev PublicStatementNormalization : Prop :=
  StatementShape.{u}

/-- The public-normalization boundary is definitionally the same as `StatementShape`. -/
theorem publicStatementNormalization_iff_statementShape :
    PublicStatementNormalization.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/-- Canonical checked name for the current repo-local statement boundary. -/
def publicStatementBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_170.StatementShape"

/-- Checked metadata for the public statement-normalization backfill. -/
def publicStatementNormalizationNotes : List String := [
  "Use AwesomeTheorems.Stage1.S1_M_170.StatementShape as the current repo-local Lean statement boundary for THM-M-1205.",
  "The boundary states that compensated-compactness hypotheses for scalar conservation-law data should yield strong subsequential Lp compactness.",
  "This is not a terminal compensated compactness theorem: entropy inequalities, negative-Sobolev compactness, div-curl or Young-measure reduction, and the PDE-to-Vitali bridge remain formalization debt."
]

/-- The public statement-normalization metadata is explicitly non-terminal. -/
def publicStatementNormalizationIsTerminal : Bool := false

/-- Sanity check for the non-terminal public-normalization gate. -/
theorem publicStatementNormalizationIsTerminal_eq_false :
    publicStatementNormalizationIsTerminal = false :=
  rfl

/-! ## External anchor integration gate -/

/-- Audit shape for a possible future external Lean 4 compensated-compactness anchor. -/
structure ExternalLeanAnchorAudit where
  exactTerminalProofFound : Prop
  importedIntoLakeClosure : Prop
  concreteIntegrationBlockerRecorded : Prop

/--
Repo-local integration-debt gate: if an exact external Lean 4 proof is found,
it must either enter this Lake closure or be blocked by a concrete integration
reason.  Anchor-only evidence is not a completed state for this slot.
-/
def RepoLocalIntegrationDebtGate (A : ExternalLeanAnchorAudit) : Prop :=
  A.exactTerminalProofFound →
    A.importedIntoLakeClosure ∨ A.concreteIntegrationBlockerRecorded

/-- If no exact external anchor is found, the integration-debt gate is vacuous. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit) (h : Not A.exactTerminalProofFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/-! ## Source-level external Lean audit -/

/-- One source-level row for auditing an external Lean 4 compensated-compactness project. -/
structure ExternalLeanSourceAuditRow where
  source : String
  revisionOrDate : String
  sourceLevelEvidence : String
  terminalProofStatus : String
  repoLocalClosureAction : String

/--
Source-level audit rows for future external Lean 4 compensated-compactness work.

These rows are intentionally metadata, not theorem claims.  The current
repo-local status is that no terminal external Lean 4 proof has been found,
pinned, imported, or checked for the full compensated-compactness theorem.
-/
def externalLeanCompensatedCompactnessSourceAuditRows :
    List ExternalLeanSourceAuditRow := [
  {
    source := "repo-local Lake closure, pinned mathlib dependency"
    revisionOrDate := "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"
    sourceLevelEvidence :=
      "local imports expose distributions, test functions, Lp convergence, uniform integrability/tightness, compact operators, and convex functions"
    terminalProofStatus :=
      "not_terminal: no compensated-compactness, div-curl, Young-measure, or scalar conservation-law entropy compactness theorem was located"
    repoLocalClosureAction :=
      "keep THM-M-1205 open; only checked conditional wrappers and audit metadata are available in this file"
  },
  {
    source := "leanprover-community/mathlib4 upstream candidate"
    revisionOrDate := "future exact commit required before use"
    sourceLevelEvidence :=
      "search terms to rerun at source level: CompensatedCompactness, Tartar, Murat, DivCurl, YoungMeasure, Kruzkov, entropy solution, conservation law"
    terminalProofStatus :=
      "not_repo_local_closed: no terminal upstream theorem is currently imported into this repository"
    repoLocalClosureAction :=
      "if a theorem lands upstream, pin the mathlib revision, import the module, and check a repo-local wrapper theorem"
  },
  {
    source := "future non-mathlib Lean 4 compensated-compactness project"
    revisionOrDate := "unassigned until a concrete repository and commit are found"
    sourceLevelEvidence :=
      "required evidence: repository URL, commit hash, Lean toolchain, Lake manifest, module path, theorem name, and closed proof body with no kernel placeholders"
    terminalProofStatus :=
      "candidate_only: no concrete external project is being used as evidence in this artifact"
    repoLocalClosureAction :=
      "before any completion claim, add the project as a pinned dependency or vendor the proof, resolve license/toolchain conflicts, and run this file in Lake"
  }
]

/-- Search terms for future external Lean 4 source-level audits. -/
def externalLeanCompensatedCompactnessSearchTerms : List String := [
  "CompensatedCompactness",
  "compensated compactness",
  "Tartar",
  "Murat",
  "DivCurl",
  "div curl",
  "YoungMeasure",
  "Young measure",
  "Kruzkov",
  "Kružkov",
  "entropy solution",
  "conservation law",
  "entropy compactness"
]

/--
Concrete audit conclusion for this artifact: no exact terminal external Lean 4
compensated-compactness proof is being used.
-/
def currentExternalLeanAnchorAudit : ExternalLeanAnchorAudit where
  exactTerminalProofFound := False
  importedIntoLakeClosure := False
  concreteIntegrationBlockerRecorded := True

/-- The current source-level audit table has the expected three rows. -/
theorem externalLeanCompensatedCompactnessSourceAuditRows_length :
    externalLeanCompensatedCompactnessSourceAuditRows.length = 3 :=
  rfl

/-- The current external-anchor gate is closed by the absence of a terminal anchor. -/
theorem currentRepoLocalIntegrationDebtGate :
    RepoLocalIntegrationDebtGate currentExternalLeanAnchorAudit :=
  repoLocalIntegrationDebtGate_of_no_external_anchor
    currentExternalLeanAnchorAudit id

/--
Checked mathlib anchor: Vitali convergence converts convergence in measure,
uniform integrability, and uniform tightness into strong `L^p` convergence.
-/
theorem strongLpConvergence_of_vitaliReady
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : VitaliReadyHypotheses D) :
    StrongLpConvergence D :=
  (tendstoInMeasure_iff_tendsto_Lp h.exponent_ge_one h.exponent_ne_top
    h.sequence_memLp h.limit_memLp).mp
      ⟨h.tendstoInMeasure, h.uniformIntegrable, h.uniformTight⟩

/-- A full strong-convergence result gives subsequence compactness using the identity subsequence. -/
theorem strongSubsequenceCompactness_of_strongLp
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : StrongLpConvergence D) :
    Nonempty (StrongSubsequenceCompactness D) :=
  ⟨{
    subsequence := id
    strictMono_subsequence := strictMono_id
    strongLp_subsequence := by
      simpa [StrongLpConvergence] using h
  }⟩

/-- Combined checked wrapper from Vitali-ready hypotheses to the subsequence conclusion. -/
theorem strongSubsequenceCompactness_of_vitaliReady
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : VitaliReadyHypotheses D) :
    Nonempty (StrongSubsequenceCompactness D) :=
  strongSubsequenceCompactness_of_strongLp (strongLpConvergence_of_vitaliReady h)

/-- Vitali convergence applied to a selected reindexed subsequence. -/
theorem strongLpConvergence_subsequence_of_vitaliReadySubsequence
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : VitaliReadySubsequenceHypotheses D) :
    Tendsto
      (fun k => eLpNorm (D.sequence (h.subsequence k) - D.limit) D.exponent D.measure)
      atTop (𝓝 0) :=
  (tendstoInMeasure_iff_tendsto_Lp h.exponent_ge_one h.exponent_ne_top
    h.sequence_memLp h.limit_memLp).mp
      ⟨h.tendstoInMeasure, h.uniformIntegrable, h.uniformTight⟩

/-- Checked wrapper from subsequence Vitali-ready hypotheses to the compactness conclusion. -/
theorem strongSubsequenceCompactness_of_vitaliReadySubsequence
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : VitaliReadySubsequenceHypotheses D) :
    Nonempty (StrongSubsequenceCompactness D) :=
  ⟨{
    subsequence := h.subsequence
    strictMono_subsequence := h.strictMono_subsequence
    strongLp_subsequence := by
      simpa using strongLpConvergence_subsequence_of_vitaliReadySubsequence h
  }⟩

/--
Direct full-sequence PDE-to-Vitali bridge expected from a future compensated
compactness proof.

The current artifact does not prove this bridge; it records the exact checked
interface needed to reuse `strongSubsequenceCompactness_of_vitaliReady`.
-/
def PDECompactnessToVitaliReadyHypotheses
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Prop :=
  CompensatedCompactnessHypotheses D → VitaliReadyHypotheses D

/--
Subsequence PDE-to-Vitali bridge expected from a future compensated compactness
proof.

This is the more faithful compactness interface: the PDE mechanism may select a
strictly increasing subsequence and prove Vitali-ready hypotheses for that
reindexed sequence.
-/
def PDECompactnessToVitaliReadySubsequenceHypotheses
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Prop :=
  CompensatedCompactnessHypotheses D →
    Nonempty (VitaliReadySubsequenceHypotheses D)

/-- Checked full-sequence bridge from PDE compactness hypotheses to subsequence compactness. -/
theorem strongSubsequenceCompactness_of_pdeCompactnessToVitaliReady
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (hcc : CompensatedCompactnessHypotheses D)
    (hbridge : PDECompactnessToVitaliReadyHypotheses D) :
    Nonempty (StrongSubsequenceCompactness D) :=
  strongSubsequenceCompactness_of_vitaliReady (hbridge hcc)

/-- Checked subsequence bridge from PDE compactness hypotheses to subsequence compactness. -/
theorem strongSubsequenceCompactness_of_pdeCompactnessToVitaliReadySubsequence
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (hcc : CompensatedCompactnessHypotheses D)
    (hbridge : PDECompactnessToVitaliReadySubsequenceHypotheses D) :
    Nonempty (StrongSubsequenceCompactness D) := by
  rcases hbridge hcc with ⟨hvit⟩
  exact strongSubsequenceCompactness_of_vitaliReadySubsequence hvit

/--
Local reduction target for the div-curl/Young-measure leaf.

This is the exact checked interface still missing from the PDE side: convert
entropy-production compactness plus the div-curl or Young-measure reduction and
genuine nonlinearity into the Vitali-ready hypotheses already handled by
mathlib.  It is a proposition-valued boundary, not a proof of the PDE reduction.
-/
def DivCurlOrYoungMeasureReductionToVitali
    {ι : Type u} [Fintype ι] (D : ConservationLawCompactnessData ι) : Prop :=
  D.distributionalConservationLaw →
    D.entropyProductionCompact →
      D.divCurlOrYoungMeasureReduction →
        D.genuineNonlinearity →
          VitaliReadyHypotheses D

/--
Checked conditional wrapper for the missing div-curl/Young-measure reduction.

Once a future local proof or pinned dependency supplies
`DivCurlOrYoungMeasureReductionToVitali D`, the existing Vitali wrapper gives
the desired strong subsequential compactness.
-/
theorem strongSubsequenceCompactness_of_divCurlOrYoungMeasureReductionToVitali
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (hcc : CompensatedCompactnessHypotheses D)
    (hred : DivCurlOrYoungMeasureReductionToVitali D) :
    Nonempty (StrongSubsequenceCompactness D) :=
  strongSubsequenceCompactness_of_vitaliReady
    (hred hcc.1 hcc.2.2.2.1 hcc.2.2.2.2.1 hcc.2.2.2.2.2)

/-- Extract the distributional conservation-law field from the PDE-side hypothesis bundle. -/
theorem CompensatedCompactnessHypotheses.distributionalConservationLaw
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : CompensatedCompactnessHypotheses D) :
    D.distributionalConservationLaw :=
  h.1

/-- Extract the entropy-production compactness field from the PDE-side hypothesis bundle. -/
theorem CompensatedCompactnessHypotheses.entropyProductionCompact
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : CompensatedCompactnessHypotheses D) :
    D.entropyProductionCompact :=
  h.2.2.2.1

/-- Extract the Young-measure/div-curl reduction field from the PDE-side hypothesis bundle. -/
theorem CompensatedCompactnessHypotheses.divCurlOrYoungMeasureReduction
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : CompensatedCompactnessHypotheses D) :
    D.divCurlOrYoungMeasureReduction :=
  h.2.2.2.2.1

/-- Extract the genuine-nonlinearity field from the PDE-side hypothesis bundle. -/
theorem CompensatedCompactnessHypotheses.genuineNonlinearity
    {ι : Type u} [Fintype ι] {D : ConservationLawCompactnessData ι}
    (h : CompensatedCompactnessHypotheses D) :
    D.genuineNonlinearity :=
  h.2.2.2.2.2

/-- Checked compactness anchor: finite sets have compact closure in R0 spaces. -/
theorem finiteSet_compactClosure
    {X : Type u} [TopologicalSpace X] [R0Space X] {s : Set X}
    (hs : s.Finite) :
    IsCompact (closure s) :=
  hs.isCompact_closure

/-- Checked compactness anchor: relatively compact boundedness is compact closure. -/
theorem relativelyCompact_isBounded_iff
    {X : Type u} [TopologicalSpace X] [R0Space X] {s : Set X} :
    @Bornology.IsBounded X (Bornology.relativelyCompact X) s ↔
      IsCompact (closure s) :=
  Bornology.relativelyCompact.isBounded_iff

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Normed.Operator.Compact",
  "Mathlib.MeasureTheory.Function.UnifTight",
  "Mathlib.MeasureTheory.Function.UniformIntegrable",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.Topology.Compactness.Compact",
  "Mathlib.Topology.Separation.Basic",
  "Mathlib.Analysis.Convex.Function"
]

/-- Checked declaration names used as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "Distribution",
  "TestFunction",
  "fderiv",
  "MeasureTheory.Integrable",
  "MeasureTheory.integral",
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.TendstoInMeasure",
  "MeasureTheory.UnifIntegrable",
  "MeasureTheory.UnifTight",
  "MeasureTheory.tendstoInMeasure_iff_tendsto_Lp",
  "ConvexOn",
  "IsCompact",
  "IsCompactOperator",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "isCompactOperator_iff_exists_mem_nhds_isCompact_closure_image",
  "Bornology.relativelyCompact.isBounded_iff",
  "Set.Finite.isCompact_closure"
]

/-- Search terms that did not locate a terminal compensated compactness theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "compensated compactness",
  "CompensatedCompactness",
  "Tartar",
  "Murat",
  "div-curl",
  "DivCurl",
  "Young measure",
  "Kruzkov",
  "Kružkov",
  "entropy solution",
  "conservation law"
]

/-! ## Negative-Sobolev and compact-embedding audit -/

/--
Pinned mathlib module-level audit for the entropy-production compactness leaf.

The entries record available adjacent infrastructure only.  They are not a
terminal negative-Sobolev compactness, Rellich-Kondrachov, Aubin-Lions, div-curl,
Young-measure, or scalar conservation-law entropy compactness theorem.
-/
def negativeSobolevCompactnessAuditRows : List (String × String) := [
  (
    "Mathlib.Analysis.Distribution.Distribution",
    "Distribution and TestFunction infrastructure suitable for weak statement shapes; no located negative Sobolev norm/topology or compactness theorem."
  ),
  (
    "Mathlib.Analysis.Distribution.TemperedDistribution",
    "Tempered-distribution and Schwartz-space substrate; no entropy-production compactness API."
  ),
  (
    "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
    "Gagliardo-Nirenberg-Sobolev eLpNorm/fderiv inequalities for compactly supported C1 functions; no SobolevSpace/WeakDerivative/negative-order space or compact embedding API located."
  ),
  (
    "Mathlib.Analysis.Normed.Operator.Compact",
    "Generic IsCompactOperator API for compact maps between topological vector spaces; no PDE Sobolev compact embedding instance located."
  ),
  (
    "Mathlib.Topology.Compactness.Compact",
    "General topological compactness substrate; not a PDE compactness theorem."
  ),
  (
    "Mathlib.MeasureTheory.Function.UnifTight",
    "Vitali-side uniform integrability/tightness substrate used after the PDE compactness mechanism is supplied."
  )
]

/-- Search terms used for the negative-Sobolev/compact-embedding audit leaf. -/
def absentNegativeSobolevCompactnessSearchTerms : List String := [
  "NegativeSobolev",
  "negative Sobolev",
  "SobolevSpace",
  "WeakDerivative",
  "CompactEmbedding",
  "Rellich",
  "Kondrachov",
  "Aubin",
  "Lions",
  "div-curl",
  "DivCurl",
  "Young measure",
  "entropy production compactness"
]

/--
Audit conclusion for the pinned mathlib snapshot used by this repo.

This is deliberately a Boolean metadata gate, not a proof of absence in all
future mathlib.  The checked local conclusion is only that this artifact is not
using a located repo-local negative-Sobolev entropy-production compactness API.
-/
def negativeSobolevEntropyCompactnessApiFoundInPinnedMathlib : Bool := false

/-- The pinned-mathlib audit is explicitly non-terminal for entropy-production compactness. -/
theorem negativeSobolevEntropyCompactnessApiFoundInPinnedMathlib_eq_false :
    negativeSobolevEntropyCompactnessApiFoundInPinnedMathlib = false :=
  rfl

/-! ## Div-curl and Young-measure reduction audit -/

/-- One missing theorem family for the div-curl/Young-measure reduction leaf. -/
structure ReductionDebtRow where
  theoremFamily : String
  requiredLeanShape : String
  currentRepoLocalStatus : String
  closureRequirement : String

/--
Pinned mathlib audit for the local div-curl/Young-measure reduction leaf.

These rows record the theorem families needed to replace
`ConservationLawCompactnessData.divCurlOrYoungMeasureReduction : Prop` with
checked Lean content.  The current file supplies only the conditional wrapper
`strongSubsequenceCompactness_of_divCurlOrYoungMeasureReductionToVitali`.
-/
def divCurlYoungMeasureReductionDebtRows : List ReductionDebtRow := [
  {
    theoremFamily := "Tartar-Murat div-curl compactness lemma"
    requiredLeanShape :=
      "weak convergence plus compact divergence/curl hypotheses imply convergence of scalar products or commutation relations in distributions"
    currentRepoLocalStatus :=
      "formalization_debt: no local or pinned mathlib DivCurl theorem family was located"
    closureRequirement :=
      "define divergence/curl for distribution-valued vector fields over SpaceTime ι and prove/import the div-curl compactness conclusion"
  },
  {
    theoremFamily := "Young-measure generation and fundamental theorem for bounded scalar sequences"
    requiredLeanShape :=
      "bounded Lp or L∞ sequence admits a parametrized probability-measure subsequence representing weak limits of nonlinear observables"
    currentRepoLocalStatus :=
      "formalization_debt: no local or pinned mathlib YoungMeasure/parameterized-measure compactness API was located"
    closureRequirement :=
      "define the Young-measure object, subsequence generation, barycenter relation, and observable convergence theorem"
  },
  {
    theoremFamily := "Entropy commutation relation for scalar conservation laws"
    requiredLeanShape :=
      "entropy-production compactness forces the Tartar commutation identity for entropy pairs along the generated Young measure"
    currentRepoLocalStatus :=
      "formalization_debt: current entropy-production action is checked, but compactness-to-commutation is not formalized"
    closureRequirement :=
      "connect entropy-production compactness in a negative Sobolev or distribution topology to the Young-measure/div-curl commutation relation"
  },
  {
    theoremFamily := "Genuine-nonlinearity collapse of Young measures"
    requiredLeanShape :=
      "the commutation relation plus genuine nonlinearity implies the generated Young measure is almost everywhere a Dirac mass"
    currentRepoLocalStatus :=
      "formalization_debt: current file keeps genuine nonlinearity as a Prop and has no Dirac-collapse theorem"
    closureRequirement :=
      "formalize genuine nonlinearity for the scalar flux and prove the Dirac-mass reduction yielding convergence in measure"
  },
  {
    theoremFamily := "PDE-to-Vitali bridge after reduction"
    requiredLeanShape :=
      "Dirac-collapse/convergence in measure plus uniform integrability and tightness produce VitaliReadyHypotheses D"
    currentRepoLocalStatus :=
      "checked conditional wrappers only: strongSubsequenceCompactness_of_pdeCompactnessToVitaliReady, strongSubsequenceCompactness_of_pdeCompactnessToVitaliReadySubsequence, and strongSubsequenceCompactness_of_divCurlOrYoungMeasureReductionToVitali"
    closureRequirement :=
      "replace PDECompactnessToVitaliReadyHypotheses or PDECompactnessToVitaliReadySubsequenceHypotheses with a local proof body or a pinned imported theorem"
  }
]

/-- Search terms used for the div-curl/Young-measure reduction audit leaf. -/
def absentDivCurlYoungMeasureSearchTerms : List String := [
  "DivCurl",
  "div-curl",
  "Tartar",
  "Murat",
  "YoungMeasure",
  "Young measure",
  "ParameterizedMeasure",
  "parametrized measure",
  "commutation relation",
  "genuine nonlinearity",
  "Dirac mass",
  "entropy compactness",
  "compensated compactness"
]

/--
Boolean metadata gate for the pinned mathlib snapshot used by this repo.

This is not a proof of absence in all Lean developments; it records that this
repo-local artifact did not locate or use a pinned div-curl or Young-measure
reduction theorem family.
-/
def divCurlYoungMeasureReductionApiFoundInPinnedMathlib : Bool := false

/-- The pinned-mathlib audit is explicitly non-terminal for the reduction leaf. -/
theorem divCurlYoungMeasureReductionApiFoundInPinnedMathlib_eq_false :
    divCurlYoungMeasureReductionApiFoundInPinnedMathlib = false :=
  rfl

/-- The reduction-debt table has the expected five local leaves. -/
theorem divCurlYoungMeasureReductionDebtRows_length :
    divCurlYoungMeasureReductionDebtRows.length = 5 :=
  rfl

/-! ## Stage1 public synchronization gate -/

/--
Checked metadata for the final Stage1 synchronization child.

This records the closure policy for `S1-M-170-C008`: local Lean validation and
private theorem-tree ledger updates are necessary, but the public Stage1
checklist must remain open until a serial integrator merges the public surface.
-/
structure Stage1ChecklistSynchronizationGate where
  localLeanValidationPassed : Bool
  theoremTreeLedgerSynchronized : Bool
  publicMergeSurfaceSynchronized : Bool
  terminalProofClosed : Bool
  checklistMayClose : Bool
  closureReason : String

/--
Current C008 synchronization status.

The public merge surface is intentionally `false` here because this worker is
not allowed to edit `Docs/Stage1_Blueprint.md`, `Docs/todos_20260430.md`, or
shared import aggregators.  Thus the checked policy keeps the public checklist
open and makes no terminal theorem claim.
-/
def currentStage1ChecklistSynchronizationGate : Stage1ChecklistSynchronizationGate where
  localLeanValidationPassed := true
  theoremTreeLedgerSynchronized := true
  publicMergeSurfaceSynchronized := false
  terminalProofClosed := false
  checklistMayClose := false
  closureReason :=
    "Keep S1-M-170 open: local validation and private ledger are ready, but the public merge surface is not synchronized and no terminal compensated-compactness proof is closed."

/-- The current C008 synchronization gate does not permit public checklist closure. -/
theorem currentStage1ChecklistMayClose_eq_false :
    currentStage1ChecklistSynchronizationGate.checklistMayClose = false :=
  rfl

/-- The current C008 synchronization gate records that public merge is still pending. -/
theorem currentStage1PublicMergeSurfaceSynchronized_eq_false :
    currentStage1ChecklistSynchronizationGate.publicMergeSurfaceSynchronized = false :=
  rfl

/-! ## Audit probes -/

#check EntropyPair
#check EntropyFluxCompatibilityAt
#check EntropyFluxCompatible
#check ScalarDistributionOn
#check EntropyProductionDistributionOn
#check SpaceTimeTestFunction
#check conservationLawWeakIntegrand
#check entropyProductionWeakIntegrand
#check EntropyProductionDistributionAction
#check DistributionalConservationLaw
#check ConservationLawCompactnessData
#check ConservationLawCompactnessData.entropyFluxCompatible
#check ConservationLawCompactnessData.entropyProductionAction
#check CompensatedCompactnessHypotheses
#check StrongLpConvergence
#check StrongSubsequenceCompactness
#check VitaliReadyHypotheses
#check VitaliReadySubsequenceHypotheses
#check StatementShape
#check strongLpConvergence_of_vitaliReady
#check strongSubsequenceCompactness_of_vitaliReady
#check strongLpConvergence_subsequence_of_vitaliReadySubsequence
#check strongSubsequenceCompactness_of_vitaliReadySubsequence
#check PDECompactnessToVitaliReadyHypotheses
#check PDECompactnessToVitaliReadySubsequenceHypotheses
#check strongSubsequenceCompactness_of_pdeCompactnessToVitaliReady
#check strongSubsequenceCompactness_of_pdeCompactnessToVitaliReadySubsequence
#check ExternalLeanSourceAuditRow
#check externalLeanCompensatedCompactnessSourceAuditRows
#check externalLeanCompensatedCompactnessSearchTerms
#check currentExternalLeanAnchorAudit
#check externalLeanCompensatedCompactnessSourceAuditRows_length
#check currentRepoLocalIntegrationDebtGate
#check DivCurlOrYoungMeasureReductionToVitali
#check strongSubsequenceCompactness_of_divCurlOrYoungMeasureReductionToVitali
#check finiteSet_compactClosure
#check relativelyCompact_isBounded_iff
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check IsCompactOperator
#check isCompactOperator_iff_exists_mem_nhds_isCompact_closure_image
#check negativeSobolevCompactnessAuditRows
#check absentNegativeSobolevCompactnessSearchTerms
#check negativeSobolevEntropyCompactnessApiFoundInPinnedMathlib_eq_false
#check divCurlYoungMeasureReductionDebtRows
#check absentDivCurlYoungMeasureSearchTerms
#check divCurlYoungMeasureReductionApiFoundInPinnedMathlib_eq_false
#check divCurlYoungMeasureReductionDebtRows_length
#check Stage1ChecklistSynchronizationGate
#check currentStage1ChecklistSynchronizationGate
#check currentStage1ChecklistMayClose_eq_false
#check currentStage1PublicMergeSurfaceSynchronized_eq_false

end S1_M_170
end Stage1
end AwesomeTheorems
