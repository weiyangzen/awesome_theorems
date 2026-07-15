import Stage1_Instances.«THM-M-1085».Statement
import Mathlib.LinearAlgebra.SesquilinearForm.Star
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.Moments.CovarianceBilin

/-!
# THM-M-1085 finite-law reduction

This module implements the pushforward and coordinate-transport part of the frozen
`M1085-N-LAWS` obligation.  It does not assert the still-open Gaussian orthant comparison.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set Matrix WithLp

namespace Stage1Instances.THM_M_1085.Proof

universe u v w

/-- The lower orthant in the random vector's codomain is measurable for a finite index type. -/
theorem measurableSet_belowAllRange {I : Type u} [Fintype I] (t : ℝ) :
    MeasurableSet {x : I → ℝ | ∀ i, x i ≤ t} := by
  rw [show {x : I → ℝ | ∀ i, x i ≤ t} = ⋂ i, {x | x i ≤ t} by ext; simp]
  exact MeasurableSet.iInter fun i ↦ measurableSet_le (measurable_pi_apply i) measurable_const

/-- The same lower orthant in the Euclidean coordinate model is measurable. -/
theorem measurableSet_belowAllEuclidean {I : Type u} [Fintype I] (t : ℝ) :
    MeasurableSet {z : EuclideanSpace ℝ I | ∀ i, z i ≤ t} := by
  rw [show {z : EuclideanSpace ℝ I | ∀ i, z i ≤ t} = ⋂ i, {z | z i ≤ t} by ext; simp]
  exact MeasurableSet.iInter fun _ ↦ measurableSet_le (by fun_prop) measurable_const

/-- Joint Gaussianity gives the exact Gaussian law of every coordinate. -/
theorem coordinate_hasGaussianLaw {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) (i : I) :
    HasGaussianLaw (fun omega ↦ X omega i) mu := by
  exact hX.eval i

/-- Every coordinate of a jointly Gaussian finite vector is integrable. -/
theorem coordinate_integrable {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) (i : I) :
    Integrable (fun omega ↦ X omega i) mu := by
  exact (coordinate_hasGaussianLaw hX i).integrable

/-- A jointly Gaussian vector forces its ambient measure to be a probability measure. -/
theorem isProbabilityMeasure_of_hasGaussianLaw {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) :
    IsProbabilityMeasure mu := by
  exact hX.isProbabilityMeasure

/-- The original vector realizes its own pushed-forward Gaussian law. -/
theorem pushforward_hasLaw {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) :
    HasLaw X (mu.map X) mu where
  aemeasurable := hX.aemeasurable
  map_eq := rfl

/-- Pushing a vector forward transports its lower-orthant event without approximation. -/
theorem map_apply_belowAllRange {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) (t : ℝ) :
    mu.map X {x : I → ℝ | ∀ i, x i ≤ t} =
      mu (Stage1Instances.THM_M_1085.BelowAll X t) := by
  rw [Measure.map_apply_of_aemeasurable hX.aemeasurable (measurableSet_belowAllRange t)]
  rfl

/-- The Euclidean pushforward has exactly the original lower-orthant probability. -/
theorem map_toLp_apply_belowAllEuclidean {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) (t : ℝ) :
    mu.map (fun omega ↦ toLp 2 (X omega)) {z : EuclideanSpace ℝ I | ∀ i, z i ≤ t} =
      mu (Stage1Instances.THM_M_1085.BelowAll X t) := by
  let hXE : HasGaussianLaw (fun omega ↦ toLp 2 (X omega)) mu := hX.toLp_pi 2
  rw [Measure.map_apply_of_aemeasurable hXE.aemeasurable (measurableSet_belowAllEuclidean t)]
  rfl

/-- Coordinate means are unchanged by passing to the vector's pushforward law. -/
theorem integral_coordinate_map {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) (i : I) :
    (∫ x, x i ∂(mu.map X)) = ∫ omega, X omega i ∂mu := by
  rw [MeasureTheory.integral_map hX.aemeasurable]
  exact Measurable.aestronglyMeasurable (measurable_pi_apply i)

/-- Coordinate covariances are unchanged by passing to the vector's pushforward law. -/
theorem covariance_coordinate_map {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) (i j : I) :
    covariance (fun x : I → ℝ ↦ x i) (fun x : I → ℝ ↦ x j) (mu.map X) =
      covariance (fun omega ↦ X omega i) (fun omega ↦ X omega j) mu := by
  rw [covariance_map]
  · rfl
  · exact Measurable.aestronglyMeasurable (measurable_pi_apply i)
  · exact Measurable.aestronglyMeasurable (measurable_pi_apply j)
  · exact hX.aemeasurable

