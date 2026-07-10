import Mathlib.NumberTheory.Chebyshev
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries
import Mathlib.NumberTheory.LSeries.Dirichlet
import Mathlib.NumberTheory.LSeries.RiemannZeta

/-!
# S1-M-258 / THM-M-0498: Riemann-von Mangoldt explicit formula

This Stage1 artifact records a conservative Lean 4 boundary for the
Riemann-von Mangoldt explicit formula for prime counting / weighted prime-power
counting.

The pinned mathlib snapshot already contains the von Mangoldt function, the
Chebyshev functions `psi` and `theta`, the prime counting function, Abel
summation bridges between `theta` and prime counting, the logarithmic derivative
identity for the von Mangoldt Dirichlet series, the Euler product for
`riemannZeta`, the residue at `1`, and the trivial zeta zeros.

This file does not claim the terminal explicit formula.  The contour-shift,
zero-enumeration, convergence, and transfer-to-prime-counting steps remain
explicit bridge fields.
-/

noncomputable section

open Nat Chebyshev ArithmeticFunction Asymptotics Filter Complex

open scoped Nat.Prime ArithmeticFunction Topology

namespace AwesomeTheorems.Stage1.S1_M_258

universe u

/-- The weighted prime-power counting function used in the explicit formula. -/
def weightedPrimePowerCounting (x : ℝ) : ℝ :=
  Chebyshev.psi x

/-- The logarithmically weighted prime-counting function. -/
def logarithmicPrimeCountingWeight (x : ℝ) : ℝ :=
  Chebyshev.theta x

/-- Prime counting at a real argument, represented through `Nat.floor`. -/
def primeCountingAtReal (x : ℝ) : ℝ :=
  (Nat.primeCounting ⌊x⌋₊ : ℝ)

/--
Normalized Stage1 data for a Riemann-von Mangoldt explicit formula.

