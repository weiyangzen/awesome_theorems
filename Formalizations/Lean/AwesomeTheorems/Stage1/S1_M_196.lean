import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.Geometry.Manifold.VectorBundle.Tensoriality
import Mathlib.LinearAlgebra.BilinearMap

/-!
# S1-M-196 / THM-M-1528: Einstein field equations

This Stage1 artifact records a conservative Lean 4 boundary for the Einstein
field equations of general relativity.

The pinned mathlib snapshot has smooth-manifold, tangent-bundle,
covariant-derivative, Riemannian-metric, and finite-dimensional linear-algebra
infrastructure.  It does not expose terminal APIs for Lorentzian metrics, Ricci
curvature, scalar curvature, Einstein tensors, stress-energy tensors, or the
Einstein field equations as tensor equations on spacetime.  The declarations
below therefore split the task into:

* a checked pointwise algebraic tensor-equation wrapper using curried
  covariant 2-tensors over a real vector space; and
* an abstract manifold-level statement shape whose missing geometric/PDE
  objects are isolated as explicit proposition fields.

No proof of the terminal Einstein field equations is claimed here.
-/

noncomputable section

open Bundle Manifold
open scoped Manifold ContDiff Topology

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_196

/-- Pointwise covariant 2-tensors, modeled as curried real-linear maps. -/
abbrev CovariantTwoTensor (V : Type u) [AddCommGroup V] [Module ℝ V] : Type u :=
  V →ₗ[ℝ] V →ₗ[ℝ] ℝ

/--
Pointwise Einstein tensor algebra:

`G = Ric - (R / 2) g`.

This is only the algebraic tensor expression at a point.  It does not construct
the Ricci tensor or scalar curvature from a Lorentzian connection.
-/
def EinsteinTensorAt {V : Type u} [AddCommGroup V] [Module ℝ V]
    (metric ricci : CovariantTwoTensor V) (scalarCurvature : ℝ) :
    CovariantTwoTensor V :=
  ricci - (scalarCurvature / 2 : ℝ) • metric

/--
Pointwise Einstein field equation with cosmological constant:

`G + Lambda g = kappa T`.

This is a checked algebraic statement shape over already-supplied tensor
objects.
-/
def EinsteinFieldEquationAt {V : Type u} [AddCommGroup V] [Module ℝ V]
    (metric ricci stressEnergy : CovariantTwoTensor V)
    (scalarCurvature cosmologicalConstant couplingConstant : ℝ) : Prop :=
  EinsteinTensorAt metric ricci scalarCurvature + cosmologicalConstant • metric =
    couplingConstant • stressEnergy

/-- Input package for the pointwise algebraic Einstein field equation. -/
structure PointwiseEinsteinData (V : Type u) [AddCommGroup V] [Module ℝ V] :
    Type u where
  metric : CovariantTwoTensor V
  ricci : CovariantTwoTensor V
  stressEnergy : CovariantTwoTensor V
  scalarCurvature : ℝ
  cosmologicalConstant : ℝ
  couplingConstant : ℝ

/-- The pointwise equation associated to a pointwise data package. -/
def PointwiseEinsteinData.Equation {V : Type u} [AddCommGroup V] [Module ℝ V]
    (X : PointwiseEinsteinData V) : Prop :=
  EinsteinFieldEquationAt X.metric X.ricci X.stressEnergy X.scalarCurvature
    X.cosmologicalConstant X.couplingConstant

/-- Checked wrapper: unfold the equation carried by a pointwise data package. -/
theorem PointwiseEinsteinData.equation_iff
    {V : Type u} [AddCommGroup V] [Module ℝ V]
    (X : PointwiseEinsteinData V) :
    X.Equation ↔
      X.ricci - (X.scalarCurvature / 2 : ℝ) • X.metric +
          X.cosmologicalConstant • X.metric =
        X.couplingConstant • X.stressEnergy :=
  Iff.rfl

