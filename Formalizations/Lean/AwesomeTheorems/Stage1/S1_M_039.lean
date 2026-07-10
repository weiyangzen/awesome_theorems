import Mathlib.Analysis.Convex.Cone.Basic
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Noetherian
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.Analysis.Meromorphic.Divisor
import Mathlib.RingTheory.PicardGroup
import Mathlib.Topology.Instances.Real.Lemmas

/-!
# S1-M-039 / THM-M-0120: Mori cone theorem, Stage1 statement shape

This file records a repo-local Lean 4 boundary artifact for Mori's cone theorem.
It intentionally does not assert the terminal theorem: mathlib currently supplies
scheme, proper morphism, noetherian, Proj, and Picard-group substrate, while the
Mori cone, numerical curve classes, klt pair hypotheses, extremal rays, and the
contraction theorem branch are represented here as explicit statement-shape
fields.
-/

noncomputable section

open CategoryTheory

universe u

namespace AwesomeTheorems.Stage1.S1_M_039

/--
Formalization boundary for the cone theorem. The fields with `Prop` type are
deliberate placeholders for concepts that are not currently available as a
terminal mathlib API for the Mori program.
-/
structure MoriConeStatementData : Type (u + 1) where
  X : AlgebraicGeometry.Scheme.{u}
  S : AlgebraicGeometry.Scheme.{u}
  f : X ⟶ S
  projectiveOverBase : Prop
  normalQFactorialVariety : Prop
  kltPairData : Prop
  relativeCanonicalDivisor : Type u
  relativeOneCycles : Type u
  moriCone : Type u
  effectiveCurveClass : relativeOneCycles → Prop
  coneClass : relativeOneCycles → moriCone
  canonicalIntersectionNegative : moriCone → Prop
  negativeExtremalRay : Type u
  raySpan : negativeExtremalRay → Set moriCone
  countablyManyNegativeRays : Prop
  coneDecomposition : Prop
  localFinitenessInNegativeHalfspace : Prop
  contractionForEveryNegativeExtremalRay : Prop

/-- Mathlib-backed hypotheses plus the explicit MMP-specific placeholders. -/
def MoriConeHypotheses (D : MoriConeStatementData.{u}) : Prop :=
  AlgebraicGeometry.IsProper D.f ∧
    AlgebraicGeometry.IsNoetherian D.X ∧
    AlgebraicGeometry.IsNoetherian D.S ∧
    D.projectiveOverBase ∧
    D.normalQFactorialVariety ∧
    D.kltPairData

/-- The usual output package of Mori's cone theorem, kept as statement shape. -/
def MoriConeConclusion (D : MoriConeStatementData.{u}) : Prop :=
  D.countablyManyNegativeRays ∧
    D.coneDecomposition ∧
    D.localFinitenessInNegativeHalfspace ∧
    D.contractionForEveryNegativeExtremalRay

/--
Stage1 normalized statement shape for the Mori cone theorem. This is a
formalization target, not a completed theorem in this repository.
-/
def StatementShape : Prop :=
  ∀ D : MoriConeStatementData.{u}, MoriConeHypotheses D → MoriConeConclusion D

/-! ## Canonical statement target decision -/

/- Candidate public theorem targets for child `S1-M-039-C002`. -/
inductive PublicStatementTarget where
  | absoluteProjectiveVarietyOverAlgebraicallyClosedField
  | relativeProjectiveMorphism
  | relativeProjectiveKltPair
deriving DecidableEq, Repr

/--
The C002 decision: use the relative projective klt-pair formulation as the
canonical Stage1 target. The absolute projective variety form is a specialization
over `Spec k`, and the unpaired variety form is a further specialization after
choosing the boundary divisor to be zero.
-/
def chosenPublicStatementTarget : PublicStatementTarget :=
  PublicStatementTarget.relativeProjectiveKltPair

/-- Checked equality for the C002 public target decision. -/
theorem chosenPublicStatementTarget_eq_relativeProjectiveKltPair :
    chosenPublicStatementTarget =
      PublicStatementTarget.relativeProjectiveKltPair := by
  rfl

/--
The selected public target is the existing relative statement scaffold with
projectivity, normal/Q-factorial data, klt-pair data, relative canonical
divisor, relative one-cycles, Mori cone, negative extremal rays, local
finiteness, and contraction output all explicit.
-/
def RelativeProjectiveKltPairStatementShape : Prop :=
  StatementShape.{u}

/-- Definitional expansion of the selected C002 target. -/
theorem relativeProjectiveKltPairStatementShape_iff_statementShape :
    RelativeProjectiveKltPairStatementShape.{u} ↔ StatementShape.{u} := by
  rfl

