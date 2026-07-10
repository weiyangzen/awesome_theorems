import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique
import Mathlib.Topology.ContinuousMap.Basic

/-!
# S1-M-168 / THM-M-1312: Choquet-Bruhat-Geroch theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Choquet-Bruhat-Geroch theorem on maximal globally hyperbolic developments of
Einstein initial data.

The pinned mathlib snapshot contains useful adjacent infrastructure: smooth
manifolds, tangent bundles, local/global integral curves, Picard-Lindelof and
Gronwall-style ODE uniqueness, continuity, and Riemannian metrics.  This audit
did not find a terminal Lorentzian geometry, Einstein equations, constraint
equations, global hyperbolicity, or maximal Cauchy development theorem.

The declarations below therefore avoid proof placeholders and false completion
claims.  They normalize the expected theorem interface and include only small
checked wrappers around available mathlib facts.
-/

noncomputable section

open Set

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_168

universe u v w

/--
Abstract Cauchy initial data for the Einstein equations.

A terminal formalization must replace the proposition-valued fields by concrete
objects: a smooth three-manifold, Riemannian metric, second fundamental form,
Einstein constraint equations, regularity hypotheses, and gauge/hyperbolic
reduction data.
-/
structure EinsteinInitialData (Sigma : Type u) [TopologicalSpace Sigma] : Type u where
  constraintEquations : Prop
  regularityHypotheses : Prop
  cauchyHypersurfaceHypotheses : Prop
  gaugeChoice : Prop
  hyperbolicReductionReady : Prop

/--
Abstract spacetime development of Einstein initial data.

The `spacetimeMetric` field is intentionally just a relation-shaped placeholder:
mathlib does not currently provide the Lorentzian metric, curvature, Ricci
tensor, Einstein tensor, and global-hyperbolicity stack required for the real
Choquet-Bruhat-Geroch theorem.
-/
structure EinsteinDevelopment (Sigma : Type u) (M : Type v)
    [TopologicalSpace Sigma] [TopologicalSpace M]
    (D : EinsteinInitialData Sigma) : Type (max u v) where
  embedInitialSurface : Sigma → M
  spacetimeMetric : M → M → Prop
  embeddingContinuous : Continuous embedInitialSurface
  inducesInitialData : Prop
  satisfiesEinsteinEquations : Prop
  globallyHyperbolic : Prop
  cauchySurface : Prop
  maximalAmongGloballyHyperbolicDevelopments : Prop
  uniquenessUpToIsometry : Prop

/-- The bundled predicates expected of a maximal globally hyperbolic development. -/
def IsMaximalGloballyHyperbolicDevelopment {Sigma : Type u} {M : Type v}
    [TopologicalSpace Sigma] [TopologicalSpace M] {D : EinsteinInitialData Sigma}
    (X : EinsteinDevelopment Sigma M D) : Prop :=
  X.inducesInitialData ∧
    X.satisfiesEinsteinEquations ∧
      X.globallyHyperbolic ∧
        X.cauchySurface ∧
          X.maximalAmongGloballyHyperbolicDevelopments ∧
            X.uniquenessUpToIsometry

/--
Existence of a maximal globally hyperbolic development, with the spacetime type
left existential.  This is a statement-shape target, not a proof of existence.
-/
def HasMaximalGloballyHyperbolicDevelopment {Sigma : Type u} [TopologicalSpace Sigma]
    (D : EinsteinInitialData Sigma) : Prop :=
  ∃ (M : Type v) (topM : TopologicalSpace M),
    Nonempty (@EinsteinDevelopment Sigma M _ topM D)

/--
Normalized Stage1 statement shape for the Choquet-Bruhat-Geroch theorem.

For every admissible Einstein initial-data set, constraint satisfaction,
regularity, Cauchy-hypersurface hypotheses, gauge choice, and hyperbolic
reduction data should imply existence of a maximal globally hyperbolic
development, unique up to the appropriate isometry.  The hard geometric/PDE
content is kept as explicit hypotheses because no terminal Lean 4 proof of that
content was found in the local dependency closure.
-/
def StatementShape : Prop :=
  ∀ (Sigma : Type u) [TopologicalSpace Sigma] (D : EinsteinInitialData Sigma),
    D.constraintEquations →
      D.regularityHypotheses →
        D.cauchyHypersurfaceHypotheses →
          D.gaugeChoice →
            D.hyperbolicReductionReady →
              @HasMaximalGloballyHyperbolicDevelopment.{u, v} Sigma _ D

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Sigma : Type u) [TopologicalSpace Sigma] (D : EinsteinInitialData Sigma),
      D.constraintEquations →
        D.regularityHypotheses →
          D.cauchyHypersurfaceHypotheses →
            D.gaugeChoice →
              D.hyperbolicReductionReady →
                @HasMaximalGloballyHyperbolicDevelopment.{u, v} Sigma _ D) :
    @StatementShape.{u, v} :=
  show @StatementShape.{u, v} from h