/-- Checked wrapper: unfold the algebraic pointwise Einstein tensor definition. -/
theorem EinsteinTensorAt_eq {V : Type u} [AddCommGroup V] [Module ℝ V]
    (metric ricci : CovariantTwoTensor V) (scalarCurvature : ℝ) :
    EinsteinTensorAt metric ricci scalarCurvature =
      ricci - (scalarCurvature / 2 : ℝ) • metric :=
  rfl

/-- Checked wrapper: unfold the pointwise Einstein field equation. -/
theorem EinsteinFieldEquationAt_iff {V : Type u} [AddCommGroup V] [Module ℝ V]
    (metric ricci stressEnergy : CovariantTwoTensor V)
    (scalarCurvature cosmologicalConstant couplingConstant : ℝ) :
    EinsteinFieldEquationAt metric ricci stressEnergy scalarCurvature
        cosmologicalConstant couplingConstant ↔
      ricci - (scalarCurvature / 2 : ℝ) • metric +
          cosmologicalConstant • metric =
        couplingConstant • stressEnergy :=
  Iff.rfl

/--
Checked wrapper: in the vacuum, zero-cosmological-constant specialization, the
pointwise equation reduces to vanishing of the pointwise Einstein tensor.
-/
theorem EinsteinFieldEquationAt_vacuum_zeroLambda_iff
    {V : Type u} [AddCommGroup V] [Module ℝ V]
    (metric ricci : CovariantTwoTensor V)
    (scalarCurvature couplingConstant : ℝ) :
    EinsteinFieldEquationAt metric ricci 0 scalarCurvature 0 couplingConstant ↔
      EinsteinTensorAt metric ricci scalarCurvature = 0 := by
  simp [EinsteinFieldEquationAt]

/--
Abstract spacetime data for a future manifold-level formalization of the
Einstein field equations.

The current local dependency closure can state that the carrier is a smooth
manifold.  The Lorentzian metric, Levi-Civita connection, Ricci contraction,
scalar curvature, stress-energy tensor, and divergence/Bianchi package are kept
as explicit proposition fields because mathlib does not yet provide the needed
Lorentzian tensor API in this snapshot.
-/
structure EinsteinSpacetimeData (M : Type w) [TopologicalSpace M] :
    Type (w + 1) where
  tensorCarrier : Type w
  metric : tensorCarrier
  inverseMetric : tensorCarrier
  connection : tensorCarrier
  ricciTensor : tensorCarrier
  scalarCurvature : ℝ
  stressEnergyTensor : tensorCarrier
  cosmologicalConstant : ℝ
  couplingConstant : ℝ
  einsteinTensor : tensorCarrier
  lorentzianMetric : Prop
  leviCivitaConnection : Prop
  ricciTensorFromCurvature : Prop
  scalarCurvatureIsTrace : Prop
  einsteinTensorDefinition : Prop
  stressEnergyModel : Prop
  tensorEquationWellTyped : Prop
  contractedBianchiIdentity : Prop
  stressEnergyConservationCompatible : Prop
  fieldEquation : Prop

/-- Hypotheses side of the normalized manifold-level Einstein-equation shape. -/
def EinsteinSpacetimeHypotheses {M : Type w} [TopologicalSpace M]
    (X : EinsteinSpacetimeData M) : Prop :=
  X.lorentzianMetric ∧
    X.leviCivitaConnection ∧
      X.ricciTensorFromCurvature ∧
        X.scalarCurvatureIsTrace ∧
          X.einsteinTensorDefinition ∧
            X.stressEnergyModel ∧
              X.tensorEquationWellTyped ∧
                X.contractedBianchiIdentity ∧
                  X.stressEnergyConservationCompatible

/-- Conclusion package for the manifold-level Einstein field equation. -/
structure EinsteinFieldEquationConclusion {M : Type w} [TopologicalSpace M]
    (X : EinsteinSpacetimeData M) : Type w where
  fieldEquation_holds : X.fieldEquation

/--
Stage1 normalized statement shape for THM-M-1528.

