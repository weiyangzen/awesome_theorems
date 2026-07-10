import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Algebra.Algebra.Spectrum.Basic
import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Orientation
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Geometry.Manifold.ChartedSpace
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Basic

/-!
# S1-M-204 / THM-M-1545: Nahm transform

This Stage1 artifact records a conservative Lean statement boundary for the
Nahm transform as a construction of monopoles from Nahm data.

The physics phrase "construction of monopoles" is not a kernel-checkable theorem
until the gauge group, base three-manifold, Higgs field, Bogomolny equation,
Nahm equations, Dirac-family kernel bundle, and regularity/framing conditions
are fixed.  The declarations below isolate that formalization boundary while
checking low-risk mathlib substrate for Hilbert-space operators, spectra,
kernels, group actions, charted spaces, and covariant-derivative interfaces.

No terminal proof of the Nahm transform is claimed here.
-/

noncomputable section

open scoped Topology

universe uModel uChart uBase uG uConn uField uNahm uH

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_204

/-- Continuous Hilbert-space operator used for the Dirac-family boundary. -/
abbrev HilbertOperator
    (H : Type uH) [NormedAddCommGroup H] [InnerProductSpace ℂ H] : Type uH :=
  H →L[ℂ] H

/-- Algebraic spectrum of a Hilbert-space operator. -/
def OperatorSpectrum
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D : HilbertOperator H) : Set ℂ :=
  spectrum ℂ D

/--
Kernel of the Dirac-family operator at the Stage1 boundary.

The analytic transform constructs a finite-rank kernel bundle from such
families; the finite-dimensionality and smoothness assertions remain fields in
the transform data below.
-/
def DiracKernel
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D : HilbertOperator H) : Submodule ℂ H :=
  LinearMap.ker D.toLinearMap

/-- The zero vector lies in every Dirac kernel. -/
theorem zero_mem_diracKernel
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D : HilbertOperator H) :
    (0 : H) ∈ DiracKernel D := by
  simp [DiracKernel]

/-- The kernel of the zero Dirac operator is the whole Hilbert space. -/
theorem diracKernel_zero_eq_top
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H] :
    DiracKernel (0 : HilbertOperator H) = ⊤ := by
  ext ψ
  simp [DiracKernel]

/-- Identity Dirac-family anchor. -/
def identityHilbertOperator
    (H : Type uH) [NormedAddCommGroup H] [InnerProductSpace ℂ H] :
    HilbertOperator H :=
  ContinuousLinearMap.id ℂ H

/-- The identity Hilbert operator acts as the identity. -/
theorem identityHilbertOperator_apply
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H] (ψ : H) :
    identityHilbertOperator H ψ = ψ :=
  ContinuousLinearMap.id_apply ψ

/--
Fredholm regularity data for one bounded realization of a Nahm Dirac operator.

The actual Nahm transform uses unbounded differential operators on Sobolev
completions.  At this Stage1 boundary, the chosen bounded realization records
the three Fredholm facts needed for the kernel-bundle construction: closed
range, finite-dimensional kernel, and finite-dimensional cokernel.  The final
field is the named analytic obligation that must later be discharged by an
elliptic/Fredholm regularity theorem or by a pinned external proof body.
-/
structure DiracOperatorFredholmRegularity
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D : HilbertOperator H) : Type uH where
  closedRange : IsClosed (LinearMap.range D.toLinearMap : Set H)
  finiteDimensionalKernel : FiniteDimensional ℂ (DiracKernel D)
  finiteDimensionalCokernel :
    FiniteDimensional ℂ (H ⧸ LinearMap.range D.toLinearMap)
  ellipticRegularityJustification : Prop

/-- Projection of closed range from a Dirac Fredholm regularity package. -/
theorem DiracOperatorFredholmRegularity.isClosed_range
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {D : HilbertOperator H} (R : DiracOperatorFredholmRegularity D) :
    IsClosed (LinearMap.range D.toLinearMap : Set H) :=
  R.closedRange

/-- Projection of finite-dimensional kernel from a Dirac Fredholm regularity package. -/
theorem DiracOperatorFredholmRegularity.finiteDimensional_kernel
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {D : HilbertOperator H} (R : DiracOperatorFredholmRegularity D) :
    FiniteDimensional ℂ (DiracKernel D) :=
  R.finiteDimensionalKernel

/-- Projection of finite-dimensional cokernel from a Dirac Fredholm regularity package. -/
theorem DiracOperatorFredholmRegularity.finiteDimensional_cokernel
    {H : Type uH} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {D : HilbertOperator H} (R : DiracOperatorFredholmRegularity D) :
    FiniteDimensional ℂ (H ⧸ LinearMap.range D.toLinearMap) :=
  R.finiteDimensionalCokernel

/-- Gauge equivalence for connections under a mathlib multiplicative action. -/
def GaugeEquivalent
    {G : Type uG} {Conn : Type uConn} [Group G] [MulAction G Conn]
    (A B : Conn) : Prop :=
  ∃ g : G, g • A = B

/-- Gauge equivalence is reflexive. -/
theorem gaugeEquivalent_refl
    {G : Type uG} {Conn : Type uConn} [Group G] [MulAction G Conn]
    (A : Conn) :
    GaugeEquivalent (G := G) A A :=
  ⟨1, one_smul G A⟩

/-- Gauge orbit of a connection. -/
def gaugeOrbit
    {G : Type uG} {Conn : Type uConn} [Group G] [MulAction G Conn]
    (A : Conn) : Set Conn :=
  {B | GaugeEquivalent (G := G) A B}

/-- Membership in the gauge orbit unfolds to gauge equivalence. -/
theorem mem_gaugeOrbit_iff
    {G : Type uG} {Conn : Type uConn} [Group G] [MulAction G Conn]
    {A B : Conn} :
    B ∈ gaugeOrbit (G := G) A ↔ GaugeEquivalent (G := G) A B :=
  Iff.rfl

/-- Every connection lies in its own gauge orbit. -/
theorem mem_gaugeOrbit_self
    {G : Type uG} {Conn : Type uConn} [Group G] [MulAction G Conn]
    (A : Conn) :
    A ∈ gaugeOrbit (G := G) A :=
  gaugeEquivalent_refl A

/--
Bundle-valued differential `k`-forms on a charted base.

This uses mathlib's `ContinuousAlternatingMap` representation of differential
forms, fiberwise over the tangent spaces of a manifold.  For the monopole
side, `Ad x` is the fiber modelling the adjoint bundle at `x`.
-/
abbrev AdjointValuedDifferentialForm
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} [TopologicalSpace Base] [ChartedSpace Chart Base]
    (I : ModelWithCorners ℝ E Chart) (Ad : Base → Type uField)
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    (k : ℕ) : Type _ :=
  (x : Base) → TangentSpace I x [⋀^Fin k]→L[ℝ] Ad x

/-- Higgs fields are sections of the same adjoint bundle. -/
abbrev HiggsField
    {Base : Type uBase} (Ad : Base → Type uField) : Type _ :=
  (x : Base) → Ad x

/--
Repo-local statement data for an oriented Riemannian three-manifold.

