import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.RingTheory.MvPolynomial.Basic

/-!
# S1-M-160 / THM-M-1255: Malgrange-Ehrenpreis theorem

This Stage1 artifact records a conservative Lean 4 boundary for the
Malgrange-Ehrenpreis theorem: every nonzero constant-coefficient linear PDE
operator on a finite-dimensional real Euclidean space has a fundamental
solution.

The pinned mathlib snapshot has tempered distributions, Schwartz functions,
Dirac delta, directional derivatives on tempered distributions, Fourier
transform infrastructure, and multivariate polynomials.  This file therefore
uses those objects to freeze a statement shape.  It does not define the full
polynomial-to-differential-operator calculus, but it now records the exact
repo-local interface that such a calculus must provide.  It does not claim the
terminal existence theorem.
-/

noncomputable section

open scoped SchwartzMap

namespace AwesomeTheorems.Stage1.S1_M_160

universe u

/-- Finite-dimensional real Euclidean space used for the normalized PDE statement. -/
abbrev Space (ι : Type u) [Fintype ι] : Type u :=
  EuclideanSpace ℝ ι

/-- Complex-valued tempered distributions on the finite-dimensional real domain. -/
abbrev TemperedDist (ι : Type u) [Fintype ι] : Type u :=
  𝓢'(Space ι, ℂ)

/-- The Dirac delta distribution at the origin. -/
def diracDeltaAtZero (ι : Type u) [Fintype ι] : TemperedDist ι :=
  TemperedDistribution.delta (0 : Space ι)

/--
Directional derivative as a continuous linear map on tempered distributions.

This is a checked mathlib anchor for the distributional derivative side of a
future constant-coefficient differential-operator calculus.
-/
def directionalDerivativeCLM (ι : Type u) [Fintype ι] (v : Space ι) :
    TemperedDist ι →L[ℂ] TemperedDist ι :=
  LineDeriv.lineDerivOpCLM ℂ (TemperedDist ι) v

/-- Linear endomorphism algebra of complex-valued tempered distributions. -/
abbrev OperatorEnd (ι : Type u) [Fintype ι] : Type u :=
  Module.End ℂ (TemperedDist ι)

/-- Standard real coordinate vector `e_i` in `EuclideanSpace ℝ ι`. -/
def coordinateDirection (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) : Space ι :=
  EuclideanSpace.single i (1 : ℝ)

/--
The distributional coordinate derivative `∂_{e_i}` as a linear endomorphism.

This is the checked variable-level action that a future canonical
`MvPolynomial ι ℂ` operator calculus must assign to `MvPolynomial.X i`.
-/
def coordinateDerivativeEnd (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    OperatorEnd ι :=
  directionalDerivativeCLM ι (coordinateDirection ι i)

/--
The Fourier-side scalar convention used by mathlib for derivatives.

With mathlib's Fourier transform convention, the transform of a directional
derivative is multiplication by `(2 * π * Complex.I)` times the corresponding
linear coordinate function.
-/
def mathlibFourierDerivativeConvention : ℂ :=
  2 * Real.pi * Complex.I

/-- The Fourier multiplier coordinate function attached to a real direction. -/
def fourierDirectionMultiplier (ι : Type u) [Fintype ι] (v : Space ι) :
    TemperedDist ι →L[ℂ] TemperedDist ι :=
  TemperedDistribution.smulLeftCLM ℂ (fun x : Space ι => (inner ℝ x v : ℂ))

/-- The Fourier multiplier coordinate function attached to `MvPolynomial.X i`. -/
def fourierCoordinateMultiplier
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) :
    TemperedDist ι →L[ℂ] TemperedDist ι :=
  fourierDirectionMultiplier ι (coordinateDirection ι i)

/--
Repo-local interface for the canonical constant-coefficient polynomial action.

