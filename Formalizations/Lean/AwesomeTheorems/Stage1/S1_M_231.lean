import Mathlib.Probability.HasLaw
import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Process.Kolmogorov
import Mathlib.Probability.Kernel.Basic
import Mathlib.MeasureTheory.Function.ConvergenceInDistribution

/-!
# S1-M-231 / THM-M-1038: Yamada-Watanabe theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Yamada-Watanabe theorem, summarized here as:

pathwise uniqueness together with weak existence for an SDE implies strong
existence and uniqueness in law.

The pinned mathlib snapshot has substantial probability infrastructure:
laws of random variables, filtrations, adapted processes, kernels, convergence
in distribution, and Kolmogorov-process moment conditions.  It does not expose
a canonical stochastic integral, Ito-process/SDE object model, Brownian-motion
structure tied to an SDE, or a terminal Yamada-Watanabe theorem.  The main
result is therefore represented as an explicit statement shape whose SDE
equation is a checked a.e. equality built from a local time-integral operator
and a local stochastic-integral operator.  No terminal Yamada-Watanabe proof is
claimed here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_231

universe uTime uΩ uState uNoise

/-- A stochastic process indexed by `Time`, on sample space `Ω`, with values in `State`. -/
abbrev Process (Time : Type uTime) (Ω : Type uΩ) (State : Type uState) :
    Type (max uTime (max uΩ uState)) :=
  Time → Ω → State

/--
Concrete local interface for the two integral operators used by an SDE.

`driftTimeIntegral b t` represents the time integral of a state-valued drift
integrand `b` up to `t`.  `stochasticIntegral σ W t` represents the stochastic
integral of a state-valued diffusion integrand `σ` against the driving process
`W` up to `t`.  The interface deliberately records operators rather than a
terminal Ito theory: the pinned mathlib snapshot has no canonical stochastic
integral API to import, but downstream code now sees a concrete equation
constructor instead of an unconstrained `Process → Process → Prop` field.
-/
structure SDEIntegralInterface (Time : Type uTime) (Ω : Type uΩ)
    (State : Type uState) (Noise : Type uNoise)
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] (P : Measure Ω)
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) :
    Type (max (max uTime uΩ) (max uState uNoise)) where
  initialTime : Time
  driftTimeIntegral : Process Time Ω State → Process Time Ω State
  stochasticIntegral : Process Time Ω State → Process Time Ω Noise → Process Time Ω State
  driftTimeIntegral_adapted :
    ∀ b : Process Time Ω State, Adapted ℱ (driftTimeIntegral b)
  stochasticIntegral_adapted :
    ∀ (σ : Process Time Ω State) (W : Process Time Ω Noise),
      Adapted ℱ (stochasticIntegral σ W)
  driftTimeIntegral_aemeasurable :
    ∀ (b : Process Time Ω State) (t : Time),
      AEMeasurable (driftTimeIntegral b t) P
  stochasticIntegral_aemeasurable :
    ∀ (σ : Process Time Ω State) (W : Process Time Ω Noise) (t : Time),
      AEMeasurable (stochasticIntegral σ W t) P

/--
SDE object model for the Stage1 Yamada-Watanabe boundary.

The stochastic equation is no longer an abstract proposition field.  It is
defined below by `SDEEquation` from the coefficient maps and the concrete
`SDEIntegralInterface`.  The remaining proposition fields mark the hypotheses
whose full mathematical content still requires Brownian/semimartingale
infrastructure and a classical weak-solution API.
-/
structure SDEModel (Time : Type uTime) (Ω : Type uΩ)
    (State : Type uState) (Noise : Type uNoise)
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] :
    Type (max (max uTime uΩ) (max uState uNoise)) where
  probabilityMeasure : Measure Ω
  filtration : Filtration Time (inferInstance : MeasurableSpace Ω)
  drift : Time → State → State
  diffusion : Time → State → Noise → State
  integralInterface :
    SDEIntegralInterface Time Ω State Noise probabilityMeasure filtration
  initialLaw : Measure State
  noiseLaw : Time → Measure Noise
  coefficientMeasurability : Prop
  coefficientRegularity : Prop
  stochasticIntegralObjectModel : Prop
  weakSolutionHypotheses : Prop
  strongConstructionHypotheses : Prop

/-- Drift integrand `b(t, X_t)`. -/
def DriftIntegrand
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise)
    (X : Process Time Ω State) : Process Time Ω State :=
  fun t ω => M.drift t (X t ω)

/-- Diffusion integrand `σ(t, X_t, W_t)`. -/
def DiffusionIntegrand
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise)
    (X : Process Time Ω State) (W : Process Time Ω Noise) : Process Time Ω State :=
  fun t ω => M.diffusion t (X t ω) (W t ω)

/--
Concrete SDE equation attached to the model:

`X_t = X_t0 + ∫ b(s, X_s) ds + ∫ σ(s, X_s, W_s) dW_s`, as an a.e. equality
at each indexed time.  The two integral terms are supplied by
`SDEIntegralInterface`, so this is a Lean-level stochastic-integral/SDE
interface even though the repository does not yet contain an Ito integral
construction.
-/
def SDEEquation
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise)
    (X : Process Time Ω State) (W : Process Time Ω Noise) : Prop :=
  ∀ t : Time,
    X t =ᵐ[M.probabilityMeasure]
      fun ω =>
        X M.integralInterface.initialTime ω +
          M.integralInterface.driftTimeIntegral (DriftIntegrand M X) t ω +
            M.integralInterface.stochasticIntegral (DiffusionIntegrand M X W) W t ω

/-- A strong solution on the fixed filtered probability space of `M`. -/
structure StrongSolution
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise) :
    Type (max (max uTime uΩ) (max uState uNoise)) where
  solution : Process Time Ω State
  drivingNoise : Process Time Ω Noise
  adapted_solution : Adapted M.filtration solution
  adapted_noise : Adapted M.filtration drivingNoise
  initial_law : ∀ t : Time, HasLaw (solution t) M.initialLaw M.probabilityMeasure
  noise_law : ∀ t : Time, HasLaw (drivingNoise t) (M.noiseLaw t) M.probabilityMeasure
  equation : SDEEquation M solution drivingNoise

