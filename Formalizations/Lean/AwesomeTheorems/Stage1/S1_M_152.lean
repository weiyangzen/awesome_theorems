import Mathlib.Analysis.Calculus.ContDiffHolder.Pointwise
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.TestFunction
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Topology.MetricSpace.HolderNorm

/-!
# S1-M-152 / THM-M-1189: Schauder estimates for the heat equation

This Stage1 artifact records a conservative Lean 4 boundary for parabolic
Schauder estimates for the heat equation.  The pinned mathlib snapshot has
usable pieces for finite-dimensional Euclidean domains, classical derivatives,
the Laplacian, `ContDiffOn`, and Holder continuity.  This audit did not find a
terminal theorem for the parabolic Schauder estimate.

The declarations below therefore normalize a statement shape and provide small
checked wrappers around available mathlib anchors.  They introduce no proof
placeholders and do not claim the terminal PDE theorem.
-/

noncomputable section

open Set TopologicalSpace
open scoped NNReal ENNReal Topology unitInterval Distributions

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_152

universe u v

/-- Space-time model for a heat equation on finite-dimensional Euclidean space. -/
abbrev HeatSpace (ι : Type u) [Fintype ι] : Type u :=
  ℝ × EuclideanSpace ℝ ι

/-- Scalar space-time field used by the normalized heat-equation statement. -/
abbrev ScalarField (ι : Type u) [Fintype ι] : Type u :=
  HeatSpace ι → ℝ

/-- Scalar distributions on an open space-time heat domain. -/
abbrev ScalarDistributionOnHeatDomain
    {ι : Type u} [Fintype ι] (U : Opens (HeatSpace ι)) : Type u :=
  Distribution U ℝ ⊤

/-- Two-sided parabolic cylinder `|t - t₀| < r²`, `dist x x₀ < r`. -/
def twoSidedParabolicCylinder
    {ι : Type u} [Fintype ι] (center : HeatSpace ι) (radius : ℝ) :
    Set (HeatSpace ι) :=
  {z | |z.1 - center.1| < radius ^ 2 ∧ dist z.2 center.2 < radius}

/-- Backward parabolic cylinder `(t₀ - r², t₀) × B(x₀,r)`. -/
def backwardParabolicCylinder
    {ι : Type u} [Fintype ι] (center : HeatSpace ι) (radius : ℝ) :
    Set (HeatSpace ι) :=
  {z | center.1 - radius ^ 2 < z.1 ∧ z.1 < center.1 ∧ dist z.2 center.2 < radius}

/-- Forward parabolic cylinder `(t₀, t₀ + r²) × B(x₀,r)`. -/
def forwardParabolicCylinder
    {ι : Type u} [Fintype ι] (center : HeatSpace ι) (radius : ℝ) :
    Set (HeatSpace ι) :=
  {z | center.1 < z.1 ∧ z.1 < center.1 + radius ^ 2 ∧ dist z.2 center.2 < radius}

/-- A named local parabolic cylinder with a positive radius. -/
structure ParabolicCylinder (ι : Type u) [Fintype ι] : Type u where
  center : HeatSpace ι
  radius : ℝ
  radius_pos : 0 < radius

/-- The two-sided set associated to a named parabolic cylinder. -/
def ParabolicCylinder.twoSidedSet
    {ι : Type u} [Fintype ι] (Q : ParabolicCylinder ι) :
    Set (HeatSpace ι) :=
  twoSidedParabolicCylinder Q.center Q.radius

/-- The backward set associated to a named parabolic cylinder. -/
def ParabolicCylinder.backwardSet
    {ι : Type u} [Fintype ι] (Q : ParabolicCylinder ι) :
    Set (HeatSpace ι) :=
  backwardParabolicCylinder Q.center Q.radius

/-- The forward set associated to a named parabolic cylinder. -/
def ParabolicCylinder.forwardSet
    {ι : Type u} [Fintype ι] (Q : ParabolicCylinder ι) :
    Set (HeatSpace ι) :=
  forwardParabolicCylinder Q.center Q.radius

/--
Parabolic distance scale for anisotropic Holder control.

The square root on the time component gives time weight two relative to the
spatial variables, matching the scaling used by heat-equation Schauder
estimates.
-/
def parabolicDistance
    {ι : Type u} [Fintype ι] (z w : HeatSpace ι) : ℝ :=
  max (Real.sqrt |z.1 - w.1|) (dist z.2 w.2)

/-- Extended nonnegative parabolic distance used to mirror `HolderOnWith`. -/
def parabolicEdist
    {ι : Type u} [Fintype ι] (z w : HeatSpace ι) : ENNReal :=
  ENNReal.ofReal (parabolicDistance z w)

/--
Anisotropic parabolic Holder seminorm bound.