The target `Module.End ℂ (TemperedDist ι)` is not a commutative algebra, so the
ordinary `MvPolynomial.aeval` API is not directly applicable without first
formalizing the commutation of the coordinate derivative endomorphisms.  This
structure is therefore an integration-ready contract: constructing a value of
it is the precise remaining Lean task for the canonical
`MvPolynomial ι ℂ -> 𝓢'(EuclideanSpace ℝ ι, ℂ) ->ₗ[ℂ]
𝓢'(EuclideanSpace ℝ ι, ℂ)` action.
-/
structure PolynomialDifferentialOperatorAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] : Type u where
  toAlgHom : MvPolynomial ι ℂ →ₐ[ℂ] OperatorEnd ι
  map_X : ∀ i : ι, toAlgHom (MvPolynomial.X i) = coordinateDerivativeEnd ι i

/--
Stage1 object model for a constant-coefficient differential operator.

The `symbol` field records the polynomial symbol.  The `action` field records
the induced linear endomorphism on tempered distributions.  The
`action_has_symbol` proof slot is deliberately explicit: the audited local
mathlib snapshot does not yet expose a canonical construction from
`MvPolynomial ι ℂ` to the corresponding constant-coefficient distributional
operator.
-/
structure ConstantCoefficientDifferentialOperator
    (ι : Type u) [Fintype ι] [DecidableEq ι] : Type u where
  symbol : MvPolynomial ι ℂ
  action : TemperedDist ι →ₗ[ℂ] TemperedDist ι
  action_has_symbol : Prop
  action_has_symbol_proof : action_has_symbol

/--
A fundamental solution for `P` is a tempered distribution `E` with `P E = δ_0`.

This is the distributional equation boundary for the Malgrange-Ehrenpreis
statement.  The existence of such an `E` for every nonzero symbol remains
formalization debt in this Stage1 artifact.
-/
def FundamentalSolution {ι : Type u} [Fintype ι] [DecidableEq ι]
    (P : ConstantCoefficientDifferentialOperator ι) (E : TemperedDist ι) : Prop :=
  P.action E = diracDeltaAtZero ι

/--
Normalized Stage1 statement shape for THM-M-1255.

For every finite-dimensional real coordinate space and every constant-
coefficient differential operator with nonzero polynomial symbol, there exists
a tempered fundamental solution.
-/
def StatementShape (ι : Type u) [Fintype ι] [DecidableEq ι] : Prop :=
  ∀ P : ConstantCoefficientDifferentialOperator ι,
    P.symbol ≠ 0 → ∃ E : TemperedDist ι, FundamentalSolution P E

/-- Definitional introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro {ι : Type u} [Fintype ι] [DecidableEq ι]
    (h : ∀ P : ConstantCoefficientDifferentialOperator ι,
      P.symbol ≠ 0 → ∃ E : TemperedDist ι, FundamentalSolution P E) :
    StatementShape ι :=
  h

/-- The fundamental-solution predicate unfolds to `P E = δ_0`. -/
theorem fundamentalSolution_iff {ι : Type u} [Fintype ι] [DecidableEq ι]
    (P : ConstantCoefficientDifferentialOperator ι) (E : TemperedDist ι) :
    FundamentalSolution P E ↔ P.action E = diracDeltaAtZero ι :=
  Iff.rfl

/-- Checked mathlib anchor: the origin delta acts by evaluating a Schwartz function at zero. -/
theorem diracDeltaAtZero_apply {ι : Type u} [Fintype ι] (φ : 𝓢(Space ι, ℂ)) :
    diracDeltaAtZero ι φ = φ (0 : Space ι) :=
  TemperedDistribution.delta_apply (0 : Space ι) φ

/-- Checked mathlib anchor: `directionalDerivativeCLM` applies as the line-derivative operator. -/
theorem directionalDerivativeCLM_apply
    {ι : Type u} [Fintype ι] (v : Space ι) (T : TemperedDist ι) :
    directionalDerivativeCLM ι v T = LineDeriv.lineDerivOp v T :=
  LineDeriv.lineDerivOpCLM_apply v T

/-- The coordinate derivative endomorphism applies as the corresponding line derivative. -/
theorem coordinateDerivativeEnd_apply
    {ι : Type u} [Fintype ι] [DecidableEq ι] (i : ι) (T : TemperedDist ι) :
    coordinateDerivativeEnd ι i T = LineDeriv.lineDerivOp (coordinateDirection ι i) T :=
  LineDeriv.lineDerivOpCLM_apply (coordinateDirection ι i) T

