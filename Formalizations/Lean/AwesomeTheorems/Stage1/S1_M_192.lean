import Mathlib.Analysis.InnerProductSpace.Symmetric
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Matrix.Spectrum

/-!
# S1-M-192 / THM-M-1524: Heisenberg uncertainty principle

This Stage1 file records a conservative Lean boundary for the Heisenberg
uncertainty principle.  The pinned mathlib snapshot has Hilbert-space,
symmetric-operator, adjoint, and Cauchy-Schwarz infrastructure, but no terminal
Robertson/Heisenberg uncertainty theorem was found in the local dependency
closure.

The declarations below therefore normalize the statement shapes around
centered observables, variance, commutators, and the canonical commutation
relation.  The Robertson inequality and its CCR-to-Heisenberg specialization
are proved for this bounded-operator Stage1 model.
-/

noncomputable section

open scoped ComplexConjugate InnerProduct

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_192

/-- A possibly unbounded observable is represented at this Stage1 boundary by a linear operator. -/
abbrev Observable (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] :=
  H →ₗ[ℂ] H

/-- Commutator of two linear observables, `A * B - B * A`. -/
def commutator {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) : Observable H :=
  A * B - B * A

/--
Expectation value of an observable in a vector state.

For symmetric observables this is real; the definition takes the real part so
that centering can be stated without adding a separate real-valuedness proof to
each statement shape.
-/
def expectation {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : Observable H) (ψ : H) : ℝ :=
  (inner ℂ (A ψ) ψ).re

/-- The centered observable vector `(A - E[A]) ψ`. -/
def centeredApply {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : Observable H) (ψ : H) : H :=
  A ψ - (expectation A ψ : ℂ) • ψ

/-- Variance of an observable in a vector state, represented as a squared norm. -/
def variance {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : Observable H) (ψ : H) : ℝ :=
  ‖centeredApply A ψ‖ ^ 2

/-- Centered covariance of two observables in a vector state. -/
def covariance {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H) : ℂ :=
  inner ℂ (centeredApply A ψ) (centeredApply B ψ)

/--
Canonical commutation relation for a pair of observables:
`[Q, P] = i * hbar * I` on all vectors in the chosen common domain/model.
-/
def CanonicalCommutationRelation {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Q P : Observable H) (hbar : ℝ) : Prop :=
  ∀ ψ : H, commutator Q P ψ = (Complex.I * (hbar : ℂ)) • ψ

/--
Robertson uncertainty statement shape for two symmetric observables.

This is the abstract inequality from which the usual Heisenberg position-momentum
form follows after supplying the canonical commutation relation.
-/
def RobertsonStatementShape : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H),
      A.IsSymmetric →
        B.IsSymmetric →
          ‖ψ‖ = 1 →
            ‖inner ℂ (commutator A B ψ) ψ‖ / 2 ≤
              Real.sqrt (variance A ψ) * Real.sqrt (variance B ψ)

/--
Heisenberg position-momentum statement shape under the canonical commutation
relation `[Q, P] = i * hbar * I`.

The field `0 ≤ hbar` freezes the physical constant as a nonnegative real
parameter.  The conclusion is still only a normalized statement shape.
-/
def HeisenbergCCRStatementShape : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Q P : Observable H) (ψ : H) (hbar : ℝ),
      Q.IsSymmetric →
        P.IsSymmetric →
          0 ≤ hbar →
            ‖ψ‖ = 1 →
              CanonicalCommutationRelation Q P hbar →
                hbar / 2 ≤ Real.sqrt (variance Q ψ) * Real.sqrt (variance P ψ)

/-- Canonical Stage1 statement boundary for this slot. -/
def StatementShape : Prop :=
  RobertsonStatementShape.{u} ∧ HeisenbergCCRStatementShape.{u}

/-- Checked boundary record: observables are modeled as complex linear operators. -/
theorem observable_eq_complex_linear_operator
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] :
    Observable H = (H →ₗ[ℂ] H) :=
  rfl

/-- Checked boundary record: the CCR is explicitly `[Q, P] = i * hbar * I`. -/
theorem canonicalCommutationRelation_iff
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Q P : Observable H) (hbar : ℝ) :
    CanonicalCommutationRelation Q P hbar ↔
      ∀ ψ : H, commutator Q P ψ = (Complex.I * (hbar : ℂ)) • ψ :=
  Iff.rfl

