import Mathlib.ModelTheory.Satisfiability
import Mathlib.ModelTheory.Types
import Mathlib.ModelTheory.Encoding
import Mathlib.ModelTheory.Ultraproducts
import Mathlib.ModelTheory.Skolem
import Mathlib.ModelTheory.ElementarySubstructures
import Mathlib.ModelTheory.ElementaryMaps

/-!
# S1-M-300 / THM-M-0674: Existence of saturated models

This Stage1 artifact records a conservative Lean 4 boundary for the model
theoretic existence theorem for saturated models.  The pinned mathlib snapshot
contains first-order syntax, semantics, compactness, complete types, realized
types, ultraproduct semantics, and Loewenheim-Skolem style cardinal wrappers.
No terminal saturated-model existence theorem was located in the local
dependency closure.

The file therefore defines a precise statement shape around parameter
expansions and realization of complete types whose tuple-index type and
parameter set both have cardinality below the target cardinal.  It proves only
low-risk wrappers around existing mathlib definitions and theorems, with no
proof placeholders or custom logical postulates.
-/

noncomputable section

open Cardinal FirstOrder

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_300

universe u v wM wA wK

variable {L : FirstOrder.Language.{u, v}} {M : Type wM} [L.Structure M] [Nonempty M]

/--
The complete theory of the expansion of `M` by constants naming the image of a
parameter map `a : A -> M`.

This is a mathlib-native way to represent a type over a parameter set: after
adding constants for the parameter indices, complete tuple types are complete
types over this expanded complete theory.
-/
def ParameterTheory {A : Type wA} (a : A -> M) : L[[A]].Theory :=
  letI : (FirstOrder.Language.constantsOn A).Structure M :=
    FirstOrder.Language.constantsOn.structure a
  L[[A]].completeTheory M

omit [Nonempty M] in
/-- The original expanded structure models its own complete parameter theory. -/
theorem parameterTheory_model {A : Type wA} (a : A -> M) :
    letI : (FirstOrder.Language.constantsOn A).Structure M :=
      FirstOrder.Language.constantsOn.structure a
    M ⊨ ParameterTheory (L := L) a := by
  dsimp [ParameterTheory]
  infer_instance

/-- The parameter theory is complete, because it is a complete theory of a structure. -/
theorem parameterTheory_isComplete {A : Type wA} (a : A -> M) :
    (ParameterTheory (L := L) a).IsComplete := by
  letI : (FirstOrder.Language.constantsOn A).Structure M :=
    FirstOrder.Language.constantsOn.structure a
  exact FirstOrder.Language.completeTheory.isComplete L[[A]] M

/--
A complete type over a named parameter set is realized in the same expanded
structure by some tuple assignment of the given index type.
-/
def RealizesTypeOver {A : Type wA} (a : A -> M) {ι : Type wK}
    (p : (ParameterTheory (L := L) a).CompleteType ι) : Prop :=
  letI : (FirstOrder.Language.constantsOn A).Structure M :=
    FirstOrder.Language.constantsOn.structure a
  haveI : M ⊨ ParameterTheory (L := L) a := parameterTheory_model (L := L) a
  p ∈ (ParameterTheory (L := L) a).realizedTypes M ι

/--
A complete unary type over a named parameter set is realized in the same
expanded structure.
-/
def RealizesUnaryTypeOver {A : Type wA} (a : A -> M)
    (p : (ParameterTheory (L := L) a).CompleteType PUnit.{wK + 1}) : Prop :=
  RealizesTypeOver (L := L) a p

/-- The cardinal smallness predicate for parameter maps used by the Stage1 boundary. -/
def SmallParameterMap (κ : Cardinal.{wK}) {A : Type wK} (_a : A -> M) : Prop :=
  #A < κ

/-- The cardinal smallness predicate for tuple-index types used by the Stage1 boundary. -/
def SmallTupleIndex (κ : Cardinal.{wK}) (ι : Type wK) : Prop :=
  #ι < κ

/--
The concrete cardinal-arithmetic side condition used for the Stage1 saturated
model existence boundary.

For the selected convention, the target model realizes all complete types whose
parameter set and tuple-index type both have cardinality `< κ`.  The standard
safe cardinal-arithmetic hypothesis for the construction is therefore
`κ ^< κ = κ`: the supremum of `κ ^ μ` over all `μ < κ` is still `κ`.
-/
def KappaClosedUnderSmallPowers (κ : Cardinal.{wK}) : Prop :=
  κ ^< κ = κ

/-- The cardinal-arithmetic side condition is exactly `κ ^< κ = κ`. -/
theorem KappaClosedUnderSmallPowers_iff {κ : Cardinal.{wK}} :
    KappaClosedUnderSmallPowers κ ↔ κ ^< κ = κ :=
  Iff.rfl

