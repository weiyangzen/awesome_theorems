import Mathlib.Probability.Kernel.Invariance
import Mathlib.Probability.Kernel.IonescuTulcea.Traj
import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Process.FiniteDimensionalLaws
import Mathlib.MeasureTheory.Integral.BoundedContinuousFunction
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Topology.ContinuousMap.Bounded.Basic

/-!
# S1-M-233 / THM-M-1040: Feller processes, Stage1 statement shape

This Stage1 artifact records a conservative Lean 4 boundary for the theorem
relating Feller semigroups and Markov processes.

The pinned mathlib snapshot has Markov kernels, kernel composition with
measures, invariant-measure predicates, probability measures, filtrations,
adapted processes, and bounded continuous functions.  This audit did not find a
terminal Feller-process theorem or a native mathlib `FellerSemigroup` object
model.  The declarations below therefore normalize the object model and expose
low-risk wrappers around checked mathlib anchors.  No construction of a Markov
process from a Feller semigroup is claimed here.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory Topology BoundedContinuousFunction

namespace AwesomeTheorems.Stage1.S1_M_233

universe u

/-- Continuous nonnegative time, the standard time domain for Feller semigroups. -/
abbrev Time : Type := ℝ≥0

variable {E Ω : Type u}

/-
Normalized data for a Feller semigroup expressed through Markov kernels.

The transition kernel determines the usual operator
`T_t f x = ∫ y, f y ∂ K_t x` on bounded continuous test functions.  The current
mathlib kernel API can express kernels, kernel composition, and Bochner
integrals of bounded continuous functions, so this file uses the concrete
kernel-integral operator below.  The Feller preservation and strong-continuity
properties remain hypotheses because no terminal Feller semigroup API was
located in the pinned dependency closure.
-/

/-- The concrete Markov operator induced by a transition kernel. -/
noncomputable def markovOperator
    [TopologicalSpace E] [MeasurableSpace E] (κ : Kernel E E) (f : E →ᵇ ℝ) :
    E → ℝ :=
  fun x => ∫ y, f y ∂(κ x)

/-- The concrete Markov operator unfolds to the Bochner integral against the kernel. -/
theorem markovOperator_apply
    [TopologicalSpace E] [MeasurableSpace E] (κ : Kernel E E)
    (f : E →ᵇ ℝ) (x : E) :
    markovOperator κ f x = ∫ y, f y ∂(κ x) :=
  rfl

/--
For a Markov kernel on a Borel-measurable topological space, every bounded
continuous real test function is integrable against each transition measure.
-/
theorem markovOperator_integrable
    [TopologicalSpace E] [MeasurableSpace E] [OpensMeasurableSpace E]
    (κ : Kernel E E) [IsMarkovKernel κ] (f : E →ᵇ ℝ) (x : E) :
    Integrable f (κ x) :=
  BoundedContinuousFunction.integrable (κ x) f

structure FellerSemigroupData (E : Type u) [TopologicalSpace E] [MeasurableSpace E] :
    Type u where
  transition : Time → Kernel E E
  isMarkov : ∀ t : Time, IsMarkovKernel (transition t)
  identity_law : transition 0 = Kernel.id
  semigroup_law : ∀ s t : Time, transition (s + t) = transition t ∘ₖ transition s
  feller_maps_bounded_continuous :
    ∀ (t : Time) (f : E →ᵇ ℝ), ∃ g : E →ᵇ ℝ, ⇑g = markovOperator (transition t) f
  strongly_continuous_at_zero :
    ∀ (f : E →ᵇ ℝ) (x : E),
      Tendsto (fun t : Time => markovOperator (transition t) f x) (𝓝 0) (𝓝 (f x))

/-- The audited Feller hypotheses outside the bare Markov-kernel semigroup laws. -/
def FellerSemigroupHypotheses
    [TopologicalSpace E] [MeasurableSpace E] (D : FellerSemigroupData E) : Prop :=
  (∀ (t : Time) (f : E →ᵇ ℝ), ∃ g : E →ᵇ ℝ,
      ⇑g = markovOperator (D.transition t) f) ∧
    ∀ (f : E →ᵇ ℝ) (x : E),
      Tendsto (fun t : Time => markovOperator (D.transition t) f x) (𝓝 0) (𝓝 (f x))

/--
An invariant probability measure for every time of a Feller semigroup.

This is not part of the main Feller-process existence statement, but it records
the checked bridge to mathlib's `Kernel.Invariant` API for stationary Feller
dynamics.
-/
structure FellerInvariantLaw
    [TopologicalSpace E] [MeasurableSpace E] (D : FellerSemigroupData E) :
    Type u where
  measure : ProbabilityMeasure E
  invariant : ∀ t : Time, Kernel.Invariant (D.transition t) (measure : Measure E)

/--
Path-regularity targets considered for the Feller-process theorem boundary.

The selected Stage1 target below is `cadlag`: right-continuity with left
limits.  Continuous sample paths are intentionally a stronger, separate target
and are not part of the default THM-M-1040 boundary recorded in this file.
-/
inductive PathRegularityTarget where
  | cadlag
  | rightContinuous
  | continuous
deriving Repr, DecidableEq

/-- The selected path-regularity target for THM-M-1040 in this Stage1 boundary. -/
def selectedPathRegularityTarget : PathRegularityTarget :=
  PathRegularityTarget.cadlag

/-- Whether a target includes right-continuity as a path regularity requirement. -/
def pathRegularityRequiresRightContinuity : PathRegularityTarget → Bool
  | PathRegularityTarget.cadlag => true
  | PathRegularityTarget.rightContinuous => true
  | PathRegularityTarget.continuous => true

/-- Whether a target includes the existence of left limits. -/
def pathRegularityRequiresLeftLimits : PathRegularityTarget → Bool
  | PathRegularityTarget.cadlag => true
  | PathRegularityTarget.rightContinuous => false
  | PathRegularityTarget.continuous => false

/-- Whether a target requires genuinely continuous paths. -/
def pathRegularityRequiresContinuousPaths : PathRegularityTarget → Bool
  | PathRegularityTarget.cadlag => false
  | PathRegularityTarget.rightContinuous => false
  | PathRegularityTarget.continuous => true

