import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.MeasureTheory.Measure.Decomposition.Lebesgue
import Mathlib.Probability.Distributions.Gaussian.Basic
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Process.FiniteDimensionalLaws
import Mathlib.Probability.Process.Kolmogorov

/-!
# S1-M-238 / THM-M-1045: Cameron-Martin theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Cameron-Martin theorem: translations of Wiener measure by Cameron-Martin
directions are quasi-invariant, with a Radon-Nikodym density.

The repo-local checked content below does not construct Wiener measure on a
path space, identify its Cameron-Martin space, or prove the terminal
quasi-invariance theorem.  It freezes:

* a translation map on a real normed path-space candidate;
* the translated measure as a mathlib `Measure.map`;
* the absolute-continuity/equivalence and Radon-Nikodym-density conclusion;
* a Hilbert Cameron-Martin direction interface with embedding, energy, norm,
  translation, and the expected exponential density expression;
* an abstract model whose fields are exactly the future Cameron-Martin proof
  obligations; and
* small checked wrappers around mathlib Gaussian-process, Gaussian-measure,
  Radon-Nikodym, and quasi-measure-preserving APIs.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal MeasureTheory RealInnerProductSpace

namespace AwesomeTheorems.Stage1.S1_M_238

universe u v

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- The nonnegative-real Brownian time axis used by the Wiener-space scaffold. -/
abbrev BrownianTime := ℝ≥0

/-- Variance parameter for the Brownian increment from `s` to `t`, assuming `s ≤ t`. -/
def brownianIncrementVariance (s t : BrownianTime) (hst : s ≤ t) : ℝ≥0 :=
  ⟨(t : ℝ) - (s : ℝ), sub_nonneg.mpr (by exact_mod_cast hst)⟩

/--
The finite-dimensional coordinate law of a candidate Wiener measure.

For a finite set `I` of times, this is the push-forward of the path measure by
the coordinate-vector map `x ↦ I.restrict (coordinate · x)`.
-/
def coordinateFiniteDimensionalLaw {Path : Type*} [MeasurableSpace Path]
    (μ : Measure Path) (coordinate : BrownianTime → Path → ℝ)
    (I : Finset BrownianTime) : Measure ((t : I) → ℝ) :=
  μ.map (fun x ↦ I.restrict (coordinate · x))

/--
A finite-coordinate cylinder event in a path-space candidate.

For a finite set `I` of Brownian times and a measurable target set `A` in the
finite-dimensional coordinate space, this is the event that the coordinate
vector of a path lies in `A`.
-/
def coordinateCylinder {Path : Type*} [MeasurableSpace Path]
    (coordinate : BrownianTime → Path → ℝ) (I : Finset BrownianTime)
    (A : Set ((t : I) → ℝ)) : Set Path :=
  {x | I.restrict (coordinate · x) ∈ A}

/-- A coordinate cylinder is measurable when its coordinate-vector map is measurable. -/
theorem measurableSet_coordinateCylinder {Path : Type*} [MeasurableSpace Path]
    (coordinate : BrownianTime → Path → ℝ) (I : Finset BrownianTime)
    {A : Set ((t : I) → ℝ)}
    (hmap : Measurable fun x : Path ↦ I.restrict (coordinate · x))
    (hA : MeasurableSet A) :
    MeasurableSet (coordinateCylinder coordinate I A) :=
  hA.preimage hmap

/--
Checked local scaffold for the Wiener-space part of Cameron-Martin.

This structure does not construct Wiener measure.  It records exactly the
coordinate-map and Brownian finite-dimensional-law data needed to turn a future
Wiener-space construction, or a pinned external Brownian construction, into a
mathlib `IsGaussianProcess` fact.
-/
structure WienerSpaceScaffold (Path : Type*) [MeasurableSpace Path] where
  wienerMeasure : Measure Path
  coordinate : BrownianTime → Path → ℝ
  coordinate_aemeasurable : ∀ t : BrownianTime, AEMeasurable (coordinate t) wienerMeasure
  finite_dimensional_gaussian :
    ∀ I : Finset BrownianTime, HasGaussianLaw (fun x ↦ I.restrict (coordinate · x)) wienerMeasure
  increment_hasLaw :
    ∀ ⦃s t : BrownianTime⦄, (hst : s ≤ t) →
      HasLaw (fun x ↦ coordinate t x - coordinate s x)
        (gaussianReal 0 (brownianIncrementVariance s t hst)) wienerMeasure
  starts_at_zero : ∀ᵐ x ∂wienerMeasure, coordinate 0 x = 0

/-- The finite-dimensional laws of a scaffold are the canonical coordinate push-forwards. -/
def WienerSpaceScaffold.finiteDimensionalLaw {Path : Type*} [MeasurableSpace Path]
    (W : WienerSpaceScaffold Path) (I : Finset BrownianTime) : Measure ((t : I) → ℝ) :=
  coordinateFiniteDimensionalLaw W.wienerMeasure W.coordinate I

