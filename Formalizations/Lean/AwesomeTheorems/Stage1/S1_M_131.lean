import Mathlib.Geometry.Manifold.IsManifold.Basic
import Mathlib.Geometry.Manifold.VectorBundle.Basic
import Mathlib.Geometry.Manifold.VectorBundle.Tangent
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.Algebra.LieGroup
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.Topology.FiberBundle.Basic
import Mathlib.Topology.Defs.Induced
import Mathlib.Topology.Compactness.Compact

/-!
# S1-M-131 / THM-M-0184: Donaldson theorem

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
Donaldson theory of moduli spaces of anti-self-dual connections on four
manifolds.

The pinned mathlib snapshot contains manifold, vector-bundle, tangent-bundle,
Lie-group, smooth-map, topology, and inner-product-space substrates.  This file
does not claim a formal proof of Donaldson's theorem: gauge-theoretic
connections, curvature, Hodge star on two-forms, elliptic deformation complexes,
Uhlenbeck compactness, orientation/gluing, and the global ASD moduli-space
theorem are kept as explicit boundary data.
-/

noncomputable section

open Set
open scoped Manifold ContDiff Topology

universe uE uH uM uG uConn uCurv

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_131

/--
Minimal object boundary for a smooth four-manifold in Donaldson theory.

The model-space, smooth-manifold, finite-dimensional, and dimension-four
fields are concrete mathlib APIs: `ModelWithCorners`, `IsManifold`,
`FiniteDimensional`, and `Module.finrank`.  Compactness, orientation, and the
Riemannian metric package remain explicit propositions until the gauge-theory
interfaces below are made concrete.
-/
structure FourManifoldBoundary
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] :
    Type (max (max uE uH) uM) where
  smoothManifold : IsManifold I ∞ M
  finiteDimensionalModel : FiniteDimensional ℝ E
  modelDimension_eq_four : Module.finrank ℝ E = 4
  compactnessHypotheses : Prop
  orientationHypotheses : Prop
  riemannianMetricHypotheses : Prop

/-- The four-manifold boundary exposes a concrete `Module.finrank` dimension target. -/
theorem fourManifoldBoundary_modelDimension_eq_four
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    (B : FourManifoldBoundary E H I M) :
    Module.finrank ℝ E = 4 :=
  B.modelDimension_eq_four

/-- Anti-self-duality for an abstract curvature value and an abstract Hodge star. -/
def IsAntiSelfDual {Curv : Type uCurv} [AddGroup Curv]
    (hodgeStar : Curv → Curv) (F : Curv) : Prop :=
  hodgeStar F = -F

/-- The anti-self-dual predicate unfolds to the expected Hodge-star equation. -/
theorem isAntiSelfDual_iff {Curv : Type uCurv} [AddGroup Curv]
    (hodgeStar : Curv → Curv) (F : Curv) :
    IsAntiSelfDual hodgeStar F ↔ hodgeStar F = -F :=
  Iff.rfl

/-- If the abstract Hodge star preserves zero, then zero curvature is anti-self-dual. -/
theorem isAntiSelfDual_zero {Curv : Type uCurv} [AddGroup Curv]
    (hodgeStar : Curv → Curv) (hzero : hodgeStar 0 = 0) :
    IsAntiSelfDual hodgeStar (0 : Curv) := by
  simp [IsAntiSelfDual, hzero]

/--
The concrete two-form substrate that is available in the pinned mathlib snapshot.

This is only the unbundled normed-vector-space differential-form shape
`E -> E [⋀^Fin 2]→L[ℝ] Ad`.  It is not yet a Donaldson curvature type: the
required adjoint vector bundle over a principal bundle, smooth manifold-valued
two-form package, and Riemannian Hodge star on those two-forms are recorded
below as formalization blockers.
-/
abbrev UnbundledNormedTwoForm
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (Ad : Type uCurv) [NormedAddCommGroup Ad] [NormedSpace ℝ Ad] :
    Type (max uE uCurv) :=
  E → E [⋀^Fin 2]→L[ℝ] Ad

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

/-- Membership in a gauge orbit is exactly gauge equivalence. -/
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
Abstract input data for a Donaldson ASD moduli-space theorem.

The abstract fields mark the current formalization boundary.  A terminal proof
must replace them with concrete APIs for principal bundles, compact Lie
structure groups, smooth connections, curvature as an adjoint-valued two-form,
the Riemannian Hodge star, gauge action, elliptic deformation theory, and
compactification.
-/
structure DonaldsonASDModuliData
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv)
    [Group G] [MulAction G Conn] [AddGroup Curv] :
    Type (max (max (max (max (max uE uH) uM) uG) uConn) uCurv) where
  manifoldBoundary : FourManifoldBoundary E H I M
  principalBundleHypotheses : Prop
  structureGroupHypotheses : Prop
  connectionRegularity : Conn → Prop
  curvature : Conn → Curv
  hodgeStar : Curv → Curv
  hodgeStar_square : ∀ F : Curv, hodgeStar (hodgeStar F) = F
  hodgeStar_neg : ∀ F : Curv, hodgeStar (-F) = -hodgeStar F
  ellipticDeformationComplexHypotheses : Prop
  transversalityHypotheses : Prop
  compactificationHypotheses : Prop

/-- The set of regular anti-self-dual connections for abstract Donaldson data. -/
def asdConnectionSet
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : DonaldsonASDModuliData E H I M G Conn Curv) :
    Set Conn :=
  {A | D.connectionRegularity A ∧ IsAntiSelfDual D.hodgeStar (D.curvature A)}

/-- Membership in the abstract ASD connection set unfolds to regularity plus ASD curvature. -/
theorem mem_asdConnectionSet_iff
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : DonaldsonASDModuliData E H I M G Conn Curv)
    {A : Conn} :
    A ∈ asdConnectionSet D ↔
      D.connectionRegularity A ∧ IsAntiSelfDual D.hodgeStar (D.curvature A) :=
  Iff.rfl

