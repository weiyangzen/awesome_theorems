import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.Calculus.Conformal.NormedSpace
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Orientation
import Mathlib.LinearAlgebra.Projectivization.Basic

/-!
# S1-M-183 / THM-M-1542: Ward correspondence

This Stage1 artifact records a conservative Lean 4 statement boundary for the
twistor correspondence with self-dual Yang-Mills fields.

The current pinned mathlib snapshot has useful manifold, vector-bundle,
covariant-derivative, complex-manifold, smooth-section, continuous-linear-map,
and Hilbert-space infrastructure.  It does not expose a terminal theorem for
twistor spaces, holomorphic vector bundles on twistor lines, gauge-theoretic
connections with curvature two-forms, Hodge star on four-manifolds, or the Ward
correspondence itself.

Accordingly this file provides a precise proposition-level interface and small
checked wrappers around the available mathematical substrate.  It does not
claim a proof of the Ward correspondence.
-/

noncomputable section

open Set
open scoped Manifold ContDiff

universe uEB uET uM uZ uG uConn uCurv uTw uE uF uH

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_183

/-- The checked point-set model used for a Riemann-sphere twistor line boundary. -/
abbrev ComplexProjectiveLine : Type :=
  Projectivization ℂ (Fin 2 → ℂ)

/--
The concrete unbundled two-form substrate currently available for an
adjoint-valued curvature boundary.

This is a normed-vector-space differential form
`E -> E [⋀^Fin 2]→L[ℝ] Ad`.  It is not yet a smooth adjoint-bundle-valued
curvature two-form over a principal bundle on a four-manifold.
-/
abbrev UnbundledAdjointValuedTwoForm
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ad : Type uCurv) [NormedAddCommGroup Ad] [NormedSpace ℝ Ad] :
    Type (max uE uCurv) :=
  E → E [⋀^Fin 2]→L[ℝ] Ad

/-- The checked unbundled two-form carrier used by the four-dimensional Hodge-star split. -/
abbrev FourDimensionalTwoForm
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (V : Type uCurv) [NormedAddCommGroup V] [NormedSpace ℝ V] :
    Type (max uE uCurv) :=
  E [⋀^Fin 2]→L[ℝ] V

/--
Repo-local boundary for the concrete Hodge-star operator on two-forms in real
dimension four.

The carrier is no longer an arbitrary `Curv`: it is the checked mathlib
continuous alternating two-form type.  The operator is still supplied as a
continuous linear map, because the pinned local mathlib closure does not yet
construct Hodge star from a Riemannian metric, orientation, and volume form on
a smooth four-manifold or adjoint bundle.
-/
structure FourDimensionalTwoFormHodgeStar
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (V : Type uCurv) [NormedAddCommGroup V] [NormedSpace ℝ V] :
    Type (max uE uCurv) where
  dimension_eq_four : Module.finrank ℝ E = 4
  star : FourDimensionalTwoForm E V →L[ℝ] FourDimensionalTwoForm E V
  star_square : ∀ F : FourDimensionalTwoForm E V, star (star F) = F

/--
Concrete Stage1 twistor fibration boundary.

The base is now expressed through mathlib's smooth real-manifold, orientation,
finite-dimensional, and conformal-map APIs.  The twistor carrier is expressed as
a complex manifold with a real-smooth projection to the base and with twistor
lines parameterized by the checked `Projectivization ℂ (Fin 2 → ℂ)` model of a
complex projective line.

This is still not a terminal twistor-space construction: mathlib does not yet
provide a bundled Ward twistor fibration, so the line family and conformal
transition family are explicit data in the boundary.
-/
structure TwistorFibrationBoundary
    (EBase : Type uEB) (ETwistor : Type uET) (M : Type uM) (Z : Type uZ)
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z] :
    Type (max (max uEB uET) (max uM uZ)) where
  baseIsSmoothManifold : IsManifold 𝓘(ℝ, EBase) ∞ M
  baseModelFiniteDimensional : FiniteDimensional ℝ EBase
  baseDimension_eq_four : Module.finrank ℝ EBase = 4
  baseOrientation : Orientation ℝ EBase (Fin 4)
  baseConformalTransition : Set (EBase → EBase)
  baseConformalTransition_conformal :
    ∀ f : EBase → EBase, f ∈ baseConformalTransition → Conformal f
  twistorIsComplexManifold : IsManifold 𝓘(ℂ, ETwistor) ∞ Z
  projection : Z → M
  projectionSmooth : MDifferentiable 𝓘(ℝ, ETwistor) 𝓘(ℝ, EBase) projection
  twistorLine : M → Set Z
  twistorLineParam : M → ComplexProjectiveLine → Z
  twistorLineParam_range :
    ∀ x : M, Set.range (twistorLineParam x) = twistorLine x
  realStructure : Z ≃ₜ Z
  realStructure_involutive : Function.Involutive realStructure

namespace TwistorFibrationBoundary

theorem base_dimension
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (T : TwistorFibrationBoundary EBase ETwistor M Z) :
    Module.finrank ℝ EBase = 4 :=
  T.baseDimension_eq_four

theorem projection_smooth
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (T : TwistorFibrationBoundary EBase ETwistor M Z) :
    MDifferentiable 𝓘(ℝ, ETwistor) 𝓘(ℝ, EBase) T.projection :=
  T.projectionSmooth

theorem conformal_transition
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (T : TwistorFibrationBoundary EBase ETwistor M Z)
    {f : EBase → EBase} (hf : f ∈ T.baseConformalTransition) :
    Conformal f :=
  T.baseConformalTransition_conformal f hf

theorem twistorLineParam_surjective
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (T : TwistorFibrationBoundary EBase ETwistor M Z) (x : M) :
    Set.range (T.twistorLineParam x) = T.twistorLine x :=
  T.twistorLineParam_range x

theorem realStructure_apply_apply
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (T : TwistorFibrationBoundary EBase ETwistor M Z) (z : Z) :
    T.realStructure (T.realStructure z) = z :=
  T.realStructure_involutive z

end TwistorFibrationBoundary

/-- Self-duality for an abstract curvature value and an abstract Hodge star. -/
def IsSelfDual {Curv : Type uCurv} [AddGroup Curv]
    (hodgeStar : Curv → Curv) (F : Curv) : Prop :=
  hodgeStar F = F

/-- The self-dual predicate unfolds to the expected Hodge-star equation. -/
theorem isSelfDual_iff {Curv : Type uCurv} [AddGroup Curv]
    (hodgeStar : Curv → Curv) (F : Curv) :
    IsSelfDual hodgeStar F ↔ hodgeStar F = F :=
  Iff.rfl

/-- If the abstract Hodge star preserves zero, then zero curvature is self-dual. -/
theorem isSelfDual_zero {Curv : Type uCurv} [AddGroup Curv]
    (hodgeStar : Curv → Curv) (hzero : hodgeStar 0 = 0) :
    IsSelfDual hodgeStar (0 : Curv) := by
  simp [IsSelfDual, hzero]

/--
Self-duality specialized to the checked four-dimensional two-form carrier.

This is the child C004 bridge from the concrete two-form Hodge-star boundary to
the existing abstract `IsSelfDual` predicate used by the Ward-correspondence
statement shape.
-/
def IsSelfDualFourDimensionalTwoForm
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {V : Type uCurv} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (H : FourDimensionalTwoFormHodgeStar E V) (F : FourDimensionalTwoForm E V) :
    Prop :=
  IsSelfDual (fun F' => H.star F') F

/-- The specialized four-dimensional predicate unfolds to the Hodge-star equation. -/
theorem isSelfDualFourDimensionalTwoForm_iff
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {V : Type uCurv} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (H : FourDimensionalTwoFormHodgeStar E V) (F : FourDimensionalTwoForm E V) :
    IsSelfDualFourDimensionalTwoForm H F ↔ H.star F = F :=
  Iff.rfl

/-- The supplied four-dimensional Hodge star is involutive on the checked two-form carrier. -/
theorem fourDimensionalTwoFormHodgeStar_square
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {V : Type uCurv} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (H : FourDimensionalTwoFormHodgeStar E V) (F : FourDimensionalTwoForm E V) :
    H.star (H.star F) = F :=
  H.star_square F

