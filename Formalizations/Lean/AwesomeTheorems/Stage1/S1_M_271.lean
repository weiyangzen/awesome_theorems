import Mathlib.Probability.CDF
import Mathlib.Probability.CentralLimitTheorem

/-!
# S1-M-271 / THM-M-0991: Berry-Esseen theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
one-dimensional i.i.d. Berry-Esseen theorem.

The pinned mathlib snapshot contains the one-dimensional i.i.d. central limit
theorem, Gaussian real distributions, cumulative distribution functions, laws,
independence, identical distribution, variance, and `MemLp` moment predicates.
It does not expose a terminal theorem giving a uniform CDF error bound of
Berry-Esseen type.  The declarations below therefore freeze the statement
shape and add checked wrappers around the available mathlib anchors.  No
terminal Berry-Esseen proof is claimed here.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Real Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_271

universe uΩ uΩ'

/--
Data package for a standard one-dimensional i.i.d. Berry-Esseen statement.

`sigma` is the positive standard deviation, `rho` bounds the third absolute
central moment, and `constant` is the universal Berry-Esseen constant.  The
fields are intentionally explicit because the terminal rate theorem is not
available in the local mathlib dependency closure.
-/
structure BerryEsseenIIDData
    (Ω : Type uΩ) [MeasurableSpace Ω] : Type uΩ where
  P : Measure Ω
  isProbability : IsProbabilityMeasure P
  X : ℕ → Ω → ℝ
  mean : ℝ
  sigma : ℝ
  rho : ℝ
  constant : ℝ
  sigma_pos : 0 < sigma
  rho_nonneg : 0 ≤ rho
  constant_nonneg : 0 ≤ constant
  mean_eq : P[X 0] = mean
  variance_eq : variance (X 0) P = sigma ^ 2
  third_abs_integrable : Integrable (fun ω => |X 0 ω - mean| ^ 3) P
  third_abs_moment_le : P[fun ω => |X 0 ω - mean| ^ 3] ≤ rho
  independent : iIndepFun X P
  identDistrib : ∀ i : ℕ, IdentDistrib (X i) (X 0) P P

/-- Centered partial sum of the first `n` coordinates. -/
def centeredSum
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω)
    (n : ℕ) (ω : Ω) : ℝ :=
  ∑ k ∈ Finset.range n, D.X k ω - (n : ℝ) * D.mean

/--
The normalized partial sum used in the classical Berry-Esseen bound:
`(S_n - n μ) / (σ sqrt n)`.

The value at `n = 0` is harmless because the conclusion quantifies over
positive `n`.
-/
def normalizedSum
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω)
    (n : ℕ) (ω : Ω) : ℝ :=
  (D.sigma * √(n : ℝ))⁻¹ * centeredSum D n ω

/-- The real probability law of the normalized sum under the source measure. -/
def normalizedSumLaw
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω)
    (n : ℕ) : Measure ℝ :=
  D.P.map (normalizedSum D n)

/-- Pointwise CDF error against the standard Gaussian CDF. -/
def cdfError
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω)
    (n : ℕ) (x : ℝ) : ℝ :=
  |cdf (normalizedSumLaw D n) x - cdf (gaussianReal 0 1) x|

/--
Berry-Esseen conclusion in pointwise-uniform CDF form.

The usual `sup_x` formulation is represented by the equivalent pointwise
upper bound for every `x`.
-/
def BerryEsseenConclusion
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω) : Prop :=
  ∀ n : ℕ, 0 < n →
    ∀ x : ℝ,
      cdfError D n x ≤ D.constant * D.rho / (D.sigma ^ 3 * √(n : ℝ))

/--
Stage1 normalized statement shape for the i.i.d. Berry-Esseen theorem.

This is a statement boundary only.  It deliberately does not assert a local
proof of the rate theorem.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) [MeasurableSpace Ω],
    ∀ D : BerryEsseenIIDData Ω,
      BerryEsseenConclusion D

/-- The statement-shape definition unfolds to the explicit data-parametrized form. -/
theorem statementShape_iff :
    StatementShape.{uΩ} ↔
      ∀ (Ω : Type uΩ) [MeasurableSpace Ω],
        ∀ D : BerryEsseenIIDData Ω,
          BerryEsseenConclusion D :=
  Iff.rfl

/-- Checked Stage1 boundary-audit row for the Berry-Esseen statement shape. -/
structure StatementShapeBoundaryAudit where
  artifactPath : String
  validatedDeclaration : String
  boundaryKind : String
  terminalProofCompletionClaim : Bool
  completedStateRepoLocalIntegrationDebt : Bool