/--
Weak-existence boundary for the same concrete-interface SDE model.

This is intentionally weaker than a final Yamada-Watanabe formalization: it
records that some candidate process/noise pair has the requested laws and
satisfies the concrete-interface SDE equation on the model's fixed filtered
probability space.  The classical weak-solution boundary is represented below
by `WeakExistenceOnSomeFilteredSpace`, which quantifies over a separate
filtered probability space.
-/
def WeakExistence
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise) : Prop :=
  ∃ (X : Process Time Ω State) (W : Process Time Ω Noise),
    (∀ t : Time, HasLaw (X t) M.initialLaw M.probabilityMeasure) ∧
      (∀ t : Time, HasLaw (W t) (M.noiseLaw t) M.probabilityMeasure) ∧
        Adapted M.filtration X ∧
          Adapted M.filtration W ∧
            SDEEquation M X W

/--
Rebase an SDE model onto a possibly different filtered probability space while
retaining the same time type, state/noise spaces, coefficients, and target laws.

This is the local Stage1 hook needed to state weak solutions in the usual
mathematical sense: the solution need not live on the fixed filtered space used
for strong solutions.
-/
def SDEModel.onFilteredSpace
    {Time : Type uTime} {Ω : Type uΩ} {Ωw : Type uΩ}
    {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace Ωw]
    [MeasurableSpace State] [MeasurableSpace Noise] [Add State]
    (M : SDEModel Time Ω State Noise)
    (Pw : Measure Ωw)
    (ℱw : Filtration Time (inferInstance : MeasurableSpace Ωw))
    (Iw : SDEIntegralInterface Time Ωw State Noise Pw ℱw) :
    SDEModel Time Ωw State Noise where
  probabilityMeasure := Pw
  filtration := ℱw
  drift := M.drift
  diffusion := M.diffusion
  integralInterface := Iw
  initialLaw := M.initialLaw
  noiseLaw := M.noiseLaw
  coefficientMeasurability := M.coefficientMeasurability
  coefficientRegularity := M.coefficientRegularity
  stochasticIntegralObjectModel := M.stochasticIntegralObjectModel
  weakSolutionHypotheses := M.weakSolutionHypotheses
  strongConstructionHypotheses := M.strongConstructionHypotheses

/--
Classical weak-existence boundary over a separate filtered probability space.

The existentially quantified `Ωw`, measurable structure, probability measure,
filtration, and integral interface define the weak solution's own stochastic
basis.  The rebased model uses the parent coefficients and laws, but its SDE
equation is checked against the weak-space measure and filtration.
-/
def WeakExistenceOnSomeFilteredSpace
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise) : Prop :=
  ∃ (Ωw : Type uΩ) (mΩw : MeasurableSpace Ωw),
    letI := mΩw
    ∃ (Pw : Measure Ωw)
      (ℱw : Filtration Time (inferInstance : MeasurableSpace Ωw))
      (Iw : SDEIntegralInterface Time Ωw State Noise Pw ℱw)
      (X : Process Time Ωw State) (W : Process Time Ωw Noise),
      let Mw : SDEModel Time Ωw State Noise :=
        M.onFilteredSpace Pw ℱw Iw
      (∀ t : Time, HasLaw (X t) M.initialLaw Pw) ∧
        (∀ t : Time, HasLaw (W t) (M.noiseLaw t) Pw) ∧
          Adapted ℱw X ∧
            Adapted ℱw W ∧
              SDEEquation Mw X W

/-- The former same-space placeholder is a special case of separate-space weak existence. -/
theorem WeakExistence.toWeakExistenceOnSomeFilteredSpace
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] {M : SDEModel Time Ω State Noise}
    (h : WeakExistence M) :
    WeakExistenceOnSomeFilteredSpace M := by
  rcases h with ⟨X, W, hX, hW, hXad, hWad, hEq⟩
  refine ⟨Ω, inferInstance, M.probabilityMeasure, M.filtration,
    M.integralInterface, X, W, ?_⟩
  refine ⟨hX, hW, hXad, hWad, ?_⟩
  simpa [SDEModel.onFilteredSpace] using hEq

/-- C004 status flag: the normalized statement uses a separate-space weak-solution predicate. -/
def statementShapeUsesSeparateWeakExistence : Bool := true

/-- C004 status flag: the same-space weak-existence predicate is not the terminal weak boundary. -/
def sameSpaceWeakExistenceIsTerminalWeakBoundary : Bool := false

theorem statementShapeUsesSeparateWeakExistence_eq_true :
    statementShapeUsesSeparateWeakExistence = true := by
  rfl

theorem sameSpaceWeakExistenceIsTerminalWeakBoundary_eq_false :
    sameSpaceWeakExistenceIsTerminalWeakBoundary = false := by
  rfl

/-- Integration-ready note for the C004 weak-solution-space split. -/
def separateWeakSolutionPublicNote : String :=
  "THM-M-1038 weak existence is represented by \
  AwesomeTheorems.Stage1.S1_M_231.WeakExistenceOnSomeFilteredSpace, which \
  existentially quantifies a weak sample space, measurable structure, \
  probability measure, filtration, integral interface, solution, and driving \
  noise. The old same-space WeakExistence predicate is retained only as a \
  checked special case via WeakExistence.toWeakExistenceOnSomeFilteredSpace."

/--
Pathwise uniqueness for solutions driven by the same noise on the same filtered
probability space.
-/
def PathwiseUniqueness
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise) : Prop :=
  ∀ S₁ S₂ : StrongSolution M,
    S₁.drivingNoise = S₂.drivingNoise →
      ∀ t : Time, S₁.solution t =ᵐ[M.probabilityMeasure] S₂.solution t