/-- Zero is self-dual for every supplied four-dimensional two-form Hodge star. -/
theorem isSelfDualFourDimensionalTwoForm_zero
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {V : Type uCurv} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (H : FourDimensionalTwoFormHodgeStar E V) :
    IsSelfDualFourDimensionalTwoForm H (0 : FourDimensionalTwoForm E V) := by
  simp [IsSelfDualFourDimensionalTwoForm, IsSelfDual]

/--
Abstract sign-convention boundary for the standard implication
`self-dual curvature -> Yang-Mills equation`.

In the geometric proof, the Bianchi identity gives `d_A F_A = 0`, while the
chosen four-dimensional Hodge-star/sign convention identifies the Yang-Mills
operator with the same covariant exterior derivative when `*F_A = F_A`.  The
current repo-local dependency closure does not yet expose the concrete
principal-bundle connection, adjoint-valued curvature, covariant exterior
derivative, or codifferential APIs needed to instantiate this structure.
-/
structure SelfDualYangMillsSignConvention
    (Conn : Type uConn) (Curv : Type uCurv) [AddGroup Curv] :
    Type (max uConn uCurv) where
  curvature : Conn → Curv
  hodgeStar : Curv → Curv
  hodgeStar_square : ∀ F : Curv, hodgeStar (hodgeStar F) = F
  covariantExteriorDerivative : Conn → Curv → Curv
  yangMillsOperator : Conn → Curv
  bianchiIdentity :
    ∀ A : Conn, covariantExteriorDerivative A (curvature A) = 0
  selfDual_yangMillsOperator_eq_bianchi :
    ∀ A : Conn, IsSelfDual hodgeStar (curvature A) →
      yangMillsOperator A = covariantExteriorDerivative A (curvature A)
  yangMillsEquation : Conn → Prop
  yangMillsEquation_iff_operator_zero :
    ∀ A : Conn, yangMillsEquation A ↔ yangMillsOperator A = 0

/--
Checked Stage1 C005 lemma boundary: under the explicit Bianchi/sign-convention
interface, self-dual curvature implies the Yang-Mills equation.

This is not yet the geometric theorem for smooth principal connections; it is
the repo-local proof skeleton that the future geometric APIs must instantiate.
-/
theorem yangMills_of_isSelfDualCurvature
    {Conn : Type uConn} {Curv : Type uCurv} [AddGroup Curv]
    (D : SelfDualYangMillsSignConvention Conn Curv) {A : Conn}
    (hA : IsSelfDual D.hodgeStar (D.curvature A)) :
    D.yangMillsEquation A := by
  rw [D.yangMillsEquation_iff_operator_zero]
  rw [D.selfDual_yangMillsOperator_eq_bianchi A hA]
  exact D.bianchiIdentity A

/-- Gauge equivalence of two connections under a mathlib multiplicative action. -/
def GaugeEquivalent {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A B : Conn) : Prop :=
  ∃ g : G, g • A = B

/-- Gauge equivalence is reflexive. -/
theorem gaugeEquivalent_refl {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A : Conn) :
    GaugeEquivalent (G := G) A A := by
  exact ⟨1, by simp⟩

/-- The gauge orbit of a connection under a mathlib multiplicative action. -/
def gaugeOrbit {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A : Conn) : Set Conn :=
  {B | GaugeEquivalent (G := G) A B}

/-- Membership in the gauge orbit is exactly gauge equivalence. -/
theorem mem_gaugeOrbit_iff {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] {A B : Conn} :
    B ∈ gaugeOrbit (G := G) A ↔ GaugeEquivalent (G := G) A B :=
  Iff.rfl

/-- Every connection lies in its own gauge orbit. -/
theorem mem_gaugeOrbit_self {G : Type uG} {Conn : Type uConn}
    [Group G] [MulAction G Conn] (A : Conn) :
    A ∈ gaugeOrbit (G := G) A :=
  gaugeEquivalent_refl A

/--
Abstract Yang-Mills side of the correspondence.

The concrete future target is a connection on a principal bundle over a
four-manifold, with curvature an adjoint-valued two-form and Hodge star from the
oriented conformal structure.  Those APIs are not terminal in the current local
Lean closure, so they remain explicit fields here.
-/
structure SelfDualYangMillsData
    (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv)
    [Group G] [MulAction G Conn] [AddGroup Curv] :
    Type (max (max uG uConn) uCurv) where
  connectionRegularity : Conn → Prop
  curvature : Conn → Curv
  hodgeStar : Curv → Curv
  hodgeStar_square : ∀ F : Curv, hodgeStar (hodgeStar F) = F
  gaugeActionPreservesRegularity : Prop
  curvatureGaugeEquivariance : Prop
  yangMillsEquation : Conn → Prop
  selfDualImpliesYangMills : ∀ A : Conn, IsSelfDual hodgeStar (curvature A) → yangMillsEquation A

/-- The set of regular self-dual Yang-Mills connections in the abstract model. -/
def selfDualConnectionSet
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : SelfDualYangMillsData G Conn Curv) : Set Conn :=
  {A | D.connectionRegularity A ∧ IsSelfDual D.hodgeStar (D.curvature A)}

/-- Membership unfolds to regularity plus self-dual curvature. -/
theorem mem_selfDualConnectionSet_iff
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : SelfDualYangMillsData G Conn Curv) {A : Conn} :
    A ∈ selfDualConnectionSet D ↔
      D.connectionRegularity A ∧ IsSelfDual D.hodgeStar (D.curvature A) :=
  Iff.rfl

/-- A self-dual connection satisfies the abstract Yang-Mills equation field. -/
theorem yangMills_of_mem_selfDualConnectionSet
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : SelfDualYangMillsData G Conn Curv) {A : Conn}
    (hA : A ∈ selfDualConnectionSet D) :
    D.yangMillsEquation A :=
  D.selfDualImpliesYangMills A hA.2

/--
Build the abstract Yang-Mills side from the explicit C005 sign-convention
boundary, leaving gauge-invariance laws as caller-supplied propositions.
-/
def SelfDualYangMillsSignConvention.toSelfDualYangMillsData
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : SelfDualYangMillsSignConvention Conn Curv)
    (connectionRegularity : Conn → Prop)
    (gaugeActionPreservesRegularity curvatureGaugeEquivariance : Prop) :
    SelfDualYangMillsData G Conn Curv where
  connectionRegularity := connectionRegularity
  curvature := D.curvature
  hodgeStar := D.hodgeStar
  hodgeStar_square := D.hodgeStar_square
  gaugeActionPreservesRegularity := gaugeActionPreservesRegularity
  curvatureGaugeEquivariance := curvatureGaugeEquivariance
  yangMillsEquation := D.yangMillsEquation
  selfDualImpliesYangMills := fun _ hA => yangMills_of_isSelfDualCurvature D hA

/--
Boundary for holomorphic vector bundles on the Ward twistor space.

The concrete future target is a holomorphic vector bundle over `Z`, trivial on
every twistor line `CP^1 -> Z`, equipped with a real-structure compatibility
isomorphism over the involution on twistor space.  The current local mathlib
closure has complex manifolds and vector bundles, but not holomorphic vector
bundles or pullback/isomorphism APIs specialized to the Ward twistor setting, so
those predicates and equivalence data remain explicit.
-/
structure HolomorphicTwistorBundleBoundary
    (EBase : Type uEB) (ETwistor : Type uET) (M : Type uM) (Z : Type uZ)
    (TwBundle : Type uTw)
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z] :
    Type (max (max (max uEB uET) (max uM uZ)) uTw) where
  twistorGeometry : TwistorFibrationBoundary EBase ETwistor M Z
  holomorphicVectorBundle : TwBundle → Prop
  trivialOnTwistorLine : TwBundle → M → Prop
  trivialOnTwistorLines : TwBundle → Prop
  trivialOnTwistorLines_iff :
    ∀ E : TwBundle, trivialOnTwistorLines E ↔ ∀ x : M, trivialOnTwistorLine E x
  realPullback : TwBundle → TwBundle
  realPullback_involutive : Function.Involutive realPullback
  realStructureIsomorphism : TwBundle → TwBundle → Prop
  realStructureCondition : TwBundle → Prop
  realStructureCondition_iff :
    ∀ E : TwBundle, realStructureCondition E ↔ realStructureIsomorphism (realPullback E) E

namespace HolomorphicTwistorBundleBoundary