/-- Checked boundary record: the Stage1 shape is exactly Robertson plus CCR Heisenberg. -/
theorem statementShape_eq :
    StatementShape.{u} =
      (RobertsonStatementShape.{u} ∧ HeisenbergCCRStatementShape.{u}) :=
  rfl

/-- Variance is nonnegative by construction as a squared norm. -/
theorem variance_nonneg {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : Observable H) (ψ : H) :
    0 ≤ variance A ψ :=
  sq_nonneg _

/-- Variance unfolds to the real inner product of the centered vector with itself. -/
theorem variance_eq_re_inner {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : Observable H) (ψ : H) :
    variance A ψ = (inner ℂ (centeredApply A ψ) (centeredApply A ψ)).re := by
  rw [variance]
  exact (inner_self_eq_norm_sq (𝕜 := ℂ) (centeredApply A ψ)).symm

/--
Checked Hilbert-space anchor: Cauchy-Schwarz applied to the two centered
observable vectors.
-/
theorem centered_cauchy_schwarz {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H) :
    ‖inner ℂ (centeredApply A ψ) (centeredApply B ψ)‖ *
        ‖inner ℂ (centeredApply B ψ) (centeredApply A ψ)‖ ≤
      (inner ℂ (centeredApply A ψ) (centeredApply A ψ)).re *
        (inner ℂ (centeredApply B ψ) (centeredApply B ψ)).re :=
  inner_mul_inner_self_le _ _

/-- Cauchy-Schwarz rewritten in the centered covariance/variance vocabulary. -/
theorem centered_cauchy_schwarz_covariance
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H) :
    ‖covariance A B ψ‖ * ‖covariance B A ψ‖ ≤ variance A ψ * variance B ψ := by
  rw [variance_eq_re_inner A ψ, variance_eq_re_inner B ψ]
  exact inner_mul_inner_self_le (𝕜 := ℂ) (centeredApply A ψ) (centeredApply B ψ)

/-- For symmetric observables, the real-valued expectation coerces back to the inner product. -/
theorem expectation_coe_eq_inner_of_symmetric
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A : Observable H) (ψ : H) (hA : A.IsSymmetric) :
    (expectation A ψ : ℂ) = inner ℂ (A ψ) ψ := by
  unfold expectation
  apply Complex.conj_eq_iff_re.mp
  calc
    (starRingEnd ℂ) (inner ℂ (A ψ) ψ) = inner ℂ ψ (A ψ) := by
      rw [inner_conj_symm (𝕜 := ℂ) ψ (A ψ)]
    _ = inner ℂ (A ψ) ψ := (hA ψ ψ).symm

/-- The commutator inner product is the skew part of the uncentered covariance. -/
theorem commutator_inner_eq_uncentered_skew_of_symmetric
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H) (hA : A.IsSymmetric) (hB : B.IsSymmetric) :
    inner ℂ (commutator A B ψ) ψ = inner ℂ (B ψ) (A ψ) - inner ℂ (A ψ) (B ψ) := by
  rw [commutator]
  simp only [LinearMap.sub_apply, Module.End.mul_apply, inner_sub_left]
  rw [hA (B ψ) ψ, hB (A ψ) ψ]

/--
Centered covariance decomposition: under symmetric observables and a normalized
state, centering cancels from the skew covariance.
-/
theorem covariance_skew_eq_uncentered_skew_of_symmetric
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H)
    (hA : A.IsSymmetric) (hB : B.IsSymmetric) (hψ : ‖ψ‖ = 1) :
    covariance B A ψ - covariance A B ψ =
      inner ℂ (B ψ) (A ψ) - inner ℂ (A ψ) (B ψ) := by
  unfold covariance centeredApply
  rw [expectation_coe_eq_inner_of_symmetric A ψ hA,
    expectation_coe_eq_inner_of_symmetric B ψ hB]
  simp only [inner_sub_left, inner_sub_right, inner_smul_left, inner_smul_right]
  rw [inner_self_eq_one_of_norm_eq_one (𝕜 := ℂ) hψ]
  rw [hA ψ ψ, hB ψ ψ]
  ring

/-- The commutator inner product equals the skew part of centered covariance. -/
theorem commutator_inner_eq_covariance_skew_of_symmetric
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H)
    (hA : A.IsSymmetric) (hB : B.IsSymmetric) (hψ : ‖ψ‖ = 1) :
    inner ℂ (commutator A B ψ) ψ = covariance B A ψ - covariance A B ψ := by
  rw [commutator_inner_eq_uncentered_skew_of_symmetric A B ψ hA hB,
    covariance_skew_eq_uncentered_skew_of_symmetric A B ψ hA hB hψ]

