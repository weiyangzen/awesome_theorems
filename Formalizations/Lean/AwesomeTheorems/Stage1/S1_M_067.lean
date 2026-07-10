import Mathlib.LinearAlgebra.QuadraticForm.TensorProduct
import Mathlib.LinearAlgebra.QuadraticForm.Real
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.Completion.FinitePlace
import Mathlib.NumberTheory.NumberField.ProductFormula

/-!
# S1-M-067 / THM-M-0423: Hasse principle

This Stage1 artifact records conservative Lean 4 statement-shape candidates for
the local-global, or Hasse, principle.  It is not a proof of a terminal Hasse
principle theorem.

The checked part is intentionally small: mathlib currently supplies number-field
adeles, finite places/completions, local-field infrastructure, and quadratic
forms, but this audit did not locate a theorem named as the full
Hasse-Minkowski theorem or a general Hasse-principle package in the repo-local
dependency closure.
-/

noncomputable section

namespace AwesomeTheorems.Stage1.S1_M_067

universe u v w

open scoped NumberField TensorProduct

/-- The mathlib adelic object for a number field, using its ring of integers. -/
abbrev NumberFieldAdeles (K : Type u) [Field K] [NumberField K] :=
  NumberField.AdeleRing (NumberField.RingOfIntegers K) K

/--
Checked mathlib wrapper: the diagonal map from a number field into its adeles is
injective.  This is infrastructure for local-global statements, not a Hasse
principle theorem.
-/
theorem numberFieldAdeles_algebraMap_injective (K : Type u) [Field K] [NumberField K] :
    Function.Injective (algebraMap K (NumberFieldAdeles K)) := by
  exact NumberField.AdeleRing.algebraMap_injective (NumberField.RingOfIntegers K) K

/-- Nontrivial isotropic vector for a quadratic form over a field. -/
def HasNontrivialZero {K : Type u} {V : Type v} [Field K] [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) : Prop :=
  ∃ x : V, x ≠ 0 ∧ Q x = 0

/--
Abstract local data for a quadratic-form Hasse-Minkowski statement.

The local vector spaces are kept abstract because the current audit only found
finite-place/completion infrastructure, not a ready theorem connecting every
number-field place, base-changed quadratic form, and isotropy predicate.
-/
structure QuadraticLocalGlobalData
    (K : Type u) [Field K] (V : Type v) [AddCommGroup V] [Module K V] :
    Type (max (u + 1) (v + 1) (w + 1)) where
  Place : Type w
  LocalVector : Place → Type v
  localAdd : ∀ place, AddCommGroup (LocalVector place)
  localModule : ∀ place, Module K (LocalVector place)
  baseChange : (place : Place) → V →ₗ[K] LocalVector place
  baseChange_injective : ∀ place, Function.Injective (baseChange place)
  localForm : (Q : QuadraticForm K V) → (place : Place) → QuadraticForm K (LocalVector place)
  localForm_baseChange_eval :
    ∀ (Q : QuadraticForm K V) (place : Place) (x : V),
      localForm Q place (baseChange place x) = Q x
  isArithmeticCompletionFamily : Prop

namespace QuadraticLocalGlobalData

variable {K : Type u} [Field K]
variable {V : Type v} [AddCommGroup V] [Module K V]
variable (D : QuadraticLocalGlobalData.{u, v, w} K V)

/-- Local solubility of a quadratic form at every place in the abstract local datum. -/
def LocallySoluble (Q : QuadraticForm K V) : Prop :=
  ∀ place : D.Place,
    letI : AddCommGroup (D.LocalVector place) := D.localAdd place
    letI : Module K (D.LocalVector place) := D.localModule place
    HasNontrivialZero (D.localForm Q place)

/--
The easy direction of a local-global statement: a global nontrivial zero gives
a local nontrivial zero after an injective base-change map.

This checked lemma is not the Hasse principle.  The hard direction is the
converse, recorded below only as a statement shape.
-/
theorem locallySoluble_of_global {Q : QuadraticForm K V} (hQ : HasNontrivialZero Q) :
    D.LocallySoluble Q := by
  intro place
  letI : AddCommGroup (D.LocalVector place) := D.localAdd place
  letI : Module K (D.LocalVector place) := D.localModule place
  rcases hQ with ⟨x, hx_ne, hx_zero⟩
  refine ⟨D.baseChange place x, ?_, ?_⟩
  · intro hx_local
    exact hx_ne (D.baseChange_injective place (by simpa using hx_local))
  · simpa [D.localForm_baseChange_eval]

/--
Statement shape for the quadratic-form Hasse-Minkowski direction over the
abstract local datum: local isotropy at all arithmetic completions implies
global isotropy.
-/
def HasseMinkowskiStatement (Q : QuadraticForm K V) : Prop :=
  D.isArithmeticCompletionFamily → D.LocallySoluble Q → HasNontrivialZero Q

end QuadraticLocalGlobalData

/--
Generic local-global datum for a Hasse principle statement.

This covers the source item's broad wording "local-global principle"; specific
instances such as quadratic forms, Severi-Brauer varieties, torsors, or elliptic
curves should later replace these abstract predicates by concrete mathlib or
pinned external APIs.
-/
structure HassePrincipleDatum (K : Type u) [Field K] : Type (max (u + 1) (v + 1) (w + 1)) where
  GlobalObject : Type v
  Place : Type w
  hasGlobalPoint : GlobalObject → Prop
  hasLocalPoint : GlobalObject → Place → Prop
  admissibleForHassePrinciple : GlobalObject → Prop

namespace HassePrincipleDatum

variable {K : Type u} [Field K]
variable (D : HassePrincipleDatum.{u, v, w} K)

/-- Statement shape for a Hasse principle attached to a concrete class of objects. -/
def Statement : Prop :=
  ∀ X : D.GlobalObject,
    D.admissibleForHassePrinciple X →
      (∀ place : D.Place, D.hasLocalPoint X place) →
        D.hasGlobalPoint X

