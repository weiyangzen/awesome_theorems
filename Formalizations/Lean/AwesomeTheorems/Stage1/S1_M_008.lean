import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Properties
import Mathlib.GroupTheory.Descent
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.NumberField.Basic

/-!
# S1-M-008 / THM-M-0395: Faltings theorem

This Stage1 artifact records the repo-local Lean 4 boundary for Faltings's
theorem, in the Mordell-conjecture form: a smooth proper curve of genus at
least two over a number field has only finitely many rational points.

The current repository and pinned mathlib snapshot do not contain a terminal
Lean proof of Faltings's theorem.  The checked content below is therefore a
self-contained statement-shape module with mathlib-backed wrappers for the
scheme-theoretic hypotheses and rational-point section type.
-/

noncomputable section

open CategoryTheory
open AlgebraicGeometry

universe u

namespace AwesomeTheorems.Stage1.S1_M_008

/-! ## Canonical statement-normalization boundary -/

/-- Public theorem id normalized by this Stage1 child. -/
def theoremId : String :=
  "THM-M-0395"

/-- Canonical Lean namespace for the THM-M-0395 Stage1 statement artifact. -/
def canonicalNamespace : String :=
  "AwesomeTheorems.Stage1.S1_M_008"

/-- The affine base scheme `Spec K`, re-exported for this Faltings slot. -/
abbrev SpecOf (K : Type u) [CommRing K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/--
A `K`-rational point of `X` over `Spec K`, expressed as a section of the
structure map.
-/
abbrev RationalPointOver {K : Type u} [Field K] (X : Scheme.{u}) (π : X ⟶ SpecOf K) :
    Type u :=
  { p : SpecOf K ⟶ X // p ≫ π = 𝟙 (SpecOf K) }

/--
Predicate slots for the geometric hypotheses not yet exposed by a stable
audited mathlib curve-genus API in this repository.
-/
structure CurvePredicateSlots (K : Type u) [Field K] [NumberField K]
    (X : Scheme.{u}) (π : X ⟶ SpecOf K) where
  geometricallyConnected : Prop
  dimensionOne : Prop
  genusAtLeastTwo : Prop

/--
Hypothesis package for the Faltings/Mordell statement over a number field.

Smoothness and properness use mathlib morphism properties through `S1_M_042`;
geometric connectedness, dimension one, and genus at least two remain explicit
predicate slots.
-/
structure CurveHypothesesOverNumberField {K : Type u} [Field K] [NumberField K]
    {X : Scheme.{u}} {π : X ⟶ SpecOf K} (slots : CurvePredicateSlots K X π) : Prop where
  smooth : Smooth π
  proper : IsProper π
  geometricallyConnected : slots.geometricallyConnected
  dimensionOne : slots.dimensionOne
  genusAtLeastTwo : slots.genusAtLeastTwo

/--
Stage1 normalized statement shape for THM-M-0395.

For every number field `K` and every smooth proper geometrically connected
one-dimensional `K`-scheme with genus at least two, the type of `K`-rational
sections is finite.  This is the checked statement boundary, not a terminal
proof of Faltings's theorem.
-/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (X : Scheme.{u}) (π : X ⟶ SpecOf K)
    (slots : CurvePredicateSlots K X π),
    CurveHypothesesOverNumberField slots → Finite (RationalPointOver X π)

/--
Checked expansion of the canonical THM-M-0395 quantifier and conclusion shape.

This theorem is intentionally definitional: it records the normalized statement
surface without providing or claiming a proof of Faltings's theorem.
-/
theorem statementShape_eq_normalizedQuantifierConclusion :
    StatementShape.{u} =
      (∀ (K : Type u) [Field K] [NumberField K] (X : Scheme.{u}) (π : X ⟶ SpecOf K)
        (slots : CurvePredicateSlots K X π),
        CurveHypothesesOverNumberField slots → Finite (RationalPointOver X π)) :=
  rfl

/-! ## Formalization-debt frontier and partial target queue -/

/--
Machine-readable status labels for the current Faltings/Mordell frontier.

`checkedStatementShape` and `checkedMathlibAnchor` are local facts about this
module and the pinned mathlib imports.  The other constructors describe open
frontier categories and must not be read as theorem completions.
-/
inductive FrontierStatus where
  | checkedStatementShape
  | checkedMathlibAnchor
  | partialMathlibAnchor
  | explicitPredicateSlot
  | partialTargetOnly
  | formalizationDebt
  | integrationBlocked
  deriving DecidableEq, Repr

/--
Canonical local nodes for the current Faltings formalization frontier.

The statement/object-model nodes and the height/Northcott/descent node have
checked local or mathlib anchors.  The latter is still only partial
infrastructure, not a proof of Faltings's theorem.  The remaining nodes are the
target leaves that still require new mathlib APIs, external dependency
integration, or future proof development.
-/
inductive FaltingsFrontierNode where
  | numberFieldBase
  | schemeSmoothProperMorphism
  | rationalPointSectionType
  | geometricConnectednessSlot
  | dimensionOneCurveSlot
  | genusAtLeastTwoSlot
  | heightNorthcottDescent
  | curveToJacobianBridge
  | abelianVarietyFaltingsCore
  | terminalRationalPointFiniteness
  deriving DecidableEq, Repr

/-- Current checked/open status for each local Faltings frontier node. -/
def frontierNodeStatus : FaltingsFrontierNode → FrontierStatus
  | .numberFieldBase => .checkedMathlibAnchor
  | .schemeSmoothProperMorphism => .checkedMathlibAnchor
  | .rationalPointSectionType => .checkedStatementShape
  | .geometricConnectednessSlot => .explicitPredicateSlot
  | .dimensionOneCurveSlot => .explicitPredicateSlot
  | .genusAtLeastTwoSlot => .explicitPredicateSlot
  | .heightNorthcottDescent => .partialMathlibAnchor
  | .curveToJacobianBridge => .formalizationDebt
  | .abelianVarietyFaltingsCore => .formalizationDebt
  | .terminalRationalPointFiniteness => .formalizationDebt

/-- The local rational-point target is already normalized as a section type. -/
theorem rationalPointSectionType_status :
    frontierNodeStatus .rationalPointSectionType = .checkedStatementShape :=
  rfl

/--
The terminal rational-point finiteness theorem remains formalization debt in
this repo-local Lean closure.
-/
theorem terminalRationalPointFiniteness_status :
    frontierNodeStatus .terminalRationalPointFiniteness = .formalizationDebt :=
  rfl

/--
The height/Northcott/descent node has checked mathlib anchors, but only as
partial infrastructure separated from the full Faltings theorem.
-/
theorem heightNorthcottDescent_status :
    frontierNodeStatus .heightNorthcottDescent = .partialMathlibAnchor :=
  rfl

/--
The open predicate slots should later be replaced by audited mathlib curve and
genus APIs, if such APIs become available.
-/
def predicateSlotFrontierNodes : List FaltingsFrontierNode := [
  .geometricConnectednessSlot,
  .dimensionOneCurveSlot,
  .genusAtLeastTwoSlot
]

/--
First partial Lean 4 targets after statement normalization.

These are deliberately target names, not theorem declarations.  They are the
next APIs/proof packages needed before a terminal Faltings wrapper could be
stated without opaque predicate slots.
-/
def partialLeanTargetQueue : List String := [
  "replace geometric connectedness slot with audited mathlib scheme/curve API",
  "replace dimension-one slot with audited curve or relative-dimension API",
  "replace genus-at-least-two slot with audited genus-of-curve API",
  "connect checked height/Northcott/descent anchors to rational points on curves or Jacobians",
  "define curve-to-Jacobian bridge target for rational points",
  "identify abelian-variety finiteness/Faltings core target or integration blocker",
  "split independently budgeted special-case packages without using them as terminal evidence",
  "state terminal wrapper only after the upstream/local proof body is in the repo-local closure"
]

/--
M0387-level theorem-tree frontier for this Faltings slot.

Each item is still `unchecked`: none is currently a leaf with a repo-local
`<=100` step proof ledger for the full theorem.
-/
def theoremTreeFrontier : List String := [
  "F0 statement normalization and rational-point section type: checked statement-shape only",
  "F1 object-model replacement for connected curve, dimension one, and genus at least two: unchecked",
  "F2 height/Northcott and abstract descent anchors: checked partial infrastructure; curve/Jacobian bridge unchecked",
  "F3 curve-to-Jacobian bridge from rational points to abelian-variety arithmetic: unchecked",
  "F4 Faltings abelian-variety core / subvariety finiteness input: unchecked",
  "F5 special-case packages such as low-genus exclusions, field/base-change variants, and effective/height subpackages: unchecked",
  "F6 terminal Mordell wrapper proving finiteness of RationalPointOver: unchecked"
]

/-! ## Theorem-tree expansion package split -/

/--
The independently budgeted proof packages requested for the Faltings/Mordell
theorem-tree expansion.

These constructors are planning nodes only.  They do not assert that the
corresponding proofs are available in this repository.
-/
inductive TheoremTreePackage where
  | curveToJacobianBridge
  | abelianVarietyFaltingsCore
  | specialCasePackages
  deriving DecidableEq, Repr

/-- One independently budgeted theorem-tree leaf for the open Faltings slot. -/
structure BudgetedTheoremTreeLeaf where
  package : TheoremTreePackage
  leafId : String
  obligation : String
  upstreamInputs : String
  downstreamInterface : String
  budgetStepLimit : Nat
  repoLocalStatus : FrontierStatus
  completionBoundary : String

/-- M0387 local proof-leaf budget limit used by this Stage1 expansion. -/
def theoremTreeLeafBudgetLimit : Nat :=
  100

/--
Integration-ready theorem-tree split for the open Faltings/Mordell proof.

Every listed leaf is independently budgeted at `<= 100` local proof steps and
remains non-completed until a checked proof body or pinned/imported upstream
closure exists.  The rows are deliberately package-level leaves for the public
backfill surface; future workers must split any row that exceeds this budget.
-/
def budgetedTheoremTreeLeaves : List BudgetedTheoremTreeLeaf := [
  {
    package := .curveToJacobianBridge,
    leafId := "S1-M-008-TT01-rational-point-to-jacobian-map",
    obligation := "Define the Abel-Jacobi/Jacobian map from curve rational points using audited curve and divisor/Picard/Jacobian APIs.",
    upstreamInputs := "normalized RationalPointOver section type; future audited smooth proper geometrically integral curve package; genus slot replacement",
    downstreamInterface := "map from curve rational points into a Jacobian or abelian-variety carrier with a stated finite-fiber/finiteness transfer target",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalStatus := .formalizationDebt,
    completionBoundary := "unchecked: no repo-local Jacobian API bridge or finite-fiber transfer proof is available"
  },
  {
    package := .curveToJacobianBridge,
    leafId := "S1-M-008-TT02-finite-fiber-or-embedding-transfer",
    obligation := "Split the finiteness transfer from curve rational points to the Jacobian image into a separate finite-fiber or embedding leaf.",
    upstreamInputs := "TT01 map; audited rational-point extensionality; curve hypothesis package",
    downstreamInterface := "finite image plus finite fibers imply Finite (RationalPointOver X pi)",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalStatus := .formalizationDebt,
    completionBoundary := "unchecked: terminal finite-fiber theorem is not present in the local closure"
  },
  {
    package := .abelianVarietyFaltingsCore,
    leafId := "S1-M-008-TT03-mordell-weil-height-input",
    obligation := "Package the Mordell-Weil/height input needed by the abelian-variety route, separated from the full Faltings theorem.",
    upstreamInputs := "checked Northcott/descent anchors in this file; future canonical height and abelian-variety group APIs",
    downstreamInterface := "finite-generation or bounded-height input usable by the Faltings core",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalStatus := .formalizationDebt,
    completionBoundary := "partial anchors only: local Northcott/descent wrappers do not prove the abelian-variety core"
  },
  {
    package := .abelianVarietyFaltingsCore,
    leafId := "S1-M-008-TT04-subvariety-finiteness-or-faltings-core",
    obligation := "Identify or formalize the abelian-variety Faltings/subvariety finiteness theorem that consumes the bridge output.",
    upstreamInputs := "TT03 height/Mordell-Weil package; future abelian-variety object model; external-primary-source audit if a terminal theorem is found",
    downstreamInterface := "finiteness of the relevant curve image or rational points after transfer",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalStatus := .formalizationDebt,
    completionBoundary := "unchecked: no pinned/imported terminal Lean 4 Faltings core theorem is available"
  },
  {
    package := .specialCasePackages,
    leafId := "S1-M-008-TT05-special-case-nonterminal-packages",
    obligation := "Isolate special cases such as genus-zero/genus-one exclusions, base-field variants, or effective bounded-height subpackages without treating them as the parent theorem.",
    upstreamInputs := "object-model audit table; external audit table; checked partial height/Northcott anchors",
    downstreamInterface := "nonterminal packages that may discharge local branches but cannot close THM-M-0395 without TT01-TT04 and the terminal wrapper",
    budgetStepLimit := theoremTreeLeafBudgetLimit,
    repoLocalStatus := .formalizationDebt,
    completionBoundary := "unchecked and nonterminal: special cases cannot be used as completed evidence for Faltings"
  }
]

/-- Current package-level status for the theorem-tree expansion. -/
def theoremTreePackageStatus : TheoremTreePackage → FrontierStatus
  | .curveToJacobianBridge => .formalizationDebt
  | .abelianVarietyFaltingsCore => .formalizationDebt
  | .specialCasePackages => .formalizationDebt

theorem curveToJacobianBridge_package_status :
    theoremTreePackageStatus .curveToJacobianBridge = .formalizationDebt :=
  rfl

theorem abelianVarietyFaltingsCore_package_status :
    theoremTreePackageStatus .abelianVarietyFaltingsCore = .formalizationDebt :=
  rfl

theorem specialCasePackages_package_status :
    theoremTreePackageStatus .specialCasePackages = .formalizationDebt :=
  rfl

/--
Gate for the public backfill: the requested theorem-tree package split exists
locally, but it is a non-completion artifact.
-/
def theoremTreeExpansionReadyForPublicBackfill : Bool :=
  true

theorem theoremTreeExpansionReadyForPublicBackfill_eq_true :
    theoremTreeExpansionReadyForPublicBackfill = true :=
  rfl

/--
No theorem-tree package introduced by this child can currently support a
completed Faltings checkbox.
-/
def theoremTreeExpansionClosesFaltings : Bool :=
  false

theorem theoremTreeExpansionClosesFaltings_eq_false :
    theoremTreeExpansionClosesFaltings = false :=
  rfl

/--
Current external-anchor audit result recorded in this local artifact.

`false` means no terminal external Lean 4 proof has been brought into this
repository's pinned verification closure.  This is not a global claim that no
external work can exist; it is the repo-local integration state for this pass.
-/
def terminalExternalLeanProofInRepoLocalClosure : Bool :=
  false

/-- No completed theorem state is claimed by the current artifact. -/
def theoremCompletionClaimed : Bool :=
  false

/--
Checked Boolean gate used by the ledger: the current artifact has no completed
state that depends on anchor-only external evidence.
-/
def noCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  !theoremCompletionClaimed || terminalExternalLeanProofInRepoLocalClosure

theorem noCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

namespace RationalPointOver

/-- A rational point over `Spec K` is a section of the structure map. -/
theorem comp_structureMap {K : Type u} [Field K] {X : Scheme.{u}} {π : X ⟶ SpecOf K}
    (p : RationalPointOver X π) :
    p.1 ≫ π = 𝟙 (SpecOf K) :=
  p.2

end RationalPointOver

namespace CurveHypothesesOverNumberField

/-- The smoothness hypothesis is available as a mathlib morphism property. -/
theorem smooth' {K : Type u} [Field K] [NumberField K]
    {X : Scheme.{u}} {π : X ⟶ SpecOf K}
    {slots : CurvePredicateSlots K X π} (h : CurveHypothesesOverNumberField slots) :
    Smooth π :=
  h.smooth

/-- The properness hypothesis is available as a mathlib morphism property. -/
theorem proper' {K : Type u} [Field K] [NumberField K]
    {X : Scheme.{u}} {π : X ⟶ SpecOf K}
    {slots : CurvePredicateSlots K X π} (h : CurveHypothesesOverNumberField slots) :
    IsProper π :=
  h.proper

end CurveHypothesesOverNumberField

/-! ## Height/Northcott and descent partial anchors -/

/--
Checked Northcott bounded-sublevel anchor.

This is the reusable finite-height-set input used by descent arguments.  It is
not a statement about rational points on curves.
-/
theorem northcott_finite_height_sublevel {α β : Type u} [LE β] (h : α → β)
    [Northcott h] (b : β) :
    {a : α | h a ≤ b}.Finite :=
  Northcott.finite_le b

/--
Checked additive descent anchor for Mordell-Weil-shaped finite-generation
arguments.

The hypotheses are intentionally explicit: finite index of doubling,
nonnegative Northcott height, and an approximate parallelogram law imply finite
generation of the additive group.  This partial anchor does not supply the
curve-to-Jacobian bridge, weak Mordell-Weil input, or the abelian-variety
Faltings core.
-/
theorem additive_descent_partial_anchor {G : Type u} [AddCommGroup G] {h : G → ℝ} {C : ℝ}
    (weakMW : (nsmulAddMonoidHom (α := G) 2).range.FiniteIndex)
    (height_nonnegative : ∀ x, 0 ≤ h x)
    (approx_parallelogram :
      ∀ x y, |h (x + y) + h (x - y) - 2 * (h x + h y)| ≤ C)
    [Northcott h] :
    AddGroup.FG G :=
  AddCommGroup.fg_of_descent' weakMW height_nonnegative approx_parallelogram

/-- One checked-row record for height/Northcott/descent infrastructure. -/
structure HeightNorthcottDescentAuditRow where
  component : String
  declarationName : String
  sourceLocation : String
  repoLocalStatus : String
  partialRole : String
  separationFromFaltings : String

/--
Audit rows for the partial height/Northcott/descent anchor.

These rows are integration-ready metadata for the public child task.  They
record infrastructure that can be checked locally while explicitly separating
it from the terminal genus `>= 2` rational-point finiteness theorem.
-/
def heightNorthcottDescentAuditTable : List HeightNorthcottDescentAuditRow := [
  {
    component := "Northcott property",
    declarationName := "Northcott",
    sourceLocation := "Mathlib/NumberTheory/Height/Northcott.lean:36",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    partialRole := "Typeclass stating finite bounded-height sublevel sets.",
    separationFromFaltings := "Only a finiteness principle for a chosen height; it does not construct the curve height or prove rational-point finiteness."
  },
  {
    component := "Northcott bounded-height finiteness",
    declarationName := "Northcott.finite_le; AwesomeTheorems.Stage1.S1_M_008.northcott_finite_height_sublevel",
    sourceLocation := "Mathlib/NumberTheory/Height/Northcott.lean:37; local wrapper",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    partialRole := "Checked local wrapper returning finiteness of `{a | h a <= b}` under `[Northcott h]`.",
    separationFromFaltings := "Useful for later bounded-height reductions, but the reduction from curve rational points to such a set remains open."
  },
  {
    component := "Number-field height API",
    declarationName := "NumberField.instAdmissibleAbsValues; NumberField.mulHeight₁_eq; NumberField.logHeight₁_eq; NumberField.totalWeight_eq_finrank",
    sourceLocation := "Mathlib/NumberTheory/Height/NumberField.lean:58; :92; :100; :123",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    partialRole := "Provides the product-formula-facing absolute-value package and scalar height formulas over number fields.",
    separationFromFaltings := "Does not define a canonical height on a Jacobian or a height bound for points on a genus `>= 2` curve."
  },
  {
    component := "Abstract additive descent",
    declarationName := "AddCommGroup.fg_of_descent'; AwesomeTheorems.Stage1.S1_M_008.additive_descent_partial_anchor",
    sourceLocation := "Mathlib/GroupTheory/Descent.lean:140; local wrapper",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    partialRole := "Finite-index doubling plus a Northcott height and approximate parallelogram law imply finite generation.",
    separationFromFaltings := "A Mordell-Weil-style ingredient only; the curve-to-Jacobian map and abelian-variety Faltings theorem are not supplied."
  },
  {
    component := "External Heights project",
    declarationName := "MichaelStollBayreuth/Heights partial height and elliptic-curve anchors",
    sourceLocation := "https://github.com/MichaelStollBayreuth/Heights at revision 688bdb63259556fab4b0f699ce0d10bd2dce23f6",
    repoLocalStatus := "external_upstream_anchor_only_partial_not_terminal",
    partialRole := "Relevant arithmetic-height and elliptic Mordell-Weil infrastructure for later audit.",
    separationFromFaltings := "Not pinned or imported here and not a full Lean 4 Faltings theorem; cannot count as completion."
  }
]

/-- This child records partial infrastructure only, not a terminal Faltings proof. -/
def heightNorthcottDescentSeparatedFromFullFaltings : Bool :=
  true

theorem heightNorthcottDescentSeparatedFromFullFaltings_eq_true :
    heightNorthcottDescentSeparatedFromFullFaltings = true :=
  rfl

/-! ## Audit constants -/

/-- Local module used as the checked statement-shape anchor for this slot. -/
def localAnchorModules : List String := [
  "AwesomeTheorems.Stage1.S1_M_008"
]

/-- mathlib modules audited through the local Faltings/Mordell statement boundary. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Properties",
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.GroupTheory.Descent",
  "Mathlib.NumberTheory.Height.NumberField",
  "Mathlib.NumberTheory.Height.Northcott",
  "Mathlib.NumberTheory.NumberField.Basic"
]

/-- Checked local or mathlib names used by this Stage1 artifact. -/
def checkedAnchorNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_008.theoremId",
  "AwesomeTheorems.Stage1.S1_M_008.canonicalNamespace",
  "AwesomeTheorems.Stage1.S1_M_008.SpecOf",
  "AwesomeTheorems.Stage1.S1_M_008.RationalPointOver",
  "AwesomeTheorems.Stage1.S1_M_008.CurvePredicateSlots",
  "AwesomeTheorems.Stage1.S1_M_008.CurveHypothesesOverNumberField",
  "AwesomeTheorems.Stage1.S1_M_008.StatementShape",
  "AwesomeTheorems.Stage1.S1_M_008.statementShape_eq_normalizedQuantifierConclusion",
  "AwesomeTheorems.Stage1.S1_M_008.FrontierStatus",
  "AwesomeTheorems.Stage1.S1_M_008.FaltingsFrontierNode",
  "AwesomeTheorems.Stage1.S1_M_008.frontierNodeStatus",
  "AwesomeTheorems.Stage1.S1_M_008.partialLeanTargetQueue",
  "AwesomeTheorems.Stage1.S1_M_008.theoremTreeFrontier",
  "AwesomeTheorems.Stage1.S1_M_008.TheoremTreePackage",
  "AwesomeTheorems.Stage1.S1_M_008.BudgetedTheoremTreeLeaf",
  "AwesomeTheorems.Stage1.S1_M_008.theoremTreeLeafBudgetLimit",
  "AwesomeTheorems.Stage1.S1_M_008.budgetedTheoremTreeLeaves",
  "AwesomeTheorems.Stage1.S1_M_008.theoremTreePackageStatus",
  "AwesomeTheorems.Stage1.S1_M_008.curveToJacobianBridge_package_status",
  "AwesomeTheorems.Stage1.S1_M_008.abelianVarietyFaltingsCore_package_status",
  "AwesomeTheorems.Stage1.S1_M_008.specialCasePackages_package_status",
  "AwesomeTheorems.Stage1.S1_M_008.theoremTreeExpansionReadyForPublicBackfill_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.theoremTreeExpansionClosesFaltings_eq_false",
  "AwesomeTheorems.Stage1.S1_M_008.heightNorthcottDescent_status",
  "AwesomeTheorems.Stage1.S1_M_008.northcott_finite_height_sublevel",
  "AwesomeTheorems.Stage1.S1_M_008.additive_descent_partial_anchor",
  "AwesomeTheorems.Stage1.S1_M_008.HeightNorthcottDescentAuditRow",
  "AwesomeTheorems.Stage1.S1_M_008.heightNorthcottDescentAuditTable",
  "AwesomeTheorems.Stage1.S1_M_008.heightNorthcottDescentSeparatedFromFullFaltings_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.ExternalPrimarySourceAuditRow",
  "AwesomeTheorems.Stage1.S1_M_008.externalPrimarySourceAuditTable",
  "AwesomeTheorems.Stage1.S1_M_008.externalPrimarySourceAuditHasRequiredFields_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.externalPrimarySourceAuditFoundTerminalFaltingsProof_eq_false",
  "AwesomeTheorems.Stage1.S1_M_008.ObjectModelAuditRow",
  "AwesomeTheorems.Stage1.S1_M_008.objectModelAuditTable",
  "AwesomeTheorems.Stage1.S1_M_008.objectModelAuditCoversRequiredComponents_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.CompletionEvidence",
  "AwesomeTheorems.Stage1.S1_M_008.noRepoLocalIntegrationDebtForEvidence",
  "AwesomeTheorems.Stage1.S1_M_008.completionCheckboxAllowedForEvidence",
  "AwesomeTheorems.Stage1.S1_M_008.currentCompletionEvidence",
  "AwesomeTheorems.Stage1.S1_M_008.currentCompletionEvidence_not_repoLocalClosed",
  "AwesomeTheorems.Stage1.S1_M_008.currentEvidenceHasNoRepoLocalIntegrationDebt_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.anchorOnlyCompletionCheckboxAllowed_eq_false",
  "AwesomeTheorems.Stage1.S1_M_008.integrationBlockerCompletionCheckboxAllowed_eq_false",
  "AwesomeTheorems.Stage1.S1_M_008.noCompletedStateRetainsRepoLocalIntegrationDebt_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.LocalValidationStatus",
  "AwesomeTheorems.Stage1.S1_M_008.c007LocalValidationStatus",
  "AwesomeTheorems.Stage1.S1_M_008.c007LeanArtifactExists",
  "AwesomeTheorems.Stage1.S1_M_008.c007LocalValidationCommand",
  "AwesomeTheorems.Stage1.S1_M_008.c007PublicStatusAfterValidation",
  "AwesomeTheorems.Stage1.S1_M_008.c007LocalValidationTaskReadyForPublicBackfill",
  "AwesomeTheorems.Stage1.S1_M_008.c007LocalValidationStatus_eq_leanFileExists",
  "AwesomeTheorems.Stage1.S1_M_008.c007LeanArtifactExists_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.c007LocalValidationTaskReadyForPublicBackfill_eq_true",
  "AwesomeTheorems.Stage1.S1_M_008.c007ValidationDoesNotCloseFaltings_eq_false",
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.IsIntegral",
  "AlgebraicGeometry.Smooth",
  "AlgebraicGeometry.IsProper",
  "Northcott",
  "Northcott.exists_min_image",
  "NumberField.instAdmissibleAbsValues",
  "NumberField.mulHeight₁_eq",
  "NumberField.logHeight₁_eq",
  "NumberField.totalWeight_eq_finrank",
  "AddCommGroup.fg_of_descent'",
  "NumberField",
  "Finite"
]

