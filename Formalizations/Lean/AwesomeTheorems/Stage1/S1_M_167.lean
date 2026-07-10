import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic

/-!
# S1-M-167 / THM-M-1311: Choquet-Bruhat local existence theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
local existence theorem for the Einstein equations from Cauchy data.

The pinned mathlib snapshot has smooth-manifold, Riemannian-metric,
covariant-derivative, distribution, Sobolev-estimate, Picard-Lindelof, and
Gronwall infrastructure.  It does not expose terminal APIs for Lorentzian
metrics, Ricci curvature, Einstein tensors, the vacuum Einstein equations, or
the hyperbolic-reduction proof of Choquet-Bruhat.  The declarations below
therefore normalize the formalization boundary without proof placeholders or
axiomatizing the theorem.
-/

noncomputable section

open Bundle Manifold MeasureTheory
open scoped Distributions ENNReal Manifold ContDiff Topology

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_167

/-- Pinned mathlib revision audited for this Stage1 boundary. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact mathlib modules required by the THM-M-1311 mathlib audit child task. -/
def auditedMathlibModules : List String := [
  "Analysis.ODE.PicardLindelof",
  "Analysis.ODE.Gronwall",
  "Analysis.Distribution.Distribution",
  "Analysis.FunctionalSpaces.SobolevInequality",
  "Geometry.Manifold.Riemannian.Basic",
  "Geometry.Manifold.VectorBundle.CovariantDerivative.Basic"
]

/--
Initial Cauchy data for the Einstein equations on a spatial slice.

The current repository can name the ambient topological/smooth-manifold carrier,
but the metric, second fundamental form, constraint equations, gauge choice, and
Sobolev/smooth regularity hypotheses are kept as explicit fields.  A terminal
formalization should replace these `Prop` boundaries by concrete Lorentzian and
geometric-analysis APIs.
-/
structure EinsteinInitialData (Space : Type u) [TopologicalSpace Space] :
    Type (u + 1) where
  spatialMetricCarrier : Type u
  extrinsicCurvatureCarrier : Type u
  spatialMetric : spatialMetricCarrier
  secondFundamentalForm : extrinsicCurvatureCarrier
  smoothCauchyHypersurface : Prop
  constraintEquations : Prop
  gaugeChoice : Prop
  regularityHypotheses : Prop

/--
Smooth-manifold realization of the spatial Cauchy slice.

The `IsManifold` field is a checked mathlib predicate.  The Einstein-specific
geometric data are deliberately stored in `EinsteinInitialData`.
-/
structure SmoothCauchySlice
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (Space : Type u) [TopologicalSpace Space] [ChartedSpace H Space] :
    Type (u + 1) where
  isManifold : IsManifold I ∞ Space
  data : EinsteinInitialData Space

/--
Output expected from local existence for the Einstein equations.

This is a statement-shape carrier, not a Lorentzian-geometry implementation.
The missing terminal notions are isolated as proposition fields: Lorentzian
signature, vacuum Einstein equation, realization of the initial data, gauge
compatibility, and local uniqueness.
-/
structure LocalEinsteinDevelopment
    (Space : Type u) [TopologicalSpace Space]
    (Spacetime : Type v) [TopologicalSpace Spacetime]
    (initial : EinsteinInitialData Space) : Type (max (u + 1) (v + 1)) where
  spacetimeMetricCarrier : Type v
  spacetimeMetric : spacetimeMetricCarrier
  timeInterval : Set ℝ
  initialEmbedding : Space → Spacetime
  containsInitialSlice : Prop
  containsInitialSlice_holds : containsInitialSlice
  lorentzianMetric : Prop
  lorentzianMetric_holds : lorentzianMetric
  solvesVacuumEinsteinEquations : Prop
  solvesVacuumEinsteinEquations_holds : solvesVacuumEinsteinEquations
  realizesInitialData : Prop
  realizesInitialData_holds : realizesInitialData
  gaugeCompatibility : Prop
  gaugeCompatibility_holds : gaugeCompatibility
  locallyUniqueUpToIsometry : Prop
  locallyUniqueUpToIsometry_holds : locallyUniqueUpToIsometry

