import Mathlib.InformationTheory.KullbackLeibler.ChainRule
import Mathlib.InformationTheory.KullbackLeibler.Basic
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Measure.Tight
import Mathlib.Probability.Independence.Basic
import Mathlib.Topology.MetricSpace.Basic

/-!
# S1-M-280 / THM-M-1000: transportation inequality

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
transportation-cost inequalities and their concentration consequences.

The pinned mathlib snapshot
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has probability measures,
product measures, Kullback-Leibler divergence, nonnegative extended integrals,
Levy-Prokhorov weak-convergence/tightness infrastructure, and
independence/product APIs.  This audit did not find a terminal
Wasserstein/Talagrand transportation inequality or concentration theorem in
the local Lake closure.

The declarations below therefore normalize transport plans, squared-distance
transport costs, the optimal transport-cost infimum, the entropy side via
`InformationTheory.klDiv`, and the missing concentration bridge as explicit
data.  No proof placeholder is introduced.
-/

noncomputable section

open InformationTheory MeasureTheory ProbabilityTheory Set Real
open scoped ENNReal NNReal

namespace AwesomeTheorems.Stage1.S1_M_280

universe u v

variable {X : Type u} [MeasurableSpace X]

/--
A transport plan between two probability measures on the same measurable space.

The plan is a probability measure on the product whose coordinate
push-forwards are the prescribed marginals.
-/
structure TransportPlan (ν μ : ProbabilityMeasure X) : Type u where
  plan : Measure (X × X)
  isProbability : IsProbabilityMeasure plan
  fst_marginal : Measure.map Prod.fst plan = (ν : Measure X)
  snd_marginal : Measure.map Prod.snd plan = (μ : Measure X)

instance (ν μ : ProbabilityMeasure X) (γ : TransportPlan ν μ) :
    IsProbabilityMeasure γ.plan :=
  γ.isProbability

/--
The independent product coupling.  This is not usually optimal, but it is a
checked nonempty-admissible-plan anchor for the formal transport-plan API.
-/
def independentPlan (ν μ : ProbabilityMeasure X) : TransportPlan ν μ where
  plan := (ν : Measure X).prod (μ : Measure X)
  isProbability := by infer_instance
  fst_marginal := by
    rw [Measure.map_fst_prod]
    simp
  snd_marginal := by
    rw [Measure.map_snd_prod]
    simp

/-- Nonnegative transport cost of a plan. -/
def TransportCost {ν μ : ProbabilityMeasure X} (c : X × X -> ENNReal)
    (γ : TransportPlan ν μ) : ENNReal :=
  ∫⁻ z, c z ∂γ.plan

/-- Optimal transport cost as an infimum over admissible plans. -/
def OptimalTransportCost (ν μ : ProbabilityMeasure X) (c : X × X -> ENNReal) :
    ENNReal :=
  ⨅ γ : TransportPlan ν μ, TransportCost c γ

/--
Squared metric cost used by the usual `T_2` / Talagrand transportation
inequality statement.
-/
def squaredDistCost [PseudoMetricSpace X] : X × X -> ENNReal :=
  fun z => ENNReal.ofReal ((dist z.1 z.2) ^ (2 : Nat))

/--
Available public transport-cost API routes for the Stage1 transportation
inequality slot.

The selected route is recorded separately below; the other constructors are
kept so a future mathlib Wasserstein API or a pinned external Lean dependency
can replace the local route only after a repo-local bridge validates.
-/
inductive TransportCostAPIRoute : Type where
  | localOptimalTransportCostSquaredDist
  | futureMathlibWasserstein
  | pinnedExternalLean4Dependency
  deriving DecidableEq

/--
Selected public transport-cost API for `THM-M-1000.transport-api`.

Use the repo-local `OptimalTransportCost` applied to `squaredDistCost` as the
canonical Stage1 surface.  This is an `ENNReal` cost infimum over transport
plans, not a completed Wasserstein metric API and not a proof of Talagrand's
inequality.
-/
def selectedTransportCostAPIRoute : TransportCostAPIRoute :=
  .localOptimalTransportCostSquaredDist

/-- The transport-cost API child selects the local squared-cost route. -/
theorem selectedTransportCostAPIRoute_eq :
    selectedTransportCostAPIRoute =
      TransportCostAPIRoute.localOptimalTransportCostSquaredDist :=
  rfl