/-- Public saturation conventions considered by the Stage1 statement-shape task. -/
inductive SaturationConvention where
  | unaryTypesOverParameterSets
  | finiteTupleTypesOverParameterSets
  | smallTupleTypesOverParameterSets
deriving Repr, DecidableEq

/--
The public convention selected for this Stage1 slot: realization of all
complete tuple types whose tuple-index type has cardinality `< κ`, over all
parameter sets of cardinality `< κ`.
-/
def chosenSaturationConvention : SaturationConvention :=
  .smallTupleTypesOverParameterSets

/-- The selected convention is the strongest of the three public options. -/
theorem chosenSaturationConvention_eq :
    chosenSaturationConvention =
      SaturationConvention.smallTupleTypesOverParameterSets :=
  rfl

/--
Full `<κ`-tuple `κ`-saturation boundary for the current Stage1 artifact: every
complete type whose tuple-index type has cardinality below `κ`, over every
parameter set of cardinality below `κ`, is realized.

This is deliberately a statement boundary, not a proof of saturation.
-/
def IsKappaTupleSaturatedAt (κ : Cardinal.{wK}) : Prop :=
  ∀ {A : Type wK} (a : A -> M),
    SmallParameterMap (M := M) κ a ->
      ∀ {ι : Type wK},
        SmallTupleIndex κ ι ->
          ∀ p : (ParameterTheory (L := L) a).CompleteType ι,
            RealizesTypeOver (L := L) a p

/--
Unary `κ`-saturation boundary retained as a weaker comparison convention:
every complete unary type over every parameter set of cardinality below `κ` is
realized.
-/
def IsUnarySaturatedAt (κ : Cardinal.{wK}) : Prop :=
  ∀ {A : Type wK} (a : A -> M),
    SmallParameterMap (M := M) κ a ->
      ∀ p : (ParameterTheory (L := L) a).CompleteType PUnit.{wK + 1},
        RealizesUnaryTypeOver (L := L) a p

/--
The chosen `<κ`-tuple convention specializes to the unary convention whenever
the singleton tuple index is `< κ`.
-/
theorem tupleSaturatedAt_implies_unarySaturatedAt {κ : Cardinal.{wK}}
    (h : IsKappaTupleSaturatedAt (L := L) (M := M) κ)
    (hUnit : SmallTupleIndex κ PUnit.{wK + 1}) :
    IsUnarySaturatedAt (L := L) (M := M) κ := by
  intro A a ha p
  exact h a ha hUnit p

/-- Assumptions normally needed before a saturated-model existence statement can be attempted. -/
structure SaturatedModelExistenceHypotheses (L : FirstOrder.Language.{u, v})
    (T : L.Theory) (κ : Cardinal.{wK}) : Type (max (max (u + 1) (v + 1)) (wK + 1)) where
  satisfiable : T.IsSatisfiable
  infiniteCardinal : ℵ₀ ≤ κ
  languageCardinal_le :
    Cardinal.lift.{wK} L.card ≤ Cardinal.lift.{max u v} κ
  smallPowerClosure : KappaClosedUnderSmallPowers κ

/--
Candidate output package for a saturated model of `T`.

The exact cardinality field records the usual target form.  The saturation
field uses the public convention chosen for this Stage1 slot: realization of
all complete `<κ`-indexed tuple types over parameter sets of size `<κ`.
-/
structure SaturatedModelPackage (L : FirstOrder.Language.{u, v}) (T : L.Theory)
    (κ : Cardinal.{wK}) : Type (max (max (u + 1) (v + 1)) (wK + 1)) where
  Carrier : Type wK
  struc : L.Structure Carrier
  nonempty : Nonempty Carrier
  modelTheory : Carrier ⊨ T
  cardinality : #Carrier = κ
  tupleSaturated :
    letI : L.Structure Carrier := struc
    letI : Nonempty Carrier := nonempty
    IsKappaTupleSaturatedAt (L := L) (M := Carrier) κ

attribute [instance] SaturatedModelPackage.struc SaturatedModelPackage.nonempty

/--
Stage1 normalized statement-shape candidate for saturated model existence.

It says that under satisfiability, size, and cardinal-arithmetic side
condition `κ ^< κ = κ`, there is a model of `T` of cardinality `κ` realizing
every complete type whose tuple-index type and parameter set both have
cardinality `< κ`.
-/
def StatementShape : Prop :=
  ∀ (L : FirstOrder.Language.{u, v}) (T : L.Theory) (κ : Cardinal.{wK}),
    SaturatedModelExistenceHypotheses L T κ ->
      Nonempty (SaturatedModelPackage L T κ)

/-- The statement shape unfolds to the explicit saturated-model package form. -/
theorem statementShape_iff :
    StatementShape.{u, v, wK} ↔
      ∀ (L : FirstOrder.Language.{u, v}) (T : L.Theory) (κ : Cardinal.{wK}),
        SaturatedModelExistenceHypotheses L T κ ->
          Nonempty (SaturatedModelPackage L T κ) :=
  Iff.rfl

