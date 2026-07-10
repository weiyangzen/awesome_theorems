import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# S1-M-197 / THM-M-1529: Yang-Mills theory

This Stage1 artifact records a conservative Lean 4 boundary for non-abelian
Yang-Mills gauge theory.

The pinned mathlib snapshot supplies useful substrate for smooth manifolds,
Riemannian vector-bundle metrics, covariant derivatives, continuous linear
operators, Hilbert/inner-product spaces, measures, and `L^p` fields.  It does
not expose a terminal gauge-theory API for principal connections, curvature
two-forms, Hodge star on adjoint-valued differential forms, gauge quotient
moduli, or a theorem named Yang-Mills.  The declarations below therefore keep
the missing geometric/PDE bridge as explicit proposition fields while locally
checking small wrappers around available group-action, linear-operator, and
`MemLp` infrastructure.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal Manifold

namespace AwesomeTheorems.Stage1.S1_M_197

universe uBase uG uConn uCurv

/-- A group is non-abelian when two elements fail to commute. -/
def IsNonAbelianGroup (G : Type uG) [Group G] : Prop :=
  ∃ a b : G, a * b ≠ b * a

/-- Gauge equivalence of two connection carriers under a mathlib multiplicative action. -/
def GaugeEquivalent {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A B : Conn) : Prop :=
  ∃ g : G, g • A = B

/-- Gauge equivalence is reflexive. -/
theorem gaugeEquivalent_refl {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A : Conn) :
    GaugeEquivalent (G := G) A A := by
  exact ⟨1, by simp⟩

/-- Gauge equivalence is symmetric. -/
theorem gaugeEquivalent_symm {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] {A B : Conn}
    (hAB : GaugeEquivalent (G := G) A B) :
    GaugeEquivalent (G := G) B A := by
  rcases hAB with ⟨g, hg⟩
  refine ⟨g⁻¹, ?_⟩
  rw [← hg]
  simp

/-- Gauge equivalence is transitive. -/
theorem gaugeEquivalent_trans {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] {A B C : Conn}
    (hAB : GaugeEquivalent (G := G) A B)
    (hBC : GaugeEquivalent (G := G) B C) :
    GaugeEquivalent (G := G) A C := by
  rcases hAB with ⟨gAB, hgAB⟩
  rcases hBC with ⟨gBC, hgBC⟩
  refine ⟨gBC * gAB, ?_⟩
  rw [mul_smul, hgAB, hgBC]

/-- The gauge orbit of a connection carrier. -/
def gaugeOrbit {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A : Conn) : Set Conn :=
  {B | GaugeEquivalent (G := G) A B}

/-- Membership in the gauge orbit is gauge equivalence. -/
theorem mem_gaugeOrbit_iff {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] {A B : Conn} :
    B ∈ gaugeOrbit (G := G) A ↔ GaugeEquivalent (G := G) A B :=
  Iff.rfl

/-- Every connection lies in its own gauge orbit. -/
theorem mem_gaugeOrbit_self {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A : Conn) :
    A ∈ gaugeOrbit (G := G) A :=
  gaugeEquivalent_refl A

/--
Linear Hodge-star boundary on the chosen curvature carrier.

For a terminal Yang-Mills formalization, `Curv` should be replaced by
adjoint-valued two-forms on an oriented Riemannian or pseudo-Riemannian
manifold, and `star_square` should follow from the concrete metric/signature.
-/
structure HodgeStar (Curv : Type uCurv)
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv] :
    Type uCurv where
  star : Curv →L[ℝ] Curv
  star_square : ∀ F : Curv, star (star F) = F

/-- Self-duality for a curvature value with respect to the abstract Hodge star. -/
def IsSelfDual {Curv : Type uCurv}
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (H : HodgeStar Curv) (F : Curv) : Prop :=
  H.star F = F

/-- Anti-self-duality for a curvature value with respect to the abstract Hodge star. -/
def IsAntiSelfDual {Curv : Type uCurv}
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (H : HodgeStar Curv) (F : Curv) : Prop :=
  H.star F = -F

/-- The zero curvature value is self-dual. -/
theorem isSelfDual_zero {Curv : Type uCurv}
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (H : HodgeStar Curv) :
    IsSelfDual H (0 : Curv) := by
  simp [IsSelfDual]

/-- The zero curvature value is anti-self-dual. -/
theorem isAntiSelfDual_zero {Curv : Type uCurv}
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (H : HodgeStar Curv) :
    IsAntiSelfDual H (0 : Curv) := by
  simp [IsAntiSelfDual]

/--
Abstract Yang-Mills input data.

`Base` is the space on which fields are measured, `G` the gauge group,
`Conn` the connection carrier, and `Curv` the curvature-value carrier.  The
fields using current mathlib APIs are concrete where possible: group actions,
Hodge-star as a continuous linear operator, a measure, and `MemLp`-based finite
action.  The genuine gauge/PDE facts remain proposition fields.
-/
structure NonAbelianYangMillsData
    (Base : Type uBase) (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv)
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv] :
    Type (max (max uBase uG) (max uConn uCurv)) where
  measure : Measure Base
  connectionRegularity : Conn → Prop
  curvature : Conn → Base → Curv
  hodgeStar : HodgeStar Curv
  nonAbelianGaugeGroup : IsNonAbelianGroup G
  gaugeActionPreservesRegularity : Prop
  curvatureGaugeEquivariance : Prop
  yangMillsEquation : Conn → Prop
  variationalCriticalPoint : Conn → Prop
  covariantDivergenceVanishes : Conn → Prop
  critical_impl_yangMills :
    ∀ A : Conn,
      connectionRegularity A →
        variationalCriticalPoint A →
          yangMillsEquation A
  yangMills_impl_covariantDivergence :
    ∀ A : Conn, yangMillsEquation A → covariantDivergenceVanishes A

/-- Finite Yang-Mills action, represented here by an `L^2` curvature condition. -/
def FiniteYangMillsAction
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (D : NonAbelianYangMillsData Base G Conn Curv) (A : Conn) : Prop :=
  MemLp (D.curvature A) 2 D.measure

