import Mathlib.MeasureTheory.Function.EssSup
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Probability.HasLaw
import Mathlib.Topology.MetricSpace.Holder

/-!
# S1-M-244 / THM-M-1051: Krylov-Safonov estimate

This Stage1 artifact records a conservative Lean 4 boundary for the
Krylov-Safonov Harnack estimate for uniformly elliptic non-divergence-form
equations.

The pinned mathlib snapshot supplies measure-theoretic essential suprema and
infima, probability laws, metric balls, and Holder-continuity predicates.  This
audit did not locate a terminal mathlib theorem for the Krylov-Safonov Harnack
inequality, nor a canonical non-divergence elliptic PDE operator API in local
mathlib.  The declaration below therefore keeps the PDE operator, ellipticity,
solution predicate, stochastic representation, ABP/growth packages, and
Harnack proof as explicit proposition fields.

No declaration in this file claims the terminal Krylov-Safonov theorem.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal Topology

namespace AwesomeTheorems.Stage1.S1_M_244

universe uE uOp uCoeff uRHS uΩ

/--
Abstract data needed to state a non-divergence-form Krylov-Safonov estimate.

The ambient domain and conclusion use concrete mathlib objects: metric balls,
essential suprema/infima, and `HolderOnWith`.  The actual PDE operator,
coefficient matrix field, viscosity/strong solution predicate, stochastic
representation, and ABP/growth lemmas remain abstract because the current local
mathlib closure has not selected a canonical non-divergence elliptic PDE API.
-/
structure KrylovSafonovData (E : Type uE) [PseudoMetricSpace E] where
  Operator : Type uOp
  Coefficients : Type uCoeff
  RHS : Type uRHS
  solutionPredicate : Operator → Coefficients → (E → ℝ) → RHS → Set E → Prop
  nonDivergenceForm : Operator → Prop
  uniformlyElliptic : Operator → Coefficients → Prop
  boundedMeasurableCoefficients : Coefficients → Prop
  boundedMeasurableRHS : RHS → Prop
  stochasticRepresentation : Operator → Coefficients → Prop
  abpEstimatePackage : Operator → Coefficients → Prop
  growthLemmaPackage : Operator → Coefficients → Prop
  harnackConstant : ℝ≥0
  holderConstant : ℝ≥0
  holderExponent : ℝ≥0

/--
Conclusion package for one local ball.

For a nonnegative solution on an outer ball, the normalized conclusion records
the Harnack comparison on the inner ball and the usual local Holder regularity
side consequence.  The comparison is stated with essential suprema/infima with
respect to an explicit measure, which leaves room for either Lebesgue-volume
or probability-kernel specializations.
-/
structure LocalHarnackConclusion
    {E : Type uE} [PseudoMetricSpace E] [MeasurableSpace E]
    (D : KrylovSafonovData E) (μ : Measure E)
    (center : E) (innerRadius : ℝ) (u : E → ℝ) : Prop where
  harnack_essSup_le :
    essSup u (μ.restrict (Metric.ball center innerRadius)) ≤
      (D.harnackConstant : ℝ) * essInf u (μ.restrict (Metric.ball center innerRadius))
  holder_on_inner_ball :
    HolderOnWith D.holderConstant D.holderExponent u (Metric.ball center innerRadius)

/--
One-ball normalized Krylov-Safonov statement shape.

The hard proof obligations are deliberately explicit assumptions:
`stochasticRepresentation`, `abpEstimatePackage`, and `growthLemmaPackage` must
eventually be replaced by imported or locally proved Lean packages before this
slot can be considered complete.
-/
def LocalHarnackFormula
    {E : Type uE} [PseudoMetricSpace E] [MeasurableSpace E]
    (D : KrylovSafonovData E) (μ : Measure E)
    (center : E) (outerRadius innerRadius : ℝ)
    (L : D.Operator) (a : D.Coefficients) (u : E → ℝ) (f : D.RHS) : Prop :=
  0 < innerRadius →
    innerRadius < outerRadius →
      D.nonDivergenceForm L →
        D.uniformlyElliptic L a →
          D.boundedMeasurableCoefficients a →
            D.boundedMeasurableRHS f →
              D.solutionPredicate L a u f (Metric.ball center outerRadius) →
                D.stochasticRepresentation L a →
                  D.abpEstimatePackage L a →
                    D.growthLemmaPackage L a →
                      (∀ x ∈ Metric.ball center outerRadius, 0 ≤ u x) →
                        Nonempty (LocalHarnackConclusion D μ center innerRadius u)

/--
Stage1 normalized statement-shape candidate for the Krylov-Safonov estimate.

This is only a proposition.  It makes universes, ambient space, measure,
operator, coefficients, radii, solution, and right-hand side explicit, while
leaving the terminal Harnack proof package outside the local closure.
-/
def StatementShape
    {E : Type uE} [PseudoMetricSpace E] [MeasurableSpace E]
    (D : KrylovSafonovData E) : Prop :=
  ∀ (μ : Measure E) (center : E) (outerRadius innerRadius : ℝ)
    (L : D.Operator) (a : D.Coefficients) (u : E → ℝ) (f : D.RHS),
      LocalHarnackFormula D μ center outerRadius innerRadius L a u f

/-- The normalized statement shape unfolds to the one-ball formula. -/
theorem statementShape_iff_forall_local_ball
    {E : Type uE} [PseudoMetricSpace E] [MeasurableSpace E]
    (D : KrylovSafonovData E) :
    StatementShape D ↔
      ∀ (μ : Measure E) (center : E) (outerRadius innerRadius : ℝ)
        (L : D.Operator) (a : D.Coefficients) (u : E → ℝ) (f : D.RHS),
          LocalHarnackFormula D μ center outerRadius innerRadius L a u f :=
  Iff.rfl

/-- Project the essential-supremum side of a local conclusion package. -/
theorem LocalHarnackConclusion.harnack_wrapper
    {E : Type uE} [PseudoMetricSpace E] [MeasurableSpace E]
    {D : KrylovSafonovData E} {μ : Measure E}
    {center : E} {innerRadius : ℝ} {u : E → ℝ}
    (C : LocalHarnackConclusion D μ center innerRadius u) :
    essSup u (μ.restrict (Metric.ball center innerRadius)) ≤
      (D.harnackConstant : ℝ) * essInf u (μ.restrict (Metric.ball center innerRadius)) :=
  C.harnack_essSup_le

/-- Project the Holder-regularity side of a local conclusion package. -/
theorem LocalHarnackConclusion.holder_wrapper
    {E : Type uE} [PseudoMetricSpace E] [MeasurableSpace E]
    {D : KrylovSafonovData E} {μ : Measure E}
    {center : E} {innerRadius : ℝ} {u : E → ℝ}
    (C : LocalHarnackConclusion D μ center innerRadius u) :
    HolderOnWith D.holderConstant D.holderExponent u (Metric.ball center innerRadius) :=
  C.holder_on_inner_ball

/-- Checked mathlib wrapper: positive-exponent Holder control gives continuity on the set. -/
theorem holderOnWith_continuousOn_mathlib_wrapper
    {E : Type uE} [PseudoEMetricSpace E] {C α : ℝ≥0} {u : E → ℝ} {s : Set E}
    (hu : HolderOnWith C α u s) (hα : 0 < α) :
    ContinuousOn u s :=
  hu.continuousOn hα