/--
Apply the normalized Stage1 statement shape to concrete theorem data.

This wrapper is intentionally only an eliminator for the statement boundary; it
does not prove the saturated-model existence theorem.
-/
theorem statementShape_apply (h : StatementShape.{u, v, wK})
    (L : FirstOrder.Language.{u, v}) (T : L.Theory) (κ : Cardinal.{wK})
    (H : SaturatedModelExistenceHypotheses L T κ) :
    Nonempty (SaturatedModelPackage L T κ) :=
  h L T κ H

/-- Project the satisfiability hypothesis from normalized existence data. -/
theorem hypotheses_satisfiable {T : L.Theory} {κ : Cardinal.{wK}}
    (H : SaturatedModelExistenceHypotheses L T κ) :
    T.IsSatisfiable :=
  H.satisfiable

/-- Project the language-cardinality hypothesis from normalized existence data. -/
theorem hypotheses_languageCardinal_le {T : L.Theory} {κ : Cardinal.{wK}}
    (H : SaturatedModelExistenceHypotheses L T κ) :
    Cardinal.lift.{wK} L.card ≤ Cardinal.lift.{max u v} κ :=
  H.languageCardinal_le

/-- Project the concrete cardinal-arithmetic closure hypothesis from normalized existence data. -/
theorem hypotheses_smallPowerClosure {T : L.Theory} {κ : Cardinal.{wK}}
    (H : SaturatedModelExistenceHypotheses L T κ) :
    KappaClosedUnderSmallPowers κ :=
  H.smallPowerClosure

/-- Project the model-of-`T` field from the saturated-model package. -/
theorem package_models {T : L.Theory} {κ : Cardinal.{wK}}
    (P : SaturatedModelPackage L T κ) :
    P.Carrier ⊨ T :=
  P.modelTheory

/-- Project the exact-cardinality field from the saturated-model package. -/
theorem package_cardinality {T : L.Theory} {κ : Cardinal.{wK}}
    (P : SaturatedModelPackage L T κ) :
    #P.Carrier = κ :=
  P.cardinality

/-- Project the `<κ`-tuple saturation boundary from the saturated-model package. -/
theorem package_tupleSaturated {T : L.Theory} {κ : Cardinal.{wK}}
    (P : SaturatedModelPackage L T κ) :
    letI : L.Structure P.Carrier := P.struc
    letI : Nonempty P.Carrier := P.nonempty
    IsKappaTupleSaturatedAt (L := L) (M := P.Carrier) κ :=
  P.tupleSaturated

/--
Mathlib wrapper: any complete type is realized in some model of its base
theory.  This is not saturation of a fixed model, but it is a key local anchor
for the future construction.
-/
theorem completeType_exists_model_realizing {T : L.Theory} {α : Type wA}
    (p : T.CompleteType α) :
    ∃ N : FirstOrder.Language.Theory.ModelType.{u, v, max u v wA} T,
      p ∈ T.realizedTypes N α :=
  FirstOrder.Language.Theory.exists_modelType_is_realized_in T p

/-! ## Audit probes retained in the checked file. -/

#check FirstOrder.Language.Term.realize
#check FirstOrder.Language.BoundedFormula.Realize
#check FirstOrder.Language.Formula.Realize
#check FirstOrder.Language.Theory.ModelsBoundedFormula
#check FirstOrder.Language.Theory.IsSatisfiable
#check FirstOrder.Language.Theory.IsFinitelySatisfiable
#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#check FirstOrder.Language.Theory.models_iff_finset_models
#check FirstOrder.Language.Theory.exists_large_model_of_infinite_model
#check FirstOrder.Language.exists_elementaryEmbedding_card_eq
#check FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge
#check FirstOrder.Language.Theory.exists_model_card_eq
#check FirstOrder.Language.Theory.CompleteType
#check FirstOrder.Language.Theory.realizedTypes
#check FirstOrder.Language.Theory.exists_modelType_is_realized_in
#check FirstOrder.Language.Ultraproduct.sentence_realize
#check FirstOrder.Language.completeTheory.isComplete
#check FirstOrder.Language.Term.card_le
#check FirstOrder.Language.BoundedFormula.card_le
#check FirstOrder.Language.skolem₁
#check FirstOrder.Language.exists_elementarySubstructure_card_eq
#check FirstOrder.Language.Substructure.IsElementary
#check FirstOrder.Language.ElementarySubstructure
#check FirstOrder.Language.ElementarySubstructure.subtype
#check FirstOrder.Language.ElementarySubstructure.theory_model_iff
#check FirstOrder.Language.ElementaryEmbedding
#check FirstOrder.Language.elementaryDiagram
#check FirstOrder.Language.Embedding.isElementary_of_exists