/--
Checked coordinate-level Fourier symbol identity.

This is the repo-local anchor for the child task's `2*pi*i` convention:
mathlib proves that, after Fourier transform, the coordinate derivative
corresponding to `MvPolynomial.X i` is multiplication by
`2 * Real.pi * Complex.I` times the coordinate frequency function.
-/
theorem fourier_coordinateDerivativeEnd_eq
    {ι : Type u} [Fintype ι] [DecidableEq ι] (i : ι) (T : TemperedDist ι) :
    FourierTransform.fourier (coordinateDerivativeEnd ι i T) =
      mathlibFourierDerivativeConvention •
        fourierCoordinateMultiplier ι i (FourierTransform.fourier T) := by
  simpa [coordinateDerivativeEnd_apply, fourierCoordinateMultiplier,
    fourierDirectionMultiplier, mathlibFourierDerivativeConvention] using
    TemperedDistribution.fourier_lineDerivOp_eq T (coordinateDirection ι i)

/-- Constants in any polynomial action act through the scalar endomorphism algebra map. -/
theorem PolynomialDifferentialOperatorAction.map_C
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (A : PolynomialDifferentialOperatorAction ι) (c : ℂ) :
    A.toAlgHom (MvPolynomial.C c) = algebraMap ℂ (OperatorEnd ι) c := by
  exact A.toAlgHom.commutes c

/-- Package a polynomial action value as the Stage1 operator model. -/
def polynomialDifferentialOperatorFromAction
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (A : PolynomialDifferentialOperatorAction ι) (P : MvPolynomial ι ℂ) :
    ConstantCoefficientDifferentialOperator ι where
  symbol := P
  action := A.toAlgHom P
  action_has_symbol := A.toAlgHom P = A.toAlgHom P
  action_has_symbol_proof := rfl

/-- The variable polynomial `X i` acts by the coordinate derivative endomorphism. -/
theorem polynomialDifferentialOperatorFromAction_X_action
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (A : PolynomialDifferentialOperatorAction ι) (i : ι) :
    (polynomialDifferentialOperatorFromAction A (MvPolynomial.X i)).action =
      coordinateDerivativeEnd ι i :=
  A.map_X i

/--
Fundamental-solution predicate specialized to operators built from a polynomial
action.

The proof-producing construction for Malgrange-Ehrenpreis must eventually
construct an `E` for every nonzero `P` satisfying this predicate.
-/
def PolynomialFundamentalSolution
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (A : PolynomialDifferentialOperatorAction ι)
    (P : MvPolynomial ι ℂ) (_hP : P ≠ 0) (E : TemperedDist ι) : Prop :=
  FundamentalSolution (polynomialDifferentialOperatorFromAction A P) E

/--
Nonzero-polynomial form of the Malgrange-Ehrenpreis statement for a fixed
polynomial action.
-/
def PolynomialStatementShape
    (ι : Type u) [Fintype ι] [DecidableEq ι]
    (A : PolynomialDifferentialOperatorAction ι) : Prop :=
  ∀ (P : MvPolynomial ι ℂ) (hP : P ≠ 0),
    ∃ E : TemperedDist ι, PolynomialFundamentalSolution A P hP E

/--
Integration-ready contract for the fundamental-solution construction.

This is not a construction of Malgrange-Ehrenpreis.  It records the exact Lean
object that must be supplied after the distribution-division or inverse-symbol
machinery exists: for every nonzero polynomial symbol, return a tempered
distribution and prove the fundamental-solution equation.
-/
structure FundamentalSolutionConstruction
    (ι : Type u) [Fintype ι] [DecidableEq ι] : Type u where
  operatorAction : PolynomialDifferentialOperatorAction ι
  fundamentalSolution :
    (P : MvPolynomial ι ℂ) → P ≠ 0 → TemperedDist ι
  fundamentalSolution_spec :
    ∀ (P : MvPolynomial ι ℂ) (hP : P ≠ 0),
      PolynomialFundamentalSolution operatorAction P hP (fundamentalSolution P hP)