/-!
## Public statement normalization

These checked declarations give the serial public-doc integrator a stable
repo-local boundary to cite while keeping THM-M-1312 explicitly nonterminal.
-/

/-- Public Stage1 alias for the current repo-local Choquet-Bruhat-Geroch boundary. -/
def PublicStatementNormalization : Prop :=
  @StatementShape.{u, v}

/-- The public Stage1 alias is definitionally the checked statement shape. -/
theorem publicStatementNormalization_iff_statementShape :
    @PublicStatementNormalization.{u, v} ↔ @StatementShape.{u, v} :=
  Iff.rfl

/-- Canonical checked declaration name for public Stage1 backfill. -/
def publicStatementBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_168.StatementShape"

/-- Integration-ready nonterminal summary for the public Stage1 surface. -/
def publicStatementNormalizationNotes : List String := [
  "StatementShape is the current repo-local Lean boundary for THM-M-1312 Choquet-Bruhat-Geroch.",
  "It normalizes the expected interface from Einstein initial data to existence of a maximal globally hyperbolic development.",
  "EinsteinInitialData and EinsteinDevelopment remain abstract placeholders for constraint equations, Lorentzian metrics, curvature tensors, global hyperbolicity, maximality, and uniqueness up to isometry.",
  "The checked local wrappers are only ODE/manifold infrastructure anchors and do not prove Einstein-equation global existence.",
  "This artifact is not a terminal Choquet-Bruhat-Geroch theorem."
]

/-- Explicit nonterminal gate for public integration text. -/
def publicStatementNormalizationIsTerminal : Bool := false

/-- Checked reminder that the public statement-normalization artifact is nonterminal. -/
theorem publicStatementNormalizationIsTerminal_eq_false :
    publicStatementNormalizationIsTerminal = false :=
  rfl

/-- A concrete development witnesses the existential statement-shape conclusion. -/
theorem hasDevelopment_of_development {Sigma : Type u} {M : Type v}
    [TopologicalSpace Sigma] [TopologicalSpace M] {D : EinsteinInitialData Sigma}
    (X : EinsteinDevelopment Sigma M D) :
    @HasMaximalGloballyHyperbolicDevelopment.{u, v} Sigma _ D :=
  ⟨M, inferInstance, ⟨X⟩⟩

/-- Extract the Einstein-equation predicate from a bundled development. -/
theorem satisfiesEinsteinEquations_of_isDevelopment {Sigma : Type u} {M : Type v}
    [TopologicalSpace Sigma] [TopologicalSpace M] {D : EinsteinInitialData Sigma}
    {X : EinsteinDevelopment Sigma M D}
    (hX : IsMaximalGloballyHyperbolicDevelopment X) :
    X.satisfiesEinsteinEquations :=
  hX.2.1

/-- Extract global hyperbolicity from a bundled development. -/
theorem globallyHyperbolic_of_isDevelopment {Sigma : Type u} {M : Type v}
    [TopologicalSpace Sigma] [TopologicalSpace M] {D : EinsteinInitialData Sigma}
    {X : EinsteinDevelopment Sigma M D}
    (hX : IsMaximalGloballyHyperbolicDevelopment X) :
    X.globallyHyperbolic :=
  hX.2.2.1

/-- Extract maximality from a bundled development. -/
theorem maximal_of_isDevelopment {Sigma : Type u} {M : Type v}
    [TopologicalSpace Sigma] [TopologicalSpace M] {D : EinsteinInitialData Sigma}
    {X : EinsteinDevelopment Sigma M D}
    (hX : IsMaximalGloballyHyperbolicDevelopment X) :
    X.maximalAmongGloballyHyperbolicDevelopments :=
  hX.2.2.2.2.1

/-- Extract uniqueness up to isometry from a bundled development. -/
theorem uniqueness_of_isDevelopment {Sigma : Type u} {M : Type v}
    [TopologicalSpace Sigma] [TopologicalSpace M] {D : EinsteinInitialData Sigma}
    {X : EinsteinDevelopment Sigma M D}
    (hX : IsMaximalGloballyHyperbolicDevelopment X) :
    X.uniquenessUpToIsometry :=
  hX.2.2.2.2.2

/-- Continuous maps preserve continuity of the embedded initial hypersurface. -/
theorem continuous_comp_developmentEmbedding {Sigma : Type u} {M : Type v} {N : Type w}
    [TopologicalSpace Sigma] [TopologicalSpace M] [TopologicalSpace N]
    {D : EinsteinInitialData Sigma} (X : EinsteinDevelopment Sigma M D)
    {f : M → N} (hf : Continuous f) :
    Continuous (f ∘ X.embedInitialSurface) :=
  hf.comp X.embeddingContinuous

/--
Checked mathlib anchor: a global manifold integral curve is continuous.

