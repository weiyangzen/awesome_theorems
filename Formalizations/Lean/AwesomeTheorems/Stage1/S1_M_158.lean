import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.DerivNotation
import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.Analysis.Distribution.TestFunction
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.Fourier.FourierTransform
import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# S1-M-158 / THM-M-1234: Yudovich theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for
Yudovich's global existence theorem for the two-dimensional incompressible Euler
equations with bounded vorticity.

The pinned mathlib snapshot has Euclidean spaces, Bochner/Lebesgue integration,
`MemLp`, `eLpNorm`, test-function/distribution infrastructure, and first-order
Sobolev inequalities.  It does not expose a terminal API for incompressible
Euler equations, vorticity transport, Biot-Savart reconstruction, or the
Yudovich existence/uniqueness theorem.

The declarations below therefore normalize the theorem statement as explicit
data.  They intentionally do not claim the terminal PDE theorem.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal Distributions Topology

namespace AwesomeTheorems.Stage1.S1_M_158

/-- Pinned mathlib revision audited for the Stage1 Yudovich slot. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- The spatial domain model used for this Stage1 boundary: two-dimensional Euclidean space. -/
abbrev Plane : Type :=
  EuclideanSpace ℝ (Fin 2)

/-- Spacetime model for the chosen weak formulation: time plus two spatial coordinates. -/
abbrev Spacetime : Type :=
  EuclideanSpace ℝ (Fin 3)

/-- Time-dependent velocity field for a two-dimensional Euler flow. -/
abbrev VelocityField : Type :=
  ℝ → Plane → Plane

/-- Time-dependent pressure field for a two-dimensional Euler flow. -/
abbrev PressureField : Type :=
  ℝ → Plane → ℝ

/-- Time-dependent scalar vorticity field. -/
abbrev VorticityField : Type :=
  ℝ → Plane → ℝ

/-- Static velocity field on the two-dimensional plane. -/
abbrev StaticVelocityField : Type :=
  Plane → Plane

/-- Static scalar vorticity field on the two-dimensional plane. -/
abbrev StaticVorticityField : Type :=
  Plane → ℝ

/-- Coordinate projection on the local Euclidean plane model. -/
def planeCoordinate (i : Fin 2) (x : Plane) : ℝ :=
  x i

/-- The coordinate unit vector in the local Euclidean plane model. -/
def planeUnitVector (i : Fin 2) : Plane :=
  EuclideanSpace.single i (1 : ℝ)

/--
Pointwise scalar curl of a two-dimensional velocity field, expressed with
mathlib's Frechet derivative.

For `u = (u₀, u₁)`, this is the usual `∂₀ u₁ - ∂₁ u₀`.  No differentiability
claim is made here; `fderiv` supplies the derivative object available in the
current mathlib API and later proof leaves must add the hypotheses under which
this expression agrees with the distributional curl.
-/
def pointwisePlaneCurl (u : StaticVelocityField) (x : Plane) : ℝ :=
  planeCoordinate 1 (fderiv ℝ u x (planeUnitVector 0)) -
    planeCoordinate 0 (fderiv ℝ u x (planeUnitVector 1))

/-- Static pointwise vorticity-as-curl predicate for a velocity/vorticity pair. -/
def StaticPointwiseVorticityIsCurl
    (u : StaticVelocityField) (ω : StaticVorticityField) : Prop :=
  ∀ x : Plane, ω x = pointwisePlaneCurl u x

/-- The whole-plane open domain, useful for distributional PDE residuals. -/
def wholePlaneOpen : TopologicalSpace.Opens Plane :=
  ⟨Set.univ, isOpen_univ⟩

/-- The whole-spacetime open domain for spacetime distributional Euler residuals. -/
def wholeSpacetimeOpen : TopologicalSpace.Opens Spacetime :=
  ⟨Set.univ, isOpen_univ⟩

/-- Scalar distributions on the whole plane. -/
abbrev ScalarDistributionOnPlane : Type :=
  Distribution wholePlaneOpen ℝ ⊤

/-- Scalar test functions on the whole plane. -/
abbrev ScalarTestFunctionOnPlane : Type :=
  TestFunction wholePlaneOpen ℝ ⊤

/-- Scalar distributions on the whole spacetime. -/
abbrev ScalarDistributionOnSpacetime : Type :=
  Distribution wholeSpacetimeOpen ℝ ⊤

/-- Scalar test functions on the whole spacetime. -/
abbrev ScalarTestFunctionOnSpacetime : Type :=
  TestFunction wholeSpacetimeOpen ℝ ⊤

/-- Vector-valued distributional residuals are represented componentwise. -/
abbrev VectorDistributionOnSpacetime : Type :=
  Fin 2 → ScalarDistributionOnSpacetime

/-- Vector-valued distributions on the whole plane are represented componentwise. -/
abbrev VectorDistributionOnPlane : Type :=
  Fin 2 → ScalarDistributionOnPlane

/-- A scalar distributional residual vanishes when it evaluates to zero on every test function. -/
def ScalarResidualVanishes (T : ScalarDistributionOnSpacetime) : Prop :=
  ∀ φ : ScalarTestFunctionOnSpacetime, T φ = 0

/-- A vector distributional residual vanishes componentwise. -/
def VectorResidualVanishes (T : VectorDistributionOnSpacetime) : Prop :=
  ∀ i : Fin 2, ScalarResidualVanishes (T i)

/--
Static curl/vorticity compatibility package.

The pointwise field records the classical smooth formula, while the
distributional field is kept as a separate obligation because the current
mathlib snapshot does not expose a ready-made spatial distributional curl
constructor for vector distributions over `Plane`.
-/
structure StaticCurlVorticityCompatibility
    (u : StaticVelocityField) (ω : StaticVorticityField) : Type where
  pointwiseVorticityIsCurl : StaticPointwiseVorticityIsCurl u ω
  distributionalVorticityIsCurl : Prop

/-- Timewise curl/vorticity compatibility for a Yudovich velocity and scalar vorticity. -/
def TimewiseCurlVorticityCompatibility (u : VelocityField) (ω : VorticityField) : Type :=
  ∀ t : ℝ, StaticCurlVorticityCompatibility (u t) (ω t)

/-- The three domain variants that must be kept separate for Biot-Savart reconstruction. -/
inductive BiotSavartDomainVariant : Type where
  | wholePlane
  | flatTorus
  | boundedDomain
  deriving DecidableEq, Repr

namespace BiotSavartDomainVariant

/-- Stable text code for the domain variant split. -/
def code : BiotSavartDomainVariant → String
  | wholePlane => "whole_plane"
  | flatTorus => "flat_torus"
  | boundedDomain => "bounded_domain"

end BiotSavartDomainVariant

/--
Whole-plane Biot-Savart reconstruction obligation.

This branch is the singular-kernel/decay or finite-energy normalization case on
`ℝ²`.  It is intentionally a predicate boundary, not a completed theorem.
-/
structure WholePlaneBiotSavartReconstruction
    (u : VelocityField) (ω : VorticityField) : Type where
  curlVorticity : TimewiseCurlVorticityCompatibility u ω
  divergenceFree : Prop
  kernelFormulaOrFourierMultiplier : Prop
  decayOrFiniteEnergyNormalization : Prop
  velocityRecoveredFromVorticity : Prop

/--
Flat-torus Biot-Savart reconstruction obligation.

This branch must carry periodicity and mean-zero normalization separately from
the whole-plane singular-kernel branch.
-/
structure TorusBiotSavartReconstruction
    (u : VelocityField) (ω : VorticityField) : Type where
  curlVorticity : TimewiseCurlVorticityCompatibility u ω
  periodicVelocity : Prop
  periodicVorticity : Prop
  meanZeroVorticity : Prop
  meanZeroVelocityNormalization : Prop
  fourierMultiplierOrGreenFunction : Prop
  velocityRecoveredFromVorticity : Prop