This is the parabolic analogue of `HolderOnWith`: it replaces the ambient
space-time metric by `parabolicEdist`, so the time variable has weight two.
-/
def parabolicHolderSeminormBound
    {ι : Type u} [Fintype ι]
    {Y : Type v} [PseudoEMetricSpace Y]
    (C α : ℝ≥0) (f : HeatSpace ι → Y) (Q : Set (HeatSpace ι)) : Prop :=
  ∀ z ∈ Q, ∀ w ∈ Q, edist (f z) (f w) ≤
    (C : ENNReal) * parabolicEdist z w ^ (α : ℝ)

/-- Supremum-norm bound for scalar fields on a parabolic cylinder. -/
def parabolicSupNormBound
    {ι : Type u} [Fintype ι]
    (M : ℝ≥0) (u : ScalarField ι) (Q : Set (HeatSpace ι)) : Prop :=
  ∀ z ∈ Q, ‖u z‖ ≤ (M : ℝ)

/--
Bounded anisotropic parabolic Holder norm API for scalar fields.

The first constant bounds the scalar sup norm and the second bounds the
parabolic Holder seminorm.  Later Schauder estimates can replace this bounded
predicate by an actual bundled norm once the surrounding analysis API exists.
-/
def parabolicHolderNormBound
    {ι : Type u} [Fintype ι]
    (M C α : ℝ≥0) (u : ScalarField ι) (Q : Set (HeatSpace ι)) : Prop :=
  parabolicSupNormBound M u Q ∧ parabolicHolderSeminormBound C α u Q

/-- Membership in the two-sided parabolic cylinder unfolds to its inequalities. -/
theorem mem_twoSidedParabolicCylinder
    {ι : Type u} [Fintype ι] {center z : HeatSpace ι} {radius : ℝ} :
    z ∈ twoSidedParabolicCylinder center radius ↔
      |z.1 - center.1| < radius ^ 2 ∧ dist z.2 center.2 < radius :=
  Iff.rfl

/-- Membership in the backward parabolic cylinder unfolds to its inequalities. -/
theorem mem_backwardParabolicCylinder
    {ι : Type u} [Fintype ι] {center z : HeatSpace ι} {radius : ℝ} :
    z ∈ backwardParabolicCylinder center radius ↔
      center.1 - radius ^ 2 < z.1 ∧ z.1 < center.1 ∧ dist z.2 center.2 < radius :=
  Iff.rfl

/-- Membership in the forward parabolic cylinder unfolds to its inequalities. -/
theorem mem_forwardParabolicCylinder
    {ι : Type u} [Fintype ι] {center z : HeatSpace ι} {radius : ℝ} :
    z ∈ forwardParabolicCylinder center radius ↔
      center.1 < z.1 ∧ z.1 < center.1 + radius ^ 2 ∧ dist z.2 center.2 < radius :=
  Iff.rfl

/-- A bounded parabolic Holder norm package exposes its supremum bound. -/
theorem parabolicHolderNormBound.supNorm
    {ι : Type u} [Fintype ι]
    {M C α : ℝ≥0} {u : ScalarField ι} {Q : Set (HeatSpace ι)}
    (h : parabolicHolderNormBound M C α u Q) :
    parabolicSupNormBound M u Q :=
  h.1

/-- A bounded parabolic Holder norm package exposes its seminorm bound. -/
theorem parabolicHolderNormBound.seminorm
    {ι : Type u} [Fintype ι]
    {M C α : ℝ≥0} {u : ScalarField ι} {Q : Set (HeatSpace ι)}
    (h : parabolicHolderNormBound M C α u Q) :
    parabolicHolderSeminormBound C α u Q :=
  h.2

/--
The classical formal heat operator `∂_t u - Δ_x u`.

This is only an expression-level object.  A terminal Schauder theorem still
needs hypotheses proving that these derivatives represent the intended weak or
classical PDE data on the chosen parabolic cylinder.
-/
def heatOperatorFormal {ι : Type u} [Fintype ι] (u : ScalarField ι) :
    ScalarField ι :=
  fun z =>
    deriv (fun t : ℝ => u (t, z.2)) z.1 -
      Laplacian.laplacian (fun x : EuclideanSpace ℝ ι => u (z.1, x)) z.2

/-- The formal heat operator unfolds to the time derivative minus spatial Laplacian. -/
theorem heatOperatorFormal_apply
    {ι : Type u} [Fintype ι] (u : ScalarField ι) (z : HeatSpace ι) :
    heatOperatorFormal u z =
      deriv (fun t : ℝ => u (t, z.2)) z.1 -
        Laplacian.laplacian (fun x : EuclideanSpace ℝ ι => u (z.1, x)) z.2 :=
  rfl

/--
Smoothness package strong enough to state a classical heat-equation residual.