This is adjacent ODE/manifold infrastructure only; it is not the Einstein
evolution theorem.
-/
theorem mIntegralCurve_continuous_anchor
    {E H M : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    [TopologicalSpace M] [ChartedSpace H M]
    {γ : ℝ → M} {V : (x : M) → TangentSpace I x}
    (hγ : IsMIntegralCurve γ V) :
    Continuous γ :=
  hγ.continuous

/--
Checked mathlib anchor: a global manifold integral curve restricts to any time set.
-/
theorem mIntegralCurveOn_of_global_anchor
    {E H M : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    [TopologicalSpace M] [ChartedSpace H M]
    {γ : ℝ → M} {V : (x : M) → TangentSpace I x}
    (hγ : IsMIntegralCurve γ V) (s : Set ℝ) :
    IsMIntegralCurveOn γ V s :=
  hγ.isMIntegralCurveOn s

/--
Checked mathlib anchor: uniqueness for finite-dimensional ODE solutions under a
uniform Lipschitz condition in the state variable.
-/
theorem ode_solution_unique_anchor
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {vfield : ℝ → E → E} {K : NNReal}
    {f g : ℝ → E} {a b : ℝ}
    (hv : ∀ t : ℝ, LipschitzWith K (vfield t))
    (hf : ContinuousOn f (Set.Icc a b))
    (hf' : ∀ t ∈ Set.Ico a b,
      HasDerivWithinAt f (vfield t (f t)) (Set.Ici t) t)
    (hg : ContinuousOn g (Set.Icc a b))
    (hg' : ∀ t ∈ Set.Ico a b,
      HasDerivWithinAt g (vfield t (g t)) (Set.Ici t) t)
    (ha : f a = g a) :
    Set.EqOn f g (Set.Icc a b) :=
  ODE_solution_unique hv hf hf' hg hg' ha

/-!
## Available wrapper boundary

These checked declarations support the public `THM-M-1312.available-wrapper`
backfill.  They identify the local wrappers that may be cited for adjacent
ODE/manifold infrastructure while explicitly excluding any Einstein-equation
global-existence claim.
-/

/-- Local wrapper names available for the THM-M-1312 Stage1 public audit. -/
def availableWrapperAnchorNames : List String := [
  "mIntegralCurve_continuous_anchor",
  "mIntegralCurveOn_of_global_anchor",
  "ode_solution_unique_anchor"
]

/-- The available-wrapper audit has exactly three local checked anchors. -/
theorem availableWrapperAnchorNames_length :
    availableWrapperAnchorNames.length = 3 :=
  rfl

/-- Audit classification for the three available local wrappers. -/
def availableWrapperInfrastructureVerdict : List String := [
  "mIntegralCurve_continuous_anchor records continuity for global manifold integral curves.",
  "mIntegralCurveOn_of_global_anchor records restriction of a global manifold integral curve to a time set.",
  "ode_solution_unique_anchor records ODE solution uniqueness under a uniform Lipschitz condition.",
  "These wrappers are ODE/manifold infrastructure only, not Einstein-equation global existence."
]

/-- Public completion guard: the available wrappers are not terminal CBG evidence. -/
def availableWrapperIsEinsteinGlobalExistence : Bool := false

/-- Checked guard against reading the ODE/manifold wrappers as Einstein evolution. -/
theorem availableWrapperIsEinsteinGlobalExistence_eq_false :
    availableWrapperIsEinsteinGlobalExistence = false :=
  rfl

/-- Pinned mathlib revision used for the THM-M-1312 Stage1 mathlib audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Checked record of the pinned mathlib revision string. -/
theorem pinnedMathlibRevision_eq :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Exact module names requested by the THM-M-1312 mathlib-audit child task. -/
def mathlibAuditAvailableModules : List String := [
  "Geometry.Manifold.ContMDiff.Basic",
  "Geometry.Manifold.MFDeriv.Basic",
  "Geometry.Manifold.VectorBundle.Tangent",
  "Geometry.Manifold.VectorBundle.Riemannian",
  "Geometry.Manifold.Riemannian.Basic",
  "Geometry.Manifold.IntegralCurve.Basic",
  "Geometry.Manifold.IntegralCurve.ExistUnique",
  "Geometry.Manifold.IntegralCurve.UniformTime",
  "Analysis.ODE.Basic",
  "Analysis.ODE.Gronwall",
  "Analysis.ODE.PicardLindelof"
]

/-- The THM-M-1312 mathlib audit currently records eleven adjacent modules. -/
theorem mathlibAuditAvailableModules_length :
    mathlibAuditAvailableModules.length = 11 :=
  rfl

/--
Audit verdict for the pinned mathlib snapshot: the modules above provide
adjacent manifold, Riemannian, integral-curve, and ODE infrastructure only.
-/
def mathlibAuditVerdict : List String := [
  "Pinned mathlib revision: 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "The recorded modules are available as adjacent differential-geometry and ODE infrastructure.",
  "They do not provide a terminal Choquet-Bruhat-Geroch theorem, Lorentzian causal theory, Einstein equations, or maximal Cauchy development proof."
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.ContMDiff.Basic",
  "Mathlib.Geometry.Manifold.MFDeriv.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.IntegralCurve.Basic",
  "Mathlib.Geometry.Manifold.IntegralCurve.ExistUnique",
  "Mathlib.Geometry.Manifold.IntegralCurve.UniformTime",
  "Mathlib.Analysis.ODE.Basic",
  "Mathlib.Analysis.ODE.Gronwall",
  "Mathlib.Analysis.ODE.PicardLindelof"
]

/-- Checked declaration names used as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "ContMDiff",
  "mfderiv",
  "TangentSpace",
  "RiemannianMetric",
  "ContMDiffRiemannianMetric",
  "IsMIntegralCurve",
  "IsMIntegralCurveOn",
  "IsMIntegralCurve.continuous",
  "IsMIntegralCurve.isMIntegralCurveOn",
  "exists_isMIntegralCurveAt_of_contMDiffAt",
  "isMIntegralCurveAt_eventuallyEq_of_contMDiffAt",
  "ODE_solution_unique",
  "ODE_solution_unique_of_eventually"
]

/--
Search terms that did not locate a terminal Choquet-Bruhat-Geroch or Einstein
maximal-development theorem in local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Choquet",
  "Bruhat",
  "Geroch",
  "Choquet-Bruhat-Geroch",
  "Einstein equations",
  "Lorentzian",
  "globally hyperbolic",
  "Cauchy development",
  "maximal development",
  "Ricci tensor",
  "Einstein tensor",
  "constraint equations",
  "vacuum Einstein"
]