/-- Energy-size functional for the normalized statement boundary. -/
def YangMillsEnergy
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (D : NonAbelianYangMillsData Base G Conn Curv) (A : Conn) : ℝ≥0∞ :=
  eLpNorm (D.curvature A) 2 D.measure

/-- Checked `L^2` wrapper: finite action gives finite `eLpNorm` energy. -/
theorem yangMillsEnergy_lt_top_of_finiteAction
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (D : NonAbelianYangMillsData Base G Conn Curv) {A : Conn}
    (hA : FiniteYangMillsAction D A) :
    YangMillsEnergy D A < ∞ :=
  hA.eLpNorm_lt_top

/-- Checked `L^2` wrapper: applying the abstract Hodge star preserves `MemLp`. -/
theorem hodgeStar_curvature_memLp
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (D : NonAbelianYangMillsData Base G Conn Curv) {A : Conn}
    (hA : FiniteYangMillsAction D A) :
    MemLp (fun x => D.hodgeStar.star (D.curvature A x)) 2 D.measure :=
  hA.continuousLinearMap_comp D.hodgeStar.star

/-- Hypotheses for the normalized non-abelian Yang-Mills theorem shape. -/
def YangMillsHypotheses
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (D : NonAbelianYangMillsData Base G Conn Curv) : Prop :=
  D.gaugeActionPreservesRegularity ∧
    D.curvatureGaugeEquivariance

/-- Solution package exposed by the normalized statement boundary. -/
structure YangMillsSolution
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    (D : NonAbelianYangMillsData Base G Conn Curv) (A : Conn) :
    Type (max (max uBase uG) (max uConn uCurv)) where
  regular : D.connectionRegularity A
  finiteAction : FiniteYangMillsAction D A
  criticalPoint : D.variationalCriticalPoint A
  equation : D.yangMillsEquation A
  covariantDivergence : D.covariantDivergenceVanishes A

/-- The solution package exposes the Yang-Mills equation field. -/
theorem YangMillsSolution.equation_holds
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    {D : NonAbelianYangMillsData Base G Conn Curv} {A : Conn}
    (S : YangMillsSolution D A) :
    D.yangMillsEquation A :=
  S.equation

/-- The solution package exposes the covariant-divergence equation field. -/
theorem YangMillsSolution.covariantDivergence_holds
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv]
    {D : NonAbelianYangMillsData Base G Conn Curv} {A : Conn}
    (S : YangMillsSolution D A) :
    D.covariantDivergenceVanishes A :=
  S.covariantDivergence

/--
Stage1 statement shape for the non-abelian Yang-Mills boundary.

For every explicitly modeled non-abelian gauge system, a regular finite-action
critical point of the Yang-Mills action should satisfy the encoded Yang-Mills
equation and its covariant-divergence form.  This is a conditional wrapper over
the supplied variational bridge, not a terminal construction of gauge theory.
-/
def StatementShape : Prop :=
  ∀ (Base : Type uBase) (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv)
    [MeasurableSpace Base] [Group G] [MulAction G Conn]
    [NormedAddCommGroup Curv] [NormedSpace ℝ Curv],
      ∀ D : NonAbelianYangMillsData Base G Conn Curv,
        YangMillsHypotheses D →
          ∀ A : Conn,
            D.connectionRegularity A →
              FiniteYangMillsAction D A →
                D.variationalCriticalPoint A →
                  Nonempty (YangMillsSolution D A)

/-- Checked closure of the conditional Stage1 statement shape. -/
theorem statementShape_from_variationalBridge :
    StatementShape.{uBase, uG, uConn, uCurv} := by
  intro Base G Conn Curv _ _ _ _ _ D _ A hreg hfinite hcritical
  let hym : D.yangMillsEquation A := D.critical_impl_yangMills A hreg hcritical
  exact ⟨{
    regular := hreg
    finiteAction := hfinite
    criticalPoint := hcritical
    equation := hym
    covariantDivergence := D.yangMills_impl_covariantDivergence A hym
  }⟩

/-- mathlib modules checked while locating repo-local Yang-Mills anchors. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Public-task module subset for `S1-M-197-public-002`. -/
def publicTaskMathlibSubstrateModules : List String := [
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic"
]

/--
Exact C002 substrate audit.

The pinned mathlib revision provides covariant-derivative, vector-bundle,
Riemannian, Hilbert/inner-product, and `MemLp` substrate.  It does not provide
a terminal non-abelian Yang-Mills theorem in the local dependency closure.
-/
def publicTaskC002SubstrateAudit : List String := [
  "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "provides covariant-derivative substrate: CovariantDerivative and IsCovariantDerivativeOn",
  "provides vector-bundle substrate: VectorBundle and tangent/vector-bundle modules",
  "provides Riemannian substrate: Riemannian manifold and vector-bundle metric modules",
  "provides Hilbert-space substrate: InnerProductSpace and continuous-linear-map APIs",
  "provides MemLp substrate: MemLp, eLpNorm, and continuousLinearMap_comp",
  "does not provide a terminal Yang-Mills theorem, principal-connection package, curvature two-form API, Hodge-star-on-adjoint-forms API, or Euler-Lagrange/PDE bridge"
]

/-- Checked normalization of the pinned revision used by the C002 audit. -/
theorem mathlibPinnedRevision_eq :
    mathlibPinnedRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Checked normalization of the exact C002 substrate module list. -/
theorem publicTaskMathlibSubstrateModules_eq :
    publicTaskMathlibSubstrateModules = [
      "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
      "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
      "Mathlib.Geometry.Manifold.Riemannian.Basic",
      "Mathlib.Analysis.InnerProductSpace.Basic",
      "Mathlib.MeasureTheory.Function.LpSpace.Basic"
    ] :=
  rfl

