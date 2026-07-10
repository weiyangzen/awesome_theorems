import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.FieldTheory.AlgebraicClosure
import Mathlib.NumberTheory.Height.Basic

/-!
# S1-M-010 / THM-M-0397: Baker's method

This Stage1 artifact records a conservative Lean 4 statement boundary for the
use of Baker-type lower bounds for linear forms in logarithms to obtain
effective finite-search bounds for Diophantine equations.

The current local artifact does not claim a kernel-checked proof of Baker's
method.  The declarations below freeze the theorem-internal data shape and
record audit constants for the future mathlib/external-anchor pass.
-/

noncomputable section

open scoped BigOperators

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_010

/--
Substrate package for the linear forms in logarithms used by a Baker-method
argument.

The logarithms are represented by arbitrary complex choices `lambda i` with
`Complex.exp (lambda i) = alpha i`; this keeps the method-level statement from
committing to a principal-branch encoding.
-/
structure LinearFormsLogInput where
  n : ℕ
  alpha : Fin n → ℂ
  lambda : Fin n → ℂ
  coeff : Fin n → ℤ
  alpha_nonzero : ∀ i, alpha i ≠ 0
  alpha_algebraic : ∀ i, IsAlgebraic ℚ (alpha i)
  exp_lambda_eq_alpha : ∀ i, Complex.exp (lambda i) = alpha i

/-- The complex linear form `Λ = Σ b_i λ_i` used in the Baker-method reduction. -/
def linearForm (L : LinearFormsLogInput) : ℂ :=
  ∑ i : Fin L.n, (L.coeff i : ℂ) * L.lambda i

/--
Input data for a Baker-method proof package.

`Solution` is the chosen formal solution space for the Diophantine problem,
`height` is the complexity measure to be bounded, `solutionPredicate` selects
the actual solutions, and `effectiveSearchBound` is the computable bound that
would make the solution set finite-searchable.

The remaining fields isolate the two mathematical promises normally supplied by
Baker's method: a lower bound for the relevant nonzero linear forms in
logarithms, and a reduction from that analytic inequality to the finite bound
on all Diophantine solutions.
-/
structure BakerMethodData : Type (u + 1) where
  Solution : Type u
  logInput : LinearFormsLogInput
  height : Solution → Nat
  solutionPredicate : Solution → Prop
  effectiveSearchBound : Nat
  linearFormCertificate : Type u
  hasBakerLowerBound : Prop
  hasReductionToFiniteSearch : Prop
  allSolutionsBounded : Prop

/--
The theorem-internal implication shape for a Baker-method argument.

This is intentionally a statement-shape predicate, not a proof that Baker's
theorem has been formalized in this repository.
-/
def HasBakerMethodBound (D : BakerMethodData.{u}) : Prop :=
  D.hasBakerLowerBound → D.hasReductionToFiniteSearch → D.allSolutionsBounded

/--
Concrete finite-search conclusion used by later refinements: every selected
solution has height at most the effective bound.
-/
def HasExplicitSolutionBound (D : BakerMethodData.{u}) : Prop :=
  ∀ x : D.Solution, D.solutionPredicate x → D.height x ≤ D.effectiveSearchBound

/--
The three public statement-normalization branches for THM-M-0397.

This is a branch index for the blueprint target, not a proof-status enum.
-/
inductive NormalizationBranch where
  | linearFormsInLogarithms
  | effectiveDiophantineBridge
  | scopedToyBranch
  deriving DecidableEq

/--
Metadata for a deliberately scoped toy branch.

Toy branches are allowed only as finite-search interfaces that still pass
through the log-linear-form object model; they are not substitutes for an
unproven Baker lower-bound theorem.
-/
structure ScopedToyBranch where
  branchName : String
  modelPredicate : Prop
  usesLogLinearForm : Prop
  hasFiniteSearchInterface : Prop

/-- Statement-normalization target for the linear-forms-in-logarithms branch. -/
def LinearFormsInLogarithmsTarget (D : BakerMethodData.{u}) : Prop :=
  D.hasBakerLowerBound

/--
Statement-normalization target for the effective Diophantine bridge branch.

The bridge is kept separate from the lower-bound oracle: it records the
problem-specific reduction and the conversion from an abstract boundedness
claim to the explicit finite-search height bound.
-/
def EffectiveDiophantineBridgeTarget (D : BakerMethodData.{u}) : Prop :=
  D.hasReductionToFiniteSearch ∧ (D.allSolutionsBounded → HasExplicitSolutionBound D)

/--
Statement-normalization target for a scoped toy branch.

Each toy branch must name its model, assert that it really uses the log-linear
form substrate, and expose a finite-search interface.
-/
def ScopedToyBranchTarget (D : BakerMethodData.{u}) (T : ScopedToyBranch) : Prop :=
  T.modelPredicate ∧ T.usesLogLinearForm ∧ T.hasFiniteSearchInterface ∧
    EffectiveDiophantineBridgeTarget D

