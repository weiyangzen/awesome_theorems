import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Density
import Mathlib.MeasureTheory.Function.ConditionalExpectation.RadonNikodym
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# S1-M-237 / THM-M-1044: Girsanov theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for
Girsanov's theorem: an absolutely continuous/equivalent change of probability
measure given by a likelihood process changes the drift of a martingale or
Brownian motion, and the compensated process is a martingale/Brownian motion
under the changed measure.

The pinned mathlib snapshot has the relevant measure-theory and probability
interfaces for Radon-Nikodym derivatives, densities, filtrations, adapted
processes, martingales, Gaussian processes, laws, and independent increments.
It does not expose a terminal stochastic-integral/exponential-martingale API or
a theorem named Girsanov.  The stochastic-integral bridge, Novikov/Kazamaki-type
condition, and drift-compensation identity are therefore explicit proposition
fields.  This file does not prove Girsanov's theorem.
-/

noncomputable section

open MeasureTheory
open ProbabilityTheory

open scoped NNReal ENNReal

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_237

/-- Continuous-time real-valued stochastic process indexed by nonnegative time. -/
abbrev ContinuousTimeProcess (Ω : Type u) :=
  ℝ≥0 → Ω → ℝ

/--
Radon-Nikodym density of `changed` with respect to `reference`.

For Girsanov, `reference` is usually the original probability measure and
`changed` is the tilted measure.
-/
def RadonNikodymDensity {Ω : Type u} [MeasurableSpace Ω]
    (reference changed : Measure Ω) : Ω → ℝ≥0∞ :=
  changed.rnDeriv reference

/-- The measure obtained from `reference` by the terminal likelihood `Z`. -/
def ChangedMeasureViaDensity {Ω : Type u} [MeasurableSpace Ω]
    (reference : Measure Ω) (Z : Ω → ℝ≥0∞) : Measure Ω :=
  reference.withDensity Z

/-- Two measures are equivalent when each is absolutely continuous with respect to the other. -/
def EquivalentMeasures {Ω : Type u} [MeasurableSpace Ω]
    (P Q : Measure Ω) : Prop :=
  P ≪ Q ∧ Q ≪ P

/--
Brownian-motion boundary over `ℝ≥0`.

mathlib has Gaussian-process and independent-increments predicates, but the
pinned snapshot does not provide a canonical `BrownianMotion` definition.  This
boundary is intentionally a conjunction of currently available interfaces.
-/
def BrownianMotionBoundary {Ω : Type u} [MeasurableSpace Ω]
    (B : ContinuousTimeProcess Ω) (P : Measure Ω) : Prop :=
  IsGaussianProcess B P ∧
    HasIndepIncrements B P ∧
      (∀ t : ℝ≥0, HasLaw (B t) (gaussianReal 0 t) P) ∧
        (∀ᵐ ω ∂P, B 0 ω = 0) ∧
          (∀ ω : Ω, Continuous fun t : ℝ≥0 => B t ω)

/--
Data needed to state a Girsanov-type change-of-measure theorem.

The fields named `stochasticExponentialRelation`, `stochasticIntegralBridge`,
`driftCompensation`, and `integrabilityCondition` are formalization boundaries:
they should be replaced by concrete stochastic-integral and exponential
martingale definitions once those APIs are available or pinned.
-/
structure GirsanovData (Ω : Type u) [MeasurableSpace Ω]
    (P Q : Measure Ω) : Type (u + 1) where
  filtration : Filtration ℝ≥0 ‹MeasurableSpace Ω›
  drivingProcess : ContinuousTimeProcess Ω
  shiftedProcess : ContinuousTimeProcess Ω
  likelihoodProcess : ContinuousTimeProcess Ω
  driftProcess : ContinuousTimeProcess Ω
  terminalDensity : Ω → ℝ≥0∞
  p_isProbability : IsProbabilityMeasure P
  q_isProbability : IsProbabilityMeasure Q
  q_abs_cont_p : Q ≪ P
  p_abs_cont_q : P ≪ Q
  q_eq_withDensity : Q = ChangedMeasureViaDensity P terminalDensity
  terminalDensity_rnDeriv :
    terminalDensity = RadonNikodymDensity P Q
  drivingAdapted : StronglyAdapted filtration drivingProcess
  shiftedAdapted : StronglyAdapted filtration shiftedProcess
  likelihoodAdapted : StronglyAdapted filtration likelihoodProcess
  drivingMartingale_reference : Martingale drivingProcess filtration P
  likelihoodMartingale_reference : Martingale likelihoodProcess filtration P
  drivingBrownian_reference : BrownianMotionBoundary drivingProcess P
  shiftedProcessDefinition :
    ∀ t : ℝ≥0, ∀ ω : Ω,
      shiftedProcess t ω = drivingProcess t ω - driftProcess t ω
  stochasticExponentialRelation : Prop
  stochasticIntegralBridge : Prop
  driftCompensation : Prop
  integrabilityCondition : Prop

/--
Normalized hypotheses for the Girsanov statement boundary.

The concrete theorem should instantiate these proposition fields with a
specific stochastic exponential and sufficient integrability condition.
-/
def GirsanovHypotheses {Ω : Type u} [MeasurableSpace Ω] {P Q : Measure Ω}
    (D : GirsanovData Ω P Q) : Prop :=
  D.stochasticExponentialRelation ∧
    D.stochasticIntegralBridge ∧
      D.driftCompensation ∧
        D.integrabilityCondition

/--
Normalized conclusion for the Brownian/martingale form of Girsanov.