/-- Checked normalization of the exact C002 audit finding. -/
theorem publicTaskC002SubstrateAudit_eq :
    publicTaskC002SubstrateAudit = [
      "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "provides covariant-derivative substrate: CovariantDerivative and IsCovariantDerivativeOn",
      "provides vector-bundle substrate: VectorBundle and tangent/vector-bundle modules",
      "provides Riemannian substrate: Riemannian manifold and vector-bundle metric modules",
      "provides Hilbert-space substrate: InnerProductSpace and continuous-linear-map APIs",
      "provides MemLp substrate: MemLp, eLpNorm, and continuousLinearMap_comp",
      "does not provide a terminal Yang-Mills theorem, principal-connection package, curvature two-form API, Hodge-star-on-adjoint-forms API, or Euler-Lagrange/PDE bridge"
    ] :=
  rfl

/-- mathlib modules checked while locating repo-local Yang-Mills anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
  "Mathlib.Geometry.Manifold.Algebra.LieGroup",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.InnerProductSpace.Rayleigh",
  "Mathlib.Analysis.Normed.Operator.Basic",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic"
]

/-- Nearby checked names used or audited for the Yang-Mills boundary. -/
def mathlibAnchorNames : List String := [
  "CovariantDerivative",
  "IsCovariantDerivativeOn",
  "CovariantDerivative.addOneForm",
  "CovariantDerivative.difference",
  "ContMDiffCovariantDerivative",
  "Bundle.ContMDiffRiemannianMetric",
  "riemannianMetricVectorSpace",
  "VectorBundle",
  "TangentSpace",
  "MulAction",
  "ContinuousLinearMap",
  "ContinuousLinearMap.id",
  "MemLp",
  "MemLp.eLpNorm_lt_top",
  "MeasureTheory.MemLp.continuousLinearMap_comp",
  "eLpNorm",
  "InnerProductSpace"
]

/-- Primary-source anchors for the pinned local Lean 4 dependency closure. -/
def primarySourceAnchors : List String := [
  "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Geometry/Manifold/VectorBundle/CovariantDerivative/Basic.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Geometry/Manifold/Riemannian/Basic.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean"
]

/-- Public integration note for the private-worker artifact. -/
def privateWorkerArtifactNote : String :=
  "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_197.lean is the " ++
  "private-worker Stage1 artifact for S1-M-197 / THM-M-1529. It validates " ++
  "a conditional non-abelian Yang-Mills statement shape, gauge-orbit wrappers, " ++
  "and MemLp/Hodge-star substrate wrappers. It is not a terminal proof of " ++
  "Yang-Mills theory and it is intentionally not imported through a shared " ++
  "Lean aggregator by this worker."

/-- Search terms that did not locate a terminal Yang-Mills theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Yang-Mills",
  "YangMills",
  "Mills",
  "gauge theory",
  "principal connection",
  "curvature two-form",
  "Hodge star",
  "instanton",
  "self-dual Yang-Mills",
  "covariant divergence",
  "Euler-Lagrange Yang-Mills"
]

/-! ## C004 formalization-debt gate -/

/--
Machine-readable M0387 debt label for the terminal non-abelian Yang-Mills
theorem.

The checked declarations above are statement-shape and substrate wrappers.
They do not construct the concrete principal-bundle, curvature, Hodge-star,
finite-action integral, or Euler-Lagrange/PDE bridge required for terminal
non-abelian Yang-Mills gauge theory.
-/
def terminalYangMillsDebtStatus : String := "formalization_debt"

/--
Concrete gates that must close before this slot can move beyond
`formalization_debt`.
-/
def terminalYangMillsDebtGates : List String := [
  "formalize_or_import_principal_bundle_connections",
  "formalize_or_import_curvature_two_forms_for_principal_or_adjoint_connections",
  "construct_metric_orientation_hodge_star_on_adjoint_valued_forms",
  "define_the_yang_mills_action_integral_and_its_finite_action_domain",
  "prove_the_variational_euler_lagrange_bridge_to_the_yang_mills_pde",
  "connect_the_pde_to_covariant_divergence_vanishing",
  "formalize_gauge_invariance_and_quotient_or_moduli_boundary",
  "pin_import_check_any_external_lean4_terminal_proof_before_completion"
]

/--
Status package for child `S1-M-197-C004`.

This is intentionally a gate, not a completion claim: the local file validates
only the conditional wrapper while the terminal theorem stays open.
-/
structure YangMillsC004FormalizationDebtGate where
  childID : String
  terminalDebtStatus : String
  statementShapeChecked : Bool
  terminalTheoremCompleted : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  requiredGates : List String
  nextAction : String

/-- Integration gate for child `S1-M-197-C004`. -/
def yangMillsC004FormalizationDebtGate : YangMillsC004FormalizationDebtGate := {
  childID := "S1-M-197-C004"
  terminalDebtStatus := terminalYangMillsDebtStatus
  statementShapeChecked := true
  terminalTheoremCompleted := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  requiredGates := terminalYangMillsDebtGates
  nextAction :=
    "Keep terminal non-abelian Yang-Mills open under formalization_debt until " ++
    "concrete principal-bundle connections, curvature two-forms, Hodge star, " ++
    "finite action, and the Euler-Lagrange/PDE bridge are formalized locally " ++
    "or imported through a pinned dependency that validates in this repository."
}

/-- The terminal theorem debt label is intentionally `formalization_debt`. -/
theorem terminalYangMillsDebtStatus_eq :
    terminalYangMillsDebtStatus = "formalization_debt" :=
  rfl

/-- The C004 gate is attached to the requested child task. -/
theorem yangMillsC004FormalizationDebtGate_childID_eq :
    yangMillsC004FormalizationDebtGate.childID = "S1-M-197-C004" :=
  rfl

/-- The C004 gate preserves the terminal `formalization_debt` classification. -/
theorem yangMillsC004FormalizationDebtGate_terminalDebtStatus_eq :
    yangMillsC004FormalizationDebtGate.terminalDebtStatus =
      "formalization_debt" :=
  rfl

