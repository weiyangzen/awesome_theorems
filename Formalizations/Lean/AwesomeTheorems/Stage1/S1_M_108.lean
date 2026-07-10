import Mathlib.Algebra.Homology.EulerCharacteristic
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.Geometry.Manifold.ChartedSpace
import Mathlib.Geometry.Manifold.IsManifold.Basic
import Mathlib.Geometry.Manifold.VectorBundle.Basic
import Mathlib.Geometry.Manifold.VectorBundle.SmoothSection
import Mathlib.Geometry.Manifold.VectorBundle.Tangent
import Mathlib.LinearAlgebra.Matrix.Permutation
import Mathlib.Topology.Homotopy.Basic
import Mathlib.Topology.Homotopy.HomotopyGroup
import Mathlib.Topology.Order.IntermediateValue

/-!
# S1-M-108 / THM-M-0576: Atiyah-Bott fixed point theorem

This Stage1 artifact records a conservative Lean statement-shape boundary for
the Atiyah-Bott fixed point formula for equivariant elliptic operators.

The pinned mathlib snapshot contains useful substrates for fixed points,
finite fixed-point counting, homological Euler characteristics, manifolds, and
vector bundles.  It does not contain a terminal theorem for equivariant elliptic
operators, equivariant index characters, or the local fixed-point contribution
formula.  The declarations below therefore avoid proof placeholders and false
completion claims.
-/

noncomputable section

open scoped BigOperators
open Set

universe uG uM uR uD uF uH uι

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_108

/-- Fixed points of the action of one element on a space. -/
def fixedPointSet {G : Type uG} {M : Type uM} [Monoid G] [MulAction G M]
    (g : G) : Set M :=
  {x | g • x = x}

/-- Membership in the fixed-point set is definitional. -/
theorem mem_fixedPointSet_iff {G : Type uG} {M : Type uM}
    [Monoid G] [MulAction G M] {g : G} {x : M} :
    x ∈ fixedPointSet g ↔ g • x = x :=
  Iff.rfl

/-- The identity element fixes every point. -/
theorem fixedPointSet_one {G : Type uG} {M : Type uM}
    [Monoid G] [MulAction G M] :
    fixedPointSet (1 : G) = (Set.univ : Set M) := by
  ext x
  simp [fixedPointSet]

/--
Minimal manifold object boundary for later replacement by concrete smooth data.

This does not assert compactness, smoothness order, orientation, transversality,
or ellipticity.  It only records that the formal target should use mathlib's
charted-space/manifold object model rather than an ad hoc topological placeholder.
-/
structure ManifoldObjectBoundary (H : Type uH) (M : Type uM)
    [TopologicalSpace H] [TopologicalSpace M] : Type (max uH uM) where
  chartedSpace : ChartedSpace H M
  smoothManifoldCondition : Prop

/--
Abstract data needed to state an Atiyah-Bott fixed-point formula.

The fields isolate the current formalization boundary.  A terminal proof must
replace `Operator`, `IsEquivariantElliptic`, `IndexCharacter`,
`FixedComponent`, and `LocalContribution` with concrete APIs for vector bundles,
elliptic operators, equivariant indices, fixed-point components, normal weights,
and determinant denominators.
-/
structure AtiyahBottFixedPointFormulaData
    (G : Type uG) (M : Type uM) (R : Type uR)
    [Monoid G] [MulAction G M] [TopologicalSpace M] [AddCommMonoid R] :
    Type (max (max (max uG uM) uR) (max (uD + 1) (uF + 1))) where
  Operator : Type uD
  IsEquivariantElliptic : Operator → Prop
  IndexCharacter : Operator → G → R
  FixedComponent : G → Type uF
  fixedComponentFintype : ∀ g : G, Fintype (FixedComponent g)
  fixedComponentPoint : ∀ g : G, FixedComponent g → M
  fixedComponent_is_fixed :
    ∀ (g : G) (c : FixedComponent g), fixedComponentPoint g c ∈ fixedPointSet g
  LocalContribution : Operator → (g : G) → FixedComponent g → R

