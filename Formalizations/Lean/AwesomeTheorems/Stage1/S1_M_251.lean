import Mathlib.Probability.Moments.Tilted
import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.MeasureTheory.Measure.Portmanteau
import Mathlib.Data.EReal.Operations

/-!
# S1-M-251 / THM-M-1059: Cramer's theorem, Stage1 statement shape

This file records a conservative Lean 4 boundary for Cramer's theorem in large
deviations for sums of independent identically distributed real random
variables.

The pinned mathlib snapshot has a substantial probability substrate:
independence of random variables, finite-sum MGF/CGF factorization, Chernoff
bounds, the integrability interval for exponential moments, analytic MGFs/CGFs,
tilted measures, weak-convergence/portmanteau infrastructure, and limsup/liminf
order APIs.  This audit did not locate a terminal large-deviation principle or
Legendre-Fenchel Cramer theorem in mathlib.

Accordingly this file provides a checked statement shape and low-risk wrappers
around the available mathlib anchors.  The terminal LDP scale decision is to
use a custom extended-rate API: probabilities stay in `ℝ≥0∞`, scaled
log-probabilities and rates are compared in `EReal`, and the current
`ℝ`-valued rate shape remains only a finite-rate compatibility sketch.  The
fields
`exponentialTightnessBridge`, `convexDualityBridge`, `lowerBoundBridge`, and
`terminalCramerConclusion` mark the remaining formalization boundary.  No
terminal proof of Cramer's theorem is claimed here.
-/

noncomputable section

open MeasureTheory Filter Finset Real Set
open scoped MeasureTheory ProbabilityTheory ENNReal NNReal Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_251

universe u