For any smooth spacetime carrier and any explicit Lorentzian/tensor model data,
if the geometric construction package is supplied, the intended terminal
formalization should produce the Einstein field equation
`G + Lambda g = kappa T`.  This is a proposition boundary, not a terminal proof.
-/
def StatementShape : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type v) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type w) [TopologicalSpace M] [ChartedSpace H M],
      IsManifold I ∞ M →
        ∀ X : EinsteinSpacetimeData M,
          EinsteinSpacetimeHypotheses X →
            Nonempty (EinsteinFieldEquationConclusion X)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      (H : Type v) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
      (M : Type w) [TopologicalSpace M] [ChartedSpace H M],
        IsManifold I ∞ M →
          ∀ X : EinsteinSpacetimeData M,
            EinsteinSpacetimeHypotheses X →
              Nonempty (EinsteinFieldEquationConclusion X)) :
    StatementShape.{u, v, w} :=
  h

/-- A conclusion package exposes the manifold-level field-equation proposition. -/
theorem EinsteinFieldEquationConclusion.fieldEquation
    {M : Type w} [TopologicalSpace M] {X : EinsteinSpacetimeData M}
    (C : EinsteinFieldEquationConclusion X) :
    X.fieldEquation :=
  C.fieldEquation_holds

/-- Checked Riemannian substrate: inner-product vector spaces carry mathlib metrics. -/
def riemannianMetricVectorSpace_anchor
    (F : Type u) [NormedAddCommGroup F] [InnerProductSpace ℝ F] :
    ContMDiffRiemannianMetric 𝓘(ℝ, F) ω F
      (fun x : F => TangentSpace 𝓘(ℝ, F) x) :=
  riemannianMetricVectorSpace F

/-! ## Audit probes retained in the checked file. -/

#check CovariantTwoTensor
#check EinsteinTensorAt
#check EinsteinFieldEquationAt
#check EinsteinFieldEquationAt_vacuum_zeroLambda_iff
#check EinsteinSpacetimeData
#check EinsteinSpacetimeHypotheses
#check EinsteinFieldEquationConclusion
#check StatementShape
#check ModelWithCorners
#check IsManifold
#check TangentSpace
#check CovariantDerivative
#check IsCovariantDerivativeOn
#check ContMDiffRiemannianMetric
#check riemannianMetricVectorSpace
#check riemannianMetricVectorSpace_anchor

/-- The pinned mathlib revision audited for this Stage1 slot. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tensoriality",
  "Mathlib.LinearAlgebra.BilinearMap"
]

/--
Exact public-task module subset for `S1-M-196-PUB-002`.

These modules provide manifold, Riemannian, covariant-derivative,
tensoriality, and bilinear/linear-map substrate anchors at the pinned revision.
They do not provide a terminal Lean definition of the Einstein field equations.
-/
def publicTaskMathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tensoriality",
  "Mathlib.LinearAlgebra.BilinearMap"
]

/-- Checked normalization of the pinned revision string for the public audit. -/
theorem mathlibPinnedRevision_eq :
    mathlibPinnedRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Checked normalization of the exact public-task module audit list. -/
theorem publicTaskMathlibAnchorModules_eq :
    publicTaskMathlibAnchorModules = [
      "Mathlib.Geometry.Manifold.Riemannian.Basic",
      "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
      "Mathlib.Geometry.Manifold.VectorBundle.Tensoriality",
      "Mathlib.LinearAlgebra.BilinearMap"
    ] :=
  rfl

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ModelWithCorners",
  "IsManifold",
  "TangentSpace",
  "CovariantDerivative",
  "IsCovariantDerivativeOn",
  "ContMDiffRiemannianMetric",
  "riemannianMetricVectorSpace",
  "LinearMap",
  "CovariantTwoTensor",
  "EinsteinTensorAt",
  "EinsteinFieldEquationAt"
]

/--
Search terms that did not locate terminal Einstein-field-equation definitions
or theorems in the local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "EinsteinTensor",
  "EinsteinFieldEquation",
  "RicciTensor",
  "ScalarCurvature",
  "LorentzianMetric",
  "StressEnergyTensor",
  "Bianchi"
]

