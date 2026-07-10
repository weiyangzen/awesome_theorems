import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.FieldTheory.AlgebraicClosure

/-!
# S1-M-009 / THM-M-0396: Baker's theorem

This Stage1 artifact records a conservative Lean 4 statement shape for Baker's
theorem on lower bounds for nonzero linear forms in logarithms of algebraic
numbers.  It deliberately does not claim the terminal theorem: the required
Diophantine-approximation proof package and effective height constants have not
been identified as a repo-local or pinned upstream Lean proof.

For the Stage1 statement-selection task, this file fixes the public theorem
variant to the standard Matveev 2000 multiplicative explicit bound convention.
The convention data below records the constant shape, but the analytic proof of
the bound remains formalization debt.
-/

noncomputable section

open scoped BigOperators

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_009

/--
Input data for a Baker linear-form-in-logarithms statement.

The logarithms are represented by arbitrary complex choices `lambda i` with
`Complex.exp (lambda i) = alpha i`; this avoids freezing the final formalization
to the principal branch `Complex.log`.
-/
structure BakerLinearFormsInput where
  n : ℕ
  alpha : Fin n → ℂ
  lambda : Fin n → ℂ
  coeff : Fin n → ℤ
  degreeBound : ℕ
  heightBound : ℝ
  coefficientBound : ℕ
  alpha_nonzero : ∀ i, alpha i ≠ 0
  alpha_algebraic : ∀ i, IsAlgebraic ℚ (alpha i)
  exp_lambda_eq_alpha : ∀ i, Complex.exp (lambda i) = alpha i
  degreeBound_positive : 0 < degreeBound
  heightBound_large_enough : 1 ≤ heightBound
  coefficientBound_covers : ∀ i, Int.natAbs (coeff i) ≤ coefficientBound

/-- The linear form `Λ = Σ b_i λ_i` appearing in Baker's theorem. -/
def linearForm (D : BakerLinearFormsInput) : ℂ :=
  ∑ i : Fin D.n, (D.coeff i : ℂ) * D.lambda i

/--
Output contract for an effective Baker lower-bound package.

The `bound` is intentionally abstract.  A later proof package must replace this
with the chosen explicit function of the degree, height, coefficient, and
dimension parameters and prove the displayed inequality.
-/
structure BakerLowerBoundData (D : BakerLinearFormsInput) where
  bound : ℝ
  bound_pos : 0 < bound
  bound_le_norm : linearForm D ≠ 0 → bound ≤ ‖linearForm D‖
  effectiveInAuditParameters : Prop
  effectiveInAuditParameters_holds : effectiveInAuditParameters

/-- Candidate named variants for the explicit Baker lower-bound theorem. -/
inductive BakerLowerBoundVariant where
  | bakerOriginal
  | bakerWuestholz
  | matveev2000Multiplicative
  | otherCitedVariant
  deriving DecidableEq, Repr

/--
Structured record for a selected lower-bound constant convention.

The numerical fields encode the standard Matveev 2000 multiplicative
convention
`1.4 * 30^(n+3) * n^(9/2) * D^2 * (1 + log D) * (1 + log B) * prod A_i`.
The text fields pin the audit semantics without asserting that the terminal
inequality has been proved in this repository.
-/
structure LowerBoundConstantConvention where
  variant : BakerLowerBoundVariant
  sourceLabel : String
  theoremForm : String
  leadingNumerator : ℕ
  leadingDenominator : ℕ
  exponentialBase : ℕ
  dimensionShift : ℕ
  dimensionPowerNumerator : ℕ
  dimensionPowerDenominator : ℕ
  degreePower : ℕ
  degreeLogFactor : String
  coefficientLogFactor : String
  heightParameterConvention : String
  coefficientBoundConvention : String
  logBranchConvention : String
  repoLocalProofStatus : String
  deriving Repr

/--
Stage1 A02 selection for `THM-M-0396`.

The chosen target is Matveev's 2000 multiplicative explicit lower bound for
`alpha_1^b_1 * ... * alpha_n^b_n - 1`, with the usual translation to a
nonzero linear form in chosen logarithms handled as a later bridge package.
-/
def selectedLowerBoundConvention : LowerBoundConstantConvention where
  variant := .matveev2000Multiplicative
  sourceLabel := "Matveev 2000 explicit lower bound for linear forms in logarithms"
  theoremForm :=
    "multiplicative Gamma = alpha_1^b_1 * ... * alpha_n^b_n - 1, Gamma != 0"
  leadingNumerator := 14
  leadingDenominator := 10
  exponentialBase := 30
  dimensionShift := 3
  dimensionPowerNumerator := 9
  dimensionPowerDenominator := 2
  degreePower := 2
  degreeLogFactor := "1 + log D"
  coefficientLogFactor := "1 + log B"
  heightParameterConvention :=
    "A_i >= max {D * h(alpha_i), |log alpha_i|, 0.16}"
  coefficientBoundConvention := "B >= max_i |b_i|"
  logBranchConvention :=
    "chosen complex logarithms; principal Complex.log is not forced"
  repoLocalProofStatus :=
    "statement-selection only; terminal lower-bound proof remains formalization_debt"

/-- The selected Stage1 lower-bound target is the Matveev 2000 convention. -/
theorem selectedLowerBoundConvention_variant :
    selectedLowerBoundConvention.variant =
      BakerLowerBoundVariant.matveev2000Multiplicative :=
  rfl

/-- The selected Matveev leading rational constant is `14 / 10`, i.e. `1.4`. -/
theorem selectedLowerBoundConvention_leadingConstant :
    selectedLowerBoundConvention.leadingNumerator = 14 ∧
      selectedLowerBoundConvention.leadingDenominator = 10 :=
  ⟨rfl, rfl⟩

/-- The selected Matveev dimension exponent is encoded as `9 / 2`. -/
theorem selectedLowerBoundConvention_dimensionPower :
    selectedLowerBoundConvention.dimensionPowerNumerator = 9 ∧
      selectedLowerBoundConvention.dimensionPowerDenominator = 2 :=
  ⟨rfl, rfl⟩

/-- The selected convention has positive denominators for rational constants. -/
theorem selectedLowerBoundConvention_denominators_pos :
    0 < selectedLowerBoundConvention.leadingDenominator ∧
      0 < selectedLowerBoundConvention.dimensionPowerDenominator := by
  decide

/--
Normalized Stage1 statement shape for Baker's theorem.

For algebraic nonzero `alpha i` and logarithm choices `lambda i`, every nonzero
integer linear form in the `lambda i` should have an effective positive lower
bound depending only on the standard audit parameters.
-/
def StatementShape : Prop :=
  ∀ D : BakerLinearFormsInput,
    linearForm D ≠ 0 →
      Nonempty (BakerLowerBoundData D)

/--
Machine-status vocabulary for this Stage1 slot.

The last two statuses are deliberately non-completing: a URL/theorem-name note
without a repo-local build is not completion, and the present Baker theorem
slot is still formalization debt.
-/
inductive MachineStatus where
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  | notRepoLocalClosed
  | formalizationDebt
  deriving DecidableEq, Repr

