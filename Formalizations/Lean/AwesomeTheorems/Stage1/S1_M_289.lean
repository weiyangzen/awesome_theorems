import Mathlib.Probability.BorelCantelli

/-!
# S1-M-289 / THM-M-1009: Erdos-Renyi second lemma

This Stage1 artifact records a conservative Lean 4 boundary for the
Erdos-Renyi/Kochen-Stone style extension of Borel-Cantelli.  The terminal
lower-bound theorem is kept as an explicit statement shape.  The checked
content below wraps the pinned mathlib Borel-Cantelli infrastructure:

* `ProbabilityTheory.measure_limsup_eq_one`, the independent second
  Borel-Cantelli lemma;
* `MeasureTheory.ae_mem_limsup_atTop_iff`, Levy's generalized
  Borel-Cantelli lemma for a filtration.

The file therefore records real repo-local anchors without claiming that
mathlib already closes the full Erdos-Renyi lower-bound theorem.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Set
open scoped ENNReal ProbabilityTheory Topology

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_289

/--
The partial sum of event probabilities, viewed as a real number.

The Erdos-Renyi lower-bound statement is traditionally written using real
finite sums of probabilities.  `Measure.real` gives a stable Lean boundary for
that form while avoiding a premature choice of an `ENNReal` division API.
-/
def partialEventMass {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) : ℝ :=
  ∑ k ∈ Finset.range n, μ.real (A k)

/--
The double finite sum of pairwise intersection probabilities.
-/
def pairwiseEventMass {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) : ℝ :=
  ∑ i ∈ Finset.range n, ∑ j ∈ Finset.range n, μ.real (A i ∩ A j)

/--
The finite-sum ratio appearing in the Erdos-Renyi/Kochen-Stone lower bound.

When the denominator is zero, Lean's field division returns `0`; the normalized
terminal statement also assumes divergence of the numerator partial sums, so a
future proof package should isolate the positivity/nonzero denominator leaf.
-/
def eventMassRatio {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) : ℝ :=
  (partialEventMass μ A n) ^ 2 / pairwiseEventMass μ A n

/--
Finite event-counting random variable `X_n = sum_{k < n} 1_{A_k}`.

This is the concrete random variable needed by the finite second-moment
package.  The current child only seeds the definition and elementary checked
facts; the expectation and second-moment identities remain explicit proof
tasks below.
-/
def eventCount {Ω : Type u} (A : ℕ → Set Ω) (n : ℕ) : Ω → ℝ :=
  fun ω => ∑ k ∈ Finset.range n, (A k).indicator (fun _ => (1 : ℝ)) ω

@[simp]
theorem eventCount_zero {Ω : Type u} (A : ℕ → Set Ω) (ω : Ω) :
    eventCount A 0 ω = 0 := by
  simp [eventCount]

/-- The finite event-counting random variable is pointwise nonnegative. -/
theorem eventCount_nonneg {Ω : Type u} (A : ℕ → Set Ω) (n : ℕ) (ω : Ω) :
    0 ≤ eventCount A n ω := by
  classical
  unfold eventCount
  exact Finset.sum_nonneg fun k _ => by
    by_cases hω : ω ∈ A k
    · simp [Set.indicator, hω]
    · simp [Set.indicator, hω]

/-- Squared event count used by the second-moment identity task. -/
def eventCountSquared {Ω : Type u} (A : ℕ → Set Ω) (n : ℕ) : Ω → ℝ :=
  fun ω => (eventCount A n ω) ^ 2

/--
Normalized lower-bound statement shape for the Erdos-Renyi second lemma.

For measurable events with divergent sum of probabilities, the probability of
the limsup event is bounded below by the limsup of the second-moment ratio.
This is the formalization boundary that remains open in this repository.
-/
def ErdosRenyiLowerBoundStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (A : ℕ → Set Ω),
      (∀ n : ℕ, MeasurableSet (A n)) →
        Tendsto (partialEventMass μ A) atTop atTop →
          Filter.limsup (eventMassRatio μ A) atTop ≤ μ.real (limsup A atTop)

/--
Common corollary-shaped statement: if the Erdos-Renyi ratio tends to one, then
the limsup event has full probability.

This is included as a separate candidate because some source traditions call
this full-probability consequence the "second lemma" and use the lower bound
as the proof engine.
-/
def ErdosRenyiFullProbabilityStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (A : ℕ → Set Ω),
      (∀ n : ℕ, MeasurableSet (A n)) →
        Tendsto (partialEventMass μ A) atTop atTop →
          Tendsto (eventMassRatio μ A) atTop (𝓝 1) →
            μ.real (limsup A atTop) = 1

