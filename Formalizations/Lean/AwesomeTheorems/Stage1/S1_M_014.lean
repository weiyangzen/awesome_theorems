import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Real.Basic
import Mathlib.FieldTheory.IntermediateField.Adjoin.Basic
import Mathlib.LinearAlgebra.LinearIndependent.Basic
import Mathlib.NumberTheory.DiophantineApproximation.Basic
import Mathlib.NumberTheory.Height.MvPolynomial
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.Height.Projectivization

/-!
# S1-M-014 / THM-M-0401: Schmidt theorem, Stage1 statement shape

This Stage1 artifact records a conservative Lean 4 statement-shape boundary
and source-audit boundary for the simultaneous approximation theorem for
algebraic numbers commonly attributed to Schmidt.  It is not a proof of
Schmidt's theorem.

The Stage0 `1980` label is treated here as a bibliographic pointer to
W. M. Schmidt's Springer Lecture Notes in Mathematics 785 book, not as the
first theorem-publication year.  The canonical simultaneous-approximation
source statement is Schmidt's 1970 Acta Mathematica theorem, reprinted and
contextualized in the 1980 book: if `1, alpha_0, ..., alpha_{n-1}` are
linearly independent over `Q`, then the product of nearest-integer distances
`||q * alpha_i||` is smaller than `q ^ (-1 - epsilon)` for only finitely many
positive integer denominators `q`.

The normalized corollary target below uses the classical real-number
formulation: if
`1, alpha_0, ..., alpha_{n-1}` are linearly independent over `Q` and the
`alpha_i` are algebraic real numbers, then for every positive `epsilon` only
finitely many integer tuples `(q, p_i)` satisfy the too-strong simultaneous
approximation inequalities

`|q * alpha_i - p_i| < |q| ^ (-(1 / n) - epsilon)`.

The current repo-local checked content is limited to the formal statement
boundary and definitional wrappers.  No proof placeholder declaration is used.
-/

noncomputable section

open scoped BigOperators

namespace AwesomeTheorems.Stage1.S1_M_014

/-- Primary bibliographic source identified for the Stage0 `1980` label. -/
def primarySourceForStage0_1980Label : String :=
  "W. M. Schmidt, Diophantine Approximation, Lecture Notes in Mathematics 785, Springer, 1980"

/-- Earlier primary theorem source for the canonical simultaneous-approximation statement. -/
def canonicalTheoremPrimarySource : String :=
  "W. M. Schmidt, Simultaneous approximation to algebraic numbers by rationals, Acta Mathematica 125 (1970), 189-201"

/--
Audit diagnosis for child task `THM-M-0401-C01`.

The `1980` label is source-bibliographic rather than the theorem's first
publication year.  The canonical theorem statement behind the Stage0 phrase
`代数数的联立逼近` is the product form using nearest-integer distances; the
common-denominator coordinatewise statement below is the standard corollary
shape useful for Lean statement normalization.
-/
def stage0_1980LabelDiagnosis : String :=
  "1980 = Schmidt LNM 785 book pointer; canonical theorem source = Acta Mathematica 125 (1970), product form"

/-- The algebraicity hypothesis for the vector of real numbers. -/
def AlgebraicVector (n : Nat) (alpha : Fin n -> Real) : Prop :=
  forall i : Fin n, IsAlgebraic Rat (alpha i)

/--
The linear-independence hypothesis `1, alpha_0, ..., alpha_{n-1}` over `Q`.

The `Option (Fin n)` index avoids committing to a particular `Fin (n + 1)`
encoding during this statement-normalization pass: `none` names the constant
`1`, and `some i` names `alpha_i`.
-/
def RationalIndependenceWithOne (n : Nat) (alpha : Fin n -> Real) : Prop :=
  LinearIndependent Rat (fun j : Option (Fin n) =>
    match j with
    | none => (1 : Real)
    | some i => alpha i)

/--
`d` is the distance from a real number `x` to the nearest integer.

This packages the classical notation `||x||` without introducing a new
computable nearest-integer function during the Stage1 source-audit pass.
-/
def NearestIntegerDistance (x d : Real) : Prop :=
  0 <= d ∧
    ∃ m : Int,
      d = abs (x - (m : Real)) ∧
        ∀ z : Int, d <= abs (x - (z : Real))

/--
Canonical product-form inequality from Schmidt's simultaneous-approximation
theorem: the product of nearest-integer distances to `q * alpha_i` is too small.
-/
def CanonicalProductTooGood
    (n : Nat) (alpha : Fin n -> Real) (epsilon : Real) (q : Nat) : Prop :=
  0 < q ∧
    ∃ d : Fin n -> Real,
      (∀ i : Fin n, NearestIntegerDistance ((q : Real) * alpha i) (d i)) ∧
        (∏ i : Fin n, d i) < Real.rpow (q : Real) (-1 - epsilon)

/--
Canonical finite-denominator conclusion for Schmidt's product-form theorem.
-/
def CanonicalProductConclusion
    (n : Nat) (alpha : Fin n -> Real) : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    Set.Finite
      {q : Nat | CanonicalProductTooGood n alpha epsilon q}

/--
Canonical Stage1 source statement shape for the theorem identified in
`THM-M-0401-C01`.

This is still a proposition only.  It records the mathematical statement
boundary identified by source audit; it is not a repo-local proof of Schmidt's
theorem.
-/
def CanonicalProductStatementShape : Prop :=
  forall (n : Nat), 0 < n ->
    forall alpha : Fin n -> Real,
      AlgebraicVector n alpha ->
      RationalIndependenceWithOne n alpha ->
      CanonicalProductConclusion n alpha

/-- Definitional expansion of the canonical product-form statement shape. -/
theorem canonicalProductStatementShape_iff :
    CanonicalProductStatementShape <->
      forall (n : Nat), 0 < n ->
        forall alpha : Fin n -> Real,
          AlgebraicVector n alpha ->
          RationalIndependenceWithOne n alpha ->
          CanonicalProductConclusion n alpha := by
  rfl

/--
The simultaneous approximation inequality package for a single denominator
`q` and integer numerator vector `p`.
-/
def TooGoodApproximation
    (n : Nat) (alpha : Fin n -> Real) (epsilon : Real)
    (q : Int) (p : Fin n -> Int) : Prop :=
  And (Not (q = 0)) (forall i : Fin n,
      abs ((q : Real) * alpha i - (p i : Real)) <
        Real.rpow (abs (q : Real)) (-(1 / (n : Real)) - epsilon))

/--
Schmidt-style finiteness conclusion for one fixed algebraic vector.

The set is finite in the type of all integer denominator/numerator tuples.
-/
def SimultaneousApproximationConclusion
    (n : Nat) (alpha : Fin n -> Real) : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    Set.Finite
      {x : Int × (Fin n -> Int) |
        TooGoodApproximation n alpha epsilon x.1 x.2}

/--
Normalized Stage1 statement shape for THM-M-0401.

This is intentionally a proposition, not a claimed theorem proof.  A later
integrator can replace it with a wrapper around a pinned external Lean 4 proof,
or refine it toward the full Schmidt subspace theorem over number fields.
-/
def StatementShape : Prop :=
  forall (n : Nat), 0 < n ->
    forall alpha : Fin n -> Real,
      AlgebraicVector n alpha ->
      RationalIndependenceWithOne n alpha ->
      SimultaneousApproximationConclusion n alpha

