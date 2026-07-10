import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.Analysis.Subadditive
import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic
import Mathlib.LinearAlgebra.Basis.Flag
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Probability.Independence.Basic
import Mathlib.RingTheory.Grassmannian
import Mathlib.Topology.Instances.Matrix

/-!
# S1-M-248 / THM-M-1056: Oseledets multiplicative ergodic theorem

This Stage1 artifact records a conservative Lean 4 boundary for Oseledets'
multiplicative ergodic theorem for random finite-dimensional real matrices.

The genuine theorem states that, under the usual measurability and logarithmic
integrability hypotheses for a matrix cocycle over a probability-preserving
transformation, almost every base point admits Lyapunov exponents and an
invariant Oseledets filtration/splitting, with vector growth rates converging to
the appropriate exponent.

The pinned mathlib substrate used by this repository has measure-preserving and
ergodic maps, probability measures, a.e. measurability, integrability,
independence, and finite matrix APIs.  It does not expose a terminal Oseledets
theorem, a bundled random linear cocycle API, measurable
Grassmannian/subspace-valued maps, or Kingman subadditive ergodic theorem in the
local dependency closure.

Accordingly this file provides only a checked statement shape and low-risk
wrappers around the currently available mathlib objects.  No terminal proof of
Oseledets' theorem is claimed here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal Topology Matrix.Norms.Operator

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_248

universe u v

/-- Finite-dimensional real vectors indexed by `ι`. -/
abbrev FiniteVector (ι : Type v) :=
  ι → ℝ

/-- Finite-dimensional real square matrices indexed by `ι`. -/
abbrev FiniteMatrix (ι : Type v) :=
  Matrix ι ι ℝ

/--
The finite-vector norm used in the Stage1 growth-rate boundary.

For `ι → ℝ`, mathlib's standard finite `Pi` norm is the `L∞` norm.
-/
def finiteVectorNorm {ι : Type v} [Fintype ι] (x : FiniteVector ι) : ℝ :=
  ‖x‖

/--
The finite-matrix operator norm used in the logarithmic integrability boundary.

The scoped `Matrix.Norms.Operator` instance makes this mathlib's `L∞` operator
norm, equivalently the operator norm of `A.mulVec` as a continuous linear map
between finite `L∞` vector spaces.
-/
def finiteMatrixOperatorNorm {ι : Type v} [Fintype ι] (A : FiniteMatrix ι) : ℝ :=
  ‖A‖

/-- The `log⁺`-style expression `log (max 1 size)` for a finite matrix. -/
def logPlusMatrixNorm {ι : Type v} [Fintype ι] (A : FiniteMatrix ι) : ℝ :=
  Real.log (max 1 (finiteMatrixOperatorNorm A))

/-- The vector-growth expression used in the Oseledets statement boundary. -/
def logPlusVectorNorm {ι : Type v} [Fintype ι] (x : FiniteVector ι) : ℝ :=
  Real.log (max 1 (finiteVectorNorm x))

/--
The chosen matrix norm agrees with the continuous-linear-map operator norm of
the multiplication map `A.mulVec`.
-/
theorem finiteMatrixOperatorNorm_eq_continuousLinearMap_opNorm
    {ι : Type v} [Fintype ι] (A : FiniteMatrix ι) :
    finiteMatrixOperatorNorm A = ‖ContinuousLinearMap.mk (Matrix.mulVecLin A)‖ := by
  simpa [finiteMatrixOperatorNorm] using Matrix.linfty_opNorm_eq_opNorm A

/-- The selected operator norm controls multiplication of vectors. -/
theorem finiteMatrixOperatorNorm_mulVec_le
    {ι : Type v} [Fintype ι] (A : FiniteMatrix ι) (v : FiniteVector ι) :
    finiteVectorNorm (A.mulVec v) ≤ finiteMatrixOperatorNorm A * finiteVectorNorm v := by
  simpa [finiteVectorNorm, finiteMatrixOperatorNorm] using Matrix.linfty_opNorm_mulVec A v

/--
Forward product of a matrix cocycle:
`A(T^[n-1] ω) * ... * A(T ω) * A(ω)`.
-/
def matrixCocycleProduct
    {Ω : Type u} {ι : Type v} [Fintype ι] [DecidableEq ι]
    (A : Ω → FiniteMatrix ι) (T : Ω → Ω) : ℕ → Ω → FiniteMatrix ι
  | 0, _ => 1
  | n + 1, ω => A ((T^[n]) ω) * matrixCocycleProduct A T n ω

/--
Bundled random finite-dimensional matrix cocycle data for the Stage1
Oseledets boundary.

The field `productAEMeasurable` is deliberately a bundled hypothesis rather
than a derived theorem: the local dependency closure has enough measurability
transport for base iterates, but not a canonical random-linear-cocycle API from
which all product measurability facts are already exposed.
-/
structure RandomMatrixCocycle
    (Ω : Type u) (ι : Type v) [MeasurableSpace Ω] [Fintype ι]
    [DecidableEq ι] : Type (max u v) where
  measure : Measure Ω
  base : Ω → Ω
  matrix : Ω → FiniteMatrix ι
  baseMeasurePreserving : MeasurePreserving base measure measure
  matrixAEMeasurable : AEStronglyMeasurable matrix measure
  productAEMeasurable :
    ∀ n : ℕ, AEStronglyMeasurable (fun ω => matrixCocycleProduct matrix base n ω) measure

namespace RandomMatrixCocycle

/-- Product attached to a bundled random matrix cocycle. -/
def product
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (n : ℕ) (ω : Ω) : FiniteMatrix ι :=
  matrixCocycleProduct C.matrix C.base n ω

/-- The bundled product is definitionally the unbundled forward product. -/
theorem product_def
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (n : ℕ) (ω : Ω) :
    C.product n ω = matrixCocycleProduct C.matrix C.base n ω :=
  rfl

/-- The empty bundled cocycle product is the identity matrix. -/
theorem product_zero
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (ω : Ω) :
    C.product 0 ω = 1 :=
  rfl

/-- The bundled successor convention matches the forward product convention. -/
theorem product_succ
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (n : ℕ) (ω : Ω) :
    C.product (n + 1) ω = C.matrix ((C.base^[n]) ω) * C.product n ω :=
  rfl