/--
The public canonical statement choice selected for THM-M-1009.

The source label "Erdos-Renyi second lemma" is ambiguous in secondary use:
some references foreground the Kochen-Stone lower bound, while others state
the full-probability consequence obtained when the ratio tends to one.  The
safe Stage1 public surface should retain both, with the lower-bound theorem as
the primary proof target and the full-probability statement as a named
corollary target.
-/
inductive PublicCanonicalStatementChoice where
  | lowerBoundOnly
  | fullProbabilityOnly
  | lowerBoundAndFullProbability
  deriving DecidableEq, Repr

/-- Machine-readable record of the canonical statement decision for C001. -/
def publicCanonicalStatementChoice : PublicCanonicalStatementChoice :=
  PublicCanonicalStatementChoice.lowerBoundAndFullProbability

/--
Public canonical statement for this Stage1 slot: keep both the lower-bound
Erdos-Renyi/Kochen-Stone form and the full-probability consequence.
-/
def PublicCanonicalStatement : Prop :=
  ErdosRenyiLowerBoundStatement.{u} ∧ ErdosRenyiFullProbabilityStatement.{u}

/-- Human-facing rationale for the canonical statement decision. -/
def publicCanonicalStatementDecisionRationale : List String := [
  "choose both lower-bound and full-probability forms for the public canonical statement",
  "treat the lower-bound Erdos-Renyi/Kochen-Stone inequality as the primary proof target",
  "treat the full-probability consequence as a named corollary target derived from the lower bound plus ratio tending to one",
  "do not mark THM-M-1009 completed until the terminal lower-bound proof body or a pinned/imported/checked external proof validates locally"
]

/--
The repo-local Stage1 statement boundary for this slot.

It is intentionally a proposition-valued target, not a proof.  The checked
wrappers below are nearby machine anchors, not a closure of this conjunction.
-/
def StatementShape : Prop :=
  PublicCanonicalStatement.{u}

/-- The normalized statement unfolds to the two Erdos-Renyi candidate forms. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ErdosRenyiLowerBoundStatement.{u} ∧
        ErdosRenyiFullProbabilityStatement.{u} :=
  Iff.rfl

/-- The selected public canonical statement is exactly `StatementShape`. -/
theorem publicCanonicalStatement_iff_statementShape :
    PublicCanonicalStatement.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/--
The independent second Borel-Cantelli theorem as a closed mathlib statement.

This is a genuine repo-local wrapper around pinned mathlib.  It is weaker than
the Erdos-Renyi lower-bound target because it assumes independent events.
-/
def IndependentSecondBorelCantelliStatement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (μ : Measure Ω) (A : ℕ → Set Ω),
    (∀ n : ℕ, MeasurableSet (A n)) →
      iIndepSet A μ →
        (∑' n : ℕ, μ (A n)) = ∞ →
          μ (limsup A atTop) = 1

/-- Checked mathlib wrapper: the independent second Borel-Cantelli lemma. -/
theorem independentSecondBorelCantelli_mathlib :
    IndependentSecondBorelCantelliStatement.{u} := by
  intro Ω _ μ A hA hInd hsum
  exact ProbabilityTheory.measure_limsup_eq_one hA hInd hsum

/--
Checked mathlib wrapper: Levy's generalized Borel-Cantelli theorem for a
filtration.  This is the martingale/conditional-expectation anchor used by
mathlib to derive the independent second Borel-Cantelli lemma.
-/
theorem levyGeneralizedBorelCantelli_mathlib
    {Ω : Type u} {mΩ : MeasurableSpace Ω} {μ : Measure Ω} [IsFiniteMeasure μ]
    {ℱ : Filtration ℕ mΩ} {A : ℕ → Set Ω}
    (hA : ∀ n : ℕ, MeasurableSet[ℱ n] (A n)) :
    ∀ᵐ ω ∂μ, ω ∈ limsup A atTop ↔
      Tendsto (fun n => ∑ k ∈ Finset.range n,
        (μ[(A (k + 1)).indicator (1 : Ω → ℝ) | ℱ k]) ω) atTop atTop := by
  simpa using MeasureTheory.ae_mem_limsup_atTop_iff (ℱ := ℱ) μ hA

/-- Repo-local validation command for this Stage1 artifact. -/
def repoLocalValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_289.lean"

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check PublicCanonicalStatementChoice
#check publicCanonicalStatementChoice
#check PublicCanonicalStatement
#check publicCanonicalStatementDecisionRationale
#check ErdosRenyiLowerBoundStatement
#check ErdosRenyiFullProbabilityStatement
#check IndependentSecondBorelCantelliStatement
#check independentSecondBorelCantelli_mathlib
#check levyGeneralizedBorelCantelli_mathlib
#check ProbabilityTheory.measure_limsup_eq_one
#check MeasureTheory.ae_mem_limsup_atTop_iff
#check ProbabilityTheory.iIndepSet
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.condExp_natural_ae_eq_of_lt
#check ProbabilityTheory.iIndepSet.condExp_indicator_filtrationOfSet_ae_eq
#check MeasureTheory.measure_limsup_atTop_eq_zero
#check repoLocalValidationCommand

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.BorelCantelli",
  "Mathlib.Probability.Martingale.BorelCantelli",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.ZeroOne",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure"
]