end HassePrincipleDatum

/--
Stage1 normalized statement-shape candidate for the number-field Hasse principle.

The theorem is parameterized by a concrete datum rather than claimed outright
from mathlib.  A later formalization must instantiate `D` with a genuine object
class and prove `D.Statement`.
-/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (D : HassePrincipleDatum.{u, v, w} K), D.Statement

/--
Stage1 normalized statement-shape candidate for the classical Hasse-Minkowski
specialization to finite-dimensional quadratic forms over number fields.
-/
def QuadraticStatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (D : QuadraticLocalGlobalData.{u, v, w} K V)
    (Q : QuadraticForm K V),
      D.HasseMinkowskiStatement Q

/--
The C001 statement-normalization boundary: keep both readings visible.

`StatementShape` is the broad generic local-global schema.  `QuadraticStatementShape`
is the classical Hasse-Minkowski specialization boundary.  Their conjunction is a
checked public-merge target only; it is not a proof of either direction.
-/
def StatementNormalizationBoundary : Prop :=
  StatementShape.{u, v, w} ∧ QuadraticStatementShape.{u, v, w}

/-- The normalization boundary is definitionally the generic/quadratic pair. -/
theorem statementNormalizationBoundary_iff :
    StatementNormalizationBoundary.{u, v, w} ↔
      StatementShape.{u, v, w} ∧ QuadraticStatementShape.{u, v, w} := by
  rfl

/--
Machine-readable C001 decision for public backfill.

This audit records that the generic and quadratic statement shapes typecheck, but
that no bridge from the abstract generic schema to concrete quadratic completions,
and no terminal Hasse principle theorem, is claimed here.
-/
structure StatementNormalizationAudit where
  genericDatumTypechecks : Bool
  genericStatementShapeTypechecks : Bool
  quadraticDatumTypechecks : Bool
  quadraticStatementShapeTypechecks : Bool
  genericQuadraticBridgeClaimed : Bool
  terminalHassePrincipleClaimed : Bool
  decision : String
  blockerSummary : List String

/-- C001 audit: statement normalization is ready for public backfill, not completion. -/
def c001StatementNormalizationAudit : StatementNormalizationAudit where
  genericDatumTypechecks := true
  genericStatementShapeTypechecks := true
  quadraticDatumTypechecks := true
  quadraticStatementShapeTypechecks := true
  genericQuadraticBridgeClaimed := false
  terminalHassePrincipleClaimed := false
  decision := "merge_generic_and_quadratic_boundaries_without_completion"
  blockerSummary := [
    "replace HassePrincipleDatum by a selected concrete theorem family before any generic completion claim",
    "replace QuadraticLocalGlobalData by actual finite and infinite completions over a number field",
    "connect QuadraticForm.baseChange to scalar extension over those completions",
    "prove or import Hilbert-symbol, local-classification, and product-formula packages for Hasse-Minkowski",
    "pin/import/check any external Lean 4 proof before changing the repo-local completion status"
  ]

/-! ## C002 mathlib anchor audit -/

/-- Exact pinned mathlib revision audited by child `S1-M-067-C002`. -/
def c002MathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules containing the C002 Hasse-principle substrate anchors. -/
def c002MathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.NumberTheory.NumberField.Completion.FinitePlace",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.LinearAlgebra.QuadraticForm.Basic",
  "Mathlib.LinearAlgebra.QuadraticForm.TensorProduct"
]

/--
One machine-readable row in the C002 anchor audit.

These rows record available mathlib infrastructure.  They are not terminal
Hasse-principle or Hasse-Minkowski proof rows.
-/
structure C002MathlibAnchorRow where
  anchorName : String
  sourceModule : String
  declarationKind : String
  roleForTHM_M_0423 : String
  completionContribution : String

/-- C002 mathlib anchor table for public backfill at the pinned revision. -/
def c002MathlibAnchorRows : List C002MathlibAnchorRow := [
  {
    anchorName := "NumberField"
    sourceModule := "Mathlib.NumberTheory.NumberField.Basic"
    declarationKind := "class"
    roleForTHM_M_0423 := "global field base for number-field local-global statements"
    completionContribution := "substrate_anchor_only_not_terminal_proof"
  },
  {
    anchorName := "NumberField.FinitePlace"
    sourceModule := "Mathlib.NumberTheory.NumberField.Completion.FinitePlace"
    declarationKind := "finite-place API"
    roleForTHM_M_0423 := "finite nonarchimedean place substrate for completions"
    completionContribution := "substrate_anchor_only_not_terminal_proof"
  },
  {
    anchorName := "NumberField.AdeleRing"
    sourceModule := "Mathlib.NumberTheory.NumberField.AdeleRing"
    declarationKind := "def"
    roleForTHM_M_0423 := "adelic infrastructure and diagonal embedding substrate"
    completionContribution := "checked adjacent wrapper only, not Hasse-Minkowski"
  },
  {
    anchorName := "IsNonarchimedeanLocalField"
    sourceModule := "Mathlib.NumberTheory.LocalField.Basic"
    declarationKind := "class"
    roleForTHM_M_0423 := "local-field class for nonarchimedean local branches"
    completionContribution := "substrate_anchor_only_not_terminal_proof"
  },
  {
    anchorName := "QuadraticForm"
    sourceModule := "Mathlib.LinearAlgebra.QuadraticForm.Basic"
    declarationKind := "structure"
    roleForTHM_M_0423 := "quadratic-form object for the classical Hasse-Minkowski branch"
    completionContribution := "substrate_anchor_only_not_terminal_proof"
  },
  {
    anchorName := "QuadraticForm.baseChange"
    sourceModule := "Mathlib.LinearAlgebra.QuadraticForm.TensorProduct"
    declarationKind := "protected def"
    roleForTHM_M_0423 := "scalar-extension API needed to compare global and local quadratic forms"
    completionContribution := "substrate_anchor_only_not_terminal_proof"
  }
]