/-- Strong existence is the existence of a strong solution in the fixed object model. -/
def StrongExistence
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise) : Prop :=
  Nonempty (StrongSolution M)

/-- Uniqueness in law for strong solutions of the same concrete-interface SDE model. -/
def UniquenessInLaw
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise) : Prop :=
  ∀ S₁ S₂ : StrongSolution M,
    ∀ t : Time,
      IdentDistrib (S₁.solution t) (S₂.solution t)
        M.probabilityMeasure M.probabilityMeasure

/--
Conclusion package expected from a full Yamada-Watanabe formalization.

The `strong_solution`, `pathwise_uniqueness`, and `uniqueness_in_law` fields
isolate the standard outputs.  A terminal proof must connect these fields to a
concrete weak-solution construction and a concrete stochastic-integral equation.
-/
structure YamadaWatanabeConclusion
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise) : Prop where
  strong_existence : StrongExistence M
  pathwise_uniqueness : PathwiseUniqueness M
  uniqueness_in_law : UniquenessInLaw M

/--
Stage1 normalized statement shape for THM-M-1038.

For every concrete-interface SDE model, coefficient measurability/regularity,
stochastic-integral infrastructure, weak existence on some filtered probability
space, and pathwise uniqueness should imply strong existence and uniqueness in
law.  The statement is not proved in this file; it freezes the theorem boundary
for a later concrete SDE formalization or pinned external Lean 4 proof.
-/
def StatementShape : Prop :=
  ∀ (Time : Type uTime) (Ω : Type uΩ)
    (State : Type uState) (Noise : Type uNoise)
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State],
      ∀ M : SDEModel Time Ω State Noise,
        M.coefficientMeasurability →
          M.coefficientRegularity →
            M.stochasticIntegralObjectModel →
              M.weakSolutionHypotheses →
                M.strongConstructionHypotheses →
                  WeakExistenceOnSomeFilteredSpace M →
                    PathwiseUniqueness M →
                      YamadaWatanabeConclusion M

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Time : Type uTime) (Ω : Type uΩ)
      (State : Type uState) (Noise : Type uNoise)
      [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
      [MeasurableSpace Noise] [Add State],
        ∀ M : SDEModel Time Ω State Noise,
          M.coefficientMeasurability →
            M.coefficientRegularity →
              M.stochasticIntegralObjectModel →
                M.weakSolutionHypotheses →
                  M.strongConstructionHypotheses →
                    WeakExistenceOnSomeFilteredSpace M →
                      PathwiseUniqueness M →
                        YamadaWatanabeConclusion M) :
    StatementShape.{uTime, uΩ, uState, uNoise} :=
  h

/-- Projection wrapper: a strong solution is adapted to the model filtration. -/
theorem StrongSolution.adapted
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] {M : SDEModel Time Ω State Noise}
    (S : StrongSolution M) :
    Adapted M.filtration S.solution :=
  S.adapted_solution

/-- Projection wrapper: a strong solution satisfies the concrete SDE equation. -/
theorem StrongSolution.satisfies_sde
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] {M : SDEModel Time Ω State Noise}
    (S : StrongSolution M) :
    SDEEquation M S.solution S.drivingNoise :=
  S.equation

/-- Projection wrapper: the drift time integral in an SDE model is adapted. -/
theorem SDEModel.driftTimeIntegral_adapted
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise)
    (b : Process Time Ω State) :
    Adapted M.filtration (M.integralInterface.driftTimeIntegral b) :=
  M.integralInterface.driftTimeIntegral_adapted b

/-- Projection wrapper: the stochastic integral in an SDE model is adapted. -/
theorem SDEModel.stochasticIntegral_adapted
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] (M : SDEModel Time Ω State Noise)
    (σ : Process Time Ω State) (W : Process Time Ω Noise) :
    Adapted M.filtration (M.integralInterface.stochasticIntegral σ W) :=
  M.integralInterface.stochasticIntegral_adapted σ W

/-- Projection wrapper: the concrete SDE equation gives its time-coordinate a.e. equality. -/
theorem SDEEquation.apply
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] {M : SDEModel Time Ω State Noise}
    {X : Process Time Ω State} {W : Process Time Ω Noise}
    (h : SDEEquation M X W) (t : Time) :
    X t =ᵐ[M.probabilityMeasure]
      fun ω =>
        X M.integralInterface.initialTime ω +
          M.integralInterface.driftTimeIntegral (DriftIntegrand M X) t ω +
            M.integralInterface.stochasticIntegral (DiffusionIntegrand M X W) W t ω :=
  h t

/-- Projection wrapper: pathwise uniqueness gives coordinatewise a.e. equality. -/
theorem PathwiseUniqueness.apply
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] [Add State] {M : SDEModel Time Ω State Noise}
    (h : PathwiseUniqueness M) (S₁ S₂ : StrongSolution M)
    (hW : S₁.drivingNoise = S₂.drivingNoise) (t : Time) :
    S₁.solution t =ᵐ[M.probabilityMeasure] S₂.solution t :=
  h S₁ S₂ hW t

/-- Checked mathlib wrapper: constant processes are adapted to any filtration. -/
theorem adapted_const_process
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) (x : State) :
    Adapted ℱ (fun _ _ => x : Process Time Ω State) :=
  adapted_const ℱ x

/-- Checked mathlib wrapper: adapted coordinates are measurable in the ambient sigma-algebra. -/
theorem adapted_coordinate_measurable
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)}
    {X : Process Time Ω State} (hX : Adapted ℱ X) (t : Time) :
    Measurable (X t) :=
  hX.measurable

/-- Checked mathlib wrapper: adapted coordinates are a.e. measurable for any measure. -/
theorem adapted_coordinate_aemeasurable
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState}
    [Preorder Time] [MeasurableSpace Ω] [MeasurableSpace State]
    {ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)}
    {X : Process Time Ω State} (hX : Adapted ℱ X)
    (P : Measure Ω) (t : Time) :
    AEMeasurable (X t) P :=
  (adapted_coordinate_measurable hX t).aemeasurable

