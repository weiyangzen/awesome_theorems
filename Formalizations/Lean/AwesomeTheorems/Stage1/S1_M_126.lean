import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.Riemannian.PathELength
import Mathlib.Geometry.Manifold.VectorBundle.Riemannian
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion
import Mathlib.Geometry.Manifold.VectorField.LieBracket

/-!
# S1-M-126 / THM-M-0165: Morse index theorem

This Stage1 file records a conservative Lean 4 boundary for the Morse index
theorem for geodesics.  The pinned mathlib snapshot has substantial manifold,
Riemannian metric, path-length, tangent-bundle, covariant-derivative, and
torsion APIs.  This audit did not find terminal mathlib declarations for
geodesics as autoparallel curves, Jacobi fields, curvature along a geodesic,
conjugate-point multiplicities, the index form, or the Morse index theorem.

The declarations below therefore normalize the theorem's expected data and
conclusion without introducing placeholders.  The checked wrappers only expose
nearby mathlib facts that later formalization work can reuse.
-/

noncomputable section

open Bundle Manifold
open scoped Manifold ContDiff Topology ENNReal

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_126

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
  {H : Type v} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
  {M : Type w} [TopologicalSpace M] [ChartedSpace H M]

/--
Input data for a future formal Morse index theorem.

The fields that mathlib does not yet expose as ready-made structures in this
snapshot are kept as propositions or abstract objects:
`isGeodesicForLeviCivita`, `noEndpointConjugacy`, `variationSpace`,
`indexForm`, and the conjugate-point multiplicity package.
-/
structure GeodesicIndexProblem
    (I : ModelWithCorners ℝ E H) (M : Type w) [TopologicalSpace M] [ChartedSpace H M] :
    Type (max (max (u + 1) (v + 1)) (w + 2)) where
  startTime : ℝ
  endTime : ℝ
  start_lt_end : startTime < endTime
  curve : ℝ → M
  curve_smoothOn : ContMDiffOn 𝓘(ℝ) I ∞ curve (Set.Icc startTime endTime)
  isGeodesicForLeviCivita : Prop
  endpointsFixed : Prop
  noEndpointConjugacy : Prop
  variationSpace : Type (max u w)
  indexForm : variationSpace → variationSpace → ℝ
  indexForm_isSecondVariation : Prop
  morseIndex : ℕ
  conjugatePointMultiplicitySum : ℕ
  conjugatePointMultiplicitySum_countsInteriorJacobiFields : Prop

/--
Terminal data expected from a full Morse index theorem formalization.

Classically, for a nondegenerate geodesic segment, the index of the second
variation/index form on endpoint-fixed variations equals the sum of
conjugate-point multiplicities in the open interval.
-/
structure MorseIndexTheoremPackage
    (G : GeodesicIndexProblem I M) : Type (max u w) where
  index_eq_conjugatePointMultiplicitySum :
    G.morseIndex = G.conjugatePointMultiplicitySum
  indexFormSecondVariation : G.indexForm_isSecondVariation
  conjugateMultiplicityCountsJacobiFields :
    G.conjugatePointMultiplicitySum_countsInteriorJacobiFields

/--
Stage1 normalized statement shape for THM-M-0165.

This is intentionally only a proposition describing the future theorem.  It is
not a proof of the Morse index theorem.
-/
def StatementShape : Prop :=
  ∀ G : GeodesicIndexProblem I M,
    G.isGeodesicForLeviCivita →
      G.endpointsFixed →
        G.noEndpointConjugacy →
          Nonempty (MorseIndexTheoremPackage G)

/-- The statement shape unfolds to the nonemptiness of the terminal theorem package. -/
theorem statementShape_iff :
    StatementShape (I := I) (M := M) ↔
      ∀ G : GeodesicIndexProblem I M,
        G.isGeodesicForLeviCivita →
          G.endpointsFixed →
            G.noEndpointConjugacy →
              Nonempty (MorseIndexTheoremPackage G) :=
  Iff.rfl

