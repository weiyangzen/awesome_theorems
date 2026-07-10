import Mathlib.Probability.HasLaw
import Mathlib.Probability.IdentDistrib
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Constructions.Polish.Basic

/-!
# S1-M-290 / THM-M-1010: Skorokhod representation theorem

This Stage1 file records a Lean 4 statement shape for the Skorokhod
representation theorem: weak convergence of probability measures on a Polish
space should have a common probability-space realization with almost-sure
pointwise convergence.

The local artifact is not a proof of Skorokhod representation.  It gives a
kernel-checked formal boundary and small wrappers around pinned mathlib's
probability-law and weak-convergence APIs, without adding placeholder proof
terms or new trusted assumptions.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Topology
open scoped ENNReal NNReal Topology ProbabilityTheory

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_290

/--
Weak convergence of probability measures, using mathlib's topology on
`ProbabilityMeasure E`.
-/
def WeakConvergenceShape {E : Type u} [TopologicalSpace E] [MeasurableSpace E]
    [BorelSpace E] (μs : ℕ → ProbabilityMeasure E) (μ : ProbabilityMeasure E) : Prop :=
  Tendsto μs atTop (𝓝 μ)

/--
Data promised by the Skorokhod representation theorem for a sequence of laws
`μs` weakly converging to `μ`.

The fields freeze the intended formal boundary:
* a common probability space,
* random variables with the prescribed laws,
* almost-sure convergence of the representing variables.
-/
structure SkorokhodRepresentationData
    (E : Type u) [TopologicalSpace E] [MeasurableSpace E]
    (μs : ℕ → ProbabilityMeasure E) (μ : ProbabilityMeasure E) : Type (u + 1) where
  sample : Type u
  sampleMeasurable : MeasurableSpace sample
  probability : Measure sample
  isProbability : IsProbabilityMeasure probability
  seqVar : ℕ → sample → E
  limitVar : sample → E
  seq_hasLaw : ∀ n : ℕ, HasLaw (seqVar n) (μs n : Measure E) probability
  limit_hasLaw : HasLaw limitVar (μ : Measure E) probability
  ae_tendsto :
    ∀ᵐ ω ∂probability, Tendsto (fun n : ℕ => seqVar n ω) atTop (𝓝 (limitVar ω))

attribute [instance] SkorokhodRepresentationData.sampleMeasurable
attribute [instance] SkorokhodRepresentationData.isProbability

/--
Normalized Stage1 statement-shape candidate.

For every Polish target space and every weakly convergent sequence of
probability measures, there should be representation data realizing the
sequence and limit on one probability space with almost-sure convergence.
-/
def StatementShape
    (E : Type u) [TopologicalSpace E] [MeasurableSpace E] [BorelSpace E]
    [PolishSpace E] : Prop :=
  ∀ (μs : ℕ → ProbabilityMeasure E) (μ : ProbabilityMeasure E),
    WeakConvergenceShape μs μ → Nonempty (SkorokhodRepresentationData E μs μ)

/-- Definitional expansion of the normalized statement shape. -/
theorem statementShape_iff
    (E : Type u) [TopologicalSpace E] [MeasurableSpace E] [BorelSpace E]
    [PolishSpace E] :
    StatementShape E ↔
      ∀ (μs : ℕ → ProbabilityMeasure E) (μ : ProbabilityMeasure E),
        WeakConvergenceShape μs μ → Nonempty (SkorokhodRepresentationData E μs μ) :=
  Iff.rfl

/--
Public Stage1 boundary alias for `S1-M-290-A01`.

This theorem is intentionally just the checked statement-shape expansion.  It
does not prove the Skorokhod representation theorem; it gives the serial
public-doc integrator a stable repo-local Lean name for the boundary consisting
of `StatementShape`, `WeakConvergenceShape`, and `SkorokhodRepresentationData`.
-/
theorem publicStage1Boundary_iff
    (E : Type u) [TopologicalSpace E] [MeasurableSpace E] [BorelSpace E]
    [PolishSpace E] :
    StatementShape E ↔
      ∀ (μs : ℕ → ProbabilityMeasure E) (μ : ProbabilityMeasure E),
        WeakConvergenceShape μs μ → Nonempty (SkorokhodRepresentationData E μs μ) :=
  statementShape_iff E

