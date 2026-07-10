import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.Complex.Harmonic.Poisson
import Mathlib.Analysis.Complex.Harmonic.MeanValue
import Mathlib.Analysis.Complex.Poisson
import Mathlib.Analysis.InnerProductSpace.Harmonic.HarmonicContOnCl
import Mathlib.Analysis.Distribution.DerivNotation
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# S1-M-144 / THM-M-1154: regular boundary points for the Dirichlet problem

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
the classical potential-theoretic theorem that regular boundary points support
existence and boundary convergence for the Dirichlet problem.

The pinned mathlib snapshot has useful adjacent planar harmonic-function
infrastructure: harmonicity via the Laplacian, continuity of harmonic functions,
the mean-value property, and the Poisson integral formula on disks.  This file
does not claim a terminal Perron/barrier proof or a full Dirichlet existence
theorem for arbitrary domains.
-/

noncomputable section

open InnerProductSpace Metric Real Set Topology
open scoped Distributions

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_144

/--
Boundary regularity datum for a point of a planar domain.

The two final fields are deliberately proposition-valued boundaries.  A terminal
formalization should replace them by the chosen Lean definitions of barriers,
Perron families, harmonic measure, or an equivalent potential-theoretic API.
-/
structure RegularBoundaryPointData (Ω : Set ℂ) (x : ℂ) : Type where
  isBoundaryPoint : x ∈ frontier Ω
  hasBarrier : Prop
  perronConvergesToBoundaryValue : Prop

/--
Data expected of a solution to the classical Dirichlet problem on a planar
domain with boundary data `g`.

The statement uses `HarmonicOnNhd` from mathlib as the currently checked
harmonic substrate and keeps the boundary condition as equality on
`frontier Ω`.  Stronger variants may replace this by filter convergence from
inside the domain at every regular boundary point.
-/
structure DirichletSolutionData (Ω : Set ℂ) (g u : ℂ → ℝ) : Prop where
  harmonicOnDomain : HarmonicOnNhd u Ω
  continuousOnClosure : ContinuousOn u (closure Ω)
  boundaryEq : EqOn u g (frontier Ω)

/--
Public statement-normalization note for `StatementShape`.

This is a statement-shape boundary for THM-M-1154, not a proof of the
Dirichlet problem.  It fixes the current Lean-side surface as: an admissible
open planar domain whose boundary points are packaged by
`RegularBoundaryPointData` should provide, for each continuous real boundary
datum, a harmonic function on the domain that is continuous on the closure and
agrees with the datum on the frontier.

The placeholders inside `RegularBoundaryPointData` and `admissibleDomain`
must be replaced by chosen potential-theoretic definitions, and a terminal
proof must come from a local proof body, a pinned mathlib wrapper, or a pinned
external dependency before the Dirichlet theorem can be marked complete.
-/
def statementShapeNormalizationNote : String :=
  "THM-M-1154 statement-shape boundary: \
  AwesomeTheorems.Stage1.S1_M_144.StatementShape records the current \
  normalized Lean target for regular boundary points and the Dirichlet \
  problem. It is not a proof of Dirichlet solvability; admissibility, regular \
  boundary point definitions, Perron/barrier machinery, and the terminal \
  existence proof remain formalization debt."

/--
Normalized Stage1 statement-shape candidate for THM-M-1154.

If `Ω` is an admissible open planar domain and every boundary point is regular,
then every continuous real boundary datum has a harmonic solution continuous up
to the closure and agreeing with the boundary datum on the boundary.  The
`admissibleDomain` predicate packages the classical side conditions left open by
this Stage1 pass, such as boundedness, nonempty interior, compact boundary,
barrier hypotheses, and the exact Perron-method setup.
-/
def StatementShape : Prop :=
  ∀ (Ω : Set ℂ),
    IsOpen Ω →
      (admissibleDomain : Prop) →
        admissibleDomain →
          (∀ x : ℂ, x ∈ frontier Ω → Nonempty (RegularBoundaryPointData Ω x)) →
            ∀ g : ℂ → ℝ,
              ContinuousOn g (frontier Ω) →
                ∃ u : ℂ → ℝ, DirichletSolutionData Ω g u

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Set ℂ),
      IsOpen Ω →
        (admissibleDomain : Prop) →
          admissibleDomain →
            (∀ x : ℂ, x ∈ frontier Ω → Nonempty (RegularBoundaryPointData Ω x)) →
              ∀ g : ℂ → ℝ,
                ContinuousOn g (frontier Ω) →
                  ∃ u : ℂ → ℝ, DirichletSolutionData Ω g u) :
    StatementShape :=
  h

/-- A Dirichlet solution datum exposes the checked mathlib harmonic predicate. -/
theorem DirichletSolutionData.harmonic
    {Ω : Set ℂ} {g u : ℂ → ℝ} (S : DirichletSolutionData Ω g u) :
    HarmonicOnNhd u Ω :=
  S.harmonicOnDomain

/-- A Dirichlet solution datum exposes continuity on the domain closure. -/
theorem DirichletSolutionData.continuous_on_closure
    {Ω : Set ℂ} {g u : ℂ → ℝ} (S : DirichletSolutionData Ω g u) :
    ContinuousOn u (closure Ω) :=
  S.continuousOnClosure