/--
Bridge obligation for any future squared-Wasserstein API.

If mathlib or a pinned external Lean 4 dependency later supplies a squared
Wasserstein cost, it should be connected to the current public API by proving
this predicate for that supplied function before changing the selected route.
-/
def WassersteinSquaredBridgeTarget [PseudoMetricSpace X]
    (W2sq : ProbabilityMeasure X -> ProbabilityMeasure X -> ENNReal) : Prop :=
  ∀ ν μ : ProbabilityMeasure X,
    W2sq ν μ = OptimalTransportCost ν μ squaredDistCost

/-- Public decision sentence for later serialized blueprint backfill. -/
def selectedTransportCostAPIPublicDecision : String :=
  "Use the repo-local `OptimalTransportCost ν μ squaredDistCost` as the public Stage1 transport-cost API for THM-M-1000. Treat a future mathlib Wasserstein API or an external Lean 4 optimal-transport dependency as a replacement only after a local bridge to `OptimalTransportCost squaredDistCost` is pinned/imported/checked in this repository."

/--
`T_2`-style transportation inequality, stated directly with the available
mathlib KL-divergence anchor.

The constant is kept in `ENNReal` so that Stage1 can avoid committing to a
particular real-valued square-root/Wasserstein API before such an API is either
found upstream or introduced locally.
-/
def TalagrandT2Inequality [PseudoMetricSpace X] (μ : ProbabilityMeasure X)
    (constant : ENNReal) : Prop :=
  ∀ ν : ProbabilityMeasure X,
    OptimalTransportCost ν μ squaredDistCost <=
      constant * klDiv (ν : Measure X) (μ : Measure X)

/--
Upper deviation event for a real-valued observable around its `μ`-mean.

The concrete concentration target uses the one-sided event
`∫ f dμ + r ≤ f x`.
-/
def upperLipschitzTailEvent (μ : ProbabilityMeasure X) (f : X -> ℝ) (r : ℝ) :
    Set X :=
  {x | (∫ y, f y ∂(μ : Measure X)) + r ≤ f x}

/-- Lower deviation event for a real-valued observable around its `μ`-mean. -/
def lowerLipschitzTailEvent (μ : ProbabilityMeasure X) (f : X -> ℝ) (r : ℝ) :
    Set X :=
  {x | f x ≤ (∫ y, f y ∂(μ : Measure X)) - r}

/--
The normalized exponential constant for the concentration consequences of the
local `T_2` convention `W₂² ≤ C · KL`.

With this file's `TalagrandT2Inequality` normalization, the target tail and
enlargement bounds use `exp (-r^2 / C)`.
-/
def t2ConcentrationExponentialBound (constant r : ℝ) : ℝ :=
  Real.exp (-(r ^ (2 : Nat)) / constant)

/--
Concrete Lipschitz-observable concentration target for the transportation
inequality slot.

For every real-valued `1`-Lipschitz observable, explicitly assuming
`AEMeasurable`, `Integrable`, and measurability of the two tail events, both
one-sided deviations are bounded by `exp (-r^2 / C)`.
-/
def LipschitzObservableTailBound [PseudoMetricSpace X]
    (μ : ProbabilityMeasure X) (constant : ℝ) : Prop :=
  ∀ ⦃f : X -> ℝ⦄,
    LipschitzWith (1 : ℝ≥0) f ->
      AEMeasurable f (μ : Measure X) ->
        Integrable f (μ : Measure X) ->
          ∀ ⦃r : ℝ⦄,
            0 ≤ r ->
              MeasurableSet (upperLipschitzTailEvent μ f r) ->
                MeasurableSet (lowerLipschitzTailEvent μ f r) ->
                  (μ : Measure X).real (upperLipschitzTailEvent μ f r) ≤
                      t2ConcentrationExponentialBound constant r ∧
                    (μ : Measure X).real (lowerLipschitzTailEvent μ f r) ≤
                      t2ConcentrationExponentialBound constant r

/-- Closed metric enlargement of a set by radius `r`. -/
def closedMetricEnlargement [PseudoMetricSpace X] (r : ℝ) (s : Set X) : Set X :=
  {x | ∃ y ∈ s, dist x y ≤ r}

/--
Concrete set-enlargement concentration target for the transportation
inequality slot.