/-- Mathlib wrapper: weak convergence is characterized by bounded continuous test integrals. -/
theorem weakConvergence_iff_testFunctions
    {E : Type u} [TopologicalSpace E] [MeasurableSpace E] [BorelSpace E]
    {μs : ℕ → ProbabilityMeasure E} {μ : ProbabilityMeasure E} :
    WeakConvergenceShape μs μ ↔
      ∀ f : BoundedContinuousFunction E ℝ,
        Tendsto (fun n : ℕ => ∫ x, f x ∂(μs n : Measure E)) atTop
          (𝓝 (∫ x, f x ∂(μ : Measure E))) := by
  exact ProbabilityMeasure.tendsto_iff_forall_integral_tendsto (F := atTop)

/-- Checked wrapper exposing the map equality contained in `HasLaw`. -/
theorem hasLaw_map_eq
    {Ω : Type u} {E : Type v} [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X : Ω → E} {μ : ProbabilityMeasure E}
    (hX : HasLaw X (μ : Measure E) P) :
    P.map X = (μ : Measure E) :=
  hX.map_eq

/-- Checked constructor wrapper for `HasLaw` from a.e. measurability and map equality. -/
theorem hasLaw_of_aemeasurable_map_eq
    {Ω : Type u} {E : Type v} [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X : Ω → E} {μ : ProbabilityMeasure E}
    (hX : AEMeasurable X P) (hmap : P.map X = (μ : Measure E)) :
    HasLaw X (μ : Measure E) P :=
  ⟨hX, hmap⟩

/-- A probability-measure push-forward has the expected `HasLaw` statement. -/
theorem hasLaw_probabilityMeasure_map
    {Ω : Type u} {E : Type v} [MeasurableSpace Ω] [MeasurableSpace E]
    (ν : ProbabilityMeasure Ω) {X : Ω → E}
    (hX : AEMeasurable X (ν : Measure Ω)) :
    HasLaw X (ProbabilityMeasure.map ν hX : Measure E) (ν : Measure Ω) := by
  exact ⟨hX, by simp⟩

/-- Two random variables with the same law are identically distributed. -/
theorem identDistrib_of_same_hasLaw
    {Ω Ω' : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace Ω'] [MeasurableSpace E]
    {P : Measure Ω} {P' : Measure Ω'} {X : Ω → E} {Y : Ω' → E}
    {μ : ProbabilityMeasure E}
    (hX : HasLaw X (μ : Measure E) P) (hY : HasLaw Y (μ : Measure E) P') :
    IdentDistrib X Y P P' :=
  hX.identDistrib hY

/-- The sequence variables in representation data have the requested laws. -/
theorem representation_seq_map_eq
    {E : Type u} [TopologicalSpace E] [MeasurableSpace E]
    {μs : ℕ → ProbabilityMeasure E} {μ : ProbabilityMeasure E}
    (D : SkorokhodRepresentationData E μs μ) (n : ℕ) :
    D.probability.map (D.seqVar n) = (μs n : Measure E) :=
  (D.seq_hasLaw n).map_eq

/-- The limit variable in representation data has the requested limit law. -/
theorem representation_limit_map_eq
    {E : Type u} [TopologicalSpace E] [MeasurableSpace E]
    {μs : ℕ → ProbabilityMeasure E} {μ : ProbabilityMeasure E}
    (D : SkorokhodRepresentationData E μs μ) :
    D.probability.map D.limitVar = (μ : Measure E) :=
  D.limit_hasLaw.map_eq

/-- The almost-sure convergence field of representation data as a standalone theorem. -/
theorem representation_ae_tendsto
    {E : Type u} [TopologicalSpace E] [MeasurableSpace E]
    {μs : ℕ → ProbabilityMeasure E} {μ : ProbabilityMeasure E}
    (D : SkorokhodRepresentationData E μs μ) :
    ∀ᵐ ω ∂D.probability,
      Tendsto (fun n : ℕ => D.seqVar n ω) atTop (𝓝 (D.limitVar ω)) :=
  D.ae_tendsto

/-! ## Audit probes retained in the checked file. -/

#check WeakConvergenceShape
#check SkorokhodRepresentationData
#check StatementShape
#check statementShape_iff
#check publicStage1Boundary_iff
#check weakConvergence_iff_testFunctions
#check hasLaw_map_eq
#check hasLaw_probabilityMeasure_map
#check identDistrib_of_same_hasLaw
#check representation_seq_map_eq
#check representation_limit_map_eq
#check representation_ae_tendsto
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.IdentDistrib
#check MeasureTheory.ProbabilityMeasure
#check MeasureTheory.ProbabilityMeasure.map
#check MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto
#check MeasureTheory.ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous
#check MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure
#check PolishSpace

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.HasLawExists",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Constructions.Polish.Basic"
]

/-- Pinned mathlib theorem and definition names wrapped or audited for this Stage1 artifact. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.map_eq",
  "ProbabilityTheory.HasLaw.aemeasurable",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.HasLaw.identDistrib",
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.ProbabilityMeasure.map",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
  "MeasureTheory.ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous",
  "MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure",
  "PolishSpace"
]

