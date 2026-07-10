import Mathlib.Probability.Martingale.OptionalSampling
import Mathlib.Probability.Martingale.OptionalStopping

/-!
# S1-M-284 / THM-M-1004: Optional stopping theorem

This Stage1 artifact records a conservative Lean 4 boundary for the optional
stopping theorem: a martingale has controlled, and in the martingale case
equal, expectation at bounded stopping times.

The pinned mathlib snapshot already contains discrete-time optional stopping
and optional sampling theorems for stopped values.  This file therefore keeps a
normalized statement shape for the equality version and provides low-risk
wrappers around the available mathlib anchors.  The repo-local equality wrapper
below is checked, while public blueprint/todo synchronization remains a serial
integration task.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems.Stage1.S1_M_284

universe uΩ

/--
Discrete-time bounded-stopping-time data for the optional stopping theorem.

The source theorem is represented in the standard bounded discrete-time form:
for stopping times `τ ≤ π`, the expected stopped values of a martingale should
agree.  The inequality direction is directly available from mathlib through the
submartingale API; the equality conclusion remains the future terminal target.
-/
structure BoundedDiscreteOptionalStoppingData (Ω : Type uΩ) [MeasurableSpace Ω]
    (μ : Measure Ω) : Type (uΩ + 1) where
  process : ℕ → Ω → ℝ
  filtration : Filtration ℕ (inferInstance : MeasurableSpace Ω)
  tau : Ω → WithTop ℕ
  pi : Ω → WithTop ℕ
  martingale : Martingale process filtration μ
  tau_stopping : IsStoppingTime filtration tau
  pi_stopping : IsStoppingTime filtration pi
  tau_le_pi : tau ≤ pi
  pi_bounded : ∃ N : ℕ, ∀ ω, pi ω ≤ N

/--
Conclusion package expected from a completed optional-stopping formalization.

The first field is the mathlib-backed inequality inherited from the martingale
as a submartingale.  The second field is the expected equality usually stated
for martingales; C004 supplies the repo-local reverse-inequality bridge below.
-/
structure BoundedDiscreteOptionalStoppingConclusion {Ω : Type uΩ}
    [MeasurableSpace Ω] {μ : Measure Ω}
    (D : BoundedDiscreteOptionalStoppingData Ω μ) : Prop where
  expected_mono :
    μ[stoppedValue D.process D.tau] ≤ μ[stoppedValue D.process D.pi]
  expected_eq :
    μ[stoppedValue D.process D.tau] = μ[stoppedValue D.process D.pi]

/--
Stage1 normalized statement shape for THM-M-1004.

For every probability space and bounded ordered pair of stopping times, a
real-valued discrete-time martingale has equal expected stopped values.  The
repository validates the statement boundary and the C004 equality wrapper
below; public theorem-surface synchronization remains integrator-owned.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type uΩ) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)) [SigmaFiniteFiltration μ ℱ]
    (f : ℕ → Ω → ℝ) (τ π : Ω → WithTop ℕ),
      Martingale f ℱ μ →
        IsStoppingTime ℱ τ →
          IsStoppingTime ℱ π →
            τ ≤ π →
              (∃ N : ℕ, ∀ ω, π ω ≤ N) →
                μ[stoppedValue f τ] = μ[stoppedValue f π]

/--
A more usable equivalent target shape with the filtration quantified before the
`SigmaFiniteFiltration` instance.
-/
def StatementShapeForFiltration : Prop :=
  StatementShape.{uΩ}

/-! ## Public statement-normalization surface -/

/--
Public statement-normalization alias for `THM-M-1004.statement`.

This is the checked Lean name that serial public backfill should cite for the
bounded discrete-time optional-stopping equality shape.  It is an alias for the
statement boundary; the checked C004 equality wrapper below supplies the local
proof body used by the terminal statement.
-/
def PublicStatementNormalization : Prop :=
  StatementShapeForFiltration.{uΩ}

/-- The public-normalization alias is definitionally the checked statement shape. -/
theorem publicStatementNormalization_iff_statementShapeForFiltration :
    PublicStatementNormalization.{uΩ} ↔ StatementShapeForFiltration.{uΩ} :=
  Iff.rfl

/-- Canonical checked declaration for the C001 public statement backfill. -/
def publicStatementNormalizationBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_284.PublicStatementNormalization"

/-- Public shared documents that must be patched only by a serial integrator. -/
def c001PublicBackfillTargets : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md"
]

/-- Checked repo-local statement names ready for the public statement backfill. -/
def c001CheckedStatementSurface : List String := [
  "StatementShape",
  "StatementShapeForFiltration",
  "PublicStatementNormalization",
  "publicStatementNormalization_iff_statementShapeForFiltration",
  "BoundedDiscreteOptionalStoppingData",
  "BoundedDiscreteOptionalStoppingConclusion"
]

/--
C001 public-statement backfill gate.

The statement surface is checked locally, but this child must not claim public
completion because the reverse inequality/equality proof and serial public-doc
sync remain open.
-/
structure PublicStatementBackfillGate where
  publicDocsRequireSerialIntegrator : Bool
  statementSurfaceChecked : Bool
  theoremCompletionClaim : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  machineDebtClassification : String
  requiredValidationCommand : String

/-- C001 gate value for public statement backfill without theorem completion. -/
def c001PublicStatementBackfillGate : PublicStatementBackfillGate where
  publicDocsRequireSerialIntegrator := true
  statementSurfaceChecked := true
  theoremCompletionClaim := false
  repoLocalIntegrationDebtRetainedAsCompleted := false
  machineDebtClassification := "formalization_debt"
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_284.lean"

/-- The C001 public backfill target set has the expected three shared surfaces. -/
theorem c001PublicBackfillTargets_length :
    c001PublicBackfillTargets.length = 3 :=
  rfl

/-- C001 records a checked statement surface but no terminal theorem completion. -/
theorem c001PublicStatementBackfillGate_no_completion :
    c001PublicStatementBackfillGate.statementSurfaceChecked = true ∧
      c001PublicStatementBackfillGate.theoremCompletionClaim = false :=
  ⟨rfl, rfl⟩

/-- C001 does not retain repo-local integration debt as a completed state. -/
theorem c001PublicStatementBackfillGate_no_completed_integration_debt :
    c001PublicStatementBackfillGate.repoLocalIntegrationDebtRetainedAsCompleted =
      false :=
  rfl

