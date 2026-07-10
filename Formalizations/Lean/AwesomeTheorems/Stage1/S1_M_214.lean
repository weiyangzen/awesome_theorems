import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Analysis.Normed.Operator.BoundedLinearMaps
import Mathlib.Analysis.Normed.Module.PiTensorProduct.InjectiveSeminorm
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.TensorProduct.Basic
import Mathlib.Topology.Algebra.Module.FiniteDimensionBilinear

/-!
# S1-M-214 / THM-M-0325: Grothendieck inequality

This Stage1 artifact records a conservative Lean 4 boundary for the real
finite-matrix form of Grothendieck's inequality.  The usual Banach-space and
tensor-norm formulations are not identified as terminal theorems in the pinned
mathlib dependency.  The declarations below therefore freeze a precise
statement shape:

* scalar matrix forms on finite unit polydiscs;
* Hilbert-space matrix forms on finite families of unit vectors;
* an explicit universal Grothendieck constant;
* checked zero-matrix, operator-norm, bounded-bilinear, and inner-product
  substrate wrappers.

No terminal proof of Grothendieck's inequality is claimed here.
-/

noncomputable section

open scoped BigOperators RealInnerProductSpace TensorProduct

universe u v w

namespace AwesomeTheorems.Stage1.S1_M_214

variable {m n : Type u} [Fintype m] [Fintype n]

/-- Pinned mathlib revision audited for the Stage1 Grothendieck substrate surface. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Substrates available at the pinned mathlib revision for this Stage1 audit.

This records API availability only; it is not a proof of the terminal
Grothendieck inequality.
-/
def availableMathlibSubstrates : List String := [
  "inner-product spaces",
  "continuous linear maps",
  "bounded bilinear maps",
  "finite matrix sums",
  "algebraic tensor products"
]

/-- Finite scalar bilinear form associated to a real matrix kernel. -/
def scalarMatrixForm (A : m → n → ℝ) (x : m → ℝ) (y : n → ℝ) : ℝ :=
  ∑ i, ∑ j, A i j * x i * y j

/-- Finite Hilbert-space matrix form associated to a real matrix kernel. -/
def hilbertMatrixForm
    (A : m → n → ℝ)
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (x : m → H) (y : n → H) : ℝ :=
  ∑ i, ∑ j, A i j * ⟪x i, y j⟫

/-- Scalar unit-polydisc bound for the finite matrix form. -/
def ScalarUnitBoundedBy (A : m → n → ℝ) (C : ℝ) : Prop :=
  ∀ x : m → ℝ, ∀ y : n → ℝ,
    (∀ i, |x i| ≤ 1) → (∀ j, |y j| ≤ 1) →
      |scalarMatrixForm A x y| ≤ C

/-- Hilbert unit-ball bound for the finite matrix form. -/
def HilbertUnitBoundedBy (A : m → n → ℝ) (C : ℝ) : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℝ H],
    ∀ x : m → H, ∀ y : n → H,
      (∀ i, ‖x i‖ ≤ 1) → (∀ j, ‖y j‖ ≤ 1) →
        |hilbertMatrixForm A H x y| ≤ C

/--
Finite real Grothendieck inequality with an explicit constant.

This is the finite matrix/Hilbert-space formulation: a scalar bound `C` for all
real unit-polydisc vectors controls all Hilbert-space inner-product sums by
`K_G * C`.  Later tensor-norm work can replace this boundary by a projective /
injective tensor-norm theorem once the corresponding APIs and proof are in the
repo-local Lean closure.
-/
def GrothendieckInequalityWithConstant (K_G : ℝ) : Prop :=
  0 ≤ K_G ∧
    ∀ (m : Type u) (n : Type u) [Fintype m] [Fintype n],
      ∀ (A : m → n → ℝ) (C : ℝ),
        0 ≤ C → ScalarUnitBoundedBy A C → HilbertUnitBoundedBy A (K_G * C)

/-- Stage1 normalized statement shape for Grothendieck's inequality. -/
def StatementShape : Prop :=
  ∃ K_G : ℝ, GrothendieckInequalityWithConstant.{u} K_G

/--
Public-documentation boundary for `THM-M-0325.statement`.

This is intentionally just the finite real matrix/Hilbert-space statement
`StatementShape`.  It is not a terminal Banach-space tensor-norm theorem, and
does not assert projective or injective normed tensor-product APIs.
-/
def StatementNormalizationBoundary : Prop :=
  StatementShape.{u}

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro {K_G : ℝ}
    (h : GrothendieckInequalityWithConstant.{u} K_G) :
    StatementShape.{u} :=
  ⟨K_G, h⟩