/--
C002 diagnosis for public backfill. This is a statement-normalization result,
not a theorem proof or completion claim.
-/
def statementTargetDecisionDiagnosis : String :=
  "C002 selects the relative projective klt-pair formulation as the canonical Lean target; absolute projective and bare-variety forms remain specializations, not competing Stage1 terminal targets"

/-! ## External Lean 4 source audit -/

/-- Date of the child-level external Lean 4 source audit. -/
def externalLeanAuditDate : String := "2026-05-01"

/--
One row from the child audit for possible Lean 4 proofs of Mori's cone theorem.

Negative and blocked search rows are deliberately recorded here too, so a later
public integrator can distinguish a real theorem anchor from an authentication
or rate-limit blocker. A row is `pinReady = true` only when it identifies a
proof candidate with a repository URL, commit SHA, module path, theorem
declaration, and Lean toolchain that can be tested in this Lake closure.
-/
structure ExternalLeanAuditRow where
  code : String
  sourceKind : String
  repositoryOrSearchUrl : String
  commitShaOrResult : String
  modulePathOrSearchScope : String
  theoremDeclarations : List String
  leanToolchain : String
  auditResult : String
  pinReady : Bool
  deriving DecidableEq, Repr

/--
Child `S1-M-039-C001` external Lean 4 audit rows.

The pinned local dependencies and available public search routes do not
currently identify a Lean 4 theorem declaration for the Mori cone theorem. The
GitHub code-search route is not closed by this worker because it requires
authentication or a non-exhausted authenticated rate limit.
-/
def externalLeanAuditRows : List ExternalLeanAuditRow := [
  {
    code := "MORI-CONE-EA-01"
    sourceKind := "pinned mathlib4 dependency"
    repositoryOrSearchUrl := "https://github.com/leanprover-community/mathlib4.git"
    commitShaOrResult := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    modulePathOrSearchScope :=
      "Mathlib/**/*.lean searched for Mori, ConeTheorem, cone theorem, ExtremalRay, klt, Klt, Kawamata, Shokurov, NumericalCurve, N1, Kleiman, and nef"
    theoremDeclarations := []
    leanToolchain := "leanprover/lean4:v4.29.0"
    auditResult :=
      "No Mori cone theorem, K-negative extremal-ray decomposition, klt-pair, or contraction-theorem declaration was found in the pinned mathlib source tree."
    pinReady := false
  },
  {
    code := "MORI-CONE-EA-02"
    sourceKind := "pinned flt-regular dependency"
    repositoryOrSearchUrl := "https://github.com/leanprover-community/flt-regular.git"
    commitShaOrResult := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
    modulePathOrSearchScope :=
      "all Lean sources searched for Mori, ConeTheorem, cone theorem, ExtremalRay, klt, Klt, Kawamata, Shokurov, NumericalCurve, and Kleiman-Mori terms"
    theoremDeclarations := []
    leanToolchain := "leanprover/lean4:v4.29.0"
    auditResult :=
      "No algebraic-geometry Mori cone theorem declaration or adjacent proof body was found."
    pinReady := false
  },
  {
    code := "MORI-CONE-EA-03"
    sourceKind := "GitHub repository search"
    repositoryOrSearchUrl :=
      "https://api.github.com/search/repositories?q=%22Mori%20cone%20theorem%22%20Lean&per_page=10"
    commitShaOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false"
    modulePathOrSearchScope := "repository search result"
    theoremDeclarations := []
    leanToolchain := "none"
    auditResult := "No repository candidate was returned."
    pinReady := false
  },
  {
    code := "MORI-CONE-EA-04"
    sourceKind := "GitHub repository search"
    repositoryOrSearchUrl :=
      "https://api.github.com/search/repositories?q=%22Cone%20theorem%22%20Lean%20algebraic%20geometry&per_page=10"
    commitShaOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false"
    modulePathOrSearchScope := "repository search result"
    theoremDeclarations := []
    leanToolchain := "none"
    auditResult := "No repository candidate was returned."
    pinReady := false
  },
  {
    code := "MORI-CONE-EA-05"
    sourceKind := "GitHub repository search"
    repositoryOrSearchUrl :=
      "https://api.github.com/search/repositories?q=Mori%20Lean%20algebraic%20geometry&per_page=10"
    commitShaOrResult :=
      "2026-05-01 unauthenticated REST repository search with HTTP/1.1: total_count = 0; incomplete_results = false"
    modulePathOrSearchScope := "repository search result"
    theoremDeclarations := []
    leanToolchain := "none"
    auditResult := "No Mori algebraic-geometry Lean repository candidate was returned."
    pinReady := false
  },
  {
    code := "MORI-CONE-EA-06"
    sourceKind := "GitHub code search"
    repositoryOrSearchUrl :=
      "https://api.github.com/search/code?q=%22ConeTheorem%22+language:Lean&per_page=10"
    commitShaOrResult :=
      "2026-05-01 unauthenticated REST code search blocked by API rate-limit exhaustion; gh CLI also reported no authenticated GitHub host"
    modulePathOrSearchScope := "Lean code search for exact ConeTheorem identifier"
    theoremDeclarations := []
    leanToolchain := "blocked"
    auditResult :=
      "Authentication or a usable authenticated rate limit is required before exact code hits can be trusted as complete."
    pinReady := false
  },
  {
    code := "MORI-CONE-EA-07"
    sourceKind := "Loogle declaration search"
    repositoryOrSearchUrl := "https://loogle.lean-lang.org/json?q=Mori"
    commitShaOrResult :=
      "2026-05-01 queries for Mori, ConeTheorem, ExtremalRay, and klt returned unknown-identifier errors"
    modulePathOrSearchScope := "declaration-name search"
    theoremDeclarations := []
    leanToolchain := "public Loogle index; exact revision not exposed by query response"
    auditResult :=
      "No public indexed declaration name for Mori, ConeTheorem, ExtremalRay, or klt was identified."
    pinReady := false
  }
]

