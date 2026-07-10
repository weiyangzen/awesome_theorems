import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Geometry.Manifold.MFDeriv.SpecificFunctions
import Mathlib.Geometry.Manifold.VectorBundle.SmoothSection
import Mathlib.Geometry.Manifold.VectorBundle.Tangent
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.MeasureTheory.Measure.Dirac

/-!
# S1-M-113 / THM-M-0570: heat-kernel proof of the index theorem

This Stage1 artifact records a conservative Lean boundary for the Atiyah-Singer
index theorem as proved by heat-kernel methods.  The pinned mathlib revision has
substantial smooth-manifold, tangent-bundle, compact-operator, and measure
substrates, but the audit did not locate a terminal Lean theorem for elliptic
differential operators, heat kernels, characteristic-class local index density,
or the Atiyah-Singer index formula.

The declarations below therefore avoid proof placeholders and false completion
claims.  They define the data needed to state the heat-kernel index formula and
provide small wrappers around currently available mathlib facts.
-/

noncomputable section

open MeasureTheory
open scoped Manifold Topology ContDiff

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_113

universe uM uD uC u𝕜 uE uH uF₁ uF₂ uV₁ uV₂ uΞ uK uT uX uY uα uβ

/--
Concrete Stage1 carrier for differential operators between smooth sections of
two smooth real vector bundles over the same smooth manifold.