This is intentionally stronger than some Schauder hypotheses: it is a local
bridge interface saying that the total space-time field has two classical
derivatives on the chosen domain and the source is continuous there.  The
actual distribution-to-classical implication is recorded separately because
mathlib does not currently expose a ready-made heat-equation weak/classical
bridge theorem.
-/
def HeatClassicalSmoothOn
    {ι : Type u} [Fintype ι]
    (u source : ScalarField ι) (Q : Set (HeatSpace ι)) : Prop :=
  ContDiffOn ℝ 2 u Q ∧ ContinuousOn source Q

/--
Bridge contract from a distributional heat residual to the pointwise classical
residual.

`residualDistribution` names the distributional object over the open heat
domain.  `distributionalResidualEqualsSource` is the selected weak/distributional
equation statement for that object.  The final field is the future theorem
needed by the Schauder pipeline: under sufficient smoothness, the
distributional equation gives the classical residual
`heatOperatorFormal u = source` on the domain.
-/
structure DistributionalHeatResidualBridge
    (ι : Type u) [Fintype ι] : Type u where
  U : Opens (HeatSpace ι)
  u : ScalarField ι
  source : ScalarField ι
  residualDistribution : ScalarDistributionOnHeatDomain U
  distributionalResidualEqualsSource : Prop
  sufficientSmoothness : HeatClassicalSmoothOn u source (U : Set (HeatSpace ι))
  distributional_to_classical :
    HeatClassicalSmoothOn u source (U : Set (HeatSpace ι)) →
      distributionalResidualEqualsSource →
        ∀ z ∈ (U : Set (HeatSpace ι)), heatOperatorFormal u z = source z

/-- The carrier set of the open domain in a distributional residual bridge. -/
def DistributionalHeatResidualBridge.domainSet
    {ι : Type u} [Fintype ι] (B : DistributionalHeatResidualBridge ι) :
    Set (HeatSpace ι) :=
  B.U

/--
Checked projection theorem for the weak/distributional-to-classical residual
bridge contract.
-/
theorem DistributionalHeatResidualBridge.classicalResidual
    {ι : Type u} [Fintype ι] (B : DistributionalHeatResidualBridge ι)
    (hResidual : B.distributionalResidualEqualsSource) :
    ∀ z ∈ B.domainSet, heatOperatorFormal B.u z = B.source z :=
  B.distributional_to_classical B.sufficientSmoothness hResidual

/-- The smoothness component stored by a distributional residual bridge. -/
theorem DistributionalHeatResidualBridge.smoothOn
    {ι : Type u} [Fintype ι] (B : DistributionalHeatResidualBridge ι) :
    HeatClassicalSmoothOn B.u B.source B.domainSet :=
  B.sufficientSmoothness

/--
Input contract for the interior constant-coefficient heat-equation Schauder
estimate on nested parabolic cylinders.

The operator is the repo-local `heatOperatorFormal`, so the coefficient matrix
is the constant identity matrix in the spatial Laplacian term.  The fields make
the local cylinder geometry and quantitative constants explicit without
asserting that the Schauder estimate has been proved.
-/
structure InteriorConstantCoefficientHeatSchauderInput
    (ι : Type u) [Fintype ι] : Type u where
  outer : ParabolicCylinder ι
  inner : ParabolicCylinder ι
  u : ScalarField ι
  source : ScalarField ι
  holderExponent : ℝ≥0
  pointwiseExponent : I
  solutionSupConstant : ℝ≥0
  sourceSupConstant : ℝ≥0
  sourceHolderConstant : ℝ≥0
  estimateConstant : ℝ≥0
  outputSupConstant : ℝ≥0
  outputHolderConstant : ℝ≥0
  sameCenter : inner.center = outer.center
  innerRadius_lt_outerRadius : inner.radius < outer.radius
  innerSubsetOuter : inner.twoSidedSet ⊆ outer.twoSidedSet
  sourceParabolicHolderOnOuter :
    parabolicHolderNormBound sourceSupConstant sourceHolderConstant
      holderExponent source outer.twoSidedSet
  solutionSupOnOuter :
    parabolicSupNormBound solutionSupConstant u outer.twoSidedSet
  classicalHeatEquationOnOuter :
    ∀ z ∈ outer.twoSidedSet, heatOperatorFormal u z = source z

/--
Output contract for a future interior constant-coefficient Schauder estimate.

`quantitativeEstimate` is deliberately a relation among explicit constants:
future work can replace the bounded-norm predicates by a bundled
`C^{2+α,1+α/2}` parabolic Holder norm while preserving this bookkeeping shape.
-/
structure InteriorConstantCoefficientHeatSchauderPackage
    {ι : Type u} [Fintype ι]
    (X : InteriorConstantCoefficientHeatSchauderInput ι) : Type u where
  solutionC2OnInner : ContDiffOn ℝ 2 X.u X.inner.twoSidedSet
  pointwiseSecondOrderHolderOnInner :
    ∀ z ∈ X.inner.twoSidedSet,
      ContDiffPointwiseHolderAt 2 X.pointwiseExponent X.u z
  parabolicHolderOnInner :
    parabolicHolderNormBound X.outputSupConstant X.outputHolderConstant
      X.holderExponent X.u X.inner.twoSidedSet
  quantitativeEstimate :
    X.outputSupConstant + X.outputHolderConstant ≤
      X.estimateConstant *
        (X.solutionSupConstant + X.sourceSupConstant + X.sourceHolderConstant)