Every measurable set of probability at least `1 / 2` has an `r`-enlargement
whose complement has probability at most `exp (-r^2 / C)`, with explicit
measurability hypotheses for the original set and its enlargement.
-/
def SetEnlargementConcentrationBound [PseudoMetricSpace X]
    (μ : ProbabilityMeasure X) (constant : ℝ) : Prop :=
  ∀ ⦃s : Set X⦄ ⦃r : ℝ⦄,
    0 ≤ r ->
      MeasurableSet s ->
        MeasurableSet (closedMetricEnlargement (X := X) r s) ->
          (1 / 2 : ℝ) ≤ (μ : Measure X).real s ->
            (μ : Measure X).real ((closedMetricEnlargement (X := X) r s)ᶜ) ≤
              t2ConcentrationExponentialBound constant r

/--
Statement-shape package for the concentration conclusion supplied by a
transportation inequality.

A terminal formalization must prove the two concrete concentration targets
from the transport inequality, rather than supplying anchor-only evidence.
The real constant `C` is connected to the local `T_2` convention by
`ENNReal.ofReal C`.
-/
structure TransportationConcentrationData [PseudoMetricSpace X]
    (μ : ProbabilityMeasure X) (constant : ℝ) : Type u where
  constant_positive : 0 < constant
  transport_inequality : TalagrandT2Inequality μ (ENNReal.ofReal constant)
  lipschitz_observable_tail_bound :
    LipschitzObservableTailBound μ constant
  set_enlargement_concentration_bound :
    SetEnlargementConcentrationBound μ constant
  tensorization_or_product_measure_branch : Prop
  tensorization_or_product_measure_branch_proof :
    tensorization_or_product_measure_branch

/--
Normalized Stage1 statement shape for the transportation inequality slot.

For a Borel pseudo-metric probability space, a `T_2` transportation inequality
with respect to the squared-distance cost and KL divergence should imply the
standard concentration package.  The current file records the exact formal
boundary; it does not prove the concentration theorem.
-/
def StatementShape (X : Type u)
    [PseudoMetricSpace X] [MeasurableSpace X] [BorelSpace X] : Prop :=
  ∀ (μ : ProbabilityMeasure X) (constant : ℝ),
    0 < constant ->
      TalagrandT2Inequality μ (ENNReal.ofReal constant) ->
      Nonempty (TransportationConcentrationData μ constant)

/-- The statement shape unfolds to the normalized concentration-data package. -/
theorem statementShape_iff (X : Type u)
    [PseudoMetricSpace X] [MeasurableSpace X] [BorelSpace X] :
    StatementShape X ↔
      ∀ (μ : ProbabilityMeasure X) (constant : ℝ),
        0 < constant ->
          TalagrandT2Inequality μ (ENNReal.ofReal constant) ->
          Nonempty (TransportationConcentrationData μ constant) :=
  Iff.rfl

/--
Structured statement-normalization row for serialized public backfill.

This row names `StatementShape` as the current repo-local Lean boundary and
records that this boundary is not a terminal transportation-concentration
proof.
-/
structure StatementNormalizationDecisionRow where
  task : String
  leanBoundaryName : String
  leanBoundaryValidatedInRepo : Bool
  terminalTransportationConcentrationProof : Bool
  publicNote : String

/--
Current public statement-normalization decision for `THM-M-1000.statement`.

The selected boundary is the checked declaration
`AwesomeTheorems.Stage1.S1_M_280.StatementShape`.  It normalizes the local
statement as a `T_2`-style transportation inequality implying concrete
Lipschitz-observable and set-enlargement concentration data.  It does not
prove that implication.
-/
def statementNormalizationDecisionRows : List StatementNormalizationDecisionRow := [
  { task := "THM-M-1000.statement",
    leanBoundaryName := "AwesomeTheorems.Stage1.S1_M_280.StatementShape",
    leanBoundaryValidatedInRepo := true,
    terminalTransportationConcentrationProof := false,
    publicNote :=
      "Use `AwesomeTheorems.Stage1.S1_M_280.StatementShape` as the current repo-local Lean boundary for THM-M-1000. This normalizes the statement as a T2-style squared-distance transportation inequality implying concrete Lipschitz-observable and set-enlargement concentration data, but it is not a terminal transportation-concentration proof." }
]

/-- The current statement-normalization audit surface has exactly one row. -/
theorem statementNormalizationDecisionRows_length :
    statementNormalizationDecisionRows.length = 1 :=
  rfl