Under the tilted measure, the compensated process should be a martingale and,
in the Brownian specialization, a Brownian motion according to the local
`BrownianMotionBoundary`.
-/
def GirsanovConclusion {Ω : Type u} [MeasurableSpace Ω] {P Q : Measure Ω}
    (D : GirsanovData Ω P Q) : Prop :=
  Martingale D.shiftedProcess D.filtration Q ∧
    BrownianMotionBoundary D.shiftedProcess Q

/--
Stage1 normalized statement shape for Girsanov's theorem.

For every pair of equivalent probability measures with a terminal
Radon-Nikodym density and a compatible likelihood process, if the likelihood is
the stochastic exponential of a drift integrand and the drift compensation
identity holds, then the compensated process is a martingale/Brownian motion
under the changed measure.

This is a formalization boundary only.  The repo-local Lean closure does not
contain the stochastic-integral proof body.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P Q : Measure Ω),
    ∀ D : GirsanovData Ω P Q,
      GirsanovHypotheses D → GirsanovConclusion D

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω] (P Q : Measure Ω),
      ∀ D : GirsanovData Ω P Q,
        GirsanovHypotheses D → GirsanovConclusion D) :
    StatementShape.{u} :=
  h

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω] (P Q : Measure Ω),
        ∀ D : GirsanovData Ω P Q,
          GirsanovHypotheses D → GirsanovConclusion D :=
  Iff.rfl

/-- A density-defined measure is absolutely continuous with respect to its reference measure. -/
theorem changedMeasure_absolutelyContinuous {Ω : Type u} [MeasurableSpace Ω]
    (P : Measure Ω) (Z : Ω → ℝ≥0∞) :
    ChangedMeasureViaDensity P Z ≪ P := by
  exact withDensity_absolutelyContinuous P Z

/-- `RadonNikodymDensity` is only a named wrapper around mathlib's `Measure.rnDeriv`. -/
theorem radonNikodymDensity_def {Ω : Type u} [MeasurableSpace Ω]
    (P Q : Measure Ω) :
    RadonNikodymDensity P Q = Q.rnDeriv P :=
  rfl

/-- `ChangedMeasureViaDensity` is only a named wrapper around mathlib's `Measure.withDensity`. -/
theorem changedMeasureViaDensity_def {Ω : Type u} [MeasurableSpace Ω]
    (P : Measure Ω) (Z : Ω → ℝ≥0∞) :
    ChangedMeasureViaDensity P Z = P.withDensity Z :=
  rfl

/-- A packaged Girsanov datum exposes equivalence of the two measures. -/
theorem equivalentMeasures_of_data {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) :
    EquivalentMeasures P Q :=
  ⟨D.p_abs_cont_q, D.q_abs_cont_p⟩

/-- A packaged Girsanov datum exposes the changed-measure density equation. -/
theorem changedMeasure_eq_of_data {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) :
    Q = ChangedMeasureViaDensity P D.terminalDensity :=
  D.q_eq_withDensity

/-- A packaged Girsanov datum exposes its terminal density as the Radon-Nikodym derivative. -/
theorem terminalDensity_eq_rnDeriv {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) :
    D.terminalDensity = RadonNikodymDensity P Q :=
  D.terminalDensity_rnDeriv

/-- A packaged Girsanov datum exposes the reference-measure driving martingale. -/
theorem drivingMartingale_reference {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) :
    Martingale D.drivingProcess D.filtration P :=
  D.drivingMartingale_reference

/-- A packaged Girsanov datum exposes the likelihood-process martingale. -/
theorem likelihoodMartingale_reference {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) :
    Martingale D.likelihoodProcess D.filtration P :=
  D.likelihoodMartingale_reference

/-- The Brownian-motion boundary exposes the Gaussian-process component. -/
theorem BrownianMotionBoundary.isGaussianProcess {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : BrownianMotionBoundary B P) :
    IsGaussianProcess B P :=
  hB.1

/-- The Brownian-motion boundary exposes independent increments. -/
theorem BrownianMotionBoundary.hasIndepIncrements {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : BrownianMotionBoundary B P) :
    HasIndepIncrements B P :=
  hB.2.1

/-- The Brownian-motion boundary exposes one-dimensional Gaussian marginals. -/
theorem BrownianMotionBoundary.hasLaw_gaussianReal {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : BrownianMotionBoundary B P) (t : ℝ≥0) :
    HasLaw (B t) (gaussianReal 0 t) P :=
  hB.2.2.1 t

/-- The Brownian-motion boundary exposes the a.e. zero initial value. -/
theorem BrownianMotionBoundary.origin_zero_ae {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : BrownianMotionBoundary B P) :
    ∀ᵐ ω ∂P, B 0 ω = 0 :=
  hB.2.2.2.1

/-- The Brownian-motion boundary exposes path continuity. -/
theorem BrownianMotionBoundary.continuous_paths {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hB : BrownianMotionBoundary B P) :
    ∀ ω : Ω, Continuous fun t : ℝ≥0 => B t ω :=
  hB.2.2.2.2

/-- Assemble the local Brownian-motion boundary from its five checked components. -/
theorem BrownianMotionBoundary.intro {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω}
    (hGaussian : IsGaussianProcess B P)
    (hIndep : HasIndepIncrements B P)
    (hLaw : ∀ t : ℝ≥0, HasLaw (B t) (gaussianReal 0 t) P)
    (hOrigin : ∀ᵐ ω ∂P, B 0 ω = 0)
    (hContinuous : ∀ ω : Ω, Continuous fun t : ℝ≥0 => B t ω) :
    BrownianMotionBoundary B P :=
  ⟨hGaussian, hIndep, hLaw, hOrigin, hContinuous⟩