/-!
## External Lean 4 audit

This audit surface records primary-source Lean repositories checked for the
terms above.  It is deliberately nonterminal: no external Choquet-Bruhat-Geroch
closure is pinned, imported, or checked by this repository.
-/

/-- One primary-source Lean repository inspected for the external CBG audit. -/
structure ExternalLeanAuditEntry where
  repoName : String
  repoURL : String
  commit : String
  toolchain : String
  matchedTerms : List String
  theoremNames : List String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  terminalClosureFound : Bool
  repoLocalIntegrated : Bool

/-- Required external-audit search terms for THM-M-1312. -/
def externalAuditSearchTerms : List String := [
  "Choquet",
  "Bruhat",
  "Geroch",
  "Choquet-Bruhat-Geroch",
  "Einstein equations",
  "Lorentzian",
  "globally hyperbolic",
  "Cauchy development",
  "maximal development",
  "Ricci tensor",
  "Einstein tensor",
  "constraint equations",
  "vacuum Einstein"
]

/--
Runtime authentication status for the external search pass.

The child ledger records that GitHub CLI authentication was unavailable in this
process, so public completion still requires an authenticated rerun.
-/
def externalAuditAuthenticationStatus : String :=
  "gh auth status reported no GitHub login; unauthenticated primary-source probes were run and public completion remains blocked until authenticated rerun."

/-- Primary-source Lean repositories inspected during the external CBG audit. -/
def externalLeanAuditEntries : List ExternalLeanAuditEntry := [
  {
    repoName := "leanprover-community/mathlib4"
    repoURL := "https://github.com/leanprover-community/mathlib4"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    toolchain := "leanprover/lean4:v4.29.0"
    matchedTerms := ["Bruhat", "Einstein"]
    theoremNames := [
      "Mathlib.Algebra.Module.Lattice",
      "Mathlib.Algebra.Star.CHSH"
    ]
    placeholderStatus := "no CBG, Lorentzian-causality, Ricci/Einstein-tensor, or maximal-development theorem found; hits are unrelated references"
    lakeDependencyFeasibility := "already pinned as repo mathlib dependency"
    terminalClosureFound := false
    repoLocalIntegrated := false
  },
  {
    repoName := "HEPLean/PhysLean"
    repoURL := "https://github.com/HEPLean/PhysLean"
    commit := "cd22b0c28882412447d12d5cfde677c4ad999994"
    toolchain := "leanprover/lean4:v4.29.1"
    matchedTerms := ["Lorentzian", "Einstein tensor"]
    theoremNames := [
      "LorentzGroup",
      "TensorSpecies",
      "TensorSpecies.metricTensor",
      "Lorentz.Vector.minkowskiProduct",
      "Lorentz.Vector.minkowskiProduct_invariant"
    ]
    placeholderStatus := "adjacent special-relativity Lorentz tensor API only; no globally hyperbolic spacetime, Einstein-equation PDE, constraint, or maximal-development theorem found"
    lakeDependencyFeasibility := "potentially importable only after Lean 4.29.1/toolchain alignment; not pinned here"
    terminalClosureFound := false
    repoLocalIntegrated := false
  },
  {
    repoName := "SNSFT/Substrate-Neutral-Structural-Foundation-Theory-SNSFT"
    repoURL := "https://github.com/SNSFT/Substrate-Neutral-Structural-Foundation-Theory-SNSFT"
    commit := "a89e93fd07ad196e2e3b38b0252b81266cdf57e3"
    toolchain := "not recorded in lean-toolchain during audit"
    matchedTerms := ["Einstein equations", "Ricci tensor"]
    theoremNames := [
      "ricci_flow_dissipates_torsion",
      "ricci_flow_reduces_tension"
    ]
    placeholderStatus := "not a Choquet-Bruhat-Geroch formalization; physics terms occur in comments or project-specific reductions"
    lakeDependencyFeasibility := "not feasible as CBG evidence; unpinned mathlib requirement and no terminal theorem target"
    terminalClosureFound := false
    repoLocalIntegrated := false
  }
]

