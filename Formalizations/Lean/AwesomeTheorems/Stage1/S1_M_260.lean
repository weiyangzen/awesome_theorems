import Mathlib.MeasureTheory.Measure.Tight
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Measure.Prokhorov

/-!
# S1-M-260 / THM-M-1011: Prohorov theorem

This Stage1 artifact records the Lean 4 boundary for Prohorov's theorem for
families of probability measures.

The pinned mathlib snapshot contains the weak-convergence topology on
`ProbabilityMeasure`, the Levy-Prokhorov metric infrastructure, the tightness
predicate `MeasureTheory.IsTightMeasureSet`, and checked theorems in both
Prohorov directions:

* relatively compact closure of a family of probability measures implies
  tightness of the corresponding set of measures.
* tightness of a family of probability measures implies compactness of its
  closure, with `T2Space` and `BorelSpace` assumptions.

The canonical Stage1 statement shape still records the weaker
`OpensMeasurableSpace` assumption boundary.  The checked full wrapper below uses
the stronger `BorelSpace` variant, matching the pinned mathlib theorem.
-/

noncomputable section

open MeasureTheory Set Topology
open scoped ENNReal Topology ProbabilityMeasure

namespace AwesomeTheorems.Stage1.S1_M_260

universe u

variable {X : Type u} [MeasurableSpace X]

/-- Coerce a family of probability measures to the corresponding set of measures. -/
def ProbabilityFamilyMeasures (S : Set (ProbabilityMeasure X)) : Set (Measure X) :=
  {μ | ∃ P ∈ S, (P : Measure X) = μ}

/-- View a family of probability measures in the Levy-Prokhorov metric type synonym. -/
def LevyProkhorovProbabilityFamily (S : Set (ProbabilityMeasure X)) :
    Set (LevyProkhorov (ProbabilityMeasure X)) :=
  LevyProkhorov.ofMeasure '' S

/-- Tightness of a family of probability measures, using mathlib's measure-set predicate. -/
def ProbabilityFamilyTight [TopologicalSpace X] (S : Set (ProbabilityMeasure X)) : Prop :=
  IsTightMeasureSet (ProbabilityFamilyMeasures S)

/--
Relative compactness of a family of probability measures for mathlib's weak
convergence topology on `ProbabilityMeasure X`.
-/
def RelativelyCompactProbabilityFamily [TopologicalSpace X] [OpensMeasurableSpace X]
    (S : Set (ProbabilityMeasure X)) : Prop :=
  IsCompact (closure S)

/--
Normalized Stage1 statement shape for Prohorov's theorem.

For a complete second-countable pseudo-metric measurable space, a family of
probability measures is tight iff its closure is compact in the topology of
weak convergence.  This is the formal target; only the compact-closure-to-tight
direction is currently discharged by pinned mathlib below.
-/
def StatementShape
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [OpensMeasurableSpace X]
    [SecondCountableTopology X] [CompleteSpace X] : Prop :=
  ∀ S : Set (ProbabilityMeasure X),
    ProbabilityFamilyTight S ↔ RelativelyCompactProbabilityFamily S

/--
Stronger Borel-space variant of the Stage1 statement shape.

`BorelSpace X` implies `OpensMeasurableSpace X`, so this variant is retained
only to make the assumption-freezing decision explicit: the canonical Stage1
target above uses `OpensMeasurableSpace`; future work may switch to this
stricter variant only if a downstream theorem needs equality with the Borel
measurable space, not merely measurability of open sets.
-/
def StatementShapeWithBorel
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] : Prop :=
  StatementShape X

/-- The statement shape unfolds to the tightness/relative-compactness equivalence. -/
theorem statementShape_iff
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [OpensMeasurableSpace X]
    [SecondCountableTopology X] [CompleteSpace X] :
    StatementShape X ↔
      ∀ S : Set (ProbabilityMeasure X),
        ProbabilityFamilyTight S ↔ RelativelyCompactProbabilityFamily S :=
  Iff.rfl

/-- `BorelSpace` supplies the weaker open-set measurability assumption. -/
theorem borelSpace_supplies_opensMeasurableSpace
    (X : Type u) [TopologicalSpace X] [MeasurableSpace X] [BorelSpace X] :
    OpensMeasurableSpace X :=
  inferInstance