/-- The packaged optional-stopping data exposes its boundedness witness. -/
theorem bounded_witness {Ω : Type uΩ} [MeasurableSpace Ω] {μ : Measure Ω}
    (D : BoundedDiscreteOptionalStoppingData Ω μ) :
    ∃ N : ℕ, ∀ ω, D.pi ω ≤ N :=
  D.pi_bounded

/-- The packaged optional-stopping data exposes the martingale hypothesis. -/
theorem martingale_of_data {Ω : Type uΩ} [MeasurableSpace Ω] {μ : Measure Ω}
    (D : BoundedDiscreteOptionalStoppingData Ω μ) :
    Martingale D.process D.filtration μ :=
  D.martingale

/-- The packaged optional-stopping data exposes the ordered stopping times. -/
theorem stopping_times_ordered {Ω : Type uΩ} [MeasurableSpace Ω] {μ : Measure Ω}
    (D : BoundedDiscreteOptionalStoppingData Ω μ) :
    IsStoppingTime D.filtration D.tau ∧
      IsStoppingTime D.filtration D.pi ∧
        D.tau ≤ D.pi :=
  ⟨D.tau_stopping, D.pi_stopping, D.tau_le_pi⟩

section MathlibWrappers

variable {Ω : Type uΩ} [MeasurableSpace Ω] {μ : Measure Ω}
  {ℱ : Filtration ℕ (inferInstance : MeasurableSpace Ω)}
  [SigmaFiniteFiltration μ ℱ] {f : ℕ → Ω → ℝ}
  {τ π σ : Ω → WithTop ℕ}

/-- Checked mathlib wrapper: deterministic times are stopping times. -/
theorem const_stopping_time_wrapper (n : ℕ) :
    IsStoppingTime ℱ (fun _ : Ω => (n : WithTop ℕ)) :=
  isStoppingTime_const ℱ n

omit [MeasurableSpace Ω] in
/-- Checked mathlib wrapper: stopping at a deterministic time returns that process value. -/
theorem stoppedValue_const_wrapper (n : ℕ) :
    stoppedValue f (fun _ : Ω => (n : WithTop ℕ)) = f n :=
  stoppedValue_const f n

/-- Checked mathlib wrapper: deterministic stopped values have the deterministic expectation. -/
theorem integral_stoppedValue_const_wrapper (n : ℕ) :
    μ[stoppedValue f (fun _ : Ω => (n : WithTop ℕ))] = μ[f n] := by
  rw [stoppedValue_const_wrapper (f := f) n]

/--
Checked mathlib wrapper: the forward optional-stopping inequality for
submartingales and bounded stopping times.
-/
theorem submartingale_expected_stoppedValue_mono_wrapper
    (hf : Submartingale f ℱ μ)
    (hτ : IsStoppingTime ℱ τ) (hπ : IsStoppingTime ℱ π)
    (hle : τ ≤ π) {N : ℕ} (hbdd : ∀ ω, π ω ≤ N) :
    μ[stoppedValue f τ] ≤ μ[stoppedValue f π] :=
  hf.expected_stoppedValue_mono hτ hπ hle hbdd

/--
Checked mathlib wrapper: every martingale inherits the forward stopped-value
expectation inequality through its submartingale view.
-/
theorem martingale_expected_stoppedValue_mono_wrapper
    (hf : Martingale f ℱ μ)
    (hτ : IsStoppingTime ℱ τ) (hπ : IsStoppingTime ℱ π)
    (hle : τ ≤ π) {N : ℕ} (hbdd : ∀ ω, π ω ≤ N) :
    μ[stoppedValue f τ] ≤ μ[stoppedValue f π] :=
  hf.submartingale.expected_stoppedValue_mono hτ hπ hle hbdd

/--
C003 checked alias: repo-local partial verification of the forward expectation
inequality for martingales at bounded ordered stopping times.
-/
theorem c003_forwardExpectationInequality
    (hf : Martingale f ℱ μ)
    (hτ : IsStoppingTime ℱ τ) (hπ : IsStoppingTime ℱ π)
    (hle : τ ≤ π) {N : ℕ} (hbdd : ∀ ω, π ω ≤ N) :
    μ[stoppedValue f τ] ≤ μ[stoppedValue f π] :=
  martingale_expected_stoppedValue_mono_wrapper hf hτ hπ hle hbdd

/-- C003 public-doc targets remain serial-integrator-owned shared surfaces. -/
def c003PublicBackfillTargets : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md"
]

/--
C003 forward-wrapper backfill gate.

The checked declaration below is a partial verification of the forward
inequality only.  C004 below separately closes the reverse inequality and the
martingale expected stopped-value equality.
-/
structure ForwardWrapperBackfillGate where
  checkedDeclaration : String
  upstreamMathlibDeclaration : String
  partialVerificationClaim : Bool
  theoremCompletionClaim : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  machineStatus : String
  requiredValidationCommand : String

/-- C003 gate value for the forward expectation inequality wrapper. -/
def c003ForwardWrapperBackfillGate : ForwardWrapperBackfillGate where
  checkedDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.martingale_expected_stoppedValue_mono_wrapper"
  upstreamMathlibDeclaration :=
    "MeasureTheory.Submartingale.expected_stoppedValue_mono"
  partialVerificationClaim := true
  theoremCompletionClaim := false
  repoLocalIntegrationDebtRetainedAsCompleted := false
  machineStatus := "local_wrapper_upstream_mathlib"
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_284.lean"

/-- C003 records a checked partial wrapper but no terminal theorem completion. -/
theorem c003ForwardWrapperBackfillGate_no_completion :
    c003ForwardWrapperBackfillGate.partialVerificationClaim = true ∧
      c003ForwardWrapperBackfillGate.theoremCompletionClaim = false :=
  ⟨rfl, rfl⟩

/-- C003 does not retain repo-local integration debt as a completed state. -/
theorem c003ForwardWrapperBackfillGate_no_completed_integration_debt :
    c003ForwardWrapperBackfillGate.repoLocalIntegrationDebtRetainedAsCompleted =
      false :=
  rfl

omit [MeasurableSpace Ω] in
/-- C004 checked bridge: stopping the negated process negates the stopped value. -/
theorem stoppedValue_neg_wrapper :
    stoppedValue (-f) τ = -stoppedValue f τ :=
  rfl

/--
C004 checked bridge: expectation of a stopped value for `-f` is the negative of
the expectation of the stopped value for `f`.
-/
theorem expected_stoppedValue_neg_wrapper :
    μ[stoppedValue (-f) τ] = -μ[stoppedValue f τ] := by
  rw [stoppedValue_neg_wrapper]
  exact integral_neg (stoppedValue f τ)