/--
Statement shape for the interior constant-coefficient heat-equation Schauder
estimate child task.

This is a target shape, not a completion claim.  It says that every input with
the explicit nested-cylinder and quantitative-constant hypotheses should
produce an interior Schauder package.
-/
def InteriorConstantCoefficientHeatSchauderStatement : Prop :=
  ∀ (ι : Type u) [Fintype ι]
    (X : InteriorConstantCoefficientHeatSchauderInput ι),
      Nonempty (InteriorConstantCoefficientHeatSchauderPackage X)

/-- Low-risk introduction wrapper for the interior Schauder statement shape. -/
theorem interiorConstantCoefficientHeatSchauderStatement_intro
    (h : ∀ (ι : Type u) [Fintype ι]
      (X : InteriorConstantCoefficientHeatSchauderInput ι),
        Nonempty (InteriorConstantCoefficientHeatSchauderPackage X)) :
    InteriorConstantCoefficientHeatSchauderStatement.{u} :=
  h

/-- The interior Schauder input exposes the heat equation on the outer cylinder. -/
theorem InteriorConstantCoefficientHeatSchauderInput.heatEquationOnOuter
    {ι : Type u} [Fintype ι]
    (X : InteriorConstantCoefficientHeatSchauderInput ι) :
    ∀ z ∈ X.outer.twoSidedSet, heatOperatorFormal X.u z = X.source z :=
  X.classicalHeatEquationOnOuter

/-- The interior Schauder input exposes source Holder control on the outer cylinder. -/
theorem InteriorConstantCoefficientHeatSchauderInput.sourceHolderOnOuter
    {ι : Type u} [Fintype ι]
    (X : InteriorConstantCoefficientHeatSchauderInput ι) :
    parabolicHolderNormBound X.sourceSupConstant X.sourceHolderConstant
      X.holderExponent X.source X.outer.twoSidedSet :=
  X.sourceParabolicHolderOnOuter

/-- A future interior package exposes the explicit quantitative constant bound. -/
theorem InteriorConstantCoefficientHeatSchauderPackage.quantitativeBound
    {ι : Type u} [Fintype ι]
    {X : InteriorConstantCoefficientHeatSchauderInput ι}
    (P : InteriorConstantCoefficientHeatSchauderPackage X) :
    X.outputSupConstant + X.outputHolderConstant ≤
      X.estimateConstant *
        (X.solutionSupConstant + X.sourceSupConstant + X.sourceHolderConstant) :=
  P.quantitativeEstimate

/--
Boundary regularity hypotheses for a future boundary Schauder estimate.

The concrete flattening-chart and parabolic `C^{2+α,1+α/2}` boundary APIs are
not available in the audited mathlib snapshot, so the analytic regularity
requirements are named as explicit propositions and carried with proof fields.
Set-theoretic boundary bookkeeping is concrete.
-/
structure BoundaryRegularityHypotheses
    (ι : Type u) [Fintype ι] : Type u where
  domain : Set (HeatSpace ι)
  parabolicBoundary : Set (HeatSpace ι)
  boundaryPatch : Set (HeatSpace ι)
  domain_open : IsOpen domain
  boundaryPatch_subset_parabolicBoundary : boundaryPatch ⊆ parabolicBoundary
  parabolicBoundary_subset_closure_domain : parabolicBoundary ⊆ closure domain
  boundaryFlatteningCharts : Prop
  boundaryFlatteningCharts_holds : boundaryFlatteningCharts
  boundaryParabolicC2Alpha : Prop
  boundaryParabolicC2Alpha_holds : boundaryParabolicC2Alpha

/-- Local domain cut out by a boundary regularity package and a cylinder. -/
def BoundaryRegularityHypotheses.localDomain
    {ι : Type u} [Fintype ι] (R : BoundaryRegularityHypotheses ι)
    (Q : ParabolicCylinder ι) : Set (HeatSpace ι) :=
  R.domain ∩ Q.twoSidedSet

/-- Local boundary patch cut out by a boundary regularity package and a cylinder. -/
def BoundaryRegularityHypotheses.localBoundaryPatch
    {ι : Type u} [Fintype ι] (R : BoundaryRegularityHypotheses ι)
    (Q : ParabolicCylinder ι) : Set (HeatSpace ι) :=
  R.boundaryPatch ∩ Q.twoSidedSet

/--
Compatibility hypotheses for the boundary branch of the heat-equation Schauder
estimate.