/-- Checked mathlib wrapper: Holder control restricts to smaller sets. -/
theorem holderOnWith_mono_mathlib_wrapper
    {E : Type uE} [PseudoEMetricSpace E] {C α : ℝ≥0} {u : E → ℝ} {s t : Set E}
    (hu : HolderOnWith C α u s) (ht : t ⊆ s) :
    HolderOnWith C α u t :=
  hu.mono ht

/-- Checked mathlib wrapper: the essential supremum of a nonzero restricted constant is constant. -/
theorem essSup_const_restrict_mathlib_wrapper
    {E : Type uE} [MeasurableSpace E] (μ : Measure E) (s : Set E) (c : ℝ)
    (hμ : μ.restrict s ≠ 0) :
    essSup (fun _ : E => c) (μ.restrict s) = c :=
  essSup_const c hμ

/-- Checked mathlib wrapper: the essential infimum of a nonzero restricted constant is constant. -/
theorem essInf_const_restrict_mathlib_wrapper
    {E : Type uE} [MeasurableSpace E] (μ : Measure E) (s : Set E) (c : ℝ)
    (hμ : μ.restrict s ≠ 0) :
    essInf (fun _ : E => c) (μ.restrict s) = c :=
  essInf_const c hμ

/-- Checked mathlib wrapper: metric balls are open. -/
theorem metric_ball_isOpen_mathlib_wrapper
    {E : Type uE} [PseudoMetricSpace E] (center : E) (radius : ℝ) :
    IsOpen (Metric.ball center radius) :=
  Metric.isOpen_ball

/-- Checked mathlib wrapper: the identity random variable has its source law. -/
theorem hasLaw_id_mathlib_wrapper
    {Ω : Type uΩ} [MeasurableSpace Ω] (μ : Measure Ω) :
    HasLaw (id : Ω → Ω) μ μ :=
  HasLaw.id

/-- mathlib commit pin checked while locating repo-local anchors for this slot. -/
def mathlibPin : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib declaration anchors checked for this slot under `mathlibPin`. -/
def checkedMathlibAnchors : List String := [
  "essSup",
  "essInf",
  "HolderOnWith",
  "Metric.ball",
  "HasLaw"
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.EssSup",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Topology.MetricSpace.Holder",
  "Mathlib.Topology.MetricSpace.Basic"
]

/--
Search terms that did not locate a terminal imported Krylov-Safonov theorem in
the pinned local mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "Krylov",
  "Safonov",
  "Krylov-Safonov",
  "Harnack",
  "nondivergence",
  "non-divergence",
  "uniformly elliptic",
  "elliptic PDE",
  "viscosity solution",
  "ABP"
]

/-! ## S1-M-244-C003 terminal mathlib blocker -/

/--
One reproducible local source-search row for the public mathlib blocker.

These rows are audit metadata only.  They intentionally do not assert a
Krylov-Safonov theorem; they record why the public Stage1 surface must keep the
terminal theorem open under the current pinned mathlib dependency.
-/
structure TerminalMathlibSearchBlockerRow where
  scope : String
  command : String
  result : String
  conclusion : String

/--
Integration-ready C003 blocker rows.

Both searches were run against this repository's pinned `.lake/packages/mathlib`
checkout at `mathlibPin`.  Exit code `1` with no output is ripgrep's normal
no-match result, so the blocker is source-search evidence that no terminal
Krylov-Safonov/non-divergence Harnack declaration is available from pinned
mathlib.
-/
def c003TerminalMathlibBlockerRows : List TerminalMathlibSearchBlockerRow := [
  {
    scope := "pinned mathlib exact theorem-name and Harnack search",
    command := "rg -n \"KrylovSafonov|Krylov_Safonov|Krylov-Safonov|Safonov|Harnack|weak_harnack|harnack|nonDivergence|non_divergence|non-divergence\" Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'",
    result := "exit code 1; no output",
    conclusion := "no exact terminal Krylov-Safonov, Safonov, Harnack, weak_harnack, harnack, or non-divergence declaration was located in pinned mathlib"
  },
  {
    scope := "pinned mathlib PDE/API support-term search",
    command := "rg -n \"\\bviscosity\\b|\\bABP\\b|uniformly elliptic|elliptic PDE|non-divergence\" Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'",
    result := "exit code 1; no output",
    conclusion := "no viscosity, ABP, uniformly elliptic, elliptic PDE, or non-divergence API anchor was located in pinned mathlib"
  }
]

/-- The C003 mathlib blocker is ready for a serial public backfill patch. -/
def c003PublicMathlibBlockerReadyForBackfill : Bool :=
  true

/-- C003 does not close the terminal Krylov-Safonov theorem. -/
def c003ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C003 state retains repo-local integration debt: this child records
an open blocker, not an anchor-only completed theorem claim.
-/
def c003NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- The C003 blocker ledger has the two local mathlib searches needed for public backfill. -/
theorem c003TerminalMathlibBlockerRows_length :
    c003TerminalMathlibBlockerRows.length = 2 := by
  native_decide

theorem c003PublicMathlibBlockerReadyForBackfill_eq_true :
    c003PublicMathlibBlockerReadyForBackfill = true :=
  rfl

theorem c003ClosesKrylovSafonovTheorem_eq_false :
    c003ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c003NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c003NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/--
External Lean 4 primary-source anchor audit.

The DeGiorgi project is a relevant Lean 4 source for divergence-form
De Giorgi-Nash-Moser Harnack and Holder estimates, but it is not an exact
non-divergence Krylov-Safonov proof and it is not in this repository's Lake
dependency closure.  It therefore does not close this Stage1 item.
-/
def externalLean4PrimaryAnchors : List String := [
  "https://github.com/scottnarmstrong/DeGiorgi/tree/4c1b3077d3782b24065184df4ba59501b2e56fc7",
  "manifest target theorems: weak_harnack, weak_harnack_on_ball, harnack, harnack_of_homogeneousWeakSolution, holder_Moser, holder_Moser_of_homogeneousWeakSolution",
  "lakefile inputRev: mathlib v4.29.0-rc6; lake-manifest mathlib revision 5c8398df528176d9c87ccd9226ba8f7c8852d59c",
  "classification for S1-M-244: adjacent divergence-form Harnack/Holder formalization, not an exact non-divergence Krylov-Safonov closure"
]

/-! ## S1-M-244-C004 adjacent DeGiorgi external-anchor note -/

/--
Integration-ready row for an adjacent external Lean 4 source.

The row records why the external project is relevant audit evidence but is not
an exact terminal proof for this Stage1 slot.  In particular, it is not in this
repository's Lake dependency closure and is classified as divergence-form
Harnack/Holder evidence rather than non-divergence Krylov-Safonov closure.
-/
structure AdjacentExternalAnchorRow where
  repository : String
  commit : String
  evidenceTheorems : List String
  classification : String
  repoLocalClosure : String
  conclusion : String

/--
C004 public-note row for `scottnarmstrong/DeGiorgi`.

This is audit metadata only.  It deliberately does not assert or import any
Krylov-Safonov theorem.
-/
def c004DegiorgiAdjacentAnchorRows : List AdjacentExternalAnchorRow := [
  {
    repository := "https://github.com/scottnarmstrong/DeGiorgi",
    commit := "4c1b3077d3782b24065184df4ba59501b2e56fc7",
    evidenceTheorems := [
      "weak_harnack",
      "weak_harnack_on_ball",
      "harnack",
      "harnack_of_homogeneousWeakSolution",
      "holder_Moser",
      "holder_Moser_of_homogeneousWeakSolution"
    ],
    classification := "adjacent divergence-form De Giorgi-Nash-Moser Harnack/Holder Lean 4 evidence",
    repoLocalClosure := "not imported, pinned, or checked by this repository's Lake dependency closure",
    conclusion := "not an exact non-divergence Krylov-Safonov closure for S1-M-244"
  }
]