/-- The child audit records seven source/search rows. -/
theorem externalLeanAuditRows_length : externalLeanAuditRows.length = 7 :=
  rfl

/-- No current row identifies a pin-ready external proof of Mori's cone theorem. -/
theorem externalLeanAuditRows_no_pinReady :
    externalLeanAuditRows.map ExternalLeanAuditRow.pinReady =
      [false, false, false, false, false, false, false] :=
  rfl

/-- Current repo-local status after the child external-source audit. -/
def externalLeanAuditStatus : String :=
  "not_repo_local_closed: no Lean 4 Mori cone theorem proof declaration was found in pinned dependencies; authenticated GitHub code search remains a concrete audit blocker"

/--
Completion gate for the M0387 repo-local integration-debt rule.

This child found no external Lean 4 proof to count as anchor-only evidence. If
a future authenticated search finds one, this Stage1 slot must pin/import/check
it or record a concrete toolchain, dependency, or license blocker before any
completion claim.
-/
def repoLocalIntegrationDebtGate : String :=
  "no completed-state repo_local_integration_debt; no external Lean 4 cone-theorem proof is currently pinned, imported, or checked"

namespace MathlibAnchors

variable {X Y Z S : AlgebraicGeometry.Scheme.{u}}

/-- Proper morphisms are closed under composition in mathlib. -/
theorem proper_comp (f : X ⟶ Y) (g : Y ⟶ Z)
    [AlgebraicGeometry.IsProper f] [AlgebraicGeometry.IsProper g] :
    AlgebraicGeometry.IsProper (f ≫ g) :=
  inferInstance

/-- Finite morphisms are proper in mathlib. -/
theorem finite_morphism_is_proper (f : X ⟶ Y) [AlgebraicGeometry.IsFinite f] :
    AlgebraicGeometry.IsProper f :=
  inferInstance

/-- Proper morphisms are stable under pullback on the first projection. -/
theorem proper_pullback_fst (f : X ⟶ S) (g : Y ⟶ S) [AlgebraicGeometry.IsProper g] :
    AlgebraicGeometry.IsProper (Limits.pullback.fst f g) :=
  inferInstance

/-- Proper morphisms are stable under pullback on the second projection. -/
theorem proper_pullback_snd (f : X ⟶ S) (g : Y ⟶ S) [AlgebraicGeometry.IsProper f] :
    AlgebraicGeometry.IsProper (Limits.pullback.snd f g) :=
  inferInstance

/-- Mathlib's finite/proper/affine characterization, exposed as a Stage1 anchor. -/
theorem finite_iff_proper_and_affine {f : X ⟶ Y} :
    AlgebraicGeometry.IsFinite f ↔
      AlgebraicGeometry.IsProper f ∧ AlgebraicGeometry.IsAffineHom f :=
  AlgebraicGeometry.IsFinite.iff_isProper_and_isAffineHom

end MathlibAnchors

/-! ## Numerical curve class / `N1` API sketch -/

/--
Child `S1-M-039-C003`: a checked boundary sketch for the numerical curve
class space usually denoted `N₁(X/S)`.

The structure is deliberately parametric in the eventual algebraic-geometric
construction of numerical equivalence. Its purpose is to pin the surrounding
mathlib API choices: an `ℝ`-module/topological vector-space carrier for `N₁`,
an effective cone as `ConvexCone ℝ N1`, the Mori cone as
`ConvexCone.closure`, and canonical-divisor intersection as a continuous
linear functional whose nonpositive halfspace is topologically closed.
-/
structure NumericalCurveClassApiSketch : Type (u + 1) where
  curve : Type u
  N1 : Type u
  [instAddCommGroup : AddCommGroup N1]
  [instModuleReal : Module ℝ N1]
  [instTopologicalSpace : TopologicalSpace N1]
  [instContinuousAdd : ContinuousAdd N1]
  [instContinuousConstSMulReal : ContinuousConstSMul ℝ N1]
  curveClass : curve → N1
  effectiveCone : ConvexCone ℝ N1
  curveClass_mem_effectiveCone : ∀ C : curve, curveClass C ∈ effectiveCone
  canonicalIntersection : N1 →L[ℝ] ℝ