/-- Branch-indexed statement target used by the public THM-M-0397 backfill. -/
def normalizedBranchTarget
    (D : BakerMethodData.{u}) (toyBranches : List ScopedToyBranch) :
    NormalizationBranch → Prop
  | .linearFormsInLogarithms => LinearFormsInLogarithmsTarget D
  | .effectiveDiophantineBridge => EffectiveDiophantineBridgeTarget D
  | .scopedToyBranch => ∀ T, T ∈ toyBranches → ScopedToyBranchTarget D T

/--
Complete statement-normalization package for THM-M-0397.

This is the repo-local Lean counterpart of the public subsection that should be
merged later by an integrator.
-/
def StatementNormalization
    (D : BakerMethodData.{u}) (toyBranches : List ScopedToyBranch) : Prop :=
  LinearFormsInLogarithmsTarget D ∧
    EffectiveDiophantineBridgeTarget D ∧
      ∀ T, T ∈ toyBranches → ScopedToyBranchTarget D T

/-- The normalized package is exactly the three requested branch targets. -/
theorem statementNormalization_iff
    (D : BakerMethodData.{u}) (toyBranches : List ScopedToyBranch) :
    StatementNormalization D toyBranches ↔
      LinearFormsInLogarithmsTarget D ∧
        EffectiveDiophantineBridgeTarget D ∧
          ∀ T, T ∈ toyBranches → ScopedToyBranchTarget D T :=
  Iff.rfl

/-- Projection for the normalized linear-forms-in-logarithms target. -/
theorem linearFormsTarget_of_statementNormalization
    (D : BakerMethodData.{u}) (toyBranches : List ScopedToyBranch)
    (h : StatementNormalization D toyBranches) :
    LinearFormsInLogarithmsTarget D :=
  h.1

/-- Projection for the normalized effective Diophantine bridge target. -/
theorem effectiveBridgeTarget_of_statementNormalization
    (D : BakerMethodData.{u}) (toyBranches : List ScopedToyBranch)
    (h : StatementNormalization D toyBranches) :
    EffectiveDiophantineBridgeTarget D :=
  h.2.1

/-- Projection for each normalized scoped toy branch target. -/
theorem scopedToyTarget_of_statementNormalization
    (D : BakerMethodData.{u}) (toyBranches : List ScopedToyBranch)
    (h : StatementNormalization D toyBranches)
    (T : ScopedToyBranch) (hT : T ∈ toyBranches) :
    ScopedToyBranchTarget D T :=
  h.2.2 T hT

/-! ## Reusable theorem-family decomposition -/

/--
Canonical reusable packages for a Baker-method application proof.

These are proof-family nodes for later M0387-level expansion.  They are not a
claim that the corresponding mathematical packages have already been proved in
this repository.
-/
inductive BakerMethodPackage where
  | logLinearSubstrate
  | linearFormAssembly
  | lowerBoundInterface
  | diophantineReduction
  | boundednessConclusion
  | explicitBoundExtraction
  | finiteSearchClosure
  deriving DecidableEq

/-- Package-local target attached to each reusable Baker-method node. -/
def BakerMethodPackageTarget (D : BakerMethodData.{u}) :
    BakerMethodPackage → Prop
  | .logLinearSubstrate =>
      ∀ i : Fin D.logInput.n,
        D.logInput.alpha i ≠ 0 ∧
          IsAlgebraic ℚ (D.logInput.alpha i) ∧
            Complex.exp (D.logInput.lambda i) = D.logInput.alpha i
  | .linearFormAssembly =>
      linearForm D.logInput =
        ∑ i : Fin D.logInput.n, (D.logInput.coeff i : ℂ) * D.logInput.lambda i
  | .lowerBoundInterface =>
      D.hasBakerLowerBound
  | .diophantineReduction =>
      D.hasReductionToFiniteSearch
  | .boundednessConclusion =>
      D.allSolutionsBounded
  | .explicitBoundExtraction =>
      D.allSolutionsBounded → HasExplicitSolutionBound D
  | .finiteSearchClosure =>
      HasExplicitSolutionBound D

/--
Checked data shape for a closed reusable Baker-method proof package.

The structure is intentionally parametrized by `D`; constructing it for a
specific Diophantine family is the future formalization task.
-/
structure BakerMethodReusableDecomposition (D : BakerMethodData.{u}) where
  logLinearSubstrate : BakerMethodPackageTarget D .logLinearSubstrate
  linearFormAssembly : BakerMethodPackageTarget D .linearFormAssembly
  lowerBoundInterface : BakerMethodPackageTarget D .lowerBoundInterface
  diophantineReduction : BakerMethodPackageTarget D .diophantineReduction
  boundednessConclusion : BakerMethodPackageTarget D .boundednessConclusion
  explicitBoundExtraction : BakerMethodPackageTarget D .explicitBoundExtraction
  finiteSearchClosure : BakerMethodPackageTarget D .finiteSearchClosure