/-- The C004 DeGiorgi adjacent-anchor note is ready for serial public backfill. -/
def c004PublicDegiorgiNoteReadyForBackfill : Bool :=
  true

/-- C004 does not close the terminal non-divergence Krylov-Safonov theorem. -/
def c004ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C004 state retains repo-local integration debt: this child records
adjacent evidence and an open boundary, not an anchor-only completed theorem.
-/
def c004NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- The C004 DeGiorgi note has one integration-ready external-anchor row. -/
theorem c004DegiorgiAdjacentAnchorRows_length :
    c004DegiorgiAdjacentAnchorRows.length = 1 := by
  native_decide

theorem c004PublicDegiorgiNoteReadyForBackfill_eq_true :
    c004PublicDegiorgiNoteReadyForBackfill = true :=
  rfl

theorem c004ClosesKrylovSafonovTheorem_eq_false :
    c004ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c004NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c004NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-244-C005 route decision -/

/--
Two viable formalization routes for the Krylov-Safonov estimate.

The C005 decision selects the PDE/viscosity route as the next proof-expansion
spine because it directly fixes the target non-divergence operator, coefficient,
solution, ABP, growth-lemma, weak-Harnack, Harnack-chain, and Holder packages.
The probabilistic diffusion/generator route remains useful, but should be
expanded only after the PDE statement API is no longer abstract.
-/
inductive FormalizationRoute where
  | pdeViscosity
  | probabilisticDiffusionGenerator
  deriving DecidableEq

/--
Integration-ready row for the C005 route decision.

This is planning metadata, not a theorem proof.  It records a checked local
decision so later public backfill can replace the open route-choice task without
claiming terminal Krylov-Safonov closure.
-/
structure FormalizationRouteDecisionRow where
  childId : String
  selectedRoute : FormalizationRoute
  deferredRoute : FormalizationRoute
  rationale : List String
  immediateLeaves : List String
  deferredBridgeLeaves : List String
  completionBoundary : String

/--
C005 chooses the PDE/viscosity API as the next expansion route.

Reason: the target theorem is a non-divergence-form elliptic Harnack estimate,
and this repository currently lacks a concrete non-divergence operator,
coefficient, ellipticity, and viscosity/strong-solution API.  Expanding the
probabilistic route first would still have to return to those PDE interfaces in
order to state the generator/PDE bridge and terminal Harnack theorem.
-/
def c005RouteDecisionRows : List FormalizationRouteDecisionRow := [
  {
    childId := "S1-M-244-C005",
    selectedRoute := FormalizationRoute.pdeViscosity,
    deferredRoute := FormalizationRoute.probabilisticDiffusionGenerator,
    rationale := [
      "the Stage1 target is a uniformly elliptic non-divergence-form Harnack estimate",
      "the current artifact already exposes abstract PDE fields for operator, coefficients, ellipticity, and solution predicate",
      "ABP, growth lemma, weak Harnack, Harnack-chain, and Holder oscillation packages are PDE-native proof leaves",
      "a diffusion/generator proof still needs the PDE operator and solution API to state the generator-to-equation bridge"
    ],
    immediateLeaves := [
      "non-divergence operator and coefficient matrix API",
      "uniform ellipticity constants and bounded measurable coefficient hypotheses",
      "viscosity or strong solution predicate on metric balls",
      "ABP estimate, growth lemma, weak Harnack, Harnack-chain, and Holder oscillation packages"
    ],
    deferredBridgeLeaves := [
      "diffusion or Markov-process construction",
      "generator identifies the non-divergence operator",
      "exit-time and hitting-probability estimates",
      "stochastic representation connected to the PDE-local Harnack conclusion"
    ],
    completionBoundary := "route decision only; does not prove or close the Krylov-Safonov theorem"
  }
]

/-- C005 selected route. -/
def c005SelectedFormalizationRoute : FormalizationRoute :=
  FormalizationRoute.pdeViscosity

/-- C005 deferred bridge route. -/
def c005DeferredFormalizationRoute : FormalizationRoute :=
  FormalizationRoute.probabilisticDiffusionGenerator

/-- The C005 route decision is ready for a serial public backfill patch. -/
def c005PublicRouteDecisionReadyForBackfill : Bool :=
  true

/-- C005 does not close the terminal non-divergence Krylov-Safonov theorem. -/
def c005ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C005 state retains repo-local integration debt: this child records
a route decision and keeps theorem closure open as formalization debt.
-/
def c005NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- The C005 route-decision row is integration-ready and unique. -/
theorem c005RouteDecisionRows_length :
    c005RouteDecisionRows.length = 1 := by
  native_decide

theorem c005SelectedFormalizationRoute_eq_pdeViscosity :
    c005SelectedFormalizationRoute = FormalizationRoute.pdeViscosity :=
  rfl

theorem c005DeferredFormalizationRoute_eq_probabilisticDiffusionGenerator :
    c005DeferredFormalizationRoute = FormalizationRoute.probabilisticDiffusionGenerator :=
  rfl

theorem c005PublicRouteDecisionReadyForBackfill_eq_true :
    c005PublicRouteDecisionReadyForBackfill = true :=
  rfl

theorem c005ClosesKrylovSafonovTheorem_eq_false :
    c005ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c005NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c005NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-244-C006 non-divergence API leaf split -/

/--
Top-level API packages needed before the Krylov-Safonov proof packages can be
expanded into concrete Lean proof leaves.

These constructors describe the statement/API layer only.  They do not assert
that the terminal non-divergence Harnack theorem has been proved.
-/
inductive NonDivergenceApiPackage where
  | operatorCore
  | coefficientCore
  | ellipticityAndBounds
  | solutionPredicate
  | localBallGeometry
  | statementCompatibility
  deriving DecidableEq

/--
One integration-ready C006 leaf row.

`proofBudgetBound` is the intended M0387 local proof-step budget for the leaf
after the API is implemented.  C006 records the split and gates; later workers
must replace the abstract fields in `KrylovSafonovData` with concrete
definitions and proofs.
-/
structure NonDivergenceApiLeafRow where
  leafId : String
  package : NonDivergenceApiPackage
  statementTarget : String
  repoLocalAnchor : String
  dependsOn : List String
  proofBudgetBound : Nat
  completionGate : String
  deriving DecidableEq

/--
C006 expansion of the non-divergence operator/coefficient/solution API package
into independent M0387-sized leaves.