/-- A Dirichlet solution datum exposes the boundary trace equation. -/
theorem DirichletSolutionData.boundary_eq
    {Ω : Set ℂ} {g u : ℂ → ℝ} (S : DirichletSolutionData Ω g u) :
    EqOn u g (frontier Ω) :=
  S.boundaryEq

/-- Checked mathlib anchor: constant functions are harmonic on any set. -/
theorem harmonicOnNhd_const_anchor (Ω : Set ℂ) (c : ℝ) :
    HarmonicOnNhd (fun _ : ℂ => c) Ω :=
  harmonicOnNhd_const c

/-- Checked mathlib anchor: harmonic functions are continuous on their domain. -/
theorem harmonicOnNhd_continuousOn_anchor
    {Ω : Set ℂ} {u : ℂ → ℝ} (hu : HarmonicOnNhd u Ω) :
    ContinuousOn u Ω :=
  hu.continuousOn

/-- Checked mathlib anchor: the planar harmonic mean-value theorem on closed disks. -/
theorem harmonic_meanValue_closedDisk_anchor
    {u : ℂ → ℝ} {c : ℂ} {R : ℝ}
    (hu : HarmonicOnNhd u (closedBall c |R|)) :
    circleAverage u c R = u c :=
  HarmonicOnNhd.circleAverage_eq hu

/-- Checked mathlib anchor: the Poisson kernel formula for harmonic functions on disks. -/
theorem harmonic_poissonKernel_closedDisk_anchor
    {u : ℂ → ℝ} {c w : ℂ} {R : ℝ}
    (hu : HarmonicOnNhd u (closedBall c R)) (hw : w ∈ ball c R) :
    circleAverage (poissonKernel c w • u) c R = u w :=
  HarmonicOnNhd.circleAverage_poissonKernel_smul hu hw

/-- Checked mathlib anchor: the Poisson-kernel formula unfolds definitionally. -/
theorem poissonKernel_def_anchor (c w z : ℂ) :
    poissonKernel c w z =
      (‖z - c‖ ^ 2 - ‖w - c‖ ^ 2) / ‖(z - c) - (w - c)‖ ^ 2 :=
  poissonKernel_def c w z

/-! ## Disk/ball Dirichlet special-case child task -/

/--
Statement-shape target for the disk/ball Dirichlet special case requested by
`THM-M-1154.disk_special_case`.

For a disk `ball c R`, this asks for a harmonic function on the disk,
continuous on the closed disk, whose boundary trace agrees with continuous
boundary data on `sphere c R`, and whose interior values are controlled by the
Poisson-kernel circle average.  This is still only a formal target: it records
the special case that should be proved before arbitrary-domain regular boundary
points are attempted.
-/
def DiskBallDirichletSpecialCaseShape : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R →
      ∀ g : ℂ → ℝ,
        ContinuousOn g (sphere c R) →
          ∃ u : ℂ → ℝ,
            HarmonicOnNhd u (ball c R) ∧
              ContinuousOn u (closedBall c R) ∧
                EqOn u g (sphere c R) ∧
                  ∀ w : ℂ,
                    w ∈ ball c R →
                      circleAverage (poissonKernel c w • g) c R = u w

/-- Low-risk introduction wrapper for the disk/ball special-case target. -/
theorem DiskBallDirichletSpecialCaseShape.intro
    (h : ∀ (c : ℂ) (R : ℝ),
      0 < R →
        ∀ g : ℂ → ℝ,
          ContinuousOn g (sphere c R) →
            ∃ u : ℂ → ℝ,
              HarmonicOnNhd u (ball c R) ∧
                ContinuousOn u (closedBall c R) ∧
                  EqOn u g (sphere c R) ∧
                    ∀ w : ℂ,
                      w ∈ ball c R →
                        circleAverage (poissonKernel c w • g) c R = u w) :
    DiskBallDirichletSpecialCaseShape :=
  h

/-- Poisson-kernel anchors that the disk/ball special-case child must use. -/
def diskBallDirichletPoissonAnchorNames : List String := [
  "harmonic_poissonKernel_closedDisk_anchor",
  "poissonKernel_def_anchor",
  "harmonic_meanValue_closedDisk_anchor",
  "Mathlib.Analysis.Complex.Harmonic.Poisson",
  "Mathlib.Analysis.Complex.Poisson"
]

/-- Integration-ready public child task text for the disk/ball special case. -/
def diskBallDirichletPublicChildTaskText : String :=
  "Create a public child task `THM-M-1154.disk_ball_dirichlet_poisson` \
  proving the disk/ball Dirichlet special case before arbitrary-domain regular \
  boundary points: for `0 < R` and continuous boundary data on `sphere c R`, \
  construct the Poisson-integral solution on `ball c R`, prove harmonicity on \
  the disk, continuity on `closedBall c R`, the boundary trace equation, and \
  the Poisson-kernel value formula. Use the checked anchors \
  `harmonic_poissonKernel_closedDisk_anchor`, `poissonKernel_def_anchor`, and \
  `harmonic_meanValue_closedDisk_anchor`. Keep THM-M-1154 open until this \
  branch has a local proof body, checked mathlib wrapper, or pinned external \
  dependency and all M0387 gates are satisfied."