`boundaryData` represents the boundary trace data.  The compatibility fields
separate trace matching from initial/corner/source compatibility so later work
can replace these proposition-level hypotheses by concrete trace and normal
derivative APIs.
-/
structure BoundaryCompatibilityHypotheses
    {ι : Type u} [Fintype ι]
    (R : BoundaryRegularityHypotheses ι)
    (u source boundaryData : ScalarField ι) : Type u where
  boundaryTraceMatches : ∀ z ∈ R.boundaryPatch, u z = boundaryData z
  initialBoundaryCompatibility : Prop
  initialBoundaryCompatibility_holds : initialBoundaryCompatibility
  sourceBoundaryCompatibility : Prop
  sourceBoundaryCompatibility_holds : sourceBoundaryCompatibility
  cornerCompatibility : Prop
  cornerCompatibility_holds : cornerCompatibility

/--
Input contract for a future boundary heat-equation Schauder estimate.

The statement is localized to nested cylinders and the concrete local sets
`boundaryRegularity.localDomain outer` and
`boundaryRegularity.localBoundaryPatch outer`.  It carries boundary regularity,
boundary trace data, compatibility hypotheses, source/boundary Holder control,
and quantitative constants explicitly.
-/
structure BoundaryHeatSchauderInput
    (ι : Type u) [Fintype ι] : Type u where
  outer : ParabolicCylinder ι
  inner : ParabolicCylinder ι
  boundaryRegularity : BoundaryRegularityHypotheses ι
  u : ScalarField ι
  source : ScalarField ι
  boundaryData : ScalarField ι
  holderExponent : ℝ≥0
  pointwiseExponent : I
  solutionSupConstant : ℝ≥0
  sourceSupConstant : ℝ≥0
  sourceHolderConstant : ℝ≥0
  boundarySupConstant : ℝ≥0
  boundaryHolderConstant : ℝ≥0
  estimateConstant : ℝ≥0
  outputSupConstant : ℝ≥0
  outputHolderConstant : ℝ≥0
  sameCenter : inner.center = outer.center
  innerRadius_lt_outerRadius : inner.radius < outer.radius
  innerSubsetOuter : inner.twoSidedSet ⊆ outer.twoSidedSet
  sourceParabolicHolderOnOuterDomain :
    parabolicHolderNormBound sourceSupConstant sourceHolderConstant
      holderExponent source (boundaryRegularity.localDomain outer)
  boundaryDataParabolicHolderOnOuterPatch :
    parabolicHolderNormBound boundarySupConstant boundaryHolderConstant
      holderExponent boundaryData (boundaryRegularity.localBoundaryPatch outer)
  solutionSupOnOuterDomain :
    parabolicSupNormBound solutionSupConstant u
      (boundaryRegularity.localDomain outer)
  classicalHeatEquationOnOuterDomain :
    ∀ z ∈ boundaryRegularity.localDomain outer,
      heatOperatorFormal u z = source z
  boundaryCompatibility :
    BoundaryCompatibilityHypotheses boundaryRegularity u source boundaryData

/--
Output contract for a future boundary Schauder estimate.

The quantitative estimate includes the boundary data constants in addition to
the interior source and solution constants.
-/
structure BoundaryHeatSchauderPackage
    {ι : Type u} [Fintype ι]
    (X : BoundaryHeatSchauderInput ι) : Type u where
  solutionC2OnInnerDomain :
    ContDiffOn ℝ 2 X.u (X.boundaryRegularity.localDomain X.inner)
  pointwiseSecondOrderHolderOnInnerDomain :
    ∀ z ∈ X.boundaryRegularity.localDomain X.inner,
      ContDiffPointwiseHolderAt 2 X.pointwiseExponent X.u z
  parabolicHolderOnInnerDomain :
    parabolicHolderNormBound X.outputSupConstant X.outputHolderConstant
      X.holderExponent X.u (X.boundaryRegularity.localDomain X.inner)
  boundaryTraceOnInnerPatch :
    ∀ z ∈ X.boundaryRegularity.localBoundaryPatch X.inner,
      X.u z = X.boundaryData z
  quantitativeEstimate :
    X.outputSupConstant + X.outputHolderConstant ≤
      X.estimateConstant *
        (X.solutionSupConstant + X.sourceSupConstant + X.sourceHolderConstant +
          X.boundarySupConstant + X.boundaryHolderConstant)

/--
Statement shape for the boundary branch of the heat-equation Schauder estimate.

This is a target shape, not a completion claim.  It says that every boundary
input with explicit boundary regularity, compatibility, local-cylinder, and
quantitative hypotheses should produce the boundary Schauder package.
-/
def BoundaryHeatSchauderStatement : Prop :=
  ∀ (ι : Type u) [Fintype ι]
    (X : BoundaryHeatSchauderInput ι),
      Nonempty (BoundaryHeatSchauderPackage X)