/--
Bounded-domain Biot-Savart reconstruction obligation.

This branch is indexed by the spatial domain and keeps boundary conditions,
Green-function choices, and harmonic corrections explicit.
-/
structure BoundedDomainBiotSavartReconstruction
    (Ω : Set Plane) (u : VelocityField) (ω : VorticityField) : Type where
  curlVorticity : TimewiseCurlVorticityCompatibility u ω
  domainIsAdmissible : Prop
  boundaryCondition : Prop
  greenFunctionOrStreamFunction : Prop
  harmonicCorrection : Prop
  velocityRecoveredFromVorticity : Prop

/-- Variant-indexed Biot-Savart reconstruction predicate. -/
def BiotSavartReconstructionForVariant
    (variant : BiotSavartDomainVariant) (Ω : Set Plane)
    (u : VelocityField) (ω : VorticityField) : Type :=
  match variant with
  | .wholePlane => WholePlaneBiotSavartReconstruction u ω
  | .flatTorus => TorusBiotSavartReconstruction u ω
  | .boundedDomain => BoundedDomainBiotSavartReconstruction Ω u ω

/-- Whole-plane branch of the variant-indexed Biot-Savart predicate. -/
theorem biotSavartReconstructionForVariant_wholePlane
    (Ω : Set Plane) (u : VelocityField) (ω : VorticityField) :
    BiotSavartReconstructionForVariant .wholePlane Ω u ω =
      WholePlaneBiotSavartReconstruction u ω :=
  rfl

/-- Flat-torus branch of the variant-indexed Biot-Savart predicate. -/
theorem biotSavartReconstructionForVariant_flatTorus
    (Ω : Set Plane) (u : VelocityField) (ω : VorticityField) :
    BiotSavartReconstructionForVariant .flatTorus Ω u ω =
      TorusBiotSavartReconstruction u ω :=
  rfl

/-- Bounded-domain branch of the variant-indexed Biot-Savart predicate. -/
theorem biotSavartReconstructionForVariant_boundedDomain
    (Ω : Set Plane) (u : VelocityField) (ω : VorticityField) :
    BiotSavartReconstructionForVariant .boundedDomain Ω u ω =
      BoundedDomainBiotSavartReconstruction Ω u ω :=
  rfl

/--
Concrete whole-plane distributional residual package for 2D incompressible
Euler.

The intended residuals are the spacetime distributions associated to
`∂ₜ u + div (u ⊗ u) + ∇p`, `div u`, and `∂ₜω + u · ∇ω`.  The current mathlib
snapshot does not provide the nonlinear PDE constructors needed to build these
residuals from `u`, `p`, and `ω`, so this Stage1 boundary records the
mathlib-native residual objects and their test-function vanishing predicates
without claiming the existence theorem.
-/
structure WholePlaneWeakEulerResiduals
    (u : VelocityField) (p : PressureField) (ω : VorticityField) : Type where
  momentumResidual : VectorDistributionOnSpacetime
  incompressibilityResidual : ScalarDistributionOnSpacetime
  vorticityTransportResidual : ScalarDistributionOnSpacetime
  momentumResidual_vanishes : VectorResidualVanishes momentumResidual
  incompressibilityResidual_vanishes : ScalarResidualVanishes incompressibilityResidual
  vorticityTransportResidual_vanishes : ScalarResidualVanishes vorticityTransportResidual

/--
Initial data expected by the Yudovich theorem.

The analytic predicates that are not yet provided by mathlib's PDE API are kept
as explicit `Prop` fields.  The bounded-vorticity hypothesis is represented by
the available `MemLp _ ⊤ volume` object.
-/
structure YudovichInitialData (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) : Type where
  velocityMeasurable : AEStronglyMeasurable u₀ volume
  vorticityMeasurable : AEStronglyMeasurable ω₀ volume
  vorticityMemLInf : MemLp ω₀ ⊤ volume
  divergenceFree : Prop
  vorticityIsCurl : StaticCurlVorticityCompatibility u₀ ω₀
  finiteEnergyOrDecay : Prop
  domainBoundaryCondition : Prop

/-- Index type for a smooth, mollified, or Galerkin approximation family. -/
abbrev ApproximationIndex : Type :=
  ℕ

/--
Timewise bounded-vorticity propagation target.

This is the concrete `L∞` surface available in the current mathlib snapshot:
membership in `MemLp _ ⊤ volume` together with an `eLpNorm` comparison.  Later
proof leaves must supply the transport or maximum-principle argument.
-/
def TimewiseVorticityLInfBound
    (ω : VorticityField) (ω₀ : StaticVorticityField) (timeSet : Set ℝ) :
    Prop :=
  ∀ t : ℝ, t ∈ timeSet →
    MemLp (ω t) ⊤ volume ∧
      MeasureTheory.eLpNorm (ω t) ⊤ volume ≤
        MeasureTheory.eLpNorm ω₀ ⊤ volume

/--
One smooth approximation in the Yudovich existence construction.

The fields name the standard approximation leaf: smooth or finite-dimensional
initial data, a global smooth/Galerkin Euler solution, a residual package, a
uniform `L∞` vorticity target, and curl/Biot-Savart compatibility.  The hard
analytic proofs are deliberately kept as explicit obligations.
-/
structure SmoothEulerApproximation
    (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) (I : YudovichInitialData u₀ ω₀) :
    Type where
  velocity : VelocityField
  pressure : PressureField
  vorticity : VorticityField
  timeSet : Set ℝ
  coversNonnegativeTimes : {t : ℝ | 0 ≤ t} ⊆ timeSet
  smoothedInitialVelocity : StaticVelocityField
  smoothedInitialVorticity : StaticVorticityField
  smoothedInitialData :
    YudovichInitialData smoothedInitialVelocity smoothedInitialVorticity
  smoothingConvergesToInitialVelocity : Prop
  smoothingConvergesToInitialVorticity : Prop
  smoothClassicalOrGalerkinEulerSolution : Prop
  weakEulerResiduals : WholePlaneWeakEulerResiduals velocity pressure vorticity
  vorticityLInfBound :
    TimewiseVorticityLInfBound vorticity smoothedInitialVorticity timeSet
  curlVorticity : TimewiseCurlVorticityCompatibility velocity vorticity
  biotSavartCompatibility : WholePlaneBiotSavartReconstruction velocity vorticity

/--
Approximation scheme for the whole-plane Yudovich existence proof.

This packages the family-level obligations separately from any one approximant:
choice of mollifier or Galerkin basis, convergence of the approximate initial
data, global approximant existence, and uniform estimates independent of the
index.
-/
structure YudovichApproximationScheme
    (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) (I : YudovichInitialData u₀ ω₀) :
    Type where
  approximant : ApproximationIndex → SmoothEulerApproximation u₀ ω₀ I
  mollifierOrGalerkinBasisChosen : Prop
  approximateInitialVelocityConverges : Prop
  approximateInitialVorticityConverges : Prop
  approximateSolutionsExistGlobally : Prop
  uniformVorticityLInfBound : Prop
  uniformVelocityCompactnessEstimate : Prop

/--
Compactness and limit-identification package for the Yudovich existence proof.