/-- Admissible twistor bundles satisfy holomorphicity, line triviality, and the real condition. -/
def admissible
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (B : HolomorphicTwistorBundleBoundary EBase ETwistor M Z TwBundle)
    (E : TwBundle) : Prop :=
  B.holomorphicVectorBundle E ∧ B.trivialOnTwistorLines E ∧ B.realStructureCondition E

/-- The admissibility predicate unfolds to the three Ward twistor-bundle conditions. -/
theorem admissible_iff
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (B : HolomorphicTwistorBundleBoundary EBase ETwistor M Z TwBundle) (E : TwBundle) :
    B.admissible E ↔
      B.holomorphicVectorBundle E ∧ B.trivialOnTwistorLines E ∧
        B.realStructureCondition E :=
  Iff.rfl

/-- Triviality on all twistor lines gives triviality on any selected line. -/
theorem trivialOnTwistorLine_of_trivialOnTwistorLines
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (B : HolomorphicTwistorBundleBoundary EBase ETwistor M Z TwBundle)
    {E : TwBundle} (hE : B.trivialOnTwistorLines E) (x : M) :
    B.trivialOnTwistorLine E x :=
  (B.trivialOnTwistorLines_iff E).1 hE x

/-- The real-structure condition unfolds to compatibility with the real pullback. -/
theorem realStructureCondition_unfold
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (B : HolomorphicTwistorBundleBoundary EBase ETwistor M Z TwBundle) (E : TwBundle) :
    B.realStructureCondition E ↔ B.realStructureIsomorphism (B.realPullback E) E :=
  B.realStructureCondition_iff E

/-- The abstract real pullback on twistor bundles is involutive. -/
theorem realPullback_apply_apply
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    (B : HolomorphicTwistorBundleBoundary EBase ETwistor M Z TwBundle) (E : TwBundle) :
    B.realPullback (B.realPullback E) = E :=
  B.realPullback_involutive E

end HolomorphicTwistorBundleBoundary

/--
Input data for a Ward-correspondence theorem.

`TwBundle` represents the holomorphic vector bundles on twistor space.  Their
holomorphicity, triviality on twistor lines, and real-structure condition are
now grouped in `HolomorphicTwistorBundleBoundary`.  A later terminal
formalization should replace those boundary fields by concrete holomorphic
bundle, sheaf-cohomology, and Penrose-transform APIs.
-/
structure WardCorrespondenceData
    (EBase : Type uEB) (ETwistor : Type uET) (M : Type uM) (Z : Type uZ)
    (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv) (TwBundle : Type uTw)
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv] :
    Type (max (max (max (max uEB uET) (max uM uZ)) (max uG uConn)) (max uCurv uTw)) where
  twistorBundles : HolomorphicTwistorBundleBoundary EBase ETwistor M Z TwBundle
  gaugeTheory : SelfDualYangMillsData G Conn Curv
  stabilityOrFramingCondition : TwBundle → Prop
  admissibleConnection : Conn → Prop
  admissibleConnection_iff :
    ∀ A : Conn, admissibleConnection A ↔ A ∈ selfDualConnectionSet gaugeTheory
  twistorTransformRegularity : Prop
  penroseWardTransformHypotheses : Prop

namespace WardCorrespondenceData

/-- Recover the twistor fibration boundary from the bundled twistor-bundle boundary. -/
def twistorGeometry
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) :
    TwistorFibrationBoundary EBase ETwistor M Z :=
  D.twistorBundles.twistorGeometry

/-- Holomorphicity predicate for the twistor-bundle side of Ward correspondence. -/
def holomorphicVectorBundle
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) :
    TwBundle → Prop :=
  D.twistorBundles.holomorphicVectorBundle

/-- Triviality-on-every-twistor-line predicate for the twistor-bundle side. -/
def trivialOnTwistorLines
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) :
    TwBundle → Prop :=
  D.twistorBundles.trivialOnTwistorLines

/-- Real-structure condition for the twistor-bundle side. -/
def realStructureCondition
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) :
    TwBundle → Prop :=
  D.twistorBundles.realStructureCondition

/-- The three twistor-bundle Ward-side conditions bundled as a single predicate. -/
def admissibleHolomorphicTwistorBundle
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle)
    (E : TwBundle) : Prop :=
  D.twistorBundles.admissible E

/-- The Ward-side admissibility predicate unfolds to holomorphicity, line triviality, and reality. -/
theorem admissibleHolomorphicTwistorBundle_iff
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) (E : TwBundle) :
    D.admissibleHolomorphicTwistorBundle E ↔
      D.holomorphicVectorBundle E ∧ D.trivialOnTwistorLines E ∧
        D.realStructureCondition E :=
  Iff.rfl

end WardCorrespondenceData

/--
Named Stage1 boundary for the Penrose-Ward transform and inverse transform.

The transform from an admissible holomorphic twistor bundle to a self-dual
connection and the inverse transform from a self-dual connection to an
admissible holomorphic twistor bundle are explicit functions here.  The
inverse-on-quotients, gauge-compatibility, and holomorphic-structure
compatibility laws remain proposition fields because the current local closure
does not yet provide concrete moduli stacks, gauge quotients, holomorphic
bundle isomorphism classes, or sheaf-cohomological Penrose-transform
construction APIs.
-/
structure PenroseWardTransformBoundary
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) :
    Type (max uConn uTw) where
  penroseWardTransform : TwBundle → Conn
  inversePenroseWardTransform : Conn → TwBundle
  penroseWardTransform_maps_admissible :
    ∀ E : TwBundle,
      D.admissibleHolomorphicTwistorBundle E →
        D.stabilityOrFramingCondition E →
          penroseWardTransform E ∈ selfDualConnectionSet D.gaugeTheory
  inversePenroseWardTransform_maps_selfDual :
    ∀ A : Conn,
      A ∈ selfDualConnectionSet D.gaugeTheory →
        D.admissibleHolomorphicTwistorBundle (inversePenroseWardTransform A)
  inverseOnAdmissibleTwistorBundles : Prop
  inverseOnSelfDualGaugeClasses : Prop
  gaugeEquivCompatible : Prop
  holomorphicStructureCompatible : Prop

namespace PenroseWardTransformBoundary

/-- The Penrose-Ward transform sends admissible twistor bundles to self-dual curvature. -/
theorem penroseWardTransform_selfDual
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    {D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle}
    (W : PenroseWardTransformBoundary D) (E : TwBundle)
    (hE : D.admissibleHolomorphicTwistorBundle E)
    (hF : D.stabilityOrFramingCondition E) :
    IsSelfDual D.gaugeTheory.hodgeStar
      (D.gaugeTheory.curvature (W.penroseWardTransform E)) :=
  (W.penroseWardTransform_maps_admissible E hE hF).2

/-- The inverse Penrose-Ward transform returns a holomorphic twistor bundle. -/
theorem inversePenroseWardTransform_holomorphic
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    {D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle}
    (W : PenroseWardTransformBoundary D) {A : Conn}
    (hA : A ∈ selfDualConnectionSet D.gaugeTheory) :
    D.holomorphicVectorBundle (W.inversePenroseWardTransform A) :=
  (D.admissibleHolomorphicTwistorBundle_iff (W.inversePenroseWardTransform A)).1
    (W.inversePenroseWardTransform_maps_selfDual A hA) |>.1

/-- The inverse Penrose-Ward transform is trivial on all twistor lines. -/
theorem inversePenroseWardTransform_trivialOnTwistorLines
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    {D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle}
    (W : PenroseWardTransformBoundary D) {A : Conn}
    (hA : A ∈ selfDualConnectionSet D.gaugeTheory) :
    D.trivialOnTwistorLines (W.inversePenroseWardTransform A) :=
  ((D.admissibleHolomorphicTwistorBundle_iff (W.inversePenroseWardTransform A)).1
    (W.inversePenroseWardTransform_maps_selfDual A hA)).2.1

/-- The inverse Penrose-Ward transform satisfies the real-structure condition. -/
theorem inversePenroseWardTransform_realStructureCondition
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    {D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle}
    (W : PenroseWardTransformBoundary D) {A : Conn}
    (hA : A ∈ selfDualConnectionSet D.gaugeTheory) :
    D.realStructureCondition (W.inversePenroseWardTransform A) :=
  ((D.admissibleHolomorphicTwistorBundle_iff (W.inversePenroseWardTransform A)).1
    (W.inversePenroseWardTransform_maps_selfDual A hA)).2.2

end PenroseWardTransformBoundary