/-! ## Public statement-target decision for `THM-M-0401-C02` -/

/--
Candidate A from the parent ledger: the simultaneous Roth-Schmidt corollary for
algebraic real vectors.

This is the selected public Lean statement target for this Stage1 slot.  The
name is an alias for `StatementShape` so later public docs can use the
mathematically explicit candidate name without creating a second canonical
proposition.
-/
def SimultaneousRothSchmidtStatementShape : Prop :=
  StatementShape

/--
Minimal object-model skeleton for the Subspace Theorem conclusion shape.

The fields intentionally describe only the statement boundary needed by this
child: a too-good approximation locus is contained in finitely many proper
subspaces.  Number fields, places, normalized local heights, and concrete
linear forms remain separate object-model audit work for `THM-M-0401-C03`.
-/
structure SchmidtSubspaceModel where
  Point : Type
  Subspace : Type
  isProper : Subspace -> Prop
  contains : Subspace -> Point -> Prop
  tooGood : Point -> Prop

/--
Candidate B from the parent ledger: a Subspace-Theorem-shaped finite
exceptional-subspace statement.

This is recorded as the upstream theorem input for a future reduction, not as
the selected public theorem target for this Stage1 slot.
-/
def SchmidtSubspaceStatementShape : Prop :=
  forall M : SchmidtSubspaceModel,
    ∃ exceptional : Set M.Subspace,
      Set.Finite exceptional ∧
        (∀ W : M.Subspace, W ∈ exceptional -> M.isProper W) ∧
          ∀ x : M.Point, M.tooGood x ->
            ∃ W : M.Subspace, W ∈ exceptional ∧ M.contains W x

/- The public target chosen by `THM-M-0401-C02`. -/
inductive PublicStatementTarget where
  | simultaneousRothSchmidt
  | schmidtSubspace
  | theoremReductionPair
deriving DecidableEq, Repr

/--
The C02 decision: publish the simultaneous Roth-Schmidt corollary as the
canonical Stage1 statement target, and keep the Subspace Theorem shape as the
future upstream reduction input.
-/
def chosenPublicStatementTarget : PublicStatementTarget :=
  PublicStatementTarget.simultaneousRothSchmidt

/-- Checked equality for the C02 public target decision. -/
theorem chosenPublicStatementTarget_eq_simultaneousRothSchmidt :
    chosenPublicStatementTarget =
      PublicStatementTarget.simultaneousRothSchmidt := by
  rfl

/--
The reduction edge that must eventually be proved or imported if the Subspace
Theorem route is used to close the simultaneous Roth-Schmidt target.
-/
def SchmidtSubspaceToSimultaneousReductionShape : Prop :=
  SchmidtSubspaceStatementShape -> SimultaneousRothSchmidtStatementShape

/-- Definitional expansion of the selected C02 target. -/
theorem simultaneousRothSchmidtStatementShape_iff_statementShape :
    SimultaneousRothSchmidtStatementShape <-> StatementShape := by
  rfl

/--
C02 diagnosis for public backfill: Candidate A is the public theorem target;
Candidate B is retained as the theorem/reduction input, not conflated with the
selected statement.
-/
def statementTargetDecisionDiagnosis : String :=
  "C02 selects SimultaneousRothSchmidtStatementShape as the public target and records SchmidtSubspaceStatementShape as the future upstream theorem input via SchmidtSubspaceToSimultaneousReductionShape"

/-- Definitional expansion of the normalized statement shape. -/
theorem statementShape_iff :
    StatementShape <->
      forall (n : Nat), 0 < n ->
        forall alpha : Fin n -> Real,
          AlgebraicVector n alpha ->
          RationalIndependenceWithOne n alpha ->
          SimultaneousApproximationConclusion n alpha := by
  rfl

/--
Projection wrapper for future proof integration: a supplied proof of the
canonical product-form statement gives the finite-denominator conclusion for
one algebraic vector.
-/
theorem canonicalProductConclusion_of_statementShape
    (h : CanonicalProductStatementShape)
    (n : Nat) (hn : 0 < n) (alpha : Fin n -> Real)
    (halg : AlgebraicVector n alpha)
    (hind : RationalIndependenceWithOne n alpha) :
    CanonicalProductConclusion n alpha :=
  h n hn alpha halg hind

/--
Projection wrapper for future proof integration: a supplied proof of the
coordinatewise statement shape gives the finite tuple conclusion for one
algebraic vector.
-/
theorem simultaneousApproximationConclusion_of_statementShape
    (h : StatementShape)
    (n : Nat) (hn : 0 < n) (alpha : Fin n -> Real)
    (halg : AlgebraicVector n alpha)
    (hind : RationalIndependenceWithOne n alpha) :
    SimultaneousApproximationConclusion n alpha :=
  h n hn alpha halg hind

/-! ## Statement/audit/proof-package split -/

/-- Work surfaces for the Stage1 split requested by `S1-M-014-E001`. -/
inductive WorkSurface where
  | statement
  | sourceAudit
  | mathlibObjectModelAudit
  | machineAnchorAudit
  | proofPackage
  | integrationGate
deriving DecidableEq, Repr

/-- Machine-state labels allowed by the M0387-level completion gate. -/
inductive MachineState where
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  | notRepoLocalClosed
deriving DecidableEq, Repr

/-- Machine-proof debt labels used by the Stage1 audit. -/
inductive MachineProofDebt where
  | mathematicalDebt
  | formalizationDebt
  | repoLocalIntegrationDebt
deriving DecidableEq, Repr

/-- A checked audit row for the statement/audit/proof-package split. -/
structure AuditRow where
  surface : WorkSurface
  label : String
  status : String
  debt : MachineProofDebt
  machineState : MachineState
deriving Repr

/-- A checked proof-package row for future M0387-level theorem-tree decomposition. -/
structure ProofPackage where
  id : String
  surface : WorkSurface
  obligation : String
  leafBudget : String
  status : String
deriving Repr

/-! ## Mathlib object-model audit for `THM-M-0401-C03` -/

/-- Required C03 object-model components for a future Schmidt/Subspace route. -/
inductive SchmidtObjectModelComponent where
  | numberFields
  | absoluteValuesAndPlaces
  | heights
  | linearForms
  | exceptionalSubspaces
deriving DecidableEq, Repr

/--
One row in the checked C03 mathlib object-model audit table.

Rows are documentation metadata retained in Lean so the public blueprint can be
backfilled serially from checked declarations.  A row naming an upstream
mathlib object is not a proof of Schmidt's theorem.
-/
structure MathlibObjectModelAuditRow where
  component : SchmidtObjectModelComponent
  publicLabel : String
  mathlibModules : List String
  declarations : List String
  repoLocalStatus : String
  schmidtRole : String
  blockerOrNextGate : String
deriving Repr

/-- mathlib revision used by this C03 object-model audit pass. -/
def schmidtObjectModelAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Public-backfill-ready C03 object-model audit table.