/-- The C002 public anchor audit has exactly the six requested rows. -/
theorem c002MathlibAnchorRows_length :
    c002MathlibAnchorRows.length = 6 := by
  rfl

/--
C002 repo-local integration-debt gate.

The audited mathlib declarations are part of the repo-local Lake closure and are
checked below by `#check`, but they are only substrate anchors.  The checked
adjacent theorem `numberFieldAdeles_algebraMap_injective` contributes local
infrastructure, not a terminal Hasse principle proof.  Therefore this child
closes the requested anchor-audit leaf without claiming theorem completion or
retaining anchor-only evidence as a completed proof state.
-/
def c002RepoLocalIntegrationDebtGate : List String := [
  "mathlib anchors are in the repo-local Lake closure at revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "no external Hasse-Minkowski or generic Hasse-principle proof is claimed by C002",
  "anchor-only substrate rows do not count as repo-local theorem completion",
  "parent remains formalization_debt/not_repo_local_closed until concrete completion and proof packages are closed"
]

/-! ## C003 concrete quadratic Hasse-Minkowski branch -/

/-- The completion of a number field at a finite place. -/
abbrev FinitePlaceCompletion (K : Type u) [Field K] [NumberField K]
    (w : NumberField.FinitePlace K) : Type u :=
  (NumberField.FinitePlace.maximalIdeal w).adicCompletion K

/-- The completion of a number field at an infinite place. -/
abbrev InfinitePlaceCompletion (K : Type u) [Field K]
    (w : NumberField.InfinitePlace K) : Type u :=
  w.Completion

/--
Concrete places for the quadratic Hasse-Minkowski branch: finite
nonarchimedean places and infinite archimedean places of a number field.
-/
inductive QuadraticPlace (K : Type u) [Field K] [NumberField K] : Type u where
  | finite : NumberField.FinitePlace K → QuadraticPlace K
  | infinite : NumberField.InfinitePlace K → QuadraticPlace K

namespace QuadraticPlace

variable {K : Type u} [Field K] [NumberField K]

/-- The completion field attached to a concrete quadratic place. -/
abbrev scalarCompletion : QuadraticPlace K → Type u
  | finite w => FinitePlaceCompletion K w
  | infinite w => InfinitePlaceCompletion K w

instance (place : QuadraticPlace K) : Field place.scalarCompletion := by
  cases place <;> infer_instance

instance (place : QuadraticPlace K) : Algebra K place.scalarCompletion := by
  cases place <;> infer_instance

/-- Scalar extension of the global vector space to a concrete completion. -/
abbrev localVector (place : QuadraticPlace K) (V : Type v)
    [AddCommGroup V] [Module K V] : Type (max u v) :=
  place.scalarCompletion ⊗[K] V

/--
Scalar extension of a global quadratic form to the vector space over a concrete
completion.
-/
noncomputable abbrev localForm (place : QuadraticPlace K) {V : Type v}
    [AddCommGroup V] [Module K V] (Q : QuadraticForm K V) :
    QuadraticForm place.scalarCompletion (place.localVector V) :=
  Q.baseChange place.scalarCompletion

/-- Evaluation of the concrete local form on the pure tensor `1 ⊗ x`. -/
@[simp]
theorem localForm_tmul_one (place : QuadraticPlace K) {V : Type v}
    [AddCommGroup V] [Module K V] (Q : QuadraticForm K V) (x : V) :
    place.localForm Q ((1 : place.scalarCompletion) ⊗ₜ[K] x) =
      algebraMap K place.scalarCompletion (Q x) := by
  cases place <;> simp [localForm, localVector, Algebra.smul_def]

end QuadraticPlace

/--
Local solubility of a quadratic form at every concrete finite and infinite
completion currently available in mathlib.
-/
def ConcreteQuadraticLocallySoluble
    (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) : Prop :=
  ∀ place : QuadraticPlace K,
    HasNontrivialZero (place.localForm (V := V) Q)

/--
Concrete statement shape for the Hasse-Minkowski direction: isotropy over every
finite and infinite completion implies global isotropy.

This is only a checked statement shape.  The local-to-global implication is not
proved here.
-/
def ConcreteQuadraticHasseMinkowskiStatement
    (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) : Prop :=
  ConcreteQuadraticLocallySoluble K V Q → HasNontrivialZero Q

/--
Stage1 concrete Hasse-Minkowski branch for finite-dimensional quadratic forms.

This replaces the abstract place family by the concrete finite/infinite
completion family at the statement-shape level, but does not claim the theorem.
-/
def ConcreteQuadraticStatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V),
      ConcreteQuadraticHasseMinkowskiStatement K V Q

/--
C003 audit record for the concrete quadratic branch.

The checked fields record that the finite/infinite completions and
`QuadraticForm.baseChange` scalar-extension shapes typecheck repo-locally.  The
hard Hasse-Minkowski proof packages are still absent.
-/
structure C003QuadraticBranchAudit where
  finiteCompletionsTypecheck : Bool
  infiniteCompletionsTypecheck : Bool
  placeSumTypechecks : Bool
  scalarExtensionFormsTypecheck : Bool
  concreteStatementShapeTypechecks : Bool
  hardLocalToGlobalClaimed : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  decision : String
  blockerSummary : List String

/-- C003 audit result: concrete statement-shape progress, not theorem completion. -/
def c003QuadraticBranchAudit : C003QuadraticBranchAudit where
  finiteCompletionsTypecheck := true
  infiniteCompletionsTypecheck := true
  placeSumTypechecks := true
  scalarExtensionFormsTypecheck := true
  concreteStatementShapeTypechecks := true
  hardLocalToGlobalClaimed := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  decision := "concrete_quadratic_completion_branch_typechecks_without_completion_claim"
  blockerSummary := [
    "prove injectivity/nonzero transport for the canonical pure-tensor maps into each completion",
    "formalize or import Hilbert symbols and local invariants over the concrete completion fields",
    "formalize or import real and nonarchimedean local classification for quadratic forms",
    "connect the product formula/Hilbert reciprocity package to the concrete local invariants",
    "prove or import the local-to-global Hasse-Minkowski implication before any completion claim"
  ]