/-- Covariance is conjugate symmetric. -/
theorem covariance_conj_symm
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H) :
    (starRingEnd ℂ) (covariance A B ψ) = covariance B A ψ := by
  unfold covariance
  rw [inner_conj_symm (𝕜 := ℂ) (centeredApply B ψ) (centeredApply A ψ)]

/-- Elementary complex estimate used in the Robertson proof. -/
theorem complex_norm_conj_sub_self_div_two_le (z : ℂ) :
    ‖(starRingEnd ℂ) z - z‖ / 2 ≤ ‖z‖ := by
  rw [div_le_iff₀ (show (0 : ℝ) < 2 by norm_num)]
  calc
    ‖(starRingEnd ℂ) z - z‖ ≤ ‖(starRingEnd ℂ) z‖ + ‖z‖ := norm_sub_le _ _
    _ = 2 * ‖z‖ := by simp [two_mul]
    _ = ‖z‖ * 2 := by ring

/-- The skew part of covariance is bounded by the covariance norm. -/
theorem covariance_skew_norm_half_le
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H) :
    ‖covariance B A ψ - covariance A B ψ‖ / 2 ≤ ‖covariance A B ψ‖ := by
  rw [← covariance_conj_symm A B ψ]
  exact complex_norm_conj_sub_self_div_two_le (covariance A B ψ)

/-- Covariance is bounded by the product of standard deviations. -/
theorem covariance_norm_le_sqrt_variance_mul
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H) :
    ‖covariance A B ψ‖ ≤ Real.sqrt (variance A ψ) * Real.sqrt (variance B ψ) := by
  calc
    ‖covariance A B ψ‖ = ‖inner ℂ (centeredApply A ψ) (centeredApply B ψ)‖ := rfl
    _ ≤ ‖centeredApply A ψ‖ * ‖centeredApply B ψ‖ := norm_inner_le_norm _ _
    _ = Real.sqrt (variance A ψ) * Real.sqrt (variance B ψ) := by
      simp [variance]

/-- Repo-local proof of the Robertson inequality in the current bounded-operator model. -/
theorem robertson_inequality
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H)
    (hA : A.IsSymmetric) (hB : B.IsSymmetric) (hψ : ‖ψ‖ = 1) :
    ‖inner ℂ (commutator A B ψ) ψ‖ / 2 ≤
      Real.sqrt (variance A ψ) * Real.sqrt (variance B ψ) := by
  rw [commutator_inner_eq_covariance_skew_of_symmetric A B ψ hA hB hψ]
  exact le_trans (covariance_skew_norm_half_le A B ψ)
    (covariance_norm_le_sqrt_variance_mul A B ψ)

/-- Checked child result: the Robertson statement shape is locally proved. -/
theorem robertson_statementShape : RobertsonStatementShape.{u} := by
  intro H _ _ A B ψ hA hB hψ
  exact robertson_inequality A B ψ hA hB hψ

/--
Under the canonical commutation relation and a normalized state, the commutator
inner-product term in Robertson has norm `hbar`.
-/
theorem ccr_commutator_inner_norm_eq_hbar_of_normalized
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Q P : Observable H) (ψ : H) (hbar : ℝ)
    (hhbar : 0 ≤ hbar) (hψ : ‖ψ‖ = 1)
    (hCCR : CanonicalCommutationRelation Q P hbar) :
    ‖inner ℂ (commutator Q P ψ) ψ‖ = hbar := by
  calc
    ‖inner ℂ (commutator Q P ψ) ψ‖ =
        ‖inner ℂ ((Complex.I * (hbar : ℂ)) • ψ) ψ‖ := by
      rw [hCCR ψ]
    _ = |hbar| := by
      rw [inner_smul_left]
      rw [inner_self_eq_one_of_norm_eq_one (𝕜 := ℂ) hψ]
      simp
    _ = hbar := abs_of_nonneg hhbar

