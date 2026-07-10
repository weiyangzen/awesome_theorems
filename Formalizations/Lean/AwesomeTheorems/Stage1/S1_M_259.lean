import Mathlib.Analysis.Asymptotics.Defs
import Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt
import Mathlib.NumberTheory.Chebyshev
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries
import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.PrimeCounting

/-!
# S1-M-259 / THM-M-0504: consequences/equivalences of the Riemann hypothesis

This Stage1 artifact records a conservative Lean 4 boundary for statements
equivalent to, or conditional on, the Riemann hypothesis.  The pinned mathlib
snapshot already defines `RiemannHypothesis`, the analytic continuation of
`riemannZeta`, its functional equation, trivial zeroes, an Euler product in
`re s > 1`, the Chebyshev `theta`/`psi` functions, the von Mangoldt arithmetic
function, and the prime-counting function.

The terminal equivalence between RH and sharp prime-counting / Chebyshev
estimates is not claimed here.  The declarations below therefore expose a
precise `Prop` statement shape and local wrappers around the checked mathlib
anchors only.
-/

noncomputable section

open Complex Filter Asymptotics
open scoped ArithmeticFunction Nat.Prime Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_259

/-- The mathlib revision audited for this Stage1 slot. -/
def auditedMathlibPin : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- The mathlib statement of the Riemann hypothesis, kept under this slot's namespace. -/
abbrev RH : Prop :=
  RiemannHypothesis

/-- Real prime-counting function obtained from mathlib's natural-valued `Nat.primeCounting`. -/
def realPrimeCounting (x : ℝ) : ℝ :=
  (Nat.primeCounting ⌊x⌋₊ : ℝ)

/--
One classical RH-equivalent analytic estimate: a square-root scale error term
for the prime-counting function.  This is a statement-shape target only; no
terminal proof is supplied by this file.
-/
def PrimeCountingErrorBound : Prop :=
  (fun x : ℝ => realPrimeCounting x - x / Real.log x)
    =O[atTop]
      (fun x : ℝ => Real.sqrt x * Real.log x)

/--
Chebyshev-psi error at the standard RH square-root scale, with a log-squared
loss.  This uses mathlib's real-valued `Chebyshev.psi` object.
-/
def ChebyshevPsiErrorBound : Prop :=
  (fun x : ℝ => Chebyshev.psi x - x)
    =O[atTop]
      (fun x : ℝ => Real.sqrt x * (Real.log x) ^ 2)

/--
Zero-location formulation mirroring mathlib's current `RiemannHypothesis`
definition: every nontrivial zero of `riemannZeta` lies on the critical line.
-/
def CriticalLineZeroCriterion : Prop :=
  ∀ (s : ℂ), riemannZeta s = 0 →
    (¬∃ n : ℕ, s = -2 * (n + 1)) →
      s ≠ 1 →
        s.re = 1 / 2

/--
Stage1 statement-shape candidate for the source item "equivalent statements /
consequences of RH".

The shape records the intended equivalence package but deliberately does not
prove it.  Closing this `Prop` requires an explicit-formula / zero-free-region /
Tauberian package or a pinned upstream theorem; the local wrappers below only
check the current mathlib substrate.
-/
def StatementShape : Prop :=
  RH ↔
    CriticalLineZeroCriterion ∧
      ChebyshevPsiErrorBound ∧
        PrimeCountingErrorBound

/-- The local zero-location criterion unfolds to mathlib's `RiemannHypothesis`. -/
theorem criticalLineZeroCriterion_iff_mathlib_RH :
    CriticalLineZeroCriterion ↔ RH :=
  Iff.rfl

/-- The Stage1 statement shape unfolds to the chosen RH-equivalence boundary. -/
theorem statementShape_iff :
    StatementShape ↔
      (RH ↔
        CriticalLineZeroCriterion ∧
          ChebyshevPsiErrorBound ∧
            PrimeCountingErrorBound) :=
  Iff.rfl

/--
Machine-status marker for the current repo-local Stage1 artifact.

The current file only validates the statement shape and adjacent mathlib
wrappers.  The second constructor is reserved for a future state in which the
terminal RH-equivalence / consequence package is actually proved or imported
through a pinned, locally checked dependency.
-/
inductive Stage1MachineStatus where
  | statementShapeAndMathlibWrappersOnly
  | terminalEquivalenceProofClosed
  deriving DecidableEq, Repr

/-- Current machine status for this Stage1 slot. -/
def currentStage1MachineStatus : Stage1MachineStatus :=
  .statementShapeAndMathlibWrappersOnly

/-- Checked witness that this artifact has not been upgraded to terminal proof closure. -/
theorem currentStage1MachineStatus_eq_statementShapeAndMathlibWrappersOnly :
    currentStage1MachineStatus =
      Stage1MachineStatus.statementShapeAndMathlibWrappersOnly :=
  rfl

/-! ## Checked mathlib wrappers for local anchors. -/

/-- mathlib wrapper: the Riemann zeta function is differentiable away from `1`. -/
theorem differentiableAt_riemannZeta_wrapper {s : ℂ} (hs : s ≠ 1) :
    DifferentiableAt ℂ riemannZeta s :=
  differentiableAt_riemannZeta hs

/-- mathlib wrapper: the trivial zeroes at negative even integers. -/
theorem trivialZero_riemannZeta_wrapper (n : ℕ) :
    riemannZeta (-2 * (n + 1)) = 0 :=
  riemannZeta_neg_two_mul_nat_add_one n

/-- mathlib wrapper: Riemann zeta functional equation in the available form. -/
theorem riemannZeta_functionalEquation_wrapper {s : ℂ}
    (hs : ∀ n : ℕ, s ≠ -n) (hs' : s ≠ 1) :
    riemannZeta (1 - s) =
      2 * (2 * Real.pi) ^ (-s) * Gamma s * cos (Real.pi * s / 2) * riemannZeta s :=
  riemannZeta_one_sub hs hs'

/-- mathlib wrapper: Dirichlet-series expression for `riemannZeta` in `re s > 1`. -/
theorem riemannZeta_dirichletSeries_wrapper {s : ℂ} (hs : 1 < s.re) :
    riemannZeta s = ∑' n : ℕ, 1 / (n + 1 : ℂ) ^ s :=
  zeta_eq_tsum_one_div_nat_add_one_cpow hs

/-- mathlib wrapper: Euler product for `riemannZeta` in `re s > 1`. -/
theorem riemannZeta_eulerProduct_wrapper {s : ℂ} (hs : 1 < s.re) :
    HasProd (fun p : Nat.Primes => (1 - (p : ℂ) ^ (-s))⁻¹) (riemannZeta s) :=
  riemannZeta_eulerProduct_hasProd hs

/-- mathlib wrapper: von Mangoldt divisor sum equals the logarithm. -/
theorem vonMangoldt_sum_wrapper {n : ℕ} :
    ∑ i ∈ n.divisors, ArithmeticFunction.vonMangoldt i = Real.log n :=
  ArithmeticFunction.vonMangoldt_sum

/-- mathlib wrapper: Chebyshev `psi` decomposes as a sum of `theta` values. -/
theorem chebyshevPsi_eq_sumTheta_wrapper {x : ℝ} (hx : 0 ≤ x) :
    Chebyshev.psi x =
      ∑ n ∈ Finset.Icc 1 ⌊Real.log x / Real.log 2⌋₊,
        Chebyshev.theta (x ^ (1 / (n : ℝ))) :=
  Chebyshev.psi_eq_sum_theta hx

/-- mathlib wrapper: checked comparison between Chebyshev `psi` and `theta`. -/
theorem chebyshev_absPsiSubTheta_wrapper {x : ℝ} (hx : 1 ≤ x) :
    |Chebyshev.psi x - Chebyshev.theta x| ≤ 2 * Real.sqrt x * Real.log x :=
  Chebyshev.abs_psi_sub_theta_le_sqrt_mul_log hx

/-- mathlib wrapper: Abel summation expresses prime counting in terms of `theta`. -/
theorem primeCounting_eq_theta_div_log_add_integral_wrapper {x : ℝ} (hx : 2 ≤ x) :
    realPrimeCounting x =
      Chebyshev.theta x / Real.log x +
        ∫ t in 2..x, Chebyshev.theta t / (t * Real.log t ^ 2) := by
  simpa [realPrimeCounting] using Chebyshev.primeCounting_eq_theta_div_log_add_integral hx

/-- mathlib wrapper: checked coarse asymptotic comparison between prime counting and `theta / log`. -/
theorem primeCounting_sub_theta_div_log_isBigO_wrapper :
    (fun x : ℝ => realPrimeCounting x - Chebyshev.theta x / Real.log x)
      =O[atTop]
        (fun x : ℝ => x / Real.log x ^ 2) := by
  simpa [realPrimeCounting] using Chebyshev.primeCounting_sub_theta_div_log_isBigO

/-- mathlib wrapper: a checked linear upper bound for Chebyshev `psi`. -/
theorem chebyshevPsi_linearUpper_wrapper {x : ℝ} (hx : 0 ≤ x) :
    Chebyshev.psi x ≤ (Real.log 4 + 4) * x :=
  Chebyshev.psi_le_const_mul_self hx

/-- mathlib wrapper: the prime-counting function tends to infinity. -/
theorem primeCounting_tendsto_wrapper :
    Tendsto Nat.primeCounting atTop atTop :=
  Nat.tendsto_primeCounting

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.LSeries.RiemannZeta",
  "Mathlib.NumberTheory.EulerProduct.DirichletLSeries",
  "Mathlib.NumberTheory.Chebyshev",
  "Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt",
  "Mathlib.NumberTheory.ArithmeticFunction.Zeta",
  "Mathlib.NumberTheory.PrimeCounting",
  "Mathlib.Analysis.Asymptotics.Defs"
]

/-- Exact mathlib declarations checked for child task `S1-M-259-C002`. -/
def checkedMathlibAnchors_C002 : List String := [
  "RiemannHypothesis",
  "riemannZeta",
  "riemannZeta_one_sub",
  "riemannZeta_eulerProduct_hasProd",
  "Chebyshev.psi",
  "Chebyshev.theta",
  "ArithmeticFunction.vonMangoldt_sum",
  "Nat.primeCounting"
]