/-- The local fixed-point contribution sum attached to abstract Atiyah-Bott data. -/
def localFixedPointContributionSum
    {G : Type uG} {M : Type uM} {R : Type uR}
    [Monoid G] [MulAction G M] [TopologicalSpace M] [AddCommMonoid R]
    (A : AtiyahBottFixedPointFormulaData.{uG, uM, uR, uD, uF} G M R)
    (D : A.Operator) (g : G) : R :=
  letI := A.fixedComponentFintype g
  Finset.univ.sum (fun c : A.FixedComponent g => A.LocalContribution D g c)

/--
Formula-level statement for the abstract Atiyah-Bott fixed-point boundary.

For each equivariant elliptic operator `D` and group element `g`, the
equivariant index character value is the sum of local contributions over the
fixed-point components of `g`.
-/
def AtiyahBottFixedPointFormula
    {G : Type uG} {M : Type uM} {R : Type uR}
    [Monoid G] [MulAction G M] [TopologicalSpace M] [AddCommMonoid R]
    (A : AtiyahBottFixedPointFormulaData.{uG, uM, uR, uD, uF} G M R) : Prop :=
  ∀ (D : A.Operator) (g : G),
    A.IsEquivariantElliptic D →
      A.IndexCharacter D g = localFixedPointContributionSum A D g

/--
Stage1 statement-shape candidate for the Atiyah-Bott fixed point theorem.

The topological/group-action hypotheses are concrete mathlib hypotheses.  The
operator, equivariant index, and local contribution infrastructure remains
abstract because no terminal repo-local or pinned mathlib theorem was located.
-/
def StatementShape (G : Type uG) (M : Type uM) (R : Type uR)
    [Monoid G] [MulAction G M] [TopologicalSpace M] [AddCommMonoid R] : Prop :=
  ∃ A : AtiyahBottFixedPointFormulaData.{uG, uM, uR, uD, uF} G M R,
    AtiyahBottFixedPointFormula A

/-! ## Missing formal API split -/

/--
The formal API families still missing before this Stage1 slot can state and
prove a terminal Atiyah-Bott fixed-point formula repo-locally.
-/
inductive AtiyahBottMissingAPIBranch where
  | smoothEquivariantActions
  | equivariantVectorBundles
  | fixedLocusComponents
  | tangentNormalBundleRestrictions
  | ellipticOperatorSymbolClasses
  | equivariantIndexCharacter
  | localDeterminantDenominators
  | localTraceTerms
  | globalEqualityTheorem
  deriving DecidableEq, Repr

/-- Stable public task name for each missing Atiyah-Bott API branch. -/
def AtiyahBottMissingAPIBranch.canonicalTaskName :
    AtiyahBottMissingAPIBranch → String
  | .smoothEquivariantActions => "THM-M-0576.smooth-equivariant-actions"
  | .equivariantVectorBundles => "THM-M-0576.equivariant-vector-bundles"
  | .fixedLocusComponents => "THM-M-0576.fixed-locus-components"
  | .tangentNormalBundleRestrictions =>
      "THM-M-0576.tangent-normal-bundle-restrictions"
  | .ellipticOperatorSymbolClasses =>
      "THM-M-0576.elliptic-operator-symbol-classes"
  | .equivariantIndexCharacter => "THM-M-0576.equivariant-index-character"
  | .localDeterminantDenominators =>
      "THM-M-0576.local-determinant-denominators"
  | .localTraceTerms => "THM-M-0576.local-trace-terms"
  | .globalEqualityTheorem => "THM-M-0576.global-equality-theorem"

/-- One M0387-style repo-local leaf for a missing formal Atiyah-Bott API family. -/
structure AtiyahBottMissingAPILeaf where
  branch : AtiyahBottMissingAPIBranch
  canonicalTaskName : String
  requiredPayload : String
  currentBoundary : String
  currentStatus : String
  debtClass : String
  leafBudgetBound : Nat
  repoLocalClosed : Bool
  derivesFromBranchName : canonicalTaskName = branch.canonicalTaskName

/--
Integration-ready split of `THM-M-0576.missing-api`.