/-! ## C004 Hilbert-symbol package audit -/

/--
Checked wrapper for mathlib's number-field product formula.

This is useful arithmetic substrate for later Hilbert reciprocity work, but it
is not itself a Hilbert-symbol reciprocity theorem and does not prove
Hasse-Minkowski.
-/
theorem numberField_productFormula_anchor
    (K : Type u) [Field K] [NumberField K] {x : K} (hx : x ≠ 0) :
    (∏ w : NumberField.InfinitePlace K, w x ^ w.mult) *
        ∏ᶠ w : NumberField.FinitePlace K, w x = 1 := by
  exact NumberField.prod_abs_eq_one hx

/--
One machine-readable row in the C004 Hilbert-symbol package audit.

Rows may be checked substrate anchors or explicitly missing APIs.  A missing row
is formalization debt, not repo-local integration debt, because this audit did
not find an external Lean 4 proof to pin/import/check.
-/
structure C004HilbertSymbolPackageRow where
  apiName : String
  expectedRoleForHasseMinkowski : String
  repoLocalStatus : String
  nextClosureCondition : String

/-- C004 package rows for the Hilbert-symbol/local-invariant proof package. -/
def c004HilbertSymbolPackageRows : List C004HilbertSymbolPackageRow := [
  {
    apiName := "NumberField.prod_abs_eq_one"
    expectedRoleForHasseMinkowski :=
      "checked number-field product formula substrate for later reciprocity arguments"
    repoLocalStatus := "local_wrapper_upstream_mathlib"
    nextClosureCondition :=
      "connect this product formula to Hilbert-symbol Hilbert reciprocity after those symbols exist"
  },
  {
    apiName := "QuadraticPlace.scalarCompletion"
    expectedRoleForHasseMinkowski :=
      "concrete finite/infinite completion carrier on which local symbols and invariants must live"
    repoLocalStatus := "local_statement_shape"
    nextClosureCondition :=
      "instantiate Hilbert symbols and local invariants over each concrete scalar completion"
  },
  {
    apiName := "HilbertSymbol"
    expectedRoleForHasseMinkowski :=
      "binary local invariant (a,b)_v controlling two-dimensional quadratic subblocks"
    repoLocalStatus := "missing_after_repo_local_mathlib_search"
    nextClosureCondition :=
      "formalize a Lean API or pin/import/check an external Lean 4 implementation"
  },
  {
    apiName := "QuadraticForm.localHasseInvariant"
    expectedRoleForHasseMinkowski :=
      "local invariant assembled from diagonal coefficients and Hilbert symbols"
    repoLocalStatus := "missing_after_repo_local_mathlib_search"
    nextClosureCondition :=
      "define the invariant over real and nonarchimedean local fields and prove basis invariance"
  },
  {
    apiName := "HilbertSymbol.product_formula"
    expectedRoleForHasseMinkowski :=
      "Hilbert reciprocity/product formula tying local invariants to a global obstruction"
    repoLocalStatus := "missing_after_repo_local_mathlib_search"
    nextClosureCondition :=
      "prove or import the reciprocity theorem and connect it to the concrete local invariant package"
  }
]

/-- The C004 Hilbert-symbol package audit has exactly the five requested rows. -/
theorem c004HilbertSymbolPackageRows_length :
    c004HilbertSymbolPackageRows.length = 5 := by
  rfl

/--
C004 audit record.

The checked part is the product-formula wrapper.  The Hilbert symbol, local
Hasse invariant, and Hilbert reciprocity APIs remain absent from the repo-local
Lean closure located by this child.
-/
structure C004HilbertSymbolPackageAudit where
  numberFieldProductFormulaInRepoLocalClosure : Bool
  hilbertSymbolDeclarationFoundInRepoLocalSearch : Bool
  localInvariantDeclarationFoundInRepoLocalSearch : Bool
  hilbertReciprocityDeclarationFoundInRepoLocalSearch : Bool
  terminalHasseMinkowskiClaimed : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  decision : String
  blockerSummary : List String

/--
C004 audit result: one checked product-formula anchor plus missing
Hilbert-symbol/local-invariant/reciprocity APIs.
-/
def c004HilbertSymbolPackageAudit : C004HilbertSymbolPackageAudit where
  numberFieldProductFormulaInRepoLocalClosure := true
  hilbertSymbolDeclarationFoundInRepoLocalSearch := false
  localInvariantDeclarationFoundInRepoLocalSearch := false
  hilbertReciprocityDeclarationFoundInRepoLocalSearch := false
  terminalHasseMinkowskiClaimed := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  decision := "product_formula_anchor_checked_hilbert_symbol_package_remains_formalization_debt"
  blockerSummary := [
    "mathlib supplies NumberField.prod_abs_eq_one, checked here by numberField_productFormula_anchor",
    "repo-local search found no HilbertSymbol declaration for the quadratic-form Hasse-Minkowski branch",
    "repo-local search found no local Hasse invariant API for quadratic forms over the concrete completions",
    "repo-local search found no Hilbert-symbol reciprocity/product-formula theorem",
    "parent remains not_repo_local_closed until these APIs are formalized or pinned/imported/checked"
  ]

/-- C004 repo-local integration-debt gate: no completed theorem state is claimed. -/
def c004RepoLocalIntegrationDebtGate : List String := [
  "NumberField.prod_abs_eq_one is in the repo-local Lake closure and wrapped by numberField_productFormula_anchor",
  "the product-formula wrapper is substrate only and is not Hilbert reciprocity",
  "no external Hilbert-symbol or Hasse-Minkowski proof is recorded as anchor-only completed evidence",
  "remaining missing Hilbert-symbol, local-invariant, and reciprocity APIs are formalization_debt/not_repo_local_closed"
]

/-! ## C005 local classification package split -/

/--
Real quadratic-form local classification statement used by the C005 package.