/--
Repo-local CCR specialization of Robertson: if `[Q, P] = i * hbar * I`,
`0 ≤ hbar`, and `ψ` is normalized, the uncertainty product is at least
`hbar / 2`.
-/
theorem heisenberg_ccr_inequality
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Q P : Observable H) (ψ : H) (hbar : ℝ)
    (hQ : Q.IsSymmetric) (hP : P.IsSymmetric)
    (hhbar : 0 ≤ hbar) (hψ : ‖ψ‖ = 1)
    (hCCR : CanonicalCommutationRelation Q P hbar) :
    hbar / 2 ≤ Real.sqrt (variance Q ψ) * Real.sqrt (variance P ψ) := by
  have hRobertson := robertson_inequality Q P ψ hQ hP hψ
  have hNorm := ccr_commutator_inner_norm_eq_hbar_of_normalized Q P ψ hbar
    hhbar hψ hCCR
  simpa [hNorm] using hRobertson

/-- Checked child result: the CCR Heisenberg statement shape is locally proved. -/
theorem heisenberg_ccr_statementShape : HeisenbergCCRStatementShape.{u} := by
  intro H _ _ Q P ψ hbar hQ hP hhbar hψ hCCR
  exact heisenberg_ccr_inequality Q P ψ hbar hQ hP hhbar hψ hCCR

/-- Checked bounded-operator Stage1 statement boundary. -/
theorem statementShape_local_proof : StatementShape.{u} :=
  ⟨robertson_statementShape, heisenberg_ccr_statementShape⟩

/-- Low-risk introduction wrapper for the combined statement shape. -/
theorem statementShape_intro
    (hR : RobertsonStatementShape.{u})
    (hH : HeisenbergCCRStatementShape.{u}) :
    StatementShape.{u} :=
  ⟨hR, hH⟩

/-- Projection wrapper from the combined boundary to the Robertson inequality shape. -/
theorem statementShape_robertson (h : StatementShape.{u}) :
    RobertsonStatementShape.{u} :=
  h.1

/-- Projection wrapper from the combined boundary to the CCR Heisenberg shape. -/
theorem statementShape_heisenberg (h : StatementShape.{u}) :
    HeisenbergCCRStatementShape.{u} :=
  h.2

/-- Checked mathlib anchor: the identity linear observable is symmetric. -/
theorem identityObservable_symmetric
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] :
    (LinearMap.id : Observable H).IsSymmetric :=
  LinearMap.IsSymmetric.id

/-- Checked mathlib anchor: the zero linear observable is symmetric. -/
theorem zeroObservable_symmetric
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] :
    (0 : Observable H).IsSymmetric :=
  LinearMap.IsSymmetric.zero

/-- Checked bounded-operator anchor: the Hilbert-space adjoint satisfies its defining identity. -/
theorem continuousLinearMap_adjoint_inner_right
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : H →L[ℂ] H) (x y : H) :
    inner ℂ x ((A†) y) = inner ℂ (A x) y :=
  ContinuousLinearMap.adjoint_inner_right A x y

/-! ## Finite-dimensional Hermitian and spectral matrix anchors. -/

/-- Checked finite-dimensional anchor: Hermitian matrices induce symmetric Euclidean linear maps. -/
theorem matrix_isHermitian_iff_isSymmetric
    {𝕜 : Type u} [RCLike 𝕜] {n : Type u} [Fintype n] [DecidableEq n]
    (A : Matrix n n 𝕜) :
    A.IsHermitian ↔ A.toEuclideanLin.IsSymmetric :=
  Matrix.isHermitian_iff_isSymmetric

/-- Checked spectral anchor: Hermitian matrix eigenvalues lie in the real spectrum. -/
theorem matrix_hermitian_eigenvalues_mem_spectrum_real
    {𝕜 : Type u} [RCLike 𝕜] {n : Type u} [Fintype n] [DecidableEq n]
    {A : Matrix n n 𝕜} (hA : A.IsHermitian) (i : n) :
    hA.eigenvalues i ∈ spectrum ℝ A :=
  hA.eigenvalues_mem_spectrum_real i

/-- Checked spectral anchor: Hermitian matrices have a unitary diagonalization. -/
theorem matrix_hermitian_spectral_theorem
    {𝕜 : Type u} [RCLike 𝕜] {n : Type u} [Fintype n] [DecidableEq n]
    {A : Matrix n n 𝕜} (hA : A.IsHermitian) :
    A =
      Unitary.conjStarAlgAut 𝕜 (Matrix n n 𝕜) hA.eigenvectorUnitary
        (Matrix.diagonal (RCLike.ofReal ∘ hA.eigenvalues)) :=
  hA.spectral_theorem