Every leaf is deliberately marked open and `formalization_debt`: this file
records the missing API frontier but does not construct smooth equivariant
elliptic-operator theory, fixed-locus normal bundle denominators, local trace
terms, or the terminal global equality theorem.
-/
def atiyahBottMissingAPILeaves : List AtiyahBottMissingAPILeaf := [
  {
    branch := .smoothEquivariantActions
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.smoothEquivariantActions.canonicalTaskName
    requiredPayload :=
      "formalize smooth group actions on manifolds with action smoothness and compatibility data"
    currentBoundary :=
      "only MulAction and fixedPointSet are concrete in this file"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .equivariantVectorBundles
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.equivariantVectorBundles.canonicalTaskName
    requiredPayload :=
      "formalize vector bundles over the action manifold with lifted equivariant bundle action"
    currentBoundary :=
      "mathlib vector-bundle modules are imported but no equivariant bundle API is instantiated"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .fixedLocusComponents
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.fixedLocusComponents.canonicalTaskName
    requiredPayload :=
      "define fixed-locus components as geometric objects with finiteness and inclusion into fixedPointSet"
    currentBoundary :=
      "AtiyahBottFixedPointFormulaData has only an abstract FixedComponent type and point map"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .tangentNormalBundleRestrictions
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.tangentNormalBundleRestrictions.canonicalTaskName
    requiredPayload :=
      "formalize tangent and normal bundle restrictions along each fixed component"
    currentBoundary :=
      "tangent/vector-bundle substrate is imported but no restriction or normal bundle construction is supplied"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .ellipticOperatorSymbolClasses
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.ellipticOperatorSymbolClasses.canonicalTaskName
    requiredPayload :=
      "define equivariant elliptic differential operators and their symbol classes"
    currentBoundary :=
      "AtiyahBottFixedPointFormulaData has only abstract Operator and IsEquivariantElliptic fields"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .equivariantIndexCharacter
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.equivariantIndexCharacter.canonicalTaskName
    requiredPayload :=
      "construct the equivariant index character from kernel-cokernel or K-theoretic index data"
    currentBoundary :=
      "AtiyahBottFixedPointFormulaData has only an abstract IndexCharacter field"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .localDeterminantDenominators
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.localDeterminantDenominators.canonicalTaskName
    requiredPayload :=
      "define the normal-bundle determinant denominator for each fixed component and group element"
    currentBoundary :=
      "no normal-weight or determinant-denominator API exists repo-locally"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .localTraceTerms
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.localTraceTerms.canonicalTaskName
    requiredPayload :=
      "define local numerator/trace terms and assemble each fixed-component contribution"
    currentBoundary :=
      "AtiyahBottFixedPointFormulaData has only an abstract LocalContribution field"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  },
  {
    branch := .globalEqualityTheorem
    canonicalTaskName :=
      AtiyahBottMissingAPIBranch.globalEqualityTheorem.canonicalTaskName
    requiredPayload :=
      "prove the global equality between the equivariant index character and the sum of local contributions"
    currentBoundary :=
      "AtiyahBottFixedPointFormula is only an abstract proposition over supplied data"
    currentStatus := "unchecked"
    debtClass := "formalization_debt"
    leafBudgetBound := 100
    repoLocalClosed := false
    derivesFromBranchName := rfl
  }
]

/-- The missing-api split has exactly the nine branches requested by Stage1. -/
theorem atiyahBottMissingAPILeaves_branches_eq :
    atiyahBottMissingAPILeaves.map (fun leaf => leaf.branch) = [
      AtiyahBottMissingAPIBranch.smoothEquivariantActions,
      AtiyahBottMissingAPIBranch.equivariantVectorBundles,
      AtiyahBottMissingAPIBranch.fixedLocusComponents,
      AtiyahBottMissingAPIBranch.tangentNormalBundleRestrictions,
      AtiyahBottMissingAPIBranch.ellipticOperatorSymbolClasses,
      AtiyahBottMissingAPIBranch.equivariantIndexCharacter,
      AtiyahBottMissingAPIBranch.localDeterminantDenominators,
      AtiyahBottMissingAPIBranch.localTraceTerms,
      AtiyahBottMissingAPIBranch.globalEqualityTheorem
    ] :=
  rfl

/-- No missing-api leaf is locally closed by this Stage1 scaffold. -/
theorem atiyahBottMissingAPILeaves_repoLocalClosed_eq :
    atiyahBottMissingAPILeaves.map (fun leaf => leaf.repoLocalClosed) =
      [false, false, false, false, false, false, false, false, false] :=
  rfl

/-- Every missing-api leaf is currently an unchecked formalization-debt leaf. -/
theorem atiyahBottMissingAPILeaves_statusDebt_eq :
    atiyahBottMissingAPILeaves.map
      (fun leaf => (leaf.currentStatus, leaf.debtClass)) = [
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt"),
        ("unchecked", "formalization_debt")
      ] :=
  rfl