/-- M0387-level child leaves for the disk/ball Dirichlet Poisson branch. -/
def diskBallDirichletChildLeaves : List String := [
  "M1154-DISK-L001: choose the boundary model as `sphere c R` for `0 < R` and connect it to `frontier (ball c R)` if the terminal statement uses frontier",
  "M1154-DISK-L002: define the Poisson-integral candidate from continuous boundary data using pinned mathlib circle-average/Poisson APIs",
  "M1154-DISK-L003: prove harmonicity of the Poisson-integral candidate on `ball c R`",
  "M1154-DISK-L004: prove continuity on `closedBall c R` and the boundary trace limit/equality on `sphere c R`",
  "M1154-DISK-L005: expose a wrapper theorem matching `DiskBallDirichletSpecialCaseShape` and validate it repo-locally",
  "M1154-DISK-L006: only after L001-L005 validate, decide how this disk/ball branch feeds the arbitrary-domain regular-boundary proof tree"
]

/--
Gate result for child `S1-M-144-C003`.

This file supplies checked anchors and an integration-ready child-task target.
It does not contain a terminal disk Dirichlet proof, and it does not complete
THM-M-1154.
-/
structure DiskBallDirichletChildGate where
  childId : String
  publicDocIntegrationRequired : Bool
  repoLocalPoissonAnchorsChecked : Bool
  terminalDiskDirichletProofInRepo : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for `S1-M-144-C003`. -/
def diskBallDirichletChildGate : DiskBallDirichletChildGate where
  childId := "S1-M-144-C003"
  publicDocIntegrationRequired := true
  repoLocalPoissonAnchorsChecked := true
  terminalDiskDirichletProofInRepo := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt := "formalization_debt / not_repo_local_closed"

/-- C003 records checked Poisson anchors for the public child task. -/
theorem diskBallDirichletChildGate_anchorsChecked :
    diskBallDirichletChildGate.repoLocalPoissonAnchorsChecked = true :=
  rfl

/-- C003 does not claim a terminal disk/ball Dirichlet proof. -/
theorem diskBallDirichletChildGate_noTerminalProof :
    diskBallDirichletChildGate.terminalDiskDirichletProofInRepo = false :=
  rfl

/-- C003 keeps THM-M-1154 below completion. -/
theorem diskBallDirichletChildGate_noCompletionClaim :
    diskBallDirichletChildGate.completionClaimAllowed = false :=
  rfl

/-- C003 leaves no completed state carrying repo-local integration debt. -/
theorem diskBallDirichletChildGate_noCompletedRepoLocalIntegrationDebt :
    diskBallDirichletChildGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## Regular-boundary definition choice child task -/

/--
Candidate families for defining a regular boundary point in Lean.

For this Stage1 slot the selected surface is `barrierBased`: a boundary point is
regular when it carries a positive potential-theoretic barrier.  The Perron,
harmonic-measure, and weak-solution/trace formulations are recorded as
deferred bridges, not as the canonical definition for the current Lean file.
-/
inductive RegularBoundaryDefinitionMethod where
  | barrierBased
  | perronResolutive
  | harmonicMeasureBased
  | weakSolutionTraceBased
deriving DecidableEq, Repr

/--
Barrier data chosen as the canonical repo-local definition boundary for
regular boundary points.

Mathlib at the audited snapshot supplies harmonic functions and Poisson kernels
but not a terminal superharmonic/barrier API.  The fields below therefore make
the topological and positive-function parts concrete while leaving the
superharmonic and fine boundary-limit requirements as proposition-valued
obligations to be replaced by a future potential-theory API.
-/
structure BoundaryBarrierData (Ω : Set ℂ) (x : ℂ) : Type where
  isBoundaryPoint : x ∈ frontier Ω
  barrier : ℂ → ℝ
  positiveOnDomain : ∀ y : ℂ, y ∈ Ω → 0 < barrier y
  tendsToZeroAtBoundaryPoint : Prop
  separatesOtherBoundaryPoints : Prop
  superharmonicOnDomain : Prop

/-- Barrier-based regularity is the selected Lean definition for this slot. -/
def BarrierBasedRegularBoundaryPoint (Ω : Set ℂ) (x : ℂ) : Prop :=
  Nonempty (BoundaryBarrierData Ω x)

/--
Chosen regular-boundary-point predicate for THM-M-1154.

This is intentionally barrier-based rather than Perron-resolutive,
harmonic-measure-based, or weak-solution/trace-based.  Later work may prove
equivalence theorems between these notions, but this Stage1 child fixes the
canonical definition boundary as `BarrierBasedRegularBoundaryPoint`.
-/
def RegularBoundaryPoint (Ω : Set ℂ) (x : ℂ) : Prop :=
  BarrierBasedRegularBoundaryPoint Ω x

/-- Machine-readable record of the chosen regular-boundary definition method. -/
def regularBoundaryDefinitionChoice : RegularBoundaryDefinitionMethod :=
  RegularBoundaryDefinitionMethod.barrierBased

/-- Human-readable summary of the regular-boundary definition decision. -/
def regularBoundaryDefinitionChoiceNote : String :=
  "THM-M-1154 regular boundary point definition choice: use a barrier-based \
  predicate as the canonical Lean boundary. A point `x ∈ frontier Ω` is regular \
  when it has `BoundaryBarrierData Ω x`. Perron-resolutive, harmonic-measure, \
  and weak-solution/trace formulations are deferred bridge theorems, not the \
  selected definition in this Stage1 artifact."

