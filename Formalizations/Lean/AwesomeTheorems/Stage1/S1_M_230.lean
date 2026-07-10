import Mathlib.Probability.HasLaw
import Mathlib.Probability.IdentDistrib
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Process.Filtration
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# S1-M-230 / THM-M-1037: strong and weak solutions of SDEs

This Stage1 artifact records a conservative Lean 4 boundary for the distinction
between strong and weak solutions of stochastic differential equations.

The pinned mathlib snapshot has probability measures, laws of random variables,
independence, filtrations, adapted and progressively measurable processes, and
Bochner integration.  This audit did not locate a terminal Brownian-motion,
stochastic-integral, or SDE strong/weak solution theorem in local mathlib.

The declarations below therefore keep the stochastic-integral and pathwise SDE
equation as proposition fields, while making the probability space, filtration,
adaptedness, law, and strong-to-weak interface explicit and kernel-checkable.

Validation surface note: the parent Stage1 ledger records that
`cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_230.lean`
passed on 2026-04-30.  This file remains a checked statement-boundary artifact,
not a completion claim for the terminal strong/weak SDE theorem.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

open scoped MeasureTheory ENNReal NNReal ProbabilityTheory

namespace AwesomeTheorems.Stage1.S1_M_230

universe uΩ uT uX uW

/--
Strong-solution data for an abstract SDE model on a fixed filtered probability
space with a fixed driving noise.

The fields `coefficientHypotheses`, `stochasticIntegralConstruction`, and
`equationHolds` are deliberately abstract: the local mathlib snapshot does not
yet provide a canonical stochastic-integral object for the general SDE theorem.
-/
structure StrongSolutionData
    (Ω : Type uΩ) [MeasurableSpace Ω]
    (Time : Type uT) [Preorder Time]
    (State : Type uX) [MeasurableSpace State]
    (Noise : Type uW) [MeasurableSpace Noise]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω))
    (drivingNoise : Time → Ω → Noise) : Type (max (max uΩ uT) (max uX uW)) where
  solution : Time → Ω → State
  initialState : Ω → State
  initialLaw : Measure State
  stateLaw : Time → Measure State
  noiseLaw : Time → Measure Noise
  solution_adapted : Adapted ℱ solution
  drivingNoise_adapted : Adapted ℱ drivingNoise
  initial_hasLaw : HasLaw initialState initialLaw P
  state_hasLaw : ∀ t, HasLaw (solution t) (stateLaw t) P
  noise_hasLaw : ∀ t, HasLaw (drivingNoise t) (noiseLaw t) P
  coefficientHypotheses : Prop
  coefficientHypotheses_holds : coefficientHypotheses
  stochasticIntegralConstruction : Prop
  stochasticIntegralConstruction_holds : stochasticIntegralConstruction
  pathwiseEquation : Prop
  pathwiseEquation_holds : pathwiseEquation
  uniquenessOrSelectionInterface : Prop

/--
Weak-solution data for the same abstract SDE model.

Unlike `StrongSolutionData`, the probability space, measure, filtration, driving
noise, and solution are existential package fields.  This matches the usual
mathematical distinction: a weak solution is a solution on some filtered
probability space with a driving noise of the required law.
-/
structure WeakSolutionData
    (Time : Type uT) [Preorder Time]
    (State : Type uX) [MeasurableSpace State]
    (Noise : Type uW) [MeasurableSpace Noise] :
    Type (max (max (uΩ + 1) uT) (max uX uW)) where
  Ω : Type uΩ
  mΩ : MeasurableSpace Ω
  P : Measure Ω
  isProbability : IsProbabilityMeasure P
  filtration : Filtration Time mΩ
  solution : Time → Ω → State
  drivingNoise : Time → Ω → Noise
  initialState : Ω → State
  initialLaw : Measure State
  stateLaw : Time → Measure State
  noiseLaw : Time → Measure Noise
  solution_adapted : Adapted filtration solution
  drivingNoise_adapted : Adapted filtration drivingNoise
  initial_hasLaw : HasLaw initialState initialLaw P
  state_hasLaw : ∀ t, HasLaw (solution t) (stateLaw t) P
  noise_hasLaw : ∀ t, HasLaw (drivingNoise t) (noiseLaw t) P
  coefficientHypotheses : Prop
  coefficientHypotheses_holds : coefficientHypotheses
  stochasticIntegralConstruction : Prop
  stochasticIntegralConstruction_holds : stochasticIntegralConstruction
  equationHolds : Prop
  equationHolds_holds : equationHolds

/--
Convert a strong-solution package into a weak-solution package on the same
filtered probability space.

This is a checked Stage1 wrapper around the definitional part of the
strong/weak distinction.  It is not a proof of SDE existence, uniqueness, or
equivalence in law.
-/
def StrongSolutionData.toWeakSolutionData
    {Ω : Type uΩ} [mΩ : MeasurableSpace Ω]
    {Time : Type uT} [Preorder Time]
    {State : Type uX} [MeasurableSpace State]
    {Noise : Type uW} [MeasurableSpace Noise]
    {P : Measure Ω} [hP : IsProbabilityMeasure P]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)}
    {drivingNoise : Time → Ω → Noise}
    (D : StrongSolutionData Ω Time State Noise P ℱ drivingNoise) :
    WeakSolutionData.{uΩ, uT, uX, uW} Time State Noise where
  Ω := Ω
  mΩ := mΩ
  P := P
  isProbability := hP
  filtration := ℱ
  solution := D.solution
  drivingNoise := drivingNoise
  initialState := D.initialState
  initialLaw := D.initialLaw
  stateLaw := D.stateLaw
  noiseLaw := D.noiseLaw
  solution_adapted := D.solution_adapted
  drivingNoise_adapted := D.drivingNoise_adapted
  initial_hasLaw := D.initial_hasLaw
  state_hasLaw := D.state_hasLaw
  noise_hasLaw := D.noise_hasLaw
  coefficientHypotheses := D.coefficientHypotheses
  coefficientHypotheses_holds := D.coefficientHypotheses_holds
  stochasticIntegralConstruction := D.stochasticIntegralConstruction
  stochasticIntegralConstruction_holds := D.stochasticIntegralConstruction_holds
  equationHolds := D.pathwiseEquation
  equationHolds_holds := D.pathwiseEquation_holds