/-- Public search terms used for the external Lean 4 anchor audit. -/
def externalLeanSearchTerms : List String := [
  "Lean 4 Faltings theorem formalization",
  "mathlib Faltings theorem Mordell conjecture Lean",
  "github Lean Faltings theorem Mordell conjecture",
  "Reservoir Lean arithmetic geometry heights Mordell Weil",
  "Reservoir Lean adele ring locally compact number field",
  "GitHub Lean 4 arithmetic geometry Faltings Mordell heights adeles"
]

/-! ## External primary-source audit -/

/--
One external Reservoir/GitHub audit row for arithmetic-geometry Lean 4 projects.

Rows record source metadata only.  A row is not completion evidence unless its
`repoLocalStatus` says the dependency is pinned/imported/checked by this
repository and its theorem is the terminal THM-M-0395 Faltings/Mordell theorem.
-/
structure ExternalPrimarySourceAuditRow where
  projectName : String
  sourceSurface : String
  projectUrl : String
  reservoirUrl : String
  auditedRevision : String
  moduleName : String
  theoremOrDeclarationName : String
  repoLocalStatus : String
  lakePinFeasibility : String
  faltingsRelevance : String
  integrationBlocker : String

/--
External-primary-source audit rows for this Faltings/Mordell slot.

The candidate projects are relevant arithmetic-geometry infrastructure, not a
terminal Faltings proof.  Every non-mathlib row remains anchor-only until a
future serial integrator pins the dependency, imports the named module, and
checks a local wrapper or records a concrete blocker.
-/
def externalPrimarySourceAuditTable : List ExternalPrimarySourceAuditRow := [
  {
    projectName := "leanprover-community/mathlib4",
    sourceSurface := "Reservoir and GitHub dependency already pinned by this repository",
    projectUrl := "https://github.com/leanprover-community/mathlib4",
    reservoirUrl := "https://reservoir.lean-lang.org/@leanprover-community/mathlib",
    auditedRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    moduleName := "Mathlib.NumberTheory.Height.Northcott; Mathlib.GroupTheory.Descent; Mathlib.NumberTheory.Height.NumberField",
    theoremOrDeclarationName := "Northcott.finite_le; AddCommGroup.fg_of_descent'; NumberField.instAdmissibleAbsValues",
    repoLocalStatus := "local_wrapper_upstream_mathlib_partial_not_terminal",
    lakePinFeasibility := "already pinned through this repository's Lake closure and checked by local wrappers in this file",
    faltingsRelevance := "Provides partial height, Northcott, number-field height, and abstract descent infrastructure.",
    integrationBlocker := "No terminal Faltings/Mordell theorem for genus-at-least-two curves is present in the pinned mathlib closure."
  },
  {
    projectName := "MichaelStollBayreuth/Heights",
    sourceSurface := "Reservoir package and GitHub repository",
    projectUrl := "https://github.com/MichaelStollBayreuth/Heights",
    reservoirUrl := "https://reservoir.lean-lang.org/@MichaelStollBayreuth/Heights",
    auditedRevision := "852034cf46fd65b6f76ff9970de6163b82a10091",
    moduleName := "Heights.Rat; Heights.Descent",
    theoremOrDeclarationName := "Projectivization.Rat.finite_of_mulHeight_le; Projectivization.Rat.finite_of_logHeight_le; Rat.finite_of_mulHeight_le; Rat.finite_of_logHeight_le; CommGroup.fg_of_descent",
    repoLocalStatus := "external_upstream_anchor_only_partial_not_terminal",
    lakePinFeasibility := "Lake project exposes `Heights` and depends on mathlib; exact pin appears feasible but must be toolchain/license checked before integration.",
    faltingsRelevance := "Heights and Northcott/descent ingredients are relevant to Mordell-Weil-style infrastructure.",
    integrationBlocker := "No terminal theorem for rational points on smooth proper genus-at-least-two curves is identified; not pinned or imported here."
  },
  {
    projectName := "smmercuri/adele-ring_locally-compact",
    sourceSurface := "GitHub repository with Lean 4 formalization described by primary paper",
    projectUrl := "https://github.com/smmercuri/adele-ring_locally-compact",
    reservoirUrl := "not located as a Reservoir package in this audit",
    auditedRevision := "e8e34608c139ee95a1e21d9d24f138524196a2e1",
    moduleName := "AdeleRingLocallyCompact.NumberTheory.NumberField.AdeleRing",
    theoremOrDeclarationName := "NumberField.AdeleRing.locallyCompactSpace",
    repoLocalStatus := "external_upstream_anchor_only_partial_not_terminal",
    lakePinFeasibility := "GitHub Lean 4 project pin may be possible only after checking its Lake manifest/toolchain against this repository's mathlib revision.",
    faltingsRelevance := "Adeles and local compactness are arithmetic-geometry infrastructure, but they do not provide the Faltings/Mordell finiteness theorem.",
    integrationBlocker := "No curve-to-Jacobian bridge or abelian-variety Faltings core theorem is identified; not pinned or imported here."
  },
  {
    projectName := "ImperialCollegeLondon/FLT",
    sourceSurface := "Reservoir package, GitHub repository, and generated documentation",
    projectUrl := "https://github.com/ImperialCollegeLondon/FLT",
    reservoirUrl := "https://reservoir.lean-lang.org/@ImperialCollegeLondon/FLT",
    auditedRevision := "2f4325e3b3e647225890f143d4f2dbf1315d4ebd",
    moduleName := "Mathlib.NumberTheory.FLT.Basic",
    theoremOrDeclarationName := "FermatLastTheorem; FermatLastTheoremFor; FermatLastTheoremWith",
    repoLocalStatus := "external_upstream_anchor_only_statement_project_not_terminal",
    lakePinFeasibility := "Reservoir reports buildable FLT package revisions; exact pin is feasible only for FLT-related dependencies and does not close THM-M-0395.",
    faltingsRelevance := "Arithmetic-geometry adjacent project with elliptic-curve and modular-form roadmap, but its documented declarations are FLT statement infrastructure.",
    integrationBlocker := "Not a Faltings/Mordell theorem source and no terminal Faltings theorem name is identified."
  }
]