The current mathlib substrate supplies tangent spaces, orientations of real
modules, and Riemannian-bundle data.  A full Hodge-star construction for
bundle-valued forms on manifolds is not available here, so the concrete
Bogomolny statement below keeps the Hodge-star operator as an explicit
operation from adjoint-valued two-forms to adjoint-valued one-forms, while this
record fixes the geometric surface on which that operation is meant to live.
-/
structure OrientedRiemannianThreeManifold
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    (Base : Type uBase) [TopologicalSpace Base] [ChartedSpace Chart Base]
    (I : ModelWithCorners ℝ E Chart) : Prop where
  smoothManifold : IsManifold I (⊤ : WithTop ℕ∞) Base
  finiteDimensionalModel : FiniteDimensional ℝ E
  modelDimension_three : Module.finrank ℝ E = 3
  orientedTangentSpaces :
    Nonempty ((x : Base) → Orientation ℝ (TangentSpace I x) (Fin 3))
  riemannianMetric :
    Nonempty (Bundle.RiemannianBundle (fun x : Base => TangentSpace I x))

/--
Concrete differential-form operations in the Bogomolny equation.

`curvature A` is the adjoint-valued curvature two-form `F_A`.
`covariantDerivativeHiggs A Φ` is the adjoint-valued one-form `d_A Φ`.
`hodgeStarCurvature` is the Hodge-star operation on curvature two-forms on the
oriented Riemannian three-manifold.
-/
structure BogomolnyFormData
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} [TopologicalSpace Base] [ChartedSpace Chart Base]
    (I : ModelWithCorners ℝ E Chart) (Ad : Base → Type uField)
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    (Conn : Type uConn) : Type (max (max (max (max uModel uChart) uBase) uField) uConn) where
  geometry : OrientedRiemannianThreeManifold Base I
  hodgeStarCurvature :
    AdjointValuedDifferentialForm I Ad 2 →
      AdjointValuedDifferentialForm I Ad 1
  curvature : Conn → AdjointValuedDifferentialForm I Ad 2
  covariantDerivativeHiggs :
    Conn → HiggsField Ad → AdjointValuedDifferentialForm I Ad 1

/-- Concrete Bogomolny equation `*F_A = d_A Φ` for adjoint-valued forms. -/
def IsBogomolny
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} [TopologicalSpace Base] [ChartedSpace Chart Base]
    {I : ModelWithCorners ℝ E Chart} {Ad : Base → Type uField}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    {Conn : Type uConn} (B : BogomolnyFormData I Ad Conn)
    (A : Conn) (Φ : HiggsField Ad) : Prop :=
  B.hodgeStarCurvature (B.curvature A) = B.covariantDerivativeHiggs A Φ

/-- The concrete Bogomolny statement unfolds to `*F_A = d_A Φ`. -/
theorem isBogomolny_iff
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} [TopologicalSpace Base] [ChartedSpace Chart Base]
    {I : ModelWithCorners ℝ E Chart} {Ad : Base → Type uField}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    {Conn : Type uConn} {B : BogomolnyFormData I Ad Conn}
    {A : Conn} {Φ : HiggsField Ad} :
    IsBogomolny B A Φ ↔
      B.hodgeStarCurvature (B.curvature A) = B.covariantDerivativeHiggs A Φ :=
  Iff.rfl

/-- Zero curvature and zero Higgs derivative solve the concrete Bogomolny equation. -/
theorem isBogomolny_zero
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} [TopologicalSpace Base] [ChartedSpace Chart Base]
    {I : ModelWithCorners ℝ E Chart} {Ad : Base → Type uField}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    {Conn : Type uConn} (geometry : OrientedRiemannianThreeManifold Base I)
    (hodgeStarCurvature :
      AdjointValuedDifferentialForm I Ad 2 →
        AdjointValuedDifferentialForm I Ad 1)
    (hzero : hodgeStarCurvature 0 = 0) (A : Conn) (Φ : HiggsField Ad) :
    IsBogomolny
      ({ geometry := geometry
         hodgeStarCurvature := hodgeStarCurvature
         curvature := fun _ : Conn => 0
         covariantDerivativeHiggs := fun _ : Conn => fun _ : HiggsField Ad => 0 } :
        BogomolnyFormData I Ad Conn) A Φ := by
  simp [IsBogomolny, hzero]

/-- Cyclic bracket term in the convention `[T₂,T₃]`, `[T₃,T₁]`, `[T₁,T₂]`. -/
def NahmBracketTerm
    {V : Type uNahm} (bracket : V → V → V) (T : Fin 3 → ℝ → V)
    (i : Fin 3) (s : ℝ) : V :=
  ![bracket (T 1 s) (T 2 s),
    bracket (T 2 s) (T 0 s),
    bracket (T 0 s) (T 1 s)] i

/-- First component of the cyclic Nahm bracket convention. -/
theorem nahmBracketTerm_zero
    {V : Type uNahm} (bracket : V → V → V) (T : Fin 3 → ℝ → V)
    (s : ℝ) :
    NahmBracketTerm bracket T 0 s = bracket (T 1 s) (T 2 s) := by
  simp [NahmBracketTerm]

/-- Second component of the cyclic Nahm bracket convention. -/
theorem nahmBracketTerm_one
    {V : Type uNahm} (bracket : V → V → V) (T : Fin 3 → ℝ → V)
    (s : ℝ) :
    NahmBracketTerm bracket T 1 s = bracket (T 2 s) (T 0 s) := by
  simp [NahmBracketTerm]

/-- Third component of the cyclic Nahm bracket convention. -/
theorem nahmBracketTerm_two
    {V : Type uNahm} (bracket : V → V → V) (T : Fin 3 → ℝ → V)
    (s : ℝ) :
    NahmBracketTerm bracket T 2 s = bracket (T 0 s) (T 1 s) := by
  simp [NahmBracketTerm]

/--
Pointwise Nahm ODE in the sign convention
`dTᵢ/ds + [Tⱼ,Tₖ] = 0`, cyclically ordered as
`(i,j,k) = (1,2,3), (2,3,1), (3,1,2)`.
-/
def NahmODEAt
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (bracket : V → V → V) (T : Fin 3 → ℝ → V) (s : ℝ) : Prop :=
  ∀ i : Fin 3, HasDerivAt (fun τ : ℝ => T i τ)
    (-(NahmBracketTerm bracket T i s)) s

/-- Nahm ODE on the chosen open interval or domain. -/
def NahmODEOn
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (interval : Set ℝ) (bracket : V → V → V) (T : Fin 3 → ℝ → V) : Prop :=
  ∀ s ∈ interval, NahmODEAt bracket T s

/-- First component of `dTᵢ/ds + [Tⱼ,Tₖ] = 0`. -/
theorem nahmODEAt_zero
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    {bracket : V → V → V} {T : Fin 3 → ℝ → V} {s : ℝ}
    (h : NahmODEAt bracket T s) :
    HasDerivAt (fun τ : ℝ => T 0 τ) (-(bracket (T 1 s) (T 2 s))) s := by
  simpa [NahmBracketTerm] using h 0

/-- Second component of `dTᵢ/ds + [Tⱼ,Tₖ] = 0`. -/
theorem nahmODEAt_one
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    {bracket : V → V → V} {T : Fin 3 → ℝ → V} {s : ℝ}
    (h : NahmODEAt bracket T s) :
    HasDerivAt (fun τ : ℝ => T 1 τ) (-(bracket (T 2 s) (T 0 s))) s := by
  simpa [NahmBracketTerm] using h 1

/-- Third component of `dTᵢ/ds + [Tⱼ,Tₖ] = 0`. -/
theorem nahmODEAt_two
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    {bracket : V → V → V} {T : Fin 3 → ℝ → V} {s : ℝ}
    (h : NahmODEAt bracket T s) :
    HasDerivAt (fun τ : ℝ => T 2 τ) (-(bracket (T 0 s) (T 1 s))) s := by
  simpa [NahmBracketTerm] using h 2