The table covers number fields, places, heights, linear forms, and exceptional
subspaces.  It records object-model availability only; the local-height
normalization, determinant/nondegeneracy bridge, and exceptional-subspace proof
packages remain open.
-/
def schmidtObjectModelAuditTable : List MathlibObjectModelAuditRow := [
  {
    component := SchmidtObjectModelComponent.numberFields
    publicLabel := "Number fields"
    mathlibModules := [
      "Mathlib.NumberTheory.NumberField.Basic",
      "Mathlib.NumberTheory.Height.NumberField"
    ]
    declarations := [
      "NumberField",
      "NumberField.instAdmissibleAbsValues",
      "NumberField.RingOfIntegers"
    ]
    repoLocalStatus := "local_wrapper_upstream_mathlib"
    schmidtRole := "Base-field object `K` for a number-field Subspace-Theorem statement and for the normalized absolute-value height package."
    blockerOrNextGate := "No blocker for the base-field class; a future theorem still has to choose the exact Schmidt statement over `K`."
  },
  {
    component := SchmidtObjectModelComponent.absoluteValuesAndPlaces
    publicLabel := "Absolute values and finite/infinite places"
    mathlibModules := [
      "Mathlib.Algebra.Order.AbsoluteValue.Basic",
      "Mathlib.NumberTheory.NumberField.Completion.FinitePlace",
      "Mathlib.NumberTheory.NumberField.InfinitePlace.Basic",
      "Mathlib.NumberTheory.NumberField.ProductFormula"
    ]
    declarations := [
      "AbsoluteValue",
      "NumberField.FinitePlace",
      "NumberField.InfinitePlace",
      "NumberField.IsFinitePlace",
      "NumberField.IsInfinitePlace",
      "NumberField.prod_abs_eq_one"
    ]
    repoLocalStatus := "local_wrapper_upstream_mathlib"
    schmidtRole := "Object model for the selected set of places and the normalized local absolute values in the product side of the Subspace Theorem."
    blockerOrNextGate := "Select the finite set `S` and prove the bridge from selected local factors to mathlib's all-place product-formula conventions."
  },
  {
    component := SchmidtObjectModelComponent.heights
    publicLabel := "Multiplicative, logarithmic, and projective heights"
    mathlibModules := [
      "Mathlib.NumberTheory.Height.Basic",
      "Mathlib.NumberTheory.Height.NumberField",
      "Mathlib.NumberTheory.Height.Projectivization",
      "Mathlib.NumberTheory.Height.MvPolynomial"
    ]
    declarations := [
      "Height.AdmissibleAbsValues",
      "Height.mulHeight",
      "Height.logHeight",
      "Projectivization.mulHeight",
      "Height.mulHeight_linearMap_apply_le"
    ]
    repoLocalStatus := "local_wrapper_upstream_mathlib"
    schmidtRole := "Global height substrate for denominator/projective-size terms and for linear-map height estimates used in future reductions."
    blockerOrNextGate := "Local-height normalization and exact exponent comparison for Schmidt's inequality remain formalization debt."
  },
  {
    component := SchmidtObjectModelComponent.linearForms
    publicLabel := "Linear forms and independence"
    mathlibModules := [
      "Mathlib.LinearAlgebra.LinearIndependent.Basic",
      "Mathlib.NumberTheory.Height.MvPolynomial"
    ]
    declarations := [
      "LinearMap",
      "LinearIndependent",
      "Height.mulHeight_linearMap_apply_le"
    ]
    repoLocalStatus := "local_wrapper_upstream_mathlib"
    schmidtRole := "Represents each family of `n` independent linear forms as maps `(Fin n -> K) ->L[K] K`, with mathlib support for linear-map height estimates."
    blockerOrNextGate := "The determinant/nondegeneracy package for each place and the product of local linear-form values are not proved here."
  },
  {
    component := SchmidtObjectModelComponent.exceptionalSubspaces
    publicLabel := "Finite exceptional proper subspaces"
    mathlibModules := [
      "Mathlib.LinearAlgebra.LinearIndependent.Basic",
      "Mathlib.Data.Set.Finite.Basic"
    ]
    declarations := [
      "Submodule",
      "Set.Finite",
      "SchmidtSubspaceModel",
      "SchmidtSubspaceStatementShape"
    ]
    repoLocalStatus := "local_object_model_skeleton_plus_mathlib"
    schmidtRole := "Conclusion surface: the too-good approximation locus is contained in finitely many proper `K`-subspaces."
    blockerOrNextGate := "The finite exceptional-subspace theorem is not available repo-locally; C04/C05 must find and integrate an external proof or keep the core as formalization debt."
  }
]

/-- The C03 audit table has exactly the five requested object-model rows. -/
theorem schmidtObjectModelAuditTable_length :
    schmidtObjectModelAuditTable.length = 5 :=
  rfl

/-- The C03 audit table covers the requested components in blueprint order. -/
theorem schmidtObjectModelAuditTable_components :
    schmidtObjectModelAuditTable.map MathlibObjectModelAuditRow.component =
      [ SchmidtObjectModelComponent.numberFields
      , SchmidtObjectModelComponent.absoluteValuesAndPlaces
      , SchmidtObjectModelComponent.heights
      , SchmidtObjectModelComponent.linearForms
      , SchmidtObjectModelComponent.exceptionalSubspaces
      ] :=
  rfl

/-- The C03 object-model audit covers all required public rows. -/
def schmidtObjectModelAuditCoversC03Components : Bool :=
  true

theorem schmidtObjectModelAuditCoversC03Components_eq_true :
    schmidtObjectModelAuditCoversC03Components = true :=
  rfl

/--
Open bridges left after C03.

These are proof-package blockers, not object-model blockers, and they prevent
any theorem-completion claim for THM-M-0401.
-/
def schmidtObjectModelOpenBridgeRows : List String := [
  "local-height normalization over a selected finite set of places",
  "linear-form determinant/nondegeneracy and product-inequality bridge",
  "finite exceptional proper-subspace theorem or pinned external proof"
]

/--
Current audit rows for THM-M-0401.