namespace NumericalCurveClassApiSketch

attribute [instance] instAddCommGroup instModuleReal instTopologicalSpace
  instContinuousAdd instContinuousConstSMulReal

/-- The Mori cone is modeled by the topological closure of the effective cone. -/
def moriCone (A : NumericalCurveClassApiSketch.{u}) : ConvexCone ℝ A.N1 :=
  A.effectiveCone.closure

/-- The underlying set-level closure corresponding to `moriCone`. -/
def moriConeSet (A : NumericalCurveClassApiSketch.{u}) : Set A.N1 :=
  closure (A.effectiveCone : Set A.N1)

/-- Membership in the cone-level Mori cone is membership in the topological closure. -/
theorem mem_moriCone_iff_mem_closure (A : NumericalCurveClassApiSketch.{u}) (γ : A.N1) :
    γ ∈ A.moriCone ↔ γ ∈ A.moriConeSet :=
  Iff.rfl

/-- Actual curve classes enter the effective cone by construction. -/
theorem curveClass_mem_effective (A : NumericalCurveClassApiSketch.{u}) (C : A.curve) :
    A.curveClass C ∈ A.effectiveCone :=
  A.curveClass_mem_effectiveCone C

/-- Actual curve classes also enter the closed Mori cone via `subset_closure`. -/
theorem curveClass_mem_moriCone (A : NumericalCurveClassApiSketch.{u}) (C : A.curve) :
    A.curveClass C ∈ A.moriCone :=
  subset_closure (A.curveClass_mem_effective C)

/-- The canonical negative region used by the cone theorem statement shape. -/
def canonicalNegativeHalfspace (A : NumericalCurveClassApiSketch.{u}) : Set A.N1 :=
  {γ | A.canonicalIntersection γ < 0}

/-- The closed nonpositive halfspace associated to canonical intersection. -/
def canonicalNonpositiveHalfspace (A : NumericalCurveClassApiSketch.{u}) : Set A.N1 :=
  {γ | A.canonicalIntersection γ ≤ 0}

/--
The topology API map for C003: continuous linear functionals provide closed
nonpositive halfspaces through `ContinuousLinearMap.continuous` and
`isClosed_Iic.preimage`.
-/
theorem canonicalNonpositiveHalfspace_isClosed (A : NumericalCurveClassApiSketch.{u}) :
    IsClosed A.canonicalNonpositiveHalfspace := by
  unfold canonicalNonpositiveHalfspace
  exact isClosed_Iic.preimage A.canonicalIntersection.continuous

/--
Human-readable C003 diagnosis, kept in Lean so the child ledger can point to a
checked artifact rather than an unvalidated prose-only sketch.
-/
def numericalCurveClassApiDiagnosis : String :=
  "C003 maps N1 to an R-vector-space/topological-space carrier, effective curve classes to ConvexCone ℝ N1, the Mori cone to ConvexCone.closure / Set.closure, and K-intersection halfspaces to ContinuousLinearMap plus closed-set preimage APIs; numerical equivalence and algebraic cycle construction remain formalization debt"

end NumericalCurveClassApiSketch

/-! ## Divisor / Picard / class-group / canonical-divisor infrastructure audit -/

/-!
Child `S1-M-039-C004` audits the infrastructure needed for the Q-factorial/klt
branch. The positive rows below are checked mathlib anchors; the negative rows
record that those anchors are still ring-level or analytic, not yet the
scheme-level MMP objects required by Mori's cone theorem.
-/

/-- Status assigned to each C004 infrastructure row. -/
inductive MmpInfrastructureStatus where
  | checkedPositiveAnchor
  | presentButWrongLevelForMmp
  | missingMmpApi
deriving DecidableEq, Repr

/-- One audited API family for the Q-factorial/klt branch. -/
structure MmpInfrastructureAuditRow where
  code : String
  apiFamily : String
  checkedAnchor : String
  mathlibModule : String
  status : MmpInfrastructureStatus
  diagnosis : String
  deriving DecidableEq, Repr

/-- Child `S1-M-039-C004` audit date. -/
def mmpInfrastructureAuditDate : String := "2026-05-01"

/--
The C004 infrastructure audit.