/-- Checked normalization of the absent terminal-search-term audit list. -/
theorem absentTerminalSearchTerms_eq :
    absentTerminalSearchTerms = [
      "EinsteinTensor",
      "EinsteinFieldEquation",
      "RicciTensor",
      "ScalarCurvature",
      "LorentzianMetric",
      "StressEnergyTensor",
      "Bianchi"
    ] :=
  rfl

/--
The theorem-tree packages proposed for the public Stage1 follow-up surface.

These are metadata anchors for the M0387-style package split.  They do not
assert that the terminal Lorentzian Einstein field equation has been proved.
-/
def theoremTreePackageIds : List String := [
  "EFE-PKG-001",
  "EFE-PKG-002",
  "EFE-PKG-003",
  "EFE-PKG-004",
  "EFE-PKG-005",
  "EFE-PKG-006"
]

/-- Checked normalization of the public theorem-tree package ids. -/
theorem theoremTreePackageIds_eq :
    theoremTreePackageIds = [
      "EFE-PKG-001",
      "EFE-PKG-002",
      "EFE-PKG-003",
      "EFE-PKG-004",
      "EFE-PKG-005",
      "EFE-PKG-006"
    ] :=
  rfl

/-- Leaf metadata for the public theorem-tree package split. -/
structure TheoremTreeLeaf where
  id : String
  packageId : String
  localBudget : Nat
  status : String
  note : String

/--
M0387-style theorem-tree leaves for the Einstein-field-equation Stage1 slot.

Every listed local budget is at most `100`.  Leaves marked `unchecked` are not
closed by this repo-local Lean artifact and must keep the public slot open.
-/
def theoremTreeLeaves : List TheoremTreeLeaf := [
  ⟨"EFE-L001", "EFE-PKG-001", 20, "checked",
    "Normalize G = Ric - (R / 2) g in EinsteinTensorAt."⟩,
  ⟨"EFE-L002", "EFE-PKG-001", 20, "checked",
    "Normalize G + Lambda g = kappa T in EinsteinFieldEquationAt."⟩,
  ⟨"EFE-L003", "EFE-PKG-003", 20, "checked",
    "EinsteinTensorAt_eq unfolds by rfl."⟩,
  ⟨"EFE-L004", "EFE-PKG-003", 20, "checked",
    "EinsteinFieldEquationAt_iff unfolds by Iff.rfl."⟩,
  ⟨"EFE-L005", "EFE-PKG-003", 30, "checked",
    "Vacuum zero-Lambda wrapper closes by simp."⟩,
  ⟨"EFE-L006", "EFE-PKG-002", 20, "checked",
    "riemannianMetricVectorSpace_anchor compiles against mathlib."⟩,
  ⟨"EFE-L007", "EFE-PKG-004", 30, "checked",
    "StatementShape.intro is a low-risk introduction wrapper only."⟩,
  ⟨"EFE-L008", "EFE-PKG-004", 20, "checked",
    "EinsteinFieldEquationConclusion.fieldEquation projection wrapper."⟩,
  ⟨"EFE-L009", "EFE-PKG-002", 80, "unchecked",
    "Replace abstract lorentzianMetric with a concrete Lorentzian metric API."⟩,
  ⟨"EFE-L010", "EFE-PKG-002", 80, "unchecked",
    "Define Levi-Civita connection for Lorentzian metrics."⟩,
  ⟨"EFE-L011", "EFE-PKG-002", 80, "unchecked",
    "Define curvature tensor and Ricci contraction."⟩,
  ⟨"EFE-L012", "EFE-PKG-002", 80, "unchecked",
    "Define scalar curvature as trace of Ricci against inverse metric."⟩,
  ⟨"EFE-L013", "EFE-PKG-004", 80, "unchecked",
    "Replace abstract stressEnergyModel with concrete stress-energy assumptions."⟩,
  ⟨"EFE-L014", "EFE-PKG-004", 80, "unchecked",
    "Formalize tensor typing of G + Lambda g = kappa T on spacetime."⟩,
  ⟨"EFE-L015", "EFE-PKG-004", 80, "unchecked",
    "Add contracted Bianchi identity in the chosen Lorentzian API."⟩,
  ⟨"EFE-L016", "EFE-PKG-004", 80, "unchecked",
    "Connect Bianchi identity to stress-energy conservation compatibility."⟩,
  ⟨"EFE-L017", "EFE-PKG-005", 60, "unchecked",
    "Authenticated GitHub code search for exact Lean identifiers."⟩,
  ⟨"EFE-L018", "EFE-PKG-005", 60, "unchecked",
    "If external Lean 4 closure exists, pin/import/check or record blocker."⟩,
  ⟨"EFE-L019", "EFE-PKG-006", 60, "unchecked",
    "Public blueprint/todo merge-back by integrator."⟩,
  ⟨"EFE-L020", "EFE-PKG-006", 40, "unchecked",
    "Final Stage1 completion gate audit."⟩
]