The rows deliberately stay at the API boundary: they are small enough for later
implementation workers to own independently, but they do not claim a concrete
PDE theory or a terminal Krylov-Safonov proof is already present.
-/
def c006NonDivergenceApiLeaves : List NonDivergenceApiLeafRow := [
  {
    leafId := "C006-L01-operator-carrier",
    package := NonDivergenceApiPackage.operatorCore,
    statementTarget := "Introduce the concrete carrier for non-divergence operators L on the ambient space E.",
    repoLocalAnchor := "KrylovSafonovData.Operator",
    dependsOn := [],
    proofBudgetBound := 60,
    completionGate := "carrier compiles and all later operator predicates quantify over it"
  },
  {
    leafId := "C006-L02-operator-nondivergence-form",
    package := NonDivergenceApiPackage.operatorCore,
    statementTarget := "Define the predicate that L has non-divergence-form second-order shape.",
    repoLocalAnchor := "KrylovSafonovData.nonDivergenceForm",
    dependsOn := ["C006-L01-operator-carrier"],
    proofBudgetBound := 80,
    completionGate := "predicate replaces the abstract field without changing LocalHarnackFormula"
  },
  {
    leafId := "C006-L03-coefficient-carrier",
    package := NonDivergenceApiPackage.coefficientCore,
    statementTarget := "Introduce the concrete coefficient object, including matrix or bilinear-form indexing data.",
    repoLocalAnchor := "KrylovSafonovData.Coefficients",
    dependsOn := ["C006-L01-operator-carrier"],
    proofBudgetBound := 70,
    completionGate := "coefficient carrier compiles and is accepted by the ellipticity predicate"
  },
  {
    leafId := "C006-L04-coefficient-measurability",
    package := NonDivergenceApiPackage.coefficientCore,
    statementTarget := "State bounded measurable coefficient hypotheses on the selected coefficient carrier.",
    repoLocalAnchor := "KrylovSafonovData.boundedMeasurableCoefficients",
    dependsOn := ["C006-L03-coefficient-carrier"],
    proofBudgetBound := 90,
    completionGate := "hypothesis is expressed with mathlib measurable/bounded vocabulary or a documented local blocker"
  },
  {
    leafId := "C006-L05-ellipticity-constants",
    package := NonDivergenceApiPackage.ellipticityAndBounds,
    statementTarget := "Add lower and upper ellipticity constants and positivity/order side conditions.",
    repoLocalAnchor := "KrylovSafonovData.uniformlyElliptic",
    dependsOn := ["C006-L03-coefficient-carrier"],
    proofBudgetBound := 85,
    completionGate := "uniform ellipticity can expose constants usable by ABP and growth leaves"
  },
  {
    leafId := "C006-L06-rhs-carrier-and-bounds",
    package := NonDivergenceApiPackage.ellipticityAndBounds,
    statementTarget := "Introduce the right-hand-side carrier and bounded/measurable RHS predicate.",
    repoLocalAnchor := "KrylovSafonovData.RHS; KrylovSafonovData.boundedMeasurableRHS",
    dependsOn := [],
    proofBudgetBound := 75,
    completionGate := "RHS predicate compiles and remains independent of terminal Harnack proof packages"
  },
  {
    leafId := "C006-L07-domain-localization",
    package := NonDivergenceApiPackage.localBallGeometry,
    statementTarget := "Package outer and inner metric balls, radius inequalities, and restriction measures.",
    repoLocalAnchor := "Metric.ball; Measure.restrict; LocalHarnackFormula",
    dependsOn := ["metric_ball_isOpen_mathlib_wrapper"],
    proofBudgetBound := 65,
    completionGate := "localized statement reuses Metric.ball and measure restriction without new axioms"
  },
  {
    leafId := "C006-L08-solution-predicate",
    package := NonDivergenceApiPackage.solutionPredicate,
    statementTarget := "Define the viscosity or strong solution predicate on a localized ball.",
    repoLocalAnchor := "KrylovSafonovData.solutionPredicate",
    dependsOn := [
      "C006-L01-operator-carrier",
      "C006-L03-coefficient-carrier",
      "C006-L06-rhs-carrier-and-bounds",
      "C006-L07-domain-localization"
    ],
    proofBudgetBound := 100,
    completionGate := "solution predicate can replace the abstract field in LocalHarnackFormula"
  },
  {
    leafId := "C006-L09-nonnegative-solution-hypothesis",
    package := NonDivergenceApiPackage.solutionPredicate,
    statementTarget := "Isolate the nonnegative-on-outer-ball hypothesis used by local Harnack.",
    repoLocalAnchor := "LocalHarnackFormula nonnegativity premise",
    dependsOn := ["C006-L07-domain-localization", "C006-L08-solution-predicate"],
    proofBudgetBound := 55,
    completionGate := "nonnegativity premise has a reusable named wrapper for later Harnack leaves"
  },
  {
    leafId := "C006-L10-operator-solution-compatibility",
    package := NonDivergenceApiPackage.statementCompatibility,
    statementTarget := "Prove the concrete operator, coefficients, RHS, and solution predicate assemble into LocalHarnackFormula premises.",
    repoLocalAnchor := "LocalHarnackFormula",
    dependsOn := [
      "C006-L02-operator-nondivergence-form",
      "C006-L04-coefficient-measurability",
      "C006-L05-ellipticity-constants",
      "C006-L08-solution-predicate"
    ],
    proofBudgetBound := 100,
    completionGate := "premise package is usable without changing StatementShape"
  },
  {
    leafId := "C006-L11-conclusion-api-compatibility",
    package := NonDivergenceApiPackage.statementCompatibility,
    statementTarget := "Check that the concrete API still targets essSup/essInf Harnack and HolderOnWith conclusions.",
    repoLocalAnchor := "LocalHarnackConclusion; LocalHarnackConclusion.harnack_wrapper; LocalHarnackConclusion.holder_wrapper",
    dependsOn := ["C006-L07-domain-localization", "C006-L10-operator-solution-compatibility"],
    proofBudgetBound := 80,
    completionGate := "conclusion wrappers continue to compile against the concrete API"
  },
  {
    leafId := "C006-L12-abp-growth-interface-hooks",
    package := NonDivergenceApiPackage.statementCompatibility,
    statementTarget := "Expose interfaces consumed later by ABP, growth lemma, weak Harnack, Harnack-chain, and Holder oscillation packages.",
    repoLocalAnchor := "KrylovSafonovData.abpEstimatePackage; KrylovSafonovData.growthLemmaPackage",
    dependsOn := [
      "C006-L05-ellipticity-constants",
      "C006-L08-solution-predicate",
      "C006-L11-conclusion-api-compatibility"
    ],
    proofBudgetBound := 95,
    completionGate := "interfaces are concrete enough for later proof-package workers to own independently"
  }
]

/-- C006 has split the API work into twelve integration-ready leaves. -/
theorem c006NonDivergenceApiLeaves_length :
    c006NonDivergenceApiLeaves.length = 12 := by
  native_decide

/-- Every C006 leaf is budgeted at or below the M0387 one-hundred-step bound. -/
def c006AllNonDivergenceApiLeavesWithinBudget : Bool :=
  c006NonDivergenceApiLeaves.all (fun row => row.proofBudgetBound <= 100)

theorem c006AllNonDivergenceApiLeavesWithinBudget_eq_true :
    c006AllNonDivergenceApiLeavesWithinBudget = true := by
  native_decide

/-- C006 is ready for a serial public backfill patch. -/
def c006PublicNonDivergenceApiSplitReadyForBackfill : Bool :=
  true

/-- C006 does not close the terminal non-divergence Krylov-Safonov theorem. -/
def c006ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C006 state retains repo-local integration debt: this child records
a repo-local API split and keeps theorem closure open as formalization debt.
-/
def c006NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c006PublicNonDivergenceApiSplitReadyForBackfill_eq_true :
    c006PublicNonDivergenceApiSplitReadyForBackfill = true :=
  rfl