/-- Pinned mathlib declaration names wrapped or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.measure_limsup_eq_one",
  "MeasureTheory.ae_mem_limsup_atTop_iff",
  "ProbabilityTheory.iIndepSet.condExp_indicator_filtrationOfSet_ae_eq",
  "ProbabilityTheory.iIndepFun.condExp_natural_ae_eq_of_lt",
  "ProbabilityTheory.iIndepSet",
  "ProbabilityTheory.iIndepFun",
  "MeasureTheory.measure_limsup_atTop_eq_zero",
  "MeasureTheory.Submartingale.bddAbove_iff_exists_tendsto",
  "MeasureTheory.Martingale.bddAbove_range_iff_bddBelow_range"
]

/-- Pinned mathlib revision used for the required C003 anchor audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Checked equality retaining the exact required mathlib pin in Lean. -/
theorem pinnedMathlibRevision_eq :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Source metadata for a pinned mathlib declaration used by this Stage1 slot. -/
structure PinnedMathlibAnchor where
  requestedName : String
  leanName : String
  moduleName : String
  sourceFile : String
  sourceLine : Nat
  sourceKind : String
  proofRole : String
  deriving Repr

/--
The exact pinned anchors requested by child task `S1-M-289-C003`.

These are real repo-local wrappers against the pinned mathlib dependency, but
they are Borel-Cantelli infrastructure only.  They do not close the terminal
Erdos-Renyi/Kochen-Stone lower-bound theorem in this repository.
-/
def requiredPinnedMathlibAnchors : List PinnedMathlibAnchor := [
  {
    requestedName := "ProbabilityTheory.measure_limsup_eq_one",
    leanName := "ProbabilityTheory.measure_limsup_eq_one",
    moduleName := "Mathlib.Probability.BorelCantelli",
    sourceFile := "Mathlib/Probability/BorelCantelli.lean",
    sourceLine := 69,
    sourceKind := "theorem",
    proofRole :=
      "independent second Borel-Cantelli wrapper used as a nearby checked anchor"
  },
  {
    requestedName := "MeasureTheory.ae_mem_limsup_atTop_iff",
    leanName := "MeasureTheory.ae_mem_limsup_atTop_iff",
    moduleName := "Mathlib.Probability.Martingale.BorelCantelli",
    sourceFile := "Mathlib/Probability/Martingale/BorelCantelli.lean",
    sourceLine := 341,
    sourceKind := "theorem",
    proofRole :=
      "Levy generalized Borel-Cantelli wrapper used by the mathlib proof path"
  }
]

/-- Number of exact pinned mathlib anchors required by C003 and recorded here. -/
def requiredPinnedMathlibAnchorCount : Nat :=
  requiredPinnedMathlibAnchors.length

/-- The C003 anchor audit records exactly the two requested mathlib anchors. -/
theorem requiredPinnedMathlibAnchorCount_eq :
    requiredPinnedMathlibAnchorCount = 2 :=
  rfl

#check pinnedMathlibRevision
#check pinnedMathlibRevision_eq
#check PinnedMathlibAnchor
#check requiredPinnedMathlibAnchors
#check requiredPinnedMathlibAnchorCount_eq

/-! ## C004 finite second-moment package split. -/

/--
C004-local status vocabulary for the `ER-L008` through `ER-L011` package.

`checkedEventCountSeed` means that this file contains a small checked local
definition/proof seed for the row.  It is not a completion marker for the row's
full proof obligation.
-/
inductive FiniteSecondMomentPackageStatus where
  | checkedEventCountSeed
  | uncheckedFormalizationDebt
  deriving DecidableEq, Repr

/-- One independently budgeted child proof task for the finite second-moment package. -/
structure FiniteSecondMomentProofTask where
  code : String
  title : String
  obligation : String
  localInterface : String
  upstreamInputs : String
  downstreamUse : String
  budgetStepLimit : Nat
  status : FiniteSecondMomentPackageStatus
  completionBoundary : String
  deriving Repr, DecidableEq