/-- Checked normalization of the unchecked theorem-tree leaf ids. -/
def uncheckedTheoremTreeLeafIds : List String := [
  "EFE-L009",
  "EFE-L010",
  "EFE-L011",
  "EFE-L012",
  "EFE-L013",
  "EFE-L014",
  "EFE-L015",
  "EFE-L016",
  "EFE-L017",
  "EFE-L018",
  "EFE-L019",
  "EFE-L020"
]

/-- Checked normalization of the public unchecked leaf id list. -/
theorem uncheckedTheoremTreeLeafIds_eq :
    uncheckedTheoremTreeLeafIds = [
      "EFE-L009",
      "EFE-L010",
      "EFE-L011",
      "EFE-L012",
      "EFE-L013",
      "EFE-L014",
      "EFE-L015",
      "EFE-L016",
      "EFE-L017",
      "EFE-L018",
      "EFE-L019",
      "EFE-L020"
    ] :=
  rfl

/-- Boolean audit that all public theorem-tree leaf budgets are at most `100`. -/
theorem theoremTreeLeaves_budget_all_le_100 :
    theoremTreeLeaves.all (fun leaf => leaf.localBudget <= 100) = true :=
  rfl

/-- Completion prerequisites for `S1-M-196-PUB-005`. -/
structure CompletionPrerequisites where
  concreteLorentzianTensorApiAvailable : Bool
  compatibleExternalPackagePinnedImportedChecked : Bool

/--
The C005 gate permits terminal completion only after a concrete Lorentzian/tensor
API is available locally or a compatible external Lean 4 package has been
pinned, imported, and checked in this repo.
-/
def completionPrerequisitesMet (G : CompletionPrerequisites) : Bool :=
  G.concreteLorentzianTensorApiAvailable ||
    G.compatibleExternalPackagePinnedImportedChecked

/--
Current C005 audit state: neither completion prerequisite is satisfied by the
repo-local closure checked in this file.
-/
def c005CompletionPrerequisites : CompletionPrerequisites where
  concreteLorentzianTensorApiAvailable := false
  compatibleExternalPackagePinnedImportedChecked := false

/-- Checked C005 gate result: S1-M-196 must remain open in this repo state. -/
theorem c005CompletionPrerequisites_not_met :
    completionPrerequisitesMet c005CompletionPrerequisites = false :=
  rfl

/--
Machine-status vocabulary for the repo-local completion gate.

Only statuses whose proof body or upstream dependency is inside the local
checked closure may count as completed for this Stage1 slot.
-/
inductive RepoLocalClosureStatus where
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  | notRepoLocalClosed
  deriving DecidableEq, Repr

/-- Whether a machine-status value is allowed to count as repo-local completed. -/
def RepoLocalClosureStatus.countsAsCompleted : RepoLocalClosureStatus → Bool
  | .localProofBody => true
  | .localWrapperUpstreamMathlib => true
  | .externalUpstreamPinned => true
  | .externalUpstreamAnchorOnly => false
  | .notRepoLocalClosed => false