/-- The first marginal field is available as a theorem wrapper. -/
theorem fst_marginal_eq {ν μ : ProbabilityMeasure X} (γ : TransportPlan ν μ) :
    Measure.map Prod.fst γ.plan = (ν : Measure X) :=
  γ.fst_marginal

/-- The second marginal field is available as a theorem wrapper. -/
theorem snd_marginal_eq {ν μ : ProbabilityMeasure X} (γ : TransportPlan ν μ) :
    Measure.map Prod.snd γ.plan = (μ : Measure X) :=
  γ.snd_marginal

/-- The product coupling has the expected first marginal. -/
theorem independentPlan_fst (ν μ : ProbabilityMeasure X) :
    Measure.map Prod.fst (independentPlan ν μ).plan = (ν : Measure X) :=
  (independentPlan ν μ).fst_marginal

/-- The product coupling has the expected second marginal. -/
theorem independentPlan_snd (ν μ : ProbabilityMeasure X) :
    Measure.map Prod.snd (independentPlan ν μ).plan = (μ : Measure X) :=
  (independentPlan ν μ).snd_marginal

/-- The optimal transport-cost infimum is bounded by every admissible plan. -/
theorem optimalTransportCost_le_plan {ν μ : ProbabilityMeasure X}
    (c : X × X -> ENNReal) (γ : TransportPlan ν μ) :
    OptimalTransportCost ν μ c <= TransportCost c γ :=
  iInf_le _ γ

/-- The KL-divergence side is pinned to mathlib and vanishes on the diagonal. -/
theorem klDiv_self_probability (μ : ProbabilityMeasure X) :
    klDiv (μ : Measure X) (μ : Measure X) = 0 := by
  exact klDiv_self (μ : Measure X)

/-! ## Entropy / KL branch audit boundary -/

/--
Available entropy-side routes for the transportation-to-concentration proof.

The checked route in this file is mathlib's KL chain rule for
composition-products.  The tilted-measure route is recorded as adjacent
infrastructure for a future entropy variational formula, but no variational
formula is proved here.
-/
inductive EntropyBranchRoute : Type where
  | compProdChainRuleTensorization
  | entropyVariationalFormulaViaTiltedMeasure
  | pinnedExternalLean4EntropyDependency
  deriving DecidableEq

/--
Selected entropy branch for the current Stage1 artifact.

This selects the repo-local mathlib chain-rule surface, not a completed
transportation-to-concentration proof.
-/
def selectedEntropyBranchRoute : EntropyBranchRoute :=
  .compProdChainRuleTensorization

/-- The entropy branch currently uses mathlib's checked KL chain-rule route. -/
theorem selectedEntropyBranchRoute_eq :
    selectedEntropyBranchRoute =
      EntropyBranchRoute.compProdChainRuleTensorization :=
  rfl

/--
Statement shape supplied by mathlib's KL chain rule for composition-products.

This is the checked tensorization-adjacent equality currently available in
`InformationTheory.KullbackLeibler.ChainRule`.
-/
def KLCompProdChainRuleTarget {Y : Type v} [MeasurableSpace Y]
    (μ ν : Measure X) (κ η : Kernel X Y) : Prop :=
  klDiv (μ ⊗ₘ κ) (ν ⊗ₘ η) =
    klDiv μ ν + klDiv (μ ⊗ₘ κ) (μ ⊗ₘ η)

/--
Statement shape saying that adjoining the same conditional law on the right
does not change KL divergence.
-/
def KLCompProdLeftTensorizationTarget {Y : Type v} [MeasurableSpace Y]
    (μ ν : Measure X) (κ : Kernel X Y) : Prop :=
  klDiv (μ ⊗ₘ κ) (ν ⊗ₘ κ) = klDiv μ ν

/-- Checked wrapper around `InformationTheory.klDiv_compProd_eq_add`. -/
theorem klDiv_compProd_chainRule_anchor {Y : Type v} [MeasurableSpace Y]
    (μ ν : Measure X) (κ η : Kernel X Y)
    [IsFiniteMeasure μ] [IsFiniteMeasure ν] [IsMarkovKernel κ] [IsMarkovKernel η] :
    KLCompProdChainRuleTarget μ ν κ η := by
  exact InformationTheory.klDiv_compProd_eq_add μ ν κ η