The candidate limit fields are supplied externally so the package can be linked
directly to `YudovichGlobalSolution`.  The package records subsequence
extraction, convergence modes, bounded-vorticity passage, and passage of the
weak Euler residuals to the selected limit residuals.
-/
structure WholePlaneYudovichExistencePackage
    (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) (I : YudovichInitialData u₀ ω₀)
    (u : VelocityField) (p : PressureField) (ω : VorticityField)
    (residuals : WholePlaneWeakEulerResiduals u p ω) : Type where
  approximationScheme : YudovichApproximationScheme u₀ ω₀ I
  compactnessSubsequence : ApproximationIndex → ApproximationIndex
  compactnessExtraction : Prop
  velocityConvergenceMode : Prop
  vorticityWeakStarConvergenceMode : Prop
  pressureNormalizationOrRecovery : Prop
  limitVorticityLInfBound :
    TimewiseVorticityLInfBound ω ω₀ {t : ℝ | 0 ≤ t}
  passageToWeakMomentumLimit : Prop
  passageToIncompressibilityLimit : Prop
  passageToVorticityTransportLimit : Prop
  selectedLimitResiduals : WholePlaneWeakEulerResiduals u p ω := residuals

/--
Admissible whole-plane Yudovich-class solution triple for uniqueness.

This class is intentionally stated independently of `YudovichGlobalSolution` so
the eventual uniqueness theorem can quantify over any competing weak solution
with the same initial data.  It reuses the checked residual, curl/vorticity, and
Biot-Savart statement surfaces while keeping the analytic trace and regularity
facts as explicit obligations.
-/
structure WholePlaneYudovichClass
    (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) (I : YudovichInitialData u₀ ω₀)
    (u : VelocityField) (p : PressureField) (ω : VorticityField)
    (residuals : WholePlaneWeakEulerResiduals u p ω) (timeSet : Set ℝ) :
    Type where
  coversNonnegativeTimes : {t : ℝ | 0 ≤ t} ⊆ timeSet
  velocityMeasurable :
    ∀ t : ℝ, t ∈ timeSet → AEStronglyMeasurable (u t) volume
  vorticityMeasurable :
    ∀ t : ℝ, t ∈ timeSet → AEStronglyMeasurable (ω t) volume
  vorticityMemLInf :
    ∀ t : ℝ, t ∈ timeSet → MemLp (ω t) ⊤ volume
  vorticityLInfPropagation : Prop
  weakEulerResiduals : WholePlaneWeakEulerResiduals u p ω := residuals
  initialTraceVelocity : Prop
  initialTraceVorticity : Prop
  curlVorticity : TimewiseCurlVorticityCompatibility u ω
  biotSavartCompatibility : WholePlaneBiotSavartReconstruction u ω

/--
Osgood modulus boundary used in the uniqueness argument.

The terminal proof must replace the proposition fields by the appropriate local
integral/divergence theorem for the chosen modulus, but this structure fixes the
shape needed by the Yudovich proof tree.
-/
structure OsgoodModulus (μ : ℝ → ℝ) : Type where
  zero_value : μ 0 = 0
  nonnegative : ∀ r : ℝ, 0 ≤ r → 0 ≤ μ r
  positiveAwayFromZero : Prop
  osgoodDivergenceAtZero : Prop

/--
Log-Lipschitz/Osgood velocity-control estimate generated by bounded vorticity.

For Yudovich uniqueness, the Biot-Savart reconstruction and the `L∞` vorticity
bound must yield a velocity modulus whose Osgood integral diverges at zero.
The hard harmonic-analysis estimate is isolated as proposition fields.
-/
structure LogLipschitzOsgoodEstimate
    (u : VelocityField) (ω : VorticityField) (timeSet : Set ℝ) : Type where
  modulus : ℝ → ℝ
  osgoodModulus : OsgoodModulus modulus
  timewiseBoundedVorticity : ∀ t : ℝ, t ∈ timeSet → MemLp (ω t) ⊤ volume
  boundedVorticityToLogLipschitz : Prop
  velocityIncrementControlledByModulus : Prop
  osgoodDistanceInequality : Prop

/--
Renormalized-flow or vorticity-transport bridge for the uniqueness proof.

Different Yudovich formalizations may proceed through regular Lagrangian flows,
renormalized transport, or an Eulerian vorticity-difference estimate.  This
package names the shared bridge obligations without committing the current
repository to one unavailable PDE API.
-/
structure RenormalizedFlowOrTransportBridge
    (u : VelocityField) (ω : VorticityField) (timeSet : Set ℝ) : Type where
  flowMap : ℝ → Plane → Plane
  flowExistsForCoveredTimes : Prop
  flowMeasurePreserving : Prop
  vorticityTransportedByFlow : Prop
  renormalizedTransportUniqueness : Prop
  compatibleWithWeakVorticityResidual : Prop

/--
Quantified uniqueness conclusion against every competing Yudovich-class weak
solution with the same initial data.

Pressure is deliberately omitted from the equality conclusion because Euler
pressure is only determined up to normalization unless an additional pressure
gauge is selected.
-/
structure WholePlaneYudovichUniquenessConclusion
    (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) (I : YudovichInitialData u₀ ω₀)
    (u : VelocityField) (p : PressureField) (ω : VorticityField)
    (residuals : WholePlaneWeakEulerResiduals u p ω) (timeSet : Set ℝ) :
    Type where
  uniqueVelocityAgainstClass :
    ∀ (v : VelocityField) (q : PressureField) (ξ : VorticityField)
      (otherTimeSet : Set ℝ) (otherResiduals : WholePlaneWeakEulerResiduals v q ξ),
      WholePlaneYudovichClass u₀ ω₀ I v q ξ otherResiduals otherTimeSet →
        ∀ t : ℝ, 0 ≤ t → ∀ x : Plane, u t x = v t x
  uniqueVorticityAgainstClass :
    ∀ (v : VelocityField) (q : PressureField) (ξ : VorticityField)
      (otherTimeSet : Set ℝ) (otherResiduals : WholePlaneWeakEulerResiduals v q ξ),
      WholePlaneYudovichClass u₀ ω₀ I v q ξ otherResiduals otherTimeSet →
        ∀ t : ℝ, 0 ≤ t → ∀ x : Plane, ω t x = ξ t x

/--
P5 uniqueness package for the whole-plane Yudovich theorem.

The fields identify the proof route: establish the admissible class, derive the
log-Lipschitz/Osgood estimate, connect vorticity transport through a flow or
renormalized bridge, and conclude uniqueness in the class.
-/
structure WholePlaneYudovichUniquenessPackage
    (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) (I : YudovichInitialData u₀ ω₀)
    (u : VelocityField) (p : PressureField) (ω : VorticityField)
    (residuals : WholePlaneWeakEulerResiduals u p ω) (timeSet : Set ℝ) :
    Type where
  yudovichClass :
    WholePlaneYudovichClass u₀ ω₀ I u p ω residuals timeSet
  logLipschitzOsgoodEstimate :
    LogLipschitzOsgoodEstimate u ω timeSet
  renormalizedFlowOrTransportBridge :
    RenormalizedFlowOrTransportBridge u ω timeSet
  uniquenessConclusion :
    WholePlaneYudovichUniquenessConclusion u₀ ω₀ I u p ω residuals timeSet

/--
Weak two-dimensional incompressible Euler solution data in the Yudovich class.