/-- Search terms that did not locate a terminal RH-equivalence theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "RiemannHypothesis equivalent prime counting",
  "PrimeNumberTheorem",
  "Chebyshev.psi = x + O(sqrt x log^2 x)",
  "riemannZeta zero explicit formula",
  "Mertens RH equivalence",
  "Liouville RH equivalence"
]

/--
Status categories for the C003 public blocker about terminal RH-equivalent
prime-counting / Chebyshev estimates in the pinned mathlib substrate.
-/
inductive TerminalEstimateBlockerStatus where
  | noTerminalTheoremInPinnedMathlib
  | terminalTheoremPinnedAndChecked
  deriving DecidableEq, Repr

/--
Checked metadata for child task `S1-M-259-C003`.

This is deliberately an audit/blocker record, not a theorem proving absence
inside mathlib.  It records the repo-local fact used by the public backfill:
the checked mathlib anchors are substrate declarations and estimates, while no
terminal theorem proving the RH-equivalent prime-counting/Chebyshev error
package has been imported, wrapped, or locally checked in this artifact.
-/
structure TerminalEstimateBlocker where
  mathlibPin : String
  checkedAnchorBatch : List String
  missingTerminalFamily : List String
  blockerStatus : TerminalEstimateBlockerStatus
  terminalTheoremImportedOrWrapped : Bool
  repoLocalCompleted : Bool
  debtClassification : String
  deriving Repr

/-- C003 blocker record for the missing terminal RH-equivalence theorem family. -/
def terminalEstimateBlocker_C003 : TerminalEstimateBlocker where
  mathlibPin := auditedMathlibPin
  checkedAnchorBatch := checkedMathlibAnchors_C002
  missingTerminalFamily := [
    "RH -> Chebyshev.psi x - x = O(sqrt x * log x ^ 2)",
    "RH -> primeCounting x - x / log x = O(sqrt x * log x)",
    "Chebyshev/prime-counting error estimates -> critical-line zero exclusion",
    "terminal equivalence between RiemannHypothesis and the full estimate package"
  ]
  blockerStatus := .noTerminalTheoremInPinnedMathlib
  terminalTheoremImportedOrWrapped := false
  repoLocalCompleted := false
  debtClassification := "formalization_debt / not_repo_local_closed"

/-- Checked C003 status: the current blocker is the missing-terminal-theorem case. -/
theorem terminalEstimateBlocker_C003_status :
    terminalEstimateBlocker_C003.blockerStatus =
      TerminalEstimateBlockerStatus.noTerminalTheoremInPinnedMathlib :=
  rfl

/-- Checked C003 gate: no terminal theorem has been imported or wrapped locally. -/
theorem terminalEstimateBlocker_C003_notImportedOrWrapped :
    terminalEstimateBlocker_C003.terminalTheoremImportedOrWrapped = false :=
  rfl

/-- Checked C003 gate: this blocker record does not mark the parent theorem completed. -/
theorem terminalEstimateBlocker_C003_notRepoLocalCompleted :
    terminalEstimateBlocker_C003.repoLocalCompleted = false :=
  rfl

/-! ## External statement-only source record for C004. -/

/--
Status categories for the C004 external `LeanMillenniumPrizeProblems` source.

The upstream Riemann file gives a checked Lean statement and adjacent mathlib
wrappers.  It is not treated here as a terminal proof of RH or of the
RH-equivalent prime-counting / Chebyshev estimate package.
-/
inductive ExternalStatementSourceStatus where
  | statementOnly
  | terminalProofPinnedAndChecked
  deriving DecidableEq, Repr

/--
Checked metadata for child task `S1-M-259-C004`.

This record is an external-anchor audit object.  It deliberately records
`terminalProofImportedOrWrapped = false` and `repoLocalCompletedEvidence =
false`, because the upstream repository is statement-oriented and is not in this
repo's local validation closure.
-/
structure ExternalStatementSource where
  repository : String
  observedMainCommit : String
  riemannFile : String
  toolchain : String
  mathlibRevision : String
  sourceStatus : ExternalStatementSourceStatus
  checkedUpstreamNames : List String
  terminalProofImportedOrWrapped : Bool
  repoLocalCompletedEvidence : Bool
  debtClassification : String
  deriving Repr

/-- External statement-only source record for child task `S1-M-259-C004`. -/
def leanMillenniumPrizeProblems_C004 : ExternalStatementSource where
  repository := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems"
  observedMainCommit := "540da94826f70f3edf4d4fc66ce6cda20e903f61"
  riemannFile := "Problems/RiemannHypothesis/Millennium.lean"
  toolchain := "leanprover/lean4:v4.26.0"
  mathlibRevision := "2df2f0150c275ad53cb3c90f7c98ec15a56a1a67"
  sourceStatus := .statementOnly
  checkedUpstreamNames := [
    "Millennium.RiemannHypothesis",
    "Millennium.riemannHypothesis_iff_mathlib",
    "Millennium.riemannZeta_eq_tsum_one_div_nat_cpow",
    "Millennium.riemannZeta_eulerProduct_hasProd",
    "Millennium.completedZeta_one_sub",
    "Millennium.psiFunction_eq_sum_thetaFunction",
    "Millennium.LSeries_vonMangoldt_eq_negLogDeriv_riemannZeta",
    "Millennium.thetaFunction_le_log4_mul_x",
    "Millennium.psiFunction_le_const_mul_self"
  ]
  terminalProofImportedOrWrapped := false
  repoLocalCompletedEvidence := false
  debtClassification := "external_upstream_anchor_only / not_repo_local_closed"

/-- Checked C004 status: the external source is statement-only evidence. -/
theorem leanMillenniumPrizeProblems_C004_status :
    leanMillenniumPrizeProblems_C004.sourceStatus =
      ExternalStatementSourceStatus.statementOnly :=
  rfl

/-- Checked C004 gate: no terminal external theorem has been imported or wrapped locally. -/
theorem leanMillenniumPrizeProblems_C004_notImportedOrWrapped :
    leanMillenniumPrizeProblems_C004.terminalProofImportedOrWrapped = false :=
  rfl

/-- Checked C004 gate: this external anchor is not completed repo-local evidence. -/
theorem leanMillenniumPrizeProblems_C004_notRepoLocalCompleted :
    leanMillenniumPrizeProblems_C004.repoLocalCompletedEvidence = false :=
  rfl

/-! ## Explicit-formula theorem-tree split for C005. -/

/--
The six explicit-formula leaves requested by child task `S1-M-259-C005`.

These are theorem-tree budget leaves, not proofs of the analytic explicit
formula.  They isolate the proof obligations that would be needed before the
RH-to-Chebyshev/prime-counting branches can be closed locally.
-/
inductive ExplicitFormulaLeafId where
  | zeroEncoding
  | perronMellinTransform
  | residueAccounting
  | contourBounds
  | zeroSumTruncation
  | errorExtraction
  deriving DecidableEq, Repr

/--
Machine status for an explicit-formula leaf in this Stage1 artifact.

`treeLeafExpanded` means the local artifact has recorded the leaf boundary and
dependencies.  It does not mean that the analytic proof body is present.
-/
inductive ExplicitFormulaLeafStatus where
  | treeLeafExpanded
  | localProofBodyClosed
  | upstreamProofPinnedAndChecked
  deriving DecidableEq, Repr

/-- Metadata for one C005 explicit-formula leaf. -/
structure ExplicitFormulaLeaf where
  id : ExplicitFormulaLeafId
  canonicalName : String
  role : String
  requiredAPIs : List String
  outputTarget : String
  budgetStatus : String
  machineStatus : ExplicitFormulaLeafStatus
  debtClassification : String
  repoLocalCompletedEvidence : Bool
  deriving Repr

/-- C005 split of the explicit-formula branch into six reviewable leaves. -/
def explicitFormulaLeaves_C005 : List ExplicitFormulaLeaf := [
  {
    id := .zeroEncoding
    canonicalName := "S1-M-259.explicitFormula.zeroEncoding"
    role :=
      "Encode nontrivial zeta zeroes with multiplicity and symmetry data."
    requiredAPIs := [
      "riemannZeta",
      "RiemannHypothesis",
      "riemannZeta_one_sub",
      "riemannZeta_neg_two_mul_nat_add_one"
    ]
    outputTarget :=
      "A zero multiset or locally finite zero-indexing API suitable for sums over rho."
    budgetStatus := "expanded / <=100-step budget still unchecked"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .perronMellinTransform
    canonicalName := "S1-M-259.explicitFormula.perronMellinTransform"
    role :=
      "Relate Chebyshev psi to a Perron or Mellin integral of the logarithmic derivative of zeta."
    requiredAPIs := [
      "Chebyshev.psi",
      "ArithmeticFunction.vonMangoldt",
      "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div",
      "riemannZeta_eulerProduct_hasProd"
    ]
    outputTarget :=
      "A checked integral identity for psi or a smoothed psi variant on a vertical line."
    budgetStatus := "expanded / <=100-step budget still unchecked"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .residueAccounting
    canonicalName := "S1-M-259.explicitFormula.residueAccounting"
    role :=
      "Account for residues at s = 1, nontrivial zeroes, trivial zeroes, and endpoint or pole terms after contour shift."
    requiredAPIs := [
      "differentiableAt_riemannZeta",
      "riemannZeta_one_sub",
      "riemannZeta_neg_two_mul_nat_add_one",
      "Complex residues around isolated poles"
    ]
    outputTarget :=
      "A residue identity with main term x and zero contribution -sum_rho x^rho / rho."
    budgetStatus := "expanded / <=100-step budget still unchecked"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .contourBounds
    canonicalName := "S1-M-259.explicitFormula.contourBounds"
    role :=
      "Bound the horizontal and left-side contour integrals using zeta growth, zero avoidance, and kernel decay."
    requiredAPIs := [
      "riemannZeta",
      "Gamma",
      "Complex.log/Real.log bounds",
      "asymptotic big-O filters"
    ]
    outputTarget :=
      "A contour-error bound uniform in x and truncation height T."
    budgetStatus := "expanded / <=100-step budget still unchecked"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .zeroSumTruncation
    canonicalName := "S1-M-259.explicitFormula.zeroSumTruncation"
    role :=
      "Truncate the zero sum by imaginary height and prove convergence/tail control for the selected zero encoding."
    requiredAPIs := [
      "zero-counting or locally finite zero set API",
      "summability of zero contributions",
      "RiemannHypothesis as optional line-location input"
    ]
    outputTarget :=
      "A finite-height zero-sum formula plus a tail estimate compatible with the RH branch."
    budgetStatus := "expanded / <=100-step budget still unchecked"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .errorExtraction
    canonicalName := "S1-M-259.explicitFormula.errorExtraction"
    role :=
      "Optimize truncation parameters and extract the final Chebyshev psi error estimate from the explicit formula."
    requiredAPIs := [
      "ChebyshevPsiErrorBound",
      "RH",
      "asymptotic big-O algebra",
      "zeroSumTruncation output"
    ]
    outputTarget :=
      "RH -> Chebyshev.psi x - x = O(sqrt x * (log x)^2)."
    budgetStatus := "expanded / <=100-step budget still unchecked"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  }
]