`Z` is the selected zero-index type.  A later integrator should instantiate it
with a canonical enumeration or truncation/filter API for the nontrivial zeros
of `riemannZeta`.  The bridge fields name the analytic proof packages not yet
available as local repo proof bodies.
-/
structure ExplicitFormulaData (Z : Type u) where
  x : ℝ
  xLowerBound : 1 < x
  zero : Z → ℂ
  zero_is_zeta_zero : ∀ z : Z, riemannZeta (zero z) = 0
  zeroWeight : Z → ℂ
  zeroWeightSummable : Prop
  poleContribution : ℂ
  trivialZeroContribution : ℂ
  endpointCorrection : ℂ
  errorTerm : ℂ
  analyticContinuationBridge : Prop
  logarithmicDerivativeBridge : Prop
  contourShiftBridge : Prop
  zeroEnumerationBridge : Prop
  explicitPsiFormula_holds :
    (weightedPrimePowerCounting x : ℂ) =
      poleContribution - (∑' z : Z, zeroWeight z) -
        trivialZeroContribution - endpointCorrection + errorTerm
  primeCountingTransfer : Prop
  primeCountingTransfer_holds : primeCountingTransfer

/-- The weighted `psi` explicit-formula proposition associated to normalized data. -/
def PsiExplicitFormula {Z : Type u} (D : ExplicitFormulaData.{u} Z) : Prop :=
  (weightedPrimePowerCounting D.x : ℂ) =
    D.poleContribution - (∑' z : Z, D.zeroWeight z) -
      D.trivialZeroContribution - D.endpointCorrection + D.errorTerm

/--
The future terminal conclusion package.

The first conjunct is the weighted explicit formula for `psi`; the second is
the transfer package turning the weighted formula into the requested
prime-counting-function statement.
-/
def ExplicitFormulaConclusion {Z : Type u} (D : ExplicitFormulaData.{u} Z) : Prop :=
  PsiExplicitFormula D ∧ D.primeCountingTransfer

/--
Stage1 normalized statement shape for the Riemann-von Mangoldt explicit formula.

This is a theorem target, not a completed local proof.  The local checked
content below verifies the statement boundary and the currently available
mathlib-side anchors.
-/
def StatementShape : Prop :=
  ∀ (Z : Type u), ∀ D : ExplicitFormulaData.{u} Z,
    D.analyticContinuationBridge →
      D.logarithmicDerivativeBridge →
        D.contourShiftBridge →
          D.zeroEnumerationBridge →
            D.zeroWeightSummable →
              ExplicitFormulaConclusion D

/--
Public target options considered for the Stage1 statement backfill.

The selected option below keeps the `psi` explicit formula as the primary
machine target and records the prime-counting formula as a linked transfer
variant, instead of collapsing both into a prime-counting-only statement.
-/
inductive PublicStatementTarget where
  | psiExplicitFormulaFirst
  | primeCountingFormulaOnly
  | twoLinkedVariants
deriving DecidableEq, Repr

/--
Selected public target for this Stage1 slot: two linked statement variants,
with the `psi` explicit formula first and the prime-counting statement reached
through a separate transfer package.
-/
def selectedPublicStatementTarget : PublicStatementTarget :=
  .twoLinkedVariants

/-- The checked public-target decision for this Stage1 artifact. -/
theorem selectedPublicStatementTarget_eq :
    selectedPublicStatementTarget = PublicStatementTarget.twoLinkedVariants :=
  rfl

/-- Public prose synchronized with `selectedPublicStatementTarget`. -/
def selectedPublicStatementTargetNote : String :=
  "Use two linked variants: first a Chebyshev psi explicit formula, then a " ++
    "prime-counting pi transfer statement.  Do not present a pi-only formula " ++
    "as the primary Lean target before the psi formula and transfer package " ++
    "are separately checked."

/-- Public variant A: the weighted `psi` explicit formula is the primary target. -/
def PsiFirstPublicVariant : Prop :=
  ∀ (Z : Type u), ∀ D : ExplicitFormulaData.{u} Z,
    D.analyticContinuationBridge →
      D.logarithmicDerivativeBridge →
        D.contourShiftBridge →
          D.zeroEnumerationBridge →
            D.zeroWeightSummable →
              PsiExplicitFormula D

/--
Public variant B: the prime-counting statement is a linked transfer target,
not the first theorem to attempt directly.
-/
def PrimeCountingTransferPublicVariant : Prop :=
  ∀ (Z : Type u), ∀ D : ExplicitFormulaData.{u} Z,
    D.analyticContinuationBridge →
      D.logarithmicDerivativeBridge →
        D.contourShiftBridge →
          D.zeroEnumerationBridge →
            D.zeroWeightSummable →
              D.primeCountingTransfer

/-- The selected public shape is exactly the pair of linked variants. -/
def TwoLinkedPublicStatementVariants : Prop :=
  PsiFirstPublicVariant.{u} ∧ PrimeCountingTransferPublicVariant.{u}

/--
The existing statement shape is equivalent to the selected two-variant public
target: prove the `psi` formula first, then carry a separate prime-counting
transfer package.
-/
theorem statementShape_iff_twoLinkedPublicStatementVariants :
    StatementShape.{u} ↔ TwoLinkedPublicStatementVariants.{u} := by
  constructor
  · intro h
    constructor
    · intro Z D hAnalytic hLogDeriv hContour hZeros hSummable
      exact (h Z D hAnalytic hLogDeriv hContour hZeros hSummable).1
    · intro Z D hAnalytic hLogDeriv hContour hZeros hSummable
      exact (h Z D hAnalytic hLogDeriv hContour hZeros hSummable).2
  · intro h Z D hAnalytic hLogDeriv hContour hZeros hSummable
    exact ⟨h.1 Z D hAnalytic hLogDeriv hContour hZeros hSummable,
      h.2 Z D hAnalytic hLogDeriv hContour hZeros hSummable⟩

/-- The statement shape unfolds to its explicit bridge-implication form. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Z : Type u), ∀ D : ExplicitFormulaData.{u} Z,
        D.analyticContinuationBridge →
          D.logarithmicDerivativeBridge →
            D.contourShiftBridge →
              D.zeroEnumerationBridge →
                D.zeroWeightSummable →
                  ExplicitFormulaConclusion D :=
  Iff.rfl

/-- Machine-readable status for this Stage1 artifact. -/
inductive Stage1MachineStatus where
  | statementShapeAndMathlibAnchors
  | terminalExplicitFormulaClosed
deriving DecidableEq, Repr

/--
Current repo-local status: checked statement shape plus checked mathlib anchors,
not a closed proof of the Riemann-von Mangoldt explicit formula.
-/
def currentStage1MachineStatus : Stage1MachineStatus :=
  .statementShapeAndMathlibAnchors

/-- The current machine status is the non-terminal Stage1 boundary status. -/
theorem currentStage1MachineStatus_eq_statementShapeAndMathlibAnchors :
    currentStage1MachineStatus = Stage1MachineStatus.statementShapeAndMathlibAnchors :=
  rfl

/--
Projection wrapper for a future terminal explicit formula package.

This theorem only checks the intended conclusion type; it does not prove the
Riemann-von Mangoldt explicit formula.
-/
theorem terminalConclusion_project {Z : Type u} (D : ExplicitFormulaData.{u} Z) :
    ExplicitFormulaConclusion D :=
  ⟨D.explicitPsiFormula_holds, D.primeCountingTransfer_holds⟩

/-- Project the weighted `psi` explicit formula from the future conclusion package. -/
theorem terminal_psi_formula {Z : Type u} (D : ExplicitFormulaData.{u} Z)
    (h : ExplicitFormulaConclusion D) :
    (weightedPrimePowerCounting D.x : ℂ) =
      D.poleContribution - (∑' z : Z, D.zeroWeight z) -
        D.trivialZeroContribution - D.endpointCorrection + D.errorTerm :=
  h.1

/-- Project the prime-counting transfer package from the future conclusion package. -/
theorem terminal_primeCounting_transfer {Z : Type u} (D : ExplicitFormulaData.{u} Z)
    (h : ExplicitFormulaConclusion D) :
    D.primeCountingTransfer :=
  h.2

section MathlibAnchors

/-- The pinned mathlib commit used for the Riemann-von Mangoldt anchor audit. -/
def mathlibAuditCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Checked spelling of the pinned mathlib commit used by this audit. -/
theorem mathlibAuditCommit_eq :
    mathlibAuditCommit = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- A source-level mathlib anchor recorded for this Stage1 audit. -/
structure PinnedMathlibAnchor where
  displayName : String
  leanName : String
  moduleName : String
  sourceFile : String
  sourceLine : Nat
  sourceKind : String
  localWitness : String
  deriving Repr

/--
Required pinned mathlib anchors for the Riemann-von Mangoldt Stage1 audit.

These are local audit records only.  The theorem wrappers below are the checked
repo-local witnesses for the theorem-valued anchors and aliases; this table is
not a terminal explicit-formula proof.
-/
def requiredPinnedMathlibAnchors : List PinnedMathlibAnchor := [
  {
    displayName := "Chebyshev.psi",
    leanName := "Chebyshev.psi",
    moduleName := "Mathlib.NumberTheory.Chebyshev",
    sourceFile := "Mathlib/NumberTheory/Chebyshev.lean",
    sourceLine := 62,
    sourceKind := "def",
    localWitness := "weightedPrimePowerCounting"
  },
  {
    displayName := "Chebyshev.theta",
    leanName := "Chebyshev.theta",
    moduleName := "Mathlib.NumberTheory.Chebyshev",
    sourceFile := "Mathlib/NumberTheory/Chebyshev.lean",
    sourceLine := 69,
    sourceKind := "def",
    localWitness := "logarithmicPrimeCountingWeight"
  },
  {
    displayName := "ArithmeticFunction.vonMangoldt",
    leanName := "ArithmeticFunction.vonMangoldt",
    moduleName := "Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt",
    sourceFile := "Mathlib/NumberTheory/ArithmeticFunction/VonMangoldt.lean",
    sourceLine := 65,
    sourceKind := "def",
    localWitness := "vonMangoldt_sum_wrapper"
  },
  {
    displayName := "Nat.primeCounting",
    leanName := "Nat.primeCounting",
    moduleName := "Mathlib.NumberTheory.PrimeCounting",
    sourceFile := "Mathlib/NumberTheory/PrimeCounting.lean",
    sourceLine := 55,
    sourceKind := "def",
    localWitness := "primeCountingAtReal"
  },
  {
    displayName := "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div",
    leanName := "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div",
    moduleName := "Mathlib.NumberTheory.LSeries.Dirichlet",
    sourceFile := "Mathlib/NumberTheory/LSeries/Dirichlet.lean",
    sourceLine := 434,
    sourceKind := "lemma",
    localWitness := "LSeries_vonMangoldt_log_derivative_wrapper"
  },
  {
    displayName := "riemannZeta_eulerProduct_exp_log",
    leanName := "riemannZeta_eulerProduct_exp_log",
    moduleName := "Mathlib.NumberTheory.EulerProduct.DirichletLSeries",
    sourceFile := "Mathlib/NumberTheory/EulerProduct/DirichletLSeries.lean",
    sourceLine := 159,
    sourceKind := "theorem",
    localWitness := "riemannZeta_eulerProduct_exp_log_wrapper"
  },
  {
    displayName := "riemannZeta_residue_one",
    leanName := "riemannZeta_residue_one",
    moduleName := "Mathlib.NumberTheory.LSeries.RiemannZeta",
    sourceFile := "Mathlib/NumberTheory/LSeries/RiemannZeta.lean",
    sourceLine := 217,
    sourceKind := "lemma",
    localWitness := "riemannZeta_residue_one_wrapper"
  },
  {
    displayName := "riemannZeta_neg_two_mul_nat_add_one",
    leanName := "riemannZeta_neg_two_mul_nat_add_one",
    moduleName := "Mathlib.NumberTheory.LSeries.RiemannZeta",
    sourceFile := "Mathlib/NumberTheory/LSeries/RiemannZeta.lean",
    sourceLine := 149,
    sourceKind := "theorem",
    localWitness := "riemannZeta_trivial_zero_wrapper"
  }
]

/-- Count of required pinned mathlib anchors recorded by this audit child. -/
def requiredPinnedMathlibAnchorCount : Nat :=
  requiredPinnedMathlibAnchors.length

/-- The audit records exactly the eight mathlib anchors named in the child task. -/
theorem requiredPinnedMathlibAnchorCount_eq :
    requiredPinnedMathlibAnchorCount = 8 :=
  rfl

/-- Checked mathlib anchor: `theta` is bounded above by `psi`. -/
theorem theta_le_psi_wrapper (x : ℝ) :
    logarithmicPrimeCountingWeight x ≤ weightedPrimePowerCounting x :=
  Chebyshev.theta_le_psi x

/-- Checked mathlib anchor: `psi - theta` is the von Mangoldt mass of non-prime prime powers. -/
theorem psi_sub_theta_eq_sum_not_prime_wrapper (x : ℝ) :
    weightedPrimePowerCounting x - logarithmicPrimeCountingWeight x =
      ∑ n ∈ Finset.Ioc 0 ⌊x⌋₊ with ¬Nat.Prime n, ArithmeticFunction.vonMangoldt n :=
  Chebyshev.psi_sub_theta_eq_sum_not_prime x

/-- Checked mathlib anchor: Abel summation expresses prime counting through `theta`. -/
theorem primeCounting_eq_theta_div_log_add_integral_wrapper {x : ℝ} (hx : 2 ≤ x) :
    primeCountingAtReal x =
      logarithmicPrimeCountingWeight x / Real.log x +
        ∫ t in 2..x, logarithmicPrimeCountingWeight t / (t * Real.log t ^ 2) :=
  Chebyshev.primeCounting_eq_theta_div_log_add_integral hx

/-- Checked mathlib anchor: the Abel-summation error term is already available as a Big-O fact. -/
theorem primeCounting_sub_theta_div_log_isBigO_wrapper :
    (fun x : ℝ => primeCountingAtReal x - logarithmicPrimeCountingWeight x / Real.log x)
      =O[atTop] fun x : ℝ => x / Real.log x ^ 2 :=
  Chebyshev.primeCounting_sub_theta_div_log_isBigO

/-- Checked mathlib anchor: the divisor sum of the von Mangoldt function is `log n`. -/
theorem vonMangoldt_sum_wrapper {n : ℕ} :
    ∑ d ∈ n.divisors, ArithmeticFunction.vonMangoldt d = Real.log (n : ℝ) :=
  ArithmeticFunction.vonMangoldt_sum

/--
Checked mathlib anchor: the von Mangoldt Dirichlet series is the negative
logarithmic derivative of the Riemann zeta function on `re s > 1`.
-/
theorem LSeries_vonMangoldt_log_derivative_wrapper {s : ℂ} (hs : 1 < s.re) :
    LSeries (fun n : ℕ => ((ArithmeticFunction.vonMangoldt n : ℝ) : ℂ)) s =
      -deriv riemannZeta s / riemannZeta s :=
  ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div hs

/-- Checked mathlib anchor: Euler product for `riemannZeta` on `re s > 1`. -/
theorem riemannZeta_eulerProduct_exp_log_wrapper {s : ℂ} (hs : 1 < s.re) :
    cexp (∑' p : Nat.Primes, -Complex.log (1 - (p : ℂ) ^ (-s))) = riemannZeta s :=
  riemannZeta_eulerProduct_exp_log hs

/-- Checked mathlib anchor: residue of `riemannZeta` at `1`. -/
theorem riemannZeta_residue_one_wrapper :
    Tendsto (fun s : ℂ => (s - 1) * riemannZeta s) (𝓝[≠] 1) (𝓝 1) :=
  riemannZeta_residue_one

/-- Checked mathlib anchor: the negative even integers are trivial zeros of `riemannZeta`. -/
theorem riemannZeta_trivial_zero_wrapper (n : ℕ) :
    riemannZeta (-2 * ((n : ℂ) + 1)) = 0 :=
  riemannZeta_neg_two_mul_nat_add_one n

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.PrimeCounting",
  "Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt",
  "Mathlib.NumberTheory.Chebyshev",
  "Mathlib.NumberTheory.AbelSummation",
  "Mathlib.NumberTheory.LSeries.RiemannZeta",
  "Mathlib.NumberTheory.LSeries.Dirichlet",
  "Mathlib.NumberTheory.EulerProduct.DirichletLSeries",
  "Mathlib.NumberTheory.LSeries.Nonvanishing",
  "Mathlib.Analysis.Asymptotics.Asymptotics"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "Nat.primeCounting",
  "Nat.primeCounting'",
  "ArithmeticFunction.vonMangoldt",
  "ArithmeticFunction.vonMangoldt_sum",
  "Chebyshev.psi",
  "Chebyshev.theta",
  "Chebyshev.theta_le_psi",
  "Chebyshev.psi_sub_theta_eq_sum_not_prime",
  "Chebyshev.primeCounting_eq_theta_div_log_add_integral",
  "Chebyshev.primeCounting_sub_theta_div_log_isBigO",
  "riemannZeta",
  "riemannZeta_eulerProduct_exp_log",
  "riemannZeta_residue_one",
  "riemannZeta_neg_two_mul_nat_add_one",
  "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div"
]

/--
Search terms that did not locate a terminal Riemann-von Mangoldt explicit
formula theorem in the local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Riemann-von Mangoldt explicit formula",
  "Riemann von Mangoldt",
  "explicit formula prime counting",
  "explicit_formula",
  "PrimeNumberTheorem explicit formula",
  "nontrivial zeros explicit formula",
  "zero counting explicit formula",
  "vonMangoldt explicit"
]

/-- Primary-source URLs/revisions for the local mathlib anchors audited here. -/
def primarySourceAnchors : List String := [
  "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95: Mathlib/NumberTheory/Chebyshev.lean",
  "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95: Mathlib/NumberTheory/ArithmeticFunction/VonMangoldt.lean",
  "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95: Mathlib/NumberTheory/PrimeCounting.lean",
  "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95: Mathlib/NumberTheory/LSeries/Dirichlet.lean",
  "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95: Mathlib/NumberTheory/LSeries/RiemannZeta.lean",
  "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95: Mathlib/NumberTheory/EulerProduct/DirichletLSeries.lean"
]

end MathlibAnchors

section ExternalPrimeNumberTheoremAndAudit

/--
Pinned external audit target for `AlexKontorovich/PrimeNumberTheoremAnd`.

The audit result below is an integration-blocker record, not imported proof
evidence.  The terminal-shaped zero-counting and explicit-formula statements
located at this commit use incomplete proof placeholders in the external tree.
-/
def primeNumberTheoremAndAuditCommit : String :=
  "baff9f946bcb5349d35b3eba72e28031748e6388"

/-- Checked spelling of the external audit commit. -/
theorem primeNumberTheoremAndAuditCommit_eq :
    primeNumberTheoremAndAuditCommit = "baff9f946bcb5349d35b3eba72e28031748e6388" :=
  rfl

/-- External branch audited for `AlexKontorovich/PrimeNumberTheoremAnd`. -/
def primeNumberTheoremAndAuditBranch : String :=
  "main"

/-- External Lean toolchain declared by the audited project. -/
def primeNumberTheoremAndAuditToolchain : String :=
  "leanprover/lean4:v4.28.0"

/-- Status vocabulary for the external `PrimeNumberTheoremAnd` terminal audit. -/
inductive ExternalTerminalAuditStatus where
  | terminalStatementPresentButBlockedByPlaceholder
  | closedTerminalProofCandidate
deriving DecidableEq, Repr

/--
Current external audit status.

The audited project contains relevant terminal-shaped statements, but they are
not usable as `pin/import/check` completion evidence while their proof bodies
remain placeholder-backed.
-/
def primeNumberTheoremAndTerminalAuditStatus : ExternalTerminalAuditStatus :=
  .terminalStatementPresentButBlockedByPlaceholder

/-- The external audit is blocked by placeholder-backed terminal-shaped statements. -/
theorem primeNumberTheoremAndTerminalAuditStatus_eq :
    primeNumberTheoremAndTerminalAuditStatus =
      ExternalTerminalAuditStatus.terminalStatementPresentButBlockedByPlaceholder :=
  rfl

/-- A source-level external audit record for `PrimeNumberTheoremAnd`. -/
structure ExternalPrimeNumberTheoremAndAnchor where
  displayName : String
  leanName : String
  moduleName : String
  sourceFile : String
  sourceLine : Nat
  sourceKind : String
  proofStatus : String
  integrationClassification : String
  deriving Repr

/--
Relevant external anchors found in `AlexKontorovich/PrimeNumberTheoremAnd`.

The terminal-shaped zero-counting and explicit-formula entries are not
repo-local closure evidence because the audited external source uses
incomplete proof placeholders for those proof bodies.  Importing them as-is
would leave an unacceptable M0387 integration blocker for this Stage1 theorem.
-/
def primeNumberTheoremAndExternalAnchors : List ExternalPrimeNumberTheoremAndAnchor := [
  {
    displayName := "zeroes_sum",
    leanName := "riemannZeta.zeroes_sum",
    moduleName := "PrimeNumberTheoremAnd.ZetaDefinitions",
    sourceFile := "PrimeNumberTheoremAnd/ZetaDefinitions.lean",
    sourceLine := 107,
    sourceKind := "def",
    proofStatus := "definition",
    integrationClassification := "adjacent_zero_api_only"
  },
  {
    displayName := "zero-counting function N(T)",
    leanName := "riemannZeta.N",
    moduleName := "PrimeNumberTheoremAnd.ZetaDefinitions",
    sourceFile := "PrimeNumberTheoremAnd/ZetaDefinitions.lean",
    sourceLine := 137,
    sourceKind := "def",
    proofStatus := "definition",
    integrationClassification := "adjacent_zero_api_only"
  },
  {
    displayName := "Riemann-von-Mangoldt bound proposition",
    leanName := "riemannZeta.Riemann_vonMangoldt_bound",
    moduleName := "PrimeNumberTheoremAnd.ZetaDefinitions",
    sourceFile := "PrimeNumberTheoremAnd/ZetaDefinitions.lean",
    sourceLine := 161,
    sourceKind := "def",
    proofStatus := "proposition_schema",
    integrationClassification := "statement_schema_only"
  },
  {
    displayName := "Hasanalizade-Shen-Wang RvM bound",
    leanName := "HSW.main_theorem",
    moduleName := "PrimeNumberTheoremAnd.ZetaSummary",
    sourceFile := "PrimeNumberTheoremAnd/ZetaSummary.lean",
    sourceLine := 35,
    sourceKind := "theorem",
    proofStatus := "placeholder",
    integrationClassification := "concrete_integration_blocker"
  },
  {
    displayName := "Rosser-Schoenfeld RvM bound",
    leanName := "RS.theorem_19",
    moduleName := "PrimeNumberTheoremAnd.RosserSchoenfeldZeta",
    sourceFile := "PrimeNumberTheoremAnd/RosserSchoenfeldZeta.lean",
    sourceLine := 18,
    sourceKind := "theorem",
    proofStatus := "placeholder",
    integrationClassification := "concrete_integration_blocker"
  },
  {
    displayName := "BKLNW/Dudek truncated psi explicit formula",
    leanName := "BKLNW_app.bklnw_eq_A_7",
    moduleName := "PrimeNumberTheoremAnd.BKLNW_app",
    sourceFile := "PrimeNumberTheoremAnd/BKLNW_app.lean",
    sourceLine := 47,
    sourceKind := "theorem",
    proofStatus := "placeholder",
    integrationClassification := "concrete_integration_blocker"
  },
  {
    displayName := "FKS theorem 3.2 truncated psi explicit formula",
    leanName := "FKS.theorem_3_2",
    moduleName := "PrimeNumberTheoremAnd.FioriKadiriSwidinsky",
    sourceFile := "PrimeNumberTheoremAnd/FioriKadiriSwidinsky.lean",
    sourceLine := 341,
    sourceKind := "theorem",
    proofStatus := "placeholder",
    integrationClassification := "concrete_integration_blocker"
  },
  {
    displayName := "Buthe2 RH-up-to psi bound",
    leanName := "Buthe2.theorem_2a",
    moduleName := "PrimeNumberTheoremAnd.TMEEMT",
    sourceFile := "PrimeNumberTheoremAnd/TMEEMT.lean",
    sourceLine := 40,
    sourceKind := "theorem",
    proofStatus := "placeholder",
    integrationClassification := "concrete_integration_blocker"
  },
  {
    displayName := "CH2 RH-up-to psi bound",
    leanName := "CH2.cor_1_3_a",
    moduleName := "PrimeNumberTheoremAnd.CH2",
    sourceFile := "PrimeNumberTheoremAnd/CH2.lean",
    sourceLine := 4280,
    sourceKind := "theorem",
    proofStatus := "placeholder",
    integrationClassification := "concrete_integration_blocker"
  }
]

/-- Number of external anchors recorded by this child audit. -/
def primeNumberTheoremAndExternalAnchorCount : Nat :=
  primeNumberTheoremAndExternalAnchors.length

/-- This child records the nine external anchors listed above. -/
theorem primeNumberTheoremAndExternalAnchorCount_eq :
    primeNumberTheoremAndExternalAnchorCount = 9 :=
  rfl

/-- Search terms used when auditing the external project for terminal evidence. -/
def primeNumberTheoremAndExternalAuditSearchTerms : List String := [
  "Riemann_vonMangoldt_bound",
  "riemannZeta.N",
  "riemannZeta.N'",
  "zero_density_bound",
  "zeroes_sum",
  "explicit formula",
  "psi(x) - x",
  "Chebyshev function",
  "placeholder",
  "unsafe declaration"
]

end ExternalPrimeNumberTheoremAndAudit

section PublicStatementTargetDecision

/--
Public statement-shape options for `THM-M-0498`.

The Stage1 source phrase says "prime counting", but the checked local analytic
boundary is safer if the weighted Chebyshev `psi` formula is the first theorem
target and the prime-counting formula is a linked transfer target.
-/
inductive PublicExplicitFormulaTarget where
  | psiFormulaFirst
  | primeCountingFormulaFirst
  | linkedPsiFormulaThenPrimeCountingTransfer
deriving DecidableEq, Repr

/--
Recommended public theorem-shape decision for this child task.

Use two linked statement variants: a primary `psi` explicit formula and a
secondary prime-counting transfer package.  This matches the local Lean
definitions `PsiExplicitFormula` and `ExplicitFormulaConclusion`.
-/
def recommendedPublicExplicitFormulaTarget : PublicExplicitFormulaTarget :=
  .linkedPsiFormulaThenPrimeCountingTransfer

/-- Checked spelling of the recommended public statement-shape decision. -/
theorem recommendedPublicExplicitFormulaTarget_eq :
    recommendedPublicExplicitFormulaTarget =
      PublicExplicitFormulaTarget.linkedPsiFormulaThenPrimeCountingTransfer :=
  rfl

/-- Machine-readable audit row for the public statement-shape decision. -/
structure PublicStatementTargetDecision where
  recommendedTarget : PublicExplicitFormulaTarget
  primaryLeanTarget : String
  linkedTransferTarget : String
  reason : String
  completionBoundary : String
  deriving Repr

/--
Integration-ready decision record for the public blueprint.

This is documentation data checked by Lean.  It does not prove the terminal
Riemann-von Mangoldt explicit formula.
-/
def publicStatementTargetDecision : PublicStatementTargetDecision where
  recommendedTarget := recommendedPublicExplicitFormulaTarget
  primaryLeanTarget :=
    "PsiExplicitFormula: weighted prime-power counting through Chebyshev.psi"
  linkedTransferTarget :=
    "ExplicitFormulaConclusion: PsiExplicitFormula plus primeCountingTransfer"
  reason :=
    "The psi formula is the natural analytic explicit-formula target; prime-counting pi needs Abel/endpoint/convergence transfer and should remain a linked secondary variant."
  completionBoundary :=
    "statement-shape decision only; Perron, contour shift, zero enumeration, convergence, endpoint corrections, and psi-to-pi transfer remain open formalization debt"

/-- The decision record selects the linked `psi`-then-prime-counting target. -/
theorem publicStatementTargetDecision_recommendedTarget :
    publicStatementTargetDecision.recommendedTarget =
      PublicExplicitFormulaTarget.linkedPsiFormulaThenPrimeCountingTransfer :=
  rfl

/-- The primary public Lean target remains the weighted `psi` explicit formula. -/
theorem publicStatementTargetDecision_primaryLeanTarget :
    publicStatementTargetDecision.primaryLeanTarget =
      "PsiExplicitFormula: weighted prime-power counting through Chebyshev.psi" :=
  rfl

/-- The linked public target records the later prime-counting transfer package. -/
theorem publicStatementTargetDecision_linkedTransferTarget :
    publicStatementTargetDecision.linkedTransferTarget =
      "ExplicitFormulaConclusion: PsiExplicitFormula plus primeCountingTransfer" :=
  rfl

end PublicStatementTargetDecision

section PackageLeafLedgerSplit

/--
Independent proof-package buckets that must be split into `<=100`-step leaf
ledgers before any completion checkbox for `THM-M-0498` is changed.

These are planning atoms, not proof evidence for the terminal explicit formula.
-/
inductive RiemannVonMangoldtProofPackage where
  | perronOrInverseMellin
  | contourShift
  | zeroEnumeration
  | zeroSumConvergence
  | primeCountingTransfer
deriving DecidableEq, Repr

/-- A machine-readable row for one Stage1 leaf-ledger package. -/
structure RiemannVonMangoldtLeafLedger where
  package : RiemannVonMangoldtProofPackage
  ledgerId : String
  packageBoundary : String
  independenceCriterion : String
  leafBudgetBound : Nat
  completionGate : String
  deriving Repr

/--
Required independent `<=100` leaf-ledger split for the Riemann-von Mangoldt
Stage1 proof tree.

The split keeps each analytic package separate so an integrator cannot mark
the parent theorem completed from a single anchor-only or statement-shape row.
-/
def requiredLeafLedgerSplit : List RiemannVonMangoldtLeafLedger := [
  {
    package := .perronOrInverseMellin,
    ledgerId := "S1-M-258.leaf.perron-or-inverse-mellin",
    packageBoundary :=
      "derive the weighted psi formula from the logarithmic derivative by Perron/inverse-Mellin truncation"
    independenceCriterion :=
      "does not own contour deformation, zero enumeration, zero-sum convergence, or psi-to-pi transfer"
    leafBudgetBound := 100,
    completionGate :=
      "closed only after local Lean lemmas for the transform, truncation, and boundary error validate without placeholders"
  },
  {
    package := .contourShift,
    ledgerId := "S1-M-258.leaf.contour-shift",
    packageBoundary :=
      "move the Perron contour and account for residues at the zeta pole, nontrivial zeros, trivial zeros, and endpoints"
    independenceCriterion :=
      "assumes an input transform identity and a chosen zero API, but does not prove zero enumeration or psi-to-pi transfer"
    leafBudgetBound := 100,
    completionGate :=
      "closed only after local Lean lemmas for contour geometry, residue accounting, and horizontal/vertical bounds validate"
  },
  {
    package := .zeroEnumeration,
    ledgerId := "S1-M-258.leaf.zero-enumeration",
    packageBoundary :=
      "choose and prove the nontrivial-zero indexing/truncation API used by the explicit formula"
    independenceCriterion :=
      "does not own Perron transform, contour estimates, convergence of the zero sum, or prime-counting transfer"
    leafBudgetBound := 100,
    completionGate :=
      "closed only after local Lean lemmas connect the selected index type with riemannZeta zeros and truncation filters"
  },
  {
    package := .zeroSumConvergence,
    ledgerId := "S1-M-258.leaf.zero-sum-convergence",
    packageBoundary :=
      "prove the summability/truncation/error semantics for the zero contribution appearing in the psi formula"
    independenceCriterion :=
      "uses the selected zero enumeration and analytic bounds, but does not own the transform or pi transfer"
    leafBudgetBound := 100,
    completionGate :=
      "closed only after local Lean lemmas validate the zero-weight summability or truncation-limit convention"
  },
  {
    package := .primeCountingTransfer,
    ledgerId := "S1-M-258.leaf.prime-counting-transfer",
    packageBoundary :=
      "transfer the checked psi/theta explicit formula to the requested prime-counting pi statement"
    independenceCriterion :=
      "depends on the psi formula as an input and separately owns Abel summation, endpoint corrections, and floor conventions"
    leafBudgetBound := 100,
    completionGate :=
      "closed only after local Lean lemmas validate the Chebyshev theta bridge and Nat.primeCounting real-argument transfer"
  }
]

/-- The required split has exactly the five independent packages named by C005. -/
theorem requiredLeafLedgerSplit_count_eq :
    requiredLeafLedgerSplit.length = 5 :=
  rfl

/-- Each required package row is budgeted as a `<=100` leaf-ledger target. -/
theorem requiredLeafLedgerSplit_budgetBounds_eq :
    requiredLeafLedgerSplit.map (fun row => row.leafBudgetBound) =
      [100, 100, 100, 100, 100] :=
  rfl

/-- Current status of the package split gate. -/
inductive PackageLeafLedgerGateStatus where
  | splitRecordedNoCompletion
  | allLeafLedgersLocallyClosed
deriving DecidableEq, Repr

/--
Current gate status: the independent package split is recorded, but the local
proof leaves remain open formalization debt.
-/
def packageLeafLedgerGateStatus : PackageLeafLedgerGateStatus :=
  .splitRecordedNoCompletion

/-- Checked spelling of the current non-completion package-ledger gate. -/
theorem packageLeafLedgerGateStatus_eq :
    packageLeafLedgerGateStatus = PackageLeafLedgerGateStatus.splitRecordedNoCompletion :=
  rfl

/--
Machine-readable completion warning for public backfill.

This string is intentionally conservative: the split can be merged as planning
progress, but it cannot justify theorem completion.
-/
def packageLeafLedgerCompletionWarning : String :=
  "Do not mark THM-M-0498 completed until the Perron/inverse-Mellin, contour-shift, zero-enumeration, zero-sum-convergence, and prime-counting-transfer leaf ledgers are each locally closed with Lean validation."

/-- Checked public completion warning for the package-ledger split. -/
theorem packageLeafLedgerCompletionWarning_eq :
    packageLeafLedgerCompletionWarning =
      "Do not mark THM-M-0498 completed until the Perron/inverse-Mellin, contour-shift, zero-enumeration, zero-sum-convergence, and prime-counting-transfer leaf ledgers are each locally closed with Lean validation." :=
  rfl

end PackageLeafLedgerSplit

end AwesomeTheorems.Stage1.S1_M_258