/--
C004 reverse optional-stopping inequality for martingales.

The proof applies the forward mathlib inequality to the martingale `-f`, then
uses stopped-value negation and integral negation to reverse the order.
-/
theorem martingale_expected_stoppedValue_reverse_wrapper
    (hf : Martingale f ℱ μ)
    (hτ : IsStoppingTime ℱ τ) (hπ : IsStoppingTime ℱ π)
    (hle : τ ≤ π) {N : ℕ} (hbdd : ∀ ω, π ω ≤ N) :
    μ[stoppedValue f π] ≤ μ[stoppedValue f τ] := by
  have hneg : μ[stoppedValue (-f) τ] ≤ μ[stoppedValue (-f) π] :=
    hf.neg.submartingale.expected_stoppedValue_mono hτ hπ hle hbdd
  rw [expected_stoppedValue_neg_wrapper (f := f) (τ := τ),
    expected_stoppedValue_neg_wrapper (f := f) (τ := π)] at hneg
  exact neg_le_neg_iff.mp hneg

/--
C004 checked equality wrapper for bounded ordered stopping times of a
martingale.
-/
theorem martingale_expected_stoppedValue_eq_wrapper
    (hf : Martingale f ℱ μ)
    (hτ : IsStoppingTime ℱ τ) (hπ : IsStoppingTime ℱ π)
    (hle : τ ≤ π) {N : ℕ} (hbdd : ∀ ω, π ω ≤ N) :
    μ[stoppedValue f τ] = μ[stoppedValue f π] :=
  le_antisymm
    (martingale_expected_stoppedValue_mono_wrapper hf hτ hπ hle hbdd)
    (martingale_expected_stoppedValue_reverse_wrapper hf hτ hπ hle hbdd)

/-- C004 closes the packaged optional-stopping conclusion repo-locally. -/
theorem data_expected_eq_wrapper
    (D : BoundedDiscreteOptionalStoppingData Ω μ)
    [SigmaFiniteFiltration μ D.filtration] :
    μ[stoppedValue D.process D.tau] = μ[stoppedValue D.process D.pi] := by
  rcases D.pi_bounded with ⟨N, hN⟩
  exact martingale_expected_stoppedValue_eq_wrapper
    D.martingale D.tau_stopping D.pi_stopping D.tau_le_pi hN

/-- C004 packages both expected-value conclusions for the bounded data record. -/
theorem data_optionalStoppingConclusion_wrapper
    (D : BoundedDiscreteOptionalStoppingData Ω μ)
    [SigmaFiniteFiltration μ D.filtration] :
    BoundedDiscreteOptionalStoppingConclusion D where
  expected_mono := by
    rcases D.pi_bounded with ⟨N, hN⟩
    exact martingale_expected_stoppedValue_mono_wrapper
      D.martingale D.tau_stopping D.pi_stopping D.tau_le_pi hN
  expected_eq := data_expected_eq_wrapper D

/-- C004 checked implementation of the normalized Stage1 statement shape. -/
theorem statementShapeForFiltration_checked :
    StatementShapeForFiltration.{uΩ} := by
  intro Ω _ μ _ ℱ _ f τ π hf hτ hπ hle hbdd
  rcases hbdd with ⟨N, hN⟩
  exact martingale_expected_stoppedValue_eq_wrapper hf hτ hπ hle hN

/-- C004 public-doc targets remain serial-integrator-owned shared surfaces. -/
def c004PublicBackfillTargets : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md"
]

/--
C004 reverse-bridge gate.

The reverse inequality and equality wrapper are checked repo-locally.  This
does not directly edit public docs or mark the full Stage1 package complete;
those remain serial-public-sync and leaf-ledger tasks.
-/
structure ReverseBridgeBackfillGate where
  checkedReverseDeclaration : String
  checkedEqualityDeclaration : String
  checkedStatementDeclaration : String
  usesNegativeMartingaleBridge : Bool
  terminalEqualityCheckedRepoLocal : Bool
  publicCompletionClaim : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  machineStatus : String
  requiredValidationCommand : String

/-- C004 gate value for the checked reverse bridge and equality wrapper. -/
def c004ReverseBridgeBackfillGate : ReverseBridgeBackfillGate where
  checkedReverseDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.martingale_expected_stoppedValue_reverse_wrapper"
  checkedEqualityDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.martingale_expected_stoppedValue_eq_wrapper"
  checkedStatementDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.statementShapeForFiltration_checked"
  usesNegativeMartingaleBridge := true
  terminalEqualityCheckedRepoLocal := true
  publicCompletionClaim := false
  repoLocalIntegrationDebtRetainedAsCompleted := false
  machineStatus := "local_proof_body"
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_284.lean"

/-- C004 has a checked terminal equality wrapper but no public completion claim. -/
theorem c004ReverseBridgeBackfillGate_terminal_checked_not_public_complete :
    c004ReverseBridgeBackfillGate.terminalEqualityCheckedRepoLocal = true ∧
      c004ReverseBridgeBackfillGate.publicCompletionClaim = false :=
  ⟨rfl, rfl⟩

/-- C004 does not retain repo-local integration debt as a completed state. -/
theorem c004ReverseBridgeBackfillGate_no_completed_integration_debt :
    c004ReverseBridgeBackfillGate.repoLocalIntegrationDebtRetainedAsCompleted =
      false :=
  rfl

/--
Checked mathlib wrapper: optional stopping as the submartingale
characterization by stopped-value expectation monotonicity.
-/
theorem submartingale_iff_expected_stoppedValue_mono_wrapper
    (hadp : StronglyAdapted ℱ f) (hint : ∀ i, Integrable (f i) μ) :
    Submartingale f ℱ μ ↔
      ∀ τ π : Ω → WithTop ℕ,
        IsStoppingTime ℱ τ →
          IsStoppingTime ℱ π →
            τ ≤ π →
              (∃ N : ℕ, ∀ ω, π ω ≤ N) →
                μ[stoppedValue f τ] ≤ μ[stoppedValue f π] :=
  submartingale_iff_expected_stoppedValue_mono hadp hint