/-- Checked C005 gate: the explicit-formula branch has exactly six split leaves. -/
theorem explicitFormulaLeaves_C005_length :
    explicitFormulaLeaves_C005.length = 6 :=
  rfl

/-- Checked C005 gate: the split uses the requested leaf order. -/
theorem explicitFormulaLeaves_C005_ids :
    explicitFormulaLeaves_C005.map (fun leaf => leaf.id) = [
      ExplicitFormulaLeafId.zeroEncoding,
      ExplicitFormulaLeafId.perronMellinTransform,
      ExplicitFormulaLeafId.residueAccounting,
      ExplicitFormulaLeafId.contourBounds,
      ExplicitFormulaLeafId.zeroSumTruncation,
      ExplicitFormulaLeafId.errorExtraction
    ] :=
  rfl

/-- C005 does not claim terminal proof closure for the explicit-formula branch. -/
def explicitFormulaTree_C005_repoLocalCompleted : Bool :=
  false

/-- Checked C005 gate: no repo-local completion is claimed by the tree split. -/
theorem explicitFormulaTree_C005_notRepoLocalCompleted :
    explicitFormulaTree_C005_repoLocalCompleted = false :=
  rfl

/--
C005 no-residual-integration-debt gate.

No external terminal explicit-formula Lean proof is recorded as completed by
anchor-only evidence in this artifact, and the local tree split itself remains
formalization debt.
-/
def explicitFormulaTree_C005_completedStateRetainsRepoLocalIntegrationDebt : Bool :=
  false

/-- Checked C005 gate: no completed state retains repo-local integration debt. -/
theorem explicitFormulaTree_C005_noCompletedRepoLocalIntegrationDebt :
    explicitFormulaTree_C005_completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## RH-to-psi error branch split for C006. -/

/--
The C006 leaves refining the branch from RH plus an explicit-formula API to the
Chebyshev `psi` error estimate.

Each leaf is intentionally bounded as a local proof obligation.  The branch is
not closed by this metadata layer.
-/
inductive RHPsiErrorLeafId where
  | normalizeTarget
  | bindExplicitFormulaContract
  | applyRHToZeroLocations
  | boundIndividualZeroTerms
  | boundTruncatedZeroSum
  | transferContourAndTailErrors
  | optimizeTruncationHeight
  | assembleBigOStatement
  deriving DecidableEq, Repr

/-- Machine status for a C006 RH-to-`psi` error leaf. -/
inductive RHPsiErrorLeafStatus where
  | treeLeafExpanded
  | localProofBodyClosed
  | upstreamProofPinnedAndChecked
  deriving DecidableEq, Repr

/-- Metadata for one C006 RH-to-`psi` error leaf. -/
structure RHPsiErrorLeaf where
  id : RHPsiErrorLeafId
  canonicalName : String
  alignedExplicitFormulaLeaf : ExplicitFormulaLeafId
  upstreamInputs : List String
  localGoal : String
  outputTarget : String
  maxProofSteps : Nat
  budgetStatus : String
  machineStatus : RHPsiErrorLeafStatus
  debtClassification : String
  repoLocalCompletedEvidence : Bool
  deriving Repr

/--
C006 split of the RH-to-`Chebyshev.psi` error branch into <=100-step leaves,
aligned with the C005 explicit-formula API.
-/
def rhToPsiErrorLeaves_C006 : List RHPsiErrorLeaf := [
  {
    id := .normalizeTarget
    canonicalName := "S1-M-259.rhToPsiError.normalizeTarget"
    alignedExplicitFormulaLeaf := .errorExtraction
    upstreamInputs := [
      "ChebyshevPsiErrorBound",
      "Asymptotics.IsBigO atTop",
      "eventual real positivity side conditions for x, log x, and sqrt x"
    ]
    localGoal :=
      "Normalize the target into an eventual absolute-value inequality usable by the explicit-formula output."
    outputTarget :=
      "A local lemma reducing ChebyshevPsiErrorBound to a concrete eventual bound for |Chebyshev.psi x - x|."
    maxProofSteps := 40
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .bindExplicitFormulaContract
    canonicalName := "S1-M-259.rhToPsiError.bindExplicitFormulaContract"
    alignedExplicitFormulaLeaf := .zeroSumTruncation
    upstreamInputs := [
      "S1-M-259.explicitFormula.zeroSumTruncation",
      "S1-M-259.explicitFormula.errorExtraction",
      "finite-height explicit formula for Chebyshev.psi"
    ]
    localGoal :=
      "State the exact explicit-formula contract consumed by the RH branch: main term x, truncated zero sum, and explicit remainder terms."
    outputTarget :=
      "A typed interface from the C005 explicit-formula leaves to the RH-specific estimates."
    maxProofSteps := 35
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .applyRHToZeroLocations
    canonicalName := "S1-M-259.rhToPsiError.applyRHToZeroLocations"
    alignedExplicitFormulaLeaf := .zeroEncoding
    upstreamInputs := [
      "RH",
      "CriticalLineZeroCriterion",
      "S1-M-259.explicitFormula.zeroEncoding"
    ]
    localGoal :=
      "Transport RH through the chosen zero-encoding API so every nontrivial zero in the explicit formula has real part 1/2."
    outputTarget :=
      "A zero-indexed hypothesis usable for bounding x^rho at square-root scale."
    maxProofSteps := 55
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .boundIndividualZeroTerms
    canonicalName := "S1-M-259.rhToPsiError.boundIndividualZeroTerms"
    alignedExplicitFormulaLeaf := .residueAccounting
    upstreamInputs := [
      "zero real-part output from applyRHToZeroLocations",
      "residue term x^rho / rho",
      "complex norm and cpow estimates"
    ]
    localGoal :=
      "For each encoded nontrivial zero rho with rho.re = 1/2, bound the individual residue contribution by sqrt x times a denominator depending on rho."
    outputTarget :=
      "Pointwise zero-term estimate compatible with the truncated zero-sum bound."
    maxProofSteps := 80
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .boundTruncatedZeroSum
    canonicalName := "S1-M-259.rhToPsiError.boundTruncatedZeroSum"
    alignedExplicitFormulaLeaf := .zeroSumTruncation
    upstreamInputs := [
      "boundIndividualZeroTerms",
      "zero-counting bound for |Im rho| <= T",
      "finite zero-sum API from C005"
    ]
    localGoal :=
      "Sum the pointwise RH zero-term estimates over the finite-height zero set."
    outputTarget :=
      "A truncated zero-sum bound of square-root size with the log factors required by the target."
    maxProofSteps := 90
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .transferContourAndTailErrors
    canonicalName := "S1-M-259.rhToPsiError.transferContourAndTailErrors"
    alignedExplicitFormulaLeaf := .contourBounds
    upstreamInputs := [
      "S1-M-259.explicitFormula.contourBounds",
      "S1-M-259.explicitFormula.zeroSumTruncation",
      "explicit-formula remainder terms"
    ]
    localGoal :=
      "Carry the contour, endpoint, trivial-zero, and zero-tail errors through the RH-specific inequality."
    outputTarget :=
      "A combined pre-optimization inequality for |Chebyshev.psi x - x| in terms of x and truncation height T."
    maxProofSteps := 85
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .optimizeTruncationHeight
    canonicalName := "S1-M-259.rhToPsiError.optimizeTruncationHeight"
    alignedExplicitFormulaLeaf := .errorExtraction
    upstreamInputs := [
      "combined pre-optimization inequality",
      "eventual logarithm inequalities",
      "asymptotic big-O algebra"
    ]
    localGoal :=
      "Choose the truncation-height regime and absorb all pre-optimization terms into sqrt x * (log x)^2."
    outputTarget :=
      "An eventual concrete bound of the Chebyshev `psi` error at RH square-root scale."
    maxProofSteps := 75
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .assembleBigOStatement
    canonicalName := "S1-M-259.rhToPsiError.assembleBigOStatement"
    alignedExplicitFormulaLeaf := .errorExtraction
    upstreamInputs := [
      "normalizeTarget",
      "optimizeTruncationHeight",
      "ChebyshevPsiErrorBound"
    ]
    localGoal :=
      "Package the eventual inequality back into the repository's statement-shape proposition ChebyshevPsiErrorBound."
    outputTarget :=
      "A future theorem with target RH -> ChebyshevPsiErrorBound."
    maxProofSteps := 45
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  }
]

/-- Checked C006 gate: the RH-to-`psi` branch is split into eight leaves. -/
theorem rhToPsiErrorLeaves_C006_length :
    rhToPsiErrorLeaves_C006.length = 8 :=
  rfl

