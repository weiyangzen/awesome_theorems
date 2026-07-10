import Mathlib.Data.Complex.Basic
import Mathlib.Data.Real.Basic
import Mathlib.NumberTheory.DiophantineApproximation.Basic
import Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.Height.Projectivization
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith

/-!
# S1-M-013 / THM-M-0400: Subspace theorem

This Stage1 repair artifact records a kernel-checkable statement shape for
Schmidt's subspace theorem in its simultaneous-approximation form.  The full
number-theoretic proof is not present in the current repo-local Lean closure.
The theorem is therefore represented as a precise `Prop`, together with a
small checked vacuous branch that exercises the quantified finite-exception
shape without claiming the full result.
-/

namespace Stage1.THMM0400

/--
A proper rational subspace placeholder for the finite exceptional family in
the subspace theorem.

The current Stage1 artifact keeps the linear-algebra object model explicit but
abstract: later work should replace `rationalLinearSubspaceModel` with the
chosen mathlib object, for example a submodule over `Rat` after freezing the
integer-vector embedding.
-/
structure ProperRationalSubspace (dimension : Nat) where
  contains : (Fin dimension -> Int) -> Prop
  rationalLinearSubspaceModel : Prop
  proper : ∃ x : Fin dimension -> Int, ¬ contains x

/--
Data for a normalized simultaneous-approximation instance of Schmidt's
subspace theorem.

`smallProductInequality x` is the formal slot for the usual product bound
involving independent algebraic linear forms, height, and a positive epsilon.
The audit fields state the intended mathematical side conditions until the
final mathlib number-field and height model is selected.
-/
structure SubspaceTheoremDatum where
  dimension : Nat
  positiveDimension : 0 < dimension
  linearFormCount : Nat
  formCount_eq_dimension : linearFormCount = dimension
  linearFormValue : Fin linearFormCount -> (Fin dimension -> Int) -> Real
  height : (Fin dimension -> Int) -> Real
  epsilon : Real
  epsilon_pos : 0 < epsilon
  algebraicCoefficientModel : Prop
  independentLinearForms : Prop
  normalizedHeightModel : Prop
  smallProductInequality : (Fin dimension -> Int) -> Prop

/--
Source-faithful coefficient model: algebraic coefficients are represented
directly as complex numbers.  This mirrors the usual printed formulation, but
it leaves a later wrapper to bridge finite algebraic coefficient data to
mathlib's number-field height APIs.
-/
structure DirectAlgebraicComplexCoefficientModel (dimension : Nat) where
  coefficient : Fin dimension -> Fin dimension -> Complex
  algebraicOverRat : ∀ i j, IsAlgebraic Rat (coefficient i j)

/--
Bundled coefficient model: choose one number field containing the coefficients
and a fixed embedding into `Complex`.  This is the preferred Stage1 wrapper
target because it aligns with mathlib's number-field and height infrastructure.
-/
structure BundledNumberFieldCoefficientModel (dimension : Nat) where
  K : Type
  [field : Field K]
  [numberField : NumberField K]
  coefficient : Fin dimension -> Fin dimension -> K
  embedToComplex : K →+* Complex

/--
The coefficient-model branch selected for the next checked wrapper.

`directAlgebraicComplex` remains the source-facing comparison statement, while
`bundledNumberField` is the integration-facing choice for later height and
product-formula work.
-/
inductive CoefficientModelChoice where
  | directAlgebraicComplex
  | bundledNumberField
deriving DecidableEq, Repr

/--
Normalized Stage1 statement shape for the subspace theorem: the integer
solutions of the product-small inequality are contained in finitely many
proper rational subspaces.
-/
def StatementShape : Prop :=
  ∀ datum : SubspaceTheoremDatum,
    datum.algebraicCoefficientModel →
    datum.independentLinearForms →
    datum.normalizedHeightModel →
      ∃ exceptionalSubspaces : List (ProperRationalSubspace datum.dimension),
        ∀ x : Fin datum.dimension -> Int,
          datum.smallProductInequality x →
          ∃ V : ProperRationalSubspace datum.dimension,
            V ∈ exceptionalSubspaces ∧ V.contains x

/--
Statement/audit/proof-package classification for this Stage1 slot.

These values are data used by the private ledger and by later public backfill;
they are not completion certificates for the Subspace theorem.
-/
inductive WorkSurface where
  | statement
  | audit
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

/-- Wrapper-facing role assigned to an audited mathlib import. -/
inductive HeightImportRole where
  | requiredForNumberFieldHeight
  | requiredForProjectiveWrapper
  | availableForPolynomialHeightBounds
  | availableForNorthcottFiniteness
  | notRequiredForFirstWrapper
deriving DecidableEq, Repr

/-- Search surfaces for external Lean 4 anchor discovery. -/
inductive ExternalAnchorSearchSurface where
  | pinnedMathlibLocal
  | authenticatedGitHubCodeSearch
  | unauthenticatedWebSanitySearch
  | integrationDebtGate