/--
The external audit has the required URL, revision, module, theorem/declaration
name, and Lake-pin feasibility fields in its row type.
-/
def externalPrimarySourceAuditHasRequiredFields : Bool :=
  true

theorem externalPrimarySourceAuditHasRequiredFields_eq_true :
    externalPrimarySourceAuditHasRequiredFields = true :=
  rfl

/--
No audited external project is currently treated as a terminal Lean 4 proof of
Faltings's theorem in the repo-local verification closure.
-/
def externalPrimarySourceAuditFoundTerminalFaltingsProof : Bool :=
  false

theorem externalPrimarySourceAuditFoundTerminalFaltingsProof_eq_false :
    externalPrimarySourceAuditFoundTerminalFaltingsProof = false :=
  rfl

/-- The terminal theorem families still missing from the repo-local Lean closure. -/
def remainingTerminalFamilies : List String := [
  "stable genus API for smooth proper curves over number fields",
  "bridge from checked height/Northcott/descent anchors to curves/Jacobians over number fields",
  "Mordell-Weil and abelian-variety finiteness bridge usable for Faltings",
  "terminal finiteness theorem for rational points on genus-at-least-two curves"
]

/-! ## Mathlib object-model audit -/

/--
One row in the local object-model audit table for the Faltings/Mordell slot.