/-- The local statement-shape wrapper is checked, but only conditionally. -/
theorem yangMillsC004FormalizationDebtGate_statementShapeChecked_eq_true :
    yangMillsC004FormalizationDebtGate.statementShapeChecked = true :=
  rfl

/-- The terminal non-abelian Yang-Mills theorem is not completed here. -/
theorem yangMillsC004FormalizationDebtGate_terminalTheoremCompleted_eq_false :
    yangMillsC004FormalizationDebtGate.terminalTheoremCompleted = false :=
  rfl

/--
M0387 gate: this child leaves no completed state retaining repo-local
integration debt.
-/
theorem yangMillsC004FormalizationDebtGate_repoLocalIntegrationDebtRetained_eq_false :
    yangMillsC004FormalizationDebtGate.repoLocalIntegrationDebtRetainedInCompletedState =
      false :=
  rfl

/-! ## C005 theorem-tree packages -/

/--
Machine-readable package node for the `S1-M-197-public-005` theorem tree.

These nodes are intentionally conservative: checked local wrappers are separated
from unchecked geometry/PDE and public-merge work, so a later integrator can
merge the same package names into the public blueprint without upgrading the
terminal theorem beyond `formalization_debt`.
-/
structure YangMillsTheoremTreePackage where
  packageName : String
  role : String
  localStatus : String
  maxLocalLeafSteps : Nat
  publicBackfillNeeded : Bool
  repoLocalIntegrationDebtInCompletedState : Bool

/-- Exact package names requested by child `S1-M-197-C005`. -/
def yangMillsC005PackageNames : List String := [
  "statement_normalization",
  "mathlib_object_model",
  "gauge_relation_leaf",
  "hodge_energy_leaf",
  "variational_bridge_wrapper",
  "geometry_pde_gap",
  "external_anchor_gate",
  "public_merge"
]

/-- Theorem-tree package ledger for child `S1-M-197-C005`. -/
def yangMillsC005TheoremTreePackages : List YangMillsTheoremTreePackage := [
  {
    packageName := "statement_normalization",
    role :=
      "Normalize the public Yang-Mills statement to the conditional " ++
      "StatementShape wrapper over explicit data and hypotheses.",
    localStatus := "checked_local_wrapper",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    packageName := "mathlib_object_model",
    role :=
      "Record the pinned mathlib substrate for covariant derivatives, " ++
      "vector bundles, Riemannian structures, Hilbert-space APIs, and MemLp.",
    localStatus := "checked_anchor_substrate_no_terminal_yang_mills",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    packageName := "gauge_relation_leaf",
    role :=
      "Expose the repo-local gauge equivalence relation and orbit wrappers " ++
      "using mathlib MulAction infrastructure.",
    localStatus := "checked_local_wrapper",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    packageName := "hodge_energy_leaf",
    role :=
      "Expose the abstract Hodge-star boundary, MemLp finite-action wrapper, " ++
      "energy eLpNorm wrapper, and Hodge-star MemLp preservation leaf.",
    localStatus := "checked_local_wrapper",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    packageName := "variational_bridge_wrapper",
    role :=
      "Use explicit proposition fields to bridge regular critical points to " ++
      "the encoded Yang-Mills equation and covariant-divergence conclusion.",
    localStatus := "checked_conditional_wrapper",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    packageName := "geometry_pde_gap",
    role :=
      "Keep principal-bundle connections, curvature two-forms, concrete " ++
      "Hodge star, action integral, and Euler-Lagrange/PDE bridge open.",
    localStatus := "formalization_debt_open",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    packageName := "external_anchor_gate",
    role :=
      "Require any future external Lean 4 terminal proof to be pinned, " ++
      "imported, and checked locally, or else record a concrete blocker.",
    localStatus := "no_external_terminal_anchor_integrated",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    packageName := "public_merge",
    role :=
      "Defer public blueprint/todo edits to the serialized integrator while " ++
      "providing exact backfill text in the private child ledger.",
    localStatus := "private_ledger_ready_public_merge_pending",
    maxLocalLeafSteps := 100,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  }
]

/-- Exact C005 theorem-tree package names are present in the requested order. -/
theorem yangMillsC005PackageNames_eq :
    yangMillsC005PackageNames = [
      "statement_normalization",
      "mathlib_object_model",
      "gauge_relation_leaf",
      "hodge_energy_leaf",
      "variational_bridge_wrapper",
      "geometry_pde_gap",
      "external_anchor_gate",
      "public_merge"
    ] :=
  rfl

/-- C005 records exactly eight theorem-tree packages. -/
theorem yangMillsC005PackageCount_eq :
    yangMillsC005TheoremTreePackages.length = 8 :=
  rfl

/--
M0387 gate for C005: the local package ledger does not mark any completed
state as retaining repo-local integration debt.
-/
def yangMillsC005RepoLocalIntegrationDebtGate : Bool :=
  yangMillsC005TheoremTreePackages.all
    (fun p => p.repoLocalIntegrationDebtInCompletedState = false)

/-- The C005 package ledger satisfies the repo-local integration-debt gate. -/
theorem yangMillsC005RepoLocalIntegrationDebtGate_eq_true :
    yangMillsC005RepoLocalIntegrationDebtGate = true :=
  rfl

/-! ## C006 unchecked public leaves -/

/--
Machine-readable unchecked public leaf for `S1-M-197-public-006`.

Each leaf is a public-backfill target rather than a completed theorem.  The
`unchecked` field is deliberately `true`, and no leaf is allowed to record a
completed state with repo-local integration debt.
-/
structure YangMillsUncheckedPublicLeaf where
  leafID : String
  topic : String
  requiredWork : String
  debtStatus : String
  unchecked : Bool
  publicBackfillNeeded : Bool
  repoLocalIntegrationDebtInCompletedState : Bool

/-- Exact unchecked leaf identifiers requested by child `S1-M-197-C006`. -/
def yangMillsC006LeafIDs : List String := [
  "principal_bundle_connection_modeling",
  "curvature_two_form_formalization",
  "metric_hodge_star_construction",
  "action_integral",
  "euler_lagrange_bridge",
  "gauge_quotient_moduli",
  "external_proof_audit"
]

