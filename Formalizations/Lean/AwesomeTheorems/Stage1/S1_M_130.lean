import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic

/-!
# S1-M-130 / THM-M-0183: Yau's Calabi conjecture

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Calabi conjecture in the Ricci-flat case: on a compact Kahler manifold with
vanishing first Chern class, there exists a Ricci-flat Kahler metric in the
prescribed Kahler class.

The pinned mathlib snapshot `8a178386ffc0f5fef0b77738bb5449d50efeea95` has
complex-manifold, compactness, differentiability, Riemannian-metric,
tangent-bundle, and covariant-derivative infrastructure.  It does not expose
terminal definitions for Kahler metrics, Ricci curvature, Chern classes of
complex manifolds, or Yau's theorem.  The checked content below is therefore
limited to statement normalization and low-risk wrappers around available
mathlib objects.
-/

noncomputable section

open scoped Manifold ContDiff Topology
open Bundle Manifold

namespace AwesomeTheorems.Stage1.S1_M_130

universe u

/-- Pinned mathlib revision audited for this Stage1 slot. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Public-audit summary intended for serial backfill into the Stage1 blueprint.

This is deliberately metadata, not a completion theorem: the audited snapshot
has the listed infrastructure but no terminal geometric Kahler metric /
Ricci-flat Calabi-Yau theorem.
-/
def publicMathlibAuditNote : String :=
  "Pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 provides " ++
  "complex-manifold, Riemannian metric, tangent-bundle, and covariant-derivative " ++
  "infrastructure, but no terminal Kahler metric / Ricci-flat Calabi-Yau theorem."

/--
Formalization boundary for a compact complex manifold carrying the data that
would be required by the Ricci-flat Calabi conjecture.

The geometric predicates are intentionally explicit `Prop` fields because the
local mathlib snapshot audited for this Stage1 slot does not yet provide a
terminal API for Kahler forms, Ricci tensors, or Chern classes of compact complex
manifolds.
-/
structure CalabiYauInput
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] : Type (u + 1) where
  isSmoothComplexManifold : IsManifold I ω M
  isCompact : CompactSpace M
  isHausdorff : T2Space M
  kahlerClass : Type u
  classIsKahler : kahlerClass → Prop
  firstChernClassVanishes : Prop

/--
Output data expected from the Ricci-flat Calabi-Yau theorem.

`metricCarrier` is an abstract carrier for the future metric object.  The current
repository cannot honestly name a mathlib `KahlerMetric` or `RicciFlat` class,
so those conditions are recorded as explicit predicates over the carrier.
-/
structure RicciFlatKahlerMetricData
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M]
    (X : CalabiYauInput E H I M) : Type (u + 1) where
  metricCarrier : Type u
  metric : metricCarrier
  representsClass : X.kahlerClass → Prop
  isKahlerMetric : metricCarrier → Prop
  isRicciFlat : metricCarrier → Prop
  smoothCompatibilityWithComplexStructure : metricCarrier → Prop

/--
Stage1 child surface for Kähler cohomology classes on compact complex
manifolds.

The current pinned mathlib snapshot does not expose a de Rham/Hodge cohomology
API specialized to compact complex Kähler classes.  This structure therefore
records the future carrier and representative obligations explicitly, without
claiming a terminal class implementation.
-/
structure CompactComplexKahlerClass
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] : Type (u + 1) where
  isSmoothComplexManifold : IsManifold I ω M
  isCompact : CompactSpace M
  isHausdorff : T2Space M
  cohomologyCarrier : Type u
  cohomologyClass : cohomologyCarrier
  representativeCarrier : Type u
  representative : representativeCarrier
  representativeIsClosedRealTwoForm : Prop
  representativeIsPositiveOnComplexLines : Prop
  classHasRepresentative : Prop
  isKahlerClass : Prop

/--
Stage1 child surface for compact complex Kähler metrics.