/--
Checked mathlib wrapper: optional sampling gives the stopped value at
`min σ τ` as a conditional expectation of the value stopped at `τ`.
-/
theorem optional_sampling_min_condExp_wrapper
    (hf : Martingale f ℱ μ)
    (hτ : IsStoppingTime ℱ τ) (hσ : IsStoppingTime ℱ σ)
    {n : ℕ} (hτ_le : ∀ x, τ x ≤ n)
    [SigmaFinite (μ.trim (hτ.min hσ).measurableSpace_le)] :
    stoppedValue f (fun x => min (σ x) (τ x)) =ᵐ[μ]
      μ[stoppedValue f τ | hσ.measurableSpace] :=
  hf.stoppedValue_min_ae_eq_condExp hτ hσ hτ_le

omit [SigmaFiniteFiltration μ ℱ] in
/-- C005 checked support: conditional expectation at a stopping time preserves the total integral. -/
theorem integral_condExp_stoppingTime_wrapper
    (hτ : IsStoppingTime ℱ τ)
    [SigmaFinite (μ.trim hτ.measurableSpace_le)] (g : Ω → ℝ) :
    μ[μ[g | hτ.measurableSpace]] = μ[g] :=
  integral_condExp hτ.measurableSpace_le

/--
C005 optional-sampling plus `integral_condExp` equality route.

This route is checked as a support theorem, but it carries stopped-time
sigma-finiteness assumptions that are not needed by the C004 negative
martingale bridge.  The public terminal proof should therefore keep using the
C004 bridge unless a later integrator deliberately normalizes these extra
instances in the theorem surface.
-/
theorem martingale_expected_stoppedValue_eq_optionalSampling_condExp_wrapper
    (hf : Martingale f ℱ μ)
    (hτ : IsStoppingTime ℱ τ) (hπ : IsStoppingTime ℱ π)
    (hle : τ ≤ π) {N : ℕ} (hbdd : ∀ ω, π ω ≤ N)
    [SigmaFinite (μ.trim hτ.measurableSpace_le)]
    [SigmaFinite (μ.trim (hπ.min hτ).measurableSpace_le)] :
    μ[stoppedValue f τ] = μ[stoppedValue f π] := by
  have hsample :
      stoppedValue f (fun x => min (τ x) (π x)) =ᵐ[μ]
        μ[stoppedValue f π | hτ.measurableSpace] :=
    optional_sampling_min_condExp_wrapper
      (f := f) (τ := π) (σ := τ) hf hπ hτ hbdd
  have hmin :
      stoppedValue f (fun x => min (τ x) (π x)) = stoppedValue f τ := by
    have htime : (fun x => min (τ x) (π x)) = τ := by
      funext x
      exact min_eq_left (hle x)
    rw [htime]
  calc
    μ[stoppedValue f τ]
        = μ[stoppedValue f (fun x => min (τ x) (π x))] := by
          rw [hmin]
    _ = μ[μ[stoppedValue f π | hτ.measurableSpace]] := by
          exact integral_congr_ae (μ := μ) hsample
    _ = μ[stoppedValue f π] :=
          integral_condExp_stoppingTime_wrapper hτ (stoppedValue f π)

/-- C005 public-doc targets remain serial-integrator-owned shared surfaces. -/
def c005PublicBackfillTargets : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md"
]

/--
C005 route-decision gate for the terminal optional-stopping proof.

The optional-sampling plus `integral_condExp` route is mathematically aligned
with mathlib's conditional-expectation theorem and is now represented by a
checked support wrapper.  It is not selected as the terminal route because the
already checked C004 proof has fewer side conditions and directly proves the
current bounded stopped-value equality surface.
-/
structure OptionalSamplingBridgeDecisionGate where
  checkedOptionalSamplingDeclaration : String
  checkedIntegralCondExpDeclaration : String
  checkedOptionalSamplingEqualityDeclaration : String
  selectedTerminalProofDeclaration : String
  useOptionalSamplingIntegralCondExpAsTerminalProof : Bool
  preferNegativeMartingaleReverseBridge : Bool
  optionalSamplingRouteCheckedAsSupport : Bool
  optionalSamplingRouteHasExtraSigmaFiniteStoppedTimeInstances : Bool
  publicCompletionClaim : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  machineStatus : String
  requiredValidationCommand : String

/-- C005 decision value: keep C004 as terminal proof, record optional sampling as support. -/
def c005OptionalSamplingBridgeDecisionGate : OptionalSamplingBridgeDecisionGate where
  checkedOptionalSamplingDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.optional_sampling_min_condExp_wrapper"
  checkedIntegralCondExpDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.integral_condExp_stoppingTime_wrapper"
  checkedOptionalSamplingEqualityDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.martingale_expected_stoppedValue_eq_optionalSampling_condExp_wrapper"
  selectedTerminalProofDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_284.martingale_expected_stoppedValue_eq_wrapper"
  useOptionalSamplingIntegralCondExpAsTerminalProof := false
  preferNegativeMartingaleReverseBridge := true
  optionalSamplingRouteCheckedAsSupport := true
  optionalSamplingRouteHasExtraSigmaFiniteStoppedTimeInstances := true
  publicCompletionClaim := false
  repoLocalIntegrationDebtRetainedAsCompleted := false
  machineStatus := "local_proof_body"
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_284.lean"

/-- C005 selects the already checked negative-martingale bridge for the terminal proof. -/
theorem c005OptionalSamplingBridgeDecisionGate_selects_negative_bridge :
    c005OptionalSamplingBridgeDecisionGate.useOptionalSamplingIntegralCondExpAsTerminalProof =
      false ∧
      c005OptionalSamplingBridgeDecisionGate.preferNegativeMartingaleReverseBridge =
        true :=
  ⟨rfl, rfl⟩

/-- C005 records optional sampling as checked support, not public completion. -/
theorem c005OptionalSamplingBridgeDecisionGate_support_not_public_complete :
    c005OptionalSamplingBridgeDecisionGate.optionalSamplingRouteCheckedAsSupport =
      true ∧
      c005OptionalSamplingBridgeDecisionGate.publicCompletionClaim = false :=
  ⟨rfl, rfl⟩

/-- C005 does not retain repo-local integration debt as a completed state. -/
theorem c005OptionalSamplingBridgeDecisionGate_no_completed_integration_debt :
    c005OptionalSamplingBridgeDecisionGate.repoLocalIntegrationDebtRetainedAsCompleted =
      false :=
  rfl