/-- THM-M-1040's selected path target is the cadlag target. -/
theorem selectedPathRegularityTarget_eq_cadlag :
    selectedPathRegularityTarget = PathRegularityTarget.cadlag :=
  rfl

/-- The selected path target requires right-continuity. -/
theorem selectedPathRegularity_requiresRightContinuity :
    pathRegularityRequiresRightContinuity selectedPathRegularityTarget = true :=
  rfl

/-- The selected path target requires left limits. -/
theorem selectedPathRegularity_requiresLeftLimits :
    pathRegularityRequiresLeftLimits selectedPathRegularityTarget = true :=
  rfl

/-- Continuous sample paths are not part of the selected THM-M-1040 boundary. -/
theorem selectedPathRegularity_doesNotRequireContinuousPaths :
    pathRegularityRequiresContinuousPaths selectedPathRegularityTarget = false :=
  rfl

/--
Realization package for a Markov process whose transition kernels are a supplied
Feller semigroup.

The Markov property and transition-law identification are explicit propositions
because the pinned mathlib snapshot does not expose a terminal Markov-process
class tying finite-dimensional laws to a Feller semigroup.
-/
structure FellerProcessRealization
    (Ω E : Type u) [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    (D : FellerSemigroupData E) : Type u where
  law : Measure Ω
  process : Time → Ω → E
  filtration : Filtration Time ‹MeasurableSpace Ω›
  isProbability : IsProbabilityMeasure law
  adapted : Adapted filtration process
  transition_law_matches_semigroup : Prop
  transition_law_matches_semigroup_holds : transition_law_matches_semigroup
  markov_property : Prop
  markov_property_holds : markov_property
  path_regularity_target : PathRegularityTarget
  path_regularity_target_eq : path_regularity_target = selectedPathRegularityTarget
  feller_path_regularization : Prop
  feller_path_regularization_holds : feller_path_regularization

/--
The finite-dimensional transition law induced by a realized process over a
finite set of times.

This is the standard pushforward `law.map (ω ↦ I.restrict (X · ω))` used by
mathlib's finite-dimensional-law API.  The dependent codomain is written
explicitly so that it aligns definitionally with `IsProjectiveMeasureFamily`.
-/
noncomputable def realizationFiniteDimensionalTransitionLaw
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D)
    (I : Finset Time) : Measure ((i : I) → (fun _ : Time => E) i) :=
  R.law.map (fun ω => I.restrict (R.process · ω))

/--
Finite-dimensional transition-law package associated to a Feller semigroup.

The package carries the actual finite-dimensional measures and the checked
projective-consistency property.  The identification with the supplied Feller
semigroup remains an explicit boundary proposition until the construction route
chooses a concrete Kolmogorov/Ionescu-Tulcea bridge.
-/
structure FellerTransitionLawPackage
    [TopologicalSpace E] [MeasurableSpace E] (D : FellerSemigroupData E) :
    Type u where
  finiteDimensionalLaw :
    (I : Finset Time) → Measure ((i : I) → (fun _ : Time => E) i)
  projective_consistency :
    @IsProjectiveMeasureFamily Time (fun _ : Time => E) (fun _ => inferInstance)
      finiteDimensionalLaw
  transition_laws_match_semigroup : Prop
  transition_laws_match_semigroup_holds : transition_laws_match_semigroup

/--
Normalized Stage1 statement shape for the Feller semigroup/process theorem.

For a supplied measurable sample space, every Feller Markov semigroup satisfying
the audited kernel/operator and strong-continuity packages admits a Markov
process realization with the stated transition semigroup.  A later integrator
should replace the abstract realization propositions by pinned finite-
dimensional-law and path-space constructions before marking the theorem
complete.
-/
def StatementShape
    (Ω E : Type u) [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    [BorelSpace E] : Prop :=
  ∀ D : FellerSemigroupData E,
    FellerSemigroupHypotheses D →
      Nonempty (FellerProcessRealization Ω E D)

/-- The statement shape unfolds to the normalized realization package. -/
theorem statementShape_iff
    (Ω E : Type u) [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    [BorelSpace E] :
    StatementShape Ω E ↔
      ∀ D : FellerSemigroupData E,
        FellerSemigroupHypotheses D →
          Nonempty (FellerProcessRealization Ω E D) :=
  Iff.rfl

/-- Project the Markov-kernel instance proof at a fixed time. -/
theorem transition_isMarkov
    [TopologicalSpace E] [MeasurableSpace E] (D : FellerSemigroupData E) (t : Time) :
    IsMarkovKernel (D.transition t) :=
  D.isMarkov t

/-- The zero-time transition kernel is the identity kernel. -/
theorem transition_zero_eq_id
    [TopologicalSpace E] [MeasurableSpace E] (D : FellerSemigroupData E) :
    D.transition 0 = Kernel.id :=
  D.identity_law

/-- The semigroup law is recorded using mathlib's kernel-composition notation. -/
theorem transition_add_eq_comp
    [TopologicalSpace E] [MeasurableSpace E] (D : FellerSemigroupData E)
    (s t : Time) :
    D.transition (s + t) = D.transition t ∘ₖ D.transition s :=
  D.semigroup_law s t

/-- The Feller hypotheses expose preservation of bounded continuous test functions. -/
theorem exists_boundedContinuous_markovOperator
    [TopologicalSpace E] [MeasurableSpace E] {D : FellerSemigroupData E}
    (hD : FellerSemigroupHypotheses D) (t : Time) (f : E →ᵇ ℝ) :
    ∃ g : E →ᵇ ℝ, ⇑g = markovOperator (D.transition t) f :=
  hD.1 t f

/-- The normalized data itself also exposes preservation of bounded continuous tests. -/
theorem data_exists_boundedContinuous_markovOperator
    [TopologicalSpace E] [MeasurableSpace E] (D : FellerSemigroupData E)
    (t : Time) (f : E →ᵇ ℝ) :
    ∃ g : E →ᵇ ℝ, ⇑g = markovOperator (D.transition t) f :=
  D.feller_maps_bounded_continuous t f

/-- The selected Markov kernel supplies an integrable concrete operator integrand. -/
theorem data_markovOperator_integrable
    [TopologicalSpace E] [MeasurableSpace E] [OpensMeasurableSpace E]
    (D : FellerSemigroupData E) (t : Time) (f : E →ᵇ ℝ) (x : E) :
    Integrable f ((D.transition t) x) := by
  haveI : IsMarkovKernel (D.transition t) := D.isMarkov t
  exact markovOperator_integrable (D.transition t) f x

/-- Strong continuity at zero for a fixed bounded continuous test and state. -/
theorem markovOperator_tendsto_zero
    [TopologicalSpace E] [MeasurableSpace E] {D : FellerSemigroupData E}
    (hD : FellerSemigroupHypotheses D) (f : E →ᵇ ℝ) (x : E) :
    Tendsto (fun t : Time => markovOperator (D.transition t) f x) (𝓝 0) (𝓝 (f x)) :=
  hD.2 f x

/-- A realization package exposes adaptedness to its filtration. -/
theorem realization_adapted
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    Adapted R.filtration R.process :=
  R.adapted

/-- Adaptedness supplies measurability of every time slice of the process. -/
theorem realization_measurable_time
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) (t : Time) :
    Measurable (R.process t) :=
  R.adapted.measurable

/-- A realization package exposes the checked probability-measure instance. -/
theorem realization_isProbability
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    IsProbabilityMeasure R.law :=
  R.isProbability

/-- A realization package exposes the transition-law identification boundary. -/
theorem realization_transition_law_matches
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    R.transition_law_matches_semigroup :=
  R.transition_law_matches_semigroup_holds

/-- The realized process induces finite-dimensional laws by pushforward. -/
theorem realizationFiniteDimensionalTransitionLaw_apply
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D)
    (I : Finset Time) :
    realizationFiniteDimensionalTransitionLaw R I =
      R.law.map (fun ω => I.restrict (R.process · ω)) :=
  rfl