/-!
## Statement normalization boundary

`StatementNormalizationBoundary` is the public Stage1 normalization target for
this slot.  It is definitionally the current repo-local `StatementShape`, and
it records only the abstract formula boundary available in this repository.
It is not a terminal Atiyah-Bott fixed-point theorem.
-/

/--
Public statement-normalization boundary for THM-M-0576.

This alias is intentionally conservative: it points public documentation at the
repo-local `StatementShape` while preserving the warning that the actual
Atiyah-Bott fixed-point theorem still requires concrete APIs for equivariant
elliptic operators, index characters, fixed-locus components, and local
contribution denominators.
-/
def StatementNormalizationBoundary (G : Type uG) (M : Type uM) (R : Type uR)
    [Monoid G] [MulAction G M] [TopologicalSpace M] [AddCommMonoid R] : Prop :=
  StatementShape.{uG, uM, uR, uD, uF} G M R

/-- The public normalization boundary is exactly the current `StatementShape`. -/
theorem statementNormalizationBoundary_iff_statementShape
    (G : Type uG) (M : Type uM) (R : Type uR)
    [Monoid G] [MulAction G M] [TopologicalSpace M] [AddCommMonoid R] :
    StatementNormalizationBoundary.{uG, uM, uR, uD, uF} G M R ↔
      StatementShape.{uG, uM, uR, uD, uF} G M R :=
  Iff.rfl

/-- The statement shape is exactly existence of abstract data satisfying the formula. -/
theorem statementShape_iff_exists_formula
    (G : Type uG) (M : Type uM) (R : Type uR)
    [Monoid G] [MulAction G M] [TopologicalSpace M] [AddCommMonoid R] :
    StatementShape.{uG, uM, uR, uD, uF} G M R ↔
      ∃ A : AtiyahBottFixedPointFormulaData.{uG, uM, uR, uD, uF} G M R,
        AtiyahBottFixedPointFormula A :=
  Iff.rfl

/--
Checked finite-set special-case anchor: the trace of a permutation matrix is
the number of fixed points of the permutation.

This is only a discrete shadow of a Lefschetz/Atiyah-Bott trace formula; it is
not the equivariant elliptic-operator theorem.
-/
theorem permutation_trace_fixedPoint_count
    {α : Type uι} {R : Type uR} [DecidableEq α] [Fintype α]
    [AddCommMonoidWithOne R] (σ : Equiv.Perm α) :
    Matrix.trace (σ.permMatrix R) = (Function.fixedPoints σ).ncard := by
  exact Matrix.trace_permutation σ

/-- Checked one-dimensional fixed-point theorem for a continuous self-map of a closed interval. -/
theorem interval_mapsTo_fixedPoint
    {α : Type uι} [ConditionallyCompleteLinearOrder α] [TopologicalSpace α]
    [OrderTopology α] [DenselyOrdered α]
    {a b : α} {f : α → α} (hf : ContinuousOn f (Icc a b))
    (hle : a ≤ b) (hmaps : MapsTo f (Icc a b) (Icc a b)) :
    ∃ c ∈ Icc a b, Function.IsFixedPt f c := by
  exact exists_mem_Icc_isFixedPt_of_mapsTo hf hle hmaps

/-- Checked wrapper around mathlib's Euler characteristic for homological complexes. -/
abbrev HomologicalComplexEulerChar
    (R : Type uR) [Ring R] {ι : Type uι} {c : ComplexShape ι}
    [c.EulerCharSigns] (C : HomologicalComplex (ModuleCat R) c) : ℤ :=
  HomologicalComplex.eulerChar C

/-- Checked wrapper around mathlib's homology-side Euler characteristic. -/
abbrev HomologicalComplexHomologyEulerChar
    (R : Type uR) [Ring R] {ι : Type uι} {c : ComplexShape ι}
    [c.EulerCharSigns] (C : HomologicalComplex (ModuleCat R) c)
    [∀ i : ι, C.HasHomology i] : ℤ :=
  HomologicalComplex.homologyEulerChar C

/-! ## Special-case exposure decisions -/

/--
Checked special-family anchors adjacent to the Atiyah-Bott fixed-point theorem.

