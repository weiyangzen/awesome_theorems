import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Measure.MutuallySingular
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
Statement-only encoding of the Cameron-Martin theorem on continuous real paths over `NNReal`.
No field below assumes quasi-invariance, singularity, or a Radon-Nikodym formula.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1045

/-- Continuous real paths on nonnegative time. -/
abbrev WienerPath := C(ℝ≥0, ℝ)

/-- Cylinder measurable structure on continuous paths. -/
instance : MeasurableSpace WienerPath :=
  MeasurableSpace.comap (fun x : WienerPath => (x : ℝ≥0 → ℝ)) ⊤

/-- Lebesgue measure on nonnegative time, expressed as the push-forward under `Real.toNNReal`. -/
def timeMeasure : Measure ℝ≥0 := volume.map Real.toNNReal

/-- Translation of a continuous path by a deterministic continuous path. -/
def translate (h x : WienerPath) : WienerPath := x + h

/-- Push-forward under `x |-> x + h`. -/
def translatedMeasure (μ : Measure WienerPath) (h : WienerPath) : Measure WienerPath :=
  μ.map (translate h)

/-- A path belongs to the Cameron-Martin space when it is the indefinite integral of an `L2`
function. This includes the condition `h 0 = 0`. -/
def IsCameronMartinDirection (h : WienerPath) : Prop :=
  ∃ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure ∧
    ∀ t : ℝ≥0, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure

/-- Half the squared Cameron-Martin norm. -/
def cameronMartinEnergy (g : ℝ≥0 → ℝ) : ℝ :=
  (∫ t : ℝ≥0, (g t) ^ (2 : Nat) ∂timeMeasure) / 2

/-- Data fixing Wiener measure and the Paley-Wiener integral used in the density expression.
The Gaussian finite-dimensional and increment fields describe the Wiener law; `paleyWienerIntegral`
is the statement-level realization of the stochastic integral, whose construction is later proof
work rather than a conclusion field. -/
structure WienerData where
  measure : Measure WienerPath
  isProbability : IsProbabilityMeasure measure
  startsAtZero : ∀ᵐ x ∂measure, x 0 = 0
  coordinateAEMeasurable : ∀ t : ℝ≥0, AEMeasurable (fun x : WienerPath => x t) measure
  finiteDimensionalGaussian :
    ∀ I : Finset ℝ≥0, HasGaussianLaw (fun x : WienerPath => I.restrict (fun t => x t)) measure
  incrementLaw : ∀ ⦃s t : ℝ≥0⦄, (hst : s ≤ t) →
    HasLaw (fun x : WienerPath => x t - x s)
      (gaussianReal 0 ⟨(t : ℝ) - (s : ℝ), sub_nonneg.mpr (by exact_mod_cast hst)⟩) measure
  paleyWienerIntegral : (ℝ≥0 → ℝ) → WienerPath → ℝ
  paleyWienerMeasurable : ∀ g, Measurable (paleyWienerIntegral g)

/-- The positive-sign density for the push-forward by `x |-> x + h`. -/
def density (W : WienerData) (g : ℝ≥0 → ℝ) (x : WienerPath) : ℝ≥0∞ :=
  ENNReal.ofReal (Real.exp
    (W.paleyWienerIntegral g x - cameronMartinEnergy g))

/-- Mutual absolute continuity, expressed without relying on a name-level equivalence alias. -/
def Equivalent (μ ν : Measure WienerPath) : Prop := μ ≪ ν ∧ ν ≪ μ

/-- Exact statement target: admissible translations are precisely the equivalent ones, with the
Cameron-Martin exponential density; every non-admissible translation is singular. -/
def CameronMartinTarget : Prop :=
  ∀ (W : WienerData) (h : WienerPath),
    (Equivalent (translatedMeasure W.measure h) W.measure ↔ IsCameronMartinDirection h) ∧
    (∀ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure →
      (∀ t : ℝ≥0, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure) →
      (translatedMeasure W.measure h).rnDeriv W.measure =ᵐ[W.measure] density W g) ∧
    (¬ IsCameronMartinDirection h →
      Measure.MutuallySingular (translatedMeasure W.measure h) W.measure)

/-- Direct expansion used to check binder order, translation orientation, density direction, and
the negative singularity branch. -/
theorem target_iff_expanded : CameronMartinTarget ↔
    ∀ (W : WienerData) (h : WienerPath),
      ((translatedMeasure W.measure h ≪ W.measure ∧
          W.measure ≪ translatedMeasure W.measure h) ↔ IsCameronMartinDirection h) ∧
      (∀ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure →
        (∀ t : ℝ≥0, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure) →
        (translatedMeasure W.measure h).rnDeriv W.measure =ᵐ[W.measure] density W g) ∧
      (¬ IsCameronMartinDirection h →
        Measure.MutuallySingular (translatedMeasure W.measure h) W.measure) := by
  rfl

def mutationRemovedSingularity : Prop :=
  ∀ (W : WienerData) (h : WienerPath),
    (Equivalent (translatedMeasure W.measure h) W.measure ↔ IsCameronMartinDirection h) ∧
    (∀ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure →
      (∀ t : ℝ≥0, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure) →
      (translatedMeasure W.measure h).rnDeriv W.measure =ᵐ[W.measure] density W g)

def mutationReversedTranslation : Prop :=
  ∀ (W : WienerData) (h : WienerPath),
    (Equivalent (W.measure.map (fun x => x - h)) W.measure ↔ IsCameronMartinDirection h) ∧
    (∀ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure →
      (∀ t : ℝ≥0, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure) →
      (W.measure.map (fun x => x - h)).rnDeriv W.measure =ᵐ[W.measure] density W g) ∧
    (¬ IsCameronMartinDirection h →
      Measure.MutuallySingular (W.measure.map (fun x => x - h)) W.measure)

def mutationOnlyForwardAC : Prop :=
  ∀ (W : WienerData) (h : WienerPath),
    (translatedMeasure W.measure h ≪ W.measure ↔ IsCameronMartinDirection h) ∧
    (∀ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure →
      (∀ t : ℝ≥0, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure) →
      (translatedMeasure W.measure h).rnDeriv W.measure =ᵐ[W.measure] density W g) ∧
    (¬ IsCameronMartinDirection h →
      Measure.MutuallySingular (translatedMeasure W.measure h) W.measure)

def mutationFiniteEnergyWithoutIntegralRepresentation : Prop :=
  ∀ (W : WienerData) (h : WienerPath),
    (Equivalent (translatedMeasure W.measure h) W.measure ↔
      ∃ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure) ∧
    (∀ g : ℝ≥0 → ℝ, MemLp g 2 timeMeasure →
      (∀ t : ℝ≥0, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure) →
      (translatedMeasure W.measure h).rnDeriv W.measure =ᵐ[W.measure] density W g) ∧
    (¬ IsCameronMartinDirection h →
      Measure.MutuallySingular (translatedMeasure W.measure h) W.measure)

/-- The zero direction is included by the selected nonnegative-time convention. -/
theorem zero_isCameronMartinDirection : IsCameronMartinDirection (0 : WienerPath) := by
  refine ⟨0, ?_, ?_⟩
  · simp
  · intro t
    simp

#print Stage1Instances.THM_M_1045.CameronMartinTarget

end Stage1Instances.THM_M_1045