deriving DecidableEq, Repr

/-- Outcome labels for child `S1-M-013-C005` anchor-search audit rows. -/
inductive ExternalAnchorSearchOutcome where
  | terminalAnchorAbsent
  | authenticatedSearchBlocked
  | supportingAnchorOnly
  | integrationRequiredIfFound
deriving DecidableEq, Repr

/-- Roles for mathlib Diophantine-approximation APIs that are not Subspace anchors. -/
inductive ApproximationNonAnchorRole where
  | dirichletRationalApproximation
  | legendreContinuedFractionCriterion
  | liouvilleExponentPredicate
deriving DecidableEq, Repr

/-- M0387-level package roles for splitting the core Subspace proof skeleton. -/
inductive CoreSubspaceSkeletonRole where
  | auxiliaryPolynomialConstruction
  | siegelLemmaDimensionCount
  | heightProductFormulaEstimates
  | zeroEstimateMultiplicity
  | exceptionalSubspaceExtraction
  | descentAndFiniteCover
  | externalClosureIntegrationGate
deriving DecidableEq, Repr

/-- Checked audit row for the direct-vs-number-field coefficient decision. -/
structure CoefficientModelDecision where
  sourceFacingModel : CoefficientModelChoice
  wrapperFacingModel : CoefficientModelChoice
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/--
Decision for child `S1-M-013-C002`: keep the direct algebraic `Complex`
coefficient model as the source-facing comparison, but select bundled
number-field coefficients as the wrapper-facing model.

This is a checked audit datum, not a proof of equivalence between the two
models and not a proof of the Subspace theorem.
-/
def coefficientModelDecision : CoefficientModelDecision := {
  sourceFacingModel := CoefficientModelChoice.directAlgebraicComplex
  wrapperFacingModel := CoefficientModelChoice.bundledNumberField
  status := "select bundled number-field coefficients for the wrapper; retain direct algebraic Complex coefficients as source-facing comparison"
  debt := MachineProofDebt.formalizationDebt
  machineState := MachineState.notRepoLocalClosed
}

/--
Remaining leaves for the coefficient-model branch.  These are deliberately
recorded as strings for ledger synchronization; they are not completion claims.
-/
def coefficientModelChildLeaves : List String := [
  "M0400-L006 prove or pin equivalence from direct algebraic Complex coefficients to a generated number-field model",
  "M0400-L007 define the bundled number-field linear-form package with a fixed Complex embedding",
  "M0400-L008 choose the height/product API over the bundled number field and bridge it to the printed Complex product inequality",
  "M0400-L020 prove scalar-extension independence preservation or keep Complex-linear independence as an explicit hypothesis"
]

/-- Checked row for the mathlib height-import audit. -/
structure HeightImportAuditRow where
  importName : String
  role : HeightImportRole
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/-- Checked audit row for external Lean 4 Subspace/Roth/Schmidt anchor search. -/
structure ExternalLeanAnchorAuditRow where
  surface : ExternalAnchorSearchSurface
  query : String
  outcome : ExternalAnchorSearchOutcome
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/-- Checked non-anchor row for Dirichlet/Legendre/Liouville mathlib APIs. -/
structure ApproximationNonAnchorAuditRow where
  moduleName : String
  declarations : List String
  role : ApproximationNonAnchorRole
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/-- Checked split row for the future core Subspace proof skeleton. -/
structure CoreSubspaceSkeletonSplitRow where
  packageId : String
  role : CoreSubspaceSkeletonRole
  upstreamInput : String
  downstreamOutput : String
  leafBudget : String
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/-- C008 cases for enforcing the repo-local integration-debt gate. -/
inductive RepoLocalIntegrationDebtGateCase where
  | noCurrentExternalClosure
  | futureExternalAnchorOnly
  | futureIntegrationBlocked
deriving DecidableEq, Repr

/--
Checked policy row for child `S1-M-013-C008`.

The row records only open/non-completion cases.  A successful future
pin/import/check would create a new completed wrapper or dependency row rather
than reusing these blocker rows.
-/
structure RepoLocalIntegrationDebtGateRow where
  gateCase : RepoLocalIntegrationDebtGateCase
  trigger : String
  requiredAction : String
  blockerIfUnresolved : String
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/-- C009 cases for public human-readable theorem-tree merge gating. -/
inductive HumanReadableMergeGateCase where
  | machineAnchorNotReady
  | localLeafLedgerUnchecked
  | serialPublicMergeOnly
  | noTheoremCompletionClaim
deriving DecidableEq, Repr

/--
Checked policy row for child `S1-M-013-C009`.