/--
The Borel-space variant is definitionally the canonical `OpensMeasurableSpace`
statement when the stronger assumption is present.
-/
theorem statementShapeWithBorel_iff_statementShape
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] :
    StatementShapeWithBorel X ↔ StatementShape X :=
  Iff.rfl

/--
Checked mathlib wrapper for the compact-closure-to-tight direction of Prohorov's
theorem.
-/
theorem compactClosure_tight_mathlib_wrapper
    [PseudoMetricSpace X] [OpensMeasurableSpace X] [SecondCountableTopology X]
    [CompleteSpace X] {S : Set (ProbabilityMeasure X)}
    (hS : RelativelyCompactProbabilityFamily S) :
    ProbabilityFamilyTight S :=
  isTightMeasureSet_of_isCompact_closure (S := S) hS

/--
Stage1 bridge target for PROH-U002: tightness implies compactness of the closure
of a family of probability measures in the Levy-Prokhorov/weak topology.

The pinned mathlib theorem proves this under `T2Space` and `BorelSpace`; this
metric-specialized wrapper is the version needed by the usual Prohorov theorem
assumptions on `LevyProkhorov (ProbabilityMeasure X)`.
-/
def LevyProkhorovTightToPrecompactnessBridge
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] [T2Space X] : Prop :=
  ∀ S : Set (ProbabilityMeasure X),
    ProbabilityFamilyTight S → RelativelyCompactProbabilityFamily S

/--
Checked mathlib wrapper for the tightness-to-precompactness bridge.

This pins `MeasureTheory.isCompact_closure_of_isTightMeasureSet` locally for the
probability-measure family notation used by this Stage1 artifact.
-/
theorem tight_precompactness_bridge_mathlib_wrapper
    [TopologicalSpace X] [T2Space X] [BorelSpace X] {S : Set (ProbabilityMeasure X)}
    (hS : ProbabilityFamilyTight S) :
    RelativelyCompactProbabilityFamily S :=
  isCompact_closure_of_isTightMeasureSet (S := S) hS

/--
Metric-specialized PROH-U002 wrapper for `LevyProkhorov (ProbabilityMeasure X)`.
-/
theorem levyProkhorov_tight_precompactness_bridge_mathlib_wrapper
    [PseudoMetricSpace X] [BorelSpace X] [SecondCountableTopology X] [CompleteSpace X]
    [T2Space X] :
    LevyProkhorovTightToPrecompactnessBridge X := by
  intro S hS
  exact tight_precompactness_bridge_mathlib_wrapper (S := S) hS

/--
Stage1 bridge target for PROH-U003: the finite partition/net construction
should turn tightness of a family of probability measures into total
boundedness in the Levy-Prokhorov metric.

The direct combinatorial construction is not exposed as a standalone mathlib
lemma in the pinned snapshot, so this proposition records the checked endpoint
that such a construction must provide.
-/
def LevyProkhorovTightFiniteNetConstruction
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] [T2Space X] : Prop :=
  ∀ S : Set (ProbabilityMeasure X),
    ProbabilityFamilyTight S → TotallyBounded (LevyProkhorovProbabilityFamily S)

/--
Checked PROH-U003 endpoint: tight probability-measure families are totally
bounded in the Levy-Prokhorov metric.

This is repo-locally validated through the pinned mathlib Prokhorov compactness
theorem plus `IsCompact.totallyBounded`; it does not claim that the direct
finite partition construction itself has been isolated as a local proof body.
-/
theorem levyProkhorov_tight_totallyBounded_mathlib_wrapper
    [PseudoMetricSpace X] [BorelSpace X] [SecondCountableTopology X] [CompleteSpace X]
    [T2Space X] :
    LevyProkhorovTightFiniteNetConstruction X := by
  intro S hS
  have hcomp : IsCompact (closure S) :=
    tight_precompactness_bridge_mathlib_wrapper (S := S) hS
  have hcompLP : IsCompact
      ((LevyProkhorov.probabilityMeasureHomeomorph (Ω := X)) '' closure S) :=
    hcomp.image (LevyProkhorov.probabilityMeasureHomeomorph (Ω := X)).continuous
  refine hcompLP.totallyBounded.subset ?_
  intro μ hμ
  rcases hμ with ⟨P, hP, rfl⟩
  exact ⟨P, subset_closure hP, rfl⟩

