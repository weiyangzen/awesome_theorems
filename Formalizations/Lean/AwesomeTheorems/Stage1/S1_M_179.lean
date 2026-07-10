import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Functor
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Scheme
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.StructureSheaf
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Topology
import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.Analytic.Basic
import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.LinearAlgebra.Projectivization.Basic

/-!
# S1-M-179 / THM-M-1543: Atiyah-Ward correspondence

This Stage1 artifact records a conservative Lean statement-shape boundary for
the Atiyah-Ward correspondence between four-dimensional instanton data and
holomorphic vector-bundle data on twistor space.

The pinned mathlib snapshot contains useful substrates for smooth manifolds,
the smooth structure on spheres, projectivization, analytic maps, schemes,
Riemannian metrics, and covariant-derivative interfaces.  It does not expose a
terminal formalization of anti-self-dual Yang-Mills instantons, twistor
incidence, holomorphic vector bundles on `CP^3`, or the Atiyah-Ward transform.
The declarations below therefore isolate the missing gauge/twistor geometry as
explicit `Prop` fields while keeping the available ambient objects in concrete
mathlib terms.  The file contains only closed declarations and audit probes.
-/

noncomputable section

open AlgebraicGeometry CategoryTheory
open scoped LinearAlgebra.Projectivization Manifold

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_179

/-- The standard smooth model for the four-sphere used by instanton examples. -/
abbrev FourSphere : Type :=
  Metric.sphere (0 : EuclideanSpace ℝ (Fin 5)) 1

/-- The algebraic/topological point-set model of complex projective three-space. -/
abbrev ComplexProjectiveThree : Type :=
  Projectivization ℂ (Fin 4 → ℂ)

/-- The checked point-set model used for twistor fibers/lines: `CP^1`. -/
abbrev ComplexProjectiveLine : Type :=
  Projectivization ℂ (Fin 2 → ℂ)

/-- An unbundled real-valued differential form on a normed vector-space model. -/
abbrev RealDifferentialForm (Base : Type u) [NormedAddCommGroup Base]
    [NormedSpace ℝ Base] (degree : ℕ) :=
  Base → Base [⋀^Fin degree]→L[ℝ] ℝ

/-- Real two-forms, used as the checked local carrier for the Hodge-star boundary. -/
abbrev RealTwoForm (Base : Type u) [NormedAddCommGroup Base] [NormedSpace ℝ Base] :=
  RealDifferentialForm Base 2

/-- Hodge star data on two-forms for a four-dimensional gauge-theory model. -/
structure HodgeStarOnTwoForms (TwoForm : Type u) [AddGroup TwoForm] : Type u where
  star : TwoForm → TwoForm
  star_square : ∀ ω : TwoForm, star (star ω) = ω

/-- Anti-self-duality for a two-form-like curvature value. -/
def IsAntiSelfDual {TwoForm : Type u} [AddGroup TwoForm]
    (hodgeStar : HodgeStarOnTwoForms TwoForm) (F : TwoForm) : Prop :=
  hodgeStar.star F = -F

/-- The ASD predicate unfolds to the expected Hodge-star equation. -/
theorem isAntiSelfDual_iff {TwoForm : Type u} [AddGroup TwoForm]
    (hodgeStar : HodgeStarOnTwoForms TwoForm) (F : TwoForm) :
    IsAntiSelfDual hodgeStar F ↔ hodgeStar.star F = -F :=
  Iff.rfl

/-- If the Hodge star preserves zero, then zero curvature is anti-self-dual. -/
theorem isAntiSelfDual_zero {TwoForm : Type u} [AddGroup TwoForm]
    (hodgeStar : HodgeStarOnTwoForms TwoForm) (hzero : hodgeStar.star 0 = 0) :
    IsAntiSelfDual hodgeStar (0 : TwoForm) := by
  simp [IsAntiSelfDual, hzero]

/-- Gauge equivalence of two connections under a mathlib multiplicative action. -/
def GaugeEquivalent {GaugeGroup Connection : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection]
    (A B : Connection) : Prop :=
  ∃ g : GaugeGroup, g • A = B

/-- Gauge equivalence is reflexive. -/
theorem gaugeEquivalent_refl {GaugeGroup Connection : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection]
    (A : Connection) :
    GaugeEquivalent (GaugeGroup := GaugeGroup) A A := by
  exact ⟨1, by simp⟩

/-- The gauge orbit of a connection. -/
def gaugeOrbit {GaugeGroup Connection : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection]
    (A : Connection) : Set Connection :=
  {B | GaugeEquivalent (GaugeGroup := GaugeGroup) A B}

/-- Orbit membership is exactly gauge equivalence. -/
theorem mem_gaugeOrbit_iff {GaugeGroup Connection : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection]
    {A B : Connection} :
    B ∈ gaugeOrbit (GaugeGroup := GaugeGroup) A ↔
      GaugeEquivalent (GaugeGroup := GaugeGroup) A B :=
  Iff.rfl

/-- Every connection is in its own gauge orbit. -/
theorem mem_gaugeOrbit_self {GaugeGroup Connection : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection]
    (A : Connection) :
    A ∈ gaugeOrbit (GaugeGroup := GaugeGroup) A :=
  gaugeEquivalent_refl A

/--
Gauge-side API boundary for `THM-M-1543.gauge-api`.

The concrete future target is a connection on a principal or vector bundle over
a four-manifold, with curvature an adjoint-valued two-form and Hodge star from
the oriented conformal structure.  The current repo-local closure can import
covariant-derivative and differential-form substrates, but not a terminal
instanton API, so the missing analytic and gauge-invariance laws are explicit.
-/
structure AntiSelfDualGaugeAPI
    (GaugeGroup Connection Curvature Charge Framing : Type u)
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature] :
    Type (u + 1) where
  admissibleConnection : Connection → Prop
  curvature : Connection → Curvature
  hodgeStarOnTwoForms : HodgeStarOnTwoForms Curvature
  yangMillsEquation : Connection → Prop
  finiteYangMillsAction : Connection → Prop
  charge : Connection → Charge
  framing : Connection → Framing
  gaugeActionPreservesAdmissibility :
    ∀ {A B : Connection}, GaugeEquivalent (GaugeGroup := GaugeGroup) A B →
      admissibleConnection A → admissibleConnection B
  curvatureGaugeEquivariance : Prop
  asdImpliesYangMills :
    ∀ A : Connection, IsAntiSelfDual hodgeStarOnTwoForms (curvature A) →
      yangMillsEquation A
  finiteActionGaugeInvariant :
    ∀ {A B : Connection}, GaugeEquivalent (GaugeGroup := GaugeGroup) A B →
      finiteYangMillsAction A → finiteYangMillsAction B
  chargeGaugeInvariant :
    ∀ {A B : Connection}, GaugeEquivalent (GaugeGroup := GaugeGroup) A B →
      charge A = charge B
  framingGaugeInvariant :
    ∀ {A B : Connection}, GaugeEquivalent (GaugeGroup := GaugeGroup) A B →
      framing A = framing B

