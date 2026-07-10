import Mathlib.Algebra.Lie.Basic

/-!
# S1-M-210 / THM-M-1551: Zero-curvature representation

This Stage1 artifact records a conservative Lean 4 boundary for the
zero-curvature representation used in the gauge-theoretic formulation of
integrable systems.

The mathematical physics phrase is normalized here as an abstract Lax pair:
two evolution directions `Dx`, `Dt`, two connection potentials `U`, `V`, and
the curvature expression

`Dx V - Dt U + ⁅U, V⁆`.

The file proves only the algebraic wrapper saying that the normalized Lax
compatibility equation implies vanishing curvature.  It does not claim a
terminal theorem for PDE integrability, spectral parameters, inverse scattering,
monodromy, principal bundles, or gauge-transformed flat connections.
-/

noncomputable section

universe uR uL uG

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_210

/-- An abstract evolution direction acting linearly on a Lie-algebra-valued field space. -/
abbrev EvolutionDirection (R : Type uR) (L : Type uL) [CommRing R] [LieRing L]
    [LieAlgebra R L] :=
  L →ₗ[R] L

/--
Curvature of a two-direction Lax connection.

In analytic notation this is the zero-curvature expression
`F_xt = D_x V - D_t U + [U,V]`.
-/
def laxCurvature {R : Type uR} {L : Type uL} [CommRing R] [LieRing L]
    [LieAlgebra R L] (Dx Dt : EvolutionDirection R L) (U V : L) : L :=
  Dx V - Dt U + ⁅U, V⁆

/-- The zero-curvature equation for a normalized abstract Lax pair. -/
def ZeroCurvature {R : Type uR} {L : Type uL} [CommRing R] [LieRing L]
    [LieAlgebra R L] (Dx Dt : EvolutionDirection R L) (U V : L) : Prop :=
  laxCurvature Dx Dt U V = 0

/--
The compatibility equation equivalent to the vanishing of the curvature
expression after moving terms across the equality.
-/
def LaxCompatibilityEquation {R : Type uR} {L : Type uL} [CommRing R] [LieRing L]
    [LieAlgebra R L] (Dx Dt : EvolutionDirection R L) (U V : L) : Prop :=
  Dx V + ⁅U, V⁆ = Dt U

/--
Gauge-covariant evolution operator at the statement boundary:
`nabla_D,A X = D X + [A, X]`.
-/
def covariantEvolution {R : Type uR} {L : Type uL} [CommRing R] [LieRing L]
    [LieAlgebra R L] (D : EvolutionDirection R L) (A X : L) : L :=
  D X + ⁅A, X⁆

/--
Constant algebraic gauge transforms for the abstract Lax-pair boundary.

This deliberately models only gauge transforms that are linear equivalences of
the Lie-algebra-valued field space, preserve the Lie bracket, and commute with
the selected evolution directions when used in covariance lemmas below.  It is
not the full variable gauge-transformation law for principal-bundle
connections.
-/
structure LaxGaugeTransform (R : Type uR) (L : Type uL) [CommRing R]
    [LieRing L] [LieAlgebra R L] : Type (max uR uL) where
  toLinearEquiv : L ≃ₗ[R] L
  map_lie' : ∀ X Y : L, toLinearEquiv ⁅X, Y⁆ = ⁅toLinearEquiv X, toLinearEquiv Y⁆

namespace LaxGaugeTransform

instance {R : Type uR} {L : Type uL} [CommRing R] [LieRing L]
    [LieAlgebra R L] : CoeFun (LaxGaugeTransform R L) (fun _ => L → L) where
  coe γ := γ.toLinearEquiv

/-- Apply a constant abstract gauge transform to a connection-potential pair. -/
def transformPotentialPair {R : Type uR} {L : Type uL} [CommRing R] [LieRing L]
    [LieAlgebra R L] (γ : LaxGaugeTransform R L) (P : L × L) : L × L :=
  (γ P.1, γ P.2)

/--
Curvature covariance for a constant abstract gauge transform.