/-- The orbit-level quotient shape for an abstract ASD moduli set. -/
def asdModuliOrbitSet
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : DonaldsonASDModuliData E H I M G Conn Curv) :
    Set (Set Conn) :=
  {O | ∃ A : Conn, A ∈ asdConnectionSet D ∧ gaugeOrbit (G := G) A = O}

/-- Membership in the orbit-level ASD moduli set unfolds to an ASD representative. -/
theorem mem_asdModuliOrbitSet_iff
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : DonaldsonASDModuliData E H I M G Conn Curv)
    {O : Set Conn} :
    O ∈ asdModuliOrbitSet D ↔
      ∃ A : Conn, A ∈ asdConnectionSet D ∧ gaugeOrbit (G := G) A = O :=
  by
    rfl

/-- The gauge orbit of any ASD representative is a point of the abstract orbit moduli set. -/
theorem gaugeOrbit_mem_asdModuliOrbitSet
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : DonaldsonASDModuliData E H I M G Conn Curv)
    {A : Conn} (hA : A ∈ asdConnectionSet D) :
    gaugeOrbit (G := G) A ∈ asdModuliOrbitSet D :=
  ⟨A, hA, rfl⟩

/--
Output contract for a Donaldson ASD moduli-space package.

The fields are propositions rather than proofs of Donaldson theory.  They state
which mathematical interfaces must be supplied by a real proof: quotient
identification, smooth/stratified moduli structure, expected dimension,
orientation, compactification, and use in Donaldson invariants.
-/
structure DonaldsonASDModuliOutput
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : DonaldsonASDModuliData E H I M G Conn Curv) :
    Type (max (max (max (max (max uE uH) uM) uG) uConn) uCurv) where
  orbitSetModel : Set (Set Conn)
  orbitSetModel_eq : orbitSetModel = asdModuliOrbitSet D
  quotientIdentification : Prop
  smoothOrStratifiedStructure : Prop
  expectedDimensionFormula : Prop
  orientationPackage : Prop
  compactificationPackage : Prop
  donaldsonInvariantInterface : Prop

/--
Formula-level statement shape for Donaldson's ASD moduli-space theorem.

For abstract input data satisfying the manifold, bundle, elliptic, transversality,
and compactification hypotheses, there should be a moduli-space package with the
expected quotient and geometric structure.
-/
def DonaldsonASDModuliTheorem
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {G : Type uG} {Conn : Type uConn} {Curv : Type uCurv}
    [Group G] [MulAction G Conn] [AddGroup Curv]
    (D : DonaldsonASDModuliData E H I M G Conn Curv) :
    Prop :=
  Module.finrank ℝ E = 4 →
  D.manifoldBoundary.compactnessHypotheses →
  D.manifoldBoundary.orientationHypotheses →
  D.manifoldBoundary.riemannianMetricHypotheses →
  D.principalBundleHypotheses →
  D.structureGroupHypotheses →
  D.ellipticDeformationComplexHypotheses →
  D.transversalityHypotheses →
  D.compactificationHypotheses →
    Nonempty (DonaldsonASDModuliOutput D)

/--
Stage1 statement-shape candidate for Donaldson's theorem.

This is intentionally a boundary statement rather than a proof.  It quantifies
over mathlib topological/manifold carriers and action data, while leaving the
gauge-theoretic analytical machinery as explicit fields in
`DonaldsonASDModuliData`.
-/
def StatementShape : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (G : Type uG) (Conn : Type uConn) (Curv : Type uCurv)
    [Group G] [MulAction G Conn] [AddGroup Curv],
      ∀ D : DonaldsonASDModuliData E H I M G Conn Curv,
        DonaldsonASDModuliTheorem D

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.ChartedSpace",
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Algebra.LieGroup",
  "Mathlib.Geometry.Manifold.ContMDiffMap",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.Analysis.Calculus.DifferentialForm.VectorField",
  "Mathlib.Topology.FiberBundle.Basic",
  "Mathlib.Topology.Defs.Induced",
  "Mathlib.Topology.Compactness.Compact",
  "Mathlib.LinearAlgebra.Alternating.Basic"
]

/-- Pinned mathlib revision audited for the C002 Donaldson API child task. -/
def auditedMathlibRevision : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Repo-local record of a single mathlib API category audited for Donaldson theory.

`status` is intentionally textual: this is an audit artifact, not a theorem
claim.  The strings below are exact module or declaration names when an API is
present, and exact searched absences when it is not present in the pinned
mathlib snapshot.
-/
structure MathlibAPIAuditEntry where
  category : String
  status : String
  modulesOrDecls : List String
  blocker : String
deriving Repr