/--
Checked wrapper for the currently machine-verified part of the packaged data:
the forward expectation inequality closes locally via mathlib.
-/
theorem data_expected_mono_wrapper
    (D : BoundedDiscreteOptionalStoppingData Ω μ)
    [SigmaFiniteFiltration μ D.filtration] :
    μ[stoppedValue D.process D.tau] ≤ μ[stoppedValue D.process D.pi] := by
  rcases D.pi_bounded with ⟨N, hN⟩
  exact D.martingale.submartingale.expected_stoppedValue_mono
    D.tau_stopping D.pi_stopping D.tau_le_pi hN

/-- Mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.HittingTime",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.Probability.Notation"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.SigmaFiniteFiltration",
  "MeasureTheory.IsStoppingTime",
  "MeasureTheory.isStoppingTime_const",
  "MeasureTheory.stoppedValue",
  "MeasureTheory.stoppedValue_const",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.submartingale",
  "MeasureTheory.Submartingale.expected_stoppedValue_mono",
  "MeasureTheory.submartingale_iff_expected_stoppedValue_mono",
  "MeasureTheory.Martingale.stoppedValue_ae_eq_condExp_of_le_const",
  "MeasureTheory.Martingale.stoppedValue_ae_eq_condExp_of_le",
  "MeasureTheory.Martingale.stoppedValue_min_ae_eq_condExp"
]

/-- Pinned mathlib commit used by this repo-local Lean project. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Structured row for the THM-M-1004 theorem-level mathlib audit. -/
structure MathlibTheoremAuditRow where
  revision : String
  moduleName : String
  sourceLocation : String
  declarationName : String
  checkedDeclaration : String
  role : String
  closureStatus : String

/--
C002 theorem-level mathlib audit table for optional stopping/sampling anchors.

Each row names a theorem at the pinned mathlib revision and a repo-local wrapper
that type-checks through this repository's Lake dependency.  These rows close
the mathlib-audit child surface only; they do not prove the terminal martingale
expected stopped-value equality.
-/
def c002MathlibTheoremLevelAudit : List MathlibTheoremAuditRow := [
  {
    revision := mathlibPinnedRevision
    moduleName := "Mathlib.Probability.Martingale.OptionalStopping"
    sourceLocation :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Martingale/OptionalStopping.lean:43"
    declarationName := "MeasureTheory.Submartingale.expected_stoppedValue_mono"
    checkedDeclaration :=
      "AwesomeTheorems.Stage1.S1_M_284.submartingale_expected_stoppedValue_mono_wrapper"
    role :=
      "forward optional-stopping inequality for bounded ordered stopping times of a submartingale"
    closureStatus :=
      "local_wrapper_upstream_mathlib; checked support theorem, not terminal martingale equality"
  },
  {
    revision := mathlibPinnedRevision
    moduleName := "Mathlib.Probability.Martingale.OptionalStopping"
    sourceLocation :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Martingale/OptionalStopping.lean:94"
    declarationName := "MeasureTheory.submartingale_iff_expected_stoppedValue_mono"
    checkedDeclaration :=
      "AwesomeTheorems.Stage1.S1_M_284.submartingale_iff_expected_stoppedValue_mono_wrapper"
    role :=
      "characterizes submartingales by stopped-value expectation monotonicity for bounded stopping times"
    closureStatus :=
      "local_wrapper_upstream_mathlib; checked characterization, not terminal martingale equality"
  },
  {
    revision := mathlibPinnedRevision
    moduleName := "Mathlib.Probability.Martingale.OptionalSampling"
    sourceLocation :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Martingale/OptionalSampling.lean:195"
    declarationName := "MeasureTheory.Martingale.stoppedValue_min_ae_eq_condExp"
    checkedDeclaration :=
      "AwesomeTheorems.Stage1.S1_M_284.optional_sampling_min_condExp_wrapper"
    role :=
      "optional-sampling conditional-expectation bridge for stopped values at min sigma tau"
    closureStatus :=
      "local_wrapper_upstream_mathlib; checked bridge theorem, not by itself the bounded expectation equality"
  }
]

/-- C002 public-doc targets remain serial-integrator-owned shared surfaces. -/
def c002PublicBackfillTargets : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md"
]

/-- C002 validates exactly the three theorem-level mathlib audit rows requested. -/
theorem c002MathlibTheoremLevelAudit_length :
    c002MathlibTheoremLevelAudit.length = 3 :=
  rfl

/-- C002 does not close the terminal martingale expected stopped-value equality. -/
def c002MathlibAuditClosesTerminalEquality : Bool := false

/-- The C002 mathlib audit is checked support, not a theorem-completion claim. -/
theorem c002MathlibAudit_no_terminal_completion :
    c002MathlibAuditClosesTerminalEquality = false :=
  rfl

/--
Search terms used for terminal equality variants not directly wrapped here.
-/
def terminalEqualitySearchTerms : List String := [
  "optional stopping theorem",
  "optional sampling theorem",
  "expected_stoppedValue_mono",
  "stoppedValue_min_ae_eq_condExp",
  "stoppedValue_ae_eq_condExp_of_le",
  "martingale stoppedValue expectation equality",
  "μ[stoppedValue f τ] = μ[stoppedValue f π]"
]

/-- Structured row for the C006 primary-source external Lean 4 audit. -/
structure ExternalLeanAuditHit where
  projectUrl : String
  filePath : String
  theoremName : String
  commitSha : String
  toolchain : String
  license : String
  lakeIntegrationStatus : String
  role : String

/--
C006 primary-source external Lean 4 audit hits.