/-- Checked mathlib wrapper: `HasLaw` exposes its map equality. -/
theorem hasLaw_map_eq
    {Ω : Type uΩ} {State : Type uState} [MeasurableSpace Ω]
    [MeasurableSpace State] {P : Measure Ω} {μ : Measure State}
    {X : Ω → State} (hX : HasLaw X μ P) :
    P.map X = μ :=
  hX.map_eq

/-- Checked mathlib wrapper: `HasLaw` exposes a.e. measurability. -/
theorem hasLaw_aemeasurable
    {Ω : Type uΩ} {State : Type uState} [MeasurableSpace Ω]
    [MeasurableSpace State] {P : Measure Ω} {μ : Measure State}
    {X : Ω → State} (hX : HasLaw X μ P) :
    AEMeasurable X P :=
  hX.aemeasurable

/-- Checked mathlib wrapper: two random variables with the same law are identically distributed. -/
theorem hasLaw_identDistrib
    {Ω : Type uΩ} {State : Type uState} [MeasurableSpace Ω]
    [MeasurableSpace State] {P : Measure Ω} {μ : Measure State}
    {X Y : Ω → State} (hX : HasLaw X μ P) (hY : HasLaw Y μ P) :
    IdentDistrib X Y P P :=
  hX.identDistrib hY

/-- Checked mathlib wrapper: deterministic kernels evaluate to Dirac measures. -/
theorem deterministicKernel_apply
    {State : Type uState} {Noise : Type uNoise} [MeasurableSpace State]
    [MeasurableSpace Noise] {f : State → Noise} (hf : Measurable f) (x : State) :
    Kernel.deterministic f hf x = Measure.dirac (f x) :=
  Kernel.deterministic_apply hf x

/-- Checked Kolmogorov-process wrapper: exact Kolmogorov processes have measurable coordinates. -/
theorem kolmogorovProcess_measurable_at
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState}
    [PseudoEMetricSpace Time] [MeasurableSpace Ω] [PseudoEMetricSpace State]
    [MeasurableSpace State] [BorelSpace State]
    {X : Process Time Ω State} {P : Measure Ω} {p q : ℝ} {M : ℝ≥0}
    (hX : IsKolmogorovProcess X P p q M) (t : Time) :
    Measurable (X t) :=
  hX.measurable t

/--
Checked Kolmogorov-process wrapper: a.e. Kolmogorov processes have a.e.
measurable coordinates.
-/
theorem aeKolmogorovProcess_aemeasurable_at
    {Time : Type uTime} {Ω : Type uΩ} {State : Type uState}
    [PseudoEMetricSpace Time] [MeasurableSpace Ω] [PseudoEMetricSpace State]
    [MeasurableSpace State] [BorelSpace State]
    {X : Process Time Ω State} {P : Measure Ω} {p q : ℝ} {M : ℝ≥0}
    (hX : IsAEKolmogorovProcess X P p q M) (t : Time) :
    AEMeasurable (X t) P :=
  hX.aemeasurable t

/-! ## Discrete-time finite-state analogue -/

/--
Discrete-time SDE analogue used as a fully checked local special case.

The state recursion is written as a one-step measurable update
`oneStep n (X_n, W_n)`.  Its transition law is exposed through a mathlib
`Kernel`, while the random variables themselves are tracked with `HasLaw` and
`Adapted`.  This is intentionally a finite/discrete analogue, not a terminal
continuous-time Yamada-Watanabe theorem.
-/
structure DiscreteSDEAnalogue (Ω : Type uΩ) (State : Type uState)
    (Noise : Type uNoise) [MeasurableSpace Ω] [MeasurableSpace State]
    [MeasurableSpace Noise] : Type (max uΩ (max uState uNoise)) where
  probabilityMeasure : Measure Ω
  filtration : Filtration ℕ (inferInstance : MeasurableSpace Ω)
  stateLaw : ℕ → Measure State
  noiseLaw : ℕ → Measure Noise
  stateProcess : Process ℕ Ω State
  drivingNoise : Process ℕ Ω Noise
  oneStep : ℕ → State × Noise → State
  oneStep_measurable : ∀ n : ℕ, Measurable (oneStep n)
  transitionKernel : ℕ → Kernel (State × Noise) State
  transitionKernel_eq :
    ∀ n : ℕ, transitionKernel n =
      Kernel.deterministic (oneStep n) (oneStep_measurable n)
  adapted_state : Adapted filtration stateProcess
  adapted_noise : Adapted filtration drivingNoise
  state_law : ∀ n : ℕ, HasLaw (stateProcess n) (stateLaw n) probabilityMeasure
  noise_law : ∀ n : ℕ, HasLaw (drivingNoise n) (noiseLaw n) probabilityMeasure
  one_step_equation :
    ∀ n : ℕ, stateProcess (n + 1) =ᵐ[probabilityMeasure]
      fun ω => oneStep n (stateProcess n ω, drivingNoise n ω)