Conclusion: mathlib has useful substrate for schemes, noetherian/proper
morphisms, ring-level Picard groups, Dedekind-domain class groups, fractional
ideals, and analytic meromorphic divisors. It does not yet provide the
scheme-level Weil/Cartier/`ℚ`-Cartier divisor stack needed to state
normal `ℚ`-factorial varieties, klt pairs, canonical divisors, discrepancies,
or log canonical thresholds in the Mori-program form.
-/
def mmpInfrastructureAuditRows : List MmpInfrastructureAuditRow := [
  {
    code := "MMP-INFRA-01"
    apiFamily := "scheme and morphism substrate"
    checkedAnchor :=
      "AlgebraicGeometry.Scheme; AlgebraicGeometry.IsNoetherian; AlgebraicGeometry.IsProper"
    mathlibModule :=
      "Mathlib.AlgebraicGeometry.Noetherian; Mathlib.AlgebraicGeometry.Morphisms.Proper"
    status := MmpInfrastructureStatus.checkedPositiveAnchor
    diagnosis :=
      "Schemes, noetherian schemes, and proper morphisms are available and already used in the statement scaffold."
  },
  {
    code := "MMP-INFRA-02"
    apiFamily := "Picard group"
    checkedAnchor := "CommRing.Pic; CommRing.Pic.mapAlgebra; CommRing.relPic"
    mathlibModule := "Mathlib.RingTheory.PicardGroup"
    status := MmpInfrastructureStatus.presentButWrongLevelForMmp
    diagnosis :=
      "The available Picard group is the ring-level group of invertible modules, not a scheme Picard functor or divisor-class API for projective varieties."
  },
  {
    code := "MMP-INFRA-03"
    apiFamily := "ideal class group and Picard comparison"
    checkedAnchor := "ClassGroup; ClassGroup.mk; ClassGroup.equivPic"
    mathlibModule := "Mathlib.RingTheory.ClassGroup; Mathlib.RingTheory.PicardGroup"
    status := MmpInfrastructureStatus.presentButWrongLevelForMmp
    diagnosis :=
      "The class group API is Dedekind-domain/fractional-ideal infrastructure; it is not a Weil divisor class group for normal varieties."
  },
  {
    code := "MMP-INFRA-04"
    apiFamily := "meromorphic divisor"
    checkedAnchor := "MeromorphicOn.divisor"
    mathlibModule := "Mathlib.Analysis.Meromorphic.Divisor"
    status := MmpInfrastructureStatus.presentButWrongLevelForMmp
    diagnosis :=
      "Analytic meromorphic divisors are available for functions on subsets of a normed field, but they do not supply algebraic Weil or Cartier divisors on schemes."
  },
  {
    code := "MMP-INFRA-05"
    apiFamily := "Weil, Cartier, and Q-Cartier divisors on schemes"
    checkedAnchor := "none found in pinned mathlib source tree"
    mathlibModule := "missing"
    status := MmpInfrastructureStatus.missingMmpApi
    diagnosis :=
      "No scheme-level Weil divisor, Cartier divisor, Q-Cartier predicate, divisor class group, or Q-factorial variety API was found."
  },
  {
    code := "MMP-INFRA-06"
    apiFamily := "canonical divisor and klt-pair branch"
    checkedAnchor := "none found in pinned mathlib source tree"
    mathlibModule := "missing"
    status := MmpInfrastructureStatus.missingMmpApi
    diagnosis :=
      "No canonical divisor/sheaf bridge, discrepancy API, klt/log-canonical pair structure, or MMP boundary divisor infrastructure was found."
  }
]

/-- The C004 infrastructure audit records six rows. -/
theorem mmpInfrastructureAuditRows_length :
    mmpInfrastructureAuditRows.length = 6 :=
  rfl

/-- Positive checked anchors are present but insufficient for the Q-factorial/klt branch. -/
theorem mmpInfrastructureAuditRows_statuses :
    mmpInfrastructureAuditRows.map MmpInfrastructureAuditRow.status =
      [ MmpInfrastructureStatus.checkedPositiveAnchor,
        MmpInfrastructureStatus.presentButWrongLevelForMmp,
        MmpInfrastructureStatus.presentButWrongLevelForMmp,
        MmpInfrastructureStatus.presentButWrongLevelForMmp,
        MmpInfrastructureStatus.missingMmpApi,
        MmpInfrastructureStatus.missingMmpApi ] :=
  rfl

/--
Human-readable C004 diagnosis. This is an infrastructure audit result, not a
completion claim for Mori's cone theorem.
-/
def mmpInfrastructureAuditDiagnosis : String :=
  "C004 finds checked mathlib substrate for schemes/proper/noetherian morphisms plus ring-level Picard/class-group and analytic meromorphic-divisor APIs, but not the scheme-level Weil/Cartier/Q-Cartier divisors, canonical divisors, discrepancies, klt pairs, or Q-factorial predicates required for the Mori cone theorem Q-factorial/klt branch; the branch remains formalization_debt, not repo-local completed"

