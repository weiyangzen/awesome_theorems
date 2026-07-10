import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Topology.Basic

/-!
# S1-M-262 / THM-M-0982: Continuity of probability

This Stage1 file records a Lean 4 statement shape for the standard continuity
properties of a probability measure:

* continuity from below for increasing events,
* continuity from above for decreasing null-measurable events.

The proof body is a local wrapper around pinned mathlib measure-continuity
theorems and introduces no kernel-trusted assumptions.
-/

noncomputable section

open Filter MeasureTheory Set Topology
open scoped Topology

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_262

/--
Continuity from below for probability measures, expressed as convergence of
the event probabilities along an increasing sequence.
-/
def ContinuityFromBelowStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ℕ → Set Ω),
      Monotone A →
        Tendsto (fun n : ℕ => P (A n)) atTop (𝓝 (P (⋃ n, A n)))

/--
Continuity from above for probability measures, expressed as convergence of
the event probabilities along a decreasing sequence.  The measurability
hypothesis is represented by `NullMeasurableSet`, matching the mathlib theorem
used below.
-/
def ContinuityFromAboveStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ℕ → Set Ω),
      (∀ n : ℕ, NullMeasurableSet (A n) P) →
        Antitone A →
          Tendsto (fun n : ℕ => P (A n)) atTop (𝓝 (P (⋂ n, A n)))

/--
Normalized Stage1 statement-shape candidate for probability continuity.

This shape covers the standard monotone sequence forms over arbitrary
probability spaces.  It is proved below by wrappers around pinned mathlib.
-/
def StatementShape : Prop :=
  ContinuityFromBelowStatement.{u} ∧ ContinuityFromAboveStatement.{u}

/-- Checked mathlib wrapper: continuity from below for a probability measure. -/
theorem continuityFromBelow_mathlib
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ℕ → Set Ω) (hA : Monotone A) :
    Tendsto (fun n : ℕ => P (A n)) atTop (𝓝 (P (⋃ n, A n))) := by
  simpa [Function.comp_def] using
    (tendsto_measure_iUnion_atTop (μ := P) hA)

/-- Checked mathlib wrapper: continuity from above for a probability measure. -/
theorem continuityFromAbove_mathlib
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ℕ → Set Ω) (hAmeas : ∀ n : ℕ, NullMeasurableSet (A n) P)
    (hA : Antitone A) :
    Tendsto (fun n : ℕ => P (A n)) atTop (𝓝 (P (⋂ n, A n))) := by
  refine tendsto_measure_iInter_atTop (μ := P) hAmeas hA ?_
  exact ⟨0, ne_top_of_le_ne_top (by simp) (measure_mono (subset_univ (A 0)))⟩

/--
Checked wrapper for the common event version of continuity from above, with
ordinary measurability hypotheses.
-/
theorem continuityFromAbove_measurable_mathlib
    {Ω : Type u} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (A : ℕ → Set Ω) (hAmeas : ∀ n : ℕ, MeasurableSet (A n))
    (hA : Antitone A) :
    Tendsto (fun n : ℕ => P (A n)) atTop (𝓝 (P (⋂ n, A n))) := by
  exact continuityFromAbove_mathlib P A (fun n => (hAmeas n).nullMeasurableSet) hA

/-- Local wrapper closing the normalized Stage1 statement shape from mathlib. -/
theorem statementShape_mathlib : StatementShape.{u} := by
  constructor
  · intro Ω _ P _ A hA
    exact continuityFromBelow_mathlib P A hA
  · intro Ω _ P _ A hAmeas hA
    exact continuityFromAbove_mathlib P A hAmeas hA

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check continuityFromBelow_mathlib
#check continuityFromAbove_mathlib
#check continuityFromAbove_measurable_mathlib
#check statementShape_mathlib
#check MeasureTheory.IsProbabilityMeasure
#check tendsto_measure_iUnion_atTop
#check tendsto_measure_iInter_atTop
#check Monotone.measure_iUnion
#check Antitone.measure_iInter
#check MeasureTheory.ProbabilityMeasure.tendsto_measure_iUnion_accumulate

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.MeasureSpace",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.FiniteMeasure",
  "Mathlib.Probability.ProductMeasure",
  "Mathlib.Probability.Kernel.Disintegration.CondCDF",
  "Mathlib.Probability.Kernel.Disintegration.Density"
]

/-- Pinned mathlib theorem names wrapped or audited for this Stage1 artifact. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.tendsto_measure_iUnion_atTop",
  "MeasureTheory.tendsto_measure_iInter_atTop",
  "Monotone.measure_iUnion",
  "Antitone.measure_iInter",
  "MeasurableSet.nullMeasurableSet",
  "Directed.measure_iUnion",
  "Directed.measure_iInter",
  "MeasureTheory.ProbabilityMeasure.tendsto_measure_iUnion_accumulate",
  "MeasureTheory.FiniteMeasure.tendsto_measure_iUnion_accumulate"
]

/--
Integration-ready public anchor rows for the Stage1 blueprint backfill.