/-- mathlib modules audited for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.ModelTheory.Syntax",
  "Mathlib.ModelTheory.Semantics",
  "Mathlib.ModelTheory.Satisfiability",
  "Mathlib.ModelTheory.Types",
  "Mathlib.ModelTheory.Encoding",
  "Mathlib.ModelTheory.Skolem",
  "Mathlib.ModelTheory.ElementarySubstructures",
  "Mathlib.ModelTheory.ElementaryMaps",
  "Mathlib.ModelTheory.Ultraproducts"
]

/-- Local mathlib revision pinned by `Formalizations/Lean/lake-manifest.json`. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- One row in the pinned mathlib anchor table for this Stage1 slot. -/
structure MathlibAnchorRow where
  moduleName : String
  mathlibRevision : String
  checkedDeclarations : List String
  role : String
  status : String
deriving Repr

/--
Pinned mathlib anchor table for the saturated-model-existence boundary.

Every row is tied to the local mathlib dependency revision recorded in
`mathlibPinnedRevision`; the declarations listed here are also represented by
checked `#check` probes above.  None of these rows is a terminal proof of
saturated-model existence.
-/
def mathlibAnchorTable : List MathlibAnchorRow := [
  {
    moduleName := "Mathlib.ModelTheory.Satisfiability",
    mathlibRevision := mathlibPinnedRevision,
    checkedDeclarations := [
      "FirstOrder.Language.Theory.IsSatisfiable",
      "FirstOrder.Language.Theory.IsFinitelySatisfiable",
      "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable",
      "FirstOrder.Language.Theory.exists_large_model_of_infinite_model",
      "FirstOrder.Language.exists_elementaryEmbedding_card_eq",
      "FirstOrder.Language.Theory.exists_model_card_eq",
      "FirstOrder.Language.Theory.ModelsBoundedFormula"
    ],
    role := "compactness, satisfiability, complete theories, and Loewenheim-Skolem cardinal wrappers",
    status := "repo-local imported and declaration-probed; no saturated-model existence theorem found"
  },
  {
    moduleName := "Mathlib.ModelTheory.Types",
    mathlibRevision := mathlibPinnedRevision,
    checkedDeclarations := [
      "FirstOrder.Language.Theory.CompleteType",
      "FirstOrder.Language.Theory.realizedTypes",
      "FirstOrder.Language.Theory.exists_modelType_is_realized_in"
    ],
    role := "complete type and realized-type API used by the `<κ`-tuple saturation statement boundary",
    status := "repo-local imported and declaration-probed; supplies type-space anchors only"
  },
  {
    moduleName := "Mathlib.ModelTheory.Encoding",
    mathlibRevision := mathlibPinnedRevision,
    checkedDeclarations := [
      "FirstOrder.Language.Term.card_le",
      "FirstOrder.Language.BoundedFormula.card_le"
    ],
    role := "syntax-cardinality estimates for future cardinal-control leaves",
    status := "repo-local imported and declaration-probed; cardinal-control support only"
  },
  {
    moduleName := "Mathlib.ModelTheory.Ultraproducts",
    mathlibRevision := mathlibPinnedRevision,
    checkedDeclarations := [
      "FirstOrder.Language.Ultraproduct.sentence_realize"
    ],
    role := "Los theorem anchor used by compactness and satisfiability infrastructure",
    status := "repo-local imported and declaration-probed; not a saturation construction"
  },
  {
    moduleName := "Mathlib.ModelTheory.Skolem",
    mathlibRevision := mathlibPinnedRevision,
    checkedDeclarations := [
      "FirstOrder.Language.skolem₁",
      "FirstOrder.Language.exists_elementarySubstructure_card_eq"
    ],
    role := "Skolemization and downward Loewenheim-Skolem elementary-substructure construction",
    status := "repo-local imported and declaration-probed; construction support only"
  },
  {
    moduleName := "Mathlib.ModelTheory.ElementarySubstructures",
    mathlibRevision := mathlibPinnedRevision,
    checkedDeclarations := [
      "FirstOrder.Language.Substructure.IsElementary",
      "FirstOrder.Language.ElementarySubstructure",
      "FirstOrder.Language.ElementarySubstructure.subtype",
      "FirstOrder.Language.ElementarySubstructure.theory_model_iff"
    ],
    role := "elementary-substructure boundary and model-preservation API",
    status := "repo-local imported and declaration-probed; no elementary-chain saturation theorem found"
  },
  {
    moduleName := "Mathlib.ModelTheory.ElementaryMaps",
    mathlibRevision := mathlibPinnedRevision,
    checkedDeclarations := [
      "FirstOrder.Language.ElementaryEmbedding",
      "FirstOrder.Language.elementaryDiagram",
      "FirstOrder.Language.Embedding.isElementary_of_exists"
    ],
    role := "elementary embeddings, elementary diagrams, and Tarski-Vaught test anchors",
    status := "repo-local imported and declaration-probed; embedding support only"
  }
]