/--
Finite-net form of the checked PROH-U003 endpoint.

For every positive Levy-Prokhorov radius, a tight family of probability
measures is covered by finitely many metric balls.  This is the public theorem
shape expected from the partition/net construction.
-/
theorem levyProkhorov_tight_finiteNet_mathlib_wrapper
    [PseudoMetricSpace X] [BorelSpace X] [SecondCountableTopology X] [CompleteSpace X]
    [T2Space X] {S : Set (ProbabilityMeasure X)}
    (hS : ProbabilityFamilyTight S) :
    ∀ ε : ℝ, 0 < ε →
      ∃ T : Set (LevyProkhorov (ProbabilityMeasure X)), T.Finite ∧
        LevyProkhorovProbabilityFamily S ⊆ ⋃ y ∈ T, Metric.ball y ε := by
  exact Metric.totallyBounded_iff.1
    (levyProkhorov_tight_totallyBounded_mathlib_wrapper (S := S) hS)

/--
Stage1 target for PROH-U004: compactness of the weak closure of a tight family
of probability measures.

The topology on `ProbabilityMeasure X` is mathlib's weak-convergence topology;
therefore the weak closure of `S` is the ordinary `closure S` in this type.
-/
def TightFamilyWeakClosureCompactness
    (X : Type u) [MeasurableSpace X] [TopologicalSpace X] [BorelSpace X]
    [T2Space X] : Prop :=
  ∀ S : Set (ProbabilityMeasure X),
    ProbabilityFamilyTight S → IsCompact (closure S)

/--
Checked PROH-U004 wrapper: a tight family of probability measures has compact
weak closure.

This is the direct public anchor for the compactness-of-weak-closure child task,
with proof body supplied by pinned mathlib theorem
`MeasureTheory.isCompact_closure_of_isTightMeasureSet`.
-/
theorem tight_weakClosure_compact_mathlib_wrapper
    [TopologicalSpace X] [BorelSpace X] [T2Space X] :
    TightFamilyWeakClosureCompactness X := by
  intro S hS
  exact isCompact_closure_of_isTightMeasureSet (S := S) hS

/--
The PROH-U004 weak-closure compactness target is the compactness statement
underlying the PROH-U002 tightness-to-precompactness bridge.
-/
theorem tight_weakClosure_compact_eq_precompactness_bridge
    [TopologicalSpace X] [BorelSpace X] [T2Space X] {S : Set (ProbabilityMeasure X)}
    (hS : ProbabilityFamilyTight S) :
    RelativelyCompactProbabilityFamily S :=
  tight_weakClosure_compact_mathlib_wrapper (S := S) hS

/--
The stronger Borel-space Stage1 statement is fully discharged by pinned mathlib:
`Prokhorov.lean` supplies tightness-to-compact-closure, while `Tight.lean`
supplies compact-closure-to-tightness.
-/
theorem statementShapeWithBorel_mathlib_wrapper
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] [T2Space X] :
    StatementShapeWithBorel X := by
  intro S
  constructor
  · intro hS
    exact tight_precompactness_bridge_mathlib_wrapper (S := S) hS
  · intro hS
    exact compactClosure_tight_mathlib_wrapper (S := S) hS

/-- Tightness unfolds to the compact-set complement estimate used by mathlib. -/
theorem tight_iff_exists_compact_measure_compl_le
    [TopologicalSpace X] (S : Set (ProbabilityMeasure X)) :
    ProbabilityFamilyTight S ↔
      ∀ ε : ℝ≥0∞, 0 < ε →
        ∃ K : Set X, IsCompact K ∧
          ∀ μ ∈ ProbabilityFamilyMeasures S, μ (Kᶜ) ≤ ε := by
  exact isTightMeasureSet_iff_exists_isCompact_measure_compl_le

/-- In a compact state space, every family of probability measures is tight. -/
theorem compactSpace_probabilityFamily_tight
    [TopologicalSpace X] [CompactSpace X] (S : Set (ProbabilityMeasure X)) :
    ProbabilityFamilyTight S :=
  IsTightMeasureSet.of_compactSpace

/-! ## PROH-U005 weak-convergence bridge audit -/

/--
PROH-U005 Portmanteau bridge: weak convergence implies the closed-set limsup
inequality.