Rows are intentionally textual metadata so this Stage1 file can record audited
mathlib declarations, local wrappers, and explicit replacement blockers without
pretending that unavailable curve/genus APIs already exist.
-/
structure ObjectModelAuditRow where
  component : String
  declarationName : String
  sourceLocation : String
  repoLocalStatus : String
  faltingsRole : String
  blockerOrReplacement : String

/-- mathlib revision used by this object's Stage1 audit pass. -/
def objectModelAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Public-backfill-ready audit table for the mathlib/local object model needed by
the normalized Faltings/Mordell statement.

`local_wrapper_upstream_mathlib` rows are usable in this repo-local Lean file.
`explicit_predicate_slot` rows are deliberately open and must be replaced by a
checked mathlib API or a pinned external dependency before theorem completion.
-/
def objectModelAuditTable : List ObjectModelAuditRow := [
  {
    component := "NumberField",
    declarationName := "NumberField",
    sourceLocation := "Mathlib/NumberTheory/NumberField/Basic.lean:42",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    faltingsRole := "Base-field class in the quantifier `∀ K [Field K] [NumberField K]`.",
    blockerOrReplacement := "No blocker for the base-field object model."
  },
  {
    component := "Scheme and affine base",
    declarationName := "AlgebraicGeometry.Scheme; AlgebraicGeometry.Spec; AwesomeTheorems.Stage1.S1_M_008.SpecOf",
    sourceLocation := "Mathlib/AlgebraicGeometry/Scheme.lean:42; Mathlib/AlgebraicGeometry/Scheme.lean:511; local wrapper",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    faltingsRole := "Represents the curve object `X` and the base `Spec K` used by the structure morphism.",
    blockerOrReplacement := "No blocker for the raw scheme/base object model."
  },
  {
    component := "Smooth morphism",
    declarationName := "AlgebraicGeometry.Smooth",
    sourceLocation := "Mathlib/AlgebraicGeometry/Morphisms/Smooth.lean:62",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    faltingsRole := "Checked morphism-property field `smooth : Smooth pi` in `CurveHypothesesOverNumberField`.",
    blockerOrReplacement := "No blocker for smoothness as a morphism property; curve-specific packaging remains open."
  },
  {
    component := "Proper morphism",
    declarationName := "AlgebraicGeometry.IsProper",
    sourceLocation := "Mathlib/AlgebraicGeometry/Morphisms/Proper.lean:42",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    faltingsRole := "Checked morphism-property field `proper : IsProper pi` in `CurveHypothesesOverNumberField`.",
    blockerOrReplacement := "No blocker for properness as a morphism property; curve-specific packaging remains open."
  },
  {
    component := "Geometric integrality",
    declarationName := "AlgebraicGeometry.IsIntegral; future geometric-integrality-over-K API",
    sourceLocation := "Mathlib/AlgebraicGeometry/Properties.lean:225; no audited geometric base-change wrapper selected",
    repoLocalStatus := "explicit_predicate_slot",
    faltingsRole := "Records the needed irreducible/reduced geometric curve condition for a stable Faltings curve package.",
    blockerOrReplacement := "Current statement uses explicit geometric/dimension slots; replace or extend them with an audited geometrically integral curve API before completion."
  },
  {
    component := "Genus",
    declarationName := "future genus-of-smooth-proper-curve API",
    sourceLocation := "not located in the pinned mathlib snapshot during this object-model audit",
    repoLocalStatus := "explicit_predicate_slot",
    faltingsRole := "Supports the hypothesis `genus at least two`, currently represented by `slots.genusAtLeastTwo`.",
    blockerOrReplacement := "Select a checked curve genus definition and prove/anchor the comparison to `slots.genusAtLeastTwo` before theorem completion."
  },
  {
    component := "Rational points",
    declarationName := "AwesomeTheorems.Stage1.S1_M_008.RationalPointOver",
    sourceLocation := "local wrapper in AwesomeTheorems/Stage1/S1_M_008.lean",
    repoLocalStatus := "local_proof_body",
    faltingsRole := "Defines a `K`-rational point as a section `Spec K ⟶ X` of the structure morphism.",
    blockerOrReplacement := "No blocker for the normalized section type; terminal finiteness proof remains formalization debt."
  }
]