/-- Projection wrapper: the discrete analogue's transition kernels are Markov kernels. -/
theorem DiscreteSDEAnalogue.transitionKernel_isMarkov
    {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [MeasurableSpace Ω] [MeasurableSpace State] [MeasurableSpace Noise]
    (D : DiscreteSDEAnalogue Ω State Noise) (n : ℕ) :
    IsMarkovKernel (D.transitionKernel n) := by
  rw [D.transitionKernel_eq n]
  infer_instance

/-- Projection wrapper: the deterministic transition kernel evaluates to a Dirac law. -/
theorem DiscreteSDEAnalogue.transitionKernel_apply
    {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [MeasurableSpace Ω] [MeasurableSpace State] [MeasurableSpace Noise]
    (D : DiscreteSDEAnalogue Ω State Noise) (n : ℕ) (z : State × Noise) :
    D.transitionKernel n z = Measure.dirac (D.oneStep n z) := by
  rw [D.transitionKernel_eq n]
  exact Kernel.deterministic_apply (D.oneStep_measurable n) z

/-- Projection wrapper: the discrete analogue exposes its checked one-step equation. -/
theorem DiscreteSDEAnalogue.oneStepEquation
    {Ω : Type uΩ} {State : Type uState} {Noise : Type uNoise}
    [MeasurableSpace Ω] [MeasurableSpace State] [MeasurableSpace Noise]
    (D : DiscreteSDEAnalogue Ω State Noise) (n : ℕ) :
    D.stateProcess (n + 1) =ᵐ[D.probabilityMeasure]
      fun ω => D.oneStep n (D.stateProcess n ω, D.drivingNoise n ω) :=
  D.one_step_equation n

/-- The one-point finite-state update used by the checked discrete analogue. -/
def unitDiscreteStep : ℕ → Unit × Unit → Unit :=
  fun _ _ => ()

/-- The one-point update is measurable. -/
theorem unitDiscreteStep_measurable (n : ℕ) :
    Measurable (unitDiscreteStep n) :=
  measurable_const

/-- Deterministic transition kernel for the one-point finite-state analogue. -/
def unitDiscreteTransitionKernel (n : ℕ) : Kernel (Unit × Unit) Unit :=
  Kernel.deterministic (unitDiscreteStep n) (unitDiscreteStep_measurable n)

/-- Checked kernel API wrapper for the one-point transition kernel. -/
theorem unitDiscreteTransitionKernel_isMarkov (n : ℕ) :
    IsMarkovKernel (unitDiscreteTransitionKernel n) := by
  rw [unitDiscreteTransitionKernel]
  infer_instance

/-- The one-point transition kernel is the Dirac kernel at `()`. -/
theorem unitDiscreteTransitionKernel_apply (n : ℕ) (z : Unit × Unit) :
    unitDiscreteTransitionKernel n z = Measure.dirac () := by
  simp [unitDiscreteTransitionKernel, unitDiscreteStep, Kernel.deterministic_apply]

/-- Checked `HasLaw` fact for the one-point random variable. -/
theorem unitConst_hasLaw :
    HasLaw (fun _ : Unit => ()) (Measure.dirac ()) (Measure.dirac ()) := by
  simpa using (HasLaw.id (μ := Measure.dirac Unit.unit))

/--
Fully checked finite-state/discrete-time SDE analogue.

This closes the local C005 special case: the state space and noise space are
finite (`Unit`), time is discrete (`ℕ`), the process/noise are adapted constant
processes, the laws are stated with `HasLaw`, and the transition is the
deterministic mathlib kernel associated to `unitDiscreteStep`.
-/
def unitFiniteStateDiscreteSDEAnalogue : DiscreteSDEAnalogue Unit Unit Unit where
  probabilityMeasure := Measure.dirac ()
  filtration := (⊤ : Filtration ℕ (inferInstance : MeasurableSpace Unit))
  stateLaw := fun _ => Measure.dirac ()
  noiseLaw := fun _ => Measure.dirac ()
  stateProcess := fun _ _ => ()
  drivingNoise := fun _ _ => ()
  oneStep := unitDiscreteStep
  oneStep_measurable := unitDiscreteStep_measurable
  transitionKernel := unitDiscreteTransitionKernel
  transitionKernel_eq := by
    intro n
    rfl
  adapted_state :=
    adapted_const_process (Ω := Unit) (State := Unit)
      (⊤ : Filtration ℕ (inferInstance : MeasurableSpace Unit)) Unit.unit
  adapted_noise :=
    adapted_const_process (Ω := Unit) (State := Unit)
      (⊤ : Filtration ℕ (inferInstance : MeasurableSpace Unit)) Unit.unit
  state_law := by
    intro n
    exact unitConst_hasLaw
  noise_law := by
    intro n
    exact unitConst_hasLaw
  one_step_equation := by
    intro n
    simp [unitDiscreteStep]

/-- The checked finite-state analogue has adapted state process. -/
theorem unitFiniteStateDiscreteSDEAnalogue_adapted_state :
    Adapted unitFiniteStateDiscreteSDEAnalogue.filtration
      unitFiniteStateDiscreteSDEAnalogue.stateProcess :=
  unitFiniteStateDiscreteSDEAnalogue.adapted_state

/-- The checked finite-state analogue records the state laws with `HasLaw`. -/
theorem unitFiniteStateDiscreteSDEAnalogue_state_law (n : ℕ) :
    HasLaw (unitFiniteStateDiscreteSDEAnalogue.stateProcess n)
      (unitFiniteStateDiscreteSDEAnalogue.stateLaw n)
      unitFiniteStateDiscreteSDEAnalogue.probabilityMeasure :=
  unitFiniteStateDiscreteSDEAnalogue.state_law n

/-- The checked finite-state analogue records the noise laws with `HasLaw`. -/
theorem unitFiniteStateDiscreteSDEAnalogue_noise_law (n : ℕ) :
    HasLaw (unitFiniteStateDiscreteSDEAnalogue.drivingNoise n)
      (unitFiniteStateDiscreteSDEAnalogue.noiseLaw n)
      unitFiniteStateDiscreteSDEAnalogue.probabilityMeasure :=
  unitFiniteStateDiscreteSDEAnalogue.noise_law n

/-- The checked finite-state analogue exposes Markov transition kernels. -/
theorem unitFiniteStateDiscreteSDEAnalogue_transitionKernel_isMarkov (n : ℕ) :
    IsMarkovKernel (unitFiniteStateDiscreteSDEAnalogue.transitionKernel n) :=
  unitFiniteStateDiscreteSDEAnalogue.transitionKernel_isMarkov n

/-- The checked finite-state analogue satisfies its one-step recurrence. -/
theorem unitFiniteStateDiscreteSDEAnalogue_oneStepEquation (n : ℕ) :
    unitFiniteStateDiscreteSDEAnalogue.stateProcess (n + 1)
      =ᵐ[unitFiniteStateDiscreteSDEAnalogue.probabilityMeasure]
        fun ω =>
          unitFiniteStateDiscreteSDEAnalogue.oneStep n
            (unitFiniteStateDiscreteSDEAnalogue.stateProcess n ω,
              unitFiniteStateDiscreteSDEAnalogue.drivingNoise n ω) :=
  unitFiniteStateDiscreteSDEAnalogue.oneStepEquation n

/-- C005 status flag: the local finite-state/discrete-time analogue is checked. -/
def finiteStateDiscreteAnalogueChecked : Bool := true

/-- C005 status flag: the analogue is not a terminal Yamada-Watanabe theorem. -/
def finiteStateDiscreteAnalogueIsTerminalYWProof : Bool := false

theorem finiteStateDiscreteAnalogueChecked_eq_true :
    finiteStateDiscreteAnalogueChecked = true := by
  rfl

theorem finiteStateDiscreteAnalogueIsTerminalYWProof_eq_false :
    finiteStateDiscreteAnalogueIsTerminalYWProof = false := by
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.IonescuTulcea.Traj",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Process.HasIndepIncrements",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic"
]

/-- Checked declaration names used or audited for the Stage1 Yamada-Watanabe boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.adapted_const",
  "MeasureTheory.Adapted.measurable",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.map_eq",
  "ProbabilityTheory.HasLaw.aemeasurable",
  "ProbabilityTheory.HasLaw.identDistrib",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.Kernel.deterministic",
  "ProbabilityTheory.Kernel.deterministic_apply",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.IsKolmogorovProcess",
  "ProbabilityTheory.IsAEKolmogorovProcess",
  "ProbabilityTheory.IsKolmogorovProcess.measurable",
  "ProbabilityTheory.IsAEKolmogorovProcess.aemeasurable",
  "MeasureTheory.TendstoInDistribution"
]