/--
Normalized Stage1 statement-shape candidate for Choquet-Bruhat local existence.

For every smooth Cauchy slice whose data satisfy the constraint equations and
the regularity/gauge hypotheses, there exists a local spacetime development
solving the vacuum Einstein equations and realizing those data.  This is only a
`Prop` boundary; it is not a proof of the analytic theorem.
-/
def StatementShape : Prop :=
  ∀ (Space : Type u) [TopologicalSpace Space] (initial : EinsteinInitialData Space),
    initial.smoothCauchyHypersurface →
      initial.constraintEquations →
        initial.gaugeChoice →
          initial.regularityHypotheses →
            ∃ (Spacetime : Type u) (_ : TopologicalSpace Spacetime),
              Nonempty (LocalEinsteinDevelopment Space Spacetime initial)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Space : Type u) [TopologicalSpace Space] (initial : EinsteinInitialData Space),
      initial.smoothCauchyHypersurface →
        initial.constraintEquations →
          initial.gaugeChoice →
            initial.regularityHypotheses →
              ∃ (Spacetime : Type u) (_ : TopologicalSpace Spacetime),
                Nonempty (LocalEinsteinDevelopment Space Spacetime initial)) :
    StatementShape.{u} :=
  h

/-- A local development exposes the placeholder vacuum-Einstein equation field. -/
theorem LocalEinsteinDevelopment.solves_vacuum
    {Space : Type u} [TopologicalSpace Space]
    {Spacetime : Type v} [TopologicalSpace Spacetime]
    {initial : EinsteinInitialData Space}
    (D : LocalEinsteinDevelopment Space Spacetime initial) :
    D.solvesVacuumEinsteinEquations :=
  D.solvesVacuumEinsteinEquations_holds

/-- A local development exposes the initial-data realization field. -/
theorem LocalEinsteinDevelopment.realizes_initial_data
    {Space : Type u} [TopologicalSpace Space]
    {Spacetime : Type v} [TopologicalSpace Spacetime]
    {initial : EinsteinInitialData Space}
    (D : LocalEinsteinDevelopment Space Spacetime initial) :
    D.realizesInitialData :=
  D.realizesInitialData_holds

/--
Gauge-reduced finite-dimensional evolution problem.

This is a checked ODE-side anchor for the standard proof strategy: after gauge
fixing and reduction one proves a local evolution theorem.  It is not the
Einstein hyperbolic-reduction theorem itself.
-/
structure GaugeReducedEvolutionProblem
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] : Type u where
  vectorField : E → E
  basePoint : E
  c1AtBase : ContDiffAt ℝ 1 vectorField basePoint

/--
Checked Picard-Lindelof anchor: a `C^1` vector field on a complete normed space
has a local integral curve through the base point.
-/
theorem gaugeReduced_local_integral_curve_anchor
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    (P : GaugeReducedEvolutionProblem E) (t₀ : ℝ) :
    ∃ α : ℝ → E, α t₀ = P.basePoint ∧ ∃ ε > (0 : ℝ),
      ∀ t ∈ Set.Ioo (t₀ - ε) (t₀ + ε),
        HasDerivAt α (P.vectorField (α t)) t :=
  P.c1AtBase.exists_forall_mem_closedBall_exists_eq_forall_mem_Ioo_hasDerivAt₀ t₀

/-- Checked Gronwall anchor used by energy-estimate and uniqueness packages. -/
theorem gronwallBound_initial_anchor (δ K ε : ℝ) :
    gronwallBound δ K ε 0 = δ :=
  gronwallBound_x0 δ K ε

/-- Checked Riemannian anchor: inner-product vector spaces have mathlib Riemannian metrics. -/
def riemannianMetricVectorSpace_anchor
    (F : Type u) [NormedAddCommGroup F] [InnerProductSpace ℝ F] :
    ContMDiffRiemannianMetric 𝓘(ℝ, F) ω F
      (fun x : F => TangentSpace 𝓘(ℝ, F) x) :=
  riemannianMetricVectorSpace F