/-- Audit rows that remain open because the pinned object model is still a predicate slot. -/
def objectModelPredicateSlotRows : List String := [
  "Geometric integrality",
  "Genus"
]

/-- The object-model audit includes the required Faltings components. -/
def objectModelAuditCoversRequiredComponents : Bool :=
  true

theorem objectModelAuditCoversRequiredComponents_eq_true :
    objectModelAuditCoversRequiredComponents = true :=
  rfl

/-- Machine proof debt classification for this open Stage1 slot. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration gate for completed-state promotion.

No completed state is claimed by this file.  If a public Lean 4 terminal proof
is later found, this slot must pin/import/check it or record a concrete
integration blocker before any completed-state promotion.
-/
def repoLocalIntegrationDebtGate : String :=
  "open: no external terminal Lean 4 proof is in the repo-local verification closure"

/-! ## C007 local validation task gate -/

/--
C007 validation status for the repo-local Stage1 artifact.

The status is file/dependency-wrapper validation metadata only.  Even when this
file validates, THM-M-0395 remains open until a terminal local proof body or a
pinned/imported/checked upstream proof enters the repo-local closure.
-/
inductive LocalValidationStatus where
  | noLeanArtifactYet
  | leanFileExists
  | dependencyWrapperExists
  | validationBlocked
  deriving DecidableEq, Repr