/--
Search terms that did not locate a terminal Yamada-Watanabe theorem or canonical
SDE stochastic-calculus API in the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Yamada",
  "Watanabe",
  "Yamada-Watanabe",
  "pathwise uniqueness",
  "weak existence",
  "strong solution",
  "stochastic differential equation",
  "SDE",
  "Ito",
  "Itô",
  "stochastic integral",
  "BrownianMotion",
  "IsBrownianMotion"
]

/-! ## External Lean 4 Yamada-Watanabe audit -/

/--
Primary-source Lean 4 audit row for child `S1-M-231-C002`.

This is audit metadata only.  A row is completion evidence only if it records a
terminal Yamada-Watanabe theorem that is pinned/imported/checked in this
repository's Lake closure.  The current rows deliberately do not make that
claim.
-/
structure ExternalYamadaWatanabeAuditRow where
  repositoryUrl : String
  commit : String
  auditedSearchTerms : List String
  sourcePaths : List String
  theoremOrDeclarationNames : List String
  license : String
  leanToolchain : String
  lakeCompatibility : String
  terminalYamadaWatanabeFound : Bool
  repoLocalImportChecked : Bool
  integrationBlocker : String

/--
Repo-local integration gate for a terminal external Yamada-Watanabe proof.

If a row ever records `terminalYamadaWatanabeFound = true`, this gate requires
either a successful repo-local import/check or a concrete nonempty blocker.
Rows with no terminal proof found satisfy the gate vacuously and are not
completion evidence.
-/
def ExternalYamadaWatanabeAuditRow.repoLocalIntegrationGate
    (row : ExternalYamadaWatanabeAuditRow) : Prop :=
  row.terminalYamadaWatanabeFound = true →
    row.repoLocalImportChecked = true ∨ row.integrationBlocker ≠ ""

/--
Primary Lean 4 repositories audited for a terminal Yamada-Watanabe theorem.

The pinned mathlib row is repo-local and compatible, but it contains no
terminal SDE/Yamada-Watanabe theorem in the audited source tree.  The
`RemyDegenne/brownian-motion` row is relevant stochastic-calculus
infrastructure only: it has Brownian-motion and stochastic-integral modules,
but the searched source tree contains no Yamada-Watanabe/pathwise-uniqueness
theorem and is not importable in this repository's current Lake closure.
-/
def externalYamadaWatanabeAuditRows : List ExternalYamadaWatanabeAuditRow := [
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    auditedSearchTerms := absentTerminalSearchTerms
    sourcePaths := [
      "Mathlib/Probability/*.lean",
      "Mathlib/Probability/Process/*.lean",
      "Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean"
    ]
    theoremOrDeclarationNames := mathlibAnchorNames
    license := "Apache-2.0"
    leanToolchain := "leanprover/lean4:v4.29.0"
    lakeCompatibility :=
      "compatible: this mathlib commit is pinned in Formalizations/Lean/lake-manifest.json and imported by the local Stage1 artifact"
    terminalYamadaWatanabeFound := false
    repoLocalImportChecked := true
    integrationBlocker :=
      "No terminal Yamada-Watanabe theorem, canonical SDE API, Brownian-motion API, or stochastic-integral API was found in the pinned local mathlib source search."
  },
  {
    repositoryUrl := "https://github.com/RemyDegenne/brownian-motion"
    commit := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
    auditedSearchTerms := [
      "Yamada",
      "Watanabe",
      "Yamada-Watanabe",
      "pathwise uniqueness",
      "weak existence",
      "strong solution",
      "stochastic differential",
      "SDE"
    ]
    sourcePaths := [
      "BrownianMotion/Gaussian/BrownianMotion.lean",
      "BrownianMotion/StochasticIntegral/*.lean",
      "BrownianMotion/Continuity/KolmogorovChentsov.lean"
    ]
    theoremOrDeclarationNames := [
      "ProbabilityTheory.IsBrownian",
      "ProbabilityTheory.brownian",
      "ProbabilityTheory.IsBrownian_brownian",
      "ProbabilityTheory.continuous_brownian",
      "ProbabilityTheory.hasIndepIncrements_brownian",
      "ProbabilityTheory.SimpleProcess.integral",
      "ProbabilityTheory.SimpleProcess.integralEval",
      "ProbabilityTheory.quadraticVariation"
    ]
    license := "Apache-2.0"
    leanToolchain := "leanprover/lean4:v4.30.0-rc1"
    lakeCompatibility :=
      "incompatible with this repository without a dependency/toolchain migration: BrownianMotion uses mathlib f23306121184717ace04f3ac514be974e3224c8b, while this repository uses leanprover/lean4:v4.29.0 with mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; local import probe failed with unknown module prefix BrownianMotion"
    terminalYamadaWatanabeFound := false
    repoLocalImportChecked := false
    integrationBlocker :=
      "No Yamada/Watanabe/pathwise-uniqueness/weak-existence/strong-solution theorem was found in the audited BrownianMotion source tree; adjacent stochastic-integral modules contain unfinished proof placeholders, so this is not terminal completion evidence."
  }
]