/-- M0387 local proof-leaf budget limit for C004 package rows. -/
def finiteSecondMomentLeafBudgetLimit : Nat :=
  100

/--
Integration-ready proof-task ledger for `ER-L008` through `ER-L011`.

The rows expose the finite second-moment package needed before the terminal
Erdos-Renyi lower-bound theorem can be attempted.  They are proof tasks, not
proof-completion claims.
-/
def finiteSecondMomentProofTasks : List FiniteSecondMomentProofTask := [
  {
    code := "ER-L008",
    title := "event-counting random variable package",
    obligation :=
      "Define X_n = sum_{k < n} 1_{A_k}; prove measurability, nonnegativity, and finite-integrability facts under measurable events and probability measure hypotheses.",
    localInterface :=
      "eventCount, eventCount_zero, eventCount_nonneg, eventCountSquared",
    upstreamInputs :=
      "Set.indicator, Finset finite sums, measurable indicator APIs, probability measure finiteness",
    downstreamUse :=
      "first-moment identity, second-moment identity, and nonzero-event support bridge",
    budgetStepLimit := finiteSecondMomentLeafBudgetLimit,
    status := .checkedEventCountSeed,
    completionBoundary :=
      "checked seed only: eventCount and nonnegativity validate locally, but measurability and integrability are still open"
  },
  {
    code := "ER-L009",
    title := "first-moment identity",
    obligation :=
      "Prove integral/event-count expectation identity: integral of X_n equals partialEventMass μ A n in real-valued form.",
    localInterface :=
      "target identity connecting eventCount and partialEventMass",
    upstreamInputs :=
      "integral_finset_sum, integral_indicator, measurable-set hypotheses, Measure.real bridge",
    downstreamUse :=
      "numerator normalization for the finite second-moment ratio",
    budgetStepLimit := finiteSecondMomentLeafBudgetLimit,
    status := .uncheckedFormalizationDebt,
    completionBoundary :=
      "unchecked formalization debt: no local proof body currently proves the first-moment identity"
  },
  {
    code := "ER-L010",
    title := "second-moment expansion",
    obligation :=
      "Prove integral/event-count-square identity: integral of X_n^2 equals pairwiseEventMass μ A n after expanding the finite square.",
    localInterface :=
      "target identity connecting eventCountSquared and pairwiseEventMass",
    upstreamInputs :=
      "Finset square expansion, indicator multiplication/intersection identity, integral finite sums, Measure.real bridge",
    downstreamUse :=
      "denominator normalization for the finite second-moment ratio",
    budgetStepLimit := finiteSecondMomentLeafBudgetLimit,
    status := .uncheckedFormalizationDebt,
    completionBoundary :=
      "unchecked formalization debt: no local proof body currently proves the second-moment expansion"
  },
  {
    code := "ER-L011",
    title := "finite second-moment lower bound",
    obligation :=
      "Prove the finite Cauchy-Schwarz/Paley-Zygmund bound that the probability of at least one of the first n events is bounded below by (E X_n)^2 / E X_n^2, with the zero-denominator case isolated.",
    localInterface :=
      "target finite lower bound feeding eventMassRatio",
    upstreamInputs :=
      "ER-L008 through ER-L010, Cauchy-Schwarz or Paley-Zygmund inequality, denominator positivity/nonzero package",
    downstreamUse :=
      "finite lower-bound step before passing to limsup in the terminal Erdos-Renyi theorem",
    budgetStepLimit := finiteSecondMomentLeafBudgetLimit,
    status := .uncheckedFormalizationDebt,
    completionBoundary :=
      "unchecked formalization debt: no local proof body currently proves the finite lower bound"
  }
]

/-- C004 records exactly the four requested finite second-moment proof tasks. -/
def finiteSecondMomentProofTaskCodes : List String :=
  finiteSecondMomentProofTasks.map (fun row => row.code)

/-- The C004 task-code list is exactly `ER-L008` through `ER-L011`. -/
theorem finiteSecondMomentProofTaskCodes_eq :
    finiteSecondMomentProofTaskCodes =
      ["ER-L008", "ER-L009", "ER-L010", "ER-L011"] := by
  native_decide

/-- The C004 proof-task split has exactly four rows. -/
theorem finiteSecondMomentProofTasks_length :
    finiteSecondMomentProofTasks.length = 4 := by
  native_decide

/-- Every C004 row is explicitly budgeted at the M0387 `<= 100` threshold. -/
theorem finiteSecondMomentProofTasks_all_le_100 :
    finiteSecondMomentProofTasks.all
      (fun row => row.budgetStepLimit ≤ finiteSecondMomentLeafBudgetLimit) = true := by
  native_decide