/-- A strong solution immediately supplies a weak solution. -/
theorem strongSolution_nonempty_to_weakSolution_nonempty
    {Ω : Type uΩ} [MeasurableSpace Ω]
    {Time : Type uT} [Preorder Time]
    {State : Type uX} [MeasurableSpace State]
    {Noise : Type uW} [MeasurableSpace Noise]
    {P : Measure Ω} [IsProbabilityMeasure P]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)}
    {drivingNoise : Time → Ω → Noise}
    (h : Nonempty (StrongSolutionData Ω Time State Noise P ℱ drivingNoise)) :
    Nonempty (WeakSolutionData.{uΩ, uT, uX, uW} Time State Noise) :=
  h.elim fun D => ⟨D.toWeakSolutionData⟩

/-- Project the adaptedness obligation from a strong-solution package. -/
theorem StrongSolutionData.solution_adapted_wrapper
    {Ω : Type uΩ} [MeasurableSpace Ω]
    {Time : Type uT} [Preorder Time]
    {State : Type uX} [MeasurableSpace State]
    {Noise : Type uW} [MeasurableSpace Noise]
    {P : Measure Ω} [IsProbabilityMeasure P]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)}
    {drivingNoise : Time → Ω → Noise}
    (D : StrongSolutionData Ω Time State Noise P ℱ drivingNoise) :
    Adapted ℱ D.solution :=
  D.solution_adapted

/-- Project the law obligation for a strong solution at a fixed time. -/
theorem StrongSolutionData.state_hasLaw_wrapper
    {Ω : Type uΩ} [MeasurableSpace Ω]
    {Time : Type uT} [Preorder Time]
    {State : Type uX} [MeasurableSpace State]
    {Noise : Type uW} [MeasurableSpace Noise]
    {P : Measure Ω} [IsProbabilityMeasure P]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)}
    {drivingNoise : Time → Ω → Noise}
    (D : StrongSolutionData Ω Time State Noise P ℱ drivingNoise) (t : Time) :
    HasLaw (D.solution t) (D.stateLaw t) P :=
  D.state_hasLaw t

/-- Project the adaptedness obligation from a weak-solution package. -/
theorem WeakSolutionData.solution_adapted_wrapper
    {Time : Type uT} [Preorder Time]
    {State : Type uX} [MeasurableSpace State]
    {Noise : Type uW} [MeasurableSpace Noise]
    (D : WeakSolutionData.{uΩ, uT, uX, uW} Time State Noise) :
    Adapted D.filtration D.solution :=
  D.solution_adapted

/-- Project the law obligation for a weak solution at a fixed time. -/
theorem WeakSolutionData.state_hasLaw_wrapper
    {Time : Type uT} [Preorder Time]
    {State : Type uX} [MeasurableSpace State]
    {Noise : Type uW} [MeasurableSpace Noise]
    (D : WeakSolutionData.{uΩ, uT, uX, uW} Time State Noise) (t : Time) :
    HasLaw (D.solution t) (D.stateLaw t) D.P :=
  D.state_hasLaw t

section MathlibAnchors

variable {Ω : Type uΩ} [MeasurableSpace Ω]
variable {Time : Type uT} [Preorder Time]
variable {State : Type uX} [MeasurableSpace State]

/-- Checked mathlib wrapper: constant processes are adapted to any filtration. -/
theorem adapted_const_process_wrapper
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) (x : State) :
    Adapted ℱ (fun _ _ => x : Time → Ω → State) :=
  adapted_const ℱ x

/-- Checked mathlib wrapper: the identity random variable has its source law. -/
theorem hasLaw_id_wrapper (μ : Measure State) :
    HasLaw (id : State → State) μ μ :=
  HasLaw.id

/-- Checked mathlib wrapper: identical distribution is reflexive for an a.e. measurable variable. -/
theorem identDistrib_refl_wrapper
    {P : Measure Ω} {X : Ω → State} (hX : AEMeasurable X P) :
    IdentDistrib X X P P :=
  IdentDistrib.refl hX

/--
Stage1 normalized statement shape for the strong/weak SDE solution slot.

The checked component is the implication from a strong solution package on a
fixed filtered probability space to a weak solution package.  The terminal SDE
existence/equivalence theorem remains future work because the stochastic
integral and Brownian-motion APIs were not found in local mathlib.
-/
def StatementShape
    (Time : Type uT) [Preorder Time]
    (State : Type uX) [MeasurableSpace State]
    (Noise : Type uW) [MeasurableSpace Noise] : Prop :=
  ∀ (Ω : Type uΩ) [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω))
    (drivingNoise : Time → Ω → Noise),
    Nonempty (StrongSolutionData Ω Time State Noise P ℱ drivingNoise) →
      Nonempty (WeakSolutionData.{uΩ, uT, uX, uW} Time State Noise)