/-- A checked `IsGaussianProcess` bridge from Brownian finite-dimensional laws. -/
theorem WienerSpaceScaffold.isGaussianProcess {Path : Type*} [MeasurableSpace Path]
    (W : WienerSpaceScaffold Path) :
    IsGaussianProcess W.coordinate W.wienerMeasure where
  hasGaussianLaw := W.finite_dimensional_gaussian

/--
The coordinate finite-dimensional laws of a scaffold form a projective family.

This uses mathlib's stochastic-process finite-dimensional-law API and is the
repo-local bridge needed before a measure-extension argument can target the
path-space sigma-algebra.
-/
theorem WienerSpaceScaffold.isProjectiveMeasureFamily_finiteDimensionalLaw
    {Path : Type*} [MeasurableSpace Path] (W : WienerSpaceScaffold Path) :
    IsProjectiveMeasureFamily (α := fun _ : BrownianTime ↦ ℝ) W.finiteDimensionalLaw := by
  simpa [WienerSpaceScaffold.finiteDimensionalLaw, coordinateFiniteDimensionalLaw] using
    (isProjectiveMeasureFamily_map_restrict (X := W.coordinate)
      (P := W.wienerMeasure) W.coordinate_aemeasurable)

/-- A checked wrapper exposing every coordinate as an a.e.-measurable random variable. -/
theorem WienerSpaceScaffold.aemeasurable_coordinate
    {Path : Type*} [MeasurableSpace Path] (W : WienerSpaceScaffold Path)
    (t : BrownianTime) :
    AEMeasurable (W.coordinate t) W.wienerMeasure :=
  W.coordinate_aemeasurable t

/-- A checked wrapper exposing the Brownian one-increment law field. -/
theorem WienerSpaceScaffold.hasLaw_increment
    {Path : Type*} [MeasurableSpace Path] (W : WienerSpaceScaffold Path)
    {s t : BrownianTime} (hst : s ≤ t) :
    HasLaw (fun x ↦ W.coordinate t x - W.coordinate s x)
      (gaussianReal 0 (brownianIncrementVariance s t hst)) W.wienerMeasure :=
  W.increment_hasLaw hst

/-- Translation by a deterministic path/direction. -/
def translatePath (h : E) (x : E) : E :=
  x + h

/-- Push-forward of a path-space measure under translation by `h`. -/
def translatedMeasure (μ : Measure E) (h : E) : Measure E :=
  μ.map (translatePath h)

/--
The measure-equivalence part of the Cameron-Martin conclusion for a
translation direction `h`.
-/
def CameronMartinEquivalence (μ : Measure E) (h : E) : Prop :=
  translatedMeasure μ h ≪ μ ∧ μ ≪ translatedMeasure μ h

/--
The Radon-Nikodym-density part of the Cameron-Martin conclusion.

The density is deliberately a supplied `E → ℝ≥0∞` function.  A later terminal
formalization should replace it by the usual exponential expression involving
the Cameron-Martin inner product and energy once the path-space/Cameron-Martin
model is available in the local Lean closure.
-/
def RNDerivativeMatches (μ : Measure E) (h : E) (density : E → ℝ≥0∞) : Prop :=
  (translatedMeasure μ h).rnDeriv μ =ᵐ[μ] density

/--
Cylinder-set density identities for a translation direction.

The intended Cameron-Martin instance has `cylinderSets` as the finite-coordinate
cylinders and `density` as the exponential Cameron-Martin density.  The
identity states equality of the translated measure and the candidate density
measure on each cylinder generator.
-/
def CylinderDensityIdentity (μ : Measure E) (h : E) (density : E → ℝ≥0∞)
    (cylinderSets : Set (Set E)) : Prop :=
  ∀ s ∈ cylinderSets, translatedMeasure μ h s = μ.withDensity density s

/--
Data needed to extend cylinder-set density identities to the full path-space
sigma-algebra.

This is the monotone-class/measure-extension boundary for the Cameron-Martin
proof branch: once finite-dimensional Gaussian shift identities give equality
on a generating π-system of cylinders, the fields below are enough to promote
the identity to equality of measures on all measurable path-space events.
-/
structure CylinderDensityExtensionData (μ : Measure E) (h : E)
    (density : E → ℝ≥0∞) where
  cylinderSets : Set (Set E)
  generate_cylinders : ‹MeasurableSpace E› = MeasurableSpace.generateFrom cylinderSets
  cylinder_piSystem : IsPiSystem cylinderSets
  spanningSets : ℕ → Set E
  spanning_iUnion : ⋃ n, spanningSets n = Set.univ
  spanning_mem : ∀ n, spanningSets n ∈ cylinderSets
  translated_spanning_ne_top :
    ∀ n, translatedMeasure μ h (spanningSets n) ≠ ∞
  cylinder_density_identity :
    CylinderDensityIdentity μ h density cylinderSets

