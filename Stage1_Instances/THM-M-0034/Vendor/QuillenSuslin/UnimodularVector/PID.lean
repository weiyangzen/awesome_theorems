/-
Copyright (c) 2026 Yongle Hu. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yongle Hu
-/
/- Port notice: modified for the repository's pinned Lean 4.29/mathlib APIs.
The exact compatibility edits are recorded in `../../../PORT_PROVENANCE.md`. -/
import Mathlib.LinearAlgebra.FreeModule.PID
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.UnimodularVector.Basic
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.UnimodularVector.SuslinMonicPolynomialThm

open Module Polynomial Finset BigOperators Bivariate

variable {R : Type*} [CommRing R] [IsDomain R] {s : Type*} [Fintype s] [DecidableEq s]

/-- Over a principal ideal domain, any two unimodular vectors are equivalent. -/
theorem unimodularVectorEquiv_of_pid [IsPrincipalIdealRing R]
    {v w : s → R} (hv : IsUnimodular v) (hw : IsUnimodular w) : UnimodularVectorEquiv v w := by
  have buildBasis {u : s → R} (hu : IsUnimodular u) : Σ n : ℕ,
      { b : Basis (Sum (Fin 1) (Fin n)) R (s → R) // b (Sum.inl 0) = u } := by
    have h1 : (1 : R) ∈ Ideal.span (Set.range u) := by
      rw [hu]
      exact Submodule.mem_top
    have hex : ∃ c : s → R, (∑ i, c i * u i) = 1 := Ideal.mem_span_range_iff_exists_fun.1 h1
    let c : s → R := Classical.choose hex
    have hc : (∑ i, c i * u i) = 1 := Classical.choose_spec hex
    let φ : (s → R) →ₗ[R] R :=
      { toFun := fun x => ∑ i, c i * x i
        map_add' _ _ := by
          simp [mul_add, Finset.sum_add_distrib]
        map_smul' _ _ := by
          simp [Pi.smul_apply, smul_eq_mul, Finset.mul_sum, mul_assoc, mul_comm] }
    let f : R →ₗ[R] (s → R) :=
      { toFun := fun r => r • u
        map_add' _ _ := by
          simp [add_smul]
        map_smul' _ _ := by
          simp [mul_smul] }
    have hφf : ∀ r : R, φ (f r) = r := by
      intro r
      calc _ = r * (∑ i : s, c i * u i) := by simp [φ, f, smul_eq_mul, mul_comm, Finset.mul_sum]
        _ = r := by simp [hc]
    have hf_inj : Function.Injective f := by
      intro a b hab
      simpa [hφf a, hφf b] using congrArg φ hab
    let p : Submodule R (s → R) := LinearMap.range f
    let proj : (s → R) →ₗ[R] p :=
      { toFun := fun x => ⟨f (φ x), ⟨φ x, rfl⟩⟩
        map_add' _ _ := by
          ext
          simp
        map_smul' _ _ := by
          ext
          simp [f, Pi.smul_apply, smul_eq_mul, mul_assoc] }
    have hproj : ∀ x : p, proj x = x := by
      rintro ⟨x, ⟨r, rfl⟩⟩
      ext
      simp [proj, hφf r]
    have bqSigma : Σ n : ℕ, Basis (Fin n) R (LinearMap.ker proj) :=
      Submodule.basisOfPid (Pi.basisFun R s) (LinearMap.ker proj)
    refine ⟨bqSigma.1, ?_⟩
    let eP : R ≃ₗ[R] p := LinearEquiv.ofInjective f hf_inj
    let bp : Basis (Fin 1) R p := (Basis.singleton (Fin 1) R).map eP
    let eSum : (p × LinearMap.ker proj) ≃ₗ[R] (s → R) :=
      Submodule.prodEquivOfIsCompl p _ <| LinearMap.isCompl_of_proj hproj
    let bM : Basis (Sum (Fin 1) (Fin bqSigma.1)) R (s → R) :=
      (bp.prod bqSigma.2).map eSum
    refine ⟨bM, ?_⟩
    have : (bp (0 : Fin 1) : (s → R)) = u := by
      -- `bp 0 = eP 1` and `eP 1` corresponds to `f 1 = u`.
      ext i
      -- First reduce `bp 0` to `eP 1`.
      simp [bp, Basis.map_apply, Basis.singleton_apply]
      -- Now unfold `eP` via `LinearEquiv.ofInjective_apply`.
      have he : ((eP (1 : R)) : s → R) = f 1 := by
        simpa [eP] using
          (LinearEquiv.ofInjective_apply (f : R →ₗ[R] s → R) (1 : R))
      -- Finally, compute `f 1`.
      simp [he, f, Pi.smul_apply, smul_eq_mul]
    simp [bM, eSum, this]
  rcases buildBasis hv with ⟨nv, ⟨bv, hbv⟩⟩
  rcases buildBasis hw with ⟨nw, ⟨bw, hbw⟩⟩
  -- Change basis: send the basis containing `v` to the basis containing `w`.
  let σ : (Sum (Fin 1) (Fin nv)) ≃ (Sum (Fin 1) (Fin nw)) := bv.indexEquiv bw
  let j : Sum (Fin 1) (Fin nw) := σ (Sum.inl 0)
  let τ : (Sum (Fin 1) (Fin nw)) ≃ (Sum (Fin 1) (Fin nw)) := Equiv.swap (Sum.inl 0) j
  let bw' : Basis (Sum (Fin 1) (Fin nw)) R (s → R) := bw.reindex τ
  let eLin : (s → R) ≃ₗ[R] (s → R) :=
    (bv.repr.trans (Finsupp.domLCongr σ)).trans bw'.repr.symm
  have heLin : eLin v = w := by
    -- `eLin` sends `bv i` to `bw' (σ i)`, and `bw' (σ (Sum.inl 0)) = w` by construction.
    have : bw' (σ (Sum.inl 0)) = w := by simpa [j] using (by simp [bw', τ, j, hbw])
    rw [← hbv]
    simp [eLin, this]
  -- Convert the linear equivalence to a matrix in `GL` and conclude.
  let g : LinearMap.GeneralLinearGroup R (s → R) := LinearMap.GeneralLinearGroup.ofLinearEquiv eLin
  let A : Matrix.GeneralLinearGroup s R := (Matrix.GeneralLinearGroup.toLin).symm g
  refine ⟨(Matrix.GeneralLinearGroup.toLin).symm g, ?_⟩
  have htoLin : Matrix.GeneralLinearGroup.toLin A = g := by
    simp [A]
  have hlin : ((Matrix.GeneralLinearGroup.toLin A : (s → R) →ₗ[R] (s → R)) v) = w := by
    simp [htoLin, g, heLin]
  simpa [Matrix.mulVecLin_apply] using (by simpa [Matrix.GeneralLinearGroup.coe_toLin] using hlin)

section thm12