/-! ## Cone theorem statement-file split plan -/

/-!
Child `S1-M-039-C005` is a statement-splitting task. The requested public
outcome is a serial blueprint/todo update plus future independent Lean statement
files; this worker owns only the current scoped artifact, so it records the
split as checked declaration-level metadata and exposes the three component
statement shapes without claiming that the future files already exist.
-/

/-- Components that should become independent statement files before proof work. -/
inductive MoriConeStatementComponent where
  | sharedHypothesesAndData
  | coneDecomposition
  | localFiniteness
  | contractionTheorem
deriving DecidableEq, Repr

/-- One proposed future file in the C005 statement split. -/
structure MoriConeStatementFileSplitRow where
  component : MoriConeStatementComponent
  proposedModulePath : String
  exportedDeclaration : String
  dependsOnlyOn : List String
  currentRepoStatus : String
  blockerBeforeCreation : String
  deriving DecidableEq, Repr

/--
Cone-decomposition component of the Mori cone theorem.

This bundles countability of negative extremal rays with the cone
decomposition formula, because the usual decomposition statement quantifies
over the same ray family.
-/
def ConeDecompositionStatementShape : Prop :=
  ∀ D : MoriConeStatementData.{u},
    MoriConeHypotheses D →
      D.countablyManyNegativeRays ∧ D.coneDecomposition

/-- Local-finiteness component of the Mori cone theorem. -/
def LocalFinitenessStatementShape : Prop :=
  ∀ D : MoriConeStatementData.{u},
    MoriConeHypotheses D →
      D.localFinitenessInNegativeHalfspace

/-- Contraction-theorem component of the Mori cone theorem. -/
def ContractionTheoremStatementShape : Prop :=
  ∀ D : MoriConeStatementData.{u},
    MoriConeHypotheses D →
      D.contractionForEveryNegativeExtremalRay

/--
The current combined statement shape is exactly equivalent to the three
component statement shapes. This is only a decomposition of the target
proposition, not a proof of any component.
-/
theorem statementShape_iff_componentStatementShapes :
    StatementShape.{u} ↔
      ConeDecompositionStatementShape.{u} ∧
        LocalFinitenessStatementShape.{u} ∧
          ContractionTheoremStatementShape.{u} := by
  constructor
  · intro h
    constructor
    · intro D hD
      exact ⟨(h D hD).1, (h D hD).2.1⟩
    · constructor
      · intro D hD
        exact (h D hD).2.2.1
      · intro D hD
        exact (h D hD).2.2.2
  · intro h D hD
    exact ⟨(h.1 D hD).1, (h.1 D hD).2, h.2.1 D hD, h.2.2 D hD⟩

/--
Integration-ready future file split for the public Stage1 surface.

The rows intentionally include a shared data/hypotheses file: independent
component statement files should import a common scaffold rather than duplicate
the MMP-specific placeholder fields.
-/
def moriConeStatementFileSplitRows : List MoriConeStatementFileSplitRow := [
  {
    component := MoriConeStatementComponent.sharedHypothesesAndData
    proposedModulePath := "AwesomeTheorems/Stage1/S1_M_039/Common.lean"
    exportedDeclaration := "MoriConeStatementData; MoriConeHypotheses"
    dependsOnlyOn := [
      "Mathlib.AlgebraicGeometry.Morphisms.Proper",
      "Mathlib.AlgebraicGeometry.Noetherian"
    ]
    currentRepoStatus :=
      "scaffold exists in S1_M_039.lean only; no independent file created by this child"
    blockerBeforeCreation :=
      "requires serial public-module creation outside this worker's owned write scope"
  },
  {
    component := MoriConeStatementComponent.coneDecomposition
    proposedModulePath := "AwesomeTheorems/Stage1/S1_M_039/ConeDecomposition.lean"
    exportedDeclaration := "ConeDecompositionStatementShape"
    dependsOnlyOn := [
      "AwesomeTheorems/Stage1/S1_M_039/Common.lean",
      "future NumericalCurveClass / N1 API"
    ]
    currentRepoStatus :=
      "component proposition is checked in S1_M_039.lean; terminal proof remains formalization_debt"
    blockerBeforeCreation :=
      "requires concrete N1, Mori cone closure, negative extremal ray, and cone-sum APIs"
  },
  {
    component := MoriConeStatementComponent.localFiniteness
    proposedModulePath := "AwesomeTheorems/Stage1/S1_M_039/LocalFiniteness.lean"
    exportedDeclaration := "LocalFinitenessStatementShape"
    dependsOnlyOn := [
      "AwesomeTheorems/Stage1/S1_M_039/Common.lean",
      "AwesomeTheorems/Stage1/S1_M_039/ConeDecomposition.lean"
    ]
    currentRepoStatus :=
      "component proposition is checked in S1_M_039.lean; local-finiteness topology proof remains formalization_debt"
    blockerBeforeCreation :=
      "requires topology on N1, closed halfspaces, locally finite ray families, and the cone-decomposition ray indexing API"
  },
  {
    component := MoriConeStatementComponent.contractionTheorem
    proposedModulePath := "AwesomeTheorems/Stage1/S1_M_039/Contraction.lean"
    exportedDeclaration := "ContractionTheoremStatementShape"
    dependsOnlyOn := [
      "AwesomeTheorems/Stage1/S1_M_039/Common.lean",
      "AwesomeTheorems/Stage1/S1_M_039/ConeDecomposition.lean"
    ]
    currentRepoStatus :=
      "component proposition is checked in S1_M_039.lean; contraction theorem proof remains formalization_debt"
    blockerBeforeCreation :=
      "requires extremal-face contraction target, morphism construction, curve-contraction iff condition, and projectivity/properness preservation APIs"
  }
]