/-- Definition methods that remain bridge targets after the barrier choice. -/
def deferredRegularBoundaryDefinitionMethods : List RegularBoundaryDefinitionMethod := [
  RegularBoundaryDefinitionMethod.perronResolutive,
  RegularBoundaryDefinitionMethod.harmonicMeasureBased,
  RegularBoundaryDefinitionMethod.weakSolutionTraceBased
]

/-- A chosen regular boundary point is, in particular, a frontier point. -/
theorem RegularBoundaryPoint.mem_frontier
    {Ω : Set ℂ} {x : ℂ} (h : RegularBoundaryPoint Ω x) :
    x ∈ frontier Ω := by
  rcases h with ⟨B⟩
  exact B.isBoundaryPoint

/-- A chosen regular boundary point exposes its barrier witness. -/
theorem RegularBoundaryPoint.exists_barrierData
    {Ω : Set ℂ} {x : ℂ} (h : RegularBoundaryPoint Ω x) :
    ∃ _ : BoundaryBarrierData Ω x, True := by
  rcases h with ⟨B⟩
  exact ⟨B, trivial⟩

/-- M0387-level child leaves forced by the barrier-definition choice. -/
def regularBoundaryDefinitionChildLeaves : List String := [
  "M1154-REGDEF-L001: replace `BoundaryBarrierData.superharmonicOnDomain` by a concrete superharmonic or subharmonic API once one is available or imported",
  "M1154-REGDEF-L002: replace `BoundaryBarrierData.tendsToZeroAtBoundaryPoint` by a filter statement for approach to `x` from inside `Ω`",
  "M1154-REGDEF-L003: replace `BoundaryBarrierData.separatesOtherBoundaryPoints` by a quantitative lower-bound or liminf condition away from `x`",
  "M1154-REGDEF-L004: prove or pin the theorem that barrier-based regularity implies Perron boundary convergence for continuous boundary data",
  "M1154-REGDEF-L005: only after L001-L004 validate, bridge `RegularBoundaryPoint` into the terminal Dirichlet statement shape"
]

/--
Gate result for child `S1-M-144-C004`.

This child chooses and records a barrier-based definition boundary.  It does not
prove barrier equivalence with Perron regularity, harmonic measure, or weak
trace regularity, and it does not complete THM-M-1154.
-/
structure RegularBoundaryDefinitionChildGate where
  childId : String
  chosenMethod : RegularBoundaryDefinitionMethod
  publicDocIntegrationRequired : Bool
  terminalPotentialTheoryAPIInRepo : Bool
  terminalDirichletProofInRepo : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for `S1-M-144-C004`. -/
def regularBoundaryDefinitionChildGate : RegularBoundaryDefinitionChildGate where
  childId := "S1-M-144-C004"
  chosenMethod := regularBoundaryDefinitionChoice
  publicDocIntegrationRequired := true
  terminalPotentialTheoryAPIInRepo := false
  terminalDirichletProofInRepo := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt := "formalization_debt / not_repo_local_closed"

/-- C004 selected the barrier-based definition method. -/
theorem regularBoundaryDefinitionChildGate_chosenBarrier :
    regularBoundaryDefinitionChildGate.chosenMethod =
      RegularBoundaryDefinitionMethod.barrierBased :=
  rfl

/-- C004 does not claim a terminal potential-theory API in this repository. -/
theorem regularBoundaryDefinitionChildGate_noTerminalPotentialTheoryAPI :
    regularBoundaryDefinitionChildGate.terminalPotentialTheoryAPIInRepo = false :=
  rfl

/-- C004 keeps THM-M-1154 below completion. -/
theorem regularBoundaryDefinitionChildGate_noCompletionClaim :
    regularBoundaryDefinitionChildGate.completionClaimAllowed = false :=
  rfl

/-- C004 leaves no completed state carrying repo-local integration debt. -/
theorem regularBoundaryDefinitionChildGate_noCompletedRepoLocalIntegrationDebt :
    regularBoundaryDefinitionChildGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-- Repo-pinned mathlib revision used for the THM-M-1154 mathlib audit. -/
def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact module surface requested by the THM-M-1154 mathlib-audit child task. -/
def mathlibAuditCheckedModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.Harmonic.Basic",
  "Mathlib.Analysis.Complex.Harmonic.MeanValue",
  "Mathlib.Analysis.Complex.Harmonic.Poisson",
  "Mathlib.Analysis.Complex.Poisson"
]

/-- mathlib modules checked while locating repo-local Dirichlet-problem anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.Analysis.InnerProductSpace.Harmonic.Basic",
  "Mathlib.Analysis.InnerProductSpace.Harmonic.HarmonicContOnCl",
  "Mathlib.Analysis.Complex.Harmonic.MeanValue",
  "Mathlib.Analysis.Complex.Harmonic.Poisson",
  "Mathlib.Analysis.Complex.Poisson",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.Distribution"
]

/-- Search terms that did not locate a terminal regular-boundary Dirichlet theorem. -/
def absentTerminalSearchTerms : List String := [
  "Dirichlet problem",
  "regular boundary point",
  "RegularBoundaryPoint",
  "Perron",
  "barrier",
  "harmonic measure",
  "Poisson problem",
  "Laplace equation boundary value",
  "weak solution Dirichlet",
  "Sobolev trace"
]