/-- The required child-task anchor table has exactly the seven requested module rows. -/
theorem mathlibAnchorTable_length : mathlibAnchorTable.length = 7 :=
  rfl

/-- Pinned mathlib declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "FirstOrder.Language.Term.realize",
  "FirstOrder.Language.BoundedFormula.Realize",
  "FirstOrder.Language.Formula.Realize",
  "FirstOrder.Language.Theory.ModelsBoundedFormula",
  "FirstOrder.Language.Theory.IsSatisfiable",
  "FirstOrder.Language.Theory.IsFinitelySatisfiable",
  "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable",
  "FirstOrder.Language.Theory.models_iff_finset_models",
  "FirstOrder.Language.Theory.exists_large_model_of_infinite_model",
  "FirstOrder.Language.exists_elementaryEmbedding_card_eq",
  "FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge",
  "FirstOrder.Language.Theory.exists_model_card_eq",
  "FirstOrder.Language.Theory.CompleteType",
  "FirstOrder.Language.Theory.realizedTypes",
  "FirstOrder.Language.Theory.exists_modelType_is_realized_in",
  "FirstOrder.Language.Ultraproduct.sentence_realize",
  "FirstOrder.Language.completeTheory.isComplete",
  "FirstOrder.Language.Term.card_le",
  "FirstOrder.Language.BoundedFormula.card_le",
  "FirstOrder.Language.skolem₁",
  "FirstOrder.Language.exists_elementarySubstructure_card_eq",
  "FirstOrder.Language.Substructure.IsElementary",
  "FirstOrder.Language.ElementarySubstructure",
  "FirstOrder.Language.ElementarySubstructure.subtype",
  "FirstOrder.Language.ElementarySubstructure.theory_model_iff",
  "FirstOrder.Language.ElementaryEmbedding",
  "FirstOrder.Language.elementaryDiagram",
  "FirstOrder.Language.Embedding.isElementary_of_exists"
]

/-- Search terms that did not locate a terminal saturated-model existence theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "saturated model",
  "saturated_model",
  "SaturatedModel",
  "IsSaturated",
  "saturat",
  "realizes all types",
  "existence of saturated",
  "model existence saturated",
  "omega saturated",
  "κ-saturated"
]

/-- Exact child-task search terms for the primary-source Lean 4 code audit. -/
def requiredPrimarySourceSearchTerms : List String := [
  "SaturatedModel",
  "IsSaturated",
  "saturated model",
  "CompleteType",
  "realizedTypes",
  "Henkin",
  "elementary chain"
]

/-- One row in the Stage1 primary-source code-search audit. -/
structure PrimarySourceCodeSearchRow where
  repository : String
  commit : String
  searchTerms : List String
  declarationsOrTheoremNames : List String
  placeholderStatus : String
deriving Repr

/--
Primary-source code-search audit rows for the saturated-model-existence slot.

The mathlib row is repo-local and pinned by `lake-manifest.json`; its
declarations are represented by checked probes above.  The external GitHub row
is deliberately marked as a blocker because this worker had no authenticated
GitHub code-search session (`gh` was not logged in and no `GH_TOKEN` was
available).  The `gh api search/code` probe exited before an authenticated
search could be issued.  Therefore this audit does not close the external-proof
gate.
-/
def primarySourceCodeSearchAudit : List PrimarySourceCodeSearchRow := [
  {
    repository := "leanprover-community/mathlib4",
    commit := mathlibPinnedRevision,
    searchTerms := requiredPrimarySourceSearchTerms,
    declarationsOrTheoremNames := [
      "FirstOrder.Language.Theory.CompleteType",
      "FirstOrder.Language.Theory.CompleteType.isMaximal",
      "FirstOrder.Language.Theory.CompleteType.subset",
      "FirstOrder.Language.Theory.CompleteType.mem_or_not_mem",
      "FirstOrder.Language.Theory.CompleteType.mem_of_models",
      "FirstOrder.Language.Theory.CompleteType.not_mem_iff",
      "FirstOrder.Language.Theory.CompleteType.setOf_subset_eq_empty_iff",
      "FirstOrder.Language.Theory.CompleteType.setOf_mem_eq_univ_iff",
      "FirstOrder.Language.Theory.CompleteType.nonempty_iff",
      "FirstOrder.Language.Theory.CompleteType.typesWith",
      "FirstOrder.Language.Theory.CompleteType.mem_typesWith_iff",
      "FirstOrder.Language.Theory.CompleteType.typesWith_inf",
      "FirstOrder.Language.Theory.CompleteType.formula_mem_typeOf",
      "FirstOrder.Language.Theory.realizedTypes",
      "FirstOrder.Language.Theory.exists_modelType_is_realized_in",
      "CompleteType.isTopologicalBasis_range_typesWith",
      "CompleteType.isOpen_typesWith",
      "CompleteType.isClosed_typesWith",
      "CompleteType.isClopen_typesWith",
      "FirstOrder.Language.exists_elementaryEmbedding_card_eq",
      "FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge",
      "FirstOrder.Language.exists_elementarySubstructure_card_eq"
    ],
    placeholderStatus :=
      "repo-local pinned mathlib source searched; type and elementary-embedding anchors found, but no SaturatedModel/IsSaturated/Henkin/elementary-chain terminal saturated-model existence theorem"
  },
  {
    repository := "external public Lean 4 repositories via GitHub code search",
    commit := "blocked before repository commits could be authenticated",
    searchTerms := requiredPrimarySourceSearchTerms,
    declarationsOrTheoremNames := [],
    placeholderStatus :=
      "blocked: gh auth status reported no logged-in GitHub host and GH_TOKEN/GITHUB_TOKEN were absent; gh api search/code exited before an authenticated search could be issued, so no external proof may be claimed"
  }
]