/-- A public, integration-ready row for `S1-M-290-A02` mathlib anchors. -/
structure MathlibAnchorRow where
  topic : String
  moduleName : String
  sourceFile : String
  declarationName : String
  checkedEvidence : String
  role : String
deriving Repr

/-- The pinned mathlib revision used for the `S1-M-290-A02` anchor audit. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Public mathlib anchor table for `S1-M-290-A02`.

These rows record substrate anchors for the Skorokhod representation statement
shape only. They do not prove the terminal Skorokhod representation theorem.
-/
def publicA02MathlibAnchorTable : List MathlibAnchorRow := [
  {
    topic := "random-variable law",
    moduleName := "Mathlib.Probability.HasLaw",
    sourceFile := "Mathlib/Probability/HasLaw.lean",
    declarationName := "ProbabilityTheory.HasLaw",
    checkedEvidence := "hasLaw_map_eq; hasLaw_of_aemeasurable_map_eq; hasLaw_probabilityMeasure_map",
    role := "records the law of each representing random variable as a push-forward equality"
  },
  {
    topic := "identical distribution",
    moduleName := "Mathlib.Probability.IdentDistrib",
    sourceFile := "Mathlib/Probability/IdentDistrib.lean",
    declarationName := "ProbabilityTheory.IdentDistrib",
    checkedEvidence := "identDistrib_of_same_hasLaw",
    role := "bridges same-law random variables to mathlib's identical-distribution interface"
  },
  {
    topic := "probability measures",
    moduleName := "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
    sourceFile := "Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean",
    declarationName := "MeasureTheory.ProbabilityMeasure",
    checkedEvidence := "WeakConvergenceShape; representation_seq_map_eq; representation_limit_map_eq",
    role := "provides the probability-law type and coercion to measures used by the statement"
  },
  {
    topic := "weak convergence tests",
    moduleName := "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
    sourceFile := "Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean",
    declarationName := "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
    checkedEvidence := "weakConvergence_iff_testFunctions",
    role := "characterizes weak convergence by bounded continuous test-function integrals"
  },
  {
    topic := "Polish target spaces",
    moduleName := "Mathlib.MeasureTheory.Constructions.Polish.Basic",
    sourceFile := "Mathlib/MeasureTheory/Constructions/Polish/Basic.lean",
    declarationName := "PolishSpace",
    checkedEvidence := "StatementShape; statementShape_iff; publicStage1Boundary_iff",
    role := "records the topological hypothesis for the Skorokhod representation target space"
  }
]

/-- Local search terms used in the pinned mathlib tree for the anchor audit. -/
def mathlibAuditSearchTerms : List String := [
  "Skorokhod",
  "Skorohod",
  "Skorokhod representation",
  "weak convergence almost sure",
  "almost sure representation",
  "HasLaw",
  "IdentDistrib",
  "ProbabilityMeasure.tendsto",
  "ConvergenceInDistribution",
  "LevyProkhorov",
  "PolishSpace"
]

/-- Primary-source pin for the mathlib APIs used by this local wrapper. -/
def mathlibPrimarySource : String :=
  "https://github.com/leanprover-community/mathlib4, revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Names forming the public Stage1 boundary for `S1-M-290-A01`. -/
def publicStage1BoundaryNames : List String := [
  "StatementShape",
  "WeakConvergenceShape",
  "SkorokhodRepresentationData",
  "publicStage1Boundary_iff"
]

/-- Current machine-proof debt class for the full Skorokhod representation theorem. -/
def machineProofDebt : String :=
  "formalization_debt"

/-- Current machine status for the full Skorokhod representation theorem. -/
def machineStatus : String :=
  "not_repo_local_closed"

/--
Public A08 status gate.

The checked statement boundary and substrate wrappers in this file are not a
proof of the Skorokhod representation theorem.  Until a full local proof body,
pinned mathlib wrapper, or pinned external Lean proof is imported and validated
in this repository, the terminal theorem remains open under
`formalization_debt` with machine status `not_repo_local_closed`.
-/
def publicA08StatusGate : String :=
  "keep THM-M-1010 as formalization_debt / not_repo_local_closed until the full local-or-pinned validation gate passes"