/-- Checked wrapper around `InformationTheory.klDiv_compProd_left`. -/
theorem klDiv_compProd_left_tensorization_anchor {Y : Type v} [MeasurableSpace Y]
    (μ ν : Measure X) (κ : Kernel X Y)
    [IsFiniteMeasure μ] [IsFiniteMeasure ν] [IsMarkovKernel κ] :
    KLCompProdLeftTensorizationTarget μ ν κ := by
  exact InformationTheory.klDiv_compProd_left μ ν κ

/--
Product-measure specialization of the checked chain-rule left tensorization:
adding the same independent probability factor preserves KL divergence.
-/
theorem klDiv_prod_right_same_probability {Y : Type v} [MeasurableSpace Y]
    (ν μ : ProbabilityMeasure X) (ρ : ProbabilityMeasure Y) :
    klDiv ((ν : Measure X).prod (ρ : Measure Y))
        ((μ : Measure X).prod (ρ : Measure Y)) =
      klDiv (ν : Measure X) (μ : Measure X) := by
  rw [← Measure.compProd_const, ← Measure.compProd_const]
  exact InformationTheory.klDiv_compProd_left (ν : Measure X) (μ : Measure X)
    (Kernel.const X (ρ : Measure Y))

/--
Future full entropy variational formula target.

The concentration proof usually needs a variational/duality inequality
relating exponential moments and KL divergence.  mathlib currently provides
`Measure.tilted` infrastructure adjacent to this route, but this proposition is
kept as an explicit open target rather than an asserted theorem.
-/
def EntropyVariationalFormulaTarget (μ : ProbabilityMeasure X) : Prop :=
  ∀ (ν : ProbabilityMeasure X) ⦃f : X -> ℝ⦄,
    AEMeasurable f (ν : Measure X) ->
      Integrable f (ν : Measure X) ->
        AEMeasurable f (μ : Measure X) ->
          Integrable (fun x => Real.exp (f x)) (μ : Measure X) ->
            ENNReal.ofReal
                ((∫ x, f x ∂(ν : Measure X)) -
                  Real.log (∫ x, Real.exp (f x) ∂(μ : Measure X))) ≤
              klDiv (ν : Measure X) (μ : Measure X)

/--
The entropy branch gate is intentionally nonterminal: the chain-rule anchors
are checked, but the full variational formula and its use in concentration are
not part of the current repo-local closure.
-/
def entropyBranchRepoLocalGateClosed : Bool := false

/-- A terminal concentration-data package exposes the `T_2` inequality. -/
theorem talagrandT2_of_data [PseudoMetricSpace X]
    {μ : ProbabilityMeasure X} {constant : ℝ}
    (d : TransportationConcentrationData μ constant) :
    TalagrandT2Inequality μ (ENNReal.ofReal constant) :=
  d.transport_inequality

/-- A terminal concentration-data package exposes positivity of its real constant. -/
theorem concentration_constant_positive_of_data [PseudoMetricSpace X]
    {μ : ProbabilityMeasure X} {constant : ℝ}
    (d : TransportationConcentrationData μ constant) :
    0 < constant :=
  d.constant_positive

/-- A terminal concentration-data package exposes the Lipschitz branch. -/
theorem lipschitz_concentration_of_data [PseudoMetricSpace X]
    {μ : ProbabilityMeasure X} {constant : ℝ}
    (d : TransportationConcentrationData μ constant) :
    LipschitzObservableTailBound μ constant :=
  d.lipschitz_observable_tail_bound

/-- A terminal concentration-data package exposes the set-enlargement branch. -/
theorem set_enlargement_concentration_of_data [PseudoMetricSpace X]
    {μ : ProbabilityMeasure X} {constant : ℝ}
    (d : TransportationConcentrationData μ constant) :
    SetEnlargementConcentrationBound μ constant :=
  d.set_enlargement_concentration_bound

omit [MeasurableSpace X] in
/-- The original set is contained in every nonnegative closed enlargement. -/
theorem subset_closedMetricEnlargement_of_nonneg [PseudoMetricSpace X]
    {r : ℝ} {s : Set X} (hr : 0 ≤ r) :
    s ⊆ closedMetricEnlargement (X := X) r s := by
  intro x hx
  exact ⟨x, hx, by simpa using hr⟩