This is Sylvester's law of inertia in the form currently available from
mathlib: every finite-dimensional real quadratic form is equivalent to a
weighted sum of squares with coefficients in `{-1, 0, 1}`.
-/
def RealLocalQuadraticClassificationStatement : Prop :=
  ∀ (V : Type v) [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V]
    (Q : QuadraticForm ℝ V),
      ∃ w : Fin (Module.finrank ℝ V) → ℝ,
        (∀ i, w i = -1 ∨ w i = 0 ∨ w i = 1) ∧
          QuadraticMap.Equivalent Q (QuadraticMap.weightedSumSquares ℝ w)

/--
Checked C005 wrapper for the real local classification leaf.

This proves only the real Sylvester diagonalization leaf.  It does not package
the result as the local invariant interface needed by the Hasse-Minkowski proof,
and it does not prove any nonarchimedean classification theorem.
-/
theorem realLocalQuadraticClassification_anchor :
    RealLocalQuadraticClassificationStatement.{v} := by
  intro V _ _ _ Q
  exact Q.equivalent_one_zero_neg_one_weighted_sum_squared

/--
Expected shape of a nonarchimedean quadratic-form classification package.

No instance of this package is constructed here.  The fields name the interfaces
that a later formalization or pinned import must provide before the
nonarchimedean local branch can feed the Hasse-Minkowski proof.
-/
structure NonarchimedeanLocalQuadraticClassificationPackage
    (F : Type u) [Field F] [ValuativeRel F] [TopologicalSpace F]
    [IsNonarchimedeanLocalField F] :
    Type (max (u + 1) (v + 1)) where
  invariant :
    (V : Type v) → [AddCommGroup V] → [Module F V] → [FiniteDimensional F V] →
      QuadraticForm F V → Type v
  classifiesEquivalentForms : Prop
  isotropyCriterion : Prop
  compatibleWithHilbertSymbols : Prop

/-- Type-level target for the nonarchimedean local classification leaf. -/
def NonarchimedeanLocalQuadraticClassificationStatementShape
    (F : Type u) [Field F] [ValuativeRel F] [TopologicalSpace F]
    [IsNonarchimedeanLocalField F] :
    Type (max (u + 1) (v + 1)) :=
  NonarchimedeanLocalQuadraticClassificationPackage.{u, v} F

/--
One C005 local classification leaf.

Each row is independently budgeted at `<= 100` proof steps.  A row may have a
checked local anchor without closing the parent Hasse-Minkowski theorem.
-/
structure C005LocalClassificationLeaf where
  canonicalLeaf : String
  localBranch : String
  expectedClassification : String
  upstreamInput : String
  downstreamOutput : String
  budgetLimit : Nat
  repoLocalStatus : String
  nextClosureCondition : String

/-- C005 real local classification leaf, anchored by Sylvester's law in mathlib. -/
def c005RealLocalClassificationLeaf : C005LocalClassificationLeaf where
  canonicalLeaf := "THM-M-0423.local_classification_package.real_sylvester"
  localBranch := "archimedean_real"
  expectedClassification :=
    "finite-dimensional real quadratic forms diagonalize to coefficients -1, 0, and 1"
  upstreamInput :=
    "QuadraticForm.equivalent_one_zero_neg_one_weighted_sum_squared"
  downstreamOutput :=
    "signature-style real local invariant and real isotropy criterion for the concrete Hasse-Minkowski branch"
  budgetLimit := 100
  repoLocalStatus :=
    "local_wrapper_upstream_mathlib_for_real_diagonal_classification_only"
  nextClosureCondition :=
    "package the checked diagonalization anchor as the exact signature/isotropy interface consumed by the local-global proof"

/-- C005 nonarchimedean local classification leaf, still missing from repo-local closure. -/
def c005NonarchimedeanLocalClassificationLeaf : C005LocalClassificationLeaf where
  canonicalLeaf := "THM-M-0423.local_classification_package.nonarchimedean"
  localBranch := "finite_nonarchimedean"
  expectedClassification :=
    "quadratic forms over nonarchimedean local fields classified by dimension, determinant/discriminant, and Hasse invariant with an isotropy criterion"
  upstreamInput :=
    "IsNonarchimedeanLocalField plus Hilbert-symbol and local-invariant APIs"
  downstreamOutput :=
    "nonarchimedean local invariant and isotropy criterion for every finite place in QuadraticPlace"
  budgetLimit := 100
  repoLocalStatus :=
    "formalization_debt_not_repo_local_closed"
  nextClosureCondition :=
    "formalize locally or pin/import/check a Lean 4 package for nonarchimedean quadratic-form classification and its Hilbert-symbol compatibility"

/-- C005 splits local classification into exactly the real and nonarchimedean leaves. -/
def c005LocalClassificationLeaves : List C005LocalClassificationLeaf := [
  c005RealLocalClassificationLeaf,
  c005NonarchimedeanLocalClassificationLeaf
]

/-- The C005 local-classification package has exactly two independently budgeted leaves. -/
theorem c005LocalClassificationLeaves_length :
    c005LocalClassificationLeaves.length = 2 := by
  rfl

/-- Both C005 leaves are explicitly budgeted at `<= 100` proof steps. -/
theorem c005LocalClassificationLeaf_budget_gates :
    c005RealLocalClassificationLeaf.budgetLimit <= 100 ∧
      c005NonarchimedeanLocalClassificationLeaf.budgetLimit <= 100 := by
  decide

/--
C005 package audit.

The real branch has a checked mathlib wrapper.  The nonarchimedean branch is a
concrete formalization-debt leaf, not anchor-only completed evidence.
-/
structure C005LocalClassificationPackageAudit where
  realSylvesterAnchorInRepoLocalClosure : Bool
  nonarchimedeanClassificationFoundInRepoLocalSearch : Bool
  independentLeavesBudgetedAtOrBelow100 : Bool
  terminalHasseMinkowskiClaimed : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  decision : String
  blockerSummary : List String