`riemannianMetric` is the checked mathlib carrier: a smooth Riemannian metric
on the real tangent bundle model of the same underlying space.  The remaining
fields are the integration obligations needed before this can become a genuine
mathlib-level Kähler metric: identifying the real atlas with the real form of
the complex atlas, proving Hermitian compatibility with the complex structure,
constructing the associated closed Kähler form, and connecting that form to a
Kähler cohomology class.
-/
structure CompactComplexKahlerMetric
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (ER : Type u) [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    (HR : Type u) [TopologicalSpace HR] (IR : ModelWithCorners ℝ ER HR)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] : Type (u + 1) where
  isSmoothComplexManifold : IsManifold I ω M
  isSmoothRealManifold : IsManifold IR ω M
  isCompact : CompactSpace M
  isHausdorff : T2Space M
  riemannianMetric :
    ContMDiffRiemannianMetric IR ω ER (fun x : M => TangentSpace IR x)
  realAtlasModelsComplexAtlas : Prop
  hermitianCompatibilityWithComplexStructure : Prop
  kahlerFormCarrier : Type u
  kahlerForm : kahlerFormCarrier
  kahlerFormDerivedFromMetric : Prop
  kahlerFormIsClosed : Prop
  kahlerClass : CompactComplexKahlerClass E H I M
  kahlerFormRepresentsClass : Prop

/--
The explicit `ContMDiffRiemannianMetric` bridge carried by a compact complex
Kähler metric package.
-/
def CompactComplexKahlerMetric.toContMDiffRiemannianMetric
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] (g : CompactComplexKahlerMetric E H I ER HR IR M) :
    ContMDiffRiemannianMetric IR ω ER (fun x : M => TangentSpace IR x) :=
  g.riemannianMetric

/--
Checked child-task anchor: the Kähler metric package is not merely an abstract
predicate; it carries the mathlib smooth Riemannian metric object that future
Kähler-form and Ricci-form definitions must use.
-/
theorem CompactComplexKahlerMetric.contMDiffRiemannianMetric_eq
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] (g : CompactComplexKahlerMetric E H I ER HR IR M) :
    g.toContMDiffRiemannianMetric = g.riemannianMetric :=
  rfl

/--
Stage1 child surface for the first-Chern-class/Ricci-form cohomology bridge on
compact complex Kähler manifolds.

The current pinned mathlib snapshot does not expose a geometric first Chern
class for compact complex manifolds, a Ricci form, or the de Rham/Hodge bridge
identifying the Ricci-form cohomology class with a fixed multiple of `c1`.
This structure therefore records the future cohomology carrier, the two classes,
the Ricci-form representative, and the vanishing bridge as explicit obligations.
-/
structure FirstChernRicciCohomologyBridge
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (ER : Type u) [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    (HR : Type u) [TopologicalSpace HR] (IR : ModelWithCorners ℝ ER HR)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M]
    (g : CompactComplexKahlerMetric E H I ER HR IR M) : Type (u + 1) where
  cohomologyCarrier : Type u
  zeroClass : cohomologyCarrier
  firstChernClass : cohomologyCarrier
  ricciFormCarrier : Type u
  ricciForm : ricciFormCarrier
  ricciFormIsClosedRealTwoForm : Prop
  ricciFormCompatibleWithMetric : Prop
  ricciFormCohomologyClass : cohomologyCarrier
  normalizationConstantAccountedFor : Prop
  firstChernClassMatchesRicciFormClass : Prop
  kahlerClassCohomologyCompatible : Prop
  firstChernClassVanishingToRicciFormClassVanishing :
    firstChernClass = zeroClass → ricciFormCohomologyClass = zeroClass
  ricciFormClassVanishingToFirstChernClassVanishing :
    ricciFormCohomologyClass = zeroClass → firstChernClass = zeroClass

/-- The first Chern class carried by the bridge package. -/
def FirstChernRicciCohomologyBridge.toFirstChernClass
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (B : FirstChernRicciCohomologyBridge E H I ER HR IR M g) :
    B.cohomologyCarrier :=
  B.firstChernClass

/-- The Ricci-form cohomology class carried by the bridge package. -/
def FirstChernRicciCohomologyBridge.toRicciFormCohomologyClass
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (B : FirstChernRicciCohomologyBridge E H I ER HR IR M g) :
    B.cohomologyCarrier :=
  B.ricciFormCohomologyClass