/-- The external audit records the two primary Lean 4 surfaces checked in this pass. -/
theorem externalYamadaWatanabeAuditRows_length :
    externalYamadaWatanabeAuditRows.length = 2 := by
  rfl

/--
Every audited row satisfies the C003 integration gate: a terminal external
proof must be pin/import/checked locally or have an explicit blocker.
-/
theorem externalYamadaWatanabeAuditRows_repoLocalIntegrationGate :
    ∀ row ∈ externalYamadaWatanabeAuditRows,
      ExternalYamadaWatanabeAuditRow.repoLocalIntegrationGate row := by
  intro row hrow
  simp [externalYamadaWatanabeAuditRows,
    ExternalYamadaWatanabeAuditRow.repoLocalIntegrationGate] at hrow ⊢
  rcases hrow with rfl | rfl <;> intro hterminal <;> cases hterminal

/-- The audited rows do not record a terminal external Yamada-Watanabe proof. -/
theorem externalYamadaWatanabeAuditRows_noTerminalProof :
    ∀ row ∈ externalYamadaWatanabeAuditRows,
      row.terminalYamadaWatanabeFound = false := by
  intro row hrow
  simp [externalYamadaWatanabeAuditRows] at hrow ⊢
  rcases hrow with rfl | rfl <;> rfl

/-- No terminal external Lean 4 Yamada-Watanabe theorem was located by this audit. -/
def externalYamadaWatanabeTerminalProofFound : Bool := false

/-- Anchor-only stochastic-calculus infrastructure is not repo-local completion evidence. -/
def externalYamadaWatanabeAnchorOnlyEvidenceIsCompletion : Bool := false

/--
M0387 integration-debt gate for this child: no completed state is claimed, and
no known terminal external Lean 4 proof is left as anchor-only evidence.
-/
def externalYamadaWatanabeCompletedStateRetainsRepoLocalIntegrationDebt : Bool := false

theorem externalYamadaWatanabeTerminalProofFound_eq_false :
    externalYamadaWatanabeTerminalProofFound = false := by
  rfl

theorem externalYamadaWatanabeAnchorOnlyEvidenceIsCompletion_eq_false :
    externalYamadaWatanabeAnchorOnlyEvidenceIsCompletion = false := by
  rfl

theorem externalYamadaWatanabeCompletedStateRetainsRepoLocalIntegrationDebt_eq_false :
    externalYamadaWatanabeCompletedStateRetainsRepoLocalIntegrationDebt = false := by
  rfl

/-! ## C006 theorem-tree package split -/

/--
Package-level ledger row for the Stage1 Yamada-Watanabe theorem tree.

This is a checked decomposition artifact, not a proof of the terminal theorem.
`leafCount` records the number of child leaf ledgers proposed for the package,
and `leafBudgetUpperBound` records the intended local proof-step cap for each
leaf in that package.
-/
structure TheoremTreePackageLedger where
  packageId : String
  role : String
  leafCount : Nat
  leafBudgetUpperBound : Nat
  repoLocalCompletionClaimed : Bool

/--
C006 package split requested by the public Stage1 backfill line.

Each row is intentionally small enough to be expanded by an integrator into
per-leaf ledgers without exceeding the M0387 `<=100` local leaf budget rule.
-/
def yamadaWatanabeTheoremTreePackages : List TheoremTreePackageLedger := [
  {
    packageId := "YW.P0.statement"
    role := "Normalize the theorem boundary: process type, laws, weak existence, pathwise uniqueness, strong existence, and uniqueness in law."
    leafCount := 8
    leafBudgetUpperBound := 100
    repoLocalCompletionClaimed := false
  },
  {
    packageId := "YW.P1.mathlib_object_model"
    role := "Track mathlib anchors for Measure, Filtration, Adapted, HasLaw, IdentDistrib, kernels, and process measurability."
    leafCount := 10
    leafBudgetUpperBound := 100
    repoLocalCompletionClaimed := false
  },
  {
    packageId := "YW.P2.SDE_API"
    role := "Replace abstract equation fields with the concrete local SDEIntegralInterface and SDEEquation boundary."
    leafCount := 10
    leafBudgetUpperBound := 100
    repoLocalCompletionClaimed := false
  },
  {
    packageId := "YW.P3.weak_solution"
    role := "Model weak solutions over a separate filtered probability space with rebased coefficients, laws, and equation."
    leafCount := 12
    leafBudgetUpperBound := 100
    repoLocalCompletionClaimed := false
  },
  {
    packageId := "YW.P4.pathwise_uniqueness"
    role := "State same-noise pathwise uniqueness as coordinatewise almost-everywhere equality for strong solutions."
    leafCount := 8
    leafBudgetUpperBound := 100
    repoLocalCompletionClaimed := false
  },
  {
    packageId := "YW.P5.strong_construction"
    role := "Reserve construction leaves for a strong solution as a measurable functional of initial data and driving noise."
    leafCount := 14
    leafBudgetUpperBound := 100
    repoLocalCompletionClaimed := false
  },
  {
    packageId := "YW.P6.uniqueness_in_law"
    role := "Reserve bridge leaves from pathwise uniqueness and weak existence to IdentDistrib conclusions."
    leafCount := 10
    leafBudgetUpperBound := 100
    repoLocalCompletionClaimed := false
  }
]