/-- Unchecked public leaves for child `S1-M-197-C006`. -/
def yangMillsC006UncheckedPublicLeaves : List YangMillsUncheckedPublicLeaf := [
  {
    leafID := "principal_bundle_connection_modeling",
    topic := "principal-bundle connection modeling",
    requiredWork :=
      "Define or import principal bundles, smooth gauge groups, principal " ++
      "connections, associated adjoint bundles, and the connection " ++
      "regularity predicate used by the Yang-Mills statement.",
    debtStatus := "formalization_debt",
    unchecked := true,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    leafID := "curvature_two_form_formalization",
    topic := "curvature two-form formalization",
    requiredWork :=
      "Replace the abstract curvature field by the curvature two-form of a " ++
      "principal or adjoint connection, including gauge equivariance.",
    debtStatus := "formalization_debt",
    unchecked := true,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    leafID := "metric_hodge_star_construction",
    topic := "metric/Hodge-star construction",
    requiredWork :=
      "Construct the oriented metric-dependent Hodge star on adjoint-valued " ++
      "differential two-forms and prove the required sign and square laws.",
    debtStatus := "formalization_debt",
    unchecked := true,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    leafID := "action_integral",
    topic := "Yang-Mills action integral",
    requiredWork :=
      "Define the Yang-Mills action as the integral of the curvature norm " ++
      "squared, connect it to the current MemLp/eLpNorm wrapper, and state " ++
      "the finite-action domain with measurability and integrability gates.",
    debtStatus := "formalization_debt",
    unchecked := true,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    leafID := "euler_lagrange_bridge",
    topic := "Euler-Lagrange bridge",
    requiredWork :=
      "Prove or import the variational derivative of the Yang-Mills action " ++
      "and bridge critical points to the Yang-Mills PDE/covariant-divergence " ++
      "equation under the selected regularity hypotheses.",
    debtStatus := "formalization_debt",
    unchecked := true,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    leafID := "gauge_quotient_moduli",
    topic := "gauge quotient/moduli",
    requiredWork :=
      "Upgrade the checked MulAction gauge-orbit wrapper to a concrete gauge " ++
      "quotient or moduli boundary, including gauge invariance of curvature, " ++
      "action, equation, and finite-action predicates.",
    debtStatus := "formalization_debt",
    unchecked := true,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    leafID := "external_proof_audit",
    topic := "external proof audit",
    requiredWork :=
      "Run a primary-source Lean 4 audit for terminal Yang-Mills proofs and " ++
      "record repository URL, commit, theorem names, toolchain, placeholder " ++
      "status, and either pin/import/check closure or a concrete integration " ++
      "blocker.",
    debtStatus := "external_anchor_gate_open",
    unchecked := true,
    publicBackfillNeeded := true,
    repoLocalIntegrationDebtInCompletedState := false
  }
]

/-- Exact C006 unchecked public leaf identifiers are present in the requested order. -/
theorem yangMillsC006LeafIDs_eq :
    yangMillsC006LeafIDs = [
      "principal_bundle_connection_modeling",
      "curvature_two_form_formalization",
      "metric_hodge_star_construction",
      "action_integral",
      "euler_lagrange_bridge",
      "gauge_quotient_moduli",
      "external_proof_audit"
    ] :=
  rfl

/-- C006 records exactly seven unchecked public leaves. -/
theorem yangMillsC006UncheckedPublicLeafCount_eq :
    yangMillsC006UncheckedPublicLeaves.length = 7 :=
  rfl

/-- C006 intentionally leaves every public leaf unchecked. -/
def yangMillsC006AllLeavesUnchecked : Bool :=
  yangMillsC006UncheckedPublicLeaves.all (fun leaf => leaf.unchecked = true)

/-- The C006 public-leaf ledger records all leaves as unchecked. -/
theorem yangMillsC006AllLeavesUnchecked_eq_true :
    yangMillsC006AllLeavesUnchecked = true :=
  rfl

/--
M0387 gate for C006: no unchecked public leaf records a completed state with
repo-local integration debt.
-/
def yangMillsC006RepoLocalIntegrationDebtGate : Bool :=
  yangMillsC006UncheckedPublicLeaves.all
    (fun leaf => leaf.repoLocalIntegrationDebtInCompletedState = false)

/-- The C006 public-leaf ledger satisfies the repo-local integration-debt gate. -/
theorem yangMillsC006RepoLocalIntegrationDebtGate_eq_true :
    yangMillsC006RepoLocalIntegrationDebtGate = true :=
  rfl

/-! ## C007 external Lean 4 primary-source audit -/

/--
One primary-source audit row for child `S1-M-197-C007`.

This row records only source-audit metadata.  It does not pin, import, or
check any external project in this repository, and it does not close the
terminal non-abelian Yang-Mills theorem.
-/
structure YangMillsExternalAuditRow where
  repositoryURL : String
  commit : String
  toolchain : String
  sourceFiles : List String
  matchedSearchTerms : List String
  relevantNames : List String
  placeholderStatus : String
  terminalProofStatus : String
  integrationBlocker : String
  repoLocalClosure : Bool
  terminalProofClaimed : Bool
  repoLocalIntegrationDebtInCompletedState : Bool

/-- Date of the C007 external audit run. -/
def yangMillsC007AuditDate : String := "2026-05-01"

/-- Search terms requested by public child `S1-M-197-public-007`. -/
def yangMillsC007SearchTerms : List String := [
  "Yang-Mills",
  "YangMills",
  "principal connection",
  "curvature two-form",
  "Hodge star",
  "instanton",
  "covariant divergence"
]

/--
Primary-source audit rows for child `S1-M-197-C007`.