/-- The specialized polynomial predicate unfolds to the concrete `P(D)E = δ_0` equation. -/
theorem polynomialFundamentalSolution_iff
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (A : PolynomialDifferentialOperatorAction ι)
    (P : MvPolynomial ι ℂ) (hP : P ≠ 0) (E : TemperedDist ι) :
    PolynomialFundamentalSolution A P hP E ↔
      (polynomialDifferentialOperatorFromAction A P).action E = diracDeltaAtZero ι :=
  Iff.rfl

/--
Any future construction contract proves the defining equation for the returned
fundamental solution.
-/
theorem FundamentalSolutionConstruction.solves_symbol_equation
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (C : FundamentalSolutionConstruction ι)
    (P : MvPolynomial ι ℂ) (hP : P ≠ 0) :
    (polynomialDifferentialOperatorFromAction C.operatorAction P).action
        (C.fundamentalSolution P hP) = diracDeltaAtZero ι :=
  C.fundamentalSolution_spec P hP

/-- Any future construction contract yields the polynomial-specialized statement shape. -/
theorem FundamentalSolutionConstruction.polynomialStatementShape
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (C : FundamentalSolutionConstruction ι) :
    PolynomialStatementShape ι C.operatorAction := by
  intro P hP
  exact ⟨C.fundamentalSolution P hP, C.fundamentalSolution_spec P hP⟩

/-- mathlib modules checked while locating repo-local anchors for this PDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Basic",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Deriv",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Fourier",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.Support",
  "Mathlib.Analysis.InnerProductSpace.PiL2",
  "Mathlib.RingTheory.MvPolynomial.Basic"
]

/-- Nearby checked names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "TemperedDistribution",
  "SchwartzMap",
  "TemperedDistribution.delta",
  "TemperedDistribution.delta_apply",
  "TemperedDistribution.fourier_delta_zero",
  "TemperedDistribution.derivCLM",
  "TemperedDistribution.lineDerivOp_apply_apply",
  "TemperedDistribution.lineDerivOpCLM_eq",
  "TemperedDistribution.fourier_lineDerivOp_eq",
  "TemperedDistribution.fourierInv_lineDerivOp_eq",
  "TemperedDistribution.smulLeftCLM",
  "FourierTransform.fourier",
  "Real.pi",
  "Complex.I",
  "LineDeriv.lineDerivOpCLM",
  "MvPolynomial",
  "Module.End",
  "EuclideanSpace.single"
]

/-- Search terms that did not locate a terminal Malgrange-Ehrenpreis theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Malgrange",
  "Ehrenpreis",
  "Malgrange-Ehrenpreis",
  "fundamental solution",
  "constant coefficient PDE",
  "constant-coefficient differential operator",
  "linear partial differential operator",
  "polynomial symbol",
  "division of distributions"
]

/--
Audit decision for the distribution-division / Bernstein-Sato-adjacent child.

This is intentionally a data audit rather than a theorem claim.  The checked
objects above show that the pinned mathlib snapshot has tempered
distributions, Fourier transform, Dirac delta, distributional derivatives, and
Fourier multiplier infrastructure.  The local source search did not locate a
distribution-division theorem, Bernstein-Sato polynomial API, D-module API, or
terminal Malgrange-Ehrenpreis theorem.  Therefore this child remains
formalization debt, not repo-local completion.
-/
def distributionDivisionBernsteinSatoAuditDecision : List String := [
  "available: tempered distributions, Schwartz functions, Dirac delta, distributional derivatives",
  "available: Fourier transform and Fourier-side derivative identities for tempered distributions",
  "available: Fourier multiplier infrastructure, but not inverse-symbol division for arbitrary polynomial symbols",
  "nearby but unrelated: Bernstein polynomial approximation APIs, not Bernstein-Sato b-functions",
  "not found: distribution-division theorem suitable for Malgrange-Ehrenpreis",
  "not found: Bernstein-Sato, D-module, or holonomic-module API suitable for this PDE slot",
  "decision: keep THM-M-1255 open as formalization_debt until these APIs are built or pinned externally"
]