/-- Checked C006 gate: every recorded leaf cap is at most 100 proof steps. -/
theorem rhToPsiErrorLeaves_C006_stepCaps :
    rhToPsiErrorLeaves_C006.map (fun leaf => leaf.maxProofSteps) =
      [40, 35, 55, 80, 90, 85, 75, 45] :=
  rfl

/-- Checked C006 gate: the split uses the requested RH-to-`psi` leaf order. -/
theorem rhToPsiErrorLeaves_C006_ids :
    rhToPsiErrorLeaves_C006.map (fun leaf => leaf.id) = [
      RHPsiErrorLeafId.normalizeTarget,
      RHPsiErrorLeafId.bindExplicitFormulaContract,
      RHPsiErrorLeafId.applyRHToZeroLocations,
      RHPsiErrorLeafId.boundIndividualZeroTerms,
      RHPsiErrorLeafId.boundTruncatedZeroSum,
      RHPsiErrorLeafId.transferContourAndTailErrors,
      RHPsiErrorLeafId.optimizeTruncationHeight,
      RHPsiErrorLeafId.assembleBigOStatement
    ] :=
  rfl

/-- C006 does not claim theorem closure for `RH -> ChebyshevPsiErrorBound`. -/
def rhToPsiError_C006_repoLocalCompleted : Bool :=
  false

/-- Checked C006 gate: no repo-local completion is claimed by this branch split. -/
theorem rhToPsiError_C006_notRepoLocalCompleted :
    rhToPsiError_C006_repoLocalCompleted = false :=
  rfl

/--
C006 no-residual-integration-debt gate.

No external terminal Lean proof of the RH-to-`psi` error branch is recorded as
completed by anchor-only evidence in this artifact.  The expanded leaves remain
formalization debt until a local proof body or pinned checked upstream proof is
available.
-/
def rhToPsiError_C006_completedStateRetainsRepoLocalIntegrationDebt : Bool :=
  false

/-- Checked C006 gate: no completed state retains repo-local integration debt. -/
theorem rhToPsiError_C006_noCompletedRepoLocalIntegrationDebt :
    rhToPsiError_C006_completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## `psi`/`theta`/prime-counting bridge split for C007. -/

/--
Chebyshev-theta error at the same square-root/log-squared scale as the local
`psi` target.

This is an intermediate statement-shape target for the C007 bridge.  It is not
proved here.
-/
def ChebyshevThetaErrorBound : Prop :=
  (fun x : ℝ => Chebyshev.theta x - x)
    =O[atTop]
      (fun x : ℝ => Real.sqrt x * (Real.log x) ^ 2)

/--
Compatibility status for the current prime-counting main term.

The existing `PrimeCountingErrorBound` uses `x / log x`.  The classical
RH-sharp prime-counting transfer is normally stated with a logarithmic-integral
main term, or with enough secondary terms to absorb the `Li x - x / log x`
offset.  This status records that the C007 bridge can be split locally, but the
terminal theorem target still needs a main-term decision before closure.
-/
inductive PrimeCountingMainTermStatus where
  | currentTargetNeedsMainTermCorrection
  | logIntegralOrSecondaryTermsSelected
  | targetCompatibilityProved
  deriving DecidableEq, Repr

/--
The C007 leaves refining the bridge from a `psi` estimate through `theta` and
Abel partial summation to the prime-counting estimate.

Some leaves are checked mathlib-anchor wrappers; the analytic transfer and
target-compatibility leaves remain formalization debt.
-/
inductive PsiThetaPrimeCountingBridgeLeafId where
  | normalizeRealPrimeCounting
  | checkPsiThetaComparison
  | transferPsiErrorToThetaError
  | checkAbelSummationIdentity
  | splitThetaMainAndError
  | selectPrimeCountingMainTerm
  | boundThetaErrorContribution
  | reconcileClassicalRemainder
  | assemblePrimeCountingTarget
  deriving DecidableEq, Repr

/-- Machine status for a C007 `psi`/`theta`/prime-counting bridge leaf. -/
inductive PsiThetaPrimeCountingBridgeLeafStatus where
  | mathlibAnchorChecked
  | treeLeafExpanded
  | blockedByMainTermCompatibility
  | localProofBodyClosed
  | upstreamProofPinnedAndChecked
  deriving DecidableEq, Repr

/-- Metadata for one C007 bridge leaf. -/
structure PsiThetaPrimeCountingBridgeLeaf where
  id : PsiThetaPrimeCountingBridgeLeafId
  canonicalName : String
  upstreamInputs : List String
  localGoal : String
  outputTarget : String
  maxProofSteps : Nat
  budgetStatus : String
  machineStatus : PsiThetaPrimeCountingBridgeLeafStatus
  debtClassification : String
  repoLocalCompletedEvidence : Bool
  deriving Repr

/-- Exact mathlib declarations checked for child task `S1-M-259-C007`. -/
def checkedMathlibAnchors_C007 : List String := [
  "Chebyshev.abs_psi_sub_theta_le_sqrt_mul_log",
  "Chebyshev.primeCounting_eq_theta_div_log_add_integral",
  "Chebyshev.primeCounting_sub_theta_div_log_isBigO",
  "Nat.primeCounting"
]

/-- C007 status for the current `PrimeCountingErrorBound` main term. -/
def primeCountingMainTermStatus_C007 : PrimeCountingMainTermStatus :=
  .currentTargetNeedsMainTermCorrection

/--
C007 split of the `psi`/`theta`/prime-counting bridge into <=100-step leaves.

This is a theorem-tree budget split and partial mathlib-anchor audit, not a
proof of `ChebyshevPsiErrorBound -> PrimeCountingErrorBound`.
-/
def psiThetaPrimeCountingBridgeLeaves_C007 : List PsiThetaPrimeCountingBridgeLeaf := [
  {
    id := .normalizeRealPrimeCounting
    canonicalName := "S1-M-259.psiThetaPrimeCounting.normalizeRealPrimeCounting"
    upstreamInputs := [
      "realPrimeCounting",
      "Nat.primeCounting",
      "Nat.floor on real arguments"
    ]
    localGoal :=
      "Fix the real-argument convention `realPrimeCounting x = (Nat.primeCounting floor(x) : Real)` and expose it to Abel-summation wrappers."
    outputTarget :=
      "A stable interface for all later `pi(floor x)` bridge statements."
    maxProofSteps := 25
    budgetStatus := "expanded / <=100-step cap assigned / local definition checked"
    machineStatus := .mathlibAnchorChecked
    debtClassification := "local_wrapper_upstream_mathlib"
    repoLocalCompletedEvidence := true
  },
  {
    id := .checkPsiThetaComparison
    canonicalName := "S1-M-259.psiThetaPrimeCounting.checkPsiThetaComparison"
    upstreamInputs := [
      "Chebyshev.psi",
      "Chebyshev.theta",
      "Chebyshev.abs_psi_sub_theta_le_sqrt_mul_log"
    ]
    localGoal :=
      "Record the checked comparison `|psi x - theta x| <= 2 * sqrt x * log x` for `1 <= x`."
    outputTarget :=
      "A local wrapper usable for transferring the `psi` error scale to `theta`."
    maxProofSteps := 20
    budgetStatus := "checked mathlib wrapper / <=100-step cap satisfied"
    machineStatus := .mathlibAnchorChecked
    debtClassification := "local_wrapper_upstream_mathlib"
    repoLocalCompletedEvidence := true
  },
  {
    id := .transferPsiErrorToThetaError
    canonicalName := "S1-M-259.psiThetaPrimeCounting.transferPsiErrorToThetaError"
    upstreamInputs := [
      "ChebyshevPsiErrorBound",
      "chebyshev_absPsiSubTheta_wrapper",
      "big-O algebra at atTop"
    ]
    localGoal :=
      "Derive `ChebyshevThetaErrorBound` from the `psi` error bound plus the checked `psi - theta` estimate."
    outputTarget :=
      "A future theorem with target ChebyshevPsiErrorBound -> ChebyshevThetaErrorBound."
    maxProofSteps := 65
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .checkAbelSummationIdentity
    canonicalName := "S1-M-259.psiThetaPrimeCounting.checkAbelSummationIdentity"
    upstreamInputs := [
      "Chebyshev.primeCounting_eq_theta_div_log_add_integral",
      "realPrimeCounting",
      "interval integral notation"
    ]
    localGoal :=
      "Record the checked Abel partial-summation identity expressing prime counting through `theta / log` plus an integral of `theta / (t * log^2 t)`."
    outputTarget :=
      "A local wrapper around mathlib's prime-counting/theta Abel identity."
    maxProofSteps := 25
    budgetStatus := "checked mathlib wrapper / <=100-step cap satisfied"
    machineStatus := .mathlibAnchorChecked
    debtClassification := "local_wrapper_upstream_mathlib"
    repoLocalCompletedEvidence := true
  },
  {
    id := .splitThetaMainAndError
    canonicalName := "S1-M-259.psiThetaPrimeCounting.splitThetaMainAndError"
    upstreamInputs := [
      "ChebyshevThetaErrorBound",
      "primeCounting_eq_theta_div_log_add_integral_wrapper",
      "eventual positivity for log"
    ]
    localGoal :=
      "Substitute `theta t = t + E(t)` into the Abel identity and split the main-term integral from the error integral."
    outputTarget :=
      "A decomposition of prime counting into a selected main term plus an error contribution controlled by `E`."
    maxProofSteps := 80
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .selectPrimeCountingMainTerm
    canonicalName := "S1-M-259.psiThetaPrimeCounting.selectPrimeCountingMainTerm"
    upstreamInputs := [
      "PrimeCountingErrorBound",
      "Abel main-term integral from splitThetaMainAndError",
      "classical logarithmic-integral asymptotics"
    ]
    localGoal :=
      "Decide whether the terminal prime-counting target uses a logarithmic-integral main term, or adds secondary terms so that the existing `x / log x` target is actually compatible with RH-sharp scale."
    outputTarget :=
      "A corrected target proposition or a proved compatibility lemma for the current target."
    maxProofSteps := 70
    budgetStatus := "expanded / blocked by main-term compatibility decision"
    machineStatus := .blockedByMainTermCompatibility
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .boundThetaErrorContribution
    canonicalName := "S1-M-259.psiThetaPrimeCounting.boundThetaErrorContribution"
    upstreamInputs := [
      "ChebyshevThetaErrorBound",
      "splitThetaMainAndError",
      "integral estimates for sqrt(t) * log(t)^2 / (t * log(t)^2)"
    ]
    localGoal :=
      "Bound the endpoint and integral contributions of the theta error by the RH prime-counting error scale."
    outputTarget :=
      "An eventual bound of size `sqrt x * log x` for the theta-error contribution."
    maxProofSteps := 95
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .reconcileClassicalRemainder
    canonicalName := "S1-M-259.psiThetaPrimeCounting.reconcileClassicalRemainder"
    upstreamInputs := [
      "checked coarse theorem Chebyshev.primeCounting_sub_theta_div_log_isBigO",
      "selected prime-counting main term",
      "asymptotic comparison of classical remainder terms"
    ]
    localGoal :=
      "Ensure the non-RH main-term remainder is either absorbed by the selected target or explicitly blocks the existing `x / log x` target."
    outputTarget :=
      "A compatibility proof or blocker for the current `PrimeCountingErrorBound` proposition."
    maxProofSteps := 70
    budgetStatus := "expanded / blocked by main-term compatibility decision"
    machineStatus := .blockedByMainTermCompatibility
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .assemblePrimeCountingTarget
    canonicalName := "S1-M-259.psiThetaPrimeCounting.assemblePrimeCountingTarget"
    upstreamInputs := [
      "transferPsiErrorToThetaError",
      "boundThetaErrorContribution",
      "selectPrimeCountingMainTerm",
      "reconcileClassicalRemainder"
    ]
    localGoal :=
      "Package the corrected bridge output into the repository's final prime-counting statement shape."
    outputTarget :=
      "A future theorem with target ChebyshevPsiErrorBound -> PrimeCountingErrorBound, after target compatibility is settled."
    maxProofSteps := 45
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  }
]