/-- Empirical mean of the first `n` real random variables in a sequence. -/
def sampleMean {Ω : Type u} (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  (n : ℝ)⁻¹ * ∑ i ∈ Finset.range n, X i ω

/--
The finite-rate Cramer shape, written as the Legendre-Fenchel transform of the
cumulant-generating function of the reference variable.

This is intentionally only an `ℝ`-valued compatibility sketch.  Child
`S1-M-251-C004` fixes the terminal LDP target to a custom extended-rate API
using `ℝ≥0∞` probabilities and `EReal` scaled log/rate values.
-/
def cramerRateFunction {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X0 : Ω → ℝ) (x : ℝ) : ℝ :=
  sSup (Set.range fun t : ℝ => t * x - ProbabilityTheory.cgf X0 μ t)

/-- Candidate scales considered for the terminal Cramer LDP statement. -/
inductive TerminalLDPScaleChoice where
  | real
  | ereal
  | customExtendedRate
deriving DecidableEq, Repr

/--
Child `S1-M-251-C004` decision: use a custom extended-rate API, not the current
plain `ℝ` sketch and not a raw `EReal`-only package.
-/
def terminalLDPScaleDecision : TerminalLDPScaleChoice :=
  .customExtendedRate

/--
Terminal-scale data for a future Cramer LDP proof.

The custom API separates the measure-level probability value (`ℝ≥0∞`) from the
ordered comparison scale (`EReal`).  This records the boundary needed for
zero-probability events, infinite rate values, and finite-rate compatibility
with the existing `cgf`/Legendre-Fenchel sketch.
-/
structure CramerTerminalScale {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X0 : Ω → ℝ) where
  extendedLog : ℝ≥0∞ → EReal
  extendedLog_zero : extendedLog 0 = ⊥
  extendedLog_one : extendedLog 1 = 0
  extendedLog_mono : Monotone extendedLog
  rate : ℝ → EReal
  rate_nonnegative : ∀ x : ℝ, (0 : EReal) ≤ rate x
  finiteRateCompatibility : Prop

/-- Infimum of the terminal extended Cramer rate over an event. -/
def cramerTerminalRateInf {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (s : Set ℝ) : EReal :=
  sInf (Set.image S.rate s)

/--
Scaled log-probability on the terminal extended scale.

The shifted index matches the finite-rate sketch above and avoids a displayed
division by zero.
-/
def cramerTerminalScaledLogProbability {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ)
    (s : Set ℝ) (n : ℕ) : EReal :=
  ((((n + 1 : ℕ) : ℝ)⁻¹ : ℝ) : EReal) *
    S.extendedLog (μ {ω | sampleMean X (n + 1) ω ∈ s})

/-- Closed-set upper-bound package on the chosen terminal extended scale. -/
def cramerTerminalUpperBound {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ F : Set ℝ,
    IsClosed F →
      limsup (fun n : ℕ => cramerTerminalScaledLogProbability S X F n) atTop ≤
        -cramerTerminalRateInf S F

/-- Open-set lower-bound package on the chosen terminal extended scale. -/
def cramerTerminalLowerBound {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ G : Set ℝ,
    IsOpen G →
      -cramerTerminalRateInf S G ≤
        liminf (fun n : ℕ => cramerTerminalScaledLogProbability S X G n) atTop

/-- Terminal extended-scale LDP conclusion selected by child `S1-M-251-C004`. -/
def CramerTerminalExtendedConclusion {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  cramerTerminalUpperBound S X ∧ cramerTerminalLowerBound S X

/--
Exposed point predicate for the terminal extended Cramer rate.

The witness `t` is the exposing slope.  The strict inequality is stated only
for distinct points, so this package can later be specialized to differentiable
points of the finite `cgf`/Legendre-Fenchel transform without deciding those
convex-analysis details in this Stage1 boundary.
-/
def cramerTerminalExposedPoint {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (x : ℝ) : Prop :=
  ∃ t : ℝ, ∀ y : ℝ, y ≠ x → S.rate y > S.rate x + ((t * (y - x) : ℝ) : EReal)

/--
Local lower-bound target at a single point.

For every open neighborhood of `x`, the scaled log-probability lower limit is
bounded below by the negative rate at `x`.
-/
def cramerTerminalPointLowerBound {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) (x : ℝ) : Prop :=
  ∀ G : Set ℝ,
    IsOpen G →
      x ∈ G →
        -S.rate x ≤
          liminf (fun n : ℕ => cramerTerminalScaledLogProbability S X G n) atTop

/--
Tilted-measure lower-bound interface at exposed points.

The parameter `t` is expected to be the exposing slope and to lie in the
interior exponential-integrability domain.  This package isolates the future
change-of-measure, LLN/weak-convergence, and exponential prefactor estimates.
-/
def cramerTerminalTiltedExposedLowerBound {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ x t : ℝ,
    cramerTerminalExposedPoint S x →
      t ∈ interior (ProbabilityTheory.integrableExpSet X0 μ) →
        cramerTerminalPointLowerBound S X x

/--
Approximation interface for nonexposed points.

Every point in an open set with finite or infinite terminal rate must be
approximated inside that open set by exposed points whose rates converge from
above in the order needed by the LDP lower-bound passage.
-/
def cramerTerminalNonexposedApproximation {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) : Prop :=
  ∀ x : ℝ,
    ∀ G : Set ℝ,
      IsOpen G →
        x ∈ G →
          ∃ xs : ℕ → ℝ,
            (∀ n : ℕ, xs n ∈ G) ∧
              (∀ n : ℕ, cramerTerminalExposedPoint S (xs n)) ∧
                Tendsto xs atTop (𝓝 x) ∧
                  Tendsto (fun n : ℕ => S.rate (xs n)) atTop (𝓝 (S.rate x))

/--
Bridge from exposed-point lower bounds and nonexposed-point approximation to
the full open-set lower LDP bound.

This is the C006 proof-package boundary: the bridge remains formalization debt
until the order/topology and rate-infimum passage is proved or imported.
-/
def cramerTerminalOpenSetLowerBridge {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  cramerTerminalTiltedExposedLowerBound S X →
    cramerTerminalNonexposedApproximation S →
      cramerTerminalLowerBound S X

/--
Compose the C006 lower-bound interfaces once the missing open-set bridge has
been supplied.

The proof is only a projection through the bridge hypothesis; the bridge itself
is exactly the unproved open-set LDP lower-bound formalization debt.
-/
theorem terminal_lower_from_openSetBridge {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ)
    (hbridge : cramerTerminalOpenSetLowerBridge S X)
    (hexposed : cramerTerminalTiltedExposedLowerBound S X)
    (happrox : cramerTerminalNonexposedApproximation S) :
    cramerTerminalLowerBound S X :=
  hbridge hexposed happrox

/-- The child `S1-M-251-C004` scale decision is definitionally the custom API. -/
theorem terminalLDPScaleDecision_eq_custom :
    terminalLDPScaleDecision = TerminalLDPScaleChoice.customExtendedRate :=
  rfl

/-- Project the zero-probability log convention from the terminal scale package. -/
theorem terminalScale_extendedLog_zero {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) :
    S.extendedLog 0 = ⊥ :=
  S.extendedLog_zero

/-- Project nonnegativity of the selected extended Cramer rate. -/
theorem terminalScale_rate_nonnegative {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (x : ℝ) :
    (0 : EReal) ≤ S.rate x :=
  S.rate_nonnegative x

/--
Upper-tail half-line upper bound on the selected terminal scale.

This is the first Chernoff-to-LDP upper-bound interface: prove the LDP upper
estimate for closed right half-lines before compact or arbitrary closed sets.
-/
def cramerTerminalUpperTailHalfLineBound {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ a : ℝ,
    limsup (fun n : ℕ => cramerTerminalScaledLogProbability S X (Set.Ici a) n)
        atTop ≤
      -cramerTerminalRateInf S (Set.Ici a)

/--
Lower-tail half-line upper bound on the selected terminal scale.

Closed left half-lines are needed with closed right half-lines to localize
bounded intervals before passing to general compact and closed sets.
-/
def cramerTerminalLowerTailHalfLineBound {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ a : ℝ,
    limsup (fun n : ℕ => cramerTerminalScaledLogProbability S X (Set.Iic a) n)
        atTop ≤
      -cramerTerminalRateInf S (Set.Iic a)

/-- The two Chernoff-driven half-line upper-bound interfaces. -/
def cramerTerminalChernoffHalfLinePackage {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  cramerTerminalUpperTailHalfLineBound S X ∧
    cramerTerminalLowerTailHalfLineBound S X

/--
Compact-set upper bound on the selected terminal scale.

This interface is intentionally stronger than half-lines and weaker than the
full closed-set LDP upper bound.  It is the finite-cover/interval localization
stage of the Cramer upper-bound proof.
-/
def cramerTerminalCompactUpperBound {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ K : Set ℝ,
    IsCompact K →
      limsup (fun n : ℕ => cramerTerminalScaledLogProbability S X K n) atTop ≤
        -cramerTerminalRateInf S K

/--
The tightness/exhaustion bridge from compact upper bounds to arbitrary closed
upper bounds.

This remains a proof-package interface, not a theorem closure.  A later proof
must instantiate it from exponential tightness and rate-function compact-level
properties on the selected `EReal` scale.
-/
def cramerTerminalClosedSetUpperBridge {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ) : Prop :=
  cramerTerminalChernoffHalfLinePackage S X →
    cramerTerminalCompactUpperBound S X →
      cramerTerminalUpperBound S X

/--
Compose the C005 upper-bound interfaces once the missing bridge package has
been supplied.

The proof is only a projection through the bridge hypothesis; the bridge itself
is exactly the unproved closed-set LDP upper-bound formalization debt.
-/
theorem terminal_upper_from_closedSetBridge {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X0 : Ω → ℝ}
    (S : CramerTerminalScale μ X0) (X : ℕ → Ω → ℝ)
    (hbridge : cramerTerminalClosedSetUpperBridge S X)
    (hhalf : cramerTerminalChernoffHalfLinePackage S X)
    (hcompact : cramerTerminalCompactUpperBound S X) :
    cramerTerminalUpperBound S X :=
  hbridge hhalf hcompact

/-- One integration-ready leaf in the C005 Cramer upper-bound package split. -/
structure CramerUpperBoundLeafLedgerRow where
  leafId : String
  role : String
  localBudgetUpperBound : ℕ
  status : String
  closesTerminalTheorem : Bool

/--
Child `S1-M-251-C005` upper-bound package ledger.

Every row is budgeted as a `<=100`-step leaf or subleaf.  The checked rows are
only local wrappers/interfaces; the package does not close Cramer's theorem
until the closed-set bridge is proved or imported and validated repo-locally.
-/
def childC005UpperBoundLeafLedger : List CramerUpperBoundLeafLedgerRow := [
  {
    leafId := "S1-M-251-C005-L01-finite-sum-upper-chernoff",
    role :=
      "Use ProbabilityTheory.measure_ge_le_exp_cgf for finite-sum right-tail events.",
    localBudgetUpperBound := 20,
    status := "checked_local_wrapper: chernoff_upper_sum",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L02-finite-sum-lower-chernoff",
    role :=
      "Use ProbabilityTheory.measure_le_le_exp_cgf for finite-sum left-tail events.",
    localBudgetUpperBound := 20,
    status := "checked_local_wrapper: chernoff_lower_sum",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L03-sample-mean-event-rescale",
    role :=
      "Rewrite sample-mean half-line events as finite-sum half-line events with the shifted positive index.",
    localBudgetUpperBound := 45,
    status := "formalization_debt: event algebra not yet proved on terminal scale",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L04-cgf-sum-normalization",
    role :=
      "Combine cgf_sum_range, identical distribution, and the n+1 normalization into the scaled Chernoff exponent.",
    localBudgetUpperBound := 60,
    status := "formalization_debt: exponent normalization not yet connected to EReal scaled log",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L05-upper-tail-rate-optimization",
    role :=
      "Optimize the right-tail Chernoff exponent over nonnegative parameters and compare with the terminal rate infimum on Ici a.",
    localBudgetUpperBound := 90,
    status := "formalization_debt: convex-duality/rate bridge missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L06-lower-tail-rate-optimization",
    role :=
      "Optimize the left-tail Chernoff exponent over nonpositive parameters and compare with the terminal rate infimum on Iic a.",
    localBudgetUpperBound := 90,
    status := "formalization_debt: convex-duality/rate bridge missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L07-interval-upper-bound",
    role :=
      "Combine left and right half-line estimates to obtain closed bounded interval upper bounds.",
    localBudgetUpperBound := 80,
    status := "formalization_debt: finite union/intersection limsup step missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L08-compact-finite-cover",
    role :=
      "Pass from interval estimates to compact-set upper bounds by finite cover and rate-infimum comparison.",
    localBudgetUpperBound := 95,
    status := "formalization_debt: compact-cover/rate-infimum package missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L09-exponential-tight-exhaustion",
    role :=
      "Use exponential tightness or a rate-level coercivity substitute to control the closed-set tail outside compact intervals.",
    localBudgetUpperBound := 95,
    status := "formalization_debt: exponential-tightness bridge missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C005-L10-closed-set-upper-bridge",
    role :=
      "Compose compact upper bounds with the tail exhaustion bridge to prove cramerTerminalUpperBound for arbitrary closed sets.",
    localBudgetUpperBound := 70,
    status := "checked_interface_only: cramerTerminalClosedSetUpperBridge and terminal_upper_from_closedSetBridge",
    closesTerminalTheorem := false
  }
]

/-- Number of C005 upper-bound leaves in the integration-ready ledger. -/
theorem childC005UpperBoundLeafLedger_length :
    childC005UpperBoundLeafLedger.length = 10 :=
  rfl

/-- Checked guard: all C005 upper-bound leaves are budgeted at `<=100` steps. -/
theorem childC005UpperBoundLeafLedger_budgets :
    (childC005UpperBoundLeafLedger.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true :=
  rfl

/-- Checked guard: no C005 row claims terminal Cramer theorem closure. -/
theorem childC005UpperBoundLeafLedger_noTerminalClosure :
    (childC005UpperBoundLeafLedger.map (fun row => row.closesTerminalTheorem)).all
      (fun closed => closed = false) = true :=
  rfl

/-- One integration-ready leaf in the C006 Cramer lower-bound package split. -/
structure CramerLowerBoundLeafLedgerRow where
  leafId : String
  role : String
  localBudgetUpperBound : ℕ
  status : String
  closesTerminalTheorem : Bool

/--
Child `S1-M-251-C006` lower-bound package ledger.

Every row is budgeted as a `<=100`-step leaf or subleaf.  The checked rows are
only local wrappers/interfaces; the package does not close Cramer's theorem
until the tilted-measure and nonexposed-approximation bridges are proved or
imported and validated repo-locally.
-/
def childC006LowerBoundLeafLedger : List CramerLowerBoundLeafLedgerRow := [
  {
    leafId := "S1-M-251-C006-L01-exposed-point-predicate",
    role :=
      "Define exposed points of the terminal extended rate by a strict supporting slope inequality.",
    localBudgetUpperBound := 25,
    status := "checked_interface_only: cramerTerminalExposedPoint",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L02-pointwise-open-neighborhood-lower-bound",
    role :=
      "State the point lower-bound target for every open neighborhood of a candidate point.",
    localBudgetUpperBound := 25,
    status := "checked_interface_only: cramerTerminalPointLowerBound",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L03-tilted-mean-anchor",
    role :=
      "Use ProbabilityTheory.integral_tilted_mul_self to identify the tilted mean with the cgf derivative at interior parameters.",
    localBudgetUpperBound := 20,
    status := "checked_local_wrapper: integral_tilted_reference_eq_deriv_cgf",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L04-exposed-slope-domain-selection",
    role :=
      "Relate an exposing slope to the interior exponential-integrability domain required by the tilted-measure API.",
    localBudgetUpperBound := 70,
    status := "formalization_debt: convex-duality/domain-selection bridge missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L05-change-of-measure-localization",
    role :=
      "Convert original-measure probabilities of neighborhoods into tilted-measure probabilities and exponential prefactors.",
    localBudgetUpperBound := 90,
    status := "formalization_debt: tilted finite-product/change-of-measure package missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L06-tilted-lln-neighborhood-mass",
    role :=
      "Prove tilted empirical means put nonexponential mass in every open neighborhood of the tilted mean.",
    localBudgetUpperBound := 95,
    status := "formalization_debt: LLN/weak-convergence-to-neighborhood package missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L07-exposed-point-lower-bound",
    role :=
      "Combine tilted localization, tilted mean convergence, and rate identification to prove point lower bounds at exposed points.",
    localBudgetUpperBound := 95,
    status := "checked_interface_only: cramerTerminalTiltedExposedLowerBound",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L08-nonexposed-point-approximation",
    role :=
      "Approximate arbitrary points inside open sets by exposed points with terminal rates converging to the target rate.",
    localBudgetUpperBound := 95,
    status := "checked_interface_only: cramerTerminalNonexposedApproximation",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L09-rate-infimum-passage",
    role :=
      "Pass from point lower bounds and approximating exposed points to the rate infimum over the open set.",
    localBudgetUpperBound := 85,
    status := "formalization_debt: EReal sInf/open-set order passage missing",
    closesTerminalTheorem := false
  },
  {
    leafId := "S1-M-251-C006-L10-open-set-lower-bridge",
    role :=
      "Compose the exposed-point package with nonexposed approximation to prove cramerTerminalLowerBound for arbitrary open sets.",
    localBudgetUpperBound := 70,
    status := "checked_interface_only: cramerTerminalOpenSetLowerBridge and terminal_lower_from_openSetBridge",
    closesTerminalTheorem := false
  }
]

/-- Number of C006 lower-bound leaves in the integration-ready ledger. -/
theorem childC006LowerBoundLeafLedger_length :
    childC006LowerBoundLeafLedger.length = 10 :=
  rfl

/-- Checked guard: all C006 lower-bound leaves are budgeted at `<=100` steps. -/
theorem childC006LowerBoundLeafLedger_budgets :
    (childC006LowerBoundLeafLedger.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true :=
  rfl

/-- Checked guard: no C006 row claims terminal Cramer theorem closure. -/
theorem childC006LowerBoundLeafLedger_noTerminalClosure :
    (childC006LowerBoundLeafLedger.map (fun row => row.closesTerminalTheorem)).all
      (fun closed => closed = false) = true :=
  rfl

/--
Closed-set upper-bound half of the large-deviation principle for empirical
means.

The index is shifted to `n + 1` to avoid division by zero in the displayed
logarithmic scale.
-/
def cramerUpperBound {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ F : Set ℝ,
    IsClosed F →
      limsup
          (fun n : ℕ =>
            ((n + 1 : ℕ) : ℝ)⁻¹ *
              log (μ.real {ω | sampleMean X (n + 1) ω ∈ F}))
          atTop ≤
        -sInf (cramerRateFunction μ (X 0) '' F)

/--
Open-set lower-bound half of the large-deviation principle for empirical
means.
-/
def cramerLowerBound {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ℕ → Ω → ℝ) : Prop :=
  ∀ G : Set ℝ,
    IsOpen G →
      -sInf (cramerRateFunction μ (X 0) '' G) ≤
        liminf
          (fun n : ℕ =>
            ((n + 1 : ℕ) : ℝ)⁻¹ *
              log (μ.real {ω | sampleMean X (n + 1) ω ∈ G}))
          atTop

/-- Terminal LDP package expected from a completed Cramer formalization. -/
def CramerConclusion {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (X : ℕ → Ω → ℝ) : Prop :=
  cramerUpperBound μ X ∧ cramerLowerBound μ X

/--
Normalized data for Cramer's theorem over one probability space.

The checked fields use current mathlib objects: probability measure,
measurability, `iIndepFun`, identical distribution, and exponential
integrability.  The bridge fields mark the missing LDP-specific proof packages.
-/
structure CramerData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  X : ℕ → Ω → ℝ
  isProbability : IsProbabilityMeasure μ
  measurable : ∀ n : ℕ, Measurable (X n)
  independent : ProbabilityTheory.iIndepFun X μ
  identDistrib : ∀ i j : ℕ, ProbabilityTheory.IdentDistrib (X i) (X j) μ μ
  expIntegrable : ∀ n : ℕ, ∀ t : ℝ, Integrable (fun ω => exp (t * X n ω)) μ
  nonemptyExponentialDomain : 0 ∈ interior (ProbabilityTheory.integrableExpSet (X 0) μ)
  exponentialTightnessBridge : Prop
  convexDualityBridge : Prop
  lowerBoundBridge : Prop
  terminalCramerConclusion : CramerConclusion μ X

/-- Hypotheses that remain as named bridge packages in this Stage1 boundary. -/
def CramerHypotheses {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) : Prop :=
  D.exponentialTightnessBridge ∧ D.convexDualityBridge ∧ D.lowerBoundBridge

/--
Stage1 normalized statement shape for Cramer's theorem.

This is the future target theorem, not a repo-local proof.  The local file only
checks that the statement and available mathlib-side wrappers are well-typed.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : CramerData Ω,
      CramerHypotheses D → CramerConclusion D.μ D.X

/-- The normalized statement unfolds to the explicit data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : CramerData Ω,
          CramerHypotheses D → CramerConclusion D.μ D.X :=
  Iff.rfl

/--
Projection wrapper for the future terminal LDP conclusion field.

This is not a proof of Cramer's theorem; it only verifies that the intended
conclusion package has a Lean type accepted by the pinned mathlib APIs.
-/
theorem terminalConclusion_project {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) :
    CramerConclusion D.μ D.X :=
  D.terminalCramerConclusion

/-- Project the closed-set upper LDP half from the future terminal package. -/
theorem terminal_upperBound {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) :
    cramerUpperBound D.μ D.X :=
  D.terminalCramerConclusion.1

/-- Project the open-set lower LDP half from the future terminal package. -/
theorem terminal_lowerBound {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) :
    cramerLowerBound D.μ D.X :=
  D.terminalCramerConclusion.2

/-- Project the independent-sequence predicate from the normalized data. -/
theorem independent_from_data {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) :
    ProbabilityTheory.iIndepFun D.X D.μ :=
  D.independent

/-- Independence in mathlib implies that the ambient measure is a probability measure. -/
theorem probability_from_independence {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) :
    IsProbabilityMeasure D.μ :=
  D.independent.isProbabilityMeasure

/-- Project measurability of each random variable. -/
theorem measurable_X {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) (n : ℕ) :
    Measurable (D.X n) :=
  D.measurable n

/-- Project identical distribution of two coordinates. -/
theorem identDistrib_X {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) (i j : ℕ) :
    ProbabilityTheory.IdentDistrib (D.X i) (D.X j) D.μ D.μ :=
  D.identDistrib i j

/-- Project exponential integrability for each coordinate and parameter. -/
theorem expIntegrable_X {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) (n : ℕ) (t : ℝ) :
    Integrable (fun ω => exp (t * D.X n ω)) D.μ :=
  D.expIntegrable n t

/-- mathlib factorizes the MGF of a finite sum of independent random variables. -/
theorem mgf_sum_range {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) (n : ℕ) (t : ℝ) :
    ProbabilityTheory.mgf (∑ i ∈ Finset.range n, D.X i) D.μ t =
      ∏ i ∈ Finset.range n, ProbabilityTheory.mgf (D.X i) D.μ t :=
  D.independent.mgf_sum D.measurable (Finset.range n)

/-- mathlib factorizes the CGF of a finite sum when the exponential moments exist. -/
theorem cgf_sum_range {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) (n : ℕ) (t : ℝ) :
    ProbabilityTheory.cgf (∑ i ∈ Finset.range n, D.X i) D.μ t =
      ∑ i ∈ Finset.range n, ProbabilityTheory.cgf (D.X i) D.μ t :=
  D.independent.cgf_sum D.measurable (fun i _hi => D.expIntegrable i t)

/-- The IID finite-sum MGF specializes to a power of the reference MGF. -/
theorem mgf_sum_range_iid {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) {n : ℕ} (hn : 0 ∈ Finset.range (n + 1)) (t : ℝ) :
    ProbabilityTheory.mgf (∑ i ∈ Finset.range (n + 1), D.X i) D.μ t =
      ProbabilityTheory.mgf (D.X 0) D.μ t ^ #(Finset.range (n + 1)) :=
  ProbabilityTheory.mgf_sum_of_identDistrib D.measurable D.independent
    (fun i _hi j _hj => D.identDistrib i j) hn t

/-- Chernoff's upper-tail bound applies to finite sums in the pinned mathlib API. -/
theorem chernoff_upper_sum {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) (n : ℕ) (ε t : ℝ) (ht : 0 ≤ t) :
    D.μ.real {ω | ε ≤ (∑ i ∈ Finset.range n, D.X i) ω} ≤
      exp (-t * ε +
        ProbabilityTheory.cgf (∑ i ∈ Finset.range n, D.X i) D.μ t) := by
  haveI : IsProbabilityMeasure D.μ := D.isProbability
  exact ProbabilityTheory.measure_ge_le_exp_cgf ε ht
    (D.independent.integrable_exp_mul_sum D.measurable
      (fun i _hi => D.expIntegrable i t))

/-- Chernoff's lower-tail bound applies to finite sums in the pinned mathlib API. -/
theorem chernoff_lower_sum {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) (n : ℕ) (ε t : ℝ) (ht : t ≤ 0) :
    D.μ.real {ω | (∑ i ∈ Finset.range n, D.X i) ω ≤ ε} ≤
      exp (-t * ε +
        ProbabilityTheory.cgf (∑ i ∈ Finset.range n, D.X i) D.μ t) := by
  haveI : IsProbabilityMeasure D.μ := D.isProbability
  exact ProbabilityTheory.measure_le_le_exp_cgf ε ht
    (D.independent.integrable_exp_mul_sum D.measurable
      (fun i _hi => D.expIntegrable i t))

/-- The pinned MGF API gives analyticity on the interior exponential-integrability domain. -/
theorem analyticOn_cgf_reference {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) :
    AnalyticOn ℝ (ProbabilityTheory.cgf (D.X 0) D.μ)
      (interior (ProbabilityTheory.integrableExpSet (D.X 0) D.μ)) :=
  ProbabilityTheory.analyticOn_cgf

/-- The pinned tilted-measure API identifies the tilted mean with the derivative of the CGF. -/
theorem integral_tilted_reference_eq_deriv_cgf {Ω : Type u} [MeasurableSpace Ω]
    (D : CramerData Ω) {t : ℝ}
    (ht : t ∈ interior (ProbabilityTheory.integrableExpSet (D.X 0) D.μ)) :
    (D.μ.tilted (t * D.X 0 ·))[D.X 0] =
      deriv (ProbabilityTheory.cgf (D.X 0) D.μ) t :=
  ProbabilityTheory.integral_tilted_mul_self ht

/-- The empirical mean at zero is definitionally zero. -/
theorem sampleMean_zero {Ω : Type u} (X : ℕ → Ω → ℝ) :
    sampleMean X 0 = fun _ => 0 := by
  ext ω
  simp [sampleMean]

/-- The empirical mean unfolds to the normalized finite-sum expression. -/
theorem sampleMean_apply {Ω : Type u}
    (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) :
    sampleMean X n ω = (n : ℝ)⁻¹ * ∑ i ∈ Finset.range n, X i ω :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Moments.Basic",
  "Mathlib.Probability.Moments.IntegrableExpMul",
  "Mathlib.Probability.Moments.MGFAnalytic",
  "Mathlib.Probability.Moments.Tilted",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Integration",
  "Mathlib.Probability.Independence.InfinitePi",
  "Mathlib.MeasureTheory.Integral.Lebesgue.Markov",
  "Mathlib.MeasureTheory.Measure.Tilted",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.Analysis.Convex.Basic"
]

/-- Pinned mathlib revision used for the S1-M-251 anchor audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.mgf",
  "ProbabilityTheory.cgf",
  "ProbabilityTheory.integrableExpSet",
  "ProbabilityTheory.convex_integrableExpSet",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.iIndepFun.mgf_sum",
  "ProbabilityTheory.iIndepFun.cgf_sum",
  "ProbabilityTheory.mgf_sum_of_identDistrib",
  "ProbabilityTheory.measure_ge_le_exp_cgf",
  "ProbabilityTheory.measure_le_le_exp_cgf",
  "ProbabilityTheory.analyticOn_mgf",
  "ProbabilityTheory.analyticOn_cgf",
  "ProbabilityTheory.integral_tilted_mul_self",
  "ProbabilityTheory.variance_tilted_mul",
  "MeasureTheory.Measure.tilted",
  "MeasureTheory.Measure.real",
  "MeasureTheory.TendstoInDistribution",
  "MeasureTheory.ProbabilityMeasure",
  "Filter.limsup",
  "Filter.liminf"
]

/-- Child S1-M-251-C002 scope: the public-facing anchor package to backfill. -/
def childC002AnchorPackage : List String := [
  "mathlib pin 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "ProbabilityTheory.mgf",
  "ProbabilityTheory.cgf",
  "ProbabilityTheory.integrableExpSet",
  "ProbabilityTheory.iIndepFun.mgf_sum",
  "ProbabilityTheory.iIndepFun.cgf_sum",
  "Chernoff upper/lower bounds via ProbabilityTheory.measure_ge_le_exp_cgf and measure_le_le_exp_cgf",
  "tilted measures via MeasureTheory.Measure.tilted and ProbabilityTheory.integral_tilted_mul_self",
  "MeasureTheory.TendstoInDistribution",
  "Filter.limsup",
  "Filter.liminf"
]

/--
Search terms that did not locate a terminal Cramer theorem or large-deviation
principle in the pinned local mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "Cramer",
  "Cramér",
  "LargeDeviation",
  "large deviation",
  "large-deviation principle",
  "rate function",
  "RateFunction",
  "Legendre-Fenchel",
  "Fenchel",
  "Varadhan",
  "Gartner",
  "Gärtner",
  "Ellis"
]

/-- Child S1-M-251-C003 public blocker text retained in the checked artifact. -/
def childC003TerminalBlocker : List String := [
  "Pinned mathlib does not currently expose a located terminal Cramer theorem.",
  "Pinned mathlib does not currently expose a located large-deviation-principle theorem.",
  "The available anchors are probability and analysis substrate, not theorem completion.",
  "Keep S1-M-251 not_repo_local_closed / formalization_debt until a terminal local proof, mathlib wrapper, or pinned external proof validates."
]

/-- Child S1-M-251-C005 upper-bound package expansion notes. -/
def childC005UpperBoundPackageNotes : List String := [
  "The checked package now separates Chernoff half-line interfaces, compact-set upper bounds, and the closed-set bridge.",
  "The existing Chernoff wrappers are checked local mathlib wrappers, but sample-mean scaling, rate optimization, finite-cover, and tightness leaves remain formalization debt.",
  "All C005 leaf rows are budgeted at <=100 steps in childC005UpperBoundLeafLedger.",
  "No C005 row claims terminal Cramer theorem closure.",
  "The parent theorem remains not_repo_local_closed / formalization_debt until cramerTerminalUpperBound and the lower-bound package validate as local proof body, mathlib wrapper, or pinned external proof."
]

/-- Child S1-M-251-C006 lower-bound package expansion notes. -/
def childC006LowerBoundPackageNotes : List String := [
  "The checked package now separates exposed-point predicates, pointwise open-neighborhood lower bounds, tilted exposed-point lower bounds, nonexposed-point approximation, and the open-set lower bridge.",
  "The tilted-mean derivative wrapper is checked against ProbabilityTheory.integral_tilted_mul_self, but the slope-domain, change-of-measure, tilted LLN, and EReal sInf/open-set passage leaves remain formalization debt.",
  "All C006 leaf rows are budgeted at <=100 steps in childC006LowerBoundLeafLedger.",
  "No C006 row claims terminal Cramer theorem closure.",
  "The parent theorem remains not_repo_local_closed / formalization_debt until cramerTerminalLowerBound and cramerTerminalUpperBound validate as local proof body, mathlib wrapper, or pinned external proof."
]

/-- One row from child `S1-M-251-C007` external Lean 4 source audit. -/
structure CramerExternalAuditRow where
  repositoryUrl : String
  commitSha : String
  exactSearchTerms : List String
  theoremName : String
  kernelClosureStatus : String
  terminalAnchorStatus : String

/--
Child `S1-M-251-C007` exact source-search audit result.

No row records a terminal external Lean 4 Cramer/LDP theorem.  Therefore this
does not create completed-state `repo_local_integration_debt`; the parent
remains `not_repo_local_closed / formalization_debt`.
-/
def childC007ExternalAuditRows : List CramerExternalAuditRow := [
  {
    repositoryUrl := "https://github.com/uw-math-ai/central_limit_theorem",
    commitSha := "0ed57e943d642eaa95fe547780024b9e3a0dfbdf",
    exactSearchTerms := [
      "Cramer", "Cramér", "LargeDeviation", "RateFunction",
      "LegendreFenchel", "Varadhan", "GartnerEllis"
    ],
    theoremName := "none located for requested Cramer/LDP terms",
    kernelClosureStatus := "not placeholder-free: repository Lean files contain open proof placeholders",
    terminalAnchorStatus :=
      "rejected as terminal anchor: central limit theorem project, no requested exact source hit"
  },
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commitSha := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    exactSearchTerms := [
      "Cramer", "Cramér", "LargeDeviation", "RateFunction",
      "LegendreFenchel", "Varadhan", "GartnerEllis"
    ],
    theoremName := "none located for terminal Cramer theorem or large-deviation principle",
    kernelClosureStatus := "pinned dependency validated for local anchors used here",
    terminalAnchorStatus :=
      "not a terminal Cramer/LDP anchor; only probability and analysis substrate located"
  }
]

/-- Number of C007 external-audit rows retained in the checked artifact. -/
theorem childC007ExternalAuditRows_length :
    childC007ExternalAuditRows.length = 2 :=
  rfl

/-- Checked guard: no C007 row claims terminal external proof closure. -/
theorem childC007ExternalAuditRows_noTerminalClosure :
    (childC007ExternalAuditRows.map (fun row => row.terminalAnchorStatus)).all
      (fun status => status != "terminal external proof pinned and checked") = true :=
  rfl

/-- One row for child `S1-M-251-C008` external-proof integration gate. -/
structure CramerExternalIntegrationGateRow where
  gateId : String
  sourceFinding : String
  requiredActionIfFound : String
  currentRepoLocalAction : String
  completionStatus : String
  externalProofPinnedAndChecked : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool

/--
Child `S1-M-251-C008` integration gate for external terminal proofs.

The C007 source audit found no terminal external Lean 4 Cramer/LDP proof with a
repository, commit, module, and theorem name.  Consequently C008 has no
specific upstream proof body to pin, import, and check in Lake.  This row keeps
the parent open and records the required action if a future exact external
proof is found.
-/
def childC008ExternalIntegrationGateRows :
    List CramerExternalIntegrationGateRow := [
  {
    gateId := "S1-M-251-C008-external-terminal-proof-gate",
    sourceFinding :=
      "no terminal external Lean 4 Cramer theorem or large-deviation-principle theorem was located by the retained exact source audit",
    requiredActionIfFound :=
      "pin/import/check the external proof in this Lake closure or record a concrete toolchain/license/dependency/placeholder blocker",
    currentRepoLocalAction :=
      "no Lake dependency or import added because no repository, commit, module, and theorem name for a terminal proof is available",
    completionStatus :=
      "open_not_completed: parent remains not_repo_local_closed / formalization_debt; external_upstream_anchor_only is not used as completion evidence",
    externalProofPinnedAndChecked := false,
    completedStateRetainsRepoLocalIntegrationDebt := false
  }
]

/-- Number of C008 external-integration gate rows retained in the checked artifact. -/
theorem childC008ExternalIntegrationGateRows_length :
    childC008ExternalIntegrationGateRows.length = 1 :=
  rfl

/-- Checked guard: C008 makes no completed external-upstream-pinned claim. -/
theorem childC008ExternalIntegrationGateRows_noPinnedExternalClaim :
    (childC008ExternalIntegrationGateRows.map
      (fun row => row.externalProofPinnedAndChecked)).all
        (fun pinned => pinned = false) = true :=
  rfl

/-- Checked guard: C008 retains no completed-state repo-local integration debt. -/
theorem childC008ExternalIntegrationGateRows_noCompletedRepoLocalIntegrationDebt :
    (childC008ExternalIntegrationGateRows.map
      (fun row => row.completedStateRetainsRepoLocalIntegrationDebt)).all
        (fun debt => debt = false) = true :=
  rfl

/-- One row for child `S1-M-251-C009` public synchronization gate. -/
structure CramerPublicSynchronizationGateRow where
  gateId : String
  childTaskScope : String
  checkedArtifactPath : String
  validationCommand : String
  publicMergeTargets : List String
  currentPublicAction : String
  theoremCompletionStatus : String
  repoLocalIntegrationDebtGate : String
  closesTerminalTheorem : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool

/--
Child `S1-M-251-C009` public synchronization gate.

This records that public blueprint/todo/README synchronization is a serialized
integrator task.  This checked row is a non-completion gate: the local artifact
may be cited by a later integrator, but the terminal Cramer theorem remains
open until the upper-bound, lower-bound, and repo-local proof/dependency gates
are closed and validated.
-/
def childC009PublicSynchronizationGateRows :
    List CramerPublicSynchronizationGateRow := [
  {
    gateId := "S1-M-251-C009-public-synchronization-gate",
    childTaskScope :=
      "After any theorem closure, synchronize public blueprint/todos/README status in a single integrator patch; worker ledgers are not public completion surfaces.",
    checkedArtifactPath :=
      "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_251.lean",
    validationCommand :=
      "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_251.lean",
    publicMergeTargets := [
      "Docs/Stage1_Blueprint.md:3380",
      "Docs/todos_20260430.md",
      "README.md"
    ],
    currentPublicAction :=
      "no public docs edited by this child; serial integrator must merge the public backfill later",
    theoremCompletionStatus :=
      "open_not_completed: terminal Cramer large-deviation principle not repo-locally proved or imported",
    repoLocalIntegrationDebtGate :=
      "pass_noncompletion: no external terminal proof was found or claimed completed; future external proof must be pinned/imported/checked or concretely blocked before completion",
    closesTerminalTheorem := false,
    completedStateRetainsRepoLocalIntegrationDebt := false
  }
]

/-- Number of C009 public-synchronization gate rows retained in the checked artifact. -/
theorem childC009PublicSynchronizationGateRows_length :
    childC009PublicSynchronizationGateRows.length = 1 :=
  rfl

/-- Checked guard: C009 does not close the terminal Cramer theorem. -/
theorem childC009PublicSynchronizationGateRows_noTerminalClosure :
    (childC009PublicSynchronizationGateRows.map
      (fun row => row.closesTerminalTheorem)).all
        (fun closed => closed = false) = true :=
  rfl

/-- Checked guard: C009 retains no completed-state repo-local integration debt. -/
theorem childC009PublicSynchronizationGateRows_noCompletedRepoLocalIntegrationDebt :
    (childC009PublicSynchronizationGateRows.map
      (fun row => row.completedStateRetainsRepoLocalIntegrationDebt)).all
        (fun debt => debt = false) = true :=
  rfl

/-- Child S1-M-251-C004 terminal log/rate-scale decision. -/
def childC004ScaleDecisionNotes : List String := [
  "Do not use the current plain Real-valued rate/log package for terminal boundary cases.",
  "Do not use a raw EReal-only package that hides the probability input scale.",
  "Use a custom extended-rate API: probabilities in ENNReal, extended log and rates in EReal.",
  "Keep the Real Legendre-Fenchel expression only as finite-rate compatibility data.",
  "Boundary cases with zero probabilities or infinite rates must be proved against the custom extended API before any terminal Cramer completion claim."
]

/-! ## Audit probes retained in the checked file. -/

#check TerminalLDPScaleChoice
#check terminalLDPScaleDecision
#check CramerTerminalScale
#check cramerTerminalScaledLogProbability
#check CramerTerminalExtendedConclusion
#check cramerTerminalExposedPoint
#check cramerTerminalPointLowerBound
#check cramerTerminalTiltedExposedLowerBound
#check cramerTerminalNonexposedApproximation
#check cramerTerminalOpenSetLowerBridge
#check terminal_lower_from_openSetBridge
#check cramerTerminalChernoffHalfLinePackage
#check cramerTerminalCompactUpperBound
#check cramerTerminalClosedSetUpperBridge
#check terminal_upper_from_closedSetBridge
#check childC005UpperBoundLeafLedger
#check childC005UpperBoundLeafLedger_budgets
#check childC006LowerBoundLeafLedger
#check childC006LowerBoundLeafLedger_budgets
#check childC007ExternalAuditRows
#check childC007ExternalAuditRows_noTerminalClosure
#check childC008ExternalIntegrationGateRows
#check childC008ExternalIntegrationGateRows_noPinnedExternalClaim
#check childC008ExternalIntegrationGateRows_noCompletedRepoLocalIntegrationDebt
#check childC009PublicSynchronizationGateRows
#check childC009PublicSynchronizationGateRows_noTerminalClosure
#check childC009PublicSynchronizationGateRows_noCompletedRepoLocalIntegrationDebt
#check ProbabilityTheory.mgf
#check ProbabilityTheory.cgf
#check ProbabilityTheory.integrableExpSet
#check ProbabilityTheory.convex_integrableExpSet
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.mgf_sum
#check ProbabilityTheory.iIndepFun.cgf_sum
#check ProbabilityTheory.mgf_sum_of_identDistrib
#check ProbabilityTheory.measure_ge_le_exp_cgf
#check ProbabilityTheory.measure_le_le_exp_cgf
#check ProbabilityTheory.analyticOn_cgf
#check ProbabilityTheory.integral_tilted_mul_self
#check ProbabilityTheory.variance_tilted_mul
#check MeasureTheory.Measure.tilted
#check MeasureTheory.TendstoInDistribution
#check Filter.limsup
#check Filter.liminf

end S1_M_251
end Stage1
end AwesomeTheorems
