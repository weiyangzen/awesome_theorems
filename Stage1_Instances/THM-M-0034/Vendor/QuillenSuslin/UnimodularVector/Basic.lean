/-
Copyright (c) 2026 Yongle Hu. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yongle Hu
-/
/- Port notice: modified for the repository's pinned Lean 4.29/mathlib APIs.
The exact compatibility edits are recorded in `../../../PORT_PROVENANCE.md`. -/
import Mathlib.LinearAlgebra.Matrix.Permutation
import Mathlib.RingTheory.Localization.Algebra
import Mathlib.RingTheory.Localization.AtPrime.Basic
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.UnimodularVector.BivariatePolynomial

open Module Polynomial Finset BigOperators

variable {R : Type*} [CommRing R] {s : Type*} [Fintype s] [DecidableEq s]

/-- A vector `v : s → R` is unimodular if its components generate the unit ideal. -/
def IsUnimodular (v : s → R) : Prop := Ideal.span (Set.range v) = ⊤

/-- Two vectors `v w : s → R` are equivalent if they differ by left multiplication by an element
of `GL s R`. -/
def UnimodularVectorEquiv (v w : s → R) : Prop :=
  ∃ M : Matrix.GeneralLinearGroup s R, M.1.mulVec v = w

/-- `UnimodularVectorEquiv` is an equivalence relation. -/
theorem unimodularVectorEquiv_equivalence :
    Equivalence (UnimodularVectorEquiv (R := R) (s := s)) := by
  refine ⟨fun v ↦ ⟨1, by simp⟩, ?_, ?_⟩
  · intro v w h
    rcases h with ⟨M, hM⟩
    refine ⟨M⁻¹, ?_⟩
    calc _ = (M⁻¹).1.mulVec (M.1.mulVec v) := by simp [hM]
      _ = v := by simp
  · intro a b c ⟨M, hM⟩ ⟨N, hN⟩
    refine ⟨N * M, ?_⟩
    calc _ = N.1.mulVec (M.1.mulVec a) := by simp
      _ = c := by simp [hM, hN]

section isUnimodular_map

variable {A B : Type*} [CommRing A] [CommRing B] {s : Type*}

/-- Unimodularity is preserved under a ring homomorphism. -/
theorem isUnimodular_map_ringHom (f : A →+* B) (v : s → A) (hv : IsUnimodular v) :
    IsUnimodular fun i => f (v i) := by
  unfold IsUnimodular at hv ⊢
  have hmap : Ideal.map f (Ideal.span (Set.range v)) = ⊤ := by
    simpa [hv] using (Ideal.map_top f : Ideal.map f (⊤ : Ideal A) = (⊤ : Ideal B))
  have hrange : (f : A → B) '' Set.range v = Set.range fun i => f (v i) := by
    ext b
    constructor
    · rintro ⟨a, ⟨i, rfl⟩, rfl⟩
      exact ⟨i, rfl⟩
    · rintro ⟨i, rfl⟩
      exact ⟨v i, ⟨i, rfl⟩, rfl⟩
  have hspan : Ideal.span ((f : A → B) '' Set.range v) = ⊤ := by simpa [Ideal.map_span] using hmap
  simpa [hrange] using hspan

/-- Unimodularity is preserved under an algebra equivalence. -/
theorem isUnimodular_map_ringEquiv (e : A ≃+* B) (v : s → A) (hv : IsUnimodular v) :
    IsUnimodular fun i => e (v i) := by
  unfold IsUnimodular at hv ⊢
  have hmap : Ideal.map (e : A →+* B) (Ideal.span (Set.range v)) = ⊤ := by
    simpa using (congrArg (Ideal.map e) hv).trans (by simpa using (Ideal.map_top (e : A →+* B)))
  have hspan : Ideal.span ((e : A →+* B) '' Set.range v) = ⊤ := by
    simpa [Ideal.map_span] using hmap
  have hrange : (e : A → B) '' Set.range v = Set.range fun i => e (v i) := by
    ext b
    constructor
    · rintro ⟨a, ⟨i, rfl⟩, rfl⟩
      exact ⟨i, rfl⟩
    · rintro ⟨i, rfl⟩
      exact ⟨v i, ⟨i, rfl⟩, rfl⟩
  simpa [hrange] using hspan

variable [Fintype s] [DecidableEq s]

/-- Push a unimodular-vector equivalence along a ring homomorphism. -/
theorem unimodularVectorEquiv_map (f : A →+* B) {v w : s → A} (hvw : UnimodularVectorEquiv v w) :
    UnimodularVectorEquiv (fun i => f (v i)) (fun i => f (w i)) := by
  rcases hvw with ⟨M, hM⟩
  refine ⟨Matrix.GeneralLinearGroup.map f M, ?_⟩
  ext i
  have hi : f ((M.1.mulVec v) i) = f (w i) := congrArg f (congrArg (fun u : s → A => u i) hM)
  have hmap : (M.1.map f).mulVec (fun j => f (v j)) i = f ((M.1.mulVec v) i) := by
    simpa [Function.comp] using (RingHom.map_mulVec f M.1 v i).symm
  simpa [Matrix.GeneralLinearGroup.map_apply, RingHom.mapMatrix_apply] using hmap.trans hi

/-- Unimodular-vector equivalence is preserved under an algebra equivalence. -/
theorem unimodularVectorEquiv_map_ringEquiv (e : A ≃+* B) (v w : s → A)
    (hvw : UnimodularVectorEquiv v w) :
    UnimodularVectorEquiv (fun i => e (v i)) (fun i => e (w i)) := by
  simpa using unimodularVectorEquiv_map e.toRingHom hvw

end isUnimodular_map

section degree

/-- If `0 < p.natDegree`, then `p ≠ 1`. -/
lemma ne_one_of_natDegree_pos {p : R[X]} (hp : 0 < p.natDegree) : p ≠ 1 := by
  rintro rfl
  simp at hp

/-- If `a` is monic and `n < a.natDegree`, then the remainder of `X^n` modulo `a` is `X^n`. -/
lemma X_pow_modByMonic_eq_self [Nontrivial R] {a : R[X]} (ha : a.Monic) {n : ℕ}
    (hn : n < a.natDegree) : (X ^ n %ₘ a) = X ^ n :=
  (Polynomial.modByMonic_eq_self_iff ha).2 (by simpa using WithBot.coe_lt_coe.mpr hn)

/-- If we have two polynomials $a(x), b(x) \in R[x]$, with $\deg a = d$ and $a$ monic,
  and $b$ of degree $\leq d-1$ containing at least one coefficient which is a unit, there is a
  polynomial $a(x) e(x) + b(x) f(x) \in (a(x), b(x))$ of degree $\leq d-1$ whose leading coefficient
  is one. -/