/-- Checked C007 gate: the bridge is split into nine leaves. -/
theorem psiThetaPrimeCountingBridgeLeaves_C007_length :
    psiThetaPrimeCountingBridgeLeaves_C007.length = 9 :=
  rfl

/-- Checked C007 gate: every recorded leaf cap is at most 100 proof steps. -/
theorem psiThetaPrimeCountingBridgeLeaves_C007_stepCaps :
    psiThetaPrimeCountingBridgeLeaves_C007.map (fun leaf => leaf.maxProofSteps) =
      [25, 20, 65, 25, 80, 70, 95, 70, 45] :=
  rfl

/-- Checked C007 gate: the split uses the requested bridge leaf order. -/
theorem psiThetaPrimeCountingBridgeLeaves_C007_ids :
    psiThetaPrimeCountingBridgeLeaves_C007.map (fun leaf => leaf.id) = [
      PsiThetaPrimeCountingBridgeLeafId.normalizeRealPrimeCounting,
      PsiThetaPrimeCountingBridgeLeafId.checkPsiThetaComparison,
      PsiThetaPrimeCountingBridgeLeafId.transferPsiErrorToThetaError,
      PsiThetaPrimeCountingBridgeLeafId.checkAbelSummationIdentity,
      PsiThetaPrimeCountingBridgeLeafId.splitThetaMainAndError,
      PsiThetaPrimeCountingBridgeLeafId.selectPrimeCountingMainTerm,
      PsiThetaPrimeCountingBridgeLeafId.boundThetaErrorContribution,
      PsiThetaPrimeCountingBridgeLeafId.reconcileClassicalRemainder,
      PsiThetaPrimeCountingBridgeLeafId.assemblePrimeCountingTarget
    ] :=
  rfl

/-- Checked C007 gate: the current target still needs a main-term compatibility decision. -/
theorem primeCountingMainTermStatus_C007_eq :
    primeCountingMainTermStatus_C007 =
      PrimeCountingMainTermStatus.currentTargetNeedsMainTermCorrection :=
  rfl

/-- C007 does not claim theorem closure for the prime-counting bridge. -/
def psiThetaPrimeCountingBridge_C007_repoLocalCompleted : Bool :=
  false

/-- Checked C007 gate: no repo-local completion is claimed by this bridge split. -/
theorem psiThetaPrimeCountingBridge_C007_notRepoLocalCompleted :
    psiThetaPrimeCountingBridge_C007_repoLocalCompleted = false :=
  rfl

/--
C007 no-residual-integration-debt gate.

No external terminal Lean proof of the `psi`/`theta`/prime-counting transfer is
recorded as completed by anchor-only evidence in this artifact.  The unchecked
bridge leaves remain formalization debt until a local proof body or pinned
checked upstream proof is available.
-/
def psiThetaPrimeCountingBridge_C007_completedStateRetainsRepoLocalIntegrationDebt : Bool :=
  false

/-- Checked C007 gate: no completed state retains repo-local integration debt. -/
theorem psiThetaPrimeCountingBridge_C007_noCompletedRepoLocalIntegrationDebt :
    psiThetaPrimeCountingBridge_C007_completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Converse zero-exclusion branch split for C008. -/

/--
Statement-shape target for the converse route from the sharp Chebyshev `psi`
error estimate to zero exclusion off the critical line.

This proposition is not proved here; it records the intended terminal theorem
boundary for child task `S1-M-259-C008`.
-/
def ChebyshevPsiConverseZeroExclusionTarget : Prop :=
  ChebyshevPsiErrorBound -> CriticalLineZeroCriterion

/--
Statement-shape target for the converse route from the prime-counting error
estimate to zero exclusion off the critical line.

The C007 main-term compatibility blocker also applies here: the current local
`PrimeCountingErrorBound` still needs a logarithmic-integral or secondary-term
decision before this branch can be closed as a classical RH-sharp converse.
-/
def PrimeCountingConverseZeroExclusionTarget : Prop :=
  PrimeCountingErrorBound -> CriticalLineZeroCriterion

/--
The C008 leaves refining converse branches from sharp error estimates to
zero exclusion off the critical line.
-/
inductive ConverseZeroExclusionLeafId where
  | normalizeConverseTargets
  | chooseConverseAnalyticCriterion
  | buildPsiMellinTransform
  | continueLogDerivZetaFromPsiError
  | encodeOffLineZeroWitness
  | extractPoleContradiction
  | controlMultiplicityAndCancellation
  | assemblePsiConverse
  | repairPrimeCountingMainTerm
  | convertPrimeCountingErrorToPsiInput
  | assemblePrimeCountingConverse
  deriving DecidableEq, Repr

/-- Machine status for a C008 converse zero-exclusion leaf. -/
inductive ConverseZeroExclusionLeafStatus where
  | statementShapeChecked
  | treeLeafExpanded
  | blockedByPrimeCountingMainTerm
  | localProofBodyClosed
  | upstreamProofPinnedAndChecked
  deriving DecidableEq, Repr

/-- Metadata for one C008 converse zero-exclusion leaf. -/
structure ConverseZeroExclusionLeaf where
  id : ConverseZeroExclusionLeafId
  canonicalName : String
  branch : String
  upstreamInputs : List String
  localGoal : String
  outputTarget : String
  maxProofSteps : Nat
  budgetStatus : String
  machineStatus : ConverseZeroExclusionLeafStatus
  debtClassification : String
  repoLocalCompletedEvidence : Bool
  deriving Repr

/--
C008 split of the converse branches into <=100-step leaves.

