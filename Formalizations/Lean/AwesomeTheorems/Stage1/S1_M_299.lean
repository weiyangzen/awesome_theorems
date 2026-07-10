import Mathlib.ModelTheory.Topology.Types
import Mathlib.ModelTheory.ElementaryMaps
import Mathlib.ModelTheory.Skolem

/-!
# S1-M-299 / THM-M-0660: principal formula theorem

This Stage1 artifact records a conservative Lean 4 boundary for the model
theoretic theorem described in the Stage1 queue as the existence of principal
formulas in stable theories.

The pinned mathlib snapshot already provides first-order languages, formulas,
sentences, theories, semantic entailment, satisfiability/compactness, complete
types, realized types, elementary maps, Skolem functions, and the Stone-style
topology on complete type spaces.  This audit did not locate a terminal
definition of stable theory, forking/rank machinery, principal formulas, or the
principal formula theorem itself.

The declarations below therefore normalize the formal boundary: a principal
formula is represented as a formula whose basic clopen in the complete-type
space is a singleton, and child task `S1-M-299-C003` selects a conservative
type-counting stability boundary over the locally available complete-type
space.  This is not yet the full source theorem's parameter/model stability
API.  The file proves only low-risk wrappers around available mathlib anchors.
-/

noncomputable section

open Set FirstOrder Cardinal
open scoped FirstOrder Cardinal

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_299

universe u v w

namespace PrincipalFormula

variable {L : FirstOrder.Language.{u, v}} {α : Type w}

/--
A formula is consistent with a theory when it is realized by some tuple in some
nonempty model of the theory.
-/
def FormulaConsistentWith (T : L.Theory) (φ : L.Formula α) : Prop :=
  ∃ (M : Type (max u v w)) (_ : L.Structure M) (_ : Nonempty M) (_ : M ⊨ T),
    ∃ x : α → M, φ.Realize x

/--
Semantic refinement of formulas over a theory: every model of `T` satisfying
`ψ` also satisfies `φ`.
-/
def FormulaRefines (T : L.Theory) (ψ φ : L.Formula α) : Prop :=
  T ⊨ᵇ ψ.imp φ

/--
The basic type-space clopen determined by a formula, using mathlib's
`Formula.equivSentence` bridge from formulas with variables to sentences in the
language expanded by constants for those variables.
-/
def TypeBasicOpen (T : L.Theory) (φ : L.Formula α) :
    Set (FirstOrder.Language.Theory.CompleteType T α) :=
  FirstOrder.Language.Theory.CompleteType.typesWith
    (T := T) (FirstOrder.Language.Formula.equivSentence φ)

/-- A formula isolates a complete type when its basic clopen is that singleton. -/
def IsolatesCompleteType (T : L.Theory) (φ : L.Formula α)
    (p : FirstOrder.Language.Theory.CompleteType T α) : Prop :=
  TypeBasicOpen T φ = {p}

/-- A principal formula is a formula isolating some complete type. -/
def IsPrincipalFormula (T : L.Theory) (φ : L.Formula α) : Prop :=
  ∃ p : FirstOrder.Language.Theory.CompleteType T α, IsolatesCompleteType T φ p

/-
The C004 child keeps singleton isolation in the complete-type space as the
repo-local principal-formula convention.  This is the standard Stone-space
form of a formula isolating a complete type; no distinct source-specific Lean
notion has been identified in the checked local substrate.
-/
inductive PrincipalDefinitionChoice where
  | singletonClopenTypeIsolation
  | sourceSpecificAlternative

/-- The C004 child selects singleton-clopen isolation of complete types. -/
def selectedPrincipalDefinitionChoice : PrincipalDefinitionChoice :=
  PrincipalDefinitionChoice.singletonClopenTypeIsolation

/-- Checked witness for the C004 principal-definition decision. -/
theorem selectedPrincipalDefinitionChoice_eq_singletonClopenTypeIsolation :
    selectedPrincipalDefinitionChoice =
      PrincipalDefinitionChoice.singletonClopenTypeIsolation :=
  rfl

