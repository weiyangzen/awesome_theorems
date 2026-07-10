import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.GroupTheory.Descent
import Mathlib.NumberTheory.NumberField.Basic

/-!
# S1-M-092 / THM-M-0450: Mordell-Weil theorem, Stage1 statement shape

This Stage1 artifact records the Lean 4 boundary for the Mordell-Weil theorem:
the rational points of an elliptic curve over a number field form a finitely
generated abelian group.

The local mathlib pin has Weierstrass curves, nonsingular Jacobian points with
an abelian group law, Northcott-style height infrastructure, and the abstract
descent theorem used in standard Mordell-Weil proofs.  It does not expose a
terminal theorem proving finite generation of `E(K)` for every elliptic curve
over every number field, so the main theorem is kept as a statement shape.

External audit note: `MichaelStollBayreuth/Heights` at commit
`688bdb63259556fab4b0f699ce0d10bd2dce23f6` has partial infrastructure in
`Heights/EllipticCurve.lean`, including `weakMW_implies_MW`, a conditional
descent theorem from weak Mordell-Weil and height hypotheses to finite
generation for its short-Weierstrass point model.  That project is not imported
or pinned by this repository, and this file does not treat it as a full
placeholder-free terminal Mordell-Weil proof.
-/

noncomputable section

universe u

namespace AwesomeTheorems.Stage1.S1_M_092

/--
How this Stage1 artifact should be exposed from the shared Lean tree.

The shared aggregator path is reserved for a serialized integrator.  This child
keeps `S1_M_092.lean` as a scoped validation file checked directly by
`lake env lean`, because the file is a statement-shape/descent-bridge artifact
rather than a terminal Mordell-Weil proof.
-/
inductive Stage1SurfaceMode where
  | scopedValidationFile
  | aggregatorImport
  deriving DecidableEq, Repr

/--
Current C008 decision: do not add `S1_M_092.lean` to a shared Lean import
aggregator in this parallel child pass.  A serialized integrator may revisit
the import only after the public Stage1 surface records that this is a
statement-shape/descent-bridge artifact and not a full Mordell-Weil proof.
-/
def selectedStage1SurfaceMode : Stage1SurfaceMode :=
  .scopedValidationFile

theorem selectedStage1SurfaceMode_eq :
    selectedStage1SurfaceMode = Stage1SurfaceMode.scopedValidationFile := rfl

/-- The mathlib type used here for the group of rational points of a Weierstrass
elliptic curve over `K`, in Jacobian coordinates. -/
abbrev RationalPointGroup (K : Type u) [Field K] (E : WeierstrassCurve K) :=
  E.toJacobian.Point

/--
Stage1 normalized statement shape for the Mordell-Weil theorem.

For every number field `K` and every elliptic Weierstrass curve `E/K`, the
additive group of nonsingular `K`-rational points is finitely generated.

This is not proved in this repository by this file; it is the target boundary
for a future local proof body or pinned upstream wrapper.
-/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (E : WeierstrassCurve K),
    E.IsElliptic → AddGroup.FG (RationalPointGroup K E)

/--
Checked mathlib descent anchor.

This is the abstract finite-generation theorem used in the standard
Mordell-Weil proof: finite index of doubling, a nonnegative Northcott height,
and an approximate parallelogram law imply finite generation.
-/
theorem addCommGroup_descent_anchor {G : Type u} [AddCommGroup G] {h : G → ℝ} {C : ℝ}
    (weakMW : (nsmulAddMonoidHom (α := G) 2).range.FiniteIndex)
    (height_nonnegative : ∀ x, 0 ≤ h x)
    (approx_parallelogram :
      ∀ x y, |h (x + y) + h (x - y) - 2 * (h x + h y)| ≤ C)
    [Northcott h] :
    AddGroup.FG G :=
  AddCommGroup.fg_of_descent' weakMW height_nonnegative approx_parallelogram

/--
Checked mathlib point-group object-model anchor.

`Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point` supplies the
Jacobian-coordinate rational-point type, and
`WeierstrassCurve.Jacobian.Point.instAddCommGroup` supplies its additive
commutative group structure.
-/
@[reducible] def jacobian_point_addCommGroup_anchor (K : Type u) [Field K] (E : WeierstrassCurve K) :
    AddCommGroup (RationalPointGroup K E) :=
  inferInstance

/--
Repo-local Mordell-Weil reduction wrapper for the mathlib elliptic-curve point
group model.

The hypotheses are exactly the missing arithmetic geometry inputs for this
Stage1 slot: weak Mordell-Weil finite-index doubling, a suitable Northcott
height, nonnegativity, and the approximate parallelogram law.  Under those
inputs, the local mathlib descent theorem proves finite generation of the
Jacobian-coordinate rational point group.
-/
theorem jacobian_points_descent_bridge (K : Type u) [Field K] [NumberField K]
    (E : WeierstrassCurve K) {h : RationalPointGroup K E → ℝ} {C : ℝ}
    (weakMW : (nsmulAddMonoidHom (α := RationalPointGroup K E) 2).range.FiniteIndex)
    (height_nonnegative : ∀ P, 0 ≤ h P)
    (approx_parallelogram :
      ∀ P Q, |h (P + Q) + h (P - Q) - 2 * (h P + h Q)| ≤ C)
    [Northcott h] :
    AddGroup.FG (RationalPointGroup K E) :=
  addCommGroup_descent_anchor weakMW height_nonnegative approx_parallelogram