/-- Endpoint side used to fix the residue sign convention. -/
inductive NahmEndpointSide where
  | left
  | right
deriving DecidableEq, Repr

/-- Cyclic bracket term for an endpoint residue triple. -/
def NahmResidueBracketTerm
    {V : Type uNahm} (bracket : V → V → V) (R : Fin 3 → V)
    (i : Fin 3) : V :=
  ![bracket (R 1) (R 2),
    bracket (R 2) (R 0),
    bracket (R 0) (R 1)] i

/--
Left-endpoint simple-pole residue for the Nahm triple.

With local coordinate `(s-a)` on the interval to the right of `a`, the residue
triple `R` is the one-sided limit of `(s-a) Tᵢ(s)`.
-/
def NahmLeftSimplePoleResidue
    {V : Type uNahm} [TopologicalSpace V] [SMul ℝ V]
    (a : ℝ) (T : Fin 3 → ℝ → V) (R : Fin 3 → V) : Prop :=
  ∀ i : Fin 3, Filter.Tendsto (fun s : ℝ => (s - a) • T i s) (𝓝[>] a) (𝓝 (R i))

/--
Right-endpoint simple-pole residue for the Nahm triple.

With local coordinate `(b-s)` on the interval to the left of `b`, the residue
triple `R` is the one-sided limit of `(b-s) Tᵢ(s)`.
-/
def NahmRightSimplePoleResidue
    {V : Type uNahm} [TopologicalSpace V] [SMul ℝ V]
    (b : ℝ) (T : Fin 3 → ℝ → V) (R : Fin 3 → V) : Prop :=
  ∀ i : Fin 3, Filter.Tendsto (fun s : ℝ => (b - s) • T i s) (𝓝[<] b) (𝓝 (R i))

/--
Endpoint residue Lie-bracket signs induced by
`dTᵢ/ds + [Tⱼ,Tₖ] = 0`.

At a left endpoint with local pole coordinate `(s-a)`, the residue triple
satisfies `[Rⱼ,Rₖ] = Rᵢ`.  At a right endpoint with coordinate `(b-s)`, it
satisfies `[Rⱼ,Rₖ] = -Rᵢ`.
-/
def NahmResidueBracketConvention
    {V : Type uNahm} [Neg V] (side : NahmEndpointSide)
    (bracket : V → V → V) (R : Fin 3 → V) : Prop :=
  match side with
  | .left => ∀ i : Fin 3, NahmResidueBracketTerm bracket R i = R i
  | .right => ∀ i : Fin 3, NahmResidueBracketTerm bracket R i = -R i

/-- Interval endpoint residue hypotheses for the standard open interval `(a,b)`. -/
structure NahmIntervalResidueHypotheses
    {V : Type uNahm} [TopologicalSpace V] [SMul ℝ V] [Neg V]
    (interval : Set ℝ) (bracket : V → V → V) (T : Fin 3 → ℝ → V) :
    Type uNahm where
  leftEndpoint : ℝ
  rightEndpoint : ℝ
  left_lt_right : leftEndpoint < rightEndpoint
  interval_eq_Ioo : interval = Set.Ioo leftEndpoint rightEndpoint
  leftResidue : Fin 3 → V
  rightResidue : Fin 3 → V
  leftSimplePoleResidue :
    NahmLeftSimplePoleResidue leftEndpoint T leftResidue
  rightSimplePoleResidue :
    NahmRightSimplePoleResidue rightEndpoint T rightResidue
  leftResidueBracket :
    NahmResidueBracketConvention .left bracket leftResidue
  rightResidueBracket :
    NahmResidueBracketConvention .right bracket rightResidue

/-- A Nahm datum exposes its checked ODE on every point of the interval. -/
theorem NahmODEOn.nahmODEAt
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    {interval : Set ℝ} {bracket : V → V → V} {T : Fin 3 → ℝ → V}
    (h : NahmODEOn interval bracket T) {s : ℝ} (hs : s ∈ interval) :
    NahmODEAt bracket T s :=
  h s hs

/--
Nahm-equation input with a checked cyclic ODE and explicit endpoint residues.

The `leftSimplePoleResidue` and `rightSimplePoleResidue` fields inside
`boundaryResidueCondition` retain the analytic asymptotic assertions as named
obligations.  The ODE sign and the residue bracket signs are kernel-visible
definitions in this file.
-/
structure NahmData
    (V : Type uNahm) [NormedAddCommGroup V] [NormedSpace ℝ V] :
    Type uNahm where
  T : Fin 3 → ℝ → V
  bracket : V → V → V
  interval : Set ℝ
  smoothOnInterval : Prop
  nahmEquation : NahmODEOn interval bracket T
  boundaryResidueCondition : Nonempty (NahmIntervalResidueHypotheses interval bracket T)
  realityCondition : Prop
  spectralCondition : Prop

/-- The checked Nahm ODE carried by a `NahmData` package. -/
theorem NahmData.nahmODEOn
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (N : NahmData V) :
    NahmODEOn N.interval N.bracket N.T :=
  N.nahmEquation

/-- The endpoint residue package carried by a `NahmData` package. -/
theorem NahmData.boundaryResidues_nonempty
    {V : Type uNahm} [NormedAddCommGroup V] [NormedSpace ℝ V]
    (N : NahmData V) :
    Nonempty (NahmIntervalResidueHypotheses N.interval N.bracket N.T) :=
  N.boundaryResidueCondition

/--
The parameterized Nahm Dirac-family operator attached to a Nahm datum.

`operator x` is the bounded Hilbert-space realization selected at monopole
parameter `x`.  The proposition fields keep the analytic modelling obligations
named: regular dependence on the parameter, the chosen Sobolev/domain boundary
conditions, and the fact that this operator is built from the triple `T_i`.
-/
structure NahmDiracFamily
    (Base : Type uBase) {V : Type uNahm} (H : Type uH)
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (N : NahmData V) : Type (max (max uBase uNahm) uH) where
  operator : Base → HilbertOperator H
  parameterRegularity : Prop
  domainBoundaryCondition : Prop
  builtFromNahmData : Prop

/-- Kernel of a parameterized Nahm Dirac-family operator. -/
def NahmDiracFamily.kernel
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} (D : NahmDiracFamily Base H N) (x : Base) :
    Submodule ℂ H :=
  DiracKernel (D.operator x)

/-- The family kernel unfolds to the Dirac kernel of the operator at the parameter. -/
theorem NahmDiracFamily.kernel_eq_diracKernel
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} (D : NahmDiracFamily Base H N) (x : Base) :
    D.kernel x = DiracKernel (D.operator x) :=
  rfl

/--
Fredholm and kernel regularity for the full parameterized Nahm Dirac family.

This is the exact C005 construction boundary: every parameter has a Fredholm
realization, and the kernels have the additional smooth/rank regularity needed
to be treated as a finite-rank smooth kernel bundle.
-/
structure NahmDiracKernelRegularity
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} (D : NahmDiracFamily Base H N) :
    Type (max (max uBase uNahm) uH) where
  fredholmAt : ∀ x : Base, DiracOperatorFredholmRegularity (D.operator x)
  kernelBundleSmooth : Prop
  kernelProjectionRegularity : Prop
  constantKernelRankOnComponents : Prop

/-- A regular Nahm Dirac family has finite-dimensional kernel at every parameter. -/
theorem NahmDiracKernelRegularity.finiteDimensional_kernel
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    (R : NahmDiracKernelRegularity D) (x : Base) :
    FiniteDimensional ℂ (DiracKernel (D.operator x)) :=
  (R.fredholmAt x).finiteDimensional_kernel