/--
Checked child-task anchor: in the abstract bridge package, vanishing of the
first Chern class is logically equivalent to vanishing of the Ricci-form
cohomology class.  The mathematical content is carried by the two explicit
structure fields; this theorem only packages them as the exact bridge needed by
the Calabi-Yau statement shape.
-/
theorem FirstChernRicciCohomologyBridge.firstChernClass_vanishes_iff_ricciFormClass_vanishes
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (B : FirstChernRicciCohomologyBridge E H I ER HR IR M g) :
    B.firstChernClass = B.zeroClass ↔ B.ricciFormCohomologyClass = B.zeroClass :=
  ⟨B.firstChernClassVanishingToRicciFormClassVanishing,
    B.ricciFormClassVanishingToFirstChernClassVanishing⟩

/--
Stage1 child surface for curvature, Ricci tensor, and Ricci form definitions
compatible with the current mathlib covariant-derivative and tensoriality APIs.

The checked carrier `tangentCovariantDerivative` is mathlib's bundled
covariant derivative on the real tangent bundle.  The curvature, Ricci tensor,
and Ricci form are represented by pointwise continuous multilinear tensor slots
over `TangentSpace IR x`; the fields after them are the formalization
obligations that a future terminal API must replace by definitions and theorems.
This does not claim the existence of mathlib Ricci curvature or Ricci-form
definitions at the pinned revision.
-/
structure CurvatureRicciTensorFormPackage
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (ER : Type u) [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    (HR : Type u) [TopologicalSpace HR] (IR : ModelWithCorners ℝ ER HR)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M]
    (g : CompactComplexKahlerMetric E H I ER HR IR M) : Type (u + 1) where
  tangentCovariantDerivative :
    CovariantDerivative IR ER (fun x : M => TangentSpace IR x)
  covariantDerivativeIsMetricCompatible : Prop
  covariantDerivativeIsTorsionFree : Prop
  curvatureTensorAt :
    (x : M) →
      TangentSpace IR x →L[ℝ]
        TangentSpace IR x →L[ℝ]
          TangentSpace IR x →L[ℝ] TangentSpace IR x
  curvatureTensorComesFromCovariantDerivative : Prop
  curvatureTensorIsTensorialInVectorFields : Prop
  ricciTensorAt :
    (x : M) → TangentSpace IR x →L[ℝ] TangentSpace IR x →L[ℝ] ℝ
  ricciTensorContractsCurvatureTensor : Prop
  ricciTensorIsSymmetric : Prop
  ricciFormAt :
    (x : M) → TangentSpace IR x →L[ℝ] TangentSpace IR x →L[ℝ] ℝ
  ricciFormIsAlternating : Prop
  ricciFormComesFromRicciTensorAndComplexStructure : Prop
  ricciFormCompatibleWithKahlerMetric : Prop
  ricciFormCompatibleWithFirstChernBridge :
    FirstChernRicciCohomologyBridge E H I ER HR IR M g → Prop
  ricciFlatIffRicciTensorVanishes : Prop
  ricciFlatIffRicciFormVanishes : Prop

/--
The bundled mathlib covariant derivative carried by the curvature/Ricci package.
-/
def CurvatureRicciTensorFormPackage.toCovariantDerivative
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (P : CurvatureRicciTensorFormPackage E H I ER HR IR M g) :
    CovariantDerivative IR ER (fun x : M => TangentSpace IR x) :=
  P.tangentCovariantDerivative

/-- The pointwise curvature tensor slot carried by the package. -/
def CurvatureRicciTensorFormPackage.toCurvatureTensorAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (P : CurvatureRicciTensorFormPackage E H I ER HR IR M g) :
    (x : M) →
      TangentSpace IR x →L[ℝ]
        TangentSpace IR x →L[ℝ]
          TangentSpace IR x →L[ℝ] TangentSpace IR x :=
  P.curvatureTensorAt