/--
Checked wrapper: mathlib's `IsRiemannianManifold` class identifies the ambient
extended distance with `riemannianEDist`.
-/
theorem isRiemannianManifold_edist_eq_riemannianEDist
    [PseudoEMetricSpace M] [RiemannianBundle (fun x : M => TangentSpace I x)]
    [IsRiemannianManifold I M] (x y : M) :
    edist x y = riemannianEDist I x y := by
  exact IsRiemannianManifold.out x y

/-- Checked wrapper: mathlib proves zero Riemannian extended distance from a point to itself. -/
theorem riemannianEDist_self_wrapper
    [RiemannianBundle (fun x : M => TangentSpace I x)] (x : M) :
    riemannianEDist I x x = 0 := by
  exact riemannianEDist_self

/-- Checked wrapper: mathlib proves symmetry of `riemannianEDist`. -/
theorem riemannianEDist_comm_wrapper
    [RiemannianBundle (fun x : M => TangentSpace I x)] (x y : M) :
    riemannianEDist I x y = riemannianEDist I y x := by
  exact riemannianEDist_comm

/--
Checked wrapper: torsion of a bundled covariant derivative vanishes on repeated
arguments.  This is adjacent connection infrastructure only, not the
Levi-Civita/geodesic/Jacobi-field package needed for the Morse index theorem.
-/
theorem covariantDerivative_torsion_self_wrapper
    [CompleteSpace E] [FiniteDimensional ℝ E] [IsManifold I 2 M]
    (cov : CovariantDerivative I E (TangentSpace I))
    {x : M} (X₀ : TangentSpace I x) :
    cov.torsion x X₀ X₀ = 0 := by
  exact CovariantDerivative.torsion_self cov X₀

/-! ## Audit probes -/

#check ModelWithCorners
#check IsManifold
#check ContMDiffOn
#check TangentSpace
#check RiemannianBundle
#check IsContMDiffRiemannianBundle
#check IsRiemannianManifold
#check riemannianEDist
#check riemannianEDist_self
#check riemannianEDist_comm
#check riemannianEDist_triangle
#check pathELength
#check riemannianEDist_le_pathELength
#check CovariantDerivative
#check IsCovariantDerivativeOn
#check CovariantDerivative.torsion
#check CovariantDerivative.torsion_self
#check CovariantDerivative.torsion_eq_zero_iff
#check VectorField.mlieBracket

/-- Pinned mathlib commit used for the Stage1 anchor audit. -/
def mathlibAnchorCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.PathELength",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Geometry.Manifold.VectorField.LieBracket"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ModelWithCorners",
  "IsManifold",
  "ContMDiffOn",
  "TangentSpace",
  "RiemannianBundle",
  "IsContMDiffRiemannianBundle",
  "IsRiemannianManifold",
  "Manifold.riemannianEDist",
  "Manifold.riemannianEDist_self",
  "Manifold.riemannianEDist_comm",
  "Manifold.riemannianEDist_triangle",
  "Manifold.pathELength",
  "Manifold.riemannianEDist_le_pathELength",
  "CovariantDerivative",
  "IsCovariantDerivativeOn",
  "CovariantDerivative.torsion",
  "CovariantDerivative.torsion_self",
  "CovariantDerivative.torsion_eq_zero_iff",
  "VectorField.mlieBracket"
]

/-- Search terms that did not locate a terminal Morse-index theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Morse index theorem",
  "MorseIndex",
  "morseIndex",
  "Jacobi field",
  "JacobiField",
  "geodesic",
  "Geodesic",
  "conjugate point",
  "ConjugatePoint",
  "index form",
  "IndexForm",
  "curvature operator",
  "sectional curvature"
]

/-- Stable, string-valued row for the C003 external Lean-code-search audit. -/
structure ExternalLeanSearchAuditRow where
  query : String
  authenticatedSearchStatus : String
  repositoryURL : String
  commitSHA : String
  theoremNames : List String
  license : String
  lakeCompatibility : String
  finding : String

/--
C003 requested authenticated GitHub code-search terms.