/-- Scalar distributions on an open domain, using mathlib's current distribution object. -/
abbrev ScalarDistributionOn
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ω : TopologicalSpace.Opens E) (n : ℕ∞ := ⊤) : Type u :=
  Distribution Ω ℝ n

/-- Checked distribution anchor: continuous linear maps act on distributions. -/
def scalarDistribution_id_map
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ω : TopologicalSpace.Opens E) (n : ℕ∞ := ⊤) :
    ScalarDistributionOn E Ω n →L[ℝ] ScalarDistributionOn E Ω n :=
  Distribution.mapCLM (Ω := Ω) (F := ℝ) (F' := ℝ) (n := n) (ContinuousLinearMap.id ℝ ℝ)

/-- mathlib modules checked while locating repo-local Choquet-Bruhat anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.Tensoriality",
  "Mathlib.Analysis.ODE.Basic",
  "Mathlib.Analysis.ODE.PicardLindelof",
  "Mathlib.Analysis.ODE.Gronwall",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality"
]

/-- Nearby checked names used or audited for the Stage1 statement boundary. -/
def mathlibAnchorNames : List String := [
  "IsManifold",
  "ContMDiff",
  "ContMDiffAt",
  "IsCovariantDerivativeOn",
  "CovariantDerivative",
  "ContMDiffRiemannianMetric",
  "riemannianMetricVectorSpace",
  "IsPicardLindelof",
  "ContDiffAt.exists_forall_mem_closedBall_exists_eq_forall_mem_Ioo_hasDerivAt₀",
  "gronwallBound",
  "gronwallBound_x0",
  "Distribution",
  "Distribution.mapCLM",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv"
]

/--
Search terms that did not locate a terminal Choquet-Bruhat or Einstein-equation
local-existence theorem in the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Choquet",
  "Bruhat",
  "Choquet-Bruhat",
  "Einstein equation",
  "EinsteinEquation",
  "vacuum Einstein",
  "Ricci",
  "Lorentz",
  "Lorentzian",
  "globally hyperbolic",
  "Cauchy development",
  "hyperbolic reduction"
]

/-- One row in the pinned mathlib negative terminal-anchor audit. -/
structure AbsentTerminalAnchorAuditRow where
  theoremFamily : String
  searchedTerms : List String
  pinnedMathlibFinding : String
  completionStatus : String
deriving Repr

/--
Structured record for the child audit:
the pinned local mathlib search found no terminal theorem for these target
families.  Incidental text hits such as Bruhat-Tits or Einstein-Podolsky-Rosen
do not supply Choquet-Bruhat, Einstein-equation, Ricci, or Lorentzian local
existence APIs.
-/
def absentTerminalAnchorAuditRows : List AbsentTerminalAnchorAuditRow := [
  { theoremFamily := "Choquet-Bruhat local existence"
    searchedTerms := ["Choquet", "Bruhat", "Choquet-Bruhat"]
    pinnedMathlibFinding :=
      "no terminal Choquet-Bruhat theorem or local Cauchy-development theorem found"
    completionStatus := "negative_anchor_only; parent remains formalization_debt" },
  { theoremFamily := "Einstein equation local existence"
    searchedTerms := ["Einstein equation", "EinsteinEquation", "vacuum Einstein"]
    pinnedMathlibFinding :=
      "no vacuum Einstein equation API or local-existence theorem found"
    completionStatus := "negative_anchor_only; parent remains formalization_debt" },
  { theoremFamily := "Ricci curvature / Einstein tensor"
    searchedTerms := ["Ricci", "Einstein tensor", "Ricci curvature"]
    pinnedMathlibFinding :=
      "no Ricci-curvature or Einstein-tensor API found for Lorentzian developments"
    completionStatus := "negative_anchor_only; parent remains formalization_debt" },
  { theoremFamily := "Lorentzian local existence"
    searchedTerms := ["Lorentz", "Lorentzian", "globally hyperbolic",
      "Cauchy development", "hyperbolic reduction"]
    pinnedMathlibFinding :=
      "no Lorentzian metric local-existence or hyperbolic-reduction theorem found"
    completionStatus := "negative_anchor_only; parent remains formalization_debt" }
]

