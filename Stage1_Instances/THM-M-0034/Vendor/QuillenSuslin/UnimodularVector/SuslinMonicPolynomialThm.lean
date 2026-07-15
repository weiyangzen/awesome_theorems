/-
Copyright (c) 2026 Yongle Hu. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yongle Hu
-/
/- Port notice: modified for the repository's pinned Lean 4.29/mathlib APIs.
The exact compatibility edits are recorded in `../../../PORT_PROVENANCE.md`. -/
import Mathlib.Algebra.Polynomial.Bivariate
import Mathlib.RingTheory.KrullDimension.Field
import Mathlib.RingTheory.KrullDimension.Polynomial

open Polynomial Bivariate

open scoped BigOperators

namespace MvPolynomial

variable (R : Type*) [CommSemiring R]

/-- The algebra isomorphism between multivariable polynomials in `Fin (n + 1)` and polynomials over
multivariable polynomials in `Fin n`, singling out the last variable. -/
noncomputable def finSuccEquivLast (n : ℕ) :
    MvPolynomial (Fin (n + 1)) R ≃ₐ[R] Polynomial (MvPolynomial (Fin n) R) :=
  (renameEquiv R _root_.finSuccEquivLast).trans (optionEquivLeft R (Fin n))

@[simp]
lemma finSuccEquivLast_X_castSucc (n : ℕ) (i : Fin n) :
    finSuccEquivLast R n (X (Fin.castSucc i)) = Polynomial.C (X i) := by
  simp [finSuccEquivLast, _root_.finSuccEquivLast_castSucc]

@[simp]
lemma finSuccEquivLast_X_last (n : ℕ) :
    finSuccEquivLast R n (X (Fin.last n)) = Polynomial.X := by
  simp [finSuccEquivLast, _root_.finSuccEquivLast_last]

@[simp]
lemma finSuccEquivLast_symm_X (n : ℕ) :
    (finSuccEquivLast R n).symm Polynomial.X = X (Fin.last n) := by
  simpa [finSuccEquivLast_X_last R n] using (finSuccEquivLast R n).symm_apply_apply (X (Fin.last n))

@[simp]
lemma finSuccEquivLast_symm_C_X (n : ℕ) (i : Fin n) :
    (finSuccEquivLast R n).symm (Polynomial.C (X i)) = X (Fin.castSucc i) := by
  simpa [finSuccEquivLast_X_castSucc R n i] using
    (finSuccEquivLast R n).symm_apply_apply (X (Fin.castSucc i))

end MvPolynomial

namespace Ideal

variable {A : Type*} [CommRing A]

lemma leadingCoeff_mono {I J : Ideal A[X]} (hIJ : I ≤ J) : I.leadingCoeff ≤ J.leadingCoeff := by
  intro x hx
  rcases (I.mem_leadingCoeff x).1 hx with ⟨p, hpI, rfl⟩
  exact (J.mem_leadingCoeff _).2 ⟨p, hIJ hpI, rfl⟩

lemma leadingCoeff_map_C (p : Ideal A) : (Ideal.map C p).leadingCoeff = p := by
  ext x
  constructor
  · intro hx
    rcases ((Ideal.map C p).mem_leadingCoeff x).1 hx with ⟨f, hf, rfl⟩
    simpa using p.mem_map_C_iff.1 hf f.natDegree
  · intro hx
    exact ((Ideal.map C p).mem_leadingCoeff x).2 ⟨C x,
      p.mem_map_C_iff.2 (by
        intro n
        cases n <;> simp [hx]),
      by simp⟩

@[simp]
lemma leadingCoeff_top : ((⊤ : Ideal A[X]).leadingCoeff : Ideal A) = ⊤ := by
  ext x
  constructor
  · intro _
    exact Submodule.mem_top
  · intro _
    exact (Ideal.mem_leadingCoeff _ x).2 ⟨C x, Submodule.mem_top, by simp⟩

variable [IsDomain A]

lemma leadingCoeff_mul_le (I J : Ideal A[X]) :
    I.leadingCoeff * J.leadingCoeff ≤ (I * J).leadingCoeff := by
  refine (Ideal.mul_le).2 ?_
  intro a ha b hb
  rcases (I.mem_leadingCoeff a).1 ha with ⟨p, hpI, hp⟩
  rcases (J.mem_leadingCoeff b).1 hb with ⟨q, hqJ, hq⟩
  -- The product `p*q` lies in `I*J` and has leading coefficient `a*b`.
  refine ((I * J).mem_leadingCoeff (a * b)).2 ⟨p * q, Ideal.mul_mem_mul hpI hqJ, ?_⟩
  simp [Polynomial.leadingCoeff_mul, hp, hq]

lemma leadingCoeff_pow_le (I : Ideal A[X]) : ∀ n : ℕ, I.leadingCoeff ^ n ≤ (I ^ n).leadingCoeff
   | 0 => by
       simp [pow_zero, Ideal.one_eq_top, leadingCoeff_top]
   | n + 1 => by
       have h₁ : I.leadingCoeff ^ n ≤ (I ^ n).leadingCoeff := leadingCoeff_pow_le I n
       have hmul : (I.leadingCoeff ^ n) * I.leadingCoeff ≤ ((I ^ n) * I).leadingCoeff := by
         refine le_trans (Ideal.mul_mono_left h₁) ?_
         simpa [mul_assoc] using leadingCoeff_mul_le (I ^ n) I
       simpa [pow_succ] using hmul