/-- Repository-local statuses that may count as completed under M0387 rules. -/
def MachineStatus.repoLocalCompleted : MachineStatus → Prop
  | .localProofBody => True
  | .localWrapperUpstreamMathlib => True
  | .externalUpstreamPinned => True
  | .externalUpstreamAnchorOnly => False
  | .notRepoLocalClosed => False
  | .formalizationDebt => False

/-- Boolean mirror of `MachineStatus.repoLocalCompleted` for finite audit tables. -/
def MachineStatus.repoLocalCompletedBool : MachineStatus → Bool
  | .localProofBody => true
  | .localWrapperUpstreamMathlib => true
  | .externalUpstreamPinned => true
  | .externalUpstreamAnchorOnly => false
  | .notRepoLocalClosed => false
  | .formalizationDebt => false

/-- Proof-package nodes that must be expanded before Baker's theorem can close. -/
inductive BakerProofPackage where
  | statementShape
  | algebraicLogInputs
  | heightDegreeBookkeeping
  | auxiliaryFunctionConstruction
  | zeroEstimate
  | determinantExtrapolation
  | explicitLowerBoundInequality
  | transcendenceCorollaries
  deriving DecidableEq, Repr

/--
Audit row for one Baker proof package.

`localBudgetStatus` records whether the package has already been decomposed into
M0387-compatible leaves.  `machineStatus` is the completion gate; it is not
derived from prose.
-/
structure BakerPackageAudit where
  package : BakerProofPackage
  role : String
  localBudgetStatus : String
  machineStatus : MachineStatus
  deriving Repr

/--
Repo-local proof-package tree for the direct Baker lower-bound theorem.

Only the statement-shape and variant-selection nodes have checked local Lean
artifacts in this file. The analytic/transcendence proof packages are listed as
formalization debt until a local proof body or pinned upstream Lean theorem is
available.
-/
def bakerProofPackageAudit : List BakerPackageAudit := [
  {
    package := .statementShape
    role := "checked local object model for chosen logarithms and abstract effective lower-bound data"
    localBudgetStatus := "checked statement shape; not a theorem proof"
    machineStatus := .notRepoLocalClosed
  },
  {
    package := .algebraicLogInputs
    role := "connect nonzero algebraic complex inputs with arbitrary logarithm choices via Complex.exp"
    localBudgetStatus := "substrate projection lemmas checked locally"
    machineStatus := .notRepoLocalClosed
  },
  {
    package := .heightDegreeBookkeeping
    role := "use the selected Matveev 2000 multiplicative constant convention for degree, height, coefficient, and dimension parameters"
    localBudgetStatus := "checked variant selection; height API bridge and terminal inequality remain unchecked"
    machineStatus := .formalizationDebt
  },
  {
    package := .auxiliaryFunctionConstruction
    role := "construct the auxiliary function or determinant used in the logarithmic-form lower bound"
    localBudgetStatus := "unchecked; no local Lean package found"
    machineStatus := .formalizationDebt
  },
  {
    package := .zeroEstimate
    role := "prove the zero estimate or multiplicity estimate controlling the auxiliary construction"
    localBudgetStatus := "unchecked; no local Lean package found"
    machineStatus := .formalizationDebt
  },
  {
    package := .determinantExtrapolation
    role := "bridge the auxiliary construction to a quantitative estimate for the chosen logarithmic form"
    localBudgetStatus := "unchecked; no local Lean package found"
    machineStatus := .formalizationDebt
  },
  {
    package := .explicitLowerBoundInequality
    role := "prove the final positive lower bound for every nonzero integer linear form in chosen logarithms"
    localBudgetStatus := "unchecked; terminal theorem not repo-local"
    machineStatus := .formalizationDebt
  },
  {
    package := .transcendenceCorollaries
    role := "derive corollary-level transcendence or nonzero-separation statements from the lower-bound theorem"
    localBudgetStatus := "unchecked; depends on the terminal lower-bound package"
    machineStatus := .formalizationDebt
  }
]

/--
Auxiliary-function proof-core subpackages for the selected Baker/Matveev route.

These are local Stage1 planning nodes for `S1-M-009-A08`.  They split the
auxiliary-function core into independently auditable packages; they do not
assert that the auxiliary construction, zero estimate, or final lower-bound
theorem has been formalized.
-/
inductive AuxiliaryCorePackage where
  | constructionSpecification
  | siegelLinearAlgebra
  | interpolationAndVanishing
  | zeroEstimate
  | analyticUpperEstimates
  | algebraicHeightControl
  | lowerBoundAssembly
  deriving DecidableEq, Repr

/-- Local closure status for one auxiliary-core leaf-budget row. -/
inductive AuxiliaryCoreLeafStatus where
  | uncheckedFormalizationDebt
  deriving DecidableEq, Repr

/--
M0387-style leaf-budget row for the auxiliary-function proof core.

`stepBudget` is a target upper bound for the eventual local proof leaf.  Because
the analytic Baker proof is not repo-local, every row below remains
`uncheckedFormalizationDebt` and has a non-completing `closureEffect`.
-/
structure AuxiliaryCoreLeafBudget where
  leafId : String
  package : AuxiliaryCorePackage
  obligation : String
  stepBudget : ℕ
  status : AuxiliaryCoreLeafStatus
  closureEffect : MachineStatus
  deriving DecidableEq, Repr

/-- The M0387 budget predicate used by the A08 auxiliary-core split. -/
def AuxiliaryCoreLeafBudget.withinM0387Budget
    (row : AuxiliaryCoreLeafBudget) : Prop :=
  row.stepBudget ≤ 100

/-- The completion-gate predicate used by the A08 auxiliary-core split. -/
def AuxiliaryCoreLeafBudget.notRepoLocalCompletion
    (row : AuxiliaryCoreLeafBudget) : Prop :=
  ¬ row.closureEffect.repoLocalCompleted

/-- Boolean mirror of the M0387 budget predicate for the finite A08 table. -/
def AuxiliaryCoreLeafBudget.withinM0387BudgetBool
    (row : AuxiliaryCoreLeafBudget) : Bool :=
  Nat.ble row.stepBudget 100

/-- Boolean mirror of the non-completion gate for the finite A08 table. -/
def AuxiliaryCoreLeafBudget.notRepoLocalCompletionBool
    (row : AuxiliaryCoreLeafBudget) : Bool :=
  !row.closureEffect.repoLocalCompletedBool

/--
Auxiliary-function proof-core leaf budget ledger for `S1-M-009-A08`.