These rows are local data for the Stage1 ledger.  They are not a proof of
Schmidt's theorem and they do not certify a completed theorem state.
-/
def statementAuditRows : List AuditRow := [
  {
    surface := WorkSurface.statement
    label := "canonical product-form statement"
    status := "checked Prop scaffold: CanonicalProductStatementShape and canonicalProductStatementShape_iff"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.statement
    label := "coordinatewise simultaneous-approximation corollary shape"
    status := "checked Prop scaffold: StatementShape and statementShape_iff"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.statement
    label := "C02 public statement-target decision"
    status := "selected SimultaneousRothSchmidtStatementShape as public target; retained SchmidtSubspaceStatementShape as future theorem/reduction input"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.mathlibObjectModelAudit
    label := "C03 mathlib object-model audit"
    status := "checked audit table covers number fields, places, heights, linear forms, and exceptional subspaces without claiming a Schmidt theorem proof"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.sourceAudit
    label := "Schmidt source boundary"
    status := "Stage0 1980 label treated as LNM 785 pointer; canonical theorem source recorded as Acta Mathematica 125 (1970)"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.machineAnchorAudit
    label := "local mathlib/external Lean terminal proof search"
    status := "no repo-local pinned/imported/checked Lean 4 proof of this Schmidt theorem is present in this artifact"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.integrationGate
    label := "repo-local integration-debt gate"
    status := "completion not claimed; any future external proof must be pinned/imported/checked or blocked explicitly"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/-- First proof-package split for Schmidt's simultaneous-approximation theorem. -/
def proofPackageSplit : List ProofPackage := [
  {
    id := "M0401.Pkg01.SourceAndStatementNormalization"
    surface := WorkSurface.statement
    obligation := "freeze the product-form theorem, the coordinatewise common-denominator corollary, and the C02 public target decision without conflating the 1970 theorem source with the 1980 book pointer"
    leafBudget := "<=100 per eventual proof leaf"
    status := "partially represented by CanonicalProductStatementShape, StatementShape, SimultaneousRothSchmidtStatementShape, chosenPublicStatementTarget, and projection wrappers"
  },
  {
    id := "M0401.Pkg02.AlgebraicInputAndIndependence"
    surface := WorkSurface.mathlibObjectModelAudit
    obligation := "formalize the algebraic real vector input and audit the mathlib object model for number fields, places, heights, linear forms, and exceptional subspaces"
    leafBudget := "<=100 per eventual proof leaf"
    status := "object-model scaffold checked via AlgebraicVector, RationalIndependenceWithOne, and schmidtObjectModelAuditTable; theorem proof unchecked"
  },
  {
    id := "M0401.Pkg03.NearestIntegerDistanceAndProductInequality"
    surface := WorkSurface.proofPackage
    obligation := "connect nearest-integer distance, product of distances, positive denominator q, and Real.rpow exponent conventions"
    leafBudget := "<=100 per eventual proof leaf"
    status := "predicate scaffold checked via NearestIntegerDistance and CanonicalProductTooGood; proof unchecked"
  },
  {
    id := "M0401.Pkg04.ProductToCoordinatewiseCorollary"
    surface := WorkSurface.proofPackage
    obligation := "derive the coordinatewise |q * alpha_i - p_i| bound from the product-form theorem with the correct epsilon rescaling and denominator normalization"
    leafBudget := "<=100 per eventual proof leaf"
    status := "corollary statement scaffold checked via TooGoodApproximation; bridge proof unchecked"
  },
  {
    id := "M0401.Pkg05.FiniteExceptionExtraction"
    surface := WorkSurface.proofPackage
    obligation := "turn the too-good approximation predicate into Set.Finite denominator or tuple exception sets"
    leafBudget := "<=100 per eventual proof leaf"
    status := "finite-set conclusion surfaces checked; full proof unchecked"
  },
  {
    id := "M0401.Pkg06.LeanAnchorOrIntegrationGate"
    surface := WorkSurface.integrationGate
    obligation := "pin/import/check a future external Lean 4 proof, create a local wrapper, or record a concrete blocker before any completion claim"
    leafBudget := "<=100 per eventual proof leaf"
    status := "open gate; no completed state claimed"
  },
  {
    id := "M0401.Pkg07.SubspaceTheoremReductionInput"
    surface := WorkSurface.proofPackage
    obligation := "treat SchmidtSubspaceStatementShape as an upstream theorem input and later prove or import SchmidtSubspaceToSimultaneousReductionShape before using the subspace route"
    leafBudget := "<=100 per eventual proof leaf"
    status := "statement/reduction shape recorded; reduction proof unchecked"
  }
]

/-- Local audit classification for the machine-proof state of this Stage1 artifact. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/-- Current machine state for the root theorem slot. -/
def currentMachineState : MachineState :=
  MachineState.notRepoLocalClosed

/-- Current proof-debt class for the root theorem slot. -/
def currentMachineProofDebt : MachineProofDebt :=
  MachineProofDebt.formalizationDebt

/-- Closed states that would count for repo-local completion. -/
def countsAsRepoLocalCompleted : MachineState -> Prop
  | MachineState.localProofBody => True
  | MachineState.localWrapperUpstreamMathlib => True
  | MachineState.externalUpstreamPinned => True
  | MachineState.externalUpstreamAnchorOnly => False
  | MachineState.notRepoLocalClosed => False

/-- Checked gate: the present machine state is not a repo-local completion state. -/
theorem currentMachineState_not_completed :
    ¬ countsAsRepoLocalCompleted currentMachineState := by
  intro h
  exact h

/--
Repo-local integration-debt gate.

No external Lean 4 proof of this Schmidt theorem has been pinned, imported, and
checked in this repository by this artifact.
-/
def repoLocalIntegrationDebtGate : String :=
  "not completed; no repo-local wrapper around a pinned external proof"

/-- Checked declaration names used as local anchors for this statement boundary. -/
def checkedAnchorNames : List String :=
  [ "IsAlgebraic"
  , "LinearIndependent"
  , "Real.rpow"
  , "Set.Finite"
  , "Finset.prod"
  , "Real.exists_rat_abs_sub_le_and_den_le"
  , "Real.exists_nat_abs_mul_sub_round_le"
  , "Real.exists_rat_eq_convergent"
  , "c09LocalValidationCommand"
  , "c09LocalValidationDate"
  , "c09LocalFileCheckStatus"
  , "SimultaneousRothSchmidtStatementShape"
  , "SchmidtSubspaceStatementShape"
  , "SchmidtSubspaceToSimultaneousReductionShape"
  , "schmidtObjectModelAuditTable"
  , "NumberField"
  , "NumberField.FinitePlace"
  , "NumberField.InfinitePlace"
  , "Height.mulHeight"
  , "Projectivization.mulHeight"
  ]

/-- Local modules searched or used while checking this Stage1 artifact. -/
def checkedOrSearchedModules : List String :=
  [ "Mathlib.Analysis.SpecialFunctions.Pow.Real"
  , "Mathlib.Data.Real.Basic"
  , "Mathlib.FieldTheory.IntermediateField.Adjoin.Basic"
  , "Mathlib.LinearAlgebra.LinearIndependent.Basic"
  , "Mathlib.NumberTheory.Height.MvPolynomial"
  , "Mathlib.NumberTheory.Height.NumberField"
  , "Mathlib.NumberTheory.Height.Projectivization"
  , "Mathlib.NumberTheory.DiophantineApproximation.Basic"
  ]

/-- Search terms that did not locate a terminal repo-local Lean theorem here. -/
def absentTerminalSearchTerms : List String :=
  [ "Schmidt"
  , "SubspaceTheorem"
  , "Subspace theorem"
  , "DiophantineApproximation"
  , "simultaneous approximation"
  ]

/-! ## External Lean 4 project-search audit for `THM-M-0401-C04` -/

/--
One row in the C04 Lean-project search ledger.

Rows record exact repository/module/theorem evidence when available.  A row
with no terminal theorem names is negative or blocked audit evidence, not a
completion certificate.
-/
structure ExternalLeanProjectSearchRow where
  searchSurface : String
  repositoryUrl : String
  commit : String
  modules : List String
  theoremNames : List String
  lakeCompatibility : String
  result : String
  integrationStatus : String
deriving Repr

/--
C04 external Lean 4 project-search rows.

As of 2026-05-01, this worker could check the repository-local pinned mathlib
source tree and the repository configuration.  Authenticated GitHub code search
could not be completed in this environment because `gh auth status` reported no
logged-in GitHub host and the unauthenticated GitHub API was rate-limited.
-/
def externalLeanProjectSearchRows : List ExternalLeanProjectSearchRow := [
  {
    searchSurface := "repo-local pinned mathlib grep"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4.git"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    modules := [
      "Mathlib.NumberTheory.DiophantineApproximation.Basic",
      "Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions",
      "Mathlib.NumberTheory.Height.NumberField",
      "Mathlib.NumberTheory.Height.Projectivization"
    ]
    theoremNames := [
      "exists_int_int_abs_mul_sub_le",
      "exists_nat_abs_mul_sub_round_le",
      "exists_rat_abs_sub_le_and_den_le",
      "Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational",
      "Real.exists_rat_eq_convergent",
      "Real.exists_convs_eq_rat"
    ]
    lakeCompatibility := "Lake-compatible in this repository via leanprover/lean4:v4.29.0 and pinned mathlib rev 8a178386ffc0f5fef0b77738bb5449d50efeea95."
    result := "Diophantine approximation substrate found, but no Schmidt/Subspace terminal theorem for THM-M-0401."
    integrationStatus := "local_wrapper_upstream_mathlib for substrate only; not a Schmidt theorem proof."
  },
  {
    searchSurface := "repo-local dependency grep: flt-regular"
    repositoryUrl := "https://github.com/leanprover-community/flt-regular.git"
    commit := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
    modules := []
    theoremNames := []
    lakeCompatibility := "Lake-compatible dependency in this repository, but unrelated to Schmidt theorem."
    result := "No Schmidt/Subspace terminal theorem found in the checked dependency grep."
    integrationStatus := "not applicable for THM-M-0401."
  },
  {
    searchSurface := "GitHub CLI authenticated code search"
    repositoryUrl := "https://github.com/search"
    commit := "blocked"
    modules := []
    theoremNames := []
    lakeCompatibility := "blocked: no candidate repository or Lake file could be authenticated and checked."
    result := "`gh auth status` reported no logged-in GitHub hosts on 2026-05-01."
    integrationStatus := "integration blocker: rerun with authenticated GitHub code search before upgrading C04."
  },
  {
    searchSurface := "GitHub REST code search"
    repositoryUrl := "https://api.github.com/search/code"
    commit := "blocked"
    modules := []
    theoremNames := []
    lakeCompatibility := "blocked: unauthenticated REST request did not provide code-search evidence."
    result := "The GitHub API returned HTTP 403 rate-limit exhaustion for the unauthenticated request on 2026-05-01."
    integrationStatus := "integration blocker: provide a GitHub token or authenticated `gh` session and rerun the code-search queries."
  },
  {
    searchSurface := "grep.app Lean code search"
    repositoryUrl := "https://grep.app"
    commit := "blocked"
    modules := []
    theoremNames := []
    lakeCompatibility := "blocked: service returned a Vercel security-checkpoint page instead of search JSON."
    result := "No usable external Lean-project evidence was obtained from grep.app in this worker environment."
    integrationStatus := "not completion evidence; use only as a search-surface blocker."
  }
]

/-- C04 audit rows distinguish checked local evidence from blocked external search. -/
theorem externalLeanProjectSearchRows_length :
    externalLeanProjectSearchRows.length = 5 :=
  rfl

/-- Current C04 result: no external terminal proof is integrated in this repository. -/
def externalLeanProjectSearchConclusion : String :=
  "no repo-local pinned/imported/checked Lean 4 proof of Schmidt's theorem; authenticated external code search remains blocked by missing GitHub auth"

/-! ## C05 core proof integration gate -/

/--
C05 integration status for the Schmidt core.

This is a checked status tag only.  It does not assert that the external
search is globally exhaustive; it records what this repo can currently validate
without leaving anchor-only evidence as a completion claim.
-/
inductive CoreProofIntegrationStatus where
  | externalProofPinnedChecked
  | externalProofBlocked
  | formalizationDebtNoCompletionClaim
deriving DecidableEq, Repr

/--
Current C05 status: no external Schmidt proof has been pinned, imported, and
checked in this repository, so the core remains formalization debt with no
repo-local completion claim.
-/
def c05CoreProofIntegrationStatus : CoreProofIntegrationStatus :=
  CoreProofIntegrationStatus.formalizationDebtNoCompletionClaim

/-- Checked C05 debt class for the full Schmidt core. -/
def c05CoreMachineProofDebt : MachineProofDebt :=
  MachineProofDebt.formalizationDebt

/-- Checked C05 machine state for the full Schmidt core. -/
def c05CoreMachineState : MachineState :=
  MachineState.notRepoLocalClosed

/--
The C05 gate is closed only as a non-completion gate: no external proof has
entered the repo-local validation closure.
-/
def c05ExternalProofPinnedImportedChecked : Bool :=
  false

/-- C05 keeps the core as formalization debt rather than theorem completion. -/
theorem c05CoreProofIntegrationStatus_eq_formalizationDebt :
    c05CoreProofIntegrationStatus =
      CoreProofIntegrationStatus.formalizationDebtNoCompletionClaim := by
  rfl

/-- C05 records no pinned/imported/checked external proof in this repository. -/
theorem c05ExternalProofPinnedImportedChecked_eq_false :
    c05ExternalProofPinnedImportedChecked = false := by
  rfl

/-- The C05 state is not a repo-local theorem completion state. -/
theorem c05CoreMachineState_not_completed :
    ¬ countsAsRepoLocalCompleted c05CoreMachineState := by
  intro h
  exact h

/--
Public-backfill-ready C05 diagnosis.

If a later authenticated search identifies an external Lean 4 proof, this
diagnosis must be replaced by a pin/import/check result or by a concrete
integration blocker.  Anchor-only evidence is not enough for completion.
-/
def c05CoreProofIntegrationDiagnosis : String :=
  "C05: no external Lean 4 proof of Schmidt's theorem is pinned/imported/checked here; core remains formalization_debt with no repo-local completion claim"

/-! ## C06 statement-shape file validation gate -/

/--
C06 status for the repo-local statement-shape artifact.

This status is about the file/import/syntax gate only.  It is not a proof of
Schmidt's theorem and it is not a repo-local completion state for the root.
-/
inductive StatementShapeFileValidationStatus where
  | importsAndSyntaxChecked
  | notCreated
  | blocked
deriving DecidableEq, Repr

/--
Current C06 status: the repo-local Stage1 statement-shape artifact exists and
has been checked by the requested file-level Lean command.
-/
def c06StatementShapeFileValidationStatus : StatementShapeFileValidationStatus :=
  StatementShapeFileValidationStatus.importsAndSyntaxChecked

/-- C06 boolean gate for import and syntax validation of this file. -/
def c06ImportsAndSyntaxValidated : Bool :=
  true

/-- C06 confirms the statement-shape file validation status. -/
theorem c06StatementShapeFileValidationStatus_eq_checked :
    c06StatementShapeFileValidationStatus =
      StatementShapeFileValidationStatus.importsAndSyntaxChecked := by
  rfl

/-- C06 confirms that imports and syntax have been validated for this artifact. -/
theorem c06ImportsAndSyntaxValidated_eq_true :
    c06ImportsAndSyntaxValidated = true := by
  rfl

/--
Public-backfill-ready C06 diagnosis.

The checked declarations in this file provide statement-shape scaffolding and
audit metadata only; the root theorem remains `formalization_debt` until a
local proof body, mathlib wrapper, or pinned external proof is validated.
-/
def c06StatementShapeFileValidationDiagnosis : String :=
  "C06: repo-local statement-shape file exists and validates by lake env lean; this is statement scaffolding only, not a Schmidt theorem proof or completion claim"

/-! ## C07 high-risk bridge leaf-ledger split -/

/-- High-risk bridge areas split by C07 into independent leaf ledgers. -/
inductive HighRiskBridgeArea where
  | localHeight
  | exceptionalSubspace
  | integrationGate
deriving DecidableEq, Repr

/--
One C07 leaf-ledger row.

The `localStepBudget` is a human proof-audit budget for the future leaf.  A row
is not a proof and cannot be used as a completion certificate for Schmidt's
theorem.
-/
structure BridgeLeafLedger where
  id : String
  area : HighRiskBridgeArea
  objective : String
  localStepBudget : Nat
  independenceBoundary : String
  status : String
deriving Repr

/--
C07 split of the local-height and exceptional-subspace bridge work into
independent `<= 100` leaf ledgers.

These rows are integration-ready proof-planning metadata.  They deliberately
keep the Schmidt core in `formalization_debt` until a local proof body or a
pinned/imported/checked external proof supplies the missing mathematics.
-/
def c07HighRiskBridgeLeafLedgers : List BridgeLeafLedger := [
  {
    id := "M0401.C07.LH01.PlaceNormalizationChoice"
    area := HighRiskBridgeArea.localHeight
    objective := "Fix the selected finite set of places, absolute-value normalization, and notation needed before comparing local factors."
    localStepBudget := 45
    independenceBoundary := "Depends only on the C03 places/absolute-values object model and does not use exceptional subspace extraction."
    status := "open leaf ledger; statement boundary only"
  },
  {
    id := "M0401.C07.LH02.LocalFactorToHeightTerm"
    area := HighRiskBridgeArea.localHeight
    objective := "Relate each selected local linear-form factor to the corresponding global/projective height term under the chosen normalization."
    localStepBudget := 80
    independenceBoundary := "Consumes LH01 conventions and mathlib height APIs; independent of finite exceptional-subspace packaging."
    status := "formalization_debt leaf; proof not present"
  },
  {
    id := "M0401.C07.LH03.SProductVsAllPlaces"
    area := HighRiskBridgeArea.localHeight
    objective := "Bridge the selected-place product used by Schmidt's inequality with mathlib's all-place product-formula conventions."
    localStepBudget := 90
    independenceBoundary := "Consumes LH01 only; can be audited separately from exponent rescaling and exceptional loci."
    status := "formalization_debt leaf; proof not present"
  },
  {
    id := "M0401.C07.LH04.ExponentAndRpowComparison"
    area := HighRiskBridgeArea.localHeight
    objective := "Check the `Real.rpow` exponent conversion between product-form and coordinatewise simultaneous-approximation inequalities."
    localStepBudget := 70
    independenceBoundary := "Uses real/rpow arithmetic and positive-denominator hypotheses; independent of place normalization after inputs are named."
    status := "formalization_debt leaf; proof not present"
  },
  {
    id := "M0401.C07.LH05.ProjectiveHeightDenominatorBridge"
    area := HighRiskBridgeArea.localHeight
    objective := "Connect the common denominator tuple `(q, p_i)` with the projective/global height size term required by the Subspace-Theorem route."
    localStepBudget := 95
    independenceBoundary := "Consumes height APIs and tuple encoding; independent of finite union extraction once the height bound is stated."
    status := "formalization_debt leaf; proof not present"
  },
  {
    id := "M0401.C07.ES01.ProperSubspacePredicate"
    area := HighRiskBridgeArea.exceptionalSubspace
    objective := "Replace the skeletal `SchmidtSubspaceModel.isProper` field by the future `Submodule`-based proper-subspace predicate."
    localStepBudget := 45
    independenceBoundary := "Pure object-model refinement; independent of local-height estimates."
    status := "open leaf ledger; statement boundary only"
  },
  {
    id := "M0401.C07.ES02.FiniteExceptionalFamilyPackaging"
    area := HighRiskBridgeArea.exceptionalSubspace
    objective := "Package the exceptional family as a finite set/list of proper subspaces with membership and containment projections."
    localStepBudget := 60
    independenceBoundary := "Consumes ES01 only; independent of the proof that the too-good locus is contained in the family."
    status := "formalization_debt leaf; proof not present"
  },
  {
    id := "M0401.C07.ES03.TooGoodLocusContainment"
    area := HighRiskBridgeArea.exceptionalSubspace
    objective := "State the bridge from the Subspace-Theorem too-good predicate to containment in one exceptional proper subspace."
    localStepBudget := 85
    independenceBoundary := "Consumes the future theorem input and ES02 packaging; independent of tuple finiteness extraction."
    status := "formalization_debt leaf; proof not present"
  },
  {
    id := "M0401.C07.ES04.TupleExceptionExtraction"
    area := HighRiskBridgeArea.exceptionalSubspace
    objective := "Extract the finite exceptional integer tuples/denominators needed by the simultaneous Roth-Schmidt corollary."
    localStepBudget := 90
    independenceBoundary := "Consumes ES03 containment and the tuple encoding; independent of local-height normalization once the too-good predicate is available."
    status := "formalization_debt leaf; proof not present"
  },
  {
    id := "M0401.C07.GATE01.ExternalProofOrBlocker"
    area := HighRiskBridgeArea.integrationGate
    objective := "Before any completion claim, pin/import/check a terminal external Lean 4 proof or record a concrete integration blocker."
    localStepBudget := 35
    independenceBoundary := "Integration gate only; it does not discharge any mathematical bridge lemma."
    status := "open non-completion gate; no anchor-only completion allowed"
  }
]

/-- C07 split contains ten independent high-risk bridge leaf rows. -/
theorem c07HighRiskBridgeLeafLedgers_length :
    c07HighRiskBridgeLeafLedgers.length = 10 :=
  rfl

/-- C07 local-height split has five independent leaf ledgers. -/
def c07LocalHeightLeafLedgerIds : List String :=
  c07HighRiskBridgeLeafLedgers.filterMap
    (fun row =>
      if row.area = HighRiskBridgeArea.localHeight then some row.id else none)

/-- C07 exceptional-subspace split has four independent leaf ledgers. -/
def c07ExceptionalSubspaceLeafLedgerIds : List String :=
  c07HighRiskBridgeLeafLedgers.filterMap
    (fun row =>
      if row.area = HighRiskBridgeArea.exceptionalSubspace then some row.id else none)

/-- C07 keeps a separate integration gate rather than treating anchors as proof. -/
def c07IntegrationGateLeafLedgerIds : List String :=
  c07HighRiskBridgeLeafLedgers.filterMap
    (fun row =>
      if row.area = HighRiskBridgeArea.integrationGate then some row.id else none)

/-- Checked local-height leaf-ledger IDs for public backfill. -/
theorem c07LocalHeightLeafLedgerIds_eq :
    c07LocalHeightLeafLedgerIds =
      [ "M0401.C07.LH01.PlaceNormalizationChoice"
      , "M0401.C07.LH02.LocalFactorToHeightTerm"
      , "M0401.C07.LH03.SProductVsAllPlaces"
      , "M0401.C07.LH04.ExponentAndRpowComparison"
      , "M0401.C07.LH05.ProjectiveHeightDenominatorBridge"
      ] :=
  rfl

/-- Checked exceptional-subspace leaf-ledger IDs for public backfill. -/
theorem c07ExceptionalSubspaceLeafLedgerIds_eq :
    c07ExceptionalSubspaceLeafLedgerIds =
      [ "M0401.C07.ES01.ProperSubspacePredicate"
      , "M0401.C07.ES02.FiniteExceptionalFamilyPackaging"
      , "M0401.C07.ES03.TooGoodLocusContainment"
      , "M0401.C07.ES04.TupleExceptionExtraction"
      ] :=
  rfl

/-- Checked C07 integration-gate ledger ID for public backfill. -/
theorem c07IntegrationGateLeafLedgerIds_eq :
    c07IntegrationGateLeafLedgerIds =
      [ "M0401.C07.GATE01.ExternalProofOrBlocker" ] :=
  rfl

/-- Literal local budgets attached to the C07 split. -/
def c07HighRiskBridgeLeafBudgets : List Nat :=
  c07HighRiskBridgeLeafLedgers.map BridgeLeafLedger.localStepBudget

/-- C07 records each independent leaf with a local budget at or below 100. -/
theorem c07HighRiskBridgeLeafBudgets_eq :
    c07HighRiskBridgeLeafBudgets =
      [45, 80, 90, 70, 95, 45, 60, 85, 90, 35] :=
  rfl

/-- C07 is a split/audit task, not a theorem-completion claim. -/
def c07HighRiskBridgeLeafSplitDiagnosis : String :=
  "C07: high-risk local-height and exceptional-subspace bridge work is split into independent <=100 leaf ledgers; all leaves remain open formalization_debt and no Schmidt theorem completion is claimed"

/-! ## C08 low-dimensional partial wrapper -/

/--
C08 API components used in the low-dimensional partial wrapper.

These are substrate APIs only.  They do not supply the full Schmidt theorem,
the product-form statement, or the finite-exception conclusion.
-/
inductive LowDimensionalPartialApi where
  | dirichletRationalApproximation
  | dirichletRoundedNumerator
  | legendreConvergentCriterion
  | heightLowerBounds
deriving DecidableEq, Repr

/--
One row in the C08 low-dimensional partial-wrapper audit table.

The row records a checked local wrapper around an existing API and its explicit
non-completion boundary.
-/
structure LowDimensionalPartialWrapperRow where
  id : String
  api : LowDimensionalPartialApi
  wrapperName : String
  mathlibAnchor : String
  dimensionBoundary : String
  schmidtBoundary : String
deriving Repr

/--
One-dimensional Dirichlet rational approximation wrapper.

This is a direct local wrapper around mathlib's Dirichlet approximation API.
It is deliberately labelled partial: it gives existence of one good rational
approximant for a chosen bound `N`, not finiteness of too-good approximants and
not Schmidt's theorem.
-/
theorem c08_dirichletOneDimensional_rationalApproximation
    (xi : Real) {N : Nat} (hN : 0 < N) :
    ∃ q : Rat,
      |xi - (q : Real)| ≤ 1 / (((N : Real) + 1) * (q.den : Real)) ∧
        q.den ≤ N :=
  Real.exists_rat_abs_sub_le_and_den_le xi hN

/--
One-dimensional rounded-numerator Dirichlet wrapper.

This packages the existing integer-denominator/rounded-numerator form.  It is
only a low-dimensional approximation substrate and is not a finite-exception
Schmidt statement.
-/
theorem c08_dirichletOneDimensional_roundedNumerator
    (xi : Real) {N : Nat} (hN : 0 < N) :
    ∃ k : Nat,
      0 < k ∧ k ≤ N ∧
        |(k : Real) * xi - (round ((k : Real) * xi) : Real)| ≤
          1 / ((N : Real) + 1) :=
  Real.exists_nat_abs_mul_sub_round_le xi hN

/--
One-dimensional Legendre wrapper.

This records the classical continued-fraction criterion already present in
mathlib: a sufficiently good rational approximant is a convergent.  This is a
classification of one-dimensional approximants, not the Schmidt theorem.
-/
theorem c08_legendreOneDimensional_convergentCriterion
    {xi : Real} {q : Rat}
    (h : |xi - (q : Real)| < 1 / (2 * (q.den : Real) ^ 2)) :
    ∃ n : Nat, q = xi.convergent n :=
  Real.exists_rat_eq_convergent h

/--
Height lower-bound wrapper for field elements.

This uses the existing height API only as a size-control substrate for future
normalization.  It does not prove any Diophantine-approximation finiteness
statement.
-/
theorem c08_heightElement_mulHeight_ge_one
    {K : Type*} [Field K] [Height.AdmissibleAbsValues K] (x : K) :
    1 ≤ Height.mulHeight₁ x :=
  Height.one_le_mulHeight₁ x

/--
Height lower-bound wrapper for finite tuples.

This is the low-dimensional/projective-size side of the C08 partial wrapper,
kept separate from any local-height or exceptional-subspace bridge claim.
-/
theorem c08_heightTuple_mulHeight_ge_one
    {K ι : Type*} [Field K] [Height.AdmissibleAbsValues K] [Finite ι]
    (x : ι → K) :
    1 ≤ Height.mulHeight x :=
  Height.one_le_mulHeight x

/-- C08 checked wrapper rows and their explicit non-Schmidt boundaries. -/
def c08LowDimensionalPartialWrapperRows :
    List LowDimensionalPartialWrapperRow := [
  {
    id := "M0401.C08.DIR01.RationalApproximation"
    api := LowDimensionalPartialApi.dirichletRationalApproximation
    wrapperName := "c08_dirichletOneDimensional_rationalApproximation"
    mathlibAnchor := "Real.exists_rat_abs_sub_le_and_den_le"
    dimensionBoundary := "one real number and one rational approximant with denominator bounded by N"
    schmidtBoundary := "existence-only Dirichlet substrate; not algebraic-input finiteness and not the full Schmidt theorem"
  },
  {
    id := "M0401.C08.DIR02.RoundedNumerator"
    api := LowDimensionalPartialApi.dirichletRoundedNumerator
    wrapperName := "c08_dirichletOneDimensional_roundedNumerator"
    mathlibAnchor := "Real.exists_nat_abs_mul_sub_round_le"
    dimensionBoundary := "one real number, one positive natural denominator, and a rounded integer numerator"
    schmidtBoundary := "existence-only rounded-numerator substrate; not product-form simultaneous approximation"
  },
  {
    id := "M0401.C08.LEG01.ConvergentCriterion"
    api := LowDimensionalPartialApi.legendreConvergentCriterion
    wrapperName := "c08_legendreOneDimensional_convergentCriterion"
    mathlibAnchor := "Real.exists_rat_eq_convergent"
    dimensionBoundary := "one real number and one rational approximant satisfying the Legendre threshold"
    schmidtBoundary := "continued-fraction classification of a single approximant; not a finite-exception Schmidt result"
  },
  {
    id := "M0401.C08.HGT01.HeightLowerBounds"
    api := LowDimensionalPartialApi.heightLowerBounds
    wrapperName := "c08_heightElement_mulHeight_ge_one / c08_heightTuple_mulHeight_ge_one"
    mathlibAnchor := "Height.one_le_mulHeight₁ / Height.one_le_mulHeight"
    dimensionBoundary := "field elements and finite tuples under Height.AdmissibleAbsValues"
    schmidtBoundary := "height substrate only; local-height normalization and exceptional-subspace extraction remain open"
  }
]

/-- C08 records four partial substrate rows. -/
theorem c08LowDimensionalPartialWrapperRows_length :
    c08LowDimensionalPartialWrapperRows.length = 4 :=
  rfl

/-- C08 wrappers are explicitly partial and do not claim the Schmidt theorem. -/
def c08LowDimensionalPartialWrapperDiagnosis : String :=
  "C08: checked low-dimensional partial wrappers around Dirichlet, Legendre, and height APIs; partial substrate only, not the full Schmidt theorem and not a completion claim"

/-! ## C09 local validation gate -/

/--
C09 status for the local build/file-check gate.

The passing state means this file checked with the recorded command on the
recorded absolute date. It is not a theorem-completion state for Schmidt's
theorem.
-/
inductive LocalValidationStatus where
  | passedFileCheckNoCompletionClaim
  | failedFileCheck
  | notRun
deriving DecidableEq, Repr

/-- C09 file-level validation command required by the child task. -/
def c09LocalValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_014.lean"

/-- C09 absolute validation date for the local file-check pass. -/
def c09LocalValidationDate : String :=
  "2026-05-01"

/--
Current C09 status: the owned Stage1 file is expected to pass the recorded
file-level check, with no public theorem-status upgrade implied.
-/
def c09LocalFileCheckStatus : LocalValidationStatus :=
  LocalValidationStatus.passedFileCheckNoCompletionClaim

/-- C09 boolean gate for the requested local file-level Lean check. -/
def c09LocalFileCheckPassed : Bool :=
  true

/--
C09 root-completion gate.

A file-level check of statement-shape/audit wrappers is insufficient to upgrade
the parent Schmidt theorem to a completed repo-local proof state.
-/
def c09AllowsRootTheoremCompletionClaim : Bool :=
  false

/-- C09 confirms the local file-check status. -/
theorem c09LocalFileCheckStatus_eq_passed :
    c09LocalFileCheckStatus =
      LocalValidationStatus.passedFileCheckNoCompletionClaim := by
  rfl

/-- C09 confirms that the file-level validation command passed. -/
theorem c09LocalFileCheckPassed_eq_true :
    c09LocalFileCheckPassed = true := by
  rfl

/-- C09 blocks a parent theorem completion claim from this validation alone. -/
theorem c09AllowsRootTheoremCompletionClaim_eq_false :
    c09AllowsRootTheoremCompletionClaim = false := by
  rfl

/--
Public-backfill-ready C09 diagnosis.

The validation result can support a public C09 status line only. It cannot be
used to mark `CanonicalProductStatementShape`, `StatementShape`, or
`SimultaneousRothSchmidtStatementShape` proved.
-/
def c09LocalValidationDiagnosis : String :=
  "C09: local file-level validation passed on 2026-05-01 with lake env lean; this validates statement-shape/audit wrappers only and does not permit a Schmidt theorem completion claim"

/-! ## Audit probes -/

#check IsAlgebraic
#check LinearIndependent
#check Real.rpow
#check Set.Finite
#check Finset.prod
#check Real.exists_rat_abs_sub_le_and_den_le
#check Real.exists_nat_abs_mul_sub_round_le
#check Real.exists_rat_eq_convergent
#check primarySourceForStage0_1980Label
#check canonicalTheoremPrimarySource
#check stage0_1980LabelDiagnosis
#check AlgebraicVector
#check RationalIndependenceWithOne
#check NearestIntegerDistance
#check CanonicalProductTooGood
#check CanonicalProductConclusion
#check CanonicalProductStatementShape
#check canonicalProductStatementShape_iff
#check TooGoodApproximation
#check SimultaneousApproximationConclusion
#check StatementShape
#check SimultaneousRothSchmidtStatementShape
#check SchmidtSubspaceModel
#check SchmidtSubspaceStatementShape
#check PublicStatementTarget
#check chosenPublicStatementTarget
#check chosenPublicStatementTarget_eq_simultaneousRothSchmidt
#check SchmidtSubspaceToSimultaneousReductionShape
#check simultaneousRothSchmidtStatementShape_iff_statementShape
#check statementTargetDecisionDiagnosis
#check statementShape_iff
#check canonicalProductConclusion_of_statementShape
#check simultaneousApproximationConclusion_of_statementShape
#check WorkSurface
#check MachineState
#check MachineProofDebt
#check SchmidtObjectModelComponent
#check MathlibObjectModelAuditRow
#check schmidtObjectModelAuditRevision
#check schmidtObjectModelAuditTable
#check schmidtObjectModelAuditTable_length
#check schmidtObjectModelAuditTable_components
#check schmidtObjectModelAuditCoversC03Components_eq_true
#check schmidtObjectModelOpenBridgeRows
#check AuditRow
#check ProofPackage
#check statementAuditRows
#check proofPackageSplit
#check currentMachineState_not_completed
#check NumberField
#check AbsoluteValue
#check NumberField.FinitePlace
#check NumberField.InfinitePlace
#check NumberField.IsFinitePlace
#check NumberField.IsInfinitePlace
#check Height.AdmissibleAbsValues
#check NumberField.instAdmissibleAbsValues
#check Height.mulHeight
#check Height.logHeight
#check Projectivization.mulHeight
#check Height.mulHeight_linearMap_apply_le
#check ExternalLeanProjectSearchRow
#check externalLeanProjectSearchRows
#check externalLeanProjectSearchRows_length
#check externalLeanProjectSearchConclusion
#check CoreProofIntegrationStatus
#check c05CoreProofIntegrationStatus
#check c05CoreMachineProofDebt
#check c05CoreMachineState
#check c05ExternalProofPinnedImportedChecked
#check c05CoreProofIntegrationStatus_eq_formalizationDebt
#check c05ExternalProofPinnedImportedChecked_eq_false
#check c05CoreMachineState_not_completed
#check c05CoreProofIntegrationDiagnosis
#check StatementShapeFileValidationStatus
#check c06StatementShapeFileValidationStatus
#check c06ImportsAndSyntaxValidated
#check c06StatementShapeFileValidationStatus_eq_checked
#check c06ImportsAndSyntaxValidated_eq_true
#check c06StatementShapeFileValidationDiagnosis
#check HighRiskBridgeArea
#check BridgeLeafLedger
#check c07HighRiskBridgeLeafLedgers
#check c07HighRiskBridgeLeafLedgers_length
#check c07LocalHeightLeafLedgerIds
#check c07ExceptionalSubspaceLeafLedgerIds
#check c07IntegrationGateLeafLedgerIds
#check c07LocalHeightLeafLedgerIds_eq
#check c07ExceptionalSubspaceLeafLedgerIds_eq
#check c07IntegrationGateLeafLedgerIds_eq
#check c07HighRiskBridgeLeafBudgets
#check c07HighRiskBridgeLeafBudgets_eq
#check c07HighRiskBridgeLeafSplitDiagnosis
#check LowDimensionalPartialApi
#check LowDimensionalPartialWrapperRow
#check c08_dirichletOneDimensional_rationalApproximation
#check c08_dirichletOneDimensional_roundedNumerator
#check c08_legendreOneDimensional_convergentCriterion
#check c08_heightElement_mulHeight_ge_one
#check c08_heightTuple_mulHeight_ge_one
#check c08LowDimensionalPartialWrapperRows
#check c08LowDimensionalPartialWrapperRows_length
#check c08LowDimensionalPartialWrapperDiagnosis
#check LocalValidationStatus
#check c09LocalValidationCommand
#check c09LocalValidationDate
#check c09LocalFileCheckStatus
#check c09LocalFileCheckPassed
#check c09AllowsRootTheoremCompletionClaim
#check c09LocalFileCheckStatus_eq_passed
#check c09LocalFileCheckPassed_eq_true
#check c09AllowsRootTheoremCompletionClaim_eq_false
#check c09LocalValidationDiagnosis

end AwesomeTheorems.Stage1.S1_M_014
