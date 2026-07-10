import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Probability.HasLaw
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Filtration

/-!
# S1-M-217 / THM-M-1093: Fokker-Planck equation

This Stage1 artifact records a conservative Lean 4 boundary for the
one-dimensional Fokker-Planck forward equation for density evolution,

`∂ₜ ρ = - ∂ₓ (b ρ) + (1 / 2) * ∂ₓₓ (a ρ)`.

The pinned mathlib snapshot has measure theory, probability laws,
probability kernels, densities via `Measure.withDensity`, classical
derivatives, and `ContDiffOn`.  It does not expose a terminal stochastic
calculus / SDE-to-Fokker-Planck theorem, so this file keeps the main theorem
as an explicit statement shape and provides only low-risk checked wrappers
around available substrate.
-/

noncomputable section

open MeasureTheory
open ProbabilityTheory

open scoped ENNReal

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_217

/-- One-dimensional time-space for a classical density equation. -/
abbrev TimeSpace : Type :=
  ℝ × ℝ

/-- A time-dependent density or coefficient field `f(t, x)`. -/
abbrev ScalarField : Type :=
  TimeSpace → ℝ

/-- Formal time derivative `∂ₜ f`. -/
def temporalDerivative (f : ScalarField) : ScalarField :=
  fun z => deriv (fun t : ℝ => f (t, z.2)) z.1

/-- Formal space derivative `∂ₓ f`. -/
def spatialDerivative (f : ScalarField) : ScalarField :=
  fun z => deriv (fun x : ℝ => f (z.1, x)) z.2

/-- Formal second space derivative `∂ₓₓ f`. -/
def secondSpatialDerivative (f : ScalarField) : ScalarField :=
  spatialDerivative (spatialDerivative f)

/-- The drift flux `b ρ`. -/
def driftFlux (b ρ : ScalarField) : ScalarField :=
  fun z => b z * ρ z

/-- The diffusion flux `a ρ`, where `a` is the scalar variance coefficient. -/
def diffusionFlux (a ρ : ScalarField) : ScalarField :=
  fun z => a z * ρ z

/--
The one-dimensional Fokker-Planck forward operator
`-∂ₓ(bρ) + (1/2)∂ₓₓ(aρ)`.
-/
def fokkerPlanckForwardOperator (b a ρ : ScalarField) : ScalarField :=
  fun z =>
    -spatialDerivative (driftFlux b ρ) z +
      (1 / 2 : ℝ) * secondSpatialDerivative (diffusionFlux a ρ) z

/-- Residual for `∂ₜρ = -∂ₓ(bρ) + (1/2)∂ₓₓ(aρ)`. -/
def fokkerPlanckResidual (b a ρ : ScalarField) : ScalarField :=
  fun z => temporalDerivative ρ z - fokkerPlanckForwardOperator b a ρ z

/-- The residual unfolds to the normalized Fokker-Planck expression. -/
theorem fokkerPlanckResidual_apply (b a ρ : ScalarField) (z : TimeSpace) :
    fokkerPlanckResidual b a ρ z =
      temporalDerivative ρ z -
        (-spatialDerivative (driftFlux b ρ) z +
          (1 / 2 : ℝ) * secondSpatialDerivative (diffusionFlux a ρ) z) :=
  rfl

/-- Classical pointwise Fokker-Planck equation on a specified time-space domain. -/
def SolvesClassicalFokkerPlanck
    (b a ρ : ScalarField) (domain : Set TimeSpace) : Prop :=
  ∀ z ∈ domain, fokkerPlanckResidual b a ρ z = 0

/--
Test functions for the selected one-dimensional weak formulation.

The explicit `boundaryTermsVanish` field records the analytic compact-support
or decay-at-infinity obligation needed by the two integrations by parts.
-/
structure FokkerPlanckTestFunction : Type where
  function : ℝ → ℝ
  smoothEnough : ContDiff ℝ 2 function
  boundaryTermsVanish : Prop

/-- The diffusion generator acting on a one-dimensional test function. -/
def diffusionGenerator (b a : ScalarField) (φ : ℝ → ℝ) : ScalarField :=
  fun z =>
    b z * deriv φ z.2 +
      (1 / 2 : ℝ) * a z * deriv (deriv φ) z.2