theorem unimodularVectorEquiv_update_add_ring {A : Type*} [CommRing A] (i j : s) (hij : i ≠ j)
    (c : A) (v : s → A) : UnimodularVectorEquiv v (Function.update v i (v i + c * v j)) := by
  let M : Matrix s s A := Matrix.transvection i j c
  have hdet : IsUnit (Matrix.det M) := by
    have : Matrix.det M = 1 := by simpa [M] using Matrix.det_transvection_of_ne i j hij c
    simp [this]
  refine ⟨Matrix.GeneralLinearGroup.mk'' M hdet, ?_⟩
  ext k
  by_cases hk : k = i
  · subst hk
    simp [M, Matrix.transvection, Matrix.mulVec, dotProduct, Matrix.one_apply, Matrix.single_apply,
      Function.update, Finset.sum_add_distrib, add_mul]
  · simp [M, Matrix.transvection, Matrix.mulVec, dotProduct, Function.update, hk, Ne.symm hk,
      Matrix.one_apply]

theorem unimodularVectorEquiv_update_add_sum {A : Type*} [CommRing A] (i : s) (t : Finset s)
    (ht : i ∉ t) (c : s → A) (v : s → A) :
    UnimodularVectorEquiv v (Function.update v i (v i + ∑ j ∈ t, c j * v j)) := by
  let vOf : Finset s → s → A := fun t => Function.update v i (v i + ∑ j ∈ t, c j * v j)
  have hvOf : ∀ t : Finset s, i ∉ t → UnimodularVectorEquiv v (vOf t) := by
    intro t
    refine Finset.induction_on t ?_ ?_
    · intro _
      have h0 : vOf (∅ : Finset s) = v := by
        funext j
        by_cases hj : j = i
        · subst hj
          simp [vOf]
        · simp [vOf, hj]
      simpa [h0] using unimodularVectorEquiv_equivalence.1 v
    · intro j t hj_notmem ih ht
      have ht' : i ∉ t := by
        intro hi
        exact ht (Finset.mem_insert_of_mem hi)
      have hij : j ≠ i := by
        intro hji
        have : i ∈ insert j t := by
          subst j
          exact Finset.mem_insert_self i t
        exact ht this
      have ih' : UnimodularVectorEquiv v (vOf t) := ih ht'
      have hadd : UnimodularVectorEquiv (vOf t)
          (Function.update (vOf t) i ((vOf t) i + c j * (vOf t) j)) := by
        simpa using unimodularVectorEquiv_update_add_ring i j (Ne.symm hij) (c j) (vOf t)
      have hstep : Function.update (vOf t) i ((vOf t) i + c j * (vOf t) j) =
          vOf (insert j t) := by
        funext x
        by_cases hx : x = i
        · subst hx
          have hvj : (vOf t) j = v j := by simp [vOf, hij]
          simp [vOf, Function.update, hvj, Finset.sum_insert, hj_notmem, add_left_comm, add_comm]
        · simp [vOf, Function.update, hx]
      exact unimodularVectorEquiv_equivalence.trans ih' (by simpa [hstep] using hadd)
  simpa [vOf] using hvOf t ht

lemma Ideal.height_add_one_le_of_forall_notMem_minimalPrimes {A : Type*} [CommRing A] {I : Ideal A}
    (a : A) {k : ℕ∞} (hk : k ≤ I.height) (ha : ∀ p ∈ I.minimalPrimes, a ∉ p) :
    k + 1 ≤ (I ⊔ Ideal.span ({a} : Set A)).height := by
  refine le_iInf₂ ?_
  intro P hP
  have : P.IsPrime := Ideal.minimalPrimes_isPrime hP
  have hIP : I ≤ P := le_trans le_sup_left hP.1.2
  rcases Ideal.exists_minimalPrimes_le hIP with ⟨q, hq, hq_le_P⟩
  have : q.IsPrime := Ideal.minimalPrimes_isPrime hq
  have haq : a ∉ q := ha q hq
  have hI_le_q : I.height ≤ q.primeHeight := by simpa [Ideal.height] using iInf₂_le q hq
  have hkq : k ≤ q.primeHeight := le_trans hk hI_le_q
  have haP : a ∈ P :=  (le_trans le_sup_right hP.1.2) (Ideal.subset_span (by simp))
  have hq_ne_P : q ≠ P := by
    intro h
    subst h
    exact haq haP
  have hq_lt_P : q < P := lt_of_le_of_ne hq_le_P hq_ne_P
  have hqp : q.primeHeight + 1 ≤ P.primeHeight := Ideal.primeHeight_add_one_le_of_lt hq_lt_P
  exact le_trans (add_le_add_left hkq 1) hqp