/-- The absent terminal-anchor audit records the four requested search families. -/
theorem absentTerminalAnchorAuditRows_length :
    absentTerminalAnchorAuditRows.length = 4 := by
  native_decide

/--
M0387 gate for the absent-terminal-anchor child: this negative mathlib audit
does not complete the parent theorem and does not create repo-local integration
debt from an external anchor-only proof.
-/
def absentTerminalAnchorGate : String :=
  "pinned mathlib search found no terminal Choquet-Bruhat, Einstein-equation, Ricci, or Lorentzian local-existence theorem; no completed state is claimed"

/--
Formalization-debt gate for THM-M-1311: the repo-local artifact is a checked
statement boundary and audit record only.  It intentionally keeps the parent
status non-completed until a terminal local proof body, pinned mathlib wrapper,
or pinned/imported/checked external Lean proof exists.
-/
def formalizationDebtGate : String :=
  "not completed; formalization_debt; no terminal Choquet-Bruhat Lean proof is in the repo-local validation closure"

/-! ## External Lean 4 source-audit boundary. -/

/--
One row in the external Lean 4 audit for THM-M-1311.

Rows record exact source coordinates only when a public adjacent Lean artifact
was visible.  They are not completion claims unless `integrationStatus`
explicitly says the external proof is pinned, imported, and checked in this
repository.
-/
structure ExternalLean4AuditRow where
  repoUrl : String
  commit : String
  sourceFile : String
  theoremName : String
  evidenceStatus : String
  integrationStatus : String
deriving Repr

/--
Authenticated GitHub audit status for this child.

The local `gh auth status` check reported no logged-in GitHub host, and no
`GH_TOKEN`, `GITHUB_TOKEN`, or `GITHUB_PAT` environment variable was available
to run authenticated code search.  The child therefore records the concrete
blocker rather than treating unauthenticated search as complete.
-/
def externalLean4AuthenticatedAuditStatus : List String := [
  "blocked: gh auth status reported no logged-in GitHub hosts on 2026-05-01",
  "blocked: no GH_TOKEN, GITHUB_TOKEN, or GITHUB_PAT environment variable was present",
  "fallback: public web/source inspection found adjacent Einstein-equation Lean material, but no Choquet-Bruhat local-existence proof candidate"
]

/--
Visible adjacent external Lean 4 source evidence from the fallback source audit.

The QFTT-WESH repository is recorded because it contains Lean theorem names
about an Einstein-equation emergence predicate.  Its statements are finite
dimensional operator/fixed-point statements and do not encode the
Choquet-Bruhat theorem: no Lorentzian Cauchy development, no Einstein initial
constraint system, no local hyperbolic PDE existence theorem, and no local
uniqueness up to isometry.
-/
def externalLean4AuditRows : List ExternalLean4AuditRow := [
  { repoUrl := "https://github.com/Luca-Casagrande/qftt-wesh"
    commit := "c27c4434c8dd8d44b450b5754629ff4940033a4d"
    sourceFile := "formal-verification/Section5.lean"
    theoremName := "theorem_5_4_einstein_emergence"
    evidenceStatus :=
      "adjacent Einstein-equation-emergence theorem over finite-dimensional operator data; not Choquet-Bruhat local Cauchy existence"
    integrationStatus :=
      "not_integrated_not_applicable; no repo_local_integration_debt because this is not a terminal THM-M-1311 proof candidate" },
  { repoUrl := "https://github.com/Luca-Casagrande/qftt-wesh"
    commit := "c27c4434c8dd8d44b450b5754629ff4940033a4d"
    sourceFile := "formal-verification/Section5.lean"
    theoremName := "theorem_D_2_variational_alignment"
    evidenceStatus :=
      "adjacent Einstein-equation-emergence theorem over finite-dimensional operator data; not Choquet-Bruhat local Cauchy existence"
    integrationStatus :=
      "not_integrated_not_applicable; no repo_local_integration_debt because this is not a terminal THM-M-1311 proof candidate" }
]

/-- The fallback external source-audit table currently records two adjacent rows. -/
theorem externalLean4AuditRows_length :
    externalLean4AuditRows.length = 2 := by
  native_decide

/--
M0387 gate for the external audit child.