theorem c006ClosesKrylovSafonovTheorem_eq_false :
    c006ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c006NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c006NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-244-C007 Krylov-Safonov proof-package leaf split -/

/--
Proof packages that remain after the non-divergence PDE API is selected.

These constructors describe the M0387-sized package ledger for C007 only.  They
do not assert that stochastic representation, ABP, weak Harnack, Harnack-chain,
or Holder oscillation estimates have already been proved in this repository.
-/
inductive KrylovSafonovProofPackage where
  | stochasticRepresentation
  | exitTimeEstimate
  | hittingEstimate
  | abpEstimate
  | growthLemma
  | weakHarnack
  | harnackChain
  | holderOscillation
  | terminalAssembly
  deriving DecidableEq

/--
One integration-ready C007 leaf row.

`proofBudgetBound` is the intended local proof-step budget once the relevant
API exists.  Rows marked by this structure are unchecked proof obligations until
a later worker replaces the abstract package fields with local or imported
Lean proofs and validates them in this repository.
-/
structure KrylovSafonovProofLeafRow where
  leafId : String
  package : KrylovSafonovProofPackage
  statementTarget : String
  repoLocalAnchor : String
  dependsOn : List String
  proofBudgetBound : Nat
  completionGate : String
  deriving DecidableEq

/--
C007 expansion of the stochastic, ABP, growth, weak-Harnack, Harnack-chain, and
Holder-oscillation packages into independent M0387-sized leaves.

The rows are planning metadata with repo-local anchors.  They keep the terminal
Krylov-Safonov theorem open as formalization debt because pinned mathlib does
not currently supply these non-divergence proof packages and this repository has
not imported an exact external Lean proof.
-/
def c007KrylovSafonovProofLeaves : List KrylovSafonovProofLeafRow := [
  {
    leafId := "C007-L01-stochastic-process-carrier",
    package := KrylovSafonovProofPackage.stochasticRepresentation,
    statementTarget := "Choose the diffusion or Markov-process carrier associated to the non-divergence operator.",
    repoLocalAnchor := "KrylovSafonovData.stochasticRepresentation",
    dependsOn := ["C006-L01-operator-carrier", "C006-L03-coefficient-carrier"],
    proofBudgetBound := 90,
    completionGate := "carrier compiles and exposes a law or transition kernel compatible with HasLaw"
  },
  {
    leafId := "C007-L02-generator-identification",
    package := KrylovSafonovProofPackage.stochasticRepresentation,
    statementTarget := "Prove that the selected generator corresponds to the non-divergence operator on the local test class.",
    repoLocalAnchor := "KrylovSafonovData.nonDivergenceForm; KrylovSafonovData.solutionPredicate",
    dependsOn := ["C007-L01-stochastic-process-carrier", "C006-L08-solution-predicate"],
    proofBudgetBound := 100,
    completionGate := "generator-to-PDE bridge is available without changing LocalHarnackFormula"
  },
  {
    leafId := "C007-L03-stochastic-representation-formula",
    package := KrylovSafonovProofPackage.stochasticRepresentation,
    statementTarget := "State and prove the optional-stopping or representation formula for localized solutions.",
    repoLocalAnchor := "KrylovSafonovData.stochasticRepresentation",
    dependsOn := ["C007-L02-generator-identification", "C006-L07-domain-localization"],
    proofBudgetBound := 100,
    completionGate := "abstract stochasticRepresentation premise can be replaced by a checked formula package or a concrete blocker"
  },
  {
    leafId := "C007-L04-exit-time-definition",
    package := KrylovSafonovProofPackage.exitTimeEstimate,
    statementTarget := "Define the exit time from the outer metric ball for the chosen process.",
    repoLocalAnchor := "Metric.ball; KrylovSafonovData.stochasticRepresentation",
    dependsOn := ["C007-L01-stochastic-process-carrier", "C006-L07-domain-localization"],
    proofBudgetBound := 75,
    completionGate := "exit time is a reusable local object for probability estimates"
  },
  {
    leafId := "C007-L05-exit-time-tail-or-moment-bound",
    package := KrylovSafonovProofPackage.exitTimeEstimate,
    statementTarget := "Prove the local exit-time tail or moment estimate used by Krylov-Safonov growth arguments.",
    repoLocalAnchor := "C007-L04-exit-time-definition",
    dependsOn := ["C007-L04-exit-time-definition", "C006-L05-ellipticity-constants"],
    proofBudgetBound := 100,
    completionGate := "estimate is checked or a concrete missing probability API blocker is recorded"
  },
  {
    leafId := "C007-L06-hitting-set-definition",
    package := KrylovSafonovProofPackage.hittingEstimate,
    statementTarget := "Define hitting events for measurable subsets of the localized ball.",
    repoLocalAnchor := "Metric.ball; Measure.restrict",
    dependsOn := ["C007-L01-stochastic-process-carrier", "C006-L07-domain-localization"],
    proofBudgetBound := 70,
    completionGate := "hitting event vocabulary compiles against the selected process carrier"
  },
  {
    leafId := "C007-L07-hitting-probability-lower-bound",
    package := KrylovSafonovProofPackage.hittingEstimate,
    statementTarget := "Prove the lower hitting-probability estimate for sets of controlled measure density.",
    repoLocalAnchor := "C007-L06-hitting-set-definition",
    dependsOn := ["C007-L05-exit-time-tail-or-moment-bound", "C007-L06-hitting-set-definition"],
    proofBudgetBound := 100,
    completionGate := "bound feeds the growth lemma or records an explicit stochastic-integration blocker"
  },
  {
    leafId := "C007-L08-abp-contact-set-interface",
    package := KrylovSafonovProofPackage.abpEstimate,
    statementTarget := "Define the contact set, convex envelope, or substitute object needed for the ABP estimate.",
    repoLocalAnchor := "KrylovSafonovData.abpEstimatePackage",
    dependsOn := ["C006-L04-coefficient-measurability", "C006-L08-solution-predicate"],
    proofBudgetBound := 95,
    completionGate := "ABP geometric interface compiles with the selected solution predicate"
  },
  {
    leafId := "C007-L09-abp-measure-estimate",
    package := KrylovSafonovProofPackage.abpEstimate,
    statementTarget := "Prove the ABP measure/Jacobian estimate controlling the negative part by the RHS.",
    repoLocalAnchor := "KrylovSafonovData.abpEstimatePackage",
    dependsOn := ["C007-L08-abp-contact-set-interface", "C006-L06-rhs-carrier-and-bounds"],
    proofBudgetBound := 100,
    completionGate := "abstract abpEstimatePackage premise can be replaced or a concrete analysis API blocker is recorded"
  },
  {
    leafId := "C007-L10-growth-lemma-small-sublevel",
    package := KrylovSafonovProofPackage.growthLemma,
    statementTarget := "State and prove the small-sublevel-set growth lemma from ABP and ellipticity data.",
    repoLocalAnchor := "KrylovSafonovData.growthLemmaPackage",
    dependsOn := ["C007-L09-abp-measure-estimate", "C006-L05-ellipticity-constants"],
    proofBudgetBound := 100,
    completionGate := "growth lemma package replaces the abstract field for one normalized ball"
  },
  {
    leafId := "C007-L11-growth-lemma-scaling",
    package := KrylovSafonovProofPackage.growthLemma,
    statementTarget := "Prove scaling and localization variants needed to iterate the growth lemma across balls.",
    repoLocalAnchor := "Metric.ball; LocalHarnackFormula",
    dependsOn := ["C007-L10-growth-lemma-small-sublevel", "C006-L07-domain-localization"],
    proofBudgetBound := 90,
    completionGate := "growth lemma can be applied at all ball scales used by weak Harnack"
  },
  {
    leafId := "C007-L12-weak-harnack-level-set-decay",
    package := KrylovSafonovProofPackage.weakHarnack,
    statementTarget := "Derive level-set decay for nonnegative supersolutions from the growth lemma.",
    repoLocalAnchor := "LocalHarnackFormula nonnegativity premise",
    dependsOn := ["C007-L11-growth-lemma-scaling", "C006-L09-nonnegative-solution-hypothesis"],
    proofBudgetBound := 100,
    completionGate := "level-set decay compiles as the first weak-Harnack leaf"
  },
  {
    leafId := "C007-L13-weak-harnack-integral-bound",
    package := KrylovSafonovProofPackage.weakHarnack,
    statementTarget := "Convert level-set decay into the weak Harnack integral or essential-infimum comparison.",
    repoLocalAnchor := "essInf; Measure.restrict",
    dependsOn := ["C007-L12-weak-harnack-level-set-decay"],
    proofBudgetBound := 100,
    completionGate := "weak Harnack output is available for the Harnack-chain package"
  },
  {
    leafId := "C007-L14-harnack-chain-geometry",
    package := KrylovSafonovProofPackage.harnackChain,
    statementTarget := "Construct finite overlapping chains of inner balls inside the localized domain.",
    repoLocalAnchor := "Metric.ball; metric_ball_isOpen_mathlib_wrapper",
    dependsOn := ["C006-L07-domain-localization"],
    proofBudgetBound := 85,
    completionGate := "chain geometry is independent of PDE proof packages and compiles locally"
  },
  {
    leafId := "C007-L15-harnack-chain-iteration",
    package := KrylovSafonovProofPackage.harnackChain,
    statementTarget := "Iterate the weak Harnack comparison along the ball chain.",
    repoLocalAnchor := "LocalHarnackConclusion.harnack_wrapper",
    dependsOn := ["C007-L13-weak-harnack-integral-bound", "C007-L14-harnack-chain-geometry"],
    proofBudgetBound := 100,
    completionGate := "local essSup/essInf Harnack comparison is produced for the inner ball"
  },
  {
    leafId := "C007-L16-holder-oscillation-decay",
    package := KrylovSafonovProofPackage.holderOscillation,
    statementTarget := "Prove geometric oscillation decay from the Harnack comparison applied to shifted solutions.",
    repoLocalAnchor := "LocalHarnackConclusion.holder_wrapper",
    dependsOn := ["C007-L15-harnack-chain-iteration"],
    proofBudgetBound := 100,
    completionGate := "oscillation decay constants are available for Holder regularity"
  },
  {
    leafId := "C007-L17-holder-on-with-conclusion",
    package := KrylovSafonovProofPackage.holderOscillation,
    statementTarget := "Convert oscillation decay into HolderOnWith regularity on the inner ball.",
    repoLocalAnchor := "HolderOnWith; holderOnWith_continuousOn_mathlib_wrapper; holderOnWith_mono_mathlib_wrapper",
    dependsOn := ["C007-L16-holder-oscillation-decay"],
    proofBudgetBound := 100,
    completionGate := "HolderOnWith conclusion fills LocalHarnackConclusion.holder_on_inner_ball"
  },
  {
    leafId := "C007-L18-local-conclusion-assembly",
    package := KrylovSafonovProofPackage.terminalAssembly,
    statementTarget := "Assemble Harnack comparison and Holder regularity into LocalHarnackConclusion.",
    repoLocalAnchor := "LocalHarnackConclusion",
    dependsOn := ["C007-L15-harnack-chain-iteration", "C007-L17-holder-on-with-conclusion"],
    proofBudgetBound := 80,
    completionGate := "LocalHarnackConclusion constructor is filled by checked proof terms"
  },
  {
    leafId := "C007-L19-local-formula-discharge",
    package := KrylovSafonovProofPackage.terminalAssembly,
    statementTarget := "Discharge LocalHarnackFormula assumptions using the checked proof packages.",
    repoLocalAnchor := "LocalHarnackFormula",
    dependsOn := ["C007-L03-stochastic-representation-formula", "C007-L10-growth-lemma-small-sublevel", "C007-L18-local-conclusion-assembly"],
    proofBudgetBound := 95,
    completionGate := "one-ball formula is proved without abstract ABP/growth/stochastic assumptions"
  },
  {
    leafId := "C007-L20-statement-shape-wrapper",
    package := KrylovSafonovProofPackage.terminalAssembly,
    statementTarget := "Lift the checked one-ball formula to the normalized StatementShape wrapper.",
    repoLocalAnchor := "StatementShape; statementShape_iff_forall_local_ball",
    dependsOn := ["C007-L19-local-formula-discharge"],
    proofBudgetBound := 60,
    completionGate := "StatementShape wrapper compiles after terminal package closure"
  }
]