/--
The C007 precondition is satisfied in this pass: the owned Lean file exists and
can therefore receive a local validation task.
-/
def c007LocalValidationStatus : LocalValidationStatus :=
  .leanFileExists

/-- Boolean form of the C007 precondition used by the child ledger. -/
def c007LeanArtifactExists : Bool :=
  true

/-- Exact file-level validation command required for this Stage1 artifact. -/
def c007LocalValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_008.lean"

/--
Public status that must remain after C007 validation.

The local validation task checks imports, syntax, and the local wrappers in
this file.  It does not prove Faltings's theorem.
-/
def c007PublicStatusAfterValidation : String :=
  "open / not_repo_local_closed"

/--
C007 is ready for public backfill because a Lean file exists and the validation
command is now concretely identified.
-/
def c007LocalValidationTaskReadyForPublicBackfill : Bool :=
  true

/-- C007 confirms the local validation status selected in this artifact. -/
theorem c007LocalValidationStatus_eq_leanFileExists :
    c007LocalValidationStatus = .leanFileExists :=
  rfl

/-- C007 confirms that the repo-local Lean artifact exists for validation. -/
theorem c007LeanArtifactExists_eq_true :
    c007LeanArtifactExists = true :=
  rfl

/-- C007 confirms that a public local-validation task can now be backfilled. -/
theorem c007LocalValidationTaskReadyForPublicBackfill_eq_true :
    c007LocalValidationTaskReadyForPublicBackfill = true :=
  rfl