/-- Every bundled finite product is a.e. strongly measurable. -/
theorem product_aestronglyMeasurable
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (n : ℕ) :
    AEStronglyMeasurable (fun ω => C.product n ω) C.measure := by
  simpa [product] using C.productAEMeasurable n

/-- Every iterate of the bundled base map is measure-preserving. -/
theorem baseMeasurePreserving_iterate
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (n : ℕ) :
    MeasurePreserving (C.base^[n]) C.measure C.measure :=
  C.baseMeasurePreserving.iterate n

/-- Every iterate of the bundled base map is quasi-measure-preserving. -/
theorem baseQuasiMeasurePreserving_iterate
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (n : ℕ) :
    Measure.QuasiMeasurePreserving (C.base^[n]) C.measure C.measure :=
  (C.baseMeasurePreserving.iterate n).quasiMeasurePreserving

/-- A one-step matrix observed along a base iterate is a.e. strongly measurable. -/
theorem matrix_comp_base_iterate_aestronglyMeasurable
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (n : ℕ) :
    AEStronglyMeasurable (fun ω => C.matrix ((C.base^[n]) ω)) C.measure :=
  C.matrixAEMeasurable.comp_quasiMeasurePreserving
    (baseQuasiMeasurePreserving_iterate C n)

end RandomMatrixCocycle

/--
The algebraic-geometry Grassmannian type currently exposed by mathlib for the
finite vector space used by this Stage1 Oseledets boundary.

This is quotient-rank Grassmannian data extending `Submodule`, not yet a
canonical measurable Grassmannian model for Oseledets filtrations.
-/
abbrev FiniteOseledetsGrassmannian (ι : Type v) [Fintype ι] (k : ℕ) :=
  Module.Grassmannian ℝ (FiniteVector ι) k

/--
A subspace-valued random family with an explicit target measurable structure.

The explicit `targetMeasurableSpace` field is intentional: the pinned mathlib
dependency closure exposes `Submodule` and algebraic `Module.Grassmannian`
objects, but not a canonical Borel/measurable-space instance on the finite
Grassmannian or all submodules suitable for Oseledets filtrations.
-/
structure MeasurableSubspaceFamily
    (Ω : Type u) (ι : Type v) [MeasurableSpace Ω] [Fintype ι]
    (μ : Measure Ω) : Type (max u v) where
  subspace : Ω → ι → Submodule ℝ (FiniteVector ι)
  targetMeasurableSpace : MeasurableSpace (Submodule ℝ (FiniteVector ι))
  subspaceAEMeasurable :
    letI := targetMeasurableSpace
    ∀ i : ι, AEMeasurable (fun ω => subspace ω i) μ

namespace MeasurableSubspaceFamily

/-- Projection wrapper for a checked subspace-valued measurability package. -/
theorem aemeasurable
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    {μ : Measure Ω} (F : MeasurableSubspaceFamily Ω ι μ) (i : ι) :
    letI := F.targetMeasurableSpace
    AEMeasurable (fun ω => F.subspace ω i) μ :=
  F.subspaceAEMeasurable i

end MeasurableSubspaceFamily

/--
A flag-valued random family with an explicit target measurable structure.

This uses mathlib's order-theoretic `Flag (Submodule ℝ V)` as a checked
placeholder for filtrations.  It does not assert that mathlib supplies the
canonical measurable Oseledets flag manifold.
-/
structure MeasurableFlagFamily
    (Ω : Type u) (ι : Type v) [MeasurableSpace Ω] [Fintype ι]
    (μ : Measure Ω) : Type (max u v) where
  flag : Ω → Flag (Submodule ℝ (FiniteVector ι))
  targetMeasurableSpace : MeasurableSpace (Flag (Submodule ℝ (FiniteVector ι)))
  flagAEMeasurable :
    letI := targetMeasurableSpace
    AEMeasurable flag μ

namespace MeasurableFlagFamily

/-- Projection wrapper for a checked flag-valued measurability package. -/
theorem aemeasurable
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    {μ : Measure Ω} (F : MeasurableFlagFamily Ω ι μ) :
    letI := F.targetMeasurableSpace
    AEMeasurable F.flag μ :=
  F.flagAEMeasurable

end MeasurableFlagFamily

/--
A fixed-rank Grassmannian-valued random family with an explicit target
measurable structure.

This records the usable mathlib type boundary for fixed quotient rank `k`;
choosing and proving the Oseledets-relevant Borel structure remains future
formalization work.
-/
structure MeasurableGrassmannianFamily
    (Ω : Type u) (ι : Type v) [MeasurableSpace Ω] [Fintype ι]
    (μ : Measure Ω) (k : ℕ) : Type (max u v) where
  grassmannian : Ω → FiniteOseledetsGrassmannian ι k
  targetMeasurableSpace : MeasurableSpace (FiniteOseledetsGrassmannian ι k)
  grassmannianAEMeasurable :
    letI := targetMeasurableSpace
    AEMeasurable grassmannian μ

namespace MeasurableGrassmannianFamily

/-- Projection wrapper for a checked fixed-Grassmannian measurability package. -/
theorem aemeasurable
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι]
    {μ : Measure Ω} {k : ℕ} (F : MeasurableGrassmannianFamily Ω ι μ k) :
    letI := F.targetMeasurableSpace
    AEMeasurable F.grassmannian μ :=
  F.grassmannianAEMeasurable

end MeasurableGrassmannianFamily

/-- Normalized input data for the Stage1 Oseledets statement boundary. -/
structure OseledetsData
    (Ω : Type u) (ι : Type v) [MeasurableSpace Ω] [Fintype ι]
    [DecidableEq ι] : Type (max u v) where
  measure : Measure Ω
  base : Ω → Ω
  matrix : Ω → FiniteMatrix ι
  isProbability : IsProbabilityMeasure measure
  baseMeasurePreserving : MeasurePreserving base measure measure
  matrixAEMeasurable : AEStronglyMeasurable matrix measure
  logPlusIntegrable : Integrable (fun ω => logPlusMatrixNorm (matrix ω)) measure
  inverseIntegrabilityBoundary : Prop
  baseErgodic : Ergodic base measure
  cocycleModelBoundary : Prop
  lyapunovExponent : ι → ℝ
  oseledetsSubspace : Ω → ι → Submodule ℝ (FiniteVector ι)
  measurableSubspaceBoundary : Prop
  equivariantSubspaceBoundary : Prop
  exponentMultiplicityBoundary : Prop