/-- The public statement-normalization boundary is exactly `StatementShape`. -/
theorem statementNormalizationBoundary_iff_statementShape :
    StatementNormalizationBoundary.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/-- The statement shape unfolds to the existence of a Grothendieck constant. -/
theorem statementShape_iff_exists_constant :
    StatementShape.{u} ↔ ∃ K_G : ℝ, GrothendieckInequalityWithConstant.{u} K_G :=
  Iff.rfl

/--
Unfolded finite real matrix/Hilbert-space boundary for the current Stage1
normalization target.
-/
theorem statementShape_iff_finite_matrix_hilbert_boundary :
    StatementShape.{u} ↔
      ∃ K_G : ℝ, 0 ≤ K_G ∧
        ∀ (m : Type u) (n : Type u) [Fintype m] [Fintype n],
          ∀ (A : m → n → ℝ) (C : ℝ),
            0 ≤ C → ScalarUnitBoundedBy A C → HilbertUnitBoundedBy A (K_G * C) :=
  Iff.rfl

/-- The scalar form of the zero matrix is zero. -/
theorem scalarMatrixForm_zero (x : m → ℝ) (y : n → ℝ) :
    scalarMatrixForm (fun _ _ => 0 : m → n → ℝ) x y = 0 := by
  simp [scalarMatrixForm]

/-- The Hilbert form of the zero matrix is zero. -/
theorem hilbertMatrixForm_zero
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (x : m → H) (y : n → H) :
    hilbertMatrixForm (fun _ _ => 0 : m → n → ℝ) H x y = 0 := by
  simp [hilbertMatrixForm]

/-- The zero matrix satisfies every nonnegative scalar unit-polydisc bound. -/
theorem zero_scalarUnitBoundedBy {C : ℝ} (hC : 0 ≤ C) :
    ScalarUnitBoundedBy (fun _ _ => 0 : m → n → ℝ) C := by
  intro x y _ _
  simpa [scalarMatrixForm] using hC

/-- The zero matrix satisfies every nonnegative Hilbert unit-ball bound. -/
theorem zero_hilbertUnitBoundedBy {C : ℝ} (hC : 0 ≤ C) :
    HilbertUnitBoundedBy (fun _ _ => 0 : m → n → ℝ) C := by
  intro H _ _ x y _ _
  simpa [hilbertMatrixForm] using hC

/-- Checked operator-norm substrate used by future bounded-map packages. -/
theorem continuousLinearMap_apply_norm_le
    {E : Type v} {F : Type w} [NormedAddCommGroup E] [NormedAddCommGroup F]
    [NormedSpace ℝ E] [NormedSpace ℝ F] (T : E →L[ℝ] F) (x : E) :
    ‖T x‖ ≤ ‖T‖ * ‖x‖ :=
  T.le_opNorm x

/-- Checked bounded-bilinear substrate for curried continuous bilinear maps. -/
theorem continuousLinearMap_isBoundedBilinear
    {E : Type u} {F : Type v} {G : Type w}
    [NormedAddCommGroup E] [NormedAddCommGroup F] [NormedAddCommGroup G]
    [NormedSpace ℝ E] [NormedSpace ℝ F] [NormedSpace ℝ G]
    (B : E →L[ℝ] F →L[ℝ] G) :
    IsBoundedBilinearMap ℝ fun p : E × F => B p.1 p.2 :=
  B.isBoundedBilinearMap

/-- Checked algebraic tensor-product substrate exposed by pinned mathlib. -/
abbrev algebraicTensorProductSubstrate
    (E : Type v) (F : Type w) [AddCommMonoid E] [AddCommMonoid F]
    [Module ℝ E] [Module ℝ F] :=
  TensorProduct ℝ E F

/-- Checked inner-product bound substrate for unit-vector local leaves. -/
theorem abs_real_inner_le_one_of_norm_le_one
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    {x y : H} (hx : ‖x‖ ≤ 1) (hy : ‖y‖ ≤ 1) :
    |⟪x, y⟫| ≤ 1 := by
  calc
    |⟪x, y⟫| ≤ ‖x‖ * ‖y‖ := abs_real_inner_le_norm x y
    _ ≤ 1 * 1 := mul_le_mul hx hy (norm_nonneg y) (by norm_num)
    _ = 1 := by norm_num