theorem exists_equiv_exists_index_height_gt_krullDim (n : ℕ) [IsNoetherianRing R]
    (v : s → MvPolynomial (Fin (n + 1)) R) (hv : IsUnimodular v)
    (hs : ringKrullDim R + 1 < (Fintype.card s : WithBot ℕ∞)) :
    ∃ o : s, ∃ v' : s → MvPolynomial (Fin (n + 1)) R, UnimodularVectorEquiv v v' ∧
      ringKrullDim R < (Ideal.span (Set.range (fun i => if i = o then 0 else v' i))).height := by
  let A := MvPolynomial (Fin (n + 1)) R
  have hr_ne_bot : ringKrullDim R ≠ (⊥ : WithBot ℕ∞) := by
    exact Order.krullDim_ne_bot_iff.2 ⟨⟨⊥, Ideal.isPrime_bot⟩⟩
  have hs_pos : 0 < Fintype.card s := by
    by_contra h0
    have hs0 : ringKrullDim R + 1 < (0 : WithBot ℕ∞) := by
      simpa [Nat.eq_zero_of_not_pos h0] using hs
    have hs0' : ringKrullDim R + 1 < ((⊥ : ℕ∞) : WithBot ℕ∞) := by
      simpa only [bot_eq_zero', WithBot.coe_zero] using hs0
    have hbot : ringKrullDim R + 1 = (⊥ : WithBot ℕ∞) := (WithBot.lt_coe_bot).1 hs0'
    have hr_bot : ringKrullDim R = (⊥ : WithBot ℕ∞) := by
      cases h : ringKrullDim R <;> simp [h] at hbot ⊢
    exact hr_ne_bot hr_bot
  have hs_nonempty : Nonempty s := (Fintype.card_pos_iff).1 hs_pos
  let o : s := Classical.choice hs_nonempty
  let t : Finset s := Finset.univ.erase o
  -- For a finite subset `S ⊆ t`, let `I(S)` be the ideal generated by the coordinates in `S`.
  let Iof (S : Finset s) (w : s → A) : Ideal A :=
    Ideal.span (Set.range fun j : s => if j ∈ S then w j else 0)
  have hbuild : ∀ S : Finset s, S ⊆ t →
      ∃ w : s → A, UnimodularVectorEquiv v w ∧ (S.card : ℕ∞) ≤ (Iof S w).height := by
    intro S
    refine Finset.induction_on S ?_ ?_
    · intro _
      refine ⟨v, unimodularVectorEquiv_equivalence.1 v, ?_⟩
      have hbot : Iof (∅ : Finset s) v = (⊥ : Ideal A) := by
        ext x
        simp [Iof]
      simp [hbot]
    · intro i S hi_notmem ih hsub
      have hsubS : S ⊆ t := by
        intro x hx
        exact hsub (Finset.mem_insert_of_mem hx)
      have hi_t : i ∈ t := hsub (Finset.mem_insert_self i S)
      rcases ih hsubS with ⟨w, hvw, hheight⟩
      have hw_unimod : IsUnimodular w :=
        (isUnimodular_iff_of_unimodularVectorEquiv_ring hvw).1 hv
      let I : Ideal A := Iof S w
      let J : Ideal A :=
        Ideal.span (Set.range fun j : s => if j ∈ insert i S then 0 else w j)
      have hfin : I.minimalPrimes.Finite :=
        Ideal.finite_minimalPrimes_of_isNoetherianRing A I
      let P : Finset (Ideal A) := hfin.toFinset
      have hmemP (p : Ideal A) : p ∈ P ↔ p ∈ I.minimalPrimes := Set.Finite.mem_toFinset hfin
      -- First choose `y ∈ J` so that `w i + y` avoids all minimal primes of `I`.
      have havoidP : ∃ y : A, y ∈ J ∧ ∀ p ∈ P, w i + y ∉ p := by
        classical
        let motive (Q : Finset (Ideal A)) : Prop :=
          Q ⊆ P → ∃ y : A, y ∈ J ∧ ∀ q ∈ Q, w i + y ∉ q
        have h0 : motive ∅ := by
          intro _
          refine ⟨0, by simp, ?_⟩
          intro q hq
          cases hq
        have hstep : ∀ (p : Ideal A) (Q : Finset (Ideal A)), p ∉ Q → motive Q →
            motive (insert p Q) := by
          intro p Q hp_notmemQ hQ hsubPQ
          have hpP : p ∈ P := hsubPQ (Finset.mem_insert_self p Q)
          have hQsub : Q ⊆ P := by
            intro q hq
            exact hsubPQ (Finset.mem_insert_of_mem hq)
          rcases hQ hQsub with ⟨y, hyJ, hyavoid⟩
          by_cases hpy : w i + y ∈ p
          · -- We need to modify `y` by adding an element `y' ∈ J` that lies in every `q ∈ Q`
            -- but not in `p`.
            have hpI : p ∈ I.minimalPrimes := (hmemP p).1 hpP
            have : p.IsPrime := Ideal.minimalPrimes_isPrime hpI
            have hIp : I ≤ p := hpI.1.2
            have hJnot : ¬ J ≤ p := by
              intro hJle
              have hyP : y ∈ p := hJle hyJ
              have hwiP : w i ∈ p := by
                have : (w i + y) - y = w i := add_sub_cancel_right (w i) y
                simpa [this] using p.sub_mem hpy hyP
              -- Then all coordinates of `w` lie in `p`, contradicting unimodularity.
              have hall : ∀ j : s, w j ∈ p := by
                intro j
                by_cases hjS : j ∈ S
                · -- `w j ∈ I ≤ p`.
                  exact hIp <| Ideal.subset_span ⟨j, by simp [hjS]⟩
                · by_cases hji : j = i
                  · subst hji
                    exact hwiP
                  · -- Otherwise `j ∉ insert i S`, hence `w j ∈ J ≤ p`.
                    have hjJ : w j ∈ J := by
                      refine Ideal.subset_span ⟨j, ?_⟩
                      have : j ∉ insert i S := by simp [hjS, hji]
                      simp [this]
                    exact hJle hjJ
              have hspan : Ideal.span (Set.range w) ≤ p := by
                refine Ideal.span_le.2 ?_
                rintro _ ⟨j, rfl⟩
                exact hall j
              have htop : (⊤ : Ideal A) ≤ p := le_trans (le_of_eq hw_unimod.symm) hspan
              exact (Ideal.IsPrime.ne_top ‹p.IsPrime›) (top_le_iff.1 htop)
            rcases (Set.not_subset.1 hJnot) with ⟨z, hzJ, hznot⟩
            have hsel : ∀ q ∈ Q, ∃ x : A, x ∈ q ∧ x ∉ p := by
              intro q hqQ
              have hqP : q ∈ P := hQsub hqQ
              have hqI : q ∈ I.minimalPrimes := (hmemP q).1 hqP
              have hq_ne_p : q ≠ p := by
                intro hqp
                subst hqp
                exact hp_notmemQ hqQ
              have hq_notle : ¬ q ≤ p := by
                intro hle
                exact hq_ne_p (le_antisymm hle (hpI.2 hqI.1 hle))
              rcases (Set.not_subset.1 hq_notle) with ⟨x, hxq, hxnp⟩
              exact ⟨x, hxq, hxnp⟩
            let x : Ideal A → A := fun q => if h : q ∈ Q then Classical.choose (hsel q h) else 1
            have hxmem : ∀ q ∈ Q, x q ∈ q := by
              intro q hqQ
              simpa [x, hqQ] using (Classical.choose_spec (hsel q hqQ)).1
            have hxnot : ∀ q ∈ Q, x q ∉ p := by
              intro q hqQ
              simpa [x, hqQ] using (Classical.choose_spec (hsel q hqQ)).2
            let t0 : A := ∏ q ∈ Q, x q
            have htQ : ∀ q ∈ Q, t0 ∈ q := by
              intro q hqQ
              have hmul : (∏ r ∈ Q.erase q, x r) * x q = ∏ r ∈ Q, x r :=
                Finset.prod_erase_mul Q x hqQ
              simpa [t0, hmul] using Ideal.mul_mem_left q (∏ r ∈ Q.erase q, x r) (hxmem q hqQ)
            have ht0np : t0 ∉ p := by
              intro ht0p
              rcases Ideal.IsPrime.prod_mem_iff.1 ht0p with ⟨q, hqQ, hxqp⟩
              exact (hxnot q hqQ) hxqp
            let y' : A := t0 * z
            have hy'J : y' ∈ J := Ideal.mul_mem_left J t0 hzJ
            have hy'Q : ∀ q ∈ Q, y' ∈ q := by
              intro q hq
              have htq : t0 ∈ q := htQ q hq
              simpa [y', mul_comm] using Ideal.mul_mem_left q z htq
            have hy'not : y' ∉ p := by
              intro hy'p
              have : t0 ∈ p ∨ z ∈ p := (show p.IsPrime from ‹p.IsPrime›).mem_or_mem hy'p
              cases this with
              | inl ht0p => exact ht0np ht0p
              | inr hzp => exact hznot hzp
            let yNew : A := y + y'
            refine ⟨yNew, J.add_mem hyJ hy'J, ?_⟩
            intro q hq
            rcases Finset.mem_insert.1 hq with hq | hq
            · subst q
              intro hpNew
              have : y' ∈ p := by
                have hy'_eq : (w i + (y + y')) - (w i + y) = y' := by
                  calc _ = (w i + y + y') - (w i + y) := by simp [add_assoc]
                    _ = y' := add_sub_cancel_left (w i + y) y'
                have hsub' : (w i + (y + y')) - (w i + y) ∈ p := p.sub_mem hpNew hpy
                exact hy'_eq ▸ hsub'
              exact hy'not this
            · have hyq : w i + y ∉ q := hyavoid q hq
              have hy'q : y' ∈ q := hy'Q q hq
              intro hsum
              have : w i + y ∈ q := by
                have : w i + y = (w i + (y + y')) - y' := by
                  simp [sub_eq_add_neg, add_assoc, add_left_comm, add_comm]
                have hsub' : (w i + (y + y')) - y' ∈ q := q.sub_mem hsum hy'q
                simpa [this] using hsub'
              exact hyq this
          · -- No modification needed, `y` already avoids `p`.
            refine ⟨y, hyJ, ?_⟩
            intro q hq
            rcases Finset.mem_insert.1 hq with hq | hq
            · subst hq
              exact hpy
            · exact hyavoid q hq
        have hmot : motive P := Finset.induction_on P h0 hstep
        simpa using hmot subset_rfl
      rcases havoidP with ⟨y, hyJ, hyavoidP⟩
      have hyavoid : ∀ p ∈ I.minimalPrimes, w i + y ∉ p := by
        intro p hpI
        exact hyavoidP p ((hmemP p).2 hpI)
      rcases (Ideal.mem_span_range_iff_exists_fun).1 hyJ with ⟨c, hc⟩
      let U : Finset s := Finset.univ.filter fun j : s => j ∉ insert i S
      have hiU : i ∉ U := by simp [U]
      have hy_sum : ∑ j ∈ U, c j * w j = y := by
        have hc0 : (∑ j : s, c j * (if j ∈ insert i S then (0 : A) else w j)) = y := by
          simpa [J] using hc
        have hc1 : (∑ j : s, if j ∉ insert i S then c j * w j else 0) = y := by
          have hterm : (∑ j : s, c j * (if j ∈ insert i S then (0 : A) else w j)) =
              ∑ j : s, if j ∉ insert i S then c j * w j else 0 := by
            refine Fintype.sum_congr _ _ ?_
            intro j
            by_cases hj : j ∈ insert i S
            · simp [hj]
            · simp [hj]
          exact hterm ▸ hc0
        have hc2 : (∑ j ∈ Finset.univ, if j ∉ insert i S then c j * w j else 0) = y := by
          simpa using hc1
        have hfilter :
            (∑ j ∈ Finset.univ, if j ∉ insert i S then c j * w j else 0) = ∑ j ∈ U, c j * w j := by
          simpa [U] using
            (Finset.sum_filter (fun j : s => j ∉ insert i S) (fun j : s => c j * w j)).symm
        exact hfilter.symm.trans hc2
      let w1 : s → A := Function.update w i (w i + y)
      have hww1 : UnimodularVectorEquiv w w1 := by
        simpa [w1, hy_sum] using unimodularVectorEquiv_update_add_sum i U hiU c w
      have hI_same : Iof S w1 = I := by
        have hw1_eq : ∀ j : s, j ∈ S → w1 j = w j := by
          intro j hj
          have hji : j ≠ i := by
            intro h
            subst h
            exact hi_notmem hj
          simp [w1, hji]
        have hfun : (fun j : s => if j ∈ S then w1 j else 0) =
            (fun j : s => if j ∈ S then w j else 0) := by
          funext j
          by_cases hj : j ∈ S
          · simp [hj, hw1_eq j hj]
          · simp [hj]
        simp [Iof, I, hfun]
      have hheight' : (S.card : ℕ∞) ≤ (Iof S w1).height := by simpa [hI_same] using hheight
      have hstep_height : (S.card : ℕ∞) + 1 ≤ (I ⊔ Ideal.span ({w1 i} : Set A)).height := by
        refine I.height_add_one_le_of_forall_notMem_minimalPrimes (w1 i) ?_ ?_
        · simpa [hI_same] using hheight'
        · intro p hp
          have : w1 i = w i + y := by simp [w1]
          simpa [this] using hyavoid p hp
      have hsup : (I ⊔ Ideal.span ({w1 i} : Set A)) ≤ Iof (insert i S) w1 := by
        refine sup_le ?_ ?_
        · refine (Ideal.span_le).2 ?_
          rintro _ ⟨j, rfl⟩
          by_cases hj : j ∈ S
          · have hji : j ≠ i := by
              intro h
              subst h
              exact hi_notmem hj
            have hw1j : w1 j = w j := by simp [w1, hji]
            exact Ideal.subset_span ⟨j, by simp [Finset.mem_insert_of_mem hj, hj, hw1j]⟩
          · simp [Iof, hj]
        · refine Ideal.span_le.2 ?_
          intro x hx
          subst hx
          exact Ideal.subset_span ⟨i, by simp [w1]⟩
      have hheight_insert : ((insert i S).card : ℕ∞) ≤ (Iof (insert i S) w1).height := by
        have : ((insert i S).card : ℕ∞) = (S.card : ℕ∞) + 1 := by
          exact_mod_cast by simpa using (Finset.card_insert_of_notMem hi_notmem)
        simpa only [this, ge_iff_le] using le_trans hstep_height (Ideal.height_mono hsup)
      refine ⟨w1, unimodularVectorEquiv_equivalence.trans hvw hww1, ?_⟩
      simpa [hI_same] using hheight_insert
  rcases hbuild t (subset_rfl) with ⟨v', hvv', htheight⟩
  have hideal : Iof t v' = Ideal.span (Set.range fun j : s => if j = o then 0 else v' j) := by
    ext x
    simp [Iof, t]
  have htcard : (t.card : ℕ) + 1 = Fintype.card s := by
    simpa [t] using Finset.card_erase_add_one  (Finset.mem_univ o)
  have hdim_lt_t : ringKrullDim R < (↑(t.card) : WithBot ℕ∞) := by
    have hs' : ringKrullDim R + 1 < (↑(t.card + 1) : WithBot ℕ∞) := by
      simpa [htcard] using hs
    exact lt_of_add_lt_add_right hs'
  have htheight' : (t.card : WithBot ℕ∞) ≤ (Iof t v').height := by exact_mod_cast htheight
  exact ⟨o, v', hvv', by simpa [hideal] using lt_of_lt_of_le hdim_lt_t htheight'⟩