The local worker had no authenticated GitHub channel on 2026-05-01:
`gh auth status` reported no logged-in hosts, no `GH_TOKEN`/`GITHUB_TOKEN`
was available, and `gh search code` exited before searching.  These rows
therefore record a concrete audit blocker rather than an external proof anchor.
-/
def externalLeanSearchAudit : List ExternalLeanSearchAuditRow := [
  {
    query := "MorseIndex language:Lean",
    authenticatedSearchStatus := "blocked: no GitHub CLI authentication or token",
    repositoryURL := "",
    commitSHA := "",
    theoremNames := [],
    license := "",
    lakeCompatibility := "not assessed; authenticated search did not run",
    finding := "No authenticated result set was produced from this worker."
  },
  {
    query := "JacobiField language:Lean",
    authenticatedSearchStatus := "blocked: no GitHub CLI authentication or token",
    repositoryURL := "",
    commitSHA := "",
    theoremNames := [],
    license := "",
    lakeCompatibility := "not assessed; authenticated search did not run",
    finding := "No authenticated result set was produced from this worker."
  },
  {
    query := "ConjugatePoint language:Lean",
    authenticatedSearchStatus := "blocked: no GitHub CLI authentication or token",
    repositoryURL := "",
    commitSHA := "",
    theoremNames := [],
    license := "",
    lakeCompatibility := "not assessed; authenticated search did not run",
    finding := "No authenticated result set was produced from this worker."
  },
  {
    query := "IndexForm language:Lean",
    authenticatedSearchStatus := "blocked: no GitHub CLI authentication or token",
    repositoryURL := "",
    commitSHA := "",
    theoremNames := [],
    license := "",
    lakeCompatibility := "not assessed; authenticated search did not run",
    finding := "No authenticated result set was produced from this worker."
  },
  {
    query := "LeviCivita language:Lean",
    authenticatedSearchStatus := "blocked: no GitHub CLI authentication or token",
    repositoryURL := "",
    commitSHA := "",
    theoremNames := [],
    license := "",
    lakeCompatibility := "not assessed; authenticated search did not run",
    finding := "No authenticated result set was produced from this worker."
  },
  {
    query := "Geodesic language:Lean",
    authenticatedSearchStatus := "blocked: no GitHub CLI authentication or token",
    repositoryURL := "",
    commitSHA := "",
    theoremNames := [],
    license := "",
    lakeCompatibility := "not assessed; authenticated search did not run",
    finding := "No authenticated result set was produced from this worker."
  }
]

/-- The C003 external search audit records exactly the six requested terms. -/
theorem externalLeanSearchAudit_length :
    externalLeanSearchAudit.length = 6 :=
  rfl

/-- Stable, string-valued row for the C004 external-proof integration gate. -/
structure ExternalMorseIndexIntegrationGate where
  externalProofFound : Bool
  integrationTaskCreated : Bool
  repoLocalStatus : String
  nextRequiredAction : String
  completionBoundary : String

/--
C004 integration gate for any future external Lean 4 Morse-index proof.

The C003 search audit recorded a concrete authentication blocker rather than a
positive external proof anchor.  Consequently there is no repository URL,
commit, theorem name, license, or Lake target that can be pinned/imported/checked
from this child.  If a later authenticated audit finds a terminal Lean 4 proof,
this gate must be replaced by a concrete integration task before any completion
claim.
-/
def externalMorseIndexIntegrationGate : ExternalMorseIndexIntegrationGate where
  externalProofFound := false
  integrationTaskCreated := false
  repoLocalStatus := "not completed; no external Lean 4 Morse-index proof identified"
  nextRequiredAction :=
    "rerun authenticated GitHub code search, then pin/import/check any terminal proof or record a concrete integration blocker"
  completionBoundary :=
    "do not mark S1-M-126 complete from anchor-only evidence; no completed state may retain repo_local_integration_debt"

/-- The C004 gate does not claim that an external proof has been found. -/
theorem externalMorseIndexIntegrationGate_no_externalProofFound :
    externalMorseIndexIntegrationGate.externalProofFound = false :=
  rfl