/-- The statement shape unfolds to the explicit strong-to-weak implication. -/
theorem statementShape_iff_strong_to_weak
    (Time : Type uT) [Preorder Time]
    (State : Type uX) [MeasurableSpace State]
    (Noise : Type uW) [MeasurableSpace Noise] :
    StatementShape.{uΩ, uT, uX, uW} Time State Noise ↔
      ∀ (Ω : Type uΩ) [MeasurableSpace Ω]
        (P : Measure Ω) [IsProbabilityMeasure P]
        (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω))
        (drivingNoise : Time → Ω → Noise),
        Nonempty (StrongSolutionData Ω Time State Noise P ℱ drivingNoise) →
          Nonempty (WeakSolutionData.{uΩ, uT, uX, uW} Time State Noise) :=
  Iff.rfl

/-- The checked Stage1 statement-shape theorem for the definitional strong-to-weak branch. -/
theorem statementShape_from_strong_to_weak
    (Time : Type uT) [Preorder Time]
    (State : Type uX) [MeasurableSpace State]
    (Noise : Type uW) [MeasurableSpace Noise] :
    StatementShape.{uΩ, uT, uX, uW} Time State Noise := by
  intro Ω _mΩ P _hP ℱ drivingNoise h
  exact strongSolution_nonempty_to_weakSolution_nonempty
    (Ω := Ω) (Time := Time) (State := State) (Noise := Noise)
    (P := P) (ℱ := ℱ) (drivingNoise := drivingNoise) h

/--
Boundary witness: the weak package is not automatically inhabited for every
state space.  With one time point and an empty state space, a probability space
would be nonempty, so no solution process into `Empty` can exist.
-/
theorem noWeakSolutionData_emptyState :
    ¬ Nonempty (WeakSolutionData.{0, 0, 0, 0} PUnit Empty PUnit) := by
  rintro ⟨D⟩
  haveI : IsProbabilityMeasure D.P := D.isProbability
  rcases nonempty_of_isProbabilityMeasure D.P with ⟨ω⟩
  exact (D.solution PUnit.unit ω).elim

/--
The checked `StatementShape` can hold while a concrete weak-solution existence
claim is false.  This keeps the local wrapper explicitly below the terminal SDE
existence, uniqueness, Brownian-motion, stochastic-integral, or equivalence-in-law
theorem.
-/
theorem statementShape_not_weak_existence_witness :
    StatementShape.{0, 0, 0, 0} PUnit Empty PUnit ∧
      ¬ Nonempty (WeakSolutionData.{0, 0, 0, 0} PUnit Empty PUnit) :=
  ⟨statementShape_from_strong_to_weak PUnit Empty PUnit, noWeakSolutionData_emptyState⟩

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Process.Basic",
  "Mathlib.Probability.Independence.Process.HasIndepIncrements",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.FiniteDimensionalLaws",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic"
]

/-- Checked declaration names used as local anchors for this Stage1 statement boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.ProgMeasurable",
  "MeasureTheory.adapted_const",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.id",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.IdentDistrib.refl",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.HasIndepIncrements",
  "ProbabilityTheory.GaussianProcess.IsGaussianProcess",
  "MeasureTheory.Integrable",
  "MeasureTheory.AEStronglyMeasurable"
]

/--
Search terms that did not locate a terminal strong/weak SDE solution theorem in
the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "SDE",
  "stochastic differential equation",
  "StrongSolution",
  "WeakSolution",
  "strong solution",
  "weak solution",
  "BrownianMotion",
  "Brownian motion",
  "Wiener process",
  "stochastic integral",
  "Ito integral",
  "Itô integral",
  "semimartingale"
]

/--
Machine-readable route classification for replacing the abstract
`stochasticIntegralConstruction` field.

Only the first two routes would discharge child task `S1-M-230-C004`.  The
selected route below records that the current repo-local closure only supplies
Stage1 substrate, not a concrete mathlib or pinned external stochastic-integral
API.
-/
inductive StochasticIntegralAPIRoute where
  | pinnedMathlibStochasticIntegral
  | pinnedExternalItoAPI
  | repoLocalStage1CandidateOnly
  | notLocatedInPinnedClosure
  deriving DecidableEq, Repr

/--
Current C004 route after local source search of the pinned mathlib tree.

This is intentionally not a replacement for `stochasticIntegralConstruction`:
the replacement must be a checked mathlib declaration or a pinned external API,
not an anchor-only note or a repo-local placeholder.
-/
def selectedStochasticIntegralAPIRoute : StochasticIntegralAPIRoute :=
  StochasticIntegralAPIRoute.notLocatedInPinnedClosure

/-- C004 has not selected a concrete mathlib stochastic-integral API. -/
theorem selectedStochasticIntegralAPIRoute_not_mathlib :
    selectedStochasticIntegralAPIRoute ≠
      StochasticIntegralAPIRoute.pinnedMathlibStochasticIntegral := by
  decide

/-- C004 has not selected a pinned external Ito/stochastic-integral API. -/
theorem selectedStochasticIntegralAPIRoute_not_external :
    selectedStochasticIntegralAPIRoute ≠
      StochasticIntegralAPIRoute.pinnedExternalItoAPI := by
  decide

/--
Integration checklist for the future replacement of
`stochasticIntegralConstruction : Prop`.

This is a checked planning object only.  It records what a later serial
integration pass must supply before the abstract proposition can be removed.
-/
structure StochasticIntegralAPIReplacementPlan where
  targetField : String
  requiredClosureModes : List String
  rejectedSubstitutes : List String
  localBlocker : String
  validationCommand : String