/-- The coordinate covariance matrix of the presented random vector. -/
noncomputable def covarianceMatrix {I : Type u} {Omega : Type v} [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Omega → I → ℝ) : Matrix I I ℝ :=
  fun i j ↦ covariance (fun omega ↦ X omega i) (fun omega ↦ X omega j) mu

/-- The coordinate matrix is the matrix of the covariance bilinear form of the pushed-forward
Euclidean vector. -/
theorem covarianceMatrix_eq {I : Type u} [Fintype I] [DecidableEq I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) :
    covarianceMatrix mu X =
      LinearMap.toMatrix₂ (PiLp.basisFun 2 ℝ I) (PiLp.basisFun 2 ℝ I)
        (covarianceBilin (mu.map (fun omega ↦ toLp 2 (X omega)))).toBilinForm := by
  letI : IsProbabilityMeasure mu := hX.isProbabilityMeasure
  ext i j
  rw [LinearMap.toMatrix₂_apply]
  exact (covarianceBilin_apply_basisFun (fun k ↦ (hX.eval k).memLp_two) i j).symm

/-- A Gaussian vector's coordinate covariance matrix is positive semidefinite, including in the
singular and repeated-coordinate cases admitted by the frozen target. -/
theorem covarianceMatrix_posSemidef {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) :
    (covarianceMatrix mu X).PosSemidef := by
  classical
  rw [covarianceMatrix_eq hX]
  exact (LinearMap.isPosSemidef_iff_posSemidef_toMatrix (PiLp.basisFun 2 ℝ I)).mp
    (LinearMap.BilinForm.isPosSemidef_iff.mp isPosSemidef_covarianceBilin)

/-- Equal coordinate variances become equal covariance-matrix diagonals. -/
theorem covarianceMatrix_diag_eq {I : Type u}
    {OmegaX : Type v} [MeasurableSpace OmegaX] {muX : Measure OmegaX}
    {OmegaY : Type w} [MeasurableSpace OmegaY] {muY : Measure OmegaY}
    {X : OmegaX → I → ℝ} {Y : OmegaY → I → ℝ}
    (hdiag : ∀ i, covariance (fun omega ↦ X omega i) (fun omega ↦ X omega i) muX =
      covariance (fun omega ↦ Y omega i) (fun omega ↦ Y omega i) muY) :
    ∀ i, covarianceMatrix muX X i i = covarianceMatrix muY Y i i := by
  intro i
  simpa [covarianceMatrix] using hdiag i

/-- Off-diagonal covariance order becomes entrywise matrix order away from the diagonal. -/
theorem covarianceMatrix_offdiag_le {I : Type u}
    {OmegaX : Type v} [MeasurableSpace OmegaX] {muX : Measure OmegaX}
    {OmegaY : Type w} [MeasurableSpace OmegaY] {muY : Measure OmegaY}
    {X : OmegaX → I → ℝ} {Y : OmegaY → I → ℝ}
    (hoff : ∀ i j, i ≠ j →
      covariance (fun omega ↦ X omega i) (fun omega ↦ X omega j) muX ≤
        covariance (fun omega ↦ Y omega i) (fun omega ↦ Y omega j) muY) :
    ∀ i j, i ≠ j → covarianceMatrix muX X i j ≤ covarianceMatrix muY Y i j := by
  intro i j hij
  simpa [covarianceMatrix] using hoff i j hij

/-- Exact covariance-matrix package required by the frozen `M1085-N-MATRIX` obligation. -/
theorem covarianceMatrix_order_data {I : Type u} [Fintype I]
    {OmegaX : Type v} [MeasurableSpace OmegaX] {muX : Measure OmegaX}
    {OmegaY : Type w} [MeasurableSpace OmegaY] {muY : Measure OmegaY}
    {X : OmegaX → I → ℝ} {Y : OmegaY → I → ℝ}
    (hX : HasGaussianLaw X muX) (hY : HasGaussianLaw Y muY)
    (hdiag : ∀ i, covariance (fun omega ↦ X omega i) (fun omega ↦ X omega i) muX =
      covariance (fun omega ↦ Y omega i) (fun omega ↦ Y omega i) muY)
    (hoff : ∀ i j, i ≠ j →
      covariance (fun omega ↦ X omega i) (fun omega ↦ X omega j) muX ≤
        covariance (fun omega ↦ Y omega i) (fun omega ↦ Y omega j) muY) :
    (covarianceMatrix muX X).PosSemidef ∧
      (covarianceMatrix muY Y).PosSemidef ∧
      (∀ i, covarianceMatrix muX X i i = covarianceMatrix muY Y i i) ∧
      (∀ i j, i ≠ j → covarianceMatrix muX X i j ≤ covarianceMatrix muY Y i j) := by
  exact ⟨covarianceMatrix_posSemidef hX, covarianceMatrix_posSemidef hY,
    covarianceMatrix_diag_eq hdiag, covarianceMatrix_offdiag_le hoff⟩