This is a theorem-tree budget split and statement-boundary record, not a proof
of either converse target.
-/
def converseZeroExclusionLeaves_C008 : List ConverseZeroExclusionLeaf := [
  {
    id := .normalizeConverseTargets
    canonicalName := "S1-M-259.converseZeroExclusion.normalizeConverseTargets"
    branch := "shared statement boundary"
    upstreamInputs := [
      "ChebyshevPsiConverseZeroExclusionTarget",
      "PrimeCountingConverseZeroExclusionTarget",
      "CriticalLineZeroCriterion",
      "ChebyshevPsiErrorBound",
      "PrimeCountingErrorBound"
    ]
    localGoal :=
      "Freeze the two converse theorem targets as implications from sharp error estimates to the local zero-exclusion criterion."
    outputTarget :=
      "Stable target propositions for future terminal converse proofs."
    maxProofSteps := 30
    budgetStatus := "statement shapes checked / <=100-step cap satisfied"
    machineStatus := .statementShapeChecked
    debtClassification := "statement_boundary_only / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .chooseConverseAnalyticCriterion
    canonicalName := "S1-M-259.converseZeroExclusion.chooseConverseAnalyticCriterion"
    branch := "shared analytic criterion"
    upstreamInputs := [
      "explicit formula branch from C005",
      "Mellin/Laplace transform criterion for prime sums",
      "analytic continuation of zeta logarithmic derivative"
    ]
    localGoal :=
      "Choose and type the analytic criterion turning a prime-sum error estimate into holomorphy of the logarithmic derivative in a half-plane."
    outputTarget :=
      "A precise API contract consumed by both converse branches before the zero-witness contradiction."
    maxProofSteps := 75
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .buildPsiMellinTransform
    canonicalName := "S1-M-259.converseZeroExclusion.buildPsiMellinTransform"
    branch := "Chebyshev psi converse"
    upstreamInputs := [
      "ChebyshevPsiErrorBound",
      "von Mangoldt Dirichlet series",
      "Mellin or Stieltjes transform of Chebyshev.psi - x"
    ]
    localGoal :=
      "Build the transform identity connecting the `psi` error term with `-zeta'/zeta` in the region needed for the converse."
    outputTarget :=
      "A checked transform identity whose convergence domain reflects the assumed square-root-scale `psi` error."
    maxProofSteps := 90
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .continueLogDerivZetaFromPsiError
    canonicalName := "S1-M-259.converseZeroExclusion.continueLogDerivZetaFromPsiError"
    branch := "Chebyshev psi converse"
    upstreamInputs := [
      "buildPsiMellinTransform",
      "ChebyshevPsiErrorBound",
      "analytic continuation APIs for meromorphic functions"
    ]
    localGoal :=
      "Use the sharp `psi` error to continue the logarithmic derivative of zeta through the region where an off-line zero would create a pole."
    outputTarget :=
      "Holomorphy or removable-singularity data for `-zeta'/zeta` in the forbidden half-plane."
    maxProofSteps := 95
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .encodeOffLineZeroWitness
    canonicalName := "S1-M-259.converseZeroExclusion.encodeOffLineZeroWitness"
    branch := "shared zero contradiction"
    upstreamInputs := [
      "riemannZeta",
      "CriticalLineZeroCriterion",
      "nontrivial zero predicate",
      "functional-equation symmetry"
    ]
    localGoal :=
      "Encode a hypothetical nontrivial zero with real part different from `1 / 2` in the half-plane addressed by the converse criterion."
    outputTarget :=
      "A typed off-critical-line zero witness suitable for pole extraction."
    maxProofSteps := 70
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .extractPoleContradiction
    canonicalName := "S1-M-259.converseZeroExclusion.extractPoleContradiction"
    branch := "shared zero contradiction"
    upstreamInputs := [
      "encodeOffLineZeroWitness",
      "continueLogDerivZetaFromPsiError or prime-counting analogue",
      "local behavior of logarithmic derivatives at zeros"
    ]
    localGoal :=
      "Show that an encoded off-line zero forces a pole of the zeta logarithmic derivative, contradicting the holomorphy obtained from the error estimate."
    outputTarget :=
      "Contradiction for one off-line nontrivial zero witness."
    maxProofSteps := 95
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .controlMultiplicityAndCancellation
    canonicalName := "S1-M-259.converseZeroExclusion.controlMultiplicityAndCancellation"
    branch := "shared zero contradiction"
    upstreamInputs := [
      "extractPoleContradiction",
      "zero multiplicity API",
      "no-cancellation statement for logarithmic-derivative poles"
    ]
    localGoal :=
      "Rule out cancellation or multiplicity bookkeeping gaps when turning a zeta zero into a logarithmic-derivative pole."
    outputTarget :=
      "A multiplicity-safe pole contradiction compatible with the selected zero encoding."
    maxProofSteps := 85
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .assemblePsiConverse
    canonicalName := "S1-M-259.converseZeroExclusion.assemblePsiConverse"
    branch := "Chebyshev psi converse"
    upstreamInputs := [
      "continueLogDerivZetaFromPsiError",
      "controlMultiplicityAndCancellation",
      "CriticalLineZeroCriterion"
    ]
    localGoal :=
      "Package the `psi`-error route into the target proposition `ChebyshevPsiConverseZeroExclusionTarget`."
    outputTarget :=
      "A future theorem with target ChebyshevPsiErrorBound -> CriticalLineZeroCriterion."
    maxProofSteps := 45
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .repairPrimeCountingMainTerm
    canonicalName := "S1-M-259.converseZeroExclusion.repairPrimeCountingMainTerm"
    branch := "prime-counting converse"
    upstreamInputs := [
      "PrimeCountingErrorBound",
      "primeCountingMainTermStatus_C007",
      "logarithmic-integral or secondary-term target decision"
    ]
    localGoal :=
      "Repair or replace the current `x / log x` prime-counting main term before using it as a sharp converse hypothesis."
    outputTarget :=
      "A corrected prime-counting converse hypothesis or a proof that the current target is compatible."
    maxProofSteps := 70
    budgetStatus := "expanded / blocked by main-term compatibility decision"
    machineStatus := .blockedByPrimeCountingMainTerm
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .convertPrimeCountingErrorToPsiInput
    canonicalName := "S1-M-259.converseZeroExclusion.convertPrimeCountingErrorToPsiInput"
    branch := "prime-counting converse"
    upstreamInputs := [
      "repaired prime-counting target",
      "C007 psi/theta/prime-counting bridge",
      "partial summation and inverse partial summation APIs"
    ]
    localGoal :=
      "Convert the corrected prime-counting error estimate into the analytic input used by the `psi` converse, or build the direct transform from prime-counting data."
    outputTarget :=
      "A bridge from the prime-counting estimate to the shared converse analytic criterion."
    maxProofSteps := 95
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    id := .assemblePrimeCountingConverse
    canonicalName := "S1-M-259.converseZeroExclusion.assemblePrimeCountingConverse"
    branch := "prime-counting converse"
    upstreamInputs := [
      "repairPrimeCountingMainTerm",
      "convertPrimeCountingErrorToPsiInput",
      "controlMultiplicityAndCancellation",
      "CriticalLineZeroCriterion"
    ]
    localGoal :=
      "Package the corrected prime-counting route into the target proposition `PrimeCountingConverseZeroExclusionTarget`."
    outputTarget :=
      "A future theorem with target PrimeCountingErrorBound -> CriticalLineZeroCriterion, after main-term compatibility is settled."
    maxProofSteps := 50
    budgetStatus := "expanded / <=100-step cap assigned / proof body absent"
    machineStatus := .treeLeafExpanded
    debtClassification := "formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  }
]

/-- Checked C008 gate: the converse branch is split into eleven leaves. -/
theorem converseZeroExclusionLeaves_C008_length :
    converseZeroExclusionLeaves_C008.length = 11 :=
  rfl

/-- Checked C008 gate: every recorded leaf cap is at most 100 proof steps. -/
theorem converseZeroExclusionLeaves_C008_stepCaps :
    converseZeroExclusionLeaves_C008.map (fun leaf => leaf.maxProofSteps) =
      [30, 75, 90, 95, 70, 95, 85, 45, 70, 95, 50] :=
  rfl

/-- Checked C008 gate: the split uses the requested converse leaf order. -/
theorem converseZeroExclusionLeaves_C008_ids :
    converseZeroExclusionLeaves_C008.map (fun leaf => leaf.id) = [
      ConverseZeroExclusionLeafId.normalizeConverseTargets,
      ConverseZeroExclusionLeafId.chooseConverseAnalyticCriterion,
      ConverseZeroExclusionLeafId.buildPsiMellinTransform,
      ConverseZeroExclusionLeafId.continueLogDerivZetaFromPsiError,
      ConverseZeroExclusionLeafId.encodeOffLineZeroWitness,
      ConverseZeroExclusionLeafId.extractPoleContradiction,
      ConverseZeroExclusionLeafId.controlMultiplicityAndCancellation,
      ConverseZeroExclusionLeafId.assemblePsiConverse,
      ConverseZeroExclusionLeafId.repairPrimeCountingMainTerm,
      ConverseZeroExclusionLeafId.convertPrimeCountingErrorToPsiInput,
      ConverseZeroExclusionLeafId.assemblePrimeCountingConverse
    ] :=
  rfl

/-- C008 does not claim theorem closure for either converse branch. -/
def converseZeroExclusion_C008_repoLocalCompleted : Bool :=
  false

/-- Checked C008 gate: no repo-local completion is claimed by this converse split. -/
theorem converseZeroExclusion_C008_notRepoLocalCompleted :
    converseZeroExclusion_C008_repoLocalCompleted = false :=
  rfl

/--
C008 no-residual-integration-debt gate.

No external terminal Lean proof of the converse zero-exclusion branches is
recorded as completed by anchor-only evidence in this artifact.  The unchecked
converse leaves remain formalization debt until a local proof body or pinned
checked upstream proof is available.
-/
def converseZeroExclusion_C008_completedStateRetainsRepoLocalIntegrationDebt : Bool :=
  false

/-- Checked C008 gate: no completed state retains repo-local integration debt. -/
theorem converseZeroExclusion_C008_noCompletedRepoLocalIntegrationDebt :
    converseZeroExclusion_C008_completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Optional RH-equivalence variant decision for C009. -/

/--
Optional RH-equivalence families considered by child task `S1-M-259-C009`.

These are adjacent to the parent theorem but are not part of the current
`StatementShape`, whose core path is zeta zeroes, Chebyshev estimates, and
prime-counting estimates.
-/
inductive OptionalRHEquivalenceVariant where
  | mertensSummatoryMobius
  | mobiusPartialSums
  | liouvillePartialSums
  | robinSigmaInequality
  | lagariasSigmaHarmonicInequality
  deriving DecidableEq, Repr

/-- Placement decision for optional RH-equivalence variants. -/
inductive OptionalRHEquivalencePlacement where
  | keepInCoreStatementShape
  | splitIntoSeparateStage1Children
  deriving DecidableEq, Repr

/-- Machine status for the C009 placement decision. -/
inductive OptionalRHEquivalenceDecisionStatus where
  | placementDecisionChecked
  | terminalVariantProofClosed
  | upstreamVariantProofPinnedAndChecked
  deriving DecidableEq, Repr

/-- Metadata for one optional RH-equivalence variant placement decision. -/
structure OptionalRHEquivalenceDecision where
  variant : OptionalRHEquivalenceVariant
  canonicalChildName : String
  placement : OptionalRHEquivalencePlacement
  reason : String
  requiredAPIs : List String
  proofTreeRoot : String
  maxLeafBudget : Nat
  decisionStatus : OptionalRHEquivalenceDecisionStatus
  debtClassification : String
  repoLocalCompletedEvidence : Bool
  deriving Repr

/--
C009 decision: keep the current S1-M-259 core statement shape focused on the
Chebyshev/prime-counting route, and split optional Mertens/Mobius/Liouville/
Robin/Lagarias RH-equivalence variants into separate Stage1 children if they
are pursued.

The Mertens row refers to RH-equivalent summatory-Mobius bounds, not the
historical pointwise Mertens conjecture.
-/
def optionalRHEquivalenceDecisions_C009 : List OptionalRHEquivalenceDecision := [
  {
    variant := .mertensSummatoryMobius
    canonicalChildName := "S1-M-259.optional.mertensSummatoryMobius"
    placement := .splitIntoSeparateStage1Children
    reason :=
      "Uses summatory Mobius/Mertens-function estimates and Dirichlet inverse APIs, not the current Chebyshev-prime-counting statement package."
    requiredAPIs := [
      "ArithmeticFunction.moebius or equivalent Mobius API",
      "summatory Mertens function M(x)",
      "Dirichlet series identity 1 / zeta(s)",
      "big-O bounds M(x) = O(x^(1/2 + epsilon))"
    ]
    proofTreeRoot :=
      "RH equivalence via summatory Mobius/Mertens bounds."
    maxLeafBudget := 100
    decisionStatus := .placementDecisionChecked
    debtClassification := "statement_variant_split / formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    variant := .mobiusPartialSums
    canonicalChildName := "S1-M-259.optional.mobiusPartialSums"
    placement := .splitIntoSeparateStage1Children
    reason :=
      "Overlaps with Mertens but should be normalized as its own summatory-Mobius theorem target before any equivalence proof is attempted."
    requiredAPIs := [
      "ArithmeticFunction.moebius",
      "partial sums over n <= x",
      "Dirichlet series for moebius",
      "zero-free-region or Perron transfer for reciprocal zeta"
    ]
    proofTreeRoot :=
      "RH equivalence via Mobius partial-sum growth bounds."
    maxLeafBudget := 100
    decisionStatus := .placementDecisionChecked
    debtClassification := "statement_variant_split / formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    variant := .liouvillePartialSums
    canonicalChildName := "S1-M-259.optional.liouvillePartialSums"
    placement := .splitIntoSeparateStage1Children
    reason :=
      "Requires Liouville-function encoding and its zeta-ratio Dirichlet series, which is a distinct arithmetic-function branch from Chebyshev psi/theta."
    requiredAPIs := [
      "Liouville arithmetic function",
      "summatory Liouville function L(x)",
      "Dirichlet series identity zeta(2s) / zeta(s)",
      "partial-sum growth bound at RH scale"
    ]
    proofTreeRoot :=
      "RH equivalence via Liouville partial-sum growth bounds."
    maxLeafBudget := 100
    decisionStatus := .placementDecisionChecked
    debtClassification := "statement_variant_split / formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    variant := .robinSigmaInequality
    canonicalChildName := "S1-M-259.optional.robinSigmaInequality"
    placement := .splitIntoSeparateStage1Children
    reason :=
      "Robin's criterion is a divisor-sum inequality with an explicit finite threshold, needing sigma, Euler gamma, and finite-exception infrastructure absent from the core statement."
    requiredAPIs := [
      "sum-of-divisors function sigma",
      "Euler-Mascheroni constant",
      "finite threshold n > 5040",
      "Robin inequality sigma(n) < exp(gamma) * n * log(log n)"
    ]
    proofTreeRoot :=
      "RH equivalence via Robin's divisor-sum inequality."
    maxLeafBudget := 100
    decisionStatus := .placementDecisionChecked
    debtClassification := "statement_variant_split / formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  },
  {
    variant := .lagariasSigmaHarmonicInequality
    canonicalChildName := "S1-M-259.optional.lagariasSigmaHarmonicInequality"
    placement := .splitIntoSeparateStage1Children
    reason :=
      "Lagarias' criterion replaces the finite Robin threshold with a harmonic-number inequality for every positive integer, giving a separate elementary-divisor-sum proof tree."
    requiredAPIs := [
      "sum-of-divisors function sigma",
      "harmonic numbers H_n",
      "real exponential and logarithm inequalities",
      "Lagarias inequality sigma(n) <= H_n + exp(H_n) * log(H_n)"
    ]
    proofTreeRoot :=
      "RH equivalence via Lagarias' harmonic-number divisor-sum inequality."
    maxLeafBudget := 100
    decisionStatus := .placementDecisionChecked
    debtClassification := "statement_variant_split / formalization_debt / not_repo_local_closed"
    repoLocalCompletedEvidence := false
  }
]

/-- Checked C009 gate: all five requested optional variant families were classified. -/
theorem optionalRHEquivalenceDecisions_C009_length :
    optionalRHEquivalenceDecisions_C009.length = 5 :=
  rfl

/-- Checked C009 gate: every optional variant is split into a separate Stage1 child. -/
theorem optionalRHEquivalenceDecisions_C009_placements :
    optionalRHEquivalenceDecisions_C009.map (fun item => item.placement) = [
      OptionalRHEquivalencePlacement.splitIntoSeparateStage1Children,
      OptionalRHEquivalencePlacement.splitIntoSeparateStage1Children,
      OptionalRHEquivalencePlacement.splitIntoSeparateStage1Children,
      OptionalRHEquivalencePlacement.splitIntoSeparateStage1Children,
      OptionalRHEquivalencePlacement.splitIntoSeparateStage1Children
    ] :=
  rfl

/-- Checked C009 gate: the optional-variant decision does not alter the core statement shape. -/
theorem optionalRHEquivalenceDecisions_C009_statementShapeUnchanged :
    StatementShape ↔
      (RH ↔
        CriticalLineZeroCriterion ∧
          ChebyshevPsiErrorBound ∧
            PrimeCountingErrorBound) :=
  Iff.rfl

/-- C009 does not claim theorem closure for any optional RH-equivalence variant. -/
def optionalRHEquivalenceDecisions_C009_repoLocalCompleted : Bool :=
  false

/-- Checked C009 gate: no repo-local theorem completion is claimed by this decision. -/
theorem optionalRHEquivalenceDecisions_C009_notRepoLocalCompleted :
    optionalRHEquivalenceDecisions_C009_repoLocalCompleted = false :=
  rfl

/--
C009 no-residual-integration-debt gate.

No external terminal Lean proof of a Mertens/Mobius/Liouville/Robin/Lagarias
criterion is recorded as completed by anchor-only evidence in this artifact.
The child closes only the placement decision.
-/
def optionalRHEquivalenceDecisions_C009_completedStateRetainsRepoLocalIntegrationDebt :
    Bool :=
  false

/-- Checked C009 gate: no completed state retains repo-local integration debt. -/
theorem optionalRHEquivalenceDecisions_C009_noCompletedRepoLocalIntegrationDebt :
    optionalRHEquivalenceDecisions_C009_completedStateRetainsRepoLocalIntegrationDebt =
      false :=
  rfl

/-! ## External terminal-proof audit for C010. -/

/--
Status categories for the C010 external terminal-proof audit.

This audit is stricter than the C004 statement-only source record: it asks
whether an external Lean 4 artifact supplies a terminal proof of the RH
Chebyshev/prime-counting consequence/equivalence package that could be pinned,
imported, and checked by this Lake project.
-/
inductive ExternalTerminalProofAuditStatus where
  | noExactTerminalProofFound
  | exactTerminalProofBlockedFromIntegration
  | exactTerminalProofPinnedImportedChecked
  deriving DecidableEq, Repr

/-- Metadata for the C010 external terminal-proof audit. -/
structure ExternalTerminalProofAudit where
  auditDate : String
  repoLocalArtifact : String
  auditedMathlibRevision : String
  searchTerms : List String
  auditedCandidateSources : List String
  exactTerminalTheorem : String
  auditStatus : ExternalTerminalProofAuditStatus
  terminalProofImportedOrWrapped : Bool
  concreteIntegrationBlockers : List String
  repoLocalCompletedEvidence : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  debtClassification : String
  deriving Repr

/--
C010 record for the external terminal-proof gate.

The known external Lean source remains the C004 statement-only
`LeanMillenniumPrizeProblems` repository.  No external artifact audited here
provides a theorem that proves the local `StatementShape`, `RH ->
ChebyshevPsiErrorBound`, `RH -> PrimeCountingErrorBound`, or the converse
zero-exclusion branches as a terminal proof package.  Therefore there is no
external theorem to pin/import/check, and no completion claim is made.
-/
def externalTerminalProofAudit_C010 : ExternalTerminalProofAudit where
  auditDate := "2026-05-01"
  repoLocalArtifact := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_259.lean"
  auditedMathlibRevision := auditedMathlibPin
  searchTerms := [
    "Lean 4 RiemannHypothesis Chebyshev psi primeCounting terminal theorem",
    "RiemannHypothesis Chebyshev.psi Nat.primeCounting Lean",
    "RiemannHypothesis prime counting Chebyshev error Lean proof",
    "LeanMillenniumPrizeProblems Problems/RiemannHypothesis/Millennium.lean"
  ]
  auditedCandidateSources := [
    "repo-pinned mathlib at 8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "lean-dojo/LeanMillenniumPrizeProblems at 540da94826f70f3edf4d4fc66ce6cda20e903f61",
    "public search hit for a conditional spectral-capture RH Lean claim"
  ]
  exactTerminalTheorem := "none located"
  auditStatus := .noExactTerminalProofFound
  terminalProofImportedOrWrapped := false
  concreteIntegrationBlockers := [
    "pinned mathlib exposes RH, zeta, Chebyshev, von Mangoldt, and prime-counting substrate anchors but no terminal RH-equivalent Chebyshev/prime-counting estimate theorem",
    "LeanMillenniumPrizeProblems Riemann file is statement-only and adjacent-wrapper evidence, not a terminal proof of RH or of the local estimate package",
    "the conditional spectral-capture search hit is not an exact terminal proof for this slot because it advertises conditional assumptions rather than a dependency-pinned theorem proving the local StatementShape"
  ]
  repoLocalCompletedEvidence := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  debtClassification := "formalization_debt / not_repo_local_closed"

/-- Checked C010 status: no exact external terminal theorem was found. -/
theorem externalTerminalProofAudit_C010_status :
    externalTerminalProofAudit_C010.auditStatus =
      ExternalTerminalProofAuditStatus.noExactTerminalProofFound :=
  rfl

/-- Checked C010 gate: no external terminal theorem has been imported or wrapped locally. -/
theorem externalTerminalProofAudit_C010_notImportedOrWrapped :
    externalTerminalProofAudit_C010.terminalProofImportedOrWrapped = false :=
  rfl

/-- Checked C010 gate: this audit does not mark the parent theorem completed. -/
theorem externalTerminalProofAudit_C010_notRepoLocalCompleted :
    externalTerminalProofAudit_C010.repoLocalCompletedEvidence = false :=
  rfl

/-- Checked C010 gate: no completed state retains repo-local integration debt. -/
theorem externalTerminalProofAudit_C010_noCompletedRepoLocalIntegrationDebt :
    externalTerminalProofAudit_C010.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Public synchronization gate for C011. -/

/--
Status categories for the C011 public synchronization gate.

The public blueprint/todo/README surfaces are intentionally serial integration
targets.  This gate records whether a theorem closure exists that would trigger
that serialized public-doc patch.
-/
inductive PublicSyncGateStatus where
  | blockedNoTheoremClosure
  | readyForSerialIntegratorPatch
  | synchronizedBySerialIntegrator
  deriving DecidableEq, Repr

/-- Metadata for the C011 serial public-synchronization gate. -/
structure PublicSyncGate where
  taskId : String
  repoLocalArtifact : String
  theoremClosureAvailable : Bool
  publicDocsEditedByChild : Bool
  sharedAggregatorsEditedByChild : Bool
  requiredSerialTargets : List String
  gateStatus : PublicSyncGateStatus
  repoLocalCompletedEvidence : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  debtClassification : String
  deriving Repr

/--
C011 record for the public backfill gate.

No theorem closure exists in this artifact: C001-C010 record statement shapes,
mathlib wrappers, branch splits, blockers, and external-anchor audits, while
the terminal RH-equivalence / consequence package remains unproved locally.
Therefore this child does not edit public planning docs and does not promote
any public completion checkbox.  A serial integrator patch is required only
after a future theorem closure or after review of the open-status backfill text.
-/
def publicSyncGate_C011 : PublicSyncGate where
  taskId := "S1-M-259-C011"
  repoLocalArtifact := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_259.lean"
  theoremClosureAvailable := false
  publicDocsEditedByChild := false
  sharedAggregatorsEditedByChild := false
  requiredSerialTargets := [
    "Docs/Stage1_Blueprint.md",
    "Docs/todos_20260430.md",
    "README.md"
  ]
  gateStatus := .blockedNoTheoremClosure
  repoLocalCompletedEvidence := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  debtClassification := "public_doc_integration_gate / formalization_debt / not_repo_local_closed"

/-- Checked C011 status: public synchronization is blocked by absent theorem closure. -/
theorem publicSyncGate_C011_status :
    publicSyncGate_C011.gateStatus =
      PublicSyncGateStatus.blockedNoTheoremClosure :=
  rfl

/-- Checked C011 gate: this child did not edit public planning docs. -/
theorem publicSyncGate_C011_noPublicDocsEditedByChild :
    publicSyncGate_C011.publicDocsEditedByChild = false :=
  rfl

/-- Checked C011 gate: this child did not edit shared Lean import aggregators. -/
theorem publicSyncGate_C011_noSharedAggregatorsEditedByChild :
    publicSyncGate_C011.sharedAggregatorsEditedByChild = false :=
  rfl

/-- Checked C011 gate: no theorem completion is claimed by the public-sync gate. -/
theorem publicSyncGate_C011_notRepoLocalCompleted :
    publicSyncGate_C011.repoLocalCompletedEvidence = false :=
  rfl

/-- Checked C011 gate: no completed state retains repo-local integration debt. -/
theorem publicSyncGate_C011_noCompletedRepoLocalIntegrationDebt :
    publicSyncGate_C011.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check RH
#check RiemannHypothesis
#check StatementShape
#check CriticalLineZeroCriterion
#check PrimeCountingErrorBound
#check ChebyshevPsiErrorBound
#check criticalLineZeroCriterion_iff_mathlib_RH
#check statementShape_iff
#check Stage1MachineStatus
#check currentStage1MachineStatus
#check currentStage1MachineStatus_eq_statementShapeAndMathlibWrappersOnly
#check auditedMathlibPin
#check checkedMathlibAnchors_C002
#check TerminalEstimateBlockerStatus
#check TerminalEstimateBlocker
#check terminalEstimateBlocker_C003
#check terminalEstimateBlocker_C003_status
#check terminalEstimateBlocker_C003_notImportedOrWrapped
#check terminalEstimateBlocker_C003_notRepoLocalCompleted
#check ExternalStatementSourceStatus
#check ExternalStatementSource
#check leanMillenniumPrizeProblems_C004
#check leanMillenniumPrizeProblems_C004_status
#check leanMillenniumPrizeProblems_C004_notImportedOrWrapped
#check leanMillenniumPrizeProblems_C004_notRepoLocalCompleted
#check ExplicitFormulaLeafId
#check ExplicitFormulaLeafStatus
#check ExplicitFormulaLeaf
#check explicitFormulaLeaves_C005
#check explicitFormulaLeaves_C005_length
#check explicitFormulaLeaves_C005_ids
#check explicitFormulaTree_C005_repoLocalCompleted
#check explicitFormulaTree_C005_notRepoLocalCompleted
#check explicitFormulaTree_C005_completedStateRetainsRepoLocalIntegrationDebt
#check explicitFormulaTree_C005_noCompletedRepoLocalIntegrationDebt
#check RHPsiErrorLeafId
#check RHPsiErrorLeafStatus
#check RHPsiErrorLeaf
#check rhToPsiErrorLeaves_C006
#check rhToPsiErrorLeaves_C006_length
#check rhToPsiErrorLeaves_C006_stepCaps
#check rhToPsiErrorLeaves_C006_ids
#check rhToPsiError_C006_repoLocalCompleted
#check rhToPsiError_C006_notRepoLocalCompleted
#check rhToPsiError_C006_completedStateRetainsRepoLocalIntegrationDebt
#check rhToPsiError_C006_noCompletedRepoLocalIntegrationDebt
#check ChebyshevThetaErrorBound
#check PrimeCountingMainTermStatus
#check PsiThetaPrimeCountingBridgeLeafId
#check PsiThetaPrimeCountingBridgeLeafStatus
#check PsiThetaPrimeCountingBridgeLeaf
#check checkedMathlibAnchors_C007
#check primeCountingMainTermStatus_C007
#check psiThetaPrimeCountingBridgeLeaves_C007
#check psiThetaPrimeCountingBridgeLeaves_C007_length
#check psiThetaPrimeCountingBridgeLeaves_C007_stepCaps
#check psiThetaPrimeCountingBridgeLeaves_C007_ids
#check primeCountingMainTermStatus_C007_eq
#check psiThetaPrimeCountingBridge_C007_repoLocalCompleted
#check psiThetaPrimeCountingBridge_C007_notRepoLocalCompleted
#check psiThetaPrimeCountingBridge_C007_completedStateRetainsRepoLocalIntegrationDebt
#check psiThetaPrimeCountingBridge_C007_noCompletedRepoLocalIntegrationDebt
#check ChebyshevPsiConverseZeroExclusionTarget
#check PrimeCountingConverseZeroExclusionTarget
#check ConverseZeroExclusionLeafId
#check ConverseZeroExclusionLeafStatus
#check ConverseZeroExclusionLeaf
#check converseZeroExclusionLeaves_C008
#check converseZeroExclusionLeaves_C008_length
#check converseZeroExclusionLeaves_C008_stepCaps
#check converseZeroExclusionLeaves_C008_ids
#check converseZeroExclusion_C008_repoLocalCompleted
#check converseZeroExclusion_C008_notRepoLocalCompleted
#check converseZeroExclusion_C008_completedStateRetainsRepoLocalIntegrationDebt
#check converseZeroExclusion_C008_noCompletedRepoLocalIntegrationDebt
#check OptionalRHEquivalenceVariant
#check OptionalRHEquivalencePlacement
#check OptionalRHEquivalenceDecisionStatus
#check OptionalRHEquivalenceDecision
#check optionalRHEquivalenceDecisions_C009
#check optionalRHEquivalenceDecisions_C009_length
#check optionalRHEquivalenceDecisions_C009_placements
#check optionalRHEquivalenceDecisions_C009_statementShapeUnchanged
#check optionalRHEquivalenceDecisions_C009_repoLocalCompleted
#check optionalRHEquivalenceDecisions_C009_notRepoLocalCompleted
#check optionalRHEquivalenceDecisions_C009_completedStateRetainsRepoLocalIntegrationDebt
#check optionalRHEquivalenceDecisions_C009_noCompletedRepoLocalIntegrationDebt
#check ExternalTerminalProofAuditStatus
#check ExternalTerminalProofAudit
#check externalTerminalProofAudit_C010
#check externalTerminalProofAudit_C010_status
#check externalTerminalProofAudit_C010_notImportedOrWrapped
#check externalTerminalProofAudit_C010_notRepoLocalCompleted
#check externalTerminalProofAudit_C010_noCompletedRepoLocalIntegrationDebt
#check PublicSyncGateStatus
#check PublicSyncGate
#check publicSyncGate_C011
#check publicSyncGate_C011_status
#check publicSyncGate_C011_noPublicDocsEditedByChild
#check publicSyncGate_C011_noSharedAggregatorsEditedByChild
#check publicSyncGate_C011_notRepoLocalCompleted
#check publicSyncGate_C011_noCompletedRepoLocalIntegrationDebt
#check differentiableAt_riemannZeta_wrapper
#check trivialZero_riemannZeta_wrapper
#check riemannZeta_functionalEquation_wrapper
#check riemannZeta_dirichletSeries_wrapper
#check riemannZeta_eulerProduct_wrapper
#check vonMangoldt_sum_wrapper
#check chebyshevPsi_eq_sumTheta_wrapper
#check chebyshev_absPsiSubTheta_wrapper
#check primeCounting_eq_theta_div_log_add_integral_wrapper
#check primeCounting_sub_theta_div_log_isBigO_wrapper
#check chebyshevPsi_linearUpper_wrapper
#check primeCounting_tendsto_wrapper
#check Chebyshev.psi
#check Chebyshev.theta
#check riemannZeta
#check riemannZeta_one_sub
#check riemannZeta_eulerProduct_hasProd
#check ArithmeticFunction.vonMangoldt_sum
#check ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
#check Nat.primeCounting

end S1_M_259
end Stage1
end AwesomeTheorems