/--
The selected principal-formula definition is definitionally the assertion that
the formula's basic complete-type open is a singleton.
-/
theorem isPrincipalFormula_iff_exists_singleton_typeBasicOpen {T : L.Theory}
    {φ : L.Formula α} :
    IsPrincipalFormula T φ ↔
      ∃ p : FirstOrder.Language.Theory.CompleteType T α, TypeBasicOpen T φ = {p} :=
  Iff.rfl

/--
The normalized local conclusion expected from a principal-formula theorem:
every consistent input formula has a consistent principal refinement.
-/
def PrincipalFormulaExistenceConclusion (T : L.Theory) : Prop :=
  ∀ φ : L.Formula α,
    FormulaConsistentWith T φ →
      ∃ ψ : L.Formula α,
        IsPrincipalFormula T ψ ∧ FormulaRefines T ψ φ ∧ FormulaConsistentWith T ψ

/-! ## Stability-definition boundary selected by child task `S1-M-299-C003`. -/

inductive StabilityDefinitionChoice where
  | typeCounting
  | noOrderProperty
  | forkingOrRank
  | exactSourceCompatible

/--
The C003 child selects the type-counting convention as the repo-local formal
stability boundary, because the checked mathlib closure already has complete
type spaces and cardinal infrastructure but no no-order-property, forking, rank,
or terminal stable-theory API.
-/
def selectedStabilityDefinitionChoice : StabilityDefinitionChoice :=
  StabilityDefinitionChoice.typeCounting

/-- Checked witness for the C003 stability-definition decision. -/
theorem selectedStabilityDefinitionChoice_eq_typeCounting :
    selectedStabilityDefinitionChoice = StabilityDefinitionChoice.typeCounting :=
  rfl

/--
Type-counting stability at the current Stage1 boundary: the complete type space
for the chosen variable index type `α` has cardinal at most the selected bound
`κ`.

This deliberately records only the type-space/cardinal convention available in
the local mathlib substrate.  It does not yet quantify over all parameter sets
or all models of a fixed cardinal, and it should not be read as a completed
Lean formalization of classical stability theory.
-/
def TypeCountingStableAt (T : L.Theory) (α : Type w) (κ : Cardinal.{max u v w}) :
    Prop :=
  Cardinal.lift #(FirstOrder.Language.Theory.CompleteType T α) ≤ κ

/-! ## Parameter-scope boundary selected by child task `S1-M-299-C005`. -/

/-- A countable first-order language, expressed using mathlib's symbol type. -/
def CountableLanguage (L : FirstOrder.Language.{u, v}) : Prop :=
  Countable L.Symbols

/--
The finite-tuple, type-counting form of omega-stability used by this Stage1
boundary: for every finite tuple arity, the complete-type space is countable.
-/
def OmegaStableTypeCounting (T : L.Theory) : Prop :=
  ∀ n : ℕ, TypeCountingStableAt T (Fin n) ℵ₀

/--
The current artifact keeps parameters out of the core theorem statement.  A
parameterized version must first expand the language by named constants and
then re-check countability and omega-stability for that expanded language.
-/
def CountableNamedParameterExpansion (L : FirstOrder.Language.{u, v}) (A : Type w) : Prop :=
  Countable (L[[A]].Symbols)

inductive ParameterScopeChoice where
  | finiteTuplesOverEmptyTheory
  | countableNamedConstantsExpansion
  | arbitraryParameterSet
  | monsterModelParameters

inductive StabilityStrengthChoice where
  | omegaStableTypeCounting
  | arbitraryStableOnly
  | totalTranscendence
  | finiteRank

inductive ModelAmbientChoice where
  | noSaturationOrMonster
  | saturatedModel
  | monsterModel