/-- C007 has split the proof-package work into twenty integration-ready leaves. -/
theorem c007KrylovSafonovProofLeaves_length :
    c007KrylovSafonovProofLeaves.length = 20 := by
  native_decide

/-- Every C007 proof-package leaf is budgeted at or below the M0387 bound. -/
def c007AllKrylovSafonovProofLeavesWithinBudget : Bool :=
  c007KrylovSafonovProofLeaves.all (fun row => row.proofBudgetBound <= 100)

theorem c007AllKrylovSafonovProofLeavesWithinBudget_eq_true :
    c007AllKrylovSafonovProofLeavesWithinBudget = true := by
  native_decide

/-- C007 is ready for a serial public backfill patch. -/
def c007PublicProofPackageSplitReadyForBackfill : Bool :=
  true

/-- C007 does not close the terminal non-divergence Krylov-Safonov theorem. -/
def c007ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C007 state retains repo-local integration debt: this child records
a repo-local proof-package split and keeps theorem closure open as
formalization debt until exact Lean proof packages are imported or written.
-/
def c007NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c007PublicProofPackageSplitReadyForBackfill_eq_true :
    c007PublicProofPackageSplitReadyForBackfill = true :=
  rfl

theorem c007ClosesKrylovSafonovTheorem_eq_false :
    c007ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c007NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c007NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-244-C008 external Lean 4 exact-source audit -/

/--
One external Lean 4 source-search audit row for the C008 task.

Rows in this table are audit metadata.  A row may contain adjacent Harnack
evidence, but it is not terminal Krylov-Safonov closure unless
`exactTerminalKrylovSafonov` is true and the source is also imported or pinned
into this repository's Lake validation closure.
-/
structure ExternalLean4SourceSearchAuditRow where
  repository : String
  commit : String
  exactSearchTerms : List String
  matchedTerms : List String
  theoremNames : List String
  sorryFreeStatus : String
  toolchain : String
  mathlibDependency : String
  exactTerminalKrylovSafonov : Bool
  repoLocalClosure : String
  conclusion : String
  deriving DecidableEq

/--
C008 exact-source audit for the located external Lean 4 PDE regularity project.