/-- The pointwise Ricci tensor slot carried by the package. -/
def CurvatureRicciTensorFormPackage.toRicciTensorAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (P : CurvatureRicciTensorFormPackage E H I ER HR IR M g) :
    (x : M) → TangentSpace IR x →L[ℝ] TangentSpace IR x →L[ℝ] ℝ :=
  P.ricciTensorAt

/-- The pointwise Ricci form slot carried by the package. -/
def CurvatureRicciTensorFormPackage.toRicciFormAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (P : CurvatureRicciTensorFormPackage E H I ER HR IR M g) :
    (x : M) → TangentSpace IR x →L[ℝ] TangentSpace IR x →L[ℝ] ℝ :=
  P.ricciFormAt

/--
Checked child-task anchor: the curvature/Ricci package carries a genuine mathlib
covariant derivative, so it inherits the zero-section law from
`CovariantDerivative.zero`.
-/
theorem CurvatureRicciTensorFormPackage.covariantDerivative_zeroSection
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (P : CurvatureRicciTensorFormPackage E H I ER HR IR M g) :
    P.toCovariantDerivative 0 = 0 :=
  CovariantDerivative.zero P.toCovariantDerivative

/--
Checked child-task anchor: the package's Ricci form projection is definitionally
the pointwise tensor slot recorded in the structure.
-/
theorem CurvatureRicciTensorFormPackage.ricciFormAt_eq
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {g : CompactComplexKahlerMetric E H I ER HR IR M}
    (P : CurvatureRicciTensorFormPackage E H I ER HR IR M g) :
    P.toRicciFormAt = P.ricciFormAt :=
  rfl

/--
Stage1 child surface for the complex Monge-Ampere equation and the continuity
method proof tree used in Yau's solution of the Calabi conjecture.

The current pinned mathlib snapshot does not provide terminal APIs for complex
Hessian operators, complex Monge-Ampere measures, elliptic Schauder estimates,
Evans-Krylov regularity, or continuity-method compactness on compact Kahler
manifolds.  This package therefore records the future carriers and proof
obligations explicitly.  The checked fields below are statement/proof-tree
interfaces only; they are not a proof of Yau's theorem.
-/
structure ComplexMongeAmpereContinuityPackage
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (ER : Type u) [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    (HR : Type u) [TopologicalSpace HR] (IR : ModelWithCorners ℝ ER HR)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M]
    (X : CalabiYauInput E H I M) (κ : X.kahlerClass)
    (g : CompactComplexKahlerMetric E H I ER HR IR M)
    (B : FirstChernRicciCohomologyBridge E H I ER HR IR M g)
    (R : CurvatureRicciTensorFormPackage E H I ER HR IR M g) : Type (u + 1) where
  potentialCarrier : Type u
  zeroPotential : potentialCarrier
  targetVolumeCarrier : Type u
  targetVolumeForm : targetVolumeCarrier
  referenceVolumeForm : targetVolumeCarrier
  normalizedVolumeCompatibility : Prop
  complexHessianCarrier : Type u
  complexHessian : potentialCarrier → complexHessianCarrier
  perturbedKahlerFormCarrier : Type u
  perturbedKahlerForm : potentialCarrier → perturbedKahlerFormCarrier
  perturbedFormRepresentsClass : potentialCarrier → Prop
  perturbedFormIsPositive : potentialCarrier → Prop
  mongeAmpereMeasureCarrier : Type u
  mongeAmpereMeasure : potentialCarrier → mongeAmpereMeasureCarrier
  mongeAmpereEquation : potentialCarrier → Prop
  mongeAmpereEquationUsesTargetVolume : Prop
  mongeAmpereEquationEquivalentToRicciPrescription : Prop
  ricciPrescriptionUsesFirstChernBridge : Prop
  parameterCarrier : Type u
  parameterZero : parameterCarrier
  parameterOne : parameterCarrier
  parameterInUnitInterval : parameterCarrier → Prop
  continuityEquation : parameterCarrier → potentialCarrier → Prop
  continuitySet : parameterCarrier → Prop
  continuitySet_def :
    ∀ t, continuitySet t ↔ ∃ φ, continuityEquation t φ
  zeroParameterInContinuitySet : continuitySet parameterZero
  targetParameterInUnitInterval : parameterInUnitInterval parameterOne
  targetEquationEquivalentToMongeAmpere :
    ∀ φ, continuityEquation parameterOne φ ↔ mongeAmpereEquation φ
  linearizationCarrier : parameterCarrier → potentialCarrier → Type u
  linearizationIsElliptic : ∀ t φ, continuityEquation t φ → Prop
  opennessByImplicitFunctionTheorem : Prop
  c0Estimate : Prop
  laplacianEstimate : Prop
  higherOrderEstimate : Prop
  closednessByArzelaAscoliAndRegularity : Prop
  continuitySetReachesTarget : continuitySet parameterOne
  solutionMetricData :
    (φ : potentialCarrier) →
      mongeAmpereEquation φ → RicciFlatKahlerMetricData E H I M X
  solutionRepresentsTargetClass :
    ∀ φ hφ, (solutionMetricData φ hφ).representsClass κ
  solutionCompatibleWithComplexStructure :
    ∀ φ hφ,
      (solutionMetricData φ hφ).smoothCompatibilityWithComplexStructure
        (solutionMetricData φ hφ).metric
  solutionIsKahlerMetric :
    ∀ φ hφ,
      (solutionMetricData φ hφ).isKahlerMetric
        (solutionMetricData φ hφ).metric
  solutionIsRicciFlat :
    ∀ φ hφ,
      (solutionMetricData φ hφ).isRicciFlat
        (solutionMetricData φ hφ).metric