/-- The centered pushed-forward Euclidean law has zero vector mean. -/
theorem integral_toLp_map_eq_zero {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu)
    (hmean : ∀ i, ∫ omega, X omega i ∂mu = 0) :
    ∫ z, z ∂(mu.map (fun omega ↦ toLp 2 (X omega))) = (0 : EuclideanSpace ℝ I) := by
  classical
  let hXE : HasGaussianLaw (fun omega ↦ toLp 2 (X omega)) mu := hX.toLp_pi 2
  letI : IsGaussian (mu.map (fun omega ↦ toLp 2 (X omega))) := hXE.isGaussian_map
  apply PiLp.ext
  intro i
  rw [MeasureTheory.eval_integral_piLp (fun k ↦ IsGaussian.integrable_id.eval_piLp k)]
  rw [MeasureTheory.integral_map hXE.aemeasurable]
  · simpa using hmean i
  · fun_prop

/-- The pushed-forward law and canonical multivariate Gaussian have the same covariance form. -/
theorem covarianceBilin_map_eq_multivariateGaussian {I : Type u} [Fintype I]
    [DecidableEq I] {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu) :
    covarianceBilin (mu.map (fun omega ↦ toLp 2 (X omega))) =
      covarianceBilin
        (multivariateGaussian (0 : EuclideanSpace ℝ I) (covarianceMatrix mu X)) := by
  letI : IsProbabilityMeasure mu := hX.isProbabilityMeasure
  rw [← ContinuousLinearMap.toBilinForm_inj]
  refine LinearMap.BilinForm.ext_basis (EuclideanSpace.basisFun I ℝ).toBasis fun i j ↦ ?_
  rw [ContinuousLinearMap.toBilinForm_apply, ContinuousLinearMap.toBilinForm_apply]
  rw [covarianceBilin_multivariateGaussian (covarianceMatrix_posSemidef hX)]
  change covarianceBilin (mu.map (fun omega ↦ toLp 2 fun k ↦ X omega k))
      (EuclideanSpace.basisFun I ℝ i) (EuclideanSpace.basisFun I ℝ j) = _
  rw [covarianceBilin_apply_basisFun (fun k ↦ (hX.eval k).memLp_two)]
  simp [covarianceMatrix]

/-- A centered jointly Gaussian presentation is exactly its canonical possibly singular
multivariate Gaussian law. -/
theorem gaussian_law_eq_multivariateGaussian {I : Type u} [Fintype I]
    [DecidableEq I] {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu)
    (hmean : ∀ i, ∫ omega, X omega i ∂mu = 0) :
    mu.map (fun omega ↦ toLp 2 (X omega)) =
      multivariateGaussian (0 : EuclideanSpace ℝ I) (covarianceMatrix mu X) := by
  let hXE : HasGaussianLaw (fun omega ↦ toLp 2 (X omega)) mu := hX.toLp_pi 2
  letI : IsGaussian (mu.map (fun omega ↦ toLp 2 (X omega))) := hXE.isGaussian_map
  apply IsGaussian.ext
  · change (∫ x, x ∂(mu.map (fun omega ↦ toLp 2 (X omega)))) =
      ∫ x, x ∂multivariateGaussian 0 (covarianceMatrix mu X)
    rw [integral_toLp_map_eq_zero hX hmean, integral_id_multivariateGaussian]
  · exact covarianceBilin_map_eq_multivariateGaussian hX

/-- The original lower-orthant probability is the corresponding probability under the canonical
possibly singular multivariate Gaussian law. -/
theorem belowAll_eq_multivariateGaussian {I : Type u} [Fintype I] [DecidableEq I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega → I → ℝ} (hX : HasGaussianLaw X mu)
    (hmean : ∀ i, ∫ omega, X omega i ∂mu = 0) (t : ℝ) :
    mu (Stage1Instances.THM_M_1085.BelowAll X t) =
      multivariateGaussian 0 (covarianceMatrix mu X)
        {z : EuclideanSpace ℝ I | ∀ i, z i ≤ t} := by
  rw [← gaussian_law_eq_multivariateGaussian hX hmean]
  exact (map_toLp_apply_belowAllEuclidean hX t).symm

