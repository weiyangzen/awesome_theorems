import Mathlib.MeasureTheory.Measure.LevyConvergence

/-!
# S1-M-291 / THM-M-1012: Levy continuity theorem

This Stage1 artifact records the repo-local Lean 4 boundary for the
characteristic-function convergence theorem for probability measures.

The pinned mathlib snapshot contains a terminal theorem for the known limiting
law form:

* `MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun`

for probability measures on finite-dimensional real inner product spaces.  This
file wraps that theorem and the adjacent tightness lemma.  It does not claim the
stronger classical existence form where an arbitrary pointwise limit, continuous
at zero, is first shown to be the characteristic function of a probability
measure.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology RealInnerProductSpace

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_291

universe u

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/--
Known-limit form of Levy's characteristic-function convergence theorem.

For probability measures on a finite-dimensional real inner product space,
weak convergence to a specified probability measure is equivalent to pointwise
convergence of characteristic functions to the characteristic function of that
specified measure.
-/
def KnownLimitStatementShape (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] : Prop :=
  ∀ (μ : ℕ → ProbabilityMeasure E) (μ₀ : ProbabilityMeasure E),
    Tendsto μ atTop (𝓝 μ₀) ↔
      ∀ t : E, Tendsto (fun n : ℕ => charFun (μ n) t) atTop (𝓝 (charFun μ₀ t))

/--
Stage1 checked statement shape for this slot.

This is the known limiting probability-measure version currently closed by
mathlib.  The stronger existence form is recorded separately as
`ClassicalExistenceStatementShape`.
-/
def StatementShape (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] : Prop :=
  KnownLimitStatementShape E

/-- The local statement shape unfolds to the known-limit formulation. -/
theorem statementShape_iff_knownLimit
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    StatementShape E ↔ KnownLimitStatementShape E :=
  Iff.rfl

/--
Repo-local wrapper around mathlib's Levy convergence theorem for probability
measures.
-/
theorem levyContinuity_knownLimit_mathlib_wrapper
    (μ : ℕ → ProbabilityMeasure E) (μ₀ : ProbabilityMeasure E) :
    Tendsto μ atTop (𝓝 μ₀) ↔
      ∀ t : E, Tendsto (fun n : ℕ => charFun (μ n) t) atTop (𝓝 (charFun μ₀ t)) :=
  ProbabilityMeasure.tendsto_iff_tendsto_charFun

/-- The checked Stage1 statement shape is closed by pinned mathlib. -/
theorem statementShape_mathlib :
    StatementShape E :=
  fun μ μ₀ => levyContinuity_knownLimit_mathlib_wrapper μ μ₀

/-- Pinned mathlib revision used for the checked local wrapper audit. -/
def checkedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Public-backfill alias for the repo-local completion status
`local_wrapper_upstream_mathlib`.
-/
theorem local_wrapper_upstream_mathlib :
    StatementShape E :=
  statementShape_mathlib

/--
Forward wrapper: weak convergence of probability measures implies pointwise
convergence of characteristic functions.
-/
theorem tendsto_charFun_of_tendsto_probabilityMeasure
    {μ : ℕ → ProbabilityMeasure E} {μ₀ : ProbabilityMeasure E}
    (hμ : Tendsto μ atTop (𝓝 μ₀)) :
    ∀ t : E, Tendsto (fun n : ℕ => charFun (μ n) t) atTop (𝓝 (charFun μ₀ t)) :=
  (levyContinuity_knownLimit_mathlib_wrapper μ μ₀).1 hμ

/--
Reverse wrapper: pointwise convergence of characteristic functions to the
characteristic function of a specified probability measure implies weak
convergence to that probability measure.
-/
theorem tendsto_probabilityMeasure_of_tendsto_charFun
    {μ : ℕ → ProbabilityMeasure E} {μ₀ : ProbabilityMeasure E}
    (hφ : ∀ t : E, Tendsto (fun n : ℕ => charFun (μ n) t) atTop (𝓝 (charFun μ₀ t))) :
    Tendsto μ atTop (𝓝 μ₀) :=
  (levyContinuity_knownLimit_mathlib_wrapper μ μ₀).2 hφ