/-- The external-audit term matrix contains the thirteen required terms. -/
theorem externalAuditSearchTerms_length :
    externalAuditSearchTerms.length = 13 :=
  rfl

/-- The recorded external repositories do not contain a terminal CBG closure. -/
theorem externalLeanAuditEntries_terminalClosureFound_eq :
    externalLeanAuditEntries.map (fun entry => entry.terminalClosureFound) =
      [false, false, false] :=
  rfl

/-- No external CBG proof body has been imported into the repo-local closure. -/
theorem externalLeanAuditEntries_repoLocalIntegrated_eq :
    externalLeanAuditEntries.map (fun entry => entry.repoLocalIntegrated) =
      [false, false, false] :=
  rfl

/-- Public integration guard for `THM-M-1312.integration-gate`. -/
def externalAuditRepoLocalIntegrationDebtRetained : Bool := false

/--
The external-audit child found no external terminal closure, so it does not
create a completed-state repo-local integration debt.
-/
theorem externalAuditRepoLocalIntegrationDebtRetained_eq_false :
    externalAuditRepoLocalIntegrationDebtRetained = false :=
  rfl

/-- Integration-ready public external-audit note for THM-M-1312. -/
def externalAuditPublicBackfillNotes : List String := [
  "THM-M-1312.external-audit searched the required Choquet/Bruhat/Geroch, Einstein-equation, Lorentzian, global-hyperbolicity, development, Ricci/Einstein tensor, constraint-equation, and vacuum-Einstein terms against primary-source Lean repositories.",
  "The checked repo-local audit entries are recorded in AwesomeTheorems.Stage1.S1_M_168.externalLeanAuditEntries.",
  "mathlib4 at 8a178386ffc0f5fef0b77738bb5449d50efeea95 has adjacent manifold/ODE infrastructure but no terminal CBG, Lorentzian-causality, Ricci/Einstein tensor, constraint-equation, or maximal-development theorem.",
  "HEPLean/PhysLean at cd22b0c28882412447d12d5cfde677c4ad999994 has special-relativity Lorentz tensor API such as LorentzGroup, TensorSpecies.metricTensor, and Lorentz.Vector.minkowskiProduct_invariant, but no globally hyperbolic Einstein-development theorem.",
  "SNSFT/Substrate-Neutral-Structural-Foundation-Theory-SNSFT at a89e93fd07ad196e2e3b38b0252b81266cdf57e3 is not CBG evidence: its Einstein/Ricci hits are comments or project-specific reductions and it has no terminal theorem target.",
  "GitHub CLI authentication was unavailable in the child runtime, so authenticated rerun remains required before the public checklist item can be marked complete."
]

/-!
## Integration gate

`THM-M-1312.integration-gate` is a completion guard, not a proof branch.  It
records whether a terminal external Lean 4 Choquet-Bruhat-Geroch proof has
entered this repository's local Lake validation closure.
-/

/-- Machine-readable integration status for an external CBG proof candidate. -/
inductive CBGIntegrationGateStatus where
  | noTerminalExternalClosureFound
  | externalUpstreamPinnedImportedChecked
  | externalUpstreamAnchorOnly
  | externalIntegrationBlocked
  | localTerminalProofBody

namespace CBGIntegrationGateStatus

/-- Whether a status is enough for repo-local completion. -/
def repoLocalCompleted : CBGIntegrationGateStatus → Bool
  | noTerminalExternalClosureFound => false
  | externalUpstreamPinnedImportedChecked => true
  | externalUpstreamAnchorOnly => false
  | externalIntegrationBlocked => false
  | localTerminalProofBody => true

/-- Whether a status would retain forbidden completed-state integration debt. -/
def retainsRepoLocalIntegrationDebt : CBGIntegrationGateStatus → Bool
  | externalUpstreamAnchorOnly => true
  | noTerminalExternalClosureFound => false
  | externalUpstreamPinnedImportedChecked => false
  | externalIntegrationBlocked => false
  | localTerminalProofBody => false

end CBGIntegrationGateStatus