The search found relevant upstream Lean 4 source in the pinned mathlib
dependency.  Each hit is already inside this repository's Lake closure through
`Formalizations/Lean/lakefile.lean`; no external anchor-only completion state is
introduced here.
-/
def c006ExternalLeanAuditHits : List ExternalLeanAuditHit := [
  {
    projectUrl := "https://github.com/leanprover-community/mathlib4"
    filePath := "Mathlib/Probability/Martingale/OptionalStopping.lean:43"
    theoremName := "MeasureTheory.Submartingale.expected_stoppedValue_mono"
    commitSha := mathlibPinnedRevision
    toolchain := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    lakeIntegrationStatus :=
      "pinned/imported/checked via mathlib dependency; wrapped by submartingale_expected_stoppedValue_mono_wrapper"
    role :=
      "forward expected stopped-value inequality for bounded ordered stopping times of a submartingale"
  },
  {
    projectUrl := "https://github.com/leanprover-community/mathlib4"
    filePath := "Mathlib/Probability/Martingale/OptionalStopping.lean:72"
    theoremName := "MeasureTheory.submartingale_of_expected_stoppedValue_mono"
    commitSha := mathlibPinnedRevision
    toolchain := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    lakeIntegrationStatus :=
      "pinned/imported through Mathlib.Probability.Martingale.OptionalStopping; not needed for terminal equality wrapper"
    role :=
      "converse direction from stopped-value expectation monotonicity to submartingale"
  },
  {
    projectUrl := "https://github.com/leanprover-community/mathlib4"
    filePath := "Mathlib/Probability/Martingale/OptionalStopping.lean:94"
    theoremName := "MeasureTheory.submartingale_iff_expected_stoppedValue_mono"
    commitSha := mathlibPinnedRevision
    toolchain := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    lakeIntegrationStatus :=
      "pinned/imported/checked via mathlib dependency; wrapped by submartingale_iff_expected_stoppedValue_mono_wrapper"
    role :=
      "optional stopping characterization for submartingales and bounded ordered stopping times"
  },
  {
    projectUrl := "https://github.com/leanprover-community/mathlib4"
    filePath := "Mathlib/Probability/Martingale/OptionalSampling.lean:112"
    theoremName := "MeasureTheory.Martingale.stoppedValue_ae_eq_condExp_of_le_const"
    commitSha := mathlibPinnedRevision
    toolchain := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    lakeIntegrationStatus :=
      "pinned/imported through Mathlib.Probability.Martingale.OptionalSampling; support theorem, not direct terminal equality"
    role :=
      "bounded stopping time value as conditional expectation of a deterministic terminal martingale value"
  },
  {
    projectUrl := "https://github.com/leanprover-community/mathlib4"
    filePath := "Mathlib/Probability/Martingale/OptionalSampling.lean:141"
    theoremName := "MeasureTheory.Martingale.stoppedValue_ae_eq_condExp_of_le"
    commitSha := mathlibPinnedRevision
    toolchain := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    lakeIntegrationStatus :=
      "pinned/imported through Mathlib.Probability.Martingale.OptionalSampling; support theorem for optional sampling route"
    role :=
      "conditional-expectation bridge for two ordered bounded stopping times"
  },
  {
    projectUrl := "https://github.com/leanprover-community/mathlib4"
    filePath := "Mathlib/Probability/Martingale/OptionalSampling.lean:195"
    theoremName := "MeasureTheory.Martingale.stoppedValue_min_ae_eq_condExp"
    commitSha := mathlibPinnedRevision
    toolchain := "leanprover/lean4:v4.29.0"
    license := "Apache-2.0"
    lakeIntegrationStatus :=
      "pinned/imported/checked via mathlib dependency; wrapped by optional_sampling_min_condExp_wrapper"
    role :=
      "optional sampling theorem for the stopped value at min sigma tau"
  }
]

/-- C006 search-status marker for non-mathlib primary-source hits. -/
def c006NonMathlibPrimarySourceHitsFound : Bool := false

/-- C006 records no external anchor-only terminal proof as completed. -/
def c006RepoLocalIntegrationDebtRetainedAsCompleted : Bool := false

/-- C006 validates the six primary-source Lean audit rows recorded locally. -/
theorem c006ExternalLeanAuditHits_length :
    c006ExternalLeanAuditHits.length = 6 :=
  rfl

/-- C006 found no non-mathlib external Lean proof requiring anchor-only debt. -/
theorem c006_no_non_mathlib_anchor_only_completion :
    c006NonMathlibPrimarySourceHitsFound = false ∧
      c006RepoLocalIntegrationDebtRetainedAsCompleted = false :=
  ⟨rfl, rfl⟩

/-! ## C007 integration gate -/

/-- Structured report for the C007 external-proof integration gate. -/
structure ExternalProofIntegrationGateReport where
  nonMathlibExternalTerminalProofFound : Bool
  externalProofPinnedImportedCheckedByThisChild : Bool
  concreteExternalIntegrationBlockerRecorded : Bool
  anchorOnlyCompletionEvidenceUsed : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  terminalEqualityRepoLocalStatus : String
  publicCompletionClaim : Bool
  requiredValidationCommand : String

/--
C007 integration-gate result.

The preceding C006 audit found no non-mathlib terminal Lean 4 proof candidate.
The mathlib optional stopping/sampling anchors that were found are already
pinned through Lake, imported above, and checked through the local wrappers in
this file.  The terminal equality is represented by the repo-local C004 proof
body, not by external anchor-only evidence.
-/
def c007ExternalProofIntegrationGate : ExternalProofIntegrationGateReport where
  nonMathlibExternalTerminalProofFound := false
  externalProofPinnedImportedCheckedByThisChild := false
  concreteExternalIntegrationBlockerRecorded := false
  anchorOnlyCompletionEvidenceUsed := false
  repoLocalIntegrationDebtRetainedAsCompleted := false
  terminalEqualityRepoLocalStatus :=
    "local_proof_body via martingale_expected_stoppedValue_eq_wrapper"
  publicCompletionClaim := false
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_284.lean"

/--
C007 records no non-mathlib external terminal proof candidate requiring a new
pin/import/check action.
-/
theorem c007ExternalProofIntegrationGate_no_external_candidate :
    c007ExternalProofIntegrationGate.nonMathlibExternalTerminalProofFound =
      false :=
  rfl

/-- C007 uses no anchor-only evidence and keeps no completed integration debt. -/
theorem c007ExternalProofIntegrationGate_no_completed_integration_debt :
    c007ExternalProofIntegrationGate.anchorOnlyCompletionEvidenceUsed = false ∧
      c007ExternalProofIntegrationGate.repoLocalIntegrationDebtRetainedAsCompleted =
        false :=
  ⟨rfl, rfl⟩

/-- C007 does not make a public Stage1 completion claim. -/
theorem c007ExternalProofIntegrationGate_no_public_completion_claim :
    c007ExternalProofIntegrationGate.publicCompletionClaim = false :=
  rfl

/-- C007 is consistent with the C006 non-mathlib external-audit result. -/
theorem c007ExternalProofIntegrationGate_inherits_c006_audit :
    c006NonMathlibPrimarySourceHitsFound = false ∧
      c006RepoLocalIntegrationDebtRetainedAsCompleted = false :=
  c006_no_non_mathlib_anchor_only_completion

/-! ## C008 leaf-ledger expansion -/

/-- M0387-style independent leaf ledger row for the optional-stopping package. -/
structure OptionalStoppingLeafLedger where
  leafId : String
  package : String
  target : String
  closureEvidence : String
  status : String
  debtClass : String
  localBudget : Nat
  publicCompletionAllowed : Bool