/-- A regular Nahm Dirac family has closed operator range at every parameter. -/
theorem NahmDiracKernelRegularity.isClosed_range
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    (R : NahmDiracKernelRegularity D) (x : Base) :
    IsClosed (LinearMap.range (D.operator x).toLinearMap : Set H) :=
  (R.fredholmAt x).isClosed_range

/-- A regular Nahm Dirac family has finite-dimensional cokernel at every parameter. -/
theorem NahmDiracKernelRegularity.finiteDimensional_cokernel
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    (R : NahmDiracKernelRegularity D) (x : Base) :
    FiniteDimensional ℂ (H ⧸ LinearMap.range (D.operator x).toLinearMap) :=
  (R.fredholmAt x).finiteDimensional_cokernel

/--
Finite-rank smooth kernel bundle built from a regular Nahm Dirac family.

The fibers are still represented repo-locally as submodules of the ambient
Hilbert space.  The smooth bundle atlas, local triviality, and smoothness of
the projection family are retained as explicit obligations because the pinned
mathlib surface does not yet provide a theorem turning a smooth constant-rank
family of Fredholm kernels into a smooth vector bundle.
-/
structure FiniteRankSmoothKernelBundle
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} (D : NahmDiracFamily Base H N)
    (R : NahmDiracKernelRegularity D) :
    Type (max (max uBase uNahm) uH) where
  fiber : Base → Submodule ℂ H
  fiber_eq_diracKernel : ∀ x : Base, fiber x = DiracKernel (D.operator x)
  finiteRank : ∀ x : Base, FiniteDimensional ℂ (fiber x)
  kernelProjection : Base → HilbertOperator H
  kernelProjection_range :
    ∀ x : Base, LinearMap.range (kernelProjection x).toLinearMap = fiber x
  kernelProjection_idempotent :
    ∀ (x : Base) (ψ : H), kernelProjection x (kernelProjection x ψ) = kernelProjection x ψ
  kernelProjection_fixes_fiber :
    ∀ (x : Base) (ψ : fiber x), kernelProjection x ψ = ψ
  smoothBundleAtlas : Prop
  locallyTrivialFiniteRank : Prop
  smoothKernelProjection : Prop

/-- The finite-rank smooth kernel-bundle fiber is the Dirac kernel. -/
theorem FiniteRankSmoothKernelBundle.fiber_eq_kernel
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    {R : NahmDiracKernelRegularity D}
    (K : FiniteRankSmoothKernelBundle D R) (x : Base) :
    K.fiber x = D.kernel x := by
  rw [K.fiber_eq_diracKernel x, D.kernel_eq_diracKernel x]

/-- A finite-rank smooth kernel bundle has finite-dimensional fibers. -/
theorem FiniteRankSmoothKernelBundle.finiteDimensional_fiber
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    {R : NahmDiracKernelRegularity D}
    (K : FiniteRankSmoothKernelBundle D R) (x : Base) :
    FiniteDimensional ℂ (K.fiber x) :=
  K.finiteRank x

/-- The kernel projection has range equal to the kernel-bundle fiber. -/
theorem FiniteRankSmoothKernelBundle.projection_range
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    {R : NahmDiracKernelRegularity D}
    (K : FiniteRankSmoothKernelBundle D R) (x : Base) :
    LinearMap.range (K.kernelProjection x).toLinearMap = K.fiber x :=
  K.kernelProjection_range x

/-- The kernel projection is idempotent. -/
theorem FiniteRankSmoothKernelBundle.projection_idempotent
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    {R : NahmDiracKernelRegularity D}
    (K : FiniteRankSmoothKernelBundle D R) (x : Base) (ψ : H) :
    K.kernelProjection x (K.kernelProjection x ψ) = K.kernelProjection x ψ :=
  K.kernelProjection_idempotent x ψ

/--
Projected connection on the finite-rank kernel bundle.

Analytically this is the ambient trivial connection followed by orthogonal
projection onto the kernel bundle.  The exact formula is kept as a proposition
field until the repository has concrete smooth-section, projection, and
connection APIs for this bundle.
-/
structure ProjectedKernelConnection
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    {R : NahmDiracKernelRegularity D}
    (K : FiniteRankSmoothKernelBundle D R) (Conn : Type uConn) :
    Type (max (max (max uBase uNahm) uH) uConn) where
  ambientConnection : Conn
  projectedConnection : Conn
  projectionFormula : Prop
  smoothProjectedConnection : Prop
  preservesKernelSections : Prop
  compatibleWithKernelProjection : Prop

/-- The projected-connection projection-formula obligation is a named field. -/
theorem ProjectedKernelConnection.projectionFormula_self
    {Base : Type uBase} {V : Type uNahm} {H : Type uH}
    [TopologicalSpace Base]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {D : NahmDiracFamily Base H N}
    {R : NahmDiracKernelRegularity D}
    {K : FiniteRankSmoothKernelBundle D R} {Conn : Type uConn}
    (C : ProjectedKernelConnection K Conn) :
    C.projectionFormula = C.projectionFormula :=
  rfl

/--
Monopole-side model for the output of the transform.

The data includes the concrete operations needed to state the Bogomolny
equation, plus regularity, finite-energy, charge/framing, and gauge-quotient
conditions that are not currently provided by a terminal mathlib theorem.
-/
structure MonopoleData
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    (Base : Type uBase) (G : Type uG) (Conn : Type uConn)
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    (I : ModelWithCorners ℝ E Chart) (Ad : Base → Type uField)
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)] :
    Type (max (max (max (max uModel uChart) uBase) uG) (max uConn uField)) where
  bogomolnyData : BogomolnyFormData I Ad Conn
  connectionRegularity : Conn → Prop
  higgsRegularity : HiggsField Ad → Prop
  finiteEnergy : Conn → HiggsField Ad → Prop
  transformedConnection : Conn
  transformedHiggs : HiggsField Ad
  gaugeActionPreservesBogomolny : Prop
  chargeOrFramingCondition : Prop
  transformedConnection_regular : connectionRegularity transformedConnection
  transformedHiggs_regular : higgsRegularity transformedHiggs
  transformedFiniteEnergy : finiteEnergy transformedConnection transformedHiggs
  transformedBogomolny :
    IsBogomolny bogomolnyData transformedConnection transformedHiggs

/-- The transformed connection supplied by the data is regular. -/
theorem MonopoleData.transformed_connection_regular
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart} {Ad : Base → Type uField}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    (M : MonopoleData Base G Conn I Ad) :
    M.connectionRegularity M.transformedConnection :=
  M.transformedConnection_regular

/-- The transformed Higgs field supplied by the data is regular. -/
theorem MonopoleData.transformed_higgs_regular
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart} {Ad : Base → Type uField}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    (M : MonopoleData Base G Conn I Ad) :
    M.higgsRegularity M.transformedHiggs :=
  M.transformedHiggs_regular

/-- The transformed pair supplied by the data has finite energy. -/
theorem MonopoleData.transformed_finiteEnergy
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart} {Ad : Base → Type uField}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    (M : MonopoleData Base G Conn I Ad) :
    M.finiteEnergy M.transformedConnection M.transformedHiggs :=
  M.transformedFiniteEnergy

/-- The transformed pair supplied by the data satisfies the concrete Bogomolny equation. -/
theorem MonopoleData.transformed_isBogomolny
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart} {Ad : Base → Type uField}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    (M : MonopoleData Base G Conn I Ad) :
    IsBogomolny M.bogomolnyData M.transformedConnection M.transformedHiggs :=
  M.transformedBogomolny