The direct source checkout was searched with:
`rg -n "KrylovSafonov|Krylov_Safonov|nonDivergence|non_divergence|\bviscosity\b|\bABP\b|weak_harnack|\bharnack\b" /tmp/s1_m_244_c008/DeGiorgi -g '*.lean'`.
The exact terminal terms `KrylovSafonov`, `Krylov_Safonov`,
`nonDivergence`, `non_divergence`, `viscosity`, and `ABP` had no `.lean`
matches in this checkout; `weak_harnack` and `harnack` matched adjacent
divergence-form De Giorgi/Moser theorem families.
-/
def c008ExternalLean4SourceSearchRows : List ExternalLean4SourceSearchAuditRow := [
  {
    repository := "https://github.com/scottnarmstrong/DeGiorgi",
    commit := "4c1b3077d3782b24065184df4ba59501b2e56fc7",
    exactSearchTerms := [
      "KrylovSafonov",
      "Krylov_Safonov",
      "nonDivergence",
      "non_divergence",
      "viscosity",
      "ABP",
      "weak_harnack",
      "harnack"
    ],
    matchedTerms := [
      "weak_harnack",
      "harnack"
    ],
    theoremNames := [
      "weak_harnack_stage_one_inverse",
      "weak_harnack_stage_one_forward",
      "weak_harnack_stage_one_forward_ball",
      "weak_harnack_stage_one_inverse_ball",
      "weak_harnack_chain",
      "weak_harnack",
      "weak_harnack_on_ball",
      "harnack",
      "harnack_of_homogeneousWeakSolution",
      "harnack_on_ball",
      "harnack_on_ball_ae_pos",
      "holder_Moser",
      "holder_Moser_of_homogeneousWeakSolution"
    ],
    sorryFreeStatus := "source search over .lean files found no sorry, admit, or axiom declarations; README states sorry-free and axiom-free beyond Lean and Mathlib",
    toolchain := "leanprover/lean4:v4.29.0-rc6",
    mathlibDependency := "mathlib inputRev v4.29.0-rc6, manifest revision 5c8398df528176d9c87ccd9226ba8f7c8852d59c",
    exactTerminalKrylovSafonov := false,
    repoLocalClosure := "not imported, pinned, or checked by this repository's Lake dependency closure",
    conclusion := "adjacent divergence-form Harnack/Holder evidence only; no exact non-divergence Krylov-Safonov terminal theorem was located"
  }
]

/-- C008 records all exact terms requested by the child task. -/
def c008ExactSearchTerms : List String := [
  "KrylovSafonov",
  "Krylov_Safonov",
  "nonDivergence",
  "non_divergence",
  "viscosity",
  "ABP",
  "weak_harnack",
  "harnack"
]

/-- Broad GitHub code search was not available in this local worker without authentication. -/
def c008BroadGithubCodeSearchRequiresAuthentication : Bool :=
  true

/-- The C008 external audit did not locate an exact terminal Krylov-Safonov Lean proof. -/
def c008FoundExactTerminalExternalLean4Proof : Bool :=
  false

/-- C008 does not close the terminal non-divergence Krylov-Safonov theorem. -/
def c008ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C008 state retains repo-local integration debt: the only concrete
external source row is classified as adjacent evidence, not as completed
terminal theorem closure.
-/
def c008NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- C008 has one concrete external source-search row. -/
theorem c008ExternalLean4SourceSearchRows_length :
    c008ExternalLean4SourceSearchRows.length = 1 := by
  native_decide

/-- C008 records the eight exact requested search terms. -/
theorem c008ExactSearchTerms_length :
    c008ExactSearchTerms.length = 8 := by
  native_decide

theorem c008BroadGithubCodeSearchRequiresAuthentication_eq_true :
    c008BroadGithubCodeSearchRequiresAuthentication = true :=
  rfl

theorem c008FoundExactTerminalExternalLean4Proof_eq_false :
    c008FoundExactTerminalExternalLean4Proof = false :=
  rfl

theorem c008ClosesKrylovSafonovTheorem_eq_false :
    c008ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c008NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c008NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-244-C009 external terminal integration gate -/

/--
Decision states for the external-terminal-proof integration gate.

This gate is only about exact terminal Lean 4 evidence for the non-divergence
Krylov-Safonov theorem.  Adjacent Harnack/Holder evidence remains useful audit
metadata, but it cannot enter the completed state unless it is exact and then
imported, pinned, or blocked with a concrete integration reason.
-/
inductive ExternalTerminalIntegrationDecision where
  | noExactTerminalProofFound
  | exactProofPinnedAndChecked
  | exactProofFoundButBlocked
  deriving DecidableEq

/--
C009 integration-gate row.

The current gate consumes the C008 source-audit result.  Since no exact
terminal external Lean 4 proof was found there, this repository has no external
proof body to pin/import/check for S1-M-244.  The result is therefore an open
formalization boundary rather than `external_upstream_anchor_only` completion.
-/
structure ExternalTerminalIntegrationGateRow where
  childId : String
  upstreamAuditAnchor : String
  decision : ExternalTerminalIntegrationDecision
  exactProofRepository : Option String
  exactProofCommit : Option String
  exactProofTheoremName : Option String
  lakeAction : String
  blocker : String
  repoLocalStatus : String
  completionBoundary : String
  deriving DecidableEq

/--
C009 records that the exact-terminal external proof integration branch is not
applicable yet because C008 found no exact non-divergence Krylov-Safonov Lean 4
proof.
-/
def c009ExternalTerminalIntegrationGateRows :
    List ExternalTerminalIntegrationGateRow := [
  {
    childId := "S1-M-244-C009",
    upstreamAuditAnchor := "c008ExternalLean4SourceSearchRows; c008FoundExactTerminalExternalLean4Proof_eq_false",
    decision := ExternalTerminalIntegrationDecision.noExactTerminalProofFound,
    exactProofRepository := none,
    exactProofCommit := none,
    exactProofTheoremName := none,
    lakeAction := "no Lake pin/import/check action is available because no exact terminal external proof was located",
    blocker := "terminal non-divergence Krylov-Safonov Lean 4 proof not found by the recorded exact source audit; adjacent DeGiorgi divergence-form Harnack evidence is not exact closure",
    repoLocalStatus := "not_repo_local_closed; formalization_debt remains",
    completionBoundary := "does not mark S1-M-244 completed and does not use external_upstream_anchor_only as completion evidence"
  }
]

/-- C009 gate decision: no exact terminal external proof has been found. -/
def c009ExternalTerminalIntegrationDecision :
    ExternalTerminalIntegrationDecision :=
  ExternalTerminalIntegrationDecision.noExactTerminalProofFound

/-- C009 found no exact terminal external Lean 4 proof to integrate. -/
def c009FoundExactTerminalExternalLean4Proof : Bool :=
  false

/-- C009 therefore did not pin/import/check an external theorem in Lake. -/
def c009PinnedImportedCheckedExternalProof : Bool :=
  false

/-- C009 does not close the terminal non-divergence Krylov-Safonov theorem. -/
def c009ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C009 state retains repo-local integration debt: the gate remains
open and records a concrete absence/blocker, not a completed anchor-only claim.
-/
def c009NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- C009 has one integration-gate row. -/
theorem c009ExternalTerminalIntegrationGateRows_length :
    c009ExternalTerminalIntegrationGateRows.length = 1 := by
  native_decide

theorem c009ExternalTerminalIntegrationDecision_eq_noExactTerminalProofFound :
    c009ExternalTerminalIntegrationDecision =
      ExternalTerminalIntegrationDecision.noExactTerminalProofFound :=
  rfl