This is the exact direction used when a weak limit must preserve upper bounds on
closed or compact complements.
-/
theorem portmanteau_tendsto_closed_limsup_bridge
    [TopologicalSpace X] [OpensMeasurableSpace X] [HasOuterApproxClosed X]
    {ι : Type*} {L : Filter ι} {μ : ProbabilityMeasure X}
    {μs : ι → ProbabilityMeasure X} (hμs : Filter.Tendsto μs L (𝓝 μ))
    {F : Set X} (hF : IsClosed F) :
    (L.limsup fun i ↦ (μs i : Measure X) F) ≤ (μ : Measure X) F :=
  ProbabilityMeasure.limsup_measure_closed_le_of_tendsto hμs hF

/--
PROH-U005 Portmanteau bridge: weak convergence implies the open-set liminf
inequality.
-/
theorem portmanteau_tendsto_open_liminf_bridge
    [TopologicalSpace X] [OpensMeasurableSpace X] [HasOuterApproxClosed X]
    {ι : Type*} {L : Filter ι} {μ : ProbabilityMeasure X}
    {μs : ι → ProbabilityMeasure X} (hμs : Filter.Tendsto μs L (𝓝 μ))
    {G : Set X} (hG : IsOpen G) :
    (μ : Measure X) G ≤ L.liminf fun i ↦ (μs i : Measure X) G :=
  ProbabilityMeasure.le_liminf_measure_open_of_tendsto hμs hG

/--
PROH-U005 Portmanteau converse bridge: open-set liminf inequalities imply weak
convergence of probability measures.
-/
theorem portmanteau_open_liminf_weakConvergence_bridge
    [TopologicalSpace X] [OpensMeasurableSpace X]
    {ι : Type*} {L : Filter ι} [L.IsCountablyGenerated]
    {μ : ProbabilityMeasure X} {μs : ι → ProbabilityMeasure X}
    (h : ∀ G : Set X, IsOpen G → μ G ≤ L.liminf fun i ↦ μs i G) :
    Filter.Tendsto μs L (𝓝 μ) :=
  tendsto_of_forall_isOpen_le_liminf h

/--
PROH-U005 Portmanteau converse bridge: closed-set limsup inequalities imply
weak convergence of probability measures.
-/
theorem portmanteau_closed_limsup_weakConvergence_bridge
    [TopologicalSpace X] [OpensMeasurableSpace X]
    {ι : Type*} {L : Filter ι} [L.IsCountablyGenerated]
    {μ : ProbabilityMeasure X} {μs : ι → ProbabilityMeasure X}
    (h : ∀ F : Set X, IsClosed F → L.limsup (fun i ↦ μs i F) ≤ μ F) :
    Filter.Tendsto μs L (𝓝 μ) :=
  tendsto_of_forall_isClosed_limsup_le h

/--
PROH-U005 Portmanteau bridge: weak convergence gives convergence on all
continuity sets of the limit probability measure.
-/
theorem portmanteau_tendsto_nullFrontier_bridge
    [TopologicalSpace X] [OpensMeasurableSpace X] [HasOuterApproxClosed X]
    {ι : Type*} {L : Filter ι} {μ : ProbabilityMeasure X}
    {μs : ι → ProbabilityMeasure X} (hμs : Filter.Tendsto μs L (𝓝 μ))
    {E : Set X} (hE : μ (frontier E) = 0) :
    Filter.Tendsto (fun i ↦ μs i E) L (𝓝 (μ E)) :=
  ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto hμs hE

/--
PROH-U005 Levy-Prokhorov bridge: on separable pseudometric spaces, the
Levy-Prokhorov topology on probability measures is exactly mathlib's weak
convergence topology.
-/
theorem levyProkhorov_weakTopology_eq_bridge
    [PseudoMetricSpace X] [OpensMeasurableSpace X] [TopologicalSpace.SeparableSpace X] :
    (inferInstance : TopologicalSpace (ProbabilityMeasure X)) =
      TopologicalSpace.coinduced LevyProkhorov.toMeasure inferInstance :=
  LevyProkhorov.eq_convergenceInDistribution (Ω := X)

/--
PROH-U005 homeomorphism bridge between weak probability measures and the
Levy-Prokhorov metric type synonym.
-/
noncomputable def levyProkhorovWeakConvergenceHomeomorph
    [PseudoMetricSpace X] [OpensMeasurableSpace X] [TopologicalSpace.SeparableSpace X] :
    ProbabilityMeasure X ≃ₜ LevyProkhorov (ProbabilityMeasure X) :=
  LevyProkhorov.probabilityMeasureHomeomorph (Ω := X)

