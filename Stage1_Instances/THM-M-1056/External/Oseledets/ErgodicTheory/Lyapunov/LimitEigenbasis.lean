/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.ForwardV
import ErgodicTheory.Lyapunov.SpectrumResiduals

/-!
# Limit eigenbasis of the Oseledets limit operator

This module builds the **limit eigenbasis** of the sanitized (everywhere self-adjoint)
Oseledets limit operator `lambdaHat A T x`, indexed by `Fin d` and sorted *decreasingly*
consistently with `Matrix.IsHermitian.eigenvalues₀`.

## Main results

* `limitEigenbasis` — the sorted orthonormal eigenbasis of `lambdaHat A T x`.
* `limitEigenbasis_eigenpair` — the everywhere eigenpair identity, with eigenvalue
  `eigenvalues₀ ⟨e, …⟩`.
* `limitEigenbasis_eigenpair_exp` — a.e. the eigenvalue is `Real.exp (lamSing A T x e)`.
* `inner_limitEigenbasis_eq_zero_of_slow` — a.e., a sorted eigenvector is orthogonal to the
  slow subspace `vslow A T (exp t) x` whenever its exponent strictly exceeds `t`.
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {μ : MeasureTheory.Measure X} {d : ℕ} {T : X → X}

/-! ### The sorted limit eigenbasis -/

/-- **The sorted limit eigenbasis.**  The orthonormal eigenbasis of the everywhere self-adjoint
sanitized limit `lambdaHat A T x`, reindexed by `Fin d` so that `limitEigenbasis A T x e` has
eigenvalue `eigenvalues₀ ⟨e, …⟩` (**antitone**, descending).  Built by mimicking
`sortedGramEigenbasis`: take the eigenvector basis of `(lambdaHat_isSelfAdjoint A T x).isHermitian`,
reindex from `Fin d` to `Fin (card (Fin d))` (the sorted index), then `finCongr` back to `Fin d`. -/
noncomputable def limitEigenbasis [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    (x : X) :
    OrthonormalBasis (Fin d) ℝ (EuclideanSpace ℝ (Fin d)) :=
  (((lambdaHat_isSelfAdjoint A T x).isHermitian.eigenvectorBasis.reindex
    (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))).symm).reindex
    (finCongr (Fintype.card_fin d)))

/-! ### The everywhere eigenpair -/

omit [MeasurableSpace X] in
/-- **The everywhere eigenpair.**  `limitEigenbasis A T x e` is an eigenvector of
`toEuclideanLin (lambdaHat A T x)` with eigenvalue the sorted eigenvalue
`eigenvalues₀ ⟨e, …⟩`.  Mimics `sortedGramEigenbasis_eigenpair`. -/
theorem limitEigenbasis_eigenpair [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    (x : X) (e : Fin d) :
    Matrix.toEuclideanLin (lambdaHat A T x) (limitEigenbasis A T x e)
      = ((lambdaHat_isSelfAdjoint A T x).isHermitian.eigenvalues₀
          ⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩) •
        limitEigenbasis A T x e := by
  set hM := (lambdaHat_isSelfAdjoint A T x).isHermitian with hMdef
  set e₁ : Fin d ≃ Fin (Fintype.card (Fin d)) :=
    (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))).symm with he₁
  -- Unfold both reindexes down to the underlying eigenvector basis.
  have hbase : limitEigenbasis A T x e
      = hM.eigenvectorBasis (e₁.symm ((finCongr (Fintype.card_fin d)).symm e)) := by
    change ((((lambdaHat_isSelfAdjoint A T x).isHermitian.eigenvectorBasis.reindex
      (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))).symm).reindex
      (finCongr (Fintype.card_fin d))) e) = _
    rw [OrthonormalBasis.reindex_apply, OrthonormalBasis.reindex_apply, he₁, hMdef]
  rw [hbase]
  set idx : Fin (Fintype.card (Fin d)) := (finCongr (Fintype.card_fin d)).symm e with hidxdef
  -- `idx = ⟨e, …⟩` since `finCongr.symm` preserves the `ℕ`-value.
  have hidx : idx = (⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩ :
      Fin (Fintype.card (Fin d))) := by
    apply Fin.ext; rw [hidxdef, finCongr_symm_apply_coe]
  -- `eigenvalues (e₁.symm idx) = eigenvalues₀ idx` via the `symm_apply_apply` cancellation.
  have hval : hM.eigenvalues (e₁.symm idx) = hM.eigenvalues₀ idx := by
    rw [Matrix.IsHermitian.eigenvalues, he₁]
    congr 1
    change (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))).symm
      ((Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))) idx) = idx
    simp [Equiv.symm_apply_apply]
  rw [hidx] at hval
  rw [← hval, Matrix.toLpLin_apply, hM.mulVec_eigenvectorBasis]; rfl