#check eventCount
#check eventCount_zero
#check eventCount_nonneg
#check eventCountSquared
#check FiniteSecondMomentPackageStatus
#check FiniteSecondMomentProofTask
#check finiteSecondMomentProofTasks
#check finiteSecondMomentProofTaskCodes_eq
#check finiteSecondMomentProofTasks_length
#check finiteSecondMomentProofTasks_all_le_100

/-! ## C005 denominator and real/ENNReal bridge package split. -/

/-- The partial sum of event probabilities in its native `ENNReal` measure form. -/
def partialEventMassENNReal {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) : ℝ≥0∞ :=
  ∑ k ∈ Finset.range n, μ (A k)

/-- The pairwise-intersection denominator in its native `ENNReal` measure form. -/
def pairwiseEventMassENNReal {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) : ℝ≥0∞ :=
  ∑ i ∈ Finset.range n, ∑ j ∈ Finset.range n, μ (A i ∩ A j)

/-- The real partial event-mass sum is nonnegative. -/
theorem partialEventMass_nonneg {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) :
    0 ≤ partialEventMass μ A n := by
  unfold partialEventMass
  exact Finset.sum_nonneg fun _ _ => measureReal_nonneg

/-- The real pairwise-intersection denominator is nonnegative. -/
theorem pairwiseEventMass_nonneg {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) :
    0 ≤ pairwiseEventMass μ A n := by
  unfold pairwiseEventMass
  exact Finset.sum_nonneg fun _ _ =>
    Finset.sum_nonneg fun _ _ => measureReal_nonneg

/--
If the numerator partial mass is positive, then the finite pairwise
denominator is positive because the double sum contains all diagonal terms.
-/
theorem pairwiseEventMass_pos_of_partialEventMass_pos {Ω : Type u}
    [MeasurableSpace Ω] (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ)
    (h : 0 < partialEventMass μ A n) :
    0 < pairwiseEventMass μ A n := by
  classical
  unfold partialEventMass at h
  rcases (Finset.sum_pos_iff_of_nonneg
    (fun _ _ => measureReal_nonneg)).1 h with ⟨i, hi, hAi⟩
  unfold pairwiseEventMass
  refine Finset.sum_pos' (fun _ _ =>
    Finset.sum_nonneg fun _ _ => measureReal_nonneg) ⟨i, hi, ?_⟩
  refine Finset.sum_pos' (fun _ _ => measureReal_nonneg) ⟨i, hi, ?_⟩
  simpa [Set.inter_self] using hAi

/-- Positive partial event mass gives a nonzero finite pairwise denominator. -/
theorem pairwiseEventMass_ne_zero_of_partialEventMass_pos {Ω : Type u}
    [MeasurableSpace Ω] (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ)
    (h : 0 < partialEventMass μ A n) :
    pairwiseEventMass μ A n ≠ 0 :=
  (pairwiseEventMass_pos_of_partialEventMass_pos μ A n h).ne'

/-- The finite Erdos-Renyi ratio is nonnegative in the real encoding. -/
theorem eventMassRatio_nonneg {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) (A : ℕ → Set Ω) (n : ℕ) :
    0 ≤ eventMassRatio μ A n := by
  unfold eventMassRatio
  exact div_nonneg (sq_nonneg _) (pairwiseEventMass_nonneg μ A n)

/--
Finite bridge from the real partial mass to the native `ENNReal` finite sum.