/-- A08 kernel check: the terminal proof debt remains formalization debt. -/
theorem machineProofDebt_eq_formalization_debt :
    machineProofDebt = "formalization_debt" :=
  rfl

/-- A08 kernel check: the terminal machine status is not repo-local closed. -/
theorem machineStatus_eq_not_repo_local_closed :
    machineStatus = "not_repo_local_closed" :=
  rfl

/-- Validation command proposed for the public `S1-M-290-A03` audit surface. -/
def publicA03ValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_290.lean"

/-- Historical pass date to backfill for `S1-M-290-A03`. -/
def publicA03HistoricalValidationDate : String :=
  "2026-04-30"

/-- Historical pass result to backfill for `S1-M-290-A03`; current runs must be recorded separately. -/
def publicA03HistoricalValidationResult : String :=
  "passed"

/-- A row in the public theorem-tree package split proposed for `S1-M-290-A04`. -/
structure SkorokhodPackageRow where
  packageId : String
  packageName : String
  responsibility : String
  upstreamInputs : List String
  downstreamOutput : String
  localLeanEvidence : List String
  status : String
deriving Repr

/-- Root node for the public theorem-tree package split of THM-M-1010. -/
def publicA04TheoremTreeRoot : String :=
  "SKOR.root: Skorokhod representation theorem for weak convergence of probability measures on Polish spaces"

/--
Integration-ready `SKOR.1` through `SKOR.6` package split for `S1-M-290-A04`.

The rows are theorem-tree planning metadata. They do not assert that the full
Skorokhod representation theorem has a repo-local Lean proof.
-/
def publicA04SkorokhodPackageSplit : List SkorokhodPackageRow := [
  {
    packageId := "SKOR.1",
    packageName := "statement_normalization",
    responsibility :=
      "Fix the Polish target type, Borel measurable structure, probability-measure sequence, weak-convergence hypothesis, common probability-space conclusion, prescribed-law fields, and almost-sure convergence field.",
    upstreamInputs := [
      "PolishSpace E",
      "BorelSpace E",
      "μs : ℕ → ProbabilityMeasure E",
      "μ : ProbabilityMeasure E"
    ],
    downstreamOutput :=
      "StatementShape E and Nonempty (SkorokhodRepresentationData E μs μ) as the normalized target.",
    localLeanEvidence := [
      "StatementShape",
      "WeakConvergenceShape",
      "SkorokhodRepresentationData",
      "statementShape_iff",
      "publicStage1Boundary_iff"
    ],
    status := "checked_statement_boundary_only; theorem proof remains open"
  },
  {
    packageId := "SKOR.2",
    packageName := "mathlib_object_model",
    responsibility :=
      "Bind the statement to mathlib objects for laws, identical distribution, probability measures, probability spaces, and almost-everywhere assertions.",
    upstreamInputs := [
      "ProbabilityTheory.HasLaw",
      "ProbabilityTheory.IdentDistrib",
      "MeasureTheory.ProbabilityMeasure",
      "MeasureTheory.IsProbabilityMeasure",
      "∀ᵐ"
    ],
    downstreamOutput :=
      "Reusable wrappers exposing prescribed laws and representation-data fields.",
    localLeanEvidence := [
      "hasLaw_map_eq",
      "hasLaw_of_aemeasurable_map_eq",
      "hasLaw_probabilityMeasure_map",
      "identDistrib_of_same_hasLaw",
      "representation_seq_map_eq",
      "representation_limit_map_eq",
      "representation_ae_tendsto"
    ],
    status := "checked_substrate_wrappers_only"
  },
  {
    packageId := "SKOR.3",
    packageName := "weak_convergence_interfaces",
    responsibility :=
      "Use the Levy-Prokhorov metricization route as the primary weak-convergence interface, with bounded-continuous test-function, portmanteau, and tightness APIs retained as supporting audits.",
    upstreamInputs := [
      "WeakConvergenceShape μs μ",
      "ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
      "LevyProkhorovMetric module",
      "Portmanteau and Tight modules",
      "no external coupling theorem unless a future proof is pinned/imported/checked"
    ],
    downstreamOutput :=
      "A metricized route from the weak-convergence hypothesis to quantitative estimates usable by the coupling package.",
    localLeanEvidence := [
      "weakConvergence_iff_testFunctions",
      "mathlibAnchorModules",
      "mathlibAnchorNames",
      "publicA02MathlibAnchorTable"
    ],
    status := "A07 route_selected_levy_prokhorov_primary; checked_interface_anchor_only; proof route not closed"
  },
  {
    packageId := "SKOR.4",
    packageName := "realization_existence",
    responsibility :=
      "Construct or import a common probability space and random variables whose laws are the sequence and limit probability measures.",
    upstreamInputs := [
      "HasLaw interface",
      "ProbabilityMeasure.map",
      "possible HasLawExists-style realization lemmas",
      "standard Borel or Polish target infrastructure"
    ],
    downstreamOutput :=
      "Candidate seqVar and limitVar fields for SkorokhodRepresentationData.",
    localLeanEvidence := [
      "SkorokhodRepresentationData.seqVar",
      "SkorokhodRepresentationData.limitVar",
      "SkorokhodRepresentationData.seq_hasLaw",
      "SkorokhodRepresentationData.limit_hasLaw"
    ],
    status := "unchecked_formalization_debt"
  },
  {
    packageId := "SKOR.5",
    packageName := "coupling_and_almost_sure_convergence",
    responsibility :=
      "Build Levy-Prokhorov-controlled couplings of the sequence and limit variables and turn summable metric-error bounds into almost-sure convergence.",
    upstreamInputs := [
      "weak-convergence estimates from SKOR.3",
      "realized variables from SKOR.4",
      "Levy-Prokhorov metric control",
      "Borel-Cantelli or summable-error branch",
      "portmanteau/tightness lemmas only as support, not the selected main route"
    ],
    downstreamOutput :=
      "The ae_tendsto field of SkorokhodRepresentationData.",
    localLeanEvidence := [
      "SkorokhodRepresentationData.ae_tendsto",
      "representation_ae_tendsto"
    ],
    status := "A07 route_selected_levy_prokhorov_primary; unchecked_formalization_debt"
  },
  {
    packageId := "SKOR.6",
    packageName := "integration_or_external_closure_gate",
    responsibility :=
      "Before any status upgrade, either close the theorem with a repo-local proof body, pin and check an upstream Lean proof, or record a concrete integration blocker.",
    upstreamInputs := [
      "fresh primary Lean 4 source search",
      "repo-local validation command",
      "placeholder-free declaration scan",
      "M0387 completion gates"
    ],
    downstreamOutput :=
      "A completed state only if local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned validation passes.",
    localLeanEvidence := [
      "machineProofDebt",
      "machineStatus",
      "publicA03ValidationCommand",
      "publicA03HistoricalValidationResult"
    ],
    status := "gate_open_not_repo_local_closed"
  }
]