/--
The C005 child selects the parameter-free finite-tuple core statement.  This is
the strongest safe local choice because the checked substrate has formulas,
complete types, and language expansions by constants, but no monster-model or
saturation API.
-/
def selectedParameterScopeChoice : ParameterScopeChoice :=
  ParameterScopeChoice.finiteTuplesOverEmptyTheory

/--
The C005 child selects omega-stability as a finite-tuple countability condition,
not arbitrary stability, total transcendence, or finite rank.
-/
def selectedStabilityStrengthChoice : StabilityStrengthChoice :=
  StabilityStrengthChoice.omegaStableTypeCounting

/-- The C005 child does not add saturation or monster-model assumptions. -/
def selectedModelAmbientChoice : ModelAmbientChoice :=
  ModelAmbientChoice.noSaturationOrMonster

theorem selectedParameterScopeChoice_eq_finiteTuplesOverEmptyTheory :
    selectedParameterScopeChoice =
      ParameterScopeChoice.finiteTuplesOverEmptyTheory :=
  rfl

theorem selectedStabilityStrengthChoice_eq_omegaStableTypeCounting :
    selectedStabilityStrengthChoice =
      StabilityStrengthChoice.omegaStableTypeCounting :=
  rfl

theorem selectedModelAmbientChoice_eq_noSaturationOrMonster :
    selectedModelAmbientChoice =
      ModelAmbientChoice.noSaturationOrMonster :=
  rfl

/--
Explicit side-condition package for the selected C005 theorem boundary.

It records that the local statement is for a complete theory in a countable
language, finite tuple variables, and omega-stability by finite-tuple type
counting.  It deliberately does not assume total transcendence, finite rank,
saturation, or a monster model.
-/
structure ParameterScopeData (L : FirstOrder.Language.{u, v}) (T : L.Theory)
    (α : Type w) where
  countableLanguage : CountableLanguage L
  omegaStable : OmegaStableTypeCounting T
  finiteTupleVariables : ∃ n : ℕ, Nonempty (α ≃ Fin n)
  noTotalTranscendenceAssumption : True
  noFiniteRankAssumption : True
  noSaturationAssumption : True
  noMonsterModelAssumption : True

/--
Stage1 data for the stable-theory principal-formula slot using the selected
type-counting stability boundary.

The C005 parameter-scope child strengthens the earlier statement-shape data
with an explicit finite-tuple/countable-language/omega-stability side-condition
package.  Parameterized versions are intentionally left to a later named
constant expansion and re-validation step.
-/
structure StablePrincipalFormulaData (L : FirstOrder.Language.{u, v}) (α : Type w) where
  theory : L.Theory
  complete : theory.IsComplete
  typeBound : Cardinal.{max u v w}
  stable : TypeCountingStableAt theory α typeBound
  parameterScope : ParameterScopeData L theory α

/--
Stage1 normalized statement-shape candidate: under the chosen complete stable
theory hypotheses, every consistent formula has a consistent principal
refinement.
-/
def StatementShape : Prop :=
  ∀ (L : FirstOrder.Language.{u, v}) (α : Type w),
    ∀ D : StablePrincipalFormulaData L α,
      PrincipalFormulaExistenceConclusion (L := L) (α := α) D.theory

/-- The statement shape unfolds to the explicit principal-refinement statement. -/
theorem statementShape_iff :
    StatementShape.{u, v, w} ↔
      ∀ (L : FirstOrder.Language.{u, v}) (α : Type w),
        ∀ D : StablePrincipalFormulaData L α,
          PrincipalFormulaExistenceConclusion (L := L) (α := α) D.theory :=
  Iff.rfl

/-- Project the complete-theory hypothesis from the normalized data. -/
theorem complete_of_data (D : StablePrincipalFormulaData L α) :
    D.theory.IsComplete :=
  D.complete

/-- Project the selected type-counting stability hypothesis from the normalized data. -/
theorem stable_of_data (D : StablePrincipalFormulaData L α) :
    TypeCountingStableAt D.theory α D.typeBound :=
  D.stable