omit [NormedSpace ℝ E] [BorelSpace E] in
/--
Cylinder-set density identities extend to equality of the translated measure
and the candidate density measure on the full generated sigma-algebra.
-/
theorem CylinderDensityExtensionData.translatedMeasure_eq_withDensity
    {μ : Measure E} {h : E} {density : E → ℝ≥0∞}
    (D : CylinderDensityExtensionData (E := E) μ h density) :
    translatedMeasure μ h = μ.withDensity density := by
  exact Measure.ext_of_generateFrom_of_iUnion D.cylinderSets D.spanningSets
    D.generate_cylinders D.cylinder_piSystem D.spanning_iUnion D.spanning_mem
    D.translated_spanning_ne_top D.cylinder_density_identity

omit [NormedSpace ℝ E] [BorelSpace E] in
/--
The same extension package yields the repo-local Radon-Nikodym-density
statement expected by the Cameron-Martin boundary.
-/
theorem CylinderDensityExtensionData.rnDerivativeMatches
    {μ : Measure E} {h : E} {density : E → ℝ≥0∞}
    [SigmaFinite μ]
    (D : CylinderDensityExtensionData (E := E) μ h density)
    (hdensity : Measurable density) :
    RNDerivativeMatches μ h density := by
  rw [RNDerivativeMatches, D.translatedMeasure_eq_withDensity]
  exact Measure.rnDeriv_withDensity _ hdensity

/--
Finite-dimensional standard-Gaussian shift density
`exp(⟪h, x⟫ - ‖h‖² / 2)`, written as an `ℝ≥0∞` density.

This is the finite-dimensional analogue of the Cameron-Martin density.  The
structure below records the remaining vector-valued `withDensity` identity as
the exact integration point needed to obtain a mathlib `Measure.rnDeriv`
statement.
-/
def finiteDimensionalGaussianShiftDensity
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    (h x : F) : ℝ≥0∞ :=
  ENNReal.ofReal (Real.exp (⟪h, x⟫ - ‖h‖ ^ (2 : Nat) / 2))

/-- The finite-dimensional standard-Gaussian shift density is measurable. -/
theorem finiteDimensionalGaussianShiftDensity_measurable
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [MeasurableSpace F] [BorelSpace F] (h : F) :
    Measurable (finiteDimensionalGaussianShiftDensity h) := by
  have h_exp : Measurable fun x : F =>
      Real.exp (⟪h, x⟫ - ‖h‖ ^ (2 : Nat) / 2) := by
    fun_prop
  simpa [finiteDimensionalGaussianShiftDensity] using h_exp.ennreal_ofReal

/--
Repo-local finite-dimensional standard-Gaussian shift package.

For a finite-dimensional real Hilbert space, the mathematical theorem is the
`shifted_eq_withDensity` field.  Once that field is supplied by a local proof or
pinned import, the lemmas below turn it into absolute continuity and an exact
`Measure.rnDeriv` density statement without further Gaussian reasoning.
-/
structure FiniteDimensionalGaussianShiftRNData
    (F : Type*) [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F] [MeasurableSpace F] [BorelSpace F] where
  shift : F
  shifted_eq_withDensity :
    translatedMeasure (E := F) (stdGaussian F) shift =
      (stdGaussian F).withDensity (finiteDimensionalGaussianShiftDensity shift)

/-- The finite-dimensional shift package gives the forward absolute-continuity branch. -/
theorem FiniteDimensionalGaussianShiftRNData.translated_ac
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F] [MeasurableSpace F] [BorelSpace F]
    (D : FiniteDimensionalGaussianShiftRNData F) :
    translatedMeasure (E := F) (stdGaussian F) D.shift ≪ stdGaussian F := by
  rw [D.shifted_eq_withDensity]
  exact withDensity_absolutelyContinuous _ _

/-- The finite-dimensional shift package gives the `Measure.rnDeriv` density branch. -/
theorem FiniteDimensionalGaussianShiftRNData.rnDeriv_eq_density
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F] [MeasurableSpace F] [BorelSpace F]
    (D : FiniteDimensionalGaussianShiftRNData F) :
    RNDerivativeMatches (E := F) (stdGaussian F) D.shift
      (finiteDimensionalGaussianShiftDensity D.shift) := by
  rw [RNDerivativeMatches, D.shifted_eq_withDensity]
  exact Measure.rnDeriv_withDensity _ (finiteDimensionalGaussianShiftDensity_measurable D.shift)

