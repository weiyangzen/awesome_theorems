/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.FiltrationFromTopGapEnvelope
import ErgodicTheory.Lyapunov.TopGapEnvelope
import ErgodicTheory.TwoSided.SpectralRank

/-!
# Strong export of the forward Oseledets filtration (two-sided MET)

This module records the
one-sided Oseledets filtration theorem in a **strong form**: the deterministic spectral
data `lam0` and the everywhere-measurable filtration `V` are *exposed* by the
existential (rather than buried), the Lyapunov exponents are the concrete descending
enumeration `expEnum lam0 d`, and — the new content — the dimension of each interior
filtration level is given by the forward dimension formula

`finrank (V i.castSucc x) = #{j < d | lam0 j ≤ expEnum lam0 d i}`.

The proof reuses the one-sided composition with the concrete witness
`V := vprime A T lam0`: it discharges the top-gap fast-band-mass envelope, builds the
spectral, slow-flag and growth interfaces exactly as `oseledets_filtration_of_topgap`
and `oseledets_filtration_of_upper'` do, and reads the structural block off
`vassembled_structure_ae` transported through `vprime_eq_vassembled_of_slowflag`.  The dimension
clause is supplied by `ae_finrank_vslow`, using that on the interior `vprime A T lam0`
reduces definitionally to `vslow` at the deterministic cutoff `expEnum lam0 d i`.

## Main results

* `oseledets_filtration_dims` — the strong export with the spectral data exposed and the
  forward dimension formula adjoined.
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix Matrix.Norms.L2Operator RealInnerProductSpace BigOperators

noncomputable section

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]

/-- **Strong forward Oseledets filtration with dimensions.**