/-- The normalized Stage1 hypotheses for the random matrix cocycle. -/
def OseledetsHypotheses
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) : Prop :=
  D.inverseIntegrabilityBoundary ∧
    D.cocycleModelBoundary

/--
Almost-everywhere growth-rate conclusion for vectors in each Oseledets
subspace.  This is a statement-shape target, not a local proof.
-/
def GrowthRateConclusion
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) : Prop :=
  ∀ i : ι,
    ∀ᵐ ω ∂D.measure,
      ∀ v : FiniteVector ι,
        v ∈ D.oseledetsSubspace ω i →
          v ≠ 0 →
            Filter.Tendsto
              (fun n : ℕ =>
                (n : ℝ)⁻¹ *
                  logPlusVectorNorm (matrixCocycleProduct D.matrix D.base n ω |>.mulVec v))
              Filter.atTop
              (𝓝 (D.lyapunovExponent i))

/--
Expected terminal conclusion package for a completed Oseledets formalization.

The subspace-valued measurability, equivariance, and exponent-multiplicity
fields are placeholders for future pinned APIs.  The growth-rate field is the
main analytic convergence boundary.
-/
structure OseledetsConclusion
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) : Prop where
  measurable_subspaces : D.measurableSubspaceBoundary
  equivariant_subspaces : D.equivariantSubspaceBoundary
  exponent_multiplicities : D.exponentMultiplicityBoundary
  growth_rates : GrowthRateConclusion D

/--
Stage1 normalized statement shape for Oseledets' multiplicative ergodic
theorem.

For a finite-dimensional real matrix cocycle over a probability-preserving
base, logarithmic integrability plus the missing ergodic/cocycle infrastructure
should imply an a.e. Oseledets filtration/splitting and Lyapunov growth rates.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ (ι : Type v) [Fintype ι] [DecidableEq ι],
      ∀ D : OseledetsData Ω ι,
        OseledetsHypotheses D → OseledetsConclusion D

/--
Public Stage1 status note for the statement boundary.

This string is intentionally part of the checked Lean surface so downstream
public-doc integration can quote the exact boundary without treating this file
as a terminal proof of Oseledets' multiplicative ergodic theorem.
-/
def statementShapePublicStatus : String :=
  "AwesomeTheorems.Stage1.S1_M_248.StatementShape is a checked statement-shape artifact, not a terminal Oseledets multiplicative ergodic theorem proof."

/--
Public substrate note for the checked statement shape.

This is retained in Lean so public planning surfaces can cite the concrete
mathlib-facing objects without upgrading the artifact to a theorem proof.
-/
def statementShapeConcreteSubstrate : List String := [
  "Ergodic",
  "MeasurePreserving",
  "IsProbabilityMeasure",
  "AEStronglyMeasurable",
  "Integrable",
  "finite matrices",
  "Submodule",
  "Filter.Tendsto"
]

/-- Human-readable one-line version of `statementShapeConcreteSubstrate`. -/
def statementShapeConcreteSubstrateStatus : String :=
  "The checked statement shape uses concrete mathlib Ergodic, MeasurePreserving, IsProbabilityMeasure, AEStronglyMeasurable, Integrable, finite matrices, Submodule-valued subspaces, and Filter.Tendsto."

/-- Public note for the canonical norm used by this statement-shape artifact. -/
def statementShapeNormStatus : String :=
  "The checked statement shape uses the standard finite Pi vector norm and mathlib's Matrix.Norms.Operator L-infinity operator norm, with a checked equality to the continuous-linear-map operator norm of Matrix.mulVec."

/-- Public note for the checked bundled random matrix cocycle API. -/
def statementShapeCocycleApiStatus : String :=
  "The checked statement shape now includes RandomMatrixCocycle with forward product convention, bundled finite-product AEStronglyMeasurable hypotheses, base iterate measure-preserving laws, and the product-add cocycle law."

/-- Public note for the checked subspace/flag measurability boundary. -/
def statementShapeMeasurableFlagApiStatus : String :=
  "Pinned mathlib exposes Submodule, order-theoretic Flag (Submodule ℝ V), Basis.flag/toFlag, and algebraic quotient-rank Module.Grassmannian; this artifact adds explicit-measurable-space wrappers for subspace-, flag-, and fixed-Grassmannian-valued random maps, but no canonical Oseledets Borel Grassmannian API is available locally."

/-- The substrate note unfolds to the public backfill list for this child task. -/
theorem statementShapeConcreteSubstrate_eq :
    statementShapeConcreteSubstrate =
      [
        "Ergodic",
        "MeasurePreserving",
        "IsProbabilityMeasure",
        "AEStronglyMeasurable",
        "Integrable",
        "finite matrices",
        "Submodule",
        "Filter.Tendsto"
      ] :=
  rfl

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Ω : Type u) [MeasurableSpace Ω],
      ∀ (ι : Type v) [Fintype ι] [DecidableEq ι],
        ∀ D : OseledetsData Ω ι,
          OseledetsHypotheses D → OseledetsConclusion D) :
    StatementShape.{u, v} :=
  h

/-- The normalized statement unfolds to the expected data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ (ι : Type v) [Fintype ι] [DecidableEq ι],
          ∀ D : OseledetsData Ω ι,
            OseledetsHypotheses D → OseledetsConclusion D :=
  Iff.rfl

/-- The empty product of the cocycle is the identity matrix. -/
theorem matrixCocycleProduct_zero
    {Ω : Type u} {ι : Type v} [Fintype ι] [DecidableEq ι]
    (A : Ω → FiniteMatrix ι) (T : Ω → Ω) (ω : Ω) :
    matrixCocycleProduct A T 0 ω = 1 :=
  rfl

/-- The successor product adds the next matrix along the base orbit. -/
theorem matrixCocycleProduct_succ
    {Ω : Type u} {ι : Type v} [Fintype ι] [DecidableEq ι]
    (A : Ω → FiniteMatrix ι) (T : Ω → Ω) (n : ℕ) (ω : Ω) :
    matrixCocycleProduct A T (n + 1) ω =
      A ((T^[n]) ω) * matrixCocycleProduct A T n ω :=
  rfl