/--
Output contract for a Ward correspondence.

The transforms are bundled as functions, while inverse, gauge, and holomorphic
compatibility are kept as proposition fields because the concrete categories
and equivalence relation are not yet fixed in mathlib.
-/
structure WardCorrespondence
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) :
    Type (max (max uConn uCurv) uTw) where
  toConnection : TwBundle → Conn
  toTwistorBundle : Conn → TwBundle
  twistor_to_selfDual :
    ∀ E : TwBundle,
      D.holomorphicVectorBundle E →
        D.trivialOnTwistorLines E →
          D.realStructureCondition E →
            D.stabilityOrFramingCondition E →
              toConnection E ∈ selfDualConnectionSet D.gaugeTheory
  selfDual_to_twistor :
    ∀ A : Conn,
      A ∈ selfDualConnectionSet D.gaugeTheory →
        D.holomorphicVectorBundle (toTwistorBundle A) ∧
          D.trivialOnTwistorLines (toTwistorBundle A) ∧
            D.realStructureCondition (toTwistorBundle A)
  inverseOnTwistorBundles : Prop
  inverseOnGaugeClasses : Prop
  gaugeEquivCompatible : Prop
  holomorphicStructureCompatible : Prop

/--
Package an existing Ward-correspondence contract as the named C007
Penrose-Ward transform boundary.
-/
def WardCorrespondence.toPenroseWardTransformBoundary
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    {D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle}
    (W : WardCorrespondence D) : PenroseWardTransformBoundary D where
  penroseWardTransform := W.toConnection
  inversePenroseWardTransform := W.toTwistorBundle
  penroseWardTransform_maps_admissible := by
    intro E hE hF
    exact W.twistor_to_selfDual E hE.1 hE.2.1 hE.2.2 hF
  inversePenroseWardTransform_maps_selfDual := by
    intro A hA
    exact (D.admissibleHolomorphicTwistorBundle_iff (W.toTwistorBundle A)).2
      (W.selfDual_to_twistor A hA)
  inverseOnAdmissibleTwistorBundles := W.inverseOnTwistorBundles
  inverseOnSelfDualGaugeClasses := W.inverseOnGaugeClasses
  gaugeEquivCompatible := W.gaugeEquivCompatible
  holomorphicStructureCompatible := W.holomorphicStructureCompatible

/-- Projection wrapper: the Ward transform from twistor data gives self-dual curvature. -/
theorem WardCorrespondence.toConnection_selfDual
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    {D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle}
    (W : WardCorrespondence D) (E : TwBundle)
    (hE : D.holomorphicVectorBundle E)
    (hT : D.trivialOnTwistorLines E)
    (hR : D.realStructureCondition E)
    (hF : D.stabilityOrFramingCondition E) :
    IsSelfDual D.gaugeTheory.hodgeStar (D.gaugeTheory.curvature (W.toConnection E)) :=
  (W.twistor_to_selfDual E hE hT hR hF).2

/-- Projection wrapper: a self-dual connection gives a holomorphic twistor bundle. -/
theorem WardCorrespondence.toTwistorBundle_holomorphic
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    {D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle}
    (W : WardCorrespondence D) {A : Conn}
    (hA : A ∈ selfDualConnectionSet D.gaugeTheory) :
    D.holomorphicVectorBundle (W.toTwistorBundle A) :=
  (W.selfDual_to_twistor A hA).1

/--
Formula-level statement shape for the Ward correspondence.

For every normalized twistor-gauge input satisfying the twistor-geometry,
holomorphicity, and transform hypotheses, there should be a correspondence
between admissible holomorphic twistor bundles and self-dual Yang-Mills
connections.  This is a statement shape, not a terminal proof.
-/
def WardCorrespondenceTheorem
    {EBase : Type uEB} {ETwistor : Type uET} {M : Type uM} {Z : Type uZ}
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv} {TwBundle : Type uTw}
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle) :
    Prop :=
  D.gaugeTheory.gaugeActionPreservesRegularity →
  D.gaugeTheory.curvatureGaugeEquivariance →
  D.twistorTransformRegularity →
  D.penroseWardTransformHypotheses →
    Nonempty (WardCorrespondence D)

/--
Stage1 statement-shape candidate for THM-M-1542.