/-- One-dimensional standard-Gaussian shift density, exposed with real multiplication. -/
def standardRealGaussianShiftDensity (h x : ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal (Real.exp (h * x - h ^ (2 : Nat) / 2))

/-- The one-dimensional standard-Gaussian shift density is measurable. -/
theorem standardRealGaussianShiftDensity_measurable (h : ℝ) :
    Measurable (standardRealGaussianShiftDensity h) := by
  have h_exp : Measurable fun x : ℝ => Real.exp (h * x - h ^ (2 : Nat) / 2) := by
    fun_prop
  simpa [standardRealGaussianShiftDensity] using h_exp.ennreal_ofReal

/-- The one-dimensional standard-Gaussian shift density is everywhere nonzero. -/
theorem standardRealGaussianShiftDensity_ne_zero (h x : ℝ) :
    standardRealGaussianShiftDensity h x ≠ 0 :=
  ne_of_gt (ENNReal.ofReal_pos.mpr (Real.exp_pos _))

/--
The density multiplication identity behind the one-dimensional standard
Gaussian shift formula.
-/
theorem gaussianPDF_zero_mul_shiftDensity_eq (h : ℝ) :
    (fun x : ℝ => gaussianPDF 0 1 x * standardRealGaussianShiftDensity h x) =
      gaussianPDF h 1 := by
  funext x
  rw [gaussianPDF, standardRealGaussianShiftDensity,
    ← ENNReal.ofReal_mul (gaussianPDFReal_nonneg 0 1 x)]
  congr 1
  rw [gaussianPDFReal]
  simp only [NNReal.coe_one, sub_zero, mul_one]
  rw [mul_assoc, ← Real.exp_add]
  congr 1
  · norm_num
  · congr 1
    norm_num
    ring

/--
The repo-local closed one-dimensional standard Gaussian shift identity:
the law of `X + h`, for `X ~ N(0,1)`, is the original Gaussian measure with
density `exp(hx - h²/2)`.
-/
theorem gaussianReal_shifted_eq_withDensity (h : ℝ) :
    (gaussianReal 0 1).map (fun x : ℝ => x + h) =
      (gaussianReal 0 1).withDensity (standardRealGaussianShiftDensity h) := by
  rw [gaussianReal_map_add_const]
  simp only [zero_add]
  rw [gaussianReal_of_var_ne_zero (μ := 0) (v := 1) (by norm_num),
    gaussianReal_of_var_ne_zero (μ := h) (v := 1) (by norm_num)]
  rw [← withDensity_mul volume (measurable_gaussianPDF 0 1)
    (standardRealGaussianShiftDensity_measurable h)]
  change volume.withDensity (gaussianPDF h 1) =
    volume.withDensity (fun x : ℝ => gaussianPDF 0 1 x * standardRealGaussianShiftDensity h x)
  rw [gaussianPDF_zero_mul_shiftDensity_eq h]

/-- The generic translation boundary specializes to the one-dimensional Gaussian shift identity. -/
theorem standardRealGaussianShift_translatedMeasure_eq_withDensity (h : ℝ) :
    translatedMeasure (E := ℝ) (gaussianReal 0 1) h =
      (gaussianReal 0 1).withDensity (standardRealGaussianShiftDensity h) := by
  simpa [translatedMeasure, translatePath] using gaussianReal_shifted_eq_withDensity h

/-- The shifted one-dimensional standard Gaussian is absolutely continuous with respect to `N(0,1)`. -/
theorem standardRealGaussianShift_translated_ac (h : ℝ) :
    translatedMeasure (E := ℝ) (gaussianReal 0 1) h ≪ gaussianReal 0 1 := by
  rw [standardRealGaussianShift_translatedMeasure_eq_withDensity]
  exact withDensity_absolutelyContinuous _ _

/-- The base `N(0,1)` is absolutely continuous with respect to its nonzero translate. -/
theorem standardRealGaussianShift_base_ac_translated (h : ℝ) :
    gaussianReal 0 1 ≪ translatedMeasure (E := ℝ) (gaussianReal 0 1) h := by
  rw [standardRealGaussianShift_translatedMeasure_eq_withDensity]
  exact withDensity_absolutelyContinuous'
    (standardRealGaussianShiftDensity_measurable h).aemeasurable
    (ae_of_all _ (standardRealGaussianShiftDensity_ne_zero h))

/-- The one-dimensional standard Gaussian shift has the expected `Measure.rnDeriv` density. -/
theorem rnDerivativeMatches_standardRealGaussianShift (h : ℝ) :
    RNDerivativeMatches (E := ℝ) (gaussianReal 0 1) h
      (standardRealGaussianShiftDensity h) := by
  rw [RNDerivativeMatches, standardRealGaussianShift_translatedMeasure_eq_withDensity]
  exact Measure.rnDeriv_withDensity _ (standardRealGaussianShiftDensity_measurable h)

/-- The one-dimensional standard Gaussian shift satisfies the local Cameron-Martin conclusion. -/
theorem cameronMartinConclusion_standardRealGaussianShift (h : ℝ) :
    CameronMartinEquivalence (E := ℝ) (gaussianReal 0 1) h ∧
      RNDerivativeMatches (E := ℝ) (gaussianReal 0 1) h
        (standardRealGaussianShiftDensity h) :=
  ⟨⟨standardRealGaussianShift_translated_ac h,
      standardRealGaussianShift_base_ac_translated h⟩,
    rnDerivativeMatches_standardRealGaussianShift h⟩

omit [NormedSpace ℝ E] in
/-- Translation by any fixed direction is Borel-measurable on the path-space candidate. -/
theorem measurable_translatePath (h : E) : Measurable (translatePath h) :=
  (continuous_id.add continuous_const).measurable

/--
Hilbert-space data expected from a Cameron-Martin direction package.

`H` is the Cameron-Martin Hilbert space, `embed` is its continuous linear
embedding into the ambient path-space candidate `E`, and `gaussianPairing`
stands for the measurable Paley-Wiener pairing `x ↦ ⟪h, x⟫` that appears in
the Radon-Nikodym density.  The actual Gaussian-shift theorem is not assumed by
this structure.
-/
structure CameronMartinHilbertData
    (H : Type v) [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H] where
  embed : H →L[ℝ] E
  embed_injective : Function.Injective embed
  gaussianPairing : H → E → ℝ
  gaussianPairing_measurable : ∀ h : H, Measurable (gaussianPairing h)

/-- The Cameron-Martin Hilbert norm, exposed as a named boundary object. -/
def cameronMartinNorm {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    [CompleteSpace H] (h : H) : ℝ :=
  ‖h‖

/-- The Cameron-Martin energy term `1 / 2 * ‖h‖²` used in the density exponent. -/
def cameronMartinEnergy {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    [CompleteSpace H] (h : H) : ℝ :=
  ‖h‖ ^ (2 : Nat) / 2

/-- The Cameron-Martin energy is nonnegative. -/
theorem cameronMartinEnergy_nonneg
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (h : H) :
    0 ≤ cameronMartinEnergy h := by
  unfold cameronMartinEnergy
  positivity

/-- The Hilbert-data embedding as a plain map into the path-space candidate. -/
def CameronMartinHilbertData.embedding
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) : H → E :=
  D.embed

omit [BorelSpace E] in
/-- The Hilbert-data embedding is injective. -/
theorem CameronMartinHilbertData.embedding_injective
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) :
    Function.Injective D.embedding :=
  D.embed_injective

/-- Translation of path space by the embedded Cameron-Martin direction. -/
def CameronMartinHilbertData.translationMap
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) (h : H) : E → E :=
  translatePath (D.embed h)