/-- The C005 split plan has one shared scaffold row and three theorem-component rows. -/
theorem moriConeStatementFileSplitRows_length :
    moriConeStatementFileSplitRows.length = 4 :=
  rfl

/-- The C005 split rows are ordered by common scaffold, decomposition, finiteness, contraction. -/
theorem moriConeStatementFileSplitRows_components :
    moriConeStatementFileSplitRows.map MoriConeStatementFileSplitRow.component =
      [ MoriConeStatementComponent.sharedHypothesesAndData,
        MoriConeStatementComponent.coneDecomposition,
        MoriConeStatementComponent.localFiniteness,
        MoriConeStatementComponent.contractionTheorem ] :=
  rfl

/--
C005 completion-boundary diagnosis: the split is checked as metadata and
component statement shapes, while future public files remain an open
integration task.
-/
def moriConeStatementFileSplitDiagnosis : String :=
  "C005 decomposes StatementShape into checked cone-decomposition, local-finiteness, and contraction-theorem component propositions and records four future module rows; no independent public Lean files were created in this worker, and the theorem remains formalization_debt / not_repo_local_closed"

/-! ## External proof pin/import/check gate -/

/-!
Child `S1-M-039-C006` is the M0387 repo-local integration gate for any
external Lean 4 proof of Mori's cone theorem. The current C001 audit rows do
not contain a pin-ready external proof, so this section records the concrete
blocker instead of converting anchor-only evidence into a completion claim.
-/

/-- C006 integration decision status for an external proof candidate. -/
inductive ExternalProofIntegrationStatus where
  | noPinReadyCandidate
  | blockedByMissingAuthenticatedSearch
  | mustPinImportCheckBeforeCompletion
deriving DecidableEq, Repr

/-- One repo-local gate row for the external-proof integration decision. -/
structure ExternalProofIntegrationGateRow where
  code : String
  sourceEvidence : String
  integrationDecision : ExternalProofIntegrationStatus
  concreteBlocker : String
  repoLocalCompletionAllowed : Bool
  deriving DecidableEq, Repr

/-- Date for the C006 external-proof integration gate. -/
def externalProofIntegrationGateDate : String := "2026-05-01"

/--
Child `S1-M-039-C006` integration gate rows.

No row allows repo-local completion: the current audit has no pin-ready Lean 4
proof candidate, and the remaining global code-search route requires
authentication or an equivalent primary-source search before absence can be
treated as fully audited.
-/
def externalProofIntegrationGateRows : List ExternalProofIntegrationGateRow := [
  {
    code := "MORI-CONE-C006-01"
    sourceEvidence :=
      "C001 externalLeanAuditRows_no_pinReady over seven audit rows"
    integrationDecision :=
      ExternalProofIntegrationStatus.noPinReadyCandidate
    concreteBlocker :=
      "No current row supplies repository URL, commit SHA, module path, theorem declaration, Lean toolchain, and license for a Mori cone theorem proof; there is no safe external proof to pin/import/check from the current audit."
    repoLocalCompletionAllowed := false
  },
  {
    code := "MORI-CONE-C006-02"
    sourceEvidence :=
      "GitHub Lean code search for exact Mori cone theorem declarations"
    integrationDecision :=
      ExternalProofIntegrationStatus.blockedByMissingAuthenticatedSearch
    concreteBlocker :=
      "Authenticated GitHub code search or an equivalent primary-source code search is required; unauthenticated REST code search was blocked/rate-limited and gh has no authenticated GitHub host."
    repoLocalCompletionAllowed := false
  },
  {
    code := "MORI-CONE-C006-03"
    sourceEvidence :=
      "Future external Lean 4 proof candidate, if one is discovered"
    integrationDecision :=
      ExternalProofIntegrationStatus.mustPinImportCheckBeforeCompletion
    concreteBlocker :=
      "Any future candidate must be added as a pinned Lake dependency, vendored dependency, or repo-local wrapper and validated with lake env lean; if integration fails, record the exact dependency, toolchain, or license blocker."
    repoLocalCompletionAllowed := false
  }
]