Every row has a proposed `<= 100` local proof budget, but every row is still
formalization debt.  This is an integration-ready split, not a completed proof
ledger.
-/
def auxiliaryCoreLeafBudgetLedger : List AuxiliaryCoreLeafBudget := [
  {
    leafId := "BTH-AUX-L001"
    package := .constructionSpecification
    obligation := "choose the auxiliary determinant or polynomial family used by the selected Matveev proof source"
    stepBudget := 80
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L002"
    package := .constructionSpecification
    obligation := "state the coefficient index set, dimension parameters, and admissible vanishing conditions"
    stepBudget := 75
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L003"
    package := .constructionSpecification
    obligation := "connect construction parameters with degree, height, and coefficient-bound inputs"
    stepBudget := 90
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L004"
    package := .siegelLinearAlgebra
    obligation := "instantiate the finite-dimensional linear system for auxiliary coefficients"
    stepBudget := 90
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L005"
    package := .siegelLinearAlgebra
    obligation := "supply the Siegel-lemma or determinant-bound input needed for a nonzero auxiliary object"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L006"
    package := .siegelLinearAlgebra
    obligation := "prove coefficient-size bounds for the chosen nonzero auxiliary object"
    stepBudget := 95
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L007"
    package := .interpolationAndVanishing
    obligation := "formalize interpolation nodes and multiplicity conditions for the auxiliary object"
    stepBudget := 90
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L008"
    package := .interpolationAndVanishing
    obligation := "prove transfer from prescribed linear equations to vanishing-order statements"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L009"
    package := .interpolationAndVanishing
    obligation := "isolate branch-specific logarithm substitutions used in interpolation"
    stepBudget := 85
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L010"
    package := .zeroEstimate
    obligation := "state the selected zero-estimate theorem with exact hypotheses and source citation"
    stepBudget := 70
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L011"
    package := .zeroEstimate
    obligation := "bridge auxiliary-object vanishing data to the selected zero-estimate hypotheses"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L012"
    package := .zeroEstimate
    obligation := "derive the nonzero evaluation or bounded multiplicity conclusion from the zero estimate"
    stepBudget := 95
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L013"
    package := .analyticUpperEstimates
    obligation := "formalize the complex norm estimate for the auxiliary function on the chosen domain"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L014"
    package := .analyticUpperEstimates
    obligation := "isolate maximum-modulus, Cauchy, or Jensen-style analytic estimates required by the source proof"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L015"
    package := .analyticUpperEstimates
    obligation := "prove exponential/logarithm comparison inequalities for chosen complex logarithms"
    stepBudget := 95
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L016"
    package := .algebraicHeightControl
    obligation := "clear algebraic denominators for auxiliary coefficients and evaluations"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L017"
    package := .algebraicHeightControl
    obligation := "prove conjugate-product height bounds for auxiliary evaluations"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L018"
    package := .algebraicHeightControl
    obligation := "bridge mathlib height or Mahler-measure APIs to the selected Matveev height convention"
    stepBudget := 95
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L019"
    package := .lowerBoundAssembly
    obligation := "combine auxiliary upper estimates with algebraic lower estimates into the contradiction inequality"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L020"
    package := .lowerBoundAssembly
    obligation := "simplify monotone constant bounds to the selected Matveev explicit expression"
    stepBudget := 95
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  },
  {
    leafId := "BTH-AUX-L021"
    package := .lowerBoundAssembly
    obligation := "derive the terminal lower-bound statement for nonzero additive linear forms from the multiplicative form"
    stepBudget := 100
    status := .uncheckedFormalizationDebt
    closureEffect := .formalizationDebt
  }
]

/-- The auxiliary-core split is nonempty. -/
theorem auxiliaryCoreLeafBudgetLedger_nonempty :
    auxiliaryCoreLeafBudgetLedger ≠ [] := by
  native_decide

/-- Every auxiliary-core row has an M0387-compatible proposed leaf budget. -/
theorem auxiliaryCoreLeafBudgetLedger_withinM0387Budget :
    auxiliaryCoreLeafBudgetLedger.all
      AuxiliaryCoreLeafBudget.withinM0387BudgetBool = true := by
  native_decide

/--
No auxiliary-core row is a repo-local completion claim.

This is the gate that keeps the A08 split from being misread as proof closure.
-/
theorem auxiliaryCoreLeafBudgetLedger_notRepoLocalCompletion :
    auxiliaryCoreLeafBudgetLedger.all
      AuxiliaryCoreLeafBudget.notRepoLocalCompletionBool = true := by
  native_decide

/-- The terminal lower-bound package is explicitly present in the audit tree. -/
theorem explicitLowerBoundInequality_mem_audit :
    ∃ row ∈ bakerProofPackageAudit,
      row.package = BakerProofPackage.explicitLowerBoundInequality := by
  refine ⟨{
    package := .explicitLowerBoundInequality
    role := "prove the final positive lower bound for every nonzero integer linear form in chosen logarithms"
    localBudgetStatus := "unchecked; terminal theorem not repo-local"
    machineStatus := .formalizationDebt
  }, ?_, rfl⟩
  simp [bakerProofPackageAudit]

/-- Formalization debt is not a repo-local completed state. -/
theorem formalizationDebt_not_repoLocalCompleted :
    ¬ MachineStatus.repoLocalCompleted MachineStatus.formalizationDebt := by
  simp [MachineStatus.repoLocalCompleted]

/-- Anchor-only evidence is not a repo-local completed state. -/
theorem anchorOnly_not_repoLocalCompleted :
    ¬ MachineStatus.repoLocalCompleted MachineStatus.externalUpstreamAnchorOnly := by
  simp [MachineStatus.repoLocalCompleted]

/-- Current parent-level machine status for the Baker lower-bound theorem. -/
def terminalMachineStatus : MachineStatus :=
  .formalizationDebt

/--
Current completion gate for the terminal Baker theorem.

This proposition is intentionally false in the present artifact; the theorem
below records that the slot cannot be marked completed from the local evidence
currently available.
-/
def terminalRepoLocalCompletionGate : Prop :=
  terminalMachineStatus.repoLocalCompleted

/-- The current terminal Baker theorem gate is not satisfied repo-locally. -/
theorem terminalRepoLocalCompletionGate_not_satisfied :
    ¬ terminalRepoLocalCompletionGate := by
  simp [terminalRepoLocalCompletionGate, terminalMachineStatus,
    MachineStatus.repoLocalCompleted]

/--
Statement-normalization boundary between the two adjacent Stage1 slots.

`THM-M-0396` owns the lower-bound theorem for nonzero linear forms in chosen
logarithms of algebraic numbers.  `THM-M-0397` owns the Baker-method application
pipeline that uses such lower bounds to produce effective finite-search
closures for Diophantine problems.  This record is intentionally textual: it is
an integration-ready note, not a proof of Baker's theorem.
-/
structure StatementNormalizationBoundary where
  theoremSlot : String
  theoremOwns : String
  methodSlot : String
  methodOwns : String
  completionGate : String
  deriving Repr

/--
Compiled statement-normalization note for the public `THM-M-0396` backfill.

This keeps the public wording separate from the proof-critical theorem shape:
the theorem slot may expose `StatementShape`, but it must not absorb the broader
Baker method until the adjacent `THM-M-0397` application pipeline is separately
modeled and validated.
-/
def statementNormalizationBoundary : StatementNormalizationBoundary where
  theoremSlot := "S1-M-009 / THM-M-0396 Baker theorem"
  theoremOwns :=
    "effective lower bounds for nonzero integer linear forms in chosen logarithms of nonzero algebraic complex numbers"
  methodSlot := "S1-M-010 / THM-M-0397 Baker method"
  methodOwns :=
    "reusable Diophantine application pipelines that consume Baker-type lower bounds and close finite searches"
  completionGate :=
    "do not mark complete from prose or anchor-only evidence; require a local proof body, pinned upstream theorem, or explicit integration blocker"