/-! ## S1-M-290-A05 unchecked leaf ledger preservation. -/

/-- Status labels for the `SKOR-L001` through `SKOR-L022` leaf ledger. -/
inductive SkorokhodLeafStatus where
  | unchecked
  | checked
deriving DecidableEq, Repr

/--
Data-only row for the local Skorokhod leaf ledger.

The `independentLocalProofStepLedger` field is intentionally `false` for every
row below.  These rows preserve the public `SKOR-L001` through `SKOR-L022`
frontier and explicitly block promotion until a future child supplies an
independent `<=100` local proof-step ledger for the corresponding leaf.
-/
structure SkorokhodLeafLedgerRow where
  leafId : String
  packageId : String
  responsibility : String
  status : SkorokhodLeafStatus
  independentLocalProofStepLedger : Bool
  promotionGate : String
deriving Repr

/-- Canonical promotion gate for each unchecked Skorokhod leaf. -/
def skorokhodLeafPromotionGate : String :=
  "do not promote before an independent <=100 local proof-step ledger is validated"

/--
Preserved unchecked `SKOR-L001` through `SKOR-L022` ledger for `S1-M-290-A05`.

This is a planning/audit surface only.  It does not prove the Skorokhod
representation theorem and does not close any of the listed leaves.
-/
def publicA05UncheckedLeafLedger : List SkorokhodLeafLedgerRow := [
  {
    leafId := "SKOR-L001.statement.universes",
    packageId := "SKOR.1",
    responsibility :=
      "Freeze universe levels for target and sample spaces and avoid accidental Prop-only encoding.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L002.statement.polish-target",
    packageId := "SKOR.1",
    responsibility :=
      "Confirm whether mathlib's PolishSpace plus BorelSpace is the final source-level hypothesis or whether a standard-Borel variant is needed.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L003.statement.weak-convergence",
    packageId := "SKOR.1",
    responsibility :=
      "Verify that the topology on ProbabilityMeasure E matches textbook weak convergence.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L004.statement.common-space",
    packageId := "SKOR.1",
    responsibility :=
      "Choose the common probability-space construction and universe level.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L005.statement.prescribed-laws",
    packageId := "SKOR.1",
    responsibility :=
      "Represent laws with HasLaw rather than duplicate map-equality fields.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L006.statement.ae-convergence",
    packageId := "SKOR.1",
    responsibility :=
      "Confirm the almost-sure convergence field as an eventually-atTop Tendsto statement under ae quantification.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L007.mathlib.haslaw",
    packageId := "SKOR.2",
    responsibility :=
      "Expand HasLaw wrappers into the public theorem-level audit.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L008.mathlib.identdistrib",
    packageId := "SKOR.2",
    responsibility :=
      "Record same-law-to-identically-distributed bridges.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L009.mathlib.probabilitymeasure-topology",
    packageId := "SKOR.3",
    responsibility :=
      "Audit ProbabilityMeasure.tendsto_iff_forall_integral_tendsto as the weak-convergence interface.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L010.mathlib.levy-prokhorov",
    packageId := "SKOR.3",
    responsibility :=
      "Decide whether the proof route should use the Levy-Prokhorov metric.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L011.mathlib.portmanteau",
    packageId := "SKOR.3",
    responsibility :=
      "Audit portmanteau lemmas needed for weak-convergence consequences.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L012.mathlib.tightness",
    packageId := "SKOR.3",
    responsibility :=
      "Audit tightness and Prokhorov prerequisites.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L013.mathlib.polish",
    packageId := "SKOR.2",
    responsibility :=
      "Audit PolishSpace and standard-Borel support theorems.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L014.realization.prescribed-single-law",
    packageId := "SKOR.4",
    responsibility :=
      "Test whether HasLawExists gives needed single-law realizations under target hypotheses.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L015.realization.sequence-laws",
    packageId := "SKOR.4",
    responsibility :=
      "Construct all sequence variables on one space without assuming independence.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L016.coupling.finite-dimensional",
    packageId := "SKOR.5",
    responsibility :=
      "Define finite-dimensional couplings or transport kernels.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L017.coupling.projective-limit",
    packageId := "SKOR.5",
    responsibility :=
      "Choose a Kolmogorov or Ionescu-Tulcea style extension if needed.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L018.coupling.metric-control",
    packageId := "SKOR.5",
    responsibility :=
      "Encode the distance estimates that force almost-sure convergence.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L019.coupling.borel-cantelli",
    packageId := "SKOR.5",
    responsibility :=
      "Prove or import summable-error to almost-sure convergence if using a metric proof.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L020.final.assemble",
    packageId := "SKOR.6",
    responsibility :=
      "Assemble weak convergence into Nonempty SkorokhodRepresentationData.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L021.integration.external-search",
    packageId := "SKOR.6",
    responsibility :=
      "Rerun primary Lean 4 source search before any completion claim.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  },
  {
    leafId := "SKOR-L022.integration.pin-or-block",
    packageId := "SKOR.6",
    responsibility :=
      "If an external proof is found, either pin/import/check it or record a concrete incompatibility blocker.",
    status := .unchecked,
    independentLocalProofStepLedger := false,
    promotionGate := skorokhodLeafPromotionGate
  }
]

/-- The preserved A05 ledger contains exactly the `SKOR-L001` through `SKOR-L022` leaves. -/
theorem publicA05UncheckedLeafLedger_length :
    publicA05UncheckedLeafLedger.length = 22 :=
  rfl

/-- No preserved A05 leaf is marked checked in this artifact. -/
theorem publicA05UncheckedLeafLedger_statuses :
    publicA05UncheckedLeafLedger.map (fun row => row.status) =
      [.unchecked, .unchecked, .unchecked, .unchecked, .unchecked, .unchecked,
        .unchecked, .unchecked, .unchecked, .unchecked, .unchecked, .unchecked,
        .unchecked, .unchecked, .unchecked, .unchecked, .unchecked, .unchecked,
        .unchecked, .unchecked, .unchecked, .unchecked] :=
  rfl

/-- No preserved A05 leaf has an independent local proof-step ledger yet. -/
theorem publicA05UncheckedLeafLedger_noIndependentStepLedgers :
    publicA05UncheckedLeafLedger.map (fun row => row.independentLocalProofStepLedger) =
      [false, false, false, false, false, false, false, false, false, false,
        false, false, false, false, false, false, false, false, false, false,
        false, false] :=
  rfl

/-! ## S1-M-290-A06 fresh primary Lean 4 source-search audit. -/

/-- One row from the A06 primary Lean 4 source-search audit. -/
structure PrimaryLeanSourceSearchRow where
  source : String
  query : String
  date : String
  result : String
  terminalProofFound : Bool
  action : String
deriving Repr

/--
Fresh A06 source-search audit before any status upgrade.

These rows record primary Lean-source searches only.  No terminal Lean 4 proof
of the Skorokhod representation theorem was found, so no external proof is
available to pin, import, and check in this repo from this audit.
-/
def publicA06PrimaryLeanSourceSearch : List PrimaryLeanSourceSearchRow := [
  {
    source := "local pinned mathlib tree at revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
    query := "rg -n -i \"skorokhod|skorohod|skorokhod representation|almost sure representation\" Formalizations/Lean/.lake/packages/mathlib/Mathlib",
    date := "2026-05-01",
    result := "no matches in pinned mathlib; matches only occur in this repo-local Stage1 audit file when that file is included in the search",
    terminalProofFound := false,
    action := "no pin/import/check target exists from pinned mathlib"
  },
  {
    source := "local pinned Lake package tree",
    query := "find Formalizations/Lean/.lake/packages -path '*Skor*' -o -path '*skor*'",
    date := "2026-05-01",
    result := "no Skorokhod/Skorohod-named files or directories found",
    terminalProofFound := false,
    action := "no package-local external proof target exists"
  },
  {
    source := "Sourcegraph global code search",
    query := "context:global Skorokhod lang:Lean fork:yes archived:yes count:20",
    date := "2026-05-01",
    result := "zero matches returned by the search stream API",
    terminalProofFound := false,
    action := "no external Lean source to pin/import/check"
  },
  {
    source := "Sourcegraph global code search",
    query := "context:global Skorohod lang:Lean fork:yes archived:yes count:20",
    date := "2026-05-01",
    result := "zero matches returned by the search stream API",
    terminalProofFound := false,
    action := "no external Lean source to pin/import/check"
  },
  {
    source := "Sourcegraph global code search",
    query := "context:global \"Skorokhod representation\" fork:yes archived:yes count:20",
    date := "2026-05-01",
    result := "zero matches returned by the search stream API",
    terminalProofFound := false,
    action := "no external Lean source to pin/import/check"
  }
]

/-- The A06 audit rows did not find a terminal external Lean proof. -/
def publicA06ExternalProofFound : Bool :=
  false

/--
Concrete A06 integration gate.

Because no external Lean 4 proof was found in the fresh primary-source audit,
there is no proof object to pin/import/check and no short-term incompatibility
blocker to record.  The completion gate remains closed until a future audit
finds a proof and the repo either validates it locally or records a concrete
integration blocker.
-/
def publicA06IntegrationGate : String :=
  "no external Lean 4 Skorokhod representation proof found on 2026-05-01; keep formalization_debt/not_repo_local_closed until a proof is locally produced or a future external proof is pinned/imported/checked"

/-- The A06 source-search table records the five completed primary-source searches. -/
theorem publicA06PrimaryLeanSourceSearch_length :
    publicA06PrimaryLeanSourceSearch.length = 5 :=
  rfl

/-- No A06 search row found a terminal proof. -/
theorem publicA06PrimaryLeanSourceSearch_noTerminalProof :
    publicA06PrimaryLeanSourceSearch.map (fun row => row.terminalProofFound) =
      [false, false, false, false, false] :=
  rfl

/-! ## S1-M-290-A07 proof-route decision. -/

/-- Candidate main routes considered for the Skorokhod representation proof plan. -/
inductive SkorokhodProofRoute where
  | levyProkhorovMetricization
  | portmanteauTightness
  | externalCouplingTheorem
deriving DecidableEq, Repr

/-- One row explaining the A07 route decision. -/
structure SkorokhodRouteDecisionRow where
  route : SkorokhodProofRoute
  role : String
  decision : String
  reason : String
  packageImpact : String
deriving Repr

/--
Selected A07 main proof route.

The route is deliberately a planning decision, not a proof of Skorokhod
representation.  `LevyProkhorovMetric` is already a checked mathlib import in
this artifact, while the fresh A06 search found no external Lean proof to use
as the main closure route.
-/
def publicA07SelectedMainProofRoute : SkorokhodProofRoute :=
  .levyProkhorovMetricization

/-- Human-readable A07 selected-route label for public backfill. -/
def publicA07SelectedMainProofRouteLabel : String :=
  "Lévy-Prokhorov metricization primary; portmanteau/tightness support; no external-coupling theorem route without a future pinned proof"

/--
Integration-ready A07 route decision table.

This table records why the public theorem-tree split should route `SKOR.3`
through Levy-Prokhorov metricization and route `SKOR.5` through metric-error
coupling plus a summable-error/Borel-Cantelli branch.  It does not mark any
proof-carrying leaf as checked.
-/
def publicA07RouteDecisionTable : List SkorokhodRouteDecisionRow := [
  {
    route := .levyProkhorovMetricization,
    role := "primary route",
    decision := "selected",
    reason :=
      "mathlib exposes `Mathlib.MeasureTheory.Measure.LevyProkhorovMetric` and a checked `MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure` anchor in this artifact; the route gives metric estimates that naturally feed the coupling and almost-sure convergence package.",
    packageImpact :=
      "SKOR.3 becomes the Levy-Prokhorov metricization interface; SKOR.5 expects Levy-Prokhorov-controlled couplings and a summable-error-to-a.e.-convergence branch."
  },
  {
    route := .portmanteauTightness,
    role := "supporting route",
    decision := "not selected as the main route",
    reason :=
      "portmanteau and tightness remain important consequences and audit targets, but by themselves they do not provide the metric coupling estimates needed for the ae_tendsto field.",
    packageImpact :=
      "Keep portmanteau and tightness anchors under SKOR.3 as support for estimates and consistency checks; do not make them the terminal SKOR.5 construction route."
  },
  {
    route := .externalCouplingTheorem,
    role := "closure fallback",
    decision := "blocked unless a future proof is found and pinned/imported/checked",
    reason :=
      "the A06 primary Lean 4 source audit found no terminal Skorokhod representation proof, so no external coupling theorem is available for repo-local closure.",
    packageImpact :=
      "SKOR.6 must keep the pin/import/check gate open and must not claim completion from anchor-only external evidence."
  }
]

/-- The A07 decision table records exactly the three considered routes. -/
theorem publicA07RouteDecisionTable_length :
    publicA07RouteDecisionTable.length = 3 :=
  rfl

/-- The selected A07 route is Levy-Prokhorov metricization. -/
theorem publicA07SelectedMainProofRoute_eq :
    publicA07SelectedMainProofRoute = .levyProkhorovMetricization :=
  rfl

/-- The A07 table does not select the external coupling theorem route. -/
theorem publicA07ExternalCouplingRoute_notSelected :
    publicA07RouteDecisionTable.map (fun row => row.decision) =
      ["selected", "not selected as the main route",
        "blocked unless a future proof is found and pinned/imported/checked"] :=
  rfl

#check publicStage1BoundaryNames
#check MathlibAnchorRow
#check mathlibAnchorRevision
#check publicA02MathlibAnchorTable
#check machineProofDebt
#check machineStatus
#check publicA08StatusGate
#check machineProofDebt_eq_formalization_debt
#check machineStatus_eq_not_repo_local_closed
#check publicA03ValidationCommand
#check publicA03HistoricalValidationDate
#check publicA03HistoricalValidationResult
#check SkorokhodPackageRow
#check publicA04TheoremTreeRoot
#check publicA04SkorokhodPackageSplit
#check SkorokhodLeafLedgerRow
#check skorokhodLeafPromotionGate
#check publicA05UncheckedLeafLedger
#check publicA05UncheckedLeafLedger_length
#check publicA05UncheckedLeafLedger_statuses
#check publicA05UncheckedLeafLedger_noIndependentStepLedgers
#check PrimaryLeanSourceSearchRow
#check publicA06PrimaryLeanSourceSearch
#check publicA06ExternalProofFound
#check publicA06IntegrationGate
#check publicA06PrimaryLeanSourceSearch_length
#check publicA06PrimaryLeanSourceSearch_noTerminalProof
#check SkorokhodProofRoute
#check SkorokhodRouteDecisionRow
#check publicA07SelectedMainProofRoute
#check publicA07SelectedMainProofRouteLabel
#check publicA07RouteDecisionTable
#check publicA07RouteDecisionTable_length
#check publicA07SelectedMainProofRoute_eq
#check publicA07ExternalCouplingRoute_notSelected

end S1_M_290
end Stage1
end AwesomeTheorems