/-- Slepian's comparison after normalization to Gaussian measures on a finite coordinate space.
This is the remaining analytic leaf after `M1085-N-LAWS`; it is deliberately a proposition, not
an assumption or a declaration without a body. -/
def LawSlepianTarget : Prop :=
  ∀ (I : Type u) [Fintype I] [Nonempty I]
    (muX muY : Measure (I → ℝ)),
      IsGaussian muX →
      IsGaussian muY →
      (∀ i, (∫ x, x i ∂muX) = 0) →
      (∀ i, (∫ y, y i ∂muY) = 0) →
      (∀ i, covariance (fun x ↦ x i) (fun x ↦ x i) muX =
        covariance (fun y ↦ y i) (fun y ↦ y i) muY) →
      (∀ i j, i ≠ j →
        covariance (fun x ↦ x i) (fun x ↦ x j) muX ≤
          covariance (fun y ↦ y i) (fun y ↦ y j) muY) →
      ∀ t : ℝ, muX {x | ∀ i, x i ≤ t} ≤ muY {y | ∀ i, y i ≤ t}

/-- Exact child-to-root reduction: a comparison theorem for finite Gaussian laws proves the
frozen target, including different sample spaces and singular laws. -/
theorem slepianTarget_of_law (h : LawSlepianTarget.{u}) :
    Stage1Instances.THM_M_1085.SlepianTarget.{u, v, w} := by
  intro I _ _ OmegaX _ muX OmegaY _ muY X Y hX hY hmeanX hmeanY hdiag hoff t
  rw [← map_apply_belowAllRange hX t, ← map_apply_belowAllRange hY t]
  apply h I (muX.map X) (muY.map Y) hX.isGaussian_map hY.isGaussian_map
  · intro i
    rw [integral_coordinate_map hX i, hmeanX i]
  · intro i
    rw [integral_coordinate_map hY i, hmeanY i]
  · intro i
    rw [covariance_coordinate_map hX i i, covariance_coordinate_map hY i i]
    exact hdiag i
  · intro i j hij
    rw [covariance_coordinate_map hX i j, covariance_coordinate_map hY i j]
    exact hoff i j hij

#print sorries measurableSet_belowAllRange
#print axioms measurableSet_belowAllRange
#print sorries measurableSet_belowAllEuclidean
#print axioms measurableSet_belowAllEuclidean
#print sorries coordinate_hasGaussianLaw
#print axioms coordinate_hasGaussianLaw
#print sorries coordinate_integrable
#print axioms coordinate_integrable
#print sorries isProbabilityMeasure_of_hasGaussianLaw
#print axioms isProbabilityMeasure_of_hasGaussianLaw
#print sorries pushforward_hasLaw
#print axioms pushforward_hasLaw
#print sorries map_apply_belowAllRange
#print axioms map_apply_belowAllRange
#print sorries map_toLp_apply_belowAllEuclidean
#print axioms map_toLp_apply_belowAllEuclidean
#print sorries integral_coordinate_map
#print axioms integral_coordinate_map
#print sorries covariance_coordinate_map
#print axioms covariance_coordinate_map
#print sorries covarianceMatrix_eq
#print axioms covarianceMatrix_eq
#print sorries covarianceMatrix_posSemidef
#print axioms covarianceMatrix_posSemidef
#print sorries covarianceMatrix_diag_eq
#print axioms covarianceMatrix_diag_eq
#print sorries covarianceMatrix_offdiag_le
#print axioms covarianceMatrix_offdiag_le
#print sorries covarianceMatrix_order_data
#print axioms covarianceMatrix_order_data
#print sorries integral_toLp_map_eq_zero
#print axioms integral_toLp_map_eq_zero
#print sorries covarianceBilin_map_eq_multivariateGaussian
#print axioms covarianceBilin_map_eq_multivariateGaussian
#print sorries gaussian_law_eq_multivariateGaussian
#print axioms gaussian_law_eq_multivariateGaussian
#print sorries belowAll_eq_multivariateGaussian
#print axioms belowAll_eq_multivariateGaussian
#print sorries slepianTarget_of_law
#print axioms slepianTarget_of_law

end Stage1Instances.THM_M_1085.Proof