Every row is classified as non-terminal for the parent theorem.  Some projects
contain useful statement scaffolding or lattice/conditional work, but none is a
repo-local validated terminal proof of non-abelian Yang-Mills gauge theory.
-/
def yangMillsC007ExternalAuditRows : List YangMillsExternalAuditRow := [
  {
    repositoryURL := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    toolchain := "leanprover/lean4:v4.29.0",
    sourceFiles := [
      "Mathlib/Geometry/Manifold/VectorBundle/CovariantDerivative/Basic.lean",
      "Mathlib/Geometry/Manifold/Riemannian/Basic.lean",
      "Mathlib/MeasureTheory/Function/LpSpace/Basic.lean"
    ],
    matchedSearchTerms := [],
    relevantNames := [
      "CovariantDerivative",
      "IsCovariantDerivativeOn",
      "Bundle.ContMDiffRiemannianMetric",
      "MemLp",
      "eLpNorm"
    ],
    placeholderStatus := "pinned local dependency; no Yang-Mills terminal declaration found",
    terminalProofStatus := "no terminal Yang-Mills theorem in pinned mathlib closure",
    integrationBlocker :=
      "not an external terminal proof; only substrate for covariant derivatives, " ++
      "Riemannian geometry, Hilbert-space APIs, and MemLp",
    repoLocalClosure := true,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    repositoryURL := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems",
    commit := "540da94826f70f3edf4d4fc66ce6cda20e903f61",
    toolchain := "leanprover/lean4:v4.26.0",
    sourceFiles := [
      "Problems/YangMills/Quantum.lean",
      "Problems/YangMills/Millennium.lean"
    ],
    matchedSearchTerms := ["Yang-Mills", "YangMills"],
    relevantNames := [
      "GaugeField",
      "FieldStrength",
      "YangMillsAction",
      "QuantumYangMillsTheory",
      "HasMassGapSpectrum",
      "YangMillsExistenceAndMassGap"
    ],
    placeholderStatus :=
      "no active proof-placeholder or postulate tokens in Problems/YangMills source scan",
    terminalProofStatus := "statement scaffolding only; YangMillsExistenceAndMassGap is a Prop, not proved",
    integrationBlocker :=
      "no theorem proving existence of a nontrivial quantum Yang-Mills " ++
      "theory with spectral mass gap; no principal-connection or PDE bridge",
    repoLocalClosure := false,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    repositoryURL := "https://github.com/mrdouglasny/lgt",
    commit := "da3d49b62b7551bacb90d7dd89fea1600660a220",
    toolchain := "leanprover/lean4:v4.29.0",
    sourceFiles := [
      "LGT/GaugeField/Connection.lean",
      "LGT/MassGap/MassGap2D.lean",
      "LGT/MassGap/MassGap3D.lean",
      "LGT/MassGap/StrongCoupling.lean"
    ],
    matchedSearchTerms := ["Yang-Mills"],
    relevantNames := [
      "GaugeConnection",
      "GaugeTransform",
      "mass_gap_2d",
      "ym_mass_gap",
      "ym_mass_gap_UN",
      "ym_mass_gap_exponential_decay"
    ],
    placeholderStatus :=
      "one active proof placeholder in LGT/MassGap/StrongCoupling.lean at ym_mass_gap_exponential_decay",
    terminalProofStatus := "lattice/strong-coupling work, not terminal continuum Yang-Mills gauge theory",
    integrationBlocker :=
      "external project has active proof placeholder and targets lattice " ++
      "correlation decay rather than principal-bundle Yang-Mills PDE/variational closure",
    repoLocalClosure := false,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    repositoryURL := "https://github.com/lluiseriksson/ym-mass-gap-lean-verification",
    commit := "8f90610352b5fe79fb98029f7d04e83dd7d3d265",
    toolchain := "leanprover/lean4:stable in nested lean/lean-toolchain",
    sourceFiles := ["lean/YMProof.lean"],
    matchedSearchTerms := [],
    relevantNames := [
      "placeholder_statement",
      "placeholder_theorem"
    ],
    placeholderStatus := "repository README says the Lean layer is modular and partially axiomatized",
    terminalProofStatus := "placeholder theorem only; no Yang-Mills declaration audited",
    integrationBlocker :=
      "no terminal source theorem, no root Lake toolchain, and no concrete " ++
      "principal-connection, curvature, Hodge-star, or PDE bridge",
    repoLocalClosure := false,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    repositoryURL := "https://github.com/ember-research-lab/Spectral-Physics-Lean",
    commit := "48db03bfe75a1d15e5a06a17d38ab1271de513fb",
    toolchain := "leanprover/lean4:v4.29.0-rc6",
    sourceFiles := [
      "SpectralPhysics/QFT/YangMillsGap.lean",
      "SpectralPhysics/QFT/YangMillsConstruction.lean",
      "SpectralPhysics/QFT/ClayStatement.lean",
      "SpectralPhysics/Analysis/SpectralFlow.lean"
    ],
    matchedSearchTerms := ["Yang-Mills", "YangMills", "instanton"],
    relevantNames := [
      "SpectralPhysics.YangMills.mass_gap_discrete",
      "SpectralPhysics.YangMills.mass_gap_continuum",
      "SpectralPhysics.YangMillsConstruction.ym_mass_gap",
      "instanton_classification",
      "HasMassGap"
    ],
    placeholderStatus :=
      "source scan found active proof placeholders and active postulate declarations in the project",
    terminalProofStatus := "conditional spectral-physics/lattice scaffolding, not terminal Clay Yang-Mills",
    integrationBlocker :=
      "project records nonformalized Cheeger-Buser, spectral convergence, " ++
      "Wightman reconstruction, and multiscale log-Sobolev ingredients; " ++
      "also contains active placeholders",
    repoLocalClosure := false,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    repositoryURL := "https://github.com/lluiseriksson/THE-ERIKSSON-PROGRAMME",
    commit := "3e9fcb6dd5c23cbbc0c90ac481921713b36bf9ac",
    toolchain := "leanprover/lean4:v4.29.0-rc6",
    sourceFiles := [
      "YangMills/L8_Terminal/ClayTheorem.lean",
      "YangMills/L8_Terminal/ClayTrivialityAudit.lean",
      "YangMills/ErikssonBridge.lean"
    ],
    matchedSearchTerms := ["Yang-Mills", "YangMills", "instanton"],
    relevantNames := [
      "ClayYangMillsTheorem",
      "ClayYangMillsStrong",
      "clayYangMillsTheorem_trivial",
      "clayYangMillsStrong_trivial",
      "clay_yangmills_unconditional"
    ],
    placeholderStatus :=
      "project contains source-level postulate declarations and mathlib_pr_drafts with active proof-placeholder tokens",
    terminalProofStatus :=
      "nonterminal for this audit: ClayYangMillsTheorem is defined as exists m_phys, 0 < m_phys",
    integrationBlocker :=
      "audited terminal endpoint is explicitly trivialized by the project's " ++
      "own ClayTrivialityAudit and does not encode concrete non-abelian " ++
      "Yang-Mills existence/PDE content",
    repoLocalClosure := false,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    repositoryURL := "https://github.com/ertwro/yang-mills-mass-gap",
    commit := "213a90b7afd34256f78421da160565cf06cf84aa",
    toolchain := "nested lean/lakefile.lean requires mathlib v4.28.0; root lean-toolchain missing",
    sourceFiles := [
      "lean/Math/YangMills/MassGap.lean",
      "lean/Math/YangMills/Kirchhoff.lean"
    ],
    matchedSearchTerms := ["Yang-Mills", "YangMills"],
    relevantNames := [
      "yang_mills_mass_gap",
      "yang_mills_universal_bound",
      "yang_mills_gap_pos",
      "yang_mills_nontrivial",
      "kuratowski_triangle_free",
      "tau_subdiv_invariant"
    ],
    placeholderStatus := "two active axioms: kuratowski_triangle_free and tau_subdiv_invariant",
    terminalProofStatus := "discrete graph/Kirchhoff model, not terminal continuum Yang-Mills",
    integrationBlocker :=
      "active axioms and theorem mismatch: proves a discrete graph mass " ++
      "gap surrogate, not principal-bundle Yang-Mills theory",
    repoLocalClosure := false,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  },
  {
    repositoryURL := "https://github.com/psinary-sketch/SIDE-effects",
    commit := "b672cbaf7d2b54af7678570ff5813dc08d7138d0",
    toolchain := "leanprover/lean4:v4.30.0-rc2",
    sourceFiles := [
      "SIDEEffects/Structural.lean",
      "SIDEEffects/Milestones.lean"
    ],
    matchedSearchTerms := ["YangMills", "instanton"],
    relevantNames := [
      "YangMills.Sector",
      "YangMills.gapped",
      "YangMills.mass_gap",
      "YangMills.all_excluded",
      "YangMills.sectors_complete"
    ],
    placeholderStatus :=
      "YangMills.Structural has no proof placeholders but Milestones.lean contains active proof-placeholder tokens",
    terminalProofStatus := "propositional sector toy model, not terminal Yang-Mills formalization",
    integrationBlocker :=
      "gapped sectors are defined as True, so the result does not encode " ++
      "analytic Yang-Mills existence, mass gap, principal connections, " ++
      "curvature, Hodge star, or covariant divergence",
    repoLocalClosure := false,
    terminalProofClaimed := false,
    repoLocalIntegrationDebtInCompletedState := false
  }
]