The one-sided Oseledets theorem stated with its spectral data exposed: there is a
deterministic antitone-on-`[0, d)` singular-exponent sequence `lam0` such that, for every
`i < d`, the normalized log of the `i`-th singular value of `A⁽ⁿ⁾` converges to `lam0 i`
a.e.; and there is an everywhere-measurable filtration `V` of `EuclideanSpace ℝ (Fin d)`
indexed by `Fin (numExp lam0 d + 1)`, whose Lyapunov exponents are the descending
enumeration `expEnum lam0 d`, which is, a.e., a strictly decreasing `A`-equivariant flag
`⊤ = V 0 ⊋ ⋯ ⊋ V (last) = ⊥` along which `(1/n) log‖A⁽ⁿ⁾ v‖ → expEnum lam0 d i` for
`v ∈ V i.castSucc ∖ V i.succ`, and whose interior level dimensions satisfy the forward
dimension formula `finrank (V i.castSucc x) = #{j < d | lam0 j ≤ expEnum lam0 d i}`. -/
theorem oseledets_filtration_dims
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ (lam0 : ℕ → ℝ),
      (∀ a b : ℕ, a ≤ b → b < d → lam0 b ≤ lam0 a) ∧
      (∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
        Filter.atTop (𝓝 (lam0 i))) ∧
      ∃ (V : Fin (numExp lam0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))),
        (∀ i, MeasurableSubspace fun x => V i x) ∧
        ∀ᵐ x ∂μ,
          V 0 x = ⊤ ∧ V (Fin.last (numExp lam0 d)) x = ⊥ ∧
          (∀ i : Fin (numExp lam0 d), V i.succ x < V i.castSucc x) ∧
          (∀ i : Fin (numExp lam0 d + 1),
            Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x)
              = V i (T x)) ∧
          (∀ i : Fin (numExp lam0 d),
            ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))),
              v ∉ V i.succ x →
              Tendsto
                (fun n : ℕ => (n : ℝ)⁻¹ *
                  Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
                atTop (𝓝 (expEnum lam0 d i))) ∧
          (∀ i : Fin (numExp lam0 d),
            Module.finrank ℝ (V i.castSucc x)
              = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card) := by
  classical
  have hTmeas : Measurable T := hT.toMeasurePreserving.measurable
  -- The deterministic singular-value exponents.
  obtain ⟨lam0, hmono, hlam0⟩ :=
    exists_lam_tendsto_singularValue hT hA hAmeas hint hint'
  -- Discharge the top-gap fast-band-mass envelope.
  have htopgap : ∀ᵐ x ∂μ, TopGapMassEnvelope A T lam0 x :=
    topGapMassEnvelope_ae hT hA hAmeas hint hint' lam0 hlam0
  -- The limit eigenbasis and its eigenpair / slow-orthogonality data.
  set b' : X → OrthonormalBasis (Fin d) ℝ (EuclideanSpace ℝ (Fin d)) :=
    fun x => limitEigenbasis A T x with hb'def
  have hb' : ∀ᵐ x ∂μ, ∀ e : Fin d,
      Matrix.toEuclideanLin (lambdaHat A T x) (b' x e)
        = Real.exp (lamSing A T x (e : ℕ)) • b' x e :=
    limitEigenbasis_eigenpair_exp hT hA hAmeas hint hint'
  have hslowperp : ∀ᵐ x ∂μ, ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, ∀ e : Fin d,
      t < lam0 (e : ℕ) → inner ℝ (b' x e) v = 0 :=
    inner_limitEigenbasis_eq_zero_of_slow hT hA hAmeas hint hint' lam0 hlam0
  -- The spectral-identification band-projector datum.
  have hident : ∀ᵐ x ∂μ, ∀ c : ℝ, 0 < c →
      (∀ i : Fin d, Real.exp (lamSing A T x (i : ℕ)) ≠ c) →
      Filter.Tendsto (fun n : ℕ => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
        Filter.atTop (𝓝 (cfc (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ)) (lambdaHat A T x))) :=
    ae_tendsto_bandProjector_cfc_indicator hT hA hAmeas hint hint'
  -- The forward graded overlap bound, consuming the top-gap envelope.
  have hfwdN :=
    forward_graded_overlap_of_topGapEnvelope hT hA hAmeas hint hint' lam0 hlam0 b' hb' hident
      htopgap
  -- The reverse cofactor bound for orthogonal matrices, after Ruelle.
  have hrev : ∀ (S : Matrix (Fin d) (Fin d) ℝ), S * Sᵀ = 1 →
      ∀ (g : Fin d → ℝ) (c : ℝ), 1 ≤ c →
      (∀ a b : Fin d, |S a b| ≤ c * Real.exp (-(max (g b - g a) 0))) →
      ∀ i j : Fin d, |S i j| ≤ (d - 1).factorial * c ^ (d - 1) * Real.exp (-(g i - g j)) :=
    fun S hS g c hc hf =>
      ErgodicTheory.RuelleCofactor.entry_reverse_bound_of_orthogonal S hS g c hc hf
  -- The band-limit bridge.
  have hbridge := vslow_bridge_bound_of_forward_graded (A := A) lam0 hlam0 b' hslowperp hfwdN hrev
  -- The grading `g x e := lam0 e`.
  set g : X → Fin d → ℝ := fun _ e => lam0 (e : ℕ) with hgdef
  -- The trivial discharge of the forward graded-overlap hypothesis.
  have hfwd : ∀ᵐ x ∂μ, ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, v ≠ 0 →
      ∃ c : ℝ, 1 ≤ c ∧ ∀ᶠ n : ℕ in atTop,
        ∀ a e : Fin d, |(inner ℝ (b' x e)
            (sortedGramEigenbasis A T n x ⟨a, lt_of_lt_of_eq a.2 (Fintype.card_fin d).symm⟩) : ℝ)|
          ≤ c * Real.exp (-(max (g x e - g x a) 0)) := by
    refine Filter.Eventually.of_forall (fun x t v _ _ => ?_)
    set M : ℝ := (Finset.univ.sup' ⟨(default, default), Finset.mem_univ _⟩
      (fun p : Fin d × Fin d => lam0 (p.1 : ℕ) - lam0 (p.2 : ℕ))) ⊔ 0 with hMdef
    have hMnn : (0 : ℝ) ≤ M := le_sup_right
    have hMpair : ∀ a e : Fin d, lam0 (e : ℕ) - lam0 (a : ℕ) ≤ M := by
      intro a e
      refine le_trans ?_ le_sup_left
      exact Finset.le_sup' (fun p : Fin d × Fin d => lam0 (p.1 : ℕ) - lam0 (p.2 : ℕ))
        (Finset.mem_univ (e, a))
    refine ⟨Real.exp M, Real.one_le_exp hMnn, Filter.Eventually.of_forall (fun n a e => ?_)⟩
    have hCS : |(inner ℝ (b' x e)
        (sortedGramEigenbasis A T n x ⟨a, lt_of_lt_of_eq a.2 (Fintype.card_fin d).symm⟩) : ℝ)|
        ≤ 1 := by
      have hb1 : ‖b' x e‖ = 1 := (b' x).orthonormal.1 e
      have hb2 : ‖sortedGramEigenbasis A T n x
          ⟨a, lt_of_lt_of_eq a.2 (Fintype.card_fin d).symm⟩‖ = 1 :=
        (sortedGramEigenbasis A T n x).orthonormal.1 _
      have hcs := abs_real_inner_le_norm (b' x e)
        (sortedGramEigenbasis A T n x ⟨a, lt_of_lt_of_eq a.2 (Fintype.card_fin d).symm⟩)
      rwa [hb1, hb2, mul_one] at hcs
    refine hCS.trans ?_
    rw [← Real.exp_add, ← Real.exp_zero]
    apply Real.exp_le_exp.mpr
    have hmle : max (g x e - g x a) 0 ≤ M := by
      rw [hgdef]
      exact max_le (hMpair a e) hMnn
    linarith
  -- The per-vector spectral upper bound on the limit slow space.
  have hupper := limsup_le_of_mem_vslow hT hTmeas hA hAmeas hint hint' hrev
    lam0 hlam0 b' g hfwd hbridge
  -- The reverse slow-flag inclusion and the slow flag identification.
  have hslowrev : ∀ᵐ x ∂μ, ∀ t : ℝ, lambdaSublevel A T x t ≤ vslow A T (Real.exp t) x :=
    ae_lambdaSublevel_le_vslow hT hA hAmeas hint hint'
  have hslowflag : ∀ᵐ x ∂μ, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t :=
    vslow_eq_lambdaSublevel_of_upper hT hA hAmeas hint hint' hupper hslowrev
  -- The spectrum-identification residuals and the `hspec` interface.
  have hub_spec : ∀ᵐ x ∂μ, lyapunovSpectrum A T x ⊆ distinctExp lam0 d :=
    lyapunovSpectrum_subset_distinctExp_of_slowflag hT hA hAmeas hint hint' hslowflag lam0 hlam0
  have hlb_spec : ∀ᵐ x ∂μ, distinctExp lam0 d ⊆ lyapunovSpectrum A T x :=
    distinctExp_subset_lyapunovSpectrum_of_slowflag hT hA hAmeas hint hint' hslowflag lam0 hlam0
  have hspec :=
    specList_eq_expEnum_of_subsets_standing hT A hA hAmeas hint hint' lam0 hub_spec hlb_spec
  -- The per-vector exact-growth interface.
  have hbdd :=
    isBoundedUnder_inv_mul_log_norm_cocycle_apply_of_mem_stratum hT A hA hAmeas hint hint'
  have hub := limsup_log_norm_cocycle_apply_le_specList_of_mem_stratum hT hA hAmeas hint hint'
  have hlb :=
    specList_le_liminf_inv_mul_log_norm_cocycle_apply_of_slowflag hT hA hAmeas hint hint' hident
      hslowflag
  have hgrowth := tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower A hub hlb hbdd
  -- The structural a.e. block on `vassembled` and its transport through `hae`.
  have hstruct := vassembled_structure_ae hT A hA hAmeas hint hint' lam0 hspec hgrowth
  have hae := vprime_eq_vassembled_of_slowflag A lam0 hspec hslowflag
  have haeT := hT.toMeasurePreserving.quasiMeasurePreserving.ae hae
  -- The a.e. forward dimension formula (`ae_finrank_vslow`).
  have hdims := ae_finrank_vslow hT hA hAmeas hint hint' lam0 hlam0
  -- Assemble the strong export with the concrete witness `V := vprime A T lam0`.
  refine ⟨lam0, hmono, hlam0, vprime A T lam0,
    measurableSubspace_vprime A T hAmeas hTmeas lam0, ?_⟩
  filter_upwards [hstruct, hae, haeT, hdims] with x hsx haex haeTx hdimx
  obtain ⟨h0, hlast, hstrict, hmap, hgrow⟩ := hsx
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [haex 0]; exact h0
  · rw [haex (Fin.last (numExp lam0 d))]; exact hlast
  · intro i; rw [haex i.succ, haex i.castSucc]; exact hstrict i
  · intro i; rw [haex i, haeTx i]; exact hmap i
  · intro i v hv hvnot
    rw [haex i.castSucc] at hv
    rw [haex i.succ] at hvnot
    exact hgrow i v hv hvnot
  · -- The dimension clause: on the interior, `vprime i.castSucc` is `vslow` at `expEnum lam0 d i`.
    intro i
    have hVeq : vprime A T lam0 i.castSucc x
        = vslow A T (Real.exp (expEnum lam0 d i)) x := by
      have hlt : (i.castSucc : ℕ) < numExp lam0 d := by
        simp only [Fin.val_castSucc]; exact i.isLt
      have hcut : slowCutoff lam0 d i.castSucc = expEnum lam0 d i := by
        rw [slowCutoff, dif_pos hlt]
        exact congrArg (expEnum lam0 d) (Fin.ext (by simp))
      unfold vprime
      rw [if_pos hlt, hcut]
    rw [hVeq, hdimx (expEnum lam0 d i)]

end ErgodicTheory