lemma leadingCoeff_finset_prod_le (s : Finset (Ideal A[X])) :
    (s.prod fun P => P.leadingCoeff) ≤ (s.prod id).leadingCoeff := by
  classical refine Finset.induction_on s ?_ ?_
  · simp
  · intro P s hP hs
    have h : P.leadingCoeff * (s.prod id).leadingCoeff ≤ (P * s.prod id).leadingCoeff := by
      simpa [mul_assoc] using leadingCoeff_mul_le P (s.prod id)
    simpa [Finset.prod_insert, hP, Finset.prod_insert, hP, mul_assoc, mul_left_comm, mul_comm] using
      le_trans (Ideal.mul_mono_right hs) h

lemma height_le_one_of_isPrime_comap_C_eq_bot (Q : Ideal A[X]) [Q.IsPrime]
    (hQ : Ideal.comap C Q = ⊥) :
    Q.height ≤ 1 := by
  let K := FractionRing A
  let M : Submonoid A[X] := Submonoid.map C (nonZeroDivisors A)
  have hdisj : Disjoint (M : Set A[X]) (Q : Set A[X]) := by
    refine Set.disjoint_left.2 ?_
    intro x hxM hxQmem
    rcases (Submonoid.mem_map).1 hxM with ⟨a, ha, rfl⟩
    have : a ∈ (Ideal.comap C Q) := by
      simpa [Ideal.mem_comap] using hxQmem
    have : a = 0 := by
      simpa [hQ] using this
    have ha0 : (a : A) ≠ 0 := (mem_nonZeroDivisors_iff_ne_zero).1 ha
    exact ha0 this
  let : Algebra A[X] K[X] := Polynomial.algebra A K
  let : IsLocalization M K[X] := Polynomial.isLocalization (nonZeroDivisors A) K
  have hheight : (Ideal.map (algebraMap A[X] K[X]) Q).height = Q.height := by
    simpa [M] using IsLocalization.height_map_of_disjoint M Q hdisj
  have hne_top : Ideal.map (algebraMap A[X] K[X]) Q ≠ (⊤ : Ideal K[X]) :=
    have hprime : (Ideal.map (algebraMap A[X] K[X]) Q).IsPrime :=
      IsLocalization.isPrime_of_isPrime_disjoint M K[X] Q inferInstance hdisj
    Ideal.IsPrime.ne_top hprime
  have hdim : ringKrullDim K[X] = (1 : WithBot ℕ∞) := by
    simp [Polynomial.ringKrullDim_of_isNoetherianRing]
  calc _ = (Ideal.map (algebraMap A[X] K[X]) Q).height := by simpa using hheight.symm
    _ ≤ 1 := (WithBot.coe_le_coe).1 <| by simpa only [WithBot.coe_one, WithBot.coe_le_one, hdim]
      using (Ideal.map (algebraMap A[X] K[X]) Q).height_le_ringKrullDim_of_ne_top hne_top

variable [IsNoetherianRing A]