The weak Euler equations are expressed by whole-spacetime distributional
residuals that vanish on mathlib test functions.  The remaining hard PDE
content is still isolated in proposition/package fields: initial trace,
Biot-Savart compatibility, the approximation/compactness existence package,
propagation of the `L∞` vorticity bound, and uniqueness in the admissible class.
-/
structure YudovichGlobalSolution
    (u₀ : Plane → Plane) (ω₀ : Plane → ℝ) (I : YudovichInitialData u₀ ω₀) :
    Type where
  velocity : VelocityField
  pressure : PressureField
  vorticity : VorticityField
  timeSet : Set ℝ
  coversNonnegativeTimes : {t : ℝ | 0 ≤ t} ⊆ timeSet
  velocityMeasurable :
    ∀ t : ℝ, t ∈ timeSet → AEStronglyMeasurable (velocity t) volume
  vorticityMeasurable :
    ∀ t : ℝ, t ∈ timeSet → AEStronglyMeasurable (vorticity t) volume
  vorticityMemLInf :
    ∀ t : ℝ, t ∈ timeSet → MemLp (vorticity t) ⊤ volume
  vorticityLInfPropagation : Prop
  weakEulerResiduals : WholePlaneWeakEulerResiduals velocity pressure vorticity
  existenceConstruction :
    WholePlaneYudovichExistencePackage u₀ ω₀ I velocity pressure vorticity
      weakEulerResiduals
  initialTraceVelocity : Prop
  initialTraceVorticity : Prop
  biotSavartCompatibility : WholePlaneBiotSavartReconstruction velocity vorticity
  uniquenessPackage :
    WholePlaneYudovichUniquenessPackage u₀ ω₀ I velocity pressure vorticity
      weakEulerResiduals timeSet

/--
Normalized Stage1 statement shape for Yudovich's theorem.

For every two-dimensional initial velocity/vorticity pair satisfying the
Yudovich admissibility package, there exists global nonnegative-time weak Euler
solution data in the bounded-vorticity class.
-/
def StatementShape : Prop :=
  ∀ (u₀ : Plane → Plane) (ω₀ : Plane → ℝ)
    (I : YudovichInitialData u₀ ω₀),
    Nonempty (YudovichGlobalSolution u₀ ω₀ I)

/-- Equivalent expanded form of the normalized statement shape. -/
theorem statementShape_iff :
    StatementShape ↔
      ∀ (u₀ : Plane → Plane) (ω₀ : Plane → ℝ)
        (I : YudovichInitialData u₀ ω₀),
        Nonempty (YudovichGlobalSolution u₀ ω₀ I) :=
  Iff.rfl