/-- Low-risk introduction wrapper for the boundary Schauder statement shape. -/
theorem boundaryHeatSchauderStatement_intro
    (h : ∀ (ι : Type u) [Fintype ι]
      (X : BoundaryHeatSchauderInput ι),
        Nonempty (BoundaryHeatSchauderPackage X)) :
    BoundaryHeatSchauderStatement.{u} :=
  h

/-- A boundary regularity package exposes the boundary-patch inclusion. -/
theorem BoundaryRegularityHypotheses.boundaryPatch_subset
    {ι : Type u} [Fintype ι]
    (R : BoundaryRegularityHypotheses ι) :
    R.boundaryPatch ⊆ R.parabolicBoundary :=
  R.boundaryPatch_subset_parabolicBoundary

/-- Boundary compatibility exposes the trace equality on the selected patch. -/
theorem BoundaryCompatibilityHypotheses.trace
    {ι : Type u} [Fintype ι]
    {R : BoundaryRegularityHypotheses ι}
    {u source boundaryData : ScalarField ι}
    (H : BoundaryCompatibilityHypotheses R u source boundaryData) :
    ∀ z ∈ R.boundaryPatch, u z = boundaryData z :=
  H.boundaryTraceMatches

/-- The boundary Schauder input exposes the heat equation on the outer local domain. -/
theorem BoundaryHeatSchauderInput.heatEquationOnOuterDomain
    {ι : Type u} [Fintype ι]
    (X : BoundaryHeatSchauderInput ι) :
    ∀ z ∈ X.boundaryRegularity.localDomain X.outer,
      heatOperatorFormal X.u z = X.source z :=
  X.classicalHeatEquationOnOuterDomain

/-- The boundary Schauder input exposes source Holder control on the outer local domain. -/
theorem BoundaryHeatSchauderInput.sourceHolderOnOuterDomain
    {ι : Type u} [Fintype ι]
    (X : BoundaryHeatSchauderInput ι) :
    parabolicHolderNormBound X.sourceSupConstant X.sourceHolderConstant
      X.holderExponent X.source (X.boundaryRegularity.localDomain X.outer) :=
  X.sourceParabolicHolderOnOuterDomain

/-- The boundary Schauder input exposes boundary-data Holder control on the patch. -/
theorem BoundaryHeatSchauderInput.boundaryDataHolderOnOuterPatch
    {ι : Type u} [Fintype ι]
    (X : BoundaryHeatSchauderInput ι) :
    parabolicHolderNormBound X.boundarySupConstant X.boundaryHolderConstant
      X.holderExponent X.boundaryData
        (X.boundaryRegularity.localBoundaryPatch X.outer) :=
  X.boundaryDataParabolicHolderOnOuterPatch

/-- The compatibility package gives the boundary trace equality on any local patch. -/
theorem BoundaryHeatSchauderInput.boundaryTraceOnOuterPatch
    {ι : Type u} [Fintype ι]
    (X : BoundaryHeatSchauderInput ι) :
    ∀ z ∈ X.boundaryRegularity.localBoundaryPatch X.outer,
      X.u z = X.boundaryData z := by
  intro z hz
  exact X.boundaryCompatibility.boundaryTraceMatches z hz.1

/-- A future boundary package exposes the explicit quantitative constant bound. -/
theorem BoundaryHeatSchauderPackage.quantitativeBound
    {ι : Type u} [Fintype ι]
    {X : BoundaryHeatSchauderInput ι}
    (P : BoundaryHeatSchauderPackage X) :
    X.outputSupConstant + X.outputHolderConstant ≤
      X.estimateConstant *
        (X.solutionSupConstant + X.sourceSupConstant + X.sourceHolderConstant +
          X.boundarySupConstant + X.boundaryHolderConstant) :=
  P.quantitativeEstimate

/--
Input data for a future formal parabolic Schauder estimate.

`classicalHeatEquation` is concrete at the formal-operator level.  The source
and solution bounds use the repo-local anisotropic parabolic Holder bound API;
the remaining proposition fields are the higher-level geometry and boundary
contracts still missing from mathlib.
-/
structure HeatSchauderInput (ι : Type u) [Fintype ι] : Type u where
  Q : Set (HeatSpace ι)
  u : ScalarField ι
  source : ScalarField ι
  holderExponent : ℝ≥0
  pointwiseExponent : I
  solutionSupConstant : ℝ≥0
  sourceSupConstant : ℝ≥0
  sourceHolderConstant : ℝ≥0
  isOpenCylinder : IsOpen Q
  nonemptyCylinder : Q.Nonempty
  sourceParabolicHolder :
    parabolicHolderNormBound sourceSupConstant sourceHolderConstant
      holderExponent source Q
  solutionSup :
    parabolicSupNormBound solutionSupConstant u Q
  classicalHeatEquation : ∀ z ∈ Q, heatOperatorFormal u z = source z
  parabolicCylinderGeometry : Prop
  boundaryCompatibility : Prop
  anisotropicHolderScale : Prop

/--
Output package expected from a parabolic Schauder estimate.