/--
Remaining proof leaves for turning the fundamental-solution construction
contract into a closed Malgrange-Ehrenpreis proof.
-/
def fundamentalSolutionConstructionLeaves : List String := [
  "define or import the canonical polynomial differential-operator action",
  "define a division or inverse-symbol construction for every nonzero polynomial symbol",
  "prove the constructed tempered distribution is well-defined",
  "prove the Fourier-side inverse-symbol identity for the constructed distribution",
  "transport the Fourier-side identity back to the distribution equation P(D)E = delta_0",
  "pin/import/check any future external Lean 4 construction before claiming completion"
]

/-- Search terms retained for the distribution-division / Bernstein-Sato audit. -/
def absentDistributionDivisionBernsteinSatoSearchTerms : List String := [
  "distribution division",
  "division of distributions",
  "Bernstein-Sato",
  "BernsteinSato",
  "b-function",
  "DModule",
  "D-module",
  "holonomic"
]

/--
Repo-local completion statuses for a possible future external Lean 4 proof.

M0387 forbids treating anchor-only evidence as completion.  For this PDE slot,
only the `pinnedImportedChecked` branch is allowed to count as a repo-local
completion gate.
-/
inductive ExternalLeanProofStatus : Type
  | noExternalProofLocated
  | externalAnchorOnly
  | integrationBlocked
  | pinnedImportedChecked
  deriving DecidableEq

/-- Whether an external-proof status is allowed to count as repo-local completion. -/
def ExternalLeanProofStatus.countsAsRepoLocalCompletion :
    ExternalLeanProofStatus → Bool
  | .pinnedImportedChecked => true
  | .noExternalProofLocated => false
  | .externalAnchorOnly => false
  | .integrationBlocked => false

/--
The data that must be recorded before a future external Lean 4 proof can close
the Malgrange-Ehrenpreis slot through an upstream route.
-/
structure PinnedExternalLeanProofCertificate : Type where
  upstreamProject : String
  upstreamRevision : String
  upstreamModule : String
  upstreamTheorem : String
  localImportModule : String
  localWrapperName : String
  localValidationCommand : String

/--
The exact repo-local validation command required by this Stage1 child for the
current artifact.
-/
def externalProofRequiredValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_160.lean"

/--
Completion contract for a future external Lean 4 proof.

It is intentionally a certificate shape rather than a theorem claim: no value of
this structure is constructed in this file.  A future integrator must provide the
upstream pin, local import/wrapper names, and a proof that the validation command
matches the required repo-local Lean check.
-/
structure ExternalProofCompletionGate : Type where
  certificate : PinnedExternalLeanProofCertificate
  validationCommand_eq :
    certificate.localValidationCommand = externalProofRequiredValidationCommand
  status : ExternalLeanProofStatus
  status_checked :
    status = .pinnedImportedChecked

/--
Current external-proof audit decision for THM-M-1255.

No terminal external Lean 4 proof has been pinned, imported, or checked in this
repository.  Therefore the current status is explicitly non-completing.
-/
def currentExternalLeanProofStatus : ExternalLeanProofStatus :=
  .noExternalProofLocated

/-- Anchor-only external evidence cannot count as repo-local completion. -/
theorem externalAnchorOnly_not_repoLocalCompletion :
    ExternalLeanProofStatus.countsAsRepoLocalCompletion
      .externalAnchorOnly = false :=
  rfl

/-- An integration blocker cannot be reclassified as repo-local completion. -/
theorem integrationBlocked_not_repoLocalCompletion :
    ExternalLeanProofStatus.countsAsRepoLocalCompletion
      .integrationBlocked = false :=
  rfl

/-- The current no-external-proof status cannot count as repo-local completion. -/
theorem currentExternalLeanProofStatus_not_repoLocalCompletion :
    ExternalLeanProofStatus.countsAsRepoLocalCompletion
      currentExternalLeanProofStatus = false :=
  rfl