/-- The theorem slot remains the direct lower-bound statement shape. -/
def TheoremSlotStatement : Prop :=
  StatementShape

/-- The recorded normalization note assigns the direct theorem to `S1-M-009`. -/
theorem statementNormalization_theoremSlot :
    statementNormalizationBoundary.theoremSlot =
      "S1-M-009 / THM-M-0396 Baker theorem" :=
  rfl

/-- The recorded normalization note keeps Baker-method applications in `S1-M-010`. -/
theorem statementNormalization_methodSlot :
    statementNormalizationBoundary.methodSlot =
      "S1-M-010 / THM-M-0397 Baker method" :=
  rfl

/-- Substrate check: algebraicity of the exponential targets is represented in mathlib. -/
theorem algebraic_target_available (D : BakerLinearFormsInput) (i : Fin D.n) :
    IsAlgebraic ℚ (D.alpha i) :=
  D.alpha_algebraic i

/-- Substrate check: arbitrary logarithm choices are connected to targets by `Complex.exp`. -/
theorem exponential_target_available (D : BakerLinearFormsInput) (i : Fin D.n) :
    Complex.exp (D.lambda i) = D.alpha i :=
  D.exp_lambda_eq_alpha i

/-- If all integer coefficients vanish, the recorded linear form vanishes. -/
theorem linearForm_zero_of_coeff_zero (D : BakerLinearFormsInput)
    (h : ∀ i : Fin D.n, D.coeff i = 0) : linearForm D = 0 := by
  simp [linearForm, h]

/-- mathlib modules audited for the current statement-shape layer. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.SpecialFunctions.Complex.Log",
  "Mathlib.Analysis.Complex.Exponential",
  "Mathlib.FieldTheory.AlgebraicClosure",
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.NumberTheory.DiophantineApproximation",
  "Mathlib.NumberTheory.SubspaceTheorem"
]

/-- Names and search tokens audited while looking for an existing Baker wrapper. -/
def anchorSearchTerms : List String := [
  "Baker",
  "Baker-Wuestholz",
  "Matveev",
  "linear forms in logarithms",
  "LinearFormsInLogarithms",
  "IsAlgebraic",
  "Complex.exp",
  "Complex.log",
  "height",
  "DiophantineApproximation",
  "SubspaceTheorem"
]

/--
One row from the external Lean 4 primary-source audit for Baker-type lower
bound theorem names and module paths.

These rows are audit evidence, not completion evidence.  A row only creates a
repo-local closure route if it identifies an exact Lean theorem and a concrete
Lake-compatible pin/import/check path.
-/
structure ExternalLeanPrimaryAuditRow where
  source : String
  queryOrProbe : String
  projectUrl : String
  commit : String
  modulePaths : List String
  theoremNames : List String
  result : String
  integrationStatus : String
  deriving Repr

/--
Primary-source Lean 4 audit rows for the Stage1 A04 pass.

The only completed source-level probe is the repository-local pinned mathlib
source grep.  Authenticated GitHub code search could not be completed in this
worker environment because `gh auth status` reported no logged-in GitHub host,
and the official GitHub code-search REST endpoint returned HTTP 401 without a
credential.  Therefore this table records a concrete audit blocker rather than
global proof absence.
-/
def externalLeanPrimaryAuditRows : List ExternalLeanPrimaryAuditRow := [
  {
    source := "pinned mathlib source tree"
    queryOrProbe :=
      "rg -n \"Baker|Wuestholz|Wustholz|Matveev|LinearFormsInLogarithms|linear forms in logarithms\" Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'"
    projectUrl := "https://github.com/leanprover-community/mathlib4"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    modulePaths := [
      "Mathlib.Analysis.SpecialFunctions.Complex.Log",
      "Mathlib.FieldTheory.AlgebraicClosure",
      "Mathlib.NumberTheory.Height.Basic",
      "Mathlib.NumberTheory.Height.NumberField",
      "Mathlib.NumberTheory.DiophantineApproximation.Basic"
    ]
    theoremNames := [
      "IsAlgebraic",
      "Complex.exp",
      "Complex.log"
    ]
    result :=
      "substrate modules found; no Baker, Baker-Wuestholz, Matveev, or LinearFormsInLogarithms terminal theorem name found by local source grep"
    integrationStatus :=
      "no external_upstream_pinned Baker theorem identified in pinned mathlib"
  },
  {
    source := "GitHub CLI authentication check"
    queryOrProbe := "gh auth status"
    projectUrl := "https://github.com"
    commit := "not applicable"
    modulePaths := []
    theoremNames := []
    result := "not logged into any GitHub hosts"
    integrationStatus :=
      "authenticated primary-source code search blocked until a GitHub credential is available"
  },
  {
    source := "official GitHub REST code search"
    queryOrProbe :=
      "https://api.github.com/search/code?q=%22Baker-Wuestholz%22+language:Lean and analogous LinearFormsInLogarithms/Matveev probes"
    projectUrl := "https://api.github.com/search/code"
    commit := "not applicable"
    modulePaths := []
    theoremNames := []
    result := "HTTP 401 without an authenticated credential"
    integrationStatus :=
      "audit blocker; not evidence of global absence and not a completion anchor"
  }
]

/-- This worker environment did not provide authenticated GitHub code search. -/
def authenticatedGitHubCodeSearchAvailable : Bool :=
  false

/--
No exact external Lean Baker/Baker-Wuestholz/Matveev theorem was identified by
the completed repo-local source audit rows.
-/
def exactExternalBakerTheoremIdentifiedByCompletedAudit : Bool :=
  false

/-- The A04 authenticated-search availability flag is currently false. -/
theorem authenticatedGitHubCodeSearchAvailable_eq_false :
    authenticatedGitHubCodeSearchAvailable = false :=
  rfl

/-- The completed source audit did not identify a terminal external theorem. -/
theorem exactExternalBakerTheoremIdentifiedByCompletedAudit_eq_false :
    exactExternalBakerTheoremIdentifiedByCompletedAudit = false :=
  rfl

/--
Integration decision for Stage1 A05.

This is separate from the A04 search table: it records whether a pin/import/check
action is currently available.  Since no exact external Baker theorem was
identified by the completed audit rows, there is no dependency to pin in this
child pass.  The remaining blocker is the unauthenticated global code-search
surface, not an anchor-only completion claim.
-/
structure ExternalProofIntegrationDecision where
  exactProofIdentified : Bool
  pinOrVendorAction : String
  repoLocalImportCheck : String
  concreteBlocker : String
  completionEffect : MachineStatus
  deriving Repr

/-- Current A05 pin/import/check decision for external Baker theorem evidence. -/
def externalBakerProofIntegrationDecision : ExternalProofIntegrationDecision where
  exactProofIdentified := exactExternalBakerTheoremIdentifiedByCompletedAudit
  pinOrVendorAction :=
    "not applicable: no exact external Baker/Baker-Wuestholz/Matveev Lean theorem was identified by completed audit rows"
  repoLocalImportCheck :=
    "no external dependency import or wrapper check was attempted because there is no identified theorem path to pin"
  concreteBlocker :=
    "authenticated GitHub code search is still required before claiming global absence or creating a pin task for an external proof"
  completionEffect := .formalizationDebt