/-- Rank-one real matrix kernel used by the checked special-case leaves. -/
def rankOneMatrixKernel (u : m → ℝ) (v : n → ℝ) : m → n → ℝ :=
  fun i j => u i * v j

/-- The scalar form of a rank-one matrix factors as the product of two scalar sums. -/
theorem rankOne_scalarMatrixForm_eq_mul_sums
    (u : m → ℝ) (v : n → ℝ) (x : m → ℝ) (y : n → ℝ) :
    scalarMatrixForm (rankOneMatrixKernel u v) x y =
      (∑ i, u i * x i) * (∑ j, v j * y j) := by
  classical
  calc
    scalarMatrixForm (rankOneMatrixKernel u v) x y
        = ∑ i, (u i * x i) * ∑ j, v j * y j := by
          apply Finset.sum_congr rfl
          intro i _
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro j _
          simp [rankOneMatrixKernel]
          ring_nf
    _ = (∑ i, u i * x i) * (∑ j, v j * y j) := by
          rw [Finset.sum_mul]

/-- Unfolding lemma for the Hilbert form of a rank-one matrix. -/
theorem rankOne_hilbertMatrixForm_eq_sum
    (u : m → ℝ) (v : n → ℝ)
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (x : m → H) (y : n → H) :
    hilbertMatrixForm (rankOneMatrixKernel u v) H x y =
      ∑ i, ∑ j, (u i * v j) * ⟪x i, y j⟫ := by
  rfl

/-- One-row scalar forms reduce to a single finite sum over columns. -/
theorem scalarMatrixForm_one_row [Unique m]
    (A : m → n → ℝ) (x : m → ℝ) (y : n → ℝ) :
    scalarMatrixForm A x y = ∑ j, A default j * x default * y j := by
  simp [scalarMatrixForm]

/-- One-column scalar forms reduce to a single finite sum over rows. -/
theorem scalarMatrixForm_one_column [Unique n]
    (A : m → n → ℝ) (x : m → ℝ) (y : n → ℝ) :
    scalarMatrixForm A x y = ∑ i, A i default * x i * y default := by
  simp [scalarMatrixForm]

/-- One-by-one scalar forms reduce to the unique matrix coefficient. -/
theorem scalarMatrixForm_one_by_one [Unique m] [Unique n]
    (A : m → n → ℝ) (x : m → ℝ) (y : n → ℝ) :
    scalarMatrixForm A x y = A default default * x default * y default := by
  simp [scalarMatrixForm]

/-- One-row Hilbert forms reduce to a single finite sum over columns. -/
theorem hilbertMatrixForm_one_row [Unique m]
    (A : m → n → ℝ)
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (x : m → H) (y : n → H) :
    hilbertMatrixForm A H x y = ∑ j, A default j * ⟪x default, y j⟫ := by
  simp [hilbertMatrixForm]

/-- One-column Hilbert forms reduce to a single finite sum over rows. -/
theorem hilbertMatrixForm_one_column [Unique n]
    (A : m → n → ℝ)
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (x : m → H) (y : n → H) :
    hilbertMatrixForm A H x y = ∑ i, A i default * ⟪x i, y default⟫ := by
  simp [hilbertMatrixForm]

/-- One-by-one Hilbert forms reduce to the unique matrix coefficient and inner product. -/
theorem hilbertMatrixForm_one_by_one [Unique m] [Unique n]
    (A : m → n → ℝ)
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (x : m → H) (y : n → H) :
    hilbertMatrixForm A H x y = A default default * ⟪x default, y default⟫ := by
  simp [hilbertMatrixForm]