/--
Compact record for the PROH-U005 audit of `Portmanteau.lean` and
`LevyProkhorovMetric.lean`.
-/
structure C005WeakConvergenceBridgeAuditLeaf where
  id : String
  sourceModule : String
  declaration : String
  role : String
  status : String
  localStepBudget : ℕ
deriving Repr, DecidableEq

/-- Checked PROH-U005 weak-convergence bridge audit leaves. -/
def c005WeakConvergenceBridgeAuditLeaves :
    List C005WeakConvergenceBridgeAuditLeaf := [
  { id := "PROH-U005-L001",
    sourceModule := "Mathlib.MeasureTheory.Measure.Portmanteau",
    declaration := "MeasureTheory.ProbabilityMeasure.limsup_measure_closed_le_of_tendsto",
    role := "weak convergence implies the closed-set limsup Portmanteau inequality",
    status := "checked local wrapper: portmanteau_tendsto_closed_limsup_bridge",
    localStepBudget := 6 },
  { id := "PROH-U005-L002",
    sourceModule := "Mathlib.MeasureTheory.Measure.Portmanteau",
    declaration := "MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto",
    role := "weak convergence implies the open-set liminf Portmanteau inequality",
    status := "checked local wrapper: portmanteau_tendsto_open_liminf_bridge",
    localStepBudget := 6 },
  { id := "PROH-U005-L003",
    sourceModule := "Mathlib.MeasureTheory.Measure.Portmanteau",
    declaration := "MeasureTheory.tendsto_of_forall_isOpen_le_liminf",
    role := "open-set liminf inequalities imply weak convergence",
    status := "checked local wrapper: portmanteau_open_liminf_weakConvergence_bridge",
    localStepBudget := 6 },
  { id := "PROH-U005-L004",
    sourceModule := "Mathlib.MeasureTheory.Measure.Portmanteau",
    declaration := "MeasureTheory.tendsto_of_forall_isClosed_limsup_le",
    role := "closed-set limsup inequalities imply weak convergence",
    status := "checked local wrapper: portmanteau_closed_limsup_weakConvergence_bridge",
    localStepBudget := 6 },
  { id := "PROH-U005-L005",
    sourceModule := "Mathlib.MeasureTheory.Measure.Portmanteau",
    declaration := "MeasureTheory.ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto",
    role := "weak convergence implies convergence on limit continuity sets",
    status := "checked local wrapper: portmanteau_tendsto_nullFrontier_bridge",
    localStepBudget := 6 },
  { id := "PROH-U005-L006",
    sourceModule := "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
    declaration := "MeasureTheory.LevyProkhorov.eq_convergenceInDistribution",
    role := "Levy-Prokhorov topology equals weak convergence topology",
    status := "checked local wrapper: levyProkhorov_weakTopology_eq_bridge",
    localStepBudget := 5 },
  { id := "PROH-U005-L007",
    sourceModule := "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
    declaration := "MeasureTheory.LevyProkhorov.probabilityMeasureHomeomorph",
    role := "homeomorphism between weak probability measures and the Levy-Prokhorov metric synonym",
    status := "checked local definition: levyProkhorovWeakConvergenceHomeomorph",
    localStepBudget := 4 },
  { id := "PROH-U005-L008",
    sourceModule := "Mathlib.MeasureTheory.Measure.Prokhorov",
    declaration := "MeasureTheory.isTightMeasureSet_of_isCompact_closure",
    role := "converse Prohorov direction consumes compactness in the weak topology",
    status := "already checked local wrapper: compactClosure_tight_mathlib_wrapper",
    localStepBudget := 5 }
]

/-- PROH-U005 audit leaf count. -/
theorem c005WeakConvergenceBridgeAuditLeaves_length :
    c005WeakConvergenceBridgeAuditLeaves.length = 8 :=
  rfl

/-- PROH-U005 budget gate: every audit leaf is within the M0387 local budget. -/
theorem c005EveryWeakConvergenceBridgeAuditLeafWithinBudget :
    c005WeakConvergenceBridgeAuditLeaves.all (fun leaf => leaf.localStepBudget ≤ 100) = true :=
  rfl