/--
Forward products satisfy the cocycle law
`P(m + n, ω) = P(m, T^[n] ω) * P(n, ω)`.
-/
theorem matrixCocycleProduct_add
    {Ω : Type u} {ι : Type v} [Fintype ι] [DecidableEq ι]
    (A : Ω → FiniteMatrix ι) (T : Ω → Ω) (m n : ℕ) (ω : Ω) :
    matrixCocycleProduct A T (m + n) ω =
      matrixCocycleProduct A T m ((T^[n]) ω) * matrixCocycleProduct A T n ω := by
  induction m with
  | zero =>
      simp [matrixCocycleProduct]
  | succ m ih =>
      rw [Nat.succ_add]
      rw [matrixCocycleProduct_succ]
      rw [ih]
      rw [matrixCocycleProduct_succ]
      rw [Function.iterate_add_apply]
      rw [Matrix.mul_assoc]

namespace RandomMatrixCocycle

/-- Bundled cocycle law for finite products. -/
theorem product_add
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (C : RandomMatrixCocycle Ω ι) (m n : ℕ) (ω : Ω) :
    C.product (m + n) ω = C.product m ((C.base^[n]) ω) * C.product n ω := by
  simpa [product] using matrixCocycleProduct_add C.matrix C.base m n ω

end RandomMatrixCocycle

/--
An Oseledets data package induces the bundled cocycle API once the finite
product measurability family has been supplied.
-/
def OseledetsData.toRandomMatrixCocycle
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι)
    (hProduct :
      ∀ n : ℕ,
        AEStronglyMeasurable
          (fun ω => matrixCocycleProduct D.matrix D.base n ω) D.measure) :
    RandomMatrixCocycle Ω ι where
  measure := D.measure
  base := D.base
  matrix := D.matrix
  baseMeasurePreserving := D.baseMeasurePreserving
  matrixAEMeasurable := D.matrixAEMeasurable
  productAEMeasurable := hProduct

/-- Projection wrapper: the data package carries a probability measure. -/
theorem data_isProbability
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) :
    IsProbabilityMeasure D.measure :=
  D.isProbability

/-- Projection wrapper: the base transformation is measure-preserving. -/
theorem data_baseMeasurePreserving
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) :
    MeasurePreserving D.base D.measure D.measure :=
  D.baseMeasurePreserving

/-- Projection wrapper: the base transformation is quasi-measure-preserving. -/
theorem data_baseQuasiMeasurePreserving
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) :
    Measure.QuasiMeasurePreserving D.base D.measure D.measure :=
  D.baseMeasurePreserving.quasiMeasurePreserving

/-- Projection wrapper: every base iterate is measure-preserving. -/
theorem data_baseMeasurePreserving_iterate
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) (n : ℕ) :
    MeasurePreserving (D.base^[n]) D.measure D.measure :=
  D.baseMeasurePreserving.iterate n

/-- Projection wrapper: the base transformation is ergodic. -/
theorem data_baseErgodic
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) :
    Ergodic D.base D.measure :=
  D.baseErgodic

/-- Projection wrapper: the matrix-valued random variable is a.e. strongly measurable. -/
theorem data_matrixAEMeasurable
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) :
    AEStronglyMeasurable D.matrix D.measure :=
  D.matrixAEMeasurable

/-- Projection wrapper: the log-plus matrix-size expression is integrable. -/
theorem data_logPlusIntegrable
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) :
    Integrable (fun ω => logPlusMatrixNorm (D.matrix ω)) D.measure :=
  D.logPlusIntegrable

/-- Projection wrapper: the conclusion package exposes the vector growth-rate claim. -/
theorem conclusion_growth_rates
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : OseledetsData Ω ι} (h : OseledetsConclusion D) :
    GrowthRateConclusion D :=
  h.growth_rates

/-- Projection wrapper: the conclusion package exposes subspace measurability. -/
theorem conclusion_measurable_subspaces
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : OseledetsData Ω ι} (h : OseledetsConclusion D) :
    D.measurableSubspaceBoundary :=
  h.measurable_subspaces

/-- Projection wrapper: the conclusion package exposes subspace equivariance. -/
theorem conclusion_equivariant_subspaces
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : OseledetsData Ω ι} (h : OseledetsConclusion D) :
    D.equivariantSubspaceBoundary :=
  h.equivariant_subspaces

/-- Projection wrapper: the conclusion package exposes exponent multiplicity data. -/
theorem conclusion_exponent_multiplicities
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : OseledetsData Ω ι} (h : OseledetsConclusion D) :
    D.exponentMultiplicityBoundary :=
  h.exponent_multiplicities

/-! ## Audit constants retained in the checked file. -/

/-- mathlib modules checked while locating repo-local Oseledets anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Dynamics.Ergodic.Ergodic",
  "Mathlib.Dynamics.Ergodic.MeasurePreserving",
  "Mathlib.Analysis.Matrix.Normed",
  "Mathlib.Analysis.SpecialFunctions.Log.Basic",
  "Mathlib.LinearAlgebra.Basis.Flag",
  "Mathlib.LinearAlgebra.Matrix.Determinant.Basic",
  "Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Topology.Instances.Matrix",
  "Mathlib.Analysis.Subadditive",
  "Mathlib.RingTheory.Grassmannian"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MeasurePreserving",
  "MeasureTheory.Measure.QuasiMeasurePreserving.iterate",
  "MeasureTheory.MeasurePreserving.integrable_comp",
  "Ergodic",
  "Ergodic.toMeasurePreserving",
  "Ergodic.ae_eq_const_of_ae_eq_comp_ae",
  "MeasureTheory.AEStronglyMeasurable",
  "MeasureTheory.Integrable",
  "MeasureTheory.IsProbabilityMeasure",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun",
  "Matrix.det",
  "Matrix.mulVec",
  "Matrix.GeneralLinearGroup",
  "Matrix.Norms.Operator",
  "Matrix.linfty_opNorm_eq_opNorm",
  "Matrix.linfty_opNorm_mulVec",
  "Function.iterate_add_apply",
  "Submodule",
  "Filter.Tendsto",
  "RandomMatrixCocycle",
  "RandomMatrixCocycle.product_add",
  "Subadditive",
  "Subadditive.tendsto_lim",
  "Flag",
  "Module.Basis.flag",
  "Module.Basis.toFlag",
  "Module.Grassmannian",
  "Module.Grassmannian.toSubmodule",
  "MeasurableSubspaceFamily",
  "MeasurableFlagFamily",
  "MeasurableGrassmannianFamily"
]