/--
The analytic transform package expected from Nahm data.

The `diracFamily` and `kernelBundle` fields express the standard kernel-bundle
construction.  Fredholm and kernel regularity are now recorded through the
checked `NahmDiracKernelRegularity` package; projection formulae and
inverse/gauge compatibility remain proposition fields until concrete APIs are
available.
-/
structure NahmTransformPackage
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    (H : Type uH)
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (N : NahmData V) (M : MonopoleData Base G Conn I Ad) :
    Type (max (max (max (max (max (max uModel uChart) uBase) uG) uConn) uField)
      (max uNahm uH)) where
  diracFamily : NahmDiracFamily Base H N
  diracFredholmKernelRegularity : NahmDiracKernelRegularity diracFamily
  finiteRankSmoothKernelBundle :
    FiniteRankSmoothKernelBundle diracFamily diracFredholmKernelRegularity
  projectedKernelConnection :
    ProjectedKernelConnection finiteRankSmoothKernelBundle Conn
  kernelBundle : Base → Submodule ℂ H
  kernelBundle_eq_diracKernel : ∀ x : Base, kernelBundle x = DiracKernel (diracFamily.operator x)
  kernelBundle_eq_smoothKernelBundle :
    ∀ x : Base, kernelBundle x = finiteRankSmoothKernelBundle.fiber x
  kernelBundleFiniteRank : ∀ x : Base, FiniteDimensional ℂ (kernelBundle x)
  kernelBundleSmooth : Prop
  projectedConnectionWellDefined : Prop
  projectedConnection_eq_transformedConnection :
    projectedKernelConnection.projectedConnection = M.transformedConnection
  higgsFieldFromParameterAction : Prop
  transformedConnection_eq : M.transformedConnection = M.transformedConnection
  transformedHiggs_eq : M.transformedHiggs = M.transformedHiggs
  producesBogomolny :
    IsBogomolny M.bogomolnyData M.transformedConnection M.transformedHiggs
  inverseNahmReconstruction : Prop
  gaugeCompatibility : Prop

/-- A transform package exposes its Bogomolny output field. -/
theorem NahmTransformPackage.produces_bogomolny
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) :
    IsBogomolny M.bogomolnyData M.transformedConnection M.transformedHiggs :=
  P.producesBogomolny

/-- A transform package exposes the kernel-as-Dirac-kernel equality. -/
theorem NahmTransformPackage.kernel_eq_diracKernel
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) (x : Base) :
    P.kernelBundle x = DiracKernel (P.diracFamily.operator x) :=
  P.kernelBundle_eq_diracKernel x

/-- A transform package exposes finite-dimensionality of its kernel bundle fibers. -/
theorem NahmTransformPackage.kernelBundle_finiteDimensional
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) (x : Base) :
    FiniteDimensional ℂ (P.kernelBundle x) :=
  P.kernelBundleFiniteRank x

/-- A transform package exposes Fredholm finite-dimensionality for Dirac kernels. -/
theorem NahmTransformPackage.diracKernel_finiteDimensional
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) (x : Base) :
    FiniteDimensional ℂ (DiracKernel (P.diracFamily.operator x)) :=
  P.diracFredholmKernelRegularity.finiteDimensional_kernel x

/-- A transform package exposes closed-range Fredholm regularity for its Dirac operators. -/
theorem NahmTransformPackage.diracFamily_isClosed_range
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) (x : Base) :
    IsClosed (LinearMap.range (P.diracFamily.operator x).toLinearMap : Set H) :=
  P.diracFredholmKernelRegularity.isClosed_range x

/-- A transform package exposes the structured finite-rank smooth kernel-bundle fiber. -/
theorem NahmTransformPackage.kernelBundle_eq_smoothKernelBundle_field
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) (x : Base) :
    P.kernelBundle x = P.finiteRankSmoothKernelBundle.fiber x :=
  P.kernelBundle_eq_smoothKernelBundle x

/-- The structured kernel-bundle projection in a transform package has the expected range. -/
theorem NahmTransformPackage.kernelProjection_range
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) (x : Base) :
    LinearMap.range (P.finiteRankSmoothKernelBundle.kernelProjection x).toLinearMap =
      P.finiteRankSmoothKernelBundle.fiber x :=
  P.finiteRankSmoothKernelBundle.projection_range x

/-- The structured kernel-bundle projection in a transform package is idempotent. -/
theorem NahmTransformPackage.kernelProjection_idempotent
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) (x : Base) (ψ : H) :
    P.finiteRankSmoothKernelBundle.kernelProjection x
        (P.finiteRankSmoothKernelBundle.kernelProjection x ψ) =
      P.finiteRankSmoothKernelBundle.kernelProjection x ψ :=
  P.finiteRankSmoothKernelBundle.projection_idempotent x ψ

/-- The projected kernel connection is the transformed connection in the package. -/
theorem NahmTransformPackage.projectedConnection_eq_transformedConnection_field
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) :
    P.projectedKernelConnection.projectedConnection = M.transformedConnection :=
  P.projectedConnection_eq_transformedConnection

/--
The package-level Bogomolny field transfers from the transformed connection to
the projected kernel connection.

This is a checked bridge, not the terminal Nahm-transform curvature
calculation: the analytic proof that the projection formula and transformed
Higgs field produce the Bogomolny identity is still the package field
`producesBogomolny`.
-/
theorem NahmTransformPackage.projectedConnection_isBogomolny
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) :
    IsBogomolny M.bogomolnyData
      P.projectedKernelConnection.projectedConnection M.transformedHiggs := by
  rw [P.projectedConnection_eq_transformedConnection]
  exact P.producesBogomolny

/--
Concrete unfolded equation for the projected connection and transformed Higgs:
`*F_A = d_A Phi` in the operations carried by `BogomolnyFormData`.

The theorem is conditional on an existing `NahmTransformPackage`; it records the
last checked bridge currently available repo-locally before the missing
curvature/Higgs computation.
-/
theorem NahmTransformPackage.projectedConnection_bogomolny_equation
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn]
    {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) :
    M.bogomolnyData.hodgeStarCurvature
        (M.bogomolnyData.curvature P.projectedKernelConnection.projectedConnection) =
      M.bogomolnyData.covariantDerivativeHiggs
        P.projectedKernelConnection.projectedConnection M.transformedHiggs :=
  isBogomolny_iff.mp P.projectedConnection_isBogomolny