/-- The terminal Monge-Ampere equation slot carried by the continuity package. -/
def ComplexMongeAmpereContinuityPackage.toMongeAmpereEquation
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {X : CalabiYauInput E H I M} {κ : X.kahlerClass}
    {g : CompactComplexKahlerMetric E H I ER HR IR M}
    {B : FirstChernRicciCohomologyBridge E H I ER HR IR M g}
    {R : CurvatureRicciTensorFormPackage E H I ER HR IR M g}
    (A : ComplexMongeAmpereContinuityPackage E H I ER HR IR M X κ g B R) :
    A.potentialCarrier → Prop :=
  A.mongeAmpereEquation

/--
Checked child-task anchor: a solution of the target continuity equation is a
solution of the terminal Monge-Ampere equation by the package equivalence.
-/
theorem ComplexMongeAmpereContinuityPackage.target_solution_solves_mongeAmpere
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {X : CalabiYauInput E H I M} {κ : X.kahlerClass}
    {g : CompactComplexKahlerMetric E H I ER HR IR M}
    {B : FirstChernRicciCohomologyBridge E H I ER HR IR M g}
    {R : CurvatureRicciTensorFormPackage E H I ER HR IR M g}
    (A : ComplexMongeAmpereContinuityPackage E H I ER HR IR M X κ g B R)
    {φ : A.potentialCarrier} (hφ : A.continuityEquation A.parameterOne φ) :
    A.mongeAmpereEquation φ :=
  (A.targetEquationEquivalentToMongeAmpere φ).mp hφ

/--
Checked child-task anchor: reaching the target parameter and identifying the
target equation with the Monge-Ampere equation yields the expected Ricci-flat
Kahler metric datum for the prescribed class.
-/
theorem ComplexMongeAmpereContinuityPackage.exists_ricciFlatKahlerMetricData
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
    {ER : Type u} [NormedAddCommGroup ER] [NormedSpace ℝ ER]
    {HR : Type u} [TopologicalSpace HR] {IR : ModelWithCorners ℝ ER HR}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M] [ChartedSpace HR M]
    [IsManifold IR 1 M] {X : CalabiYauInput E H I M} {κ : X.kahlerClass}
    {g : CompactComplexKahlerMetric E H I ER HR IR M}
    {B : FirstChernRicciCohomologyBridge E H I ER HR IR M g}
    {R : CurvatureRicciTensorFormPackage E H I ER HR IR M g}
    (A : ComplexMongeAmpereContinuityPackage E H I ER HR IR M X κ g B R) :
    ∃ q : RicciFlatKahlerMetricData E H I M X,
      q.representsClass κ ∧
        q.smoothCompatibilityWithComplexStructure q.metric ∧
          q.isKahlerMetric q.metric ∧ q.isRicciFlat q.metric := by
  rcases (A.continuitySet_def A.parameterOne).mp A.continuitySetReachesTarget with
    ⟨φ, hφ⟩
  let hMA : A.mongeAmpereEquation φ :=
    A.target_solution_solves_mongeAmpere hφ
  refine ⟨A.solutionMetricData φ hMA, ?_, ?_, ?_, ?_⟩
  · exact A.solutionRepresentsTargetClass φ hMA
  · exact A.solutionCompatibleWithComplexStructure φ hMA
  · exact A.solutionIsKahlerMetric φ hMA
  · exact A.solutionIsRicciFlat φ hMA