/-- The C004 gate creates no concrete integration task without a concrete external proof target. -/
theorem externalMorseIndexIntegrationGate_no_taskCreated :
    externalMorseIndexIntegrationGate.integrationTaskCreated = false :=
  rfl

/-- Canonical C005 branches for a future Morse-index proof package. -/
inductive FutureMorseIndexProofBranch where
  | leviCivitaConnection
  | geodesicEquation
  | curvatureJacobiFields
  | conjugateMultiplicity
  | indexFormSecondVariation
  | finalIndexEquality
  deriving DecidableEq, Repr

/--
Stable row for the C005 package split.

Each row is deliberately an unchecked future-proof ledger entry.  The local
artifact records the intended branch budget and dependencies; it does not claim
that the branch proof exists in mathlib or in this repository.
-/
structure FutureMorseIndexProofLeaf where
  branch : FutureMorseIndexProofBranch
  leafId : String
  title : String
  upstreamInput : String
  proofObligation : String
  downstreamOutput : String
  leafBudget : Nat
  status : String
  debtClass : String
  repoLocalClosed : Bool
  deriving DecidableEq, Repr

/--
C005 split of the future proof package into the six requested branches.

The `leafBudget := 100` entries are local ledger ceilings, not estimates that
the branch is already proven.  The branch status remains `unchecked`, with
`formalization_debt`, until concrete geodesic/Jacobi/index-form APIs and proofs
are supplied by mathlib, a pinned external dependency, or local proof bodies.
-/
def futureMorseIndexProofLeaves : List FutureMorseIndexProofLeaf := [
  {
    branch := FutureMorseIndexProofBranch.leviCivitaConnection
    leafId := "M0165.LC01"
    title := "Levi-Civita connection package"
    upstreamInput :=
      "RiemannianBundle, CovariantDerivative, torsion and metric-compatibility infrastructure"
    proofObligation :=
      "construct or import the Levi-Civita connection with uniqueness, torsion-free, and metric-compatible APIs"
    downstreamOutput :=
      "canonical connection object usable by the geodesic equation branch"
    leafBudget := 100
    status := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
  },
  {
    branch := FutureMorseIndexProofBranch.geodesicEquation
    leafId := "M0165.GE01"
    title := "Geodesic equation package"
    upstreamInput := "Levi-Civita connection package plus smooth curve interval data"
    proofObligation :=
      "define geodesics as autoparallel curves and connect the coordinate/geometric geodesic equation"
    downstreamOutput :=
      "geodesic segment predicate for the Jacobi-field and index-form branches"
    leafBudget := 100
    status := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
  },
  {
    branch := FutureMorseIndexProofBranch.curvatureJacobiFields
    leafId := "M0165.JF01"
    title := "Curvature and Jacobi-field package"
    upstreamInput := "geodesic equation package plus curvature operator APIs"
    proofObligation :=
      "define vector fields along a geodesic, the Jacobi equation, and the variation-to-Jacobi bridge"
    downstreamOutput :=
      "Jacobi-field solution space used by conjugate multiplicity and index-form kernel arguments"
    leafBudget := 100
    status := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
  },
  {
    branch := FutureMorseIndexProofBranch.conjugateMultiplicity
    leafId := "M0165.CM01"
    title := "Conjugate-point multiplicity package"
    upstreamInput := "Jacobi-field package plus endpoint evaluation maps along the geodesic"
    proofObligation :=
      "define interior conjugate times and multiplicity as the relevant Jacobi endpoint-map kernel dimension"
    downstreamOutput :=
      "finite multiplicity sum over the open geodesic interval"
    leafBudget := 100
    status := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
  },
  {
    branch := FutureMorseIndexProofBranch.indexFormSecondVariation
    leafId := "M0165.IF01"
    title := "Index form and second-variation package"
    upstreamInput := "geodesic, curvature/Jacobi, and endpoint-fixed variation-space packages"
    proofObligation :=
      "define the index form, prove it is the endpoint-fixed second variation, and identify its kernel with Jacobi fields"
    downstreamOutput :=
      "self-adjoint quadratic-form package with finite Morse index"
    leafBudget := 100
    status := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
  },
  {
    branch := FutureMorseIndexProofBranch.finalIndexEquality
    leafId := "M0165.EQ01"
    title := "Final Morse-index equality package"
    upstreamInput := "conjugate multiplicity package plus index-form/second-variation package"
    proofObligation :=
      "prove the Morse index equals the sum of conjugate-point multiplicities under nondegenerate endpoint hypotheses"
    downstreamOutput :=
      "MorseIndexTheoremPackage.index_eq_conjugatePointMultiplicitySum"
    leafBudget := 100
    status := "unchecked"
    debtClass := "formalization_debt"
    repoLocalClosed := false
  }
]