The theorem quantifies over explicit universes, carrier types, topology,
group-action data, curvature values, and abstract twistor-bundle objects.
-/
def StatementShape : Prop :=
  ∀ (EBase : Type uEB) (ETwistor : Type uET) (M : Type uM) (Z : Type uZ)
    (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv) (TwBundle : Type uTw)
    [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
    [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
    [TopologicalSpace M] [TopologicalSpace Z]
    [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
    [Group G] [MulAction G Conn] [AddGroup Curv],
      ∀ D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle,
        WardCorrespondenceTheorem D

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (EBase : Type uEB) (ETwistor : Type uET) (M : Type uM) (Z : Type uZ)
      (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv) (TwBundle : Type uTw)
      [NormedAddCommGroup EBase] [NormedSpace ℝ EBase]
      [NormedAddCommGroup ETwistor] [NormedSpace ℂ ETwistor] [NormedSpace ℝ ETwistor]
      [TopologicalSpace M] [TopologicalSpace Z]
      [ChartedSpace EBase M] [ChartedSpace ETwistor Z]
      [Group G] [MulAction G Conn] [AddGroup Curv],
        ∀ D : WardCorrespondenceData EBase ETwistor M Z G Conn Curv TwBundle,
          WardCorrespondenceTheorem D) :
    StatementShape.{uEB, uET, uM, uZ, uG, uConn, uCurv, uTw} :=
  h

/--
Repo-local C003 audit record for principal-bundle and curvature APIs.

This is evidence for keeping the Ward gauge-theory fields abstract.  The
checked mathlib closure supplies topological/vector bundles, Lie-group
manifolds, covariant derivatives on vector bundles, and unbundled normed-space
two-forms.  It does not yet supply the principal-bundle gauge-theory stack
needed to instantiate the Ward correspondence.
-/
structure GaugeCurvatureAPIAudit where
  childTask : String
  mathlibRevision : String
  availableConcreteSubstrate : String
  checkedMathlibModules : List String
  checkedNames : List String
  exactAbsences : List String
  replacementDecision : String
  validationTarget : String
deriving Repr

/-- Repo-local C004 audit record for the four-dimensional Hodge-star split. -/
structure HodgeStarAPIAudit where
  childTask : String
  mathlibRevision : String
  concreteCarrier : String
  checkedNames : List String
  exactAbsences : List String
  replacementDecision : String
  validationTarget : String
deriving Repr

/-- Repo-local C005 audit record for the self-dual-curvature to Yang-Mills implication. -/
structure SelfDualYangMillsLemmaAudit where
  childTask : String
  mathlibRevision : String
  checkedBoundary : String
  checkedNames : List String
  exactAbsences : List String
  replacementDecision : String
  validationTarget : String
deriving Repr

/-- Repo-local C006 audit record for the holomorphic twistor-bundle boundary. -/
structure HolomorphicTwistorBundleAPIAudit where
  childTask : String
  mathlibRevision : String
  checkedBoundary : String
  checkedNames : List String
  exactAbsences : List String
  replacementDecision : String
  validationTarget : String
deriving Repr

/-- Repo-local C007 audit record for the Penrose-Ward transform boundary. -/
structure PenroseWardTransformAPIAudit where
  childTask : String
  mathlibRevision : String
  checkedBoundary : String
  checkedNames : List String
  exactMissingTheoremFamily : List String
  debtClassification : String
  replacementDecision : String
  validationTarget : String
deriving Repr

/-- Repo-local C009 synchronization gate for keeping the public checklist open. -/
structure Stage1SynchronizationGate where
  childTask : String
  checkedArtifact : String
  validationCommand : String
  theoremTreeLedger : String
  publicMergeSurface : String
  localLeanStatus : String
  theoremCompletionStatus : String
  repoLocalIntegrationDebtGate : String
  remainingOpenLeaves : List String
  publicBackfillDecision : String
deriving Repr

/-- Machine-readable row for the C008 external Ward-correspondence source audit. -/
structure ExternalWardLeanAuditCandidate where
  repository : String
  commit : String
  toolchain : String
  moduleOrSearchScope : String
  matchedTerms : List String
  relevantNames : List String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  closureStatus : String
  terminalWardTheoremFound : Bool
deriving Repr

/--
C003 decision: keep the gauge-theory side abstract until the missing
principal-bundle curvature APIs exist locally or are imported from a checked
dependency.
-/
def gaugeCurvatureAPIAudit : GaugeCurvatureAPIAudit := {
  childTask := "S1-M-183-C003",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  availableConcreteSubstrate :=
    "FiberBundle, VectorBundle, LieGroup, CovariantDerivative, IsCovariantDerivativeOn, " ++
    "CovariantDerivative.difference, and UnbundledAdjointValuedTwoForm E Ad = " ++
    "E -> E [⋀^Fin 2]→L[ℝ] Ad",
  checkedMathlibModules := [
    "Mathlib.Topology.FiberBundle.Basic",
    "Mathlib.Geometry.Manifold.VectorBundle.Basic",
    "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
    "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
    "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
    "Mathlib.Geometry.Manifold.Algebra.LieGroup",
    "Mathlib.Analysis.Calculus.DifferentialForm.Basic"
  ],
  checkedNames := [
    "FiberBundle",
    "VectorBundle",
    "LieGroup",
    "CovariantDerivative",
    "IsCovariantDerivativeOn",
    "CovariantDerivative.ContMDiffCovariantDerivative",
    "CovariantDerivative.difference",
    "UnbundledAdjointValuedTwoForm",
    "extDeriv"
  ],
  exactAbsences := [
    "no PrincipalBundle declaration or principal-bundle module in the pinned local mathlib tree",
    "no gauge-group bundle automorphism API for principal bundles",
    "no smooth principal connection or Ehresmann connection API with curvature",
    "no adjoint bundle API for a principal bundle representation",
    "no smooth manifold-valued adjoint-bundle curvature two-form API",
    "no terminal Yang-Mills or self-dual Yang-Mills theorem",
    "no Ward, Penrose-Ward, twistor Yang-Mills, or self-dual curvature correspondence theorem"
  ],
  replacementDecision :=
    "blocked: SelfDualYangMillsData keeps Conn, Curv, curvature, hodgeStar, " ++
    "gauge equivariance, and selfDualImpliesYangMills abstract until a concrete " ++
    "principal-bundle/adjoint-curvature stack is available or imported",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_183.lean"
}

/-- Exact search terms requested by the C008 external Ward-correspondence audit. -/
def externalWardAuditSearchTerms : List String := [
  "Ward correspondence",
  "WardCorrespondence",
  "Penrose-Ward",
  "PenroseWard",
  "Penrose Ward",
  "self-dual Yang-Mills",
  "self dual Yang-Mills",
  "SelfDualYangMills",
  "YangMills",
  "Yang-Mills",
  "SDYM",
  "twistor",
  "Twistor",
  "trivialOnTwistorLines"
]

/--
Authentication status for the C008 GitHub source-search channel.

On 2026-05-01 in this worker environment, `gh auth status` reported no logged
in GitHub host, no `GH_TOKEN`/`GITHUB_TOKEN`-style environment token was
present, `gh search` refused to run, and GitHub REST code search returned
`Requires authentication`.  The rows below therefore record refreshed
primary-source repository inspection, not a completed authenticated GitHub code
search closure.
-/
def externalWardAuditAuthenticationStatus : String :=
  "blocked: no authenticated GitHub session was available to this worker on " ++
  "2026-05-01; gh search could not run and GitHub REST code search returned " ++
  "Requires authentication"

/--
Primary-source Lean 4 rows refreshed for the external Ward-correspondence audit.

These rows are evidence metadata only.  No external repository is pinned as a
dependency of this project by this declaration, and no row is treated as a
completed upstream proof body.
-/
def externalWardLeanAuditCandidates : List ExternalWardLeanAuditCandidate := [
  {
    repository := "https://github.com/leanprover-community/mathlib4"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    toolchain := "leanprover/lean4:v4.29.0 through this repository"
    moduleOrSearchScope :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib plus local " ++
      "AwesomeTheorems Stage1 files"
    matchedTerms := ["Penrose", "Ward", "twistor", "Yang-Mills", "YangMills"]
    relevantNames := [
      "FiberBundle",
      "VectorBundle",
      "CovariantDerivative",
      "extDeriv",
      "Projectivization",
      "Mathlib.Tactic.Widget.StringDiagram.PenroseVar",
      "no WardCorrespondence/PenroseWard/SelfDualYangMills/twistor-Yang-Mills theorem name found"
    ]
    placeholderStatus := "no target external proof found; no placeholder target to audit"
    lakeDependencyFeasibility :=
      "already pinned and locally checked as this repo's mathlib dependency, " ++
      "but it supplies only adjacent manifold/vector-bundle/differential-form/" ++
      "projectivization substrate, not a terminal Ward correspondence theorem"
    closureStatus :=
      "not terminal: local mathlib search found no Ward, Penrose-Ward, " ++
      "twistor Yang-Mills, or self-dual Yang-Mills correspondence theorem"
    terminalWardTheoremFound := false
  },
  {
    repository := "https://github.com/HEPLean/PhysLean"
    commit := "cd22b0c28882412447d12d5cfde677c4ad999994"
    toolchain := "leanprover/lean4:v4.29.1"
    moduleOrSearchScope := "repository-wide Lean-file scan in shallow clone"
    matchedTerms := []
    relevantNames := [
      "no matches for WardCorrespondence",
      "no matches for Penrose-Ward/PenroseWard",
      "no matches for twistor/Twistor",
      "no matches for YangMills/Yang-Mills/SDYM in the C008 scan"
    ]
    placeholderStatus := "no target proof or placeholder target located by the audited terms"
    lakeDependencyFeasibility :=
      "not currently Lake-compatible with this repo without integration work: " ++
      "PhysLean uses Lean 4.29.1 and mathlib revision " ++
      "5e932f97dd25535344f80f9dd8da3aab83df0fe6, while this repo uses Lean " ++
      "4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95"
    closureStatus :=
      "not terminal: no Ward correspondence, Penrose-Ward transform, twistor, " ++
      "or self-dual Yang-Mills closure was found in the refreshed scan"
    terminalWardTheoremFound := false
  },
  {
    repository := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems"
    commit := "540da94826f70f3edf4d4fc66ce6cda20e903f61"
    toolchain := "leanprover/lean4:v4.26.0"
    moduleOrSearchScope := "Problems/YangMills/Millennium.lean; Problems/YangMills/Quantum.lean"
    matchedTerms := ["YangMills", "Yang-Mills"]
    relevantNames := [
      "MillenniumYangMills.YangMillsExistenceAndMassGap",
      "MillenniumYangMillsDefs.QuantumYangMillsTheory",
      "MillenniumYangMillsDefs.YangMillsAction",
      "MillenniumYangMillsDefs.GaugeField",
      "MillenniumYangMillsDefs.FieldStrength"
    ]
    placeholderStatus :=
      "relevant YangMills files contain statement/data scaffolding; no Ward, " ++
      "Penrose-Ward, twistor, SDYM, or line-triviality proof target was found"
    lakeDependencyFeasibility :=
      "not feasible as a THM-M-1542 dependency without a theorem bridge and " ++
      "toolchain migration: the project uses Lean 4.26.0 and mathlib revision " ++
      "2df2f0150c275ad53cb3c90f7c98ec15a56a1a67"
    closureStatus :=
      "adjacent Yang-Mills statement scaffolding only; no Ward correspondence " ++
      "or self-dual Yang-Mills/twistor-bundle closure"
    terminalWardTheoremFound := false
  },
  {
    repository := "https://github.com/the-omega-institute/automath"
    commit := "605f51d73d0ccf42d89352da7cde5199124fbd4a"
    toolchain := "leanprover/lean4:v4.28.0 under lean4/"
    moduleOrSearchScope := "lean4/Omega/SyncKernelWeighted and lean4/Omega/Zeta self-dual files"
    matchedTerms := ["SelfDual"]
    relevantNames := [
      "Omega.SyncKernelWeighted.SelfDualBlockMatrix",
      "Omega.SyncKernelWeighted.paper_self_dual_normal_form_1pmu",
      "Omega.SyncKernelWeighted.paper_self_dual_u1_two_channel_zeta"
    ]
    placeholderStatus :=
      "inspected self-dual files contain completed elementary/spectral proofs, " ++
      "but they are unrelated to curvature self-duality or Ward correspondence"
    lakeDependencyFeasibility :=
      "not feasible for THM-M-1542; name match is about spectral/kernel " ++
      "self-duality and uses Lean 4.28.0 with mathlib revision " ++
      "8f9d9cff6bd728b17a24e163c9402775d9e6a365"
    closureStatus :=
      "false positive: no Ward, twistor, Yang-Mills, connection, curvature, " ++
      "or holomorphic-bundle theorem family"
    terminalWardTheoremFound := false
  }
]

/-- The C008 external Ward audit records four refreshed primary-source rows. -/
theorem externalWardLeanAuditCandidates_length :
    externalWardLeanAuditCandidates.length = 4 :=
  rfl

/-- No refreshed external row contains a terminal Ward-correspondence theorem. -/
theorem externalWardLeanAuditCandidates_no_terminal :
    externalWardLeanAuditCandidates.all (fun row => !row.terminalWardTheoremFound) = true :=
  rfl

/-- Repo-local integration gate for the C008 external Ward-correspondence audit. -/
def externalWardIntegrationGateResult : String :=
  "pass_noncompletion: no terminal external Ward-correspondence Lean 4 proof " ++
  "was found in the refreshed primary-source rows, authenticated GitHub code " ++
  "search is explicitly blocked, no external_upstream_anchor_only evidence is " ++
  "treated as completion, and THM-M-1542 remains not_repo_local_closed / " ++
  "formalization_debt"

/--
C009 synchronization gate: the checked Lean artifact, theorem-tree ledger, and
public merge surface are aligned on non-completion.

This is intentionally a gate record, not a proof of the Ward correspondence.
The public checklist must stay open until a concrete local proof body, a
mathlib wrapper, or a pinned external dependency validates locally and the
serialized public backfill is merged.
-/
def stage1SynchronizationGate : Stage1SynchronizationGate := {
  childTask := "S1-M-183-C009"
  checkedArtifact := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_183.lean"
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_183.lean"
  theoremTreeLedger :=
    ".cron/results/stage1_20260430/codex_workers/S1-M-183.md plus child " ++
    "ledgers .cron/results/stage1_20260430_child/codex_workers/S1-M-183-C001.md " ++
    "through S1-M-183-C009.md"
  publicMergeSurface :=
    "Docs/Stage1_Blueprint.md:2520 and related public todo/checklist surfaces; " ++
    "not edited by this child because public-doc integration is serialized"
  localLeanStatus :=
    "checked statement-shape, API-boundary, audit-record, and synchronization-gate " ++
    "declarations only; no sorry, admit, or axiom is required by this gate"
  theoremCompletionStatus :=
    "open_not_completed: WardCorrespondenceTheorem and StatementShape remain " ++
    "unproved terminal theorem targets"
  repoLocalIntegrationDebtGate :=
    "pass_noncompletion: no completed state retains repo_local_integration_debt; " ++
    "C008 found no terminal external Lean 4 Ward proof in refreshed rows and " ++
    "recorded authenticated GitHub search as blocked"
  remainingOpenLeaves := [
    "replace TwistorFibrationBoundary proposition fields with concrete APIs for smooth oriented conformal four-manifolds and twistor spaces",
    "instantiate principal bundles, gauge groups, smooth connections, and adjoint-valued curvature two-forms",
    "construct metric/orientation-derived Hodge star on two-forms in dimension four and connect it to IsSelfDual",
    "instantiate the self-dual curvature implies Yang-Mills lemma for concrete gauge-theory data",
    "define concrete holomorphic vector bundles on twistor space, line triviality, and real-structure compatibility",
    "construct the Penrose-Ward transform and inverse transform or import a checked theorem family",
    "rerun authenticated primary-source GitHub/Lean search and pin/import/check any terminal proof found or record a concrete blocker",
    "merge the checked local status into public blueprint/todo surfaces without marking THM-M-1542 complete"
  ]
  publicBackfillDecision :=
    "integrator-ready: merge a non-completion status note, local validation command, " ++
    "checked declaration anchors, and open leaves into the public Stage1 surface"
}

/-- C009 keeps the Ward-correspondence checklist open. -/
theorem stage1SynchronizationGate_completion_status :
    stage1SynchronizationGate.theoremCompletionStatus =
      "open_not_completed: WardCorrespondenceTheorem and StatementShape remain " ++
      "unproved terminal theorem targets" :=
  rfl

/-- C009 records eight genuinely remaining public leaves. -/
theorem stage1SynchronizationGate_remainingOpenLeaves_length :
    stage1SynchronizationGate.remainingOpenLeaves.length = 8 :=
  rfl

/--
C004 decision: expose a checked two-form Hodge-star boundary and self-duality
bridge, but do not claim a metric/orientation-derived Hodge-star construction.
-/
def hodgeStarAPIAudit : HodgeStarAPIAudit := {
  childTask := "S1-M-183-C004",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  concreteCarrier :=
    "FourDimensionalTwoForm E V = E [⋀^Fin 2]→L[ℝ] V, with " ++
    "FourDimensionalTwoFormHodgeStar.star : FourDimensionalTwoForm E V →L[ℝ] " ++
    "FourDimensionalTwoForm E V and Module.finrank ℝ E = 4",
  checkedNames := [
    "FourDimensionalTwoForm",
    "FourDimensionalTwoFormHodgeStar",
    "FourDimensionalTwoFormHodgeStar.star",
    "FourDimensionalTwoFormHodgeStar.star_square",
    "IsSelfDualFourDimensionalTwoForm",
    "isSelfDualFourDimensionalTwoForm_iff",
    "fourDimensionalTwoFormHodgeStar_square",
    "isSelfDualFourDimensionalTwoForm_zero",
    "ContinuousAlternatingMap",
    "ContinuousLinearMap"
  ],
  exactAbsences := [
    "no pinned local mathlib Hodge-star construction on smooth manifold differential forms",
    "no repo-local metric/orientation/volume-form formula for Hodge star on two-forms",
    "no adjoint-bundle-valued Hodge star for curvature two-forms on a principal bundle",
    "no checked geometric sign-convention theorem connecting a constructed star to Yang-Mills"
  ],
  replacementDecision :=
    "partial local progress: the two-form carrier and self-duality bridge are " ++
    "checked; the geometric construction of star from a four-manifold metric " ++
    "and orientation remains formalization_debt, not repo_local_integration_debt",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_183.lean"
}

/--
C005 decision: prove the Yang-Mills implication under an explicit abstract
Bianchi/sign-convention interface, while recording the missing concrete
principal-bundle instantiation as formalization debt.
-/
def selfDualYangMillsLemmaAudit : SelfDualYangMillsLemmaAudit := {
  childTask := "S1-M-183-C005",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  checkedBoundary :=
    "SelfDualYangMillsSignConvention packages curvature, hodgeStar, " ++
    "hodgeStar_square, covariantExteriorDerivative, yangMillsOperator, " ++
    "Bianchi identity, the selected self-dual sign-convention equality, and " ++
    "yangMillsEquation_iff_operator_zero.  The checked theorem " ++
    "yangMills_of_isSelfDualCurvature proves self-dual curvature implies the " ++
    "Yang-Mills equation from those fields.",
  checkedNames := [
    "SelfDualYangMillsSignConvention",
    "SelfDualYangMillsSignConvention.curvature",
    "SelfDualYangMillsSignConvention.hodgeStar",
    "SelfDualYangMillsSignConvention.hodgeStar_square",
    "SelfDualYangMillsSignConvention.covariantExteriorDerivative",
    "SelfDualYangMillsSignConvention.yangMillsOperator",
    "SelfDualYangMillsSignConvention.bianchiIdentity",
    "SelfDualYangMillsSignConvention.selfDual_yangMillsOperator_eq_bianchi",
    "SelfDualYangMillsSignConvention.yangMillsEquation_iff_operator_zero",
    "yangMills_of_isSelfDualCurvature",
    "SelfDualYangMillsSignConvention.toSelfDualYangMillsData",
    "yangMills_of_mem_selfDualConnectionSet"
  ],
  exactAbsences := [
    "no concrete smooth principal-bundle connection API in the pinned local closure",
    "no adjoint-bundle-valued curvature two-form API over a smooth four-manifold",
    "no covariant exterior derivative on adjoint-valued forms for gauge connections",
    "no codifferential / formal adjoint API for the Yang-Mills operator",
    "no metric/orientation-derived Hodge-star sign theorem on curvature forms",
    "no terminal Ward or self-dual Yang-Mills theorem to import"
  ],
  replacementDecision :=
    "partial local proof progress: the implication is checked for an explicit " ++
    "Bianchi/sign-convention boundary.  Instantiating that boundary with " ++
    "geometric principal-bundle curvature data remains formalization_debt, " ++
    "not a completed Ward-correspondence proof.",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_183.lean"
}

/--
C006 decision: group holomorphicity, line-triviality, and real-structure
compatibility into a checked twistor-bundle boundary without claiming concrete
holomorphic vector-bundle infrastructure.
-/
def holomorphicTwistorBundleAPIAudit : HolomorphicTwistorBundleAPIAudit := {
  childTask := "S1-M-183-C006",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  checkedBoundary :=
    "HolomorphicTwistorBundleBoundary packages the existing twistor fibration, " ++
    "a holomorphicVectorBundle predicate on abstract twistor-bundle objects, " ++
    "linewise triviality over each base point, all-line triviality, an " ++
    "involutive realPullback, a realStructureIsomorphism relation, and the " ++
    "realStructureCondition equivalence.  WardCorrespondenceData now consumes " ++
    "this boundary and exposes checked wrappers for holomorphicity, triviality " ++
    "on twistor lines, reality, and admissibleHolomorphicTwistorBundle.",
  checkedNames := [
    "HolomorphicTwistorBundleBoundary",
    "HolomorphicTwistorBundleBoundary.twistorGeometry",
    "HolomorphicTwistorBundleBoundary.holomorphicVectorBundle",
    "HolomorphicTwistorBundleBoundary.trivialOnTwistorLine",
    "HolomorphicTwistorBundleBoundary.trivialOnTwistorLines",
    "HolomorphicTwistorBundleBoundary.trivialOnTwistorLines_iff",
    "HolomorphicTwistorBundleBoundary.realPullback",
    "HolomorphicTwistorBundleBoundary.realPullback_involutive",
    "HolomorphicTwistorBundleBoundary.realStructureIsomorphism",
    "HolomorphicTwistorBundleBoundary.realStructureCondition",
    "HolomorphicTwistorBundleBoundary.admissible",
    "HolomorphicTwistorBundleBoundary.admissible_iff",
    "HolomorphicTwistorBundleBoundary.trivialOnTwistorLine_of_trivialOnTwistorLines",
    "HolomorphicTwistorBundleBoundary.realStructureCondition_unfold",
    "HolomorphicTwistorBundleBoundary.realPullback_apply_apply",
    "WardCorrespondenceData.twistorBundles",
    "WardCorrespondenceData.holomorphicVectorBundle",
    "WardCorrespondenceData.trivialOnTwistorLines",
    "WardCorrespondenceData.realStructureCondition",
    "WardCorrespondenceData.admissibleHolomorphicTwistorBundle",
    "WardCorrespondenceData.admissibleHolomorphicTwistorBundle_iff"
  ],
  exactAbsences := [
    "no concrete holomorphic vector-bundle API over complex manifolds in the pinned local closure",
    "no Ward twistor-line restricted bundle trivialization API",
    "no pullback of holomorphic vector bundles along the twistor real involution",
    "no isomorphism category/equivalence relation for real holomorphic twistor bundles",
    "no sheaf-cohomological Penrose-Ward construction or inverse construction",
    "no terminal theorem identifying these twistor bundles with self-dual Yang-Mills gauge classes"
  ],
  replacementDecision :=
    "partial local interface progress: the three Ward-side twistor-bundle " ++
    "conditions are now a named checked boundary with projection lemmas.  " ++
    "Replacing the predicates by concrete holomorphic bundle, restriction, " ++
    "pullback, and real-isomorphism APIs remains formalization_debt, not a " ++
    "completed Ward-correspondence proof.",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_183.lean"
}

/--
C007 decision: expose a named Penrose-Ward transform/inverse-transform
boundary and record the exact missing theorem family as formalization debt.
-/
def penroseWardTransformAPIAudit : PenroseWardTransformAPIAudit := {
  childTask := "S1-M-183-C007",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  checkedBoundary :=
    "PenroseWardTransformBoundary packages penroseWardTransform : TwBundle -> " ++
    "Conn, inversePenroseWardTransform : Conn -> TwBundle, the checked " ++
    "forward map from admissible holomorphic twistor bundles to " ++
    "selfDualConnectionSet, the checked inverse map from selfDualConnectionSet " ++
    "to admissibleHolomorphicTwistorBundle, and proposition fields for inverse " ++
    "laws on admissible twistor bundles and self-dual gauge classes plus gauge " ++
    "and holomorphic-structure compatibility.  WardCorrespondence can be " ++
    "projected to this boundary by WardCorrespondence.toPenroseWardTransformBoundary.",
  checkedNames := [
    "PenroseWardTransformBoundary",
    "PenroseWardTransformBoundary.penroseWardTransform",
    "PenroseWardTransformBoundary.inversePenroseWardTransform",
    "PenroseWardTransformBoundary.penroseWardTransform_maps_admissible",
    "PenroseWardTransformBoundary.inversePenroseWardTransform_maps_selfDual",
    "PenroseWardTransformBoundary.penroseWardTransform_selfDual",
    "PenroseWardTransformBoundary.inversePenroseWardTransform_holomorphic",
    "PenroseWardTransformBoundary.inversePenroseWardTransform_trivialOnTwistorLines",
    "PenroseWardTransformBoundary.inversePenroseWardTransform_realStructureCondition",
    "WardCorrespondence.toPenroseWardTransformBoundary"
  ],
  exactMissingTheoremFamily := [
    "construction of the Penrose-Ward transform from a concrete holomorphic vector bundle trivial on each twistor line to a smooth self-dual principal connection",
    "construction of the inverse Penrose-Ward transform from a smooth self-dual principal connection to a holomorphic twistor bundle with line triviality and real structure",
    "proof that the two transforms are inverse on admissible holomorphic twistor bundles modulo the chosen holomorphic bundle isomorphism/framing relation",
    "proof that the two transforms are inverse on self-dual Yang-Mills connections modulo gauge equivalence",
    "proof of compatibility with gauge actions, framing/stability conditions, and real-structure conventions",
    "terminal theorem identifying the resulting moduli classes as the Ward correspondence"
  ],
  debtClassification :=
    "formalization_debt: the mathematical Ward correspondence is known, but " ++
    "the repo-local Lean closure lacks the concrete twistor/gauge/holomorphic " ++
    "bundle APIs and checked transform constructions.  No external checked " ++
    "proof is pinned/imported/checked here, so this is not a completed theorem " ++
    "and not a repo_local_integration_debt completion state.",
  replacementDecision :=
    "partial local interface progress: keep WardCorrespondenceTheorem open and " ++
    "use PenroseWardTransformBoundary as the integration target for future " ++
    "concrete Penrose-Ward and inverse-transform proofs",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_183.lean"
}

/-- Checked complex-manifold anchor: holomorphic maps on compact connected complex manifolds are constant. -/
theorem holomorphicMap_constant_on_compact_connected
    {EModel : Type uE} [NormedAddCommGroup EModel] [NormedSpace ℂ EModel]
    {FModel : Type uF} [NormedAddCommGroup FModel] [NormedSpace ℂ FModel]
    {H : Type uH} [TopologicalSpace H]
    {I : ModelWithCorners ℂ EModel H} [I.Boundaryless]
    {X : Type uM} [TopologicalSpace X] [ChartedSpace H X]
    [IsManifold I 1 X] [CompactSpace X] [PreconnectedSpace X]
    {f : X → FModel} (hf : MDiff f) (a b : X) :
    f a = f b :=
  MDifferentiable.apply_eq_of_compactSpace hf a b

/-- Checked linear-operator substrate: the identity state dictionary is continuous linear. -/
def identityLinearDictionary
    (H : Type uH) [TopologicalSpace H] [AddCommMonoid H] [Module ℂ H] : H →L[ℂ] H :=
  ContinuousLinearMap.id ℂ H

/-- The checked identity dictionary acts as the identity. -/
theorem identityLinearDictionary_apply
    {H : Type uH} [TopologicalSpace H] [AddCommMonoid H] [Module ℂ H] (x : H) :
    identityLinearDictionary H x = x :=
  ContinuousLinearMap.id_apply x

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Topology.FiberBundle.Basic",
  "Mathlib.Geometry.Manifold.ChartedSpace",
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.Complex",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.Analysis.Calculus.Conformal.NormedSpace",
  "Mathlib.Analysis.InnerProductSpace.Orientation",
  "Mathlib.LinearAlgebra.Projectivization.Basic",
  "Mathlib.Geometry.Manifold.Algebra.LieGroup",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.Normed.Operator.Basic"
]

/-- Nearby checked names used or audited for the Ward-correspondence boundary. -/
def mathlibAnchorNames : List String := [
  "ChartedSpace",
  "IsManifold",
  "MDifferentiable.apply_eq_of_compactSpace",
  "MDifferentiable.exists_eq_const_of_compactSpace",
  "FiberBundle",
  "VectorBundle",
  "LieGroup",
  "TangentSpace",
  "ContMDiffSection",
  "CovariantDerivative",
  "IsCovariantDerivativeOn",
  "CovariantDerivative.ContMDiffCovariantDerivative",
  "CovariantDerivative.difference",
  "Orientation",
  "Conformal",
  "MDifferentiable",
  "Projectivization",
  "UnbundledAdjointValuedTwoForm",
  "FourDimensionalTwoForm",
  "FourDimensionalTwoFormHodgeStar",
  "IsSelfDualFourDimensionalTwoForm",
  "SelfDualYangMillsSignConvention",
  "yangMills_of_isSelfDualCurvature",
  "SelfDualYangMillsSignConvention.toSelfDualYangMillsData",
  "HolomorphicTwistorBundleBoundary",
  "HolomorphicTwistorBundleBoundary.admissible",
  "HolomorphicTwistorBundleBoundary.trivialOnTwistorLine_of_trivialOnTwistorLines",
  "HolomorphicTwistorBundleBoundary.realStructureCondition_unfold",
  "WardCorrespondenceData.admissibleHolomorphicTwistorBundle",
  "PenroseWardTransformBoundary",
  "PenroseWardTransformBoundary.penroseWardTransform_selfDual",
  "PenroseWardTransformBoundary.inversePenroseWardTransform_holomorphic",
  "WardCorrespondence.toPenroseWardTransformBoundary",
  "Stage1SynchronizationGate",
  "stage1SynchronizationGate",
  "stage1SynchronizationGate_completion_status",
  "stage1SynchronizationGate_remainingOpenLeaves_length",
  "extDeriv",
  "MulAction",
  "ContinuousLinearMap.id",
  "ContinuousLinearMap.id_apply",
  "InnerProductSpace"
]

/-- Search terms that did not locate a terminal Ward theorem in the pinned local mathlib tree. -/
def absentTerminalSearchTerms : List String := [
  "Ward correspondence",
  "twistor",
  "Twistor",
  "PrincipalBundle",
  "principal bundle",
  "principal connection",
  "gauge group",
  "adjoint bundle",
  "adjoint-valued curvature",
  "curvature two-form",
  "self-dual Yang-Mills",
  "Yang-Mills",
  "YangMills",
  "SDYM",
  "Penrose transform",
  "Penrose-Ward transform",
  "inverse Penrose-Ward transform",
  "holomorphic vector bundle",
  "twistor line",
  "Hodge star"
]

/-! ## Audit probes retained in the checked file. -/

#check TwistorFibrationBoundary
#check TwistorFibrationBoundary.projection_smooth
#check TwistorFibrationBoundary.conformal_transition
#check ComplexProjectiveLine
#check UnbundledAdjointValuedTwoForm
#check FourDimensionalTwoForm
#check FourDimensionalTwoFormHodgeStar
#check FourDimensionalTwoFormHodgeStar.star
#check FourDimensionalTwoFormHodgeStar.star_square
#check IsSelfDual
#check isSelfDual_zero
#check IsSelfDualFourDimensionalTwoForm
#check isSelfDualFourDimensionalTwoForm_iff
#check fourDimensionalTwoFormHodgeStar_square
#check isSelfDualFourDimensionalTwoForm_zero
#check SelfDualYangMillsSignConvention
#check SelfDualYangMillsSignConvention.bianchiIdentity
#check SelfDualYangMillsSignConvention.selfDual_yangMillsOperator_eq_bianchi
#check yangMills_of_isSelfDualCurvature
#check SelfDualYangMillsSignConvention.toSelfDualYangMillsData
#check GaugeEquivalent
#check gaugeEquivalent_refl
#check SelfDualYangMillsData
#check selfDualConnectionSet
#check yangMills_of_mem_selfDualConnectionSet
#check HolomorphicTwistorBundleBoundary
#check HolomorphicTwistorBundleBoundary.twistorGeometry
#check HolomorphicTwistorBundleBoundary.holomorphicVectorBundle
#check HolomorphicTwistorBundleBoundary.trivialOnTwistorLine
#check HolomorphicTwistorBundleBoundary.trivialOnTwistorLines
#check HolomorphicTwistorBundleBoundary.trivialOnTwistorLines_iff
#check HolomorphicTwistorBundleBoundary.realPullback
#check HolomorphicTwistorBundleBoundary.realPullback_involutive
#check HolomorphicTwistorBundleBoundary.realStructureIsomorphism
#check HolomorphicTwistorBundleBoundary.realStructureCondition
#check HolomorphicTwistorBundleBoundary.admissible
#check HolomorphicTwistorBundleBoundary.admissible_iff
#check HolomorphicTwistorBundleBoundary.trivialOnTwistorLine_of_trivialOnTwistorLines
#check HolomorphicTwistorBundleBoundary.realStructureCondition_unfold
#check HolomorphicTwistorBundleBoundary.realPullback_apply_apply
#check WardCorrespondenceData
#check WardCorrespondenceData.twistorBundles
#check WardCorrespondenceData.holomorphicVectorBundle
#check WardCorrespondenceData.trivialOnTwistorLines
#check WardCorrespondenceData.realStructureCondition
#check WardCorrespondenceData.admissibleHolomorphicTwistorBundle
#check WardCorrespondenceData.admissibleHolomorphicTwistorBundle_iff
#check PenroseWardTransformBoundary
#check PenroseWardTransformBoundary.penroseWardTransform
#check PenroseWardTransformBoundary.inversePenroseWardTransform
#check PenroseWardTransformBoundary.penroseWardTransform_maps_admissible
#check PenroseWardTransformBoundary.inversePenroseWardTransform_maps_selfDual
#check PenroseWardTransformBoundary.penroseWardTransform_selfDual
#check PenroseWardTransformBoundary.inversePenroseWardTransform_holomorphic
#check PenroseWardTransformBoundary.inversePenroseWardTransform_trivialOnTwistorLines
#check PenroseWardTransformBoundary.inversePenroseWardTransform_realStructureCondition
#check WardCorrespondence
#check WardCorrespondence.toPenroseWardTransformBoundary
#check WardCorrespondenceTheorem
#check StatementShape
#check GaugeCurvatureAPIAudit
#check gaugeCurvatureAPIAudit
#check HodgeStarAPIAudit
#check hodgeStarAPIAudit
#check SelfDualYangMillsLemmaAudit
#check selfDualYangMillsLemmaAudit
#check HolomorphicTwistorBundleAPIAudit
#check holomorphicTwistorBundleAPIAudit
#check PenroseWardTransformAPIAudit
#check penroseWardTransformAPIAudit
#check Stage1SynchronizationGate
#check stage1SynchronizationGate
#check stage1SynchronizationGate_completion_status
#check stage1SynchronizationGate_remainingOpenLeaves_length
#check ExternalWardLeanAuditCandidate
#check externalWardAuditSearchTerms
#check externalWardAuditAuthenticationStatus
#check externalWardLeanAuditCandidates
#check externalWardLeanAuditCandidates_length
#check externalWardLeanAuditCandidates_no_terminal
#check externalWardIntegrationGateResult
#check holomorphicMap_constant_on_compact_connected
#check identityLinearDictionary_apply
#check ChartedSpace
#check IsManifold
#check FiberBundle
#check VectorBundle
#check LieGroup
#check CovariantDerivative
#check IsCovariantDerivativeOn
#check CovariantDerivative.ContMDiffCovariantDerivative
#check CovariantDerivative.difference
#check extDeriv
#check MDifferentiable.apply_eq_of_compactSpace

end S1_M_183
end Stage1
end AwesomeTheorems