/--
Finite-dimensional laws of any realized Feller process form a projective
measure family.
-/
theorem realizationFiniteDimensionalTransitionLaw_projective
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    @IsProjectiveMeasureFamily Time (fun _ : Time => E) (fun _ => inferInstance)
      (fun I : Finset Time => realizationFiniteDimensionalTransitionLaw R I) := by
  unfold realizationFiniteDimensionalTransitionLaw
  exact isProjectiveMeasureFamily_map_restrict (P := R.law)
    (X := fun t ω => R.process t ω)
    (fun t => (realization_measurable_time R t).aemeasurable)

/--
Build the finite-dimensional transition-law package attached to a realized
Feller process.
-/
noncomputable def transitionLawPackageOfRealization
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    FellerTransitionLawPackage D where
  finiteDimensionalLaw := fun I => realizationFiniteDimensionalTransitionLaw R I
  projective_consistency := realizationFiniteDimensionalTransitionLaw_projective R
  transition_laws_match_semigroup := R.transition_law_matches_semigroup
  transition_laws_match_semigroup_holds := R.transition_law_matches_semigroup_holds

/-- Projection of projective consistency from a transition-law package. -/
theorem transitionLawPackage_projective
    [TopologicalSpace E] [MeasurableSpace E] {D : FellerSemigroupData E}
    (P : FellerTransitionLawPackage D) :
    @IsProjectiveMeasureFamily Time (fun _ : Time => E) (fun _ => inferInstance)
      P.finiteDimensionalLaw :=
  P.projective_consistency

/-- Projection of the semigroup-identification boundary from a transition-law package. -/
theorem transitionLawPackage_matches_semigroup
    [TopologicalSpace E] [MeasurableSpace E] {D : FellerSemigroupData E}
    (P : FellerTransitionLawPackage D) :
    P.transition_laws_match_semigroup :=
  P.transition_laws_match_semigroup_holds

/-- A realization package exposes the Markov-property boundary. -/
theorem realization_markov_property
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    R.markov_property :=
  R.markov_property_holds

/-- A realization package records the selected path-regularity target. -/
theorem realization_pathRegularityTarget
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    R.path_regularity_target = selectedPathRegularityTarget :=
  R.path_regularity_target_eq

/-- A realization package exposes the path-regularization boundary proposition. -/
theorem realization_path_regularization
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E]
    {D : FellerSemigroupData E} (R : FellerProcessRealization Ω E D) :
    R.feller_path_regularization :=
  R.feller_path_regularization_holds

/-- An invariant-law package supplies invariance at each time. -/
theorem invariantLaw_invariant
    [TopologicalSpace E] [MeasurableSpace E] {D : FellerSemigroupData E}
    (π : FellerInvariantLaw D) (t : Time) :
    Kernel.Invariant (D.transition t) (π.measure : Measure E) :=
  π.invariant t

/-- Invariance unfolds to equality after composing the measure with the kernel. -/
theorem invariantLaw_bind_eq
    [TopologicalSpace E] [MeasurableSpace E] {D : FellerSemigroupData E}
    (π : FellerInvariantLaw D) (t : Time) :
    (π.measure : Measure E).bind (D.transition t) = (π.measure : Measure E) :=
  (π.invariant t).def

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Composition.Comp",
  "Mathlib.Probability.Kernel.Composition.MeasureComp",
  "Mathlib.Probability.Kernel.Invariance",
  "Mathlib.Probability.Kernel.IonescuTulcea.Traj",
  "Mathlib.Probability.Process.FiniteDimensionalLaws",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.Topology.ContinuousMap.Bounded.Basic",
  "Mathlib.MeasureTheory.Integral.BoundedContinuousFunction"
]

/-- Checked declaration names used as anchors for the Stage1 boundary. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.Kernel.id",
  "ProbabilityTheory.Kernel.comp",
  "ProbabilityTheory.Kernel.Invariant",
  "ProbabilityTheory.Kernel.Invariant.def",
  "MeasureTheory.Measure.bind",
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.Filtration",
  "MeasureTheory.Adapted",
  "MeasureTheory.Adapted.measurable",
  "MeasureTheory.IsProjectiveMeasureFamily",
  "BoundedContinuousFunction",
  "BoundedContinuousFunction.integrable",
  "Filter.Tendsto"
]