/-- A05 currently has no exact external proof candidate to pin. -/
theorem externalBakerProofIntegrationDecision_no_exactProof :
    externalBakerProofIntegrationDecision.exactProofIdentified = false :=
  rfl

/-- The current A05 decision is not a repo-local theorem completion. -/
theorem externalBakerProofIntegrationDecision_not_repoLocalCompleted :
    ¬ externalBakerProofIntegrationDecision.completionEffect.repoLocalCompleted := by
  simp [externalBakerProofIntegrationDecision, MachineStatus.repoLocalCompleted]

/--
Stage1 A06 mathlib-wrapper decision.

A wrapper can only be built after the pinned mathlib source tree exposes an
exact terminal Baker/Baker-Wuestholz/Matveev lower-bound theorem.  The completed
local grep did not identify such a theorem, so this child records the absence
of a wrapper target rather than creating an anchor-only completion claim.
-/
structure MathlibWrapperDecision where
  terminalTheoremInPinnedMathlib : Bool
  searchedPinnedMathlib : String
  wrapperAction : String
  importAction : String
  concreteBlocker : String
  completionEffect : MachineStatus
  deriving Repr

/-- Current A06 decision for a possible mathlib wrapper around Baker's theorem. -/
def mathlibBakerWrapperDecision : MathlibWrapperDecision where
  terminalTheoremInPinnedMathlib := exactExternalBakerTheoremIdentifiedByCompletedAudit
  searchedPinnedMathlib :=
    "mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95; grep tokens Baker, Wuestholz, Wustholz, Matveev, LinearFormsInLogarithms, linear forms in logarithms"
  wrapperAction :=
    "no wrapper built: no exact terminal Baker lower-bound theorem name or module path was found in pinned mathlib"
  importAction :=
    "existing imports cover substrate APIs only; no new mathlib terminal-theorem import is available for A06"
  concreteBlocker :=
    "A06 requires a future mathlib theorem landing with an exact module path and declaration name, followed by a local wrapper checked by lake env lean"
  completionEffect := .formalizationDebt

/-- The current A06 decision has no terminal Baker theorem in pinned mathlib. -/
theorem mathlibBakerWrapperDecision_no_terminalTheorem :
    mathlibBakerWrapperDecision.terminalTheoremInPinnedMathlib = false :=
  rfl

/-- The current A06 decision is not a repo-local theorem completion. -/
theorem mathlibBakerWrapperDecision_not_repoLocalCompleted :
    ¬ mathlibBakerWrapperDecision.completionEffect.repoLocalCompleted := by
  simp [mathlibBakerWrapperDecision, MachineStatus.repoLocalCompleted]

/--
Multiplicative expression corresponding to the selected Matveev-style target.

This is only the algebraic/logarithmic bridge object
`alpha_1 ^ b_1 * ... * alpha_n ^ b_n`; the selected theorem variant would apply
to `multiplicativeForm D - 1` after its nonvanishing and height hypotheses are
bridged.
-/
def multiplicativeForm (D : BakerLinearFormsInput) : ℂ :=
  ∏ i : Fin D.n, D.alpha i ^ D.coeff i

/-- The multiplicative expression attached to valid Baker input is nonzero. -/
theorem multiplicativeForm_ne_zero (D : BakerLinearFormsInput) :
    multiplicativeForm D ≠ 0 := by
  rw [multiplicativeForm]
  exact Finset.prod_ne_zero_iff.mpr fun i _ =>
    zpow_ne_zero (D.coeff i) (D.alpha_nonzero i)

/--
Chosen logarithms bridge the additive linear form to the multiplicative
Matveev-style expression.

This is a local algebraic bridge, not the analytic Baker lower-bound theorem.
-/
theorem exp_linearForm_eq_multiplicativeForm (D : BakerLinearFormsInput) :
    Complex.exp (linearForm D) = multiplicativeForm D := by
  rw [linearForm, multiplicativeForm, Complex.exp_sum]
  refine Finset.prod_congr rfl ?_
  intro i _
  rw [Complex.exp_int_mul, D.exp_lambda_eq_alpha]

/-- If the additive linear form vanishes, the multiplicative expression is `1`. -/
theorem multiplicativeForm_eq_one_of_linearForm_eq_zero
    (D : BakerLinearFormsInput) (h : linearForm D = 0) :
    multiplicativeForm D = 1 := by
  rw [← exp_linearForm_eq_multiplicativeForm, h, Complex.exp_zero]

/--
The multiplicative nonvanishing hypothesis used by Matveev-style statements
implies the additive linear form is nonzero.
-/
theorem linearForm_ne_zero_of_multiplicativeForm_ne_one
    (D : BakerLinearFormsInput) (h : multiplicativeForm D ≠ 1) :
    linearForm D ≠ 0 := by
  intro hzero
  exact h (multiplicativeForm_eq_one_of_linearForm_eq_zero D hzero)

/-- Coefficient-bound bridge extracted from the input object model. -/
theorem coefficientBound_covers_abs_coeff
    (D : BakerLinearFormsInput) (i : Fin D.n) :
    Int.natAbs (D.coeff i) ≤ D.coefficientBound :=
  D.coefficientBound_covers i

/-- Degree-bound bridge extracted from the input object model. -/
theorem degreeBound_positive_available (D : BakerLinearFormsInput) :
    0 < D.degreeBound :=
  D.degreeBound_positive

/-- Height-parameter bridge extracted from the input object model. -/
theorem heightBound_large_enough_available (D : BakerLinearFormsInput) :
    1 ≤ D.heightBound :=
  D.heightBound_large_enough

/-- The selected convention keeps the Matveev height-parameter text available. -/
theorem selectedLowerBoundConvention_heightParameterConvention :
    selectedLowerBoundConvention.heightParameterConvention =
      "A_i >= max {D * h(alpha_i), |log alpha_i|, 0.16}" :=
  rfl

/-- The selected convention keeps the coefficient-bound text available. -/
theorem selectedLowerBoundConvention_coefficientBoundConvention :
    selectedLowerBoundConvention.coefficientBoundConvention =
      "B >= max_i |b_i|" :=
  rfl

/-- The selected convention records chosen-logarithm semantics, not principal logs. -/
theorem selectedLowerBoundConvention_logBranchConvention :
    selectedLowerBoundConvention.logBranchConvention =
      "chosen complex logarithms; principal Complex.log is not forced" :=
  rfl

/--
Checked bridge certificate for the A07 substrate.

The certificate packages local facts about algebraic nonzero inputs, chosen
logarithms, coefficient bounds, degree/height parameters, and the additive-to-
multiplicative logarithm bridge.  It deliberately does not contain the terminal
lower-bound inequality.
-/
structure BakerBridgeCertificate (D : BakerLinearFormsInput) where
  targets_nonzero : ∀ i, D.alpha i ≠ 0
  targets_algebraic : ∀ i, IsAlgebraic ℚ (D.alpha i)
  chosen_logs : ∀ i, Complex.exp (D.lambda i) = D.alpha i
  degree_positive : 0 < D.degreeBound
  height_large_enough : 1 ≤ D.heightBound
  coefficients_bounded : ∀ i, Int.natAbs (D.coeff i) ≤ D.coefficientBound
  multiplicative_nonzero : multiplicativeForm D ≠ 0
  exp_linearForm_bridge : Complex.exp (linearForm D) = multiplicativeForm D