variable [IsPrincipalIdealRing R]

theorem exists_algEquiv_exists_equiv_exists_monic_finSuccEquiv (n : ℕ)
    (v : s → MvPolynomial (Fin (n + 1)) R) (hv : IsUnimodular v) :
    ∃ e : MvPolynomial (Fin (n + 1)) R ≃ₐ[R] MvPolynomial (Fin (n + 1)) R,
      ∃ w : s → MvPolynomial (Fin (n + 1)) R,
        UnimodularVectorEquiv (fun i : s => e (v i)) w ∧
          ∃ i : s, (MvPolynomial.finSuccEquiv R n (w i)).Monic := by
  cases hcard : Fintype.card s with
  | zero =>
    have : IsEmpty s := (Fintype.card_eq_zero_iff).1 hcard
    have hbot : (⊥ : Ideal (MvPolynomial (Fin (n + 1)) R)) = ⊤ := by
      simp [IsUnimodular, Set.range_eq_empty] at hv
    exact False.elim (bot_ne_top hbot)
  | succ m =>
    cases m with
    | zero =>
      have h1 : Fintype.card s = 1 := by simp [hcard]
      rcases (Fintype.card_eq_one_iff).1 h1 with ⟨o, ho⟩
      have hrange : Set.range v = {v o} := by
        ext x
        constructor
        · rintro ⟨i, rfl⟩
          simp [ho i]
        · intro hx
          rcases hx with rfl
          exact ⟨o, rfl⟩
      have hunit : IsUnit (v o) :=
        (Ideal.span_singleton_eq_top).1 (by simpa [IsUnimodular, hrange] using hv)
      rcases hunit with ⟨u, hu⟩
      let w : s → MvPolynomial (Fin (n + 1)) R := fun _ => 1
      let d : s → MvPolynomial (Fin (n + 1)) R := fun j => if j = o then u⁻¹.1 else 1
      let D : Matrix s s (MvPolynomial (Fin (n + 1)) R) := Matrix.diagonal d
      have hdet : IsUnit (Matrix.det D) := by
        -- With `card s = 1`, `det (diagonal d) = d o = u⁻¹`.
        have : Matrix.det D = u⁻¹ := by
          simp [D, d, Matrix.det_diagonal, ho, Finset.prod_const, Finset.card_univ, h1]
        rw [this]
        exact Units.isUnit u⁻¹
      refine ⟨AlgEquiv.refl, w, ?_, ⟨o, by simp [w]⟩⟩
      refine ⟨Matrix.GeneralLinearGroup.mk'' D hdet, ?_⟩
      funext j
      have hj : j = o := ho j
      subst hj
      have hvu : v j = (u : MvPolynomial (Fin (n + 1)) R) := by simpa using hu.symm
      simp [w, D, d, Matrix.mulVec_diagonal, hvu]
    | succ m =>
      cases m with
      | zero =>
        have h2 : Fintype.card s = 2 := by simp [hcard]
        let eσ : s ≃ Fin 2 := Fintype.equivFinOfCardEq h2
        let a : s := eσ.symm 0
        let b : s := eσ.symm 1
        have h1 : 1 ∈ Ideal.span (Set.range v) := by
          unfold IsUnimodular at hv
          simp [hv]
        rcases (Ideal.mem_span_range_iff_exists_fun).1 h1 with ⟨c, hc⟩
        have hc2 : c a * v a + c b * v b = 1 := by
          have hsum : (∑ i : s, c i * v i) = ∑ j : Fin 2, c (eσ.symm j) * v (eσ.symm j) := by
            simpa only [Fin.sum_univ_two, Fin.isValue] using
              Fintype.sum_equiv eσ (fun i : s => c i * v i)
                (fun j : Fin 2 => c (eσ.symm j) * v (eσ.symm j)) (fun _ => by simp)
          have : ∑ j : Fin 2, c (eσ.symm j) * v (eσ.symm j) = 1 := by
            simpa only [Fin.sum_univ_two, Fin.isValue, hsum] using hc
          simpa only [Fin.isValue, Fin.sum_univ_two] using this
        let w : s → MvPolynomial (Fin (n + 1)) R := fun i => if i = a then 1 else 0
        let MFin : Matrix (Fin 2) (Fin 2) (MvPolynomial (Fin (n + 1)) R) :=
          ![![c a, c b], ![-v b, v a]]
        let M : Matrix s s (MvPolynomial (Fin (n + 1)) R) := Matrix.reindex eσ.symm eσ.symm MFin
        have hdet : IsUnit (Matrix.det M) := by
          have hdet' : Matrix.det M = 1 := by
            have hre : Matrix.det M = Matrix.det MFin := by simp [M]
            exact hre.trans (by simp [MFin, Matrix.det_fin_two, hc2, sub_eq_add_neg])
          rw [hdet']
          exact isUnit_one
        have hmul : (M.mulVec v) = w := by
          funext i
          have hentry : ∀ x y : s, M x y = MFin (eσ x) (eσ y) := by
            intro x y
            simp [M]
          have hsum : (∑ j : s, M i j * v j) = ∑ j : Fin 2, MFin (eσ i) j * v (eσ.symm j) := by
            simpa only [hentry, Fin.sum_univ_two, Fin.isValue] using
              Fintype.sum_equiv eσ (fun j : s => MFin (eσ i) (eσ j) * v j)
                (fun j : Fin 2 => MFin (eσ i) j * v (eσ.symm j)) (fun _ => by simp)
          cases h : eσ i using Fin.cases with
          | zero =>
            have : i = a := by
              have h' := congrArg eσ.symm h
              simp only [Equiv.symm_apply_apply, Fin.isValue] at h'
              exact h'
            subst this
            have : (∑ j : s, M a j * v j) = 1 := by
              calc _ = ∑ j : Fin 2, MFin (eσ a) j * v (eσ.symm j) := hsum
                _ = ∑ j : Fin 2, MFin 0 j * v (eσ.symm j) := by
                  simp only [h, Fin.isValue, Fin.sum_univ_two]
                _ = c a * v a + c b * v b := by
                  simp only [Fin.isValue, Matrix.cons_val', Matrix.cons_val_fin_one,
                    Matrix.cons_val_zero, Fin.sum_univ_two, Matrix.cons_val_one, MFin, a, b]
                _ = 1 := hc2
            simpa only [Matrix.mulVec, dotProduct, ↓reduceIte, w] using this
          | succ j =>
            fin_cases j
            have : i = b := by
              have h' := congrArg eσ.symm h
              simp only [Equiv.symm_apply_apply] at h'
              exact h'
            subst this
            have : (∑ j : s, M b j * v j) = 0 := by
              calc _ = ∑ j : Fin 2, MFin (eσ b) j * v (eσ.symm j) := hsum
                _ = ∑ j : Fin 2, MFin 1 j * v (eσ.symm j) := by
                  simp only [h, Fin.zero_eta, Fin.isValue, Fin.succ_zero_eq_one, Fin.sum_univ_two]
                _ = (-v b) * v a + v a * v b := by
                  simp only [Fin.isValue, Matrix.cons_val', Matrix.cons_val_fin_one, a, b,
                    Matrix.cons_val_one, Fin.sum_univ_two, Matrix.cons_val_zero, neg_mul, MFin]
                _ = 0 := by simp only [mul_comm, mul_neg, neg_add_cancel]
            have hb : b ≠ a := by
              intro hba
              exact (show (1 : Fin 2) ≠ 0 by decide) <| by
                simpa only [Fin.isValue, one_ne_zero, Equiv.apply_symm_apply, b, a] using
                  congrArg eσ hba
            simp [Matrix.mulVec, dotProduct, w, hb]
            exact this
        refine ⟨AlgEquiv.refl, w, ⟨Matrix.GeneralLinearGroup.mk'' M hdet, by simp [hmul]⟩, ?_⟩
        exact ⟨a, by simp [w]⟩
      | succ m =>
        have hsNat : 2 < Fintype.card s := by
          rw [hcard]
          exact Nat.succ_lt_succ (Nat.succ_lt_succ (Nat.succ_pos m))
        have hs : ringKrullDim R + 1 < (Fintype.card s : WithBot ℕ∞) := by
          have hle' : ringKrullDim R ≤ (1 : WithBot ℕ∞) := by
            simpa [Ring.krullDimLE_iff] using show Ring.KrullDimLE 1 R from inferInstance
          have hle : ringKrullDim R ≤ (1 : WithBot ℕ∞) := by simpa using hle'
          have hle2 : ringKrullDim R + 1 ≤ (2 : WithBot ℕ∞) := by
            have : ringKrullDim R + 1 ≤ (1 : WithBot ℕ∞) + 1 := by
              simpa only [add_comm] using add_le_add_right hle (1 : WithBot ℕ∞)
            simpa only [ge_iff_le, one_add_one_eq_two] using this
          have hsCard : (2 : WithBot ℕ∞) < (Fintype.card s : WithBot ℕ∞) := by
            exact_mod_cast hsNat
          exact lt_of_le_of_lt hle2 hsCard
        rcases exists_equiv_exists_index_height_gt_krullDim n v hv hs with ⟨o, v', hvv', hheight⟩
        let I : Ideal (MvPolynomial (Fin (n + 1)) R) :=
          Ideal.span (Set.range (fun i : s => if i = o then 0 else v' i))
        have hr : ringKrullDim R < (⊤ : WithBot ℕ∞) := by
          have hle : ringKrullDim R ≤ (1 : WithBot ℕ∞) := by
            simpa [Ring.krullDimLE_iff] using show Ring.KrullDimLE 1 R from inferInstance
          have h1lt : (1 : WithBot ℕ∞) < ⊤ := by
            refine (lt_top_iff_ne_top).2 ?_
            intro h
            have h' : (1 : ℕ∞) = (⊤ : ℕ∞) := WithBot.coe_eq_coe.mp (by simpa using h)
            exact WithTop.coe_ne_top h'
          exact lt_of_le_of_lt hle h1lt
        rcases suslin_monic_polynomial_theorem n I (by simpa [I] using hheight) with
          ⟨α, f, hfI, hmonicf⟩
        -- Express `f` as a linear combination of the generators of `I`.
        rcases (Ideal.mem_span_range_iff_exists_fun).1 hfI with ⟨c, hc⟩
        let A := MvPolynomial (Fin n) R
        let instA : CommRing A := inferInstance
        let : CommSemiring A := instA.toCommSemiring
        let φ : MvPolynomial (Fin (n + 1)) R ≃ₐ[R] Polynomial A := MvPolynomial.finSuccEquiv R n
        let φr : MvPolynomial (Fin (n + 1)) R ≃+* Polynomial A := φ.toRingEquiv
        let u : s → MvPolynomial (Fin (n + 1)) R := fun i => α (v' i)
        let uPoly : s → Polynomial A := fun i => φ (u i)
        let fPoly : Polynomial A := φ (α f)
        have hmonic_fPoly : fPoly.Monic := by simpa [fPoly, φ] using hmonicf
        have hcf : (∑ i : s, φ (α (c i)) * (if i = o then 0 else uPoly i)) = fPoly := by
          have hc' : (∑ i : s, c i * (if i = o then 0 else v' i)) = f := hc
          have hmap : φ (α (∑ i : s, c i * (if i = o then 0 else v' i))) = φ (α f) := by
            simpa only [mul_ite, mul_zero, map_sum] using congrArg (fun x => φ (α x)) hc'
          have hsum : (∑ i : s, φ (α (c i * (if i = o then 0 else v' i)))) = φ (α f) := by
            simpa only [mul_ite, mul_zero, map_sum] using hmap
          have hterm : ∑ i : s, φ (α (c i * (if i = o then 0 else v' i))) =
              ∑ i : s, φ (α (c i)) * (if i = o then 0 else uPoly i) := by
            refine Fintype.sum_congr _ _ ?_
            intro i
            by_cases hi : i = o
            · subst hi
              simp [uPoly]
            · simp [uPoly, u, hi, map_mul]
          exact hterm.symm.trans hsum
        let N : ℕ := (uPoly o).natDegree + 1
        let t : Finset s := Finset.univ.erase o
        let wPolyOf (t : Finset s) : s → Polynomial A :=
          Function.update uPoly o (uPoly o + ∑ i ∈ t, (X ^ N * φ (α (c i))) * uPoly i)
        let wPoly : s → Polynomial A := wPolyOf t
        have huwPoly : UnimodularVectorEquiv uPoly wPoly := by
          have hwPolyOf : ∀ t : Finset s, o ∉ t → UnimodularVectorEquiv uPoly (wPolyOf t) := by
            intro t
            refine Finset.induction_on t ?_ ?_
            · intro _
              have hw0 : wPolyOf (∅ : Finset s) = uPoly := by
                funext j
                by_cases hj : j = o
                · subst j
                  simp [wPolyOf]
                · simp [wPolyOf, hj]
              simpa [hw0] using unimodularVectorEquiv_equivalence.1 uPoly
            · intro i t hi_notmem ih ht_insert
              have ht : o ∉ t := by
                intro ho
                exact ht_insert (Finset.mem_insert_of_mem ho)
              have hio : i ≠ o := by
                intro hio
                have : o ∈ insert i t := by
                  subst i
                  exact Finset.mem_insert_self o t
                exact ht_insert this
              have hadd : UnimodularVectorEquiv (wPolyOf t) <| Function.update (wPolyOf t) o
                  (wPolyOf t o + (X ^ N * φ (α (c i))) * (wPolyOf t) i) :=
                unimodularVectorEquiv_update_add o i hio.symm (X ^ N * φ (α (c i))) (wPolyOf t)
              have hwPoly_step : Function.update (wPolyOf t) o
                    (wPolyOf t o + (X ^ N * φ (α (c i))) * wPolyOf t i) = wPolyOf (insert i t) := by
                funext j
                by_cases hj : j = o
                · subst j
                  have hi_t : (wPolyOf t) i = uPoly i := by
                    simp [wPolyOf, hio]
                  have ho_t : (wPolyOf t) o =
                      uPoly o + ∑ j ∈ t, (X ^ N * φ (α (c j))) * uPoly j := by
                    simp [wPolyOf]
                  have ho_it : (wPolyOf (insert i t)) o =
                      uPoly o + ∑ j ∈ insert i t, (X ^ N * φ (α (c j))) * uPoly j := by
                    simp [wPolyOf]
                  have : (wPolyOf t) o + (X ^ N * φ (α (c i))) * (wPolyOf t) i =
                      uPoly o + ∑ j ∈ insert i t, (X ^ N * φ (α (c j))) * uPoly j := by
                    simp only [ho_t, hi_t]
                    calc
                      _ = uPoly o + ((X ^ N * φ (α (c i))) * uPoly i +
                          ∑ j ∈ t, (X ^ N * φ (α (c j))) * uPoly j) := by
                        abel
                      _ = uPoly o + ∑ j ∈ insert i t, (X ^ N * φ (α (c j))) * uPoly j := by
                        simp only [hi_notmem, not_false_eq_true, sum_insert]
                  simpa [Function.update_self, ho_it] using this
                · have hj' : j ≠ o := hj
                  have ht : (wPolyOf t) j = uPoly j := by simp [wPolyOf, hj']
                  have hit : (wPolyOf (insert i t)) j = uPoly j := by simp [wPolyOf, hj']
                  simp [Function.update_of_ne hj', ht, hit]
              exact unimodularVectorEquiv_equivalence.trans (ih ht) <|
                by simpa [hwPoly_step] using hadd
          simpa [wPoly] using hwPolyOf t (by simp [t])
        let w : s → MvPolynomial (Fin (n + 1)) R := fun i => φ.symm (wPoly i)
        have huw : UnimodularVectorEquiv u w := by
          have hcompu : (fun i : s => φr.symm (uPoly i)) = u := by
            funext i
            simpa [uPoly, u, φr] using φr.symm_apply_apply (u i)
          simpa only [hcompu] using unimodularVectorEquiv_map_ringEquiv φr.symm uPoly wPoly huwPoly
        have hαvv' : UnimodularVectorEquiv (fun i : s => α (v i)) u :=
          unimodularVectorEquiv_map_ringEquiv α.toRingEquiv v v' hvv'
        have hαvw : UnimodularVectorEquiv (fun i : s => α (v i)) w :=
          unimodularVectorEquiv_equivalence.trans hαvv' huw
        have hmonic_wPoly : (MvPolynomial.finSuccEquiv R n (w o)).Monic := by
          have hw : MvPolynomial.finSuccEquiv R n (w o) = wPoly o := by
            show φ (φ.symm (wPoly o)) = wPoly o
            simp
          have hsum_cf : ∑ i : s, φ (α (c i)) * (if i = o then 0 else uPoly i) =
              ∑ i ∈ t, φ (α (c i)) * uPoly i := by
            let h : s → Polynomial A := fun i => φ (α (c i)) * (if i = o then 0 else uPoly i)
            let g : s → Polynomial A := fun i => φ (α (c i)) * uPoly i
            have ho : o ∈ (Finset.univ : Finset s) := by simp
            have h_erase : (∑ i ∈ (Finset.univ.erase o : Finset s), h i) =
                ∑ i ∈ (Finset.univ.erase o : Finset s), g i := by
              refine Finset.sum_congr rfl ?_
              intro i hi
              have : i ≠ o := by simpa only [ne_eq, mem_erase, mem_univ, and_true] using hi
              simp only [mul_ite, mul_zero, this, reduceIte, h, g]
            have hs : (∑ i ∈ (Finset.univ.erase o : Finset s), h i) + h o =
                  ∑ i ∈ (Finset.univ : Finset s), h i :=
              Finset.sum_erase_add (Finset.univ : Finset s) h ho
            have ho0 : h o = 0 := by simp [h]
            have hs' : (∑ i ∈ (Finset.univ.erase o : Finset s), h i) =
                  ∑ i ∈ (Finset.univ : Finset s), h i := by
              rw [Finset.sum_erase_eq_sub ho, ho0, sub_zero]
            have : (∑ i ∈ (Finset.univ.erase o : Finset s), g i) =
                  ∑ i ∈ (Finset.univ : Finset s), h i := by
              exact h_erase.symm.trans hs'
            simpa only [h, g, t, mul_ite, mul_zero] using this.symm
          have hwPoly_o : wPoly o = uPoly o + X ^ N * fPoly := by
            have hwPoly_o' : wPoly o = uPoly o + ∑ i ∈ t, (X ^ N * φ (α (c i))) * uPoly i := by
              simp [wPoly, wPolyOf]
            have hsum_t : (∑ i ∈ t, φ (α (c i)) * uPoly i) = fPoly :=
              Eq.trans (by simpa only [mul_ite, mul_zero] using hsum_cf.symm) hcf
            have hsum_X : (∑ i ∈ t, (X ^ N * φ (α (c i))) * uPoly i) =
                  X ^ N * fPoly := by
              calc
                _ = ∑ i ∈ t, X ^ N * (φ (α (c i)) * uPoly i) := by
                  refine Finset.sum_congr rfl ?_
                  intro i hi
                  simp only [mul_assoc]
                _ = X ^ N * ∑ i ∈ t, φ (α (c i)) * uPoly i := by rw [mul_sum]
                _ = X ^ N * fPoly := by simp only [hsum_t]
            exact hwPoly_o'.trans <| by simp only [hsum_X]
          have hdeg : (uPoly o).degree < (X ^ N * fPoly).degree := by
            have hltN : (uPoly o).degree < (N : WithBot ℕ) := by
              have hN : (N : WithBot ℕ) = (uPoly o).natDegree + 1 := by
                simp [N, Nat.cast_add, Nat.cast_one]
              rw [hN]
              exact degree_le_natDegree.trans_lt (WithBot.coe_lt_coe.2 (Nat.lt_succ_self _))
            have hN_le : (N : WithBot ℕ) ≤ (X ^ N * fPoly).degree := by
              have hdeg_Xf : (X ^ N * fPoly).degree = fPoly.degree + N := by
                simp only [mul_comm, degree_mul, degree_pow, degree_X, nsmul_eq_mul, one_mul]
              have h0 : (0 : WithBot ℕ) ≤ fPoly.degree := by
                have : (0 : WithBot ℕ) ≤ (fPoly.natDegree : WithBot ℕ) :=
                  (WithBot.coe_le_coe).2 (Nat.zero_le _)
                simp [Polynomial.degree_eq_natDegree hmonic_fPoly.ne_zero]
              have hN_le' : (N : WithBot ℕ) ≤ fPoly.degree + N := by
                simpa only [zero_add] using (add_le_add_left h0 (N : WithBot ℕ))
              simpa only [hdeg_Xf, ge_iff_le] using hN_le'
            exact lt_of_lt_of_le hltN hN_le
          have : (wPoly o).Monic := by
            simpa only [hwPoly_o] using Monic.add_of_right ((monic_X_pow N).mul hmonic_fPoly) hdeg
          simpa only [hw] using this
        exact ⟨α, w, hαvw, ⟨o, hmonic_wPoly⟩⟩

/-- Let $R = k[x_1, \dots, x_n]$ be a polynomial ring over a principal ideal domain $k$, and let
  $v \in R^n$ be a unimodular vector. Then $v \sim e_1$. -/
theorem thm12 {σ : Type*} [Fintype σ] (o : s) (v : s → MvPolynomial σ R) (hv : IsUnimodular v) :
    UnimodularVectorEquiv v (fun i => if i = o then 1 else 0) := by
  let n : ℕ := Fintype.card σ
  let eσ : σ ≃ Fin n := Fintype.equivFin σ
  let ρ : MvPolynomial σ R ≃ₐ[R] MvPolynomial (Fin n) R := MvPolynomial.renameEquiv R eσ
  let v' : s → MvPolynomial (Fin n) R := fun i => ρ (v i)
  have hv' : IsUnimodular v' := isUnimodular_map_ringEquiv ρ.toRingEquiv v hv
  have hfin (n : ℕ) : ∀ v : s → MvPolynomial (Fin n) R, IsUnimodular v →
      UnimodularVectorEquiv v (fun i : s => if i = o then 1 else 0) := by
    induction n with
    | zero =>
      intro v hv
      let e : MvPolynomial (Fin 0) R ≃+* R := MvPolynomial.isEmptyRingEquiv R (Fin 0)
      have hv' : IsUnimodular fun i => e (v i) := isUnimodular_map_ringEquiv e v hv
      have hstd : IsUnimodular fun i : s => if i = o then (1 : R) else 0 :=
        (Ideal.span (Set.range fun i : s => if i = o then (1 : R) else 0)).eq_top_of_isUnit_mem
          (Ideal.subset_span ⟨o, by simp⟩) isUnit_one
      have h' : UnimodularVectorEquiv
          (fun i => e (v i)) (fun i : s => if i = o then (1 : R) else 0) := by
        simpa using unimodularVectorEquiv_of_pid hv' hstd
      have h'' : UnimodularVectorEquiv
          v (fun i : s => if i = o then (1 : MvPolynomial (Fin 0) R) else 0) := by
        simpa using unimodularVectorEquiv_map_ringEquiv e.symm (fun i => e (v i))
          (fun i : s => if i = o then (1 : R) else 0) h'
      simpa using h''
    | succ n ih =>
      intro v hv
      let A := MvPolynomial (Fin n) R
      let φ : MvPolynomial (Fin (n + 1)) R ≃ₐ[R] Polynomial A := MvPolynomial.finSuccEquiv R n
      let φr : MvPolynomial (Fin (n + 1)) R ≃+* Polynomial A := φ.toRingEquiv
      rcases exists_algEquiv_exists_equiv_exists_monic_finSuccEquiv n v hv with ⟨e, w, hvw⟩
      rcases hvw with ⟨hvw, hmonic⟩
      have hv' : IsUnimodular fun i : s => e (v i) := isUnimodular_map_ringEquiv e.toRingEquiv v hv
      have hw : IsUnimodular w := (isUnimodular_iff_of_unimodularVectorEquiv_ring hvw).1 hv'
      let wpoly : s → Polynomial A := fun j => φr (w j)
      have hwpoly : IsUnimodular wpoly := by simpa [wpoly] using isUnimodular_map_ringEquiv φr w hw
      have hmonic' : ∃ j : s, (wpoly j).Monic := by
        rcases hmonic with ⟨i, hi⟩
        exact ⟨i, by simpa [wpoly, φr, φ] using hi⟩
      have hcor : UnimodularVectorEquiv wpoly (fun j => Polynomial.C ((wpoly j).eval 0)) :=
        cor11 wpoly hwpoly hmonic'
      let ev0 : Polynomial A →+* A := Polynomial.evalRingHom 0
      let v0 : s → A := fun j => ev0 (wpoly j)
      have hv0 : IsUnimodular v0 := isUnimodular_map_ringHom ev0 wpoly hwpoly
      have hmap : UnimodularVectorEquiv
          (fun j => Polynomial.C (v0 j)) (fun j : s => if j = o then 1 else 0) := by
        simpa [v0] using unimodularVectorEquiv_map C (ih v0 hv0)
      have hwstdPoly : UnimodularVectorEquiv wpoly (fun j : s => if j = o then 1 else 0) := by
        have hcor0 : UnimodularVectorEquiv wpoly (fun j => Polynomial.C (v0 j)) := by
          simpa [v0, ev0] using hcor
        exact unimodularVectorEquiv_equivalence.trans hcor0 hmap
      have hwstd : UnimodularVectorEquiv w (fun j : s => if j = o then 1 else 0) := by
        have hcomp : (fun j => φr.symm (wpoly j)) = w := by
          funext j
          simp [wpoly]
        have hstdcomp : (fun j : s => φr.symm (if j = o then 1 else 0)) =
            (fun j : s => if j = o then 1 else 0) := by
          funext j
          by_cases hj : j = o <;> simp [hj]
        simpa [hcomp, hstdcomp] using unimodularVectorEquiv_map_ringEquiv φr.symm wpoly
          (fun j : s => if j = o then 1 else 0) hwstdPoly
      let er : MvPolynomial (Fin (n + 1)) R ≃+* MvPolynomial (Fin (n + 1)) R := e.toRingEquiv
      have hcomp : (fun j => er.symm (er (v j))) = v := by
        funext j
        simpa [er] using er.symm_apply_apply (v j)
      have hstdcomp : (fun j : s => er.symm (if j = o then 1 else 0)) =
          (fun j : s => if j = o then 1 else 0) := by
        funext j
        by_cases hj : j = o <;> simp [hj, er]
      simpa only [RingEquiv.symm_apply_apply, MonoidWithZeroHom.map_ite_one_zero] using
        unimodularVectorEquiv_map_ringEquiv er.symm (fun j => er (v j))
          (fun j : s => if j = o then 1 else 0)
            (by simpa [er] using unimodularVectorEquiv_equivalence.trans hvw hwstd)
  simpa [v', ρ] using unimodularVectorEquiv_map_ringEquiv ρ.symm.toRingEquiv v'
    (fun i : s => if i = o then 1 else 0) (hfin n v' hv')

end thm12