/-- Pinned mathlib revision used for the Stage1 audit of this slot. -/
def mathlibRevision : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.InformationTheory.KullbackLeibler.Basic",
  "Mathlib.InformationTheory.KullbackLeibler.ChainRule",
  "Mathlib.MeasureTheory.Measure.Tilted",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.Prod",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.MeasureTheory.Measure.TightNormed",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Process.Basic",
  "Mathlib.Probability.Moments.Variance"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.IsProbabilityMeasure",
  "MeasureTheory.Measure.prod",
  "MeasureTheory.Measure.map_fst_prod",
  "MeasureTheory.Measure.map_snd_prod",
  "InformationTheory.klDiv",
  "InformationTheory.klDiv_self",
  "InformationTheory.klDiv_eq_zero_iff",
  "InformationTheory.klDiv_compProd_eq_add",
  "InformationTheory.klDiv_compProd_left",
  "MeasureTheory.Measure.compProd_const",
  "MeasureTheory.Measure.tilted",
  "MeasureTheory.tilted_absolutelyContinuous",
  "MeasureTheory.isProbabilityMeasure_tilted",
  "MeasureTheory.levyProkhorovEDist",
  "MeasureTheory.levyProkhorovDist",
  "MeasureTheory.IsTightMeasureSet",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.variance",
  "lintegral",
  "iInf"
]

/--
Search terms that did not locate a terminal transportation-inequality theorem
in pinned mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Wasserstein",
  "Talagrand",
  "transportation inequality",
  "Transportation",
  "OptimalTransport",
  "optimal transport",
  "T2 inequality",
  "concentration inequality",
  "transport cost",
  "set enlargement",
  "Donsker Varadhan",
  "entropy variational formula",
  "conditional KL integral chain rule"
]

/--
External Lean 4 search terms audited for `THM-M-1000.external-audit`.

These are metadata terms only.  The external audit found adjacent Lean 4
concentration and entropy-duality material, but no pinned/imported/checked
external `T_2` / Talagrand transportation-inequality closure in this
repository.
-/
def externalAuditSearchTerms : List String := [
  "Wasserstein",
  "Talagrand",
  "transportation inequality",
  "T2Inequality",
  "TalagrandT2",
  "OptimalTransport",
  "Concentration",
  "klDiv",
  "set enlargement"
]

/--
External-audit integration gate for this slot.

`false` means no external Lean 4 transportation-inequality dependency has been
entered into the local Lake closure and validated as a terminal theorem.
-/
def externalAuditRepoLocalGateClosed : Bool := false

/--
Structured integration-gate row for `THM-M-1000.integration-gate`.

This row is metadata for the Stage1 audit surface.  It records whether an
external Lean 4 transportation-inequality closure is already present in the
repo-local Lake validation closure, and whether any anchor-only evidence is
being counted as completed.
-/
structure IntegrationGateDecisionRow where
  task : String
  terminalExternalClosureFound : Bool
  pinnedImportedCheckedInRepo : Bool
  anchorOnlyCountedCompleted : Bool
  repoLocalIntegrationDebtStatus : String
  requiredActionBeforeCompletion : String

/--
Current integration-gate decision for the transportation-inequality slot.

No external `T_2` / Talagrand transportation-inequality Lean 4 proof has been
pinned, imported, and checked in this repository.  The slot therefore remains
open; if a terminal external closure is later found, it must be brought into
the local Lake closure or recorded with a concrete integration blocker before
any completion claim.
-/
def integrationGateDecisionRows : List IntegrationGateDecisionRow := [
  { task := "THM-M-1000.integration-gate",
    terminalExternalClosureFound := false,
    pinnedImportedCheckedInRepo := false,
    anchorOnlyCountedCompleted := false,
    repoLocalIntegrationDebtStatus :=
      "open_not_completed_no_terminal_external_closure_in_repo_local_lake_closure",
    requiredActionBeforeCompletion :=
      "If an external Lean 4 T2/Talagrand transportation-inequality closure is found, pin/import/check it in this repository or record the concrete integration blocker before any public completion claim." }
]

/-- The current integration-gate audit surface has exactly one decision row. -/
theorem integrationGateDecisionRows_length :
    integrationGateDecisionRows.length = 1 :=
  rfl

/--
Human-readable completion gate for public backfill.

This is intentionally an open gate, not a theorem proof and not a completion
claim for the transportation inequality.
-/
def integrationGateCompletionGate : String :=
  "open: no external Lean 4 T2/Talagrand transportation-inequality closure is pinned/imported/checked in this repository; do not count external_upstream_anchor_only evidence as completed"