This is stronger than the original abstract `Operator : Type` boundary: the
operator is now a Lean function between mathlib `C^∞` section spaces.  The
finite-jet property remains a proposition because the pinned mathlib closure
does not yet expose a native finite-jet/differential-operator API.
-/
structure SmoothVectorBundleDifferentialOperator
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    (V₁ : M → Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    (V₂ : M → Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I] where
  order : ℕ
  toFun : ContMDiffSection I F₁ ∞ V₁ → ContMDiffSection I F₂ ∞ V₂
  locallyFiniteJetDetermined : Prop

/--
Checked projection: the concrete differential-operator carrier sends smooth
sections to smooth sections by construction.
-/
theorem smoothVectorBundleDifferentialOperator_maps_smooth_sections
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    {V₁ : M → Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    {V₂ : M → Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (P : SmoothVectorBundleDifferentialOperator I M F₁ V₁ F₂ V₂)
    (s : ContMDiffSection I F₁ ∞ V₁) :
    CMDiff ∞ (T% fun x => P.toFun s x) :=
  (P.toFun s).contMDiff

/--
Principal-symbol data for a smooth vector-bundle differential operator.

The covector model is explicit because this pinned mathlib checkout has tangent
spaces and smooth vector-bundle sections, but no native cotangent-bundle /
finite-jet principal-symbol object for differential operators.  The symbol
itself is still concrete at each base point: a linear map from the source fiber
to the target fiber.
-/
structure BundlePrincipalSymbol
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    (V₁ : M → Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    (V₂ : M → Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (Ξ : M → Type uΞ) where
  isNonzeroCovector : (x : M) → Ξ x → Prop
  symbolAt : (x : M) → Ξ x → V₁ x →ₗ[ℝ] V₂ x
  symbolIsInvertible : (x : M) → Ξ x → Prop

/--
Ellipticity for the local principal-symbol model: the top-order symbol is
invertible at every nonzero covector.
-/
def BundlePrincipalSymbol.IsElliptic
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    {V₁ : M → Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    {V₂ : M → Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    {Ξ : M → Type uΞ}
    (σ : BundlePrincipalSymbol I M F₁ V₁ F₂ V₂ Ξ) : Prop :=
  ∀ x ξ, σ.isNonzeroCovector x ξ → σ.symbolIsInvertible x ξ

/--
Concrete elliptic differential-operator API for the heat-kernel index slot.

This package links the smooth-section operator carrier to a principal symbol
and stores the two proof obligations needed before the object can be treated as
a genuine elliptic differential operator: the symbol is the top-order symbol of
the operator, and the symbol is invertible off the zero section.
-/
structure EllipticDifferentialOperatorAPI
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    (V₁ : M → Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    (V₂ : M → Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I] where
  operator : SmoothVectorBundleDifferentialOperator I M F₁ V₁ F₂ V₂
  CotangentVector : M → Type uΞ
  principalSymbol : BundlePrincipalSymbol I M F₁ V₁ F₂ V₂ CotangentVector
  principalSymbolMatchesTopOrderPart : Prop
  elliptic : principalSymbol.IsElliptic

/-- Checked projection of ellipticity from the concrete operator API. -/
theorem ellipticDifferentialOperatorAPI_isElliptic
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    {V₁ : M → Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    {V₂ : M → Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (P : EllipticDifferentialOperatorAPI I M F₁ V₁ F₂ V₂) :
    P.principalSymbol.IsElliptic :=
  P.elliptic

/--
Repo-local Fredholm analytic-index carrier for continuous linear
realizations.

This is intentionally separate from mathlib's compact-operator Fredholm
alternative: a Fredholm realization is recorded by finite-dimensional kernel,
closed range, and finite-dimensional cokernel.  No compactness hypothesis is
part of this structure.
-/
structure FredholmAnalyticOperator
    (𝕜 : Type u𝕜) [NontriviallyNormedField 𝕜]
    (X : Type uX) [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    (Y : Type uY) [NormedAddCommGroup Y] [NormedSpace 𝕜 Y] where
  toContinuousLinearMap : X →L[𝕜] Y
  closedRange : IsClosed (LinearMap.range toContinuousLinearMap.toLinearMap : Set Y)
  finiteDimensionalKernel :
    FiniteDimensional 𝕜 (LinearMap.ker toContinuousLinearMap.toLinearMap)
  finiteDimensionalCokernel :
    FiniteDimensional 𝕜 (Y ⧸ LinearMap.range toContinuousLinearMap.toLinearMap)

namespace FredholmAnalyticOperator

/--
The Fredholm analytic index of a continuous linear realization:
`dim ker(T) - dim coker(T)`.
-/
noncomputable def analyticIndex
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace 𝕜 Y]
    (T : FredholmAnalyticOperator 𝕜 X Y) : ℤ :=
  (Module.finrank 𝕜 (LinearMap.ker T.toContinuousLinearMap.toLinearMap) : ℤ) -
    (Module.finrank 𝕜 (Y ⧸ LinearMap.range T.toContinuousLinearMap.toLinearMap) : ℤ)

/-- Checked projection of finite-dimensionality of the Fredholm kernel. -/
theorem finiteDimensional_kernel
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace 𝕜 Y]
    (T : FredholmAnalyticOperator 𝕜 X Y) :
    FiniteDimensional 𝕜 (LinearMap.ker T.toContinuousLinearMap.toLinearMap) :=
  T.finiteDimensionalKernel

/-- Checked projection of finite-dimensionality of the Fredholm cokernel. -/
theorem finiteDimensional_cokernel
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace 𝕜 Y]
    (T : FredholmAnalyticOperator 𝕜 X Y) :
    FiniteDimensional 𝕜 (Y ⧸ LinearMap.range T.toContinuousLinearMap.toLinearMap) :=
  T.finiteDimensionalCokernel

/-- Checked projection of closed range, included because cokernel dimension alone is not enough. -/
theorem isClosed_range
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace 𝕜 Y]
    (T : FredholmAnalyticOperator 𝕜 X Y) :
    IsClosed (LinearMap.range T.toContinuousLinearMap.toLinearMap : Set Y) :=
  T.closedRange

/-- The analytic-index definition unfolds to kernel dimension minus cokernel dimension. -/
theorem analyticIndex_def
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace 𝕜 Y]
    (T : FredholmAnalyticOperator 𝕜 X Y) :
    T.analyticIndex =
      (Module.finrank 𝕜 (LinearMap.ker T.toContinuousLinearMap.toLinearMap) : ℤ) -
        (Module.finrank 𝕜 (Y ⧸ LinearMap.range T.toContinuousLinearMap.toLinearMap) : ℤ) :=
  rfl

end FredholmAnalyticOperator

/--
Fredholm analytic-index package for an elliptic differential operator after
choosing analytic realization spaces, e.g. Sobolev completions of smooth
sections.

The two proposition fields are explicit integration obligations.  They mark
where a later formalization must prove that the continuous linear realization
really models the differential operator and that elliptic regularity supplies
the Fredholm property.
-/
structure EllipticFredholmAnalyticIndexPackage
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (F₁ : Type uF₁) [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    (V₁ : M → Type uV₁) [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    (F₂ : Type uF₂) [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    (V₂ : M → Type uV₂) [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    (X : Type uX) [NormedAddCommGroup X] [NormedSpace ℝ X]
    (Y : Type uY) [NormedAddCommGroup Y] [NormedSpace ℝ Y] where
  ellipticOperator :
    EllipticDifferentialOperatorAPI.{uM, uE, uH, uF₁, uF₂, uV₁, uV₂, uΞ}
      I M F₁ V₁ F₂ V₂
  realization : FredholmAnalyticOperator ℝ X Y
  realizationModelsDifferentialOperator : Prop
  ellipticRegularityGivesFredholmRealization : Prop

namespace EllipticFredholmAnalyticIndexPackage

/-- Analytic index of the selected Fredholm realization of an elliptic operator. -/
noncomputable def analyticIndex
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    {V₁ : M → Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    {V₂ : M → Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace ℝ Y]
    (A : EllipticFredholmAnalyticIndexPackage I M F₁ V₁ F₂ V₂ X Y) : ℤ :=
  A.realization.analyticIndex

/-- Checked projection: the package exposes the underlying ellipticity proof. -/
theorem elliptic
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    {V₁ : M → Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    {V₂ : M → Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace ℝ Y]
    (A : EllipticFredholmAnalyticIndexPackage I M F₁ V₁ F₂ V₂ X Y) :
    A.ellipticOperator.principalSymbol.IsElliptic :=
  A.ellipticOperator.elliptic

/-- The elliptic package index is exactly the Fredholm realization index. -/
theorem analyticIndex_def
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {F₁ : Type uF₁} [NormedAddCommGroup F₁] [NormedSpace ℝ F₁]
    {V₁ : M → Type uV₁} [TopologicalSpace (Bundle.TotalSpace F₁ V₁)]
    [∀ x : M, TopologicalSpace (V₁ x)] [FiberBundle F₁ V₁]
    [∀ x : M, AddCommGroup (V₁ x)] [∀ x : M, Module ℝ (V₁ x)]
    [VectorBundle ℝ F₁ V₁] [ContMDiffVectorBundle ∞ F₁ V₁ I]
    {F₂ : Type uF₂} [NormedAddCommGroup F₂] [NormedSpace ℝ F₂]
    {V₂ : M → Type uV₂} [TopologicalSpace (Bundle.TotalSpace F₂ V₂)]
    [∀ x : M, TopologicalSpace (V₂ x)] [FiberBundle F₂ V₂]
    [∀ x : M, AddCommGroup (V₂ x)] [∀ x : M, Module ℝ (V₂ x)]
    [VectorBundle ℝ F₂ V₂] [ContMDiffVectorBundle ∞ F₂ V₂ I]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {Y : Type uY} [NormedAddCommGroup Y] [NormedSpace ℝ Y]
    (A : EllipticFredholmAnalyticIndexPackage I M F₁ V₁ F₂ V₂ X Y) :
    A.analyticIndex = A.realization.analyticIndex :=
  rfl

end EllipticFredholmAnalyticIndexPackage

/--
Repo-local heat-semigroup/kernel carrier for the McKean-Singer branch.

The semigroup itself is concrete as a family of continuous linear endomorphisms.
The heat kernel is recorded as a scalar kernel on the underlying base type, with
separate propositions for the analytic facts not present in pinned mathlib:
solving the heat equation, representing the semigroup, and trace-class
regularity for positive time.
-/
structure HeatSemigroupKernelPackage
    (𝕜 : Type u𝕜) [NontriviallyNormedField 𝕜]
    (X : Type uX) [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    (M : Type uM) where
  generator : X →L[𝕜] X
  heatSemigroup : ℝ → X →L[𝕜] X
  heatKernel : ℝ → M → M → 𝕜
  positiveTime : ℝ → Prop
  semigroup_zero : heatSemigroup 0 = ContinuousLinearMap.id 𝕜 X
  semigroup_add :
    ∀ {s t : ℝ}, positiveTime s → positiveTime t →
      heatSemigroup (s + t) = (heatSemigroup s).comp (heatSemigroup t)
  solvesHeatEquation : Prop
  kernelRepresentsSemigroup : Prop
  traceClassForPositiveTime : Prop

namespace HeatSemigroupKernelPackage

/-- Checked projection of the time-zero semigroup law. -/
theorem heatSemigroup_zero
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    {M : Type uM} (K : HeatSemigroupKernelPackage 𝕜 X M) :
    K.heatSemigroup 0 = ContinuousLinearMap.id 𝕜 X :=
  K.semigroup_zero

/-- Checked projection of the positive-time semigroup composition law. -/
theorem heatSemigroup_add
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X]
    {M : Type uM} (K : HeatSemigroupKernelPackage 𝕜 X M)
    {s t : ℝ} (hs : K.positiveTime s) (ht : K.positiveTime t) :
    K.heatSemigroup (s + t) = (K.heatSemigroup s).comp (K.heatSemigroup t) :=
  K.semigroup_add hs ht

end HeatSemigroupKernelPackage

/--
Two-parity heat supertrace data.

For a Dirac-type operator, McKean-Singer compares the heat traces on the even
and odd summands.  This structure keeps those two heat-kernel packages
separate and records the supertrace as `tracePlus - traceMinus`, while leaving
the infinite-dimensional trace-class and kernel-integral identifications as
explicit formalization obligations.
-/
structure HeatSupertracePackage
    (𝕜 : Type u𝕜) [NontriviallyNormedField 𝕜]
    (XPlus : Type uX) [NormedAddCommGroup XPlus] [NormedSpace 𝕜 XPlus]
    (XMinus : Type uY) [NormedAddCommGroup XMinus] [NormedSpace 𝕜 XMinus]
    (M : Type uM) where
  plusHeat : HeatSemigroupKernelPackage 𝕜 XPlus M
  minusHeat : HeatSemigroupKernelPackage 𝕜 XMinus M
  tracePlus : ℝ → 𝕜
  traceMinus : ℝ → 𝕜
  supertrace : ℝ → 𝕜
  supertrace_def : ∀ t : ℝ, supertrace t = tracePlus t - traceMinus t
  tracePlusFromHeatKernel : Prop
  traceMinusFromHeatKernel : Prop
  heatKernelParametrixControlsTrace : Prop

namespace HeatSupertracePackage

/-- Checked projection of the supertrace definition. -/
theorem supertrace_eq_trace_sub
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {XPlus : Type uX} [NormedAddCommGroup XPlus] [NormedSpace 𝕜 XPlus]
    {XMinus : Type uY} [NormedAddCommGroup XMinus] [NormedSpace 𝕜 XMinus]
    {M : Type uM} (T : HeatSupertracePackage 𝕜 XPlus XMinus M) (t : ℝ) :
    T.supertrace t = T.tracePlus t - T.traceMinus t :=
  T.supertrace_def t

end HeatSupertracePackage

/--
Concrete finite-dimensional supertrace wrapper using mathlib matrix trace.

This is not the infinite-dimensional heat trace used in the full theorem.  It
is a checked local substrate for the `trace(e^{-tD^-D^+}) -
trace(e^{-tD^+D^-})` shape that later analytic packages must refine.
-/
noncomputable def matrixSupertrace
    {ιPlus : Type uα} {ιMinus : Type uβ} [Fintype ιPlus] [Fintype ιMinus]
    (APlus : Matrix ιPlus ιPlus ℝ) (AMinus : Matrix ιMinus ιMinus ℝ) : ℝ :=
  Matrix.trace APlus - Matrix.trace AMinus

/-- The finite-dimensional matrix supertrace unfolds to trace on even minus odd blocks. -/
theorem matrixSupertrace_def
    {ιPlus : Type uα} {ιMinus : Type uβ} [Fintype ιPlus] [Fintype ιMinus]
    (APlus : Matrix ιPlus ιPlus ℝ) (AMinus : Matrix ιMinus ιMinus ℝ) :
    matrixSupertrace APlus AMinus = Matrix.trace APlus - Matrix.trace AMinus :=
  rfl

/-- Checked sanity check: the matrix supertrace of zero blocks is zero. -/
theorem matrixSupertrace_zero
    {ιPlus : Type uα} {ιMinus : Type uβ} [Fintype ιPlus] [Fintype ιMinus] :
    matrixSupertrace (0 : Matrix ιPlus ιPlus ℝ) (0 : Matrix ιMinus ιMinus ℝ) = 0 := by
  simp [matrixSupertrace]

/--
McKean-Singer identity boundary for a real two-parity heat supertrace package.

The theorem field is intentionally a hypothesis of this package, not a claimed
proof.  It records the precise terminal identity later work must establish
after the heat-kernel parametrix and trace-class infrastructure are available.
-/
structure RealMcKeanSingerIdentityPackage
    (XPlus : Type uX) [NormedAddCommGroup XPlus] [NormedSpace ℝ XPlus]
    (XMinus : Type uY) [NormedAddCommGroup XMinus] [NormedSpace ℝ XMinus]
    (M : Type uM) where
  heatSupertracePackage : HeatSupertracePackage ℝ XPlus XMinus M
  fredholmIndex : ℤ
  supertrace_eq_index :
    ∀ {t : ℝ}, heatSupertracePackage.plusHeat.positiveTime t →
      heatSupertracePackage.supertrace t = (fredholmIndex : ℝ)

namespace RealMcKeanSingerIdentityPackage

/-- Checked eliminator for the McKean-Singer identity once the package obligations are supplied. -/
theorem apply_supertrace_eq_index
    {XPlus : Type uX} [NormedAddCommGroup XPlus] [NormedSpace ℝ XPlus]
    {XMinus : Type uY} [NormedAddCommGroup XMinus] [NormedSpace ℝ XMinus]
    {M : Type uM} (A : RealMcKeanSingerIdentityPackage XPlus XMinus M)
    {t : ℝ} (ht : A.heatSupertracePackage.plusHeat.positiveTime t) :
    A.heatSupertracePackage.supertrace t = (A.fredholmIndex : ℝ) :=
  A.supertrace_eq_index ht

end RealMcKeanSingerIdentityPackage

/--
The two local-index-density variants needed by the usual Atiyah-Singer
interfaces: the Todd-class form for complex elliptic symbols and the A-hat form
for Dirac-type operators with a twisting Chern character.
-/
inductive LocalIndexDensityVariant where
  | todd
  | aHat
deriving DecidableEq, Repr

namespace LocalIndexDensityVariant

/-- Human-readable label for ledger and audit surfaces. -/
def label : LocalIndexDensityVariant → String
  | todd => "Todd-class density"
  | aHat => "A-hat-class density"

/-- The Todd and A-hat branches are distinct local-density variants. -/
theorem todd_ne_aHat : LocalIndexDensityVariant.todd ≠ LocalIndexDensityVariant.aHat := by
  decide

end LocalIndexDensityVariant

/--
Repo-local characteristic-class API for the local index density.

This deliberately remains an API package rather than a theorem asserting that
mathlib currently provides Chern character, Todd class, or A-hat class objects
for smooth vector bundles.  It records the exact operations and identities the
heat-kernel index statement needs: Chern character of the elliptic symbol,
Chern character of a Dirac twisting class, Todd and A-hat characteristic
classes of the tangent datum, cup/product in the cohomology target, and the
fundamental-class pairing that produces the topological index.
-/
structure CharacteristicClassLocalIndexDensityAPI (M : Type uM) where
  Operator : Type uD
  CohomologyClass : Type uC
  SymbolKClass : Type uK
  TwistingKClass : Type uX
  TangentCharacteristicInput : Type uT
  cohomologyMul : CohomologyClass → CohomologyClass → CohomologyClass
  cohomologyPairing : CohomologyClass → ℤ
  symbolKClass : Operator → SymbolKClass
  twistingKClass : Operator → TwistingKClass
  baseTangentClass : TangentCharacteristicInput
  chernCharacterSymbol : SymbolKClass → CohomologyClass
  chernCharacterTwist : TwistingKClass → CohomologyClass
  toddClass : TangentCharacteristicInput → CohomologyClass
  aHatClass : TangentCharacteristicInput → CohomologyClass
  localIndexDensity : LocalIndexDensityVariant → Operator → CohomologyClass
  localIndexDensity_todd :
    ∀ P : Operator,
      localIndexDensity .todd P =
        cohomologyMul (chernCharacterSymbol (symbolKClass P)) (toddClass baseTangentClass)
  localIndexDensity_aHat :
    ∀ P : Operator,
      localIndexDensity .aHat P =
        cohomologyMul (aHatClass baseTangentClass) (chernCharacterTwist (twistingKClass P))
  topologicalIndex : LocalIndexDensityVariant → Operator → ℤ
  topologicalIndex_def :
    ∀ (v : LocalIndexDensityVariant) (P : Operator),
      topologicalIndex v P = cohomologyPairing (localIndexDensity v P)
  localDensityIdentified : LocalIndexDensityVariant → Operator → Prop

namespace CharacteristicClassLocalIndexDensityAPI

/-- Todd-class local density selected from the characteristic-class API. -/
def toddLocalIndexDensity {M : Type uM} (A : CharacteristicClassLocalIndexDensityAPI M)
    (P : A.Operator) : A.CohomologyClass :=
  A.localIndexDensity .todd P

/-- A-hat local density selected from the characteristic-class API. -/
def aHatLocalIndexDensity {M : Type uM} (A : CharacteristicClassLocalIndexDensityAPI M)
    (P : A.Operator) : A.CohomologyClass :=
  A.localIndexDensity .aHat P

/-- Checked Todd-density equation: `ch(symbol(P)) * Todd(TM)`. -/
theorem toddLocalIndexDensity_eq {M : Type uM}
    (A : CharacteristicClassLocalIndexDensityAPI M) (P : A.Operator) :
    A.toddLocalIndexDensity P =
      A.cohomologyMul (A.chernCharacterSymbol (A.symbolKClass P))
        (A.toddClass A.baseTangentClass) :=
  A.localIndexDensity_todd P

/-- Checked A-hat-density equation: `Ahat(TM) * ch(twist(P))`. -/
theorem aHatLocalIndexDensity_eq {M : Type uM}
    (A : CharacteristicClassLocalIndexDensityAPI M) (P : A.Operator) :
    A.aHatLocalIndexDensity P =
      A.cohomologyMul (A.aHatClass A.baseTangentClass)
        (A.chernCharacterTwist (A.twistingKClass P)) :=
  A.localIndexDensity_aHat P

/-- The selected topological index is the pairing with the selected local density. -/
theorem topologicalIndex_eq_pairing {M : Type uM}
    (A : CharacteristicClassLocalIndexDensityAPI M)
    (v : LocalIndexDensityVariant) (P : A.Operator) :
    A.topologicalIndex v P = A.cohomologyPairing (A.localIndexDensity v P) :=
  A.topologicalIndex_def v P

/-- Todd-form topological index as the pairing of `ch(symbol(P)) * Todd(TM)`. -/
theorem topologicalIndex_todd_eq_pairing {M : Type uM}
    (A : CharacteristicClassLocalIndexDensityAPI M) (P : A.Operator) :
    A.topologicalIndex .todd P =
      A.cohomologyPairing
        (A.cohomologyMul (A.chernCharacterSymbol (A.symbolKClass P))
          (A.toddClass A.baseTangentClass)) := by
  calc
    A.topologicalIndex .todd P =
        A.cohomologyPairing (A.localIndexDensity .todd P) :=
      A.topologicalIndex_eq_pairing .todd P
    _ = A.cohomologyPairing
        (A.cohomologyMul (A.chernCharacterSymbol (A.symbolKClass P))
          (A.toddClass A.baseTangentClass)) := by
      rw [A.localIndexDensity_todd P]

/-- A-hat-form topological index as the pairing of `Ahat(TM) * ch(twist(P))`. -/
theorem topologicalIndex_aHat_eq_pairing {M : Type uM}
    (A : CharacteristicClassLocalIndexDensityAPI M) (P : A.Operator) :
    A.topologicalIndex .aHat P =
      A.cohomologyPairing
        (A.cohomologyMul (A.aHatClass A.baseTangentClass)
          (A.chernCharacterTwist (A.twistingKClass P))) := by
  calc
    A.topologicalIndex .aHat P =
        A.cohomologyPairing (A.localIndexDensity .aHat P) :=
      A.topologicalIndex_eq_pairing .aHat P
    _ = A.cohomologyPairing
        (A.cohomologyMul (A.aHatClass A.baseTangentClass)
          (A.chernCharacterTwist (A.twistingKClass P))) := by
      rw [A.localIndexDensity_aHat P]

end CharacteristicClassLocalIndexDensityAPI

/--
Abstract data required to state the heat-kernel form of the index theorem.

The fields intentionally isolate the formalization boundary.  A later
integrator should replace `Operator`, `CohomologyClass`, the heat supertrace,
and the local-density predicates with concrete APIs for elliptic differential
operators on vector bundles over compact smooth manifolds.
-/
structure HeatKernelIndexData (M : Type uM) where
  Operator : Type uD
  CohomologyClass : Type uC
  analyticIndex : Operator → ℤ
  topologicalIndex : Operator → ℤ
  localIndexDensity : Operator → CohomologyClass
  heatSupertrace : Operator → ℝ → ℝ
  isElliptic : Operator → Prop
  isDiracType : Operator → Prop
  hasHeatKernelParametrix : Operator → Prop
  heatTraceComputesAnalyticIndex : Operator → Prop
  localDensityIdentified : Operator → Prop
  topologicalPairingComputesIndex : Operator → Prop

/--
Single-operator statement shape for the heat-kernel index formula.

The hypotheses separate the analytic heat-kernel branch from the topological
characteristic-class branch.  The conclusion is the expected equality of the
Fredholm analytic index and the topological index.
-/
def HeatKernelIndexFormula {M : Type uM} (D : HeatKernelIndexData M)
    (P : D.Operator) : Prop :=
  D.isElliptic P →
    D.hasHeatKernelParametrix P →
      D.heatTraceComputesAnalyticIndex P →
        D.localDensityIdentified P →
          D.topologicalPairingComputesIndex P →
            D.analyticIndex P = D.topologicalIndex P

/--
Stage1 normalized statement-shape candidate for the heat-kernel proof of the
Atiyah-Singer index theorem over a compact smooth real manifold.

The manifold hypotheses are concrete mathlib hypotheses.  The elliptic operator,
heat kernel, local index density, and characteristic-class pairing remain
abstract because no terminal repo-local or pinned mathlib API was located for
the full theorem.
-/
def StatementShape
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [CompactSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] (D : HeatKernelIndexData M) : Prop :=
  ∀ P : D.Operator, D.isDiracType P → HeatKernelIndexFormula D P

/-- The normalized statement shape unfolds to the per-operator heat-kernel formula. -/
theorem statementShape_iff_forall_operator
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [CompactSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] (D : HeatKernelIndexData M) :
    StatementShape E H I M D ↔
      ∀ P : D.Operator, D.isDiracType P → HeatKernelIndexFormula D P :=
  Iff.rfl

/--
Checked eliminator for the Stage1 statement shape.

This proves only that the abstract boundary has the expected final equality once
all analytic and topological hypotheses are supplied; it is not a proof that
those hypotheses hold for any concrete elliptic operator.
-/
theorem statementShape_apply
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [CompactSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] (D : HeatKernelIndexData M)
    (h : StatementShape E H I M D) (P : D.Operator)
    (hDirac : D.isDiracType P) (hElliptic : D.isElliptic P)
    (hHeat : D.hasHeatKernelParametrix P)
    (hTrace : D.heatTraceComputesAnalyticIndex P)
    (hDensity : D.localDensityIdentified P)
    (hPairing : D.topologicalPairingComputesIndex P) :
    D.analyticIndex P = D.topologicalIndex P :=
  h P hDirac hElliptic hHeat hTrace hDensity hPairing

/-- Checked wrapper: the identity map on a charted manifold is `C^n`. -/
theorem contMDiff_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {n : WithTop ℕ∞} :
    ContMDiff I I n (id : M → M) :=
  contMDiff_id

/-- Checked wrapper: the tangent map of the identity is the identity on the tangent bundle. -/
theorem tangentMap_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] :
    tangentMap I I (id : M → M) = id :=
  tangentMap_id

/-- Checked wrapper: the manifold derivative of the identity is the identity on each tangent space. -/
theorem mfderiv_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] (x : M) :
    mfderiv I I (id : M → M) x = ContinuousLinearMap.id 𝕜 (TangentSpace I x) :=
  mfderiv_id

/--
Checked wrapper for mathlib's Fredholm alternative for compact operators.

This is an analytic substrate only; it is not a Fredholm-index theorem for
elliptic differential operators.
-/
theorem compact_operator_fredholm_alternative_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X] [CompleteSpace X]
    {T : X →L[𝕜] X} {μ : 𝕜}
    (hT : IsCompactOperator (T : X → X)) (hμ : μ ≠ 0) :
    Module.End.HasEigenvalue (T : Module.End 𝕜 X) μ ∨ μ ∈ resolventSet 𝕜 T :=
  IsCompactOperator.hasEigenvalue_or_mem_resolventSet hT hμ

/-- Checked wrapper: nonzero spectral points of a compact operator are eigenvalues. -/
theorem compact_operator_hasEigenvalue_iff_mem_spectrum_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {X : Type uX} [NormedAddCommGroup X] [NormedSpace 𝕜 X] [CompleteSpace X]
    {T : X →L[𝕜] X} {μ : 𝕜}
    (hT : IsCompactOperator (T : X → X)) (hμ : μ ≠ 0) :
    Module.End.HasEigenvalue (T : Module.End 𝕜 X) μ ↔ μ ∈ spectrum 𝕜 T :=
  IsCompactOperator.hasEigenvalue_iff_mem_spectrum hT hμ

/-- Checked wrapper for functoriality of Dirac measures under measurable maps. -/
theorem map_dirac_mathlib_wrapper
    {α : Type uα} {β : Type uβ} [MeasurableSpace α] [MeasurableSpace β]
    {f : α → β} (hf : Measurable f) (a : α) :
    Measure.map f (Measure.dirac a) = Measure.dirac (f a) :=
  Measure.map_dirac' hf a

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.MFDeriv.SpecificFunctions",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.Bordism",
  "Mathlib.Geometry.Manifold.WhitneyEmbedding",
  "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance",
  "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
  "Mathlib.LinearAlgebra.FiniteDimensional.Lemmas",
  "Mathlib.LinearAlgebra.Matrix.Trace",
  "Mathlib.MeasureTheory.Measure.Dirac",
  "Mathlib.Analysis.Distribution.TemperedDistribution"
]

/-- Search terms that did not locate a terminal Atiyah-Singer theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Atiyah",
  "Singer",
  "Atiyah-Singer",
  "index theorem",
  "IndexTheorem",
  "elliptic operator",
  "Dirac operator",
  "heat kernel",
  "HeatKernel",
  "Chern character",
  "Todd class",
  "A-hat class"
]

/--
Primary Lean 4 source audit rows for the external-anchor child task.

These strings are intentionally data-only: they record source anchors without
turning anchor-only evidence into a completed theorem claim.
-/
def externalPrimarySourceAuditRows : List String := [
  "leanprover-community/mathlib4 @ 8a178386ffc0f5fef0b77738bb5449d50efeea95: no terminal Atiyah-Singer / heat-kernel index theorem found; this repo validates only the abstract Stage1 boundary and substrate wrappers.",
  "ember-research-lab/Spectral-Physics-Lean @ 48db03bfe75a1d15e5a06a17d38ab1271de513fb: SpectralPhysics/Analysis/HeatSemigroup.lean contains heat-semigroup lemmas such as heat_kernel_psd, contraction, correlator_decay, and mass_from_gap; it is not a terminal Atiyah-Singer theorem and its SpectralDecomp structure is explicitly axiomatized in comments."
]

/--
Machine-closure status for an external Lean 4 proof candidate.

Only the three proof-body statuses can count as repo-local completion.  The
`externalAnchorOnly` state is deliberately separated so anchor-only evidence
cannot be misread as completed Stage1 closure.
-/
inductive ExternalLeanProofIntegrationStatus where
  | noTerminalProofFound
  | externalAnchorOnly
  | externalUpstreamPinned
  | localWrapperUpstreamMathlib
  | localProofBody
  | integrationBlocked
deriving DecidableEq, Repr

namespace ExternalLeanProofIntegrationStatus

/-- Whether this status is allowed to count as repo-local theorem completion. -/
def repoLocalCompleted : ExternalLeanProofIntegrationStatus → Bool
  | externalUpstreamPinned => true
  | localWrapperUpstreamMathlib => true
  | localProofBody => true
  | noTerminalProofFound => false
  | externalAnchorOnly => false
  | integrationBlocked => false

/-- Whether this status retains unresolved anchor-only integration debt. -/
def retainsRepoLocalIntegrationDebt : ExternalLeanProofIntegrationStatus → Bool
  | externalAnchorOnly => true
  | noTerminalProofFound => false
  | externalUpstreamPinned => false
  | localWrapperUpstreamMathlib => false
  | localProofBody => false
  | integrationBlocked => false

end ExternalLeanProofIntegrationStatus

/--
C008 integration gate row for the external Lean 4 proof audit.

The fields are strings because this Stage1 artifact is metadata, not a Lake
dependency declaration.  A future integrator must replace the `none` fields by
a pinned dependency or a concrete blocker before any completion upgrade.
-/
structure ExternalLeanProofIntegrationGate where
  candidate : String
  repository : String
  commit : String
  theoremFile : String
  theoremName : String
  toolchain : String
  lakeClosureResult : String
  status : ExternalLeanProofIntegrationStatus
  blocker : String
deriving Repr

/--
Current C008 gate: no terminal external Lean 4 proof of the heat-kernel
Atiyah-Singer theorem has been found and brought into this repo's Lake closure.
-/
def c008ExternalProofIntegrationGate : ExternalLeanProofIntegrationGate := {
  candidate := "terminal Atiyah-Singer / heat-kernel index theorem"
  repository := "none found"
  commit := "none"
  theoremFile := "none"
  theoremName := "none"
  toolchain := "none"
  lakeClosureResult := "not applicable: no terminal external proof candidate located"
  status := .noTerminalProofFound
  blocker :=
    "formalization_debt: build or import elliptic-operator, Fredholm-index, heat-kernel, and characteristic-class APIs; if a terminal external Lean 4 proof is later found, pin/import/check it or record a concrete dependency/toolchain/license blocker"
}

/-- The current C008 external-proof gate is not a repo-local completion state. -/
theorem c008ExternalProofIntegrationGate_not_completed :
    c008ExternalProofIntegrationGate.status.repoLocalCompleted = false :=
  rfl

/-- The current C008 gate retains no completed-state repo-local integration debt. -/
theorem c008ExternalProofIntegrationGate_no_repo_local_integration_debt :
    c008ExternalProofIntegrationGate.status.retainsRepoLocalIntegrationDebt = false :=
  rfl

/-- The current primary-source audit table has two data rows. -/
theorem externalPrimarySourceAuditRows_length :
    externalPrimarySourceAuditRows.length = 2 :=
  rfl

/--
Local proof-package status used by the Stage1 child ledgers.

`unchecked` means the package has a concrete proof target and a local step
budget, but no repo-local Lean proof body or pinned upstream proof has closed
that package.
-/
inductive LocalProofPackageStatus where
  | checked
  | unchecked
deriving DecidableEq, Repr

/--
Data-only local ledger row for the unchecked `L010` through `L026` proof
packages.  The `stepBudget` field records the M0387 upper bound for the future
local proof body; `budgetClosed = false` prevents this statement-shape artifact
from counting any of these rows as completed theorem leaves.
-/
structure LocalProofPackageLedger where
  leafId : String
  packageId : String
  status : LocalProofPackageStatus
  stepBudget : Nat
  budgetClosed : Bool
  repoLocalAnchor : String
  nextAction : String
deriving Repr

/-- M0387 budget predicate for a local proof-package ledger row. -/
def LocalProofPackageLedger.WithinM0387Budget (L : LocalProofPackageLedger) : Prop :=
  L.stepBudget <= 100

/--
The child-task split of previously flat unchecked leaves `L010` through `L026`.

Every row is intentionally `unchecked` and has `budgetClosed = false`: this is
an integration-ready package ledger, not a completion claim for the
Atiyah-Singer theorem.
-/
def uncheckedLeafLedgersL010ToL026 : List LocalProofPackageLedger := [
  { leafId := "L010_smooth_vector_bundle_sections",
    packageId := "P03.01_section_model",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "ContMDiffSection carrier and smooth-section projection",
    nextAction := "Replace the carrier boundary by the selected vector-bundle section API and prove coercion/evaluation lemmas." },
  { leafId := "L011_differential_operator_api",
    packageId := "P03.02_differential_operator_api",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "SmoothVectorBundleDifferentialOperator",
    nextAction := "Add finite-jet/order laws or import a differential-operator API; connect local coordinate formulas to section maps." },
  { leafId := "L012_principal_symbol",
    packageId := "P03.03_principal_symbol_ellipticity",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "BundlePrincipalSymbol and BundlePrincipalSymbol.IsElliptic",
    nextAction := "Replace abstract cotangent vectors by a cotangent-bundle API and prove symbol invertibility is the ellipticity predicate." },
  { leafId := "L013_dirac_type_operator",
    packageId := "P03.04_dirac_type_specialization",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "HeatKernelIndexData.isDiracType boundary",
    nextAction := "Define graded Clifford module data, Dirac-type operators, and the induced elliptic principal symbol." },
  { leafId := "L014_kernel_cokernel_finite_dimensional",
    packageId := "P03.05_fredholm_regularization",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "FredholmAnalyticOperator finiteDimensional_kernel/cokernel projections",
    nextAction := "Prove or import elliptic regularity and Fredholmness for the chosen analytic realization." },
  { leafId := "L015_analytic_index_definition",
    packageId := "P03.06_analytic_index",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "FredholmAnalyticOperator.analyticIndex and EllipticFredholmAnalyticIndexPackage.analyticIndex",
    nextAction := "Tie the Fredholm index to the elliptic operator realization and prove invariance under the selected completion." },
  { leafId := "L016_heat_semigroup",
    packageId := "P04.01_heat_semigroup",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "HeatSemigroupKernelPackage.heatSemigroup_zero/add",
    nextAction := "Construct the heat semigroup for the Laplace-type operator or pin an upstream construction." },
  { leafId := "L017_heat_kernel_existence",
    packageId := "P04.02_heat_kernel_existence",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "HeatSemigroupKernelPackage.heatKernel boundary",
    nextAction := "Prove kernel existence/regularity and that the kernel represents the semigroup for positive time." },
  { leafId := "L018_supertrace_definition",
    packageId := "P04.03_supertrace",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "HeatSupertracePackage.supertrace_eq_trace_sub and matrixSupertrace wrappers",
    nextAction := "Replace scalar trace placeholders by trace-class operators or a validated finite trace surrogate." },
  { leafId := "L019_mckean_singer_identity",
    packageId := "P04.04_mckean_singer",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "RealMcKeanSingerIdentityPackage.apply_supertrace_eq_index boundary",
    nextAction := "Prove positive-time supertrace constancy and identify the value with the Fredholm analytic index." },
  { leafId := "L020_small_time_asymptotics",
    packageId := "P04.05_small_time_asymptotics",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "HeatKernelIndexData.hasHeatKernelParametrix boundary",
    nextAction := "Formalize the heat-kernel parametrix and asymptotic coefficient extraction." },
  { leafId := "L021_local_index_density",
    packageId := "P06.01_local_density_extraction",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "CharacteristicClassLocalIndexDensityAPI.localIndexDensity",
    nextAction := "Define the local density coefficient produced by the small-time expansion and expose the Todd/A-hat branch selector." },
  { leafId := "L022_characteristic_class_api",
    packageId := "P05.01_characteristic_classes",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "CharacteristicClassLocalIndexDensityAPI Chern/Todd/A-hat fields",
    nextAction := "Import or build Chern character, Todd class, A-hat class, and multiplicative product laws for the selected cohomology target." },
  { leafId := "L023_fundamental_class_pairing",
    packageId := "P05.02_fundamental_class_pairing",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "CharacteristicClassLocalIndexDensityAPI.cohomologyPairing",
    nextAction := "Connect compact oriented manifold integration or fundamental-class cap pairing to the cohomology target." },
  { leafId := "L024_density_equals_characteristic_form",
    packageId := "P06.02_density_characteristic_identification",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "toddLocalIndexDensity_eq and aHatLocalIndexDensity_eq",
    nextAction := "Prove that the heat asymptotic local coefficient equals the selected characteristic-class expression." },
  { leafId := "L025_global_pairing_equals_topological_index",
    packageId := "P07.01_topological_index_pairing",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "topologicalIndex_eq_pairing and branch-specific pairing wrappers",
    nextAction := "Identify the integrated local density with the chosen topological index definition." },
  { leafId := "L026_analytic_equals_topological",
    packageId := "P07.02_terminal_assembly",
    status := .unchecked,
    stepBudget := 100,
    budgetClosed := false,
    repoLocalAnchor := "statementShape_apply",
    nextAction := "Assemble ellipticity, McKean-Singer, local density, and pairing packages into the terminal equality." }
]

/-- The child split covers exactly leaves `L010` through `L026`. -/
theorem uncheckedLeafLedgersL010ToL026_length :
    uncheckedLeafLedgersL010ToL026.length = 17 :=
  rfl

/-- Every newly split child leaf has the required local `<= 100` step budget. -/
theorem uncheckedLeafLedgersL010ToL026_budgetList :
    uncheckedLeafLedgersL010ToL026.map (fun L => L.stepBudget) =
      [100, 100, 100, 100, 100, 100, 100, 100, 100,
        100, 100, 100, 100, 100, 100, 100, 100] :=
  rfl

/-- No `L010` through `L026` package is counted as budget-closed in this artifact. -/
theorem uncheckedLeafLedgersL010ToL026_budgetClosedList :
    uncheckedLeafLedgersL010ToL026.map (fun L => L.budgetClosed) =
      [false, false, false, false, false, false, false, false, false,
        false, false, false, false, false, false, false, false] :=
  rfl

end S1_M_113
end Stage1
end AwesomeTheorems