/--
Leaf-budget ledger for the Monge-Ampere/continuity-method package.

Each count is a local proof-unit budget, not a completed theorem count.  The
checked inequalities record that the proposed child ledger is already split
below the M0387 `<=100` leaf threshold.
-/
structure MongeAmpereContinuityLeafLedger : Type where
  statementAndNormalizationLeaves : Nat
  cohomologyAndRicciPrescriptionLeaves : Nat
  continuitySetSetupLeaves : Nat
  opennessLeaves : Nat
  closednessAndEstimateLeaves : Nat
  targetExtractionLeaves : Nat
  statementAndNormalizationWithinBudget : statementAndNormalizationLeaves ≤ 100
  cohomologyAndRicciPrescriptionWithinBudget : cohomologyAndRicciPrescriptionLeaves ≤ 100
  continuitySetSetupWithinBudget : continuitySetSetupLeaves ≤ 100
  opennessWithinBudget : opennessLeaves ≤ 100
  closednessAndEstimateWithinBudget : closednessAndEstimateLeaves ≤ 100
  targetExtractionWithinBudget : targetExtractionLeaves ≤ 100

/-- Integration-ready `<=100` leaf budget for child task `S1-M-130-C006`. -/
def mongeAmpereContinuityLeafLedger : MongeAmpereContinuityLeafLedger where
  statementAndNormalizationLeaves := 8
  cohomologyAndRicciPrescriptionLeaves := 10
  continuitySetSetupLeaves := 9
  opennessLeaves := 12
  closednessAndEstimateLeaves := 18
  targetExtractionLeaves := 7
  statementAndNormalizationWithinBudget := by decide
  cohomologyAndRicciPrescriptionWithinBudget := by decide
  continuitySetSetupWithinBudget := by decide
  opennessWithinBudget := by decide
  closednessAndEstimateWithinBudget := by decide
  targetExtractionWithinBudget := by decide

/--
Normalized Stage1 statement shape for the Ricci-flat Calabi conjecture.

For every compact smooth complex manifold in the audited object model, if the
first Chern class vanishes and the chosen class is a Kahler class, then there is
a metric datum representing that class, compatible with the complex structure,
Kahler, and Ricci-flat.  This is a proposition only; no proof of the terminal
theorem is claimed in this Stage1 artifact.
-/
def StatementShape : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M]
    (X : CalabiYauInput E H I M) (κ : X.kahlerClass),
      X.firstChernClassVanishes →
        X.classIsKahler κ →
          ∃ g : RicciFlatKahlerMetricData E H I M X,
            g.representsClass κ ∧
              g.smoothCompatibilityWithComplexStructure g.metric ∧
                g.isKahlerMetric g.metric ∧ g.isRicciFlat g.metric

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℂ E]
      (H : Type u) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
      (M : Type u) [TopologicalSpace M] [ChartedSpace H M]
      (X : CalabiYauInput E H I M) (κ : X.kahlerClass),
        X.firstChernClassVanishes →
          X.classIsKahler κ →
            ∃ g : RicciFlatKahlerMetricData E H I M X,
              g.representsClass κ ∧
                g.smoothCompatibilityWithComplexStructure g.metric ∧
                  g.isKahlerMetric g.metric ∧ g.isRicciFlat g.metric) :
    StatementShape.{u} :=
  h