/-! ## Future proof-package split

The eight constructors below are a repo-local, Lean-checked index of the public
child packages that must remain separate when the statement-shape artifact is
upgraded into a terminal proof.  They are bookkeeping data only: the checked
packages identify current local anchors, while the remaining packages record
formalization debt and do not assert the Mordell-Weil theorem.
-/

/-- Canonical future proof packages for the Mordell-Weil Stage1 slot. -/
inductive ProofPackage where
  | statement_normalization
  | point_group_model
  | abstract_descent_bridge
  | height_model
  | approx_parallelogram
  | weak_mordell_weil
  | model_equivalence
  | terminal_assembly
  deriving DecidableEq, Repr

namespace ProofPackage

/-- Stable public name for each future proof package. -/
def canonicalName : ProofPackage → String
  | statement_normalization => "statement_normalization"
  | point_group_model => "point_group_model"
  | abstract_descent_bridge => "abstract_descent_bridge"
  | height_model => "height_model"
  | approx_parallelogram => "approx_parallelogram"
  | weak_mordell_weil => "weak_mordell_weil"
  | model_equivalence => "model_equivalence"
  | terminal_assembly => "terminal_assembly"

/-- Current repo-local status of a future proof package. -/
def localStatus : ProofPackage → String
  | statement_normalization => "checked_statement_shape"
  | point_group_model => "checked_mathlib_object_model_anchor"
  | abstract_descent_bridge => "checked_mathlib_descent_wrapper"
  | height_model => "formalization_debt"
  | approx_parallelogram => "formalization_debt"
  | weak_mordell_weil => "formalization_debt"
  | model_equivalence => "formalization_debt"
  | terminal_assembly => "formalization_debt_not_repo_local_closed"

/-- Packages with repo-local checked anchors in this artifact. -/
def hasLocalCheckedAnchor : ProofPackage → Prop
  | statement_normalization => True
  | point_group_model => True
  | abstract_descent_bridge => True
  | height_model => False
  | approx_parallelogram => False
  | weak_mordell_weil => False
  | model_equivalence => False
  | terminal_assembly => False

end ProofPackage

/-- The exact public child-package split requested for future Mordell-Weil work. -/
def futureProofPackages : List ProofPackage :=
  [ ProofPackage.statement_normalization
  , ProofPackage.point_group_model
  , ProofPackage.abstract_descent_bridge
  , ProofPackage.height_model
  , ProofPackage.approx_parallelogram
  , ProofPackage.weak_mordell_weil
  , ProofPackage.model_equivalence
  , ProofPackage.terminal_assembly
  ]

/-- String form of the package split, suitable for public backfill. -/
def futureProofPackageNames : List String :=
  futureProofPackages.map ProofPackage.canonicalName

/-- Checked equality pinning the public package names and order. -/
theorem futureProofPackageNames_eq :
    futureProofPackageNames =
      [ "statement_normalization"
      , "point_group_model"
      , "abstract_descent_bridge"
      , "height_model"
      , "approx_parallelogram"
      , "weak_mordell_weil"
      , "model_equivalence"
      , "terminal_assembly"
      ] :=
  rfl

/-- The statement-normalization package is locally represented by `StatementShape`. -/
theorem statement_normalization_package_anchor :
    ProofPackage.hasLocalCheckedAnchor ProofPackage.statement_normalization :=
  trivial

/-- The point-group-model package is locally represented by the Jacobian point group instance. -/
theorem point_group_model_package_anchor (K : Type u) [Field K] (E : WeierstrassCurve K) :
    ProofPackage.hasLocalCheckedAnchor ProofPackage.point_group_model ∧
      Nonempty (AddCommGroup (RationalPointGroup K E)) :=
  ⟨trivial, ⟨jacobian_point_addCommGroup_anchor K E⟩⟩

/-- The abstract-descent package is locally represented by the descent bridge wrapper. -/
theorem abstract_descent_bridge_package_anchor (K : Type u) [Field K] [NumberField K]
    (E : WeierstrassCurve K) {h : RationalPointGroup K E → ℝ} {C : ℝ}
    (weakMW : (nsmulAddMonoidHom (α := RationalPointGroup K E) 2).range.FiniteIndex)
    (height_nonnegative : ∀ P, 0 ≤ h P)
    (approx_parallelogram :
      ∀ P Q, |h (P + Q) + h (P - Q) - 2 * (h P + h Q)| ≤ C)
    [Northcott h] :
    ProofPackage.hasLocalCheckedAnchor ProofPackage.abstract_descent_bridge ∧
      AddGroup.FG (RationalPointGroup K E) :=
  ⟨trivial, jacobian_points_descent_bridge K E weakMW height_nonnegative approx_parallelogram⟩