/-- Checked spectral anchor: the real spectrum is the range of Hermitian eigenvalues. -/
theorem matrix_hermitian_spectrum_real_eq_range_eigenvalues
    {𝕜 : Type u} [RCLike 𝕜] {n : Type u} [Fintype n] [DecidableEq n]
    {A : Matrix n n 𝕜} (hA : A.IsHermitian) :
    spectrum ℝ A = Set.range hA.eigenvalues :=
  hA.spectrum_real_eq_range_eigenvalues

/-! ## Public-boundary blocker for unbounded position and momentum operators. -/

/--
Common-domain data needed before upgrading the public target from the abstract
CCR/Robertson boundary to a full position/momentum theorem for unbounded
operators.

The current `Observable` abbreviation is an everywhere-defined complex linear
map.  A genuine position/momentum formalization needs an explicit domain, plus
enough invariance to make the commutator meaningful on that same domain.
-/
structure CommonDomainUnboundedOperatorModel
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] where
  domain : Submodule ℂ H
  Q : domain →ₗ[ℂ] H
  P : domain →ₗ[ℂ] H
  invariantUnderQ : ∀ ψ : domain, Q ψ ∈ domain
  invariantUnderP : ∀ ψ : domain, P ψ ∈ domain

/--
CCR shape on a shared invariant domain for unbounded position/momentum-style
operators.
-/
def CommonDomainCanonicalCommutationRelation
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (M : CommonDomainUnboundedOperatorModel H) (hbar : ℝ) : Prop :=
  ∀ ψ : M.domain,
    M.Q ⟨M.P ψ, M.invariantUnderP ψ⟩ -
        M.P ⟨M.Q ψ, M.invariantUnderQ ψ⟩ =
      (Complex.I * (hbar : ℂ)) • (ψ : H)

/--
Prerequisite shape for claiming the full position/momentum theorem rather than
the abstract CCR/Robertson boundary.
-/
def FullPositionMomentumCommonDomainPrerequisite : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H],
    Nonempty (CommonDomainUnboundedOperatorModel H)

/--
Public theorem boundary for this slot: either supply a common-domain model for
unbounded position/momentum operators, or keep the public theorem at the current
abstract CCR/Robertson statement shape.
-/
def PublicPositionMomentumBoundaryDecision : Prop :=
  FullPositionMomentumCommonDomainPrerequisite.{u} ∨ StatementShape.{u}

/-- Checked record of the public blocker boundary for the full position/momentum theorem. -/
theorem publicPositionMomentumBoundaryDecision_eq :
    PublicPositionMomentumBoundaryDecision.{u} =
      (FullPositionMomentumCommonDomainPrerequisite.{u} ∨ StatementShape.{u}) :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check Observable