/--
Search terms audited while checking for a terminal Feller-process theorem in
pinned local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Feller",
  "FellerProcess",
  "FellerSemigroup",
  "Markov process",
  "Markov semigroup",
  "transition semigroup",
  "right-continuous Markov process",
  "cadlag Markov process",
  "IonescuTulcea Feller"
]

/-! ## Mathlib anchor audit for the pinned revision. -/

/-- The mathlib revision used by this Stage1 anchor audit. -/
def mathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- A compile-checked, integration-ready description of one mathlib anchor. -/
structure MathlibAnchorAuditEntry where
  subject : String
  moduleName : String
  declarationNames : List String
  role : String
  closedRepoLocalAnchor : Bool
deriving Repr, DecidableEq

/--
Mathlib anchors requested by `S1-M-233-mathlib-audit`.

`closedRepoLocalAnchor = true` means this file imports the module and checks at
least one declaration from the listed API below.  This is only an anchor audit:
it does not claim a terminal Feller-process construction theorem.
-/
def mathlibAnchorAudit : List MathlibAnchorAuditEntry := [
  { subject := "Kernel"
    moduleName := "Mathlib.Probability.Kernel.Basic"
    declarationNames := [
      "ProbabilityTheory.Kernel",
      "ProbabilityTheory.Kernel.id",
      "ProbabilityTheory.Kernel.comp"
    ]
    role := "Markov transition-kernel carrier and composition notation."
    closedRepoLocalAnchor := true },
  { subject := "IsMarkovKernel"
    moduleName := "Mathlib.Probability.Kernel.Basic"
    declarationNames := [
      "ProbabilityTheory.IsMarkovKernel"
    ]
    role := "Probability-preserving kernel predicate for each transition time."
    closedRepoLocalAnchor := true },
  { subject := "Kernel.Invariant"
    moduleName := "Mathlib.Probability.Kernel.Invariance"
    declarationNames := [
      "ProbabilityTheory.Kernel.Invariant",
      "ProbabilityTheory.Kernel.Invariant.def"
    ]
    role := "Stationary-law bridge: `μ.bind κ = μ`."
    closedRepoLocalAnchor := true },
  { subject := "ProbabilityMeasure"
    moduleName := "Mathlib.MeasureTheory.Measure.ProbabilityMeasure"
    declarationNames := [
      "MeasureTheory.ProbabilityMeasure"
    ]
    role := "Bundled probability measures used by invariant Feller laws."
    closedRepoLocalAnchor := true },
  { subject := "Filtration"
    moduleName := "Mathlib.Probability.Process.Filtration"
    declarationNames := [
      "MeasureTheory.Filtration",
      "MeasureTheory.Filtration.mono",
      "MeasureTheory.Filtration.le"
    ]
    role := "Indexed filtration on the sample-space measurable structure."
    closedRepoLocalAnchor := true },
  { subject := "Adapted"
    moduleName := "Mathlib.Probability.Process.Adapted"
    declarationNames := [
      "MeasureTheory.Adapted",
      "MeasureTheory.Adapted.measurable"
    ]
    role := "Time-slice measurability of the realized process."
    closedRepoLocalAnchor := true },
  { subject := "FiniteDimensionalLaws"
    moduleName := "Mathlib.Probability.Process.FiniteDimensionalLaws"
    declarationNames := [
      "ProbabilityTheory.isProjectiveMeasureFamily_map_restrict",
      "ProbabilityTheory.isProjectiveLimit_map",
      "ProbabilityTheory.map_eq_iff_forall_finset_map_restrict_eq",
      "ProbabilityTheory.identDistrib_iff_forall_finset_identDistrib"
    ]
    role := "Finite-dimensional laws and projective-limit comparison for processes."
    closedRepoLocalAnchor := true },
  { subject := "Kernel.IonescuTulcea.Traj"
    moduleName := "Mathlib.Probability.Kernel.IonescuTulcea.Traj"
    declarationNames := [
      "ProbabilityTheory.Kernel.traj",
      "ProbabilityTheory.Kernel.trajMeasure",
      "ProbabilityTheory.Kernel.map_traj_succ_self",
      "ProbabilityTheory.Kernel.condDistrib_trajMeasure"
    ]
    role := "Discrete-time trajectory kernel and trajectory measure construction route."
    closedRepoLocalAnchor := true },
  { subject := "BoundedContinuousFunction"
    moduleName := "Mathlib.Topology.ContinuousMap.Bounded.Basic"
    declarationNames := [
      "BoundedContinuousFunction"
    ]
    role := "Bounded continuous test-function space for Feller operators."
    closedRepoLocalAnchor := true },
  { subject := "BoundedContinuousFunction.integrable"
    moduleName := "Mathlib.MeasureTheory.Integral.BoundedContinuousFunction"
    declarationNames := [
      "BoundedContinuousFunction.integrable"
    ]
    role := "Bochner-integrability bridge for the concrete Markov operator integral."
    closedRepoLocalAnchor := true }
]

/-- Every requested mathlib anchor has a repo-local imported declaration anchor. -/
theorem mathlibAnchorAudit_no_repoLocalIntegrationDebt :
    mathlibAnchorAudit.all (fun entry => entry.closedRepoLocalAnchor) = true := by
  native_decide

/-! ## Path-regularity boundary for `S1-M-233-path-regularity`. -/

/-- API blockers for replacing the abstract path-regularization proposition. -/
inductive PathRegularityApiBlocker where
  | canonicalPathSpace
  | rightContinuousPredicate
  | leftLimitPredicate
  | cadlagMeasurability
  | finiteDimensionalLawPreservation
  | fellerRegularizationTheorem
deriving Repr, DecidableEq

/-- Compile-checked metadata for one path-regularity API blocker. -/
structure PathRegularityApiBlockerEntry where
  blocker : PathRegularityApiBlocker
  requiredForSelectedTarget : Bool
  repoLocalAnchorImported : Bool
  completionClaim : Bool
  note : String