/--
Checked mathlib branch available for a future measurable Oseledets filtration
package.

The branch gives algebraic/order-theoretic carriers for subspaces and flags,
but not the canonical measurable Grassmannian or Oseledets flag-manifold API.
-/
def measurableFlagBranchModules : List String := [
  "Mathlib.LinearAlgebra.Basis.Flag",
  "Mathlib.RingTheory.Grassmannian",
  "Mathlib.Order.Preorder.Chain"
]

/-- Checked names in the usable but non-terminal measurable-flag branch. -/
def measurableFlagBranchAnchors : List String := [
  "Submodule",
  "Flag",
  "Module.Basis.flag",
  "Module.Basis.toFlag",
  "Module.Grassmannian",
  "Module.Grassmannian.toSubmodule",
  "MeasurableSpace",
  "AEMeasurable",
  "MeasurableSubspaceFamily",
  "MeasurableFlagFamily",
  "MeasurableGrassmannianFamily"
]

/--
Status of the checked measurable subspace/flag API audit.

Future proof work must supply or import the actual measurable/Borel model and
prove that the Oseledets filtration lands in it measurably.
-/
def measurableFlagBranchStatus : String :=
  "Pinned mathlib provides Submodule, order-theoretic Flag, Basis.flag/toFlag, and quotient-rank Module.Grassmannian. It does not provide a canonical measurable finite-dimensional Grassmannian or Oseledets flag-valued map API, so this file records explicit-measurable-space wrappers only."

/--
Checked mathlib branch available for a future Kingman/subadditive proof route.

This branch is useful but non-terminal: `Subadditive.tendsto_lim` supplies the
deterministic Fekete limit for subadditive real sequences, while the ergodic
modules supply measure-preserving iterates, integrability transport, and the
invariant-limit-to-constant step.
-/
def kingmanSubadditiveBranchModules : List String := [
  "Mathlib.Analysis.Subadditive",
  "Mathlib.Dynamics.Ergodic.MeasurePreserving",
  "Mathlib.Dynamics.Ergodic.Ergodic",
  "Mathlib.Dynamics.Ergodic.Function"
]

/-- Checked names in the usable but non-terminal Kingman/subadditive branch. -/
def kingmanSubadditiveBranchAnchors : List String := [
  "Subadditive",
  "Subadditive.lim",
  "Subadditive.tendsto_lim",
  "MeasureTheory.MeasurePreserving.iterate",
  "MeasureTheory.MeasurePreserving.integrable_comp",
  "MeasureTheory.MeasurePreserving.quasiMeasurePreserving",
  "MeasureTheory.Measure.QuasiMeasurePreserving.iterate",
  "Ergodic",
  "Ergodic.toMeasurePreserving",
  "Ergodic.ae_eq_const_of_ae_eq_comp_ae"
]

/--
Status of the checked Kingman/subadditive branch audit.

No terminal Kingman theorem or Oseledets theorem is provided by these anchors;
they are proof infrastructure for a future local proof tree.
-/
def kingmanSubadditiveBranchStatus : String :=
  "Pinned mathlib exposes deterministic Subadditive.tendsto_lim plus ergodic measure-preserving and invariant-function infrastructure, but no terminal Kingman/subadditive ergodic theorem wrapper and no Oseledets multiplicative ergodic theorem."

/--
External proof-assistant audit status for the subadditive branch.

The Archive of Formal Proofs Isabelle/HOL entry `Ergodic_Theory` has modules
`Kingman` and `Gouezel_Karlsson`, but this is not a Lean 4 dependency and is
not a repo-local Lean closure for this Stage1 slot.
-/
def externalSubadditiveProofAssistantStatus : String :=
  "External non-Lean anchor found: Isabelle/HOL AFP Ergodic_Theory lists Kingman and Gouezel_Karlsson modules; no public Lean 4 terminal Kingman or Oseledets proof was located, so there is no repo_local_integration_debt completion claim."

/--
Search terms that did not locate a terminal Oseledets theorem in local mathlib
or the repository's pinned Lean dependency closure.
-/
def absentTerminalSearchTerms : List String := [
  "Oseledets",
  "multiplicative ergodic theorem",
  "Lyapunov exponent",
  "random matrix cocycle",
  "linear cocycle",
  "measurable splitting",
  "Oseledets filtration",
  "Kingman",
  "subadditive ergodic theorem",
  "SubadditiveErgodic"
]

/--
Machine proof debt classification for this Stage1 slot.

The module currently validates a statement-shape and nearby mathlib anchors.
It does not provide a repo-local proof body or a pinned external Lean 4
dependency for Oseledets' multiplicative ergodic theorem.
-/
def machineProofDebt : String := "formalization_debt"

/--
Repo-local integration-debt gate.

No external Lean 4 closure is integrated by this artifact. If a complete
Lean 4 Oseledets proof is found later, the completion gate requires
pin/import/check or an explicit dependency/toolchain/license blocker.
-/
def repoLocalIntegrationDebtGate : String :=
  "not completed; no completed-state repo_local_integration_debt"

/-! ## S1-M-248-C009 external Lean 4 anchor-audit boundary -/

/--
External Lean 4 anchor-audit query row for Oseledets' theorem.

This records the data contract required before any external-upstream completion
claim: a hit must be converted into a pinned dependency, vendored proof body, or
repo-local wrapper that passes this repository's Lake validation.
-/
structure ExternalLeanOseledetsAnchorAuditQuery where
  query : String
  requiredHitRecord : String
  completionGate : String

/--
C009 external Lean 4 queries that must be satisfied by authenticated primary
source search before any external-upstream Oseledets claim is made.
-/
def c009ExternalLeanAnchorAuditQueries :
    List ExternalLeanOseledetsAnchorAuditQuery := [
  {
    query := "Oseledets language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "declaration name, placeholder status, Lean toolchain, Lake dependency " ++
      "closure, and license"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  },
  {
    query := "MultiplicativeErgodic language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "declaration name, placeholder status, Lean toolchain, Lake dependency " ++
      "closure, and license"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  },
  {
    query := "\"multiplicative ergodic theorem\" language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "declaration name, placeholder status, Lean toolchain, Lake dependency " ++
      "closure, and license"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  },
  {
    query := "\"Lyapunov exponent\" language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "declaration name, placeholder status, Lean toolchain, Lake dependency " ++
      "closure, and license"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  },
  {
    query := "Kingman cocycle language:Lean"
    requiredHitRecord := "repository URL, exact commit SHA, Lean module path, " ++
      "declaration name, placeholder status, Lean toolchain, Lake dependency " ++
      "closure, and license"
    completionGate := "external_upstream_anchor_only is not completed; pin, " ++
      "vendor, or locally wrap and validate with Lake"
  }
]