The finite-measure hypothesis is exactly the condition needed by
`ofReal_measureReal`; probability measures satisfy it.
-/
theorem ofReal_partialEventMass {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (A : ℕ → Set Ω) (n : ℕ) :
    ENNReal.ofReal (partialEventMass μ A n) =
      partialEventMassENNReal μ A n := by
  unfold partialEventMass partialEventMassENNReal
  rw [ENNReal.ofReal_sum_of_nonneg]
  · refine Finset.sum_congr rfl ?_
    intro k _
    exact ofReal_measureReal (μ := μ) (s := A k)
  · intro k _
    exact measureReal_nonneg

/--
Finite bridge from the real pairwise denominator to the native `ENNReal`
finite double sum.
-/
theorem ofReal_pairwiseEventMass {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (A : ℕ → Set Ω) (n : ℕ) :
    ENNReal.ofReal (pairwiseEventMass μ A n) =
      pairwiseEventMassENNReal μ A n := by
  unfold pairwiseEventMass pairwiseEventMassENNReal
  rw [ENNReal.ofReal_sum_of_nonneg]
  · refine Finset.sum_congr rfl ?_
    intro i _
    rw [ENNReal.ofReal_sum_of_nonneg]
    · refine Finset.sum_congr rfl ?_
      intro j _
      exact ofReal_measureReal (μ := μ) (s := A i ∩ A j)
    · intro j _
      exact measureReal_nonneg
  · intro i _
    exact Finset.sum_nonneg fun j _ => measureReal_nonneg

/--
C005-local status vocabulary for denominator and real/`ENNReal` bridge rows.

`checkedLocalLemmaSeed` means this file now has a closed lemma useful for the
row.  It is not a completion marker for the terminal Erdos-Renyi lower bound.
-/
inductive DenominatorBridgePackageStatus where
  | checkedLocalLemmaSeed
  | uncheckedFormalizationDebt
  deriving DecidableEq, Repr

/-- One independently budgeted child proof task for the denominator/bridge package. -/
structure DenominatorBridgeProofTask where
  code : String
  title : String
  obligation : String
  localInterface : String
  upstreamInputs : String
  downstreamUse : String
  budgetStepLimit : Nat
  status : DenominatorBridgePackageStatus
  completionBoundary : String
  deriving Repr, DecidableEq

/-- M0387 local proof-leaf budget limit for C005 denominator/bridge rows. -/
def denominatorBridgeLeafBudgetLimit : Nat :=
  100

/--
Integration-ready proof-task ledger for denominator positivity/nonzero and
real/`ENNReal` bridge work before the terminal lower-bound theorem.
-/
def denominatorBridgeProofTasks : List DenominatorBridgeProofTask := [
  {
    code := "ER-L012",
    title := "finite denominator nonnegativity and nonzero criterion",
    obligation :=
      "Prove nonnegativity of partialEventMass and pairwiseEventMass, and isolate a usable nonzero denominator criterion before any division-sensitive lower-bound step.",
    localInterface :=
      "partialEventMass_nonneg, pairwiseEventMass_nonneg, pairwiseEventMass_pos_of_partialEventMass_pos, pairwiseEventMass_ne_zero_of_partialEventMass_pos",
    upstreamInputs :=
      "measureReal_nonneg, finite sums of nonnegative terms, diagonal terms A_i ∩ A_i = A_i",
    downstreamUse :=
      "zero-denominator branch of ER-L011 and the terminal finite-ratio-to-limsup passage",
    budgetStepLimit := denominatorBridgeLeafBudgetLimit,
    status := .checkedLocalLemmaSeed,
    completionBoundary :=
      "checked local seed only: positivity/nonzero lemmas validate locally, but they are not yet integrated into ER-L011 or the terminal theorem"
  },
  {
    code := "ER-L013",
    title := "real finite-ratio sign and zero-case normalization",
    obligation :=
      "Normalize the real-valued eventMassRatio in zero and nonzero denominator cases, including monotonicity-friendly rewrites for (partialEventMass n)^2 / pairwiseEventMass n.",
    localInterface :=
      "eventMassRatio_nonneg plus future zero-denominator and division-cancellation lemmas",
    upstreamInputs :=
      "ER-L012, sq_nonneg, div_nonneg, field division lemmas over ℝ",
    downstreamUse :=
      "Paley-Zygmund/Cauchy-Schwarz finite lower bound and limsup inequality statement",
    budgetStepLimit := denominatorBridgeLeafBudgetLimit,
    status := .checkedLocalLemmaSeed,
    completionBoundary :=
      "checked seed only: nonnegativity is proved, but division-cancellation and zero-case rewrites remain open"
  },
  {
    code := "ER-L014",
    title := "finite real-to-ENNReal measure-sum bridges",
    obligation :=
      "Bridge partialEventMass and pairwiseEventMass to native ENNReal finite sums under finite/probability measure hypotheses.",
    localInterface :=
      "partialEventMassENNReal, pairwiseEventMassENNReal, ofReal_partialEventMass, ofReal_pairwiseEventMass",
    upstreamInputs :=
      "ofReal_measureReal, ENNReal.ofReal_sum_of_nonneg, IsFiniteMeasure from probability measures",
    downstreamUse :=
      "translation between mathlib measure statements and the real normalized lower-bound ratio",
    budgetStepLimit := denominatorBridgeLeafBudgetLimit,
    status := .checkedLocalLemmaSeed,
    completionBoundary :=
      "checked finite-sum bridges only: no infinite-series, limsup, or terminal lower-bound bridge is claimed"
  },
  {
    code := "ER-L015",
    title := "limsup and atTop real/ENNReal bridge",
    obligation :=
      "Prove the infinite/limit bridge needed to pass from finite real ratios to the ENNReal measure of limsup, including top/finite side conditions and order conversion.",
    localInterface :=
      "future lemmas connecting Filter.limsup eventMassRatio atTop and μ (limsup A atTop)",
    upstreamInputs :=
      "ER-L014, ENNReal.toReal/ofReal order lemmas, tendsto/limsup APIs, probability-measure finiteness",
    downstreamUse :=
      "terminal ErdosRenyiLowerBoundStatement",
    budgetStepLimit := denominatorBridgeLeafBudgetLimit,
    status := .uncheckedFormalizationDebt,
    completionBoundary :=
      "unchecked formalization debt: no local proof body currently proves the terminal real/ENNReal limsup bridge"
  }
]

/-- C005 proof-task codes for denominator and real/`ENNReal` bridge work. -/
def denominatorBridgeProofTaskCodes : List String :=
  denominatorBridgeProofTasks.map (fun row => row.code)

/-- The C005 task-code list is exactly `ER-L012` through `ER-L015`. -/
theorem denominatorBridgeProofTaskCodes_eq :
    denominatorBridgeProofTaskCodes =
      ["ER-L012", "ER-L013", "ER-L014", "ER-L015"] := by
  native_decide

/-- The C005 denominator/bridge split has exactly four rows. -/
theorem denominatorBridgeProofTasks_length :
    denominatorBridgeProofTasks.length = 4 := by
  native_decide

/-- Every C005 row is explicitly budgeted at the M0387 `<= 100` threshold. -/
theorem denominatorBridgeProofTasks_all_le_100 :
    denominatorBridgeProofTasks.all
      (fun row => row.budgetStepLimit ≤ denominatorBridgeLeafBudgetLimit) = true := by
  native_decide

#check partialEventMassENNReal
#check pairwiseEventMassENNReal
#check partialEventMass_nonneg
#check pairwiseEventMass_nonneg
#check pairwiseEventMass_pos_of_partialEventMass_pos
#check pairwiseEventMass_ne_zero_of_partialEventMass_pos
#check eventMassRatio_nonneg
#check ofReal_partialEventMass
#check ofReal_pairwiseEventMass
#check DenominatorBridgePackageStatus
#check DenominatorBridgeProofTask
#check denominatorBridgeProofTasks
#check denominatorBridgeProofTaskCodes_eq
#check denominatorBridgeProofTasks_length
#check denominatorBridgeProofTasks_all_le_100

/-- Search terms used in the pinned local mathlib tree for the anchor audit. -/
def mathlibAuditSearchTerms : List String := [
  "BorelCantelli",
  "measure_limsup_eq_one",
  "ae_mem_limsup_atTop_iff",
  "iIndepSet",
  "condExp_indicator_filtrationOfSet",
  "Erdos",
  "Renyi",
  "Kochen",
  "Stone",
  "pairwiseEventMass",
  "limsup"
]

/-- Primary-source pin for the mathlib proof bodies used by the local wrappers. -/
def mathlibPrimarySource : String :=
  "https://github.com/leanprover-community/mathlib4, revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Machine-proof debt classification for the terminal Erdos-Renyi statement. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration-debt gate for this Stage1 repair.

The local module checks mathlib Borel-Cantelli wrappers, but it does not claim
that the terminal Erdos-Renyi/Kochen-Stone lower bound is already closed by an
external Lean 4 proof.  Therefore no completed state is asserted and no
completed state retains repo-local integration debt.
-/
def repoLocalIntegrationDebtGate : String :=
  "not_completed; no completed-state repo_local_integration_debt retained"

/-- M0387 completion gates still open for the terminal theorem. -/
def m0387OpenCompletionGates : List String := [
  "terminal Erdos-Renyi lower-bound proof body or pinned upstream wrapper",
  "independent <=100-step ledgers for all proof leaves",
  "public blueprint/todo/README merge-back by a later integrator",
  "repo-local validation for the final theorem or dependency closure"
]

/-! ## C006 external Lean 4 primary-source audit. -/

/--
C006-local status vocabulary for external Lean 4 proof-body searches.

The status is deliberately about audit evidence, not theorem completion.
`checkedLocalMathlibOnly` means the proof body is already in the pinned local
mathlib dependency and wrapped above.  `blockedUnauthenticatedCodeSearch`
records a concrete search limitation that prevents claiming exhaustive GitHub
code-search coverage from this worker.
-/
inductive ExternalLeanProofSearchStatus where
  | checkedLocalMathlibOnly
  | noTerminalExternalProofFound
  | falsePositiveNotTerminal
  | blockedUnauthenticatedCodeSearch
  deriving DecidableEq, Repr

/-- One primary-source search probe from the C006 external-audit pass. -/
structure ExternalLeanProofSearchProbe where
  query : String
  surface : String
  result : String
  status : ExternalLeanProofSearchStatus
  completionImpact : String
  deriving Repr, DecidableEq

/-- Absolute date for the C006 external Lean 4 audit rerun. -/
def externalLeanProofSearchDate : String :=
  "2026-05-01"

/--
External Lean 4 primary-source search probes rerun for C006.

No terminal Erdos-Renyi/Kochen-Stone lower-bound proof body was found outside
the already pinned mathlib Borel-Cantelli infrastructure.  The unauthenticated
GitHub code-search limitation is retained as a concrete blocker against any
completion upgrade based on this audit alone.
-/
def externalLeanProofSearchProbes : List ExternalLeanProofSearchProbe := [
  {
    query := "Kochen-Stone Lean; Kochen Stone Borel-Cantelli Lean",
    surface := "web search over public Lean/GitHub-indexed pages",
    result :=
      "no credible Lean 4 repository or theorem-level proof body for the terminal Kochen-Stone lower-bound theorem was found",
    status := .noTerminalExternalProofFound,
    completionImpact :=
      "no external proof body available to pin/import/check from this probe"
  },
  {
    query := "Erdos-Renyi Borel-Cantelli Lean; ErdosRenyi BorelCantelli Lean",
    surface := "web search over public Lean/GitHub-indexed pages",
    result :=
      "results exposed mathlib Borel-Cantelli documentation and unrelated ErdosRenyi random-graph material, not the probability lower-bound theorem",
    status := .noTerminalExternalProofFound,
    completionImpact :=
      "no completion upgrade; terminal theorem remains not repo-local closed"
  },
  {
    query := "measure_limsup_eq_one and ae_mem_limsup_atTop_iff",
    surface := "pinned local mathlib and mathlib4 source documentation",
    result :=
      "only the independent second Borel-Cantelli theorem and Levy generalized Borel-Cantelli theorem are available and already wrapped locally",
    status := .checkedLocalMathlibOnly,
    completionImpact :=
      "valid nearby anchors, but not a terminal Erdos-Renyi/Kochen-Stone proof"
  },
  {
    query := "LeanCamCombi.ErdosRenyi.*",
    surface := "Lean community archive / public build log false-positive review",
    result :=
      "ErdosRenyi hits concern random-graph modules and visible placeholder warnings, not Borel-Cantelli or Kochen-Stone",
    status := .falsePositiveNotTerminal,
    completionImpact :=
      "not an integration candidate for THM-M-1009"
  },
  {
    query := "gh search code \"Kochen Stone Borel Cantelli language:Lean\" and related queries",
    surface := "GitHub CLI code search",
    result :=
      "blocked because gh is not logged in and GH_TOKEN is absent in this environment",
    status := .blockedUnauthenticatedCodeSearch,
    completionImpact :=
      "completion upgrade remains blocked until an authenticated code search is run or a concrete proof body is supplied"
  },
  {
    query := "GitHub REST code search for Kochen/Borel Lean",
    surface := "api.github.com/search/code",
    result :=
      "blocked by unauthenticated API rate limit; repository search variants returned zero repositories",
    status := .blockedUnauthenticatedCodeSearch,
    completionImpact :=
      "do not claim exhaustive external search coverage from this worker"
  }
]

/-- C006 found no non-mathlib external terminal proof body to integrate. -/
def externalLeanTerminalProofBodiesFound : List String := []

/-- C006 records exactly six external-search probes. -/
theorem externalLeanProofSearchProbes_length :
    externalLeanProofSearchProbes.length = 6 := by
  native_decide

/-- No terminal external proof body was available for pin/import/check. -/
theorem externalLeanTerminalProofBodiesFound_eq_nil :
    externalLeanTerminalProofBodiesFound = [] :=
  rfl

/--
C006 integration decision for the terminal theorem.

Because no non-mathlib terminal Lean 4 proof body was discovered, this child
does not introduce repo-local integration debt.  It also does not close the
terminal theorem: authenticated GitHub code search or a supplied proof body is
still required before any completion upgrade can be justified by external
evidence.
-/
def externalLeanProofIntegrationDecision : String :=
  "no non-mathlib terminal proof body found; no pin/import/check candidate available; completion upgrade blocked pending authenticated code search or supplied proof body"

#check ExternalLeanProofSearchStatus
#check ExternalLeanProofSearchProbe
#check externalLeanProofSearchDate
#check externalLeanProofSearchProbes
#check externalLeanProofSearchProbes_length
#check externalLeanTerminalProofBodiesFound
#check externalLeanTerminalProofBodiesFound_eq_nil
#check externalLeanProofIntegrationDecision

end S1_M_289
end Stage1
end AwesomeTheorems