/--
Checked adjacent tightness wrapper: if characteristic functions of a sequence
of probability measures converge pointwise to a function continuous at zero,
then the corresponding set of measures is tight.
-/
theorem tight_of_tendsto_charFun
    (μ : ℕ → ProbabilityMeasure E) {f : E → ℂ} (hf : ContinuousAt f 0)
    (hφ : ∀ t : E,
      Tendsto (fun n : ℕ => charFun ((μ n : ProbabilityMeasure E) : Measure E) t)
        atTop (𝓝 (f t))) :
    IsTightMeasureSet (Set.range fun n : ℕ => ((μ n : ProbabilityMeasure E) : Measure E)) := by
  simpa using
    (isTightMeasureSet_of_tendsto_charFun
      (μ := fun n : ℕ => ((μ n : ProbabilityMeasure E) : Measure E)) hf hφ)

/--
Classical existence-form target for later backfill.

This is the stronger continuity theorem often stated as: if characteristic
functions converge pointwise to a function continuous at zero, then that limit
is the characteristic function of a probability measure and the measures
converge weakly to it.  This file records only the shape; no proof is claimed.
-/
def ClassicalExistenceStatementShape
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] : Prop :=
  ∀ (μ : ℕ → ProbabilityMeasure E) (f : E → ℂ),
    ContinuousAt f 0 →
      (∀ t : E, Tendsto (fun n : ℕ => charFun (μ n) t) atTop (𝓝 (f t))) →
        ∃ μ₀ : ProbabilityMeasure E,
          Tendsto μ atTop (𝓝 μ₀) ∧ ∀ t : E, f t = charFun μ₀ t

/--
Statement-intent alternatives audited for the public THM-M-1012 slot.

`knownLimitEquivalence` is the form closed by pinned mathlib.  The
`arbitraryLimitExistence` alternative is the stronger textbook form that first
constructs a limiting probability measure from an arbitrary continuous-at-zero
pointwise characteristic-function limit.
-/
inductive StatementIntent where
  | knownLimitEquivalence
  | arbitraryLimitExistence
  deriving DecidableEq, Repr

/-- Translate the audited statement intent into the corresponding Lean shape. -/
def StatementShapeForIntent
    (intent : StatementIntent) (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] : Prop :=
  match intent with
  | .knownLimitEquivalence => KnownLimitStatementShape E
  | .arbitraryLimitExistence => ClassicalExistenceStatementShape E

/--
Child decision for `S1-M-291-C002`.

The intended repo-local Stage1 final statement should remain the known limiting
law equivalence unless a later serialized public decision explicitly upgrades
THM-M-1012 to the stronger arbitrary-limit existence theorem and supplies a
pin/import/check route for that missing constructor.
-/
def intendedFinalStatementDecision : StatementIntent :=
  .knownLimitEquivalence

/-- Checked decision marker: this child selects the known-limit equivalence. -/
theorem intendedFinalStatementDecision_is_knownLimit :
    intendedFinalStatementDecision = StatementIntent.knownLimitEquivalence :=
  rfl

/-- The selected child decision is exactly the locally checked `StatementShape`. -/
theorem statementShapeForDecision_iff_statementShape :
    StatementShapeForIntent intendedFinalStatementDecision E ↔ StatementShape E :=
  Iff.rfl

/--
Open leaves if the public theorem is later upgraded to the stronger arbitrary
limit existence form.
-/
def strongerExistenceOpenLeaves : List String := [
  "M291-L08: construct a probability measure μ₀ from the continuous-at-zero pointwise limit",
  "M291-L09: identify the limit function with charFun μ₀ and apply the known-limit wrapper"
]

/--
Public theorem-tree leaves to backfill as `unchecked` in the serialized
blueprint/todo integration pass for `S1-M-291-C004`.
-/
def publicBackfillUncheckedLeaves : List String := [
  "M291-L08 [unchecked]: show an arbitrary continuous-at-zero pointwise charFun limit is the characteristic function of some probability measure",
  "M291-L09 [unchecked]: connect the constructed limiting law to the known-limit wrapper and prove weak convergence",
  "M291-L10 [unchecked]: record the public statement-scope decision gate between the known-limit equivalence and the stronger arbitrary-limit existence form"
]

/-- mathlib modules checked while locating repo-local Levy continuity anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.LevyConvergence",
  "Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.Probability.Independence.CharacteristicFunction",
  "Mathlib.Probability.CentralLimitTheorem"
]

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
  "MeasureTheory.ProbabilityMeasure.tendsto_of_tendsto_charFun",
  "MeasureTheory.ProbabilityMeasure.tendsto_charPoly_of_tendsto_charFun",
  "MeasureTheory.isTightMeasureSet_of_tendsto_charFun",
  "MeasureTheory.isCompact_closure_of_isTightMeasureSet",
  "MeasureTheory.charFun",
  "MeasureTheory.charFun_eq_integral_innerProbChar",
  "MeasureTheory.Measure.ext_of_charFunDual",
  "MeasureTheory.IsTightMeasureSet",
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.LevyProkhorov.eq_convergenceInDistribution"
]