/--
C009 local authentication status.

The local GitHub CLI was not authenticated during this child pass, so the
authenticated GitHub code-search component is a concrete integration blocker
rather than completion evidence.
-/
def c009AuthenticatedExternalSearchStatus : String :=
  "blocked: gh auth status reported no logged-in GitHub hosts, and no GH_TOKEN/GITHUB_TOKEN environment variable was present; GitHub code-search API returned 401 Requires authentication."

/-- C009 did not locate a terminal external Lean 4 Oseledets proof. -/
def c009TerminalExternalLeanOseledetsProofLocated : Bool :=
  false

/--
No completed state in C009 retains repo-local integration debt: no external
Lean 4 proof is claimed, imported, or used as anchor-only completion evidence.
-/
def c009NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c009TerminalExternalLeanOseledetsProofLocated_eq_false :
    c009TerminalExternalLeanOseledetsProofLocated = false :=
  rfl

theorem c009NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c009NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-248-C010 external Lean 4 integration gate -/

/--
Integration-gate row for the C010 child task.

This is the repository-local decision record that follows the C009 external
anchor audit.  It is deliberately open: no external Lean 4 terminal proof of
Oseledets' theorem is available in the current local/audited inputs, so there is
no proof to pin/import/check and no anchor-only evidence is treated as
completion.
-/
structure ExternalLeanOseledetsIntegrationGate where
  terminalProofLocated : Bool
  integrationAction : String
  concreteBlocker : String
  completionStatus : String
  repoLocalDebtGate : String

/--
C010 repo-local integration decision.

If a complete external Lean 4 proof is found later, this row must be replaced by
a pinned dependency, vendored proof body, or repo-local wrapper theorem that
passes this repository's Lake validation, unless a concrete dependency,
toolchain, or license blocker prevents integration.
-/
def c010ExternalLeanOseledetsIntegrationGate :
    ExternalLeanOseledetsIntegrationGate where
  terminalProofLocated := false
  integrationAction := "no pin/import/check performed because no terminal " ++
    "external Lean 4 Oseledets proof was located in the current audited inputs"
  concreteBlocker := "authenticated GitHub code search remains blocked by " ++
    "missing local GitHub credentials; unauthenticated repository search and " ++
    "local pinned-dependency search found no terminal candidate"
  completionStatus := "open/not completed; this artifact is a checked " ++
    "statement-shape and integration-gate record only"
  repoLocalDebtGate := "passes the no-completed-state-with-" ++
    "repo_local_integration_debt gate because no external anchor is claimed " ++
    "as completed"

/-- C010 has no terminal external Lean 4 proof available to integrate. -/
def c010TerminalExternalLeanOseledetsProofLocated : Bool :=
  false

/--
C010 does not close Oseledets' theorem and does not leave anchor-only evidence
as a completed repo-local integration state.
-/
def c010NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c010TerminalExternalLeanOseledetsProofLocated_eq_false :
    c010TerminalExternalLeanOseledetsProofLocated = false :=
  rfl

theorem c010NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c010NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-248-C008 theorem-tree proof packages -/

/--
The five proof packages requested by the public Stage1 Oseledets theorem-tree
line.  These names are stable integration handles for future proof-body work;
the current artifact records the split without claiming the terminal theorem.
-/
inductive OseledetsTheoremTreePackage where
  | kingmanExteriorPower
  | measurableFlag
  | equivariance
  | exponentOrder
  | vectorGrowth
  deriving DecidableEq, Repr

/--
Package-local target for the C008 split.

The Kingman/exterior-power package is tied to the normalized hypotheses because
the local dependency closure has no terminal Kingman theorem or exterior-power
cocycle API.  The remaining packages align with the explicit conclusion
boundaries already present in `OseledetsConclusion`.
-/
def OseledetsTheoremTreePackageTarget
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    (D : OseledetsData Ω ι) :
    OseledetsTheoremTreePackage → Prop
  | .kingmanExteriorPower => OseledetsHypotheses D
  | .measurableFlag => D.measurableSubspaceBoundary
  | .equivariance => D.equivariantSubspaceBoundary
  | .exponentOrder => D.exponentMultiplicityBoundary
  | .vectorGrowth => GrowthRateConclusion D

/-- C008-local status vocabulary; no row is a terminal Oseledets proof. -/
inductive OseledetsPackageStatus where
  | checkedStatementBoundary
  | uncheckedFormalizationDebt
  deriving DecidableEq, Repr

/-- One independently budgeted theorem-tree leaf for the C008 package split. -/
structure OseledetsPackageLeafBudget where
  package : OseledetsTheoremTreePackage
  leafId : String
  obligation : String
  upstreamInputs : String
  downstreamInterface : String
  budgetStepLimit : Nat
  status : OseledetsPackageStatus
  completionBoundary : String

/-- M0387 local proof-leaf budget limit used by the C008 split. -/
def c008LeafBudgetLimit : Nat :=
  100

/--
Integration-ready package ledger for C008.