/--
PROH-U005 is an audit child, not a new terminal theorem-completion claim for the
canonical `OpensMeasurableSpace` statement shape.
-/
def c005TerminalStatementShapeCompleted : Bool :=
  false

/-- Checked non-completion gate for PROH-U005. -/
theorem c005TerminalStatementShapeCompleted_eq_false :
    c005TerminalStatementShapeCompleted = false :=
  rfl

/-- The full statement shape would supply the currently missing tight-to-compact direction. -/
theorem tight_compactClosure_of_statementShape
    [PseudoMetricSpace X] [OpensMeasurableSpace X] [SecondCountableTopology X]
    [CompleteSpace X] (h : StatementShape X) {S : Set (ProbabilityMeasure X)}
    (hS : ProbabilityFamilyTight S) :
    RelativelyCompactProbabilityFamily S :=
  (h S).1 hS

/-- The full statement shape also contains the mathlib-dischargeable compact-to-tight direction. -/
theorem compactClosure_tight_of_statementShape
    [PseudoMetricSpace X] [OpensMeasurableSpace X] [SecondCountableTopology X]
    [CompleteSpace X] (h : StatementShape X) {S : Set (ProbabilityMeasure X)}
    (hS : RelativelyCompactProbabilityFamily S) :
    ProbabilityFamilyTight S :=
  (h S).2 hS

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.MeasureTheory.Measure.TightNormed",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Measure.RegularityCompacts"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
  "MeasureTheory.ProbabilityMeasure.continuous_lintegral_boundedContinuousFunction",
  "MeasureTheory.ProbabilityMeasure.continuous_integral_boundedContinuousFunction",
  "MeasureTheory.ProbabilityMeasure.limsup_measure_closed_le_of_tendsto",
  "MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto",
  "MeasureTheory.ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto",
  "MeasureTheory.tendsto_of_forall_isOpen_le_liminf",
  "MeasureTheory.tendsto_of_forall_isClosed_limsup_le",
  "MeasureTheory.levyProkhorovEDist",
  "MeasureTheory.levyProkhorovDist",
  "MeasureTheory.LevyProkhorov.continuous_toMeasure_probabilityMeasure",
  "MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure",
  "MeasureTheory.LevyProkhorov.levyProkhorovDist_metricSpace_probabilityMeasure",
  "MeasureTheory.LevyProkhorov.eq_convergenceInDistribution",
  "MeasureTheory.LevyProkhorov.probabilityMeasureHomeomorph",
  "MeasureTheory.IsTightMeasureSet",
  "MeasureTheory.isTightMeasureSet_iff_exists_isCompact_measure_compl_le",
  "MeasureTheory.isTightMeasureSet_singleton_of_innerRegular",
  "MeasureTheory.isTightMeasureSet_singleton",
  "MeasureTheory.IsTightMeasureSet.of_compactSpace",
  "MeasureTheory.IsTightMeasureSet.map",
  "MeasureTheory.isTightMeasureSet_of_isCompact_closure",
  "MeasureTheory.isCompact_setOf_probabilityMeasure_mass_eq_compl_isCompact_le",
  "MeasureTheory.isCompact_closure_of_isTightMeasureSet",
  "Topology.IsCompact.totallyBounded",
  "Metric.totallyBounded_iff"
]

/--
Search terms used while locating the terminal tight-to-relative-compactness
Prohorov theorem in pinned local mathlib.
-/
def prohorovTerminalSearchTerms : List String := [
  "Prohorov",
  "Prokhorov",
  "tight iff compact",
  "tightness relative compact",
  "relatively compact probability measure",
  "compactness of tight probability measures",
  "IsTightMeasureSet_of",
  "isCompact_closure_of_isTightMeasureSet",
  "TotallyBounded probability measures",
  "Metric.totallyBounded_iff"
]

/-! ## PROH-U008 external-proof integration gate -/

/--
PROH-U008/C006 integration status.

The terminal Borel-space Prohorov statement used by this artifact is not an
anchor-only external citation: the proof body is in the pinned mathlib
dependency, the module is imported above, and the local wrapper
`statementShapeWithBorel_mathlib_wrapper` is checked by this file.
-/
def c006ProhorovIntegrationStatus : String :=
  "local_wrapper_upstream_mathlib via Mathlib.MeasureTheory.Measure.Prokhorov"