/--
C008 integration-ready leaf ledger for `OST.L001` through `OST.L022`.

The rows are process/proof ledgers, not public completion evidence.  Several
machine rows are already checked by declarations in this file, but the public
completion flag stays false until the serial public sync surfaces are updated.
-/
def c008OptionalStoppingLeafLedgers : List OptionalStoppingLeafLedger := [
  {
    leafId := "OST.L001"
    package := "OST.P2.mathlib-object-model"
    target := "Verify deterministic stopping times through isStoppingTime_const."
    closureEvidence := "const_stopping_time_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 10
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L002"
    package := "OST.P2.mathlib-object-model"
    target := "Verify deterministic stopped values through stoppedValue_const."
    closureEvidence := "stoppedValue_const_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 10
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L003"
    package := "OST.P2.mathlib-object-model"
    target := "Rewrite deterministic stopped-value expectations."
    closureEvidence := "integral_stoppedValue_const_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 10
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L004"
    package := "OST.P3.forward-inequality"
    target := "Instantiate Submartingale.expected_stoppedValue_mono for bounded stopping times."
    closureEvidence := "submartingale_expected_stoppedValue_mono_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 20
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L005"
    package := "OST.P3.forward-inequality"
    target := "Derive the forward martingale inequality from the submartingale view."
    closureEvidence := "martingale_expected_stoppedValue_mono_wrapper and c003_forwardExpectationInequality"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 20
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L006"
    package := "OST.P3.forward-inequality"
    target := "Record the optional-stopping characterization of submartingales."
    closureEvidence := "submartingale_iff_expected_stoppedValue_mono_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 25
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L007"
    package := "OST.P4.optional-sampling-bridge"
    target := "Instantiate Martingale.stoppedValue_min_ae_eq_condExp."
    closureEvidence := "optional_sampling_min_condExp_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 25
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L008"
    package := "OST.P1.statement-normalization"
    target := "Expose packaged boundedness, martingale, and stopping-time order fields."
    closureEvidence := "bounded_witness, martingale_of_data, stopping_times_ordered"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 20
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L009"
    package := "OST.P3.forward-inequality"
    target := "Prove the packaged forward expected stopped-value inequality."
    closureEvidence := "data_expected_mono_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 25
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L010"
    package := "OST.P7.repo-local-gate"
    target := "Audit whether a direct imported equality theorem exists."
    closureEvidence := "c006ExternalLeanAuditHits and c006_no_non_mathlib_anchor_only_completion"
    status := "checked_repo_local_audit"
    debtClass := "none"
    localBudget := 60
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L011"
    package := "OST.P5.reverse-inequality"
    target := "Rewrite stopped values of the negated process."
    closureEvidence := "stoppedValue_neg_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 10
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L012"
    package := "OST.P5.reverse-inequality"
    target := "Use Martingale.neg for the negated process route."
    closureEvidence := "martingale_expected_stoppedValue_reverse_wrapper uses hf.neg"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 20
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L013"
    package := "OST.P5.reverse-inequality"
    target := "Derive the reverse inequality via the forward theorem applied to -f."
    closureEvidence := "expected_stoppedValue_neg_wrapper and martingale_expected_stoppedValue_reverse_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 35
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L014"
    package := "OST.P6.equality-closure"
    target := "Combine forward and reverse inequalities by antisymmetry."
    closureEvidence := "martingale_expected_stoppedValue_eq_wrapper"
    status := "checked_repo_local"
    debtClass := "none"
    localBudget := 20
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L015"
    package := "OST.P4.optional-sampling-bridge"
    target := "Record the optional-sampling plus integral_condExp equality route."
    closureEvidence := "martingale_expected_stoppedValue_eq_optionalSampling_condExp_wrapper"
    status := "checked_repo_local_support"
    debtClass := "none"
    localBudget := 50
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L016"
    package := "OST.P6.equality-closure"
    target := "Account for stopped-value integrability side conditions."
    closureEvidence := "absorbed by pinned mathlib optional-stopping theorems used by local wrappers"
    status := "checked_by_imported_mathlib_side_conditions"
    debtClass := "none"
    localBudget := 40
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L017"
    package := "OST.P1.statement-normalization"
    target := "Decide the probability and sigma-finite filtration assumptions."
    closureEvidence := "StatementShape and StatementShapeForFiltration"
    status := "checked_repo_local_statement_boundary"
    debtClass := "none"
    localBudget := 30
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L018"
    package := "OST.P1.statement-normalization"
    target := "Use WithTop Nat stopping-time values as the public Lean surface."
    closureEvidence := "BoundedDiscreteOptionalStoppingData and StatementShape"
    status := "checked_repo_local_statement_boundary"
    debtClass := "none"
    localBudget := 25
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L019"
    package := "OST.P1.statement-normalization"
    target := "Keep the terminal equality surface ordered by tau <= pi."
    closureEvidence := "StatementShape and martingale_expected_stoppedValue_eq_wrapper"
    status := "checked_repo_local_statement_boundary"
    debtClass := "none"
    localBudget := 25
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L020"
    package := "OST.P6.equality-closure"
    target := "Add or skip a deterministic-time corollary after public route selection."
    closureEvidence := "not required for statementShapeForFiltration_checked"
    status := "unchecked_optional_corollary"
    debtClass := "formalization_debt"
    localBudget := 45
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L021"
    package := "OST.P7.repo-local-gate"
    target := "Merge theorem-level audit rows into the public Stage1 surface."
    closureEvidence := "c002MathlibTheoremLevelAudit is checked locally; public docs are integrator-owned"
    status := "public_sync_pending"
    debtClass := "formalization_debt"
    localBudget := 30
    publicCompletionAllowed := false
  },
  {
    leafId := "OST.L022"
    package := "OST.P7.repo-local-gate"
    target := "Synchronize README, todo, and blueprint state after all gates agree."
    closureEvidence := "serial public-sync task remains outside this child write scope"
    status := "public_sync_pending"
    debtClass := "formalization_debt"
    localBudget := 30
    publicCompletionAllowed := false
  }
]

/-- C008 records exactly the requested `OST.L001` through `OST.L022` rows. -/
theorem c008OptionalStoppingLeafLedgers_length :
    c008OptionalStoppingLeafLedgers.length = 22 :=
  rfl