/-- Every local Baker input yields the checked A07 bridge certificate. -/
def bakerBridgeCertificate (D : BakerLinearFormsInput) :
    BakerBridgeCertificate D where
  targets_nonzero := D.alpha_nonzero
  targets_algebraic := D.alpha_algebraic
  chosen_logs := D.exp_lambda_eq_alpha
  degree_positive := D.degreeBound_positive
  height_large_enough := D.heightBound_large_enough
  coefficients_bounded := D.coefficientBound_covers
  multiplicative_nonzero := multiplicativeForm_ne_zero D
  exp_linearForm_bridge := exp_linearForm_eq_multiplicativeForm D

/-- A07 bridge certificates are substrate artifacts, not terminal completion. -/
theorem bakerBridgeCertificate_not_terminal_completion :
    ¬ MachineStatus.repoLocalCompleted terminalMachineStatus := by
  simpa [terminalMachineStatus] using formalizationDebt_not_repoLocalCompleted

/--
Theorem-level audit row for `S1-M-009-A09`.

The table is intentionally declaration-level rather than proof-package-level:
it names a module path and a theorem/definition/structure name, then records the
mathematical role and closure state.  The machine status is the completion gate.
-/
structure TheoremLevelAuditRow where
  modulePath : String
  theoremName : String
  mathematicalRole : String
  closureState : String
  machineStatus : MachineStatus
  deriving DecidableEq, Repr

/-- Boolean gate: an A09 theorem-level audit row is not a repo-local completion. -/
def TheoremLevelAuditRow.notRepoLocalCompletedBool
    (row : TheoremLevelAuditRow) : Bool :=
  !row.machineStatus.repoLocalCompletedBool

/--
A09 theorem-level audit table for the Baker lower-bound slot.

Rows with mathlib module paths are substrate anchors only.  Rows with local
module paths are checked Stage1 scaffolding, bridge metadata, or public
statement aliases.  No row is a terminal Baker lower-bound proof.
-/
def theoremLevelAuditTable : List TheoremLevelAuditRow := [
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "BakerLinearFormsInput"
    mathematicalRole :=
      "input object model for algebraic nonzero targets, chosen logarithms, integer coefficients, and audit parameters"
    closureState :=
      "local statement scaffold checked by Lean; not a lower-bound proof"
    machineStatus := .notRepoLocalClosed
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "StatementShape"
    mathematicalRole :=
      "normalized Prop shape for nonzero linear forms in logarithms admitting effective positive lower-bound data"
    closureState :=
      "statement-only local target; terminal theorem remains formalization_debt"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "selectedLowerBoundConvention"
    mathematicalRole :=
      "selected Matveev 2000 multiplicative explicit constant convention"
    closureState :=
      "variant and constants checked as metadata; no analytic inequality proof"
    machineStatus := .notRepoLocalClosed
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "exp_linearForm_eq_multiplicativeForm"
    mathematicalRole :=
      "local bridge from additive chosen-logarithm linear form to multiplicative expression"
    closureState :=
      "checked bridge lemma; supporting infrastructure only"
    machineStatus := .notRepoLocalClosed
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "bakerBridgeCertificate"
    mathematicalRole :=
      "packages algebraicity, nonzero targets, chosen logs, degree/height/coefficient bounds, and multiplicative bridge"
    closureState :=
      "checked substrate certificate; terminal lower-bound inequality absent"
    machineStatus := .notRepoLocalClosed
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "bakerProofPackageAudit"
    mathematicalRole :=
      "package-level proof tree for statement shape, algebraic inputs, heights, auxiliary function, zero estimate, determinant extrapolation, and final inequality"
    closureState :=
      "audit tree recorded; analytic packages remain formalization_debt"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "auxiliaryCoreLeafBudgetLedger"
    mathematicalRole :=
      "M0387-style auxiliary-function leaf budget split for the selected Baker/Matveev route"
    closureState :=
      "21 proposed leaves checked for <=100 budget only; all leaves remain unchecked formalization_debt"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "externalLeanPrimaryAuditRows"
    mathematicalRole :=
      "external Lean 4 primary-source audit rows for Baker/Baker-Wuestholz/Matveev theorem anchors"
    closureState :=
      "completed local mathlib source grep found substrate only; authenticated global search remains blocked"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "externalBakerProofIntegrationDecision"
    mathematicalRole :=
      "pin/import/check decision for any exact external Baker theorem candidate"
    closureState :=
      "no exact external theorem identified by completed audit rows; no dependency pin available"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "mathlibBakerWrapperDecision"
    mathematicalRole :=
      "decision record for a possible wrapper around a terminal Baker theorem in pinned mathlib"
    closureState :=
      "no terminal Baker lower-bound theorem name or module path found in pinned mathlib"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "publicProofFlowMergeDecision"
    mathematicalRole :=
      "A11 decision record for when human-readable Baker proof-flow text may enter the authoritative public surface"
    closureState :=
      "public merge is blocked until machine anchors, local ledger, and serial public integration agree"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.Stage1.S1_M_009"
    theoremName := "readmeMetaStage1SyncDecision"
    mathematicalRole :=
      "A12 decision record for README, metadata, and Stage1 checklist synchronization"
    closureState :=
      "public synchronization is blocked until serial merge-back and build validation evidence agree"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "Mathlib.FieldTheory.AlgebraicClosure"
    theoremName := "IsAlgebraic"
    mathematicalRole :=
      "mathlib predicate used to state algebraicity of the complex inputs"
    closureState :=
      "substrate API imported and checked; not a Baker lower-bound theorem"
    machineStatus := .notRepoLocalClosed
  },
  {
    modulePath := "Mathlib.Analysis.SpecialFunctions.Complex.Log"
    theoremName := "Complex.exp"
    mathematicalRole :=
      "complex exponential API used to relate chosen logarithms to algebraic targets"
    closureState :=
      "substrate API imported and checked; not a Baker lower-bound theorem"
    machineStatus := .notRepoLocalClosed
  },
  {
    modulePath := "Mathlib.Analysis.SpecialFunctions.Complex.Log"
    theoremName := "Complex.log"
    mathematicalRole :=
      "principal-log API audited to avoid accidentally forcing principal branch semantics"
    closureState :=
      "substrate API imported and checked; selected statement uses arbitrary chosen logs"
    machineStatus := .notRepoLocalClosed
  },
  {
    modulePath := "AwesomeTheorems.NumberTheory.THM_M_0396"
    theoremName := "Statement"
    mathematicalRole :=
      "public statement-only namespace alias for the checked Stage1 Baker statement shape"
    closureState :=
      "public alias surface only; completion gate remains false"
    machineStatus := .formalizationDebt
  },
  {
    modulePath := "AwesomeTheorems.NumberTheory.THM_M_0396"
    theoremName := "terminalRepoLocalCompletionGate_not_satisfied"
    mathematicalRole :=
      "public non-completion gate for the Baker theorem namespace"
    closureState :=
      "checked negative gate; explicitly prevents a theorem-completion claim"
    machineStatus := .formalizationDebt
  }
]