/-- C002 audit of the pinned mathlib API surface needed by Donaldson ASD theory. -/
def donaldsonMathlibAPIAudit : List MathlibAPIAuditEntry := [
  { category := "principal-bundle",
    status := "absent as principal-bundle API; only topological fiber-bundle substrate present",
    modulesOrDecls := [
      "Mathlib.Topology.FiberBundle.Basic",
      "FiberBundle",
      "FiberBundleCore",
      "FiberBundle.trivializationAtlas",
      "FiberBundle.trivializationAt",
      "FiberBundle.isQuotientMap_proj"
    ],
    blocker :=
      "No `PrincipalBundle` declaration or `Mathlib.Topology.FiberBundle.Principal` module was found; searched `PrincipalBundle`, `principal bundle`, and principal-bundle file names." },
  { category := "connection",
    status := "partial vector-bundle covariant-derivative API present; no principal/Ehresmann connection API",
    modulesOrDecls := [
      "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
      "IsCovariantDerivativeOn",
      "ContMDiffCovariantDerivativeOn",
      "CovariantDerivative",
      "ContMDiffCovariantDerivative",
      "CovariantDerivative.addOneForm",
      "CovariantDerivative.difference",
      "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
      "IsCovariantDerivativeOn.torsion",
      "CovariantDerivative.torsion"
    ],
    blocker :=
      "The checked connection API is for vector-bundle/Koszul covariant derivatives; the file itself notes a future `CovariantDerivative/Ehresmann.lean`, and no principal-connection API was found." },
  { category := "curvature",
    status := "absent for Donaldson/gauge/Riemannian curvature",
    modulesOrDecls := [],
    blocker :=
      "Searches for `curvature`, `Curvature`, `YangMills`, `AntiSelfDual`, `Donaldson`, and `Uhlenbeck` in Geometry/Analysis/Topology/LinearAlgebra found no usable curvature or ASD gauge-theory declaration." },
  { category := "differential-form",
    status := "partial unbundled normed-space differential-form API present",
    modulesOrDecls := [
      "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
      "Mathlib.Analysis.Calculus.DifferentialForm.VectorField",
      "ContinuousAlternatingMap",
      "extDeriv",
      "extDerivWithin",
      "extDerivWithin_univ",
      "extDeriv_extDeriv",
      "extDeriv_pullback",
      "Mathlib.LinearAlgebra.Alternating.Basic",
      "AlternatingMap"
    ],
    blocker :=
      "The differential-form file represents forms as `E -> E [⋀^Fin n]→L[𝕜] F` on normed spaces and its TODO says bundled smooth forms on manifolds are not defined yet." },
  { category := "hodge-star",
    status := "absent",
    modulesOrDecls := [],
    blocker :=
      "No `Hodge`, `hodge`, `hodgeStar`, or Hodge-star module/declaration was found in the audited mathlib tree." },
  { category := "riemannian-metric",
    status := "Riemannian vector-bundle and Riemannian-manifold substrate present",
    modulesOrDecls := [
      "Mathlib.Topology.VectorBundle.Riemannian",
      "RiemannianMetric",
      "RiemannianBundle",
      "ContinuousRiemannianMetric",
      "ContinuousRiemannianMetric.toRiemannianMetric",
      "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
      "IsContMDiffRiemannianBundle",
      "ContMDiffRiemannianMetric",
      "ContMDiffRiemannianMetric.toRiemannianMetric",
      "Mathlib.Geometry.Manifold.Riemannian.Basic",
      "IsRiemannianManifold",
      "riemannianMetricVectorSpace",
      "EMetricSpace.ofRiemannianMetric"
    ],
    blocker :=
      "This supplies Riemannian metric infrastructure, but not Hodge-star-on-two-forms or ASD curvature interfaces." },
  { category := "quotient",
    status := "general topological quotient maps and bundle projection quotient theorem present",
    modulesOrDecls := [
      "Mathlib.Topology.Defs.Induced",
      "Topology.IsQuotientMap",
      "TopologicalSpace.coinduced",
      "Mathlib.Topology.FiberBundle.Basic",
      "FiberBundle.isQuotientMap_proj",
      "Mathlib.Topology.Algebra.Group.Quotient",
      "MulAction.isOpenQuotientMap_quotientMk"
    ],
    blocker :=
      "No gauge-orbit quotient moduli-space API was found; available quotient facts are generic topological/group-action substrate only." },
  { category := "compactness",
    status := "general topological compactness API present; Uhlenbeck compactness absent",
    modulesOrDecls := [
      "Mathlib.Topology.Defs.Filter",
      "IsCompact",
      "CompactSpace",
      "WeaklyLocallyCompactSpace",
      "LocallyCompactSpace",
      "Mathlib.Topology.Compactness.Compact",
      "isCompact_iff_finite_subcover",
      "isCompact_univ_iff",
      "isCompact_univ"
    ],
    blocker :=
      "No Uhlenbeck compactness, ASD compactification, bubbling, or gauge compactness theorem was found; only general compactness substrate is present." }
]

/--
Repo-local C006 blocker for replacing abstract curvature and Hodge-star fields.

This is audit data, not a Donaldson theorem.  It records the exact reason the
current `Curv` and `hodgeStar` fields in `DonaldsonASDModuliData` remain
abstract in this artifact.
-/
structure CurvatureHodgeStarFormalizationBlocker where
  childTask : String
  availableConcreteSubstrate : String
  missingCurvatureTarget : String
  missingHodgeStarTarget : String
  checkedMathlibModules : List String
  exactAbsences : List String
  replacementDecision : String
  validationTarget : String
deriving Repr

/--
C006 decision: do not replace `Curv`/`hodgeStar` with a fake local API.

The pinned mathlib snapshot provides unbundled normed-space two-forms via
`UnbundledNormedTwoForm`, but it does not provide the principal-bundle,
adjoint-bundle, curvature, bundled smooth manifold two-form, or Riemannian
Hodge-star APIs needed for Donaldson ASD moduli theory.
-/
def donaldsonCurvatureHodgeStarBlocker : CurvatureHodgeStarFormalizationBlocker := {
  childTask := "S1-M-131-C006",
  availableConcreteSubstrate :=
    "UnbundledNormedTwoForm E Ad = E -> E [⋀^Fin 2]→L[ℝ] Ad, backed by Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  missingCurvatureTarget :=
    "curvature of a smooth principal connection as a smooth adjoint-bundle-valued two-form over a four-manifold",
  missingHodgeStarTarget :=
    "Riemannian Hodge star on smooth adjoint-bundle-valued two-forms over an oriented four-manifold, with the ASD equation star F_A = -F_A",
  checkedMathlibModules := [
    "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
    "Mathlib.Analysis.Calculus.DifferentialForm.VectorField",
    "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
    "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion",
    "Mathlib.Geometry.Manifold.Riemannian.Basic",
    "Mathlib.Geometry.Manifold.Algebra.LieGroup",
    "Mathlib.Topology.FiberBundle.Basic",
    "Mathlib.Topology.VectorBundle.Riemannian"
  ],
  exactAbsences := [
    "no PrincipalBundle declaration or principal-bundle module in the audited mathlib tree",
    "no principal/Ehresmann connection API suitable for gauge-theory curvature; CovariantDerivative.Basic records planned future CovariantDerivative/Ehresmann.lean work",
    "no curvature, YangMills, AntiSelfDual, Uhlenbeck, Donaldson, or DonaldsonInvariant declaration usable as Donaldson ASD curvature data",
    "DifferentialForm.Basic represents forms as unbundled normed-space maps and its TODO says smooth forms on manifolds are not defined yet",
    "no Hodge, hodge, hodgeStar, or Hodge-star module/declaration in the audited mathlib tree"
  ],
  replacementDecision :=
    "blocked: keep DonaldsonASDModuliData.curvature : Conn -> Curv and hodgeStar : Curv -> Curv abstract until mathlib or a pinned dependency supplies the missing adjoint-valued curvature and Hodge-star APIs",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_131.lean"
}