lemma height_le_leadingCoeff_of_isPrime (P : Ideal A[X]) [P.IsPrime] :
    P.height ≤ P.leadingCoeff.height := by
  -- Let `p = P ∩ A`.
  let p : Ideal A := Ideal.comap C P
  have : p.IsPrime := Ideal.comap_isPrime C P
  have hp_le : p ≤ P.leadingCoeff := by
    intro a ha
    exact (P.mem_leadingCoeff a).2 ⟨C a, ha, by simp⟩
  have : P.LiesOver p := ⟨by
    ext
    rfl⟩
  have hheight : P.height =
      p.height + (Ideal.map (Ideal.Quotient.mk (Ideal.map (algebraMap A A[X]) p)) P).height := by
    simpa [Ideal.under_def] using Ideal.height_eq_height_add_of_liesOver_of_hasGoingDown p P
  by_cases hPeq : P = Ideal.map C p
  · have hQ : Ideal.map (Ideal.Quotient.mk (Ideal.map (algebraMap A A[X]) p)) P = ⊥ := by
      rw [hPeq]
      simpa only [Polynomial.algebraMap_eq] using
        Ideal.map_quotient_self (Ideal.map C p)
    have hI0_ne_top : Ideal.map (algebraMap A A[X]) p ≠ ⊤ := by
      simpa only [Polynomial.algebraMap_eq] using
        (Ideal.IsPrime.ne_top (Ideal.isPrime_map_C_iff_isPrime p |>.2 inferInstance))
    letI : Nontrivial (A[X] ⧸ (Ideal.map (algebraMap A A[X]) p)) :=
      Ideal.Quotient.nontrivial hI0_ne_top
    have hp' : P.height = p.height := by
      rw [hheight, hQ, Ideal.height_bot, add_zero]
    simpa [hp'] using Ideal.height_mono hp_le
  · let I0 : Ideal A[X] := Ideal.map C p
    let q : A[X] →+* (A[X] ⧸ I0) := Ideal.Quotient.mk I0
    let Q : Ideal (A[X] ⧸ I0) := Ideal.map q P
    have hI0_le : I0 ≤ P := by simpa [I0] using Ideal.map_comap_le
    have hker : RingHom.ker q ≤ P := by
      simpa [q, Ideal.mk_ker] using hI0_le
    have : Q.IsPrime := by
      have hQprime : (Ideal.map q P).IsPrime :=
        P.map_isPrime_of_surjective Ideal.Quotient.mk_surjective hker
      simpa [Q] using hQprime
    have hQle : Q.height ≤ 1 := by
      let e : (A ⧸ p)[X] ≃+* (A[X] ⧸ I0) :=
        p.polynomialQuotientEquivQuotientPolynomial
      have hcomap : Ideal.comap (C : (A ⧸ p) →+* (A ⧸ p)[X]) (Ideal.comap e.toRingHom Q) =
          (⊥ : Ideal (A ⧸ p)) := by
        ext a
        have hEq : e (C a) ∈ Q ↔ a = 0 := by
          refine Quotient.inductionOn a ?_
          intro a0
          have hCe : e (C (Ideal.Quotient.mk p a0)) = q (C a0) := by
            simpa [I0, q] using p.polynomialQuotientEquivQuotientPolynomial_map_mk (C a0)
          have hmem : q (C a0) ∈ Q ↔ C a0 ∈ P := by
            constructor
            · intro hx
              rcases (Ideal.mem_map_iff_of_surjective q Ideal.Quotient.mk_surjective).1 hx
                with ⟨y, hyP, hyEq⟩
              have hySub : y - C a0 ∈ I0 := Ideal.Quotient.eq.1 hyEq
              have hySubP : y - C a0 ∈ P := hI0_le hySub
              have : y - (y - C a0) ∈ P := Ideal.sub_mem P hyP hySubP
              simpa [sub_sub] using this
            · intro hx
              exact Ideal.mem_map_of_mem q hx
          have hp0 : C a0 ∈ P ↔ a0 ∈ p := by simp [p, Ideal.mem_comap]
          have hq0 : (Ideal.Quotient.mk p a0 = (0 : A ⧸ p)) ↔ a0 ∈ p := by
            simpa using Ideal.Quotient.eq_zero_iff_mem
          calc e (C (Ideal.Quotient.mk p a0)) ∈ Q ↔ q (C a0) ∈ Q := by simp [hCe]
            _ ↔ C a0 ∈ P := hmem
            _ ↔ a0 ∈ p := hp0
            _ ↔ (Ideal.Quotient.mk p a0 = (0 : A ⧸ p)) := hq0.symm
        simp only [RingEquiv.toRingHom_eq_coe, mem_comap, RingHom.coe_coe, hEq, Submodule.mem_bot]
      have hcomap_height : (Ideal.comap e.toRingHom Q).height = Q.height :=
        e.height_comap Q
      calc _ = (Ideal.comap e.toRingHom Q).height := by simpa using hcomap_height.symm
        _ ≤ 1 := height_le_one_of_isPrime_comap_C_eq_bot (Ideal.comap e.toRingHom Q) hcomap
    -- `P.height = p.height + Q.height ≤ p.height + 1`.
    have hP_le : P.height ≤ p.height + 1 := by
      have hheight' : P.height = p.height + Q.height := by simpa [Q, q, I0] using hheight
      rw [hheight']
      exact add_le_add_right hQle p.height
    have hp_lt : p < P.leadingCoeff := by
      refine lt_of_le_of_ne hp_le ?_
      -- Choose a polynomial of minimal `natDegree` in `P \ I0`.
      have hex : ∃ f : A[X], f ∈ P ∧ f ∉ I0 := by
        by_contra h
        have hle : P ≤ I0 := by
          intro f hfP
          by_contra hfI0
          exact h ⟨f, hfP, hfI0⟩
        exact hPeq (by simpa [I0] using le_antisymm hle hI0_le)
      let Pred : ℕ → Prop := fun n => ∃ f : A[X], f ∈ P ∧ f ∉ I0 ∧ f.natDegree = n
      have hNat : ∃ n, Pred n := by
        rcases hex with ⟨f, hfP, hfI0⟩
        exact ⟨f.natDegree, f, hfP, hfI0, rfl⟩
      classical
      let n0 : ℕ := Nat.find hNat
      have hn0 : Pred n0 := Nat.find_spec hNat
      rcases hn0 with ⟨f0, hf0P, hf0I0, hf0deg⟩
      have hf0_ne0 : f0 ≠ 0 := by
        intro hf0z
        apply hf0I0
        simp [hf0z]
      have hmin : ∀ m : ℕ, m < n0 → ¬ Pred m := ((n0.find_eq_iff hNat).1 rfl).2
      have hLCnot : f0.leadingCoeff ∉ p := by
        intro hLC
        let d : ℕ := f0.natDegree
        let t : A[X] := C f0.leadingCoeff * Polynomial.X ^ d
        let g : A[X] := f0 - t
        have htP : t ∈ P :=
          P.mul_mem_right (Polynomial.X ^ d) <| by simpa [p, Ideal.mem_comap] using hLC
        have hgP : g ∈ P := by simpa [g] using P.sub_mem hf0P htP
        have htI0 : t ∈ I0 :=
          I0.mul_mem_right (Polynomial.X ^ d) (Ideal.mem_map_of_mem C hLC)
        have hgI0 : g ∉ I0 := by
          intro hg
          exact hf0I0 <| by simpa [g, sub_add_cancel] using I0.add_mem hg htI0
        have hdeg_lt : g.degree < f0.degree := by
          have hdeg_f0 : f0.degree = (d : WithBot ℕ) := by
            simpa [hf0deg, d] using (Polynomial.degree_eq_natDegree hf0_ne0)
          have hdeg_t : t.degree = (d : WithBot ℕ) := by
            have hLC0 : f0.leadingCoeff ≠ 0 := (Polynomial.leadingCoeff_ne_zero).2 hf0_ne0
            simpa [t] using (Polynomial.degree_C_mul_X_pow d hLC0)
          have hLCeq : f0.leadingCoeff = t.leadingCoeff := by simp [t]
          simpa [g] using Polynomial.degree_sub_lt (by simp [hdeg_f0, hdeg_t]) hf0_ne0 hLCeq
        have hnat_lt : g.natDegree < n0 := by
          by_cases hg0 : g = 0
          · have hn0' : n0 ≠ 0 := by
              intro hn0z
              have hd0 : d = 0 := by simp [d, hf0deg, hn0z]
              have hf0_eq_t : f0 = t := sub_eq_zero.mp <| by simpa [g] using hg0
              exact hf0I0 <| by simpa [hf0_eq_t] using htI0
            simpa [hg0] using Nat.pos_of_ne_zero hn0'
          · simpa [hf0deg, d] using Polynomial.natDegree_lt_natDegree hg0 hdeg_lt
        exact (hmin g.natDegree hnat_lt) ⟨g, hgP, hgI0, rfl⟩
      have hLCmem : f0.leadingCoeff ∈ P.leadingCoeff :=
        (P.mem_leadingCoeff f0.leadingCoeff).2 ⟨f0, hf0P, rfl⟩
      intro hEq
      exact hLCnot <| by simpa [hEq] using hLCmem
    have hp_height_le : p.height + 1 ≤ P.leadingCoeff.height := by
      refine le_iInf₂ ?_
      intro q hq
      have : q.IsPrime := Ideal.minimalPrimes_isPrime hq
      have hpq : p < q := lt_of_lt_of_le hp_lt (hq.1.2)
      have : p.primeHeight + 1 ≤ q.primeHeight := Ideal.primeHeight_add_one_le_of_lt hpq
      simpa [p.height_eq_primeHeight, q.height_eq_primeHeight] using this
    exact le_trans hP_le hp_height_le

theorem height_le_height_leadingCoeff (I : Ideal A[X]) : I.height ≤ I.leadingCoeff.height := by
  by_cases hI : I = ⊤
  · subst hI
    simp
  have hfin : I.minimalPrimes.Finite := Ideal.finite_minimalPrimes_of_isNoetherianRing A[X] I
  let Pset : Finset (Ideal A[X]) := hfin.toFinset
  let J : Ideal A[X] := Pset.prod id
  have hJ_le_rad : J ≤ I.radical := by
    have hprod : J ≤ Pset.inf id := Ideal.prod_le_inf
    have hinf : (Pset.inf id : Ideal A[X]) = sInf I.minimalPrimes := by
      have : Pset = I.minimalPrimes := by simp [Pset]
      simp [Finset.inf_id_eq_sInf, this]
    simpa [J, hinf, Ideal.sInf_minimalPrimes] using hprod
  have hJfg : J.FG := Ideal.fg_of_isNoetherianRing J
  rcases Ideal.exists_pow_le_of_le_radical_of_fg hJ_le_rad hJfg with ⟨N, hJN⟩
  refine le_iInf fun q => le_iInf fun hq => ?_
  have : q.IsPrime := Ideal.minimalPrimes_isPrime hq
  have hLC : (Pset.prod fun P => P.leadingCoeff) ^ N ≤ I.leadingCoeff := by
    have h₁ : (Pset.prod fun P => P.leadingCoeff) ≤ J.leadingCoeff := by
      simpa [J] using leadingCoeff_finset_prod_le Pset
    have h₂ : (Pset.prod fun P => P.leadingCoeff) ^ N ≤ J.leadingCoeff ^ N := pow_right_mono h₁ N
    have h₃ : J.leadingCoeff ^ N ≤ (J ^ N).leadingCoeff := leadingCoeff_pow_le J N
    exact le_trans (le_trans h₂ h₃) (leadingCoeff_mono hJN)
  have hLCq : (Pset.prod fun P => P.leadingCoeff) ^ N ≤ q := le_trans hLC hq.1.2
  have hLCq' : (Pset.prod fun P => P.leadingCoeff) ≤ q := Ideal.IsPrime.le_of_pow_le hLCq
  rcases (Ideal.IsPrime.prod_le inferInstance).1 (by simpa using hLCq') with ⟨P, hP, hPq⟩
  have hPmin : P ∈ I.minimalPrimes := (Set.Finite.mem_toFinset hfin).1 hP
  have : P.IsPrime := Ideal.minimalPrimes_isPrime hPmin
  have hI_le_P : I.height ≤ P.primeHeight := by simpa [Ideal.height] using (iInf₂_le P hPmin)
  have hP_le : P.primeHeight ≤ q.primeHeight := by
    have hP' : P.height ≤ P.leadingCoeff.height := height_le_leadingCoeff_of_isPrime P
    have hP'' : P.primeHeight ≤ P.leadingCoeff.height := by
      simpa [P.height_eq_primeHeight] using hP'
    simpa [q.height_eq_primeHeight] using le_trans hP'' (Ideal.height_mono hPq)
  exact le_trans hI_le_P hP_le

end Ideal

lemma bivariate_swap_C {A : Type*} [CommSemiring A] (p : A[X]) :
    Polynomial.Bivariate.swap (C p) = Polynomial.map C p :=
  Polynomial.Bivariate.swap_C p

lemma finSuccEquiv_map_finSuccEquivLast_apply {R : Type*} [CommRing R] (n : ℕ)
    (f : MvPolynomial (Fin (n + 2)) R) :
    (mapAlgEquiv (MvPolynomial.finSuccEquivLast R n) (MvPolynomial.finSuccEquiv R (n + 1) f)) =
    Polynomial.Bivariate.swap (mapAlgEquiv (MvPolynomial.finSuccEquiv R n)
      (MvPolynomial.finSuccEquivLast R (n + 1) f)) := by
  let F : MvPolynomial (Fin (n + 2)) R →ₐ[R] Polynomial (Polynomial (MvPolynomial (Fin n) R)) :=
    ((MvPolynomial.finSuccEquiv R (n + 1)).trans
      (Polynomial.mapAlgEquiv (MvPolynomial.finSuccEquivLast R n))).toAlgHom
  let swapR : Polynomial (Polynomial (MvPolynomial (Fin n) R)) ≃ₐ[R] _ :=
    (Polynomial.Bivariate.swap).restrictScalars R
  let G : MvPolynomial (Fin (n + 2)) R →ₐ[R] Polynomial (Polynomial (MvPolynomial (Fin n) R)) :=
    (((MvPolynomial.finSuccEquivLast R (n + 1)).trans
      (Polynomial.mapAlgEquiv (MvPolynomial.finSuccEquiv R n))).trans swapR).toAlgHom
  have hFG : F = G := by
    refine MvPolynomial.algHom_ext ?_
    intro i
    cases i using Fin.lastCases with
    | last =>
      have hlast : MvPolynomial.finSuccEquiv R (n + 1) (MvPolynomial.X (Fin.last (n + 1))) =
          C (MvPolynomial.X (Fin.last n)) := by
        simpa [Fin.succ_last] using MvPolynomial.finSuccEquiv_X_succ (j := Fin.last n)
      have hF : F (MvPolynomial.X (Fin.last (n + 1))) = C X := by
        simp [F, hlast, MvPolynomial.finSuccEquivLast_X_last R n]
      have hG' : G (MvPolynomial.X (Fin.last (n + 1))) = swapR Y := by simp [G]
      have hG : G (MvPolynomial.X (Fin.last (n + 1))) = C X := by
        simpa [hG', swapR] using
          (Polynomial.Bivariate.swap_Y (R := MvPolynomial (Fin n) R))
      simp [hF, hG]
    | cast i =>
      cases i using Fin.cases with
      | zero =>
        have hF : F (MvPolynomial.X (0 : Fin (n + 2))) = Y := by
          simp [F, MvPolynomial.finSuccEquiv_X_zero]
        have hG' : G (MvPolynomial.X (0 : Fin (n + 2))) = swapR (C X) := by
          have h0 : MvPolynomial.finSuccEquivLast R (n + 1) (MvPolynomial.X (0 : Fin (n + 2))) =
              C (MvPolynomial.X (0 : Fin (n + 1))) := by
            simpa using MvPolynomial.finSuccEquivLast_X_castSucc R (n + 1) (0 : Fin (n + 1))
          simp [G, h0, MvPolynomial.finSuccEquiv_X_zero]
        have hG : G (MvPolynomial.X (0 : Fin (n + 2))) = Y := by
          have : swapR (C X) = Y := by
            simpa [swapR] using
              (Polynomial.Bivariate.swap_X (R := MvPolynomial (Fin n) R))
          simp [hG', this]
        simp [hF, hG]
      | succ j =>
        have hF : F (MvPolynomial.X j.castSucc.succ) = C (C (MvPolynomial.X j)) := by
          simp [F, MvPolynomial.finSuccEquiv_X_succ, MvPolynomial.finSuccEquivLast_X_castSucc]
        have hG' : G (MvPolynomial.X j.castSucc.succ) = swapR (C (C (MvPolynomial.X j))) := by
          have hcast : MvPolynomial.finSuccEquivLast R (n + 1) (MvPolynomial.X j.castSucc.succ) =
              C (MvPolynomial.X (Fin.succ j)) := by
            simpa [Fin.castSucc_succ] using
              (MvPolynomial.finSuccEquivLast_X_castSucc R (n + 1) (Fin.succ j))
          simp [G, hcast, MvPolynomial.finSuccEquiv_X_succ]
        have hswap : swapR (C (C (MvPolynomial.X j))) = C (C (MvPolynomial.X j)) := by
          simp only [swapR, AlgEquiv.restrictScalars_apply, bivariate_swap_C, Polynomial.map_C]
        have hG : G (MvPolynomial.X j.castSucc.succ) = C (C (MvPolynomial.X j)) := by
          simp [hG', hswap]
        simp [hF, hG]
  simpa [F, G] using congrArg (fun h => h f) hFG

theorem exists_K_monic_swap_algEquivAevalXAddC {S : Type*} [CommRing S] [Nontrivial S] (p : S[X][Y])
    (hp : p.leadingCoeff.Monic) : ∃ K : ℕ, (swap ((algEquivAevalXAddC (X ^ K)) p)).Monic := by
  have hp0 : p ≠ 0 := by
    intro h
    have : p.leadingCoeff = 0 := by simp [h]
    exact hp.ne_zero this
  let N : ℕ := p.natDegree
  let M : ℕ := (Finset.range N).sup fun i => (p.coeff i).natDegree
  let K : ℕ := M + 1
  refine ⟨K, ?_⟩
  let t : S[X] := X ^ K
  let τ : S[X][Y] ≃ₐ[S[X]] S[X][Y] := Polynomial.algEquivAevalXAddC t
  let swapS : S[X][Y] ≃ₐ[S] _ := Polynomial.Bivariate.swap
  let base : S[X][Y] := (C X) + Y ^ K
  let term : ℕ → S[X][Y] := fun i => swapS (C (p.coeff i)) * base ^ i
  have hτ : τ p =  ∑ i ∈ Finset.range (N + 1), (C (p.coeff i)) * (Y + C t) ^ i := by
    simpa [τ, N, Algebra.smul_def, mul_assoc, mul_left_comm, mul_comm] using
      Polynomial.aeval_eq_sum_range (Y + C t)
  have hswap_YCt : swapS (Y + C t) = base := by
    simp only [map_add, swapS, Polynomial.Bivariate.swap_Y, t, map_pow,
      Polynomial.Bivariate.swap_X, base]
  have hswap : swapS (τ p) = ∑ i ∈ Finset.range (N + 1), term i := by
    simpa [term, map_sum, map_mul, map_pow, map_add, hswap_YCt] using congrArg swapS hτ
  let rest : S[X][Y] := ∑ i ∈ Finset.range N, term i
  let main : S[X][Y] := term N
  have hswap' : swapS (τ p) = rest + main := by
    have hsum : (∑ i ∈ Finset.range (N + 1), term i) = rest + main := by
      simp [rest, main, Finset.sum_range_succ]
    simpa [hswap] using (hswap.trans hsum)
  have hK0 : K ≠ 0 := Nat.succ_ne_zero M
  have hbase_monic : base.Monic := by
    simpa [base, add_comm, add_left_comm, add_assoc] using Polynomial.monic_X_pow_add_C X hK0
  have hbase_natDegree : base.natDegree = K := by
    simp only [add_comm, natDegree_add_C, natDegree_X_pow, base]
  have hcoeffN : p.coeff N = p.leadingCoeff := by simp [N]
  have hswapLC_monic : (swapS (C p.leadingCoeff)).Monic := by
    have hswapC : swapS (C p.leadingCoeff) = Polynomial.map (C : S →+* S[X]) p.leadingCoeff := by
      simpa [swapS] using (bivariate_swap_C p.leadingCoeff)
    simpa [hswapC] using (hp.map (C : S →+* S[X]))
  have hmain_monic : (term N).Monic := by
    have h1 : (swapS (C (p.coeff N))).Monic := by
      simpa [hcoeffN] using hswapLC_monic
    simpa [term] using h1.mul (hbase_monic.pow N)
  let bound : WithBot ℕ := (M : WithBot ℕ) + (((N - 1) * K : ℕ) : WithBot ℕ)
  have hdeg_term : ∀ i, i < N → (term i).degree ≤ bound := by
    intro i hi
    have hi_mem : i ∈ Finset.range N := Finset.mem_range.2 hi
    have hMi : (p.coeff i).natDegree ≤ M :=
      Finset.le_sup (f := fun j => (p.coeff j).natDegree) hi_mem
    have hdeg_swapCi : (swapS (C (p.coeff i))).degree ≤ (M : WithBot ℕ) := by
      have hnat : (swapS (C (p.coeff i))).natDegree = (p.coeff i).natDegree := by
        have hswapC : swapS (C (p.coeff i)) =
            Polynomial.map (C : S →+* S[X]) (p.coeff i) := by
          simpa [swapS] using (bivariate_swap_C (p.coeff i))
        simpa [hswapC] using Polynomial.natDegree_map_eq_of_injective C_injective (p.coeff i)
      have hdeg_le_nat : (swapS (C (p.coeff i))).degree ≤
          (swapS (C (p.coeff i))).natDegree := Polynomial.degree_le_natDegree
      exact le_trans hdeg_le_nat (by
        simpa [hnat] using (WithBot.coe_le_coe.2 hMi))
    have hi_le : i ≤ N - 1 := Nat.le_pred_of_lt hi
    have hdeg_base_i : (base ^ i).degree ≤ (((N - 1) * K : ℕ) : WithBot ℕ) := by
      have hbase_i_monic : (base ^ i).Monic := (hbase_monic.pow i)
      have hnat_base_i : (base ^ i).natDegree = i * K := by
        simpa [hbase_natDegree] using (hbase_monic.natDegree_pow i)
      have hdeg_eq : (base ^ i).degree = ((i * K : ℕ) : WithBot ℕ) := by
        have hne : base ^ i ≠ 0 := hbase_i_monic.ne_zero
        simpa [hnat_base_i] using (Polynomial.degree_eq_natDegree hne)
      have hmul_le : ((i * K : ℕ) : WithBot ℕ) ≤ (((N - 1) * K : ℕ) : WithBot ℕ) :=
        WithBot.coe_le_coe.2 (Nat.mul_le_mul_right K hi_le)
      simpa [hdeg_eq] using hmul_le
    simpa [bound] using (Polynomial.degree_mul_le (swapS (C (p.coeff i))) (base ^ i)).trans
        (add_le_add hdeg_swapCi hdeg_base_i)
  have hdeg_rest : rest.degree ≤ bound := by
    have hsup : (Finset.range N).sup (fun i => (term i).degree) ≤ bound := by
      refine Finset.sup_le ?_
      intro i hi
      exact (hdeg_term i (Finset.mem_range.1 hi)).trans le_rfl
    have : rest.degree ≤ (Finset.range N).sup (fun i => (term i).degree) := by
      simpa [rest] using Polynomial.degree_sum_le (Finset.range N) (fun i => term i)
    exact le_trans this hsup
  have hdeg_lt : rest.degree < main.degree := by
    by_cases hN0 : N = 0
    · have hmain0 : main ≠ 0 := by
        have : (term 0).Monic := by simpa [main, hN0] using hmain_monic
        simpa [main, hN0] using this.ne_zero
      have hdeg0 : (⊥ : WithBot ℕ) < main.degree :=
        (bot_lt_iff_ne_bot).2 (by simpa [Polynomial.degree_eq_bot] using hmain0)
      simpa [hN0, rest, main] using hdeg0
    have hnat_swapLC : (swapS (C p.leadingCoeff)).natDegree =
        p.leadingCoeff.natDegree := by
      have hswapC : swapS (C p.leadingCoeff) = Polynomial.map (C : S →+* S[X]) p.leadingCoeff := by
        simpa [swapS] using (bivariate_swap_C p.leadingCoeff)
      simpa [hswapC] using Polynomial.natDegree_map_eq_of_injective C_injective p.leadingCoeff
    have hnat_baseN : (base ^ N).natDegree = N * K := by
      simpa [hbase_natDegree] using (hbase_monic.natDegree_pow N)
    have hnat_main : main.natDegree = p.leadingCoeff.natDegree + N * K := by
      simpa [main, term, hcoeffN, hnat_swapLC, hnat_baseN, add_comm, add_left_comm, add_assoc] using
        hswapLC_monic.natDegree_mul (hbase_monic.pow N)
    have hmain_deg : main.degree = ((p.leadingCoeff.natDegree + N * K : ℕ) : WithBot ℕ) := by
      have hne : main ≠ 0 := hmain_monic.ne_zero
      simpa [hnat_main] using (Polynomial.degree_eq_natDegree hne)
    have hNK : N * K = (N - 1) * K + K := by
      have hpos : 0 < N := Nat.pos_of_ne_zero hN0
      have h1 : 1 ≤ N := (Nat.succ_le_iff).2 hpos
      have hsub : N - 1 + 1 = N := Nat.sub_add_cancel h1
      calc _ = (N - 1 + 1) * K := by simp [hsub]
        _ = (N - 1) * K + 1 * K := by simp [Nat.add_mul]
        _ = (N - 1) * K + K := by simp
    have hM_lt_TK : M < p.leadingCoeff.natDegree + K :=
      lt_of_lt_of_le (Nat.lt_succ_self M) (Nat.le_add_left _ _)
    have hbound_lt : (M : WithBot ℕ) + (((N - 1) * K : ℕ) : WithBot ℕ) <
        ((p.leadingCoeff.natDegree + N * K : ℕ) : WithBot ℕ) := by
      simpa [hNK, Nat.add_assoc, Nat.add_left_comm, Nat.add_comm, bound] using
        WithBot.coe_lt_coe.2 <| Nat.add_lt_add_right hM_lt_TK ((N - 1) * K)
    have hmain_eq : ((p.leadingCoeff.natDegree + N * K : ℕ) : WithBot ℕ) = main.degree := by
      simp [hmain_deg]
    exact lt_of_le_of_lt hdeg_rest (by simpa [hmain_eq] using hbound_lt)
  have : (swapS (τ p)).Monic := by
    simpa [hswap', rest, main, add_comm, add_left_comm, add_assoc] using
      Polynomial.Monic.add_of_right hmain_monic hdeg_lt
  simpa [swapS, τ, t, K] using this

theorem suslin_monic_polynomial_theorem {R : Type*} [CommRing R] [IsDomain R] [IsNoetherianRing R]
    (n : ℕ) (I : Ideal (MvPolynomial (Fin (n + 1)) R)) (hI : ringKrullDim R < I.height) :
    ∃ e : MvPolynomial (Fin (n + 1)) R ≃ₐ[R] MvPolynomial (Fin (n + 1)) R,
      ∃ f : MvPolynomial (Fin (n + 1)) R, f ∈ I ∧ (MvPolynomial.finSuccEquiv R n (e f)).Monic := by
  induction n with
  | zero =>
    let eEmpty : MvPolynomial (Fin 0) R ≃ₐ[R] R := MvPolynomial.isEmptyAlgEquiv R (Fin 0)
    let e0 : MvPolynomial (Fin (0 + 1)) R ≃ₐ[R] Polynomial R :=
      (MvPolynomial.finSuccEquiv R 0).trans (Polynomial.mapAlgEquiv eEmpty)
    let J : Ideal (Polynomial R) := Ideal.map e0.toRingHom I
    have hheight : J.height = I.height := e0.toRingEquiv.height_map I
    have hJ : ringKrullDim R < J.height := by simpa [hheight] using hI
    have hJ_le : (J.height : WithBot ℕ∞) ≤ (J.leadingCoeff.height : WithBot ℕ∞) :=
      (WithBot.coe_le_coe).2 J.height_le_height_leadingCoeff
    have hLC : ringKrullDim R < (J.leadingCoeff.height : WithBot ℕ∞) := lt_of_lt_of_le hJ hJ_le
    have hLC_top : (J.leadingCoeff : Ideal R) = ⊤ := by
      by_contra hne
      have hbound : (J.leadingCoeff.height : WithBot ℕ∞) ≤ ringKrullDim R := by
        simpa using J.leadingCoeff.height_le_ringKrullDim_of_ne_top hne
      exact (not_lt_of_ge hbound) hLC
    have h1 : (1 : R) ∈ (J.leadingCoeff : Ideal R) := by simp [hLC_top]
    rcases (J.mem_leadingCoeff 1).1 h1 with ⟨g, hgJ, hgLC⟩
    have hgMonic : g.Monic := by simp [Polynomial.Monic, hgLC]
    rcases (Ideal.mem_map_iff_of_surjective e0.toRingHom e0.toRingEquiv.surjective).1 hgJ with
      ⟨f, hfI, rfl⟩
    refine ⟨AlgEquiv.refl, f, hfI, ?_⟩
    have hf_map : e0 f = Polynomial.map eEmpty ((MvPolynomial.finSuccEquiv R 0) f) := by
      simp [e0, Polynomial.mapAlgEquiv, Polynomial.mapAlgHom]
    have hLC_map : (Polynomial.map eEmpty ((MvPolynomial.finSuccEquiv R 0) f)).leadingCoeff =
        eEmpty ((MvPolynomial.finSuccEquiv R 0) f).leadingCoeff := by
      simpa using Polynomial.leadingCoeff_map_of_injective eEmpty.toRingEquiv.injective
        ((MvPolynomial.finSuccEquiv R 0) f)
    have hLC_image : eEmpty (((MvPolynomial.finSuccEquiv R 0) f).leadingCoeff) = 1 := by
      have : (map eEmpty.toRingHom ((MvPolynomial.finSuccEquiv R 0) f)).leadingCoeff = 1 := by
        simpa [hf_map] using (show (e0 f).leadingCoeff = 1 from hgMonic)
      simpa [hLC_map] using this
    have hLC : ((MvPolynomial.finSuccEquiv R 0) f).leadingCoeff = 1 :=
      eEmpty.toRingEquiv.injective <| by simpa using hLC_image
    simpa [Polynomial.Monic] using hLC
  | succ n ih =>
    let A := MvPolynomial (Fin (n + 2)) R
    let B := MvPolynomial (Fin (n + 1)) R
    let S := MvPolynomial (Fin n) R
    let eLast : A ≃ₐ[R] Polynomial B := MvPolynomial.finSuccEquivLast R (n + 1)
    let J : Ideal (Polynomial B) := Ideal.map eLast.toRingHom I
    have hJheight : J.height = I.height := eLast.toRingEquiv.height_map I
    have hJ : ringKrullDim R < J.height := by simpa [hJheight] using hI
    have hJ_le : (J.height : WithBot ℕ∞) ≤ (J.leadingCoeff.height : WithBot ℕ∞) :=
      (WithBot.coe_le_coe).2 (Ideal.height_le_height_leadingCoeff J)
    have hLC : ringKrullDim R < (J.leadingCoeff.height : WithBot ℕ∞) := lt_of_lt_of_le hJ hJ_le
    rcases ih J.leadingCoeff hLC with ⟨eB, g, hgLC, hgMonic⟩
    rcases (J.mem_leadingCoeff g).1 hgLC with ⟨q, hqJ, hqLC⟩
    rcases (Ideal.mem_map_iff_of_surjective eLast.toRingHom eLast.toRingEquiv.surjective).1 hqJ with
      ⟨f0, hf0I, hq⟩
    have hq : eLast f0 = q := hq
    let eExt : A ≃ₐ[R] A := (eLast.trans (Polynomial.mapAlgEquiv eB)).trans eLast.symm
    let eX : B ≃ₐ[R] Polynomial S := MvPolynomial.finSuccEquiv R n
    let H : A ≃ₐ[R] Polynomial (Polynomial S) := eLast.trans (Polynomial.mapAlgEquiv eX)
    let p : Polynomial (Polynomial S) := H (eExt f0)
    have hp_lc : p.leadingCoeff = eX (eB g) := by
      have h₁ : eLast (eExt f0) = Polynomial.map eB (eLast f0) := by
        have hf : eExt f0 = eLast.symm (Polynomial.map eB (eLast f0)) := by
          simpa [eExt, Polynomial.mapAlgEquiv, Polynomial.mapAlgHom] using by rfl
        simp [hf]
      have hLC_q1 : (eLast (eExt f0)).leadingCoeff = eB g := by
        have hLC_mapB :
            (Polynomial.map eB (eLast f0)).leadingCoeff = eB (eLast f0).leadingCoeff := by
          simpa using Polynomial.leadingCoeff_map_of_injective eB.toRingEquiv.injective (eLast f0)
        simpa [h₁, hq, hqLC] using hLC_mapB
      have hp_def : p = Polynomial.map eX (eLast (eExt f0)) := by
        simp [p, H, Polynomial.mapAlgEquiv, Polynomial.mapAlgHom]
      have hLC_mapX :
          (map eX (eLast (eExt f0))).leadingCoeff = eX (eLast (eExt f0)).leadingCoeff := by
        simpa using
          Polynomial.leadingCoeff_map_of_injective eX.toRingEquiv.injective (eLast (eExt f0))
      simp [hp_def, hLC_mapX, hLC_q1]
    have hp_lc_monic : p.leadingCoeff.Monic := by simpa [hp_lc, eX] using hgMonic
    rcases exists_K_monic_swap_algEquivAevalXAddC p hp_lc_monic with ⟨K, hmonic_swap⟩
    let τ : (Polynomial (Polynomial S)) ≃ₐ[Polynomial S] (Polynomial (Polynomial S)) :=
      Polynomial.algEquivAevalXAddC ((Polynomial.X : Polynomial S) ^ K)
    let eTau : A ≃ₐ[R] A := (H.trans (τ.restrictScalars R)).trans H.symm
    let eTotal : A ≃ₐ[R] A := eExt.trans eTau
    have hHp : H (eTotal f0) = τ p := by simp [eTotal, eTau, p, H]
    have hEq : (mapAlgEquiv (MvPolynomial.finSuccEquivLast R n)
        (MvPolynomial.finSuccEquiv R (n + 1) (eTotal f0))) =
        Polynomial.Bivariate.swap (H (eTotal f0)) := by
      simpa [H, eLast, eX] using finSuccEquiv_map_finSuccEquivLast_apply n (eTotal f0)
    have hLHS_monic : (Polynomial.mapAlgEquiv (MvPolynomial.finSuccEquivLast R n)
        (MvPolynomial.finSuccEquiv R (n + 1) (eTotal f0))).Monic := by
      simpa [hEq, hHp, τ] using hmonic_swap
    set q0 := MvPolynomial.finSuccEquiv R (n + 1) (eTotal f0) with hq0
    have hLC_q0 : q0.leadingCoeff = 1 := by
      let eCoeff : B →+* Polynomial S := MvPolynomial.finSuccEquivLast R n
      have hLC_map : (Polynomial.map eCoeff q0).leadingCoeff = eCoeff q0.leadingCoeff := by
        simpa [eCoeff] using Polynomial.leadingCoeff_map_of_injective
          (MvPolynomial.finSuccEquivLast R n).toRingEquiv.injective q0
      have : eCoeff q0.leadingCoeff = eCoeff (1 : B) := by
        have : (Polynomial.map eCoeff q0).leadingCoeff = 1 := by
          simpa [eCoeff, Polynomial.mapAlgEquiv, Polynomial.mapAlgHom] using hLHS_monic
        simpa [hLC_map] using this
      exact (MvPolynomial.finSuccEquivLast R n).toRingEquiv.injective this
    exact ⟨eTotal, f0, hf0I, by simpa [hq0] using by simpa [Polynomial.Monic] using hLC_q0⟩