/-- C008 preserves the canonical optional-stopping leaf ids. -/
theorem c008OptionalStoppingLeafLedgers_ids :
    c008OptionalStoppingLeafLedgers.map OptionalStoppingLeafLedger.leafId =
      ["OST.L001", "OST.L002", "OST.L003", "OST.L004", "OST.L005",
        "OST.L006", "OST.L007", "OST.L008", "OST.L009", "OST.L010",
        "OST.L011", "OST.L012", "OST.L013", "OST.L014", "OST.L015",
        "OST.L016", "OST.L017", "OST.L018", "OST.L019", "OST.L020",
        "OST.L021", "OST.L022"] :=
  rfl

/-- Every C008 leaf has an explicit local proof/process budget at or below 100. -/
theorem c008OptionalStoppingLeafLedgers_budgets_within_cap :
    ((c008OptionalStoppingLeafLedgers.map OptionalStoppingLeafLedger.localBudget).all
      fun n => decide (n ≤ 100)) = true :=
  rfl

/-- No individual C008 ledger row is public theorem-completion evidence. -/
theorem c008OptionalStoppingLeafLedgers_no_public_completion :
    c008OptionalStoppingLeafLedgers.map
      OptionalStoppingLeafLedger.publicCompletionAllowed =
        [false, false, false, false, false, false, false, false, false, false,
          false, false, false, false, false, false, false, false, false, false,
          false, false] :=
  rfl

/-- C008 summary gate for the expanded leaf-ledger child. -/
structure OptionalStoppingLeafLedgerGate where
  requestedLeavesExpanded : Bool
  allLeafBudgetsAtMost100 : Bool
  terminalEqualityRepoLocalChecked : Bool
  optionalCorollaryStillOpen : Bool
  serialPublicSyncComplete : Bool
  publicCompletionClaimAllowed : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  requiredValidationCommand : String

/-- C008 gate value: leaf expansion is checked locally, public completion is not claimed. -/
def c008OptionalStoppingLeafLedgerGate : OptionalStoppingLeafLedgerGate where
  requestedLeavesExpanded := true
  allLeafBudgetsAtMost100 := true
  terminalEqualityRepoLocalChecked := true
  optionalCorollaryStillOpen := true
  serialPublicSyncComplete := false
  publicCompletionClaimAllowed := false
  repoLocalIntegrationDebtRetainedAsCompleted := false
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_284.lean"

/-- C008 expands the requested ledger but does not claim public completion. -/
theorem c008OptionalStoppingLeafLedgerGate_expanded_not_public_complete :
    c008OptionalStoppingLeafLedgerGate.requestedLeavesExpanded = true ∧
      c008OptionalStoppingLeafLedgerGate.publicCompletionClaimAllowed = false :=
  ⟨rfl, rfl⟩

/-- C008 keeps all row budgets under the M0387 leaf cap. -/
theorem c008OptionalStoppingLeafLedgerGate_budget_cap :
    c008OptionalStoppingLeafLedgerGate.allLeafBudgetsAtMost100 = true :=
  rfl

/-- C008 records no completed-state repo-local integration debt. -/
theorem c008OptionalStoppingLeafLedgerGate_no_completed_integration_debt :
    c008OptionalStoppingLeafLedgerGate.repoLocalIntegrationDebtRetainedAsCompleted =
      false :=
  rfl

/-- C008 still requires serial public synchronization outside this child scope. -/
theorem c008OptionalStoppingLeafLedgerGate_public_sync_pending :
    c008OptionalStoppingLeafLedgerGate.serialPublicSyncComplete = false :=
  rfl

/-! ## C009 public-sync integration boundary -/

/--
C009 public-sync gate.

The terminal equality, theorem-level audit rows, external-audit/integration
gate, and leaf-ledger table are represented in this repo-local Lean artifact.
The actual public document patch is intentionally not performed here because
the blueprint, todo, and README surfaces are serial-integrator-owned.
-/
structure PublicSyncIntegratorGate where
  localTerminalEqualityChecked : Bool
  mathlibAuditRowsChecked : Bool
  externalIntegrationGateChecked : Bool
  leafLedgerExpanded : Bool
  optionalDeterministicCorollaryResolvedOrDropped : Bool
  serialPublicDocsIntegratorRequired : Bool
  publicDocsPatchedByThisChild : Bool
  publicCompletionClaimAllowed : Bool
  repoLocalIntegrationDebtRetainedAsCompleted : Bool
  requiredValidationCommand : String

/--
C009 gate value: prepare the public backfill plan without editing shared public
documents or claiming public completion.
-/
def c009PublicSyncIntegratorGate : PublicSyncIntegratorGate where
  localTerminalEqualityChecked := true
  mathlibAuditRowsChecked := true
  externalIntegrationGateChecked := true
  leafLedgerExpanded := true
  optionalDeterministicCorollaryResolvedOrDropped := false
  serialPublicDocsIntegratorRequired := true
  publicDocsPatchedByThisChild := false
  publicCompletionClaimAllowed := false
  repoLocalIntegrationDebtRetainedAsCompleted := false
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_284.lean"

/-- C009 records checked local proof/audit prerequisites for integrator review. -/
theorem c009PublicSyncIntegratorGate_local_prerequisites :
    c009PublicSyncIntegratorGate.localTerminalEqualityChecked = true ∧
      c009PublicSyncIntegratorGate.mathlibAuditRowsChecked = true ∧
        c009PublicSyncIntegratorGate.externalIntegrationGateChecked = true ∧
          c009PublicSyncIntegratorGate.leafLedgerExpanded = true :=
  ⟨rfl, rfl, rfl, rfl⟩

/-- C009 keeps public document patching in the serial integrator lane. -/
theorem c009PublicSyncIntegratorGate_serial_public_docs :
    c009PublicSyncIntegratorGate.serialPublicDocsIntegratorRequired = true ∧
      c009PublicSyncIntegratorGate.publicDocsPatchedByThisChild = false :=
  ⟨rfl, rfl⟩

/-- C009 does not permit a public completion claim from this child pass. -/
theorem c009PublicSyncIntegratorGate_no_public_completion :
    c009PublicSyncIntegratorGate.publicCompletionClaimAllowed = false :=
  rfl

/-- C009 does not retain repo-local integration debt as a completed state. -/
theorem c009PublicSyncIntegratorGate_no_completed_integration_debt :
    c009PublicSyncIntegratorGate.repoLocalIntegrationDebtRetainedAsCompleted =
      false :=
  rfl

end MathlibWrappers

end AwesomeTheorems.Stage1.S1_M_284