/-- C006 gate fact: anchor-only external evidence is not a completed state. -/
theorem externalAnchorOnly_not_completed :
    RepoLocalClosureStatus.externalUpstreamAnchorOnly.countsAsCompleted = false :=
  rfl

/-- C006 gate fact: an unclosed repo-local target is not a completed state. -/
theorem notRepoLocalClosed_not_completed :
    RepoLocalClosureStatus.notRepoLocalClosed.countsAsCompleted = false :=
  rfl

/--
Metadata for a future external Lean 4 Einstein-field-equation closure.

`pinnedImportedChecked` means the external closure has entered this repo's
Lean dependency closure and passed local checking.  `integrationBlocker` records
a concrete reason why pin/import/check cannot currently be done.
-/
structure ExternalClosureCandidate where
  repository : String
  commitOrRevision : String
  moduleOrTheorem : String
  pinnedImportedChecked : Bool
  integrationBlocker : Option String

/-- Whether an external candidate has a concrete recorded integration blocker. -/
def ExternalClosureCandidate.hasIntegrationBlocker
    (C : ExternalClosureCandidate) : Bool :=
  match C.integrationBlocker with
  | some _ => true
  | none => false

/--
C006 integration-debt gate for future external Lean 4 closure claims.

The gate is satisfied only when the external closure is checked in the
repo-local Lean dependency closure, or when a concrete integration blocker is
recorded while the Stage1 item remains open.
-/
def externalClosureIntegrationGateSatisfied
    (C : ExternalClosureCandidate) : Bool :=
  C.pinnedImportedChecked || C.hasIntegrationBlocker

/--
Current C006 audit state for S1-M-196: the repo has no pinned/imported/checked
external Lean 4 Einstein-field-equation package and no concrete blocker to a
specific candidate package.
-/
def c006CurrentExternalCandidate : ExternalClosureCandidate where
  repository := ""
  commitOrRevision := ""
  moduleOrTheorem := ""
  pinnedImportedChecked := false
  integrationBlocker := none

/--
Checked C006 gate result: the current anchor-only/no-candidate state is not
eligible for completion.
-/
theorem c006CurrentExternalCandidate_gate_not_satisfied :
    externalClosureIntegrationGateSatisfied c006CurrentExternalCandidate = false :=
  rfl

/--
Checked C006 completion state for this repo-local artifact.

The current Lean file is a statement-boundary artifact, not a completed terminal
formalization of the Lorentzian Einstein field equation.
-/
def c006CurrentClosureStatus : RepoLocalClosureStatus :=
  RepoLocalClosureStatus.notRepoLocalClosed

/-- Checked C006 state result: the current artifact is not repo-local completed. -/
theorem c006CurrentClosureStatus_not_completed :
    c006CurrentClosureStatus.countsAsCompleted = false :=
  rfl

#check mathlibPinnedRevision
#check publicTaskMathlibAnchorModules
#check mathlibPinnedRevision_eq
#check publicTaskMathlibAnchorModules_eq
#check absentTerminalSearchTerms
#check absentTerminalSearchTerms_eq
#check theoremTreePackageIds
#check theoremTreePackageIds_eq
#check theoremTreeLeaves
#check uncheckedTheoremTreeLeafIds
#check uncheckedTheoremTreeLeafIds_eq
#check theoremTreeLeaves_budget_all_le_100
#check CompletionPrerequisites
#check completionPrerequisitesMet
#check c005CompletionPrerequisites
#check c005CompletionPrerequisites_not_met
#check RepoLocalClosureStatus
#check RepoLocalClosureStatus.countsAsCompleted
#check externalAnchorOnly_not_completed
#check notRepoLocalClosed_not_completed
#check ExternalClosureCandidate
#check ExternalClosureCandidate.hasIntegrationBlocker
#check externalClosureIntegrationGateSatisfied
#check c006CurrentExternalCandidate
#check c006CurrentExternalCandidate_gate_not_satisfied
#check c006CurrentClosureStatus
#check c006CurrentClosureStatus_not_completed

end S1_M_196
end Stage1
end AwesomeTheorems