/-- Public-backfill note carried by the checked Lean artifact. -/
def statementShapeBoundaryAudit : StatementShapeBoundaryAudit where
  artifactPath := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_271.lean"
  validatedDeclaration := "AwesomeTheorems.Stage1.S1_M_271.StatementShape"
  boundaryKind := "Berry-Esseen CDF-rate statement boundary; not terminal proof completion"
  terminalProofCompletionClaim := false
  completedStateRepoLocalIntegrationDebt := false

/-- The checked boundary-audit row does not claim a terminal Berry-Esseen proof. -/
theorem statementShapeBoundaryAudit_no_terminal_completion :
    statementShapeBoundaryAudit.terminalProofCompletionClaim = false :=
  rfl

/--
M0387 gate for this statement-shape child: no completed state is claimed, and
therefore no completed state retains repo-local integration debt.
-/
theorem statementShapeBoundaryAudit_no_completed_integration_debt :
    statementShapeBoundaryAudit.completedStateRepoLocalIntegrationDebt = false :=
  rfl

/--
Current repo-local machine status for the terminal Berry-Esseen CDF-rate
theorem.  The local artifact contains a checked statement boundary and adjacent
mathlib anchors, but not a terminal quantitative rate proof.
-/
def currentMachineStatus : String :=
  "not_repo_local_closed"

/--
Current machine-proof debt class for the terminal Berry-Esseen CDF-rate theorem:
the classical theorem is mathematically known, but this repository dependency
closure does not contain a Lean proof of the uniform CDF-rate bound.
-/
def currentMachineDebtClass : String :=
  "formalization_debt"

/--
Audit flag for the specific blocker behind `currentMachineDebtClass`.

`false` means no theorem in the local mathlib dependency closure has been
identified that proves the terminal Berry-Esseen uniform CDF-rate statement.
-/
def terminalCDFRateProofInLocalClosure : Bool :=
  false

/-- The local dependency closure does not currently contain the terminal CDF-rate proof. -/
theorem terminalCDFRateProofInLocalClosure_eq_false :
    terminalCDFRateProofInLocalClosure = false :=
  rfl

/-- The checked debt marker is the expected M0387 debt class for this open theorem. -/
theorem currentMachineDebtClass_eq :
    currentMachineDebtClass = "formalization_debt" :=
  rfl

/-- Projection wrapper: the source measure is a probability measure. -/
theorem source_isProbability
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω) :
    IsProbabilityMeasure D.P :=
  D.isProbability

/-- Projection wrapper: the input sequence is independent. -/
theorem sequence_iIndepFun
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω) :
    iIndepFun D.X D.P :=
  D.independent

/-- Projection wrapper: every coordinate has the same distribution as `X 0`. -/
theorem coordinate_identDistrib_zero
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω) (i : ℕ) :
    IdentDistrib (D.X i) (D.X 0) D.P D.P :=
  D.identDistrib i

/-- Projection wrapper: the variance normalization is part of the statement data. -/
theorem variance_eq_sigma_sq
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω) :
    variance (D.X 0) D.P = D.sigma ^ 2 :=
  D.variance_eq

/-- Projection wrapper: the third absolute central moment is integrable. -/
theorem third_abs_integrable
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω) :
    Integrable (fun ω => |D.X 0 ω - D.mean| ^ 3) D.P :=
  D.third_abs_integrable

/-- The normalized-sum notation unfolds to the CDF-rate expression. -/
theorem normalizedSum_apply
    {Ω : Type uΩ} [MeasurableSpace Ω] (D : BerryEsseenIIDData Ω)
    (n : ℕ) (ω : Ω) :
    normalizedSum D n ω =
      (D.sigma * √(n : ℝ))⁻¹ *
        (∑ k ∈ Finset.range n, D.X k ω - (n : ℝ) * D.mean) :=
  rfl

/-- CDFs are nonnegative in the pinned mathlib API. -/
theorem cdf_nonneg_mathlib_wrapper (μ : Measure ℝ) (x : ℝ) :
    0 ≤ cdf μ x :=
  ProbabilityTheory.cdf_nonneg μ x

/-- CDFs are bounded above by `1` in the pinned mathlib API. -/
theorem cdf_le_one_mathlib_wrapper (μ : Measure ℝ) (x : ℝ) :
    cdf μ x ≤ 1 :=
  ProbabilityTheory.cdf_le_one μ x

/-- The standard Gaussian measure is a probability measure in the pinned mathlib API. -/
theorem standardGaussian_isProbability_mathlib_wrapper :
    IsProbabilityMeasure (gaussianReal 0 1) :=
  inferInstance

/--
Checked adjacent anchor: mathlib's one-dimensional i.i.d. CLT for centered
`sqrt n`-scaled sums.