/-! ## External Lean 4 primary-source audit -/

/-- Status for one external Lean 4 source-search probe. -/
inductive ExternalLeanAuditSearchStatus where
  | authenticatedSearchBlocked
  | unauthenticatedFallbackNoTerminalProof
  | localPinnedSourceNoTerminalProof
deriving DecidableEq, Repr

/-- One concrete source-search probe for `THM-M-1154.external_audit`. -/
structure ExternalLeanAuditSearchItem where
  status : ExternalLeanAuditSearchStatus
  surface : String
  query : String
  result : String
deriving Repr

/-- Required C006 search terms for terminal Lean 4 proof discovery. -/
def externalAuditRequiredSearchTerms : List String := [
  "RegularBoundaryPoint",
  "Dirichlet problem",
  "Perron",
  "barrier",
  "harmonic measure",
  "Poisson kernel"
]

/--
Source-search probes rerun for child `S1-M-144-C006`.

The GitHub CLI and GitHub REST code-search attempts show an authentication
blocker in this environment, so this child records the blocker instead of
upgrading the theorem from fallback evidence.  The local pinned mathlib source
search found only auxiliary Poisson/Perron-integration hits, not a terminal
regular-boundary Dirichlet theorem.
-/
def externalLeanAuditSearchItems : List ExternalLeanAuditSearchItem := [
  {
    status := ExternalLeanAuditSearchStatus.authenticatedSearchBlocked,
    surface := "GitHub CLI",
    query := "gh auth status",
    result := "blocked: gh is installed, but no GitHub host is logged in"
  },
  {
    status := ExternalLeanAuditSearchStatus.authenticatedSearchBlocked,
    surface := "GitHub REST code search",
    query := "\"RegularBoundaryPoint\" language:Lean; \"Dirichlet problem\" lean-toolchain",
    result := "blocked: unauthenticated code search returned HTTP 403 and no GH_TOKEN/GITHUB_TOKEN was available"
  },
  {
    status := ExternalLeanAuditSearchStatus.localPinnedSourceNoTerminalProof,
    surface := "Pinned local mathlib source",
    query := "Dirichlet problem | regular boundary point | RegularBoundaryPoint | Perron | barrier | harmonic measure | Poisson kernel",
    result := "no terminal regular-boundary Dirichlet theorem found; hits are Poisson-kernel anchors or unrelated Perron-integration/Frobenius text"
  },
  {
    status := ExternalLeanAuditSearchStatus.unauthenticatedFallbackNoTerminalProof,
    surface := "Web search fallback",
    query := "site:github.com Lean 4 searches for RegularBoundaryPoint, Dirichlet problem, Perron, barrier, harmonic measure, and Poisson kernel",
    result := "no pin-ready terminal Lean 4 proof was identified; fallback evidence is not an authenticated completion gate"
  }
]

/-- Human-readable C006 audit summary. -/
def externalLeanAuditNote : String :=
  "THM-M-1154 external_audit C006: authenticated GitHub source search is \
  blocked in this environment because `gh auth status` reports no logged-in \
  GitHub host, GitHub REST code search returns HTTP 403 without a token, and \
  no GH_TOKEN/GITHUB_TOKEN is available. Fallback local pinned mathlib source \
  search and web search did not identify a terminal Lean 4 proof of the \
  regular-boundary-point Dirichlet theorem. No external proof was pinned, \
  imported, or checked; THM-M-1154 remains not_repo_local_closed."

/--
Gate result for child `S1-M-144-C006`.

This child is an external-anchor audit with an authentication blocker.  It does
not complete the theorem and it does not leave an anchor-only external proof in
a completed state.
-/
structure ExternalLeanAuditChildGate where
  childId : String
  authenticatedGithubSearchAvailable : Bool
  authenticatedPrimarySourceSearchCompleted : Bool
  unauthenticatedFallbacksRun : Bool
  terminalExternalLeanProofFound : Bool
  terminalExternalLeanProofPinnedAndChecked : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for `S1-M-144-C006`. -/
def externalLeanAuditChildGate : ExternalLeanAuditChildGate where
  childId := "S1-M-144-C006"
  authenticatedGithubSearchAvailable := false
  authenticatedPrimarySourceSearchCompleted := false
  unauthenticatedFallbacksRun := true
  terminalExternalLeanProofFound := false
  terminalExternalLeanProofPinnedAndChecked := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt := "formalization_debt / not_repo_local_closed; authenticated external search blocker"

/-- C006 records that authenticated GitHub source search was unavailable. -/
theorem externalLeanAuditChildGate_noAuthenticatedGithubSearch :
    externalLeanAuditChildGate.authenticatedGithubSearchAvailable = false :=
  rfl

/-- C006 records that no terminal external Lean proof was found. -/
theorem externalLeanAuditChildGate_noTerminalExternalProof :
    externalLeanAuditChildGate.terminalExternalLeanProofFound = false :=
  rfl

/-- C006 records that no external proof was pinned and checked. -/
theorem externalLeanAuditChildGate_noPinnedExternalProof :
    externalLeanAuditChildGate.terminalExternalLeanProofPinnedAndChecked = false :=
  rfl