/-! ### Almost-everywhere eigenvalue identification as `exp (lamSing)` -/

/-- **A.e. eigenvalue identification.**  On the a.e. set where the Oseledets limit is Hermitian,
`lambdaHat = oseledetsLimit`, and the sorted eigenvalue equals `Real.exp (lamSing A T x e)`. -/
theorem limitEigenbasis_eigenpair_exp [MeasureTheory.IsProbabilityMeasure μ] [NeZero d]
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, ∀ e : Fin d,
      Matrix.toEuclideanLin (lambdaHat A T x) (limitEigenbasis A T x e)
        = Real.exp (lamSing A T x (e : ℕ)) • limitEigenbasis A T x e := by
  filter_upwards [oseledetsLimit_isSelfAdjoint hT hA hAmeas hint hint',
    oseledetsLimit_eigenvalues₀_eq hT hA hAmeas hint hint'] with x hsa heig
  intro e
  -- On the Hermitian set `lambdaHat = oseledetsLimit`.
  have hH : (oseledetsLimit A T x).IsHermitian := Matrix.isHermitian_iff_isSelfAdjoint.mpr hsa
  have hlh : lambdaHat A T x = oseledetsLimit A T x := by rw [lambdaHat, if_pos hH]
  -- The two `IsHermitian` instances are over equal matrices, so their `eigenvalues₀` agree.
  have hHeq : (lambdaHat_isSelfAdjoint A T x).isHermitian.eigenvalues₀
      ⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩
      = hH.eigenvalues₀ ⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩ := by
    -- `eigenvalues₀` depends only on the matrix; transport along `hlh` and use proof irrelevance.
    have key : ∀ (M : Matrix (Fin d) (Fin d) ℝ) (hM : M.IsHermitian),
        M = oseledetsLimit A T x →
        hM.eigenvalues₀ ⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩
          = hH.eigenvalues₀ ⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩ := by
      rintro M hM rfl
      rw [Subsingleton.elim hM hH]
    exact key (lambdaHat A T x) (lambdaHat_isSelfAdjoint A T x).isHermitian hlh
  rw [limitEigenbasis_eigenpair, hHeq,
    heig hH ⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩]

/-! ### Orthogonality to the slow subspace -/

/-- **Slow orthogonality.**  A.e., a sorted limit eigenvector `limitEigenbasis A T x e` whose
exponent `lam0 e` strictly exceeds the cutoff `t` is orthogonal to every vector in the slow subspace
`vslow A T (exp t) x`.

Route: `v ∈ vslow` means `slowProjector` fixes `v`; self-adjointness moves the projector onto the
eigenvector, where the indicator-CFC `slowProjector` annihilates it (its eigenvalue `exp (lam0 e)`
exceeds `exp t`, outside `Iic (exp t)`). -/
theorem inner_limitEigenbasis_eq_zero_of_slow [MeasureTheory.IsProbabilityMeasure μ] [NeZero d]
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i))) :
    ∀ᵐ x ∂μ, ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, ∀ e : Fin d,
      t < lam0 (e : ℕ) → inner ℝ (limitEigenbasis A T x e) v = 0 := by
  filter_upwards [limitEigenbasis_eigenpair_exp hT hA hAmeas hint hint',
    ae_lamSing_eq_lam0 lam0 hlam0] with x hpair hlameq
  intro t v hv e het
  -- `v ∈ vslow` ⟺ `slowProjector` fixes `v` (idempotency bridge).
  have hPv : Matrix.toEuclideanLin (slowProjector A T (Real.exp t) x) v = v := by
    rw [vslow, mem_range_toEuclideanCLM_iff (slowProjector_mul_self A T (Real.exp t) x)] at hv
    exact hv
  set b := limitEigenbasis A T x e with hb
  -- Move the self-adjoint projector from `v` onto the eigenvector `b`.
  have hsa : IsSelfAdjoint
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (slowProjector A T (Real.exp t) x)) := by
    have hself := slowProjector_isSelfAdjoint A T (Real.exp t) x
    rw [IsSelfAdjoint]
    exact (Matrix.toEuclideanCLM (n := Fin d) (𝕜 := ℝ)).map_star'
        (slowProjector A T (Real.exp t) x) ▸
      congrArg (Matrix.toEuclideanCLM (n := Fin d) (𝕜 := ℝ)) hself
  have hcoe : ∀ w, Matrix.toEuclideanLin (slowProjector A T (Real.exp t) x) w
      = Matrix.toEuclideanCLM (𝕜 := ℝ) (slowProjector A T (Real.exp t) x) w := fun w => by
    rw [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]; rfl
  -- `⟪b, v⟫ = ⟪b, P v⟫ = ⟪P b, v⟫` and `P b = 0`.
  have hPb : Matrix.toEuclideanLin (slowProjector A T (Real.exp t) x) b = 0 := by
    -- `slowProjector = cfc (indicator (Iic (exp t))) lambdaHat`, acting on the eigenvector `b`.
    rw [slowProjector]
    -- `b` is an eigenvector of `lambdaHat` with eigenvalue `exp (lamSing e) = exp (lam0 e)`.
    have hev : Matrix.toEuclideanLin (lambdaHat A T x) b
        = Real.exp (lamSing A T x (e : ℕ)) • b := hpair e
    -- The indicator at that eigenvalue is `0` since `exp (lam0 e) > exp t`.
    have hgt : Real.exp t < Real.exp (lamSing A T x (e : ℕ)) := by
      rw [hlameq e]; exact Real.exp_lt_exp.mpr het
    have hind : Set.indicator (Set.Iic (Real.exp t)) (1 : ℝ → ℝ)
        (Real.exp (lamSing A T x (e : ℕ))) = 0 :=
      Set.indicator_of_notMem (by simp only [Set.mem_Iic, not_le]; exact hgt) _
    -- Apply the cfc-on-eigenvector lemma, using that `b` is an eigenvector basis vector of
    -- `lambdaHat`: reduce `b` to the underlying `eigenvectorBasis` index and use
    -- `toEuclideanLin_cfc_eigenvectorBasis`.
    set hM := (lambdaHat_isSelfAdjoint A T x).isHermitian with hMdef
    set e₁ : Fin d ≃ Fin (Fintype.card (Fin d)) :=
      (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))).symm with he₁
    have hbase : b = hM.eigenvectorBasis (e₁.symm ((finCongr (Fintype.card_fin d)).symm e)) := by
      rw [hb]
      change ((((lambdaHat_isSelfAdjoint A T x).isHermitian.eigenvectorBasis.reindex
        (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))).symm).reindex
        (finCongr (Fintype.card_fin d))) e) = _
      rw [OrthonormalBasis.reindex_apply, OrthonormalBasis.reindex_apply, he₁, hMdef]
    rw [hbase, toEuclideanLin_cfc_eigenvectorBasis (lambdaHat A T x) hM
      (Set.indicator (Set.Iic (Real.exp t)) (1 : ℝ → ℝ))
      (e₁.symm ((finCongr (Fintype.card_fin d)).symm e))]
    -- The eigenvalue here equals `exp (lamSing e)`, where the indicator vanishes.
    set idx : Fin (Fintype.card (Fin d)) := (finCongr (Fintype.card_fin d)).symm e with hidxdef
    have hidx : idx = (⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩ :
        Fin (Fintype.card (Fin d))) := by
      apply Fin.ext; rw [hidxdef, finCongr_symm_apply_coe]
    have hvaleq : hM.eigenvalues (e₁.symm idx)
        = Real.exp (lamSing A T x (e : ℕ)) := by
      -- `eigenvalues (e₁.symm idx) = eigenvalues₀ idx`, and the eigenpair pins this to
      -- `exp (lamSing)`.
      have h1 : hM.eigenvalues (e₁.symm idx) = hM.eigenvalues₀ idx := by
        rw [Matrix.IsHermitian.eigenvalues, he₁]
        congr 1
        change (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))).symm
          ((Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d)))) idx) = idx
        simp [Equiv.symm_apply_apply]
      rw [h1, hidx]
      -- compare with `limitEigenbasis_eigenpair` and `hpair`.
      have heq2 :
          (hM.eigenvalues₀ ⟨(e : ℕ), lt_of_lt_of_eq e.isLt (Fintype.card_fin d).symm⟩) • b
            = Real.exp (lamSing A T x (e : ℕ)) • b := by
        rw [← limitEigenbasis_eigenpair A T x e, ← hb, hev]
      -- `b ≠ 0` (orthonormal basis vector), so cancel.
      have hbne : b ≠ 0 := by
        intro h0
        have hnorm := (limitEigenbasis A T x).orthonormal.1 e
        rw [← hb, h0] at hnorm; simp at hnorm
      exact smul_left_injective ℝ hbne heq2
    rw [hvaleq, hind, zero_smul]
  -- Assemble: `⟪b, v⟫ = ⟪b, P v⟫ = ⟪P b, v⟫ = ⟪0, v⟫ = 0`.
  have hmove : (inner ℝ b v : ℝ)
      = inner ℝ
          ((Matrix.toEuclideanCLM (𝕜 := ℝ) (slowProjector A T (Real.exp t) x)) b) v := by
    conv_lhs => rw [← hPv, hcoe]
    exact (hsa.isSymmetric.apply_clm b v).symm
  rw [hmove, ← hcoe, hPb, inner_zero_left]

end ErgodicTheory