/-- Hypotheses retained by the normalized Nahm-transform statement boundary. -/
def NahmTransformHypotheses
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn] {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
  (N : NahmData V) (M : MonopoleData Base G Conn I Ad) : Prop :=
  N.smoothOnInterval ∧
    NahmODEOn N.interval N.bracket N.T ∧
      Nonempty (NahmIntervalResidueHypotheses N.interval N.bracket N.T) ∧
        N.realityCondition ∧
          N.spectralCondition ∧
            True ∧
              M.gaugeActionPreservesBogomolny ∧
                M.chargeOrFramingCondition

/-- Conclusion package expected from the Nahm transform. -/
def NahmTransformConclusion
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    (H : Type uH)
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn] {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (N : NahmData V) (M : MonopoleData Base G Conn I Ad) : Prop :=
  Nonempty (NahmTransformPackage H N M) ∧
    IsBogomolny M.bogomolnyData M.transformedConnection M.transformedHiggs ∧
      M.connectionRegularity M.transformedConnection ∧
        M.higgsRegularity M.transformedHiggs ∧
          M.finiteEnergy M.transformedConnection M.transformedHiggs

/--
Stage1 normalized statement shape for THM-M-1545.

For every explicitly modelled Nahm input satisfying the Nahm equations,
boundary residues, reality, spectral, base, gauge, and framing hypotheses, the
Nahm transform should produce a kernel-bundle package and a monopole pair
satisfying the Bogomolny equation with regularity and finite energy.

This is only a precise statement boundary; it is not a terminal proof of the
Nahm transform.
-/
def StatementShape : Prop :=
  ∀ (E : Type uModel) (Chart : Type uChart) (Base : Type uBase)
    (G : Type uG) (Conn : Type uConn) (Ad : Base → Type uField)
    (V : Type uNahm) (H : Type uH)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace Chart]
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [Group G] [MulAction G Conn]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H],
      ∀ (I : ModelWithCorners ℝ E Chart)
        (N : NahmData V) (M : MonopoleData Base G Conn I Ad),
        NahmTransformHypotheses N M →
          NahmTransformConclusion H N M

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (E : Type uModel) (Chart : Type uChart) (Base : Type uBase)
      (G : Type uG) (Conn : Type uConn) (Ad : Base → Type uField)
      (V : Type uNahm) (H : Type uH)
      [NormedAddCommGroup E] [NormedSpace ℝ E]
      [TopologicalSpace Chart]
      [TopologicalSpace Base] [ChartedSpace Chart Base]
      [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
      [Group G] [MulAction G Conn]
      [NormedAddCommGroup V] [NormedSpace ℝ V]
      [NormedAddCommGroup H] [InnerProductSpace ℂ H],
        ∀ (I : ModelWithCorners ℝ E Chart)
          (N : NahmData V) (M : MonopoleData Base G Conn I Ad),
          NahmTransformHypotheses N M →
            NahmTransformConclusion H N M) :
    StatementShape.{uModel, uChart, uBase, uG, uConn, uField, uNahm, uH} :=
  h

/-- A checked wrapper assembling the conclusion from an existing package and monopole fields. -/
theorem nahmTransformConclusion_of_package
    {E : Type uModel} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {Chart : Type uChart} [TopologicalSpace Chart]
    {Base : Type uBase} {G : Type uG} {Conn : Type uConn}
    {Ad : Base → Type uField} {V : Type uNahm}
    {H : Type uH}
    [TopologicalSpace Base] [ChartedSpace Chart Base]
    [Group G] [MulAction G Conn] {I : ModelWithCorners ℝ E Chart}
    [∀ x, NormedAddCommGroup (Ad x)] [∀ x, NormedSpace ℝ (Ad x)]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {N : NahmData V} {M : MonopoleData Base G Conn I Ad}
    (P : NahmTransformPackage H N M) :
    NahmTransformConclusion H N M :=
  ⟨⟨P⟩, P.produces_bogomolny,
    M.transformed_connection_regular,
    M.transformed_higgs_regular,
    M.transformed_finiteEnergy⟩

/-- Structured audit record for the gauge-theory APIs needed by the Nahm transform. -/
structure NahmGaugeAPIAudit where
  childTask : String
  mathlibRevision : String
  presentSubstrate : List String
  absentOrIncompleteSubstrate : List String
  integrationDecision : String
  validationTarget : String
deriving Repr

/--
C003 audit of the pinned local mathlib surface for the monopole side of the
Nahm transform.

This record is intentionally proof-neutral: it records checked declarations and
specific missing API families, without claiming that the Nahm transform has
been proved in this repository.
-/
def nahmGaugeAPIAudit : NahmGaugeAPIAudit := {
  childTask := "S1-M-204-C003",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  presentSubstrate := [
    "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
    "ContinuousAlternatingMap",
    "Mathlib.Geometry.Manifold.ChartedSpace",
    "ChartedSpace",
    "IsManifold",
    "TangentSpace",
    "Mathlib.Geometry.Manifold.Riemannian.Basic",
    "Bundle.RiemannianBundle",
    "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
    "IsCovariantDerivativeOn",
    "ContMDiffCovariantDerivativeOn",
    "CovariantDerivative",
    "CovariantDerivative.addOneForm",
    "CovariantDerivative.difference",
    "MulAction"
  ],
  absentOrIncompleteSubstrate := [
    "no `PrincipalBundle` declaration or principal-bundle module in the pinned local mathlib tree",
    "no gauge group API as automorphisms of a principal bundle or associated adjoint bundle",
    "no smooth principal connection or Ehresmann connection API with curvature two-form",
    "no adjoint-bundle-valued smooth curvature two-form API",
    "no dedicated Higgs-field section API for gauge-Higgs monopole data",
    "no Hodge-star construction on smooth adjoint-bundle-valued forms over an oriented Riemannian three-manifold",
    "no terminal Nahm-transform, Bogomolny-monopole, or ADHMN theorem in the pinned local mathlib tree"
  ],
  integrationDecision :=
    "formalization_debt: the repo-local statement keeps principal-bundle, " ++
    "curvature, Higgs-field, and Hodge-star operations explicit in the data; " ++
    "no external Lean 4 proof was found or pinned during this child audit, so " ++
    "there is no completed state carrying repo_local_integration_debt",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_204.lean"
}

/--
Checked operator-theoretic anchor: mathlib's Fredholm alternative for compact
operators.

This is useful nearby analytic substrate, but it is not the Fredholm theorem
for the Nahm Dirac family.  C005 therefore records it only as an adjacent
checked anchor and keeps the Nahm Dirac Fredholm regularity theorem as
formalization debt.
-/
theorem compactOperator_fredholmAlternative_anchor
    {H : Type uH} [NormedAddCommGroup H] [NormedSpace ℂ H] [CompleteSpace H]
    {T : H →L[ℂ] H} (hT : IsCompactOperator T) {μ : ℂ} (hμ : μ ≠ 0) :
    Module.End.HasEigenvalue (T : Module.End ℂ H) μ ∨ μ ∈ resolventSet ℂ T :=
  IsCompactOperator.hasEigenvalue_or_mem_resolventSet hT hμ

/-- Structured C005 audit record for the Nahm Dirac-family Fredholm regularity surface. -/
def nahmDiracFredholmKernelAudit : NahmGaugeAPIAudit := {
  childTask := "S1-M-204-C005",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  presentSubstrate := [
    "HilbertOperator",
    "DiracKernel",
    "DiracOperatorFredholmRegularity",
    "NahmDiracFamily",
    "NahmDiracKernelRegularity",
    "NahmTransformPackage.diracKernel_finiteDimensional",
    "NahmTransformPackage.diracFamily_isClosed_range",
    "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
    "IsCompactOperator.hasEigenvalue_or_mem_resolventSet"
  ],
  absentOrIncompleteSubstrate := [
    "no mathlib `Fredholm` operator class or index API for general bounded/unbounded operators",
    "no geometric Dirac operator API on monopole/Nahm spinor bundles",
    "no Sobolev-domain realization for the interval Nahm Dirac operator",
    "no elliptic regularity theorem proving closed range and finite-dimensional kernel/cokernel for this family",
    "no smooth kernel-bundle theorem converting parameterized finite-dimensional kernels into a vector bundle",
    "no terminal Nahm-transform theorem connecting the projected connection to the Bogomolny equation"
  ],
  integrationDecision :=
    "formalization_debt: C005 adds checked local statement carriers and " ++
    "projection lemmas for Dirac Fredholm/kernel regularity, plus a checked " ++
    "compact-operator Fredholm-alternative anchor.  No external terminal " ++
    "Nahm-transform Lean 4 proof is pinned/imported/checked here, so this " ++
    "child must remain open and carries no completed repo_local_integration_debt.",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_204.lean"
}