deriving Repr, DecidableEq

/--
Path-regularity decision for THM-M-1040.

The selected target is cadlag regularization, i.e. right-continuity together
with left limits.  Continuous paths are not required by this Stage1 boundary.
All blocker rows are open formalization work, not completed anchor-only claims.
-/
def pathRegularityApiBlockers : List PathRegularityApiBlockerEntry := [
  { blocker := PathRegularityApiBlocker.canonicalPathSpace
    requiredForSelectedTarget := true
    repoLocalAnchorImported := false
    completionClaim := false
    note :=
      "Need a canonical path-space model for Time-indexed E-valued trajectories, " ++
        "or a pinned external theorem providing one." },
  { blocker := PathRegularityApiBlocker.rightContinuousPredicate
    requiredForSelectedTarget := true
    repoLocalAnchorImported := false
    completionClaim := false
    note :=
      "Need a reusable Lean predicate/API for right-continuity of each sample path." },
  { blocker := PathRegularityApiBlocker.leftLimitPredicate
    requiredForSelectedTarget := true
    repoLocalAnchorImported := false
    completionClaim := false
    note :=
      "Need a reusable Lean predicate/API for left limits along Time = RNNReal." },
  { blocker := PathRegularityApiBlocker.cadlagMeasurability
    requiredForSelectedTarget := true
    repoLocalAnchorImported := false
    completionClaim := false
    note :=
      "Need measurability/Borel infrastructure for the selected cadlag path space." },
  { blocker := PathRegularityApiBlocker.finiteDimensionalLawPreservation
    requiredForSelectedTarget := true
    repoLocalAnchorImported := false
    completionClaim := false
    note :=
      "Need proof that regularization/modification preserves the finite-dimensional " ++
        "transition laws supplied by the Feller semigroup." },
  { blocker := PathRegularityApiBlocker.fellerRegularizationTheorem
    requiredForSelectedTarget := true
    repoLocalAnchorImported := false
    completionClaim := false
    note :=
      "Need a repo-local proof or pinned external Lean theorem constructing a " ++
        "cadlag Feller-process realization under the selected state-space hypotheses." }
]

/-- Every path-regularity blocker is required for the selected cadlag target. -/
theorem pathRegularityApiBlockers_all_required :
    pathRegularityApiBlockers.all (fun entry => entry.requiredForSelectedTarget) = true := by
  native_decide

/--
No path-regularity blocker is marked completed without a repo-local anchor.

This keeps the child-local completed-state gate free of
`repo_local_integration_debt`: all rows are open blockers, not completed
anchor-only evidence.
-/
theorem pathRegularityApiBlockers_no_completed_repoLocalIntegrationDebt :
    pathRegularityApiBlockers.all
      (fun entry => !entry.completionClaim || entry.repoLocalAnchorImported) = true := by
  native_decide

/-! ## Construction-route decision for `S1-M-233-construction-route`. -/

/-- Candidate construction routes for the Feller-process existence theorem. -/
inductive ConstructionRoute where
  | mathlibIonescuTulceaDiscrete
  | kolmogorovContinuous
  | pinnedExternalContinuous
deriving Repr, DecidableEq

/--
Checked route-decision metadata for the construction task.

`closedRepoLocalAnchor` records whether this file imports and checks the route's
machine anchor.  `completionClaim` is deliberately separate: the discrete-time
Ionescu-Tulcea route is a checked local construction substrate, but it is not a
terminal proof of the continuous-time Feller-process theorem.
-/
structure ConstructionRouteDecision where
  route : ConstructionRoute
  scope : String
  closedRepoLocalAnchor : Bool
  completionClaim : Bool
  blocker : String
deriving Repr, DecidableEq

/--
Selected repo-local construction route for this pass.

The local proof should use mathlib's Ionescu-Tulcea trajectory construction for
discrete-time special cases.  Continuous time remains an explicit integration
target: it needs either a Kolmogorov-extension construction plus path
regularity, or a pinned/imported external Lean 4 theorem.  No terminal
continuous-time Feller-process theorem was found in the pinned local mathlib
closure.
-/
def selectedConstructionRoute : ConstructionRouteDecision where
  route := ConstructionRoute.mathlibIonescuTulceaDiscrete
  scope :=
    "Repo-local checked substrate for discrete-time special cases via " ++
      "Mathlib.Probability.Kernel.IonescuTulcea.Traj."
  closedRepoLocalAnchor := true
  completionClaim := false
  blocker :=
    "Does not construct a continuous-time Feller process or path-regularized realization."

/-- The selected route has a checked repo-local mathlib anchor in this file. -/
theorem selectedConstructionRoute_hasRepoLocalAnchor :
    selectedConstructionRoute.closedRepoLocalAnchor = true :=
  rfl

/-- The selected route is not a terminal completion claim for THM-M-1040. -/
theorem selectedConstructionRoute_noCompletionClaim :
    selectedConstructionRoute.completionClaim = false :=
  rfl

/-- Integration-ready audit of the route alternatives considered by this child task. -/
def constructionRouteAlternatives : List ConstructionRouteDecision := [
  selectedConstructionRoute,
  { route := ConstructionRoute.kolmogorovContinuous
    scope :=
      "Continuous-time finite-dimensional laws and projective consistency via " ++
        "a future Kolmogorov-extension bridge."
    closedRepoLocalAnchor := false
    completionClaim := false
    blocker :=
      "No repo-local Kolmogorov-extension path-space construction or " ++
        "continuous-time Feller-process realization theorem is present yet." },
  { route := ConstructionRoute.pinnedExternalContinuous
    scope :=
      "Continuous-time proof by importing a pinned external Lean 4 theorem, if one exists."
    closedRepoLocalAnchor := false
    completionClaim := false
    blocker :=
      "No external Lean 4 Feller-process theorem has been pinned/imported/checked in this repo." }
]

/--
No route recorded as a completed construction leaves repo-local integration debt.