/-- The initial bounded-vorticity hypothesis projects from the initial-data package. -/
theorem initial_vorticity_memLInf {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    (I : YudovichInitialData u₀ ω₀) :
    MemLp ω₀ ⊤ volume :=
  I.vorticityMemLInf

/-- A global solution package exposes bounded vorticity at each covered time. -/
theorem solution_vorticity_memLInf {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I)
    {t : ℝ} (ht : t ∈ S.timeSet) :
    MemLp (S.vorticity t) ⊤ volume :=
  S.vorticityMemLInf t ht

/-- A global solution package covers every nonnegative time. -/
theorem nonnegative_time_mem {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I)
    {t : ℝ} (ht : 0 ≤ t) :
    t ∈ S.timeSet :=
  S.coversNonnegativeTimes ht

/-- Scalar distributions on the whole plane are nonempty. -/
theorem scalarDistributionOnPlane_nonempty : Nonempty ScalarDistributionOnPlane :=
  inferInstance

/-- Scalar distributions on the whole spacetime are nonempty. -/
theorem scalarDistributionOnSpacetime_nonempty : Nonempty ScalarDistributionOnSpacetime :=
  inferInstance

/-- Distributional scalar maps are available for future weak Euler residuals. -/
def distributionMapCLM (A : ℝ →L[ℝ] ℝ) :
    ScalarDistributionOnPlane →L[ℝ] ScalarDistributionOnPlane :=
  Distribution.mapCLM A

/-- A solution package exposes a vanishing momentum residual. -/
theorem solution_momentumResidual_vanishes {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    VectorResidualVanishes S.weakEulerResiduals.momentumResidual :=
  S.weakEulerResiduals.momentumResidual_vanishes

/-- A solution package exposes a vanishing incompressibility residual. -/
theorem solution_incompressibilityResidual_vanishes
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    ScalarResidualVanishes S.weakEulerResiduals.incompressibilityResidual :=
  S.weakEulerResiduals.incompressibilityResidual_vanishes

/-- A solution package exposes a vanishing vorticity-transport residual. -/
theorem solution_vorticityTransportResidual_vanishes
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    ScalarResidualVanishes S.weakEulerResiduals.vorticityTransportResidual :=
  S.weakEulerResiduals.vorticityTransportResidual_vanishes

/-- The initial-data package exposes the static vorticity-as-curl obligation. -/
def initial_vorticity_is_curl {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    (I : YudovichInitialData u₀ ω₀) :
    StaticCurlVorticityCompatibility u₀ ω₀ :=
  I.vorticityIsCurl

/-- A global solution package exposes whole-plane Biot-Savart compatibility. -/
def solution_biotSavartCompatibility {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    WholePlaneBiotSavartReconstruction S.velocity S.vorticity :=
  S.biotSavartCompatibility

/-- A global solution package exposes timewise curl/vorticity compatibility. -/
def solution_timewiseCurlVorticityCompatibility
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    TimewiseCurlVorticityCompatibility S.velocity S.vorticity :=
  S.biotSavartCompatibility.curlVorticity

/-- A global solution package exposes the P4 approximation/compactness construction package. -/
def solution_existenceConstruction
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    WholePlaneYudovichExistencePackage u₀ ω₀ I S.velocity S.pressure S.vorticity
      S.weakEulerResiduals :=
  S.existenceConstruction

/-- A global solution package exposes the P4 approximation scheme. -/
def solution_approximationScheme
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    YudovichApproximationScheme u₀ ω₀ I :=
  S.existenceConstruction.approximationScheme

/-- The P4 construction package exposes the nonnegative-time `L∞` vorticity bound. -/
theorem solution_nonnegative_vorticity_linf_bound
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I)
    {t : ℝ} (ht : 0 ≤ t) :
    MemLp (S.vorticity t) ⊤ volume ∧
      MeasureTheory.eLpNorm (S.vorticity t) ⊤ volume ≤
        MeasureTheory.eLpNorm ω₀ ⊤ volume :=
  S.existenceConstruction.limitVorticityLInfBound t ht

/-- The P4 construction records the selected weak-momentum passage-to-limit obligation. -/
def solution_passageToWeakMomentumLimit
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    Prop :=
  S.existenceConstruction.passageToWeakMomentumLimit

/-- The P4 construction records the selected vorticity-transport passage-to-limit obligation. -/
def solution_passageToVorticityTransportLimit
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    Prop :=
  S.existenceConstruction.passageToVorticityTransportLimit

/-- A global solution package exposes the P5 uniqueness package. -/
def solution_uniquenessPackage
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    WholePlaneYudovichUniquenessPackage u₀ ω₀ I S.velocity S.pressure S.vorticity
      S.weakEulerResiduals S.timeSet :=
  S.uniquenessPackage

/-- A global solution package exposes its Yudovich-class membership. -/
def solution_yudovichClass
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    WholePlaneYudovichClass u₀ ω₀ I S.velocity S.pressure S.vorticity
      S.weakEulerResiduals S.timeSet :=
  S.uniquenessPackage.yudovichClass

/-- A global solution package exposes its log-Lipschitz/Osgood estimate branch. -/
def solution_logLipschitzOsgoodEstimate
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    LogLipschitzOsgoodEstimate S.velocity S.vorticity S.timeSet :=
  S.uniquenessPackage.logLipschitzOsgoodEstimate

/-- A global solution package exposes its flow or renormalized-transport bridge. -/
def solution_renormalizedFlowOrTransportBridge
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    RenormalizedFlowOrTransportBridge S.velocity S.vorticity S.timeSet :=
  S.uniquenessPackage.renormalizedFlowOrTransportBridge

/-- A global solution package exposes the quantified uniqueness conclusion. -/
def solution_uniquenessConclusion
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I) :
    WholePlaneYudovichUniquenessConclusion u₀ ω₀ I S.velocity S.pressure
      S.vorticity S.weakEulerResiduals S.timeSet :=
  S.uniquenessPackage.uniquenessConclusion

/-- The P5 package proves velocity uniqueness against any competing Yudovich-class solution. -/
theorem solution_uniqueVelocityAgainstClass
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I)
    (v : VelocityField) (q : PressureField) (ξ : VorticityField)
    (otherTimeSet : Set ℝ) (otherResiduals : WholePlaneWeakEulerResiduals v q ξ)
    (otherClass : WholePlaneYudovichClass u₀ ω₀ I v q ξ otherResiduals otherTimeSet) :
    ∀ t : ℝ, 0 ≤ t → ∀ x : Plane, S.velocity t x = v t x :=
  S.uniquenessPackage.uniquenessConclusion.uniqueVelocityAgainstClass
    v q ξ otherTimeSet otherResiduals otherClass

/-- The P5 package proves vorticity uniqueness against any competing Yudovich-class solution. -/
theorem solution_uniqueVorticityAgainstClass
    {u₀ : Plane → Plane} {ω₀ : Plane → ℝ}
    {I : YudovichInitialData u₀ ω₀} (S : YudovichGlobalSolution u₀ ω₀ I)
    (v : VelocityField) (q : PressureField) (ξ : VorticityField)
    (otherTimeSet : Set ℝ) (otherResiduals : WholePlaneWeakEulerResiduals v q ξ)
    (otherClass : WholePlaneYudovichClass u₀ ω₀ I v q ξ otherResiduals otherTimeSet) :
    ∀ t : ℝ, 0 ≤ t → ∀ x : Plane, S.vorticity t x = ξ t x :=
  S.uniquenessPackage.uniquenessConclusion.uniqueVorticityAgainstClass
    v q ξ otherTimeSet otherResiduals otherClass

/-- The local audit row format for the P4 existence construction package. -/
structure YudovichExistencePackageAuditRow where
  leafCode : String
  publicLabel : String
  checkedLeanSurface : String
  currentRepoLocalBoundary : String
  nextFormalizationLeaf : String
  localBudgetUpperBound : Nat
  status : String

/--
Integration-ready audit rows for the P4 existence package.

These rows are local statement-surface evidence only.  They name the proof
leaves that must later be replaced by proof bodies or pinned imports before the
existence half of Yudovich's theorem can be marked complete.
-/
def yudovichExistencePackageAuditRows : List YudovichExistencePackageAuditRow := [
  {
    leafCode := "M1234-P4a"
    publicLabel := "smooth or Galerkin approximation scheme"
    checkedLeanSurface :=
      "ApproximationIndex; SmoothEulerApproximation; YudovichApproximationScheme"
    currentRepoLocalBoundary :=
      "the approximant family and smoothed-data convergence obligations are named, but no mollifier, Galerkin basis, or smooth Euler existence theorem is constructed"
    nextFormalizationLeaf :=
      "choose mollification or Galerkin truncation, construct smooth initial data, and prove convergence to the Yudovich initial data"
    localBudgetUpperBound := 100
    status := "formalization_debt: statement surface only"
  },
  {
    leafCode := "M1234-P4b"
    publicLabel := "uniform L-infinity vorticity bound"
    checkedLeanSurface :=
      "TimewiseVorticityLInfBound; SmoothEulerApproximation.vorticityLInfBound; YudovichApproximationScheme.uniformVorticityLInfBound"
    currentRepoLocalBoundary :=
      "the bound is expressed with `MemLp _ ⊤ volume` and `eLpNorm`; the transport or maximum-principle proof is not present"
    nextFormalizationLeaf :=
      "prove the smooth approximants preserve or uniformly bound `eLpNorm omega_n(t) ⊤ volume` by the approximated initial vorticity bound"
    localBudgetUpperBound := 100
    status := "formalization_debt: estimate not proved"
  },
  {
    leafCode := "M1234-P4c"
    publicLabel := "compactness and subsequence extraction"
    checkedLeanSurface :=
      "WholePlaneYudovichExistencePackage.compactnessSubsequence; compactnessExtraction; velocityConvergenceMode; vorticityWeakStarConvergenceMode"
    currentRepoLocalBoundary :=
      "the compactness interfaces are named, but no Arzela-Ascoli, Aubin-Lions, weak-star compactness, or measure compactness theorem is imported"
    nextFormalizationLeaf :=
      "formalize the compactness theorem needed for bounded-vorticity approximants and extract a subsequence converging to the candidate weak solution"
    localBudgetUpperBound := 100
    status := "formalization_debt: compactness proof absent"
  },
  {
    leafCode := "M1234-P4d"
    publicLabel := "limit vorticity bound and pressure recovery"
    checkedLeanSurface :=
      "WholePlaneYudovichExistencePackage.limitVorticityLInfBound; pressureNormalizationOrRecovery; solution_nonnegative_vorticity_linf_bound"
    currentRepoLocalBoundary :=
      "the limit bound and pressure normalization/recovery obligations are named; no lower-semicontinuity or pressure construction proof is present"
    nextFormalizationLeaf :=
      "pass the uniform `L∞` vorticity estimate to the weak-star limit and choose a pressure normalization compatible with the weak residual formulation"
    localBudgetUpperBound := 100
    status := "formalization_debt: limit estimate and pressure branch open"
  },
  {
    leafCode := "M1234-P4e"
    publicLabel := "passage to the weak Euler limit"
    checkedLeanSurface :=
      "WholePlaneYudovichExistencePackage.passageToWeakMomentumLimit; passageToIncompressibilityLimit; passageToVorticityTransportLimit; selectedLimitResiduals"
    currentRepoLocalBoundary :=
      "the three weak-limit passage obligations are named against mathlib distributional residuals; no nonlinear convergence theorem is proved"
    nextFormalizationLeaf :=
      "prove convergence of the momentum, incompressibility, and vorticity-transport residuals on every test function and identify the selected limit residuals"
    localBudgetUpperBound := 100
    status := "formalization_debt: weak-limit passage open"
  }
]

/-- The P4 existence package split contains exactly the five expected leaves. -/
theorem yudovichExistencePackageAuditRows_length :
    yudovichExistencePackageAuditRows.length = 5 := by
  native_decide

/-- Each P4 existence leaf is kept within the M0387 child leaf budget target. -/
theorem yudovichExistencePackageAuditRows_budgets :
    (yudovichExistencePackageAuditRows.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true := by
  native_decide

/-- Repo-local integration-debt gate record for the P4 existence child surface. -/
structure P4RepoLocalIntegrationDebtGate where
  externalLeanProofFound : Bool
  externalLeanProofPinnedOrImported : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  result : String

/--
P4 is not marked complete and does not retain repo-local integration debt in a
completed state.

No external Lean 4 proof of the Yudovich existence construction was found or
integrated in this child pass.  The remaining status is formalization debt, not
anchor-only completion.
-/
def p4RepoLocalIntegrationDebtGate : P4RepoLocalIntegrationDebtGate where
  externalLeanProofFound := false
  externalLeanProofPinnedOrImported := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  result :=
    "pass_for_noncompletion: no external Lean 4 Yudovich existence proof was \
    used as anchor-only completion; P4 remains formalization_debt"

/-- The P4 child does not claim completion with repo-local integration debt present. -/
theorem p4RepoLocalIntegrationDebtGate_completedDebt_eq_false :
    p4RepoLocalIntegrationDebtGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- The local audit row format for the P5 Yudovich uniqueness package. -/
structure YudovichUniquenessPackageAuditRow where
  leafCode : String
  publicLabel : String
  checkedLeanSurface : String
  currentRepoLocalBoundary : String
  nextFormalizationLeaf : String
  localBudgetUpperBound : Nat
  status : String

/--
Integration-ready audit rows for the P5 uniqueness package.

These rows are local statement-surface evidence only.  They name the proof
leaves that must later be replaced by proof bodies or pinned imports before the
Yudovich uniqueness theorem can be marked complete.
-/
def yudovichUniquenessPackageAuditRows : List YudovichUniquenessPackageAuditRow := [
  {
    leafCode := "M1234-P5a"
    publicLabel := "Yudovich admissible uniqueness class"
    checkedLeanSurface :=
      "WholePlaneYudovichClass; solution_yudovichClass"
    currentRepoLocalBoundary :=
      "the class bundles time coverage, measurability, `MemLp _ ⊤ volume`, residuals, traces, curl/vorticity, and Biot-Savart compatibility; no theorem proves a candidate belongs to this class except by carrying the package"
    nextFormalizationLeaf :=
      "replace remaining class `Prop` fields with concrete trace, propagation, curl, and Biot-Savart predicates or checked imports"
    localBudgetUpperBound := 100
    status := "formalization_debt: admissible class surface only"
  },
  {
    leafCode := "M1234-P5b"
    publicLabel := "log-Lipschitz/Osgood estimate"
    checkedLeanSurface :=
      "OsgoodModulus; LogLipschitzOsgoodEstimate; solution_logLipschitzOsgoodEstimate"
    currentRepoLocalBoundary :=
      "the modulus, Osgood divergence, and velocity-increment estimate are named; no harmonic-analysis proof from bounded vorticity is present"
    nextFormalizationLeaf :=
      "prove or import the Yudovich estimate that bounded vorticity plus Biot-Savart reconstruction gives a log-Lipschitz velocity modulus with Osgood divergence"
    localBudgetUpperBound := 100
    status := "formalization_debt: estimate not proved"
  },
  {
    leafCode := "M1234-P5c"
    publicLabel := "renormalized flow or transport bridge"
    checkedLeanSurface :=
      "RenormalizedFlowOrTransportBridge; solution_renormalizedFlowOrTransportBridge"
    currentRepoLocalBoundary :=
      "the flow map and renormalized-transport obligations are named; no regular Lagrangian flow, DiPerna-Lions, or Eulerian transport uniqueness theorem is imported"
    nextFormalizationLeaf :=
      "choose the Lagrangian or Eulerian route and prove compatibility between the weak vorticity residual and transported vorticity"
    localBudgetUpperBound := 100
    status := "formalization_debt: flow/transport bridge open"
  },
  {
    leafCode := "M1234-P5d"
    publicLabel := "Osgood uniqueness conclusion"
    checkedLeanSurface :=
      "WholePlaneYudovichUniquenessConclusion; solution_uniquenessConclusion"
    currentRepoLocalBoundary :=
      "velocity and vorticity equality against every competing class member are packaged as quantified conclusions; no Gronwall/Osgood proof body is present"
    nextFormalizationLeaf :=
      "prove the distance or vorticity-difference inequality and close it with the Osgood lemma for all nonnegative times"
    localBudgetUpperBound := 100
    status := "formalization_debt: uniqueness proof absent"
  },
  {
    leafCode := "M1234-P5e"
    publicLabel := "solution-level uniqueness projections"
    checkedLeanSurface :=
      "solution_uniqueVelocityAgainstClass; solution_uniqueVorticityAgainstClass"
    currentRepoLocalBoundary :=
      "projection theorems expose any carried uniqueness package but do not construct the package from the PDE hypotheses"
    nextFormalizationLeaf :=
      "after P5a-P5d are proved or imported, instantiate the uniqueness package for any two global Yudovich solutions sharing the initial data"
    localBudgetUpperBound := 100
    status := "formalization_debt: projection surface only"
  }
]

/-- The P5 uniqueness package split contains exactly the five expected leaves. -/
theorem yudovichUniquenessPackageAuditRows_length :
    yudovichUniquenessPackageAuditRows.length = 5 := by
  native_decide

/-- Each P5 uniqueness leaf is kept within the M0387 child leaf budget target. -/
theorem yudovichUniquenessPackageAuditRows_budgets :
    (yudovichUniquenessPackageAuditRows.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true := by
  native_decide

/-- Repo-local integration-debt gate record for the P5 uniqueness child surface. -/
structure P5RepoLocalIntegrationDebtGate where
  externalLeanProofFound : Bool
  externalLeanProofPinnedOrImported : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  result : String

/--
P5 is not marked complete and does not retain repo-local integration debt in a
completed state.

No external Lean 4 proof of the Yudovich uniqueness/Osgood package was found or
integrated in this child pass.  The remaining status is formalization debt, not
anchor-only completion.
-/
def p5RepoLocalIntegrationDebtGate : P5RepoLocalIntegrationDebtGate where
  externalLeanProofFound := false
  externalLeanProofPinnedOrImported := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  result :=
    "pass_for_noncompletion: no external Lean 4 Yudovich uniqueness proof was \
    used as anchor-only completion; P5 remains formalization_debt"

/-- The P5 child does not claim completion with repo-local integration debt present. -/
theorem p5RepoLocalIntegrationDebtGate_completedDebt_eq_false :
    p5RepoLocalIntegrationDebtGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- The local audit row format for the P3 curl/vorticity and Biot-Savart split. -/
structure BiotSavartVariantAuditRow where
  variant : BiotSavartDomainVariant
  publicLabel : String
  checkedLeanSurface : String
  currentRepoLocalBoundary : String
  nextFormalizationLeaf : String
  localBudgetUpperBound : Nat
  status : String

/--
Integration-ready audit rows for the three Biot-Savart reconstruction variants.

These rows are local statement-surface evidence only.  They do not close the
PDE theorem; each row records the next proof leaf needed before the branch can
contribute to a terminal Yudovich proof.
-/
def biotSavartVariantAuditRows : List BiotSavartVariantAuditRow := [
  {
    variant := .wholePlane
    publicLabel := "whole-plane Biot-Savart reconstruction"
    checkedLeanSurface :=
      "WholePlaneBiotSavartReconstruction; biotSavartReconstructionForVariant_wholePlane"
    currentRepoLocalBoundary :=
      "curl/vorticity compatibility is named; singular-kernel or Fourier-multiplier reconstruction remains a Prop obligation"
    nextFormalizationLeaf :=
      "define the whole-plane Biot-Savart kernel or Fourier multiplier, prove divergence-free reconstruction and curl(K * omega) = omega under Yudovich-class hypotheses"
    localBudgetUpperBound := 100
    status := "formalization_debt: statement surface only"
  },
  {
    variant := .flatTorus
    publicLabel := "flat-torus Biot-Savart reconstruction"
    checkedLeanSurface :=
      "TorusBiotSavartReconstruction; biotSavartReconstructionForVariant_flatTorus"
    currentRepoLocalBoundary :=
      "periodicity and mean-zero normalization are explicit obligations; no torus Euler/Biot-Savart theorem is imported"
    nextFormalizationLeaf :=
      "choose the torus model, define periodic scalar vorticity and mean-zero Green/Fourier reconstruction, then prove curl and divergence compatibility"
    localBudgetUpperBound := 100
    status := "formalization_debt: statement surface only"
  },
  {
    variant := .boundedDomain
    publicLabel := "bounded-domain Biot-Savart reconstruction"
    checkedLeanSurface :=
      "BoundedDomainBiotSavartReconstruction; biotSavartReconstructionForVariant_boundedDomain"
    currentRepoLocalBoundary :=
      "domain admissibility, boundary condition, Green/stream function, and harmonic correction are explicit obligations"
    nextFormalizationLeaf :=
      "select the bounded-domain regularity and boundary-condition regime, build the Green/stream-function reconstruction, and prove the harmonic correction gives the desired velocity"
    localBudgetUpperBound := 100
    status := "formalization_debt: statement surface only"
  }
]

/-- The P3 variant split contains exactly the requested three branches. -/
theorem biotSavartVariantAuditRows_length :
    biotSavartVariantAuditRows.length = 3 := by
  native_decide

/-- Each P3 branch is kept within the M0387 child leaf budget target. -/
theorem biotSavartVariantAuditRows_budgets :
    (biotSavartVariantAuditRows.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true := by
  native_decide

/-- Repo-local integration-debt gate record for this child surface. -/
structure P3RepoLocalIntegrationDebtGate where
  externalLeanProofFound : Bool
  externalLeanProofPinnedOrImported : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  result : String

/--
P3 is not marked complete and does not retain repo-local integration debt in a
completed state.

No external Lean 4 proof of Yudovich/Biot-Savart reconstruction was found or
integrated in this child pass.  The remaining status is formalization debt, not
anchor-only completion.
-/
def p3RepoLocalIntegrationDebtGate : P3RepoLocalIntegrationDebtGate where
  externalLeanProofFound := false
  externalLeanProofPinnedOrImported := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  result :=
    "pass_for_noncompletion: no external Lean 4 Yudovich/Biot-Savart proof was \
    used as anchor-only completion; P3 remains formalization_debt"

/-- The P3 child does not claim completion with repo-local integration debt present. -/
theorem p3RepoLocalIntegrationDebtGate_completedDebt_eq_false :
    p3RepoLocalIntegrationDebtGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- mathlib source files audited for analytic anchors and terminal theorem names. -/
def auditedMathlibSourceFiles : List String := [
  "Mathlib/Analysis/Distribution/Distribution.lean",
  "Mathlib/Analysis/Distribution/TestFunction.lean",
  "Mathlib/Analysis/Distribution/DerivNotation.lean",
  "Mathlib/Analysis/Distribution/TemperedDistribution.lean",
  "Mathlib/Analysis/Distribution/FourierSchwartz.lean",
  "Mathlib/Analysis/Distribution/FourierMultiplier.lean",
  "Mathlib/Analysis/Calculus/FDeriv/Basic.lean",
  "Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean",
  "Mathlib/Analysis/Fourier/FourierTransform.lean",
  "Mathlib/Analysis/Fourier/FourierTransformDeriv.lean",
  "Mathlib/Analysis/Fourier/LpSpace.lean",
  "Mathlib/Analysis/Fourier/AddCircleMulti.lean",
  "Mathlib/MeasureTheory/Function/LpSpace/Basic.lean",
  "Mathlib/MeasureTheory/Function/LpSpace/Complete.lean",
  "Mathlib/MeasureTheory/Function/LpSeminorm/Defs.lean",
  "Mathlib/MeasureTheory/Function/LpSeminorm/Basic.lean",
  "Mathlib/MeasureTheory/Integral/Bochner/Basic.lean",
  "Mathlib/MeasureTheory/Integral/TorusIntegral.lean",
  "Mathlib/MeasureTheory/Measure/Lebesgue/Basic.lean"
]

/-- mathlib modules checked while locating repo-local anchors for this PDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Fourier.FourierTransform",
  "Mathlib.Analysis.Fourier.LpSpace",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Measure.Lebesgue.Basic"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "EuclideanSpace",
  "MeasureTheory.volume",
  "MeasureTheory.AEStronglyMeasurable",
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "fderiv",
  "Distribution",
  "Distribution.mapCLM",
  "TestFunction",
  "TemperedDistribution",
  "MeasureTheory.Lp.fourierTransformₗᵢ",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one"
]

/--
Search terms that did not locate a terminal Yudovich/Euler theorem in pinned
mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Yudovich",
  "Yudovitch",
  "EulerEquation",
  "incompressible Euler",
  "vorticity",
  "Vorticity",
  "BiotSavart",
  "Biot-Savart",
  "curl",
  "Curl",
  "weak Euler solution",
  "fluid equations",
  "NavierStokes"
]

/-- The local audit row format for the P6 external GitHub code-search child. -/
structure ExternalGitHubCodeSearchAuditRow where
  searchTerm : String
  requestedSearchMode : String
  executedSearchMode : String
  localResult : String
  integrationAction : String

/--
P6 requested authenticated GitHub code-search terms.

The environment did not have `gh` authentication available in this child pass,
so these rows deliberately record a concrete blocker instead of treating
anchor-only or unauthenticated evidence as completion.
-/
def externalGitHubCodeSearchAuditRows :
    List ExternalGitHubCodeSearchAuditRow := [
  {
    searchTerm := "Yudovich"
    requestedSearchMode := "authenticated GitHub code search for Lean 4 proof candidates"
    executedSearchMode := "`gh search code \"Yudovich language:Lean\" --limit 5`"
    localResult :=
      "blocked: GitHub CLI reported no logged-in GitHub host and requested `gh auth login` or `GH_TOKEN`"
    integrationAction :=
      "rerun authenticated code search; if a Lean 4 proof candidate appears, pin/import/check before any completion claim"
  },
  {
    searchTerm := "Yudovitch"
    requestedSearchMode := "authenticated GitHub code search for Lean 4 proof candidates"
    executedSearchMode := "`gh search code \"Yudovitch language:Lean\" --limit 5`"
    localResult :=
      "blocked: GitHub CLI reported no logged-in GitHub host and requested `gh auth login` or `GH_TOKEN`"
    integrationAction :=
      "rerun authenticated code search; if a Lean 4 proof candidate appears, pin/import/check before any completion claim"
  },
  {
    searchTerm := "EulerEquation"
    requestedSearchMode := "authenticated GitHub code search for Lean 4 proof candidates"
    executedSearchMode := "`gh search code \"EulerEquation language:Lean\" --limit 5`"
    localResult :=
      "blocked: GitHub CLI reported no logged-in GitHub host and requested `gh auth login` or `GH_TOKEN`"
    integrationAction :=
      "rerun authenticated code search; if a Lean 4 proof candidate appears, pin/import/check before any completion claim"
  },
  {
    searchTerm := "incompressible Euler"
    requestedSearchMode := "authenticated GitHub code search for Lean 4 proof candidates"
    executedSearchMode := "`gh search code \"incompressible Euler language:Lean\" --limit 5`"
    localResult :=
      "blocked: GitHub CLI reported no logged-in GitHub host and requested `gh auth login` or `GH_TOKEN`"
    integrationAction :=
      "rerun authenticated code search; if a Lean 4 proof candidate appears, pin/import/check before any completion claim"
  },
  {
    searchTerm := "Vorticity"
    requestedSearchMode := "authenticated GitHub code search for Lean 4 proof candidates"
    executedSearchMode := "`gh search code \"Vorticity language:Lean\" --limit 5`"
    localResult :=
      "blocked: GitHub CLI reported no logged-in GitHub host and requested `gh auth login` or `GH_TOKEN`"
    integrationAction :=
      "rerun authenticated code search; if a Lean 4 proof candidate appears, pin/import/check before any completion claim"
  },
  {
    searchTerm := "BiotSavart"
    requestedSearchMode := "authenticated GitHub code search for Lean 4 proof candidates"
    executedSearchMode := "`gh search code \"BiotSavart language:Lean\" --limit 5`"
    localResult :=
      "blocked: GitHub CLI reported no logged-in GitHub host and requested `gh auth login` or `GH_TOKEN`"
    integrationAction :=
      "rerun authenticated code search; if a Lean 4 proof candidate appears, pin/import/check before any completion claim"
  },
  {
    searchTerm := "weak Euler solution"
    requestedSearchMode := "authenticated GitHub code search for Lean 4 proof candidates"
    executedSearchMode := "`gh search code \"weak Euler solution language:Lean\" --limit 5`"
    localResult :=
      "blocked: GitHub CLI reported no logged-in GitHub host and requested `gh auth login` or `GH_TOKEN`"
    integrationAction :=
      "rerun authenticated code search; if a Lean 4 proof candidate appears, pin/import/check before any completion claim"
  }
]

/-- The P6 external-search audit contains exactly the requested seven terms. -/
theorem externalGitHubCodeSearchAuditRows_length :
    externalGitHubCodeSearchAuditRows.length = 7 := by
  native_decide

/-- Repo-local integration-debt gate record for the P6 external-search child. -/
structure P6RepoLocalIntegrationDebtGate where
  authenticatedGitHubCodeSearchCompleted : Bool
  externalLeanProofPinnedOrImported : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  concreteIntegrationBlocker : String
  result : String

/--
P6 is not marked complete and does not retain repo-local integration debt in a
completed state.

The authenticated GitHub code search requested by the child task could not be
completed in this environment because GitHub CLI authentication was absent.
Therefore no external Lean 4 proof is used as anchor-only completion, and no
`external_upstream_anchor_only` state is promoted to completed.
-/
def p6RepoLocalIntegrationDebtGate : P6RepoLocalIntegrationDebtGate where
  authenticatedGitHubCodeSearchCompleted := false
  externalLeanProofPinnedOrImported := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  concreteIntegrationBlocker :=
    "2026-05-01: `gh auth status` reported no logged-in GitHub hosts; \
    each requested `gh search code ... language:Lean` probe asked for \
    `gh auth login` or `GH_TOKEN`."
  result :=
    "blocked_for_completion: rerun authenticated GitHub code search and \
    pin/import/check any discovered Lean 4 proof before changing P6 status"

/-- The P6 child does not claim completion with repo-local integration debt present. -/
theorem p6RepoLocalIntegrationDebtGate_completedDebt_eq_false :
    p6RepoLocalIntegrationDebtGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- Repo-local validation gate record for the P7 validation/public-backfill child. -/
structure P7RepoLocalValidationGate where
  leanArtifactExists : Bool
  validationCommand : String
  validationPassedOn : String
  proofDependencyPinnedOrLocalProofBodyAddedByThisChild : Bool
  publicDocsEditedByThisChild : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  result : String

/--
P7 records validation of the current repo-local Lean artifact and reserves
public blueprint/todo edits for a later serial integrator pass.

This child does not pin a proof dependency and does not add a terminal
Yudovich proof body.  It therefore records validation and non-completion
without promoting anchor-only evidence or public-doc state.
-/
def p7RepoLocalValidationGate : P7RepoLocalValidationGate where
  leanArtifactExists := true
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_158.lean"
  validationPassedOn := "2026-05-01"
  proofDependencyPinnedOrLocalProofBodyAddedByThisChild := false
  publicDocsEditedByThisChild := false
  completedStateRetainsRepoLocalIntegrationDebt := false
  result :=
    "pass_for_validation_only: current S1_M_158 Lean artifact validates; \
    no public blueprint/todo edits were made by this child, and the parent \
    theorem remains formalization_debt rather than completed"

/-- The P7 child did not edit public docs directly. -/
theorem p7RepoLocalValidationGate_publicDocsEdited_eq_false :
    p7RepoLocalValidationGate.publicDocsEditedByThisChild = false :=
  rfl

/-- The P7 child does not claim completion with repo-local integration debt present. -/
theorem p7RepoLocalValidationGate_completedDebt_eq_false :
    p7RepoLocalValidationGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Audit probes -/

#check Plane
#check Spacetime
#check VelocityField
#check PressureField
#check VorticityField
#check StaticVelocityField
#check StaticVorticityField
#check planeCoordinate
#check planeUnitVector
#check pointwisePlaneCurl
#check StaticPointwiseVorticityIsCurl
#check ScalarDistributionOnPlane
#check ScalarTestFunctionOnPlane
#check ScalarDistributionOnSpacetime
#check ScalarTestFunctionOnSpacetime
#check VectorDistributionOnSpacetime
#check VectorDistributionOnPlane
#check ScalarResidualVanishes
#check VectorResidualVanishes
#check StaticCurlVorticityCompatibility
#check TimewiseCurlVorticityCompatibility
#check BiotSavartDomainVariant
#check BiotSavartDomainVariant.code
#check WholePlaneBiotSavartReconstruction
#check TorusBiotSavartReconstruction
#check BoundedDomainBiotSavartReconstruction
#check BiotSavartReconstructionForVariant
#check biotSavartReconstructionForVariant_wholePlane
#check biotSavartReconstructionForVariant_flatTorus
#check biotSavartReconstructionForVariant_boundedDomain
#check WholePlaneWeakEulerResiduals
#check YudovichInitialData
#check ApproximationIndex
#check TimewiseVorticityLInfBound
#check SmoothEulerApproximation
#check YudovichApproximationScheme
#check WholePlaneYudovichExistencePackage
#check WholePlaneYudovichClass
#check OsgoodModulus
#check LogLipschitzOsgoodEstimate
#check RenormalizedFlowOrTransportBridge
#check WholePlaneYudovichUniquenessConclusion
#check WholePlaneYudovichUniquenessPackage
#check YudovichGlobalSolution
#check StatementShape
#check initial_vorticity_memLInf
#check solution_vorticity_memLInf
#check nonnegative_time_mem
#check scalarDistributionOnSpacetime_nonempty
#check solution_momentumResidual_vanishes
#check solution_incompressibilityResidual_vanishes
#check solution_vorticityTransportResidual_vanishes
#check initial_vorticity_is_curl
#check solution_biotSavartCompatibility
#check solution_timewiseCurlVorticityCompatibility
#check solution_existenceConstruction
#check solution_approximationScheme
#check solution_nonnegative_vorticity_linf_bound
#check solution_passageToWeakMomentumLimit
#check solution_passageToVorticityTransportLimit
#check solution_uniquenessPackage
#check solution_yudovichClass
#check solution_logLipschitzOsgoodEstimate
#check solution_renormalizedFlowOrTransportBridge
#check solution_uniquenessConclusion
#check solution_uniqueVelocityAgainstClass
#check solution_uniqueVorticityAgainstClass
#check yudovichExistencePackageAuditRows
#check yudovichExistencePackageAuditRows_length
#check yudovichExistencePackageAuditRows_budgets
#check p4RepoLocalIntegrationDebtGate
#check p4RepoLocalIntegrationDebtGate_completedDebt_eq_false
#check yudovichUniquenessPackageAuditRows
#check yudovichUniquenessPackageAuditRows_length
#check yudovichUniquenessPackageAuditRows_budgets
#check p5RepoLocalIntegrationDebtGate
#check p5RepoLocalIntegrationDebtGate_completedDebt_eq_false
#check biotSavartVariantAuditRows
#check biotSavartVariantAuditRows_length
#check biotSavartVariantAuditRows_budgets
#check p3RepoLocalIntegrationDebtGate
#check p3RepoLocalIntegrationDebtGate_completedDebt_eq_false
#check ExternalGitHubCodeSearchAuditRow
#check externalGitHubCodeSearchAuditRows
#check externalGitHubCodeSearchAuditRows_length
#check P6RepoLocalIntegrationDebtGate
#check p6RepoLocalIntegrationDebtGate
#check p6RepoLocalIntegrationDebtGate_completedDebt_eq_false
#check P7RepoLocalValidationGate
#check p7RepoLocalValidationGate
#check p7RepoLocalValidationGate_publicDocsEdited_eq_false
#check p7RepoLocalValidationGate_completedDebt_eq_false
#check fderiv
#check Distribution.mapCLM
#check TestFunction
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.Lp.fourierTransformₗᵢ

end AwesomeTheorems.Stage1.S1_M_158