/-- C007 audited exactly eight primary-source rows. -/
theorem yangMillsC007ExternalAuditRows_length_eq :
    yangMillsC007ExternalAuditRows.length = 8 :=
  rfl

/-- C007 did not identify a terminal external Lean 4 proof to pin. -/
def yangMillsC007TerminalExternalProofFound : Bool :=
  yangMillsC007ExternalAuditRows.any (fun row => row.terminalProofClaimed = true)

/-- The C007 audit found no terminal external Lean 4 proof claim. -/
theorem yangMillsC007TerminalExternalProofFound_eq_false :
    yangMillsC007TerminalExternalProofFound = false :=
  rfl

/--
M0387 gate for C007: no audited row is being treated as a completed state
with repo-local integration debt.
-/
def yangMillsC007RepoLocalIntegrationDebtGate : Bool :=
  yangMillsC007ExternalAuditRows.all
    (fun row => row.repoLocalIntegrationDebtInCompletedState = false)

/-- The C007 audit satisfies the repo-local integration-debt gate. -/
theorem yangMillsC007RepoLocalIntegrationDebtGate_eq_true :
    yangMillsC007RepoLocalIntegrationDebtGate = true :=
  rfl

/-! ## C008 future external terminal-proof integration gate -/

/--
Integration gate for child `S1-M-197-C008`.

This records the exact M0387 rule for any future external terminal Lean 4
Yang-Mills proof: a URL, theorem name, or audit row is not completion.  The
proof must be brought into this repository's validation closure, or a concrete
integration blocker must remain attached while the parent stays open.
-/
structure YangMillsC008ExternalTerminalProofGate where
  childID : String
  latestAuditChildID : String
  externalTerminalProofFound : Bool
  repoLocalPinImportCheckPerformed : Bool
  exactIntegrationBlocker : String
  completedStateAllowed : Bool
  repoLocalIntegrationDebtInCompletedState : Bool

/--
C008 gate result after the C007 primary-source audit.

No terminal external Lean 4 proof was found, so there is no integration-ready
dependency to pin in this pass.  The blocker is exact: the latest audit found
only substrate, scaffolding, placeholder/axiomatized work, lattice or
surrogate models, and toy endpoints rather than a closed terminal theorem for
non-abelian Yang-Mills gauge theory.
-/
def yangMillsC008ExternalTerminalProofGate :
    YangMillsC008ExternalTerminalProofGate := {
  childID := "S1-M-197-C008"
  latestAuditChildID := "S1-M-197-C007"
  externalTerminalProofFound := yangMillsC007TerminalExternalProofFound
  repoLocalPinImportCheckPerformed := false
  exactIntegrationBlocker :=
    "No terminal external Lean 4 proof was found by S1-M-197-C007. " ++
    "The audited candidates are substrate, statement scaffolding, " ++
    "placeholder or axiomatized workspaces, lattice/spectral or graph " ++
    "surrogates, or propositional toy models; none supplies a closed " ++
    "principal-bundle connection, curvature two-form, Hodge-star, " ++
    "finite-action, Euler-Lagrange/PDE, covariant-divergence, and gauge-" ++
    "quotient/moduli proof that can be pinned/imported/checked here."
  completedStateAllowed := false
  repoLocalIntegrationDebtInCompletedState := false
}