/-- The A09 theorem-level audit table is present and nonempty. -/
theorem theoremLevelAuditTable_nonempty :
    theoremLevelAuditTable ≠ [] := by
  native_decide

/-- Every A09 theorem-level row is explicitly non-completing repo-locally. -/
theorem theoremLevelAuditTable_notRepoLocalCompletion :
    theoremLevelAuditTable.all
      TheoremLevelAuditRow.notRepoLocalCompletedBool = true := by
  native_decide

/-- The A09 table names the local normalized Baker statement shape. -/
theorem theoremLevelAuditTable_contains_statementShape :
    ∃ row ∈ theoremLevelAuditTable,
      row.modulePath = "AwesomeTheorems.Stage1.S1_M_009" ∧
        row.theoremName = "StatementShape" := by
  native_decide

/-- The A09 table names the public statement-only Baker namespace surface. -/
theorem theoremLevelAuditTable_contains_publicStatement :
    ∃ row ∈ theoremLevelAuditTable,
      row.modulePath = "AwesomeTheorems.NumberTheory.THM_M_0396" ∧
        row.theoremName = "Statement" := by
  native_decide

/--
Stage1 A10 build-gate decision.

The parent task requires `lake build` once a terminal local wrapper or pinned
dependency exists.  The current artifact has statement scaffolding and public
aliases only; A06/A09 still record that no terminal Baker lower-bound theorem
is available in pinned mathlib or as an external dependency.
-/
structure LocalBuildGateDecision where
  terminalWrapperOrDependencyExists : Bool
  validatedTarget : String
  fullBuildAction : String
  blocker : String
  completionEffect : MachineStatus
  deriving DecidableEq, Repr

/-- Current A10 decision: the terminal-wrapper/dependency precondition is not met. -/
def localBuildGateDecision : LocalBuildGateDecision where
  terminalWrapperOrDependencyExists := false
  validatedTarget := "AwesomeTheorems/Stage1/S1_M_009.lean"
  fullBuildAction :=
    "do not treat lake build as a theorem-completion gate until a terminal local wrapper or pinned dependency exists"
  blocker :=
    "no exact Baker/Baker-Wuestholz/Matveev lower-bound theorem is currently imported, wrapped, or pinned repo-locally"
  completionEffect := .formalizationDebt

/-- A10 is not unlocked because no terminal wrapper or dependency exists yet. -/
theorem localBuildGateDecision_no_terminalWrapperOrDependency :
    localBuildGateDecision.terminalWrapperOrDependencyExists = false :=
  rfl

/-- The current A10 decision is not a repo-local theorem completion. -/
theorem localBuildGateDecision_not_repoLocalCompleted :
    ¬ localBuildGateDecision.completionEffect.repoLocalCompleted := by
  simp [localBuildGateDecision, MachineStatus.repoLocalCompleted]

/--
Stage1 A11 public proof-flow merge decision.

This record does not contain the public prose itself.  It records the gate that a
serial integrator must satisfy before moving reader-facing proof-flow text into
the authoritative public surface.  In the current artifact the local statement,
audit table, A08 leaf ledger, and validation record are coherent, but no terminal
Baker lower-bound proof anchor has been imported, wrapped, pinned, or blocked by
an exact external theorem integration issue.
-/
structure PublicProofFlowMergeDecision where
  localMachineLedgerCoherent : Bool
  terminalMachineAnchorAvailable : Bool
  publicMergeAllowedNow : Bool
  publicMergeTarget : String
  proofFlowSummaryStatus : String
  blocker : String
  completionEffect : MachineStatus
  deriving DecidableEq, Repr

/-- Current A11 decision: keep the proof-flow summary as private backfill text. -/
def publicProofFlowMergeDecision : PublicProofFlowMergeDecision where
  localMachineLedgerCoherent := true
  terminalMachineAnchorAvailable := false
  publicMergeAllowedNow := false
  publicMergeTarget :=
    "serial merge into Docs/Stage1_Blueprint.md or successor public Stage1 surface only"
  proofFlowSummaryStatus :=
    "integration-ready private backfill text; not yet authoritative public proof-flow"
  blocker :=
    "no terminal Baker/Baker-Wuestholz/Matveev lower-bound proof is repo-locally imported, wrapped, pinned, or tied to a concrete external integration blocker"
  completionEffect := .formalizationDebt

/-- The A11 local ledger is coherent enough to carry private backfill text. -/
theorem publicProofFlowMergeDecision_localLedgerCoherent :
    publicProofFlowMergeDecision.localMachineLedgerCoherent = true :=
  rfl

/-- A11 has no terminal machine anchor available for public completion. -/
theorem publicProofFlowMergeDecision_no_terminalMachineAnchor :
    publicProofFlowMergeDecision.terminalMachineAnchorAvailable = false :=
  rfl

/-- A11 must not be merged directly by this worker into public docs. -/
theorem publicProofFlowMergeDecision_publicMergeBlocked :
    publicProofFlowMergeDecision.publicMergeAllowedNow = false :=
  rfl

/-- The current A11 decision is not a repo-local theorem completion. -/
theorem publicProofFlowMergeDecision_not_repoLocalCompleted :
    ¬ publicProofFlowMergeDecision.completionEffect.repoLocalCompleted := by
  simp [publicProofFlowMergeDecision, MachineStatus.repoLocalCompleted]

/--
Stage1 A12 README/meta/checklist synchronization decision.

The synchronization target is public project metadata, so this worker can only
record the gate.  The public docs must stay unchanged until a serial integrator
has merged the authoritative public Stage1 text and rerun the relevant build
validation for that merged state.
-/
structure ReadmeMetaStage1SyncDecision where
  publicMergeBackComplete : Bool
  buildValidationReadyForPublicSync : Bool
  readmeMetaChecklistSyncAllowedNow : Bool
  authoritativePublicTargets : List String
  requiredValidation : String
  blocker : String
  completionEffect : MachineStatus
  deriving DecidableEq, Repr

/--
Current A12 decision: do not synchronize README, metadata, or public Stage1
checkboxes from this child pass.
-/
def readmeMetaStage1SyncDecision : ReadmeMetaStage1SyncDecision where
  publicMergeBackComplete := false
  buildValidationReadyForPublicSync := false
  readmeMetaChecklistSyncAllowedNow := false
  authoritativePublicTargets := [
    "README.md",
    "Docs/Stage1_Blueprint.md",
    "Docs/todos_20260430.md",
    "the future THM-M-0396 meta/status surface selected by the serial integrator"
  ]
  requiredValidation :=
    "after serial public merge-back, rerun cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_009.lean; if the shared aggregator imports this file or a terminal wrapper/dependency exists, also rerun cd Formalizations/Lean && lake build"
  blocker :=
    "A11 public merge-back has not happened in this child pass, and no terminal Baker lower-bound wrapper or pinned dependency exists"
  completionEffect := .formalizationDebt

/-- A12 public merge-back has not been completed by this child. -/
theorem readmeMetaStage1SyncDecision_no_publicMergeBack :
    readmeMetaStage1SyncDecision.publicMergeBackComplete = false :=
  rfl