This gate is vacuous for the continuous-time alternatives because neither is
marked complete.  It prevents an anchor-only external route from being treated
as completion in this checked artifact.
-/
theorem constructionRouteAlternatives_no_completed_repoLocalIntegrationDebt :
    constructionRouteAlternatives.all
      (fun entry => !entry.completionClaim || entry.closedRepoLocalAnchor) = true := by
  native_decide

/-! ## External-anchor audit for `S1-M-233-external-audit`. -/

/-- Source classes used by the external Lean 4 audit. -/
inductive ExternalAuditSourceKind where
  | localPinnedMathlib
  | mathlibDocumentation
  | publicLeanSourceSearch
  | unavailableSearchEndpoint
deriving Repr, DecidableEq

/--
Compile-checked metadata for one external-audit source row.

`terminalFellerProofFound` is reserved for a theorem constructing the
continuous-time Feller-process realization target, not for support APIs such as
discrete-time Ionescu-Tulcea trajectories.  If such a theorem is ever found,
`repoLocalAnchorImported` must become true before any completion claim.
-/
structure ExternalLeanAuditEntry where
  sourceKind : ExternalAuditSourceKind
  source : String
  searchTerms : List String
  terminalFellerProofFound : Bool
  repoLocalAnchorImported : Bool
  completionClaim : Bool
  blocker : String
deriving Repr, DecidableEq

/-- Broader external-audit search terms requested for this child task. -/
def externalLeanAuditSearchTerms : List String := [
  "Feller",
  "FellerSemigroup",
  "FellerProcess",
  "MarkovSemigroup",
  "transition semigroup",
  "IonescuTulcea"
]

/--
External Lean 4 audit result for the terminal Feller-process theorem.

The only checked repo-local machine anchor found by this pass is mathlib's
discrete-time Ionescu-Tulcea trajectory construction.  It is already imported
above, but it is not a continuous-time Feller-process proof.  No external
Lean 4 terminal theorem was found to pin/import/check in this pass.
-/
def externalLeanAudit : List ExternalLeanAuditEntry := [
  { sourceKind := ExternalAuditSourceKind.localPinnedMathlib
    source :=
      "Formalizations/Lean/.lake/packages/mathlib at " ++ mathlibAuditRevision
    searchTerms := externalLeanAuditSearchTerms
    terminalFellerProofFound := false
    repoLocalAnchorImported := false
    completionClaim := false
    blocker :=
      "Local grep found Ionescu-Tulcea support APIs but no FellerSemigroup, " ++
        "FellerProcess, MarkovSemigroup, or continuous-time transition-semigroup " ++
        "terminal theorem." },
  { sourceKind := ExternalAuditSourceKind.localPinnedMathlib
    source := "Mathlib.Probability.Kernel.IonescuTulcea.Traj"
    searchTerms := ["IonescuTulcea", "transition semigroup"]
    terminalFellerProofFound := false
    repoLocalAnchorImported := true
    completionClaim := false
    blocker :=
      "Imported and checked as a discrete-time trajectory-kernel substrate only; " ++
        "it does not close the continuous-time Feller-process theorem." },
  { sourceKind := ExternalAuditSourceKind.mathlibDocumentation
    source :=
      "https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Kernel/IonescuTulcea/Traj.html"
    searchTerms := ["IonescuTulcea", "Kernel.traj", "Kernel.trajMeasure"]
    terminalFellerProofFound := false
    repoLocalAnchorImported := true
    completionClaim := false
    blocker :=
      "Official docs expose discrete-time trajectory APIs, not a Feller-process " ++
        "existence theorem." },
  { sourceKind := ExternalAuditSourceKind.mathlibDocumentation
    source :=
      "https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Kernel/Basic.html"
    searchTerms := ["Kernel", "IsMarkovKernel", "Feller"]
    terminalFellerProofFound := false
    repoLocalAnchorImported := true
    completionClaim := false
    blocker :=
      "Official docs expose Markov-kernel infrastructure; no native Feller " ++
        "semigroup/process object or terminal theorem was located." },
  { sourceKind := ExternalAuditSourceKind.publicLeanSourceSearch
    source := "Public web/source search on 2026-05-01"
    searchTerms := externalLeanAuditSearchTerms
    terminalFellerProofFound := false
    repoLocalAnchorImported := false
    completionClaim := false
    blocker :=
      "No candidate external Lean 4 module/theorem was located to pin/import/check." },
  { sourceKind := ExternalAuditSourceKind.unavailableSearchEndpoint
    source := "GitHub unauthenticated code-search API"
    searchTerms := externalLeanAuditSearchTerms
    terminalFellerProofFound := false
    repoLocalAnchorImported := false
    completionClaim := false
    blocker :=
      "Unauthenticated GitHub code search was rate-limited; rerun with an authenticated " ++
        "code-search token before converting this audit into a completion claim." }
]

/-- This audit found no terminal external Feller-process theorem. -/
theorem externalLeanAudit_no_terminalFellerProofFound :
    externalLeanAudit.all (fun entry => !entry.terminalFellerProofFound) = true := by
  native_decide

/--
No external-audit row is marked completed without a repo-local imported anchor.

The discrete-time mathlib rows are imported anchors but still have no completion
claim because they do not prove the continuous-time Feller-process theorem.
-/
theorem externalLeanAudit_no_completed_repoLocalIntegrationDebt :
    externalLeanAudit.all
      (fun entry => !entry.completionClaim || entry.repoLocalAnchorImported) = true := by
  native_decide

/-! ## Leaf-budget ledger for `S1-M-233-leaf-ledger`. -/

/--
Compile-checked metadata for one Stage1 leaf-budget row.

`checked = false` records that the row is preserved as an open proof leaf, not
as a completed theorem claim.  `proofBudgetBound = 100` records the M0387
budget target that must be met by a later local proof ledger before completion.
-/
structure LeafBudgetEntry where
  leafId : String
  packageId : String
  checked : Bool
  proofBudgetBound : Nat
  task : String
deriving Repr, DecidableEq

/--
The 38 unchecked leaf ids from the parent `S1-M-233` ledger.