/--
C007 validation is not completion evidence for Faltings's theorem.
-/
def c007ValidationClosesFaltings : Bool :=
  false

theorem c007ValidationDoesNotCloseFaltings_eq_false :
    c007ValidationClosesFaltings = false :=
  rfl

/-! ## No-integration-debt completion gate -/

/--
Evidence states relevant to completed-state promotion for this Faltings slot.

`externalAnchorOnly` is the forbidden integration-debt residue: it records a
URL, revision, module, or theorem name without bringing the proof into this
repository's checked Lake closure.  `integrationBlocker` is allowed as an open
non-completion state because it names why pin/import/check could not yet be
performed.
-/
inductive CompletionEvidence where
  | noTerminalLeanProofFound
  | externalAnchorOnly
  | externalPinnedImportedChecked
  | integrationBlocker
  | localProofBody
  deriving DecidableEq, Repr

/--
Whether an evidence state avoids repo-local integration debt.

This is a debt gate, not a theorem-completion gate: an explicit blocker avoids
silent anchor-only debt, but it still does not allow a completed checkbox.
-/
def noRepoLocalIntegrationDebtForEvidence : CompletionEvidence → Bool
  | .externalAnchorOnly => false
  | .noTerminalLeanProofFound => true
  | .externalPinnedImportedChecked => true
  | .integrationBlocker => true
  | .localProofBody => true