/--
Statement that a particular Baker-method data package has been decomposed into
the reusable theorem-family nodes.
-/
def HasReusableTheoremFamilyDecomposition (D : BakerMethodData.{u}) : Prop :=
  Nonempty (BakerMethodReusableDecomposition D)

/-- The package target for the log-linear substrate is supplied by the input data. -/
theorem logLinearSubstrateTarget (D : BakerMethodData.{u}) :
    BakerMethodPackageTarget D .logLinearSubstrate := by
  intro i
  exact ⟨D.logInput.alpha_nonzero i,
    D.logInput.alpha_algebraic i,
    D.logInput.exp_lambda_eq_alpha i⟩

/-- The package target for assembling the linear form is definitional. -/
theorem linearFormAssemblyTarget (D : BakerMethodData.{u}) :
    BakerMethodPackageTarget D .linearFormAssembly :=
  rfl

/--
A closed reusable decomposition supplies the theorem-internal Baker-method
implication for its data package.
-/
theorem bakerMethodBound_of_reusableDecomposition
    (D : BakerMethodData.{u}) (H : BakerMethodReusableDecomposition D) :
    HasBakerMethodBound D := by
  intro _ _
  exact H.boundednessConclusion

/-- A closed reusable decomposition supplies the explicit finite-search bound. -/
theorem explicitBound_of_reusableDecomposition
    (D : BakerMethodData.{u}) (H : BakerMethodReusableDecomposition D) :
    HasExplicitSolutionBound D :=
  H.finiteSearchClosure

/--
The reusable decomposition is stronger than the local statement package for a
fixed `D`.
-/
theorem statementPackage_of_reusableDecomposition
    (D : BakerMethodData.{u}) (H : BakerMethodReusableDecomposition D) :
    HasBakerMethodBound D ∧ (D.allSolutionsBounded → HasExplicitSolutionBound D) :=
  ⟨bakerMethodBound_of_reusableDecomposition D H, H.explicitBoundExtraction⟩

/-- Canonical theorem-family package names for public backfill. -/
def reusablePackageNames : List String := [
  "log_linear_substrate",
  "linear_form_assembly",
  "lower_bound_interface",
  "diophantine_reduction",
  "boundedness_conclusion",
  "explicit_bound_extraction",
  "finite_search_closure"
]

/-- M0387-level child leaves that still need serial public integration. -/
def theoremFamilyChildLeaves : List String := [
  "THM-M-0397-P01 log-linear-form substrate over algebraic nonzero complex targets",
  "THM-M-0397-P02 linear-form assembly and nonzero-form side condition",
  "THM-M-0397-P03 Baker/Baker-Wuestholz/Matveev lower-bound interface selection",
  "THM-M-0397-P04 problem-specific Diophantine reduction to the lower-bound interface",
  "THM-M-0397-P05 extraction of an explicit height or coefficient bound",
  "THM-M-0397-P06 finite-search closure for the selected solution predicate",
  "THM-M-0397-P07 repo-local wrapper, pinned external dependency, or local proof-body completion gate"
]

/-- Audit shape for a possible external Lean 4 Baker-method theorem anchor. -/
structure ExternalLeanAnchorAudit where
  exactTheoremFound : Prop
  importedIntoLakeClosure : Prop
  concreteIntegrationBlockerRecorded : Prop

/--
Repo-local integration-debt gate for THM-M-0397.

If an exact external Lean 4 proof is found, anchor-only evidence is not enough:
the proof must either enter this Lake closure or receive a concrete blocker.
-/
def RepoLocalIntegrationDebtGate (A : ExternalLeanAnchorAudit) : Prop :=
  A.exactTheoremFound →
    A.importedIntoLakeClosure ∨ A.concreteIntegrationBlockerRecorded

/--
If an exact external anchor is found and has entered this Lake closure, the
repo-local integration-debt gate is discharged by import/check integration.
-/
theorem repoLocalIntegrationDebtGate_of_imported
    (A : ExternalLeanAnchorAudit) (h : A.importedIntoLakeClosure) :
    RepoLocalIntegrationDebtGate A := by
  intro _
  exact Or.inl h

/--
If an exact external anchor is found but cannot yet enter this Lake closure, the
gate can only be discharged by recording a concrete integration blocker.
-/
theorem repoLocalIntegrationDebtGate_of_blocker
    (A : ExternalLeanAnchorAudit) (h : A.concreteIntegrationBlockerRecorded) :
    RepoLocalIntegrationDebtGate A := by
  intro _
  exact Or.inr h