theorem degree_lowering (a b : R[X]) (ha : a.Monic) (hb : b.natDegree < a.natDegree)
    (h : ∃ i : ℕ, IsUnit (b.coeff i)) :
    ∃ e f : R[X], (a * e + b * f).Monic ∧ (a * e + b * f).natDegree = a.natDegree - 1 := by
  rcases subsingleton_or_nontrivial R with hR | hR
  · have hab : a = b := Subsingleton.elim _ _
    have : ¬ b.natDegree < a.natDegree := by simp [hab]
    exact (this hb).elim
  · set d : ℕ := a.natDegree
    have hdpos : 0 < d := by simpa [d] using lt_of_le_of_lt (Nat.zero_le _) hb
    have ha_ne_one : a ≠ 1 := by
      apply ne_one_of_natDegree_pos
      simpa [d] using hdpos
    let I : Ideal R[X] := Ideal.span ({a, b} : Set R[X])
    let L : R[X] →ₗ[R] R := (Polynomial.lcoeff R (d - 1)).comp (Polynomial.modByMonicHom a)
    let J : Submodule R R := Submodule.map L (I.restrictScalars R)
    have ha_mem_I : a ∈ I := Ideal.subset_span (by simp)
    have hb_mem_I : b ∈ I := Ideal.subset_span (by simp)
    have hL_X_pow_lt : ∀ {n : ℕ}, n < d - 1 → L (X ^ n) = 0 := by
      intro n hn
      have hn' : n < d := lt_of_lt_of_le hn (Nat.sub_le d 1)
      have hx : X ^ n %ₘ a = X ^ n := by
        simpa [d] using X_pow_modByMonic_eq_self ha (by simpa [d] using hn')
      have hne : (d - 1 : ℕ) ≠ n := ne_of_gt hn
      simp [L, Polynomial.lcoeff_apply, hx, Polynomial.coeff_X_pow, hne]
    have hL_X_pow_eq : L (X ^ (d - 1)) = 1 := by
      have hlt : d - 1 < d := Nat.sub_lt hdpos Nat.one_pos
      have hx : X ^ (d - 1) %ₘ a = X ^ (d - 1) := by
        simpa [d] using X_pow_modByMonic_eq_self ha (by simpa [d] using hlt)
      simp [L, Polynomial.lcoeff_apply, hx, Polynomial.coeff_X_pow]
    have hbCoeff_mem_J (i : ℕ) : i < d → b.coeff i ∈ J := by
      let P (k : ℕ) : Prop := ∀ j : ℕ, k ≤ j → j < d → b.coeff j ∈ J
      have hP_top : P d := by
        intro j hj hlt
        exact (not_lt_of_ge hj hlt).elim
      have hStep : ∀ k : ℕ, k < d → 0 ≤ k → P (k + 1) → P k := by
        intro k hk _ ih j hjk hjd
        by_cases hkj : j = k
        · subst j
          let s : ℕ := d - 1 - k
          have hsI : X ^ s * b ∈ I := I.mul_mem_left _ hb_mem_I
          have hsJ : L (X ^ s * b) ∈ J := by
            refine (Submodule.mem_map).2 ?_
            refine ⟨X ^ s * b, ?_, rfl⟩
            exact hsI
          have hb_sum : b = ∑ i ∈ range d, C (b.coeff i) * X ^ i := by
            simpa using b.as_sum_range_C_mul_X_pow' (by simpa [d] using hb)
          have hs_sum : X ^ s * b = ∑ i ∈ range d, b.coeff i • X ^ (s + i) := by
            conv_lhs => rw [hb_sum]
            simp only [mul_sum]
            refine sum_congr rfl ?_
            intro i hi
            calc _ = C (b.coeff i) * (X ^ s * X ^ i) := by grind
              _ = b.coeff i • X ^ (s + i) := by simp [pow_add, Polynomial.smul_eq_C_mul]
          have hs_L : L (X ^ s * b) = ∑ i ∈ range d, b.coeff i * L (X ^ (s + i)) := by
            simp [hs_sum, L, map_sum, map_smul, smul_eq_mul]
          let f : ℕ → R := fun i => b.coeff i * L (X ^ (s + i))
          have hk1 : k + 1 ≤ d := Nat.succ_le_of_lt hk
          have hsplit : (∑ i ∈ range (k + 1), f i) + (∑ i ∈ Ico (k + 1) d, f i) =
              ∑ i ∈ range d, f i := by
            simpa using (Finset.sum_range_add_sum_Ico f hk1)
          have hprefix_zero : (∑ i ∈ range k, f i) = 0 := by
            refine Finset.sum_eq_zero ?_
            intro i hi
            have hik : i < k := mem_range.mp hi
            have hni : s + i < d - 1 := by
              have hk_le : k ≤ d - 1 := Nat.le_pred_of_lt hk
              simpa [s, Nat.sub_add_cancel (hk_le)] using Nat.add_lt_add_left hik s
            simp [f, hL_X_pow_lt hni]
          have hprefix : (∑ i ∈ range (k + 1), f i) = b.coeff k := by
            have hs_add : s + k = d - 1 := by
              simpa [s] using (Nat.sub_add_cancel (Nat.le_pred_of_lt hk))
            have hfk : f k = b.coeff k := by
              simp [f, hs_add, hL_X_pow_eq]
            simp [Finset.sum_range_succ, hprefix_zero, hfk]
          have hs_eq_total : L (X ^ s * b) =
              b.coeff k + ∑ i ∈ Ico (k + 1) d, f i := by
            calc _ = ∑ i ∈ range d, f i := by simp [hs_L, f]
              _ = (∑ i ∈ range (k + 1), f i) + (∑ i ∈ Ico (k + 1) d, f i) := by
                simpa [add_comm, add_left_comm, add_assoc] using hsplit.symm
              _ = b.coeff k + (∑ i ∈ Ico (k + 1) d, f i) := by simp [hprefix]
          have htail_mem : (∑ i ∈ Ico (k + 1) d, f i) ∈ J := by
            refine Submodule.sum_mem J ?_
            intro i hi
            simpa [f, smul_eq_mul, mul_comm, mul_left_comm, mul_assoc] using
              J.smul_mem (L (X ^ (s + i))) (ih i (mem_Ico.mp hi).1 (mem_Ico.mp hi).2)
          have : L (X ^ s * b) - (∑ i ∈ Ico (k + 1) d, f i) = b.coeff k :=
            (sub_eq_iff_eq_add).2 <| by
              simpa [add_assoc, add_comm, add_left_comm] using hs_eq_total
          simpa [this] using J.sub_mem hsJ htail_mem
        · have hjk' : k < j := lt_of_le_of_ne hjk (Ne.symm hkj)
          have hjk1 : k + 1 ≤ j := Nat.succ_le_of_lt hjk'
          exact ih j hjk1 hjd
      have hP0 : P 0 := Nat.decreasingInduction' hStep (Nat.zero_le _) hP_top
      exact hP0 i (Nat.zero_le _)
    rcases h with ⟨i, hi_unit⟩
    have hi_le : i ≤ b.natDegree := le_natDegree_of_ne_zero (IsUnit.ne_zero hi_unit)
    have hi_lt : i < d := lt_of_le_of_lt hi_le (by simpa [d] using hb)
    have hbi_mem : b.coeff i ∈ J := hbCoeff_mem_J i hi_lt
    rcases hi_unit with ⟨u, hu⟩
    have hone_mem : (1 : R) ∈ J := by
      have : (↑u⁻¹ : R) • (b.coeff i) ∈ J := J.smul_mem (↑u⁻¹ : R) hbi_mem
      simpa [hu.symm, smul_eq_mul] using this
    rcases (Submodule.mem_map).1 hone_mem with ⟨p, hpI, hpL⟩
    let g : R[X] := p %ₘ a
    have hg_coeff : g.coeff (d - 1) = 1 := by simpa [g, L, Polynomial.lcoeff_apply] using hpL
    have hg_deg : g.natDegree < d := by
      simpa [d, g] using Polynomial.natDegree_modByMonic_lt p ha ha_ne_one
    have hg_mem_I : g ∈ I := by
      have hmul : a * (p /ₘ a) ∈ I := I.mul_mem_right _ ha_mem_I
      have hmod : p %ₘ a = p - a * (p /ₘ a) := Polynomial.modByMonic_eq_sub_mul_div p a
      simpa [g, hmod] using I.sub_mem hpI hmul
    have hg_monic : g.Monic := by
      have hg_le : g.natDegree ≤ d - 1 := Nat.le_pred_of_lt (by simpa [d] using hg_deg)
      exact monic_of_natDegree_le_of_coeff_eq_one (d - 1) hg_le (by simpa using hg_coeff)
    rcases (Ideal.mem_span_pair).1 hg_mem_I with ⟨e, f, hef⟩
    have hcomb : a * e + b * f = g := by
      simpa [mul_comm, add_comm, add_left_comm, add_assoc] using hef
    have hg_natDegree : g.natDegree = d - 1 := by
      have hge : d - 1 ≤ g.natDegree := by
        refine le_natDegree_of_ne_zero ?_
        simp [hg_coeff]
      have hle : g.natDegree ≤ d - 1 := Nat.le_pred_of_lt hg_deg
      exact le_antisymm hle hge
    refine ⟨e, f, ?_, ?_⟩
    · simpa [hcomb] using hg_monic
    · simpa [hcomb, d] using hg_natDegree

end degree

section horrocks

/-- An elementary `GL` operation: add `c` times component `j` to component `i`. -/
theorem unimodularVectorEquiv_update_add (i j : s) (hij : i ≠ j) (c : R[X]) (v : s → R[X]) :
    UnimodularVectorEquiv v (Function.update v i (v i + c * v j)) := by
  let A : Matrix s s R[X] := Matrix.transvection i j c
  have hdet : IsUnit (Matrix.det A) := by
    have : Matrix.det A = 1 := by
      simpa [A] using Matrix.det_transvection_of_ne i j hij c
    simp [this]
  refine ⟨Matrix.GeneralLinearGroup.mk'' A hdet, ?_⟩
  ext k n
  by_cases hk : k = i
  · subst hk
    simp [A, Matrix.transvection, Matrix.mulVec, dotProduct, Matrix.one_apply, Matrix.single_apply,
      Function.update, Finset.sum_add_distrib, add_mul]
  · simp [A, Matrix.transvection, Matrix.mulVec, dotProduct, Matrix.one_apply, hk, Ne.symm hk,
      Function.update]

/-- An elementary `GL` operation: replace component `j` by `v j %ₘ v i` when `v i` is monic. -/
theorem unimodularVectorEquiv_update_modByMonic (i j : s) (hij : j ≠ i)
    (v : s → R[X]) (hi : (v i).Monic) :
    UnimodularVectorEquiv v (Function.update v j (v j %ₘ v i)) := by
  have hmod : v j %ₘ v i = v j + (-(v j /ₘ v i)) * v i := by
    simpa [sub_eq_add_neg, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc]
      using Polynomial.modByMonic_eq_sub_mul_div (v j) (v i)
  simpa [hmod] using unimodularVectorEquiv_update_add j i hij (-(v j /ₘ v i)) v

/-- Swapping two coordinates is a `GL`-equivalence. -/
theorem unimodularVectorEquiv_swap (i j : s) (v : s → R[X]) :
    UnimodularVectorEquiv v (v ∘ Equiv.swap i j) := by
  let σ : Equiv.Perm s := Equiv.swap i j
  let A : Matrix s s R[X] := σ.permMatrix R[X]
  have hdet : IsUnit (Matrix.det A) := by
    have hsign : IsUnit (σ.sign : R[X]) := by
      simpa using Units.isUnit (Units.map (Int.castRingHom (R[X])).toMonoidHom σ.sign)
    simpa [A, Matrix.det_permutation] using hsign
  exact ⟨Matrix.GeneralLinearGroup.mk'' A hdet, by simpa [A, σ] using Matrix.permMatrix_mulVec σ⟩

/-- If a polynomial is nonzero, then some coefficient is nonzero. -/
theorem exists_coeff_ne_zero_of_ne_zero {S : Type*} [Semiring S] {p : S[X]} (hp : p ≠ 0) :
    ∃ n : ℕ, p.coeff n ≠ 0 := by
  by_contra h
  apply hp
  ext n
  have : ¬ p.coeff n ≠ 0 := by
    intro hn
    exact h ⟨n, hn⟩
  simpa using Classical.not_not.mp this

/-- An elementary `GL` operation: scale component `i` by a unit `u`. -/
theorem unimodularVectorEquiv_update_mul_isUnit (i : s) (u : R[X]) (hu : IsUnit u)
    (v : s → R[X]) :
    UnimodularVectorEquiv v (Function.update v i (u * v i)) := by
  let d : s → R[X] := fun j => if j = i then u else 1
  let D : Matrix s s R[X] := Matrix.diagonal d
  have hdet : IsUnit (Matrix.det D) := by
    -- `det (diagonal d) = ∏ j, d j = u`.
    have : Matrix.det D = u := by
      simp [D, d, Matrix.det_diagonal, Finset.prod_ite_eq']
    simpa [this] using hu
  refine ⟨Matrix.GeneralLinearGroup.mk'' D hdet, ?_⟩
  ext j
  by_cases hji : j = i
  · subst hji
    simp [D, d, Matrix.mulVec_diagonal, Function.update]
  · simp [D, d, Matrix.mulVec_diagonal, Function.update, hji]

/-- The ideal generated by the coordinates of `M.mulVec v` agrees with the ideal generated by the
coordinates of `v` when `M ∈ GL`. -/
theorem ideal_span_range_mulVec (M : Matrix.GeneralLinearGroup s R[X]) (v : s → R[X]) :
    Ideal.span (Set.range (M.1.mulVec v)) = Ideal.span (Set.range v) := by
  -- First show `span (range (M.mulVec v)) ≤ span (range v)` for all `M`.
  have span_mulVec_le (N : Matrix.GeneralLinearGroup s R[X]) (v : s → R[X])
      : Ideal.span (Set.range (N.1.mulVec v)) ≤ Ideal.span (Set.range v) := by
    let I : Ideal R[X] := Ideal.span (Set.range v)
    refine Ideal.span_le.2 ?_
    rintro _ ⟨i, rfl⟩
    have hvj (j : s) : v j ∈ I := Ideal.subset_span ⟨j, rfl⟩
    have hterm (j : s) : N.1 i j * v j ∈ I := by
      simpa [mul_comm] using I.mul_mem_left (N.1 i j) (hvj j)
    simpa [Matrix.mulVec, dotProduct, I] using I.sum_mem (fun j _ => hterm j)
  refine le_antisymm (span_mulVec_le M v) ?_
  -- Apply the inequality to `M⁻¹` and the vector `M.mulVec v`.
  have hle' : Ideal.span (Set.range ((M⁻¹).1.mulVec (M.1.mulVec v))) ≤
      Ideal.span (Set.range (M.1.mulVec v)) :=
    span_mulVec_le (M⁻¹) (M.1.mulVec v)
  simpa using hle'

/-- `IsUnimodular` is invariant under `UnimodularVectorEquiv`. -/
theorem isUnimodular_iff_of_unimodularVectorEquiv {v w : s → R[X]}
    (hvw : UnimodularVectorEquiv v w) : IsUnimodular v ↔ IsUnimodular w := by
  rcases hvw with ⟨M, rfl⟩
  unfold IsUnimodular
  simp [ideal_span_range_mulVec M v]

/-- If `2 < Fintype.card s` and `i ≠ o`, there exists `k` different from both `o` and `i`. -/
theorem exists_ne_ne_of_two_lt_card (o i : s) (hio : i ≠ o) (hcard : 2 < Fintype.card s) :
    ∃ k : s, k ≠ o ∧ k ≠ i := by
  -- Consider `((univ.erase o).erase i)`.
  have ho_mem : o ∈ (Finset.univ : Finset s) := Finset.mem_univ o
  have hi_mem : i ∈ (Finset.univ.erase o : Finset s) := by
    simp [Finset.mem_erase, hio]
  have hcard_erase_o : (Finset.univ.erase o : Finset s).card = Fintype.card s - 1 := by
    simp [Finset.card_univ]
  have hcard_erase_oi : ((Finset.univ.erase o).erase i : Finset s).card =
      Fintype.card s - 2 := by
    calc _ = (Finset.univ.erase o : Finset s).card - 1 := by
          simpa using Finset.card_erase_of_mem hi_mem
      _ = (Fintype.card s - 1) - 1 := by simp [hcard_erase_o, Nat.sub_sub]
  have hnonempty : ((Finset.univ.erase o).erase i : Finset s).Nonempty := by
    have : 0 < ((Finset.univ.erase o).erase i : Finset s).card := by
      have : 0 < Fintype.card s - 2 := Nat.sub_pos_of_lt hcard
      simpa [hcard_erase_oi] using this
    exact Finset.card_pos.1 this
  rcases hnonempty with ⟨k, hk⟩
  refine ⟨k, ?_, ?_⟩
  · have hk' : k ≠ o := (Finset.mem_erase.1 (Finset.mem_of_mem_erase hk)).1
    exact hk'
  · have hk' : k ≠ i := (Finset.mem_erase.1 hk).1
    exact hk'

/-- If `v o = 1`, then `v` is `GL`-equivalent to the standard basis vector supported at `o`. -/
theorem unimodularVectorEquiv_stdBasis_of_eq_one (o : s) (v : s → R[X]) (ho : v o = 1) :
    UnimodularVectorEquiv v (fun i => if i = o then 1 else 0) := by
  -- Clear all coordinates (except `o`) by iterating over `Finset.univ`.
  let P (t : Finset s) : Prop := ∃ w : s → R[X], UnimodularVectorEquiv v w ∧ w o = 1 ∧
      (∀ i : s, i ∈ t → i ≠ o → w i = 0) ∧ (∀ i : s, i ∉ t → w i = v i)
  have hP : P (Finset.univ : Finset s) := by
    refine (Finset.univ : Finset s).induction_on ?_ ?_
    · refine ⟨v, unimodularVectorEquiv_equivalence.refl v, by simp [ho], ?_, ?_⟩
      · intro i hi _hio
        simp at hi
      · intro i hi
        rfl
    · intro a t ha_not_mem ih
      rcases ih with ⟨w, hvw, hwo, hw_clear, hw_keep⟩
      by_cases hao : a = o
      · subst hao
        refine ⟨w, hvw, hwo, ?_, ?_⟩
        · intro i hi hio
          have hit : i ∈ t := by
            simpa [Finset.mem_insert, hio] using hi
          exact hw_clear i hit hio
        · intro i hi
          have hit : i ∉ t := by
            intro hit
            exact hi (Finset.mem_insert_of_mem hit)
          exact hw_keep i hit
      · let w' : s → R[X] := Function.update w a (w a + (-(w a)) * w o)
        have hw' : UnimodularVectorEquiv w w' := unimodularVectorEquiv_update_add a o hao (-(w a)) w
        refine ⟨w', unimodularVectorEquiv_equivalence.trans hvw hw', ?_, ?_, ?_⟩
        · -- `w' o = 1`
          have hoa : o ≠ a := by simpa [eq_comm] using hao
          simp [w', hwo, hoa]
        · -- Cleared coordinates in `insert a t`.
          intro i hi hio
          by_cases hia : i = a
          · subst hia
            simp [w', hwo]
          · have hit : i ∈ t := by
              simpa [Finset.mem_insert, hia] using hi
            simpa [w', Function.update, hia] using hw_clear i hit hio
        · -- Coordinates not in `insert a t` are unchanged.
          intro i hi
          by_cases hia : i = a
          · subst hia
            exact (hi (Finset.mem_insert_self i t)).elim
          · have hit : i ∉ t := by
              intro hit
              exact hi (Finset.mem_insert_of_mem hit)
            simpa [w', Function.update, hia] using hw_keep i hit
  rcases hP with ⟨w, hvw, hwo, hw_clear, _hw_keep⟩
  have hw : w = fun i => if i = o then 1 else 0 := by
    funext i
    by_cases hio : i = o
    · subst hio
      simp [hwo]
    · have hi_univ : i ∈ (Finset.univ : Finset s) := Finset.mem_univ i
      simpa [hio] using hw_clear i hi_univ hio
  simpa [hw] using hvw

/-- Reduce every coordinate `i ≠ o` modulo the monic polynomial `v o`, using elementary `GL`
operations. -/
theorem unimodularVectorEquiv_modByMonic_all (o : s) (v : s → R[X]) (ho : (v o).Monic) :
    ∃ w : s → R[X], UnimodularVectorEquiv v w ∧ w o = v o ∧
      (∀ i : s, i ≠ o → w i = v i %ₘ v o) := by
  let w : s → R[X] := fun i => if i = o then v o else v i %ₘ v o
  let P : Finset s → Prop := fun t =>
    ∃ u : s → R[X], UnimodularVectorEquiv v u ∧ u o = v o ∧
      (∀ i : s, i ∈ t → i ≠ o → u i = v i %ₘ v o) ∧ (∀ i : s, i ∉ t → u i = v i)
  have hP : P (Finset.univ : Finset s) := by
    refine (Finset.univ : Finset s).induction_on ?_ ?_
    · refine ⟨v, unimodularVectorEquiv_equivalence.refl v, rfl, ?_, ?_⟩
      · intro i hi _hio
        simp at hi
      · intro i hi
        rfl
    · intro a t ha_not_mem ih
      rcases ih with ⟨u, hvu, huo, hu_mod, hu_keep⟩
      by_cases hao : a = o
      · subst hao
        refine ⟨u, hvu, huo, ?_, ?_⟩
        · intro i hi hio
          have hit : i ∈ t := by
            simpa [Finset.mem_insert, hio] using hi
          exact hu_mod i hit hio
        · intro i hi
          have hit : i ∉ t := by
            intro hit
            exact hi (Finset.mem_insert_of_mem hit)
          exact hu_keep i hit
      · let u' : s → R[X] := Function.update u a (u a %ₘ u o)
        have hu' : UnimodularVectorEquiv u u' :=
          unimodularVectorEquiv_update_modByMonic o a hao u (by simpa [huo] using ho)
        refine ⟨u', unimodularVectorEquiv_equivalence.trans hvu hu', ?_, ?_, ?_⟩
        · -- `u' o = v o`
          have hoa : o ≠ a := by simpa [eq_comm] using hao
          simp [u', huo, hoa]
        · -- Updated coordinates.
          intro i hi hio
          by_cases hia : i = a
          · subst hia
            have hua : u i = v i := hu_keep i ha_not_mem
            simp [u', huo, hua]
          · have hit : i ∈ t := by
              simpa [Finset.mem_insert, hia] using hi
            simpa [u', Function.update, hia] using hu_mod i hit hio
        · -- Unchanged coordinates.
          intro i hi
          by_cases hia : i = a
          · subst hia
            exact (hi (Finset.mem_insert_self i t)).elim
          · have hit : i ∉ t := by
              intro hit
              exact hi (Finset.mem_insert_of_mem hit)
            simpa [u', Function.update, hia] using hu_keep i hit
  rcases hP with ⟨u, hvu, huo, hu_mod, _hu_keep⟩
  refine ⟨w, ?_, ?_, ?_⟩
  · -- `v` is equivalent to `w`.
    have huw : u = w := by
      funext i
      by_cases hio : i = o
      · subst hio
        simp [w, huo]
      · have hi_univ : i ∈ (Finset.univ : Finset s) := Finset.mem_univ i
        simpa [w, hio, huo] using hu_mod i hi_univ hio
    simpa [huw] using hvu
  · simp [w]
  · intro i hio
    simp [w, hio]

omit [DecidableEq s] in
/-- Over a local ring, a unimodular vector with a monic component of positive degree has another
component with a coefficient that is a unit. -/
theorem exists_unit_coeff_of_isUnimodular [IsLocalRing R] (o : s) (v : s → R[X])
    (huv : IsUnimodular v) (ho : (v o).Monic) (hd : 0 < (v o).natDegree) :
    ∃ i : s, i ≠ o ∧ ∃ n : ℕ, IsUnit ((v i).coeff n) := by
  let m : Ideal R := IsLocalRing.maximalIdeal R
  let k := R ⧸ m
  let f : R →+* k := Ideal.Quotient.mk _
  let F : R[X] →+* k[X] := Polynomial.mapRingHom f
  -- Get an explicit unimodularity certificate.
  have h1 : (1 : R[X]) ∈ Ideal.span (Set.range v) := by
    rw [huv]
    exact Submodule.mem_top
  rcases (Ideal.mem_span_range_iff_exists_fun).1 h1 with ⟨c, hc⟩
  have hc' : (∑ i : s, F (c i) * F (v i)) = 1 := by
    simpa [map_sum, map_mul] using congrArg F hc
  have h_not_all_zero : ¬ (∀ i : s, i ≠ o → F (v i) = 0) := by
    intro hzero
    have hsum : (∑ i : s, F (c i) * F (v i)) = F (c o) * F (v o) := by
      simpa using Finset.sum_eq_single o
        (h₀ := by
          intro i _ hi
          simp [hzero i hi])
        (h₁ := by
          intro ho'
          exact (ho' (Finset.mem_univ o)).elim)
    have hunit : IsUnit (F (v o)) := by
      refine ⟨⟨F (v o), F (c o), ?_, ?_⟩, rfl⟩
      · -- `F (v o) * F (c o) = 1`
        have : F (c o) * F (v o) = 1 := by
          simpa [hsum] using hc'
        simpa [mul_comm] using this
      · -- `F (c o) * F (v o) = 1`
        simpa [hsum] using hc'
    -- But `F (v o)` has positive degree, hence is not a unit.
    have hdeg' : 0 < (F (v o)).natDegree := by
      have hcoeff : (F (v o)).coeff (v o).natDegree = 1 := by
        simp [F, Polynomial.coeff_map, ho.coeff_natDegree]
      have hne : (F (v o)).coeff (v o).natDegree ≠ 0 := by
        simp [hcoeff]
      have hle : (v o).natDegree ≤ (F (v o)).natDegree := le_natDegree_of_ne_zero hne
      exact lt_of_lt_of_le hd hle
    exact (Polynomial.not_isUnit_of_natDegree_pos (F (v o)) hdeg') hunit
  rcases not_forall.1 h_not_all_zero with ⟨i, hi⟩
  have hio : i ≠ o := by
    by_contra h'
    subst h'
    exact hi (by simp)
  have hne : F (v i) ≠ 0 := by
    intro h0
    apply hi
    intro _hio
    exact h0
  rcases exists_coeff_ne_zero_of_ne_zero hne with ⟨n, hn⟩
  have hn' : (v i).coeff n ∉ m := by
    intro hmem
    have : f ((v i).coeff n) = 0 := by
      -- `mk` is zero iff the element is in the ideal.
      exact (Ideal.Quotient.eq_zero_iff_mem).2 hmem
    have : (F (v i)).coeff n = 0 := by simpa [F, Polynomial.coeff_map] using this
    exact hn this
  refine ⟨i, hio, n, ?_⟩
  simpa [m] using IsLocalRing.notMem_maximalIdeal.1 hn'

/-- Let `A = R[X]` for a local ring `R`. Then any unimodular vector in `A^s` with a monic
component is equivalent to `e₁`. -/
theorem horrocks [IsLocalRing R] (o : s) (v : s → R[X]) (huv : IsUnimodular v)
    (h : ∃ i : s, (v i).Monic) : UnimodularVectorEquiv v (fun i => if i = o then 1 else 0) := by
  rcases subsingleton_or_nontrivial R with hR | hR
  · have hv : v = fun i => if i = o then 1 else 0 := by
      funext i
      exact Subsingleton.elim _ _
    simpa [hv] using unimodularVectorEquiv_equivalence.refl v
  · rcases h with ⟨i0, hi0⟩
    let v0 : s → R[X] := v ∘ Equiv.swap i0 o
    have hv0 : UnimodularVectorEquiv v v0 := unimodularVectorEquiv_swap i0 o v
    have huv0 : IsUnimodular v0 := (isUnimodular_iff_of_unimodularVectorEquiv hv0).1 huv
    have ho0 : (v0 o).Monic := by simpa [v0] using hi0
    have main : UnimodularVectorEquiv v0 (fun i => if i = o then 1 else 0) := by
      -- Split by the cardinality of `s`.
      by_cases hcard1 : Fintype.card s = 1
      · have : Subsingleton s := (Fintype.card_le_one_iff_subsingleton).1 (le_of_eq hcard1)
        have hrange : Set.range v0 = ({v0 o} : Set R[X]) := by
          ext x
          constructor
          · rintro ⟨i, rfl⟩
            simpa using congrArg v0 (Subsingleton.elim i o)
          · intro hx
            refine ⟨o, ?_⟩
            simpa using hx.symm
        have hunit : IsUnit (v0 o) := by
          have : Ideal.span ({v0 o} : Set R[X]) = ⊤ := by
            simpa [IsUnimodular, hrange] using huv0
          simpa using (Ideal.span_singleton_eq_top).1 this
        rcases hunit with ⟨u, hu⟩
        -- Scale by `u⁻¹` to make the distinguished coordinate equal to `1`.
        have hscale : UnimodularVectorEquiv v0
            (Function.update v0 o ((↑(u⁻¹) : R[X]) * v0 o)) :=
          unimodularVectorEquiv_update_mul_isUnit o (↑(u⁻¹) : R[X]) (by simp) v0
        have hone : (Function.update v0 o ((↑(u⁻¹) : R[X]) * v0 o)) o = 1 := by
          have hu' : v0 o = (u : R[X]) := hu.symm
          simp [Function.update, hu']
        exact unimodularVectorEquiv_equivalence.trans hscale
          (unimodularVectorEquiv_stdBasis_of_eq_one o
            (Function.update v0 o ((↑(u⁻¹) : R[X]) * v0 o)) hone)
      · by_cases hcard2 : Fintype.card s = 2
        · -- In dimension `2`, any unimodular vector is equivalent to a basis vector.
          have hNat : Nat.card s = 2 := by
            simpa [Nat.card_eq_fintype_card] using hcard2
          rcases (Nat.card_eq_two_iff' o).1 hNat with ⟨i, hio, hi_unique⟩
          have hoi : o ≠ i := Ne.symm hio
          have huniv : (Finset.univ : Finset s) = ({o, i} : Finset s) := by
            ext j
            constructor
            · intro _
              by_cases hj : j = o
              · subst hj
                simp
              · have : j = i := hi_unique j hj
                subst this
                simp [hio]
            · intro _
              simp
          -- Get a unimodularity certificate `∑ c j * v0 j = 1`.
          have h1 : (1 : R[X]) ∈ Ideal.span (Set.range v0) := by
            rw [huv0]
            exact Submodule.mem_top
          rcases (Ideal.mem_span_range_iff_exists_fun).1 h1 with ⟨c, hc⟩
          have hc' : c o * v0 o + c i * v0 i = 1 := by
            -- Rewrite the sum over `s` using `univ = {o, i}`.
            simpa [huniv, hoi, add_comm, add_left_comm, add_assoc, mul_assoc] using hc
          -- Build the classical `SL₂` matrix sending `v0` to `e_o`.
          let A : Matrix s s R[X] := fun r s' =>
            if r = o then c s' else if s' = o then -(v0 i) else v0 o
          let B : Matrix s s R[X] := fun r s' =>
            if r = o then if s' = o then v0 o else -(c i) else if s' = o then v0 i else c o
          have hAB : A * B = 1 := by
            apply Matrix.ext
            intro r s'
            by_cases hr : r = o
            · subst r
              by_cases hs : s' = o
              · subst s'
                -- (row o, col o)
                simp [Matrix.mul_apply, huniv, A, B, hio, hoi, hc', Finset.sum_insert,
                  Finset.sum_singleton]
              · have hs' : s' = i := hi_unique s' (by simpa using hs)
                subst s'
                -- (row o, col i)
                simp [Matrix.mul_apply, huniv, A, B, hio, hoi, Finset.sum_insert,
                  Finset.sum_singleton]
                ring
            · have hr' : r = i := hi_unique r hr
              subst r
              by_cases hs : s' = o
              · subst s'
                -- (row i, col o)
                simp [Matrix.mul_apply, huniv, A, B, hio, hoi, Finset.sum_insert,
                  Finset.sum_singleton]
                ring
              · have hs' : s' = i := hi_unique s' (by simpa using hs)
                subst s'
                -- (row i, col i)
                simp [Matrix.mul_apply, huniv, A, B, hio, hoi, Finset.sum_insert,
                  Finset.sum_singleton]
                simpa [mul_comm, add_comm, add_left_comm, add_assoc] using hc'
          have hdet : IsUnit (Matrix.det A) := by
            have hdet_mul : Matrix.det A * Matrix.det B = 1 := by
              simpa [Matrix.det_mul, Matrix.det_one] using congrArg Matrix.det hAB
            refine ⟨⟨Matrix.det A, Matrix.det B, hdet_mul, ?_⟩, rfl⟩
            simpa [mul_comm] using hdet_mul
          have hmul : A.mulVec v0 = (fun j => if j = o then 1 else 0) := by
            funext r
            by_cases hr : r = o
            · subst r
              -- The first row is the certificate.
              have : (∑ j : s, A o j * v0 j) = 1 := by
                -- `A o j = c j`.
                simpa [A] using hc
              simp [Matrix.mulVec, dotProduct, this]
            · have hr' : r = i := hi_unique r hr
              subst r
              have : (∑ j : s, A i j * v0 j) = 0 := by
                -- `A i o * v0 o + A i i * v0 i = 0`.
                simp [huniv, A, hio, hoi]
                ring
              simp [Matrix.mulVec, dotProduct, hr, this]
          refine ⟨Matrix.GeneralLinearGroup.mk'' A hdet, ?_⟩
          simp [hmul]
        · -- The main Horrocks induction for `2 < card s`.
          have hcard_pos : 0 < Fintype.card s := Fintype.card_pos_iff.2 ⟨o⟩
          have hcard_ne0 : Fintype.card s ≠ 0 := Nat.ne_of_gt hcard_pos
          have hcard_gt1 : 1 < Fintype.card s :=
            Nat.one_lt_iff_ne_zero_and_ne_one.2 ⟨hcard_ne0, hcard1⟩
          have hcard_ge2 : 2 ≤ Fintype.card s := Nat.succ_le_iff.2 hcard_gt1
          have hcard : 2 < Fintype.card s := lt_of_le_of_ne hcard_ge2 (Ne.symm hcard2)
          -- Induct on `n = natDegree (v0 o)`.
          let P (n : ℕ) : Prop :=
            ∀ u : s → R[X], IsUnimodular u → (u o).Monic → (u o).natDegree = n →
              UnimodularVectorEquiv u (fun i => if i = o then 1 else 0)
          have hP : ∀ n : ℕ, P n := by
            intro n
            induction n with
            | zero =>
                intro u huu huo hdeg
                have huo' : u o = 1 := Polynomial.eq_one_of_monic_natDegree_zero huo hdeg
                simpa [huo'] using unimodularVectorEquiv_stdBasis_of_eq_one o u huo'
            | succ n ih =>
                intro u huu huo hdeg
                have hdpos : 0 < (u o).natDegree := by
                  simp [hdeg]
                have huo_ne_one : u o ≠ 1 :=
                  ne_one_of_natDegree_pos hdpos
                -- First reduce all other coordinates modulo the monic entry `u o`.
                rcases unimodularVectorEquiv_modByMonic_all o u huo with
                  ⟨w, huw, hwo, hwmod⟩
                have hwu : IsUnimodular w :=
                  (isUnimodular_iff_of_unimodularVectorEquiv huw).1 huu
                have hwo_monic : (w o).Monic := by simpa [hwo] using huo
                have hdegw : (w o).natDegree = n + 1 := by simp [hwo, hdeg]
                -- Find an index with a unit coefficient.
                rcases exists_unit_coeff_of_isUnimodular o w hwu hwo_monic (by simp [hdegw]) with
                  ⟨i, hio, m, hm_unit⟩
                rcases exists_ne_ne_of_two_lt_card o i hio hcard with ⟨k, hko, hki⟩
                let a : R[X] := w o
                let b : R[X] := w i
                have ha_ne_one : a ≠ 1 := by
                  apply ne_one_of_natDegree_pos
                  simp [a, hdegw]
                have hbdeg : b.natDegree < a.natDegree := by
                  have := Polynomial.natDegree_modByMonic_lt (u i) huo huo_ne_one
                  -- `b = u i %ₘ u o` and `a = u o`.
                  have hb : b = u i %ₘ u o := by
                    simp [b, hwmod i hio]
                  have ha : a = u o := by simp [a, hwo]
                  simpa [hb, ha] using this
                rcases degree_lowering a b hwo_monic hbdeg ⟨m, hm_unit⟩ with
                  ⟨e, f, hg_monic, hg_deg⟩
                let g : R[X] := a * e + b * f
                have hg_nat : g.natDegree = a.natDegree - 1 := hg_deg
                have hg_coeff : g.coeff (a.natDegree - 1) = 1 := by
                  -- `g` is monic and has natDegree `a.natDegree - 1`.
                  simpa [g, hg_nat] using hg_monic.coeff_natDegree
                let r0 : R := 1 - (w k).coeff (a.natDegree - 1)
                let r : R[X] := C r0
                -- Add `r*e` times `w o` and `r*f` times `w i` to coordinate `k`.
                let w1 : s → R[X] := Function.update w k (w k + (r * e) * w o)
                let w2 : s → R[X] := Function.update w1 k (w1 k + (r * f) * w1 i)
                have hw_w2 : UnimodularVectorEquiv w w2 := unimodularVectorEquiv_equivalence.trans
                  (unimodularVectorEquiv_update_add k o hko (r * e) w)
                    (unimodularVectorEquiv_update_add k i hki (r * f) w1)
                have hw2k : w2 k = w k + r * g := by
                  -- Unfold the two updates.
                  have hki' : i ≠ k := Ne.symm hki
                  have hko' : o ≠ k := Ne.symm hko
                  simp [w2, w1, hki', g, a, b]
                  ring
                have hdeg_wk : (w k).natDegree ≤ a.natDegree - 1 := by
                  have hklt : (w k).natDegree < a.natDegree := by
                    have := Polynomial.natDegree_modByMonic_lt (u k) huo huo_ne_one
                    have hk : w k = u k %ₘ u o := by
                      simp [hwmod k hko]
                    have ha : a = u o := by simp [a, hwo]
                    simpa [hk, ha] using this
                  exact Nat.le_pred_of_lt hklt
                have hrdeg : r.natDegree = 0 := by simp [r]
                have hdeg_rg : (r * g).natDegree ≤ a.natDegree - 1 := by
                  have : (r * g).natDegree ≤ r.natDegree + g.natDegree :=
                    Polynomial.natDegree_mul_le
                  have hg_le : g.natDegree ≤ a.natDegree - 1 := by simp [g, hg_nat]
                  have : (r * g).natDegree ≤ 0 + (a.natDegree - 1) := by
                    simpa [hrdeg, hg_nat, add_comm, add_left_comm, add_assoc] using this
                  simpa using this
                have hdeg_t : (w2 k).natDegree ≤ a.natDegree - 1 := by
                  -- Use the degree bounds for `w k` and `r*g`.
                  have : (w k + r * g).natDegree ≤ max (w k).natDegree (r * g).natDegree :=
                    Polynomial.natDegree_add_le _ _
                  have hmax : max (w k).natDegree (r * g).natDegree ≤ a.natDegree - 1 :=
                    max_le_iff.2 ⟨hdeg_wk, hdeg_rg⟩
                  simpa [hw2k] using le_trans this hmax
                have hcoeff_t : (w2 k).coeff (a.natDegree - 1) = 1 := by
                  -- Coefficient computation: force the top coefficient to be `1`.
                  have hg' : g.coeff (a.natDegree - 1) = 1 := hg_coeff
                  -- Keep `r` as `C r0` to use `coeff_C_mul` cleanly.
                  have hrcoeff :
                      (r * g).coeff (a.natDegree - 1) = r0 * g.coeff (a.natDegree - 1) := by
                    simp [r, Polynomial.coeff_C_mul]
                  -- Now compute the top coefficient of `w k + r * g`.
                  simp [hw2k, Polynomial.coeff_add, hrcoeff, hg', r0]
                have hdeg_eq : (w2 k).natDegree = a.natDegree - 1 := by
                  have hge : a.natDegree - 1 ≤ (w2 k).natDegree := by
                    refine le_natDegree_of_ne_zero ?_
                    simp [hcoeff_t]
                  exact le_antisymm hdeg_t hge
                have hmonic_k : (w2 k).Monic := by
                  -- Use `coeff = 1` at the top degree.
                  have hle : (w2 k).natDegree ≤ a.natDegree - 1 := by simp [hdeg_eq]
                  exact monic_of_natDegree_le_of_coeff_eq_one (a.natDegree - 1) hle
                    (by simp [hcoeff_t])
                -- Swap `k` and `o` to move the new monic polynomial to coordinate `o`.
                let w3 : s → R[X] := w2 ∘ Equiv.swap o k
                have hw2_w3 : UnimodularVectorEquiv w2 w3 := unimodularVectorEquiv_swap o k w2
                have hwu3 : IsUnimodular w3 :=
                  (isUnimodular_iff_of_unimodularVectorEquiv
                    (unimodularVectorEquiv_equivalence.trans hw_w2 hw2_w3)).1 hwu
                have hdeg3 : (w3 o).natDegree = n := by
                  have ha_deg : a.natDegree = n + 1 := by
                    simpa [a] using hdegw
                  calc _ = (w2 k).natDegree := by simp [w3]
                    _ = n := by simpa [ha_deg] using hdeg_eq
                have hmonic3 : (w3 o).Monic := by simpa [w3] using hmonic_k
                exact unimodularVectorEquiv_equivalence.trans huw <|
                  unimodularVectorEquiv_equivalence.trans
                    (unimodularVectorEquiv_equivalence.trans hw_w2 hw2_w3) <|
                      ih w3 hwu3 hmonic3 hdeg3
          exact hP (v0 o).natDegree v0 huv0 ho0 rfl
    exact unimodularVectorEquiv_equivalence.trans hv0 main

end horrocks

/-- If $R$ is local and $v(x) \in R[x]^s$ is a unimodular vector one of whose elements is monic,
  then $v(x) \sim v(0)$. -/
theorem cor9 [IsLocalRing R] (v : s → R[X]) (hv : IsUnimodular v)
    (h : ∃ i : s, (v i).Monic) : UnimodularVectorEquiv v (fun i => C ((v i).eval 0)) := by
  rcases subsingleton_or_nontrivial R with hR | hR
  · have hv0 : v = fun i => C ((v i).eval 0) := by
      funext i
      exact Subsingleton.elim _ _
    refine ⟨1, ?_⟩
    simpa using hv0
  -- Get an explicit unimodularity certificate `∑ i, c i * v i = 1`.
  have h1 : (1 : R[X]) ∈ Ideal.span (Set.range v) := by
    rw [hv]
    exact Submodule.mem_top
  rcases (Ideal.mem_span_range_iff_exists_fun).1 h1 with ⟨c, hc⟩
  -- Evaluate at `0` to get a relation in `R`.
  let ev0 : R[X] →+* R := Polynomial.evalRingHom 0
  have hc0 : (∑ i : s, ev0 (c i) * ev0 (v i)) = 1 := by
    simpa [map_sum, map_mul] using congrArg ev0 hc
  -- Over a local ring, not all `v i` can evaluate into the maximal ideal.
  let m : Ideal R := IsLocalRing.maximalIdeal R
  have hex : ∃ o : s, ev0 (v o) ∉ m := by
    by_contra hno
    have hall : ∀ i : s, ev0 (v i) ∈ m := by
      intro i
      by_contra hi
      exact hno ⟨i, hi⟩
    have hsum_mem : (∑ i : s, ev0 (c i) * ev0 (v i)) ∈ m := by
      refine m.sum_mem ?_
      intro i _
      exact m.mul_mem_left _ (hall i)
    have : (1 : R) ∈ m := by simpa [hc0] using hsum_mem
    exact (Ideal.ne_top_iff_one m).1 (IsLocalRing.maximalIdeal.isMaximal R).ne_top this
  rcases hex with ⟨o, ho_not_mem⟩
  have hunit0 : IsUnit (ev0 (v o)) := by
    have : ev0 (v o) ∉ IsLocalRing.maximalIdeal R := by simpa [m] using ho_not_mem
    exact IsLocalRing.notMem_maximalIdeal.1 this
  -- Let `v(0)` be the constant polynomial vector.
  let v0 : s → R[X] := fun i => C (ev0 (v i))
  -- `v(0)` is also equivalent to `e_o` since the `o`-th component is a unit.
  have hv0_to_e : UnimodularVectorEquiv v0 (fun i => if i = o then 1 else 0) := by
    have hunitC : IsUnit (v0 o) := by
      simpa [v0] using hunit0.map Polynomial.C
    rcases hunitC with ⟨u, hu⟩
    exact unimodularVectorEquiv_equivalence.trans
      (unimodularVectorEquiv_update_mul_isUnit o (↑(u⁻¹) : R[X]) (by simp) v0)
        (unimodularVectorEquiv_stdBasis_of_eq_one o
          (Function.update v0 o ((↑(u⁻¹) : R[X]) * v0 o)) (by simp [Function.update, hu.symm]))
  simpa [v0, ev0] using unimodularVectorEquiv_equivalence.trans (horrocks o v hv h)
    (unimodularVectorEquiv_equivalence.symm hv0_to_e)

open Bivariate

variable {R : Type*} [CommRing R] [IsDomain R] {s : Type*} [Fintype s] [DecidableEq s]

/-- Suppose $v(x) \sim v(0)$ over the localization $R_S[x]$. Then there exists a $c \in S$ such
  that $v(x) \sim v(x + cy)$ over $R[x, y]$. -/
theorem lem10 {S : Submonoid R} (hs : S ≤ nonZeroDivisors R) (v : s → R[X])
    (h : UnimodularVectorEquiv (fun i => (v i).map (algebraMap R (Localization S)))
      (fun i => C (algebraMap R (Localization S) ((v i).eval 0)))) :
    ∃ c : S, UnimodularVectorEquiv (fun i => C (v i))
      (fun i => (v i).eval₂ ((C : R[X] →+* R[X][Y]).comp C) (C X + (c : R) • Y)) := by
  rcases h with ⟨M, hM⟩
  let Sx : Submonoid R[X] := S.map C
  let Sxy : Submonoid R[X][Y] := Sx.map (C : R[X] →+* R[X][Y])
  let : IsLocalization Sx (Localization S)[X] := by
    simpa [Sx] using (Polynomial.isLocalization S (Localization S))
  let : IsLocalization Sxy ((Localization S)[X][Y]) := by
    simpa [Sxy] using (Polynomial.isLocalization Sx (Localization S)[X])
  rcases IsLocalization.exist_integer_multiples_of_finite Sxy (fun ij : s × s => W S M ij.1 ij.2)
    with ⟨b, hb⟩
  rcases b.property with ⟨rX, hrX, hrXb⟩
  rcases hrX with ⟨rR, hrR, hrRC⟩
  let c : S := ⟨rR, hrR⟩
  have hrXb : (C (C (c : R)) : R[X][Y]) = (b : R[X][Y]) :=
    (congrArg (C : R[X] →+* R[X][Y]) hrRC).trans <| by simpa [c] using hrXb
  have hb : ∀ ij : s × s, IsLocalization.IsInteger R[X][Y]
      ((C (C (c : R)) : R[X][Y]) • W S M ij.1 ij.2) := by
    intro ij
    simpa [hrXb, Algebra.smul_def] using hb ij
  have hc : ∀ i j : s,
      IsLocalization.IsInteger R[X][Y] ((C (C (c : R)) : R[X][Y]) • σA c (W S M i j)) := by
    intro i j
    have hfix : σA c (C (C ((algebraMap R (Localization S)) (c : R)))) =
        (C (C ((algebraMap R (Localization S)) (c : R)))) := by
      simp only [σA, algebraMap_smul, coe_eval₂RingHom, eval₂_C]
    simpa only [Algebra.smul_def, algebraMap_def, coe_mapRingHom, map_C, map_mul, hfix] using
      isInteger_σA c (hb (i, j))
  have hmulVec : ((U hs M hc)⁻¹.1).mulVec (fun i => C (v i)) = _ := hU hs v M hM hc
  exact ⟨c, (U hs M hc)⁻¹, by simpa only [Matrix.coe_units_inv] using hmulVec⟩

noncomputable section cor11

abbrev cor11ι : R →+* R[X][Y] := (C : R[X] →+* R[X][Y]).comp C

abbrev cor11vx (v : s → R[X]) : s → R[X][Y] := fun i => C (v i)

/-- The vector `v(x + qy)` in `R[X][Y]`. -/
abbrev cor11vxy (v : s → R[X]) (q : R) : s → R[X][Y] :=
  fun i => (v i).eval₂ cor11ι (C X + q • Y)

omit [IsDomain R] in
lemma cor11_hAlg : algebraMap R R[X][Y] = cor11ι := by
  ext r
  simp [cor11ι]

/-- The ideal generated by the coordinates of `M.mulVec v` agrees with the ideal generated by the
coordinates of `v` when `M ∈ GL`. (Ring-level version.) -/
theorem ideal_span_range_mulVec_ring {A : Type*} [CommRing A] (M : Matrix.GeneralLinearGroup s A)
    (v : s → A) : Ideal.span (Set.range (M.1.mulVec v)) = Ideal.span (Set.range v) := by
  -- First show `span (range (M.mulVec v)) ≤ span (range v)` for all `M`.
  have span_mulVec_le (N : Matrix.GeneralLinearGroup s A) (v : s → A) :
      Ideal.span (Set.range (N.1.mulVec v)) ≤ Ideal.span (Set.range v) := by
    let I : Ideal A := Ideal.span (Set.range v)
    refine Ideal.span_le.2 ?_
    rintro _ ⟨i, rfl⟩
    have hvj (j : s) : v j ∈ I := Ideal.subset_span ⟨j, rfl⟩
    have hterm (j : s) : N.1 i j * v j ∈ I := by
      simpa [mul_comm] using I.mul_mem_left (N.1 i j) (hvj j)
    simpa [Matrix.mulVec, dotProduct, I] using I.sum_mem (fun j _ => hterm j)
  refine le_antisymm (span_mulVec_le M v) ?_
  simpa only [Matrix.coe_units_inv, Matrix.mulVec_mulVec, Matrix.isUnits_det_units,
    Matrix.nonsing_inv_mul, Matrix.one_mulVec] using span_mulVec_le (M⁻¹) (M.1.mulVec v)

/-- `IsUnimodular` is invariant under `UnimodularVectorEquiv`. (Ring-level version.) -/
theorem isUnimodular_iff_of_unimodularVectorEquiv_ring {A : Type*} [CommRing A] {v w : s → A}
    (hvw : UnimodularVectorEquiv v w) : IsUnimodular v ↔ IsUnimodular w := by
  rcases hvw with ⟨M, rfl⟩
  unfold IsUnimodular
  simp [ideal_span_range_mulVec_ring M v]

/-- The ideal of `q : R` such that `v(x + qy) ∼ v(x)` in `R[X][Y]`. -/
def cor11IdealCarrier (v : s → R[X]) : Set R :=
  {q | UnimodularVectorEquiv (cor11vx v) (cor11vxy v q)}

omit [IsDomain R] in
/-- `0 ∈ cor11IdealCarrier v`. -/
lemma cor11Ideal_zero_mem (v : s → R[X]) : (0 : R) ∈ cor11IdealCarrier v := by
  have hC : (Polynomial.eval₂RingHom cor11ι (C X)) = (C : R[X] →+* R[X][Y]) := by
    refine Polynomial.ringHom_ext' ?_ ?_
    · ext r
      simp [cor11ι]
    · simp [cor11ι]
  have h0 : cor11vxy v 0 = cor11vx v := by
    funext i
    simpa [cor11vxy, cor11vx] using  congrArg (fun f : R[X] →+* R[X][Y] => f (v i)) hC
  simpa [cor11IdealCarrier, h0] using unimodularVectorEquiv_equivalence.refl (cor11vx v)

lemma cor11Ideal_add_mem (v : s → R[X]) {a b : R} (ha : a ∈ cor11IdealCarrier v)
    (hb : b ∈ cor11IdealCarrier v) :
    a + b ∈ cor11IdealCarrier v := by
  let shift : R[X][Y] →+* R[X][Y] := eval₂RingHom (Polynomial.eval₂RingHom cor11ι (C X + b • Y)) Y
  have hx : (fun i : s => shift (cor11vx v i)) = cor11vxy v b := by
    funext i
    simp only [shift, cor11vx, cor11vxy, eval₂_C, coe_eval₂RingHom]
  have hxy : (fun i : s => shift (cor11vxy v a i)) = cor11vxy v (a + b) := by
    funext i
    have hcoeff : shift.comp cor11ι = cor11ι := by
      ext r
      dsimp [shift, cor11ι]
      simp only [eval₂_C, coe_eval₂RingHom, RingHom.coe_comp, Function.comp_apply]
    have hCX : shift (C X) = C X + b • Y := by
      dsimp [shift]
      simp only [eval₂_C, coe_eval₂RingHom, eval₂_X]
    have hY : shift Y = Y := by
      dsimp [shift]
      simp only [eval₂_X]
    have hιa : shift (cor11ι a) = cor11ι a := by
      have := congrArg (fun f : R →+* R[X][Y] => f a) hcoeff
      simpa [RingHom.comp_apply] using this
    have haY : shift (a • Y) = a • Y := by
      calc shift (a • Y) = shift (cor11ι a * Y) := by simp [Algebra.smul_def, cor11_hAlg]
        _ = shift (cor11ι a) * shift Y := by simp
        _ = shift (cor11ι a) * Y := by simp [hY]
        _ = cor11ι a * Y := by simpa [hιa]
        _ = a • Y := by simp [Algebra.smul_def, cor11_hAlg]
    have hX : shift (C X + a • Y) = C X + (a + b) • Y := by
      calc shift (C X + a • Y) = shift (C X) + shift (a • Y) := by simp only [map_add]
        _ = (C X + b • Y) + a • Y := by simp only [hCX, haY]
        _ = C X + (a + b) • Y := by simp only [add_comm, add_smul, add_assoc]
    have := Polynomial.hom_eval₂ (v i) cor11ι shift (C X + a • Y)
    simpa only [cor11vxy, hcoeff, hX] using this
  have hab : UnimodularVectorEquiv (cor11vxy v b) (cor11vxy v (a + b)) := by
    simpa [hx, hxy] using unimodularVectorEquiv_map shift ha
  exact (unimodularVectorEquiv_equivalence).trans hb hab

omit [IsDomain R] in
/-- `cor11IdealCarrier v` is closed under scalar multiplication (i.e. multiplication in `R`). -/
lemma cor11Ideal_smul_mem (v : s → R[X]) (r : R) {a : R} (ha : a ∈ cor11IdealCarrier v) :
    r * a ∈ cor11IdealCarrier v := by
  let scaleY : R[X][Y] →+* R[X][Y] :=
    Polynomial.eval₂RingHom (C : R[X] →+* R[X][Y]) (r • Y)
  have hx : (fun i : s => scaleY (cor11vx v i)) = cor11vx v := by
    funext i
    dsimp [scaleY, cor11vx]
    simp only [eval₂_C]
  have hxy : (fun i : s => scaleY (cor11vxy v a i)) = cor11vxy v (r * a) := by
    funext i
    have hcoeff : scaleY.comp cor11ι = cor11ι := by
      ext x
      dsimp [scaleY, cor11ι]
      simp only [eval₂_C]
    have hCX : scaleY (C X) = C X := by
      dsimp [scaleY]
      simp only [eval₂_C]
    have hY : scaleY Y = r • Y := by
      dsimp [scaleY]
      simp only [eval₂_X]
    have hιa : scaleY (cor11ι a) = cor11ι a := by
      simpa [RingHom.comp_apply] using congrArg (fun f : R →+* R[X][Y] => f a) hcoeff
    have hYa : scaleY (a • Y) = (r * a) • Y := by
      have hιr : (r : R) • Y = cor11ι r * Y := by simp [Algebra.smul_def, cor11_hAlg, cor11ι]
      calc
        _ = scaleY (cor11ι a) * scaleY Y := by
          simp only [Algebra.smul_def, cor11_hAlg, RingHom.coe_comp, Function.comp_apply, map_mul]
        _ = cor11ι a * (cor11ι r * Y) := by rw [hY, hιa, hιr]
        _ = (cor11ι a * cor11ι r) * Y := by rw [mul_assoc]
        _ = cor11ι (a * r) * Y := by rw [map_mul]
        _ = cor11ι (r * a) * Y := by
          simp only [mul_comm, RingHom.coe_comp, Function.comp_apply, map_mul]
        _ = (r * a) • Y := by simp [Algebra.smul_def, cor11_hAlg, cor11ι]
    have hX : scaleY (C X + a • Y) = C X + (r * a) • Y := by
      simp only [map_add, hCX, hYa]
    have := Polynomial.hom_eval₂ (v i) cor11ι scaleY (C X + a • Y)
    simpa only [cor11vxy, hcoeff, hX] using this
  simpa [cor11IdealCarrier, hx, hxy] using unimodularVectorEquiv_map scaleY ha

def cor11Ideal (v : s → R[X]) : Ideal R :=
  { carrier := cor11IdealCarrier v
    zero_mem' := cor11Ideal_zero_mem v
    add_mem' := cor11Ideal_add_mem v
    smul_mem' := cor11Ideal_smul_mem v }

theorem cor11Ideal_eq_top (v : s → R[X]) (hv : IsUnimodular v) (h : ∃ i : s, (v i).Monic) :
    cor11Ideal v = ⊤ := by
  let I : Ideal R := cor11Ideal v
  by_contra hI
  rcases Ideal.exists_le_maximal I hI with ⟨m, hm, hIm⟩
  let S : Submonoid R := Ideal.primeCompl m
  have hS0 : (0 : R) ∉ S := by simp [S, Ideal.primeCompl]
  have hs : S ≤ nonZeroDivisors R := le_nonZeroDivisors_of_noZeroDivisors hS0
  let vS : s → (Localization S)[X] := fun i => (v i).map (algebraMap R (Localization S))
  have hvS : IsUnimodular vS := by
    have h1 : (1 : R[X]) ∈ Ideal.span (Set.range v) := by
      rw [hv]
      exact Submodule.mem_top
    rcases (Ideal.mem_span_range_iff_exists_fun).1 h1 with ⟨c, hc⟩
    let fX : R[X] →+* (Localization S)[X] := Polynomial.mapRingHom (algebraMap R (Localization S))
    have hc' : (∑ i : s, fX (c i) * fX (v i)) = 1 := by
      simpa [map_sum, map_mul, fX] using congrArg fX hc
    have : (1 : (Localization S)[X]) ∈ Ideal.span (Set.range vS) := by
      refine (Ideal.mem_span_range_iff_exists_fun).2 ?_
      refine ⟨fun i => fX (c i), ?_⟩
      simpa [vS, map_sum, map_mul, fX] using hc'
    exact (Ideal.eq_top_iff_one _).2 this
  have hmonicS : ∃ i : s, (vS i).Monic := by
    rcases h with ⟨i, hi⟩
    refine ⟨i, ?_⟩
    simpa [vS] using hi.map (algebraMap R (Localization S))
  have : IsLocalRing (Localization S) := by
    simpa [S, Localization.AtPrime] using Localization.AtPrime.isLocalRing m
  have hloc : UnimodularVectorEquiv vS
      (fun i => C (algebraMap R (Localization S) ((v i).eval 0))) := by
    have hev0 : (fun i => C ((vS i).eval 0)) = fun i => C (algebraMap R (Localization S) ((v i).eval 0)) := by
      funext i
      have : (vS i).eval 0 = algebraMap R (Localization S) ((v i).eval 0) := by
        simpa [vS] using (Polynomial.eval_zero_map (algebraMap R (Localization S)) (v i))
      simp [this]
    simpa [hev0] using cor9 vS hvS hmonicS
  rcases lem10 hs v hloc with ⟨c, hc⟩
  exact c.2 (hIm hc)

/-- Suppose $R$ is any ring, and $v(x) \in R[x]^s$ is a unimodular vector one of whose
  leading coefficients is one. Then $v(x) \sim v(0)$. -/
theorem cor11 (v : s → R[X]) (hv : IsUnimodular v) (h : ∃ i : s, (v i).Monic) :
    UnimodularVectorEquiv v (fun i => C ((v i).eval 0)) :=
  let I : Ideal R := cor11Ideal v
  have hI : I = ⊤ := cor11Ideal_eq_top v hv h
  have h1 : (1 : R) ∈ I := by simp [hI]
  have hI1 : UnimodularVectorEquiv (cor11vx v) (cor11vxy v 1) := h1
  let ev0 : R[X] →+* R[X] := Polynomial.eval₂RingHom C 0
  let evXY : R[X][Y] →+* R[X] := Polynomial.eval₂RingHom ev0 X
  have hev0 (i : s) : ev0 (v i) = C ((v i).eval 0) := by
    simp [ev0, Polynomial.coeff_zero_eq_eval_zero]
  have hevXY_vx : (fun i => evXY (cor11vx v i)) = fun i => C ((v i).eval 0) := by
    funext i
    simp [evXY, ev0, hev0 i]
  have hevXY_vxy : (fun i => evXY (cor11vxy v 1 i)) = v := by
    funext i
    have hcoeff : evXY.comp cor11ι = C := by
      ext r
      simp [evXY, ev0, cor11ι]
    have hX : evXY (C X + Y) = X := by simp [evXY, ev0]
    have hhom := Polynomial.hom_eval₂ (v i) cor11ι evXY (C X + Y)
    have : evXY (cor11vxy v 1 i) = (v i).eval₂ C X := by
      simpa [cor11vxy, cor11ι, one_smul, hcoeff, hX] using hhom
    simpa [Polynomial.eval₂_C_X] using this
  have hmain : UnimodularVectorEquiv (fun i => C ((v i).eval 0)) v := by
    simpa [hevXY_vx, hevXY_vxy] using unimodularVectorEquiv_map evXY hI1
  unimodularVectorEquiv_equivalence.symm hmain

end cor11