/-- Checked mathlib anchor: holomorphic functions on compact complex manifolds are locally constant. -/
theorem compactComplex_holomorphic_isLocallyConstant
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {F : Type u} [NormedAddCommGroup F] [NormedSpace ℂ F]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H} [I.Boundaryless]
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I 1 M] [CompactSpace M] {f : M → F} (hf : MDiff f) :
    IsLocallyConstant f :=
  hf.isLocallyConstant

/-- Checked mathlib anchor: holomorphic functions on compact preconnected complex manifolds are constant. -/
theorem compactPreconnectedComplex_holomorphic_apply_eq
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℂ E]
    {F : Type u} [NormedAddCommGroup F] [NormedSpace ℂ F]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners ℂ E H} [I.Boundaryless]
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I 1 M] [CompactSpace M] [PreconnectedSpace M]
    {f : M → F} (hf : MDiff f) (a b : M) :
    f a = f b :=
  hf.apply_eq_of_compactSpace a b

/-- Checked mathlib anchor: the standard real vector space carries a smooth Riemannian metric. -/
def riemannianMetricVectorSpaceAnchor
    (F : Type u) [NormedAddCommGroup F] [InnerProductSpace ℝ F] :
    ContMDiffRiemannianMetric 𝓘(ℝ, F) ω F
      (fun x : F => TangentSpace 𝓘(ℝ, F) x) :=
  riemannianMetricVectorSpace F

/-- Checked mathlib anchor: the vector-space Riemannian extended distance is reflexive. -/
theorem vectorSpace_riemannianEDist_selfAnchor
    {F : Type u} [NormedAddCommGroup F] [InnerProductSpace ℝ F] (x : F) :
    riemannianEDist 𝓘(ℝ, F) x x = 0 :=
  riemannianEDist_self

/-- Checked mathlib anchor: a covariant derivative sends the zero section to zero on its domain. -/
theorem covariantDerivative_zeroSectionAnchor
    {𝕜 : Type u} [NontriviallyNormedField 𝕜]
    {E : Type u} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type u} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type u} [TopologicalSpace M] [ChartedSpace H M]
    (F : Type u) [NormedAddCommGroup F] [NormedSpace 𝕜 F]
    {V : M → Type u} [TopologicalSpace (TotalSpace F V)]
    [∀ x, NormedAddCommGroup (V x)] [∀ x, Module 𝕜 (V x)]
    [∀ x : M, TopologicalSpace (V x)]
    [∀ x, IsTopologicalAddGroup (V x)] [∀ x, ContinuousSMul 𝕜 (V x)]
    [FiberBundle F V] [VectorBundle 𝕜 F V]
    {cov : (Π x : M, V x) → (Π x : M, TangentSpace I x →L[𝕜] V x)}
    {s : Set M} (hcov : IsCovariantDerivativeOn F cov s) {x : M} (hx : x ∈ s) :
    cov 0 x = 0 :=
  hcov.zero hx

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Complex",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.Tensoriality",
  "Mathlib.RingTheory.Kaehler.Basic"
]

/--
Nearby mathlib names audited for the statement boundary.

The `KaehlerDifferential` names are algebraic Kähler differentials, not Kahler
metrics on complex manifolds.
-/
def mathlibAnchorNames : List String := [
  "MDifferentiable.isLocallyConstant",
  "MDifferentiable.apply_eq_of_compactSpace",
  "ContMDiffRiemannianMetric",
  "riemannianMetricVectorSpace",
  "riemannianEDist",
  "riemannianEDist_self",
  "IsCovariantDerivativeOn",
  "CovariantDerivative",
  "TensorialAt",
  "ContinuousLinearMap",
  "KaehlerDifferential",
  "KaehlerDifferential.D"
]

/-- Search terms that did not locate a terminal importable Calabi-Yau theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Calabi",
  "Yau",
  "CalabiYau",
  "Calabi-Yau",
  "KahlerMetric",
  "Kähler metric",
  "Riemann curvature",
  "CurvatureTensor",
  "Ricci",
  "RicciTensor",
  "RicciForm",
  "RicciFlat",
  "Chern class compact complex manifold",
  "Monge Ampere"
]