No completed state is claimed: authenticated GitHub code search is blocked by
missing credentials, and the only visible adjacent Lean source is not a
Choquet-Bruhat local-existence theorem.  Therefore there is no external proof
to pin/import/check, and no repo-local integration debt is introduced.
-/
def externalLean4AuditGate : String :=
  "not completed as an authenticated audit; no terminal external Choquet-Bruhat Lean 4 proof candidate found in fallback source inspection; no repo_local_integration_debt introduced"

/-! ## Theorem-tree merge inventory for the public Stage1 backfill. -/

/--
One theorem-tree leaf for the Choquet-Bruhat Stage1 plan.

The first eighteen leaves are repo-local checked statement/audit leaves.  The
remaining leaves are deliberately marked `unchecked`: they are the unresolved
Lorentzian-geometry, Einstein-equation, hyperbolic-PDE, uniqueness, external
audit, import-aggregator, and public-merge obligations.
-/
structure TheoremTreeLeaf where
  leafId : String
  package : String
  action : String
  budget : String
  status : String
deriving Repr

/-- Integration-ready theorem-tree leaves for THM-M-1311. -/
def theoremTreeLeaves : List TheoremTreeLeaf := [
  { leafId := "M1311-L001", package := "P0",
    action := "Define EinsteinInitialData with metric, second fundamental form, constraints, gauge, and regularity fields.",
    budget := "<=20", status := "checked local" },
  { leafId := "M1311-L002", package := "P0",
    action := "Define SmoothCauchySlice with mathlib IsManifold I infinity Space.",
    budget := "<=20", status := "checked local" },
  { leafId := "M1311-L003", package := "P0",
    action := "Define LocalEinsteinDevelopment with abstract Lorentzian, Einstein-equation, and initial-data evidence fields.",
    budget := "<=25", status := "checked local" },
  { leafId := "M1311-L004", package := "P0",
    action := "Define StatementShape : Prop.", budget := "<=15", status := "checked local" },
  { leafId := "M1311-L005", package := "P0",
    action := "Add StatementShape.intro.", budget := "<=10", status := "checked local" },
  { leafId := "M1311-L006", package := "P0",
    action := "Expose solvesVacuumEinsteinEquations_holds.",
    budget := "<=10", status := "checked local" },
  { leafId := "M1311-L007", package := "P0",
    action := "Expose realizesInitialData_holds.", budget := "<=10", status := "checked local" },
  { leafId := "M1311-L008", package := "P1",
    action := "Audit smooth-manifold modules and names.", budget := "<=30", status := "checked local" },
  { leafId := "M1311-L009", package := "P1",
    action := "Audit Riemannian modules and names.", budget := "<=30", status := "checked local" },
  { leafId := "M1311-L010", package := "P1",
    action := "Audit covariant-derivative modules and names.",
    budget := "<=30", status := "checked local" },
  { leafId := "M1311-L011", package := "P1",
    action := "Audit distribution/Sobolev modules and names.",
    budget := "<=30", status := "checked local" },
  { leafId := "M1311-L012", package := "P1",
    action := "Audit ODE/Picard-Lindelof/Gronwall modules and names.",
    budget := "<=30", status := "checked local" },
  { leafId := "M1311-L013", package := "P1",
    action := "Add GaugeReducedEvolutionProblem.", budget := "<=15", status := "checked local" },
  { leafId := "M1311-L014", package := "P1",
    action := "Add Picard-Lindelof local integral-curve wrapper.",
    budget := "<=20", status := "checked local" },
  { leafId := "M1311-L015", package := "P1",
    action := "Add Gronwall initial-value wrapper.", budget := "<=10", status := "checked local" },
  { leafId := "M1311-L016", package := "P1",
    action := "Add Riemannian vector-space metric wrapper.",
    budget := "<=10", status := "checked local" },
  { leafId := "M1311-L017", package := "P1",
    action := "Add distribution carrier and identity-map wrapper.",
    budget := "<=20", status := "checked local" },
  { leafId := "M1311-L018", package := "P1",
    action := "Record absent terminal search terms in Lean file.",
    budget := "<=10", status := "checked local" },
  { leafId := "M1311-L019", package := "P2",
    action := "Choose concrete harmonic/wave-coordinate gauge.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L020", package := "P2",
    action := "Define Lorentzian metric object or locate importable upstream API.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L021", package := "P2",
    action := "Define Ricci curvature / Einstein tensor object or locate importable upstream API.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L022", package := "P2",
    action := "Formalize vacuum Einstein equation Ric(g)=0 or equivalent target.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L023", package := "P2",
    action := "Formalize reduced hyperbolic Einstein system.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L024", package := "P2",
    action := "Prove reduced-system/equation bridge under gauge and constraints.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L025", package := "P3",
    action := "Select Sobolev/smooth regularity API and data spaces.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L026", package := "P3",
    action := "Prove local existence for quasilinear hyperbolic system.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L027", package := "P3",
    action := "Prove energy estimate with Gronwall-style closure.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L028", package := "P3",
    action := "Prove constraint propagation.", budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L029", package := "P3",
    action := "Build LocalEinsteinDevelopment from concrete solution data.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L030", package := "P4",
    action := "Define local spacetime isometry in selected object model.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L031", package := "P4",
    action := "Prove uniqueness for reduced local solution.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L032", package := "P4",
    action := "Transfer uniqueness to geometric local isometry.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L033", package := "P5",
    action := "Re-run authenticated external Lean 4 source audit.",
    budget := "<=60", status := "unchecked" },
  { leafId := "M1311-L034", package := "P5",
    action := "If external proof exists, pin/import/check or document exact integration blocker.",
    budget := "<=100", status := "unchecked" },
  { leafId := "M1311-L035", package := "P5",
    action := "Add any accepted Stage1 file to shared import aggregator in a serialized integrator patch.",
    budget := "<=30", status := "unchecked" },
  { leafId := "M1311-L036", package := "P5",
    action := "Merge public status, validation command, and debt classification into public surfaces consistently.",
    budget := "<=60", status := "unchecked" }
]