/-- The C005 split has exactly the six requested future proof branches. -/
theorem futureMorseIndexProofLeaves_length :
    futureMorseIndexProofLeaves.length = 6 :=
  rfl

/-- Every C005 branch has an explicit local leaf-ledger ceiling of at most 100 steps. -/
theorem futureMorseIndexProofLeaves_budget_le_100 :
    ∀ row ∈ futureMorseIndexProofLeaves, row.leafBudget ≤ 100 := by
  decide

/-- The C005 split records only unchecked future work, not completed proof leaves. -/
theorem futureMorseIndexProofLeaves_not_repoLocalClosed :
    ∀ row ∈ futureMorseIndexProofLeaves, row.repoLocalClosed = false := by
  decide

/-- The C005 split leaves the remaining work as formalization debt, not integration debt. -/
theorem futureMorseIndexProofLeaves_formalizationDebt :
    ∀ row ∈ futureMorseIndexProofLeaves, row.debtClass = "formalization_debt" := by
  decide

/-- Stable row for the C006 local-wrapper gate. -/
structure LocalMorseIndexWrapperGate where
  concreteGeodesicAPI : Bool
  concreteJacobiFieldAPI : Bool
  concreteIndexFormAPI : Bool
  terminalMorseIndexTheorem : Bool
  localTerminalWrapperAdded : Bool
  allowedNextAction : String
  status : String
  debtClass : String
  repoLocalClosed : Bool
  deriving DecidableEq, Repr

/--
C006 gate for local Morse-index wrappers.

This child does not add a terminal local theorem wrapper: the audited mathlib
snapshot and current local artifact still lack concrete geodesic/Jacobi-field
and index-form APIs, and no pinned external dependency supplies the final
Morse-index theorem.  The existing checked wrappers remain adjacent
Riemannian/covariant-derivative infrastructure only.
-/
def localMorseIndexWrapperGate : LocalMorseIndexWrapperGate where
  concreteGeodesicAPI := false
  concreteJacobiFieldAPI := false
  concreteIndexFormAPI := false
  terminalMorseIndexTheorem := false
  localTerminalWrapperAdded := false
  allowedNextAction :=
    "add local wrappers only after mathlib or a pinned external dependency supplies concrete geodesic, Jacobi-field, index-form, and terminal Morse-index APIs"
  status :=
    "blocked: no concrete geodesic/Jacobi/index-form API stack or terminal Morse-index theorem available for a local wrapper"
  debtClass := "formalization_debt"
  repoLocalClosed := false

/-- The C006 gate records that no terminal local Morse-index wrapper was added. -/
theorem localMorseIndexWrapperGate_no_terminalWrapper :
    localMorseIndexWrapperGate.localTerminalWrapperAdded = false :=
  rfl

/-- The C006 gate records formalization debt rather than repo-local integration debt. -/
theorem localMorseIndexWrapperGate_formalizationDebt :
    localMorseIndexWrapperGate.debtClass = "formalization_debt" :=
  rfl

/-- The C006 gate does not close the parent Morse-index theorem repo-locally. -/
theorem localMorseIndexWrapperGate_not_repoLocalClosed :
    localMorseIndexWrapperGate.repoLocalClosed = false :=
  rfl

end S1_M_126
end Stage1
end AwesomeTheorems