/-- The Hilbert-data translation map is Borel-measurable. -/
theorem CameronMartinHilbertData.translationMap_measurable
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) (h : H) :
    Measurable (D.translationMap h) :=
  measurable_translatePath (D.embed h)

/-- Push-forward of a path-space measure by a Cameron-Martin Hilbert translation. -/
def CameronMartinHilbertData.translatedMeasure
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) (μ : Measure E) (h : H) : Measure E :=
  μ.map (D.translationMap h)

omit [BorelSpace E] in
/-- The Hilbert-data translated measure agrees with the generic translation boundary. -/
theorem CameronMartinHilbertData.translatedMeasure_eq
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) (μ : Measure E) (h : H) :
    D.translatedMeasure μ h =
      AwesomeTheorems.Stage1.S1_M_238.translatedMeasure μ (D.embed h) :=
  rfl

/--
The Cameron-Martin Radon-Nikodym density expression
`exp(⟪h, x⟫ - ‖h‖² / 2)`, coerced to `ℝ≥0∞`.

The pairing is supplied by `CameronMartinHilbertData` because on a Banach path
space it is generally a measurable Gaussian linear functional rather than the
ambient normed-space inner product.
-/
def cameronMartinDensityExpression
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) (h : H) (x : E) : ℝ≥0∞ :=
  ENNReal.ofReal (Real.exp (D.gaussianPairing h x - cameronMartinEnergy h))

omit [BorelSpace E] in
/-- The Cameron-Martin exponential density expression is measurable. -/
theorem CameronMartinHilbertData.densityExpression_measurable
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) (h : H) :
    Measurable (cameronMartinDensityExpression D h) := by
  have h_exp : Measurable fun x : E =>
      Real.exp (D.gaussianPairing h x - cameronMartinEnergy h) :=
    Real.measurable_exp.comp ((D.gaussianPairing_measurable h).sub measurable_const)
  simpa [cameronMartinDensityExpression] using h_exp.ennreal_ofReal

/--
Abstract Stage1 model for a Cameron-Martin theorem over a path-space candidate.

`wienerMeasure` is required to be a mathlib Gaussian measure, but the file does
not assume that mathlib already has a canonical Wiener-space construction.  The
fields after `density` are the proof obligations that a future local proof body
or pinned external Lean 4 dependency must provide.
-/
structure CameronMartinModel where
  wienerMeasure : Measure E
  isGaussian : IsGaussian wienerMeasure
  CameronMartinSpace : Type v
  embed : CameronMartinSpace → E
  energy : CameronMartinSpace → ℝ
  density : CameronMartinSpace → E → ℝ≥0∞
  translate_measurable :
    ∀ h : CameronMartinSpace, Measurable (translatePath (embed h))
  density_measurable :
    ∀ h : CameronMartinSpace, Measurable (density h)
  translated_absolutelyContinuous :
    ∀ h : CameronMartinSpace, translatedMeasure wienerMeasure (embed h) ≪ wienerMeasure
  base_absolutelyContinuous_translated :
    ∀ h : CameronMartinSpace, wienerMeasure ≪ translatedMeasure wienerMeasure (embed h)
  rnDeriv_eq_density :
    ∀ h : CameronMartinSpace,
      RNDerivativeMatches wienerMeasure (embed h) (density h)

attribute [instance] CameronMartinModel.isGaussian