/-- Connections with admissible, anti-self-dual curvature and finite action. -/
def antiSelfDualFiniteActionConnections
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    (D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing) :
    Set Connection :=
  {A | D.admissibleConnection A ∧
    IsAntiSelfDual D.hodgeStarOnTwoForms (D.curvature A) ∧
      D.finiteYangMillsAction A}

/-- Membership unfolds to admissibility, ASD curvature, and finite action. -/
theorem mem_antiSelfDualFiniteActionConnections_iff
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    (D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing)
    {A : Connection} :
    A ∈ antiSelfDualFiniteActionConnections D ↔
      D.admissibleConnection A ∧
        IsAntiSelfDual D.hodgeStarOnTwoForms (D.curvature A) ∧
          D.finiteYangMillsAction A :=
  Iff.rfl

/-- An ASD finite-action connection satisfies the Yang-Mills equation. -/
theorem yangMills_of_mem_antiSelfDualFiniteActionConnections
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    (D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing)
    {A : Connection}
    (hA : A ∈ antiSelfDualFiniteActionConnections D) :
    D.yangMillsEquation A :=
  D.asdImpliesYangMills A hA.2.1

/-- Charge is constant along gauge-equivalent connections in the API boundary. -/
theorem charge_eq_of_gaugeEquivalent
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    (D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing)
    {A B : Connection}
    (hAB : GaugeEquivalent (GaugeGroup := GaugeGroup) A B) :
    D.charge A = D.charge B :=
  D.chargeGaugeInvariant hAB

/-- Framing is constant along gauge-equivalent connections in the API boundary. -/
theorem framing_eq_of_gaugeEquivalent
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    (D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing)
    {A B : Connection}
    (hAB : GaugeEquivalent (GaugeGroup := GaugeGroup) A B) :
    D.framing A = D.framing B :=
  D.framingGaugeInvariant hAB

/--
Abstract twistor-space model over a four-dimensional base.

The current local dependencies can name topological and smooth-manifold
carriers, but they do not provide a complete twistor fibration or incidence API.
Those missing conditions are kept as proposition fields.
-/
structure TwistorModel (Base Twistor : Type u)
    [TopologicalSpace Base] [TopologicalSpace Twistor] : Type (u + 1) where
  projection : Twistor → Base
  twistorLine : Base → Set Twistor
  baseIsFourManifold : Prop
  twistorHasComplexStructure : Prop
  twistorLinesAreProjectiveLines : Prop
  realStructure : Prop
  incidenceRelation : Prop