/-- Search terms that did not locate a terminal Donaldson theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Donaldson",
  "anti self dual",
  "anti-self-dual",
  "ASD connection",
  "gauge theory",
  "gauge group",
  "connection curvature",
  "Uhlenbeck",
  "YangMills",
  "Hodge star",
  "moduli space"
]

/--
Repo-local record of the C003 GitHub Lean 4 upstream search.

These entries are audit data only.  They do not introduce a dependency, a local
wrapper, or a proof of Donaldson ASD moduli theory.
-/
structure ExternalLeanSearchCandidate where
  searchTerms : List String
  repoURL : String
  commit : String
  files : List String
  names : List String
  placeholderStatus : String
deriving Repr

/-- C003 primary-source GitHub candidates found while searching for Donaldson-adjacent Lean code. -/
def externalLeanSearchCandidates : List ExternalLeanSearchCandidate := [
  { searchTerms := ["YangMills", "gauge theory"],
    repoURL := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems",
    commit := "540da94826f70f3edf4d4fc66ce6cda20e903f61",
    files := [
      "Problems/YangMills/Quantum.lean",
      "Problems/YangMills/Millennium.lean"
    ],
    names := [
      "MillenniumYangMillsDefs.CompactSimpleGaugeGroup",
      "MillenniumYangMillsDefs.GaugeField",
      "MillenniumYangMillsDefs.FieldStrength",
      "MillenniumYangMillsDefs.YangMillsAction",
      "MillenniumYangMillsDefs.QuantumYangMillsTheory",
      "MillenniumYangMills.HasMassGap",
      "MillenniumYangMills.YangMillsExistenceAndMassGap"
    ],
    placeholderStatus :=
      "statement-shape candidate for Clay Yang-Mills; not Donaldson ASD moduli theory; no repo-local dependency or wrapper" },
  { searchTerms := ["gauge theory", "YangMills", "ASD connection"],
    repoURL := "https://github.com/mrdouglasny/lgt",
    commit := "da3d49b62b7551bacb90d7dd89fea1600660a220",
    files := [
      "GaugeField/Connection.lean",
      "GaugeField/GaugeGroup.lean",
      "MassGap/StrongCoupling.lean"
    ],
    names := [
      "ym_mass_gap_UN",
      "ym_mass_gap_exponential_decay",
      "ym_mass_gap_rate_exists",
      "HasGaugeTrace"
    ],
    placeholderStatus :=
      "lattice Yang-Mills strong-coupling candidate; README reports one open proof placeholder in the exponential-decay target; not Donaldson ASD moduli theory" },
  { searchTerms := ["Hodge star", "anti-self-dual", "ASD"],
    repoURL := "https://github.com/gift-framework/core",
    commit := "fc5ed2c2c3a660d73acf7772f7705d216131a969",
    files := [
      "GIFT/Geometry/HodgeStarCompute.lean",
      "GIFT/Geometry/HodgeStarR7.lean",
      "GIFT/Spectral/ComputedSpectrum.lean"
    ],
    names := [
      "GIFT.Geometry.HodgeStarCompute.hodgeStar3to4",
      "GIFT.Geometry.HodgeStarCompute.hodgeStar4to3",
      "GIFT.Geometry.HodgeStarCompute.hodgeStar_invol_3",
      "GIFT.Geometry.HodgeStarCompute.hodgeStar_invol_4",
      "GIFT.Geometry.HodgeStarR7.psi_eq_star_phi",
      "GIFT.Geometry.HodgeStarR7.hodge_infrastructure_complete",
      "GIFT.Spectral.ComputedSpectrum.sd_asd_gap_large"
    ],
    placeholderStatus :=
      "explicit R7/G2 Hodge-star and SD/ASD spectral arithmetic candidate; README reports project axioms; not four-dimensional Donaldson ASD gauge theory" }
]

/-- Search terms from C003 for which no terminal Donaldson ASD Lean 4 theorem was found. -/
def externalLeanSearchNoDonaldsonTerms : List String := [
  "Donaldson",
  "DonaldsonInvariant",
  "anti-self-dual",
  "ASD connection",
  "Uhlenbeck"
]

/--
Repo-local C004 integration gate for external Donaldson ASD proofs.

This is audit data only.  It records that the currently known external
candidates are not terminal Donaldson ASD moduli proofs and therefore should
not be converted into Lake dependencies or completion evidence.
-/
structure ExternalProofIntegrationGate where
  childTask : String
  currentStatus : String
  requiredClosureModes : List String
  rejectedClosureModes : List String
  blocker : String
  validatedLocalCommand : String
deriving Repr

/--
C004 integration decision for the currently recorded Donaldson upstream search.