#check commutator
#check expectation
#check centeredApply
#check variance
#check covariance
#check CanonicalCommutationRelation
#check RobertsonStatementShape
#check HeisenbergCCRStatementShape
#check StatementShape
#check observable_eq_complex_linear_operator
#check canonicalCommutationRelation_iff
#check statementShape_eq
#check variance_nonneg
#check variance_eq_re_inner
#check centered_cauchy_schwarz
#check centered_cauchy_schwarz_covariance
#check expectation_coe_eq_inner_of_symmetric
#check commutator_inner_eq_uncentered_skew_of_symmetric
#check covariance_skew_eq_uncentered_skew_of_symmetric
#check commutator_inner_eq_covariance_skew_of_symmetric
#check covariance_conj_symm
#check complex_norm_conj_sub_self_div_two_le
#check covariance_skew_norm_half_le
#check covariance_norm_le_sqrt_variance_mul
#check robertson_inequality
#check robertson_statementShape
#check ccr_commutator_inner_norm_eq_hbar_of_normalized
#check heisenberg_ccr_inequality
#check heisenberg_ccr_statementShape
#check statementShape_local_proof
#check inner_smul_left
#check abs_of_nonneg
#check LinearMap.IsSymmetric
#check LinearMap.IsSymmetric.id
#check LinearMap.IsSymmetric.zero
#check LinearMap.IsSymmetric.add
#check LinearMap.IsSymmetric.sub
#check inner_mul_inner_self_le
#check inner_self_eq_norm_sq
#check ContinuousLinearMap.adjoint
#check ContinuousLinearMap.adjoint_inner_left
#check ContinuousLinearMap.adjoint_inner_right
#check Matrix.IsHermitian
#check Matrix.isHermitian_iff_isSymmetric
#check Matrix.spectrum_toLpLin
#check Matrix.IsHermitian.eigenvalues₀
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.eigenvectorBasis
#check Matrix.IsHermitian.mulVec_eigenvectorBasis
#check Matrix.IsHermitian.eigenvalues_mem_spectrum_real
#check Matrix.IsHermitian.eigenvectorUnitary
#check Matrix.IsHermitian.spectral_theorem
#check Matrix.IsHermitian.spectrum_eq_image_range
#check Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues
#check Matrix.IsHermitian.det_eq_prod_eigenvalues
#check LinearMap.IsSymmetric.eigenvectorBasis
#check LinearMap.IsSymmetric.eigenvalues
#check LinearMap.IsSymmetric.hasEigenvalue_eigenvalues
#check CommonDomainUnboundedOperatorModel
#check CommonDomainCanonicalCommutationRelation
#check FullPositionMomentumCommonDomainPrerequisite
#check PublicPositionMomentumBoundaryDecision
#check publicPositionMomentumBoundaryDecision_eq

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.InnerProductSpace.Symmetric",
  "Mathlib.Analysis.InnerProductSpace.Adjoint",
  "Mathlib.Analysis.InnerProductSpace.Projection.Basic",
  "Mathlib.Analysis.InnerProductSpace.Spectrum",
  "Mathlib.Analysis.Matrix.Hermitian",
  "Mathlib.Analysis.Matrix.Spectrum",
  "Mathlib.Analysis.CStarAlgebra.Spectrum",
  "Mathlib.Probability.Distributions.Gaussian.Multivariate",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic"
]

/-- Nearby checked names used or audited for the Stage1 statement boundary. -/
def mathlibAnchorNames : List String := [
  "InnerProductSpace",
  "LinearMap.IsSymmetric",
  "LinearMap.IsSymmetric.id",
  "LinearMap.IsSymmetric.zero",
  "LinearMap.IsSymmetric.add",
  "LinearMap.IsSymmetric.sub",
  "inner_mul_inner_self_le",
  "inner_self_eq_norm_sq",
  "norm_inner_le_norm",
  "inner_self_eq_one_of_norm_eq_one",
  "inner_smul_left",
  "abs_of_nonneg",
  "ccr_commutator_inner_norm_eq_hbar_of_normalized",
  "heisenberg_ccr_inequality",
  "heisenberg_ccr_statementShape",
  "statementShape_local_proof",
  "ContinuousLinearMap.adjoint",
  "ContinuousLinearMap.adjoint_inner_left",
  "ContinuousLinearMap.adjoint_inner_right",
  "Matrix.IsHermitian",
  "Matrix.isHermitian_iff_isSymmetric",
  "Matrix.spectrum_toLpLin",
  "Matrix.IsHermitian.eigenvalues₀",
  "Matrix.IsHermitian.eigenvalues",
  "Matrix.IsHermitian.eigenvectorBasis",
  "Matrix.IsHermitian.mulVec_eigenvectorBasis",
  "Matrix.IsHermitian.eigenvalues_mem_spectrum_real",
  "Matrix.IsHermitian.eigenvectorUnitary",
  "Matrix.IsHermitian.spectral_theorem",
  "Matrix.IsHermitian.spectrum_eq_image_range",
  "Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues",
  "Matrix.IsHermitian.det_eq_prod_eigenvalues",
  "LinearMap.IsSymmetric.eigenvectorBasis",
  "LinearMap.IsSymmetric.eigenvalues",
  "LinearMap.IsSymmetric.hasEigenvalue_eigenvalues",
  "IsSelfAdjoint.mem_spectrum_eq_re",
  "MeasureTheory.MemLp",
  "CommonDomainUnboundedOperatorModel",
  "CommonDomainCanonicalCommutationRelation",
  "FullPositionMomentumCommonDomainPrerequisite",
  "PublicPositionMomentumBoundaryDecision"
]

/--
Search terms that did not locate a terminal Robertson/Heisenberg uncertainty
theorem in the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Heisenberg uncertainty",
  "uncertainty principle",
  "Robertson",
  "Schrodinger uncertainty",
  "Schroedinger uncertainty",
  "variance observable",
  "canonical commutation relation",
  "CCR",
  "position operator",
  "momentum operator"
]