/-- Project the explicit C005 parameter-scope side-condition package. -/
theorem parameterScope_of_data (D : StablePrincipalFormulaData L α) :
    ParameterScopeData L D.theory α :=
  D.parameterScope

/-- Project the countable-language hypothesis selected by C005. -/
theorem countableLanguage_of_data (D : StablePrincipalFormulaData L α) :
    CountableLanguage L :=
  D.parameterScope.countableLanguage

/-- Project the omega-stability hypothesis selected by C005. -/
theorem omegaStable_of_data (D : StablePrincipalFormulaData L α) :
    OmegaStableTypeCounting D.theory :=
  D.parameterScope.omegaStable

/-- Project the finite-tuple variable scope selected by C005. -/
theorem finiteTupleVariables_of_data (D : StablePrincipalFormulaData L α) :
    ∃ n : ℕ, Nonempty (α ≃ Fin n) :=
  D.parameterScope.finiteTupleVariables

/-- A principal formula exposes a type that it isolates. -/
theorem exists_isolated_type_of_principal {T : L.Theory} {φ : L.Formula α}
    (h : IsPrincipalFormula T φ) :
    ∃ p : FirstOrder.Language.Theory.CompleteType T α, IsolatesCompleteType T φ p :=
  h

/-- If a formula isolates `p`, then the corresponding basic open contains `p`. -/
theorem mem_typeBasicOpen_of_isolates {T : L.Theory} {φ : L.Formula α}
    {p : FirstOrder.Language.Theory.CompleteType T α}
    (h : IsolatesCompleteType T φ p) :
    p ∈ TypeBasicOpen T φ := by
  rw [h]
  exact mem_singleton p

/-- If a formula isolates `p`, then its sentence-with-constants belongs to `p`. -/
theorem formula_mem_of_isolates {T : L.Theory} {φ : L.Formula α}
    {p : FirstOrder.Language.Theory.CompleteType T α}
    (h : IsolatesCompleteType T φ p) :
    FirstOrder.Language.Formula.equivSentence φ ∈ p := by
  simpa [TypeBasicOpen] using mem_typeBasicOpen_of_isolates (T := T) (φ := φ) (p := p) h

/-- The mathlib type-space basic open determined by any formula is clopen. -/
theorem isClopen_typeBasicOpen (T : L.Theory) (φ : L.Formula α) :
    IsClopen (TypeBasicOpen T φ) :=
  CompleteType.isClopen_typesWith (FirstOrder.Language.Formula.equivSentence φ)

/--
A principal formula therefore determines a singleton clopen subset of the
complete-type space.
-/
theorem exists_singleton_clopen_typeBasicOpen_of_principal {T : L.Theory}
    {φ : L.Formula α} (h : IsPrincipalFormula T φ) :
    ∃ p : FirstOrder.Language.Theory.CompleteType T α,
      TypeBasicOpen T φ = {p} ∧ IsClopen (TypeBasicOpen T φ) := by
  rcases (isPrincipalFormula_iff_exists_singleton_typeBasicOpen.mp h) with ⟨p, hp⟩
  exact ⟨p, hp, isClopen_typeBasicOpen T φ⟩

/-- Checked semantic-use wrapper for formula refinement. -/
theorem FormulaRefines.realize {T : L.Theory} {ψ φ : L.Formula α}
    (h : FormulaRefines T ψ φ) (M : Type*) [L.Structure M] [M ⊨ T] [Nonempty M]
    {v : α → M} : ψ.Realize v → φ.Realize v := by
  intro hψ
  have hImp : (ψ.imp φ).Realize v :=
    FirstOrder.Language.Theory.ModelsBoundedFormula.realize_formula h M
  exact (FirstOrder.Language.Formula.realize_imp.mp hImp) hψ