/-! ## Completion gate inventory

These constructors make the public "do not mark complete until every gate is
closed" rule visible in the Lean artifact.  The true values below are audit
gates closed for this statement-shape file; they are not a proof of
`StatementShape`.
-/

/-- Completion gates that must all close before `S1-M-092` can be marked complete. -/
inductive CompletionGate where
  | weak_mordell_weil
  | height_northcott_parallelogram
  | model_equivalence
  | local_lean_validation
  | public_mergeback
  | repo_local_integration_debt
  deriving DecidableEq, Repr

namespace CompletionGate

/-- Stable public name for each Mordell-Weil completion gate. -/
def canonicalName : CompletionGate → String
  | weak_mordell_weil => "weak_mordell_weil"
  | height_northcott_parallelogram => "height_northcott_parallelogram"
  | model_equivalence => "model_equivalence"
  | local_lean_validation => "local_lean_validation"
  | public_mergeback => "public_mergeback"
  | repo_local_integration_debt => "repo_local_integration_debt"

/-- Current gate status for this repo-local Stage1 artifact. -/
def currentStatus : CompletionGate → String
  | weak_mordell_weil => "open_formalization_debt"
  | height_northcott_parallelogram => "open_formalization_debt"
  | model_equivalence => "open_formalization_debt"
  | local_lean_validation => "closed_for_statement_shape_and_descent_bridge_only"
  | public_mergeback => "open_serial_public_doc_integration"
  | repo_local_integration_debt =>
      "closed_for_current_audit_no_full_external_terminal_proof_found"

/--
Whether the gate is closed for the current artifact.

The terminal theorem remains blocked because weak Mordell-Weil, the height
inputs, model equivalence, and public merge-back are still open.
-/
def currentlyClosedForCompletion : CompletionGate → Bool
  | weak_mordell_weil => false
  | height_northcott_parallelogram => false
  | model_equivalence => false
  | local_lean_validation => true
  | public_mergeback => false
  | repo_local_integration_debt => true

end CompletionGate

/-- The exact completion gates from the public Stage1 blocker. -/
def completionGates : List CompletionGate :=
  [ CompletionGate.weak_mordell_weil
  , CompletionGate.height_northcott_parallelogram
  , CompletionGate.model_equivalence
  , CompletionGate.local_lean_validation
  , CompletionGate.public_mergeback
  , CompletionGate.repo_local_integration_debt
  ]

/-- String form of the completion-gate split, suitable for public backfill. -/
def completionGateNames : List String :=
  completionGates.map CompletionGate.canonicalName

/-- Checked equality pinning the completion gate names and order. -/
theorem completionGateNames_eq :
    completionGateNames =
      [ "weak_mordell_weil"
      , "height_northcott_parallelogram"
      , "model_equivalence"
      , "local_lean_validation"
      , "public_mergeback"
      , "repo_local_integration_debt"
      ] :=
  rfl

/-- The current Stage1 artifact cannot close every completion gate. -/
theorem completionGates_not_all_closed :
    completionGates.all CompletionGate.currentlyClosedForCompletion = false :=
  rfl

/-- Concrete open gates that bar a completed Mordell-Weil claim in this artifact. -/
theorem terminalCompletionBlockedInThisArtifact :
    CompletionGate.currentlyClosedForCompletion CompletionGate.weak_mordell_weil = false ∧
    CompletionGate.currentlyClosedForCompletion CompletionGate.height_northcott_parallelogram = false ∧
    CompletionGate.currentlyClosedForCompletion CompletionGate.model_equivalence = false ∧
    CompletionGate.currentlyClosedForCompletion CompletionGate.public_mergeback = false :=
  ⟨rfl, rfl, rfl, rfl⟩

/-! ## Audit probes -/

#check NumberField
#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.toJacobian
#check WeierstrassCurve.Jacobian.Point
#check WeierstrassCurve.Jacobian.Point.instAddCommGroup
#check AddGroup.FG
#check Northcott
#check AddCommGroup.fg_of_descent'
#check StatementShape
#check Stage1SurfaceMode
#check selectedStage1SurfaceMode
#check selectedStage1SurfaceMode_eq
#check addCommGroup_descent_anchor
#check jacobian_point_addCommGroup_anchor
#check jacobian_points_descent_bridge
#check ProofPackage
#check ProofPackage.canonicalName
#check ProofPackage.localStatus
#check ProofPackage.hasLocalCheckedAnchor
#check futureProofPackages
#check futureProofPackageNames_eq
#check statement_normalization_package_anchor
#check point_group_model_package_anchor
#check abstract_descent_bridge_package_anchor
#check CompletionGate
#check CompletionGate.canonicalName
#check CompletionGate.currentStatus
#check CompletionGate.currentlyClosedForCompletion
#check completionGates
#check completionGateNames_eq
#check completionGates_not_all_closed
#check terminalCompletionBlockedInThisArtifact

end AwesomeTheorems.Stage1.S1_M_092