/-- C005 audit result: split and partially anchored, but not theorem completion. -/
def c005LocalClassificationPackageAudit : C005LocalClassificationPackageAudit where
  realSylvesterAnchorInRepoLocalClosure := true
  nonarchimedeanClassificationFoundInRepoLocalSearch := false
  independentLeavesBudgetedAtOrBelow100 := true
  terminalHasseMinkowskiClaimed := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  decision := "split_real_and_nonarchimedean_local_classification_leaves_without_completion_claim"
  blockerSummary := [
    "real Sylvester diagonalization is checked by realLocalQuadraticClassification_anchor",
    "real branch still needs packaging as the signature/isotropy interface consumed by Hasse-Minkowski",
    "repo-local search found no nonarchimedean quadratic-form classification package over IsNonarchimedeanLocalField",
    "nonarchimedean branch remains formalization_debt until locally proved or pinned/imported/checked",
    "parent remains not_repo_local_closed until local classification, Hilbert-symbol, reciprocity, and local-to-global packages are all connected"
  ]

/-- C005 repo-local integration-debt gate: no completed theorem state is claimed. -/
def c005RepoLocalIntegrationDebtGate : List String := [
  "the real classification leaf is a repo-local wrapper over pinned mathlib, not an external anchor-only completion",
  "no external nonarchimedean classification proof is recorded as anchor-only completed evidence",
  "the nonarchimedean missing package is formalization_debt/not_repo_local_closed",
  "terminal Hasse-Minkowski completion remains blocked by unclosed local classification and local-to-global packages"
]

/-! ## C006 external Lean 4 audit gate -/

/-- Date for the C006 external Lean 4 audit pass. -/
def c006ExternalLean4AuditDate : String :=
  "2026-05-01"

/--
One C006 primary-source external Lean 4 search row.

Rows record repository/code-search attempts and external project anchors.  A row
is never completion evidence unless `exactTerminalProofFound` is true and the
proof has been pinned, imported, and checked in this repository.
-/
structure C006ExternalLean4SearchRow where
  searchName : String
  primarySource : String
  queryOrAnchor : String
  resultSummary : String
  exactTerminalProofFound : Bool
  pinImportCheckStatus : String
  completionGate : String

/--
C006 external Lean 4 audit rows.

The GitHub repository searches below were primary-source repository searches.
Unauthenticated GitHub code search returned `401 Requires authentication`, so it
is recorded as an audit blocker rather than negative evidence.  The Lorentz
workshop report is an external Lean project-progress anchor, but it reports an
incomplete formalization rather than a terminal proof ready to pin.
-/
def c006ExternalLean4SearchRows : List C006ExternalLean4SearchRow := [
  {
    searchName := "github_repository_search_exact_hasse_minkowski"
    primarySource := "GitHub REST search/repositories"
    queryOrAnchor := "q=\"Hasse-Minkowski\" Lean"
    resultSummary := "total_count=0, incomplete_results=false"
    exactTerminalProofFound := false
    pinImportCheckStatus := "no repository candidate to pin"
    completionGate := "not completion evidence"
  },
  {
    searchName := "github_repository_search_identifier_hasse_minkowski"
    primarySource := "GitHub REST search/repositories"
    queryOrAnchor := "q=HasseMinkowski Lean"
    resultSummary := "total_count=0, incomplete_results=false"
    exactTerminalProofFound := false
    pinImportCheckStatus := "no repository candidate to pin"
    completionGate := "not completion evidence"
  },
  {
    searchName := "github_repository_search_hasse_principle"
    primarySource := "GitHub REST search/repositories"
    queryOrAnchor := "q=\"Hasse principle\" Lean"
    resultSummary := "total_count=0, incomplete_results=false"
    exactTerminalProofFound := false
    pinImportCheckStatus := "no repository candidate to pin"
    completionGate := "not completion evidence"
  },
  {
    searchName := "github_repository_search_quadratic_hasse"
    primarySource := "GitHub REST search/repositories"
    queryOrAnchor := "q=\"QuadraticForm\" \"Hasse\" Lean"
    resultSummary := "total_count=0, incomplete_results=false"
    exactTerminalProofFound := false
    pinImportCheckStatus := "no repository candidate to pin"
    completionGate := "not completion evidence"
  },
  {
    searchName := "github_repository_search_hilbert_symbol"
    primarySource := "GitHub REST search/repositories"
    queryOrAnchor := "q=\"HilbertSymbol\" Lean"
    resultSummary := "total_count=0, incomplete_results=false"
    exactTerminalProofFound := false
    pinImportCheckStatus := "no repository candidate to pin"
    completionGate := "not completion evidence"
  },
  {
    searchName := "github_code_search_authentication_gate"
    primarySource := "GitHub REST search/code"
    queryOrAnchor :=
      "q=\"Hasse-Minkowski\" language:Lean; q=HasseMinkowski language:Lean; q=\"QuadraticForm\" \"Hasse\" language:Lean"
    resultSummary := "GitHub returned 401 Requires authentication; gh auth status reported no logged-in host and GH_TOKEN/GITHUB_TOKEN were unset"
    exactTerminalProofFound := false
    pinImportCheckStatus := "blocked until authenticated code search is rerun"
    completionGate := "blocker, not negative evidence and not completion evidence"
  },
  {
    searchName := "lorentz_workshop_hasse_minkowski_project_report"
    primarySource := "Lean community Lorentz Center workshop project report"
    queryOrAnchor :=
      "Machine-Checked Mathematics formalization projects, July 14 2023, section 2 The Hasse-Minkowski Theorem"
    resultSummary :=
      "project report says the theorem was stated, n=0/n=1 were nearly done, and n=2 was being split into smaller lemmas; no terminal proof or pin-ready repository was identified"
    exactTerminalProofFound := false
    pinImportCheckStatus := "external progress anchor only; no pin/import/check candidate"
    completionGate := "incomplete external-progress anchor, not completion evidence"
  }
]