This is weaker than Berry-Esseen because it gives convergence in distribution,
not a quantitative uniform CDF rate.
-/
theorem centralLimitTheorem_mathlib_wrapper
    {Ω : Type uΩ} {Ω' : Type uΩ'} [MeasurableSpace Ω] [MeasurableSpace Ω']
    {P : Measure Ω} {P' : Measure Ω'} [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    {X : ℕ → Ω → ℝ} {Y : Ω' → ℝ}
    (hY : HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P')
    (hX : MemLp (X 0) 2 P)
    (hindep : iIndepFun X P)
    (hident : ∀ i : ℕ, IdentDistrib (X i) (X 0) P P) :
    TendstoInDistribution
      (fun (n : ℕ) (ω : Ω) =>
        (√(n : ℝ))⁻¹ * (∑ k ∈ Finset.range n, X k ω - (n : ℝ) * P[X 0]))
      atTop Y (fun _ : ℕ => P) P' :=
  ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
    hY hX hindep hident

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.CentralLimitTheorem",
  "Mathlib.Probability.CDF",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.CharacteristicFunction",
  "Mathlib.Probability.Moments.Variance",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic"
]

/-- Checked declaration names used or audited as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub",
  "MeasureTheory.TendstoInDistribution",
  "ProbabilityTheory.cdf",
  "ProbabilityTheory.cdf_nonneg",
  "ProbabilityTheory.cdf_le_one",
  "ProbabilityTheory.ofReal_cdf",
  "ProbabilityTheory.cdf_eq_real",
  "ProbabilityTheory.gaussianReal",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.IdentDistrib",
  "MeasureTheory.MemLp",
  "ProbabilityTheory.variance"
]

/-- One integration-ready row for the public Berry-Esseen mathlib anchor list. -/
structure MathlibAnchorRow where
  anchor : String
  importedBy : String
  repoLocalRole : String
  terminalBerryEsseenProof : Bool

/--
Checked mathlib anchor list requested by `S1-M-271-P03`.

These rows are audit metadata for the adjacent APIs used by the statement-shape
artifact.  The final field is deliberately `false` throughout: none of these
anchors is a terminal Berry-Esseen uniform CDF-rate theorem.
-/
def requestedMathlibAnchorTable : List MathlibAnchorRow := [
  { anchor := "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub",
    importedBy := "Mathlib.Probability.CentralLimitTheorem",
    repoLocalRole := "adjacent one-dimensional iid CLT anchor wrapped by centralLimitTheorem_mathlib_wrapper",
    terminalBerryEsseenProof := false },
  { anchor := "ProbabilityTheory.cdf",
    importedBy := "Mathlib.Probability.CDF",
    repoLocalRole := "CDF API used in cdfError and checked by CDF bound wrappers",
    terminalBerryEsseenProof := false },
  { anchor := "ProbabilityTheory.gaussianReal",
    importedBy := "Mathlib.Probability.CentralLimitTheorem",
    repoLocalRole := "standard Gaussian measure used as the Berry-Esseen comparison law",
    terminalBerryEsseenProof := false },
  { anchor := "ProbabilityTheory.HasLaw",
    importedBy := "Mathlib.Probability.CentralLimitTheorem",
    repoLocalRole := "law hypothesis used by the adjacent CLT wrapper",
    terminalBerryEsseenProof := false },
  { anchor := "ProbabilityTheory.iIndepFun",
    importedBy := "Mathlib.Probability.CentralLimitTheorem",
    repoLocalRole := "iid independence predicate in BerryEsseenIIDData and the adjacent CLT wrapper",
    terminalBerryEsseenProof := false },
  { anchor := "ProbabilityTheory.IdentDistrib",
    importedBy := "Mathlib.Probability.CentralLimitTheorem",
    repoLocalRole := "identical-distribution predicate in BerryEsseenIIDData and the adjacent CLT wrapper",
    terminalBerryEsseenProof := false },
  { anchor := "MeasureTheory.MemLp",
    importedBy := "Mathlib.Probability.CentralLimitTheorem",
    repoLocalRole := "second-moment integrability hypothesis for the adjacent CLT wrapper",
    terminalBerryEsseenProof := false },
  { anchor := "ProbabilityTheory.variance",
    importedBy := "Mathlib.Probability.CentralLimitTheorem",
    repoLocalRole := "variance normalization used by BerryEsseenIIDData and the adjacent CLT wrapper",
    terminalBerryEsseenProof := false }
]

/-- Integration-ready public theorem-tree package row for Berry-Esseen. -/
structure TheoremTreePackageRow where
  packageId : String
  role : String
  upstreamInputs : String
  downstreamOutput : String
  leafIds : List String
  leafStatus : String
  terminalProofClaim : Bool

/-!
Public theorem-tree split proposed for `S1-M-271-P04`.

Every package row is intentionally marked with `leafStatus := "unchecked"` and
`terminalProofClaim := false`: this is a proof-tree skeleton, not a completed
Berry-Esseen proof ledger.
-/
namespace BE

/-- `BE.Pkg01`: normalize the i.i.d. data and target statement. -/
def Pkg01 : TheoremTreePackageRow where
  packageId := "BE.Pkg01"
  role := "statement/data normalization for iid variables, centering, variance, third absolute moment, and universal constant"
  upstreamInputs := "BerryEsseenIIDData, centeredSum, normalizedSum, normalizedSumLaw, cdfError"
  downstreamOutput := "canonical pointwise CDF-rate target for all positive n and all real x"
  leafIds := ["BE-L001"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg02`: establish the measurable/integrable substrate for sums and CDFs. -/
def Pkg02 : TheoremTreePackageRow where
  packageId := "BE.Pkg02"
  role := "measurability and integrability substrate for finite sums, normalized laws, and CDF expressions"
  upstreamInputs := "MeasurableSpace, Integrable third absolute central moment, MemLp-style moment anchors, CDF API"
  downstreamOutput := "well-formed normalized-sum distribution and CDF error terms"
  leafIds := ["BE-L002", "BE-L003"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg03`: set up characteristic functions and local expansions. -/
def Pkg03 : TheoremTreePackageRow where
  packageId := "BE.Pkg03"
  role := "characteristic-function setup for centered summands and normalized sums"
  upstreamInputs := "iid law data, mean and variance normalization, third absolute moment bound"
  downstreamOutput := "single-step characteristic-function expansion interface with third-moment remainder"
  leafIds := ["BE-L004", "BE-L005"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg04`: prove moment/Taylor remainder bounds for one centered variable. -/
def Pkg04 : TheoremTreePackageRow where
  packageId := "BE.Pkg04"
  role := "Taylor and moment remainder bounds controlled by rho and sigma"
  upstreamInputs := "centered variable, variance_eq, third_abs_integrable, third_abs_moment_le"
  downstreamOutput := "quantitative bound for the one-step characteristic-function error"
  leafIds := ["BE-L006", "BE-L007"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg05`: factor characteristic functions over independent coordinates. -/
def Pkg05 : TheoremTreePackageRow where
  packageId := "BE.Pkg05"
  role := "independence and identical-distribution factorization for normalized finite sums"
  upstreamInputs := "iIndepFun, IdentDistrib, Finset.range finite-sum normalization"
  downstreamOutput := "product/power form of the normalized-sum characteristic function"
  leafIds := ["BE-L008"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg06`: compare the normalized characteristic function with the Gaussian. -/
def Pkg06 : TheoremTreePackageRow where
  packageId := "BE.Pkg06"
  role := "Gaussian comparison and exponential approximation for the product characteristic function"
  upstreamInputs := "one-step remainder bound, product factorization, standard Gaussian characteristic function"
  downstreamOutput := "frequency-window bound between normalized-sum and Gaussian characteristic functions"
  leafIds := ["BE-L009", "BE-L010"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg07`: convert characteristic-function control into CDF control. -/
def Pkg07 : TheoremTreePackageRow where
  packageId := "BE.Pkg07"
  role := "Esseen smoothing inequality bridge from characteristic functions to uniform CDF error"
  upstreamInputs := "frequency-window characteristic-function bound and Gaussian anti-concentration/smoothing constants"
  downstreamOutput := "CDF-error bound with a truncation parameter"
  leafIds := ["BE-L011", "BE-L012"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg08`: optimize the smoothing cutoff. -/
def Pkg08 : TheoremTreePackageRow where
  packageId := "BE.Pkg08"
  role := "truncation-window choice and rate optimization"
  upstreamInputs := "CDF-error bound with cutoff, sigma positivity, rho nonnegativity, n positivity"
  downstreamOutput := "optimized O(rho / (sigma^3 * sqrt n)) bound up to a universal constant"
  leafIds := ["BE-L013"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg09`: align constants and pointwise CDF statement form. -/
def Pkg09 : TheoremTreePackageRow where
  packageId := "BE.Pkg09"
  role := "constant bookkeeping and conversion to the pointwise forall-x CDF inequality"
  upstreamInputs := "optimized smoothing bound, cdfError, BerryEsseenConclusion"
  downstreamOutput := "pointwise CDF inequality for every positive n and every real x"
  leafIds := ["BE-L014", "BE-L015"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- `BE.Pkg10`: assemble the final Berry-Esseen statement boundary. -/
def Pkg10 : TheoremTreePackageRow where
  packageId := "BE.Pkg10"
  role := "final assembly from package interfaces to StatementShape"
  upstreamInputs := "BE.Pkg01 through BE.Pkg09 package outputs"
  downstreamOutput := "StatementShape if all unchecked leaves are later replaced by validated proof ledgers"
  leafIds := ["BE-L016"]
  leafStatus := "unchecked"
  terminalProofClaim := false

/-- The P04 package split in canonical order. -/
def publicTheoremTreePackages : List TheoremTreePackageRow := [
  Pkg01,
  Pkg02,
  Pkg03,
  Pkg04,
  Pkg05,
  Pkg06,
  Pkg07,
  Pkg08,
  Pkg09,
  Pkg10
]

/-- The public theorem-tree split keeps every package leaf set unchecked. -/
theorem publicTheoremTreePackages_leafStatus_eq :
    publicTheoremTreePackages.map (fun pkg => (pkg.packageId, pkg.leafStatus)) =
      [ ("BE.Pkg01", "unchecked"),
        ("BE.Pkg02", "unchecked"),
        ("BE.Pkg03", "unchecked"),
        ("BE.Pkg04", "unchecked"),
        ("BE.Pkg05", "unchecked"),
        ("BE.Pkg06", "unchecked"),
        ("BE.Pkg07", "unchecked"),
        ("BE.Pkg08", "unchecked"),
        ("BE.Pkg09", "unchecked"),
        ("BE.Pkg10", "unchecked") ] :=
  rfl

/-- The P04 package split makes no terminal Berry-Esseen proof claim. -/
theorem publicTheoremTreePackages_no_terminal_claim :
    publicTheoremTreePackages.map (fun pkg => (pkg.packageId, pkg.terminalProofClaim)) =
      [ ("BE.Pkg01", false),
        ("BE.Pkg02", false),
        ("BE.Pkg03", false),
        ("BE.Pkg04", false),
        ("BE.Pkg05", false),
        ("BE.Pkg06", false),
        ("BE.Pkg07", false),
        ("BE.Pkg08", false),
        ("BE.Pkg09", false),
        ("BE.Pkg10", false) ] :=
  rfl

end BE

/-! ## S1-M-271-P05 local unchecked leaf ledger -/

/-- One row in the local Berry-Esseen leaf ledger requested by `S1-M-271-P05`. -/
structure BerryEsseenLocalLeafRow where
  leafId : String
  packageId : String
  obligation : String
  budgetCeiling : Nat
  status : String
  independentProofLedger : String
  terminalProofClaim : Bool
  deriving Repr, DecidableEq

/--
Local leaf ledger for `BE-L001` through `BE-L016`.

Every row is deliberately `unchecked`.  The `budgetCeiling` field records the
intended M0387 `<=100` local proof-budget target for a future proof ledger; it
is not evidence that the corresponding proof has been supplied.
-/
def berryEsseenLocalLeafLedger : List BerryEsseenLocalLeafRow := [
  { leafId := "BE-L001",
    packageId := "BE.Pkg01",
    obligation := "Normalize iid data, centered sums, normalized laws, and the pointwise CDF-rate target.",
    budgetCeiling := 60,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L002",
    packageId := "BE.Pkg02",
    obligation := "Supply measurability facts for centered finite sums and normalized sums.",
    budgetCeiling := 80,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L003",
    packageId := "BE.Pkg02",
    obligation := "Connect normalized-sum laws with CDF expressions and basic CDF bounds.",
    budgetCeiling := 80,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L004",
    packageId := "BE.Pkg03",
    obligation := "Define the centered-summand characteristic-function interface.",
    budgetCeiling := 90,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L005",
    packageId := "BE.Pkg03",
    obligation := "Relate normalized finite-sum characteristic functions to the one-step interface.",
    budgetCeiling := 95,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L006",
    packageId := "BE.Pkg04",
    obligation := "Prove the one-variable Taylor expansion with third absolute moment remainder.",
    budgetCeiling := 100,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L007",
    packageId := "BE.Pkg04",
    obligation := "Convert the Taylor remainder to a rho and sigma controlled bound.",
    budgetCeiling := 100,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L008",
    packageId := "BE.Pkg05",
    obligation := "Factor the normalized finite-sum characteristic function using independence and identical distribution.",
    budgetCeiling := 100,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L009",
    packageId := "BE.Pkg06",
    obligation := "Compare the iid product characteristic function with the Gaussian exponential on a bounded frequency window.",
    budgetCeiling := 100,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L010",
    packageId := "BE.Pkg06",
    obligation := "Track frequency-window constants for the Gaussian characteristic-function comparison.",
    budgetCeiling := 90,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L011",
    packageId := "BE.Pkg07",
    obligation := "State or prove the Esseen smoothing inequality needed for CDF control.",
    budgetCeiling := 100,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L012",
    packageId := "BE.Pkg07",
    obligation := "Apply smoothing to convert characteristic-function control into a CDF-error bound with cutoff.",
    budgetCeiling := 100,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L013",
    packageId := "BE.Pkg08",
    obligation := "Optimize the smoothing cutoff to obtain the inverse-square-root rate.",
    budgetCeiling := 95,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L014",
    packageId := "BE.Pkg09",
    obligation := "Normalize constants and sigma/rho algebra in the final CDF-rate inequality.",
    budgetCeiling := 90,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L015",
    packageId := "BE.Pkg09",
    obligation := "Convert the optimized uniform bound into the pointwise forall-x statement form.",
    budgetCeiling := 70,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false },
  { leafId := "BE-L016",
    packageId := "BE.Pkg10",
    obligation := "Assemble BE.Pkg01 through BE.Pkg09 into StatementShape after all prior leaves validate.",
    budgetCeiling := 60,
    status := "unchecked",
    independentProofLedger := "missing_independent_<=100_proof_ledger",
    terminalProofClaim := false }
]

/-- The P05 local leaf ledger contains exactly sixteen rows. -/
theorem berryEsseenLocalLeafLedger_length :
    berryEsseenLocalLeafLedger.length = 16 :=
  rfl

/-- The P05 local leaf ledger uses exactly `BE-L001` through `BE-L016`. -/
theorem berryEsseenLocalLeafLedger_leafIds_eq :
    berryEsseenLocalLeafLedger.map (fun row => row.leafId) =
      [ "BE-L001", "BE-L002", "BE-L003", "BE-L004",
        "BE-L005", "BE-L006", "BE-L007", "BE-L008",
        "BE-L009", "BE-L010", "BE-L011", "BE-L012",
        "BE-L013", "BE-L014", "BE-L015", "BE-L016" ] :=
  rfl

/-- Every P05 local leaf remains unchecked. -/
theorem berryEsseenLocalLeafLedger_statuses_eq :
    berryEsseenLocalLeafLedger.map (fun row => row.status) =
      [ "unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- No P05 local leaf claims a terminal Berry-Esseen proof. -/
theorem berryEsseenLocalLeafLedger_no_terminal_claim :
    berryEsseenLocalLeafLedger.map (fun row => row.terminalProofClaim) =
      [ false, false, false, false,
        false, false, false, false,
        false, false, false, false,
        false, false, false, false ] :=
  rfl

/-- Every P05 local leaf records the M0387 `<=100` proof-budget ceiling. -/
theorem berryEsseenLocalLeafLedger_budgetCeilings_le_100 :
    berryEsseenLocalLeafLedger.all (fun row => decide (row.budgetCeiling <= 100)) = true :=
  rfl

/--
P05 promotion gate: unchecked leaves cannot be promoted without an independent
`<=100` proof ledger and local Lean validation.
-/
def berryEsseenLocalLeafPromotionGate : String :=
  "no_BE_leaf_checked_without_independent_<=100_proof_ledger_and_repo_local_validation"

/-- The P05 promotion gate is recorded in the checked Lean artifact. -/
theorem berryEsseenLocalLeafPromotionGate_eq :
    berryEsseenLocalLeafPromotionGate =
      "no_BE_leaf_checked_without_independent_<=100_proof_ledger_and_repo_local_validation" :=
  rfl

/--
Search terms that did not locate a terminal Berry-Esseen theorem in the local
mathlib dependency closure.
-/
def absentTerminalSearchTerms : List String := [
  "Berry",
  "Esseen",
  "Berry-Esseen",
  "Berry_Esseen",
  "Kolmogorov distance",
  "kolmogorovDistance",
  "uniform CDF error",
  "normal approximation rate",
  "third absolute moment"
]

/-! ## S1-M-271-P06 external Lean 4 search audit -/

/-- One terminal Berry-Esseen Lean 4 hit from an external primary-source search. -/
structure ExternalLean4SearchHitRow where
  repositoryUrl : String
  commitSha : String
  theoremName : String
  lakeCompatibility : String
  integrationDisposition : String
  deriving Repr, DecidableEq

/--
P06 hit table for external Lean 4 Berry-Esseen searches.

This table is empty because no terminal Berry-Esseen Lean 4 theorem was
identified in the locally available pinned source closure, and the requested
authenticated GitHub code search was blocked by missing local GitHub
credentials.  The companion status strings below record the exact blocker.
-/
def externalLean4SearchHitTable : List ExternalLean4SearchHitRow := []

/-- The P06 audit currently records no external Lean 4 terminal theorem hits. -/
theorem externalLean4SearchHitTable_length :
    externalLean4SearchHitTable.length = 0 :=
  rfl

/-- Local primary-source package search result for the required P06 terms. -/
def localPinnedSourceSearchResult : String :=
  "rg over pinned Lake packages found no terminal Berry/Esseen/Kolmogorov-distance/normal-approximation-rate theorem text"

/-- GitHub authentication status for the requested authenticated external search. -/
def authenticatedGithubCodeSearchStatus : String :=
  "blocked: gh auth status reported no logged-in GitHub host; GitHub code search/API required sign-in or returned rate-limit"

/-- P06 integration gate: no external-upstream anchor was created from this blocked search. -/
def externalLean4SearchIntegrationGate : String :=
  "no_external_upstream_anchor_only_created; rerun authenticated code search before any P06 completion claim"

/-! ## S1-M-271-P07 external proof integration gate -/

/-- Repo-local integration audit row for the P07 external-proof gate. -/
structure ExternalProofIntegrationGateRow where
  childTaskId : String
  externalTerminalProofKnown : Bool
  repoLocalPinnedOrImported : Bool
  concreteIntegrationBlocker : String
  completionDisposition : String
  deriving Repr, DecidableEq

/--
P07 gate for external Lean 4 Berry-Esseen evidence.

No terminal external Lean 4 Berry-Esseen proof is known from the parent audit
or from the local pinned dependency closure.  Therefore this row creates no
repo-local integration debt and makes no completion claim.
-/
def externalProofIntegrationGateP07 : ExternalProofIntegrationGateRow where
  childTaskId := "S1-M-271-C007"
  externalTerminalProofKnown := false
  repoLocalPinnedOrImported := false
  concreteIntegrationBlocker :=
    "no external terminal Lean 4 Berry-Esseen proof is currently known; authenticated GitHub code search remains the next audit step"
  completionDisposition :=
    "not_completed; no external_upstream_anchor_only evidence is counted as completion"

/-- P07 currently has no known external terminal proof to pin or import. -/
theorem externalProofIntegrationGateP07_no_known_external_terminal_proof :
    externalProofIntegrationGateP07.externalTerminalProofKnown = false :=
  rfl

/-- P07 makes no pinned-external completion claim. -/
theorem externalProofIntegrationGateP07_no_pinned_external_claim :
    externalProofIntegrationGateP07.repoLocalPinnedOrImported = false :=
  rfl

/-- P07 preserves the no anchor-only completion rule. -/
theorem externalProofIntegrationGateP07_completionDisposition_eq :
    externalProofIntegrationGateP07.completionDisposition =
      "not_completed; no external_upstream_anchor_only evidence is counted as completion" :=
  rfl

/-! ## S1-M-271-P08 public statement-surface decision -/

/-- Repo-local decision row for the public Berry-Esseen statement surface. -/
structure StatementSurfaceDecisionRow where
  childTaskId : String
  canonicalStatementSurface : String
  introduceLocalKolmogorovDistanceDefinition : Bool
  reason : String
  repoLocalIntegrationDebt : Bool
  completionDisposition : String
  deriving Repr, DecidableEq

/--
P08 decision: keep the public canonical statement in pointwise `forall x` CDF
bound form.

This matches the checked `BerryEsseenConclusion` declaration above and avoids
creating a local Kolmogorov-distance API that is not present in the pinned
mathlib closure.  A later proof-integration pass may add a Kolmogorov-distance
abbreviation only if it is backed by a pinned upstream API or by a terminal
repo-local proof interface.
-/
def statementSurfaceDecisionP08 : StatementSurfaceDecisionRow where
  childTaskId := "S1-M-271-C008"
  canonicalStatementSurface := "keep_pointwise_forall_x_CDF_bound"
  introduceLocalKolmogorovDistanceDefinition := false
  reason :=
    "BerryEsseenConclusion already states the uniform CDF-rate target as a pointwise forall-x bound using pinned mathlib cdf; no pinned Kolmogorov-distance API was found"
  repoLocalIntegrationDebt := false
  completionDisposition :=
    "decision_recorded_for_public_backfill; no terminal Berry-Esseen proof completion claimed"

/-- P08 keeps the canonical statement surface in pointwise `forall x` form. -/
theorem statementSurfaceDecisionP08_surface_eq :
    statementSurfaceDecisionP08.canonicalStatementSurface =
      "keep_pointwise_forall_x_CDF_bound" :=
  rfl

/-- P08 does not introduce a new local Kolmogorov-distance definition. -/
theorem statementSurfaceDecisionP08_no_local_kolmogorov_definition :
    statementSurfaceDecisionP08.introduceLocalKolmogorovDistanceDefinition = false :=
  rfl

/-- P08 creates no repo-local integration debt. -/
theorem statementSurfaceDecisionP08_no_repo_local_integration_debt :
    statementSurfaceDecisionP08.repoLocalIntegrationDebt = false :=
  rfl

/-! ## S1-M-271-P09 public backfill gate -/

/-- Repo-local gate row for deferred public Stage1/todo/README backfill. -/
structure PublicBackfillGateRow where
  childTaskId : String
  publicDocsEditableByChild : Bool
  serialIntegratorReviewRequired : Bool
  terminalProofRequired : Bool
  publicMergeBackRequired : Bool
  localValidationRequired : Bool
  leafLedgersRequired : Bool
  keepTheoremOpen : Bool
  repoLocalIntegrationDebt : Bool
  completionDisposition : String
  deriving Repr, DecidableEq

/--
P09 gate: public status backfill is intentionally deferred to a serial
integrator, and the theorem remains open until all M0387 completion gates close.

This row is metadata only.  It does not complete the terminal Berry-Esseen
CDF-rate theorem and it does not edit public planning documents.
-/
def publicBackfillGateP09 : PublicBackfillGateRow where
  childTaskId := "S1-M-271-C009"
  publicDocsEditableByChild := false
  serialIntegratorReviewRequired := true
  terminalProofRequired := true
  publicMergeBackRequired := true
  localValidationRequired := true
  leafLedgersRequired := true
  keepTheoremOpen := true
  repoLocalIntegrationDebt := false
  completionDisposition :=
    "public_backfill_deferred_to_serial_integrator; keep THM-M-0991 open until terminal proof, public merge-back, local validation, and <=100 leaf ledgers close"

/-- P09 records that this child may not directly edit public planning docs. -/
theorem publicBackfillGateP09_public_docs_not_child_editable :
    publicBackfillGateP09.publicDocsEditableByChild = false :=
  rfl

/-- P09 keeps the Berry-Esseen theorem open. -/
theorem publicBackfillGateP09_keep_open :
    publicBackfillGateP09.keepTheoremOpen = true :=
  rfl

/-- P09 creates no completed-state repo-local integration debt. -/
theorem publicBackfillGateP09_no_repo_local_integration_debt :
    publicBackfillGateP09.repoLocalIntegrationDebt = false :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check BerryEsseenConclusion
#check statementShapeBoundaryAudit
#check statementShapeBoundaryAudit_no_terminal_completion
#check statementShapeBoundaryAudit_no_completed_integration_debt
#check currentMachineStatus
#check currentMachineDebtClass
#check terminalCDFRateProofInLocalClosure
#check terminalCDFRateProofInLocalClosure_eq_false
#check currentMachineDebtClass_eq
#check MathlibAnchorRow
#check requestedMathlibAnchorTable
#check TheoremTreePackageRow
#check BE.Pkg01
#check BE.Pkg02
#check BE.Pkg03
#check BE.Pkg04
#check BE.Pkg05
#check BE.Pkg06
#check BE.Pkg07
#check BE.Pkg08
#check BE.Pkg09
#check BE.Pkg10
#check BE.publicTheoremTreePackages
#check BE.publicTheoremTreePackages_leafStatus_eq
#check BE.publicTheoremTreePackages_no_terminal_claim
#check BerryEsseenLocalLeafRow
#check berryEsseenLocalLeafLedger
#check berryEsseenLocalLeafLedger_length
#check berryEsseenLocalLeafLedger_leafIds_eq
#check berryEsseenLocalLeafLedger_statuses_eq
#check berryEsseenLocalLeafLedger_no_terminal_claim
#check berryEsseenLocalLeafLedger_budgetCeilings_le_100
#check berryEsseenLocalLeafPromotionGate
#check berryEsseenLocalLeafPromotionGate_eq
#check ExternalLean4SearchHitRow
#check externalLean4SearchHitTable
#check externalLean4SearchHitTable_length
#check localPinnedSourceSearchResult
#check authenticatedGithubCodeSearchStatus
#check externalLean4SearchIntegrationGate
#check ExternalProofIntegrationGateRow
#check externalProofIntegrationGateP07
#check externalProofIntegrationGateP07_no_known_external_terminal_proof
#check externalProofIntegrationGateP07_no_pinned_external_claim
#check externalProofIntegrationGateP07_completionDisposition_eq
#check StatementSurfaceDecisionRow
#check statementSurfaceDecisionP08
#check statementSurfaceDecisionP08_surface_eq
#check statementSurfaceDecisionP08_no_local_kolmogorov_definition
#check statementSurfaceDecisionP08_no_repo_local_integration_debt
#check PublicBackfillGateRow
#check publicBackfillGateP09
#check publicBackfillGateP09_public_docs_not_child_editable
#check publicBackfillGateP09_keep_open
#check publicBackfillGateP09_no_repo_local_integration_debt
#check ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check MeasureTheory.TendstoInDistribution
#check ProbabilityTheory.cdf
#check ProbabilityTheory.cdf_nonneg
#check ProbabilityTheory.cdf_le_one
#check ProbabilityTheory.gaussianReal
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.IdentDistrib
#check MeasureTheory.MemLp
#check ProbabilityTheory.variance

end S1_M_271
end Stage1
end AwesomeTheorems