/--
Structured public-status decision row for `THM-M-1000.public-status`.

The public checklist must remain open until one of the accepted repo-local
closure routes validates in this repository and the integration-debt gate has
no completed-state debt.
-/
structure PublicStatusDecisionRow where
  task : String
  publicStatusShouldRemainOpen : Bool
  localProofBodyValidated : Bool
  mathlibWrapperValidated : Bool
  pinnedExternalDependencyValidated : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  requiredClosureBeforeCompletion : String

/--
Current public-status decision for the transportation-inequality slot.

This metadata records the negative completion judgment only.  It does not
prove the transportation inequality and does not update public planning docs.
-/
def publicStatusDecisionRows : List PublicStatusDecisionRow := [
  { task := "THM-M-1000.public-status",
    publicStatusShouldRemainOpen := true,
    localProofBodyValidated := false,
    mathlibWrapperValidated := false,
    pinnedExternalDependencyValidated := false,
    completedStateRetainsRepoLocalIntegrationDebt := false,
    requiredClosureBeforeCompletion :=
      "Keep public status open until a local proof body, mathlib wrapper, or pinned external dependency validates in this repository, and no completed state retains repo_local_integration_debt." }
]

/-- The current public-status audit surface has exactly one decision row. -/
theorem publicStatusDecisionRows_length :
    publicStatusDecisionRows.length = 1 :=
  rfl

/--
Human-readable public status gate for serialized blueprint backfill.

The value is intentionally open/nonterminal.
-/
def publicStatusCompletionGate : String :=
  "open: THM-M-1000 has no repo-local terminal transportation-concentration proof body, no mathlib wrapper theorem, and no pinned/imported/checked external dependency in this repository; keep the public checklist item open"

/-! ## Audit probes -/

#check TransportPlan
#check independentPlan
#check TransportCost
#check OptimalTransportCost
#check squaredDistCost
#check TransportCostAPIRoute
#check selectedTransportCostAPIRoute
#check selectedTransportCostAPIRoute_eq
#check WassersteinSquaredBridgeTarget
#check selectedTransportCostAPIPublicDecision
#check EntropyBranchRoute
#check selectedEntropyBranchRoute
#check selectedEntropyBranchRoute_eq
#check KLCompProdChainRuleTarget
#check KLCompProdLeftTensorizationTarget
#check klDiv_compProd_chainRule_anchor
#check klDiv_compProd_left_tensorization_anchor
#check klDiv_prod_right_same_probability
#check EntropyVariationalFormulaTarget
#check entropyBranchRepoLocalGateClosed
#check TalagrandT2Inequality
#check upperLipschitzTailEvent
#check lowerLipschitzTailEvent
#check t2ConcentrationExponentialBound
#check LipschitzObservableTailBound
#check closedMetricEnlargement
#check SetEnlargementConcentrationBound
#check TransportationConcentrationData
#check StatementShape
#check statementShape_iff
#check StatementNormalizationDecisionRow
#check statementNormalizationDecisionRows
#check statementNormalizationDecisionRows_length
#check optimalTransportCost_le_plan
#check klDiv_self_probability
#check talagrandT2_of_data
#check concentration_constant_positive_of_data
#check lipschitz_concentration_of_data
#check set_enlargement_concentration_of_data
#check subset_closedMetricEnlargement_of_nonneg
#check mathlibRevision
#check MeasureTheory.ProbabilityMeasure
#check MeasureTheory.IsProbabilityMeasure
#check MeasureTheory.IsTightMeasureSet
#check MeasureTheory.levyProkhorovEDist
#check InformationTheory.klDiv
#check InformationTheory.klDiv_self
#check InformationTheory.klDiv_compProd_eq_add
#check InformationTheory.klDiv_compProd_left
#check Measure.compProd_const
#check Measure.tilted
#check tilted_absolutelyContinuous
#check isProbabilityMeasure_tilted
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.IndepFun
#check Measure.map_fst_prod
#check Measure.map_snd_prod
#check externalAuditSearchTerms
#check externalAuditRepoLocalGateClosed
#check IntegrationGateDecisionRow
#check integrationGateDecisionRows
#check integrationGateDecisionRows_length
#check integrationGateCompletionGate
#check PublicStatusDecisionRow
#check publicStatusDecisionRows
#check publicStatusDecisionRows_length
#check publicStatusCompletionGate

end AwesomeTheorems.Stage1.S1_M_280