/-- The C008 gate is attached to the requested child task. -/
theorem yangMillsC008ExternalTerminalProofGate_childID_eq :
    yangMillsC008ExternalTerminalProofGate.childID = "S1-M-197-C008" :=
  rfl

/-- C008 consumes the latest C007 external-audit finding. -/
theorem yangMillsC008ExternalTerminalProofGate_latestAuditChildID_eq :
    yangMillsC008ExternalTerminalProofGate.latestAuditChildID =
      "S1-M-197-C007" :=
  rfl

/-- No terminal external Lean 4 proof is currently available to pin. -/
theorem yangMillsC008ExternalTerminalProofGate_externalProofFound_eq_false :
    yangMillsC008ExternalTerminalProofGate.externalTerminalProofFound = false :=
  rfl

/--
No pin/import/check action was performed because the audit found no terminal
external proof target.
-/
theorem yangMillsC008ExternalTerminalProofGate_pinImportCheck_eq_false :
    yangMillsC008ExternalTerminalProofGate.repoLocalPinImportCheckPerformed =
      false :=
  rfl

/-- C008 does not permit a theorem-completed state. -/
theorem yangMillsC008ExternalTerminalProofGate_completedStateAllowed_eq_false :
    yangMillsC008ExternalTerminalProofGate.completedStateAllowed = false :=
  rfl

/-!
M0387 gate: the current non-completion state does not retain completed-state
repo-local integration debt.
-/
theorem yangMillsC008ExternalTerminalProofGate_repoLocalIntegrationDebt_eq_false :
    yangMillsC008ExternalTerminalProofGate.repoLocalIntegrationDebtInCompletedState =
      false :=
  rfl

/-! ## Audit probes -/

#check IsNonAbelianGroup
#check GaugeEquivalent
#check gaugeEquivalent_refl
#check gaugeEquivalent_symm
#check gaugeEquivalent_trans
#check HodgeStar
#check IsSelfDual
#check isSelfDual_zero
#check NonAbelianYangMillsData
#check FiniteYangMillsAction
#check YangMillsEnergy
#check yangMillsEnergy_lt_top_of_finiteAction
#check hodgeStar_curvature_memLp
#check YangMillsHypotheses
#check YangMillsSolution
#check StatementShape
#check statementShape_from_variationalBridge
#check mathlibPinnedRevision
#check publicTaskMathlibSubstrateModules
#check publicTaskC002SubstrateAudit
#check mathlibPinnedRevision_eq
#check publicTaskMathlibSubstrateModules_eq
#check publicTaskC002SubstrateAudit_eq
#check mathlibAnchorModules
#check mathlibAnchorNames
#check primarySourceAnchors
#check privateWorkerArtifactNote
#check absentTerminalSearchTerms
#check terminalYangMillsDebtStatus
#check terminalYangMillsDebtGates
#check YangMillsC004FormalizationDebtGate
#check yangMillsC004FormalizationDebtGate
#check terminalYangMillsDebtStatus_eq
#check yangMillsC004FormalizationDebtGate_childID_eq
#check yangMillsC004FormalizationDebtGate_terminalDebtStatus_eq
#check yangMillsC004FormalizationDebtGate_statementShapeChecked_eq_true
#check yangMillsC004FormalizationDebtGate_terminalTheoremCompleted_eq_false
#check yangMillsC004FormalizationDebtGate_repoLocalIntegrationDebtRetained_eq_false
#check YangMillsTheoremTreePackage
#check yangMillsC005PackageNames
#check yangMillsC005TheoremTreePackages
#check yangMillsC005PackageNames_eq
#check yangMillsC005PackageCount_eq
#check yangMillsC005RepoLocalIntegrationDebtGate
#check yangMillsC005RepoLocalIntegrationDebtGate_eq_true
#check YangMillsUncheckedPublicLeaf
#check yangMillsC006LeafIDs
#check yangMillsC006UncheckedPublicLeaves
#check yangMillsC006LeafIDs_eq
#check yangMillsC006UncheckedPublicLeafCount_eq
#check yangMillsC006AllLeavesUnchecked
#check yangMillsC006AllLeavesUnchecked_eq_true
#check yangMillsC006RepoLocalIntegrationDebtGate
#check yangMillsC006RepoLocalIntegrationDebtGate_eq_true
#check YangMillsExternalAuditRow
#check yangMillsC007AuditDate
#check yangMillsC007SearchTerms
#check yangMillsC007ExternalAuditRows
#check yangMillsC007ExternalAuditRows_length_eq
#check yangMillsC007TerminalExternalProofFound
#check yangMillsC007TerminalExternalProofFound_eq_false
#check yangMillsC007RepoLocalIntegrationDebtGate
#check yangMillsC007RepoLocalIntegrationDebtGate_eq_true
#check YangMillsC008ExternalTerminalProofGate
#check yangMillsC008ExternalTerminalProofGate
#check yangMillsC008ExternalTerminalProofGate_childID_eq
#check yangMillsC008ExternalTerminalProofGate_latestAuditChildID_eq
#check yangMillsC008ExternalTerminalProofGate_externalProofFound_eq_false
#check yangMillsC008ExternalTerminalProofGate_pinImportCheck_eq_false
#check yangMillsC008ExternalTerminalProofGate_completedStateAllowed_eq_false
#check yangMillsC008ExternalTerminalProofGate_repoLocalIntegrationDebt_eq_false
#check CovariantDerivative
#check IsCovariantDerivativeOn
#check MemLp
#check eLpNorm

end AwesomeTheorems.Stage1.S1_M_197