/--
Finite-dimensional bilinear continuity wrapper for algebraic bilinear maps
between real normed spaces.
-/
abbrev finiteDimensionalContinuousBilinearMap
    {E : Type v} {F : Type w} {G : Type u}
    [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [NormedSpace ℝ G]
    (B : E →ₗ[ℝ] F →ₗ[ℝ] G) :
    E →L[ℝ] F →L[ℝ] G :=
  B.toContinuousBilinearMap

/-- The finite-dimensional continuity wrapper preserves pointwise evaluation. -/
theorem finiteDimensionalContinuousBilinearMap_apply
    {E : Type v} {F : Type w} {G : Type u}
    [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [NormedSpace ℝ G]
    (B : E →ₗ[ℝ] F →ₗ[ℝ] G) (x : E) (y : F) :
    finiteDimensionalContinuousBilinearMap B x y = B x y :=
  rfl

/-- A finite-dimensional algebraic bilinear map is a bounded bilinear map after wrapping. -/
theorem finiteDimensionalContinuousBilinearMap_isBoundedBilinear
    {E : Type v} {F : Type w} {G : Type u}
    [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [NormedSpace ℝ G]
    (B : E →ₗ[ℝ] F →ₗ[ℝ] G) :
    IsBoundedBilinearMap ℝ fun p : E × F =>
      finiteDimensionalContinuousBilinearMap B p.1 p.2 :=
  (finiteDimensionalContinuousBilinearMap B).isBoundedBilinearMap

/-- A finite-dimensional algebraic bilinear map is jointly continuous. -/
theorem finiteDimensionalBilinearMap_continuous
    {E : Type v} {F : Type w} {G : Type u}
    [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [NormedSpace ℝ G]
    (B : E →ₗ[ℝ] F →ₗ[ℝ] G) :
    Continuous fun p : E × F => B p.1 p.2 := by
  simpa [finiteDimensionalContinuousBilinearMap] using
    (finiteDimensionalContinuousBilinearMap_isBoundedBilinear B).continuous

/-- mathlib modules checked while locating repo-local Grothendieck-inequality anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.Normed.Operator.Basic",
  "Mathlib.Analysis.Normed.Operator.BoundedLinearMaps",
  "Mathlib.Topology.Algebra.Module.FiniteDimensionBilinear",
  "Mathlib.Topology.Algebra.Module.WeakBilin",
  "Mathlib.Topology.Algebra.Module.StrongTopology",
  "Mathlib.Analysis.Normed.Module.PiTensorProduct.ProjectiveSeminorm",
  "Mathlib.Analysis.Normed.Module.PiTensorProduct.InjectiveSeminorm",
  "Mathlib.Data.Matrix.Mul",
  "Mathlib.LinearAlgebra.TensorProduct.Basic",
  "Mathlib.LinearAlgebra.TensorProduct.Map",
  "Mathlib.LinearAlgebra.BilinearForm.TensorProduct"
]

/-- Negative audit search terms for the terminal theorem. -/
def absentTerminalSearchTerms : List String := [
  "Grothendieck inequality",
  "GrothendieckInequality",
  "projective tensor norm",
  "injective tensor norm",
  "GrothendieckConstant",
  "tensor norm inequality",
  "cross norm",
  "Banach space Grothendieck theorem"
]

/-- External source status for the `THM-M-0325.external-audit` pass. -/
inductive ExternalAuditStatus where
  /-- No terminal Lean 4 theorem or constant was found for the audited query. -/
  | noTerminalTheoremFound
  /-- Only supporting tensor-norm infrastructure was found, not Grothendieck's inequality. -/
  | substrateOnly
  /-- Authentication or rate-limit failure prevented a complete hosted-code search. -/
  | searchBlocked
  deriving DecidableEq, Repr

/-- Structured record for an external Lean 4 primary-source audit query. -/
structure ExternalAuditRecord where
  searchTerm : String
  repoURL : String
  revision : String
  modules : List String
  theoremNames : List String
  placeholderStatus : String
  status : ExternalAuditStatus
  deriving Repr

/--
External Lean 4 audit records for `THM-M-0325.external-audit`.

These records are audit metadata only.  They do not assert a terminal proof of
Grothendieck's inequality.  The checked mathlib revision supplies tensor
seminorm substrates, while the named Grothendieck-inequality theorem and
constant searches did not identify a repo-local or pinned external closure.
-/
def externalLeanAuditRecords : List ExternalAuditRecord := [
  {
    searchTerm := "GrothendieckInequality",
    repoURL := "https://github.com/leanprover-community/mathlib4.git",
    revision := mathlibPinnedRevision,
    modules := [],
    theoremNames := [],
    placeholderStatus := "no matching terminal Lean 4 theorem in pinned mathlib checkout",
    status := ExternalAuditStatus.noTerminalTheoremFound
  },
  {
    searchTerm := "Grothendieck inequality",
    repoURL := "https://github.com/leanprover-community/mathlib4.git",
    revision := mathlibPinnedRevision,
    modules := [],
    theoremNames := [],
    placeholderStatus := "no matching terminal Lean 4 theorem in pinned mathlib checkout",
    status := ExternalAuditStatus.noTerminalTheoremFound
  },
  {
    searchTerm := "GrothendieckConstant",
    repoURL := "https://github.com/leanprover-community/mathlib4.git",
    revision := mathlibPinnedRevision,
    modules := [],
    theoremNames := [],
    placeholderStatus := "no matching terminal Lean 4 constant in pinned mathlib checkout",
    status := ExternalAuditStatus.noTerminalTheoremFound
  },
  {
    searchTerm := "projective tensor norm",
    repoURL := "https://github.com/leanprover-community/mathlib4.git",
    revision := mathlibPinnedRevision,
    modules := [
      "Mathlib.Analysis.Normed.Module.PiTensorProduct.ProjectiveSeminorm"
    ],
    theoremNames := [
      "PiTensorProduct.projectiveSeminorm",
      "PiTensorProduct.projectiveSeminorm_tprod_le"
    ],
    placeholderStatus := "substrate present; not a Grothendieck-inequality theorem",
    status := ExternalAuditStatus.substrateOnly
  },
  {
    searchTerm := "injective tensor norm",
    repoURL := "https://github.com/leanprover-community/mathlib4.git",
    revision := mathlibPinnedRevision,
    modules := [
      "Mathlib.Analysis.Normed.Module.PiTensorProduct.InjectiveSeminorm"
    ],
    theoremNames := [
      "PiTensorProduct.injectiveSeminorm",
      "PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm",
      "PiTensorProduct.norm_eval_le_injectiveSeminorm"
    ],
    placeholderStatus := "substrate present; not a Grothendieck-inequality theorem",
    status := ExternalAuditStatus.substrateOnly
  },
  {
    searchTerm := "authenticated GitHub Lean code search",
    repoURL := "https://github.com/search",
    revision := "not available: local gh auth absent and unauthenticated API rate-limited",
    modules := [],
    theoremNames := [],
    placeholderStatus := "search blocked before any external terminal proof could be identified",
    status := ExternalAuditStatus.searchBlocked
  }
]

/-- Machine-readable gate: the external audit produced no terminal theorem anchor. -/
def externalAuditFoundTerminalTheorem : Bool :=
  false

/-- The external audit does not close the Stage1 statement boundary. -/
theorem externalAudit_found_no_terminal_theorem :
    externalAuditFoundTerminalTheorem = false :=
  rfl

/-- Repo-local integration gate status for external Grothendieck-inequality proofs. -/
inductive IntegrationGateStatus where
  /-- No terminal external Lean 4 theorem was identified by the current audit records. -/
  | noExternalTerminalTheoremIdentified
  /-- A terminal external theorem was identified and must be pinned, imported, and checked. -/
  | externalTheoremRequiresPinImportCheck
  /-- A terminal external theorem was identified but a concrete integration blocker remains. -/
  | externalTheoremBlocked
  deriving DecidableEq, Repr

/--
Integration gate for `THM-M-0325.integration-gate`.

The current repo-local audit records do not identify a terminal external Lean 4
Grothendieck-inequality theorem.  Therefore there is no external theorem anchor
that can be counted as completed evidence, and no `repo_local_integration_debt`
may be hidden under a completed state.
-/
def integrationGateStatus : IntegrationGateStatus :=
  IntegrationGateStatus.noExternalTerminalTheoremIdentified

/-- Machine-checkable integration-gate fact for the current audit state. -/
theorem integrationGateStatus_noExternalTerminalTheoremIdentified :
    integrationGateStatus =
      IntegrationGateStatus.noExternalTerminalTheoremIdentified :=
  rfl

/--
Concrete integration blockers that must be cleared before the public
integration-gate checkbox can close.
-/
def integrationGateOpenBlockers : List String := [
  "authenticated hosted-code Lean 4 source search remains blocked by missing GitHub credentials/rate limits",
  "no placeholder-free external Lean 4 theorem has been pinned as a Lake dependency or vendored source",
  "no external Grothendieck-inequality theorem has passed repo-local `lake env lean` validation"
]

/-- Stage1 tensor-API branch choices audited by `THM-M-0325.tensor-api`. -/
inductive TensorApiDecision where
  /-- Build projective/injective normed tensor-product APIs in this repository. -/
  | buildLocalNormedTensorApis
  /-- Import a complete external Lean formalization of Grothendieck's inequality. -/
  | importExternalFormalization
  /-- Keep the finite real matrix/Hilbert-space formulation as the Stage1 Lean target. -/
  | keepFiniteMatrixCanonical
  deriving DecidableEq, Repr

/--
Decision for `THM-M-0325.tensor-api`.

The pinned mathlib closure has finite-family `PiTensorProduct` projective and
injective seminorm substrates, checked below.  They are useful infrastructure,
but they do not by themselves supply a terminal Banach-space tensor-norm
Grothendieck theorem or a repo-local proof.  Stage1 therefore keeps the finite
matrix/Hilbert-space `StatementShape` as the canonical Lean target.
-/
def tensorApiDecision : TensorApiDecision :=
  TensorApiDecision.keepFiniteMatrixCanonical

/-- Machine-checkable one-line gate for the tensor-API decision. -/
theorem tensorApiDecision_is_keepFiniteMatrixCanonical :
    tensorApiDecision = TensorApiDecision.keepFiniteMatrixCanonical :=
  rfl

/-- Human-readable rationale strings for the `THM-M-0325.tensor-api` decision. -/
def tensorApiDecisionRationale : List String := [
  "mathlib exposes finite-family PiTensorProduct projective and injective seminorm APIs",
  "no repo-local terminal Banach-space tensor-norm Grothendieck theorem is present",
  "no external Grothendieck Lean proof has been pinned/imported/checked in this repository",
  "canonical Stage1 target remains the finite real matrix/Hilbert-space StatementShape"
]

/--
Checked projective seminorm substrate from mathlib's finite-family
`PiTensorProduct` API.
-/
abbrev checkedPiProjectiveSeminorm
    {ι : Type u} [Fintype ι]
    {𝕜 : Type v} [NormedField 𝕜]
    {E : ι → Type w} [∀ i, SeminormedAddCommGroup (E i)]
    [∀ i, NormedSpace 𝕜 (E i)] :
    Seminorm 𝕜 (⨂[𝕜] i, E i) :=
  PiTensorProduct.projectiveSeminorm

/-- Checked projective seminorm bound on pure tensors. -/
theorem checkedPiProjectiveSeminorm_tprod_le
    {ι : Type u} [Fintype ι]
    {𝕜 : Type v} [NormedField 𝕜]
    {E : ι → Type w} [∀ i, SeminormedAddCommGroup (E i)]
    [∀ i, NormedSpace 𝕜 (E i)]
    (x : Π i, E i) :
    checkedPiProjectiveSeminorm (𝕜 := 𝕜) (E := E) (⨂ₜ[𝕜] i, x i) ≤
      ∏ i, ‖x i‖ := by
  simpa [checkedPiProjectiveSeminorm] using
    PiTensorProduct.projectiveSeminorm_tprod_le (𝕜 := 𝕜) (E := E) x

/--
Checked injective seminorm substrate from mathlib's finite-family
`PiTensorProduct` API.
-/
abbrev checkedPiInjectiveSeminorm
    {ι : Type u} [Fintype ι]
    {𝕜 : Type v} [NontriviallyNormedField 𝕜]
    {E : ι → Type w} [∀ i, SeminormedAddCommGroup (E i)]
    [∀ i, NormedSpace 𝕜 (E i)] :
    Seminorm 𝕜 (⨂[𝕜] i, E i) :=
  PiTensorProduct.injectiveSeminorm

/-- Checked injective seminorm evaluation bound for continuous multilinear maps. -/
theorem checkedPiNormEvalLeInjectiveSeminorm
    {ι : Type u} [Fintype ι]
    {𝕜 : Type v} [NontriviallyNormedField 𝕜]
    {E : ι → Type w} [∀ i, SeminormedAddCommGroup (E i)]
    [∀ i, NormedSpace 𝕜 (E i)]
    {F : Type*} [SeminormedAddCommGroup F] [NormedSpace 𝕜 F]
    (f : ContinuousMultilinearMap 𝕜 E F) (x : ⨂[𝕜] i, E i) :
    ‖PiTensorProduct.lift f.toMultilinearMap x‖ ≤
      ‖f‖ * checkedPiInjectiveSeminorm (𝕜 := 𝕜) (E := E) x := by
  simpa [checkedPiInjectiveSeminorm] using
    PiTensorProduct.norm_eval_le_injectiveSeminorm (𝕜 := 𝕜) (E := E) f x

/--
The tensor-API decision does not change the public Stage1 statement boundary.
-/
theorem tensorApiDecision_preserves_statement_boundary :
    tensorApiDecision = TensorApiDecision.keepFiniteMatrixCanonical →
      (StatementNormalizationBoundary.{u} ↔ StatementShape.{u}) := by
  intro _
  exact statementNormalizationBoundary_iff_statementShape

end AwesomeTheorems.Stage1.S1_M_214