/-- Proof packages used by the Stage1 theorem-tree expansion. -/
inductive ProofPackage where
  | statementNormalization
  | mathlibAnchorAudit
  | compactness
  | oneStepTypeRealization
  | elementaryChain
  | cardinalControl
  | finalSaturation
  | repoLocalClosureGate
deriving Repr, DecidableEq

/-- Audit status for an individual theorem-tree leaf. -/
inductive ProofLeafStatus where
  | checkedLocalWrapper
  | checkedStatementShape
  | uncheckedFormalizationDebt
  | blockedExternalSearch
deriving Repr, DecidableEq

/-- One independent `<=100` Stage1 theorem-tree leaf for the saturated-model slot. -/
structure ProofLeaf where
  leafId : String
  package : ProofPackage
  target : String
  budgetSteps : Nat
  status : ProofLeafStatus
deriving Repr, DecidableEq

/--
Independent theorem-tree leaves for the saturated-model existence proof plan.

The list separates compactness, one-step type realization, elementary-chain
construction, cardinal control, and final saturation.  The checked entries are
only statement-shape or mathlib-wrapper leaves already present in this file;
the construction leaves remain explicit formalization debt.
-/
def saturatedModelProofLeaves : List ProofLeaf := [
  {
    leafId := "M0674-L001",
    package := .statementNormalization,
    target := "Define ParameterTheory as the complete theory of the expansion by named parameters.",
    budgetSteps := 20,
    status := .checkedStatementShape
  },
  {
    leafId := "M0674-L002",
    package := .statementNormalization,
    target := "Prove the expanded structure models its own ParameterTheory.",
    budgetSteps := 10,
    status := .checkedLocalWrapper
  },
  {
    leafId := "M0674-L003",
    package := .statementNormalization,
    target := "Prove ParameterTheory is complete.",
    budgetSteps := 10,
    status := .checkedLocalWrapper
  },
  {
    leafId := "M0674-L004",
    package := .statementNormalization,
    target := "Define type realization over named parameters using CompleteType and realizedTypes.",
    budgetSteps := 20,
    status := .checkedStatementShape
  },
  {
    leafId := "M0674-L005",
    package := .statementNormalization,
    target := "Define SmallParameterMap, SmallTupleIndex, and the chosen <kappa tuple saturation predicate.",
    budgetSteps := 25,
    status := .checkedStatementShape
  },
  {
    leafId := "M0674-L006",
    package := .cardinalControl,
    target := "Expose KappaClosedUnderSmallPowers as the concrete kappa ^< kappa = kappa side condition.",
    budgetSteps := 20,
    status := .checkedStatementShape
  },
  {
    leafId := "M0674-L007",
    package := .statementNormalization,
    target := "Define the saturated-model output package and StatementShape boundary.",
    budgetSteps := 30,
    status := .checkedStatementShape
  },
  {
    leafId := "M0674-L008",
    package := .mathlibAnchorAudit,
    target := "Wrap exists_modelType_is_realized_in for complete types realized in some model.",
    budgetSteps := 15,
    status := .checkedLocalWrapper
  },
  {
    leafId := "M0674-L009",
    package := .compactness,
    target := "Pin the compactness root through isSatisfiable_iff_isFinitelySatisfiable and models_iff_finset_models.",
    budgetSteps := 60,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L010",
    package := .compactness,
    target := "Convert finite satisfiability of the type-realization diagram into a model realizing the next type.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L011",
    package := .oneStepTypeRealization,
    target := "Encode one complete type over a small parameter map as a diagram extension of the current model.",
    budgetSteps := 90,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L012",
    package := .oneStepTypeRealization,
    target := "Build an elementary extension realizing one selected small tuple type.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L013",
    package := .oneStepTypeRealization,
    target := "Package the one-step extension so the original model embeds elementarily into the extension.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L014",
    package := .elementaryChain,
    target := "Enumerate all small parameter maps and small tuple types using the kappa-closure hypothesis.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L015",
    package := .elementaryChain,
    target := "Construct the successor stage by applying the one-step realization package to the next enumerated type.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L016",
    package := .elementaryChain,
    target := "Construct limit stages as elementary unions or direct limits of the previous chain.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L017",
    package := .elementaryChain,
    target := "Prove each transition map in the chain is elementary and preserves the theory T.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L018",
    package := .cardinalControl,
    target := "Bound the number of complete small tuple types over all small parameter sets by kappa.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L019",
    package := .cardinalControl,
    target := "Prove successor-stage cardinality remains at most kappa.",
    budgetSteps := 90,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L020",
    package := .cardinalControl,
    target := "Prove the elementary-chain union has cardinality exactly kappa.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L021",
    package := .finalSaturation,
    target := "Show every small parameter map into the final model factors through some chain stage.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L022",
    package := .finalSaturation,
    target := "Show every small complete tuple type appears in the construction schedule.",
    budgetSteps := 90,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L023",
    package := .finalSaturation,
    target := "Transport realization from the scheduled stage to the final elementary union.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L024",
    package := .finalSaturation,
    target := "Assemble modelhood, exact cardinality, and <kappa tuple saturation into SaturatedModelPackage.",
    budgetSteps := 100,
    status := .uncheckedFormalizationDebt
  },
  {
    leafId := "M0674-L025",
    package := .repoLocalClosureGate,
    target := "Replace the statement boundary by a local proof or pinned external wrapper before any completion claim.",
    budgetSteps := 80,
    status := .blockedExternalSearch
  }
]