/-- mathlib compactness anchor as a local wrapper. -/
theorem satisfiable_iff_finitely_satisfiable (T : L.Theory) :
    T.IsSatisfiable ↔ T.IsFinitelySatisfiable :=
  FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable

/-- mathlib complete-type nonemptiness anchor as a local wrapper. -/
theorem completeType_nonempty_iff_satisfiable (T : L.Theory) :
    Nonempty (FirstOrder.Language.Theory.CompleteType T α) ↔ T.IsSatisfiable :=
  FirstOrder.Language.Theory.CompleteType.nonempty_iff

/-- mathlib type-of anchor: a realized tuple has a complete type over `T`. -/
theorem formula_mem_typeOf_iff {T : L.Theory} {M : Type*} [L.Structure M]
    [Nonempty M] [M ⊨ T] {v : α → M} {φ : L.Formula α} :
    FirstOrder.Language.Formula.equivSentence φ ∈ T.typeOf v ↔ φ.Realize v :=
  FirstOrder.Language.Theory.CompleteType.formula_mem_typeOf

/-! ## Audit probes retained in the checked file. -/

#check FirstOrder.Language
#check FirstOrder.Language.Formula
#check FirstOrder.Language.Sentence
#check FirstOrder.Language.Theory
#check FirstOrder.Language.Theory.ModelsBoundedFormula
#check FirstOrder.Language.Theory.IsSatisfiable
#check FirstOrder.Language.Theory.IsFinitelySatisfiable
#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#check FirstOrder.Language.Theory.IsComplete
#check FirstOrder.Language.Theory.CompleteType
#check FirstOrder.Language.Theory.CompleteType.nonempty_iff
#check FirstOrder.Language.Theory.CompleteType.typesWith
#check FirstOrder.Language.Theory.CompleteType.formula_mem_typeOf
#check FirstOrder.Language.Theory.exists_modelType_is_realized_in
#check FirstOrder.Language.Theory.realizedTypes
#check FirstOrder.Language.Formula.equivSentence
#check FirstOrder.Language.Formula.realize_imp
#check CompleteType.isClopen_typesWith
#check FirstOrder.Language.ElementaryEmbedding
#check FirstOrder.Language.skolem₁
#check StabilityDefinitionChoice
#check selectedStabilityDefinitionChoice
#check selectedStabilityDefinitionChoice_eq_typeCounting
#check TypeCountingStableAt
#check CountableLanguage
#check OmegaStableTypeCounting
#check CountableNamedParameterExpansion
#check ParameterScopeData
#check selectedParameterScopeChoice
#check selectedParameterScopeChoice_eq_finiteTuplesOverEmptyTheory
#check selectedStabilityStrengthChoice
#check selectedStabilityStrengthChoice_eq_omegaStableTypeCounting
#check selectedModelAmbientChoice
#check selectedModelAmbientChoice_eq_noSaturationOrMonster
#check PrincipalDefinitionChoice
#check selectedPrincipalDefinitionChoice
#check selectedPrincipalDefinitionChoice_eq_singletonClopenTypeIsolation
#check isPrincipalFormula_iff_exists_singleton_typeBasicOpen
#check exists_singleton_clopen_typeBasicOpen_of_principal

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.ModelTheory.Syntax",
  "Mathlib.ModelTheory.Semantics",
  "Mathlib.ModelTheory.Satisfiability",
  "Mathlib.ModelTheory.Types",
  "Mathlib.ModelTheory.Topology.Types",
  "Mathlib.ModelTheory.ElementaryMaps",
  "Mathlib.ModelTheory.ElementarySubstructures",
  "Mathlib.ModelTheory.Skolem",
  "Mathlib.ModelTheory.Encoding",
  "Mathlib.ModelTheory.Complexity"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "FirstOrder.Language",
  "FirstOrder.Language.Formula",
  "FirstOrder.Language.Sentence",
  "FirstOrder.Language.Theory",
  "FirstOrder.Language.Formula.equivSentence",
  "FirstOrder.Language.Formula.Realize",
  "FirstOrder.Language.Theory.ModelsBoundedFormula",
  "FirstOrder.Language.Theory.IsSatisfiable",
  "FirstOrder.Language.Theory.IsFinitelySatisfiable",
  "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable",
  "FirstOrder.Language.Theory.IsComplete",
  "FirstOrder.Language.Theory.CompleteType",
  "FirstOrder.Language.Theory.CompleteType.nonempty_iff",
  "FirstOrder.Language.Theory.CompleteType.typesWith",
  "FirstOrder.Language.Theory.CompleteType.formula_mem_typeOf",
  "FirstOrder.Language.Theory.exists_modelType_is_realized_in",
  "FirstOrder.Language.Theory.realizedTypes",
  "CompleteType.isClopen_typesWith",
  "FirstOrder.Language.ElementaryEmbedding",
  "FirstOrder.Language.skolem₁"
]