These are useful public anchors because they exercise fixed-point counting,
fixed-point existence, and Euler-characteristic vocabulary in pinned mathlib.
None closes the equivariant elliptic-operator formula.
-/
inductive AtiyahBottSpecialCaseAnchor where
  | finitePermutationTraceFixedPointCount
  | intervalFixedPointTheorem
  | homologicalEulerCharacteristicWrapper
  deriving DecidableEq, Repr

/-- Repo-local declaration selected for each special-family anchor. -/
def AtiyahBottSpecialCaseAnchor.anchorDeclaration :
    AtiyahBottSpecialCaseAnchor → String
  | .finitePermutationTraceFixedPointCount =>
      "AwesomeTheorems.Stage1.S1_M_108.permutation_trace_fixedPoint_count"
  | .intervalFixedPointTheorem =>
      "AwesomeTheorems.Stage1.S1_M_108.interval_mapsTo_fixedPoint"
  | .homologicalEulerCharacteristicWrapper =>
      "AwesomeTheorems.Stage1.S1_M_108.HomologicalComplexEulerChar; " ++
      "AwesomeTheorems.Stage1.S1_M_108.HomologicalComplexHomologyEulerChar"

/-- One M0387-style exposure decision for a checked adjacent special-family anchor. -/
structure AtiyahBottSpecialCaseExposureDecision where
  anchor : AtiyahBottSpecialCaseAnchor
  anchorDeclaration : String
  publicExposureRecommended : Bool
  exposureStatus : String
  caveat : String
  repoLocalChecked : Bool
  closesTerminalAtiyahBottTheorem : Bool
  terminalDebtClass : String
  leafBudgetBound : Nat

/--
Decision inventory for `THM-M-0576.special-cases`.

All three anchors are worth public exposure as checked adjacent anchors, provided
the public text states that they are not a proof of the Atiyah-Bott fixed-point
formula and do not discharge the missing equivariant elliptic-operator APIs.
-/
def atiyahBottSpecialCaseExposureDecisions :
    List AtiyahBottSpecialCaseExposureDecision := [
  {
    anchor := .finitePermutationTraceFixedPointCount
    anchorDeclaration :=
      AtiyahBottSpecialCaseAnchor.finitePermutationTraceFixedPointCount.anchorDeclaration
    publicExposureRecommended := true
    exposureStatus := "checked_adjacent_anchor_not_terminal"
    caveat :=
      "finite permutation trace equals fixed-point count; discrete trace shadow only"
    repoLocalChecked := true
    closesTerminalAtiyahBottTheorem := false
    terminalDebtClass := "formalization_debt"
    leafBudgetBound := 20
  },
  {
    anchor := .intervalFixedPointTheorem
    anchorDeclaration :=
      AtiyahBottSpecialCaseAnchor.intervalFixedPointTheorem.anchorDeclaration
    publicExposureRecommended := true
    exposureStatus := "checked_adjacent_anchor_not_terminal"
    caveat :=
      "one-dimensional fixed-point existence theorem; not an index formula"
    repoLocalChecked := true
    closesTerminalAtiyahBottTheorem := false
    terminalDebtClass := "formalization_debt"
    leafBudgetBound := 20
  },
  {
    anchor := .homologicalEulerCharacteristicWrapper
    anchorDeclaration :=
      AtiyahBottSpecialCaseAnchor.homologicalEulerCharacteristicWrapper.anchorDeclaration
    publicExposureRecommended := true
    exposureStatus := "checked_adjacent_anchor_not_terminal"
    caveat :=
      "Euler-characteristic vocabulary for complexes and homology; no equivariant local term theorem"
    repoLocalChecked := true
    closesTerminalAtiyahBottTheorem := false
    terminalDebtClass := "formalization_debt"
    leafBudgetBound := 20
  }
]

/-- The special-case decision inventory contains exactly the three requested anchors. -/
theorem atiyahBottSpecialCaseExposureDecisions_anchors_eq :
    atiyahBottSpecialCaseExposureDecisions.map (fun d => d.anchor) = [
      AtiyahBottSpecialCaseAnchor.finitePermutationTraceFixedPointCount,
      AtiyahBottSpecialCaseAnchor.intervalFixedPointTheorem,
      AtiyahBottSpecialCaseAnchor.homologicalEulerCharacteristicWrapper
    ] :=
  rfl