/-- The theorem-tree expansion currently has 25 independent leaves. -/
theorem saturatedModelProofLeaves_length : saturatedModelProofLeaves.length = 25 :=
  rfl

/-- Every current theorem-tree leaf is budgeted at `<= 100` proof steps. -/
theorem saturatedModelProofLeaves_budget_le_100 :
    saturatedModelProofLeaves.all (fun leaf => leaf.budgetSteps <= 100) := by
  decide

/-- The proof tree explicitly contains a compactness leaf package. -/
theorem saturatedModelProofLeaves_has_compactness :
    ∃ leaf ∈ saturatedModelProofLeaves, leaf.package = ProofPackage.compactness := by
  refine ⟨saturatedModelProofLeaves[8], ?_, ?_⟩
  · decide
  · rfl

/-- The proof tree explicitly contains a one-step type-realization package. -/
theorem saturatedModelProofLeaves_has_oneStep :
    ∃ leaf ∈ saturatedModelProofLeaves, leaf.package = ProofPackage.oneStepTypeRealization := by
  refine ⟨saturatedModelProofLeaves[10], ?_, ?_⟩
  · decide
  · rfl

/-- The proof tree explicitly contains an elementary-chain construction package. -/
theorem saturatedModelProofLeaves_has_chain :
    ∃ leaf ∈ saturatedModelProofLeaves, leaf.package = ProofPackage.elementaryChain := by
  refine ⟨saturatedModelProofLeaves[13], ?_, ?_⟩
  · decide
  · rfl

/-- The proof tree explicitly contains a cardinal-control package. -/
theorem saturatedModelProofLeaves_has_cardinalControl :
    ∃ leaf ∈ saturatedModelProofLeaves, leaf.package = ProofPackage.cardinalControl := by
  refine ⟨saturatedModelProofLeaves[5], ?_, ?_⟩
  · decide
  · rfl

/-- The proof tree explicitly contains a final-saturation package. -/
theorem saturatedModelProofLeaves_has_finalSaturation :
    ∃ leaf ∈ saturatedModelProofLeaves, leaf.package = ProofPackage.finalSaturation := by
  refine ⟨saturatedModelProofLeaves[20], ?_, ?_⟩
  · decide
  · rfl

/-- Package-level audit rows for the construction leaves required by child `S1-M-300-E007`. -/
structure ConstructionPackageAuditRow where
  package : ProofPackage
  leafIds : List String
  constructionRole : String
  locallyClosed : Bool
deriving Repr, DecidableEq

/--
The five construction packages requested for the saturated-model theorem tree.