/--
PROH-U008/C006 checked wrapper for the pinned mathlib Prohorov closure gate.
-/
theorem c006_statementShapeWithBorel_pinned_mathlib_wrapper
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] [T2Space X] :
    StatementShapeWithBorel X :=
  statementShapeWithBorel_mathlib_wrapper X

/-- PROH-U008/C006 repo-local integration-debt gate. -/
def c006RepoLocalIntegrationDebtRetained : Bool :=
  false

/--
Checked C006 gate: this file does not retain completed-state
`repo_local_integration_debt`; the proof is pinned/imported/checked through
mathlib and local wrappers.
-/
theorem c006RepoLocalIntegrationDebtRetained_eq_false :
    c006RepoLocalIntegrationDebtRetained = false :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check ProbabilityFamilyMeasures
#check ProbabilityFamilyTight
#check RelativelyCompactProbabilityFamily
#check StatementShape
#check StatementShapeWithBorel
#check statementShape_iff
#check borelSpace_supplies_opensMeasurableSpace
#check statementShapeWithBorel_iff_statementShape
#check compactClosure_tight_mathlib_wrapper
#check LevyProkhorovTightToPrecompactnessBridge
#check tight_precompactness_bridge_mathlib_wrapper
#check levyProkhorov_tight_precompactness_bridge_mathlib_wrapper
#check LevyProkhorovTightFiniteNetConstruction
#check levyProkhorov_tight_totallyBounded_mathlib_wrapper
#check levyProkhorov_tight_finiteNet_mathlib_wrapper
#check TightFamilyWeakClosureCompactness
#check tight_weakClosure_compact_mathlib_wrapper
#check tight_weakClosure_compact_eq_precompactness_bridge
#check statementShapeWithBorel_mathlib_wrapper
#check tight_iff_exists_compact_measure_compl_le
#check compactSpace_probabilityFamily_tight
#check portmanteau_tendsto_closed_limsup_bridge
#check portmanteau_tendsto_open_liminf_bridge
#check portmanteau_open_liminf_weakConvergence_bridge
#check portmanteau_closed_limsup_weakConvergence_bridge
#check portmanteau_tendsto_nullFrontier_bridge
#check levyProkhorov_weakTopology_eq_bridge
#check levyProkhorovWeakConvergenceHomeomorph
#check C005WeakConvergenceBridgeAuditLeaf
#check c005WeakConvergenceBridgeAuditLeaves
#check c005WeakConvergenceBridgeAuditLeaves_length
#check c005EveryWeakConvergenceBridgeAuditLeafWithinBudget
#check c005TerminalStatementShapeCompleted_eq_false
#check tight_compactClosure_of_statementShape
#check compactClosure_tight_of_statementShape
#check c006ProhorovIntegrationStatus
#check c006_statementShapeWithBorel_pinned_mathlib_wrapper
#check c006RepoLocalIntegrationDebtRetained_eq_false
#check ProbabilityMeasure
#check ProbabilityMeasure.tendsto_iff_forall_integral_tendsto
#check ProbabilityMeasure.continuous_integral_boundedContinuousFunction
#check ProbabilityMeasure.limsup_measure_closed_le_of_tendsto
#check ProbabilityMeasure.le_liminf_measure_open_of_tendsto
#check ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto
#check tendsto_of_forall_isOpen_le_liminf
#check tendsto_of_forall_isClosed_limsup_le
#check levyProkhorovEDist
#check levyProkhorovDist
#check LevyProkhorov.continuous_toMeasure_probabilityMeasure
#check LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure
#check LevyProkhorov.levyProkhorovDist_metricSpace_probabilityMeasure
#check LevyProkhorov.eq_convergenceInDistribution
#check LevyProkhorov.probabilityMeasureHomeomorph
#check IsTightMeasureSet
#check isTightMeasureSet_iff_exists_isCompact_measure_compl_le
#check IsTightMeasureSet.of_compactSpace
#check IsTightMeasureSet.map
#check isTightMeasureSet_of_isCompact_closure
#check isCompact_setOf_probabilityMeasure_mass_eq_compl_isCompact_le
#check isCompact_closure_of_isTightMeasureSet
#check IsCompact.totallyBounded
#check Metric.totallyBounded_iff

end AwesomeTheorems.Stage1.S1_M_260