/-- The fiber of a twistor projection over a base point. -/
abbrev TwistorFiber {Twistor : Type u} {Base : Type v} (projection : Twistor → Base)
    (x : Base) : Type u :=
  {z : Twistor // projection z = x}

/-- The line subset over a base point, bundled as a type. -/
abbrev TwistorLineCarrier {Twistor : Type u} (twistorLine : FourSphere → Set Twistor)
    (x : FourSphere) : Type u :=
  {z : Twistor // z ∈ twistorLine x}

/--
Refined twistor-space API over the checked `FourSphere` carrier.

This is the strongest current repo-local boundary for `THM-M-1543.twistor-api`.
It names the projection, twistor lines, real structure, incidence relation, and
the selected proof object that each projection fiber is modeled by `CP^1`.  It
does not construct the classical twistor fibration `CP^3 → S^4`; that remains a
formalization target or an upstream import target.
-/
structure TwistorSpaceOverFourSphereAPI (Twistor : Type u)
    [TopologicalSpace Twistor] : Type (u + 1) where
  projection : Twistor → FourSphere
  twistorLine : FourSphere → Set Twistor
  twistorLineParam : FourSphere → ComplexProjectiveLine → Twistor
  twistorLineParam_mem :
    ∀ x : FourSphere, ∀ p : ComplexProjectiveLine, twistorLineParam x p ∈ twistorLine x
  twistorLineParam_surjective :
    ∀ x : FourSphere, ∀ z : Twistor, z ∈ twistorLine x →
      ∃ p : ComplexProjectiveLine, twistorLineParam x p = z
  twistorLine_eq_fiber :
    ∀ x : FourSphere, twistorLine x = {z : Twistor | projection z = x}
  fiberProjectiveLineEquiv :
    ∀ x : FourSphere, TwistorFiber projection x ≃ ComplexProjectiveLine
  realStructure : Twistor ≃ₜ Twistor
  realStructure_involutive : Function.Involutive realStructure
  realStructure_preserves_fibers :
    ∀ z : Twistor, projection (realStructure z) = projection z
  incidence : FourSphere → Twistor → Prop
  incidence_iff_mem_twistorLine :
    ∀ x : FourSphere, ∀ z : Twistor, incidence x z ↔ z ∈ twistorLine x

namespace TwistorSpaceOverFourSphereAPI

/-- The parametrization of a twistor line has exactly the declared line as range. -/
theorem twistorLineParam_range {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) (x : FourSphere) :
    Set.range (T.twistorLineParam x) = T.twistorLine x := by
  ext z
  constructor
  · rintro ⟨p, rfl⟩
    exact T.twistorLineParam_mem x p
  · intro hz
    exact T.twistorLineParam_surjective x z hz

/-- Membership in the twistor line is equivalent to lying in the projection fiber. -/
theorem mem_twistorLine_iff_projection_eq {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) (x : FourSphere) (z : Twistor) :
    z ∈ T.twistorLine x ↔ T.projection z = x := by
  rw [T.twistorLine_eq_fiber x]
  rfl

/-- Incidence is the same as the projection-fiber relation in this API boundary. -/
theorem incidence_iff_projection_eq {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) (x : FourSphere) (z : Twistor) :
    T.incidence x z ↔ T.projection z = x :=
  (T.incidence_iff_mem_twistorLine x z).trans
    (mem_twistorLine_iff_projection_eq T x z)

/-- The line carrier and the projection fiber are definitionally aligned by the API. -/
def twistorLineEquivFiber {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) (x : FourSphere) :
    TwistorLineCarrier T.twistorLine x ≃ TwistorFiber T.projection x where
  toFun z := ⟨z.1, (mem_twistorLine_iff_projection_eq T x z.1).1 z.2⟩
  invFun z := ⟨z.1, (mem_twistorLine_iff_projection_eq T x z.1).2 z.2⟩
  left_inv z := Subtype.ext (by rfl)
  right_inv z := Subtype.ext (by rfl)

/-- Twistor lines are projective lines in the selected `CP^1` model. -/
def twistorLineEquivProjectiveLine {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) (x : FourSphere) :
    TwistorLineCarrier T.twistorLine x ≃ ComplexProjectiveLine :=
  (twistorLineEquivFiber T x).trans (T.fiberProjectiveLineEquiv x)

/-- Projection fibers are projective lines in the selected `CP^1` model. -/
theorem twistorFiber_equiv_projectiveLine {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) (x : FourSphere) :
    Nonempty (TwistorFiber T.projection x ≃ ComplexProjectiveLine) :=
  ⟨T.fiberProjectiveLineEquiv x⟩

/-- The real structure is involutive. -/
theorem realStructure_apply_apply {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) (z : Twistor) :
    T.realStructure (T.realStructure z) = z :=
  T.realStructure_involutive z

/-- The real structure preserves each projection fiber. -/
theorem realStructure_mem_fiber {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) {x : FourSphere} {z : Twistor}
    (hz : T.projection z = x) :
    T.projection (T.realStructure z) = x := by
  rw [T.realStructure_preserves_fibers z]
  exact hz

end TwistorSpaceOverFourSphereAPI

/--
Gauge-theoretic input data for an instanton.

The fields `antiSelfDualCurvature`, `yangMillsEquation`, and
`finiteYangMillsAction` mark the analytic/gauge-theory boundary that is not
available as a terminal mathlib theorem in this snapshot.
-/
structure GaugeInstantonData (Base : Type u) [TopologicalSpace Base] :
    Type (u + 1) where
  gaugeGroup : Type u
  principalBundle : Type u
  connection : Type u
  curvature : Type u
  smoothConnection : Prop
  antiSelfDualCurvature : Prop
  yangMillsEquation : Prop
  finiteYangMillsAction : Prop
  chargeOrFramingFixed : Prop

/--
Holomorphic bundle-side data over twistor space.

The `twistorScheme` field uses mathlib's `AlgebraicGeometry.Scheme` as a
checked algebraic-geometry anchor.  The holomorphic-vector-bundle and
line-triviality predicates remain abstract until a concrete API is available.
-/
structure HolomorphicTwistorBundleData (Twistor : Type u)
    [TopologicalSpace Twistor] : Type (u + 1) where
  twistorScheme : Scheme.{u}
  vectorBundleCarrier : Type u
  rank : ℕ
  charge : ℤ
  holomorphicStructure : Prop
  trivialOnTwistorLines : Prop
  realityCondition : Prop
  stabilityOrFraming : Prop

/--
Refined holomorphic vector-bundle boundary over twistor space.

`moduleSheaf` is the strongest available checked algebraic-geometry anchor in
this mathlib snapshot: a sheaf of modules on a scheme.  The analytic
holomorphic-vector-bundle structure and local-freeness hypotheses remain
explicit proposition fields until a concrete twistor-space bundle API is
available.
-/
structure HolomorphicVectorBundleOnTwistorSpace (Twistor : Type u)
    [TopologicalSpace Twistor] : Type (u + 1) where
  twistorScheme : Scheme.{u}
  moduleSheaf : twistorScheme.Modules
  totalSpace : Type u
  projection : totalSpace → Twistor
  fiber : Twistor → Type u
  rank : ℕ
  charge : ℤ
  holomorphicStructure : Prop
  locallyFreeFiniteRank : Prop
  vectorBundleProjectionCompatible : Prop

/-- The carrier of the restriction of a twistor bundle to one twistor line. -/
abbrev TwistorLineBundleRestriction {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) (x : FourSphere) :
    Type u :=
  (z : TwistorLineCarrier T.twistorLine x) → E.fiber z.1

/-- Trivialization data for the restriction of a bundle to one twistor line. -/
structure TwistorLineBundleTrivialization {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) (x : FourSphere) :
    Type (u + 1) where
  modelFiber : Type u
  fiberEquiv : ∀ z : TwistorLineCarrier T.twistorLine x, E.fiber z.1 ≃ modelFiber
  holomorphicAlongLine : Prop
  rankCompatible : Prop

/-- The restriction of a holomorphic twistor bundle to a fixed twistor line is trivial. -/
def TrivialOnTwistorLine {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) (x : FourSphere) : Prop :=
  Nonempty (TwistorLineBundleTrivialization T E x)

/-- The Ward-transform line-triviality condition: trivial on every twistor line. -/
def TrivialOnAllTwistorLines {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) : Prop :=
  ∀ x : FourSphere, TrivialOnTwistorLine T E x

/-- Line-triviality unfolds to a trivialization over each twistor line. -/
theorem trivialOnAllTwistorLines_iff {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) :
    TrivialOnAllTwistorLines T E ↔
      ∀ x : FourSphere, Nonempty (TwistorLineBundleTrivialization T E x) :=
  Iff.rfl

/-- A globally line-trivial bundle is trivial on any selected twistor line. -/
theorem trivialOnTwistorLine_of_trivialOnAll {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {E : HolomorphicVectorBundleOnTwistorSpace Twistor}
    (hE : TrivialOnAllTwistorLines T E) (x : FourSphere) :
    TrivialOnTwistorLine T E x :=
  hE x

/--
Reality condition for a holomorphic twistor bundle.

The fields are proposition-with-witness boundaries for compatibility with the
twistor real structure, anti-linearity on fibers, and involutivity of the lifted
real structure.
-/
structure BundleRealityCondition {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) : Type (u + 1) where
  conjugatePullbackCompatible : Prop
  conjugatePullbackCompatible_holds : conjugatePullbackCompatible
  antiLinearOnFibers : Prop
  antiLinearOnFibers_holds : antiLinearOnFibers
  involutiveLift : Prop
  involutiveLift_holds : involutiveLift

/-- Stability/framing package for the bundle side of the correspondence. -/
structure BundleStabilityFraming {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) : Type (u + 1) where
  stableOrPolystable : Prop
  stableOrPolystable_holds : stableOrPolystable
  framingAlongInfinity : Prop
  framingAlongInfinity_holds : framingAlongInfinity
  framingCompatibleWithReality : Prop
  framingCompatibleWithReality_holds : framingCompatibleWithReality

/--
Bundle-side API for `THM-M-1543.bundle-api`.

This packages the holomorphic vector bundle, its restrictions to twistor lines,
the line-triviality condition, reality condition, and stability/framing data.
-/
structure HolomorphicTwistorBundleAPI {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor) : Type (u + 1) where
  bundle : HolomorphicVectorBundleOnTwistorSpace Twistor
  trivialOnTwistorLines : TrivialOnAllTwistorLines T bundle
  reality : BundleRealityCondition T bundle
  stabilityFraming : BundleStabilityFraming T bundle

namespace HolomorphicTwistorBundleAPI

/-- Forget the refined bundle API back to the older statement-shape bundle data. -/
def toData {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (A : HolomorphicTwistorBundleAPI T) : HolomorphicTwistorBundleData Twistor where
  twistorScheme := A.bundle.twistorScheme
  vectorBundleCarrier := A.bundle.totalSpace
  rank := A.bundle.rank
  charge := A.bundle.charge
  holomorphicStructure := A.bundle.holomorphicStructure
  trivialOnTwistorLines := TrivialOnAllTwistorLines T A.bundle
  realityCondition := Nonempty (BundleRealityCondition T A.bundle)
  stabilityOrFraming := Nonempty (BundleStabilityFraming T A.bundle)

/-- The forgetful map preserves the line-triviality witness. -/
theorem toData_trivialOnTwistorLines {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (A : HolomorphicTwistorBundleAPI T) :
    A.toData.trivialOnTwistorLines :=
  A.trivialOnTwistorLines

/-- The forgetful map records the reality witness as nonempty data. -/
theorem toData_realityCondition {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (A : HolomorphicTwistorBundleAPI T) :
    A.toData.realityCondition :=
  ⟨A.reality⟩

/-- The forgetful map records the stability/framing witness as nonempty data. -/
theorem toData_stabilityOrFraming {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (A : HolomorphicTwistorBundleAPI T) :
    A.toData.stabilityOrFraming :=
  ⟨A.stabilityFraming⟩

end HolomorphicTwistorBundleAPI

/--
Moduli equivalence relation for holomorphic twistor bundles.

The actual equivalence should be isomorphism preserving holomorphic structure,
line triviality, reality, and framing.  This structure records that relation and
the invariance laws needed by the correspondence without pretending that the
concrete quotient moduli stack has already been constructed.
-/
structure HolomorphicTwistorBundleModuliRelation {Twistor : Type u}
    [TopologicalSpace Twistor] (T : TwistorSpaceOverFourSphereAPI Twistor) :
    Type (u + 1) where
  equivalent :
    HolomorphicVectorBundleOnTwistorSpace Twistor →
      HolomorphicVectorBundleOnTwistorSpace Twistor → Prop
  isEquivalence : Equivalence equivalent
  preservesRank :
    ∀ {E F : HolomorphicVectorBundleOnTwistorSpace Twistor},
      equivalent E F → E.rank = F.rank
  preservesCharge :
    ∀ {E F : HolomorphicVectorBundleOnTwistorSpace Twistor},
      equivalent E F → E.charge = F.charge
  preservesLineTriviality :
    ∀ {E F : HolomorphicVectorBundleOnTwistorSpace Twistor},
      equivalent E F → TrivialOnAllTwistorLines T E → TrivialOnAllTwistorLines T F
  preservesReality :
    ∀ {E F : HolomorphicVectorBundleOnTwistorSpace Twistor},
      equivalent E F → BundleRealityCondition T E → BundleRealityCondition T F
  preservesStabilityFraming :
    ∀ {E F : HolomorphicVectorBundleOnTwistorSpace Twistor},
      equivalent E F → BundleStabilityFraming T E → BundleStabilityFraming T F

namespace HolomorphicTwistorBundleModuliRelation

/-- Moduli equivalence is reflexive. -/
theorem refl {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (M : HolomorphicTwistorBundleModuliRelation T)
    (E : HolomorphicVectorBundleOnTwistorSpace Twistor) :
    M.equivalent E E :=
  M.isEquivalence.refl E

/-- Moduli equivalence is symmetric. -/
theorem symm {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (M : HolomorphicTwistorBundleModuliRelation T)
    {E F : HolomorphicVectorBundleOnTwistorSpace Twistor}
    (hEF : M.equivalent E F) :
    M.equivalent F E :=
  M.isEquivalence.symm hEF

/-- Moduli equivalence is transitive. -/
theorem trans {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (M : HolomorphicTwistorBundleModuliRelation T)
    {E F G : HolomorphicVectorBundleOnTwistorSpace Twistor}
    (hEF : M.equivalent E F) (hFG : M.equivalent F G) :
    M.equivalent E G :=
  M.isEquivalence.trans hEF hFG

/-- Rank descends to bundle-side moduli classes in the abstract relation. -/
theorem rank_eq_of_equivalent {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (M : HolomorphicTwistorBundleModuliRelation T)
    {E F : HolomorphicVectorBundleOnTwistorSpace Twistor}
    (hEF : M.equivalent E F) :
    E.rank = F.rank :=
  M.preservesRank hEF

/-- Charge descends to bundle-side moduli classes in the abstract relation. -/
theorem charge_eq_of_equivalent {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    (M : HolomorphicTwistorBundleModuliRelation T)
    {E F : HolomorphicVectorBundleOnTwistorSpace Twistor}
    (hEF : M.equivalent E F) :
    E.charge = F.charge :=
  M.preservesCharge hEF

end HolomorphicTwistorBundleModuliRelation

/--
Repo-local boundary for `THM-M-1543.transform`.

This is the strongest transform-level API that can be checked in the current
repository without pretending to construct the classical Ward transform.  It
names both transforms on the refined instanton and bundle boundaries, records
that they respect the gauge and bundle moduli relations, records the two inverse
laws on moduli representatives, and compares the gauge-side charge with the
integer bundle charge through an explicit normalization map.
-/
structure WardTransformAPI {Twistor : Type u} [TopologicalSpace Twistor]
    (T : TwistorSpaceOverFourSphereAPI Twistor)
    (GaugeGroup Connection Curvature Charge Framing : Type u)
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    (D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing)
    (M : HolomorphicTwistorBundleModuliRelation T) : Type (u + 1) where
  chargeToInteger : Charge → ℤ
  instantonToBundle :
    (A : Connection) → A ∈ antiSelfDualFiniteActionConnections D →
      HolomorphicTwistorBundleAPI T
  bundleToInstanton : HolomorphicTwistorBundleAPI T → Connection
  bundleToInstanton_mem :
    ∀ E : HolomorphicTwistorBundleAPI T,
      bundleToInstanton E ∈ antiSelfDualFiniteActionConnections D
  instantonToBundle_respects_gauge :
    ∀ {A B : Connection}
      (hA : A ∈ antiSelfDualFiniteActionConnections D)
      (hB : B ∈ antiSelfDualFiniteActionConnections D),
        GaugeEquivalent (GaugeGroup := GaugeGroup) A B →
          M.equivalent (instantonToBundle A hA).bundle
            (instantonToBundle B hB).bundle
  bundleToInstanton_respects_equiv :
    ∀ {E F : HolomorphicTwistorBundleAPI T},
      M.equivalent E.bundle F.bundle →
        GaugeEquivalent (GaugeGroup := GaugeGroup) (bundleToInstanton E)
          (bundleToInstanton F)
  bundleToInstanton_left_inverse :
    ∀ {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D),
      GaugeEquivalent (GaugeGroup := GaugeGroup)
        (bundleToInstanton (instantonToBundle A hA)) A
  instantonToBundle_right_inverse :
    ∀ E : HolomorphicTwistorBundleAPI T,
      M.equivalent
        (instantonToBundle (bundleToInstanton E) (bundleToInstanton_mem E)).bundle
        E.bundle
  instantonToBundle_charge :
    ∀ {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D),
      (instantonToBundle A hA).bundle.charge = chargeToInteger (D.charge A)
  bundleToInstanton_charge :
    ∀ E : HolomorphicTwistorBundleAPI T,
      chargeToInteger (D.charge (bundleToInstanton E)) = E.bundle.charge

namespace WardTransformAPI

/-- The instanton-to-bundle transform lands in line-trivial twistor bundles. -/
theorem instantonToBundle_trivialOnTwistorLines
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D) :
    TrivialOnAllTwistorLines T (W.instantonToBundle A hA).bundle :=
  (W.instantonToBundle A hA).trivialOnTwistorLines

/-- The instanton-to-bundle transform supplies the bundle reality condition. -/
def instantonToBundle_reality
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D) :
    BundleRealityCondition T (W.instantonToBundle A hA).bundle :=
  (W.instantonToBundle A hA).reality

/-- The instanton-to-bundle transform supplies the stability/framing package. -/
def instantonToBundle_stabilityFraming
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D) :
    BundleStabilityFraming T (W.instantonToBundle A hA).bundle :=
  (W.instantonToBundle A hA).stabilityFraming

/-- The bundle-to-instanton transform lands in ASD finite-action connections. -/
theorem bundleToInstanton_mem_asdFiniteAction
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    (E : HolomorphicTwistorBundleAPI T) :
    W.bundleToInstanton E ∈ antiSelfDualFiniteActionConnections D :=
  W.bundleToInstanton_mem E

/-- The instanton-to-bundle transform descends along gauge equivalence. -/
theorem instantonToBundle_equivalent_of_gaugeEquivalent
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {A B : Connection}
    (hA : A ∈ antiSelfDualFiniteActionConnections D)
    (hB : B ∈ antiSelfDualFiniteActionConnections D)
    (hAB : GaugeEquivalent (GaugeGroup := GaugeGroup) A B) :
    M.equivalent (W.instantonToBundle A hA).bundle
      (W.instantonToBundle B hB).bundle :=
  W.instantonToBundle_respects_gauge hA hB hAB

/-- The bundle-to-instanton transform descends along bundle moduli equivalence. -/
theorem bundleToInstanton_gaugeEquivalent_of_equivalent
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {E F : HolomorphicTwistorBundleAPI T}
    (hEF : M.equivalent E.bundle F.bundle) :
    GaugeEquivalent (GaugeGroup := GaugeGroup) (W.bundleToInstanton E)
      (W.bundleToInstanton F) :=
  W.bundleToInstanton_respects_equiv hEF

/-- Moduli-level left inverse law for the bundle-to-instanton transform. -/
theorem bundleToInstanton_left_inverse_moduli
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D) :
    GaugeEquivalent (GaugeGroup := GaugeGroup)
      (W.bundleToInstanton (W.instantonToBundle A hA)) A :=
  W.bundleToInstanton_left_inverse hA

/-- Moduli-level right inverse law for the instanton-to-bundle transform. -/
theorem instantonToBundle_right_inverse_moduli
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    (E : HolomorphicTwistorBundleAPI T) :
    M.equivalent
      (W.instantonToBundle (W.bundleToInstanton E)
        (W.bundleToInstanton_mem E)).bundle
      E.bundle :=
  W.instantonToBundle_right_inverse E

/-- Charge compatibility for the instanton-to-bundle transform. -/
theorem instantonToBundle_charge_eq
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D) :
    (W.instantonToBundle A hA).bundle.charge = W.chargeToInteger (D.charge A) :=
  W.instantonToBundle_charge hA

/-- Charge compatibility for the bundle-to-instanton transform. -/
theorem bundleToInstanton_charge_eq
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    (E : HolomorphicTwistorBundleAPI T) :
    W.chargeToInteger (D.charge (W.bundleToInstanton E)) = E.bundle.charge :=
  W.bundleToInstanton_charge E

/-- Charge normalization is unchanged by the instanton-to-bundle-to-instanton round trip. -/
theorem charge_roundTrip_instantonToBundleToInstanton
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    {A : Connection} (hA : A ∈ antiSelfDualFiniteActionConnections D) :
    W.chargeToInteger
        (D.charge (W.bundleToInstanton (W.instantonToBundle A hA))) =
      W.chargeToInteger (D.charge A) := by
  rw [W.bundleToInstanton_charge, W.instantonToBundle_charge hA]

/-- Bundle charge is unchanged by the bundle-to-instanton-to-bundle round trip. -/
theorem charge_roundTrip_bundleToInstantonToBundle
    {Twistor : Type u} [TopologicalSpace Twistor]
    {T : TwistorSpaceOverFourSphereAPI Twistor}
    {GaugeGroup Connection Curvature Charge Framing : Type u}
    [Group GaugeGroup] [MulAction GaugeGroup Connection] [AddGroup Curvature]
    {D : AntiSelfDualGaugeAPI GaugeGroup Connection Curvature Charge Framing}
    {M : HolomorphicTwistorBundleModuliRelation T}
    (W : WardTransformAPI T GaugeGroup Connection Curvature Charge Framing D M)
    (E : HolomorphicTwistorBundleAPI T) :
    (W.instantonToBundle (W.bundleToInstanton E)
        (W.bundleToInstanton_mem E)).bundle.charge = E.bundle.charge := by
  rw [W.instantonToBundle_charge, W.bundleToInstanton_charge]

end WardTransformAPI

/--
Hypotheses needed before an Atiyah-Ward correspondence theorem can be stated.

These are intentionally explicit: a terminal proof must replace the abstract
fields by concrete twistor incidence, ASD connection, and holomorphic bundle
definitions or by a pinned upstream theorem.
-/
def AtiyahWardHypotheses
    {Base Twistor : Type u} [TopologicalSpace Base] [TopologicalSpace Twistor]
    (T : TwistorModel Base Twistor)
    (I : GaugeInstantonData Base)
    (B : HolomorphicTwistorBundleData Twistor) : Prop :=
  T.baseIsFourManifold ∧
    T.twistorHasComplexStructure ∧
      T.twistorLinesAreProjectiveLines ∧
        T.realStructure ∧
          T.incidenceRelation ∧
            I.smoothConnection ∧
              I.antiSelfDualCurvature ∧
                I.yangMillsEquation ∧
                  I.finiteYangMillsAction ∧
                    I.chargeOrFramingFixed ∧
                      B.holomorphicStructure ∧
                        B.trivialOnTwistorLines ∧
                          B.realityCondition ∧
                            B.stabilityOrFraming

/--
Output package for the correspondence.

It records the two transforms and the moduli-level inverse laws as proposition
fields.  A future terminal formalization should replace these fields by
concrete equivalences between quotient moduli spaces.
-/
structure AtiyahWardCorrespondencePackage
    {Base Twistor : Type u} [TopologicalSpace Base] [TopologicalSpace Twistor]
    (T : TwistorModel Base Twistor)
    (I : GaugeInstantonData Base)
    (B : HolomorphicTwistorBundleData Twistor) : Type (u + 1) where
  instantonToBundle :
    GaugeInstantonData Base → HolomorphicTwistorBundleData Twistor
  bundleToInstanton :
    HolomorphicTwistorBundleData Twistor → GaugeInstantonData Base
  transformPreservesASD : Prop
  transformPreservesASD_holds : transformPreservesASD
  transformPreservesLineTriviality : Prop
  transformPreservesLineTriviality_holds : transformPreservesLineTriviality
  inverseOnInstantonModuli : Prop
  inverseOnInstantonModuli_holds : inverseOnInstantonModuli
  inverseOnBundleModuli : Prop
  inverseOnBundleModuli_holds : inverseOnBundleModuli
  chargeCompatibility : Prop
  chargeCompatibility_holds : chargeCompatibility

/--
Public statement-normalization note for `THM-M-1543.statement`.

`StatementShape` is the current repo-local Lean boundary for the
Atiyah-Ward correspondence.  It packages the intended transform data behind
abstract gauge, twistor, and bundle-side hypotheses, but it is not a terminal
Atiyah-Ward proof.
-/
def statementNormalizationNote : String :=
  "THM-M-1543.statement normalization: " ++
    "`AwesomeTheorems.Stage1.S1_M_179.StatementShape` is the current " ++
      "repo-local Lean boundary for the Atiyah-Ward correspondence. It " ++
        "packages the expected transform data behind abstract gauge, " ++
          "twistor, and bundle-side hypotheses and checked mathlib anchors, " ++
            "but it is not a terminal Atiyah-Ward proof. The ASD gauge API, " ++
              "twistor incidence model, holomorphic bundle " ++
                "triviality/reality conditions, Ward transform, inverse " ++
                  "laws on moduli classes, and charge compatibility remain " ++
                    "formalization debt until concrete definitions or a " ++
                      "pinned/imported/checked upstream Lean 4 theorem close them."

/--
Normalized Stage1 statement shape for the Atiyah-Ward correspondence.

Given an abstract four-dimensional twistor model, instanton data, and
holomorphic twistor-bundle data satisfying the listed hypotheses, there should
exist a correspondence package whose transforms preserve ASD/bundle conditions
and are inverse on the intended moduli classes.  This is a formalization
boundary, not a proof of the Atiyah-Ward theorem.
-/
def StatementShape : Prop :=
  ∀ (Base Twistor : Type u) [TopologicalSpace Base] [TopologicalSpace Twistor]
    (T : TwistorModel Base Twistor)
    (I : GaugeInstantonData Base)
    (B : HolomorphicTwistorBundleData Twistor),
      AtiyahWardHypotheses T I B →
        Nonempty (AtiyahWardCorrespondencePackage T I B)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Base Twistor : Type u) [TopologicalSpace Base] [TopologicalSpace Twistor]
      (T : TwistorModel Base Twistor)
      (I : GaugeInstantonData Base)
      (B : HolomorphicTwistorBundleData Twistor),
        AtiyahWardHypotheses T I B →
          Nonempty (AtiyahWardCorrespondencePackage T I B)) :
    StatementShape.{u} :=
  h

/-- A correspondence package exposes its ASD-preservation field. -/
theorem AtiyahWardCorrespondencePackage.preserves_asd
    {Base Twistor : Type u} [TopologicalSpace Base] [TopologicalSpace Twistor]
    {T : TwistorModel Base Twistor}
    {I : GaugeInstantonData Base}
    {B : HolomorphicTwistorBundleData Twistor}
    (P : AtiyahWardCorrespondencePackage T I B) :
    P.transformPreservesASD :=
  P.transformPreservesASD_holds

/-- A correspondence package exposes its line-triviality preservation field. -/
theorem AtiyahWardCorrespondencePackage.preserves_line_triviality
    {Base Twistor : Type u} [TopologicalSpace Base] [TopologicalSpace Twistor]
    {T : TwistorModel Base Twistor}
    {I : GaugeInstantonData Base}
    {B : HolomorphicTwistorBundleData Twistor}
    (P : AtiyahWardCorrespondencePackage T I B) :
    P.transformPreservesLineTriviality :=
  P.transformPreservesLineTriviality_holds

/-- A correspondence package exposes its instanton-side inverse law. -/
theorem AtiyahWardCorrespondencePackage.inverse_on_instantons
    {Base Twistor : Type u} [TopologicalSpace Base] [TopologicalSpace Twistor]
    {T : TwistorModel Base Twistor}
    {I : GaugeInstantonData Base}
    {B : HolomorphicTwistorBundleData Twistor}
    (P : AtiyahWardCorrespondencePackage T I B) :
    P.inverseOnInstantonModuli :=
  P.inverseOnInstantonModuli_holds

/-- A correspondence package exposes its bundle-side inverse law. -/
theorem AtiyahWardCorrespondencePackage.inverse_on_bundles
    {Base Twistor : Type u} [TopologicalSpace Base] [TopologicalSpace Twistor]
    {T : TwistorModel Base Twistor}
    {I : GaugeInstantonData Base}
    {B : HolomorphicTwistorBundleData Twistor}
    (P : AtiyahWardCorrespondencePackage T I B) :
    P.inverseOnBundleModuli :=
  P.inverseOnBundleModuli_holds

/-- A correspondence package exposes its charge-compatibility field. -/
theorem AtiyahWardCorrespondencePackage.charge_compatibility
    {Base Twistor : Type u} [TopologicalSpace Base] [TopologicalSpace Twistor]
    {T : TwistorModel Base Twistor}
    {I : GaugeInstantonData Base}
    {B : HolomorphicTwistorBundleData Twistor}
    (P : AtiyahWardCorrespondencePackage T I B) :
    P.chargeCompatibility :=
  P.chargeCompatibility_holds

/-- The standard four-sphere has the smooth manifold instance supplied by mathlib. -/
theorem fourSphere_isManifold_anchor :
    IsManifold (𝓡 4) ⊤ FourSphere :=
  inferInstance

/-- Generic smooth-sphere inclusion anchor from mathlib's sphere manifold file. -/
theorem sphere_inclusion_contMDiff_anchor
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {n : ℕ} [Fact (Module.finrank ℝ E = n + 1)] :
    ContMDiff (𝓡 n) 𝓘(ℝ, E) ⊤
      ((↑) : Metric.sphere (0 : E) 1 → E) :=
  contMDiff_coe_sphere

/-- A point of `CP^3` has a nonzero representative in `ℂ^4`. -/
theorem complexProjectiveThree_rep_nonzero
    (p : ComplexProjectiveThree) :
    Projectivization.rep p ≠ 0 :=
  Projectivization.rep_nonzero p

/-- Checked analytic anchor: the identity map on complex four-space is analytic. -/
theorem complexProjectiveAffine_identity_analytic :
    AnalyticOn ℂ (fun z : Fin 4 → ℂ => z) Set.univ :=
  analyticOn_id

/-- Checked algebraic-geometry anchor: every mathlib scheme has an identity morphism. -/
def schemeIdentityAnchor (X : Scheme.{u}) : X ⟶ X :=
  𝟙 X

/-- Checked Riemannian anchor available for finite-dimensional vector-space models. -/
def euclideanRiemannianMetric_anchor :
    Bundle.ContMDiffRiemannianMetric 𝓘(ℝ, EuclideanSpace ℝ (Fin 4)) ⊤
      (EuclideanSpace ℝ (Fin 4))
      (fun x : EuclideanSpace ℝ (Fin 4) =>
        TangentSpace 𝓘(ℝ, EuclideanSpace ℝ (Fin 4)) x) :=
  riemannianMetricVectorSpace (EuclideanSpace ℝ (Fin 4))

/-- Pinned mathlib revision used for the Stage1 Atiyah-Ward module audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
mathlib modules checked while locating repo-local Atiyah-Ward anchors.

The `ProjectiveSpectrum.*` public-doc shorthand is expanded here to the concrete
modules present in the pinned checkout.
-/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Instances.Sphere",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.LinearAlgebra.Projectivization.Basic",
  "Mathlib.LinearAlgebra.Projectivization.Subspace",
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Functor",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Scheme",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.StructureSheaf",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Topology",
  "Mathlib.AlgebraicGeometry.Modules.Sheaf",
  "Mathlib.Analysis.Analytic.Basic"
]

/-- Search terms that did not locate a terminal Atiyah-Ward theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "AtiyahWard",
  "Atiyah-Ward",
  "Atiyah Ward",
  "instanton",
  "Yang-Mills",
  "YangMills",
  "Twistor",
  "twistor",
  "AntiSelfDual",
  "anti-self-dual",
  "SelfDual",
  "self-dual",
  "ASD",
  "trivialOnTwistorLines"
]

/-- Exact external Lean 4 search terms requested for the Atiyah-Ward audit. -/
def externalAuditSearchTerms : List String := [
  "AtiyahWard",
  "\"Atiyah-Ward\"",
  "\"Atiyah Ward\"",
  "instanton",
  "YangMills",
  "\"Yang-Mills\"",
  "Twistor",
  "twistor",
  "AntiSelfDual",
  "SelfDual",
  "ASD",
  "trivialOnTwistorLines"
]

/--
Machine-readable row for external Lean 4 source-search candidates.

The `lakeDependencyFeasibility` field records whether a candidate could plausibly
enter this repository's Lake closure for `THM-M-1543`; it is not a completion
claim.
-/
structure ExternalLeanAuditCandidate where
  repository : String
  commit : String
  toolchain : String
  modulePath : String
  relevantNames : List String
  matchedTerms : List String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  closureStatus : String

/--
External audit authentication status for `THM-M-1543.external-audit`.

`gh auth status` reported no logged-in GitHub host in this local worker
environment on 2026-05-01, and GitHub REST code search was rate-limited without
authentication.  The candidate rows therefore record primary-source fallback
inspection by direct repository URL/commit, not an authenticated GitHub code
search completion.
-/
def externalAuditAuthenticationStatus : String :=
  "blocked: no authenticated GitHub session available to this worker; " ++
    "fallback primary-source repository inspection was used for candidate rows"

/-- External Lean 4 candidates found during the Atiyah-Ward source audit. -/
def externalLeanAuditCandidates : List ExternalLeanAuditCandidate := [
  {
    repository := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems"
    commit := "540da94826f70f3edf4d4fc66ce6cda20e903f61"
    toolchain := "leanprover/lean4:v4.26.0"
    modulePath := "Problems/YangMills/Millennium.lean; Problems/YangMills/Quantum.lean"
    relevantNames := [
      "MillenniumYangMills.YangMillsExistenceAndMassGap",
      "MillenniumYangMillsDefs.QuantumYangMillsTheory",
      "MillenniumYangMillsDefs.YangMillsAction",
      "MillenniumYangMillsDefs.GaugeField"
    ]
    matchedTerms := ["YangMills"]
    placeholderStatus :=
      "relevant YangMills files contain no proof-placeholder keyword matches in local scan"
    lakeDependencyFeasibility :=
      "not feasible as a THM-M-1543 dependency without a statement bridge; " ++
        "uses Lean 4.26/mathlib v4.26.0 while this repo uses Lean 4.29/mathlib " ++
          mathlibPinnedRevision
    closureStatus :=
      "adjacent Yang-Mills statement scaffolding only; no Atiyah-Ward, twistor, " ++
        "instanton, ASD curvature, or trivial-on-twistor-lines closure"
  },
  {
    repository := "https://github.com/the-omega-institute/automath"
    commit := "605f51d73d0ccf42d89352da7cde5199124fbd4a"
    toolchain := "leanprover/lean4:v4.28.0"
    modulePath := "lean4/Omega/Zeta/SelfdualSSFodd.lean"
    relevantNames := [
      "Omega.Zeta.selfdual_ssf_odd_data",
      "Omega.Zeta.paper_selfdual_ssf_odd"
    ]
    matchedTerms := ["SelfDual"]
    placeholderStatus := "inspected file contains no proof-placeholder keyword matches"
    lakeDependencyFeasibility :=
      "not feasible for THM-M-1543; name match is about self-dual scattering " ++
        "phase/spectral-shift data, not ASD Yang-Mills instantons or twistor bundles"
    closureStatus :=
      "false positive for this theorem; no Atiyah-Ward or Ward transform content"
  }
]

/-- No external Lean 4 candidate in this audit closes the Atiyah-Ward correspondence. -/
def externalAtiyahWardClosureStatus : String :=
  "not_found_not_repo_local_closed"

/-! ## Repo-local integration gate -/

/--
Machine-readable integration gate for external Lean 4 Atiyah-Ward closures.

This records the M0387 rule used by `THM-M-1543.integration-gate`: external
anchor-only evidence is not completion evidence.  A future external proof can
close this gate only after it is pinned or vendored, imported by this
repository, and checked by a repo-local Lean validation command.  If a terminal
external proof is found but cannot be integrated, the blocker must name the
repository, commit, module/theorem, toolchain mismatch or license/dependency
conflict, and the next condition needed before a public completion claim.
-/
structure ExternalAtiyahWardIntegrationGate where
  childTask : String
  acceptedExternalClosureFound : Bool
  closurePinnedOrVendored : Bool
  closureImportedInRepo : Bool
  repoLocalValidationPassedForClosure : Bool
  anchorOnlyEvidenceMarkedCompleted : Bool
  completedStateHasRepoLocalIntegrationDebt : Bool
  publicCompletionAllowed : Bool
  terminalMachineStatus : String
  terminalDebtClass : String
  acceptedCompletionEvidence : List String
  rejectedCompletionEvidence : List String
  integrationBlocker : String

/--
Current C008 integration decision for `THM-M-1543`.

The fallback external audit records only adjacent or false-positive Lean 4
candidates, not a terminal Atiyah-Ward correspondence theorem.  Therefore no
external proof is accepted, no Lake dependency is added, and public status
surfaces must remain open.
-/
def atiyahWardIntegrationGate : ExternalAtiyahWardIntegrationGate where
  childTask := "S1-M-179-C008"
  acceptedExternalClosureFound := false
  closurePinnedOrVendored := false
  closureImportedInRepo := false
  repoLocalValidationPassedForClosure := false
  anchorOnlyEvidenceMarkedCompleted := false
  completedStateHasRepoLocalIntegrationDebt := false
  publicCompletionAllowed := false
  terminalMachineStatus := "not_repo_local_closed"
  terminalDebtClass := "formalization_debt"
  acceptedCompletionEvidence := [
    "local_proof_body",
    "local_wrapper_upstream_mathlib",
    "external_upstream_pinned"
  ]
  rejectedCompletionEvidence := [
    "external_upstream_anchor_only",
    "adjacent Yang-Mills scaffolding without Atiyah-Ward theorem",
    "SelfDual name matches outside four-dimensional ASD Yang-Mills/twistor geometry",
    "repo_local_integration_debt"
  ]
  integrationBlocker :=
    "no terminal external Lean 4 Atiyah-Ward correspondence closure is " ++
      "accepted from the available audit; `gh auth status` reports no " ++
        "logged-in GitHub host in this worker, and fallback source inspection " ++
          "found only non-closing candidates. Before any public completion " ++
            "claim, rerun authenticated code search and either pin/import/check " ++
              "a terminal theorem in this repository or record a concrete " ++
                "repo/commit/module/theorem/toolchain integration blocker."

/-- C008 rejects anchor-only completion and residual repo-local integration debt. -/
theorem atiyahWardIntegrationGate_noAnchorOnlyCompletion :
    atiyahWardIntegrationGate.anchorOnlyEvidenceMarkedCompleted = false ∧
      atiyahWardIntegrationGate.completedStateHasRepoLocalIntegrationDebt = false ∧
        atiyahWardIntegrationGate.publicCompletionAllowed = false := by
  simp [atiyahWardIntegrationGate]

/-- C008 records that no external Atiyah-Ward closure has been checked repo-locally. -/
theorem atiyahWardIntegrationGate_noExternalClosureChecked :
    atiyahWardIntegrationGate.acceptedExternalClosureFound = false ∧
      atiyahWardIntegrationGate.closurePinnedOrVendored = false ∧
        atiyahWardIntegrationGate.closureImportedInRepo = false ∧
          atiyahWardIntegrationGate.repoLocalValidationPassedForClosure = false := by
  simp [atiyahWardIntegrationGate]

/-- C008 records the current terminal machine status and debt class. -/
theorem atiyahWardIntegrationGate_status_eq :
    atiyahWardIntegrationGate.terminalMachineStatus = "not_repo_local_closed" ∧
      atiyahWardIntegrationGate.terminalDebtClass = "formalization_debt" := by
  simp [atiyahWardIntegrationGate]

/-- C008 repo-local integration-debt gate result for the child ledger. -/
def atiyahWardIntegrationGateResult : String :=
  "pass for non-completion: no terminal external Atiyah-Ward Lean 4 proof " ++
    "has been accepted or checked in this repository, so no " ++
      "repo_local_integration_debt is being claimed as completed; public " ++
        "statuses must remain open until local_proof_body, " ++
          "local_wrapper_upstream_mathlib, or external_upstream_pinned " ++
            "evidence validates in this repo"

/--
Public backfill text for the C008 integration gate.

This is static text for a later serial public-doc integrator; this worker does
not edit shared public planning documents.
-/
def atiyahWardIntegrationGateBackfillProposal : String :=
  "S1-M-179-C008: The checked Lean artifact records " ++
    "`ExternalAtiyahWardIntegrationGate` and `atiyahWardIntegrationGate`, " ++
      "with `publicCompletionAllowed := false` and " ++
        "`completedStateHasRepoLocalIntegrationDebt := false`. Current " ++
          "repo-local closure is `not_repo_local_closed`: no terminal external " ++
            "Lean 4 Atiyah-Ward correspondence proof has been accepted, pinned " ++
              "or vendored, imported, and checked in this repository. Keep " ++
                "`THM-M-1543.integration-gate` open and do not mark " ++
                  "`external_upstream_anchor_only` as completed. Completion " ++
                    "evidence is restricted to `local_proof_body`, " ++
                      "`local_wrapper_upstream_mathlib`, or " ++
                        "`external_upstream_pinned`, validated by " ++
                          "`cd Formalizations/Lean && lake env lean " ++
                            "AwesomeTheorems/Stage1/S1_M_179.lean`."

/-! ## Audit probes -/

#check FourSphere
#check ComplexProjectiveThree
#check RealDifferentialForm
#check RealTwoForm
#check HodgeStarOnTwoForms
#check IsAntiSelfDual
#check isAntiSelfDual_zero
#check GaugeEquivalent
#check gaugeEquivalent_refl
#check AntiSelfDualGaugeAPI
#check antiSelfDualFiniteActionConnections
#check yangMills_of_mem_antiSelfDualFiniteActionConnections
#check TwistorModel
#check ComplexProjectiveLine
#check TwistorFiber
#check TwistorSpaceOverFourSphereAPI
#check TwistorSpaceOverFourSphereAPI.incidence_iff_projection_eq
#check TwistorSpaceOverFourSphereAPI.twistorLineEquivProjectiveLine
#check TwistorSpaceOverFourSphereAPI.twistorFiber_equiv_projectiveLine
#check GaugeInstantonData
#check HolomorphicTwistorBundleData
#check HolomorphicVectorBundleOnTwistorSpace
#check TwistorLineBundleRestriction
#check TwistorLineBundleTrivialization
#check TrivialOnAllTwistorLines
#check BundleRealityCondition
#check BundleStabilityFraming
#check HolomorphicTwistorBundleAPI
#check HolomorphicTwistorBundleAPI.toData
#check HolomorphicTwistorBundleModuliRelation
#check HolomorphicTwistorBundleModuliRelation.rank_eq_of_equivalent
#check WardTransformAPI
#check WardTransformAPI.instantonToBundle_trivialOnTwistorLines
#check WardTransformAPI.bundleToInstanton_mem_asdFiniteAction
#check WardTransformAPI.bundleToInstanton_left_inverse_moduli
#check WardTransformAPI.instantonToBundle_right_inverse_moduli
#check WardTransformAPI.instantonToBundle_charge_eq
#check WardTransformAPI.bundleToInstanton_charge_eq
#check WardTransformAPI.charge_roundTrip_instantonToBundleToInstanton
#check WardTransformAPI.charge_roundTrip_bundleToInstantonToBundle
#check AtiyahWardHypotheses
#check AtiyahWardCorrespondencePackage
#check AtiyahWardCorrespondencePackage.charge_compatibility
#check statementNormalizationNote
#check StatementShape
#check mathlibPinnedRevision
#check mathlibAnchorModules
#check externalAuditSearchTerms
#check externalAuditAuthenticationStatus
#check ExternalLeanAuditCandidate
#check externalLeanAuditCandidates
#check externalAtiyahWardClosureStatus
#check ExternalAtiyahWardIntegrationGate
#check atiyahWardIntegrationGate
#check atiyahWardIntegrationGate_noAnchorOnlyCompletion
#check atiyahWardIntegrationGate_noExternalClosureChecked
#check atiyahWardIntegrationGate_status_eq
#check atiyahWardIntegrationGateResult
#check atiyahWardIntegrationGateBackfillProposal
#check fourSphere_isManifold_anchor
#check complexProjectiveThree_rep_nonzero
#check complexProjectiveAffine_identity_analytic
#check schemeIdentityAnchor
#check euclideanRiemannianMetric_anchor

end S1_M_179
end Stage1
end AwesomeTheorems