Each row records `(mathlib revision, module or declaration, role)`.
-/
def publicAnchorRows : List (String × String × String) := [
  ("8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "Mathlib.MeasureTheory.Measure.MeasureSpace",
    "mathlib module containing the measure-continuity API anchors"),
  ("8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "MeasureTheory.tendsto_measure_iUnion_atTop",
    "continuity from below wrapper source"),
  ("8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "MeasureTheory.tendsto_measure_iInter_atTop",
    "continuity from above wrapper source"),
  ("8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "Monotone.measure_iUnion",
    "monotone union measure identity anchor"),
  ("8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "Antitone.measure_iInter",
    "antitone intersection measure identity anchor")
]

/--
Integration-ready theorem-tree package split for the serialized public
blueprint backfill.
-/
def publicTheoremTreePackages : List String := [
  "M0982-P01.statement_normalization | checked | Fix universe, measurable space, probability measure, event sequence, monotonicity hypotheses, measurability hypotheses, and Tendsto conclusions",
  "M0982-P02.mathlib_object_model | checked | Audit Measure, IsProbabilityMeasure, NullMeasurableSet, monotone/antitone families, and ENNReal-valued measure convergence",
  "M0982-P03.continuity_from_below | checked | Wrap tendsto_measure_iUnion_atTop for increasing event sequences",
  "M0982-P04.continuity_from_above | checked | Wrap tendsto_measure_iInter_atTop for decreasing event sequences and discharge the finite-measure side condition from probability mass",
  "M0982-P05.event_measurability_bridge | checked | Provide the ordinary MeasurableSet wrapper through MeasurableSet.nullMeasurableSet",
  "M0982-P06.repo_local_wrapper_gate | checked | Close StatementShape by combining the checked below-continuity and above-continuity wrappers",
  "M0982-P07.public_merge_back | unchecked | Public blueprint/todo/README merge-back remains outside this worker write scope"
]

/--
Integration-ready local leaf-budget ledger for the public theorem-tree
backfill.  Only the public merge-back leaves are intentionally unchecked.
-/
def publicLeafBudgetRows : List String := [
  "M0982-L001 | M0982-P01 | <=100 | checked | Universe and measurable-space variables normalized in Lean",
  "M0982-L002 | M0982-P01 | <=100 | checked | Probability measure represented as (P : Measure Omega) [IsProbabilityMeasure P]",
  "M0982-L003 | M0982-P01 | <=100 | checked | Increasing event sequence and below-continuity target encoded in ContinuityFromBelowStatement",
  "M0982-L004 | M0982-P01 | <=100 | checked | Decreasing event sequence and above-continuity target encoded in ContinuityFromAboveStatement",
  "M0982-L005 | M0982-P02 | <=100 | checked | IsProbabilityMeasure, NullMeasurableSet, and monotone/antitone APIs are imported and probed",
  "M0982-L006 | M0982-P03 | <=100 | checked | continuityFromBelow_mathlib wraps tendsto_measure_iUnion_atTop",
  "M0982-L007 | M0982-P04 | <=100 | checked | continuityFromAbove_mathlib wraps tendsto_measure_iInter_atTop",
  "M0982-L008 | M0982-P04 | <=100 | checked | Finite-measure side condition for continuity from above discharged from probability mass",
  "M0982-L009 | M0982-P05 | <=100 | checked | continuityFromAbove_measurable_mathlib bridges MeasurableSet events to null-measurable events",
  "M0982-L010 | M0982-P06 | <=100 | checked | statementShape_mathlib closes the normalized StatementShape",
  "M0982-L011 | M0982-P06 | <=100 | checked | File-level validation command exits with code 0",
  "M0982-L012 | M0982-P07 | <=100 | unchecked | Public Docs/Stage1_Blueprint.md theorem-tree merge-back is outside this worker write scope",
  "M0982-L013 | M0982-P07 | <=100 | unchecked | Public todo/README consistency sync is outside this worker write scope"
]

/-- The only unchecked public merge-back leaves for this split. -/
def publicUncheckedLeaves : List String := [
  "M0982-L012",
  "M0982-L013"
]

/--
Search terms used in the pinned local mathlib tree for the anchor audit.
-/
def mathlibAuditSearchTerms : List String := [
  "continuity from below",
  "continuity from above",
  "tendsto_measure_iUnion_atTop",
  "tendsto_measure_iInter_atTop",
  "Monotone.measure_iUnion",
  "Antitone.measure_iInter",
  "ProbabilityMeasure.tendsto_measure_iUnion_accumulate",
  "measure_iUnion",
  "measure_iInter"
]

/--
Primary-source pin for the mathlib proof body used by this local wrapper.
-/
def mathlibPrimarySource : String :=
  "https://github.com/leanprover-community/mathlib4, revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"

#check publicAnchorRows
#check publicTheoremTreePackages
#check publicLeafBudgetRows
#check publicUncheckedLeaves

end S1_M_262
end Stage1
end AwesomeTheorems