The rows split future proof-body work into independently budgeted packages.
They are deliberately open: this is a checked package ledger and statement
boundary, not a proof of Oseledets' multiplicative ergodic theorem.
-/
def c008OseledetsPackageLeafBudgets : List OseledetsPackageLeafBudget := [
  {
    package := .kingmanExteriorPower,
    leafId := "S1-M-248-C008-L001-kingman-exterior-power",
    obligation := "Build or import the Kingman/subadditive ergodic theorem branch, exterior-power cocycle construction, determinant/norm comparison, and Lyapunov exponent extraction.",
    upstreamInputs := "RandomMatrixCocycle, matrixCocycleProduct_add, logPlusIntegrable, Mathlib.Analysis.Subadditive, MeasurePreserving.iterate, Ergodic.ae_eq_const_of_ae_eq_comp_ae, and a future exterior-power API",
    downstreamInterface := "OseledetsHypotheses D plus future exterior-power exponent existence lemmas",
    budgetStepLimit := c008LeafBudgetLimit,
    status := .uncheckedFormalizationDebt,
    completionBoundary := "unchecked formalization debt: pinned mathlib has deterministic Subadditive.tendsto_lim but no terminal Kingman theorem, exterior-power cocycle package, or Oseledets theorem"
  },
  {
    package := .measurableFlag,
    leafId := "S1-M-248-C008-L002-measurable-flag",
    obligation := "Choose or import the canonical measurable finite-dimensional Grassmannian/flag model and prove the Oseledets filtration/splitting maps are measurable.",
    upstreamInputs := "MeasurableSubspaceFamily, MeasurableFlagFamily, MeasurableGrassmannianFamily, Submodule, Flag, Module.Grassmannian, and future Borel Grassmannian compatibility lemmas",
    downstreamInterface := "D.measurableSubspaceBoundary",
    budgetStepLimit := c008LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "statement-boundary checked only: explicit measurable-space wrappers exist, but no canonical Oseledets measurable flag API is proved locally"
  },
  {
    package := .equivariance,
    leafId := "S1-M-248-C008-L003-equivariance",
    obligation := "Prove that the Oseledets filtration or splitting is equivariant under the base map and the random matrix cocycle with the repository's forward-product convention.",
    upstreamInputs := "RandomMatrixCocycle.product_succ, RandomMatrixCocycle.product_add, baseMeasurePreserving_iterate, measurable-flag package, and future invariant subspace/splitting lemmas",
    downstreamInterface := "D.equivariantSubspaceBoundary",
    budgetStepLimit := c008LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "statement-boundary checked only: the forward product and base-iterate laws are local anchors, but no invariant filtration proof is present"
  },
  {
    package := .exponentOrder,
    leafId := "S1-M-248-C008-L004-exponent-order",
    obligation := "Prove ordering, multiplicity, rank/drop, and finite-dimensional bookkeeping for the Lyapunov exponents attached to the filtration or splitting.",
    upstreamInputs := "finite index type ι, lyapunovExponent field, exterior-power exponent outputs, determinant/rank bookkeeping, and future multiplicity lemmas",
    downstreamInterface := "D.exponentMultiplicityBoundary",
    budgetStepLimit := c008LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "statement-boundary checked only: exponent multiplicity is an explicit conclusion field, not a proved ordering theorem"
  },
  {
    package := .vectorGrowth,
    leafId := "S1-M-248-C008-L005-vector-growth",
    obligation := "Derive the a.e. vector growth-rate convergence for nonzero vectors in each Oseledets subspace from the exponent, flag, equivariance, and norm-comparison packages.",
    upstreamInputs := "GrowthRateConclusion, finiteMatrixOperatorNorm_mulVec_le, matrixCocycleProduct_add, exponent-order package, equivariance package, and future lower-bound/splitting estimates",
    downstreamInterface := "GrowthRateConclusion D",
    budgetStepLimit := c008LeafBudgetLimit,
    status := .checkedStatementBoundary,
    completionBoundary := "statement-boundary checked only: GrowthRateConclusion is typed, but the analytic convergence proof is not supplied"
  }
]

/-- The C008 package split contains exactly the five requested public packages. -/
theorem c008OseledetsPackageLeafBudgets_length :
    c008OseledetsPackageLeafBudgets.length = 5 := by
  native_decide

/-- Every C008 local leaf is explicitly budgeted at the M0387 `<= 100` threshold. -/
theorem c008OseledetsPackageLeafBudgets_all_le_100 :
    c008OseledetsPackageLeafBudgets.all
      (fun row => row.budgetStepLimit ≤ c008LeafBudgetLimit) = true := by
  native_decide

/--
The normalized hypotheses and conclusion expose each C008 package-local target.

This is only a boundary-alignment theorem.  It does not construct
`OseledetsConclusion D`.
-/
theorem packageTarget_of_hypotheses_and_conclusion
    {Ω : Type u} {ι : Type v} [MeasurableSpace Ω] [Fintype ι] [DecidableEq ι]
    {D : OseledetsData Ω ι}
    (hHyp : OseledetsHypotheses D) (hConclusion : OseledetsConclusion D)
    (package : OseledetsTheoremTreePackage) :
    OseledetsTheoremTreePackageTarget D package := by
  cases package
  · exact hHyp
  · exact hConclusion.measurable_subspaces
  · exact hConclusion.equivariant_subspaces
  · exact hConclusion.exponent_multiplicities
  · exact hConclusion.growth_rates

/-- The C008 split is ready for serial public backfill as an open package ledger. -/
def c008PackageSplitReadyForPublicBackfill : Bool :=
  true

/-- C008 does not close Oseledets' multiplicative ergodic theorem. -/
def c008ClosesOseledetsTheorem : Bool :=
  false

/--
No completed state in the C008 package ledger retains repo-local integration
debt: the package split has no completed terminal theorem state.
-/
def c008NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

theorem c008PackageSplitReadyForPublicBackfill_eq_true :
    c008PackageSplitReadyForPublicBackfill = true :=
  rfl

theorem c008ClosesOseledetsTheorem_eq_false :
    c008ClosesOseledetsTheorem = false :=
  rfl

theorem c008NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c008NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## S1-M-248-C011 public-surface synchronization gate -/

/--
Public surface that must be updated only by a serial integrator.

This child task is documentation-integration work, so the Lean artifact records
the handoff contract without editing shared public planning documents.
-/
structure PublicSurfaceSyncTarget where
  path : String
  mergeCondition : String

/--
C011 public synchronization targets.

These are intentionally not edited by this child worker; the private ledger and
this checked row are the integration-ready handoff for a later serial merge.
-/
def c011PublicSurfaceSyncTargets : List PublicSurfaceSyncTarget := [
  {
    path := "Docs/Stage1_Blueprint.md"
    mergeCondition := "serial integrator merges the private C011 ledger into the public Stage1 surface"
  },
  {
    path := "Docs/todos_20260430.md"
    mergeCondition := "serial integrator propagates the same open/not-completed status and validation record"
  },
  {
    path := "README.md"
    mergeCondition := "serial integrator updates only if the authoritative status surface requires a public summary"
  },
  {
    path := "related meta surface"
    mergeCondition := "serial integrator keeps all public status summaries consistent with the open formalization-debt state"
  }
]