theorem c009FoundExactTerminalExternalLean4Proof_eq_false :
    c009FoundExactTerminalExternalLean4Proof = false :=
  rfl

theorem c009PinnedImportedCheckedExternalProof_eq_false :
    c009PinnedImportedCheckedExternalProof = false :=
  rfl

theorem c009ClosesKrylovSafonovTheorem_eq_false :
    c009ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c009NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c009NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-244-C010 public synchronization gate -/

/--
Decision states for the public synchronization gate.

This gate is deliberately separate from theorem proving.  Public blueprint,
todo, and README updates are serial integrator work, and this child does not
own those shared documents.
-/
inductive PublicBackfillGateDecision where
  | noTheoremClosureYet
  | readyForSerialIntegratorPatch
  deriving DecidableEq

/--
C010 public-backfill gate row.

The current Lean artifact records statement-shape and audit metadata only.
Since C009 found no exact terminal proof to pin/import/check and no local
terminal theorem is proved here, there is no theorem-closure status to backfill
into public documents.  The row preserves the rule that any future closure must
be synchronized by a single serial integrator patch rather than by child
workers editing shared public surfaces.
-/
structure PublicBackfillGateRow where
  childId : String
  theoremClosureValidated : Bool
  decision : PublicBackfillGateDecision
  publicDocsOwnedByThisChild : Bool
  requiredPublicTargets : List String
  integratorPatchRule : String
  repoLocalStatus : String
  completionBoundary : String
  deriving DecidableEq

/--
C010 records that no public completion backfill is permitted yet, because this
slot has not closed the terminal non-divergence Krylov-Safonov theorem.
-/
def c010PublicBackfillGateRows : List PublicBackfillGateRow := [
  {
    childId := "S1-M-244-C010",
    theoremClosureValidated := false,
    decision := PublicBackfillGateDecision.noTheoremClosureYet,
    publicDocsOwnedByThisChild := false,
    requiredPublicTargets := [
      "Docs/Stage1_Blueprint.md",
      "Docs/todos_20260430.md",
      "README.md"
    ],
    integratorPatchRule := "after a future repo-local theorem closure, update blueprint, todos, and README together in one serial integrator patch; worker ledgers under .cron/results/ are not public completion surfaces",
    repoLocalStatus := "not_repo_local_closed; formalization_debt remains",
    completionBoundary := "documentation synchronization gate only; does not prove or close the Krylov-Safonov theorem"
  }
]

/-- C010 found no theorem closure requiring public completion backfill. -/
def c010TheoremClosureValidated : Bool :=
  false

/-- C010 does not own or edit shared public planning documents. -/
def c010PublicDocsOwnedByThisChild : Bool :=
  false

/-- C010 does not close the terminal non-divergence Krylov-Safonov theorem. -/
def c010ClosesKrylovSafonovTheorem : Bool :=
  false

/--
No completed C010 state retains repo-local integration debt: there is no
completed theorem state, and the gate remains open as public integration work.
-/
def c010NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- C010 has one public-backfill gate row. -/
theorem c010PublicBackfillGateRows_length :
    c010PublicBackfillGateRows.length = 1 := by
  native_decide

theorem c010TheoremClosureValidated_eq_false :
    c010TheoremClosureValidated = false :=
  rfl

theorem c010PublicDocsOwnedByThisChild_eq_false :
    c010PublicDocsOwnedByThisChild = false :=
  rfl

theorem c010ClosesKrylovSafonovTheorem_eq_false :
    c010ClosesKrylovSafonovTheorem = false :=
  rfl

theorem c010NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c010NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check StatementShape
#check statementShape_iff_forall_local_ball
#check LocalHarnackConclusion.harnack_wrapper
#check LocalHarnackConclusion.holder_wrapper
#check holderOnWith_continuousOn_mathlib_wrapper
#check holderOnWith_mono_mathlib_wrapper
#check essSup_const_restrict_mathlib_wrapper
#check essInf_const_restrict_mathlib_wrapper
#check metric_ball_isOpen_mathlib_wrapper
#check hasLaw_id_mathlib_wrapper
#check TerminalMathlibSearchBlockerRow
#check c003TerminalMathlibBlockerRows
#check c003TerminalMathlibBlockerRows_length
#check c003PublicMathlibBlockerReadyForBackfill_eq_true
#check c003ClosesKrylovSafonovTheorem_eq_false
#check c003NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check AdjacentExternalAnchorRow
#check c004DegiorgiAdjacentAnchorRows
#check c004DegiorgiAdjacentAnchorRows_length
#check c004PublicDegiorgiNoteReadyForBackfill_eq_true
#check c004ClosesKrylovSafonovTheorem_eq_false
#check c004NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check FormalizationRoute
#check FormalizationRouteDecisionRow
#check c005RouteDecisionRows
#check c005RouteDecisionRows_length
#check c005SelectedFormalizationRoute_eq_pdeViscosity
#check c005DeferredFormalizationRoute_eq_probabilisticDiffusionGenerator
#check c005PublicRouteDecisionReadyForBackfill_eq_true
#check c005ClosesKrylovSafonovTheorem_eq_false
#check c005NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check NonDivergenceApiPackage
#check NonDivergenceApiLeafRow
#check c006NonDivergenceApiLeaves
#check c006NonDivergenceApiLeaves_length
#check c006AllNonDivergenceApiLeavesWithinBudget_eq_true
#check c006PublicNonDivergenceApiSplitReadyForBackfill_eq_true
#check c006ClosesKrylovSafonovTheorem_eq_false
#check c006NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check KrylovSafonovProofPackage
#check KrylovSafonovProofLeafRow
#check c007KrylovSafonovProofLeaves
#check c007KrylovSafonovProofLeaves_length
#check c007AllKrylovSafonovProofLeavesWithinBudget_eq_true
#check c007PublicProofPackageSplitReadyForBackfill_eq_true
#check c007ClosesKrylovSafonovTheorem_eq_false
#check c007NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check ExternalLean4SourceSearchAuditRow
#check c008ExternalLean4SourceSearchRows
#check c008ExternalLean4SourceSearchRows_length
#check c008ExactSearchTerms
#check c008ExactSearchTerms_length
#check c008BroadGithubCodeSearchRequiresAuthentication_eq_true
#check c008FoundExactTerminalExternalLean4Proof_eq_false
#check c008ClosesKrylovSafonovTheorem_eq_false
#check c008NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check ExternalTerminalIntegrationDecision
#check ExternalTerminalIntegrationGateRow
#check c009ExternalTerminalIntegrationGateRows
#check c009ExternalTerminalIntegrationGateRows_length
#check c009ExternalTerminalIntegrationDecision_eq_noExactTerminalProofFound
#check c009FoundExactTerminalExternalLean4Proof_eq_false
#check c009PinnedImportedCheckedExternalProof_eq_false
#check c009ClosesKrylovSafonovTheorem_eq_false
#check c009NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check PublicBackfillGateDecision
#check PublicBackfillGateRow
#check c010PublicBackfillGateRows
#check c010PublicBackfillGateRows_length
#check c010TheoremClosureValidated_eq_false
#check c010PublicDocsOwnedByThisChild_eq_false
#check c010ClosesKrylovSafonovTheorem_eq_false
#check c010NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check HolderOnWith
#check essSup
#check essInf
#check Metric.ball
#check HasLaw

end AwesomeTheorems.Stage1.S1_M_244