/--
Promote checked Hilbert Cameron-Martin boundary data into the abstract model
once the two absolute-continuity branches and the Radon-Nikodym identity are
supplied by a future local proof body or pinned external dependency.
-/
def CameronMartinModel.ofHilbertData
    {H : Type v} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (D : CameronMartinHilbertData (E := E) H) (μ : Measure E) [IsGaussian μ]
    (translated_ac : ∀ h : H, translatedMeasure μ (D.embed h) ≪ μ)
    (base_ac_translated : ∀ h : H, μ ≪ translatedMeasure μ (D.embed h))
    (rnDeriv_density : ∀ h : H,
      RNDerivativeMatches μ (D.embed h) (cameronMartinDensityExpression D h)) :
    CameronMartinModel.{u, v} (E := E) where
  wienerMeasure := μ
  isGaussian := inferInstance
  CameronMartinSpace := H
  embed := D.embed
  energy := cameronMartinEnergy
  density := cameronMartinDensityExpression D
  translate_measurable := D.translationMap_measurable
  density_measurable := D.densityExpression_measurable
  translated_absolutelyContinuous := translated_ac
  base_absolutelyContinuous_translated := base_ac_translated
  rnDeriv_eq_density := rnDeriv_density

/--
Design choices considered for the repo-local Cameron-Martin formalization.

The selected route is recorded below as checked metadata.  It is not a proof of
the terminal theorem; it fixes the interface that later concrete Wiener-space or
abstract-Wiener-space instances should target.
-/
inductive ModelingStrategy where
  | concreteContinuousPathWienerSpace
  | abstractWienerSpace
  | reusableGaussianQuasiInvarianceInterface
  deriving DecidableEq, Repr

/--
Stage1 design decision for this slot: build the theorem around a reusable
Gaussian-measure quasi-invariance interface first.
-/
def selectedModelingStrategy : ModelingStrategy :=
  .reusableGaussianQuasiInvarianceInterface

/--
Checked rationale metadata for `selectedModelingStrategy`.

The current local closure has Gaussian-measure, Gaussian-process,
Radon-Nikodym, measure-map, and quasi-measure-preserving APIs.  It does not yet
have a repo-local continuous-path Wiener-space construction or a full abstract
Wiener-space package, so those should be future instances of the reusable
interface rather than the initial theorem boundary.
-/
def selectedModelingStrategyRationale : List String := [
  "Use a reusable Gaussian-measure quasi-invariance interface as the first \
    repo-local boundary.",
  "Represent Cameron-Martin directions by a real Hilbert space with a continuous \
    linear embedding into the path-space candidate, energy norm squared over two, \
    and a measurable exponential density expression.",
  "Treat a concrete continuous-path Wiener space as a later instance once \
    coordinate maps, finite-dimensional Brownian laws, continuity, and the \
    IsGaussianProcess bridge are locally available or pinned.",
  "Treat an abstract Wiener space as a later generalization after the Hilbert \
    embedding, measurable Banach completion, and density formula are available.",
  "Do not mark Cameron-Martin completed until a repo-local proof body or \
    pinned/imported terminal Lean proof validates."
]

/-- The recorded Stage1 design decision is the reusable quasi-invariance interface. -/
theorem selectedModelingStrategy_eq :
    selectedModelingStrategy =
      ModelingStrategy.reusableGaussianQuasiInvarianceInterface :=
  rfl

/-- The formal conclusion expected from the Cameron-Martin theorem. -/
def CameronMartinConclusion (M : CameronMartinModel.{u, v} (E := E))
    (h : M.CameronMartinSpace) : Prop :=
  CameronMartinEquivalence M.wienerMeasure (M.embed h) ∧
    RNDerivativeMatches M.wienerMeasure (M.embed h) (M.density h)

omit [BorelSpace E] in
/--
Terminal local wrapper for the abstract Cameron-Martin conclusion.

This theorem does not prove Cameron-Martin quasi-invariance from first
principles; it packages the absolute-continuity and Radon-Nikodym fields of a
`CameronMartinModel` into the normalized conclusion expected by this Stage1
slot.
-/
theorem CameronMartinModel.cameronMartinConclusion
    (M : CameronMartinModel.{u, v} (E := E)) (h : M.CameronMartinSpace) :
    CameronMartinConclusion M h :=
  ⟨⟨M.translated_absolutelyContinuous h, M.base_absolutelyContinuous_translated h⟩,
    M.rnDeriv_eq_density h⟩

/--
Stage1 normalized statement shape.

For every declared Cameron-Martin model and every Cameron-Martin direction, the
translated Wiener measure is equivalent to the original Wiener measure and has
the declared Radon-Nikodym density.
-/
def StatementShape : Prop :=
  ∀ (M : CameronMartinModel.{u, v} (E := E)) (h : M.CameronMartinSpace),
    CameronMartinConclusion M h

omit [BorelSpace E] in
/-- The statement shape unfolds to the expected model/direction quantification. -/
theorem statementShape_iff_forall_model :
    StatementShape.{u, v} (E := E) ↔
      ∀ (M : CameronMartinModel.{u, v} (E := E)) (h : M.CameronMartinSpace),
        CameronMartinConclusion M h :=
  ⟨fun h M d => h M d, fun h M d => h M d⟩