/-- C004 integration-ready replacement plan for the stochastic-integral slot. -/
def stochasticIntegralAPIReplacementPlan : StochasticIntegralAPIReplacementPlan where
  targetField := "StrongSolutionData.stochasticIntegralConstruction"
  requiredClosureModes := [
    "local_wrapper_upstream_mathlib",
    "external_upstream_pinned"
  ]
  rejectedSubstitutes := [
    "external_upstream_anchor_only",
    "repo_local_stage1_candidate_only",
    "bare Prop field without an imported stochastic-integral declaration"
  ]
  localBlocker :=
    "No concrete StochasticIntegral/ItoIntegral API was located in the pinned local mathlib tree."
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_230.lean"

/--
Route choices for the canonical noise model in the future terminal SDE
statement.

The selected route is deliberately separated from the existing abstract
`Noise` parameter: choosing the model is a public statement-normalization step,
while replacing the current generic structures requires a later serial
integration pass.
-/
inductive CanonicalNoiseModelChoice where
  | brownianMotion
  | wienerProcess
  | gaussianProcessWithIndependentIncrements
  | discreteTimeFiniteStateAnalogue
  deriving DecidableEq, Repr

/--
Current C005 decision: use the mathlib-exposed Gaussian-process and
independent-increments interfaces as the canonical repo-local noise boundary.

This is not a claim that the repository has a terminal Brownian-motion or
Wiener-process API.  It records the strongest checked local substrate currently
available for the noise slot.
-/
def selectedCanonicalNoiseModelChoice : CanonicalNoiseModelChoice :=
  CanonicalNoiseModelChoice.gaussianProcessWithIndependentIncrements

/-- C005 selected the Gaussian-process-plus-independent-increments route. -/
theorem selectedCanonicalNoiseModelChoice_eq_gaussian_independent :
    selectedCanonicalNoiseModelChoice =
      CanonicalNoiseModelChoice.gaussianProcessWithIndependentIncrements :=
  rfl

/-- C005 did not select a named Brownian-motion API. -/
theorem selectedCanonicalNoiseModelChoice_not_brownian :
    selectedCanonicalNoiseModelChoice ≠ CanonicalNoiseModelChoice.brownianMotion := by
  decide

/-- C005 did not select a named Wiener-process API. -/
theorem selectedCanonicalNoiseModelChoice_not_wiener :
    selectedCanonicalNoiseModelChoice ≠ CanonicalNoiseModelChoice.wienerProcess := by
  decide

/-- C005 did not switch the parent theorem to a discrete-time finite-state analogue. -/
theorem selectedCanonicalNoiseModelChoice_not_discrete :
    selectedCanonicalNoiseModelChoice ≠
      CanonicalNoiseModelChoice.discreteTimeFiniteStateAnalogue := by
  decide

/--
Checked repo-local boundary for the selected noise model.

This packages exactly the mathlib predicates available in the current Lean
closure: a real-valued nonnegative-time process whose finite-dimensional laws
are Gaussian and whose increments are independent.  Brownian normalization,
sample-path continuity, and stochastic-integration compatibility remain future
work.
-/
structure GaussianIndependentIncrementNoiseBoundary
    (Ω : Type uΩ) [MeasurableSpace Ω] (P : Measure Ω) : Type (uΩ + 1) where
  process : ℝ≥0 → Ω → ℝ
  gaussianProcess : IsGaussianProcess process P
  independentIncrements : HasIndepIncrements process P