The only safe repo-local action is to keep the theorem open unless a future
primary-source audit finds a terminal Lean 4 proof that can be pinned,
vendored, or blocked with a concrete integration reason.
-/
def donaldsonExternalProofIntegrationGate : ExternalProofIntegrationGate := {
  childTask := "S1-M-131-C004",
  currentStatus :=
    "no terminal external Lean 4 proof of Donaldson ASD moduli theory found in the recorded candidates; do not create a dependency from anchor-only evidence",
  requiredClosureModes := [
    "pinned Lake dependency exposing a checked Donaldson ASD theorem plus local wrapper",
    "vendored proof body with license-compatible source and local wrapper",
    "concrete integration blocker if a terminal external proof is later found but cannot be pinned/imported/checked"
  ],
  rejectedClosureModes := [
    "external_upstream_anchor_only",
    "nearby Yang-Mills statement-shape repositories",
    "Hodge-star arithmetic candidates outside four-dimensional Donaldson gauge theory",
    "projects with kernel placeholders or extra assumptions on the relevant proof path"
  ],
  blocker :=
    "current repo Lake closure contains mathlib@8a178386ffc0f5fef0b77738bb5449d50efeea95 and flt-regular@56161b6eb5281fbfe9c38f2bcec0f429ebc11a27, but no Donaldson ASD external dependency",
  validatedLocalCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_131.lean"
}

/--
One independently checkable M0387-style leaf below the public `M0184.P2` through
`M0184.P6` theorem-tree packages.

These rows are planning and audit data.  They do not assert any Donaldson proof
body, and every current row is deliberately `unchecked`.
-/
structure DonaldsonP2P6LeafLedger where
  packageId : String
  leafId : String
  role : String
  upstreamInputs : List String
  downstreamOutput : String
  localProofStepLedger : List String
  targetStepBudget : String
  currentStatus : String
  debtClass : String
  repoLocalClosed : Bool
deriving Repr

/--
C007 split of the theorem tree below `M0184.P2` through `M0184.P6`.