/-- Exact checked anchor list requested by child task `S1-M-299-C002`. -/
def childC002CheckedAnchorNames : List String := [
  "FirstOrder.Language.Formula.equivSentence",
  "FirstOrder.Language.Theory.ModelsBoundedFormula",
  "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable",
  "FirstOrder.Language.Theory.CompleteType",
  "FirstOrder.Language.Theory.CompleteType.typesWith",
  "FirstOrder.Language.Theory.CompleteType.nonempty_iff",
  "FirstOrder.Language.Theory.CompleteType.formula_mem_typeOf",
  "CompleteType.isClopen_typesWith"
]

/-- Exact stability-definition decision recorded by child task `S1-M-299-C003`. -/
def childC003StabilityDefinitionDecision : List String := [
  "selected_definition: type-counting",
  "checked_handle: TypeCountingStableAt",
  "cardinal_bound: Cardinal.lift #(FirstOrder.Language.Theory.CompleteType T α) ≤ κ",
  "reason: local mathlib has CompleteType/type-space/cardinal anchors but no stable-theory, no-order-property, forking, or rank API",
  "scope_guard: parameter/model-scope stability remains open under S1-M-299.parameter-scope"
]

/-- Exact principal-definition decision recorded by child task `S1-M-299-C004`. -/
def childC004PrincipalDefinitionDecision : List String := [
  "selected_definition: singleton-clopen isolation of complete types",
  "checked_handle: IsPrincipalFormula",
  "equivalence: isPrincipalFormula_iff_exists_singleton_typeBasicOpen",
  "clopen_wrapper: exists_singleton_clopen_typeBasicOpen_of_principal",
  "reason: local mathlib has complete type spaces, basic clopens, and formula-to-sentence constants; no distinct source-specific principal-formula API was identified",
  "scope_guard: this is a statement-boundary decision, not a proof of principal-formula existence from stability"
]

/-- Exact parameter-scope decision recorded by child task `S1-M-299-C005`. -/
def childC005ParameterScopeDecision : List String := [
  "selected_parameter_scope: finite tuple formulas over the empty theory language",
  "parameterized_variant: only via named-constant language expansion, with countability rechecked",
  "countability: required as CountableLanguage L",
  "stability_strength: omega-stability encoded as OmegaStableTypeCounting T",
  "omega_stability_handle: ∀ n : ℕ, TypeCountingStableAt T (Fin n) ℵ₀",
  "finite_variables: required as ∃ n : ℕ, Nonempty (α ≃ Fin n)",
  "total_transcendence: not added as an independent local assumption",
  "finite_rank: not added as an independent local assumption",
  "saturation: not added",
  "monster_model: not added",
  "checked_side_condition_package: ParameterScopeData"
]