/-- The selected noise boundary exposes the driving process. -/
def GaussianIndependentIncrementNoiseBoundary.drivingNoise
    {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (N : GaussianIndependentIncrementNoiseBoundary Ω P) :
    ℝ≥0 → Ω → ℝ :=
  N.process

/-- The selected noise boundary exposes the mathlib Gaussian-process predicate. -/
theorem GaussianIndependentIncrementNoiseBoundary.isGaussianProcess
    {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (N : GaussianIndependentIncrementNoiseBoundary Ω P) :
    IsGaussianProcess N.process P :=
  N.gaussianProcess

/-- The selected noise boundary exposes the mathlib independent-increments predicate. -/
theorem GaussianIndependentIncrementNoiseBoundary.hasIndepIncrements
    {Ω : Type uΩ} [MeasurableSpace Ω] {P : Measure Ω}
    (N : GaussianIndependentIncrementNoiseBoundary Ω P) :
    HasIndepIncrements N.process P :=
  N.independentIncrements

/--
C005 integration-ready replacement plan for the abstract `Noise` slot.

The plan is checked data, not a public-doc merge and not terminal theorem
closure.  A later integration pass must still connect this boundary to the
chosen `Time`, `State`, SDE equation, and stochastic-integral API.
-/
structure CanonicalNoiseModelIntegrationPlan where
  selectedRoute : String
  checkedBoundary : String
  selectedMathlibAnchors : List String
  rejectedCompletionClaims : List String
  localBlocker : String
  validationCommand : String

/-- C005 plan for serially replacing the abstract noise model in the public theorem surface. -/
def canonicalNoiseModelIntegrationPlan : CanonicalNoiseModelIntegrationPlan where
  selectedRoute := "Gaussian process plus independent increments"
  checkedBoundary :=
    "AwesomeTheorems.Stage1.S1_M_230.GaussianIndependentIncrementNoiseBoundary"
  selectedMathlibAnchors := [
    "ProbabilityTheory.IsGaussianProcess",
    "ProbabilityTheory.HasIndepIncrements"
  ]
  rejectedCompletionClaims := [
    "named BrownianMotion API selected",
    "named WienerProcess API selected",
    "discrete-time finite-state analogue selected",
    "terminal strong/weak SDE theorem completed"
  ]
  localBlocker :=
    "The selected noise boundary is not yet connected to a concrete stochastic-integral API or explicit SDE equation."
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_230.lean"

/--
Explicit real-valued SDE equation terms for the next replacement of
`pathwiseEquation : Prop` and `equationHolds : Prop`.

This fixes the checked local equation shape to `Time = ℝ≥0`, `State = ℝ`, and
`Noise = ℝ`: for each time and sample point, the solution equals the initial
state plus a drift-integral term plus a stochastic-integral term.  The terms are
still named processes, not a construction of Ito integration.
-/
structure RealValuedSDEEquationTerms (Ω : Type uΩ) : Type uΩ where
  solution : ℝ≥0 → Ω → ℝ
  initialState : Ω → ℝ
  driftIntegralTerm : ℝ≥0 → Ω → ℝ
  stochasticIntegralTerm : ℝ≥0 → Ω → ℝ

/-- The explicit pathwise equation associated to `RealValuedSDEEquationTerms`. -/
def RealValuedSDEEquationTerms.equationHolds
    {Ω : Type uΩ} (E : RealValuedSDEEquationTerms Ω) : Prop :=
  ∀ (t : ℝ≥0) (ω : Ω),
    E.solution t ω =
      E.initialState ω + E.driftIntegralTerm t ω + E.stochasticIntegralTerm t ω

/-- The explicit equation predicate unfolds to the pointwise real-valued SDE shape. -/
theorem RealValuedSDEEquationTerms.equationHolds_iff
    {Ω : Type uΩ} (E : RealValuedSDEEquationTerms Ω) :
    E.equationHolds ↔
      ∀ (t : ℝ≥0) (ω : Ω),
        E.solution t ω =
          E.initialState ω + E.driftIntegralTerm t ω + E.stochasticIntegralTerm t ω :=
  Iff.rfl

/-- A package carrying the explicit SDE equation boundary and its proof. -/
structure RealValuedSDEEquationBoundary (Ω : Type uΩ) : Type uΩ where
  terms : RealValuedSDEEquationTerms Ω
  equation_holds : terms.equationHolds

/-- Project the solution process from an explicit real-valued SDE equation boundary. -/
def RealValuedSDEEquationBoundary.solution
    {Ω : Type uΩ} (E : RealValuedSDEEquationBoundary Ω) :
    ℝ≥0 → Ω → ℝ :=
  E.terms.solution

/-- Project the checked pointwise equation from an explicit real-valued boundary. -/
theorem RealValuedSDEEquationBoundary.equation_wrapper
    {Ω : Type uΩ} (E : RealValuedSDEEquationBoundary Ω) :
    ∀ (t : ℝ≥0) (ω : Ω),
      E.solution t ω =
        E.terms.initialState ω + E.terms.driftIntegralTerm t ω +
          E.terms.stochasticIntegralTerm t ω :=
  E.equation_holds

/--
Integration checklist for the future replacement of `pathwiseEquation : Prop`
and `equationHolds : Prop` with `RealValuedSDEEquationTerms.equationHolds`.

This is checked planning data plus a checked equation predicate.  It is not a
terminal SDE theorem and does not close the stochastic-integral construction
blocker.
-/
structure ExplicitSDEEquationReplacementPlan where
  targetFields : List String
  selectedTime : String
  selectedState : String
  selectedNoise : String
  checkedEquationBoundary : String
  requiredBeforeReplacement : List String
  rejectedCompletionClaims : List String
  localBlocker : String
  validationCommand : String

/-- C006 integration-ready replacement plan for the abstract SDE equation slots. -/
def explicitSDEEquationReplacementPlan : ExplicitSDEEquationReplacementPlan where
  targetFields := [
    "StrongSolutionData.pathwiseEquation",
    "WeakSolutionData.equationHolds"
  ]
  selectedTime := "ℝ≥0"
  selectedState := "ℝ"
  selectedNoise := "ℝ"
  checkedEquationBoundary :=
    "AwesomeTheorems.Stage1.S1_M_230.RealValuedSDEEquationTerms.equationHolds"
  requiredBeforeReplacement := [
    "replace stochasticIntegralTerm with a concrete mathlib or pinned external Ito/stochastic-integral API",
    "serially migrate StrongSolutionData and WeakSolutionData away from bare Prop equation fields",
    "update public blueprint/todo/README through an integrator-owned merge"
  ]
  rejectedCompletionClaims := [
    "terminal strong/weak SDE theorem completed",
    "Ito integral constructed in repo-local Lean",
    "Brownian/Wiener API selected",
    "external upstream theorem integrated"
  ]
  localBlocker :=
    "The explicit equation shape is checked locally, but its stochastic-integral term is still an uninterpreted process until C004 supplies a concrete API."
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_230.lean"

/--
C007 external-primary audit row for the strong/weak SDE source search.

The row format intentionally matches the public child-task fields.  Rows with
`integrationClassification = "external_upstream_anchor_only"` are evidence
records only; they do not count as repo-local theorem completion.
-/
structure ExternalSDEPrimarySourceAuditRow where
  targetSearchTerm : String
  repositoryUrl : String
  commitSHA : String
  modulePath : String
  theoremName : String
  leanToolchain : String
  license : String
  lakeIntegrationFeasibility : String
  integrationClassification : String

/-- External-primary audit rows found or ruled out for C007. -/
def externalSDEPrimarySourceAuditRows : List ExternalSDEPrimarySourceAuditRow := [
  {
    targetSearchTerm := "BrownianMotion"
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commitSHA := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    modulePath := "BrownianMotion.Gaussian.BrownianMotion"
    theoremName := "ProbabilityTheory.IsBrownian; ProbabilityTheory.IsBrownian_brownian"
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    lakeIntegrationFeasibility :=
      "Not directly importable in this repo-local pass: local Lean is v4.29.0 with mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95, while upstream HEAD uses v4.30.0-rc1 with mathlib f23306121184717ace04f3ac514be974e3224c8b and kolmogorov_extension4 e236e968c2b038b952444df54075a6e8b1058380. Serial integration should test a compatible tag or vendor checked declarations."
    integrationClassification := "external_upstream_anchor_only"
  },
  {
    targetSearchTerm := "WienerProcess"
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commitSHA := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    modulePath := "BrownianMotion.Gaussian.BrownianMotion"
    theoremName := "No declaration named WienerProcess located; Brownian predicate is ProbabilityTheory.IsBrownian."
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    lakeIntegrationFeasibility :=
      "No named WienerProcess API found in the audited external source. A future integration can either bridge IsBrownian to a repo-local WienerProcess wrapper or record that the canonical external name is IsBrownian."
    integrationClassification := "not_repo_local_closed"
  },
  {
    targetSearchTerm := "StochasticIntegral"
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commitSHA := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    modulePath := "BrownianMotion.StochasticIntegral.SimpleProcess"
    theoremName := "SimpleProcess.integral; SimpleProcess.integralEval"
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    lakeIntegrationFeasibility :=
      "Relevant elementary stochastic-integral source exists, but the upstream StochasticIntegral tree still contains sorry placeholders in adjacent modules such as SquareIntegrable, OptionalSampling, DoobMeyer, QuadraticVariation, LocalMartingale, UniformIntegrable, and Komlos at the audited commit. This is not a terminal Ito/SDE integration target without a pinned checked subset or proof-body closure."
    integrationClassification := "external_upstream_anchor_only"
  },
  {
    targetSearchTerm := "ItoIntegral"
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commitSHA := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    modulePath := "not located"
    theoremName := "No declaration named ItoIntegral or Itô integral located."
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    lakeIntegrationFeasibility :=
      "The audited source has elementary stochastic-integral infrastructure, but no named ItoIntegral API or checked Ito-integral terminal theorem was located."
    integrationClassification := "not_repo_local_closed"
  },
  {
    targetSearchTerm := "SDE"
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commitSHA := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    modulePath := "not located"
    theoremName := "No SDE declaration or theorem located."
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    lakeIntegrationFeasibility :=
      "No external SDE statement or proof target was found to pin/import/check for THM-M-1037."
    integrationClassification := "not_repo_local_closed"
  },
  {
    targetSearchTerm := "StrongSolution"
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commitSHA := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    modulePath := "not located"
    theoremName := "No declaration named StrongSolution located."
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    lakeIntegrationFeasibility :=
      "No external strong-solution SDE API was found to replace the repo-local StrongSolutionData boundary."
    integrationClassification := "not_repo_local_closed"
  },
  {
    targetSearchTerm := "WeakSolution"
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commitSHA := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    modulePath := "not located"
    theoremName := "No declaration named WeakSolution located."
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    license := "Apache-2.0"
    lakeIntegrationFeasibility :=
      "No external weak-solution SDE API was found to replace the repo-local WeakSolutionData boundary."
    integrationClassification := "not_repo_local_closed"
  }
]

/-- C007 records anchor/search evidence only; it is not repo-local completion. -/
def externalSDEPrimaryAuditClosesRepoLocalDebt : Bool :=
  false

/-- Completion gate sanity check for the C007 external-primary audit. -/
theorem externalSDEPrimaryAuditClosesRepoLocalDebt_eq_false :
    externalSDEPrimaryAuditClosesRepoLocalDebt = false :=
  rfl

/--
Possible outcomes for the C008 terminal-proof integration gate.

Only `terminalProofPinnedAndChecked` can support a repo-local completion claim.
The current audit is weaker: it found relevant Brownian and elementary
stochastic-integral anchors, but no terminal Lean 4 theorem for strong/weak SDE
solutions to pin, import, and check.
-/
inductive ExternalTerminalProofIntegrationStatus where
  | noTerminalProofLocated
  | terminalProofLocatedButNotPinned
  | terminalProofPinnedAndChecked
  | integrationBlocked
  deriving DecidableEq, Repr

/--
C008 integration-gate record for discovered external Lean 4 terminal proofs.

This is intentionally a blocker/planning object, not a dependency declaration:
public-doc edits and Lake dependency changes are reserved for the serial
integrator, and the C007 audit did not find a terminal `SDE`/`StrongSolution`/
`WeakSolution` theorem to import.
-/
structure ExternalTerminalProofIntegrationGate where
  childId : String
  status : ExternalTerminalProofIntegrationStatus
  discoveredTerminalProof : String
  actionTaken : String
  concreteBlocker : String
  repoLocalCompletionAllowed : Bool

/-- C008 gate: no external terminal strong/weak SDE proof is available to pin. -/
def s1m230C008ExternalTerminalProofIntegrationGate :
    ExternalTerminalProofIntegrationGate where
  childId := "S1-M-230-C008"
  status := ExternalTerminalProofIntegrationStatus.noTerminalProofLocated
  discoveredTerminalProof :=
    "No external Lean 4 terminal proof for SDE strong/weak solutions was located."
  actionTaken :=
    "No pin/import/check was attempted for anchor-only evidence; keep THM-M-1037 open."
  concreteBlocker :=
    "Audited external anchors cover Brownian predicates and elementary stochastic-integral pieces, but no named SDE, StrongSolution, WeakSolution, or ItoIntegral terminal theorem was found; the relevant external Brownian-motion source is also on a different Lean/mathlib toolchain from this repo-local closure."
  repoLocalCompletionAllowed := false

/-- C008 does not permit a repo-local completion claim. -/
theorem s1m230C008_repoLocalCompletionAllowed_eq_false :
    s1m230C008ExternalTerminalProofIntegrationGate.repoLocalCompletionAllowed = false :=
  rfl

/-- C008 did not reach the pinned-and-checked external-terminal-proof state. -/
theorem s1m230C008_status_ne_terminalProofPinnedAndChecked :
    s1m230C008ExternalTerminalProofIntegrationGate.status ≠
      ExternalTerminalProofIntegrationStatus.terminalProofPinnedAndChecked := by
  decide

/--
C009 successor leaf row for splitting the terminal strong/weak SDE theorem.

Each row is a planning/checklist object for a later public child task.  It is
not a proof of the corresponding mathematical branch, and `terminalCompletionAllowed`
must stay false until that branch has an independent `<=100` ledger and a
repo-local Lean closure.
-/
structure TerminalSDETheoremSuccessorLeaf where
  nodeId : String
  childTask : String
  terminalBranch : String
  independentLedgerPath : String
  maxLeafSteps : Nat
  independentLeafLedgerRequired : Bool
  terminalCompletionAllowed : Bool
  activeDebtClass : String
  repoLocalIntegrationGate : String

/--
C009 integration-ready successor split for the unchecked terminal theorem.

The split refines the parent `M1037-U011` through `M1037-U017` frontier into
seven independent public child tasks.  The paths are proposed ledger anchors for
the serial integrator; this worker does not create public docs or claim that
any successor branch is closed.
-/
def s1m230C009TerminalTheoremSuccessorLeaves :
    List TerminalSDETheoremSuccessorLeaf := [
  {
    nodeId := "M1037-U011"
    childTask :=
      "Choose and close the canonical continuous-noise model for the terminal SDE statement."
    terminalBranch :=
      "Brownian/Wiener/Gaussian-independent-increment noise model"
    independentLedgerPath :=
      ".cron/results/stage1_20260430_child/terminal_leaves/M1037-U011.md"
    maxLeafSteps := 100
    independentLeafLedgerRequired := true
    terminalCompletionAllowed := false
    activeDebtClass := "formalization_debt"
    repoLocalIntegrationGate :=
      "No terminal completion until the selected noise API is local, mathlib-backed, or pinned/imported/checked."
  },
  {
    nodeId := "M1037-U012"
    childTask :=
      "Replace stochasticIntegralConstruction with a concrete stochastic-integral or Ito API."
    terminalBranch := "stochastic integral construction"
    independentLedgerPath :=
      ".cron/results/stage1_20260430_child/terminal_leaves/M1037-U012.md"
    maxLeafSteps := 100
    independentLeafLedgerRequired := true
    terminalCompletionAllowed := false
    activeDebtClass := "formalization_debt"
    repoLocalIntegrationGate :=
      "Anchor-only stochastic-integral evidence is not completion; pin/import/check or record a blocker."
  },
  {
    nodeId := "M1037-U013"
    childTask :=
      "Encode coefficient hypotheses for drift and diffusion, including measurability and integrability."
    terminalBranch := "drift/diffusion coefficient hypotheses"
    independentLedgerPath :=
      ".cron/results/stage1_20260430_child/terminal_leaves/M1037-U013.md"
    maxLeafSteps := 100
    independentLeafLedgerRequired := true
    terminalCompletionAllowed := false
    activeDebtClass := "formalization_debt"
    repoLocalIntegrationGate :=
      "Coefficient predicates must be checked Lean structures or imported API fields before completion."
  },
  {
    nodeId := "M1037-U014"
    childTask :=
      "Replace abstract pathwiseEquation/equationHolds fields with the explicit SDE equation."
    terminalBranch := "pathwise SDE equation"
    independentLedgerPath :=
      ".cron/results/stage1_20260430_child/terminal_leaves/M1037-U014.md"
    maxLeafSteps := 100
    independentLeafLedgerRequired := true
    terminalCompletionAllowed := false
    activeDebtClass := "formalization_debt"
    repoLocalIntegrationGate :=
      "The equation branch is not closed while the stochastic-integral term remains uninterpreted."
  },
  {
    nodeId := "M1037-U015"
    childTask :=
      "Prove or import the concrete existence/uniqueness or strong-to-weak-in-law theorem."
    terminalBranch := "terminal SDE theorem"
    independentLedgerPath :=
      ".cron/results/stage1_20260430_child/terminal_leaves/M1037-U015.md"
    maxLeafSteps := 100
    independentLeafLedgerRequired := true
    terminalCompletionAllowed := false
    activeDebtClass := "formalization_debt"
    repoLocalIntegrationGate :=
      "Completion requires a local proof body, mathlib wrapper, or pinned external theorem checked in this repo."
  },
  {
    nodeId := "M1037-U016"
    childTask :=
      "Audit external Lean 4 terminal candidates and pin/import/check any actual terminal proof."
    terminalBranch := "external terminal proof integration"
    independentLedgerPath :=
      ".cron/results/stage1_20260430_child/terminal_leaves/M1037-U016.md"
    maxLeafSteps := 100
    independentLeafLedgerRequired := true
    terminalCompletionAllowed := false
    activeDebtClass := "formalization_debt"
    repoLocalIntegrationGate :=
      "If a terminal external proof is found, anchor-only evidence must become a pin/import/check task or a concrete blocker."
  },
  {
    nodeId := "M1037-U017"
    childTask :=
      "Serially merge accepted terminal-split status into public Stage1/todo/README surfaces."
    terminalBranch := "public merge and status synchronization"
    independentLedgerPath :=
      ".cron/results/stage1_20260430_child/terminal_leaves/M1037-U017.md"
    maxLeafSteps := 100
    independentLeafLedgerRequired := true
    terminalCompletionAllowed := false
    activeDebtClass := "public_doc_integration_work"
    repoLocalIntegrationGate :=
      "Public completion remains open until machine closure, validation, leaf ledgers, and serial merge-back agree."
  }
]

/-- C009 produces exactly the proposed `M1037-U011` through `M1037-U017` split. -/
theorem s1m230C009_terminalTheoremSuccessorLeaves_length :
    s1m230C009TerminalTheoremSuccessorLeaves.length = 7 :=
  rfl

/-- C009 records every successor leaf with a `<=100` step budget. -/
def s1m230C009AllSuccessorBudgetsWithinLimit : Bool :=
  s1m230C009TerminalTheoremSuccessorLeaves.all
    (fun L => decide (L.maxLeafSteps ≤ 100))

/-- The checked C009 successor split satisfies the local `<=100` budget gate. -/
theorem s1m230C009AllSuccessorBudgetsWithinLimit_eq_true :
    s1m230C009AllSuccessorBudgetsWithinLimit = true :=
  rfl

/-- C009 requires an independent ledger for every terminal successor leaf. -/
def s1m230C009AllSuccessorsRequireIndependentLedgers : Bool :=
  s1m230C009TerminalTheoremSuccessorLeaves.all
    (fun L => L.independentLeafLedgerRequired)

/-- Every C009 successor leaf is marked as requiring its own ledger. -/
theorem s1m230C009AllSuccessorsRequireIndependentLedgers_eq_true :
    s1m230C009AllSuccessorsRequireIndependentLedgers = true :=
  rfl

/-- C009 does not mark any terminal successor leaf as theorem-completion-ready. -/
def s1m230C009NoSuccessorCompletionClaim : Bool :=
  s1m230C009TerminalTheoremSuccessorLeaves.all
    (fun L => !L.terminalCompletionAllowed)

/-- No C009 successor leaf is allowed to support a terminal completion claim yet. -/
theorem s1m230C009NoSuccessorCompletionClaim_eq_true :
    s1m230C009NoSuccessorCompletionClaim = true :=
  rfl

end MathlibAnchors

/-! ## Audit probes -/

#check StrongSolutionData
#check WeakSolutionData
#check StrongSolutionData.toWeakSolutionData
#check strongSolution_nonempty_to_weakSolution_nonempty
#check statementShape_from_strong_to_weak
#check noWeakSolutionData_emptyState
#check statementShape_not_weak_existence_witness
#check Filtration
#check Adapted
#check ProgMeasurable
#check HasLaw
#check IdentDistrib
#check StochasticIntegralAPIRoute
#check selectedStochasticIntegralAPIRoute
#check selectedStochasticIntegralAPIRoute_not_mathlib
#check selectedStochasticIntegralAPIRoute_not_external
#check StochasticIntegralAPIReplacementPlan
#check stochasticIntegralAPIReplacementPlan
#check IsGaussianProcess
#check HasIndepIncrements
#check CanonicalNoiseModelChoice
#check selectedCanonicalNoiseModelChoice
#check selectedCanonicalNoiseModelChoice_eq_gaussian_independent
#check selectedCanonicalNoiseModelChoice_not_brownian
#check selectedCanonicalNoiseModelChoice_not_wiener
#check selectedCanonicalNoiseModelChoice_not_discrete
#check GaussianIndependentIncrementNoiseBoundary
#check GaussianIndependentIncrementNoiseBoundary.drivingNoise
#check GaussianIndependentIncrementNoiseBoundary.isGaussianProcess
#check GaussianIndependentIncrementNoiseBoundary.hasIndepIncrements
#check CanonicalNoiseModelIntegrationPlan
#check canonicalNoiseModelIntegrationPlan
#check RealValuedSDEEquationTerms
#check RealValuedSDEEquationTerms.equationHolds
#check RealValuedSDEEquationTerms.equationHolds_iff
#check RealValuedSDEEquationBoundary
#check RealValuedSDEEquationBoundary.solution
#check RealValuedSDEEquationBoundary.equation_wrapper
#check ExplicitSDEEquationReplacementPlan
#check explicitSDEEquationReplacementPlan
#check ExternalSDEPrimarySourceAuditRow
#check externalSDEPrimarySourceAuditRows
#check externalSDEPrimaryAuditClosesRepoLocalDebt
#check externalSDEPrimaryAuditClosesRepoLocalDebt_eq_false
#check ExternalTerminalProofIntegrationStatus
#check ExternalTerminalProofIntegrationGate
#check s1m230C008ExternalTerminalProofIntegrationGate
#check s1m230C008_repoLocalCompletionAllowed_eq_false
#check s1m230C008_status_ne_terminalProofPinnedAndChecked
#check TerminalSDETheoremSuccessorLeaf
#check s1m230C009TerminalTheoremSuccessorLeaves
#check s1m230C009_terminalTheoremSuccessorLeaves_length
#check s1m230C009AllSuccessorBudgetsWithinLimit
#check s1m230C009AllSuccessorBudgetsWithinLimit_eq_true
#check s1m230C009AllSuccessorsRequireIndependentLedgers
#check s1m230C009AllSuccessorsRequireIndependentLedgers_eq_true
#check s1m230C009NoSuccessorCompletionClaim
#check s1m230C009NoSuccessorCompletionClaim_eq_true

end AwesomeTheorems.Stage1.S1_M_230