If the gauge transform preserves the bracket and commutes with both evolution
directions, the Lax curvature of the transformed potential pair is the
transformed Lax curvature.
-/
theorem laxCurvature_transform_eq {R : Type uR} {L : Type uL} [CommRing R]
    [LieRing L] [LieAlgebra R L] (γ : LaxGaugeTransform R L)
    (Dx Dt : EvolutionDirection R L) (U V : L)
    (hDx : ∀ X : L, Dx (γ X) = γ (Dx X))
    (hDt : ∀ X : L, Dt (γ X) = γ (Dt X)) :
    laxCurvature Dx Dt (γ U) (γ V) = γ (laxCurvature Dx Dt U V) := by
  simp [laxCurvature, hDx, hDt, γ.map_lie']

/--
The zero-curvature predicate is invariant under a constant abstract gauge
transform that commutes with the two selected evolution directions.
-/
theorem zeroCurvature_transform_iff {R : Type uR} {L : Type uL} [CommRing R]
    [LieRing L] [LieAlgebra R L] (γ : LaxGaugeTransform R L)
    (Dx Dt : EvolutionDirection R L) (U V : L)
    (hDx : ∀ X : L, Dx (γ X) = γ (Dx X))
    (hDt : ∀ X : L, Dt (γ X) = γ (Dt X)) :
    ZeroCurvature Dx Dt (γ U) (γ V) ↔ ZeroCurvature Dx Dt U V := by
  simp [ZeroCurvature, laxCurvature_transform_eq γ Dx Dt U V hDx hDt]

end LaxGaugeTransform

/--
Abstract flat Lax-pair data.

Concrete future work should replace the linear directions and potentials with
smooth Lie-algebra-valued functions, spectral parameters, and a bundle
connection model.
-/
structure FlatLaxPairData (R : Type uR) (L : Type uL) [CommRing R] [LieRing L]
    [LieAlgebra R L] : Type (max uR uL) where
  Dx : EvolutionDirection R L
  Dt : EvolutionDirection R L
  U : L
  V : L
  compatibility : LaxCompatibilityEquation Dx Dt U V

/--
Field/object-model choices considered for the zero-curvature representation.

The selected Stage1 path is `abstractLieAlgebraValuedFields`: keep potentials
and evolution directions in an abstract Lie-algebra-valued field space.  Matrix
potentials, manifold sections, and principal-bundle connections are preserved as
future bridge targets rather than being claimed as available concrete APIs.
-/
inductive LaxFieldObjectModel where
  | abstractLieAlgebraValuedFields
  | matrixValuedFunctions
  | manifoldSections
  | principalBundleConnectionApi
  deriving DecidableEq, Repr

/-- Repo-local record of the S1-M-210 concrete field-model decision. -/
structure LaxFieldObjectModelDecision where
  selectedModel : LaxFieldObjectModel
  selectedModelName : String
  rejectedDirectModels : List String
  rationale : List String
  requiredBridgeApis : List String
  repoLocalCompletionStatus : String

/--
Field model decision for THM-M-1551.

The current checked artifact models a Lax pair as abstract Lie-algebra-valued
potentials `U`, `V : L` and linear evolution directions on `L`.  This is the
strongest repo-local model already validated in this file.  Direct
matrix-valued functions, smooth manifold sections, and principal-bundle
connection APIs require additional concrete mathlib or pinned-dependency
interfaces before they can replace this boundary.
-/
def selectedLaxFieldObjectModelDecision : LaxFieldObjectModelDecision where
  selectedModel := LaxFieldObjectModel.abstractLieAlgebraValuedFields
  selectedModelName := "abstract_lie_algebra_valued_fields"
  rejectedDirectModels := [
    "matrix_valued_functions: no matrix-valued function Lax-pair API is repo-local pinned/imported/checked for this slot",
    "mathlib_manifold_sections: covariant-derivative and vector-field anchors exist, but no concrete Lie-algebra-bundle section model is wired into this theorem",
    "principal_bundle_connection_api: no terminal principal-bundle connection and curvature API is available in this repo-local Stage1 closure"
  ]
  rationale := [
    "The existing checked statement already proves that the normalized compatibility equation implies the abstract curvature equation",
    "An abstract Lie-algebra-valued model keeps the bracket, linear evolution directions, and zero-curvature expression kernel-checkable without fabricating analytic regularity assumptions",
    "Matrix-valued, manifold-section, and principal-bundle formulations should be added later as bridge theorems from their concrete APIs into this abstract boundary"
  ]
  requiredBridgeApis := [
    "function-space model for smooth or formal fields with pointwise Lie bracket",
    "matrix-valued potential model with commutator bracket and derivative directions",
    "manifold section model for Lie-algebra bundles with compatible covariant derivatives",
    "principal-bundle connection curvature API and local-potential trivialization theorem",
    "replacement theorem connecting each concrete model to `LaxCompatibilityEquation` and `ZeroCurvature`"
  ]
  repoLocalCompletionStatus := "not_repo_local_closed"

/-- The selected local field model is the abstract Lie-algebra-valued boundary. -/
theorem selectedLaxFieldObjectModelDecision_model :
    selectedLaxFieldObjectModelDecision.selectedModel =
      LaxFieldObjectModel.abstractLieAlgebraValuedFields :=
  rfl

/-- The field-model decision does not close the terminal zero-curvature theorem. -/
theorem selectedLaxFieldObjectModelDecision_not_closed :
    selectedLaxFieldObjectModelDecision.repoLocalCompletionStatus =
      "not_repo_local_closed" :=
  rfl

/--
External Lean-source audit states for the zero-curvature representation slot.

This separates a completed pin/import/check closure from an unavailable or
anchor-only search result, so that external evidence cannot be counted as
repo-local theorem completion.
-/
inductive ExternalLeanAuditStatus where
  | authenticatedSearchBlocked
  | localSourceSearchNoTerminalProof
  | externalAnchorOnlyNeedsIntegration
  | externalProofPinnedAndChecked
  deriving DecidableEq, Repr

/--
Repo-local record for the child task that audits external Lean 4 proof sources.
-/
structure ExternalLeanAuditRecord where
  status : ExternalLeanAuditStatus
  authenticatedToolStatus : String
  localSearchSurfaces : List String
  requiredExternalQueries : List String
  localSourceResult : String
  integrationBlocker : String
  nextIntegrationActions : List String
  repoLocalCompletionStatus : String

/--
External Lean proof audit record for THM-M-1551.

The authenticated GitHub search required by the public child task is not closed
in this workspace because `gh auth status` reports that no GitHub host is
logged in.  Local mathlib/repo-source search did not locate a terminal
zero-curvature, Lax-pair compatibility, or gauge-curvature-covariance theorem.
-/
def externalLeanProofAuditRecord : ExternalLeanAuditRecord where
  status := ExternalLeanAuditStatus.authenticatedSearchBlocked
  authenticatedToolStatus :=
    "gh is installed, but gh auth status reports no logged-in GitHub host"
  localSearchSurfaces := [
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib",
    "Formalizations/Lean/AwesomeTheorems"
  ]
  requiredExternalQueries := [
    "\"zero curvature\" \"Lean\" \"Lax\"",
    "\"ZeroCurvature\" \"LaxPair\" \"Lean\"",
    "\"Lax pair\" \"integrable systems\" \"Lean\"",
    "\"gauge\" \"curvature\" \"covariance\" \"Lean\"",
    "\"flat connection\" \"gauge\" \"Lean\""
  ]
  localSourceResult :=
    "no terminal Lean 4 theorem found in local mathlib/repo source search"
  integrationBlocker :=
    "authenticated GitHub code search cannot run until a GitHub host is logged in"
  nextIntegrationActions := [
    "rerun authenticated GitHub code search with pinned query strings",
    "for any external Lean proof found, record repository, commit, module, theorem name, and license",
    "pin/import/check the external proof or record a concrete incompatibility blocker",
    "do not mark THM-M-1551 completed from anchor-only search evidence"
  ]
  repoLocalCompletionStatus := "not_repo_local_closed"

/-- The external Lean audit child remains open until authenticated search closes. -/
theorem externalLeanProofAuditRecord_status :
    externalLeanProofAuditRecord.status =
      ExternalLeanAuditStatus.authenticatedSearchBlocked :=
  rfl

/-- The external Lean audit does not close the repo-local theorem target. -/
theorem externalLeanProofAuditRecord_not_closed :
    externalLeanProofAuditRecord.repoLocalCompletionStatus =
      "not_repo_local_closed" :=
  rfl

/--
Status values for the PDE/spectral-parameter bridge split.

The current Stage1 child records a checked split plan only.  It does not prove
that a concrete PDE family, spectral parameter, or auxiliary linear problem has
been connected to `LaxCompatibilityEquation`.
-/
inductive PdeSpectralBridgeStatus where
  | splitPlanRecorded
  | blockedOnConcreteEquationFamily
  | localBridgeProofBodyAvailable
  deriving DecidableEq, Repr

/-- A budgeted leaf in the future PDE/spectral-parameter bridge proof tree. -/
structure PdeSpectralBridgeLeaf where
  id : String
  target : String
  prerequisites : List String
  maxProofSteps : Nat
  repoLocalStatus : String
  blocker : String

/--
Repo-local split plan for the PDE/spectral-parameter bridge.

Each leaf is capped at `<= 100` planned proof steps, but all leaves remain open
until a concrete PDE family and spectral-parameter model are selected and
checked.  This is a machine-checkable planning artifact, not a completion
claim for the zero-curvature representation theorem.
-/
def pdeSpectralBridgeLeaves : List PdeSpectralBridgeLeaf := [
  {
    id := "THM-M-1551.pde-spectral-001"
    target := "choose one concrete PDE family and freeze sign/normalization conventions"
    prerequisites := [
      "selected field model",
      "public statement boundary",
      "domain and derivative conventions"
    ]
    maxProofSteps := 100
    repoLocalStatus := "open_formalization_debt"
    blocker := "no concrete PDE family is selected in the repo-local closure"
  },
  {
    id := "THM-M-1551.pde-spectral-002"
    target := "define a spectral-parameter type and parameterized Lax potentials"
    prerequisites := [
      "chosen PDE family",
      "abstract Lie-algebra-valued field boundary",
      "parameter domain conventions"
    ]
    maxProofSteps := 100
    repoLocalStatus := "open_formalization_debt"
    blocker := "spectral parameter and parameterized potential APIs are not defined"
  },
  {
    id := "THM-M-1551.pde-spectral-003"
    target := "state the auxiliary linear problem whose compatibility produces the Lax equation"
    prerequisites := [
      "parameterized Lax potentials",
      "evolution directions",
      "linear auxiliary wave-function space"
    ]
    maxProofSteps := 100
    repoLocalStatus := "open_formalization_debt"
    blocker := "no auxiliary linear problem model is present"
  },
  {
    id := "THM-M-1551.pde-spectral-004"
    target := "prove the compatibility-to-curvature algebra for the chosen parameterized potentials"
    prerequisites := [
      "auxiliary linear problem statement",
      "commuting evolution directions",
      "bracket and derivative interaction lemmas"
    ]
    maxProofSteps := 100
    repoLocalStatus := "open_formalization_debt"
    blocker := "the derivative/bracket lemmas for concrete fields are not available"
  },
  {
    id := "THM-M-1551.pde-spectral-005"
    target := "bridge the concrete PDE equation to `LaxCompatibilityEquation`"
    prerequisites := [
      "chosen PDE normalization",
      "parameterized compatibility equation",
      "coefficient comparison or equation-family identity"
    ]
    maxProofSteps := 100
    repoLocalStatus := "open_formalization_debt"
    blocker := "no checked PDE-to-Lax equivalence theorem exists"
  },
  {
    id := "THM-M-1551.pde-spectral-006"
    target := "compose the bridge with `zeroCurvature_of_laxCompatibility` without upgrading parent status"
    prerequisites := [
      "concrete PDE-to-Lax bridge",
      "local validation command",
      "public merge-back and status synchronization plan"
    ]
    maxProofSteps := 100
    repoLocalStatus := "open_formalization_debt"
    blocker := "upstream bridge leaves are still open"
  }
]

/-- Repo-local record for the PDE/spectral-parameter bridge child split. -/
structure PdeSpectralBridgeSplitRecord where
  status : PdeSpectralBridgeStatus
  leaves : List PdeSpectralBridgeLeaf
  debtType : String
  repoLocalCompletionStatus : String
  completionGate : String

/-- Checked split-plan record for the THM-M-1551 PDE/spectral bridge. -/
def pdeSpectralBridgeSplitRecord : PdeSpectralBridgeSplitRecord where
  status := PdeSpectralBridgeStatus.splitPlanRecorded
  leaves := pdeSpectralBridgeLeaves
  debtType := "formalization_debt"
  repoLocalCompletionStatus := "not_repo_local_closed"
  completionGate :=
    "do not update completion status until each bridge leaf has a checked proof body or pinned/imported/checked upstream closure and public merge-back is complete"

/-- Every recorded PDE/spectral bridge leaf has a planned budget of at most 100 steps. -/
theorem pdeSpectralBridgeLeaves_budgeted :
    pdeSpectralBridgeLeaves.all (fun leaf => decide (leaf.maxProofSteps <= 100)) =
      true :=
  rfl

/-- The PDE/spectral bridge split is recorded, but not closed. -/
theorem pdeSpectralBridgeSplitRecord_status :
    pdeSpectralBridgeSplitRecord.status =
      PdeSpectralBridgeStatus.splitPlanRecorded :=
  rfl

/-- The PDE/spectral bridge split does not complete THM-M-1551. -/
theorem pdeSpectralBridgeSplitRecord_not_closed :
    pdeSpectralBridgeSplitRecord.repoLocalCompletionStatus =
      "not_repo_local_closed" :=
  rfl

/-- The curvature equation unfolds to the explicit algebraic expression. -/
theorem zeroCurvature_iff_laxCurvature_eq_zero {R : Type uR} {L : Type uL}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    (Dx Dt : EvolutionDirection R L) (U V : L) :
    ZeroCurvature Dx Dt U V ↔ laxCurvature Dx Dt U V = 0 :=
  Iff.rfl

/-- Checked algebraic wrapper: Lax compatibility gives zero curvature. -/
theorem zeroCurvature_of_laxCompatibility {R : Type uR} {L : Type uL}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    {Dx Dt : EvolutionDirection R L} {U V : L}
    (h : LaxCompatibilityEquation Dx Dt U V) :
    ZeroCurvature Dx Dt U V := by
  dsimp [ZeroCurvature, laxCurvature, LaxCompatibilityEquation] at h ⊢
  rw [← h]
  abel

/-- A packaged flat Lax pair has zero curvature. -/
theorem FlatLaxPairData.zeroCurvature {R : Type uR} {L : Type uL}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    (D : FlatLaxPairData R L) :
    ZeroCurvature D.Dx D.Dt D.U D.V :=
  zeroCurvature_of_laxCompatibility D.compatibility

/-- Zero potentials always give a flat abstract Lax connection. -/
theorem zeroCurvature_zeroPotentials {R : Type uR} {L : Type uL}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    (Dx Dt : EvolutionDirection R L) :
    ZeroCurvature Dx Dt 0 0 := by
  simp [ZeroCurvature, laxCurvature]

/-- The same potential in the same direction is a degenerate flat special case. -/
theorem zeroCurvature_samePotential_sameDirection {R : Type uR} {L : Type uL}
    [CommRing R] [LieRing L] [LieAlgebra R L]
    (D : EvolutionDirection R L) (U : L) :
    ZeroCurvature D D U U := by
  simp [ZeroCurvature, laxCurvature]

/-- Abstract gauge equivalence for connection-potential pairs. -/
def GaugeEquivalentPotentialPair {G : Type uG} {L : Type uL} [Group G]
    [MulAction G L] (P Q : L × L) : Prop :=
  ∃ g : G, (g • P.1, g • P.2) = Q

/-- Gauge equivalence is reflexive at the abstract potential-pair boundary. -/
theorem gaugeEquivalentPotentialPair_refl {G : Type uG} {L : Type uL}
    [Group G] [MulAction G L] (P : L × L) :
    GaugeEquivalentPotentialPair (G := G) P P := by
  exact ⟨1, by simp⟩

/-- The gauge orbit of a connection-potential pair. -/
def gaugePotentialPairOrbit {G : Type uG} {L : Type uL} [Group G]
    [MulAction G L] (P : L × L) : Set (L × L) :=
  {Q | GaugeEquivalentPotentialPair (G := G) P Q}

/-- Membership in the gauge orbit unfolds to gauge equivalence. -/
theorem mem_gaugePotentialPairOrbit_iff {G : Type uG} {L : Type uL}
    [Group G] [MulAction G L] {P Q : L × L} :
    Q ∈ gaugePotentialPairOrbit (G := G) P ↔
      GaugeEquivalentPotentialPair (G := G) P Q :=
  Iff.rfl

/-- Every potential pair lies in its own gauge orbit. -/
theorem mem_gaugePotentialPairOrbit_self {G : Type uG} {L : Type uL}
    [Group G] [MulAction G L] (P : L × L) :
    P ∈ gaugePotentialPairOrbit (G := G) P :=
  gaugeEquivalentPotentialPair_refl P

/--
Stage1 normalized statement shape.

This is the formalized algebraic core of the zero-curvature representation:
once the physical compatibility condition has been translated into the Lax
compatibility equation, the connection curvature vanishes.  It is not the full
integrable-systems theorem.
-/
def ZeroCurvatureRepresentationStatement : Prop :=
  ∀ (R : Type uR) (L : Type uL) [CommRing R] [LieRing L] [LieAlgebra R L]
    (Dx Dt : EvolutionDirection R L) (U V : L),
      LaxCompatibilityEquation Dx Dt U V → ZeroCurvature Dx Dt U V

/-- Canonical Stage1 statement boundary for this slot. -/
def StatementShape : Prop :=
  ZeroCurvatureRepresentationStatement.{uR, uL}

/-- Checked closure of the normalized algebraic Stage1 statement shape. -/
theorem statementShape_from_laxCompatibility : StatementShape.{uR, uL} := by
  intro R L _ _ _ Dx Dt U V h
  exact zeroCurvature_of_laxCompatibility h

/--
Child-task public surface anchor: this is the checked Lean object that the
Stage1 blueprint should cite when backfilling the normalized Lax-pair statement
shape for `THM-M-1551`.
-/
theorem publicBlueprintStatementShape : StatementShape.{uR, uL} :=
  statementShape_from_laxCompatibility

/-! ## Audit probes retained in the checked file. -/

#check EvolutionDirection
#check laxCurvature
#check ZeroCurvature
#check LaxCompatibilityEquation
#check covariantEvolution
#check LaxGaugeTransform
#check LaxGaugeTransform.transformPotentialPair
#check LaxGaugeTransform.laxCurvature_transform_eq
#check LaxGaugeTransform.zeroCurvature_transform_iff
#check FlatLaxPairData
#check LaxFieldObjectModel
#check LaxFieldObjectModelDecision
#check selectedLaxFieldObjectModelDecision
#check selectedLaxFieldObjectModelDecision_model
#check selectedLaxFieldObjectModelDecision_not_closed
#check ExternalLeanAuditStatus
#check ExternalLeanAuditRecord
#check externalLeanProofAuditRecord
#check externalLeanProofAuditRecord_status
#check externalLeanProofAuditRecord_not_closed
#check PdeSpectralBridgeStatus
#check PdeSpectralBridgeLeaf
#check pdeSpectralBridgeLeaves
#check PdeSpectralBridgeSplitRecord
#check pdeSpectralBridgeSplitRecord
#check pdeSpectralBridgeLeaves_budgeted
#check pdeSpectralBridgeSplitRecord_status
#check pdeSpectralBridgeSplitRecord_not_closed
#check zeroCurvature_of_laxCompatibility
#check zeroCurvature_zeroPotentials
#check zeroCurvature_samePotential_sameDirection
#check GaugeEquivalentPotentialPair
#check gaugePotentialPairOrbit
#check statementShape_from_laxCompatibility
#check publicBlueprintStatementShape
#check LieRing
#check LieAlgebra
#check lie_self
#check lie_skew
#check leibniz_lie
#check LinearMap

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Lie.Basic",
  "Mathlib.Algebra.Lie.OfAssociative",
  "Mathlib.RingTheory.Derivation.Basic",
  "Mathlib.RingTheory.Derivation.Lie",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Geometry.Manifold.VectorField.LieBracket",
  "Mathlib.Geometry.Manifold.Algebra.LieGroup",
  "Mathlib.Geometry.Manifold.GroupLieAlgebra"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "LieRing",
  "LieAlgebra",
  "Bracket",
  "lie_self",
  "lie_skew",
  "lie_add",
  "add_lie",
  "leibniz_lie",
  "LinearMap",
  "Derivation",
  "Derivation.instLieAlgebra",
  "CovariantDerivative",
  "IsCovariantDerivativeOn",
  "CovariantDerivative.torsion",
  "VectorField.mlieBracket",
  "AwesomeTheorems.Stage1.S1_M_210.LaxGaugeTransform",
  "AwesomeTheorems.Stage1.S1_M_210.LaxGaugeTransform.laxCurvature_transform_eq",
  "AwesomeTheorems.Stage1.S1_M_210.LaxGaugeTransform.zeroCurvature_transform_iff",
  "AwesomeTheorems.Stage1.S1_M_210.PdeSpectralBridgeSplitRecord",
  "AwesomeTheorems.Stage1.S1_M_210.pdeSpectralBridgeSplitRecord",
  "AwesomeTheorems.Stage1.S1_M_210.pdeSpectralBridgeLeaves_budgeted",
  "AwesomeTheorems.Stage1.S1_M_210.pdeSpectralBridgeSplitRecord_not_closed"
]

/--
Search terms that did not locate a terminal zero-curvature representation
theorem in the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "zero curvature representation",
  "ZeroCurvature",
  "Lax pair",
  "LaxPair",
  "integrable system",
  "inverse scattering",
  "spectral parameter",
  "monodromy",
  "flat connection"
]

end S1_M_210
end Stage1
end AwesomeTheorems