/-- If no exact external anchor is found, the integration-debt gate is vacuous. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit) (h : Not A.exactTheoremFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/--
Integration-ready public task text for the external-proof-found branch.

This is checked metadata for the later serial public-doc integrator.  It is not
an assertion that an external Baker-method proof has been found.
-/
def externalBakerProofPublicIntegratorTask : List String := [
  "If an exact external Lean 4 Baker-method proof is found, record project URL, commit, license, Lake toolchain, module paths, theorem names, and the matched THM-M-0397 branch.",
  "Pin the dependency in the repository Lake closure or vendor the proof body, then import the exact module from a repo-local wrapper.",
  "Check the wrapper with the repository toolchain and record the command, dependency revisions, and theorem names.",
  "If pin/import/check is blocked, record a concrete integration blocker with the failing command, compatibility issue, or license/dependency conflict.",
  "Keep THM-M-0397 not completed while evidence is anchor-only; remove any repo_local_integration_debt before a completed status is claimed."
]

/--
Gate for the later public theorem-tree backfill.

This child keeps the private runtime ledger out of the public completion
surface.  A serialized integrator may publish the theorem-tree page only after
the machine anchors and package-level ledgers are stable and a public merge
target has been selected.
-/
structure PublicTheoremTreeBackfillGate where
  machineAnchorsStable : Prop
  packageLevelLedgersStable : Prop
  publicMergeTargetReady : Prop
  privateRuntimeLedgerExcluded : Prop

/-- Public theorem-tree backfill is allowed exactly when every gate is closed. -/
def PublicTheoremTreeBackfillAllowed (G : PublicTheoremTreeBackfillGate) : Prop :=
  G.machineAnchorsStable ∧
    G.packageLevelLedgersStable ∧
      G.publicMergeTargetReady ∧
        G.privateRuntimeLedgerExcluded

/-- Projection: public backfill requires stable machine anchors. -/
theorem machineAnchorsStable_of_publicBackfillAllowed
    (G : PublicTheoremTreeBackfillGate)
    (h : PublicTheoremTreeBackfillAllowed G) :
    G.machineAnchorsStable :=
  h.1

/-- Projection: public backfill requires stable package-level ledgers. -/
theorem packageLevelLedgersStable_of_publicBackfillAllowed
    (G : PublicTheoremTreeBackfillGate)
    (h : PublicTheoremTreeBackfillAllowed G) :
    G.packageLevelLedgersStable :=
  h.2.1

/-- Projection: public backfill requires a stable public merge target. -/
theorem publicMergeTargetReady_of_publicBackfillAllowed
    (G : PublicTheoremTreeBackfillGate)
    (h : PublicTheoremTreeBackfillAllowed G) :
    G.publicMergeTargetReady :=
  h.2.2.1

/-- Projection: the private runtime ledger is never the public completion surface. -/
theorem privateRuntimeLedgerExcluded_of_publicBackfillAllowed
    (G : PublicTheoremTreeBackfillGate)
    (h : PublicTheoremTreeBackfillAllowed G) :
    G.privateRuntimeLedgerExcluded :=
  h.2.2.2

/--
Integration-ready checklist for the later public theorem-tree page.

The checklist is retained as checked metadata in the Lean artifact; the public
docs must be updated only by a serialized integrator.
-/
def publicTheoremTreeBackfillChecklist : List String := [
  "Do not publish .cron runtime ledgers as the THM-M-0397 completion surface.",
  "Publish the human-readable theorem-tree page only after machine anchors are stable at the recorded mathlib revision.",
  "Publish the page only after the reusable Baker-method package ledger is stable and each open leaf remains explicitly unchecked.",
  "Keep THM-M-0397 open unless local validation, public merge-back, leaf ledgers, and the no-repo-local-integration-debt gate all pass."
]

/--
Normalized Stage1 statement shape for THM-M-0397.

Later work should replace the abstract certificate predicates by the selected
mathlib or pinned external Lean 4 formalization of lower bounds for linear forms
in logarithms, heights over number fields, and the relevant Diophantine
reduction.
-/
def StatementShape : Prop :=
  ∀ D : BakerMethodData.{u},
    HasBakerMethodBound D ∧ (D.allSolutionsBounded → HasExplicitSolutionBound D)

/-- The statement shape unfolds to the explicit data-parametrized form. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ D : BakerMethodData.{u},
        HasBakerMethodBound D ∧
          (D.allSolutionsBounded → HasExplicitSolutionBound D) :=
  Iff.rfl

/-- Projection wrapper for the Baker lower-bound premise in the data package. -/
theorem bakerLowerBound_premise (D : BakerMethodData.{u})
    (h : D.hasBakerLowerBound) :
    D.hasBakerLowerBound :=
  h

/-- Projection wrapper for the finite-search reduction premise in the data package. -/
theorem reductionToFiniteSearch_premise (D : BakerMethodData.{u})
    (h : D.hasReductionToFiniteSearch) :
    D.hasReductionToFiniteSearch :=
  h

/-- Substrate check: algebraicity of the exponential targets is represented in mathlib. -/
theorem algebraic_target_available (D : BakerMethodData.{u}) (i : Fin D.logInput.n) :
    IsAlgebraic ℚ (D.logInput.alpha i) :=
  D.logInput.alpha_algebraic i

/-- Substrate check: logarithm choices are connected to targets by `Complex.exp`. -/
theorem exponential_target_available (D : BakerMethodData.{u}) (i : Fin D.logInput.n) :
    Complex.exp (D.logInput.lambda i) = D.logInput.alpha i :=
  D.logInput.exp_lambda_eq_alpha i

/--
Checked local wrapper: a proof of `StatementShape` supplies the explicit bound
conclusion for any particular Baker-method data package.
-/
theorem explicitBound_of_statementShape
    (h : StatementShape.{u}) (D : BakerMethodData.{u})
    (hbounded : D.allSolutionsBounded) :
    HasExplicitSolutionBound D :=
  (h D).2 hbounded

/--
Checked local wrapper: a proof of `StatementShape` supplies the theorem-internal
Baker-method implication for any particular data package.
-/
theorem bakerMethodBound_of_statementShape
    (h : StatementShape.{u}) (D : BakerMethodData.{u}) :
    HasBakerMethodBound D :=
  (h D).1

/-- Pinned mathlib revision used for the THM-M-0397 local anchor audit. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
One public-table row for the mathlib substrate audit requested by the Stage1
THM-M-0397 backfill.

These rows are module anchors and status notes only.  They do not assert that a
Baker lower-bound theorem or a full Baker-method Diophantine closure exists in
mathlib.
-/
structure MathlibAnchorRow where
  category : String
  modules : List String
  status : String

/--
Integration-ready mathlib anchor table for the public THM-M-0397 backfill.

The module names were checked against the local mathlib source tree pinned by
`Formalizations/Lean/lakefile.lean` at `mathlibAnchorRevision`.
-/
def mathlibAnchorTable : List MathlibAnchorRow := [
  { category := "height",
    modules := [
      "Mathlib.NumberTheory.Height.Basic",
      "Mathlib.NumberTheory.Height.NumberField",
      "Mathlib.NumberTheory.Height.Northcott",
      "Mathlib.NumberTheory.Height.Projectivization",
      "Mathlib.NumberTheory.Height.MvPolynomial"
    ],
    status := "height/Northcott substrate available; no Baker lower-bound closure claimed" },
  { category := "number-field",
    modules := [
      "Mathlib.NumberTheory.NumberField.Basic",
      "Mathlib.NumberTheory.NumberField.Norm",
      "Mathlib.NumberTheory.NumberField.ProductFormula",
      "Mathlib.NumberTheory.NumberField.FractionalIdeal",
      "Mathlib.NumberTheory.NumberField.Ideal.Basic",
      "Mathlib.NumberTheory.NumberField.FinitePlaces",
      "Mathlib.NumberTheory.NumberField.Discriminant.Basic",
      "Mathlib.NumberTheory.NumberField.CanonicalEmbedding.Basic"
    ],
    status := "number-field object model available for future height and product-formula branches" },
  { category := "local-field",
    modules := [
      "Mathlib.NumberTheory.LocalField.Basic",
      "Mathlib.NumberTheory.NumberField.Completion.FinitePlace",
      "Mathlib.NumberTheory.NumberField.Completion.InfinitePlace",
      "Mathlib.NumberTheory.Padics.PadicNumbers",
      "Mathlib.NumberTheory.Padics.PadicVal.Basic"
    ],
    status := "local-field and completion substrate available; no Baker local estimate claimed" },
  { category := "unit",
    modules := [
      "Mathlib.NumberTheory.NumberField.Units.Basic",
      "Mathlib.NumberTheory.NumberField.Units.DirichletTheorem",
      "Mathlib.NumberTheory.NumberField.Units.Regulator"
    ],
    status := "unit-group and regulator-adjacent modules available; no S-unit equation closure claimed" },
  { category := "class-group",
    modules := [
      "Mathlib.NumberTheory.NumberField.ClassNumber",
      "Mathlib.NumberTheory.ClassNumber.Finite",
      "Mathlib.RingTheory.ClassGroup"
    ],
    status := "class-number and class-group substrate available; not a Baker-method theorem" },
  { category := "Liouville/Lindemann-adjacent",
    modules := [
      "Mathlib.NumberTheory.Transcendental.Liouville.Basic",
      "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith",
      "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleNumber",
      "Mathlib.NumberTheory.Transcendental.Liouville.Measure",
      "Mathlib.NumberTheory.Transcendental.Liouville.Residual",
      "Mathlib.NumberTheory.Transcendental.Lindemann.AnalyticalPart"
    ],
    status := "transcendence-adjacent APIs available; no linear-forms-in-logarithms lower bound found" },
  { category := "Diophantine approximation",
    modules := [
      "Mathlib.NumberTheory.DiophantineApproximation.Basic",
      "Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions"
    ],
    status := "Diophantine approximation substrate available; no effective Baker bridge claimed" }
]

/-- Mathlib areas audited for future Baker-method object-model integration. -/
def mathlibAnchorModules : List String :=
  mathlibAnchorTable.foldr (fun row acc => row.modules ++ acc) []

/--
Search terms that must be revisited before this slot can move beyond
statement-shape status.
-/
def externalAnchorSearchTerms : List String := [
  "Baker method Lean 4",
  "linear forms in logarithms Lean",
  "Baker theorem mathlib",
  "Diophantine effective bounds Lean",
  "number field heights Lean 4",
  "S-unit equation Lean"
]

/--
One row from the external Lean 4 code-search audit requested by the Stage1
THM-M-0397 backfill.

Rows are documentary anchors only.  They do not assert that an external Baker
proof exists unless `exactBakerTheorem` records that status and the integration
debt gate above has also been discharged.
-/
structure ExternalLeanCodeSearchRow where
  source : String
  query : String
  projectUrl : String
  commit : String
  modules : List String
  theoremNames : List String
  lakeCompatibility : String
  exactBakerTheorem : String
  integrationStatus : String

/--
External Lean 4 code-search audit rows for the C003 pass.

Authenticated GitHub code search was blocked in the local environment: `gh auth
status` reported no logged-in host and no `GH_TOKEN`/`GITHUB_TOKEN` environment
variable was present.  The unauthenticated GitHub code-search API returned
HTTP 401, and later unauthenticated REST probes hit the public rate limit.
The entries below therefore record reproducible negative probes and one
web-search false positive, not proof absence.
-/
def externalLeanCodeSearchAuditRows : List ExternalLeanCodeSearchRow := [
  { source := "GitHub CLI auth check",
    query := "gh auth status",
    projectUrl := "https://github.com",
    commit := "not applicable",
    modules := [],
    theoremNames := [],
    lakeCompatibility := "authenticated search unavailable: no logged-in GitHub host",
    exactBakerTheorem := "not established",
    integrationStatus := "blocked until an authenticated GitHub code-search credential is available" },
  { source := "GitHub REST code search",
    query := "Baker linear forms logarithms language:Lean",
    projectUrl := "https://api.github.com/search/code",
    commit := "not applicable",
    modules := [],
    theoremNames := [],
    lakeCompatibility := "not applicable",
    exactBakerTheorem := "not established: API returned HTTP 401 Requires authentication",
    integrationStatus := "audit blocker, not evidence of global absence" },
  { source := "GitHub repository search",
    query := "\"Baker\" \"Lean 4\" theorem; \"linear forms in logarithms\" Lean; \"Baker method\" Lean",
    projectUrl := "https://api.github.com/search/repositories",
    commit := "not applicable",
    modules := [],
    theoremNames := [],
    lakeCompatibility := "no candidate repository returned by the completed repository-search probes",
    exactBakerTheorem := "not found by repository-level probes",
    integrationStatus := "no repo-local integration debt created by these negative repository probes" },
  { source := "Web search false positive",
    query := "site:github.com Lean Baker theorem linear forms logarithms",
    projectUrl := "https://github.com/QuixiAI/collatz",
    commit := "937e7f7ccf737151db79fa01724db3a0af040895",
    modules := [],
    theoremNames := [],
    lakeCompatibility := "not imported; candidate was not audited as a Lake-compatible Baker proof",
    exactBakerTheorem := "not a THM-M-0397 anchor: search snippet describes Baker-style material as dependency context",
    integrationStatus := "false positive; no pin/import/check task should be created from this row alone" }
]

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check HasBakerMethodBound
#check HasExplicitSolutionBound
#check NormalizationBranch
#check StatementNormalization
#check normalizedBranchTarget
#check BakerMethodPackage
#check BakerMethodPackageTarget
#check BakerMethodReusableDecomposition
#check HasReusableTheoremFamilyDecomposition
#check IsAlgebraic
#check Complex.exp
#check Complex.log
#check linearForm
#check logLinearSubstrateTarget
#check linearFormAssemblyTarget
#check bakerMethodBound_of_reusableDecomposition
#check explicitBound_of_reusableDecomposition
#check RepoLocalIntegrationDebtGate
#check repoLocalIntegrationDebtGate_of_imported
#check repoLocalIntegrationDebtGate_of_blocker
#check explicitBound_of_statementShape
#check bakerMethodBound_of_statementShape
#check externalBakerProofPublicIntegratorTask
#check PublicTheoremTreeBackfillGate
#check PublicTheoremTreeBackfillAllowed
#check machineAnchorsStable_of_publicBackfillAllowed
#check packageLevelLedgersStable_of_publicBackfillAllowed
#check publicMergeTargetReady_of_publicBackfillAllowed
#check privateRuntimeLedgerExcluded_of_publicBackfillAllowed
#check publicTheoremTreeBackfillChecklist
#check mathlibAnchorRevision
#check MathlibAnchorRow
#check mathlibAnchorTable
#check mathlibAnchorModules
#check ExternalLeanCodeSearchRow
#check externalLeanCodeSearchAuditRows

end S1_M_010
end Stage1
end AwesomeTheorems

namespace AwesomeTheorems
namespace NumberTheory
namespace THM_M_0397

/-!
## Checkable branch selected for the local THM-M-0397 namespace

This namespace intentionally starts with the low-risk height-substrate wrapper
branch.  It does not contain, assume, or package a Baker lower bound for linear
forms in logarithms.
-/

/--
The locally selected checkable branch for THM-M-0397.

Only `heightSubstrateWrapper` is selected here: it wraps already imported
mathlib height APIs and is kept separate from any future Baker lower-bound
interface.
-/
inductive CheckableBranch where
  | heightSubstrateWrapper
  deriving DecidableEq

/-- The branch selected before opening the local THM-M-0397 namespace surface. -/
def selectedBranch : CheckableBranch :=
  .heightSubstrateWrapper

namespace HeightSubstrateWrapper

variable {K : Type u} [Field K] [Height.AdmissibleAbsValues K]
variable {ι : Type v}

/-- Local name for mathlib's multiplicative height of one field element. -/
def multiplicativeHeight (x : K) : ℝ :=
  Height.mulHeight₁ x

/-- Local name for mathlib's logarithmic height of one field element. -/
def logarithmicHeight (x : K) : ℝ :=
  Height.logHeight₁ x

/-- Local name for mathlib's multiplicative height of a tuple. -/
def tupleMultiplicativeHeight (x : ι → K) : ℝ :=
  Height.mulHeight x

/-- Local name for mathlib's logarithmic height of a tuple. -/
def tupleLogarithmicHeight (x : ι → K) : ℝ :=
  Height.logHeight x

/--
Checked mathlib wrapper: multiplicative height of a field element is positive.
-/
theorem multiplicativeHeight_pos (x : K) :
    0 < multiplicativeHeight x :=
  Height.mulHeight₁_pos x

/--
Checked mathlib wrapper: logarithmic height of a field element is nonnegative.
-/
theorem logarithmicHeight_nonneg (x : K) :
    0 ≤ logarithmicHeight x :=
  Height.zero_le_logHeight₁ x

/--
Checked mathlib wrapper: logarithmic height is the logarithm of multiplicative
height for one field element.
-/
theorem logarithmicHeight_eq_log_multiplicativeHeight (x : K) :
    logarithmicHeight x = Real.log (multiplicativeHeight x) :=
  Height.logHeight₁_eq_log_mulHeight₁ x

/-- Checked mathlib wrapper: the multiplicative height of `1` is `1`. -/
theorem multiplicativeHeight_one :
    multiplicativeHeight (1 : K) = 1 :=
  Height.mulHeight₁_one

/-- Checked mathlib wrapper: the logarithmic height of `1` is `0`. -/
theorem logarithmicHeight_one :
    logarithmicHeight (1 : K) = 0 :=
  Height.logHeight₁_one

/-- Checked mathlib wrapper: multiplicative tuple height is positive. -/
theorem tupleMultiplicativeHeight_pos [Finite ι] (x : ι → K) :
    0 < tupleMultiplicativeHeight x :=
  Height.mulHeight_pos x

/-- Checked mathlib wrapper: logarithmic tuple height is nonnegative. -/
theorem tupleLogarithmicHeight_nonneg [Finite ι] (x : ι → K) :
    0 ≤ tupleLogarithmicHeight x :=
  Height.logHeight_nonneg x

/--
Checked mathlib wrapper: tuple logarithmic height is the logarithm of tuple
multiplicative height.
-/
theorem tupleLogarithmicHeight_eq_log_tupleMultiplicativeHeight (x : ι → K) :
    tupleLogarithmicHeight x = Real.log (tupleMultiplicativeHeight x) :=
  Height.logHeight_eq_log_mulHeight x

/-- Checked mathlib wrapper: logarithmic height is invariant under inverse. -/
theorem logarithmicHeight_inv (x : K) :
    logarithmicHeight (x⁻¹) = logarithmicHeight x :=
  Height.logHeight₁_inv x

/-- Checked mathlib wrapper: logarithmic height of a power. -/
theorem logarithmicHeight_pow (x : K) (n : ℕ) :
    logarithmicHeight (x ^ n) = (n : ℝ) * logarithmicHeight x :=
  Height.logHeight₁_pow x n

/-- Checked mathlib wrapper: logarithmic height is invariant under negation. -/
theorem logarithmicHeight_neg (x : K) :
    logarithmicHeight (-x) = logarithmicHeight x :=
  Height.logHeight₁_neg x

/-- Checked mathlib wrapper: logarithmic height is subadditive for products. -/
theorem logarithmicHeight_mul_le (x y : K) :
    logarithmicHeight (x * y) ≤ logarithmicHeight x + logarithmicHeight y :=
  Height.logHeight₁_mul_le x y

/--
Checked mathlib wrapper: logarithmic height satisfies the standard addition
bound.
-/
theorem logarithmicHeight_add_le (x y : K) :
    logarithmicHeight (x + y) ≤
      (Height.totalWeight K : ℝ) * Real.log 2 +
        logarithmicHeight x + logarithmicHeight y :=
  Height.logHeight₁_add_le x y

/--
Checked mathlib wrapper: logarithmic height satisfies the standard subtraction
bound.
-/
theorem logarithmicHeight_sub_le (x y : K) :
    logarithmicHeight (x - y) ≤
      (Height.totalWeight K : ℝ) * Real.log 2 +
        logarithmicHeight x + logarithmicHeight y :=
  Height.logHeight₁_sub_le x y

/-- Checked mathlib wrapper: tuple logarithmic height is invariant under negation. -/
theorem tupleLogarithmicHeight_neg (x : ι → K) :
    tupleLogarithmicHeight (-x) = tupleLogarithmicHeight x :=
  Height.logHeight_neg x

/-- Checked mathlib wrapper: tuple logarithmic height is invariant under nonzero scaling. -/
theorem tupleLogarithmicHeight_smul_eq_tupleLogarithmicHeight
    [Finite ι] (x : ι → K) {c : K} (hc : c ≠ 0) :
    tupleLogarithmicHeight (c • x) = tupleLogarithmicHeight x :=
  Height.logHeight_smul_eq_logHeight x hc

/-- Checked mathlib wrapper: tuple logarithmic height is subadditive for products. -/
theorem tupleLogarithmicHeight_mul_le [Finite ι] (x y : ι → K) :
    tupleLogarithmicHeight (x * y) ≤
      tupleLogarithmicHeight x + tupleLogarithmicHeight y :=
  Height.logHeight_mul_le x y

/-- Checked mathlib wrapper: tuple logarithmic height of a power. -/
theorem tupleLogarithmicHeight_pow [Finite ι] (x : ι → K) (n : ℕ) :
    tupleLogarithmicHeight (x ^ n) = (n : ℝ) * tupleLogarithmicHeight x :=
  Height.logHeight_pow x n

end HeightSubstrateWrapper

/-! ## THM-local audit probes retained in the checked file. -/

#check CheckableBranch
#check selectedBranch
#check HeightSubstrateWrapper.multiplicativeHeight
#check HeightSubstrateWrapper.logarithmicHeight
#check HeightSubstrateWrapper.tupleMultiplicativeHeight
#check HeightSubstrateWrapper.tupleLogarithmicHeight
#check HeightSubstrateWrapper.multiplicativeHeight_pos
#check HeightSubstrateWrapper.logarithmicHeight_nonneg
#check HeightSubstrateWrapper.logarithmicHeight_eq_log_multiplicativeHeight
#check HeightSubstrateWrapper.tupleMultiplicativeHeight_pos
#check HeightSubstrateWrapper.tupleLogarithmicHeight_nonneg
#check HeightSubstrateWrapper.tupleLogarithmicHeight_eq_log_tupleMultiplicativeHeight
#check HeightSubstrateWrapper.logarithmicHeight_inv
#check HeightSubstrateWrapper.logarithmicHeight_pow
#check HeightSubstrateWrapper.logarithmicHeight_neg
#check HeightSubstrateWrapper.logarithmicHeight_mul_le
#check HeightSubstrateWrapper.logarithmicHeight_add_le
#check HeightSubstrateWrapper.logarithmicHeight_sub_le
#check HeightSubstrateWrapper.tupleLogarithmicHeight_neg
#check HeightSubstrateWrapper.tupleLogarithmicHeight_smul_eq_tupleLogarithmicHeight
#check HeightSubstrateWrapper.tupleLogarithmicHeight_mul_le
#check HeightSubstrateWrapper.tupleLogarithmicHeight_pow

end THM_M_0397
end NumberTheory
end AwesomeTheorems