/-- Exact child-task search terms required for the external Lean 4 audit. -/
def externalLeanSearchTerms : List String := [
  "CalabiYau",
  "RicciFlat",
  "KahlerMetric",
  "Monge-Ampere",
  "first Chern"
]

/--
Authenticated GitHub code search status for child task `S1-M-130-C007`.

The child runtime had no `gh` login and no `GH_TOKEN`/`GITHUB_TOKEN`
environment token, so the required authenticated external Lean 4 code search is
recorded as blocked rather than completed.  No external placeholder-free
Calabi-Yau Lean 4 proof has been pinned, imported, or checked in this local Lake
closure.
-/
def externalLeanSearchAuthenticationStatus : String :=
  "blocked: gh auth status reported no logged-in GitHub host; GH_TOKEN and " ++
  "GITHUB_TOKEN were unset; unauthenticated GitHub code search was rate-limited."

/--
M0387 integration-debt boundary for the external-audit child.

This is deliberately a non-completion note: no external theorem closure is being
kept as anchor-only evidence, and no `repo_local_integration_debt` is being
declared complete.
-/
def externalLeanSearchConclusion : String :=
  "S1-M-130-C007 remains open: authenticated external Lean 4 search must be " ++
  "rerun before any public completion claim. If a placeholder-free external " ++
  "proof is found, it must be pin/import/check integrated or recorded with a " ++
  "concrete integration blocker."

/--
M0387 completion-eligible routes for this Stage1 theorem slot.

The `externalUpstreamPinned` case means an external proof body has entered this
repository's Lake closure as a pinned or vendored dependency and has a local
wrapper that validates.  It is not an anchor-only URL or theorem-name note.
-/
inductive RepoLocalClosureRoute : Type
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned

/--
Repo-local closure gate for child task `S1-M-130-C008`.

No value of this structure is constructed here.  The point is to make the
completion contract explicit: a future completion must carry a local proof of
`StatementShape`, a passing local Lean validation record, a placeholder-free
artifact condition, and an explicit no-`repo_local_integration_debt` condition.
-/
structure RepoLocalClosureGate : Type (u + 1) where
  route : RepoLocalClosureRoute
  statementShapeProof : StatementShape.{u}
  validationCommand : String
  validationPassed : Prop
  noSorryAdmitAxiom : Prop
  noRepoLocalIntegrationDebt : Prop

/-- The M0387 gate conditions that must accompany any future completion claim. -/
def RepoLocalClosureGate.m0387Eligible (G : RepoLocalClosureGate.{u}) : Prop :=
  G.validationPassed ∧ G.noSorryAdmitAxiom ∧ G.noRepoLocalIntegrationDebt

/--
Checked gate projection: once a future artifact carries a full repo-local
closure gate, the normalized Calabi-Yau statement is available locally.
-/
theorem RepoLocalClosureGate.statementShape_of_m0387Eligible
    (G : RepoLocalClosureGate.{u}) (_hG : G.m0387Eligible) : StatementShape.{u} :=
  G.statementShapeProof

/-- The integration-debt component forced by the M0387 completion gate. -/
theorem RepoLocalClosureGate.noRepoLocalIntegrationDebt_of_m0387Eligible
    (G : RepoLocalClosureGate.{u}) (hG : G.m0387Eligible) :
    G.noRepoLocalIntegrationDebt :=
  hG.2.2

/--
Child-task `S1-M-130-C008` status note.

This is intentionally an open-state note: the local file now checks the gate
shape, but no local proof body, mathlib wrapper, or pinned external proof
closure for Yau's theorem has been supplied.
-/
def c008RepoLocalClosureGateConclusion : String :=
  "S1-M-130-C008 remains open: completion requires a validating " ++
  "RepoLocalClosureGate via local_proof_body, local_wrapper_upstream_mathlib, " ++
  "or external_upstream_pinned, with no residual repo_local_integration_debt."

end AwesomeTheorems.Stage1.S1_M_130