/-- Whether an evidence state can support a completed checkbox for THM-M-0395. -/
def completionCheckboxAllowedForEvidence : CompletionEvidence → Bool
  | .externalPinnedImportedChecked => true
  | .localProofBody => true
  | .noTerminalLeanProofFound => false
  | .externalAnchorOnly => false
  | .integrationBlocker => false

/--
Current gate state for this artifact: no terminal external Lean 4 Faltings proof
has been found or brought into the repo-local closure, so the theorem remains
open rather than integration-debt-completed.
-/
def currentCompletionEvidence : CompletionEvidence :=
  .noTerminalLeanProofFound

theorem currentCompletionEvidence_not_repoLocalClosed :
    completionCheckboxAllowedForEvidence currentCompletionEvidence = false :=
  rfl

theorem currentEvidenceHasNoRepoLocalIntegrationDebt_eq_true :
    noRepoLocalIntegrationDebtForEvidence currentCompletionEvidence = true :=
  rfl

/-- Anchor-only external evidence can never support a completed checkbox. -/
theorem anchorOnlyCompletionCheckboxAllowed_eq_false :
    completionCheckboxAllowedForEvidence .externalAnchorOnly = false :=
  rfl

/--
An explicit integration blocker is a valid open gate result, but not completion
evidence.
-/
theorem integrationBlockerCompletionCheckboxAllowed_eq_false :
    completionCheckboxAllowedForEvidence .integrationBlocker = false :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check theoremId
#check canonicalNamespace
#check SpecOf
#check RationalPointOver
#check CurvePredicateSlots
#check CurveHypothesesOverNumberField
#check StatementShape
#check statementShape_eq_normalizedQuantifierConclusion
#check FrontierStatus
#check FaltingsFrontierNode
#check frontierNodeStatus
#check rationalPointSectionType_status
#check terminalRationalPointFiniteness_status
#check heightNorthcottDescent_status
#check predicateSlotFrontierNodes
#check partialLeanTargetQueue
#check theoremTreeFrontier
#check TheoremTreePackage
#check BudgetedTheoremTreeLeaf
#check theoremTreeLeafBudgetLimit
#check budgetedTheoremTreeLeaves
#check theoremTreePackageStatus
#check curveToJacobianBridge_package_status
#check abelianVarietyFaltingsCore_package_status
#check specialCasePackages_package_status
#check theoremTreeExpansionReadyForPublicBackfill
#check theoremTreeExpansionReadyForPublicBackfill_eq_true
#check theoremTreeExpansionClosesFaltings
#check theoremTreeExpansionClosesFaltings_eq_false
#check northcott_finite_height_sublevel
#check additive_descent_partial_anchor
#check HeightNorthcottDescentAuditRow
#check heightNorthcottDescentAuditTable
#check heightNorthcottDescentSeparatedFromFullFaltings
#check heightNorthcottDescentSeparatedFromFullFaltings_eq_true
#check ExternalPrimarySourceAuditRow
#check externalPrimarySourceAuditTable
#check externalPrimarySourceAuditHasRequiredFields
#check externalPrimarySourceAuditHasRequiredFields_eq_true
#check externalPrimarySourceAuditFoundTerminalFaltingsProof
#check externalPrimarySourceAuditFoundTerminalFaltingsProof_eq_false
#check ObjectModelAuditRow
#check objectModelAuditRevision
#check objectModelAuditTable
#check objectModelPredicateSlotRows
#check objectModelAuditCoversRequiredComponents
#check objectModelAuditCoversRequiredComponents_eq_true
#check CompletionEvidence
#check noRepoLocalIntegrationDebtForEvidence
#check completionCheckboxAllowedForEvidence
#check currentCompletionEvidence
#check currentCompletionEvidence_not_repoLocalClosed
#check currentEvidenceHasNoRepoLocalIntegrationDebt_eq_true
#check anchorOnlyCompletionCheckboxAllowed_eq_false
#check integrationBlockerCompletionCheckboxAllowed_eq_false
#check terminalExternalLeanProofInRepoLocalClosure
#check theoremCompletionClaimed
#check noCompletedStateRetainsRepoLocalIntegrationDebt
#check noCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check LocalValidationStatus
#check c007LocalValidationStatus
#check c007LeanArtifactExists
#check c007LocalValidationCommand
#check c007PublicStatusAfterValidation
#check c007LocalValidationTaskReadyForPublicBackfill
#check c007LocalValidationStatus_eq_leanFileExists
#check c007LeanArtifactExists_eq_true
#check c007LocalValidationTaskReadyForPublicBackfill_eq_true
#check c007ValidationClosesFaltings
#check c007ValidationDoesNotCloseFaltings_eq_false
#check RationalPointOver.comp_structureMap
#check CurveHypothesesOverNumberField.smooth'
#check CurveHypothesesOverNumberField.proper'
#check AlgebraicGeometry.IsIntegral
#check Northcott
#check Northcott.exists_min_image
#check NumberField.instAdmissibleAbsValues
#check NumberField.mulHeight₁_eq
#check NumberField.logHeight₁_eq
#check NumberField.totalWeight_eq_finrank
#check AddCommGroup.fg_of_descent'

end AwesomeTheorems.Stage1.S1_M_008