/-- C006 keeps THM-M-1154 below completion. -/
theorem externalLeanAuditChildGate_noCompletionClaim :
    externalLeanAuditChildGate.completionClaimAllowed = false :=
  rfl

/-- C006 leaves no completed state carrying repo-local integration debt. -/
theorem externalLeanAuditChildGate_noCompletedRepoLocalIntegrationDebt :
    externalLeanAuditChildGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## Weak Dirichlet bridge audit -/

/-- Status class used by the weak Dirichlet bridge API audit. -/
inductive WeakDirichletBridgeApiStatus where
  | availableRepoLocalAnchor
  | adjacentButNotSufficient
  | missingBlockingApi
deriving DecidableEq, Repr

/-- One audited API item for the weak Dirichlet formulation branch. -/
structure WeakDirichletBridgeApiItem where
  status : WeakDirichletBridgeApiStatus
  name : String
  diagnosis : String
deriving Repr

/--
Checked repo-local anchors relevant to a weak Dirichlet formulation.

These declarations elaborate at the audited mathlib snapshot, but they do not
yet assemble a weak Dirichlet problem on a bounded domain.
-/
def weakDirichletBridgeAvailableApiItems : List WeakDirichletBridgeApiItem := [
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "MeasureTheory.MemLp",
    diagnosis := "Lp membership predicate for measurable functions is available."
  },
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "MeasureTheory.eLpNorm",
    diagnosis := "Lp seminorm/norm infrastructure is available."
  },
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one",
    diagnosis := "Gagliardo-Nirenberg-Sobolev inequality for compactly supported C1 functions is available."
  },
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
    diagnosis := "Finite-dimensional GNS estimate using classical Frechet derivatives is available."
  },
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "TestFunction",
    diagnosis := "Bundled compactly supported smooth/Cn test functions on open sets are available."
  },
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "TestFunction.fderivCLM",
    diagnosis := "Continuous linear Frechet derivative map for test functions is available."
  },
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "Distribution",
    diagnosis := "Distributions on open sets as continuous linear maps on test functions are available."
  },
  {
    status := WeakDirichletBridgeApiStatus.availableRepoLocalAnchor,
    name := "Distribution.mapCLM",
    diagnosis := "Continuous linear postcomposition for distribution values is available."
  },
  {
    status := WeakDirichletBridgeApiStatus.adjacentButNotSufficient,
    name := "LineDeriv / Laplacian notation classes",
    diagnosis := "Derivative and Laplacian notation classes exist, but DerivNotation says future uses include distributions and Sobolev spaces."
  }
]

/--
Adjacent distributional APIs found outside the domain-distribution weak
Dirichlet surface.

These are useful signposts, but they are not enough for `W^{1,2}` Dirichlet
data on an arbitrary planar domain because they concern Schwartz or tempered
distributions on whole spaces rather than Sobolev functions with boundary trace
on `frontier Ω`.
-/
def weakDirichletBridgeAdjacentNonDomainApis : List String := [
  "SchwartzMap.fderivCLM",
  "SchwartzMap.lineDerivOp_apply_eq_fderiv",
  "SchwartzMap.integral_bilinear_lineDerivOp_right_eq_neg_left",
  "SchwartzMap.integral_bilinear_laplacian_right_eq_left",
  "TemperedDistribution.instLineDeriv",
  "TemperedDistribution.laplacian_apply_apply",
  "TemperedDistribution.lineDerivOp_apply_apply",
  "TemperedDistribution.laplacian_toTemperedDistributionCLM_eq"
]

/--
Blocking missing APIs for a weak Dirichlet formulation of THM-M-1154.

This list is intentionally concrete: each item names the absent formal surface
that must exist before the weak-solution/trace route can replace the current
barrier-based statement boundary.
-/
def weakDirichletBridgeMissingApiItems : List WeakDirichletBridgeApiItem := [
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "SobolevSpace / MemSobolev on domains",
    diagnosis := "No bundled W^{1,p}, H1, H1_0, or domain-restricted Sobolev membership API was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "WeakDerivative for functions on Opens",
    diagnosis := "No predicate relating a locally integrable function to its distributional weak derivative on an open set was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "Distribution.lineDeriv on domain distributions",
    diagnosis := "Domain distributions exist, but no directional derivative/laplacian operator on 𝓓'(Ω,F) was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "SobolevTrace",
    diagnosis := "No boundary trace operator from W^{1,p}(Ω) or H1(Ω) to an Lp space on frontier Ω was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "ZeroTrace / H1_0",
    diagnosis := "No zero-trace subspace or closure of compactly supported smooth functions in a Sobolev norm was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "WeakHarmonicOn / WeakLaplaceEq",
    diagnosis := "No weak harmonic predicate such as integral grad u dot grad phi = 0 for all test functions was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "WeakDirichletSolution",
    diagnosis := "No structure combining Sobolev membership, weak Laplace equation, and boundary trace equal to g was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "Green identity / integration by parts on domains with boundary",
    diagnosis := "No domain Green formula connecting weak gradients, Laplacian, and boundary trace on frontier Ω was found."
  },
  {
    status := WeakDirichletBridgeApiStatus.missingBlockingApi,
    name := "RegularBoundaryPoint weak-trace bridge",
    diagnosis := "No theorem connecting the selected barrier-based regular boundary predicate to weak trace or boundary convergence was found."
  }
]