/--
Search terms that did not locate a terminal theorem for the stronger
arbitrary-limit existence form in pinned local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Levy continuity theorem",
  "Levy convergence theorem existence",
  "exists probability measure charFun",
  "continuous at zero characteristic function limit",
  "pointwise characteristic function limit exists law",
  "Bochner theorem",
  "Minlos theorem"
]

/--
Primary Lean 4 sources audited for the stronger arbitrary-limit existence
constructor required by `S1-M-291-C003`.

The mathlib entry is the pinned repo-local dependency.  The CLT and
lean-stat-learning-theory entries are primary upstream Lean 4 source
repositories whose Levy-continuity files predate or mirror the known-limit
mathlib route.
-/
def strongerExistencePrimaryLeanSources : List String := [
  "mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95: Mathlib.MeasureTheory.Measure.LevyConvergence",
  "RemyDegenne/CLT@50990c17040e099e3f6891bf332c28277046351d: Clt/Inversion.lean",
  "YuanheZ/lean-stat-learning-theory@4aaea15591360ccfffa1befdf0e7162f5af17f60: SLT/GaussianPoincare/LevyContinuity.lean"
]

/--
`S1-M-291-C003` audit result.

No audited primary Lean 4 source exposed a terminal theorem whose hypotheses are
an arbitrary `f : E → ℂ`, `ContinuousAt f 0`, and pointwise convergence
`charFun (μ n) t → f t`, and whose conclusion constructs
`∃ μ₀ : ProbabilityMeasure E, ...`.  The checked available theorem remains the
known-limit wrapper, while the arbitrary-limit constructor remains formalization
debt unless a future primary-source search finds and imports such a theorem.
-/
def strongerExistenceConstructorAuditResult : String :=
  "no terminal primary Lean 4 constructor for μ₀ from an arbitrary continuous-at-zero pointwise charFun limit was found"

/--
Concrete integration blocker if the public statement is later upgraded to the
stronger arbitrary-limit existence form.
-/
def strongerExistenceIntegrationBlocker : String :=
  "need a pinned/imported/checked Lean 4 theorem proving M291-L08; audited sources only provide tightness plus known-limit convergence"

/--
`S1-M-291-C005` validation command for the serialized public merge-back pass.

The child task is public validation-surface backfill, not a new theorem proof:
after the public blueprint/todo merge-back lands, an integrator should rerun
this exact command and copy the exact result into the authoritative public
validation surface.
-/
def publicValidationBackfillCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_291.lean"

/-- `S1-M-291-C005` public validation-surface action item. -/
def publicValidationBackfillAction : String :=
  "after public merge-back, rerun the owned Stage1 Lean file and record the exact result publicly"

/-! ## Audit probes retained in the checked file. -/

#check KnownLimitStatementShape
#check StatementShape
#check ClassicalExistenceStatementShape
#check StatementIntent
#check StatementShapeForIntent
#check intendedFinalStatementDecision
#check intendedFinalStatementDecision_is_knownLimit
#check statementShapeForDecision_iff_statementShape
#check strongerExistenceOpenLeaves
#check publicBackfillUncheckedLeaves
#check strongerExistencePrimaryLeanSources
#check strongerExistenceConstructorAuditResult
#check strongerExistenceIntegrationBlocker
#check publicValidationBackfillCommand
#check publicValidationBackfillAction
#check statementShape_mathlib
#check checkedMathlibRevision
#check local_wrapper_upstream_mathlib
#check levyContinuity_knownLimit_mathlib_wrapper
#check tendsto_charFun_of_tendsto_probabilityMeasure
#check tendsto_probabilityMeasure_of_tendsto_charFun
#check tight_of_tendsto_charFun
#check ProbabilityMeasure.tendsto_iff_tendsto_charFun
#check ProbabilityMeasure.tendsto_of_tendsto_charFun
#check ProbabilityMeasure.tendsto_charPoly_of_tendsto_charFun
#check isTightMeasureSet_of_tendsto_charFun
#check isCompact_closure_of_isTightMeasureSet
#check charFun
#check IsTightMeasureSet
#check ProbabilityMeasure

end S1_M_291
end Stage1
end AwesomeTheorems