/-- The C006 integration gate records three rows. -/
theorem externalProofIntegrationGateRows_length :
    externalProofIntegrationGateRows.length = 3 :=
  rfl

/-- The current C006 rows are ordered by no-candidate, search blocker, future-candidate rule. -/
theorem externalProofIntegrationGateRows_decisions :
    externalProofIntegrationGateRows.map ExternalProofIntegrationGateRow.integrationDecision =
      [ ExternalProofIntegrationStatus.noPinReadyCandidate,
        ExternalProofIntegrationStatus.blockedByMissingAuthenticatedSearch,
        ExternalProofIntegrationStatus.mustPinImportCheckBeforeCompletion ] :=
  rfl

/-- No current C006 row permits a repo-local completion claim. -/
theorem externalProofIntegrationGateRows_no_completion :
    externalProofIntegrationGateRows.map ExternalProofIntegrationGateRow.repoLocalCompletionAllowed =
      [false, false, false] :=
  rfl

/--
C006 diagnosis for public backfill. This records a blocker/gate, not a proof of
Mori's cone theorem and not an anchor-only completion.
-/
def externalProofIntegrationGateDiagnosis : String :=
  "C006 records that no discovered Lean 4 Mori cone theorem proof is currently pin-ready; authenticated code search remains a concrete audit blocker, and any future external proof must be pinned/imported/checked or blocked by exact dependency/toolchain/license reasons before completion"

#check externalLeanAuditDate
#check ExternalLeanAuditRow
#check externalLeanAuditRows
#check externalLeanAuditRows_length
#check externalLeanAuditRows_no_pinReady
#check externalLeanAuditStatus
#check repoLocalIntegrationDebtGate
#check PublicStatementTarget
#check chosenPublicStatementTarget
#check chosenPublicStatementTarget_eq_relativeProjectiveKltPair
#check RelativeProjectiveKltPairStatementShape
#check relativeProjectiveKltPairStatementShape_iff_statementShape
#check statementTargetDecisionDiagnosis
#check NumericalCurveClassApiSketch
#check NumericalCurveClassApiSketch.moriCone
#check NumericalCurveClassApiSketch.moriConeSet
#check NumericalCurveClassApiSketch.mem_moriCone_iff_mem_closure
#check NumericalCurveClassApiSketch.curveClass_mem_effective
#check NumericalCurveClassApiSketch.curveClass_mem_moriCone
#check NumericalCurveClassApiSketch.canonicalNegativeHalfspace
#check NumericalCurveClassApiSketch.canonicalNonpositiveHalfspace
#check NumericalCurveClassApiSketch.canonicalNonpositiveHalfspace_isClosed
#check NumericalCurveClassApiSketch.numericalCurveClassApiDiagnosis
#check AlgebraicGeometry.Scheme
#check AlgebraicGeometry.IsNoetherian
#check AlgebraicGeometry.IsProper
#check CommRing.Pic
#check CommRing.Pic.mapAlgebra
#check CommRing.relPic
#check ClassGroup
#check ClassGroup.mk
#check ClassGroup.equivPic
#check MeromorphicOn.divisor
#check MmpInfrastructureStatus
#check MmpInfrastructureAuditRow
#check mmpInfrastructureAuditDate
#check mmpInfrastructureAuditRows
#check mmpInfrastructureAuditRows_length
#check mmpInfrastructureAuditRows_statuses
#check mmpInfrastructureAuditDiagnosis
#check MoriConeStatementComponent
#check MoriConeStatementFileSplitRow
#check ConeDecompositionStatementShape
#check LocalFinitenessStatementShape
#check ContractionTheoremStatementShape
#check statementShape_iff_componentStatementShapes
#check moriConeStatementFileSplitRows
#check moriConeStatementFileSplitRows_length
#check moriConeStatementFileSplitRows_components
#check moriConeStatementFileSplitDiagnosis
#check ExternalProofIntegrationStatus
#check ExternalProofIntegrationGateRow
#check externalProofIntegrationGateDate
#check externalProofIntegrationGateRows
#check externalProofIntegrationGateRows_length
#check externalProofIntegrationGateRows_decisions
#check externalProofIntegrationGateRows_no_completion
#check externalProofIntegrationGateDiagnosis

end AwesomeTheorems.Stage1.S1_M_039