/-- The C006 external Lean 4 audit records seven search/progress rows. -/
theorem c006ExternalLean4SearchRows_length :
    c006ExternalLean4SearchRows.length = 7 := by
  rfl

/--
C006 external Lean 4 audit result.

This child does not close the terminal Hasse principle or Hasse-Minkowski
theorem.  Its checked contribution is the integration gate: if a future external
Lean 4 proof is found, a completed-state claim first requires a concrete
repository URL, commit, module, theorem name, compatible dependency plan, and a
repo-local `lake env lean` validation through a pinned import or vendored proof.
-/
structure C006ExternalLean4Audit where
  repositorySearchesFoundPinReadyCandidate : Bool
  authenticatedCodeSearchCompleted : Bool
  externalIncompleteProgressAnchorFound : Bool
  terminalHasseMinkowskiProofPinnedImportedChecked : Bool
  terminalHassePrincipleProofPinnedImportedChecked : Bool
  completedStateClaimed : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  decision : String
  blockerSummary : List String

/-- C006 audit result: external search gate recorded, no completion claim. -/
def c006ExternalLean4Audit : C006ExternalLean4Audit where
  repositorySearchesFoundPinReadyCandidate := false
  authenticatedCodeSearchCompleted := false
  externalIncompleteProgressAnchorFound := true
  terminalHasseMinkowskiProofPinnedImportedChecked := false
  terminalHassePrincipleProofPinnedImportedChecked := false
  completedStateClaimed := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  decision :=
    "external_audit_gate_recorded_no_pin_ready_terminal_proof_no_completion_claim"
  blockerSummary := [
    "authenticated GitHub code search must be rerun before treating this audit as exhaustive",
    "the 2023 Lorentz Hasse-Minkowski project report is an incomplete progress anchor, not a terminal proof",
    "no repository URL, commit, module, and theorem-name tuple was available for pin/import/check",
    "if a future external Lean 4 proof is found, it must enter this repository's Lake closure or be blocked with concrete toolchain/dependency/license reasons before any completed-state claim",
    "parent remains formalization_debt/not_repo_local_closed rather than completed repo_local_integration_debt"
  ]

/-- C006 repo-local integration-debt gate: no anchor-only external proof closes the theorem. -/
def c006RepoLocalIntegrationDebtGate : List String := [
  "no external Lean 4 terminal Hasse-Minkowski or generic Hasse-principle proof is pinned, imported, or checked by this child",
  "unauthenticated code-search failure is an integration/audit blocker, not evidence of absence and not completion evidence",
  "the Lorentz Hasse-Minkowski progress report is incomplete external-progress evidence, not a pin-ready terminal theorem",
  "no completed theorem state is claimed, so no completed state retains repo_local_integration_debt"
]

/-! ## C007 scope decision -/

/--
C007 scope decision for the public slot `THM-M-0423`.

The stable theorem target should be the classical Hasse-Minkowski theorem for
finite-dimensional quadratic forms over number fields.  The generic Hasse
principle schema remains useful as statement-normalization infrastructure, but
it is too broad to be a terminal theorem without object-specific hypotheses.
-/
def c007PrimaryScopeDecision : String :=
  "THM-M-0423_primary_scope_is_classical_quadratic_hasse_minkowski"

/--
One C007 branch-disposition row.

Rows are public-backfill guidance, not completed theorem evidence.  Branches
outside the quadratic Hasse-Minkowski theorem must receive separately allocated
theorem IDs before they can be tracked as proof tasks.
-/
structure C007ScopeDispositionRow where
  branchName : String
  recommendedPublicSurface : String
  theoremIdDisposition : String
  repoLocalLeanSurface : String
  completionGate : String

/-- C007 scope-disposition table for the Hasse-principle wording. -/
def c007ScopeDispositionRows : List C007ScopeDispositionRow := [
  {
    branchName := "classical_quadratic_hasse_minkowski"
    recommendedPublicSurface :=
      "retain as THM-M-0423: finite-dimensional quadratic forms over number fields; local isotropy at every finite and infinite completion implies global isotropy"
    theoremIdDisposition := "primary_scope_for_existing_THM-M-0423"
    repoLocalLeanSurface :=
      "ConcreteQuadraticStatementShape and ConcreteQuadraticHasseMinkowskiStatement"
    completionGate :=
      "not complete until concrete local-to-global proof packages are locally proved or pinned/imported/checked"
  },
  {
    branchName := "generic_hasse_principle_schema"
    recommendedPublicSurface :=
      "keep only as normalization infrastructure explaining the local-global template"
    theoremIdDisposition :=
      "not a terminal theorem ID without a selected admissible object class and hypotheses"
    repoLocalLeanSurface := "HassePrincipleDatum and StatementShape"
    completionGate :=
      "schema alone cannot be completed because unrestricted Hasse principles are object-dependent and may fail"
  },
  {
    branchName := "severi_brauer_or_brauer_group_local_global"
    recommendedPublicSurface :=
      "split to a separately allocated theorem ID with explicit central-simple-algebra or Brauer-group hypotheses"
    theoremIdDisposition := "allocate_new_nonquadratic_THM_M_id"
    repoLocalLeanSurface := "no terminal branch in this Stage1 artifact"
    completionGate :=
      "requires exact Lean object model, local invariants, and a repo-local proof or pinned import"
  },
  {
    branchName := "torsor_galois_cohomology_hasse_principles"
    recommendedPublicSurface :=
      "split to a separately allocated theorem ID for each concrete torsor/cohomology theorem"
    theoremIdDisposition := "allocate_new_nonquadratic_THM_M_id"
    repoLocalLeanSurface := "no terminal branch in this Stage1 artifact"
    completionGate :=
      "requires object-specific hypotheses and proof packages before any completion claim"
  },
  {
    branchName := "elliptic_curve_local_global_failures_or_obstructions"
    recommendedPublicSurface :=
      "split to separately allocated theorem IDs, distinguishing true local-global theorems from counterexamples or Brauer-Manin obstruction statements"
    theoremIdDisposition := "allocate_new_nonquadratic_THM_M_id"
    repoLocalLeanSurface := "no terminal branch in this Stage1 artifact"
    completionGate :=
      "requires a precise theorem/counterexample statement and repo-local validation target"
  }
]