/-- Pairing of a density time-slice with a test function. -/
def densityTestPairing (ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : ℝ :=
  ∫ x, φ.function x * ρ (t, x) ∂(volume : Measure ℝ)

/-- Pairing of a density time-slice with the diffusion generator of a test function. -/
def generatorDensityPairing
    (b a ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : ℝ :=
  ∫ x, diffusionGenerator b a φ.function (t, x) * ρ (t, x) ∂(volume : Measure ℝ)

/--
Selected weak Fokker-Planck formulation:
`d/dt ∫ φ ρ(t) = ∫ (Lφ) ρ(t)` for every chosen test function.
-/
def SolvesWeakFokkerPlanck (b a ρ : ScalarField) : Prop :=
  ∀ φ : FokkerPlanckTestFunction,
    ∀ t : ℝ,
      deriv (fun s : ℝ => densityTestPairing ρ φ s) t =
        generatorDensityPairing b a ρ φ t

/-- The weak formulation unfolds to the selected generator-pairing identity. -/
theorem solvesWeakFokkerPlanck_apply (b a ρ : ScalarField) :
    SolvesWeakFokkerPlanck b a ρ =
      ∀ φ : FokkerPlanckTestFunction,
        ∀ t : ℝ,
          deriv (fun s : ℝ => densityTestPairing ρ φ s) t =
            generatorDensityPairing b a ρ φ t :=
  rfl

/-- Pairing of a formal time derivative of the density with a test function. -/
def temporalDerivativeTestPairing
    (ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : ℝ :=
  ∫ x, φ.function x * temporalDerivative ρ (t, x) ∂(volume : Measure ℝ)

/--
Leaf P3-L007: differentiating the density-test pairing under the integral sign.

This is stated as a target identity, not proved from analytic hypotheses here.
-/
def DifferentiationUnderIntegralLeaf
    (ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : Prop :=
  deriv (fun s : ℝ => densityTestPairing ρ φ s) t =
    temporalDerivativeTestPairing ρ φ t

/--
Leaf P3-L004: drift integration by parts,
moving `-∂ₓ(bρ)` onto `φ'`.
-/
def DriftIntegrationByPartsLeaf
    (b ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : Prop :=
  ∫ x, φ.function x * (-spatialDerivative (driftFlux b ρ) (t, x))
      ∂(volume : Measure ℝ) =
    ∫ x, b (t, x) * deriv φ.function x * ρ (t, x)
      ∂(volume : Measure ℝ)

/--
Leaf P3-L005: first diffusion integration by parts,
moving one derivative from `∂ₓₓ(aρ)` onto `φ'`.
-/
def DiffusionFirstIntegrationByPartsLeaf
    (a ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : Prop :=
  ∫ x, φ.function x * secondSpatialDerivative (diffusionFlux a ρ) (t, x)
      ∂(volume : Measure ℝ) =
    -∫ x, deriv φ.function x * spatialDerivative (diffusionFlux a ρ) (t, x)
      ∂(volume : Measure ℝ)

/--
Leaf P3-L006: second diffusion integration by parts,
moving the remaining derivative onto `φ''`.
-/
def DiffusionSecondIntegrationByPartsLeaf
    (a ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : Prop :=
  -∫ x, deriv φ.function x * spatialDerivative (diffusionFlux a ρ) (t, x)
      ∂(volume : Measure ℝ) =
    ∫ x, deriv (deriv φ.function) x * a (t, x) * ρ (t, x)
      ∂(volume : Measure ℝ)

/--
Leaf P3-L008: final assembly from the pointwise residual equation and the
preceding analytic leaves into the selected weak generator identity.
-/
def WeakFormulationAssemblyLeaf
    (b a ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : Prop :=
  deriv (fun s : ℝ => densityTestPairing ρ φ s) t =
    generatorDensityPairing b a ρ φ t

/--
Evidence package for a single test function and time in the P3 weak-form split.

The field names are the remaining local proof leaves.  Supplying this package
for all tests and times is exactly enough to expose `SolvesWeakFokkerPlanck`.
-/
structure WeakFormulationLeafEvidence
    (b a ρ : ScalarField) (φ : FokkerPlanckTestFunction) (t : ℝ) : Prop where
  differentiatingUnderIntegral : DifferentiationUnderIntegralLeaf ρ φ t
  driftIntegrationByParts : DriftIntegrationByPartsLeaf b ρ φ t
  diffusionFirstIntegrationByParts : DiffusionFirstIntegrationByPartsLeaf a ρ φ t
  diffusionSecondIntegrationByParts : DiffusionSecondIntegrationByPartsLeaf a ρ φ t
  weakAssembly : WeakFormulationAssemblyLeaf b a ρ φ t

/-- The per-test P3 evidence package projects the selected weak formulation. -/
theorem solvesWeakFokkerPlanck_of_leafEvidence
    (b a ρ : ScalarField)
    (H : ∀ φ : FokkerPlanckTestFunction,
      ∀ t : ℝ, WeakFormulationLeafEvidence b a ρ φ t) :
    SolvesWeakFokkerPlanck b a ρ := by
  intro φ t
  exact (H φ t).weakAssembly

/-- Measure with density `ρ(t, ·)` relative to one-dimensional Lebesgue measure. -/
def densityMeasure (ρ : ScalarField) (t : ℝ) : Measure ℝ :=
  (volume : Measure ℝ).withDensity fun x => ENNReal.ofReal (ρ (t, x))

/-- Initial measure with density `ρ₀` relative to one-dimensional Lebesgue measure. -/
def initialDensityMeasure (ρ₀ : ℝ → ℝ) : Measure ℝ :=
  (volume : Measure ℝ).withDensity fun x => ENNReal.ofReal (ρ₀ x)

/--
Density-measure probability bridge for nonnegative measurable real densities.

The normalization is stated as the `lintegral` of the `ENNReal.ofReal`
density, which is exactly the total mass computed by `Measure.withDensity`.
-/
theorem withDensity_ofReal_isProbability_of_lintegral_eq_one
    (f : ℝ → ℝ) (hf : Measurable f) (hnonneg : ∀ x : ℝ, 0 ≤ f x)
    (hmass : ∫⁻ x, ENNReal.ofReal (f x) ∂(volume : Measure ℝ) = 1) :
    IsProbabilityMeasure
      ((volume : Measure ℝ).withDensity fun x => ENNReal.ofReal (f x)) := by
  have _ : Measurable fun x => ENNReal.ofReal (f x) := hf.ennreal_ofReal
  have _ : ∀ x : ℝ, 0 ≤ f x := hnonneg
  refine ⟨?_⟩
  rw [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ]
  exact hmass

/--
Real-integral variant of the density-measure bridge.

The explicit `Integrable` hypothesis records the Lean-side condition needed to
convert the Bochner integral normalization into the `lintegral` normalization
used by `Measure.withDensity`.
-/
theorem withDensity_ofReal_isProbability_of_integral_eq_one
    (f : ℝ → ℝ) (hf : Measurable f) (hnonneg : ∀ x : ℝ, 0 ≤ f x)
    (hfint : Integrable f (volume : Measure ℝ))
    (hmass : ∫ x, f x ∂(volume : Measure ℝ) = 1) :
    IsProbabilityMeasure
      ((volume : Measure ℝ).withDensity fun x => ENNReal.ofReal (f x)) := by
  refine withDensity_ofReal_isProbability_of_lintegral_eq_one f hf hnonneg ?_
  rw [← ofReal_integral_eq_lintegral_ofReal hfint]
  · simp [hmass]
  · exact Filter.Eventually.of_forall hnonneg

/-- Initial-density specialization of the `lintegral` normalization bridge. -/
theorem initialDensityMeasure_isProbability_of_lintegral_eq_one
    {ρ₀ : ℝ → ℝ} (hρ₀ : Measurable ρ₀) (hρ₀_nonneg : ∀ x : ℝ, 0 ≤ ρ₀ x)
    (hρ₀_mass : ∫⁻ x, ENNReal.ofReal (ρ₀ x) ∂(volume : Measure ℝ) = 1) :
    IsProbabilityMeasure (initialDensityMeasure ρ₀) := by
  simpa [initialDensityMeasure] using
    withDensity_ofReal_isProbability_of_lintegral_eq_one ρ₀ hρ₀ hρ₀_nonneg hρ₀_mass

/-- Time-slice specialization of the `lintegral` normalization bridge. -/
theorem densityMeasure_isProbability_of_lintegral_eq_one
    (ρ : ScalarField) (t : ℝ)
    (hρt : Measurable fun x : ℝ => ρ (t, x))
    (hρt_nonneg : ∀ x : ℝ, 0 ≤ ρ (t, x))
    (hρt_mass : ∫⁻ x, ENNReal.ofReal (ρ (t, x)) ∂(volume : Measure ℝ) = 1) :
    IsProbabilityMeasure (densityMeasure ρ t) := by
  simpa [densityMeasure] using
    withDensity_ofReal_isProbability_of_lintegral_eq_one
      (fun x : ℝ => ρ (t, x)) hρt hρt_nonneg hρt_mass

/-- The density measure evaluates by the defining `withDensity` integral. -/
theorem densityMeasure_apply (ρ : ScalarField) (t : ℝ)
    {s : Set ℝ} (hs : MeasurableSet s) :
    densityMeasure ρ t s =
      ∫⁻ x in s, ENNReal.ofReal (ρ (t, x)) ∂(volume : Measure ℝ) := by
  exact withDensity_apply _ hs

/-- Initial data package for a future Fokker-Planck theorem. -/
structure FokkerPlanckInitialData (ρ₀ : ℝ → ℝ) : Type where
  initialMeasurable : Measurable ρ₀
  initialNonnegative : ∀ x : ℝ, 0 ≤ ρ₀ x
  initialIsProbability : IsProbabilityMeasure (initialDensityMeasure ρ₀)
  finiteMomentHypotheses : Prop
  admissibleForDiffusion : Prop

/-- Drift/diffusion coefficient package for the normalized one-dimensional equation. -/
structure FokkerPlanckCoefficients : Type where
  drift : ScalarField
  variance : ScalarField
  driftRegularity : Prop
  varianceRegularity : Prop
  varianceNonnegative : ∀ z : TimeSpace, 0 ≤ variance z
  generatorMatchesDiffusion : Prop

/--
Density-evolution solution package.

The proposition fields mark the hard analytic and probabilistic bridge
obligations: weak formulation, law evolution, SDE/generator compatibility, and
uniqueness in the chosen admissible class.
-/
structure FokkerPlanckDensityEvolution
    (ρ₀ : ℝ → ℝ) (I : FokkerPlanckInitialData ρ₀)
    (C : FokkerPlanckCoefficients) : Type where
  density : ScalarField
  domain : Set TimeSpace
  coversNonnegativeTimes : {t : ℝ | 0 ≤ t} ⊆
    {t : ℝ | ∀ x : ℝ, (t, x) ∈ domain}
  densityRegularity : ContDiffOn ℝ 2 density domain
  densityNonnegative : ∀ z ∈ domain, 0 ≤ density z
  densityIsProbability : ∀ t : ℝ, IsProbabilityMeasure (densityMeasure density t)
  solvesClassicalEquation :
    SolvesClassicalFokkerPlanck C.drift C.variance density domain
  initialTrace : ∀ x : ℝ, density (0, x) = ρ₀ x
  weakFormulation : Prop
  weakFormulationMatchesSelectedClass :
    weakFormulation = SolvesWeakFokkerPlanck C.drift C.variance density
  lawEvolutionAgreement : Prop
  sdeGeneratorCompatibility : Prop
  uniquenessInAdmissibleClass : Prop
  weakFormulation_holds : weakFormulation
  lawEvolutionAgreement_holds : lawEvolutionAgreement
  sdeGeneratorCompatibility_holds : sdeGeneratorCompatibility
  uniquenessInAdmissibleClass_holds : uniquenessInAdmissibleClass

/--
Normalized Stage1 statement shape for THM-M-1093.

For admissible initial density and drift/diffusion coefficients, a later full
formalization should construct a nonnegative-time density evolution satisfying
the classical or weak Fokker-Planck equation, the initial trace, the probability
normalization, law evolution, generator compatibility, and uniqueness.  This
file does not prove that terminal theorem.
-/
def StatementShape : Prop :=
  ∀ (ρ₀ : ℝ → ℝ) (I : FokkerPlanckInitialData ρ₀)
    (C : FokkerPlanckCoefficients),
      I.finiteMomentHypotheses →
        I.admissibleForDiffusion →
          C.driftRegularity →
            C.varianceRegularity →
              C.generatorMatchesDiffusion →
                Nonempty (FokkerPlanckDensityEvolution ρ₀ I C)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (ρ₀ : ℝ → ℝ) (I : FokkerPlanckInitialData ρ₀)
      (C : FokkerPlanckCoefficients),
        I.finiteMomentHypotheses →
          I.admissibleForDiffusion →
            C.driftRegularity →
              C.varianceRegularity →
                C.generatorMatchesDiffusion →
                  Nonempty (FokkerPlanckDensityEvolution ρ₀ I C)) :
    StatementShape :=
  h

/-- The initial law package exposes probability normalization. -/
theorem initial_density_isProbability {ρ₀ : ℝ → ℝ}
    (I : FokkerPlanckInitialData ρ₀) :
    IsProbabilityMeasure (initialDensityMeasure ρ₀) :=
  I.initialIsProbability

/-- A solution package exposes the pointwise Fokker-Planck equation on its domain. -/
theorem solution_solves_fokkerPlanck {ρ₀ : ℝ → ℝ}
    {I : FokkerPlanckInitialData ρ₀} {C : FokkerPlanckCoefficients}
    (S : FokkerPlanckDensityEvolution ρ₀ I C) :
    SolvesClassicalFokkerPlanck C.drift C.variance S.density S.domain :=
  S.solvesClassicalEquation

/-- A solution package exposes its initial density trace. -/
theorem solution_initial_trace {ρ₀ : ℝ → ℝ}
    {I : FokkerPlanckInitialData ρ₀} {C : FokkerPlanckCoefficients}
    (S : FokkerPlanckDensityEvolution ρ₀ I C) (x : ℝ) :
    S.density (0, x) = ρ₀ x :=
  S.initialTrace x

/-- A solution package covers each nonnegative time slice. -/
theorem nonnegative_time_slice_mem {ρ₀ : ℝ → ℝ}
    {I : FokkerPlanckInitialData ρ₀} {C : FokkerPlanckCoefficients}
    (S : FokkerPlanckDensityEvolution ρ₀ I C) {t : ℝ} (ht : 0 ≤ t) (x : ℝ) :
    (t, x) ∈ S.domain :=
  S.coversNonnegativeTimes ht x

/-- A solution package exposes the probability normalization of each density slice. -/
theorem solution_density_isProbability {ρ₀ : ℝ → ℝ}
    {I : FokkerPlanckInitialData ρ₀} {C : FokkerPlanckCoefficients}
    (S : FokkerPlanckDensityEvolution ρ₀ I C) (t : ℝ) :
    IsProbabilityMeasure (densityMeasure S.density t) :=
  S.densityIsProbability t

/-- A solution package exposes the weak-formulation bridge obligation. -/
theorem solution_weakFormulation {ρ₀ : ℝ → ℝ}
    {I : FokkerPlanckInitialData ρ₀} {C : FokkerPlanckCoefficients}
    (S : FokkerPlanckDensityEvolution ρ₀ I C) :
    S.weakFormulation :=
  S.weakFormulation_holds

/-- A solution package exposes the selected test-function weak formulation. -/
theorem solution_solvesWeakFokkerPlanck {ρ₀ : ℝ → ℝ}
    {I : FokkerPlanckInitialData ρ₀} {C : FokkerPlanckCoefficients}
    (S : FokkerPlanckDensityEvolution ρ₀ I C) :
    SolvesWeakFokkerPlanck C.drift C.variance S.density := by
  rw [← S.weakFormulationMatchesSelectedClass]
  exact S.weakFormulation_holds

/-- A solution package exposes the law-evolution bridge obligation. -/
theorem solution_lawEvolutionAgreement {ρ₀ : ℝ → ℝ}
    {I : FokkerPlanckInitialData ρ₀} {C : FokkerPlanckCoefficients}
    (S : FokkerPlanckDensityEvolution ρ₀ I C) :
    S.lawEvolutionAgreement :=
  S.lawEvolutionAgreement_holds

/--
P4 checked statement substrate: the time marginals of a process have the
density measures generated by `ρ`.

This uses only `HasLaw`; it deliberately does not introduce an SDE,
stochastic integral, Brownian motion, or Ito-process placeholder.
-/
structure MarginalLawEvolution
    (Ω : Type) [MeasurableSpace Ω] (P : Measure Ω)
    (X : ℝ → Ω → ℝ) (ρ : ScalarField) : Prop where
  marginalLaw : ∀ t : ℝ, HasLaw (X t) (densityMeasure ρ t) P

/-- Projection wrapper for the checked marginal-law package. -/
theorem marginalLawEvolution_hasLaw
    {Ω : Type} [MeasurableSpace Ω] {P : Measure Ω}
    {X : ℝ → Ω → ℝ} {ρ : ScalarField}
    (H : MarginalLawEvolution Ω P X ρ) (t : ℝ) :
    HasLaw (X t) (densityMeasure ρ t) P :=
  H.marginalLaw t

/--
P4 placeholder-free bridge shape available in current mathlib:
there is a process whose one-time marginals are the density measures and those
density measures satisfy the selected weak generator identity.

This is a law-evolution / generator statement shape only.  It is weaker than
an SDE-to-Fokker-Planck theorem because it does not derive the generator from a
stochastic integral representation of the process.
-/
def GeneratorWeakLawEvolutionBridge (b a ρ : ScalarField) : Prop :=
  (∃ (Ω : Type) (_ : MeasurableSpace Ω) (P : Measure Ω) (X : ℝ → Ω → ℝ),
      MarginalLawEvolution Ω P X ρ) ∧
    SolvesWeakFokkerPlanck b a ρ

/-- The P4 bridge shape unfolds to the marginal-law plus weak-generator identity. -/
theorem generatorWeakLawEvolutionBridge_apply (b a ρ : ScalarField) :
    GeneratorWeakLawEvolutionBridge b a ρ =
      ((∃ (Ω : Type) (_ : MeasurableSpace Ω) (P : Measure Ω) (X : ℝ → Ω → ℝ),
          MarginalLawEvolution Ω P X ρ) ∧
        SolvesWeakFokkerPlanck b a ρ) :=
  rfl

/--
P4 route classification for the pinned mathlib stochastic-process APIs.

The selected route is intentionally the `HasLaw` marginal-law plus weak
generator identity.  The full stochastic-integral/SDE route is recorded as a
different constructor so that the local artifact does not silently treat the
available statement shape as a terminal diffusion theorem.
-/
inductive P4StochasticProcessAPIRoute where
  | hasLawMarginalsAndWeakGenerator
  | stochasticIntegralSDEToGenerator
deriving DecidableEq, Repr

/-- Selected P4 route available without stochastic-integral placeholders. -/
def selectedP4StochasticProcessAPIRoute : P4StochasticProcessAPIRoute :=
  P4StochasticProcessAPIRoute.hasLawMarginalsAndWeakGenerator

/-- The selected P4 route is the checked `HasLaw`/weak-generator route. -/
theorem selectedP4StochasticProcessAPIRoute_eq :
    selectedP4StochasticProcessAPIRoute =
      P4StochasticProcessAPIRoute.hasLawMarginalsAndWeakGenerator :=
  rfl

/--
The selected P4 route is not the unavailable stochastic-integral/SDE route.

This theorem is only a route classification.  It is not a theorem saying that
no future mathlib or external project can provide such an API.
-/
theorem selectedP4StochasticProcessAPIRoute_ne_sde :
    selectedP4StochasticProcessAPIRoute ≠
      P4StochasticProcessAPIRoute.stochasticIntegralSDEToGenerator := by
  intro h
  cases h

/--
P4 checked statement-availability package: current local APIs can state the
placeholder-free marginal-law plus weak-generator bridge.
-/
def PlaceholderFreeWeakLawBridgeStatementAvailable : Prop :=
  ∀ b a ρ : ScalarField,
    GeneratorWeakLawEvolutionBridge b a ρ =
      ((∃ (Ω : Type) (_ : MeasurableSpace Ω) (P : Measure Ω) (X : ℝ → Ω → ℝ),
          MarginalLawEvolution Ω P X ρ) ∧
        SolvesWeakFokkerPlanck b a ρ)

/-- The placeholder-free weak law-evolution bridge statement is locally checked. -/
theorem placeholderFreeWeakLawBridgeStatementAvailable :
    PlaceholderFreeWeakLawBridgeStatementAvailable := by
  intro b a ρ
  rfl

/-- Checked mathlib anchor: density measures are absolutely continuous. -/
theorem densityMeasure_absolutelyContinuous (ρ : ScalarField) (t : ℝ) :
    densityMeasure ρ t ≪ (volume : Measure ℝ) :=
  withDensity_absolutelyContinuous _ _

section ProbabilityAnchors

variable {Ω X Y : Type*} [MeasurableSpace Ω] [MeasurableSpace X] [MeasurableSpace Y]
variable {P : Measure Ω} {μ : Measure X}
variable {Z : Ω → X}

/-- Checked mathlib anchor: `HasLaw` exposes the map-equality defining a law. -/
theorem hasLaw_map_eq (hZ : HasLaw Z μ P) :
    P.map Z = μ :=
  hZ.map_eq

/-- Checked mathlib anchor: `HasLaw` exposes almost-everywhere measurability. -/
theorem hasLaw_aemeasurable (hZ : HasLaw Z μ P) :
    AEMeasurable Z P :=
  hZ.aemeasurable

/-- Checked mathlib anchor: deterministic kernels evaluate to Dirac measures. -/
theorem deterministicKernel_apply {f : X → Y} (hf : Measurable f) (x : X) :
    Kernel.deterministic f hf x = Measure.dirac (f x) :=
  Kernel.deterministic_apply hf x

/-- Checked mathlib anchor: deterministic kernels are Markov kernels. -/
theorem deterministicKernel_isMarkov {f : X → Y} (hf : Measurable f) :
    IsMarkovKernel (Kernel.deterministic f hf) :=
  inferInstance

theorem isMarkovKernel_apply_isProbability (κ : Kernel X Y) [IsMarkovKernel κ] (x : X) :
    IsProbabilityMeasure (κ x) :=
  IsMarkovKernel.isProbabilityMeasure x

end ProbabilityAnchors

section ProbabilityMeasureAnchors

variable {α : Type*} [MeasurableSpace α] {μ : Measure α}

/-- Checked mathlib anchor: a probability measure has total mass one. -/
theorem probabilityMeasure_univ [IsProbabilityMeasure μ] :
    μ Set.univ = 1 :=
  measure_univ

end ProbabilityMeasureAnchors

section ConvergenceDistributionAnchors

variable {ι E Ω' : Type*} {Ω : ι → Type*} {m : ∀ i, MeasurableSpace (Ω i)}
variable {m' : MeasurableSpace Ω'} {mE : MeasurableSpace E}
variable [TopologicalSpace E] [OpensMeasurableSpace E]
variable {X : (i : ι) → Ω i → E} {Z : Ω' → E}
variable {l : Filter ι} {μ : (i : ι) → Measure (Ω i)} {μ' : Measure Ω'}
variable [∀ i, IsProbabilityMeasure (μ i)] [IsProbabilityMeasure μ']

/-- Checked mathlib anchor: convergence in distribution records measurable approximants. -/
theorem tendstoInDistribution_forall_aemeasurable
    (h : MeasureTheory.TendstoInDistribution X l Z μ μ') (i : ι) :
    AEMeasurable (X i) (μ i) :=
  h.forall_aemeasurable i

/-- Checked mathlib anchor: convergence in distribution records a measurable limit. -/
theorem tendstoInDistribution_limit_aemeasurable
    (h : MeasureTheory.TendstoInDistribution X l Z μ μ') :
    AEMeasurable Z μ' :=
  h.aemeasurable_limit

end ConvergenceDistributionAnchors

section ProcessAnchors

variable {Ω E ι : Type*} [Preorder ι] {m0 : MeasurableSpace Ω}
variable {ℱ : MeasureTheory.Filtration ι m0} {i j : ι}

/-- Checked mathlib anchor: filtrations are monotone families of sub-σ-algebras. -/
theorem filtration_mono (hij : i ≤ j) :
    ℱ i ≤ ℱ j :=
  ℱ.mono hij

variable [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
variable {f : ι → Ω → E} {μ : Measure Ω}

/-- Checked mathlib anchor: a martingale is strongly adapted to its filtration. -/
theorem martingale_stronglyAdapted
    (hf : MeasureTheory.Martingale f ℱ μ) :
    MeasureTheory.StronglyAdapted ℱ f :=
  hf.stronglyAdapted

end ProcessAnchors

section IndependenceAnchors

variable {Ω X Y : Type*} [MeasurableSpace Ω] [MeasurableSpace X] [MeasurableSpace Y]
variable {P : Measure Ω} {U : Ω → X} {V : Ω → Y}

/-- Checked mathlib anchor: function independence is the constant-kernel specialization. -/
theorem indepFun_kernel_def :
    ProbabilityTheory.IndepFun U V P =
      ProbabilityTheory.Kernel.IndepFun U V
        (ProbabilityTheory.Kernel.const Unit P) (Measure.dirac () : Measure Unit) :=
  rfl

end IndependenceAnchors

/-- A public, integration-ready row for mathlib anchors audited for this Stage1 slot. -/
structure MathlibAnchorRow where
  topic : String
  moduleName : String
  declarationName : String
  checkedAnchor : String
  role : String
deriving Repr

/-- The pinned mathlib revision used for the anchor audit in this file. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Public mathlib anchor table for the Fokker-Planck Stage1 backfill.

Each row names the upstream mathlib module/declaration and a repo-local checked
anchor in this file.  These anchors support statement design only; they do not
prove a terminal SDE-to-Fokker-Planck theorem.
-/
def publicMathlibAnchorTable : List MathlibAnchorRow := [
  {
    topic := "density measure",
    moduleName := "Mathlib.MeasureTheory.Measure.WithDensity",
    declarationName := "MeasureTheory.Measure.withDensity",
    checkedAnchor := "densityMeasure_apply; densityMeasure_absolutelyContinuous",
    role := "represents densities as measures absolutely continuous to volume"
  },
  {
    topic := "probability normalization",
    moduleName := "Mathlib.MeasureTheory.Measure.Typeclasses.Probability",
    declarationName := "MeasureTheory.IsProbabilityMeasure",
    checkedAnchor := "probabilityMeasure_univ; initial_density_isProbability",
    role := "records total-mass-one obligations for density slices"
  },
  {
    topic := "random-variable law",
    moduleName := "Mathlib.Probability.HasLaw",
    declarationName := "ProbabilityTheory.HasLaw",
    checkedAnchor := "hasLaw_map_eq; hasLaw_aemeasurable",
    role := "connects random variables with pushed-forward law measures"
  },
  {
    topic := "probability kernels",
    moduleName := "Mathlib.Probability.Kernel.Basic",
    declarationName := "ProbabilityTheory.Kernel",
    checkedAnchor := "deterministicKernel_apply",
    role := "available substrate for transition kernels and deterministic kernels"
  },
  {
    topic := "Markov kernels",
    moduleName := "Mathlib.Probability.Kernel.Basic",
    declarationName := "ProbabilityTheory.IsMarkovKernel",
    checkedAnchor := "deterministicKernel_isMarkov; isMarkovKernel_apply_isProbability",
    role := "states that each kernel fiber is a probability measure"
  },
  {
    topic := "convergence in distribution",
    moduleName := "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
    declarationName := "MeasureTheory.TendstoInDistribution",
    checkedAnchor := "tendstoInDistribution_forall_aemeasurable; tendstoInDistribution_limit_aemeasurable",
    role := "weak convergence of random variables through laws in ProbabilityMeasure"
  },
  {
    topic := "filtrations",
    moduleName := "Mathlib.Probability.Process.Filtration",
    declarationName := "MeasureTheory.Filtration",
    checkedAnchor := "filtration_mono",
    role := "monotone time-indexed sub-σ-algebras for process statements"
  },
  {
    topic := "independence",
    moduleName := "Mathlib.Probability.Independence.Basic",
    declarationName := "ProbabilityTheory.IndepFun",
    checkedAnchor := "indepFun_kernel_def",
    role := "function independence via generated σ-algebras / constant kernels"
  },
  {
    topic := "martingales",
    moduleName := "Mathlib.Probability.Martingale.Basic",
    declarationName := "MeasureTheory.Martingale",
    checkedAnchor := "martingale_stronglyAdapted",
    role := "martingale process statements relative to filtrations"
  }
]

/-- A public, integration-ready row for the P3 weak-formulation leaf split. -/
structure WeakFormulationLeafRow where
  leafId : String
  target : String
  budget : String
  status : String
deriving Repr

/--
Unchecked P3 proof leaves for the selected weak formulation.

The first three rows are now represented by checked declarations in this file.
The integration-by-parts and differentiating-under-the-integral leaves remain
formalization debt and are intentionally not claimed as completed.
-/
def weakFormulationLeafSplit : List WeakFormulationLeafRow := [
  {
    leafId := "M1093-P3-L001",
    target := "Define the chosen test-function class with smoothness and boundary-term obligations.",
    budget := "<=30",
    status := "checked locally: FokkerPlanckTestFunction"
  },
  {
    leafId := "M1093-P3-L002",
    target := "Define the diffusion generator L phi = b phi' + (1/2) a phi''.",
    budget := "<=30",
    status := "checked locally: diffusionGenerator"
  },
  {
    leafId := "M1093-P3-L003",
    target := "Define the weak generator-pairing identity for every test function and time.",
    budget := "<=45",
    status := "checked locally: SolvesWeakFokkerPlanck"
  },
  {
    leafId := "M1093-P3-L004",
    target := "Prove the drift integration-by-parts leaf moving -d_x(b rho) onto phi'.",
    budget := "<=100",
    status := "checked target declaration: DriftIntegrationByPartsLeaf; proof unchecked formalization_debt"
  },
  {
    leafId := "M1093-P3-L005",
    target := "Prove the first diffusion integration-by-parts leaf moving d_xx(a rho) onto phi'.",
    budget := "<=100",
    status := "checked target declaration: DiffusionFirstIntegrationByPartsLeaf; proof unchecked formalization_debt"
  },
  {
    leafId := "M1093-P3-L006",
    target := "Prove the second diffusion integration-by-parts leaf moving the remaining derivative onto phi''.",
    budget := "<=100",
    status := "checked target declaration: DiffusionSecondIntegrationByPartsLeaf; proof unchecked formalization_debt"
  },
  {
    leafId := "M1093-P3-L007",
    target := "Justify differentiating the density-test pairing under the integral sign.",
    budget := "<=100",
    status := "checked target declaration: DifferentiationUnderIntegralLeaf; proof unchecked formalization_debt"
  },
  {
    leafId := "M1093-P3-L008",
    target := "Assemble the classical residual equation into the weak generator identity.",
    budget := "<=100",
    status := "checked target declaration: WeakFormulationAssemblyLeaf; proof unchecked formalization_debt"
  }
]

/-- A P4 audit row for the stochastic-process generator/law-evolution bridge. -/
structure StochasticBridgeAuditRow where
  layer : String
  mathlibSurface : String
  repoLocalAnchor : String
  verdict : String
  nextGate : String
deriving Repr

/--
P4 audit verdict for the pinned mathlib snapshot.

The current APIs are enough to state a marginal-law evolution bridge against
the repo-local weak generator identity.  They are not enough to state a full
diffusion/SDE generator theorem without adding placeholders for stochastic
integrals, Brownian drivers, Ito processes, or a continuous-time infinitesimal
generator framework.
-/
def stochasticBridgeAuditTable : List StochasticBridgeAuditRow := [
  {
    layer := "selected P4 route",
    mathlibSurface := "ProbabilityTheory.HasLaw plus repo-local weak generator identity",
    repoLocalAnchor := "P4StochasticProcessAPIRoute; selectedP4StochasticProcessAPIRoute; PlaceholderFreeWeakLawBridgeStatementAvailable",
    verdict := "checked: selected route is marginal laws plus weak generator, not a stochastic-integral/SDE route",
    nextGate := "do not mark terminal diffusion theorem complete from this route alone"
  },
  {
    layer := "marginal laws",
    mathlibSurface := "ProbabilityTheory.HasLaw",
    repoLocalAnchor := "MarginalLawEvolution; marginalLawEvolution_hasLaw",
    verdict := "checked: can state one-time laws of a process as densityMeasure rho t",
    nextGate := "none for statement shape; proof requires existence/regularity of the chosen process"
  },
  {
    layer := "weak generator identity",
    mathlibSurface := "deriv; MeasureTheory.Measure.withDensity; Bochner integral",
    repoLocalAnchor := "diffusionGenerator; SolvesWeakFokkerPlanck; GeneratorWeakLawEvolutionBridge",
    verdict := "checked: can state the law-evolution identity without stochastic integrals",
    nextGate := "P3 integration-by-parts and differentiating-under-the-integral leaves remain open"
  },
  {
    layer := "transition kernels",
    mathlibSurface := "ProbabilityTheory.Kernel; ProbabilityTheory.IsMarkovKernel",
    repoLocalAnchor := "deterministicKernel_apply; deterministicKernel_isMarkov",
    verdict := "partial substrate: kernels exist, but no continuous-time diffusion semigroup/generator theorem was found",
    nextGate := "choose P5 finite-state or deterministic branch before attempting continuous diffusion closure"
  },
  {
    layer := "adapted process/martingale scaffolding",
    mathlibSurface := "MeasureTheory.Filtration; MeasureTheory.Martingale",
    repoLocalAnchor := "filtration_mono; martingale_stronglyAdapted",
    verdict := "checked substrate only: process measurability/adaptation can be discussed",
    nextGate := "not a replacement for stochastic integration or Ito formula"
  },
  {
    layer := "SDE-to-generator bridge",
    mathlibSurface := "no pinned mathlib declaration found for SDE, stochastic integral, Ito process, semimartingale, Brownian-driven diffusion, or infinitesimal diffusion generator",
    repoLocalAnchor := "absentTerminalSearchTerms",
    verdict := "blocked for placeholder-free full diffusion theorem",
    nextGate := "P6 external search must pin/import/check a real Lean 4 proof or record a concrete blocker"
  }
]

/--
Finite-state continuous-time Markov-chain generator data.

Rows sum to zero and off-diagonal rates are nonnegative.  This is the selected
bounded P5 branch; it avoids stochastic integration and continuous spatial PDE
regularity while retaining the forward-equation shape.
-/
structure FiniteStateRateMatrix (α : Type*) [Fintype α] [DecidableEq α] where
  rate : α → α → ℝ
  offDiagonal_nonneg : ∀ i j : α, i ≠ j → 0 ≤ rate i j
  row_sum_zero : ∀ i : α, ∑ j : α, rate i j = 0

/-- A finite-state mass vector. -/
abbrev FiniteStateMass (α : Type*) :=
  α → ℝ

/-- Total mass of a finite-state mass vector. -/
def finiteStateTotalMass
    {α : Type*} [Fintype α] (p : FiniteStateMass α) : ℝ :=
  ∑ i : α, p i

/-- The forward-equation right-hand side `p Q`, written componentwise. -/
def finiteStateForwardRHS
    {α : Type*} [Fintype α] [DecidableEq α]
    (Q : FiniteStateRateMatrix α) (p : FiniteStateMass α) : FiniteStateMass α :=
  fun i => ∑ j : α, p j * Q.rate j i

/-- Residual for the finite-state Kolmogorov forward equation. -/
def finiteStateForwardResidual
    {α : Type*} [Fintype α] [DecidableEq α]
    (Q : FiniteStateRateMatrix α) (p : ℝ → FiniteStateMass α) :
    ℝ → FiniteStateMass α :=
  fun t i => deriv (fun s : ℝ => p s i) t - finiteStateForwardRHS Q (p t) i

/-- The finite-state Kolmogorov forward equation `d p_i / dt = ∑_j p_j q_{ji}`. -/
def SolvesFiniteStateForwardEquation
    {α : Type*} [Fintype α] [DecidableEq α]
    (Q : FiniteStateRateMatrix α) (p : ℝ → FiniteStateMass α) : Prop :=
  ∀ t : ℝ, ∀ i : α, finiteStateForwardResidual Q p t i = 0

/-- The finite-state forward residual unfolds to the componentwise master equation. -/
theorem finiteStateForwardResidual_apply
    {α : Type*} [Fintype α] [DecidableEq α]
    (Q : FiniteStateRateMatrix α) (p : ℝ → FiniteStateMass α) (t : ℝ) (i : α) :
    finiteStateForwardResidual Q p t i =
      deriv (fun s : ℝ => p s i) t - ∑ j : α, p t j * Q.rate j i :=
  rfl

/-- The finite-state forward RHS has zero total-mass contribution. -/
theorem finiteStateForwardRHS_totalMass_eq_zero
    {α : Type*} [Fintype α] [DecidableEq α]
    (Q : FiniteStateRateMatrix α) (p : FiniteStateMass α) :
    finiteStateTotalMass (finiteStateForwardRHS Q p) = 0 := by
  classical
  calc
    finiteStateTotalMass (finiteStateForwardRHS Q p)
        = ∑ i : α, ∑ j : α, p j * Q.rate j i := rfl
    _ = ∑ j : α, ∑ i : α, p j * Q.rate j i := Finset.sum_comm
    _ = ∑ j : α, p j * ∑ i : α, Q.rate j i := by
      simp [Finset.mul_sum]
    _ = 0 := by
      simp [Q.row_sum_zero]

/--
Any differentiable finite-state path satisfying the forward equation has zero
derivative of total mass.
-/
theorem solvesFiniteStateForwardEquation_totalMass_deriv_eq_zero
    {α : Type*} [Fintype α] [DecidableEq α]
    (Q : FiniteStateRateMatrix α) (p : ℝ → FiniteStateMass α)
    (hsolves : SolvesFiniteStateForwardEquation Q p)
    (hdiff : ∀ t : ℝ, ∀ i : α, DifferentiableAt ℝ (fun s : ℝ => p s i) t)
    (t : ℝ) :
    deriv (fun s : ℝ => finiteStateTotalMass (p s)) t = 0 := by
  classical
  rw [show (fun s : ℝ => finiteStateTotalMass (p s)) =
      fun s : ℝ => ∑ i : α, p s i by rfl]
  have hderiv_sum :
      deriv (fun s : ℝ => ∑ i : α, p s i) t =
        ∑ i : α, deriv (fun s : ℝ => p s i) t := by
    simpa using
      (deriv_fun_sum (u := Finset.univ)
        (A := fun i : α => fun s : ℝ => p s i)
        (x := t) (fun i _hi => hdiff t i))
  rw [hderiv_sum]
  calc
    ∑ i : α, deriv (fun s : ℝ => p s i) t =
        finiteStateTotalMass (finiteStateForwardRHS Q (p t)) := by
      apply Finset.sum_congr rfl
      intro i _hi
      simpa [finiteStateForwardResidual, sub_eq_zero] using hsolves t i
    _ = 0 := finiteStateForwardRHS_totalMass_eq_zero Q (p t)

/-- The zero finite-state generator. -/
def zeroFiniteStateRateMatrix (α : Type*) [Fintype α] [DecidableEq α] :
    FiniteStateRateMatrix α where
  rate := fun _ _ => 0
  offDiagonal_nonneg := by
    intro i j hij
    simp
  row_sum_zero := by
    intro i
    simp

/-- Constant finite-state mass paths solve the forward equation for the zero generator. -/
theorem constantMass_solves_zeroFiniteStateForwardEquation
    {α : Type*} [Fintype α] [DecidableEq α] (p0 : FiniteStateMass α) :
    SolvesFiniteStateForwardEquation (zeroFiniteStateRateMatrix α) (fun _ : ℝ => p0) := by
  intro t i
  simp [finiteStateForwardResidual, finiteStateForwardRHS, zeroFiniteStateRateMatrix]

/-- A P5 audit row for bounded special-case branch selection. -/
structure SpecialCaseBranchAuditRow where
  branch : String
  repoLocalSurface : String
  checkedLeaf : String
  verdict : String
  nextGate : String
deriving Repr

/--
P5 selected bounded branch.

The finite-state CTMC forward equation is the first bounded branch for this
slot.  It is not claimed as the full Fokker-Planck diffusion theorem; it is a
repo-local checked special-case surface that can be expanded before attempting
continuous diffusion closure.
-/
def specialCaseBranchAuditTable : List SpecialCaseBranchAuditRow := [
  {
    branch := "finite-state continuous-time Markov-chain forward equation",
    repoLocalSurface := "FiniteStateRateMatrix; finiteStateForwardRHS; finiteStateForwardResidual; SolvesFiniteStateForwardEquation",
    checkedLeaf := "finiteStateForwardResidual_apply; finiteStateForwardRHS_totalMass_eq_zero; solvesFiniteStateForwardEquation_totalMass_deriv_eq_zero",
    verdict := "selected P5 bounded branch; checked statement shape, residual unfolding, and finite-sum mass-balance derivative",
    nextGate := "prove nonnegative semigroup/evolution existence for finite state spaces"
  },
  {
    branch := "zero-generator stationary finite-state branch",
    repoLocalSurface := "zeroFiniteStateRateMatrix; constantMass_solves_zeroFiniteStateForwardEquation",
    checkedLeaf := "constantMass_solves_zeroFiniteStateForwardEquation",
    verdict := "checked local proof body for a minimal stationary special case",
    nextGate := "generalize from zero generator to arbitrary finite rate matrices"
  },
  {
    branch := "one-dimensional deterministic or constant-coefficient diffusion branch",
    repoLocalSurface := "not selected in this child",
    checkedLeaf := "none",
    verdict := "deferred to avoid continuous PDE/stochastic-calculus debt in P5",
    nextGate := "consider only after finite-state mass-preservation and semigroup leaves are closed"
  }
]

/-- mathlib modules checked while locating repo-local anchors for this Fokker-Planck slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.MeasureTheory.Measure.WithDensity",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Integral.DominatedConvergence",
  "Mathlib.Probability.HasLaw",
  "Mathlib.Probability.Kernel.Basic",
  "Mathlib.Probability.Kernel.Invariance",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.FiniteDimensionalLaws",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Martingale.Basic"
]

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "ContDiffOn",
  "Measure.withDensity",
  "withDensity_apply",
  "withDensity_absolutelyContinuous",
  "IsProbabilityMeasure",
  "ProbabilityTheory.HasLaw",
  "ProbabilityTheory.HasLaw.map_eq",
  "ProbabilityTheory.HasLaw.aemeasurable",
  "ProbabilityTheory.Kernel",
  "ProbabilityTheory.Kernel.deterministic",
  "ProbabilityTheory.Kernel.deterministic_apply",
  "ProbabilityTheory.IsMarkovKernel",
  "ProbabilityTheory.Kernel.Invariant",
  "MeasureTheory.TendstoInDistribution",
  "MeasureTheory.TendstoInDistribution.forall_aemeasurable",
  "MeasureTheory.TendstoInDistribution.aemeasurable_limit",
  "MeasureTheory.Measure.tendsto_iff_forall_lintegral_tendsto",
  "MeasureTheory.tendstoInMeasure",
  "MeasureTheory.AEStronglyMeasurable",
  "MeasureTheory.Filtration",
  "MeasureTheory.Filtration.mono",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.stronglyAdapted"
]

/--
Search terms that did not locate a terminal Fokker-Planck theorem in the
pinned local mathlib snapshot.
-/
def absentTerminalSearchTerms : List String := [
  "Fokker",
  "Planck",
  "FokkerPlanck",
  "Fokker-Planck",
  "Kolmogorov forward",
  "KolmogorovForward",
  "diffusion equation",
  "stochastic differential equation",
  "SDE",
  "Ito process",
  "Itô process",
  "stochastic integral",
  "semimartingale",
  "quadratic variation",
  "Brownian motion",
  "infinitesimal generator",
  "density evolution",
  "forward equation"
]

/-- A P6 audit row for external Lean 4 code-search integration. -/
structure ExternalCodeSearchAuditRow where
  searchSurface : String
  queryFamily : String
  observedResult : String
  repoLocalConsequence : String
  nextGate : String
deriving Repr

/--
P6 external-anchor audit state for authenticated GitHub code search.

This records the concrete credential blocker observed in the child pass.  It is
not evidence of theorem completion: no external Lean 4 proof body has been
found, pinned, imported, or checked in this repository.
-/
def externalCodeSearchAuditTable : List ExternalCodeSearchAuditRow := [
  {
    searchSurface := "GitHub CLI authentication",
    queryFamily := "gh auth status; gh search code for FokkerPlanck, Fokker-Planck, stochastic integral, Kolmogorov forward",
    observedResult := "blocked: no GH_TOKEN/GITHUB_TOKEN and gh reports no logged-in GitHub host",
    repoLocalConsequence := "no external_upstream_pinned or local_wrapper_upstream proof claim is available",
    nextGate := "rerun authenticated GitHub code search with a token; pin/import/check any real Lean 4 proof or record a candidate-specific integration blocker"
  },
  {
    searchSurface := "repo-local Lean closure",
    queryFamily := "current Lake dependencies and pinned mathlib source",
    observedResult := "no terminal Fokker-Planck, SDE-to-generator, stochastic-integral, or diffusion forward-equation theorem is in the local verification closure",
    repoLocalConsequence := "THM-M-1093 remains formalization_debt, not completed",
    nextGate := "continue from statement-shape, weak-formulation, stochastic-bridge audit, and finite-state branch leaves"
  }
]

#check StatementShape
#check FokkerPlanckInitialData
#check FokkerPlanckCoefficients
#check FokkerPlanckDensityEvolution
#check fokkerPlanckResidual
#check SolvesClassicalFokkerPlanck
#check FokkerPlanckTestFunction
#check diffusionGenerator
#check SolvesWeakFokkerPlanck
#check temporalDerivativeTestPairing
#check DifferentiationUnderIntegralLeaf
#check DriftIntegrationByPartsLeaf
#check DiffusionFirstIntegrationByPartsLeaf
#check DiffusionSecondIntegrationByPartsLeaf
#check WeakFormulationAssemblyLeaf
#check WeakFormulationLeafEvidence
#check solvesWeakFokkerPlanck_of_leafEvidence
#check weakFormulationLeafSplit
#check MarginalLawEvolution
#check marginalLawEvolution_hasLaw
#check GeneratorWeakLawEvolutionBridge
#check generatorWeakLawEvolutionBridge_apply
#check P4StochasticProcessAPIRoute
#check selectedP4StochasticProcessAPIRoute
#check selectedP4StochasticProcessAPIRoute_eq
#check selectedP4StochasticProcessAPIRoute_ne_sde
#check PlaceholderFreeWeakLawBridgeStatementAvailable
#check placeholderFreeWeakLawBridgeStatementAvailable
#check stochasticBridgeAuditTable
#check FiniteStateRateMatrix
#check finiteStateTotalMass
#check finiteStateForwardRHS
#check finiteStateForwardResidual
#check SolvesFiniteStateForwardEquation
#check finiteStateForwardResidual_apply
#check finiteStateForwardRHS_totalMass_eq_zero
#check solvesFiniteStateForwardEquation_totalMass_deriv_eq_zero
#check zeroFiniteStateRateMatrix
#check constantMass_solves_zeroFiniteStateForwardEquation
#check specialCaseBranchAuditTable
#check densityMeasure
#check withDensity_ofReal_isProbability_of_lintegral_eq_one
#check withDensity_ofReal_isProbability_of_integral_eq_one
#check initialDensityMeasure_isProbability_of_lintegral_eq_one
#check densityMeasure_isProbability_of_lintegral_eq_one
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.Kernel
#check ProbabilityTheory.Kernel.deterministic
#check MeasureTheory.Measure.withDensity
#check MeasureTheory.withDensity_absolutelyContinuous
#check MeasureTheory.TendstoInDistribution
#check MeasureTheory.Filtration
#check ProbabilityTheory.IndepFun
#check ProbabilityTheory.iIndepFun
#check MeasureTheory.Martingale
#check publicMathlibAnchorTable
#check externalCodeSearchAuditTable

end S1_M_217
end Stage1
end AwesomeTheorems