/-- One C006 integration-gate decision row. -/
structure CBGIntegrationGateRecord where
  candidate : String
  repository : String
  commit : String
  theoremName : String
  lakeClosureResult : String
  status : CBGIntegrationGateStatus
  blocker : String

/--
Current C006 gate records.

No terminal external Lean 4 closure for Choquet-Bruhat-Geroch was located in
the recorded audit rows, and no external proof has been pinned, imported, or
checked in this repository.  The authentication row is a public-completion
blocker for the external-audit rerun, not an anchor-only completion claim.
-/
def cbgIntegrationGateRecords : List CBGIntegrationGateRecord := [
  {
    candidate := "terminal Choquet-Bruhat-Geroch Lean 4 theorem"
    repository := "none found in recorded primary-source audit rows"
    commit := "none"
    theoremName := "none"
    lakeClosureResult :=
      "not applicable: no terminal external CBG proof candidate was located"
    status := CBGIntegrationGateStatus.noTerminalExternalClosureFound
    blocker :=
      "formalization_debt remains: build or import Lorentzian causality, Einstein-equation PDE, constraint, maximal-development, and uniqueness APIs; if a terminal external Lean 4 proof is later found, pin/import/check it or record a dependency/toolchain/license blocker"
  },
  {
    candidate := "authenticated global external Lean 4 search rerun"
    repository := "GitHub primary-source code search"
    commit := "not applicable"
    theoremName := "not applicable"
    lakeClosureResult :=
      "not applicable: gh auth status reported no GitHub login in the child runtime"
    status := CBGIntegrationGateStatus.externalIntegrationBlocked
    blocker :=
      "public completion requires authenticated rerun of the thirteen-term matrix before closing THM-M-1312.external-audit or upgrading the integration gate"
  }
]

/-- No local terminal CBG theorem has passed validation in this artifact. -/
def localTerminalCBGTheoremValidationPassed : Bool := false

/-- No pinned external terminal CBG proof has been imported and checked here. -/
def pinnedExternalTerminalCBGProofImportedAndChecked : Bool := false

/-- Anchor-only external CBG evidence is insufficient for completion. -/
def anchorOnlyExternalCBGEvidenceSufficientForCompletion : Bool := false

/--
Completion gate for `THM-M-1312.integration-gate`.

It can only be satisfied by a local terminal proof body or by a terminal
external proof that has been pinned, imported, and checked in this Lake closure.
-/
def CBGIntegrationGateSatisfied : Prop :=
  localTerminalCBGTheoremValidationPassed = true ∨
    pinnedExternalTerminalCBGProofImportedAndChecked = true

/-- The current C006 artifact does not satisfy the terminal integration gate. -/
theorem cbgIntegrationGate_not_satisfied : ¬ CBGIntegrationGateSatisfied := by
  intro h
  cases h with
  | inl hLocal => cases hLocal
  | inr hExternal => cases hExternal

/-- Checked certificate for the current C006 integration-gate statuses. -/
theorem cbgIntegrationGateRecords_statuses_eq :
    cbgIntegrationGateRecords.map (fun row => row.status) =
      [CBGIntegrationGateStatus.noTerminalExternalClosureFound,
        CBGIntegrationGateStatus.externalIntegrationBlocked] :=
  rfl

/-- Checked certificate that current C006 rows are not completion states. -/
theorem cbgIntegrationGateRecords_repoLocalCompleted_eq :
    cbgIntegrationGateRecords.map
        (fun row => row.status.repoLocalCompleted) = [false, false] :=
  rfl

/-- Checked certificate that current C006 rows retain no completed-state debt. -/
theorem cbgIntegrationGateRecords_no_repoLocalIntegrationDebt :
    cbgIntegrationGateRecords.map
        (fun row => row.status.retainsRepoLocalIntegrationDebt) =
      [false, false] :=
  rfl

/-- Checked policy fact: anchor-only external CBG evidence is insufficient. -/
theorem anchorOnlyExternalCBGEvidenceSufficientForCompletion_eq_false :
    anchorOnlyExternalCBGEvidenceSufficientForCompletion = false :=
  rfl

/-- Public backfill note for `THM-M-1312.integration-gate`. -/
def cbgIntegrationGatePublicBackfillNote : String :=
  "THM-M-1312.integration-gate remains open: no terminal external Lean 4 Choquet-Bruhat-Geroch closure was found in the recorded audit rows, no external proof has been pinned/imported/checked in this repository, and anchor-only evidence is explicitly insufficient for completion. Authenticated external search rerun remains required before any public completion claim."

/-!
## Missing formal API split

`THM-M-1312.missing-api` is a formalization-debt inventory, not a proof of the
Choquet-Bruhat-Geroch theorem.  The checked declarations below split the
currently missing formal surface into stable M0387-style leaves without adding
assumptions, unproved constants, or terminal theorem claims.
-/