/-- The C007 scope split records exactly five branch dispositions. -/
theorem c007ScopeDispositionRows_length :
    c007ScopeDispositionRows.length = 5 := by
  rfl

/--
C007 audit result.

This child makes a scope decision only.  It does not prove Hasse-Minkowski and
does not convert the generic schema into a completed theorem.
-/
structure C007ScopeDecisionAudit where
  primaryScopeIsClassicalQuadraticHasseMinkowski : Bool
  genericSchemaRetainedOnlyAsNormalizationInfrastructure : Bool
  nonQuadraticBranchesRequireSeparateTheoremIds : Bool
  terminalHasseMinkowskiClaimed : Bool
  terminalGenericHassePrincipleClaimed : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  decision : String
  blockerSummary : List String

/-- C007 audit result: scope chosen, non-quadratic branches split, no completion claim. -/
def c007ScopeDecisionAudit : C007ScopeDecisionAudit where
  primaryScopeIsClassicalQuadraticHasseMinkowski := true
  genericSchemaRetainedOnlyAsNormalizationInfrastructure := true
  nonQuadraticBranchesRequireSeparateTheoremIds := true
  terminalHasseMinkowskiClaimed := false
  terminalGenericHassePrincipleClaimed := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  decision :=
    "keep_THM-M-0423_as_classical_quadratic_hasse_minkowski_split_nonquadratic_branches"
  blockerSummary := [
    "the phrase Hasse principle is too broad to be a single terminal Lean theorem without selected object-specific hypotheses",
    "the existing quadratic branch has the strongest repo-local Lean surface through ConcreteQuadraticStatementShape",
    "generic HassePrincipleDatum remains a normalization template and should not be marked completed",
    "Severi-Brauer/Brauer-group, torsor/cohomology, and elliptic-curve obstruction branches need separately allocated theorem IDs",
    "parent remains formalization_debt/not_repo_local_closed until the concrete quadratic Hasse-Minkowski local-to-global proof is proved or pinned/imported/checked"
  ]

/-- C007 repo-local integration-debt gate: no completed theorem state is claimed. -/
def c007RepoLocalIntegrationDebtGate : List String := [
  "C007 records a scope decision, not an external anchor-only terminal proof",
  "no non-quadratic Hasse-principle branch is counted as completed inside THM-M-0423",
  "any future external proof must be pinned, imported, and checked or blocked with concrete integration reasons",
  "no completed theorem state is claimed, so no completed state retains repo_local_integration_debt"
]

/-! ## Audit probes -/

#check NumberField
#check NumberField.FinitePlace
#check NumberField.InfinitePlace
#check NumberField.AdeleRing
#check NumberField.AdeleRing.algebraMap_injective
#check NumberField.prod_abs_eq_one
#check IsNonarchimedeanLocalField
#check QuadraticForm
#check QuadraticForm.baseChange
#check NumberFieldAdeles
#check numberFieldAdeles_algebraMap_injective
#check numberField_productFormula_anchor
#check HasNontrivialZero
#check QuadraticLocalGlobalData.locallySoluble_of_global
#check StatementShape
#check QuadraticStatementShape
#check StatementNormalizationBoundary
#check statementNormalizationBoundary_iff
#check StatementNormalizationAudit
#check c001StatementNormalizationAudit
#check c002MathlibPinnedRevision
#check c002MathlibAnchorModules
#check C002MathlibAnchorRow
#check c002MathlibAnchorRows
#check c002MathlibAnchorRows_length
#check c002RepoLocalIntegrationDebtGate
#check FinitePlaceCompletion
#check InfinitePlaceCompletion
#check QuadraticPlace
#check QuadraticPlace.scalarCompletion
#check QuadraticPlace.localVector
#check QuadraticPlace.localForm
#check QuadraticPlace.localForm_tmul_one
#check ConcreteQuadraticLocallySoluble
#check ConcreteQuadraticHasseMinkowskiStatement
#check ConcreteQuadraticStatementShape
#check C003QuadraticBranchAudit
#check c003QuadraticBranchAudit
#check C004HilbertSymbolPackageRow
#check c004HilbertSymbolPackageRows
#check c004HilbertSymbolPackageRows_length
#check C004HilbertSymbolPackageAudit
#check c004HilbertSymbolPackageAudit
#check c004RepoLocalIntegrationDebtGate
#check QuadraticForm.equivalent_one_zero_neg_one_weighted_sum_squared
#check RealLocalQuadraticClassificationStatement
#check realLocalQuadraticClassification_anchor
#check NonarchimedeanLocalQuadraticClassificationPackage
#check NonarchimedeanLocalQuadraticClassificationStatementShape
#check C005LocalClassificationLeaf
#check c005RealLocalClassificationLeaf
#check c005NonarchimedeanLocalClassificationLeaf
#check c005LocalClassificationLeaves
#check c005LocalClassificationLeaves_length
#check c005LocalClassificationLeaf_budget_gates
#check C005LocalClassificationPackageAudit
#check c005LocalClassificationPackageAudit
#check c005RepoLocalIntegrationDebtGate
#check c006ExternalLean4AuditDate
#check C006ExternalLean4SearchRow
#check c006ExternalLean4SearchRows
#check c006ExternalLean4SearchRows_length
#check C006ExternalLean4Audit
#check c006ExternalLean4Audit
#check c006RepoLocalIntegrationDebtGate
#check c007PrimaryScopeDecision
#check C007ScopeDispositionRow
#check c007ScopeDispositionRows
#check c007ScopeDispositionRows_length
#check C007ScopeDecisionAudit
#check c007ScopeDecisionAudit
#check c007RepoLocalIntegrationDebtGate

end AwesomeTheorems.Stage1.S1_M_067