The differentiability and pointwise Holder conclusions use current mathlib
objects.  The quantitative parabolic norm estimate is now a concrete
repo-local anisotropic Holder norm-bound inequality rather than an abstract
proposition placeholder.
-/
structure HeatSchauderEstimatePackage
    {ι : Type u} [Fintype ι] (X : HeatSchauderInput ι) : Type u where
  solutionC2SpaceTime : ContDiffOn ℝ 2 X.u X.Q
  pointwiseSecondOrderHolder :
    ∀ z ∈ X.Q, ContDiffPointwiseHolderAt 2 X.pointwiseExponent X.u z
  estimateConstant : ℝ≥0
  outputSupConstant : ℝ≥0
  outputHolderConstant : ℝ≥0
  parabolicHolderEstimate :
    parabolicHolderNormBound outputSupConstant outputHolderConstant
      X.holderExponent X.u X.Q
  quantitativeEstimate :
    outputSupConstant + outputHolderConstant ≤
      estimateConstant *
        (X.solutionSupConstant + X.sourceSupConstant + X.sourceHolderConstant)

/--
Normalized Stage1 statement shape for THM-M-1189.

For a finite-dimensional spatial domain and an audited heat-equation input,
Holder regularity of the source term plus the missing parabolic geometry,
boundary, and anisotropic Holder-scale hypotheses should produce a
`C^{2,alpha}`-style package and a quantitative estimate on the cylinder.
-/
def StatementShape : Prop :=
  ∀ (ι : Type u) [Fintype ι] (X : HeatSchauderInput ι),
    X.parabolicCylinderGeometry →
      X.boundaryCompatibility →
        X.anisotropicHolderScale →
          Nonempty (HeatSchauderEstimatePackage X)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem statementShape_intro
    (h : ∀ (ι : Type u) [Fintype ι] (X : HeatSchauderInput ι),
      X.parabolicCylinderGeometry →
        X.boundaryCompatibility →
          X.anisotropicHolderScale →
            Nonempty (HeatSchauderEstimatePackage X)) :
    StatementShape.{u} :=
  h

/-- Checked wrapper exposing the stored parabolic Holder condition on the source term. -/
theorem source_parabolicHolderNormBound
    {ι : Type u} [Fintype ι] (X : HeatSchauderInput ι) :
    parabolicHolderNormBound X.sourceSupConstant X.sourceHolderConstant
      X.holderExponent X.source X.Q :=
  X.sourceParabolicHolder

/-- Checked wrapper exposing the stored supremum bound on the solution. -/
theorem solution_parabolicSupNormBound
    {ι : Type u} [Fintype ι] (X : HeatSchauderInput ι) :
    parabolicSupNormBound X.solutionSupConstant X.u X.Q :=
  X.solutionSup

/-- Checked wrapper exposing the formal classical heat-equation residual. -/
theorem heatEquation_holds
    {ι : Type u} [Fintype ι] (X : HeatSchauderInput ι) :
    ∀ z ∈ X.Q, heatOperatorFormal X.u z = X.source z :=
  X.classicalHeatEquation

/-- A root Schauder package exposes its concrete parabolic Holder estimate. -/
theorem HeatSchauderEstimatePackage.parabolicHolderBound
    {ι : Type u} [Fintype ι]
    {X : HeatSchauderInput ι}
    (P : HeatSchauderEstimatePackage X) :
    parabolicHolderNormBound P.outputSupConstant P.outputHolderConstant
      X.holderExponent X.u X.Q :=
  P.parabolicHolderEstimate

/-- A root Schauder package exposes its concrete quantitative estimate. -/
theorem HeatSchauderEstimatePackage.quantitativeBound
    {ι : Type u} [Fintype ι]
    {X : HeatSchauderInput ι}
    (P : HeatSchauderEstimatePackage X) :
    P.outputSupConstant + P.outputHolderConstant ≤
      P.estimateConstant *
        (X.solutionSupConstant + X.sourceSupConstant + X.sourceHolderConstant) :=
  P.quantitativeEstimate

/-- Checked mathlib anchor: Holder exponent `1` is exactly Lipschitz continuity on a set. -/
theorem holderOnWith_one_iff_lipschitzOnWith
    {X Y : Type v} [PseudoEMetricSpace X] [PseudoEMetricSpace Y]
    {C : ℝ≥0} {f : X → Y} {s : Set X} :
    HolderOnWith C 1 f s ↔ LipschitzOnWith C f s :=
  holderOnWith_one

/-- Checked mathlib anchor: higher differentiability gives pointwise Holder regularity. -/
theorem contDiffAt_to_pointwiseHolderAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {F : Type v} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {k : ℕ} {α : I} {f : E → F} {a : E} {n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f a) (hk : k < n) :
    ContDiffPointwiseHolderAt k α f a :=
  hf.contDiffPointwiseHolderAt hk α