/-- C006 records exactly the seven requested theorem-tree packages. -/
theorem yamadaWatanabeTheoremTreePackages_length :
    yamadaWatanabeTheoremTreePackages.length = 7 := by
  rfl

/-- Every C006 package has at most 100 child leaf ledgers and at most 100 steps per leaf. -/
theorem yamadaWatanabeTheoremTreePackages_leafBudgetGate :
    ∀ pkg ∈ yamadaWatanabeTheoremTreePackages,
      pkg.leafCount <= 100 ∧ pkg.leafBudgetUpperBound <= 100 := by
  intro pkg hpkg
  simp [yamadaWatanabeTheoremTreePackages] at hpkg
  rcases hpkg with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- The C006 package split is decomposition metadata and makes no terminal completion claim. -/
theorem yamadaWatanabeTheoremTreePackages_noCompletionClaim :
    ∀ pkg ∈ yamadaWatanabeTheoremTreePackages,
      pkg.repoLocalCompletionClaimed = false := by
  intro pkg hpkg
  simp [yamadaWatanabeTheoremTreePackages] at hpkg
  rcases hpkg with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> rfl

/-- C006 status flag: the requested package split exists as a checked local ledger. -/
def theoremTreePackageSplitChecked : Bool := true

/-- C006 status flag: checked package metadata is not a terminal Yamada-Watanabe proof. -/
def theoremTreePackageSplitIsTerminalYWProof : Bool := false

theorem theoremTreePackageSplitChecked_eq_true :
    theoremTreePackageSplitChecked = true := by
  rfl

theorem theoremTreePackageSplitIsTerminalYWProof_eq_false :
    theoremTreePackageSplitIsTerminalYWProof = false := by
  rfl

/-! ## Audit probes -/

#check SDEModel
#check SDEIntegralInterface
#check DriftIntegrand
#check DiffusionIntegrand
#check SDEEquation
#check StrongSolution
#check WeakExistence
#check SDEModel.onFilteredSpace
#check WeakExistenceOnSomeFilteredSpace
#check WeakExistence.toWeakExistenceOnSomeFilteredSpace
#check statementShapeUsesSeparateWeakExistence_eq_true
#check sameSpaceWeakExistenceIsTerminalWeakBoundary_eq_false
#check separateWeakSolutionPublicNote
#check PathwiseUniqueness
#check StrongExistence
#check UniquenessInLaw
#check YamadaWatanabeConclusion
#check StatementShape
#check StatementShape.intro
#check adapted_const_process
#check adapted_coordinate_measurable
#check adapted_coordinate_aemeasurable
#check SDEModel.driftTimeIntegral_adapted
#check SDEModel.stochasticIntegral_adapted
#check SDEEquation.apply
#check hasLaw_map_eq
#check hasLaw_aemeasurable
#check hasLaw_identDistrib
#check deterministicKernel_apply
#check kolmogorovProcess_measurable_at
#check aeKolmogorovProcess_aemeasurable_at
#check DiscreteSDEAnalogue
#check DiscreteSDEAnalogue.transitionKernel_isMarkov
#check DiscreteSDEAnalogue.transitionKernel_apply
#check DiscreteSDEAnalogue.oneStepEquation
#check unitDiscreteStep
#check unitDiscreteStep_measurable
#check unitDiscreteTransitionKernel
#check unitDiscreteTransitionKernel_isMarkov
#check unitDiscreteTransitionKernel_apply
#check unitConst_hasLaw
#check unitFiniteStateDiscreteSDEAnalogue
#check unitFiniteStateDiscreteSDEAnalogue_adapted_state
#check unitFiniteStateDiscreteSDEAnalogue_state_law
#check unitFiniteStateDiscreteSDEAnalogue_noise_law
#check unitFiniteStateDiscreteSDEAnalogue_transitionKernel_isMarkov
#check unitFiniteStateDiscreteSDEAnalogue_oneStepEquation
#check finiteStateDiscreteAnalogueChecked_eq_true
#check finiteStateDiscreteAnalogueIsTerminalYWProof_eq_false
#check Filtration
#check Adapted
#check HasLaw
#check IdentDistrib
#check IsMarkovKernel
#check IsKolmogorovProcess
#check IsAEKolmogorovProcess
#check ExternalYamadaWatanabeAuditRow
#check ExternalYamadaWatanabeAuditRow.repoLocalIntegrationGate
#check externalYamadaWatanabeAuditRows
#check externalYamadaWatanabeAuditRows_length
#check externalYamadaWatanabeAuditRows_repoLocalIntegrationGate
#check externalYamadaWatanabeAuditRows_noTerminalProof
#check externalYamadaWatanabeTerminalProofFound_eq_false
#check externalYamadaWatanabeAnchorOnlyEvidenceIsCompletion_eq_false
#check externalYamadaWatanabeCompletedStateRetainsRepoLocalIntegrationDebt_eq_false
#check TheoremTreePackageLedger
#check yamadaWatanabeTheoremTreePackages
#check yamadaWatanabeTheoremTreePackages_length
#check yamadaWatanabeTheoremTreePackages_leafBudgetGate
#check yamadaWatanabeTheoremTreePackages_noCompletionClaim
#check theoremTreePackageSplitChecked_eq_true
#check theoremTreePackageSplitIsTerminalYWProof_eq_false

end S1_M_231
end Stage1
end AwesomeTheorems