/-- Search terms used by child task `S1-M-299-C006` for the external-audit pass. -/
def childC006ExternalAuditSearchTerms : List String := [
  "StableTheory language:Lean",
  "\"stable theory\" language:Lean",
  "\"order property\" \"FirstOrder\" language:Lean",
  "forking \"FirstOrder\" language:Lean",
  "\"Morley rank\" language:Lean",
  "\"principal formula\" \"model theory\" language:Lean",
  "PrincipalFormula language:Lean",
  "\"isolated type\" CompleteType language:Lean",
  "\"FirstOrder.Language.Theory.CompleteType\" Stable language:Lean",
  "\"Mathlib.ModelTheory\" \"stable\" language:Lean"
]

/--
Result of child task `S1-M-299-C006`.

The requested authenticated GitHub Code Search could not be completed in this
worker environment because no GitHub credentials were available.  The retained
local artifact therefore records a concrete integration blocker rather than
treating anchor-only evidence as theorem completion.
-/
def childC006AuthenticatedGitHubCodeSearchResult : List String := [
  "requested_channel: authenticated GitHub Code Search",
  "local_auth_status: blocked; gh auth status reports no logged-in GitHub hosts",
  "token_env_status: GH_TOKEN, GITHUB_TOKEN, and GITHUB_PAT were unset",
  "gh_probe: gh search code 'StableTheory language:Lean' --limit 20 returned exit code 4 and requested gh auth login or GH_TOKEN",
  "rest_probe: unauthenticated GitHub REST code search returned HTTP 403 rate-limit output and is not a substitute for authenticated code search",
  "fallback_local_mathlib_revision: 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "fallback_local_mathlib_result: pinned mathlib has CompleteType, typesWith, formula-to-sentence, satisfiability, elementary-map, and Skolem anchors but no terminal stable-theory or principal-formula theorem",
  "pin_import_check_status: no external terminal Lean 4 theorem was identified, so no external dependency was pinned, imported, or checked",
  "integration_blocker: rerun with gh auth login or GH_TOKEN available; if a terminal theorem is found, pin/import/check it or record a dependency/toolchain/license blocker",
  "status: external-audit remains open; parent remains formalization_debt and not_repo_local_closed"
]

/-- No completed state is claimed by child task `S1-M-299-C006`. -/
def childC006RepoLocalIntegrationDebtGate : String :=
  "pass_for_noncompletion: no external theorem is claimed completed, no anchor-only evidence is promoted, and no completed state retains repo_local_integration_debt"

/-! ## Public-status gate retained by child task `S1-M-299-C007`. -/

/--
Repo-local closure statuses accepted by the Stage1 public-status gate for
THM-M-0660.

Anchor-only external evidence is represented explicitly so the audit can reject
it as a completion state under the M0387-level integration-debt rule.
-/
inductive RepoLocalClosureStatus where
  | notRepoLocalClosed
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  deriving DecidableEq, Repr

/-- Closure statuses that may support a public Stage1 checkmark. -/
def RepoLocalClosureStatus.isCompletionStatus :
    RepoLocalClosureStatus -> Bool
  | RepoLocalClosureStatus.localProofBody => true
  | RepoLocalClosureStatus.localWrapperUpstreamMathlib => true
  | RepoLocalClosureStatus.externalUpstreamPinned => true
  | RepoLocalClosureStatus.notRepoLocalClosed => false
  | RepoLocalClosureStatus.externalUpstreamAnchorOnly => false

/--
Machine-readable public-status gate for S1-M-299.

The redundant booleans are intentional: the serial public-doc integrator can
inspect the checked artifact without inferring from prose whether the public
checkbox may close.
-/
structure PublicStatusGateReport where
  currentStatus : RepoLocalClosureStatus
  localProofBodyValidated : Bool
  localWrapperOverPinnedMathlibValidated : Bool
  pinnedExternalProofValidated : Bool
  publicTheoremTreeAndLedgerMerged : Bool
  anchorOnlyEvidenceCountedAsCompletion : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  publicStage1CheckboxMayClose : Bool
  rationale : List String
  deriving Repr, DecidableEq