/-- Canonical missing formal-API branches for the Choquet-Bruhat-Geroch theorem. -/
inductive ChoquetBruhatGerochMissingAPIBranch where
  | lorentzianMetric
  | causalGlobalHyperbolicity
  | curvatureRicciEinsteinTensors
  | initialDataConstraints
  | gaugeHyperbolicReduction
  | localQuasilinearHyperbolicPDEWellPosedness
  | developmentMorphisms
  | gluing
  | maximality
  | uniquenessUpToIsometry

namespace ChoquetBruhatGerochMissingAPIBranch

/-- Stable public task name for a missing formal-API branch. -/
def canonicalTaskName : ChoquetBruhatGerochMissingAPIBranch → String
  | lorentzianMetric =>
      "THM-M-1312.missing-api.lorentzian-metric"
  | causalGlobalHyperbolicity =>
      "THM-M-1312.missing-api.causal-global-hyperbolicity"
  | curvatureRicciEinsteinTensors =>
      "THM-M-1312.missing-api.curvature-ricci-einstein-tensors"
  | initialDataConstraints =>
      "THM-M-1312.missing-api.initial-data-constraints"
  | gaugeHyperbolicReduction =>
      "THM-M-1312.missing-api.gauge-hyperbolic-reduction"
  | localQuasilinearHyperbolicPDEWellPosedness =>
      "THM-M-1312.missing-api.local-quasilinear-hyperbolic-pde-well-posedness"
  | developmentMorphisms =>
      "THM-M-1312.missing-api.development-morphisms"
  | gluing =>
      "THM-M-1312.missing-api.gluing"
  | maximality =>
      "THM-M-1312.missing-api.maximality"
  | uniquenessUpToIsometry =>
      "THM-M-1312.missing-api.uniqueness-up-to-isometry"

/-- Human-readable description of a missing formal-API branch. -/
def description : ChoquetBruhatGerochMissingAPIBranch → String
  | lorentzianMetric =>
      "Define or import smooth Lorentzian metrics, signature conventions, time orientation, and compatibility with the manifold tangent-bundle API."
  | causalGlobalHyperbolicity =>
      "Define causal curves, chronological/causal futures and pasts, Cauchy hypersurfaces, and global hyperbolicity for Lorentzian spacetimes."
  | curvatureRicciEinsteinTensors =>
      "Define or import Levi-Civita connection, curvature, Ricci tensor, scalar curvature, Einstein tensor, and vacuum or matter Einstein equations."
  | initialDataConstraints =>
      "Define spacelike initial hypersurfaces, induced metric, second fundamental form, regularity assumptions, and the Einstein constraint equations."
  | gaugeHyperbolicReduction =>
      "Formalize a gauge choice, the reduced Einstein system, and the bridge from the reduced hyperbolic equations back to the geometric Einstein equations."
  | localQuasilinearHyperbolicPDEWellPosedness =>
      "Prove or import local existence, uniqueness, regularity, and stability for the relevant quasilinear hyperbolic PDE system."
  | developmentMorphisms =>
      "Define Cauchy developments and morphisms or isometric embeddings between developments that preserve the initial data."
  | gluing =>
      "Prove compatibility and gluing for chains or directed systems of developments while preserving the Cauchy and global-hyperbolicity predicates."
  | maximality =>
      "Construct a maximal globally hyperbolic development by the selected maximality principle and prove it satisfies the target development predicate."
  | uniquenessUpToIsometry =>
      "Prove uniqueness of maximal globally hyperbolic developments up to the appropriate initial-data-preserving isometry."

end ChoquetBruhatGerochMissingAPIBranch

/-- One M0387-style repo-local leaf for a missing Choquet-Bruhat-Geroch API family. -/
structure ChoquetBruhatGerochMissingAPILeaf where
  branch : ChoquetBruhatGerochMissingAPIBranch
  taskName : String
  description : String
  currentStatus : String
  debtClass : String
  repoLocalClosed : Bool
  leafBudgetBound : Nat

/--
Integration-ready split of `THM-M-1312.missing-api`.