/-! ## C007 external Lean 4 audit metadata. -/

/-- One primary-source external Lean 4 audit row for the C007 child task. -/
structure ExternalLeanAuditRow where
  repository : String
  revision : String
  sourcePath : String
  queryHit : String
  terminalUncertaintyTheorem : Bool
  repoLocalIntegrationBlocker : String
deriving Repr

/-- External audit search terms required by child task `S1-M-192-C007`. -/
def c007ExternalAuditSearchTerms : List String := [
  "Heisenberg",
  "Robertson",
  "uncertainty",
  "CCR",
  "canonical commutation relation",
  "position momentum commutator"
]

/-- Primary-source external Lean 4 audit rows recorded by child task `S1-M-192-C007`. -/
def c007ExternalLeanAuditRows : List ExternalLeanAuditRow := [
  {
    repository := "https://github.com/HEPLean/PhysLean"
    revision := "cd22b0c28882412447d12d5cfde677c4ad999994"
    sourcePath := "Physlib/QuantumMechanics/DDimensions/Operators/Commutation.lean"
    queryHit := "position_commutation_momentum"
    terminalUncertaintyTheorem := false
    repoLocalIntegrationBlocker :=
      "CCR lemma body only; PhysLean uses Lean 4.29.1 and mathlib 5e932f97dd25535344f80f9dd8da3aab83df0fe6, while this repo is pinned to Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95."
  },
  {
    repository := "https://github.com/HEPLean/PhysLean"
    revision := "cd22b0c28882412447d12d5cfde677c4ad999994"
    sourcePath := "Physlib/QuantumMechanics/OneDimension/Operators/Commutation.lean"
    queryHit := "positionOperatorSchwartz_commutation_momentumOperatorSchwartz"
    terminalUncertaintyTheorem := false
    repoLocalIntegrationBlocker :=
      "CCR lemma body only; not a Robertson or Heisenberg uncertainty theorem and not in this repository's Lake dependency closure."
  },
  {
    repository := "https://github.com/SwayingWheatfield/Measure"
    revision := "d70e9ba722ee4a70e163746399bafbc6adbfd48b"
    sourcePath := "measure/src/Measure/Examples/QuantumHarmonic.lean"
    queryHit := "uncertaintyPrinciple"
    terminalUncertaintyTheorem := false
    repoLocalIntegrationBlocker :=
      "Unproved-constant dimensional example, not an importable proof body; project uses Lean 4.28.0-rc1."
  },
  {
    repository := "https://github.com/Timeroot/Lean-QuantumInfo"
    revision := "9b74fd907c9774ac092d5a6b4caa892edaf8a8e9"
    sourcePath := "QuantumInfo/InfiniteDim/QState.lean"
    queryHit := "commented quantum-state skeleton with incomplete proof markers"
    terminalUncertaintyTheorem := false
    repoLocalIntegrationBlocker :=
      "No terminal Heisenberg, Robertson, uncertainty, or CCR proof body found in inspected hits; inspected candidate has incomplete proof markers and uses Lean 4.28.0."
  },
  {
    repository := "https://github.com/DebarghaG/LEAN-Autoformalization-Uncertainty"
    revision := "3cf4278f995a47bb882cc017f20506fbe5e31275"
    sourcePath := "GrammarsFormalUncertainty/Basic.lean"
    queryHit := "uncertainty repository search hit"
    terminalUncertaintyTheorem := false
    repoLocalIntegrationBlocker :=
      "Grammar/probabilistic uncertainty project, not a quantum uncertainty theorem proof body."
  }
]

/-- The C007 audit found no terminal external uncertainty theorem ready for completion. -/
def c007ExternalAuditTerminalClosureFound : Bool := false

/-- The C007 audit does not claim repo-local completion from external anchors. -/
def c007ExternalAuditRepoLocalCompletionClaimed : Bool := false

/-- Checked no-completion gate for the C007 external audit. -/
theorem c007ExternalAuditTerminalClosureFound_eq_false :
    c007ExternalAuditTerminalClosureFound = false :=
  rfl

/-- Checked no-anchor-only-completion gate for the C007 external audit. -/
theorem c007ExternalAuditRepoLocalCompletionClaimed_eq_false :
    c007ExternalAuditRepoLocalCompletionClaimed = false :=
  rfl

end S1_M_192
end Stage1
end AwesomeTheorems