omit [BorelSpace E] in
/--
If a future package supplies the Cameron-Martin model fields, the repo-local
wrapper projects the equivalence and Radon-Nikodym-density conclusion.
-/
theorem statementShape_from_model_fields :
    StatementShape.{u, v} (E := E) := by
  intro M h
  exact M.cameronMartinConclusion h

omit [BorelSpace E] in
/-- Project the absolute-continuity branch from the normalized conclusion. -/
theorem CameronMartinConclusion.translated_ac
    {M : CameronMartinModel.{u, v} (E := E)} {h : M.CameronMartinSpace}
    (hc : CameronMartinConclusion M h) :
    translatedMeasure M.wienerMeasure (M.embed h) ≪ M.wienerMeasure :=
  hc.1.1

omit [BorelSpace E] in
/-- Project the reverse absolute-continuity branch from the normalized conclusion. -/
theorem CameronMartinConclusion.base_ac_translated
    {M : CameronMartinModel.{u, v} (E := E)} {h : M.CameronMartinSpace}
    (hc : CameronMartinConclusion M h) :
    M.wienerMeasure ≪ translatedMeasure M.wienerMeasure (M.embed h) :=
  hc.1.2

omit [BorelSpace E] in
/-- Project the Radon-Nikodym-density branch from the normalized conclusion. -/
theorem CameronMartinConclusion.rnDeriv_density
    {M : CameronMartinModel.{u, v} (E := E)} {h : M.CameronMartinSpace}
    (hc : CameronMartinConclusion M h) :
    RNDerivativeMatches M.wienerMeasure (M.embed h) (M.density h) :=
  hc.2

omit [NormedSpace ℝ E] [BorelSpace E] in
/-- Translation by zero leaves a measure unchanged. -/
theorem translatedMeasure_zero (μ : Measure E) :
    translatedMeasure μ (0 : E) = μ := by
  calc
    translatedMeasure μ (0 : E) = μ.map id := by
      rw [translatedMeasure]
      exact Measure.map_congr (by filter_upwards with x; simp [translatePath])
    _ = μ := Measure.map_id

omit [NormedSpace ℝ E] [BorelSpace E] in
/-- The zero translation gives measure equivalence without using Cameron-Martin theory. -/
theorem cameronMartinEquivalence_zero (μ : Measure E) :
    CameronMartinEquivalence μ (0 : E) := by
  simp [CameronMartinEquivalence, translatedMeasure_zero, Measure.AbsolutelyContinuous.rfl]

omit [NormedSpace ℝ E] [BorelSpace E] in
/-- For a sigma-finite measure, the self Radon-Nikodym derivative is `1` a.e. -/
theorem rnDerivativeMatches_zero_one
    (μ : Measure E) [SigmaFinite μ] :
    RNDerivativeMatches μ (0 : E) (fun _ : E => (1 : ℝ≥0∞)) := by
  simpa [RNDerivativeMatches, translatedMeasure_zero] using Measure.rnDeriv_self μ

omit [NormedSpace ℝ E] [BorelSpace E] in
/--
Absolute continuity of the translated measure is exactly the second field of a
mathlib `QuasiMeasurePreserving` translation map once measurability is supplied.
-/
theorem quasiMeasurePreserving_translation_of_ac
    {μ : Measure E} {h : E}
    (hmeas : Measurable (translatePath h))
    (hac : translatedMeasure μ h ≪ μ) :
    Measure.QuasiMeasurePreserving (translatePath h) μ μ :=
  ⟨hmeas, hac⟩

/-- A checked wrapper around mathlib's Gaussian-process evaluation measurability. -/
theorem gaussianProcess_aemeasurable_eval
    {T Ω F : Type*} {mΩ : MeasurableSpace Ω} {P : Measure Ω}
    {X : T → Ω → F}
    [MeasurableSpace F] [TopologicalSpace F] [AddCommMonoid F] [Module ℝ F]
    (hX : IsGaussianProcess X P) (t : T) :
    AEMeasurable (X t) P :=
  hX.aemeasurable t

/-- Mapping a Gaussian measure by a continuous linear map is Gaussian in mathlib. -/
theorem isGaussian_map_continuousLinearMap
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    [MeasurableSpace F] [BorelSpace F]
    {μ : Measure E} [IsGaussian μ] (L : E →L[ℝ] F) :
    IsGaussian (μ.map L) := by
  infer_instance