/-- Each checked special-family anchor is recommended for public exposure. -/
theorem atiyahBottSpecialCaseExposureDecisions_publicExposure_eq :
    atiyahBottSpecialCaseExposureDecisions.map
      (fun d => d.publicExposureRecommended) = [true, true, true] :=
  rfl

/-- Each special-family anchor is repo-locally checked but terminally non-closing. -/
theorem atiyahBottSpecialCaseExposureDecisions_checkedNonterminal_eq :
    atiyahBottSpecialCaseExposureDecisions.map
      (fun d => (d.repoLocalChecked, d.closesTerminalAtiyahBottTheorem)) =
        [(true, false), (true, false), (true, false)] :=
  rfl

/-- Every exposed special-case anchor keeps the terminal theorem as formalization debt. -/
theorem atiyahBottSpecialCaseExposureDecisions_statusDebt_eq :
    atiyahBottSpecialCaseExposureDecisions.map
      (fun d => (d.exposureStatus, d.terminalDebtClass)) = [
        ("checked_adjacent_anchor_not_terminal", "formalization_debt"),
        ("checked_adjacent_anchor_not_terminal", "formalization_debt"),
        ("checked_adjacent_anchor_not_terminal", "formalization_debt")
      ] :=
  rfl

/-- Pinned mathlib revision audited for this Stage1 artifact. -/
def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Topology.Order.IntermediateValue",
  "Mathlib.Dynamics.FixedPoints.Basic",
  "Mathlib.LinearAlgebra.Matrix.Permutation",
  "Mathlib.Algebra.Homology.EulerCharacteristic",
  "Mathlib.Topology.Homotopy.Basic",
  "Mathlib.Topology.Homotopy.HomotopyGroup",
  "Mathlib.Geometry.Manifold.ChartedSpace",
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection"
]

/--
Family-level mathlib areas available in the pinned snapshot.

These are audit categories, not imports of every file below each prefix.
-/
def mathlibAnchorModuleFamilies : List String := [
  "Mathlib.Topology.Homotopy.*",
  "Mathlib.Geometry.Manifold.*",
  "Mathlib.Geometry.Manifold.VectorBundle.*"
]

/-- Search terms that did not locate a terminal Atiyah-Bott theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Atiyah",
  "Bott",
  "AtiyahBott",
  "Lefschetz",
  "equivariant index",
  "elliptic operator",
  "fixed point formula",
  "local contribution"
]

/-! ## External Lean 4 audit gate -/

/-- Exact external Lean 4 code-search terms requested for the Stage1 child audit. -/
def externalAuditRequestedSearchTerms : List String := [
  "AtiyahBott",
  "Atiyah-Bott",
  "Atiyah Bott",
  "Lefschetz",
  "fixed point formula",
  "equivariant index",
  "elliptic operator",
  "IndexCharacter",
  "LocalContribution"
]

/--
Machine-readable status for the external Lean 4 audit pass.

This does not certify a completed upstream search: the current local process has
no authenticated GitHub code-search credentials, so any public backfill must keep
the child item open until an authenticated search is rerun or credentials are
provided.
-/
structure ExternalLeanAuditGate where
  authenticatedGitHubCodeSearchRan : Bool
  publicFallbackSearchRan : Bool
  verifiedExternalLean4ClosureFound : Bool
  candidateLakeDependencyFeasible : Bool
  repoLocalIntegrationDebtInCompletedState : Bool
  statusDetail : String

/--
Current external-audit gate for THM-M-0576.

The local pass checked the pinned mathlib source and public fallback search
surfaces, but GitHub authenticated code search was blocked by missing
credentials.  Therefore no external Lean 4 closure is accepted here, no Lake
dependency is proposed, and the terminal theorem remains open.
-/
def atiyahBottExternalLeanAuditGate : ExternalLeanAuditGate where
  authenticatedGitHubCodeSearchRan := false
  publicFallbackSearchRan := true
  verifiedExternalLean4ClosureFound := false
  candidateLakeDependencyFeasible := false
  repoLocalIntegrationDebtInCompletedState := false
  statusDetail :=
    "authenticated GitHub code search blocked: gh is not logged in, GITHUB_TOKEN/GH_TOKEN are unset, and REST code search returns 401; public fallback found no Lean 4 Atiyah-Bott fixed-point closure"