Human-readable theorem-tree content may be merged into public Stage1 surfaces
only after the machine-anchor audit and local `<=100` leaf ledger are stable.
These rows record the current open gate and the future serial-merge rule; they
are not a proof of `StatementShape`.
-/
structure HumanReadableMergeGateRow where
  gateCase : HumanReadableMergeGateCase
  prerequisite : String
  mergeRule : String
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/--
Audit result for child `S1-M-013-C003`: the first wrapper should import the
number-field height module, and should add projective height only if the wrapper
uses mathlib `Projectivization` rather than raw tuples.

This is import-level audit data, not a theorem-body claim for the Subspace
theorem.
-/
def heightImportAuditRows : List HeightImportAuditRow := [
  {
    importName := "Mathlib.NumberTheory.Height.NumberField"
    role := HeightImportRole.requiredForNumberFieldHeight
    status := "wrapper-facing import for Height.mulHeight/logHeight on tuples over a NumberField; also provides the NumberField AdmissibleAbsValues instance and product-formula-facing API"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    importName := "Mathlib.NumberTheory.Height.Projectivization"
    role := HeightImportRole.requiredForProjectiveWrapper
    status := "required only if the wrapper represents solution points as Projectivization K (Fin n -> K); raw tuple wrappers can defer this import"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    importName := "Mathlib.NumberTheory.Height.MvPolynomial"
    role := HeightImportRole.availableForPolynomialHeightBounds
    status := "available for later polynomial height-bound leaves; not needed for the first statement-only linear-form wrapper"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    importName := "Mathlib.NumberTheory.Height.Northcott"
    role := HeightImportRole.availableForNorthcottFiniteness
    status := "available for later Northcott/finiteness leaves; not needed for the first finite-exception statement wrapper"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/--
Audit result for child `S1-M-013-C006`: mathlib's Dirichlet,
Legendre, and Liouville APIs are usable approximation substrate, but they are
not proof anchors for Schmidt's Subspace theorem.

These checked rows document positive local declarations while keeping their
non-anchor status explicit.  They do not provide a theorem body for
`StatementShape`.
-/
def approximationNonAnchorAuditRows : List ApproximationNonAnchorAuditRow := [
  {
    moduleName := "Mathlib.NumberTheory.DiophantineApproximation.Basic"
    declarations := [
      "Real.exists_int_int_abs_mul_sub_le",
      "Real.exists_nat_abs_mul_sub_round_le",
      "Real.exists_rat_abs_sub_le_and_den_le",
      "Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational",
      "Rat.finite_rat_abs_sub_lt_one_div_den_sq",
      "Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational"
    ]
    role := ApproximationNonAnchorRole.dirichletRationalApproximation
    status := "checked one-dimensional Dirichlet/rational-approximation APIs; useful for low-dimensional scaffolding, but not a simultaneous algebraic linear-form theorem and not a finite union of proper rational subspaces"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    moduleName := "Mathlib.NumberTheory.DiophantineApproximation.Basic and Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions"
    declarations := [
      "Real.exists_rat_eq_convergent",
      "Real.exists_convs_eq_rat"
    ]
    role := ApproximationNonAnchorRole.legendreContinuedFractionCriterion
    status := "checked Legendre continued-fraction criteria for rational approximation; these are one-real continued-fraction facts and do not supply Roth, Schmidt, or Subspace theorem closure"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    moduleName := "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith"
    declarations := [
      "LiouvilleWith",
      "LiouvilleWith.exists_pos",
      "LiouvilleWith.mono",
      "LiouvilleWith.frequently_lt_rpow_neg",
      "LiouvilleWith.irrational",
      "forall_liouvilleWith_iff"
    ]
    role := ApproximationNonAnchorRole.liouvilleExponentPredicate
    status := "checked Liouville exponent predicate and elementary closure/irrationality lemmas; the file comments mention Thue-Siegel-Roth as stronger context, but no algebraic irrational Roth theorem or Subspace theorem proof is provided"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/--
Child `S1-M-013-C007`: split `M0400.Pkg05.CoreSubspaceProofSkeleton`
into smaller formalization packages because no external Lean 4 closure is
pinned/imported/checked for the root Subspace theorem in this repository.

These rows are a checked package decomposition only.  They deliberately keep
each package in `notRepoLocalClosed` state until an actual local proof body or
pinned upstream closure exists.
-/
def coreSubspaceProofSkeletonSplit : List CoreSubspaceSkeletonSplitRow := [
  {
    packageId := "M0400.Pkg05a.AuxiliaryPolynomialConstruction"
    role := CoreSubspaceSkeletonRole.auxiliaryPolynomialConstruction
    upstreamInput := "normalized number-field coefficient package, height model, epsilon, and finite-dimensional linear-form data"
    downstreamOutput := "auxiliary polynomial or section with controlled degree, height, and prescribed vanishing conditions"
    leafBudget := "unchecked; split into <=100-step leaves after the chosen polynomial/section API is fixed"
    status := "open formalization package; no external closure pinned locally"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    packageId := "M0400.Pkg05b.SiegelLemmaDimensionCount"
    role := CoreSubspaceSkeletonRole.siegelLemmaDimensionCount
    upstreamInput := "linear constraint count from vanishing conditions and the selected height/degree bounds"
    downstreamOutput := "existence of a nonzero auxiliary object with explicit coefficient-height control"
    leafBudget := "unchecked; requires a separate <=100-step ledger for dimension count and height bound"
    status := "open formalization package; candidate proof depends on available Siegel-lemma infrastructure"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    packageId := "M0400.Pkg05c.HeightProductFormulaEstimates"
    role := CoreSubspaceSkeletonRole.heightProductFormulaEstimates
    upstreamInput := "number-field height APIs, admissible absolute values, product formula, and evaluated linear forms"
    downstreamOutput := "global height/product inequalities needed to force small auxiliary values"
    leafBudget := "unchecked; split archimedean, nonarchimedean, and normalization leaves separately"
    status := "open formalization package; mathlib substrate exists but no Subspace theorem estimate chain is closed"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    packageId := "M0400.Pkg05d.ZeroEstimateMultiplicity"
    role := CoreSubspaceSkeletonRole.zeroEstimateMultiplicity
    upstreamInput := "auxiliary object plus small-value inequalities at candidate integer points"
    downstreamOutput := "multiplicity or zero-estimate contradiction unless points satisfy a linear dependence alternative"
    leafBudget := "unchecked; split multiplicity definitions, derivative/vanishing propagation, and contradiction leaves"
    status := "open formalization package; no checked zero-estimate proof body exists in this repo"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    packageId := "M0400.Pkg05e.ExceptionalSubspaceExtraction"
    role := CoreSubspaceSkeletonRole.exceptionalSubspaceExtraction
    upstreamInput := "linear dependence alternative produced by the zero estimate"
    downstreamOutput := "proper rational subspace containing each remaining solution point in the current branch"
    leafBudget := "unchecked; depends on the final rational-submodule object model"
    status := "open formalization package; statement-side placeholder is present but extraction proof is absent"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    packageId := "M0400.Pkg05f.DescentAndFiniteCover"
    role := CoreSubspaceSkeletonRole.descentAndFiniteCover
    upstreamInput := "exceptional-subspace extraction for each branch, plus induction/descent measure"
    downstreamOutput := "finite list of proper rational subspaces covering all product-small integer solutions"
    leafBudget := "unchecked; split branch enumeration, descent termination, and finite-list assembly"
    status := "open formalization package; this is the finite-cover assembly, not a completed theorem"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    packageId := "M0400.Pkg05g.ExternalClosureIntegrationGate"
    role := CoreSubspaceSkeletonRole.externalClosureIntegrationGate
    upstreamInput := "any future authenticated Lean 4 proof of Schmidt's Subspace theorem or an equivalent terminal wrapper"
    downstreamOutput := "pinned/imported/checked repo-local closure, or a concrete integration blocker"
    leafBudget := "not a proof leaf; M0387 integration gate"
    status := "open gate; anchor-only evidence must not be marked completed"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/--
Child `S1-M-013-C008`: enforce the M0387 repo-local integration-debt gate.

If a future authenticated external Lean 4 proof of Schmidt's Subspace theorem
appears, this slot may not be marked completed from a URL, theorem name, or
anchor-only row.  The proof must enter the repository validation closure by a
pinned/imported/checked dependency or wrapper; otherwise the public state must
record a concrete blocker and remain open.
-/
def repoLocalIntegrationDebtGateRows : List RepoLocalIntegrationDebtGateRow := [
  {
    gateCase := RepoLocalIntegrationDebtGateCase.noCurrentExternalClosure
    trigger := "current C005/C007 audit state has no pin-ready external Lean 4 closure for Schmidt's Subspace theorem"
    requiredAction := "keep the parent theorem open under formalization_debt and continue local package splitting"
    blockerIfUnresolved := "not applicable: no external terminal proof candidate is currently being left outside the repo-local closure"
    status := "open non-completion gate; no completed state claimed"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    gateCase := RepoLocalIntegrationDebtGateCase.futureExternalAnchorOnly
    trigger := "future authenticated search finds a Lean 4 theorem/module/repository name but it is not pinned/imported/checked here"
    requiredAction := "create a pin/import/check task with repository URL, commit, module path, theorem name, license, toolchain, and Lake feasibility"
    blockerIfUnresolved := "anchor-only evidence must remain external_upstream_anchor_only and must not count as public completion"
    status := "future blocker row; public completed state is forbidden until repo-local validation succeeds"
    debt := MachineProofDebt.repoLocalIntegrationDebt
    machineState := MachineState.externalUpstreamAnchorOnly
  },
  {
    gateCase := RepoLocalIntegrationDebtGateCase.futureIntegrationBlocked
    trigger := "future external Lean 4 proof appears but cannot yet be integrated because of toolchain, dependency, license, or trust-boundary audit failure"
    requiredAction := "record the concrete blocker, keep the item open, and rerun local validation only after the blocker is resolved"
    blockerIfUnresolved := "repo_local_integration_debt may be recorded only as an open blocker, never as a completed state"
    status := "future blocker row; no repo-local theorem closure exists while the blocker remains"
    debt := MachineProofDebt.repoLocalIntegrationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/--
Child `S1-M-013-C009`: gate public human-readable theorem-tree merge-back.

The C007 package split is useful reader-facing material only after its
machine-anchor boundary and local leaf ledger are stable.  This table keeps the
current public merge as a serial integrator action, not a worker-side public-doc
edit and not a theorem-completion claim.
-/
def humanReadableMergeGateRows : List HumanReadableMergeGateRow := [
  {
    gateCase := HumanReadableMergeGateCase.machineAnchorNotReady
    prerequisite := "externalLeanAnchorAuditRows and repoLocalIntegrationDebtGateRows must rule out anchor-only completion or provide a pinned/imported/checked terminal Lean theorem"
    mergeRule := "do not merge stable reader-facing theorem-tree prose ahead of the machine-anchor audit; use only integration-ready proposal text until then"
    status := "open gate; current C005/C008 state has no repo-local terminal Subspace theorem anchor"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    gateCase := HumanReadableMergeGateCase.localLeafLedgerUnchecked
    prerequisite := "coreSubspaceProofSkeletonSplit packages must be refined into independent <=100-step local leaf ledgers or explicitly marked unchecked"
    mergeRule := "public theorem-tree content may carry unchecked package rows, but must not state leaf closure or theorem completion"
    status := "open gate; C007 package rows are checked metadata, while their leaf budgets remain unchecked"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    gateCase := HumanReadableMergeGateCase.serialPublicMergeOnly
    prerequisite := "machine-anchor status, local ledger status, validation command, and debt classification are recorded in the private child ledger"
    mergeRule := "a serial integrator may merge the Public Backfill Proposal into the authoritative public surface; parallel child workers must not edit shared public docs"
    status := "integration-ready proposal only; no public document edited by this child"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    gateCase := HumanReadableMergeGateCase.noTheoremCompletionClaim
    prerequisite := "repo-local completion requires localProofBody, localWrapperUpstreamMathlib, or externalUpstreamPinned validation"
    mergeRule := "human-readable theorem-tree prose alone is not completion evidence and cannot discharge repo_local_integration_debt"
    status := "no completion claimed for THM-M-0400"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/--
Audit result for child `S1-M-013-C005`: external Lean 4 anchor search for
Subspace/Roth/Schmidt terms.

This records machine-checkable status metadata only.  It does not certify a
complete external proof, and it deliberately keeps blocked or anchor-only
evidence out of repo-local completion states.
-/
def externalLeanAnchorAuditRows : List ExternalLeanAnchorAuditRow := [
  {
    surface := ExternalAnchorSearchSurface.pinnedMathlibLocal
    query := "Subspace/Schmidt/Roth/Thue-Siegel terms in pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"
    outcome := ExternalAnchorSearchOutcome.terminalAnchorAbsent
    status := "local search found combinatorial Roth and general subspace APIs, plus Diophantine-approximation and height support, but no terminal Schmidt subspace theorem or Diophantine Roth theorem"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := ExternalAnchorSearchSurface.authenticatedGitHubCodeSearch
    query := "GitHub code search for Lean 4 Subspace theorem, Schmidt subspace theorem, Thue-Siegel-Roth, and LiouvilleWith/Roth"
    outcome := ExternalAnchorSearchOutcome.authenticatedSearchBlocked
    status := "authenticated GitHub CLI search is blocked in this environment because gh reports no logged-in host and no GH_TOKEN; this is a concrete integration blocker, not a completion claim"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := ExternalAnchorSearchSurface.unauthenticatedWebSanitySearch
    query := "web sanity search for Lean 4 Schmidt subspace theorem and Lean 4 Roth theorem"
    outcome := ExternalAnchorSearchOutcome.supportingAnchorOnly
    status := "web sanity search surfaced non-terminal math references and adjacent Lean 4 formalization activity, but no authenticated primary Lean 4 source file or theorem name for a complete Subspace theorem proof"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.externalUpstreamAnchorOnly
  },
  {
    surface := ExternalAnchorSearchSurface.integrationDebtGate
    query := "future external Lean 4 proof if one is found"
    outcome := ExternalAnchorSearchOutcome.integrationRequiredIfFound
    status := "future hits must be pinned/imported/checked locally or recorded with a concrete blocker before any public completed state"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/-- A checked audit row for the Stage1 statement/proof split. -/
structure AuditRow where
  surface : WorkSurface
  label : String
  status : String
  debt : MachineProofDebt
  machineState : MachineState

/-- A checked proof-package row for future M0387-level decomposition. -/
structure ProofPackage where
  id : String
  surface : WorkSurface
  obligation : String
  leafBudget : String
  status : String

/-- Current audit rows: statement scaffold exists; full proof remains formalization debt. -/
def statementAuditRows : List AuditRow := [
  {
    surface := WorkSurface.statement
    label := "direct simultaneous-approximation statement shape"
    status := "checked Prop scaffold with abstract object-model slots"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.audit
    label := "mathlib and external Lean 4 anchor audit"
    status := "no repo-local full Subspace theorem proof anchor is pinned or checked here"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  },
  {
    surface := WorkSurface.integrationGate
    label := "repo-local integration-debt gate"
    status := "completion not claimed; any future external closure must be pinned/imported/checked or blocked explicitly"
    debt := MachineProofDebt.formalizationDebt
    machineState := MachineState.notRepoLocalClosed
  }
]

/--
Child `S1-M-013-C004`: checked Lean statement-only file status.

The file provides statement and audit declarations for the Subspace theorem
slot, plus non-completion gates and a vacuous sanity branch for the finite
exceptional-family shape.  It does not provide a theorem body for
`StatementShape` and does not claim the full Subspace theorem.
-/
def checkedStatementOnlyFileStatus : AuditRow := {
  surface := WorkSurface.statement
  label := "checked Lean statement-only file"
  status := "S1_M_013.lean checks as a statement/audit artifact; no theorem body for StatementShape is claimed"
  debt := MachineProofDebt.formalizationDebt
  machineState := MachineState.notRepoLocalClosed
}

/-- First proof-package split, intentionally unchecked as theorem completion. -/
def proofPackageSplit : List ProofPackage := [
  {
    id := "M0400.Pkg01.StatementNormalization"
    surface := WorkSurface.statement
    obligation := "freeze dimension, algebraic linear forms, height/product inequality, and rational exceptional subspaces"
    leafBudget := "<=100 per eventual leaf"
    status := "partially represented by SubspaceTheoremDatum and StatementShape"
  },
  {
    id := "M0400.Pkg02.ObjectModelAudit"
    surface := WorkSurface.audit
    obligation := "select mathlib objects for number fields, heights, places, linear forms, and rational submodules"
    leafBudget := "<=100 per eventual leaf"
    status := "unchecked; requires import-level audit before public completion"
  },
  {
    id := "M0400.Pkg03.BridgeLemmas"
    surface := WorkSurface.proofPackage
    obligation := "bridge integer vectors, rational vectors, complex evaluation, norms, products, and zero-vector conventions"
    leafBudget := "<=100 per eventual leaf"
    status := "unchecked formalization debt"
  },
  {
    id := "M0400.Pkg04.CoreSubspaceArgument"
    surface := WorkSurface.proofPackage
    obligation := "formalize or import the auxiliary-polynomial, height, zero-estimate, and descent argument"
    leafBudget := "<=100 per eventual leaf"
    status := "unchecked formalization debt"
  },
  {
    id := "M0400.Pkg05.IntegrationGate"
    surface := WorkSurface.integrationGate
    obligation := "pin/import/check any future external Lean 4 closure or record a concrete integration blocker"
    leafBudget := "<=100 per eventual leaf"
    status := "open gate; no completion state claimed"
  }
]

/--
The reduced branch in which no integer vector satisfies the product-small
inequality.  This is a checked partial theorem for the finite-exception wrapper
shape, not a proof of the full subspace theorem.
-/
theorem vacuous_exceptional_family
    (datum : SubspaceTheoremDatum)
    (hsmall : ∀ x : Fin datum.dimension -> Int, ¬ datum.smallProductInequality x) :
    ∃ exceptionalSubspaces : List (ProperRationalSubspace datum.dimension),
      ∀ x : Fin datum.dimension -> Int,
        datum.smallProductInequality x →
          ∃ V : ProperRationalSubspace datum.dimension,
            V ∈ exceptionalSubspaces ∧ V.contains x := by
  refine ⟨[], ?_⟩
  intro x hx
  exact False.elim (hsmall x hx)

/-- Machine-proof debt classification for this Stage1 slot. -/
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

/-- Child `S1-M-013-C002` does not claim theorem completion. -/
theorem coefficientModelDecision_not_completed :
    ¬ countsAsRepoLocalCompleted coefficientModelDecision.machineState := by
  intro h
  exact h

/-- Child `S1-M-013-C003` does not claim theorem completion. -/
theorem heightImportAuditRows_not_completed :
    ∀ row ∈ heightImportAuditRows, ¬ countsAsRepoLocalCompleted row.machineState := by
  intro row hmem hclosed
  simp [heightImportAuditRows] at hmem
  rcases hmem with h | h | h | h <;> subst row <;> exact hclosed

/-- Child `S1-M-013-C004` does not claim theorem completion. -/
theorem checkedStatementOnlyFileStatus_not_completed :
    ¬ countsAsRepoLocalCompleted checkedStatementOnlyFileStatus.machineState := by
  intro h
  exact h

/-- Child `S1-M-013-C005` does not claim theorem completion. -/
theorem externalLeanAnchorAuditRows_not_completed :
    ∀ row ∈ externalLeanAnchorAuditRows, ¬ countsAsRepoLocalCompleted row.machineState := by
  intro row hmem hclosed
  simp [externalLeanAnchorAuditRows] at hmem
  rcases hmem with h | h | h | h <;> subst row <;> exact hclosed

/-- Child `S1-M-013-C006` documents non-anchors and does not claim completion. -/
theorem approximationNonAnchorAuditRows_not_completed :
    ∀ row ∈ approximationNonAnchorAuditRows, ¬ countsAsRepoLocalCompleted row.machineState := by
  intro row hmem hclosed
  simp [approximationNonAnchorAuditRows] at hmem
  rcases hmem with h | h | h <;> subst row <;> exact hclosed

/-- Child `S1-M-013-C007` splits the core skeleton and does not claim completion. -/
theorem coreSubspaceProofSkeletonSplit_not_completed :
    ∀ row ∈ coreSubspaceProofSkeletonSplit, ¬ countsAsRepoLocalCompleted row.machineState := by
  intro row hmem hclosed
  simp [coreSubspaceProofSkeletonSplit] at hmem
  rcases hmem with h | h | h | h | h | h | h <;> subst row <;> exact hclosed

/-- Child `S1-M-013-C008` enforces the integration-debt gate without completion claims. -/
theorem repoLocalIntegrationDebtGateRows_not_completed :
    ∀ row ∈ repoLocalIntegrationDebtGateRows, ¬ countsAsRepoLocalCompleted row.machineState := by
  intro row hmem hclosed
  simp [repoLocalIntegrationDebtGateRows] at hmem
  rcases hmem with h | h | h <;> subst row <;> exact hclosed

/--
Child `S1-M-013-C009` gates public human-readable theorem-tree merge-back
without claiming theorem completion.
-/
theorem humanReadableMergeGateRows_not_completed :
    ∀ row ∈ humanReadableMergeGateRows, ¬ countsAsRepoLocalCompleted row.machineState := by
  intro row hmem hclosed
  simp [humanReadableMergeGateRows] at hmem
  rcases hmem with h | h | h | h <;> subst row <;> exact hclosed

/-- Checked gate: anchor-only evidence would not count as repo-local completion. -/
theorem externalAnchorOnly_not_completed :
    ¬ countsAsRepoLocalCompleted MachineState.externalUpstreamAnchorOnly := by
  intro h
  exact h

/--
Repo-local integration-debt gate.

No external Lean 4 proof of the full subspace theorem has been pinned, imported,
and checked in this repository for this slot, so the module intentionally stays
open instead of claiming completion.
-/
def repoLocalIntegrationDebtGate : String :=
  "no repo_local_integration_debt discharge claimed; no completed state"

/-- Statement-normalization child leaves for later M0387-level backfill. -/
def theoremInternalChildLeaves : List String := [
  "S1-M-013.1 freeze number-field/rational-vector ambient object model",
  "S1-M-013.2 define algebraic independent linear-form package",
  "S1-M-013.3 define multiplicative height and epsilon product inequality",
  "S1-M-013.3a instantiate the first wrapper with Mathlib.NumberTheory.Height.NumberField and add Projectivization only if points are bundled projectively",
  "S1-M-013.4 prove or pin finite exceptional proper-subspace cover",
  "S1-M-013.5 split each imported or local proof branch into <=100-step leaves",
  "S1-M-013.6 repo-local wrapper/dependency closure and public merge audit"
]

/- Parent-line child `S1-M-013-C007` leaves for the core proof skeleton split. -/
def coreSubspaceSkeletonChildLeaves : List String := [
  "M0400.Pkg05a define and bound the auxiliary polynomial or section construction",
  "M0400.Pkg05b formalize the Siegel-lemma dimension count and coefficient-height bound",
  "M0400.Pkg05c prove the number-field height and product-formula estimate chain",
  "M0400.Pkg05d prove the zero-estimate or multiplicity contradiction package",
  "M0400.Pkg05e extract the proper rational exceptional subspace from the linear dependence alternative",
  "M0400.Pkg05f assemble the descent or induction into a finite exceptional cover",
  "M0400.Pkg05g pin/import/check any future external closure or record a concrete integration blocker"
]

/- Parent-line child `S1-M-013-C008` leaves for the integration-debt gate. -/
def integrationDebtGateChildLeaves : List String := [
  "M0400.Gate01 rerun authenticated external Lean 4 anchor search with primary-source URLs, commits, modules, and theorem names",
  "M0400.Gate02 if a terminal external proof is found, pin or vendor the dependency and add a repo-local wrapper theorem",
  "M0400.Gate03 validate the wrapper with lake env lean in this repository before marking any completed state",
  "M0400.Gate04 if pin/import/check is blocked, record the concrete blocker and keep the public parent state open"
]

/- Parent-line child `S1-M-013-C009` leaves for human-readable theorem-tree merge-back. -/
def humanReadableTheoremTreeMergeChildLeaves : List String := [
  "M0400.HR01 verify the machine-anchor status against externalLeanAnchorAuditRows and repoLocalIntegrationDebtGateRows before publishing stable theorem-tree prose",
  "M0400.HR02 refine coreSubspaceProofSkeletonSplit into independent <=100-step local leaf ledgers or keep each unresolved package explicitly unchecked",
  "M0400.HR03 translate the stable package rows into reader-facing theorem-tree prose using the canonical M0400.Pkg identifiers",
  "M0400.HR04 serially merge the public backfill into the authoritative public surface only after HR01-HR03 and local Lean validation are recorded",
  "M0400.HR05 keep THM-M-0400 open until a local proof body, pinned mathlib wrapper, or pinned external upstream closure validates in this repository"
]

/-- Integration-ready public note for child `S1-M-013-C009`. -/
def humanReadableTheoremTreePublicBackfill : List String := [
  "#### THM-M-0400 human-readable theorem-tree merge gate",
  "Checked repo-locally in Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_013.lean as humanReadableMergeGateRows and humanReadableMergeGateRows_not_completed.",
  "Stable reader-facing theorem-tree prose may be merged only after machine-anchor status and the local <=100 leaf-ledger status are recorded. Current status: the C007 package split is checked metadata, but the leaves remain unchecked and no repo-local terminal Subspace theorem proof is pinned/imported/checked.",
  "Public merge rule: a serial integrator may merge reader-facing package text using the canonical M0400.Pkg identifiers, preserving unchecked status where applicable. The merge must not mark THM-M-0400 completed unless the repo-local completion state is localProofBody, localWrapperUpstreamMathlib, or externalUpstreamPinned and the Lean validation command passes.",
  "No completed state may retain repo_local_integration_debt; anchor-only external evidence must remain open until pinned/imported/checked or recorded with a concrete blocker."
]

/-! ## Audit probes -/

#check StatementShape
#check vacuous_exceptional_family
#check statementAuditRows
#check proofPackageSplit
#check DirectAlgebraicComplexCoefficientModel
#check BundledNumberFieldCoefficientModel
#check coefficientModelDecision
#check coefficientModelDecision_not_completed
#check coefficientModelChildLeaves
#check Height.AdmissibleAbsValues
#check Height.mulHeight
#check Height.logHeight
#check NumberField.instAdmissibleAbsValues
#check NumberField.mulHeight_eq
#check NumberField.prod_abs_eq_one
#check Projectivization.mulHeight
#check Projectivization.logHeight
#check heightImportAuditRows
#check heightImportAuditRows_not_completed
#check approximationNonAnchorAuditRows
#check approximationNonAnchorAuditRows_not_completed
#check CoreSubspaceSkeletonRole
#check CoreSubspaceSkeletonSplitRow
#check coreSubspaceProofSkeletonSplit
#check coreSubspaceProofSkeletonSplit_not_completed
#check RepoLocalIntegrationDebtGateCase
#check RepoLocalIntegrationDebtGateRow
#check repoLocalIntegrationDebtGateRows
#check repoLocalIntegrationDebtGateRows_not_completed
#check HumanReadableMergeGateCase
#check HumanReadableMergeGateRow
#check humanReadableMergeGateRows
#check humanReadableMergeGateRows_not_completed
#check Real.exists_int_int_abs_mul_sub_le
#check Real.exists_nat_abs_mul_sub_round_le
#check Real.exists_rat_abs_sub_le_and_den_le
#check Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational
#check Rat.finite_rat_abs_sub_lt_one_div_den_sq
#check Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational
#check Real.exists_rat_eq_convergent
#check Real.exists_convs_eq_rat
#check LiouvilleWith
#check LiouvilleWith.exists_pos
#check LiouvilleWith.mono
#check LiouvilleWith.frequently_lt_rpow_neg
#check LiouvilleWith.irrational
#check forall_liouvilleWith_iff
#check checkedStatementOnlyFileStatus
#check checkedStatementOnlyFileStatus_not_completed
#check externalLeanAnchorAuditRows
#check externalLeanAnchorAuditRows_not_completed
#check machineProofDebtClassification
#check currentMachineState_not_completed
#check externalAnchorOnly_not_completed
#check repoLocalIntegrationDebtGate
#check theoremInternalChildLeaves
#check coreSubspaceSkeletonChildLeaves
#check integrationDebtGateChildLeaves
#check humanReadableTheoremTreeMergeChildLeaves
#check humanReadableTheoremTreePublicBackfill

end Stage1.THMM0400