/-- A checked wrapper exposing the Kolmogorov-process edge used in stochastic-process audits. -/
theorem kolmogorovProcess_aemeasurable_edist
    {T Ω F : Type*} [PseudoEMetricSpace T] {mΩ : MeasurableSpace Ω}
    [PseudoEMetricSpace F] {P : Measure Ω} {X : T → Ω → F}
    {p q : ℝ} {M : ℝ≥0}
    (hX : IsAEKolmogorovProcess X P p q M) {s t : T} :
    AEMeasurable (fun ω => edist (X s ω) (X t ω)) P :=
  hX.aemeasurable_edist

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.SpecialFunctions.Exp",
  "Mathlib.MeasureTheory.Measure.AbsolutelyContinuous",
  "Mathlib.MeasureTheory.Measure.Decomposition.Lebesgue",
  "Mathlib.MeasureTheory.Measure.QuasiMeasurePreserving",
  "Mathlib.Probability.Distributions.Gaussian.Basic",
  "Mathlib.Probability.Distributions.Gaussian.Real",
  "Mathlib.Probability.Distributions.Gaussian.Multivariate",
  "Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic",
  "Mathlib.Probability.Process.FiniteDimensionalLaws",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Kolmogorov",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Martingale.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "Measure.AbsolutelyContinuous",
  "Measure.QuasiMeasurePreserving",
  "Measure.rnDeriv",
  "Measure.rnDeriv_self",
  "Measure.rnDeriv_withDensity",
  "withDensity_mul",
  "withDensity_absolutelyContinuous",
  "withDensity_absolutelyContinuous'",
  "Measure.map_id",
  "InnerProductSpace",
  "ContinuousLinearMap",
  "Real.exp",
  "Measurable.ennreal_ofReal",
  "IsGaussian",
  "stdGaussian",
  "gaussianPDF",
  "gaussianReal_map_add_const",
  "gaussianReal_of_var_ne_zero",
  "IsGaussian.map_eq_gaussianReal",
  "isGaussian_map_continuousLinearMap",
  "IsGaussianProcess",
  "IsGaussianProcess.aemeasurable",
  "IsGaussianProcess.hasGaussianLaw",
  "IsAEKolmogorovProcess.aemeasurable_edist",
  "ProbabilityTheory.isProjectiveMeasureFamily_map_restrict",
  "Filtration",
  "Martingale",
  "IsStoppingTime"
]

/-- External Lean 4 audit candidates checked for this Stage1 slot.

These strings are audit metadata only.  They do not import an external proof and
therefore do not close the Cameron-Martin theorem locally.
-/
def externalLeanAuditAnchors : List String := [
  "mathlib@8a178386ffc0f5fef0b77738bb5449d50efeea95: no terminal Cameron-Martin, \
    abstract Wiener, Wiener-measure, Brownian-motion, or Gaussian quasi-invariance theorem \
    found by direct source search; lower-level Gaussian, RN-derivative, and \
    Gaussian-process anchors are available.",
  "RemyDegenne/brownian-motion@91885e6172648ea7f9c6a16b3a7069f92c88e023: \
    BrownianMotion.Gaussian.BrownianMotion defines IsBrownian, brownian, gaussianLimit, \
    isGaussianProcess_brownian, hasLaw_brownian_eval, continuous_brownian, and \
    hasIndepIncrements_brownian, but no Cameron-Martin quasi-invariance theorem was found; \
    toolchain leanprover/lean4:v4.30.0-rc1 is not this repo's v4.29.0 toolchain."
]

/--
Repo-local integration status for any external Lean 4 Cameron-Martin closure.

This is audit metadata, not a mathematical theorem.  The status is deliberately
separate from `externalLeanAuditAnchors`: an external Brownian/Wiener substrate
can be useful while still not being a terminal proof that may justify a
completion-state update.
-/
inductive ExternalClosureIntegrationStatus where
  | noTerminalClosureFound
  | terminalClosureBlocked
  | terminalClosurePinnedAndChecked
  deriving DecidableEq, Repr

/--
Current C009 gate result: no terminal external Lean 4 Cameron-Martin proof has
been found, pinned, imported, or checked in this repository.
-/
def externalClosureIntegrationStatus : ExternalClosureIntegrationStatus :=
  .noTerminalClosureFound

/--
Concrete blockers before any future external-anchor completion claim.

If a later authenticated audit finds a terminal external Lean 4 Cameron-Martin
theorem, this list must be replaced by repository URL, commit, module path,
theorem name, toolchain, dependency, license, placeholder, and local Lake
validation details for the pin/import/check attempt.
-/
def externalClosureIntegrationBlockers : List String := [
  "No terminal external Lean 4 theorem for Cameron-Martin quasi-invariance was \
    found in the pinned mathlib source audit or the known external Brownian-motion \
    substrate audit.",
  "GitHub code search was not authenticated in this worker environment; gh auth \
    status reported no logged-in GitHub hosts, and unauthenticated GitHub code \
    search API calls were rate-limited.",
  "The known external Brownian-motion project supplies Brownian/Wiener measure \
    substrate objects but no Cameron-Martin quasi-invariance or RN-density theorem \
    name was found.",
  "The known external Brownian-motion project is not in this repository's Lake \
    closure and uses a different Lean/mathlib pin, so it cannot be treated as \
    repo-local completion evidence."
]

/-- The C009 external-closure gate is explicitly not a pinned checked closure. -/
theorem externalClosureIntegrationStatus_eq :
    externalClosureIntegrationStatus =
      ExternalClosureIntegrationStatus.noTerminalClosureFound :=
  rfl

end AwesomeTheorems.Stage1.S1_M_238