/-- The local Brownian-motion boundary is exactly the available mathlib component package. -/
theorem brownianMotionBoundary_iff_components {Ω : Type u} [MeasurableSpace Ω]
    {P : Measure Ω} {B : ContinuousTimeProcess Ω} :
    BrownianMotionBoundary B P ↔
      IsGaussianProcess B P ∧
        HasIndepIncrements B P ∧
          (∀ t : ℝ≥0, HasLaw (B t) (gaussianReal 0 t) P) ∧
            (∀ᵐ ω ∂P, B 0 ω = 0) ∧
              (∀ ω : Ω, Continuous fun t : ℝ≥0 => B t ω) :=
  Iff.rfl

/-- A Girsanov conclusion exposes the changed-measure martingale branch. -/
theorem GirsanovConclusion.shiftedMartingale {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (h : GirsanovConclusion D) :
    Martingale D.shiftedProcess D.filtration Q :=
  h.1

/-- A Girsanov conclusion exposes the Brownian-motion branch under the changed measure. -/
theorem GirsanovConclusion.shiftedBrownian {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (h : GirsanovConclusion D) :
    BrownianMotionBoundary D.shiftedProcess Q :=
  h.2

/-- The shifted Brownian boundary exposes its Gaussian-process component under `Q`. -/
theorem GirsanovConclusion.shiftedBrownian_isGaussianProcess {Ω : Type u}
    [MeasurableSpace Ω] {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (h : GirsanovConclusion D) :
    IsGaussianProcess D.shiftedProcess Q :=
  BrownianMotionBoundary.isGaussianProcess h.2

/-- The shifted Brownian boundary exposes independent increments under `Q`. -/
theorem GirsanovConclusion.shiftedBrownian_hasIndepIncrements {Ω : Type u}
    [MeasurableSpace Ω] {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (h : GirsanovConclusion D) :
    HasIndepIncrements D.shiftedProcess Q :=
  BrownianMotionBoundary.hasIndepIncrements h.2

/-- The shifted Brownian boundary exposes Gaussian marginals under `Q`. -/
theorem GirsanovConclusion.shiftedBrownian_hasLaw_gaussianReal {Ω : Type u}
    [MeasurableSpace Ω] {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (h : GirsanovConclusion D) (t : ℝ≥0) :
    HasLaw (D.shiftedProcess t) (gaussianReal 0 t) Q :=
  BrownianMotionBoundary.hasLaw_gaussianReal h.2 t

/-- The shifted Brownian boundary exposes the a.e. zero initial value under `Q`. -/
theorem GirsanovConclusion.shiftedBrownian_origin_zero_ae {Ω : Type u}
    [MeasurableSpace Ω] {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (h : GirsanovConclusion D) :
    ∀ᵐ ω ∂Q, D.shiftedProcess 0 ω = 0 :=
  BrownianMotionBoundary.origin_zero_ae h.2

/-- The shifted Brownian boundary exposes path continuity for the shifted process. -/
theorem GirsanovConclusion.shiftedBrownian_continuous_paths {Ω : Type u}
    [MeasurableSpace Ω] {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (h : GirsanovConclusion D) :
    ∀ ω : Ω, Continuous fun t : ℝ≥0 => D.shiftedProcess t ω :=
  BrownianMotionBoundary.continuous_paths h.2

/-! ## C006 shifted Brownian boundary route. -/

/--
Route for the C006 Brownian-boundary child.

The local mathlib snapshot has Gaussian-process, independent-increments, law,
and path-continuity interfaces, but no canonical `BrownianMotion` API found by
local source search.  The safe route is therefore to keep the local boundary
and make its component obligations explicit.
-/
inductive BrownianBoundaryRoute where
  | keepLocalBoundary
  | replaceWithMathlibBrownian
deriving DecidableEq

/-- C006 route: keep the local component boundary in this pinned mathlib snapshot. -/
def selectedBrownianBoundaryRoute : BrownianBoundaryRoute :=
  BrownianBoundaryRoute.keepLocalBoundary

/-- C006 did not replace the boundary with a canonical mathlib Brownian API. -/
theorem selectedBrownianBoundaryRoute_not_replace :
    selectedBrownianBoundaryRoute ≠ BrownianBoundaryRoute.replaceWithMathlibBrownian := by
  intro h
  cases h

/-- Local source search did not find a canonical mathlib `BrownianMotion` API. -/
def canonicalMathlibBrownianAPIFound : Bool :=
  false

/-- C006 records that no canonical mathlib Brownian API was available locally. -/
theorem canonicalMathlibBrownianAPIFound_eq_false :
    canonicalMathlibBrownianAPIFound = false :=
  rfl

/-- Local mathlib search terms used for the C006 Brownian-boundary route. -/
def brownianBoundaryLocalSearchTerms : List String := [
  "Brownian",
  "brownian",
  "BrownianMotion",
  "Wiener",
  "WienerProcess"
]

/-- Remaining obligations after C006 component-boundary closure. -/
def brownianBoundaryRemainingObligations : List String := [
  "derive IsGaussianProcess D.shiftedProcess Q from the measure-change and drift-compensation proof",
  "derive HasIndepIncrements D.shiftedProcess Q from the measure-change and drift-compensation proof",
  "derive HasLaw (D.shiftedProcess t) (gaussianReal 0 t) Q for every t",
  "derive Q-a.e. zero initial value for D.shiftedProcess from the shifted-process definition",
  "derive path continuity for D.shiftedProcess from the driving and drift processes",
  "replace the local component boundary with a canonical mathlib Brownian API if one becomes available and validates locally"
]

/-! ## Audit probes retained in the checked file. -/

#check Measure.rnDeriv
#check Measure.withDensity
#check withDensity_absolutelyContinuous
#check Measure.absolutelyContinuous_rfl
#check Filtration
#check StronglyAdapted
#check Martingale
#check Martingale.integrable
#check IsGaussianProcess
#check HasIndepIncrements
#check HasLaw
#check gaussianReal
#check RadonNikodymDensity
#check ChangedMeasureViaDensity
#check EquivalentMeasures
#check BrownianMotionBoundary
#check BrownianMotionBoundary.intro
#check brownianMotionBoundary_iff_components
#check BrownianMotionBoundary.origin_zero_ae
#check BrownianMotionBoundary.continuous_paths
#check GirsanovConclusion.shiftedBrownian_isGaussianProcess
#check GirsanovConclusion.shiftedBrownian_hasIndepIncrements
#check GirsanovConclusion.shiftedBrownian_hasLaw_gaussianReal
#check GirsanovConclusion.shiftedBrownian_origin_zero_ae
#check GirsanovConclusion.shiftedBrownian_continuous_paths
#check BrownianBoundaryRoute
#check selectedBrownianBoundaryRoute
#check selectedBrownianBoundaryRoute_not_replace
#check canonicalMathlibBrownianAPIFound_eq_false
#check brownianBoundaryRemainingObligations
#check GirsanovData
#check StatementShape

/-- mathlib revision used for the Stage1 C002 anchor audit. -/
def mathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Exact requested anchor probes for `THM-M-1044.mathlib-audit`.

The `#check` commands above are the kernel-checked audit surface; this list is
retained as data so the child ledger and later public backfill can quote the
same anchor set without implying that Girsanov itself has been proved here.
-/
def requestedMathlibAnchorProbes : List String := [
  "Measure.rnDeriv",
  "Measure.withDensity",
  "withDensity_absolutelyContinuous",
  "Filtration",
  "StronglyAdapted",
  "Martingale",
  "IsGaussianProcess",
  "HasIndepIncrements",
  "HasLaw",
  "gaussianReal"
]

/--
Boundary retained with the audit: this Stage1 file checks the available
mathlib anchors and local statement-shape wrappers, but it does not provide a
stochastic-integral proof of Girsanov's theorem.
-/
def mathlibAuditBoundary : String :=
  "anchor audit only; not a proof of Girsanov"

/-- mathlib modules checked while locating repo-local Girsanov anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym",
  "Mathlib.MeasureTheory.Measure.WithDensity",
  "Mathlib.MeasureTheory.Function.ConditionalExpectation.RadonNikodym",
  "Mathlib.Probability.Density",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Predictable",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Independence.Process.HasIndepIncrements",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Kernel.RadonNikodym",
  "Mathlib.Probability.Kernel.WithDensity"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Measure.rnDeriv",
  "MeasureTheory.Measure.withDensity",
  "MeasureTheory.withDensity_absolutelyContinuous",
  "MeasureTheory.Filtration",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "ProbabilityTheory.IsGaussianProcess",
  "ProbabilityTheory.HasIndepIncrements",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.gaussianReal"
]

/-- Search terms that did not locate a terminal Girsanov proof in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Girsanov",
  "Cameron-Martin-Girsanov",
  "stochastic exponential",
  "StochasticExponential",
  "Doleans",
  "Doléans",
  "Novikov",
  "Kazamaki",
  "stochastic integral",
  "StochasticIntegral",
  "semimartingale",
  "local martingale",
  "Brownian"
]

/-! ## C003 stochastic-integral API decision. -/

/--
Route chosen for the stochastic-integral/exponential-martingale API gap.

The `buildRepoLocalBoundary` route means: keep the current repo-local
statement-boundary fields and split future concrete stochastic-integral,
stochastic-exponential, Novikov/Kazamaki, and measure-change bridges into
local `<=100` leaves, instead of treating an unimported or unfinished external
project as completed evidence.
-/
inductive StochasticIntegralAPIRoute where
  | buildRepoLocalBoundary
  | pinExternalCompletedProject
  | waitForMathlib
deriving DecidableEq

/--
C003 decision: do not pin an external project as a completed upstream API in
the current repo-local validation closure.
-/
def selectedStochasticIntegralAPIRoute : StochasticIntegralAPIRoute :=
  StochasticIntegralAPIRoute.buildRepoLocalBoundary

/-- The C003 decision did not select an external project as completed evidence. -/
theorem selectedStochasticIntegralAPIRoute_not_external :
    selectedStochasticIntegralAPIRoute ≠
      StochasticIntegralAPIRoute.pinExternalCompletedProject := by
  intro h
  cases h

/-- The C003 decision did not defer the boundary to a future mathlib API. -/
theorem selectedStochasticIntegralAPIRoute_not_waitForMathlib :
    selectedStochasticIntegralAPIRoute ≠
      StochasticIntegralAPIRoute.waitForMathlib := by
  intro h
  cases h

/--
Primary-source external candidate audited for the C003 API decision.

The candidate has useful adjacent stochastic-calculus source files, but it is
not a terminal Girsanov/stochastic-exponential dependency for this repository.
-/
def stochasticIntegralExternalCandidate : List String := [
  "repository: https://github.com/RemyDegenne/brownian-motion",
  "audited commit: 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "commit date: 2026-05-01T06:05:08Z",
  "lean-toolchain: leanprover/lean4:v4.30.0-rc1",
  "mathlib dependency: f23306121184717ace04f3ac514be974e3224c8b",
  "kolmogorov_extension4 dependency: e236e968c2b038b952444df54075a6e8b1058380"
]

/--
Positive adjacent anchors found in the external candidate.

These are not imported here and do not prove Girsanov.  They only identify a
possible future source for local API design or a later compatible dependency
pin.
-/
def stochasticIntegralExternalAdjacentAnchors : List String := [
  "BrownianMotion.lean imports BrownianMotion.StochasticIntegral.* modules",
  "BrownianMotion/StochasticIntegral/LocalMartingale.lean defines ProbabilityTheory.IsLocalMartingale",
  "BrownianMotion/StochasticIntegral/DoobMeyer.lean states ProbabilityTheory.IsLocalSubmartingale.doob_meyer",
  "BrownianMotion/StochasticIntegral/QuadraticVariation.lean defines ProbabilityTheory.quadraticVariation",
  "BrownianMotion/StochasticIntegral/SimpleProcess.lean defines ProbabilityTheory.SimpleProcess.integral",
  "BrownianMotion/StochasticIntegral/SimpleProcess.lean defines ProbabilityTheory.SimpleProcess.integralEval",
  "BrownianMotion/StochasticIntegral/L2M.lean defines ProbabilityTheory.L2Predictable"
]

/--
Negative terminal search results for C003.

No exact terminal Girsanov, stochastic-exponential, or exponential-martingale
proof anchor was located in the audited external Lean sources.
-/
def stochasticIntegralExternalNegativeSearchResults : List String := [
  "Girsanov: no primary Lean source match",
  "Cameron-Martin-Girsanov: no primary Lean source match",
  "Novikov: no primary Lean source match",
  "Kazamaki: no primary Lean source match",
  "StochasticExponential: no primary Lean source match",
  "stochastic exponential: no primary Lean source match",
  "Doleans/Doléans/Dade: no primary Lean source match",
  "exponential martingale: no primary Lean source match",
  "Semimartingale: no primary Lean source match"
]

/--
Concrete blockers against pinning the external candidate as a completed API.

These blockers are integration blockers, not completed evidence.  They keep
the parent theorem in formalization debt rather than repo-local integration
debt.
-/
def stochasticIntegralExternalIntegrationBlockers : List String := [
  "No terminal theorem or API for Girsanov was found.",
  "No Doleans-Dade/stochastic-exponential construction was found.",
  "No Novikov/Kazamaki exponential-martingale theorem was found.",
  "The external stochastic-integral subtree contains unclosed proof placeholders, including QuadraticVariation.lean, DoobMeyer.lean, OptionalSampling.lean, SquareIntegrable.lean, UniformIntegrable.lean, Komlos.lean, and LocalMartingale.lean.",
  "The external project uses Lean 4.30.0-rc1 and mathlib f23306121184717ace04f3ac514be974e3224c8b, while this repository currently validates against Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "The external project is not pinned/imported into this repository's Lake closure.",
  "A future pin would still need a checked repo-local wrapper theorem before any completion claim."
]

/-- No exact external terminal Girsanov/stochastic-exponential proof was found by C003. -/
def externalTerminalStochasticAPIProofFound : Bool :=
  false

/-- Anchor-only external stochastic-integral evidence is not repo-local completion evidence. -/
def externalStochasticAPIAnchorOnlyEvidenceIsCompletion : Bool :=
  false

/-- C003 repo-local integration-debt gate for the external API audit. -/
theorem externalTerminalStochasticAPIProofFound_eq_false :
    externalTerminalStochasticAPIProofFound = false :=
  rfl

/-- C003 records that anchor-only external evidence cannot close the parent theorem. -/
theorem externalStochasticAPIAnchorOnlyEvidenceIsCompletion_eq_false :
    externalStochasticAPIAnchorOnlyEvidenceIsCompletion = false :=
  rfl

/-! ## C004 Novikov/Kazamaki leaf package. -/

/--
Concrete finite-horizon data for a Novikov/Kazamaki-type sufficient condition
inside the Girsanov statement boundary.

The two concrete conditions below are:
* Novikov: integrability of `exp(1 / 2 * <M>_T)`;
* Kazamaki type: submartingality of `exp(M_t / 2)`.

The current repository does not yet construct the driver `M`, its quadratic
variation, or the Doléans-Dade stochastic exponential from a stochastic
integral.  Those construction and identification steps remain explicit bridge
fields rather than hidden axioms.
-/
structure NovikovKazamakiLeafData {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) : Type (u + 1) where
  terminalTime : ℝ≥0
  exponentialDriver : ContinuousTimeProcess Ω
  quadraticVariation : ContinuousTimeProcess Ω
  driverAdapted : StronglyAdapted D.filtration exponentialDriver
  quadraticVariationAdapted : StronglyAdapted D.filtration quadraticVariation
  quadraticVariationNonnegative : ∀ t : ℝ≥0, 0 ≤ᵐ[P] quadraticVariation t
  likelihoodFormula :
    ∀ t : ℝ≥0,
      D.likelihoodProcess t =ᵐ[P]
        fun ω => Real.exp
          (exponentialDriver t ω - ((1 : ℝ) / 2) * quadraticVariation t ω)
  terminalDensityFormula :
    D.terminalDensity =
      fun ω => ENNReal.ofReal
        (Real.exp
          (exponentialDriver terminalTime ω -
            ((1 : ℝ) / 2) * quadraticVariation terminalTime ω))

/-- The terminal Novikov weight `exp(1 / 2 * <M>_T)`. -/
def novikovKazamakiTerminalWeight {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (N : NovikovKazamakiLeafData D) : Ω → ℝ :=
  fun ω => Real.exp (((1 : ℝ) / 2) * N.quadraticVariation N.terminalTime ω)

/-- The half-exponential process used by Kazamaki-type criteria. -/
def kazamakiHalfExponential {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (N : NovikovKazamakiLeafData D) : ContinuousTimeProcess Ω :=
  fun t ω => Real.exp (N.exponentialDriver t ω / 2)

/--
Concrete leaf condition available to a later Girsanov proof.

Either branch is intentionally stated with current repo-local APIs.  The
Novikov branch is an `Integrable` statement over the terminal exponential
weight; the Kazamaki branch is a `Submartingale` statement for the
half-exponential process.
-/
def NovikovKazamakiLeafCondition {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (N : NovikovKazamakiLeafData D) : Prop :=
  Integrable (novikovKazamakiTerminalWeight N) P ∨
    Submartingale (kazamakiHalfExponential N) D.filtration P

/--
Package that connects a concrete Novikov/Kazamaki condition to the
`GirsanovData.integrabilityCondition` field.

The bridge field is the remaining stochastic-calculus proof obligation: a
future terminal proof must replace it with a construction or a pinned upstream
theorem, not with anchor-only evidence.
-/
structure NovikovKazamakiLeafPackage {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) : Type (u + 1) where
  data : NovikovKazamakiLeafData D
  condition : NovikovKazamakiLeafCondition data
  conditionSuppliesGirsanovIntegrability :
    NovikovKazamakiLeafCondition data → D.integrabilityCondition

/-- The Novikov branch supplies the concrete leaf condition. -/
theorem NovikovKazamakiLeafCondition.of_novikov {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (N : NovikovKazamakiLeafData D)
    (h : Integrable (novikovKazamakiTerminalWeight N) P) :
    NovikovKazamakiLeafCondition N :=
  Or.inl h

/-- The Kazamaki-type branch supplies the concrete leaf condition. -/
theorem NovikovKazamakiLeafCondition.of_kazamaki {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (N : NovikovKazamakiLeafData D)
    (h : Submartingale (kazamakiHalfExponential N) D.filtration P) :
    NovikovKazamakiLeafCondition N :=
  Or.inr h

/-- The packaged leaf exposes the Girsanov integrability condition. -/
theorem novikovKazamakiLeaf_integrabilityCondition {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (L : NovikovKazamakiLeafPackage D) :
    D.integrabilityCondition :=
  L.conditionSuppliesGirsanovIntegrability L.condition

/-- The packaged leaf exposes the terminal density formula. -/
theorem novikovKazamakiLeaf_terminalDensityFormula {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (L : NovikovKazamakiLeafPackage D) :
    D.terminalDensity =
      fun ω => ENNReal.ofReal
        (Real.exp
          (L.data.exponentialDriver L.data.terminalTime ω -
            ((1 : ℝ) / 2) * L.data.quadraticVariation L.data.terminalTime ω)) :=
  L.data.terminalDensityFormula

/-- The packaged leaf exposes the likelihood stochastic-exponential formula. -/
theorem novikovKazamakiLeaf_likelihoodFormula {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} {D : GirsanovData Ω P Q}
    (L : NovikovKazamakiLeafPackage D) (t : ℝ≥0) :
    D.likelihoodProcess t =ᵐ[P]
      fun ω => Real.exp
        (L.data.exponentialDriver t ω -
          ((1 : ℝ) / 2) * L.data.quadraticVariation t ω) :=
  L.data.likelihoodFormula t

/-- The C004 package is not a terminal proof of Girsanov or of Novikov/Kazamaki. -/
def novikovKazamakiLeafIsTerminalProof : Bool :=
  false

/-- C004 non-terminal proof gate. -/
theorem novikovKazamakiLeafIsTerminalProof_eq_false :
    novikovKazamakiLeafIsTerminalProof = false :=
  rfl

/-- Remaining proof obligations after the C004 checked leaf package. -/
def novikovKazamakiLeafRemainingObligations : List String := [
  "construct or pin the stochastic integral and Doleans-Dade stochastic exponential",
  "identify the supplied quadratic-variation process with the stochastic bracket",
  "prove or pin Novikov/Kazamaki implies true martingality for the stochastic exponential",
  "replace conditionSuppliesGirsanovIntegrability with a proof body or pinned wrapper theorem"
]

/-! ## C005 conditional-expectation/Radon-Nikodym measure-change bridge. -/

/--
Conditional density of `Q` relative to `P` on a sub-sigma-algebra, expressed
as the Radon-Nikodym derivative of trimmed measures.
-/
def ConditionalDensityTrimmed {Ω : Type u} {mΩ : MeasurableSpace Ω}
    (P Q : @Measure Ω mΩ) (subm : MeasurableSpace Ω)
    (hm : subm ≤ mΩ) : Ω → ℝ :=
  fun ω => ((Q.trim hm).rnDeriv (P.trim hm) ω).toReal

/--
Conditional density of `Q` relative to `P` on a sub-sigma-algebra, expressed
as a conditional expectation under `P`.
-/
def ConditionalDensityByCondExp {Ω : Type u} {mΩ : MeasurableSpace Ω}
    (P Q : @Measure Ω mΩ) (subm : MeasurableSpace Ω) : Ω → ℝ :=
  letI : MeasurableSpace Ω := mΩ
  P[fun ω => (Q.rnDeriv P ω).toReal | subm]

/--
The numerator in the Bayes formula for transferring conditional expectations
from `P` to `Q`.
-/
def MeasureChangeBayesNumerator {Ω : Type u} {mΩ : MeasurableSpace Ω}
    (P Q : @Measure Ω mΩ) (subm : MeasurableSpace Ω) (X : Ω → ℝ) : Ω → ℝ :=
  letI : MeasurableSpace Ω := mΩ
  P[fun ω => X ω * (Q.rnDeriv P ω).toReal | subm]

/--
Bayes quotient expected for conditional expectations under a changed measure.

This definition records the target shape needed for the changed-measure
martingale proof.  The checked bridge below proves the RN/conditional-density
identity supplied by mathlib; the full quotient theorem still requires the
integrability and nonzero-denominator hypotheses appropriate to the later
martingale step.
-/
def MeasureChangeBayesQuotient {Ω : Type u} {mΩ : MeasurableSpace Ω}
    (P Q : @Measure Ω mΩ) (subm : MeasurableSpace Ω) (X : Ω → ℝ) : Ω → ℝ :=
  fun ω =>
    MeasureChangeBayesNumerator P Q subm X ω /
      ConditionalDensityByCondExp P Q subm ω

/-- Integration against a density-defined changed measure unfolds to weighted integration. -/
theorem changedMeasure_lintegral_eq_lintegral_mul {Ω : Type u} [MeasurableSpace Ω]
    (P : Measure Ω) {Z f : Ω → ℝ≥0∞}
    (hZ : Measurable Z) (hf : Measurable f) :
    ∫⁻ ω, f ω ∂ChangedMeasureViaDensity P Z =
      ∫⁻ ω, (Z * f) ω ∂P := by
  simpa [ChangedMeasureViaDensity] using
    (lintegral_withDensity_eq_lintegral_mul P hZ hf)

/-- Set integration against a density-defined changed measure unfolds to weighted integration. -/
theorem changedMeasure_setLIntegral_eq_setLIntegral_mul {Ω : Type u}
    [MeasurableSpace Ω] (P : Measure Ω) {Z f : Ω → ℝ≥0∞}
    (hZ : Measurable Z) (hf : Measurable f) {s : Set Ω}
    (hs : MeasurableSet s) :
    ∫⁻ ω in s, f ω ∂ChangedMeasureViaDensity P Z =
      ∫⁻ ω in s, (Z * f) ω ∂P := by
  simpa [ChangedMeasureViaDensity] using
    (setLIntegral_withDensity_eq_setLIntegral_mul P hZ hf hs)

/-- The RN derivative of a density-defined changed measure is the supplied density. -/
theorem changedMeasure_rnDeriv_eq_density {Ω : Type u} [MeasurableSpace Ω]
    (P : Measure Ω) [SigmaFinite P] {Z : Ω → ℝ≥0∞}
    (hZ : Measurable Z) :
    RadonNikodymDensity P (ChangedMeasureViaDensity P Z) =ᵐ[P] Z := by
  simpa [RadonNikodymDensity, ChangedMeasureViaDensity] using
    (Measure.rnDeriv_withDensity P hZ)

/--
mathlib-backed conditional-expectation/Radon-Nikodym bridge.

For `Q ≪ P`, the RN derivative of the trimmed measures on a sub-sigma-algebra
is the `P`-conditional expectation of the terminal RN derivative.  This is the
repo-local checked bridge needed before a later Bayes-quotient martingale
transfer can be proved.
-/
theorem conditionalDensity_trimmed_ae_eq_condExp {Ω : Type u}
    {mΩ : MeasurableSpace Ω} {P Q : @Measure Ω mΩ}
    (subm : MeasurableSpace Ω) (hm : subm ≤ mΩ) [IsFiniteMeasure Q]
    [SigmaFinite (P.trim hm)] (hQP : Q ≪ P) :
    ConditionalDensityTrimmed P Q subm hm =ᵐ[P.trim hm]
      ConditionalDensityByCondExp P Q subm := by
  letI : MeasurableSpace Ω := mΩ
  exact toReal_rnDeriv_trim hm hQP

/-- The packaged terminal density is a.e. the RN derivative used by the bridge. -/
theorem terminalDensity_ae_eq_rnDeriv_of_data {Ω : Type u} [MeasurableSpace Ω]
    {P Q : Measure Ω} (D : GirsanovData Ω P Q) :
    D.terminalDensity =ᵐ[P] fun ω => Q.rnDeriv P ω := by
  rw [D.terminalDensity_rnDeriv, RadonNikodymDensity]

/--
Target statement for the later Bayes quotient conditional-expectation theorem.

This is retained as a proposition, not asserted as proved.  Closing it will
require the exact integrability and positivity hypotheses for the denominator
before deriving the changed-measure martingale property.
-/
def MeasureChangeBayesBridgeTarget {Ω : Type u} {mΩ : MeasurableSpace Ω}
    (P Q : @Measure Ω mΩ) (subm : MeasurableSpace Ω) : Prop :=
  letI : MeasurableSpace Ω := mΩ
  ∀ X : Ω → ℝ,
    Integrable X Q →
      Q[X | subm] =ᵐ[Q] MeasureChangeBayesQuotient P Q subm X

/-- C005 checked bridge is not a terminal proof of the changed-measure martingale step. -/
def measureChangeBridgeIsTerminalMartingaleProof : Bool :=
  false

/-- C005 non-terminal proof gate. -/
theorem measureChangeBridgeIsTerminalMartingaleProof_eq_false :
    measureChangeBridgeIsTerminalMartingaleProof = false :=
  rfl

/-- Remaining proof obligations after the C005 checked RN/conditional-density bridge. -/
def measureChangeBridgeRemainingObligations : List String := [
  "add integrability hypotheses for the Bayes numerator X * dQ/dP under P",
  "prove the Bayes quotient conditional-expectation identity under Q",
  "prove positivity or nonzero denominator hypotheses for the conditional density",
  "instantiate the quotient bridge for the shifted process increments",
  "derive Martingale D.shiftedProcess D.filtration Q from the bridge and drift-compensation identity"
]

/-! ## C007 external Girsanov integration gate. -/

/--
Repo-local status options for the external-proof integration gate.

Only `pinnedAndChecked` can support completion.  The current C007 status is
`noTerminalProofFound`, so this artifact remains a statement boundary plus
checked local scaffolding, not a proof of Girsanov's theorem.
-/
inductive ExternalGirsanovIntegrationStatus where
  | noTerminalProofFound
  | exactProofBlocked
  | pinnedAndChecked
deriving DecidableEq

/-- C007 status: no terminal external Lean 4 Girsanov proof was found to pin. -/
def c007ExternalGirsanovIntegrationStatus : ExternalGirsanovIntegrationStatus :=
  ExternalGirsanovIntegrationStatus.noTerminalProofFound

/-- C007 did not pin/import/check an external Girsanov proof. -/
theorem c007ExternalGirsanovIntegrationStatus_not_pinned :
    c007ExternalGirsanovIntegrationStatus ≠
      ExternalGirsanovIntegrationStatus.pinnedAndChecked := by
  intro h
  cases h

/-- C007 search terms for terminal external Lean 4 Girsanov evidence. -/
def c007ExternalGirsanovSearchTerms : List String := [
  "Girsanov",
  "Cameron-Martin-Girsanov",
  "CameronMartinGirsanov",
  "StochasticExponential",
  "stochastic exponential",
  "Doleans-Dade",
  "Doléans-Dade",
  "Novikov",
  "Kazamaki",
  "Semimartingale"
]

/-- C007 primary-source audit findings. -/
def c007ExternalGirsanovAuditFindings : List String := [
  "local pinned mathlib@8a178386ffc0f5fef0b77738bb5449d50efeea95 has no terminal Girsanov theorem or stochastic-exponential API found by local source search",
  "GitHub CLI code search was blocked because gh is not authenticated in this worker environment",
  "GitHub REST code search for Girsanov language:Lean returned 401 Requires authentication",
  "GitHub repository search for Girsanov Lean4 returned total_count 0",
  "RemyDegenne/brownian-motion is adjacent stochastic-analysis infrastructure, not a terminal Girsanov proof",
  "RemyDegenne/brownian-motion README says stochastic integrals and Ito's lemma are in progress",
  "repo-local import probe for BrownianMotion.Gaussian.BrownianMotion failed with unknown module prefix BrownianMotion"
]

/-- Concrete C007 blockers against treating external evidence as completed. -/
def c007ExternalGirsanovIntegrationBlockers : List String := [
  "No exact external Lean 4 theorem named or identified as Girsanov was found.",
  "No external Lean 4 Cameron-Martin-Girsanov theorem was found.",
  "No external stochastic-exponential or Novikov/Kazamaki theorem sufficient to close Girsanov was found.",
  "The adjacent RemyDegenne/brownian-motion project uses leanprover/lean4:v4.30.0-rc1 and mathlib f23306121184717ace04f3ac514be974e3224c8b, while this repository validates with Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "The adjacent BrownianMotion package is not a Lake dependency of this repository; importing BrownianMotion.Gaussian.BrownianMotion fails locally.",
  "Completion still requires local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned validation."
]

/-- Anchor-only or adjacent external evidence is not completion evidence for C007. -/
def c007AnchorOnlyExternalEvidenceIsCompletion : Bool :=
  false

/-- C007 records that no terminal external Lean 4 Girsanov proof was integrated. -/
def c007TerminalExternalGirsanovProofIntegrated : Bool :=
  false

/-- C007 repo-local integration-debt gate result. -/
def c007RepoLocalIntegrationDebtGateResult : String :=
  "pass_noncompletion: no completed state is claimed, no terminal external Lean 4 Girsanov proof was found, and anchor-only adjacent evidence is not completion evidence"

/-- C007 proof that anchor-only external evidence is not completion evidence. -/
theorem c007AnchorOnlyExternalEvidenceIsCompletion_eq_false :
    c007AnchorOnlyExternalEvidenceIsCompletion = false :=
  rfl

/-- C007 proof that no terminal external Girsanov proof was integrated. -/
theorem c007TerminalExternalGirsanovProofIntegrated_eq_false :
    c007TerminalExternalGirsanovProofIntegrated = false :=
  rfl

#check StochasticIntegralAPIRoute
#check selectedStochasticIntegralAPIRoute
#check selectedStochasticIntegralAPIRoute_not_external
#check selectedStochasticIntegralAPIRoute_not_waitForMathlib
#check stochasticIntegralExternalCandidate
#check stochasticIntegralExternalAdjacentAnchors
#check stochasticIntegralExternalNegativeSearchResults
#check stochasticIntegralExternalIntegrationBlockers
#check externalTerminalStochasticAPIProofFound_eq_false
#check NovikovKazamakiLeafData
#check NovikovKazamakiLeafPackage
#check NovikovKazamakiLeafCondition.of_novikov
#check NovikovKazamakiLeafCondition.of_kazamaki
#check novikovKazamakiLeaf_integrabilityCondition
#check novikovKazamakiLeafIsTerminalProof_eq_false
#check ConditionalDensityTrimmed
#check ConditionalDensityByCondExp
#check MeasureChangeBayesNumerator
#check MeasureChangeBayesQuotient
#check changedMeasure_lintegral_eq_lintegral_mul
#check changedMeasure_setLIntegral_eq_setLIntegral_mul
#check changedMeasure_rnDeriv_eq_density
#check conditionalDensity_trimmed_ae_eq_condExp
#check terminalDensity_ae_eq_rnDeriv_of_data
#check MeasureChangeBayesBridgeTarget
#check measureChangeBridgeIsTerminalMartingaleProof_eq_false
#check ExternalGirsanovIntegrationStatus
#check c007ExternalGirsanovIntegrationStatus
#check c007ExternalGirsanovIntegrationStatus_not_pinned
#check c007ExternalGirsanovSearchTerms
#check c007ExternalGirsanovAuditFindings
#check c007ExternalGirsanovIntegrationBlockers
#check c007AnchorOnlyExternalEvidenceIsCompletion_eq_false
#check c007TerminalExternalGirsanovProofIntegrated_eq_false
#check c007RepoLocalIntegrationDebtGateResult

end S1_M_237
end Stage1
end AwesomeTheorems