Every leaf has a local proof-step ledger with at most five high-level steps,
well below the M0387 `<=100` budget.  The ledgers are not proof closures: they
state the independently checkable work units that must be replaced by local
proof bodies, mathlib wrappers, or pinned external wrappers before completion.
-/
def donaldsonP2P6LeafLedgers : List DonaldsonP2P6LeafLedger := [
  { packageId := "M0184.P2",
    leafId := "M0184.P2.L01-four-manifold-model",
    role := "Select the concrete compact oriented smooth Riemannian four-manifold model.",
    upstreamInputs := ["FourManifoldBoundary", "mathlib manifold and Riemannian substrate audit"],
    downstreamOutput := "Concrete replacement target for the current four-manifold boundary fields.",
    localProofStepLedger := [
      "Choose the model-space and charted-space parameters.",
      "Instantiate `IsManifold` for the chosen smooth model.",
      "Record finite dimensionality over `ℝ`.",
      "Prove or import `Module.finrank ℝ E = 4`.",
      "Attach compactness, orientation, and metric hypotheses without hiding them in the theorem conclusion."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P2",
    leafId := "M0184.P2.L02-principal-bundle-and-group",
    role := "Replace generic structure-group hypotheses by principal-bundle and compact Lie-group APIs.",
    upstreamInputs := ["donaldsonMathlibAPIAudit principal-bundle row", "structureGroupHypotheses"],
    downstreamOutput := "A checked principal-bundle carrier and structure-group interface for connections.",
    localProofStepLedger := [
      "Locate or add the principal-bundle structure.",
      "Bind the structure group to a smooth compact Lie group API.",
      "Expose the total space, projection, local trivializations, and action laws.",
      "Record compatibility with the base four-manifold.",
      "Reject ordinary fiber-bundle data as insufficient for gauge theory."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P2",
    leafId := "M0184.P2.L03-connection-regularity-space",
    role := "Define the smooth connection space and the regularity predicate.",
    upstreamInputs := ["connectionRegularity", "CovariantDerivative audit boundary"],
    downstreamOutput := "Concrete `Conn` type and checked regularity predicate for ASD candidates.",
    localProofStepLedger := [
      "Choose a principal/Ehresmann connection representation.",
      "Define smoothness or Sobolev regularity for the selected representation.",
      "Show regularity is well typed over the selected bundle.",
      "Connect regularity to the current `connectionRegularity` field.",
      "Keep vector-bundle covariant derivatives separate unless an equivalence is proved."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P2",
    leafId := "M0184.P2.L04-curvature-two-form",
    role := "Replace abstract curvature with adjoint-valued two-form curvature.",
    upstreamInputs := ["curvature", "UnbundledNormedTwoForm", "donaldsonCurvatureHodgeStarBlocker"],
    downstreamOutput := "Checked curvature map landing in a smooth adjoint-bundle-valued two-form type.",
    localProofStepLedger := [
      "Define or import the adjoint bundle.",
      "Define curvature for the selected smooth connection API.",
      "Show curvature is a two-form over the base four-manifold.",
      "Show the target is adjoint-valued.",
      "Bridge the concrete curvature to `DonaldsonASDModuliData.curvature`."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P2",
    leafId := "M0184.P2.L05-hodge-star-and-asd-equation",
    role := "Replace abstract Hodge star and ASD predicate by the Riemannian two-form API.",
    upstreamInputs := ["hodgeStar", "IsAntiSelfDual", "orientationHypotheses", "riemannianMetricHypotheses"],
    downstreamOutput := "Concrete anti-self-dual curvature equation `star F_A = -F_A`.",
    localProofStepLedger := [
      "Import or define the Hodge star on two-forms in dimension four.",
      "State the star-square law on the relevant two-form target.",
      "State compatibility with negation.",
      "Specialize the ASD equation to curvature.",
      "Prove the concrete predicate unfolds to the existing statement-shape predicate."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P3",
    leafId := "M0184.P3.L01-gauge-group-action",
    role := "Construct the gauge group action on the connection space.",
    upstreamInputs := ["GaugeEquivalent", "MulAction G Conn", "principal-bundle API"],
    downstreamOutput := "Concrete gauge action replacing the abstract `MulAction G Conn` field.",
    localProofStepLedger := [
      "Define gauge transformations as bundle automorphisms over the identity.",
      "Prove group structure.",
      "Define action on smooth connections.",
      "Prove identity and multiplication action laws.",
      "Bridge the action to `GaugeEquivalent`."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P3",
    leafId := "M0184.P3.L02-asd-set-gauge-invariance",
    role := "Show regular ASD connections are preserved by gauge transformations.",
    upstreamInputs := ["asdConnectionSet", "gauge group action", "curvature transformation law"],
    downstreamOutput := "Gauge-invariant ASD subset suitable for quotienting.",
    localProofStepLedger := [
      "State regularity preservation under gauge action.",
      "State curvature equivariance under gauge action.",
      "State Hodge-star compatibility with adjoint action.",
      "Rewrite ASD curvature after gauge action.",
      "Conclude membership preservation for `asdConnectionSet`."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P3",
    leafId := "M0184.P3.L03-orbit-equivalence-relation",
    role := "Promote gauge equivalence from orbit membership to an equivalence relation.",
    upstreamInputs := ["GaugeEquivalent", "gaugeOrbit", "MulAction group laws"],
    downstreamOutput := "Checked quotient relation for the ASD moduli set.",
    localProofStepLedger := [
      "Prove reflexivity from the identity gauge transformation.",
      "Prove symmetry using inverse gauge transformations.",
      "Prove transitivity using multiplication.",
      "Restrict the relation to the ASD subset.",
      "Relate quotient classes to `gaugeOrbit`."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P3",
    leafId := "M0184.P3.L04-moduli-quotient-carrier",
    role := "Replace the set-of-orbits shape by a concrete quotient carrier.",
    upstreamInputs := ["asdModuliOrbitSet", "orbit equivalence relation", "topological quotient audit"],
    downstreamOutput := "Typed quotient carrier for the ASD moduli space.",
    localProofStepLedger := [
      "Choose quotient type or quotient topology representation.",
      "Define the projection from ASD connections to quotient points.",
      "Show the set-of-orbits model matches the quotient carrier.",
      "Record quotient-map or coinduced-topology properties.",
      "Bridge to `DonaldsonASDModuliOutput.orbitSetModel_eq`."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P3",
    leafId := "M0184.P3.L05-stabilizer-and-slice-boundary",
    role := "Separate stabilizer and local-slice hypotheses needed for smooth moduli structure.",
    upstreamInputs := ["transversalityHypotheses", "quotient carrier", "gauge action"],
    downstreamOutput := "Explicit irreducibility/slice boundary for later smooth-structure leaves.",
    localProofStepLedger := [
      "Define stabilizers of connections under the gauge action.",
      "State the irreducible or framed condition used to control stabilizers.",
      "State the local slice theorem target.",
      "Connect slice data to quotient charts.",
      "Mark absent slice theorem APIs as blockers instead of proof closures."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P4",
    leafId := "M0184.P4.L01-deformation-complex-definition",
    role := "Define the ASD deformation complex at a connection.",
    upstreamInputs := ["ellipticDeformationComplexHypotheses", "curvature two-form", "Hodge-star API"],
    downstreamOutput := "Typed complex controlling infinitesimal ASD deformations.",
    localProofStepLedger := [
      "Define the gauge infinitesimal map.",
      "Define the linearized ASD curvature map.",
      "State the target self-dual or anti-self-dual two-form bundle.",
      "Prove the composition is zero.",
      "Expose the complex as the object used by later index leaves."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P4",
    leafId := "M0184.P4.L02-ellipticity-and-fredholmness",
    role := "Prove ellipticity and Fredholmness of the deformation complex.",
    upstreamInputs := ["deformation complex", "Riemannian metric", "elliptic operator substrate"],
    downstreamOutput := "Fredholm package for the local moduli dimension calculation.",
    localProofStepLedger := [
      "Identify the principal symbol complex.",
      "Prove symbol exactness away from the zero section.",
      "Apply or import elliptic Fredholm theory.",
      "State finite-dimensional kernel and cokernel.",
      "Record any missing elliptic-analysis API as a blocker."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P4",
    leafId := "M0184.P4.L03-tangent-obstruction-cohomology",
    role := "Identify tangent and obstruction spaces with deformation-complex cohomology.",
    upstreamInputs := ["deformation complex", "slice boundary", "Fredholm package"],
    downstreamOutput := "Local tangent/obstruction interface for transversality.",
    localProofStepLedger := [
      "Define zeroth, first, and second cohomology of the complex.",
      "Relate infinitesimal gauge directions to the zeroth term.",
      "Relate tangent vectors to first cohomology.",
      "Relate obstructions to second cohomology.",
      "Bridge these identifications to local quotient charts."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P4",
    leafId := "M0184.P4.L04-transversality-smooth-structure",
    role := "Use transversality to obtain a smooth or stratified moduli structure.",
    upstreamInputs := ["transversalityHypotheses", "tangent-obstruction cohomology", "slice theorem"],
    downstreamOutput := "`DonaldsonASDModuliOutput.smoothOrStratifiedStructure`.",
    localProofStepLedger := [
      "State the regularity or perturbation hypothesis.",
      "Show obstruction space vanishes or is handled by strata.",
      "Apply the implicit-function or Kuranishi model theorem.",
      "Patch local models over quotient charts.",
      "Return the smooth or stratified structure proposition."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P4",
    leafId := "M0184.P4.L05-index-expected-dimension",
    role := "Compute the expected dimension from the deformation-complex index.",
    upstreamInputs := ["Fredholm package", "Atiyah-Singer or index theorem anchor", "characteristic-class data"],
    downstreamOutput := "`DonaldsonASDModuliOutput.expectedDimensionFormula`.",
    localProofStepLedger := [
      "State the Fredholm index of the deformation complex.",
      "Import or prove the required index theorem specialization.",
      "Normalize characteristic-class conventions.",
      "Rewrite the index into the Donaldson expected-dimension formula.",
      "Bridge the formula to the output contract."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P5",
    leafId := "M0184.P5.L01-uhlenbeck-compactness",
    role := "Prove the compactness theorem for bounded-energy ASD connections modulo gauge.",
    upstreamInputs := ["compactnessHypotheses", "ASD equation", "gauge quotient"],
    downstreamOutput := "Compactness input for moduli compactification.",
    localProofStepLedger := [
      "State energy bounds for ASD connections.",
      "State local gauge fixing and weak compactness.",
      "Handle bubbling or removable singularities.",
      "Extract a convergent subsequence modulo gauge.",
      "Record absent Uhlenbeck APIs as blockers if no proof anchor exists."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P5",
    leafId := "M0184.P5.L02-compactification-carrier",
    role := "Construct the compactified moduli carrier.",
    upstreamInputs := ["Uhlenbeck compactness", "asdModuliOrbitSet", "compactificationHypotheses"],
    downstreamOutput := "`DonaldsonASDModuliOutput.compactificationPackage` carrier component.",
    localProofStepLedger := [
      "Define ideal connections or bubbling strata.",
      "Embed ordinary moduli points into the compactified carrier.",
      "Define the compactification topology.",
      "Prove compactness or record the exact imported theorem.",
      "Relate the compactification back to the uncompactified quotient."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P5",
    leafId := "M0184.P5.L03-orientation-package",
    role := "Orient the moduli space using determinant-line data.",
    upstreamInputs := ["orientationHypotheses", "deformation complex", "smoothOrStratifiedStructure"],
    downstreamOutput := "`DonaldsonASDModuliOutput.orientationPackage`.",
    localProofStepLedger := [
      "Define the determinant line of the deformation complex.",
      "State orientation data on the base and bundle.",
      "Construct the induced orientation of local moduli charts.",
      "Prove compatibility under gauge and chart transition.",
      "Return the global orientation package."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P5",
    leafId := "M0184.P5.L04-gluing-and-boundary-strata",
    role := "Control boundary strata and gluing needed for invariance.",
    upstreamInputs := ["compactification carrier", "orientation package", "analysis gluing theorem"],
    downstreamOutput := "Boundary and gluing compatibility for Donaldson invariant construction.",
    localProofStepLedger := [
      "State local gluing parameters around strata.",
      "Construct the gluing map.",
      "Prove the gluing map covers a neighborhood of the stratum.",
      "Track orientations through gluing.",
      "Record boundary codimension statements needed by invariance."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P6",
    leafId := "M0184.P6.L01-mu-map-and-observable-interface",
    role := "Define the cohomological observables used by Donaldson invariants.",
    upstreamInputs := ["universal bundle or substitute", "moduli quotient carrier", "cohomology API"],
    downstreamOutput := "Typed observable interface for invariant evaluation.",
    localProofStepLedger := [
      "Define the universal or framed bundle data over the moduli family.",
      "Define the characteristic class used in the mu map.",
      "Define the slant or pairing operation with homology classes.",
      "Prove degree bookkeeping for the observable.",
      "Bridge the construction to `donaldsonInvariantInterface`."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P6",
    leafId := "M0184.P6.L02-fundamental-class-or-cycle",
    role := "Produce the cycle or virtual fundamental class used for pairings.",
    upstreamInputs := ["smoothOrStratifiedStructure", "orientationPackage", "compactificationPackage"],
    downstreamOutput := "Fundamental-cycle input for Donaldson invariant evaluation.",
    localProofStepLedger := [
      "State the dimension and compactness hypotheses needed for a cycle.",
      "Use orientation to define the class or virtual class.",
      "Handle strata or perturbation choices.",
      "Prove boundary contributions vanish or are controlled.",
      "Expose the class for cohomological pairing."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P6",
    leafId := "M0184.P6.L03-pairing-definition",
    role := "Define the Donaldson invariant as a pairing of observables with the moduli class.",
    upstreamInputs := ["mu-map observables", "fundamental class", "cohomology pairing API"],
    downstreamOutput := "Formal invariant value for the selected inputs.",
    localProofStepLedger := [
      "Form the product of observable classes.",
      "Check the total degree matches the moduli dimension.",
      "Pair the product with the fundamental class.",
      "Prove independence of representative choices at the cochain/cohomology level.",
      "Return the typed invariant value."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P6",
    leafId := "M0184.P6.L04-metric-and-perturbation-independence",
    role := "Prove the invariant is independent of metric and auxiliary perturbation choices.",
    upstreamInputs := ["pairing definition", "compactified one-parameter moduli spaces", "gluing boundary control"],
    downstreamOutput := "Donaldson invariant well-definedness statement.",
    localProofStepLedger := [
      "Define a path between choices.",
      "Construct the one-parameter moduli space.",
      "Identify its boundary with the two endpoint moduli spaces plus controlled strata.",
      "Use Stokes/cobordism to show pairings agree.",
      "Record any missing cobordism or integration API as a blocker."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false },
  { packageId := "M0184.P6",
    leafId := "M0184.P6.L05-terminal-output-assembly",
    role := "Assemble the output contract for the statement-shape theorem.",
    upstreamInputs := ["P2 concrete ASD data", "P3 quotient carrier", "P4 smooth/index package", "P5 compactification/orientation", "P6 invariant interface"],
    downstreamOutput := "Candidate inhabitant of `DonaldsonASDModuliOutput D` after all preceding leaves close.",
    localProofStepLedger := [
      "Fill `orbitSetModel` with the quotient carrier.",
      "Prove `orbitSetModel_eq` against `asdModuliOrbitSet`.",
      "Attach quotient, smooth, dimension, orientation, compactification, and invariant fields.",
      "Check all assumptions of `DonaldsonASDModuliTheorem` are consumed.",
      "Only then attempt a terminal proof of `StatementShape` or a concrete specialization."
    ],
    targetStepBudget := "<=100",
    currentStatus := "unchecked",
    debtClass := "formalization_debt",
    repoLocalClosed := false }
]

/-- C007 does not claim that the split below `M0184.P2` through `M0184.P6` closes Donaldson. -/
def donaldsonP2P6SplitClosesTheorem : Bool := false

/-- C007 records the local validation command for the theorem-tree split artifact. -/
def donaldsonP2P6SplitValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_131.lean"

/--
Public backfill text for the C007 theorem-tree split.

This string is meant for a serial public-doc integrator.  Worker tasks must not
edit the shared public blueprint or todo files directly.
-/
def donaldsonP2P6PublicBackfillProposal : String :=
  "S1-M-131-C007: The checked Lean artifact now contains `DonaldsonP2P6LeafLedger` and `donaldsonP2P6LeafLedgers`, splitting `M0184.P2` through `M0184.P6` into 24 unchecked independently checkable leaves, each with `targetStepBudget := \"<=100\"`, explicit local proof-step ledger text, `debtClass := \"formalization_debt\"`, and `repoLocalClosed := false`. Validation target: `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_131.lean`. This is a theorem-tree planning/audit split only; keep `S1-M-131 / THM-M-0184` not completed until a local proof body, local wrapper to pinned mathlib, or pinned external upstream proof validates in the repo and every promoted leaf is actually closed."

/--
C008 public-status integration gate for `S1-M-131 / THM-M-0184`.

This is a repo-local audit object for the serial public-doc integrator.  It does
not edit the public blueprint, todo, or README, and it does not certify a proof
of Donaldson's theorem.
-/
structure DonaldsonPublicStatusGate where
  childTask : String
  publicSurfaces : List String
  currentRepoLocalClosure : String
  allowedCompletionEvidence : List String
  forbiddenCompletionEvidence : List String
  repoLocalIntegrationDebtMayBeCompleted : Bool
  publicStatusesMustRemainOpen : Bool
  validationCommand : String
deriving Repr

/--
C008 decision: public status surfaces must stay open.

The current artifact contains checked statement-shape, API-audit, external-audit,
integration-gate, blocker, and theorem-tree ledger data.  It does not contain a
local proof body, a local wrapper to pinned mathlib, or a pinned external
upstream proof of Donaldson ASD moduli theory.
-/
def donaldsonPublicStatusGate : DonaldsonPublicStatusGate := {
  childTask := "S1-M-131-C008",
  publicSurfaces := [
    "Docs/Stage1_Blueprint.md",
    "Docs/todos_20260430.md",
    "README.md"
  ],
  currentRepoLocalClosure :=
    "not completed: statement-shape and audit data validate locally, but no Donaldson ASD proof body, pinned mathlib wrapper, or pinned external upstream proof validates in this repo",
  allowedCompletionEvidence := [
    "local_proof_body",
    "local_wrapper_upstream_mathlib",
    "external_upstream_pinned"
  ],
  forbiddenCompletionEvidence := [
    "anchor-only external URLs",
    "nearby Yang-Mills or Hodge-star repositories that are not terminal Donaldson ASD moduli proofs",
    "unchecked theorem-tree planning ledgers",
    "statement-shape artifacts whose fields remain abstract formalization boundaries",
    "repo_local_integration_debt"
  ],
  repoLocalIntegrationDebtMayBeCompleted := false,
  publicStatusesMustRemainOpen := true,
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_131.lean"
}

/-- C008 records that repo-local integration debt is not completion evidence. -/
theorem donaldsonPublicStatusGate_repoLocalIntegrationDebt_not_completed :
    donaldsonPublicStatusGate.repoLocalIntegrationDebtMayBeCompleted = false :=
  rfl

/-- C008 records that the public status surfaces remain open at this stage. -/
theorem donaldsonPublicStatusGate_publicStatuses_open :
    donaldsonPublicStatusGate.publicStatusesMustRemainOpen = true :=
  rfl

/-- C008 repo-local integration-debt gate result for the child ledger. -/
def donaldsonPublicStatusGateResult : String :=
  "pass for non-completion: no external Donaldson ASD Lean proof has been found, so no repo_local_integration_debt is being claimed as completed; public statuses must remain open until local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned evidence validates in this repo"

/--
Public backfill text for the C008 public-status gate.

This string is meant for a serial public-doc integrator.  Worker tasks must not
edit the shared public blueprint, todo, or README directly.
-/
def donaldsonPublicStatusGateBackfillProposal : String :=
  "S1-M-131-C008: The checked Lean artifact records `DonaldsonPublicStatusGate` and `donaldsonPublicStatusGate`, with `publicStatusesMustRemainOpen := true` and `repoLocalIntegrationDebtMayBeCompleted := false`. Current repo-local closure is `not completed`: the artifact validates statement-shape, audit, blocker, integration-gate, and theorem-tree ledger data, but no local proof body, local wrapper to pinned mathlib, or pinned external upstream Donaldson ASD proof validates in the repo. Keep `Docs/Stage1_Blueprint.md`, `Docs/todos_20260430.md`, and `README.md` statuses open. Completion evidence is restricted to `local_proof_body`, `local_wrapper_upstream_mathlib`, or `external_upstream_pinned`, validated by `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_131.lean`."

end S1_M_131
end Stage1
end AwesomeTheorems