/--
Search terms retained for a future external Lean 4 proof audit before any status
upgrade.  If one of these searches locates a proof, the next step is not
anchor-only completion; it is pin/import/check or a concrete blocker.
-/
def futureExternalLeanProofSearchTerms : List String := [
  "Malgrange Ehrenpreis Lean",
  "Malgrange-Ehrenpreis Lean 4",
  "Malgrange Ehrenpreis mathlib",
  "fundamental solution constant coefficient PDE Lean",
  "distribution division Lean",
  "Bernstein-Sato Lean",
  "D-module Lean"
]

/--
Repo-local integration leaves for a future external Lean 4 proof.
-/
def externalLeanProofIntegrationLeaves : List String := [
  "locate a public Lean 4 proof of the full Malgrange-Ehrenpreis theorem or the exact construction contract",
  "record upstream project, revision, module, theorem name, and license compatibility",
  "pin or vendor the upstream dependency in the Lean project without editing shared aggregators concurrently",
  "add a repo-local wrapper theorem or certificate that imports the upstream theorem",
  "run the required local validation command and record the exact result",
  "only then change the external-proof status to pinnedImportedChecked"
]

/-- The audit decision records seven concrete rows. -/
theorem distributionDivisionBernsteinSatoAuditDecision_length :
    distributionDivisionBernsteinSatoAuditDecision.length = 7 :=
  rfl

/-- The fundamental-solution construction ledger records six remaining proof leaves. -/
theorem fundamentalSolutionConstructionLeaves_length :
    fundamentalSolutionConstructionLeaves.length = 6 :=
  rfl

/-- The future external-proof search ledger records seven concrete search terms. -/
theorem futureExternalLeanProofSearchTerms_length :
    futureExternalLeanProofSearchTerms.length = 7 :=
  rfl

/-- The external-proof integration ledger records six remaining proof leaves. -/
theorem externalLeanProofIntegrationLeaves_length :
    externalLeanProofIntegrationLeaves.length = 6 :=
  rfl

/-! ## Audit probes -/

#check Space
#check TemperedDist
#check diracDeltaAtZero
#check directionalDerivativeCLM
#check OperatorEnd
#check coordinateDirection
#check coordinateDerivativeEnd
#check PolynomialDifferentialOperatorAction
#check ConstantCoefficientDifferentialOperator
#check FundamentalSolution
#check StatementShape
#check StatementShape.intro
#check fundamentalSolution_iff
#check diracDeltaAtZero_apply
#check directionalDerivativeCLM_apply
#check coordinateDerivativeEnd_apply
#check mathlibFourierDerivativeConvention
#check fourierDirectionMultiplier
#check fourierCoordinateMultiplier
#check fourier_coordinateDerivativeEnd_eq
#check PolynomialDifferentialOperatorAction.map_C
#check polynomialDifferentialOperatorFromAction
#check polynomialDifferentialOperatorFromAction_X_action
#check PolynomialFundamentalSolution
#check PolynomialStatementShape
#check FundamentalSolutionConstruction
#check polynomialFundamentalSolution_iff
#check FundamentalSolutionConstruction.solves_symbol_equation
#check FundamentalSolutionConstruction.polynomialStatementShape
#check TemperedDistribution.delta
#check TemperedDistribution.fourier_delta_zero
#check TemperedDistribution.fourier_lineDerivOp_eq
#check distributionDivisionBernsteinSatoAuditDecision
#check fundamentalSolutionConstructionLeaves
#check absentDistributionDivisionBernsteinSatoSearchTerms
#check ExternalLeanProofStatus
#check ExternalLeanProofStatus.countsAsRepoLocalCompletion
#check PinnedExternalLeanProofCertificate
#check externalProofRequiredValidationCommand
#check ExternalProofCompletionGate
#check currentExternalLeanProofStatus
#check externalAnchorOnly_not_repoLocalCompletion
#check integrationBlocked_not_repoLocalCompletion
#check currentExternalLeanProofStatus_not_repoLocalCompletion
#check futureExternalLeanProofSearchTerms
#check externalLeanProofIntegrationLeaves
#check distributionDivisionBernsteinSatoAuditDecision_length
#check fundamentalSolutionConstructionLeaves_length
#check futureExternalLeanProofSearchTerms_length
#check externalLeanProofIntegrationLeaves_length

end AwesomeTheorems.Stage1.S1_M_160