/-- Structured C006 audit record for the smooth kernel bundle and projected connection. -/
def nahmKernelBundleProjectedConnectionAudit : NahmGaugeAPIAudit := {
  childTask := "S1-M-204-C006",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  presentSubstrate := [
    "FiniteRankSmoothKernelBundle",
    "FiniteRankSmoothKernelBundle.fiber_eq_kernel",
    "FiniteRankSmoothKernelBundle.finiteDimensional_fiber",
    "FiniteRankSmoothKernelBundle.projection_range",
    "FiniteRankSmoothKernelBundle.projection_idempotent",
    "ProjectedKernelConnection",
    "ProjectedKernelConnection.projectionFormula_self",
    "NahmTransformPackage.finiteRankSmoothKernelBundle",
    "NahmTransformPackage.projectedKernelConnection",
    "NahmTransformPackage.kernelProjection_range",
    "NahmTransformPackage.kernelProjection_idempotent",
    "NahmTransformPackage.projectedConnection_eq_transformedConnection_field"
  ],
  absentOrIncompleteSubstrate := [
    "no concrete vector-bundle construction from a smooth constant-rank family of Dirac kernels",
    "no proof that the abstract kernel projections are the orthogonal projections onto the Dirac kernels",
    "no smooth-section API specialized to this kernel bundle and projection family",
    "no concrete ambient trivial connection followed by projection formula on kernel-bundle sections",
    "no curvature computation for the projected connection",
    "no theorem proving that the projected connection and transformed Higgs field satisfy Bogomolny"
  ],
  integrationDecision :=
    "formalization_debt: C006 adds checked local carriers for the finite-rank " ++
    "smooth kernel bundle, its projection family, and the projected connection " ++
    "used by the transform.  The analytic construction and curvature/Bogomolny " ++
    "proof remain proposition-level obligations; no external terminal " ++
    "Nahm-transform Lean 4 proof is pinned/imported/checked here, so there is " ++
    "no completed repo_local_integration_debt state.",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_204.lean"
}

/--
Structured C007 audit record for the projected-connection Bogomolny equation.

This audit deliberately classifies the remaining work as formalization debt:
the repo-local file can transport the existing package-level Bogomolny field to
the projected connection and unfold it as a concrete form equation, but it does
not prove the missing curvature/Higgs computation from Nahm data.
-/
def nahmProjectedBogomolnyAudit : NahmGaugeAPIAudit := {
  childTask := "S1-M-204-C007",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  presentSubstrate := [
    "BogomolnyFormData",
    "IsBogomolny",
    "isBogomolny_iff",
    "ProjectedKernelConnection",
    "NahmTransformPackage.projectedConnection_eq_transformedConnection_field",
    "NahmTransformPackage.projectedConnection_isBogomolny",
    "NahmTransformPackage.projectedConnection_bogomolny_equation"
  ],
  absentOrIncompleteSubstrate := [
    "no concrete curvature formula for the projected kernel connection",
    "no concrete transformed-Higgs definition from parameter multiplication or Nahm endpoint data",
    "no Weitzenbock/Green-kernel identity connecting the Nahm equations to the projected curvature",
    "no Hodge-star theorem for adjoint-bundle-valued curvature forms on the selected three-manifold",
    "no proof that the projection-formula connection and transformed Higgs satisfy `*F_A = d_A Phi` without taking Bogomolny as a package field",
    "no terminal repo-local or pinned external Lean 4 Nahm-transform Bogomolny theorem"
  ],
  integrationDecision :=
    "formalization_debt: C007 adds checked bridge lemmas from an existing " ++
    "NahmTransformPackage to the concrete projected-connection Bogomolny " ++
    "equation.  It does not close the analytic curvature/Higgs computation " ++
    "from Nahm data, and no external terminal Lean 4 proof is " ++
    "pinned/imported/checked here; therefore there is no completed " ++
    "repo_local_integration_debt state.",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_204.lean"
}

/-- Primary-source surfaces checked or attempted for external Nahm-transform Lean proofs. -/
def externalPrimarySearchSurfaces : List String := [
  "local pinned mathlib tree under Formalizations/Lean/.lake/packages/mathlib",
  "local awesome_theorems Stage1 artifacts and prior S1-M-204 child ledgers",
  "GitHub CLI authentication state via `gh auth status`",
  "GitHub REST repository search for quoted Nahm-transform / Lean terms",
  "GitHub REST code search for quoted Nahm-transform / Lean terms"
]

/-- External proof-search terms used for the C008 Nahm-transform audit. -/
def externalLeanProofSearchTerms : List String := [
  "Nahm transform Lean",
  "Nahm transform theorem Lean",
  "Nahm Bogomolny Lean",
  "Nahm equation Lean 4",
  "ADHMN Lean",
  "Bogomolny monopole Lean"
]

/--
Structured C008 audit record for external Nahm-transform proof search.

The requested authenticated GitHub code search could not be completed because
the local GitHub CLI has no authenticated host.  Unauthenticated primary-source
checks did not locate a Lean 4 proof repository or source file for the terminal
Nahm-transform theorem, and no external proof is pinned/imported/checked here.
-/
def nahmExternalProofSearchAudit : NahmGaugeAPIAudit := {
  childTask := "S1-M-204-C008",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  presentSubstrate := [
    "externalPrimarySearchSurfaces",
    "externalLeanProofSearchTerms",
    "absentTerminalSearchTerms",
    "nahmGaugeAPIAudit",
    "nahmDiracFredholmKernelAudit",
    "nahmKernelBundleProjectedConnectionAudit",
    "nahmProjectedBogomolnyAudit"
  ],
  absentOrIncompleteSubstrate := [
    "GitHub CLI is not authenticated on this machine, so the requested authenticated primary-source GitHub code search is blocked",
    "GitHub REST code search returned 401 Requires authentication for quoted Nahm-transform Lean code queries",
    "GitHub REST repository search for quoted Nahm-transform / Lean terms returned no candidate proof repository",
    "local pinned mathlib search found no `Nahm`, `ADHMN`, `Bogomolny`, or terminal monopole-transform theorem family",
    "no external Lean 4 Nahm-transform proof body, module, theorem name, or Lake dependency was found to pin/import/check"
  ],
  integrationDecision :=
    "not_repo_local_closed / formalization_debt with an external-search " ++
    "authentication blocker: no external checked Lean 4 Nahm-transform proof " ++
    "was found and no anchor-only evidence is treated as completed.  To close " ++
    "a future external proof branch, an authenticated primary-source GitHub " ++
    "code search must identify a concrete Lean project and the repository must " ++
    "pin/import/check it locally or record a dependency/toolchain/license/API " ++
    "blocker.",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_204.lean"
}

/--
Structured C009 synchronization audit for the Stage1 checklist, theorem-tree
ledger, and public merge surface.