/-- Human-readable audit summary for `THM-M-1154.weak_bridge`. -/
def weakDirichletBridgeAuditNote : String :=
  "THM-M-1154 weak_bridge audit: mathlib provides Lp/eLpNorm, GNS \
  estimates for compactly supported C1 functions, test functions on open sets, \
  and distributions on open sets. The weak Dirichlet route is blocked by \
  missing domain Sobolev spaces, weak derivative predicates, derivative or \
  Laplacian operators on domain distributions, Sobolev trace/zero-trace APIs, \
  weak harmonic/Dirichlet solution predicates, Green identities on domains \
  with boundary, and a bridge from barrier regularity to weak trace data."

/--
Gate result for child `S1-M-144-C005`.

This child is an API audit and formalization-debt inventory.  It records
available local anchors and the precise missing weak-formulation APIs, but it
does not complete a weak Dirichlet theorem.
-/
structure WeakDirichletBridgeChildGate where
  childId : String
  distributionOnOpenSetsAvailable : Bool
  sobolevDomainApiAvailable : Bool
  boundaryTraceApiAvailable : Bool
  weakDirichletSolutionApiAvailable : Bool
  terminalWeakDirichletProofInRepo : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String

/-- Machine-readable result for `S1-M-144-C005`. -/
def weakDirichletBridgeChildGate : WeakDirichletBridgeChildGate where
  childId := "S1-M-144-C005"
  distributionOnOpenSetsAvailable := true
  sobolevDomainApiAvailable := false
  boundaryTraceApiAvailable := false
  weakDirichletSolutionApiAvailable := false
  terminalWeakDirichletProofInRepo := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt := "formalization_debt / not_repo_local_closed"

/-- C005 records that domain distributions are available. -/
theorem weakDirichletBridgeChildGate_distributionAvailable :
    weakDirichletBridgeChildGate.distributionOnOpenSetsAvailable = true :=
  rfl

/-- C005 records that the domain Sobolev API is not yet available. -/
theorem weakDirichletBridgeChildGate_noSobolevDomainApi :
    weakDirichletBridgeChildGate.sobolevDomainApiAvailable = false :=
  rfl

/-- C005 records that the boundary trace API is not yet available. -/
theorem weakDirichletBridgeChildGate_noBoundaryTraceApi :
    weakDirichletBridgeChildGate.boundaryTraceApiAvailable = false :=
  rfl

/-- C005 keeps THM-M-1154 below completion. -/
theorem weakDirichletBridgeChildGate_noCompletionClaim :
    weakDirichletBridgeChildGate.completionClaimAllowed = false :=
  rfl

/-- C005 leaves no completed state carrying repo-local integration debt. -/
theorem weakDirichletBridgeChildGate_noCompletedRepoLocalIntegrationDebt :
    weakDirichletBridgeChildGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## Repo-local completion gate -/

/--
Repo-local completion gate for child `S1-M-144-C007`.

This gate records the current terminal status of THM-M-1154.  It is deliberately
negative: the local file has checked statement/audit anchors, but it has neither
a terminal proof body for the regular-boundary Dirichlet theorem nor a pinned
upstream wrapper in the repository's Lake validation closure.
-/
structure RepoLocalCompletionGate where
  childId : String
  publicStatusMustRemainNotCompleted : Bool
  localTerminalProofBodyChecked : Bool
  pinnedUpstreamWrapperChecked : Bool
  allTerminalPathLeavesChecked : Bool
  anchorOnlyEvidenceCountedAsCompletion : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  residualDebt : String
  requiredValidationCommand : String

/-- Machine-readable C007 gate value for THM-M-1154. -/
def repoLocalCompletionGate : RepoLocalCompletionGate where
  childId := "S1-M-144-C007"
  publicStatusMustRemainNotCompleted := true
  localTerminalProofBodyChecked := false
  pinnedUpstreamWrapperChecked := false
  allTerminalPathLeavesChecked := false
  anchorOnlyEvidenceCountedAsCompletion := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  residualDebt := "formalization_debt / not_repo_local_closed"
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_144.lean"

/--
Terminal-path leaves that still block completion under the M0387 `<=100` local
ledger rule.
-/
def repoLocalCompletionGateRemainingLeaves : List String := [
  "M1154-L013: audit `HarmonicContOnCl` as a possible stronger disk/domain solution predicate",
  "M1154-L014: audit Sobolev and distribution APIs for weak Dirichlet formulation and trace support",
  "M1154-L016: prove equivalence between chosen regularity definition and the boundary convergence field used by `StatementShape`",
  "M1154-L017: formalize disk/ball Dirichlet solution from Poisson integral under continuous boundary data",
  "M1154-L018: prove disk boundary convergence from Poisson kernel under the chosen boundary trace convention",
  "M1154-L019: define weak Dirichlet problem, Sobolev space, trace, and energy functional for this theorem variant",
  "M1154-L020: bridge weak harmonicity to `HarmonicOnNhd` under regularity assumptions",
  "M1154-L021: formalize Perron upper/lower classes or import a checked equivalent existence theorem",
  "M1154-L022: prove existence of a harmonic function satisfying interior estimates and candidate boundary behavior",
  "M1154-L023: prove boundary convergence at one regular boundary point for continuous boundary data",
  "M1154-L024: lift pointwise regular-boundary convergence to equality on `frontier Ω` or the selected trace predicate",
  "M1154-L025: add a terminal local wrapper theorem only after a proof body or pinned upstream theorem is available",
  "M1154-L026: merge human-readable statement/audit into the public Stage1 surface after integrator review"
]

