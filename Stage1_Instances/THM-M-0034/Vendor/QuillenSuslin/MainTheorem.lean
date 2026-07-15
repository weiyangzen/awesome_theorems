/-
Copyright (c) 2026 Yongle Hu. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yongle Hu
-/
/- Port notice: sibling imports are target-local for the repository's pinned environment.
The exact compatibility edits are recorded in `../../PORT_PROVENANCE.md`. -/
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.UnimodularVector.PID
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.FiniteFreeResolution.StablyFree

variable (R : Type*) [CommRing R]

open Module

private lemma module_free_of_prod_free_of_unimodularVectorEquiv
    (hR : ∀ {s : Type} [Fintype s] [DecidableEq s] (o : s) {v : s → R} (_ : IsUnimodular v),
      UnimodularVectorEquiv v (fun i => if i = o then 1 else 0))
    (Q : Type*) [AddCommGroup Q] [Module R Q] [Module.Free R (Q × R)] : Module.Free R Q := by
  rcases subsingleton_or_nontrivial R with hsub | hnontriv
  · have : Subsingleton Q := Module.subsingleton R Q
    exact Module.Free.of_subsingleton R Q
  · let F := Q × R
    let I := Module.Free.ChooseBasisIndex R F
    let b : Basis I R F := Module.Free.chooseBasis R F
    let x : F := (0, 1)
    have hx : x ≠ 0 := by
      intro hx
      exact one_ne_zero <| congrArg Prod.snd hx
    let c : I →₀ R := b.repr x
    have hc : c ≠ 0 := by
      intro hc
      apply hx <| b.repr.injective (by simpa [c] using hc)
    let t : Finset I := c.support
    have ht : t.Nonempty := Finsupp.support_nonempty_iff.2 hc
    let o : t := ⟨ht.choose, ht.choose_spec⟩
    let v : t → R := fun i => c i
    have hv : IsUnimodular v := by
      refine (Ideal.eq_top_iff_one _).2 <|
        Ideal.mem_span_range_iff_exists_fun.2 ⟨fun i => (b i).2, ?_⟩
      have hsnd : (LinearMap.snd R Q R) x = t.sum fun i => c i * (b i).2 := by
        calc _ = (LinearMap.snd R Q R) (Finsupp.linearCombination R b c) := by simp [c]
          _ = t.sum fun i => c i * (b i).2 := by
            simp [t, Finsupp.linearCombination_apply, Finsupp.sum, map_sum, smul_eq_mul]
      have hsum : (∑ i : t, (b i).2 * v i) = (1 : R) := by
        calc _ = t.sum fun i => (b i).2 * c i := by
              simpa [v] using Finset.sum_coe_sort t (fun i => (b i).2 * c i)
          _ = t.sum fun i => c i * (b i).2 := by
            refine Finset.sum_congr rfl ?_
            intro i hi
            simp [mul_comm]
          _ = (LinearMap.snd R Q R) x := hsnd.symm
          _ = 1 := by simp [x]
      simpa [hsum]
    let n : ℕ := Fintype.card t
    let e : t ≃ Fin n := Fintype.equivFin t
    let o' : Fin n := e o
    let v' : Fin n → R := v ∘ e.symm
    have hv' : IsUnimodular v' := by
      unfold IsUnimodular at hv ⊢
      have hrange : Set.range v' = Set.range v := by
        ext r
        constructor
        · rintro ⟨i, rfl⟩
          refine ⟨e.symm i, ?_⟩
          simp [v']
        · rintro ⟨i, rfl⟩
          refine ⟨e i, ?_⟩
          simp [v']
      simpa [hrange] using hv
    have hvo' : UnimodularVectorEquiv v' (fun i : Fin n => if i = o' then 1 else 0) := hR o' hv'
    rcases hvo' with ⟨M, hM⟩
    let gM : LinearMap.GeneralLinearGroup R (Fin n → R) := Matrix.GeneralLinearGroup.toLin M
    let eM : (Fin n → R) ≃ₗ[R] (Fin n → R) := gM.toLinearEquiv
    have heM : eM v' = (fun i : Fin n => if i = o' then 1 else 0) := by
      have : (gM : (Fin n → R) →ₗ[R] Fin n → R) v' = fun i : Fin n => if i = o' then 1 else 0 := by
        simpa [gM, Matrix.GeneralLinearGroup.coe_toLin, Matrix.mulVecLin_apply] using hM
      simpa [eM] using this
    let I₂ := { i : I // i ∉ t }
    let eI : (t ⊕ I₂) ≃ I := Equiv.sumCompl fun i : I => i ∈ t
    let eF' : F ≃ₗ[R] (t ⊕ I₂) →₀ R := b.repr.trans (Finsupp.domLCongr eI).symm
    let eF'' : F ≃ₗ[R] (t →₀ R) × (I₂ →₀ R) :=
      eF'.trans (Finsupp.sumFinsuppLEquivProdFinsupp R : (_ →₀ R) ≃ₗ[R] _)
    let eF''' : F ≃ₗ[R] (Fin n →₀ R) × (I₂ →₀ R) :=
      eF''.trans <| LinearEquiv.prodCongr (Finsupp.domLCongr e) (LinearEquiv.refl R _)
    let eF : F ≃ₗ[R] (Fin n → R) × (I₂ →₀ R) := eF'''.trans <|
      LinearEquiv.prodCongr (Finsupp.linearEquivFunOnFinite R R (Fin n)) (LinearEquiv.refl R _)
    have hxE : eF x = (v', (0 : I₂ →₀ R)) := by
      ext i
      · simp
        exact congrArg (fun k => (b.repr x) k) <| Equiv.sumCompl_apply_inl (e.symm i)
      · have hi0 : c (i : I) = 0 := by
          by_contra hne
          exact i.property (by simpa [t] using Finsupp.mem_support_iff.2 hne)
        simp
        calc _ = (b.repr x) (i : I) := congrArg (fun k => (b.repr x) k) (Equiv.sumCompl_apply_inr i)
          _ = 0 := by simp [c, hi0]
    let U := (Fin n → R) × (I₂ →₀ R)
    let φ : U ≃ₗ[R] U := LinearEquiv.prodCongr eM (LinearEquiv.refl R _)
    let g : R →ₗ[R] U := (eF.toLinearMap).comp (LinearMap.inr R Q R)
    let std : Fin n → R := fun i => if i = o' then 1 else 0
    let gstd : R →ₗ[R] U :=
      { toFun := fun r => (r • std, 0)
        map_add' := by
          intro a b
          refine Prod.ext ?_ ?_
          · show (a + b) • std = a • std + b • std
            simp [add_smul]
          · show (0 : I₂ →₀ R) = (0 : I₂ →₀ R) + 0
            simp
        map_smul' := by
          intro a b
          refine Prod.ext ?_ ?_
          · show (a * b) • std = a • (b • std)
            simp [mul_smul]
          · show (0 : I₂ →₀ R) = a • (0 : I₂ →₀ R)
            simp }
    have hφ : (φ.toLinearMap).comp g = gstd := by
      apply LinearMap.ext
      intro r
      have hg1 : g 1 = (v', (0 : I₂ →₀ R)) := by simpa [g, x] using hxE
      have hgr : g r = (r • v', (0 : I₂ →₀ R)) := by
        calc g r = r • g 1 := by simpa using (g.map_smul r (1 : R))
          _ = (r • v', (0 : I₂ →₀ R)) := by
            refine (by simpa using congrArg (fun u => r • u) hg1 : r • g 1 = r • (v', 0)).trans ?_
            refine Prod.ext ?_ ?_
            · rfl
            · show r • (0 : I₂ →₀ R) = 0
              simp
      refine Prod.ext ?_ ?_
      · calc _ = eM (g r).1 := rfl
          _ = (gstd r).1 := by simp [hgr, heM, std, gstd]
      · calc _ = (g r).2 := rfl
          _ = (gstd r).2 := by simp [hgr, gstd]
    have hg : Submodule.map eF.toLinearMap (LinearMap.range (LinearMap.inr R Q R)) =
        LinearMap.range g := by
      simpa [g] using (LinearMap.range_comp (LinearMap.inr R Q R) (eF.toLinearMap)).symm
    have hgφ : Submodule.map φ.toLinearMap (LinearMap.range g) = LinearMap.range gstd := by
      calc _ = LinearMap.range ((φ.toLinearMap).comp g) := by
              simpa using (LinearMap.range_comp g (φ.toLinearMap)).symm
        _ = LinearMap.range gstd := by simp [hφ]
    let t' := { i : Fin n // i ≠ o' }
    let restrict : (Fin n → R) →ₗ[R] (t' → R) :=
      { toFun := fun f i => f i.1
        map_add' := fun _ _ => by congr
        map_smul' := fun _ _ => by congr }
    let projU : U →ₗ[R] (t' → R) × (I₂ →₀ R) :=
      { toFun := fun x => (restrict x.1, x.2)
        map_add' := fun _ _ => by congr
        map_smul' := fun _ _ => by congr }
    have hprojU_surj : Function.Surjective projU := by
      rintro ⟨f, g⟩
      refine ⟨(fun i => if h : i = o' then 0 else f ⟨i, h⟩, g), ?_⟩
      ext i
      · cases i with | mk i hi => simp [projU, restrict, hi]
      · simp [projU]
    have hkerU : LinearMap.ker projU = LinearMap.range gstd := by
      ext x
      constructor
      · intro hx
        have hx₂ : x.2 = 0 := by
          simpa [projU] using congrArg Prod.snd (show projU x = 0 from hx)
        have hx₁ : ∀ i : Fin n, i ≠ o' → x.1 i = 0 := by
          intro i hi
          have : restrict x.1 ⟨i, hi⟩ = 0 := by
            simpa [projU] using
              congrArg (fun f : t' → R => f ⟨i, hi⟩) <| congrArg Prod.fst (show projU x = 0 from hx)
          simpa [restrict] using this
        refine ⟨x.1 o', Prod.ext ?_ ?_⟩
        · funext i
          by_cases hi : i = o'
          · simp [gstd, std, hi]
          · simp [gstd, std, hi, hx₁ i hi]
        · simpa [gstd] using hx₂.symm
      · rintro ⟨r, rfl⟩
        ext i
        · cases i with
          | mk i hi => simp [projU, restrict, gstd, std, hi]
        · simp [projU, gstd]
    let p : Submodule R F := LinearMap.range (LinearMap.inr R Q R)
    let eFquot : (F ⧸ p) ≃ₗ[R] (U ⧸ LinearMap.range g) :=
      Submodule.Quotient.equiv _ _ eF (by simpa [p] using hg)
    let eφquot : (U ⧸ LinearMap.range g) ≃ₗ[R] (U ⧸ LinearMap.range gstd) :=
      Submodule.Quotient.equiv _ _ φ hgφ
    let eQuot : (U ⧸ LinearMap.range gstd) ≃ₗ[R] (t' → R) × (I₂ →₀ R) :=
      (Submodule.quotEquivOfEq _ _ hkerU.symm) ≪≫ₗ projU.quotKerEquivOfSurjective hprojU_surj
    have hTarget : Module.Free R ((t' → R) × (I₂ →₀ R)) :=
      Module.Free.of_basis <| (Pi.basisFun R t').prod Finsupp.basisSingleOne
    have hFp : Module.Free R (F ⧸ p) :=
      Module.Free.of_equiv (eFquot ≪≫ₗ eφquot ≪≫ₗ eQuot).symm
    have hfst_surj : Function.Surjective (LinearMap.fst R Q R) := by
      intro q
      exact ⟨(q, 0), rfl⟩
    have hker : LinearMap.ker (LinearMap.fst R Q R) = p := by
      simpa [p] using LinearMap.ker_fst R Q R
    let eQ : (F ⧸ p) ≃ₗ[R] Q :=
      (Submodule.quotEquivOfEq _ _ hker.symm) ≪≫ₗ
        (LinearMap.fst R Q R).quotKerEquivOfSurjective hfst_surj
    exact Module.Free.of_equiv eQ

theorem module_free_of_isStablyFree_of_unimodularVectorEquiv
    (hR : ∀ {s : Type} [Fintype s] [DecidableEq s] (o : s) {v : s → R} (_ : IsUnimodular v),
      UnimodularVectorEquiv v (fun i => if i = o then 1 else 0))
    (P : Type*) [AddCommGroup P] [Module R P] (h : IsStablyFree R P) : Module.Free R P := by
  rcases h with ⟨N, _, _, _, _, _⟩
  let ι := Module.Free.ChooseBasisIndex R N
  let n : ℕ := Fintype.card ι
  let eι : ι ≃ Fin n := Fintype.equivFin ι
  let bN : Basis (Fin n) R N := (Module.Free.chooseBasis R N).reindex eι
  let eN : N ≃ₗ[R] Fin n → R := bN.repr.trans (Finsupp.linearEquivFunOnFinite R R (Fin n))
  have hPFin : Module.Free R (P × (Fin n → R)) :=
    Module.Free.of_equiv (LinearEquiv.prodCongr (LinearEquiv.refl R P) eN)
  have : ∀ n : ℕ, Module.Free R (P × (Fin n → R)) → Module.Free R P := by
    intro n
    induction n with
    | zero =>
        intro h0
        have e0 : (P × (Fin 0 → R)) ≃ₗ[R] P :=
          { toFun := Prod.fst
            invFun := fun p => (p, 0)
            left_inv := by
              rintro ⟨p, f⟩
              refine Prod.ext rfl ?_
              funext x
              exact Fin.elim0 x
            right_inv := fun _ => rfl
            map_add' := fun _ _ => rfl
            map_smul' := fun _ _ => rfl }
        exact Module.Free.of_equiv e0
    | succ n ih =>
        intro hsn
        let ePi : (Fin (n + 1) → R) ≃ₗ[R] (Fin n ⊕ Fin 1 → R) :=
          (LinearEquiv.piCongrLeft R (fun _ : Fin (n + 1) => R) finSumFinEquiv).symm
        let eSum : (Fin n ⊕ Fin 1 → R) ≃ₗ[R] (Fin n → R) × (Fin 1 → R) :=
          LinearEquiv.sumArrowLequivProdArrow (Fin n) (Fin 1) R R
        let e1 : (Fin 1 → R) ≃ₗ[R] R := LinearEquiv.funUnique (Fin 1) R R
        let eFin : (Fin (n + 1) → R) ≃ₗ[R] (Fin n → R) × R :=
          ePi.trans (eSum.trans (LinearEquiv.prodCongr (LinearEquiv.refl R _) e1))
        have hQ : Module.Free R ((P × (Fin n → R)) × R) := by
          have eAssoc : (P × (Fin (n + 1) → R)) ≃ₗ[R] ((P × (Fin n → R)) × R) :=
            (LinearEquiv.prodCongr (LinearEquiv.refl R P) eFin) ≪≫ₗ
              (LinearEquiv.prodAssoc R P (Fin n → R) R).symm
          exact Module.Free.of_equiv eAssoc
        have hQ' : Module.Free R (P × (Fin n → R)) :=
          module_free_of_prod_free_of_unimodularVectorEquiv R hR (P × (Fin n → R))
        exact ih hQ'
  exact this n hPFin

/-- Any finitely generated projective module over $k[x_1, \dots, x_n]$ for $k$ a
  principal ideal domain is free. -/
theorem quillenSuslin [IsDomain R] [IsPrincipalIdealRing R] (σ : Type*) [Fintype σ]
    (P : Type*) [AddCommGroup P] [Module (MvPolynomial σ R) P] [Module.Finite (MvPolynomial σ R) P]
    [Projective (MvPolynomial σ R) P] : Module.Free (MvPolynomial σ R) P := by
  refine module_free_of_isStablyFree_of_unimodularVectorEquiv (MvPolynomial σ R) ?_ P <|
    mvPolynomial_isStablyFree_of_isPrincipalIdealRing R σ P
  intro _ _ _
  exact thm12