/-- The external audit used exactly the nine child-task search terms. -/
theorem externalAuditRequestedSearchTerms_eq :
    externalAuditRequestedSearchTerms = [
      "AtiyahBott",
      "Atiyah-Bott",
      "Atiyah Bott",
      "Lefschetz",
      "fixed point formula",
      "equivariant index",
      "elliptic operator",
      "IndexCharacter",
      "LocalContribution"
    ] :=
  rfl

/-- The authenticated external code-search gate is still open in this process. -/
theorem atiyahBottExternalLeanAuditGate_authenticationOpen :
    atiyahBottExternalLeanAuditGate.authenticatedGitHubCodeSearchRan = false ∧
      atiyahBottExternalLeanAuditGate.verifiedExternalLean4ClosureFound = false ∧
      atiyahBottExternalLeanAuditGate.repoLocalIntegrationDebtInCompletedState = false := by
  exact ⟨rfl, rfl, rfl⟩

/-! ## Repo-local integration gate -/

/--
Machine-readable integration gate for external Lean 4 closures.

This records the M0387 rule that anchor-only external evidence is not a
completed state.  A future external proof can close this gate only after it is
pinned or vendored, imported by this repository, and checked by a repo-local
Lean validation command, or after a concrete integration blocker is recorded.
-/
structure ExternalLeanIntegrationGate where
  acceptedExternalClosureFound : Bool
  closurePinnedOrVendored : Bool
  closureImportedInRepo : Bool
  repoLocalValidationPassedForClosure : Bool
  anchorOnlyEvidenceMarkedCompleted : Bool
  completedStateHasRepoLocalIntegrationDebt : Bool
  publicCompletionAllowed : Bool
  terminalMachineStatus : String
  terminalDebtClass : String
  integrationBlocker : String

/--
Current integration gate for THM-M-0576.

No external Lean 4 Atiyah-Bott fixed-point closure is accepted from the blocked
authenticated audit, and no external proof has been pinned, imported, or checked
in this repository.  Therefore the public item must remain open rather than
completed from `external_upstream_anchor_only` evidence.
-/
def atiyahBottIntegrationGate : ExternalLeanIntegrationGate where
  acceptedExternalClosureFound := false
  closurePinnedOrVendored := false
  closureImportedInRepo := false
  repoLocalValidationPassedForClosure := false
  anchorOnlyEvidenceMarkedCompleted := false
  completedStateHasRepoLocalIntegrationDebt := false
  publicCompletionAllowed := false
  terminalMachineStatus := "not_repo_local_closed"
  terminalDebtClass := "formalization_debt"
  integrationBlocker :=
    "authenticated external Lean 4 search is still blocked in this process, so no external Atiyah-Bott closure is accepted; rerun the authenticated search before any pin/import/check attempt or public completion claim"

/-- The integration gate rejects anchor-only completion and residual integration debt. -/
theorem atiyahBottIntegrationGate_noAnchorOnlyCompletion :
    atiyahBottIntegrationGate.anchorOnlyEvidenceMarkedCompleted = false ∧
      atiyahBottIntegrationGate.completedStateHasRepoLocalIntegrationDebt = false ∧
      atiyahBottIntegrationGate.publicCompletionAllowed = false := by
  exact ⟨rfl, rfl, rfl⟩

/-- The current terminal machine status is not repo-locally closed. -/
theorem atiyahBottIntegrationGate_status_eq :
    atiyahBottIntegrationGate.terminalMachineStatus = "not_repo_local_closed" ∧
      atiyahBottIntegrationGate.terminalDebtClass = "formalization_debt" := by
  exact ⟨rfl, rfl⟩

/-- No external closure has been pinned, imported, or checked in this repository. -/
theorem atiyahBottIntegrationGate_noExternalClosureChecked :
    atiyahBottIntegrationGate.acceptedExternalClosureFound = false ∧
      atiyahBottIntegrationGate.closurePinnedOrVendored = false ∧
      atiyahBottIntegrationGate.closureImportedInRepo = false ∧
      atiyahBottIntegrationGate.repoLocalValidationPassedForClosure = false := by
  exact ⟨rfl, rfl, rfl, rfl⟩

end S1_M_108
end Stage1
end AwesomeTheorems