/-- C007 requires the public status to remain not completed. -/
theorem repoLocalCompletionGate_publicStatusNotCompleted :
    repoLocalCompletionGate.publicStatusMustRemainNotCompleted = true :=
  rfl

/-- C007 records that no local terminal proof body has been checked. -/
theorem repoLocalCompletionGate_noLocalTerminalProof :
    repoLocalCompletionGate.localTerminalProofBodyChecked = false :=
  rfl

/-- C007 records that no pinned upstream wrapper has been checked. -/
theorem repoLocalCompletionGate_noPinnedUpstreamWrapper :
    repoLocalCompletionGate.pinnedUpstreamWrapperChecked = false :=
  rfl

/-- C007 records that the terminal-path `<=100` leaves are not all checked. -/
theorem repoLocalCompletionGate_terminalLeavesNotAllChecked :
    repoLocalCompletionGate.allTerminalPathLeavesChecked = false :=
  rfl

/-- C007 does not count anchor-only evidence as completion. -/
theorem repoLocalCompletionGate_noAnchorOnlyCompletion :
    repoLocalCompletionGate.anchorOnlyEvidenceCountedAsCompletion = false :=
  rfl

/-- C007 keeps THM-M-1154 below completion. -/
theorem repoLocalCompletionGate_noCompletionClaim :
    repoLocalCompletionGate.completionClaimAllowed = false :=
  rfl

/-- C007 leaves no completed state carrying repo-local integration debt. -/
theorem repoLocalCompletionGate_noCompletedRepoLocalIntegrationDebt :
    repoLocalCompletionGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## Audit probes -/

#check RegularBoundaryPointData
#check DirichletSolutionData
#check statementShapeNormalizationNote
#check StatementShape
#check harmonicOnNhd_const_anchor
#check harmonicOnNhd_continuousOn_anchor
#check harmonic_meanValue_closedDisk_anchor
#check harmonic_poissonKernel_closedDisk_anchor
#check poissonKernel_def_anchor
#check DiskBallDirichletSpecialCaseShape
#check diskBallDirichletPoissonAnchorNames
#check diskBallDirichletPublicChildTaskText
#check diskBallDirichletChildLeaves
#check diskBallDirichletChildGate
#check diskBallDirichletChildGate_anchorsChecked
#check diskBallDirichletChildGate_noCompletionClaim
#check RegularBoundaryDefinitionMethod
#check BoundaryBarrierData
#check BarrierBasedRegularBoundaryPoint
#check RegularBoundaryPoint
#check regularBoundaryDefinitionChoice
#check regularBoundaryDefinitionChoiceNote
#check deferredRegularBoundaryDefinitionMethods
#check RegularBoundaryPoint.mem_frontier
#check RegularBoundaryPoint.exists_barrierData
#check regularBoundaryDefinitionChildLeaves
#check regularBoundaryDefinitionChildGate
#check regularBoundaryDefinitionChildGate_chosenBarrier
#check regularBoundaryDefinitionChildGate_noCompletionClaim
#check auditedMathlibRevision
#check mathlibAuditCheckedModules
#check ExternalLeanAuditSearchStatus
#check externalAuditRequiredSearchTerms
#check externalLeanAuditSearchItems
#check externalLeanAuditNote
#check externalLeanAuditChildGate
#check externalLeanAuditChildGate_noAuthenticatedGithubSearch
#check externalLeanAuditChildGate_noTerminalExternalProof
#check externalLeanAuditChildGate_noPinnedExternalProof
#check externalLeanAuditChildGate_noCompletionClaim
#check externalLeanAuditChildGate_noCompletedRepoLocalIntegrationDebt
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check TestFunction
#check TestFunction.fderivCLM
#check Distribution
#check Distribution.mapCLM
#check LineDeriv.lineDerivOp
#check LineDeriv.iteratedLineDerivOp
#check Laplacian.laplacian
#check weakDirichletBridgeAvailableApiItems
#check weakDirichletBridgeAdjacentNonDomainApis
#check weakDirichletBridgeMissingApiItems
#check weakDirichletBridgeAuditNote
#check weakDirichletBridgeChildGate
#check weakDirichletBridgeChildGate_distributionAvailable
#check weakDirichletBridgeChildGate_noSobolevDomainApi
#check weakDirichletBridgeChildGate_noBoundaryTraceApi
#check weakDirichletBridgeChildGate_noCompletionClaim
#check RepoLocalCompletionGate
#check repoLocalCompletionGate
#check repoLocalCompletionGateRemainingLeaves
#check repoLocalCompletionGate_publicStatusNotCompleted
#check repoLocalCompletionGate_noLocalTerminalProof
#check repoLocalCompletionGate_noPinnedUpstreamWrapper
#check repoLocalCompletionGate_terminalLeavesNotAllChecked
#check repoLocalCompletionGate_noAnchorOnlyCompletion
#check repoLocalCompletionGate_noCompletionClaim
#check repoLocalCompletionGate_noCompletedRepoLocalIntegrationDebt

end S1_M_144
end Stage1
end AwesomeTheorems