/-- C011 deliberately did not edit shared public documentation. -/
def c011PublicDocsEditedByChild : Bool :=
  false

/-- C011 requires serial public integration after the private ledger is merged. -/
def c011RequiresSerialIntegratorMerge : Bool :=
  true

/-- C011 is not a terminal proof of Oseledets' multiplicative ergodic theorem. -/
def c011ClosesOseledetsTheorem : Bool :=
  false

/--
No completed state in the C011 synchronization handoff retains repo-local
integration debt: C011 makes no completion claim and imports no external proof.
-/
def c011NoCompletedStateRetainsRepoLocalIntegrationDebt : Bool :=
  true

/-- The C011 public synchronization handoff lists the expected four target classes. -/
theorem c011PublicSurfaceSyncTargets_length :
    c011PublicSurfaceSyncTargets.length = 4 := by
  native_decide

theorem c011PublicDocsEditedByChild_eq_false :
    c011PublicDocsEditedByChild = false :=
  rfl

theorem c011RequiresSerialIntegratorMerge_eq_true :
    c011RequiresSerialIntegratorMerge = true :=
  rfl

theorem c011ClosesOseledetsTheorem_eq_false :
    c011ClosesOseledetsTheorem = false :=
  rfl

theorem c011NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c011NoCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check MeasureTheory.MeasurePreserving
#check MeasureTheory.MeasurePreserving.iterate
#check MeasureTheory.MeasurePreserving.integrable_comp
#check MeasureTheory.MeasurePreserving.quasiMeasurePreserving
#check MeasureTheory.Measure.QuasiMeasurePreserving.iterate
#check Ergodic
#check Ergodic.toMeasurePreserving
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae
#check MeasureTheory.AEStronglyMeasurable
#check MeasureTheory.Integrable
#check MeasureTheory.IsProbabilityMeasure
#check ProbabilityTheory.IndepFun
#check ProbabilityTheory.iIndepFun
#check Matrix.det
#check Matrix.mulVec
#check Matrix.GeneralLinearGroup
#check Matrix.linfty_opNorm_eq_opNorm
#check Matrix.linfty_opNorm_mulVec
#check Submodule
#check Filter.Tendsto
#check Subadditive
#check Subadditive.tendsto_lim
#check StatementShape
#check statementShape_iff_forall_data
#check statementShapePublicStatus
#check statementShapeConcreteSubstrate
#check statementShapeConcreteSubstrateStatus
#check statementShapeConcreteSubstrate_eq
#check statementShapeNormStatus
#check statementShapeCocycleApiStatus
#check statementShapeMeasurableFlagApiStatus
#check finiteVectorNorm
#check finiteMatrixOperatorNorm
#check finiteMatrixOperatorNorm_eq_continuousLinearMap_opNorm
#check finiteMatrixOperatorNorm_mulVec_le
#check RandomMatrixCocycle
#check RandomMatrixCocycle.product
#check RandomMatrixCocycle.product_aestronglyMeasurable
#check RandomMatrixCocycle.baseMeasurePreserving_iterate
#check RandomMatrixCocycle.baseQuasiMeasurePreserving_iterate
#check RandomMatrixCocycle.matrix_comp_base_iterate_aestronglyMeasurable
#check matrixCocycleProduct_add
#check RandomMatrixCocycle.product_add
#check OseledetsData.toRandomMatrixCocycle
#check Flag
#check Module.Basis.flag
#check Module.Basis.toFlag
#check Module.Grassmannian
#check Module.Grassmannian.toSubmodule
#check FiniteOseledetsGrassmannian
#check MeasurableSubspaceFamily
#check MeasurableSubspaceFamily.aemeasurable
#check MeasurableFlagFamily
#check MeasurableFlagFamily.aemeasurable
#check MeasurableGrassmannianFamily
#check MeasurableGrassmannianFamily.aemeasurable
#check measurableFlagBranchModules
#check measurableFlagBranchAnchors
#check measurableFlagBranchStatus
#check kingmanSubadditiveBranchModules
#check kingmanSubadditiveBranchAnchors
#check kingmanSubadditiveBranchStatus
#check externalSubadditiveProofAssistantStatus
#check ExternalLeanOseledetsAnchorAuditQuery
#check c009ExternalLeanAnchorAuditQueries
#check c009AuthenticatedExternalSearchStatus
#check c009TerminalExternalLeanOseledetsProofLocated
#check c009TerminalExternalLeanOseledetsProofLocated_eq_false
#check c009NoCompletedStateRetainsRepoLocalIntegrationDebt
#check c009NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check ExternalLeanOseledetsIntegrationGate
#check c010ExternalLeanOseledetsIntegrationGate
#check c010TerminalExternalLeanOseledetsProofLocated
#check c010TerminalExternalLeanOseledetsProofLocated_eq_false
#check c010NoCompletedStateRetainsRepoLocalIntegrationDebt
#check c010NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true
#check OseledetsTheoremTreePackage
#check OseledetsTheoremTreePackageTarget
#check OseledetsPackageStatus
#check OseledetsPackageLeafBudget
#check c008OseledetsPackageLeafBudgets
#check c008OseledetsPackageLeafBudgets_length
#check c008OseledetsPackageLeafBudgets_all_le_100
#check packageTarget_of_hypotheses_and_conclusion
#check c008PackageSplitReadyForPublicBackfill
#check c008ClosesOseledetsTheorem
#check c008NoCompletedStateRetainsRepoLocalIntegrationDebt
#check PublicSurfaceSyncTarget
#check c011PublicSurfaceSyncTargets
#check c011PublicSurfaceSyncTargets_length
#check c011PublicDocsEditedByChild
#check c011PublicDocsEditedByChild_eq_false
#check c011RequiresSerialIntegratorMerge
#check c011RequiresSerialIntegratorMerge_eq_true
#check c011ClosesOseledetsTheorem
#check c011ClosesOseledetsTheorem_eq_false
#check c011NoCompletedStateRetainsRepoLocalIntegrationDebt
#check c011NoCompletedStateRetainsRepoLocalIntegrationDebt_eq_true

end S1_M_248
end Stage1
end AwesomeTheorems