This record is intentionally an open-gate audit.  It records that the local
Lean artifact is the checked statement/debt surface, while public blueprint and
todo synchronization must be performed later by a serialized integrator.
-/
def nahmStage1SynchronizationAudit : NahmGaugeAPIAudit := {
  childTask := "S1-M-204-C009",
  mathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
  presentSubstrate := [
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_204.lean",
    "StatementShape",
    "NahmTransformHypotheses",
    "NahmTransformConclusion",
    "NahmTransformPackage.projectedConnection_bogomolny_equation",
    "nahmGaugeAPIAudit",
    "nahmDiracFredholmKernelAudit",
    "nahmKernelBundleProjectedConnectionAudit",
    "nahmProjectedBogomolnyAudit",
    "nahmExternalProofSearchAudit",
    ".cron/results/stage1_20260430/codex_workers/S1-M-204.md",
    ".cron/results/stage1_20260430_child/codex_workers/S1-M-204-C009.md"
  ],
  absentOrIncompleteSubstrate := [
    "public Stage1 checklist remains open and was not edited by this child",
    "public todo/README surfaces remain reserved for serialized integrator merge-back",
    "no terminal repo-local proof of StatementShape is present",
    "no pinned/imported external Lean 4 Nahm-transform proof is present",
    "authenticated GitHub code search remains blocked unless a future process has GitHub credentials",
    "theorem-tree leaves for concrete principal bundles, Hodge star, Dirac Fredholm regularity, kernel-bundle smoothness, and the projected curvature/Bogomolny computation remain open"
  ],
  integrationDecision :=
    "not_repo_local_closed / formalization_debt: C009 synchronizes the " ++
    "repo-local checked Lean surface with the private theorem-tree ledger and " ++
    "records exact public backfill text for a later integrator.  The public " ++
    "checklist must stay open; no completed state relies on " ++
    "repo_local_integration_debt, and no public blueprint/todo/README surface " ++
    "is edited by this child.",
  validationTarget :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_204.lean"
}

/-- mathlib modules checked while locating repo-local Nahm-transform anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.Deriv.Basic",
  "Mathlib.Algebra.Algebra.Spectrum.Basic",
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.InnerProductSpace.Orientation",
  "Mathlib.Analysis.Normed.Operator.Basic",
  "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
  "Mathlib.Geometry.Manifold.ChartedSpace",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.LinearAlgebra.FiniteDimensional.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.SmoothSection",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.Analysis.Distribution.TemperedDistribution"
]

/-- Nearby checked names used or audited for this Stage1 boundary. -/
def mathlibAnchorNames : List String := [
  "HilbertOperator",
  "ContinuousLinearMap",
  "ContinuousLinearMap.id",
  "ContinuousLinearMap.id_apply",
  "LinearMap.ker",
  "Submodule",
  "FiniteDimensional",
  "DiracOperatorFredholmRegularity",
  "NahmDiracFamily",
  "NahmDiracKernelRegularity",
  "FiniteRankSmoothKernelBundle",
  "ProjectedKernelConnection",
  "NahmTransformPackage.finiteRankSmoothKernelBundle",
  "NahmTransformPackage.projectedKernelConnection",
  "NahmTransformPackage.projectedConnection_isBogomolny",
  "NahmTransformPackage.projectedConnection_bogomolny_equation",
  "nahmProjectedBogomolnyAudit",
  "nahmExternalProofSearchAudit",
  "nahmStage1SynchronizationAudit",
  "IsCompactOperator.hasEigenvalue_or_mem_resolventSet",
  "spectrum",
  "MulAction",
  "GaugeEquivalent",
  "ContinuousAlternatingMap",
  "AdjointValuedDifferentialForm",
  "TangentSpace",
  "Orientation",
  "Bundle.RiemannianBundle",
  "OrientedRiemannianThreeManifold",
  "BogomolnyFormData",
  "HasDerivAt",
  "NahmBracketTerm",
  "NahmODEAt",
  "NahmODEOn",
  "NahmLeftSimplePoleResidue",
  "NahmRightSimplePoleResidue",
  "NahmResidueBracketConvention",
  "NahmIntervalResidueHypotheses",
  "ChartedSpace",
  "IsManifold",
  "CovariantDerivative",
  "IsCovariantDerivativeOn"
]

/-- Search terms that did not locate a terminal Nahm-transform theorem in pinned local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Nahm",
  "Nahm transform",
  "Nahm equations",
  "ADHMN",
  "monopole",
  "Bogomolny",
  "Bogomolny equation",
  "Dirac family",
  "kernel bundle",
  "gauge theory",
  "Yang-Mills-Higgs"
]

/-! ## Audit probes retained in the checked file. -/

#check HilbertOperator
#check OperatorSpectrum
#check DiracKernel
#check zero_mem_diracKernel
#check diracKernel_zero_eq_top
#check identityHilbertOperator_apply
#check DiracOperatorFredholmRegularity
#check DiracOperatorFredholmRegularity.isClosed_range
#check DiracOperatorFredholmRegularity.finiteDimensional_kernel
#check DiracOperatorFredholmRegularity.finiteDimensional_cokernel
#check GaugeEquivalent
#check gaugeEquivalent_refl
#check gaugeOrbit
#check AdjointValuedDifferentialForm
#check HiggsField
#check OrientedRiemannianThreeManifold
#check BogomolnyFormData
#check IsBogomolny
#check isBogomolny_zero
#check NahmBracketTerm
#check NahmODEAt
#check NahmODEOn
#check nahmODEAt_zero
#check nahmODEAt_one
#check nahmODEAt_two
#check NahmEndpointSide
#check NahmResidueBracketTerm
#check NahmLeftSimplePoleResidue
#check NahmRightSimplePoleResidue
#check NahmResidueBracketConvention
#check NahmIntervalResidueHypotheses
#check NahmData.nahmODEOn
#check NahmData.boundaryResidues_nonempty
#check NahmData
#check NahmDiracFamily
#check NahmDiracFamily.kernel
#check NahmDiracFamily.kernel_eq_diracKernel
#check NahmDiracKernelRegularity
#check NahmDiracKernelRegularity.finiteDimensional_kernel
#check NahmDiracKernelRegularity.isClosed_range
#check NahmDiracKernelRegularity.finiteDimensional_cokernel
#check FiniteRankSmoothKernelBundle
#check FiniteRankSmoothKernelBundle.fiber_eq_kernel
#check FiniteRankSmoothKernelBundle.finiteDimensional_fiber
#check FiniteRankSmoothKernelBundle.projection_range
#check FiniteRankSmoothKernelBundle.projection_idempotent
#check ProjectedKernelConnection
#check ProjectedKernelConnection.projectionFormula_self
#check MonopoleData
#check NahmTransformPackage
#check NahmTransformHypotheses
#check NahmTransformConclusion
#check StatementShape
#check nahmTransformConclusion_of_package
#check NahmTransformPackage.kernelBundle_finiteDimensional
#check NahmTransformPackage.diracKernel_finiteDimensional
#check NahmTransformPackage.diracFamily_isClosed_range
#check NahmTransformPackage.kernelBundle_eq_smoothKernelBundle_field
#check NahmTransformPackage.kernelProjection_range
#check NahmTransformPackage.kernelProjection_idempotent
#check NahmTransformPackage.projectedConnection_eq_transformedConnection_field
#check NahmTransformPackage.projectedConnection_isBogomolny
#check NahmTransformPackage.projectedConnection_bogomolny_equation
#check NahmGaugeAPIAudit
#check nahmGaugeAPIAudit
#check compactOperator_fredholmAlternative_anchor
#check nahmDiracFredholmKernelAudit
#check nahmKernelBundleProjectedConnectionAudit
#check nahmProjectedBogomolnyAudit
#check externalPrimarySearchSurfaces
#check externalLeanProofSearchTerms
#check nahmExternalProofSearchAudit
#check nahmStage1SynchronizationAudit
#check spectrum
#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet
#check ContinuousLinearMap.id
#check LinearMap.ker
#check ContinuousAlternatingMap
#check TangentSpace
#check Orientation
#check Bundle.RiemannianBundle
#check IsManifold
#check ChartedSpace
#check CovariantDerivative
#check HasDerivAt

end S1_M_204
end Stage1
end AwesomeTheorems