/-- mathlib modules checked while locating repo-local anchors for this PDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Calculus.ContDiffHolder.Pointwise",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Topology.MetricSpace.Holder",
  "Mathlib.Topology.MetricSpace.HolderNorm",
  "Mathlib.MeasureTheory.Function.Holder",
  "Mathlib.MeasureTheory.Measure.Lebesgue.Basic"
]

/-- Nearby mathlib names audited for the heat-equation Schauder statement boundary. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "fderiv",
  "iteratedFDeriv",
  "Laplacian.laplacian",
  "twoSidedParabolicCylinder",
  "backwardParabolicCylinder",
  "forwardParabolicCylinder",
  "ParabolicCylinder",
  "ScalarDistributionOnHeatDomain",
  "parabolicDistance",
  "parabolicEdist",
  "parabolicHolderSeminormBound",
  "parabolicHolderNormBound",
  "HeatClassicalSmoothOn",
  "DistributionalHeatResidualBridge",
  "DistributionalHeatResidualBridge.classicalResidual",
  "InteriorConstantCoefficientHeatSchauderInput",
  "InteriorConstantCoefficientHeatSchauderPackage",
  "InteriorConstantCoefficientHeatSchauderStatement",
  "interiorConstantCoefficientHeatSchauderStatement_intro",
  "BoundaryRegularityHypotheses",
  "BoundaryRegularityHypotheses.localDomain",
  "BoundaryRegularityHypotheses.localBoundaryPatch",
  "BoundaryCompatibilityHypotheses",
  "BoundaryHeatSchauderInput",
  "BoundaryHeatSchauderPackage",
  "BoundaryHeatSchauderStatement",
  "boundaryHeatSchauderStatement_intro",
  "BoundaryHeatSchauderInput.heatEquationOnOuterDomain",
  "BoundaryHeatSchauderInput.sourceHolderOnOuterDomain",
  "BoundaryHeatSchauderInput.boundaryDataHolderOnOuterPatch",
  "BoundaryHeatSchauderInput.boundaryTraceOnOuterPatch",
  "BoundaryHeatSchauderPackage.quantitativeBound",
  "HeatSchauderInput",
  "HeatSchauderEstimatePackage",
  "HeatSchauderEstimatePackage.parabolicHolderBound",
  "HeatSchauderEstimatePackage.quantitativeBound",
  "source_parabolicHolderNormBound",
  "solution_parabolicSupNormBound",
  "StatementShape",
  "statementShape_intro",
  "ContDiffOn",
  "ContDiffAt",
  "ContDiffPointwiseHolderAt",
  "ContDiffAt.contDiffPointwiseHolderAt",
  "HolderOnWith",
  "holderOnWith_one",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.MemLp",
  "Distribution"
]

/--
Search terms that did not locate a terminal parabolic Schauder estimate theorem
in local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Schauder",
  "heat equation Schauder",
  "parabolic Schauder",
  "parabolic Holder",
  "anisotropic Holder",
  "caloric",
  "heat operator",
  "PDE regularity",
  "classical heat equation",
  "weak heat equation",
  "distributional heat residual",
  "weak-to-classical heat residual bridge"
]

/--
Public Lean source search terms for terminal parabolic Schauder theorem names.

This child audit searched these strings in public Lean source indexes on
2026-05-01.  It found no terminal heat-equation parabolic Schauder estimate
theorem name that could be pinned into this Lake project.
-/
def externalLeanSourceSearchTerms : List String := [
  "parabolic Schauder",
  "Schauder estimate",
  "SchauderEstimate",
  "HeatSchauder",
  "parabolic Holder",
  "heat equation",
  "caloric"
]

/--
Repo-local summary of the external-source search result.

The result is intentionally a string-valued audit note, not a proof of the
analytic theorem.  If a public Lean 4 terminal proof appears later, this gate
must change to a pinned/imported/checked dependency or a concrete integration
blocker before any completion claim.
-/
def externalLeanSourceSearchResult : String :=
  "no_public_terminal_parabolic_schauder_lean4_theorem_found_on_2026-05-01"

/-- Machine-proof debt classification for the current Stage1 repair pass. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration-debt gate for this module.

No external Lean 4 terminal proof of the heat-equation Schauder estimate has
been pinned into the local Lake dependency closure, and this module is not
marked complete.  If such a proof is found later, the integrator must
pin/import/check it or record a concrete integration blocker before any
completion claim.
-/
def repoLocalIntegrationDebtGate : String :=
  "no_external_terminal_lean4_proof_pinned; no_completion_claim"

/-! ## Audit probes -/

#check deriv
#check fderiv
#check iteratedFDeriv
#check Laplacian.laplacian
#check HolderOnWith
#check holderOnWith_one
#check ContDiffOn
#check ContDiffPointwiseHolderAt
#check ContDiffAt.contDiffPointwiseHolderAt

end S1_M_152
end Stage1
end AwesomeTheorems