Each row points back to independent leaves in `saturatedModelProofLeaves`.  The
`locallyClosed` field is false for every row because this file only records a
checked statement boundary and audit tree, not the terminal saturated-model
existence proof.
-/
def constructionPackageAuditRows : List ConstructionPackageAuditRow := [
  {
    package := .compactness,
    leafIds := ["M0674-L009", "M0674-L010"],
    constructionRole :=
      "Use compactness to turn finite satisfiability of the type-realization diagram into a model.",
    locallyClosed := false
  },
  {
    package := .oneStepTypeRealization,
    leafIds := ["M0674-L011", "M0674-L012", "M0674-L013"],
    constructionRole :=
      "Adjoin one selected small complete tuple type and produce an elementary extension realizing it.",
    locallyClosed := false
  },
  {
    package := .elementaryChain,
    leafIds := ["M0674-L014", "M0674-L015", "M0674-L016", "M0674-L017"],
    constructionRole :=
      "Schedule all small type obligations and build successor and limit stages of the elementary chain.",
    locallyClosed := false
  },
  {
    package := .cardinalControl,
    leafIds := ["M0674-L018", "M0674-L019", "M0674-L020"],
    constructionRole :=
      "Use the kappa-closure side condition to bound scheduled types, successor stages, and the final union.",
    locallyClosed := false
  },
  {
    package := .finalSaturation,
    leafIds := ["M0674-L021", "M0674-L022", "M0674-L023", "M0674-L024"],
    constructionRole :=
      "Factor parameters through a stage, locate the scheduled type, transport realization, and assemble the package.",
    locallyClosed := false
  }
]

/-- The E007 package audit has exactly the five requested construction packages. -/
theorem constructionPackageAuditRows_length :
    constructionPackageAuditRows.length = 5 :=
  rfl

/-- No construction package is locally closed by this statement-boundary artifact. -/
theorem constructionPackageAuditRows_none_locallyClosed :
    constructionPackageAuditRows.all (fun row => row.locallyClosed = false) := by
  decide

/-- Count of locally checked statement-shape or wrapper leaves in the current tree. -/
theorem saturatedModelProofLeaves_checked_count :
    (saturatedModelProofLeaves.filter
      (fun leaf =>
        leaf.status = ProofLeafStatus.checkedLocalWrapper ||
          leaf.status = ProofLeafStatus.checkedStatementShape)).length = 8 := by
  decide

/-- Count of open formalization-debt construction leaves in the current tree. -/
theorem saturatedModelProofLeaves_uncheckedFormalizationDebt_count :
    (saturatedModelProofLeaves.filter
      (fun leaf => leaf.status = ProofLeafStatus.uncheckedFormalizationDebt)).length = 16 := by
  decide

/-- Count of external-search-blocked closure-gate leaves in the current tree. -/
theorem saturatedModelProofLeaves_blockedExternalSearch_count :
    (saturatedModelProofLeaves.filter
      (fun leaf => leaf.status = ProofLeafStatus.blockedExternalSearch)).length = 1 := by
  decide

/-- E007 completion gate: a tree audit is checked, but the theorem is not complete. -/
structure E007CompletionGate where
  theoremTreeExpanded : Bool
  leafBudgetsChecked : Bool
  terminalProofIntegratedAndChecked : Bool
  theoremCompletionClaimed : Bool
deriving Repr, DecidableEq

/-- Current completion gate values for child `S1-M-300-E007`. -/
def e007CompletionGate : E007CompletionGate where
  theoremTreeExpanded := true
  leafBudgetsChecked := true
  terminalProofIntegratedAndChecked := false
  theoremCompletionClaimed := false

/-- The E007 audit expands the tree but does not integrate a terminal proof. -/
theorem e007CompletionGate_no_terminalProof :
    e007CompletionGate.terminalProofIntegratedAndChecked = false :=
  rfl

/-- The E007 audit does not claim theorem completion. -/
theorem e007CompletionGate_no_completionClaim :
    e007CompletionGate.theoremCompletionClaimed = false :=
  rfl

/-- Primary-source pin for the local mathlib proof body baseline. -/
def mathlibPrimarySourceRevision : String :=
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Repo-local integration gate state for the external-proof child task.

This separates two facts required by the M0387 standard: the local Lake
dependency closure contains no terminal saturated-model existence theorem, and
the broader external Lean 4 search is still blocked before a repository commit
or theorem name can be authenticated.  Therefore no pinned dependency or
vendored proof body is added by this Stage1 child.
-/
inductive ExternalProofGateState where
  | noLocalTerminalProof
  | externalSearchBlocked
  | terminalProofFoundNeedsIntegration
  | integratedAndChecked
deriving Repr, DecidableEq

/-- Current external-proof integration gate states for this Stage1 slot. -/
def externalProofGateStates : List ExternalProofGateState := [
  .noLocalTerminalProof,
  .externalSearchBlocked
]

/--
The current gate is explicitly not an integrated-and-checked external proof.
This prevents the audit metadata from being read as a completion claim.
-/
theorem externalProofGateStates_not_integrated :
    ExternalProofGateState.integratedAndChecked ∉ externalProofGateStates :=
  by decide

end S1_M_300
end Stage1
end AwesomeTheorems