Each leaf is currently unchecked formalization debt with a target local proof
budget of at most `100` steps after the relevant APIs exist.
-/
def choquetBruhatGerochMissingAPILeaves :
    List ChoquetBruhatGerochMissingAPILeaf := [
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.lorentzianMetric
    taskName := ChoquetBruhatGerochMissingAPIBranch.lorentzianMetric.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.lorentzianMetric.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.causalGlobalHyperbolicity
    taskName := ChoquetBruhatGerochMissingAPIBranch.causalGlobalHyperbolicity.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.causalGlobalHyperbolicity.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.curvatureRicciEinsteinTensors
    taskName := ChoquetBruhatGerochMissingAPIBranch.curvatureRicciEinsteinTensors.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.curvatureRicciEinsteinTensors.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.initialDataConstraints
    taskName := ChoquetBruhatGerochMissingAPIBranch.initialDataConstraints.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.initialDataConstraints.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.gaugeHyperbolicReduction
    taskName := ChoquetBruhatGerochMissingAPIBranch.gaugeHyperbolicReduction.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.gaugeHyperbolicReduction.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.localQuasilinearHyperbolicPDEWellPosedness
    taskName :=
      ChoquetBruhatGerochMissingAPIBranch.localQuasilinearHyperbolicPDEWellPosedness.canonicalTaskName
    description :=
      ChoquetBruhatGerochMissingAPIBranch.localQuasilinearHyperbolicPDEWellPosedness.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.developmentMorphisms
    taskName := ChoquetBruhatGerochMissingAPIBranch.developmentMorphisms.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.developmentMorphisms.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.gluing
    taskName := ChoquetBruhatGerochMissingAPIBranch.gluing.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.gluing.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.maximality
    taskName := ChoquetBruhatGerochMissingAPIBranch.maximality.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.maximality.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  },
  {
    branch := ChoquetBruhatGerochMissingAPIBranch.uniquenessUpToIsometry
    taskName := ChoquetBruhatGerochMissingAPIBranch.uniquenessUpToIsometry.canonicalTaskName
    description := ChoquetBruhatGerochMissingAPIBranch.uniquenessUpToIsometry.description
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
    leafBudgetBound := 100
  }
]

/-- The missing formal-API split has exactly the ten requested leaves. -/
theorem choquetBruhatGerochMissingAPILeaves_length :
    choquetBruhatGerochMissingAPILeaves.length = 10 :=
  rfl

/-- The missing formal-API split records the requested branches in public order. -/
theorem choquetBruhatGerochMissingAPILeaves_branches_eq :
    choquetBruhatGerochMissingAPILeaves.map
        (fun leaf => leaf.branch) = [
      ChoquetBruhatGerochMissingAPIBranch.lorentzianMetric,
      ChoquetBruhatGerochMissingAPIBranch.causalGlobalHyperbolicity,
      ChoquetBruhatGerochMissingAPIBranch.curvatureRicciEinsteinTensors,
      ChoquetBruhatGerochMissingAPIBranch.initialDataConstraints,
      ChoquetBruhatGerochMissingAPIBranch.gaugeHyperbolicReduction,
      ChoquetBruhatGerochMissingAPIBranch.localQuasilinearHyperbolicPDEWellPosedness,
      ChoquetBruhatGerochMissingAPIBranch.developmentMorphisms,
      ChoquetBruhatGerochMissingAPIBranch.gluing,
      ChoquetBruhatGerochMissingAPIBranch.maximality,
      ChoquetBruhatGerochMissingAPIBranch.uniquenessUpToIsometry
    ] :=
  rfl

/-- No missing formal-API leaf is repo-locally closed by this Stage1 scaffold. -/
theorem choquetBruhatGerochMissingAPILeaves_repoLocalClosed_eq :
    choquetBruhatGerochMissingAPILeaves.map
        (fun leaf => leaf.repoLocalClosed) =
      [false, false, false, false, false, false, false, false, false, false] :=
  rfl

/-- Each missing formal-API leaf keeps the M0387 local expansion budget at `100`. -/
theorem choquetBruhatGerochMissingAPILeaves_budget_eq :
    choquetBruhatGerochMissingAPILeaves.map
        (fun leaf => leaf.leafBudgetBound) =
      [100, 100, 100, 100, 100, 100, 100, 100, 100, 100] :=
  rfl

/-- Each missing formal-API leaf remains unchecked formalization debt. -/
theorem choquetBruhatGerochMissingAPILeaves_statusDebt_eq :
    choquetBruhatGerochMissingAPILeaves.map
        (fun leaf => (leaf.currentStatus, leaf.debtClass)) = [
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt"),
      ("unchecked", "formalization_debt")
    ] :=
  rfl

/-- Integration-ready public missing-API note for `THM-M-1312.missing-api`. -/
def choquetBruhatGerochMissingAPIPublicBackfillNotes : List String := [
  "THM-M-1312.missing-api is split into ten repo-local leaves recorded by AwesomeTheorems.Stage1.S1_M_168.ChoquetBruhatGerochMissingAPIBranch and choquetBruhatGerochMissingAPILeaves.",
  "The ten leaves are Lorentzian metric; causal/global-hyperbolicity theory; curvature/Ricci/Einstein tensors; initial-data constraints; gauge/hyperbolic reduction; local quasilinear hyperbolic PDE well-posedness; development morphisms; gluing; maximality; and uniqueness up to isometry.",
  "The checked guards choquetBruhatGerochMissingAPILeaves_length, choquetBruhatGerochMissingAPILeaves_repoLocalClosed_eq, and choquetBruhatGerochMissingAPILeaves_statusDebt_eq record that this is an unchecked formalization-debt inventory, not terminal Choquet-Bruhat-Geroch completion."
]

end S1_M_168
end Stage1
end AwesomeTheorems