This list is intentionally proof-budget metadata.  It preserves the independent
leaf ids that must be refined or discharged before THM-M-1040 can be marked
checked/completed.
-/
def leafBudgetLedger : List LeafBudgetEntry := [
  { leafId := "S1-M-233-L001", packageId := "P0", checked := false, proofBudgetBound := 100,
    task := "Choose canonical state-space assumptions." },
  { leafId := "S1-M-233-L002", packageId := "P0", checked := false, proofBudgetBound := 100,
    task := "Decide final time index." },
  { leafId := "S1-M-233-L003", packageId := "P0", checked := false, proofBudgetBound := 100,
    task := "Freeze kernel-composition order in the semigroup law." },
  { leafId := "S1-M-233-L004", packageId := "P0", checked := false, proofBudgetBound := 100,
    task := "Decide supplied sample-space versus canonical path-space conclusion." },
  { leafId := "S1-M-233-L005", packageId := "P0", checked := false, proofBudgetBound := 100,
    task := "Decide whether conclusion includes path regularity." },
  { leafId := "S1-M-233-L006", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit Kernel and IsMarkovKernel universe and instance requirements." },
  { leafId := "S1-M-233-L007", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit Kernel.id and kernel composition notation." },
  { leafId := "S1-M-233-L008", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit measure-kernel composition and Measure.bind." },
  { leafId := "S1-M-233-L009", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit Kernel.Invariant for stationary Feller-process subgoals." },
  { leafId := "S1-M-233-L010", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit ProbabilityMeasure coercions to Measure." },
  { leafId := "S1-M-233-L011", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit Filtration over nonnegative real time." },
  { leafId := "S1-M-233-L012", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit Adapted and Adapted.measurable for process time slices." },
  { leafId := "S1-M-233-L013", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit FiniteDimensionalLaws as a law-identification bridge." },
  { leafId := "S1-M-233-L014", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit Kernel.IonescuTulcea.Traj for discrete-time construction reuse." },
  { leafId := "S1-M-233-L015", packageId := "P1", checked := false, proofBudgetBound := 100,
    task := "Audit BoundedContinuousFunction notation and integration support." },
  { leafId := "S1-M-233-L016", packageId := "P2", checked := false, proofBudgetBound := 100,
    task := "Define the Markov operator associated to a kernel on bounded continuous tests." },
  { leafId := "S1-M-233-L017", packageId := "P2", checked := false, proofBudgetBound := 100,
    task := "Prove measurability or integrability of bounded continuous tests under Markov kernels." },
  { leafId := "S1-M-233-L018", packageId := "P2", checked := false, proofBudgetBound := 100,
    task := "Prove Feller preservation for the chosen operator representation." },
  { leafId := "S1-M-233-L019", packageId := "P2", checked := false, proofBudgetBound := 100,
    task := "Prove strong continuity at zero in the chosen topology or norm." },
  { leafId := "S1-M-233-L020", packageId := "P2", checked := false, proofBudgetBound := 100,
    task := "Prove semigroup continuity propagates from zero to arbitrary times if required." },
  { leafId := "S1-M-233-L021", packageId := "P3", checked := false, proofBudgetBound := 100,
    task := "Encode the transition law conditioned on the past filtration." },
  { leafId := "S1-M-233-L022", packageId := "P3", checked := false, proofBudgetBound := 100,
    task := "Encode finite-dimensional distributions from an initial law and transition semigroup." },
  { leafId := "S1-M-233-L023", packageId := "P3", checked := false, proofBudgetBound := 100,
    task := "Prove consistency or projectivity of finite-dimensional distributions." },
  { leafId := "S1-M-233-L024", packageId := "P3", checked := false, proofBudgetBound := 100,
    task := "Connect finite-dimensional laws to process law using projective-family APIs." },
  { leafId := "S1-M-233-L025", packageId := "P4", checked := false, proofBudgetBound := 100,
    task := "Specialize Ionescu-Tulcea to time-homogeneous discrete-time Markov kernels." },
  { leafId := "S1-M-233-L026", packageId := "P4", checked := false, proofBudgetBound := 100,
    task := "Identify whether continuous-time construction needs Kolmogorov extension." },
  { leafId := "S1-M-233-L027", packageId := "P4", checked := false, proofBudgetBound := 100,
    task := "Construct canonical path-space measure if projective consistency is available." },
  { leafId := "S1-M-233-L028", packageId := "P4", checked := false, proofBudgetBound := 100,
    task := "Prove coordinate process is adapted to the canonical filtration." },
  { leafId := "S1-M-233-L029", packageId := "P4", checked := false, proofBudgetBound := 100,
    task := "Prove coordinate process has the required transition semigroup." },
  { leafId := "S1-M-233-L030", packageId := "P4", checked := false, proofBudgetBound := 100,
    task := "Prove the Markov property from the kernel construction." },
  { leafId := "S1-M-233-L031", packageId := "P5", checked := false, proofBudgetBound := 100,
    task := "Identify the path-regularity hypothesis required by the source theorem." },
  { leafId := "S1-M-233-L032", packageId := "P5", checked := false, proofBudgetBound := 100,
    task := "Prove or import cadlag or right-continuous modification existence if required." },
  { leafId := "S1-M-233-L033", packageId := "P5", checked := false, proofBudgetBound := 100,
    task := "Show path regularization preserves finite-dimensional laws." },
  { leafId := "S1-M-233-L034", packageId := "P6", checked := false, proofBudgetBound := 100,
    task := "Decide whether final proof body is local, mathlib-wrapper, or pinned external dependency." },
  { leafId := "S1-M-233-L035", packageId := "P6", checked := false, proofBudgetBound := 100,
    task := "If an external Lean proof is found, pin, import, and check it before completion." },
  { leafId := "S1-M-233-L036", packageId := "P6", checked := false, proofBudgetBound := 100,
    task := "Run the local validation gate and record exact command and result." },
  { leafId := "S1-M-233-L037", packageId := "P6", checked := false, proofBudgetBound := 100,
    task := "Merge human-readable proof tree into public surface after machine-anchor closure." },
  { leafId := "S1-M-233-L038", packageId := "P6", checked := false, proofBudgetBound := 100,
    task := "Synchronize public checklist and summaries after integrator merge-back." }
]

/-- The preserved leaf-id list for integration backfill. -/
def leafBudgetLedgerIds : List String :=
  leafBudgetLedger.map (fun entry => entry.leafId)

/-- The ledger preserves exactly the 38 parent leaf ids. -/
theorem leafBudgetLedger_length :
    leafBudgetLedger.length = 38 := by
  native_decide

/-- All preserved leaves remain unchecked; no child completion claim is made. -/
theorem leafBudgetLedger_all_unchecked :
    leafBudgetLedger.all (fun entry => !entry.checked) = true := by
  native_decide

/-- Every preserved leaf is explicitly bounded by the M0387 `<= 100` target. -/
theorem leafBudgetLedger_all_budget_le_100 :
    leafBudgetLedger.all (fun entry => entry.proofBudgetBound ≤ 100) = true := by
  native_decide

/-! ## Completion gate for `S1-M-233-completion-gate`. -/

/--
Compile-checked status row for the public Stage1 checkbox gate.

Dynamic build output still belongs in the worker ledger, not in Lean.  This row
records the static gates that decide whether a later public integrator may close
the Stage1 checkbox.  The current artifact has a checked statement boundary and
no completed-state integration debt, but it has not been publicly merged back
and its independent proof leaves are intentionally still open.
-/
structure CompletionGateStatus where
  checkedStatementBoundary : Bool
  localValidationCommandRecorded : Bool
  publicMergeBackComplete : Bool
  independentLeafLedgerComplete : Bool
  noCompletedRepoLocalIntegrationDebt : Bool
  terminalFellerProcessProofComplete : Bool
deriving Repr, DecidableEq

/-- The C009 completion gate status for this Stage1 artifact. -/
def completionGateStatus : CompletionGateStatus where
  checkedStatementBoundary := true
  localValidationCommandRecorded := true
  publicMergeBackComplete := false
  independentLeafLedgerComplete := false
  noCompletedRepoLocalIntegrationDebt := true
  terminalFellerProcessProofComplete := false

/-- The public Stage1 checkbox may close only when every gate component is true. -/
def completionGateMayClose : Bool :=
  completionGateStatus.checkedStatementBoundary &&
    completionGateStatus.localValidationCommandRecorded &&
    completionGateStatus.publicMergeBackComplete &&
    completionGateStatus.independentLeafLedgerComplete &&
    completionGateStatus.noCompletedRepoLocalIntegrationDebt &&
    completionGateStatus.terminalFellerProcessProofComplete

/-- C009 keeps the Stage1 checkbox open in this artifact. -/
theorem completionGate_mustStayOpen :
    completionGateMayClose = false := by
  native_decide

/-! ## Audit probes retained in the checked file. -/

#check FellerSemigroupData
#check FellerSemigroupHypotheses
#check FellerInvariantLaw
#check FellerProcessRealization
#check FellerTransitionLawPackage
#check PathRegularityTarget
#check selectedPathRegularityTarget
#check selectedPathRegularityTarget_eq_cadlag
#check selectedPathRegularity_requiresRightContinuity
#check selectedPathRegularity_requiresLeftLimits
#check selectedPathRegularity_doesNotRequireContinuousPaths
#check StatementShape
#check statementShape_iff
#check markovOperator
#check markovOperator_apply
#check markovOperator_integrable
#check transition_isMarkov
#check transition_zero_eq_id
#check transition_add_eq_comp
#check exists_boundedContinuous_markovOperator
#check data_exists_boundedContinuous_markovOperator
#check data_markovOperator_integrable
#check markovOperator_tendsto_zero
#check realization_measurable_time
#check realizationFiniteDimensionalTransitionLaw
#check realizationFiniteDimensionalTransitionLaw_apply
#check realizationFiniteDimensionalTransitionLaw_projective
#check transitionLawPackageOfRealization
#check transitionLawPackage_projective
#check transitionLawPackage_matches_semigroup
#check realization_pathRegularityTarget
#check realization_path_regularization
#check invariantLaw_bind_eq
#check Kernel
#check IsMarkovKernel
#check Kernel.Invariant
#check Kernel.Invariant.def
#check Measure.bind
#check ProbabilityMeasure
#check Filtration
#check Filtration.mono
#check Filtration.le
#check Adapted
#check Adapted.measurable
#check isProjectiveMeasureFamily_map_restrict
#check isProjectiveLimit_map
#check map_eq_iff_forall_finset_map_restrict_eq
#check identDistrib_iff_forall_finset_identDistrib
#check Kernel.traj
#check Kernel.trajMeasure
#check Kernel.map_traj_succ_self
#check Kernel.condDistrib_trajMeasure
#check BoundedContinuousFunction
#check BoundedContinuousFunction.integrable
#check mathlibAnchorAudit_no_repoLocalIntegrationDebt
#check PathRegularityApiBlocker
#check PathRegularityApiBlockerEntry
#check pathRegularityApiBlockers
#check pathRegularityApiBlockers_all_required
#check pathRegularityApiBlockers_no_completed_repoLocalIntegrationDebt
#check ConstructionRoute
#check ConstructionRouteDecision
#check selectedConstructionRoute
#check selectedConstructionRoute_hasRepoLocalAnchor
#check selectedConstructionRoute_noCompletionClaim
#check constructionRouteAlternatives
#check constructionRouteAlternatives_no_completed_repoLocalIntegrationDebt
#check ExternalAuditSourceKind
#check ExternalLeanAuditEntry
#check externalLeanAuditSearchTerms
#check externalLeanAudit
#check externalLeanAudit_no_terminalFellerProofFound
#check externalLeanAudit_no_completed_repoLocalIntegrationDebt
#check LeafBudgetEntry
#check leafBudgetLedger
#check leafBudgetLedgerIds
#check leafBudgetLedger_length
#check leafBudgetLedger_all_unchecked
#check leafBudgetLedger_all_budget_le_100
#check CompletionGateStatus
#check completionGateStatus
#check completionGateMayClose
#check completionGate_mustStayOpen

end AwesomeTheorems.Stage1.S1_M_233