/-- The public theorem-tree merge inventory has the requested 36 leaves. -/
theorem theoremTreeLeaves_length : theoremTreeLeaves.length = 36 := by
  native_decide

/-- Leaves still open after the repo-local statement-shape and audit work. -/
def theoremTreeUncheckedLeafIds : List String := [
  "M1311-L019",
  "M1311-L020",
  "M1311-L021",
  "M1311-L022",
  "M1311-L023",
  "M1311-L024",
  "M1311-L025",
  "M1311-L026",
  "M1311-L027",
  "M1311-L028",
  "M1311-L029",
  "M1311-L030",
  "M1311-L031",
  "M1311-L032",
  "M1311-L033",
  "M1311-L034",
  "M1311-L035",
  "M1311-L036"
]

/-- The unchecked portion of the public theorem tree has the requested 18 leaves. -/
theorem theoremTreeUncheckedLeafIds_length : theoremTreeUncheckedLeafIds.length = 18 := by
  native_decide

/-! ## Audit probes retained in the checked file. -/

#check EinsteinInitialData
#check pinnedMathlibRevision
#check auditedMathlibModules
#check SmoothCauchySlice
#check LocalEinsteinDevelopment
#check StatementShape
#check GaugeReducedEvolutionProblem
#check gaugeReduced_local_integral_curve_anchor
#check gronwallBound_initial_anchor
#check riemannianMetricVectorSpace_anchor
#check ScalarDistributionOn
#check scalarDistribution_id_map
#check absentTerminalSearchTerms
#check AbsentTerminalAnchorAuditRow
#check absentTerminalAnchorAuditRows
#check absentTerminalAnchorAuditRows_length
#check absentTerminalAnchorGate
#check formalizationDebtGate
#check ExternalLean4AuditRow
#check externalLean4AuthenticatedAuditStatus
#check externalLean4AuditRows
#check externalLean4AuditRows_length
#check externalLean4AuditGate
#check TheoremTreeLeaf
#check theoremTreeLeaves
#check theoremTreeLeaves_length
#check theoremTreeUncheckedLeafIds
#check theoremTreeUncheckedLeafIds_length

end S1_M_167
end Stage1
end AwesomeTheorems