/-- Predicate strong enough to permit public completion for this Stage1 slot. -/
def PublicStatusGateReport.allowsCompletion (R : PublicStatusGateReport) : Prop :=
  R.publicStage1CheckboxMayClose = true /\
    R.currentStatus.isCompletionStatus = true /\
    (R.localProofBodyValidated = true \/
      R.localWrapperOverPinnedMathlibValidated = true \/
      R.pinnedExternalProofValidated = true) /\
    R.publicTheoremTreeAndLedgerMerged = true /\
    R.anchorOnlyEvidenceCountedAsCompletion = false /\
    R.completedStateRetainsRepoLocalIntegrationDebt = false

/--
Current C007 public-status gate.

The local file validates statement-shape, type-space, stability-boundary,
parameter-scope, principal-definition, and external-audit-blocker metadata
only.  No local proof body, mathlib wrapper, or pinned external proof validates
the terminal principal-formula theorem, and the public theorem tree/ledger have
not been merged by a serial integrator.
-/
def childC007PublicStatusGate : PublicStatusGateReport where
  currentStatus := RepoLocalClosureStatus.notRepoLocalClosed
  localProofBodyValidated := false
  localWrapperOverPinnedMathlibValidated := false
  pinnedExternalProofValidated := false
  publicTheoremTreeAndLedgerMerged := false
  anchorOnlyEvidenceCountedAsCompletion := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  publicStage1CheckboxMayClose := false
  rationale := [
    "statement-shape and local mathlib-anchor wrappers compile, but no terminal principal-formula theorem proof body is present",
    "no mathlib theorem at revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 has been wrapped as the terminal theorem",
    "no external Lean 4 proof dependency has been pinned/imported/checked in this Lake closure",
    "C006 authenticated GitHub Code Search is still blocked by missing credentials and cannot support completion",
    "public theorem tree and ledger merge-back is reserved for a serial integrator",
    "anchor-only evidence is not counted as completion and no completed state retains repo_local_integration_debt"
  ]

/-- The current C007 public-status gate is not repo-local closed. -/
theorem childC007PublicStatusGate_status :
    childC007PublicStatusGate.currentStatus =
      RepoLocalClosureStatus.notRepoLocalClosed :=
  rfl

/-- The public Stage1 checkbox must remain open in the current repo-local state. -/
theorem childC007PublicStatusGate_checkbox_open :
    childC007PublicStatusGate.publicStage1CheckboxMayClose = false :=
  rfl

/-- C007 records no completed-state repo-local integration debt. -/
theorem childC007PublicStatusGate_no_completed_repo_local_integration_debt :
    childC007PublicStatusGate.completedStateRetainsRepoLocalIntegrationDebt =
      false :=
  rfl

/-- C007 records that anchor-only evidence is not counted as completion. -/
theorem childC007PublicStatusGate_no_anchor_only_completion :
    childC007PublicStatusGate.anchorOnlyEvidenceCountedAsCompletion = false :=
  rfl

/-- The current report cannot satisfy the public-completion predicate. -/
theorem childC007PublicStatusGate_not_allowsCompletion :
    Not childC007PublicStatusGate.allowsCompletion := by
  intro h
  exact Bool.false_ne_true h.1

#check childC006ExternalAuditSearchTerms
#check childC006AuthenticatedGitHubCodeSearchResult
#check childC006RepoLocalIntegrationDebtGate
#check RepoLocalClosureStatus
#check PublicStatusGateReport
#check childC007PublicStatusGate
#check childC007PublicStatusGate_not_allowsCompletion

/-- Search terms that did not locate a terminal principal-formula theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "stable theory",
  "StableTheory",
  "Stability",
  "forking",
  "Morley rank",
  "principal formula",
  "PrincipalFormula",
  "isolated type",
  "isolates complete type",
  "main formula theorem",
  "principal formula theorem"
]

end PrincipalFormula

end S1_M_299
end Stage1
end AwesomeTheorems