/-- A12 build validation is not yet sufficient for public metadata sync. -/
theorem readmeMetaStage1SyncDecision_no_publicSyncBuildValidation :
    readmeMetaStage1SyncDecision.buildValidationReadyForPublicSync = false :=
  rfl

/-- A12 public README/meta/checklist synchronization is currently blocked. -/
theorem readmeMetaStage1SyncDecision_publicSyncBlocked :
    readmeMetaStage1SyncDecision.readmeMetaChecklistSyncAllowedNow = false :=
  rfl

/-- The current A12 synchronization decision is not a repo-local theorem completion. -/
theorem readmeMetaStage1SyncDecision_not_repoLocalCompleted :
    ¬ readmeMetaStage1SyncDecision.completionEffect.repoLocalCompleted := by
  simp [readmeMetaStage1SyncDecision, MachineStatus.repoLocalCompleted]

#check IsAlgebraic
#check Complex.exp
#check Complex.log
#check linearForm
#check multiplicativeForm
#check multiplicativeForm_ne_zero
#check exp_linearForm_eq_multiplicativeForm
#check multiplicativeForm_eq_one_of_linearForm_eq_zero
#check linearForm_ne_zero_of_multiplicativeForm_ne_one
#check coefficientBound_covers_abs_coeff
#check degreeBound_positive_available
#check heightBound_large_enough_available
#check selectedLowerBoundConvention_heightParameterConvention
#check selectedLowerBoundConvention_coefficientBoundConvention
#check selectedLowerBoundConvention_logBranchConvention
#check BakerBridgeCertificate
#check bakerBridgeCertificate
#check bakerBridgeCertificate_not_terminal_completion
#check selectedLowerBoundConvention
#check selectedLowerBoundConvention_variant
#check selectedLowerBoundConvention_denominators_pos
#check statementNormalizationBoundary
#check TheoremSlotStatement
#check bakerProofPackageAudit
#check AuxiliaryCorePackage
#check AuxiliaryCoreLeafBudget
#check auxiliaryCoreLeafBudgetLedger
#check auxiliaryCoreLeafBudgetLedger_nonempty
#check auxiliaryCoreLeafBudgetLedger_withinM0387Budget
#check auxiliaryCoreLeafBudgetLedger_notRepoLocalCompletion
#check explicitLowerBoundInequality_mem_audit
#check terminalRepoLocalCompletionGate_not_satisfied
#check externalLeanPrimaryAuditRows
#check authenticatedGitHubCodeSearchAvailable_eq_false
#check exactExternalBakerTheoremIdentifiedByCompletedAudit_eq_false
#check externalBakerProofIntegrationDecision
#check externalBakerProofIntegrationDecision_no_exactProof
#check externalBakerProofIntegrationDecision_not_repoLocalCompleted
#check mathlibBakerWrapperDecision
#check mathlibBakerWrapperDecision_no_terminalTheorem
#check mathlibBakerWrapperDecision_not_repoLocalCompleted
#check TheoremLevelAuditRow
#check theoremLevelAuditTable
#check theoremLevelAuditTable_nonempty
#check theoremLevelAuditTable_notRepoLocalCompletion
#check theoremLevelAuditTable_contains_statementShape
#check theoremLevelAuditTable_contains_publicStatement
#check LocalBuildGateDecision
#check localBuildGateDecision
#check localBuildGateDecision_no_terminalWrapperOrDependency
#check localBuildGateDecision_not_repoLocalCompleted
#check PublicProofFlowMergeDecision
#check publicProofFlowMergeDecision
#check publicProofFlowMergeDecision_localLedgerCoherent
#check publicProofFlowMergeDecision_no_terminalMachineAnchor
#check publicProofFlowMergeDecision_publicMergeBlocked
#check publicProofFlowMergeDecision_not_repoLocalCompleted
#check ReadmeMetaStage1SyncDecision
#check readmeMetaStage1SyncDecision
#check readmeMetaStage1SyncDecision_no_publicMergeBack
#check readmeMetaStage1SyncDecision_no_publicSyncBuildValidation
#check readmeMetaStage1SyncDecision_publicSyncBlocked
#check readmeMetaStage1SyncDecision_not_repoLocalCompleted

end S1_M_009
end Stage1

namespace NumberTheory
namespace THM_M_0396

/-!
Statement-only public namespace for `THM-M-0396`.

This namespace intentionally re-exports the checked Stage1 object model rather
than proving Baker's theorem.  The terminal lower-bound proof remains governed
by `terminalRepoLocalCompletionGate`.
-/

/-- Public theorem namespace alias for the checked Baker input object model. -/
abbrev BakerLinearFormsInput :=
  Stage1.S1_M_009.BakerLinearFormsInput

/-- Public theorem namespace alias for abstract lower-bound output data. -/
abbrev BakerLowerBoundData :=
  Stage1.S1_M_009.BakerLowerBoundData

/-- Public theorem namespace alias for the selected lower-bound variant type. -/
abbrev BakerLowerBoundVariant :=
  Stage1.S1_M_009.BakerLowerBoundVariant

/-- Public theorem namespace alias for the selected constant convention record. -/
abbrev LowerBoundConstantConvention :=
  Stage1.S1_M_009.LowerBoundConstantConvention

/-- Public theorem namespace alias for the linear form `Λ = Σ b_i λ_i`. -/
abbrev linearForm (D : BakerLinearFormsInput) : ℂ :=
  Stage1.S1_M_009.linearForm D

/--
Statement-only target for `THM-M-0396`.

For algebraic nonzero inputs and chosen logarithms, every nonzero integer linear
form should have an effective positive lower bound.  This is a statement
surface only; no terminal Baker lower-bound proof is claimed here.
-/
def Statement : Prop :=
  Stage1.S1_M_009.StatementShape

/-- Selected public constant convention for the statement-only namespace. -/
def selectedLowerBoundConvention : LowerBoundConstantConvention :=
  Stage1.S1_M_009.selectedLowerBoundConvention

/-- The public namespace uses the checked Matveev 2000 convention selection. -/
theorem selectedLowerBoundConvention_variant :
    selectedLowerBoundConvention.variant =
      Stage1.S1_M_009.BakerLowerBoundVariant.matveev2000Multiplicative :=
  Stage1.S1_M_009.selectedLowerBoundConvention_variant

/-- The public namespace statement is definitionally the checked Stage1 shape. -/
theorem statement_eq_stage1_statement :
    Statement = Stage1.S1_M_009.StatementShape :=
  rfl

/--
Current completion gate for the public Baker theorem namespace.

This remains false until a local proof body, pinned upstream theorem, or other
repo-local validation closure is available.
-/
def terminalRepoLocalCompletionGate : Prop :=
  Stage1.S1_M_009.terminalRepoLocalCompletionGate

/-- The public Baker theorem namespace is not repo-locally completed yet. -/
theorem terminalRepoLocalCompletionGate_not_satisfied :
    ¬ terminalRepoLocalCompletionGate :=
  Stage1.S1_M_009.terminalRepoLocalCompletionGate_not_satisfied

#check Statement
#check selectedLowerBoundConvention
#check selectedLowerBoundConvention_variant
#check terminalRepoLocalCompletionGate_not_satisfied

end THM_M_0396
end NumberTheory
end AwesomeTheorems
