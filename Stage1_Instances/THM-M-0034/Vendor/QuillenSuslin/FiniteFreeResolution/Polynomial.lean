/-
Copyright (c) 2026 Yongle Hu. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yongle Hu
-/
/- Port notice: modified for the repository's pinned Lean 4.29/mathlib APIs.
The exact compatibility edit is recorded in `../../../PORT_PROVENANCE.md`. -/
import Mathlib.Algebra.Polynomial.Module.TensorProduct
import Mathlib.RingTheory.Ideal.IsPrincipal
import Mathlib.RingTheory.Ideal.Quotient.Noetherian
import Mathlib.RingTheory.Polynomial.Quotient
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.FiniteFreeResolution.Basic

universe u v w

variable {R : Type u} [CommRing R]

open Polynomial Module Ideal

section polynomial

/-- A subsingleton finitely generated module has a finite free resolution. -/
theorem hasFiniteFreeResolution_of_subsingleton (M : Type v)
    [AddCommGroup M] [Module R M] [Module.Finite R M] [Subsingleton M] :
    HasFiniteFreeResolution R M :=
  hasFiniteFreeResolution_of_finite_of_free M

/-- Push a finite free resolution of an `R`-ideal `I` to a resolution of `I · R[X]`. -/
theorem hasFiniteFreeResolution_map_C_of_hasFiniteFreeResolution
    (I : Ideal R) (hI : HasFiniteFreeResolution R I) :
    HasFiniteFreeResolution R[X] (Ideal.map (C : R →+* R[X]) I) := by
  rcases hasFiniteFreeResolutionLength_of_hasFiniteFreeResolution I hI with ⟨n, hn⟩
  let polyMap {P Q : Type u} [AddCommGroup P] [Module R P] [AddCommGroup Q] [Module R Q]
      (f : P →ₗ[R] Q) : PolynomialModule R P →ₗ[R[X]] PolynomialModule R Q :=
    { toFun := PolynomialModule.map R f
      map_add' := by
        intro x y
        simp
      map_smul' := by
        intro p q
        simp [PolynomialModule.map_smul R f p q] }
  have liftLength : ∀ {P : Type u} [AddCommGroup P] [Module R P] {n : ℕ},
      HasFiniteFreeResolutionLength R P n →
        HasFiniteFreeResolutionLength R[X] (PolynomialModule R P) n := by
    intro P _ _ n hn
    induction hn with
    | zero P =>
        let e := PolynomialModule.polynomialTensorProductLEquivPolynomialModule R P
        let : Module.Finite R[X] (PolynomialModule R P) :=
          Module.Finite.of_surjective e.toLinearMap e.surjective
        let : Module.Free R[X] (PolynomialModule R P) := Module.Free.of_equiv e
        exact HasFiniteFreeResolutionLength.zero (PolynomialModule R P)
    | succ P n F f hf hker ih =>
        let eF := PolynomialModule.polynomialTensorProductLEquivPolynomialModule R F
        let : Module.Finite R[X] (PolynomialModule R F) :=
          Module.Finite.of_surjective eF.toLinearMap eF.surjective
        let : Module.Free R[X] (PolynomialModule R F) := Module.Free.of_equiv eF
        let fX := polyMap f
        have hfX : Function.Surjective fX := by
          intro y
          induction y using PolynomialModule.induction_linear with
          | zero => exact ⟨0, by simp [fX, polyMap]⟩
          | add y z hy hz =>
              rcases hy with ⟨y, rfl⟩
              rcases hz with ⟨z, rfl⟩
              refine ⟨y + z, by simp [fX, polyMap]⟩
          | single i m =>
              rcases hf m with ⟨x, rfl⟩
              refine ⟨PolynomialModule.single R i x, by simp [fX, polyMap]⟩
        let sub : LinearMap.ker f →ₗ[R] F := (LinearMap.ker f).subtype
        let kX : PolynomialModule R (LinearMap.ker f) →ₗ[R[X]] PolynomialModule R F :=
          polyMap sub
        have hkX : LinearMap.ker fX = LinearMap.range kX := by
          ext y
          constructor
          · intro hy
            have hy0 : fX y = 0 := by simpa using hy
            let z : PolynomialModule R (LinearMap.ker f) :=
              Finsupp.onFinset y.support
                (fun a => ⟨y a, by
                  have : (fX y) a = 0 := congrArg (fun g => g a) hy0
                  simpa [fX, polyMap, PolynomialModule.map, Finsupp.mapRange_apply] using this⟩)
                (by
                  intro a ha
                  have : y a ≠ 0 := by
                    intro hya
                    apply ha
                    apply Subtype.ext
                    simp [hya]
                  exact (Finsupp.mem_support_iff).2 this)
            refine ⟨z, ?_⟩
            apply Finsupp.ext
            intro a
            have hz : ((Finsupp.mapRange.linearMap sub) z) a = sub (z a) := by
              simp [Finsupp.mapRange.linearMap_apply, Finsupp.mapRange_apply]
            simp [kX, polyMap, PolynomialModule.map]
            refine hz.trans ?_
            simp [z, Finsupp.onFinset_apply, sub]
          · rintro ⟨z, rfl⟩
            show fX (kX z) = 0
            apply Finsupp.ext
            intro a
            dsimp [fX, kX, polyMap, PolynomialModule.map]
            have hz : ((Finsupp.mapRange.linearMap sub) z) a = sub (z a) := by
              simp [Finsupp.mapRange.linearMap_apply, Finsupp.mapRange_apply]
            have hzKer : f (sub (z a)) = 0 := (z a).2
            have hcoeff : ((Finsupp.mapRange.linearMap f) ((Finsupp.mapRange.linearMap sub) z)) a =
                f (((Finsupp.mapRange.linearMap sub) z) a) := by
              simp [Finsupp.mapRange.linearMap_apply, Finsupp.mapRange_apply]
            exact hcoeff.trans ((congrArg f hz).trans hzKer)
        have hkerX : HasFiniteFreeResolutionLength R[X] (LinearMap.ker fX) n := by
          have hkX' : LinearMap.range kX = LinearMap.ker fX := hkX.symm
          have hinj : Function.Injective kX := by
            intro x y hxy
            apply Finsupp.ext
            intro a
            apply Subtype.ext
            have hxy' : (kX x) a = (kX y) a := congrArg (fun g => g a) hxy
            let mx := Finsupp.mapRange.linearMap (α := ℕ) sub
            have hxy0 : (mx x) a = (mx y) a := by
              simp [kX, polyMap, PolynomialModule.map] at hxy'
              exact hxy'
            have hx0 : (mx x) a = sub (x a) := by
              simp [mx, Finsupp.mapRange.linearMap_apply, Finsupp.mapRange_apply]
            have hy0 : (mx y) a = sub (y a) := by
              simp [mx, Finsupp.mapRange.linearMap_apply, Finsupp.mapRange_apply]
            have hsub : sub (x a) = sub (y a) := by
              calc _ = (mx x) a := hx0.symm
                _ = (mx y) a := hxy0
                _ = sub (y a) := hy0
            dsimp [sub] at hsub
            exact hsub
          exact hasFiniteFreeResolutionLength_of_linearEquiv
            ((LinearEquiv.ofInjective kX hinj).trans (LinearEquiv.ofEq _ _ hkX')) ih
        exact HasFiniteFreeResolutionLength.succ (PolynomialModule R P) n
          (PolynomialModule R F) fX hfX hkerX
  have hPoly : HasFiniteFreeResolution R[X] (PolynomialModule R I) :=
    hasFiniteFreeResolution_of_hasFiniteFreeResolutionLength (PolynomialModule R I)
      ⟨n, liftLength hn⟩
  let incl : I →ₗ[R] R := I.subtype
  let inclX : PolynomialModule R I →ₗ[R[X]] PolynomialModule R R := polyMap incl
  have inclX_apply (p : PolynomialModule R I) (n : ℕ) : (inclX p) n = (p n : R) := by
    simp [inclX, polyMap, PolynomialModule.map]
    show (fun q => q n) ((Finsupp.mapRange.linearMap incl) p) = p n
    have h := congrArg (fun q => q n) (Finsupp.mapRange.linearMap_apply incl p)
    rw [h]
    simp [Finsupp.mapRange_apply, incl]
  let φ0 : PolynomialModule R I →ₗ[R[X]] R[X] :=
    PolynomialModule.equivPolynomialSelf.toLinearMap.comp inclX
  have hφ0inj : Function.Injective φ0 := by
    intro x y hxy
    have hxy' : inclX x = inclX y := by
      simpa [φ0] using congrArg PolynomialModule.equivPolynomialSelf.symm hxy
    apply Finsupp.ext
    intro a
    apply Subtype.ext
    have hxy0 : (inclX x) a = (inclX y) a := congrArg (fun g => g a) hxy'
    let mx := Finsupp.mapRange.linearMap (α := ℕ) incl
    have hxy1 : (mx x) a = (mx y) a := by
      have h := hxy0
      simp [inclX, polyMap, PolynomialModule.map] at h
      exact h
    have hx0 : (mx x) a = incl (x a) := by
      simp [mx, Finsupp.mapRange.linearMap_apply, Finsupp.mapRange_apply]
    have hy0 : (mx y) a = incl (y a) := by
      simp [mx, Finsupp.mapRange.linearMap_apply, Finsupp.mapRange_apply]
    have hincl : incl (x a) = incl (y a) := by
      calc _ = (mx x) a := hx0.symm
        _ = (mx y) a := hxy1
        _ = incl (y a) := hy0
    dsimp [incl] at hincl
    exact hincl
  have hφ0range : LinearMap.range φ0 = (Ideal.map (C : R →+* R[X]) I : Ideal R[X]) := by
    ext f
    constructor
    · rintro ⟨p, rfl⟩
      refine (Ideal.mem_map_C_iff).2 fun n => ?_
      have : (φ0 p).coeff n = (inclX p) n := by
        simp [φ0, PolynomialModule.equivPolynomialSelf, toFinsuppIso,
          coeff_ofFinsupp]
      have hp : (inclX p) n = (p n : R) := inclX_apply p n
      rw [this, hp]
      exact (p n).2
    · intro hf
      have hf' : ∀ n, f.coeff n ∈ I := (Ideal.mem_map_C_iff).1 hf
      let p : PolynomialModule R I := Finsupp.onFinset f.support (fun n => ⟨f.coeff n, hf' n⟩) <| by
          intro n hn
          have : f.coeff n ≠ 0 := by
            intro h0
            apply hn
            apply Subtype.ext
            simp [h0]
          exact (Polynomial.mem_support_iff).2 this
      refine ⟨p, ?_⟩
      apply Polynomial.ext
      intro n
      have hφ : (φ0 p).coeff n = (inclX p) n := by
        simp [φ0, PolynomialModule.equivPolynomialSelf, toFinsuppIso,
          coeff_ofFinsupp]
      rw [hφ, inclX_apply p n]
      simp [p, Finsupp.onFinset_apply]
  exact hasFiniteFreeResolution_of_linearEquiv
    ((LinearEquiv.ofInjective φ0 hφ0inj).trans (LinearEquiv.ofEq _ _ hφ0range)) hPoly

/-- The canonical `R`-algebra equivalence `(R ⧸ I)[X] ≃ R[X] ⧸ I·R[X]`. -/
noncomputable def polynomialQuotientEquiv (I : Ideal R) :
    (R ⧸ I)[X] ≃ₐ[R] R[X] ⧸ I.map (C : R →+* R[X]) :=
  have h : RingHom.ker (mapAlgHom (Ideal.Quotient.mkₐ R I)) = I.map (C : R →+* R[X]) := by
    apply Eq.trans (ker_mapRingHom (Ideal.Quotient.mkₐ R I).toRingHom)
    congr
    simp
  (quotientKerAlgEquivOfSurjective <| map_surjective _ <| Quotient.mkₐ_surjective R I).symm.trans <|
    quotientEquivAlgOfEq _ h

/-- Over a domain, the principal ideal `(f)` is linearly equivalent to the ambient ring. -/
noncomputable def linearEquiv_mul_spanSingleton [IsDomain R] {f : R}
    (hf : f ≠ 0) : R ≃ₗ[R] (Ideal.span ({f} : Set R) : Ideal R) :=
  Ideal.isoBaseOfIsPrincipal <| (Submodule.ne_bot_iff (span {f})).mpr
    ⟨f, mem_span_singleton_self f, hf⟩

/-- If `P ⊂ R[X]` is an ideal over a Noetherian domain `R` with `P ∩ R = (0)`, then there exists
  `d ≠ 0` and `f ∈ P` such that `d • P ⊆ (f)`. -/
theorem exists_nonzero_C_mul_mem_span_singleton [IsDomain R] [IsNoetherianRing R] {P : Ideal (R[X])}
    (hP : ∀ x : R, C x ∈ P → x = 0) (hPne : P ≠ ⊥) :
    ∃ d : R, d ≠ 0 ∧ ∃ f : R[X], f ∈ P ∧ f ≠ 0 ∧
      ∀ g ∈ P, C d * g ∈ Ideal.span ({f} : Set (R[X])) := by
  classical
  have hPfg : P.FG := IsNoetherian.noetherian P
  rcases hPfg with ⟨s, hs⟩
  obtain ⟨⟨p0, hp0P⟩, hp0ne⟩ := Submodule.nonzero_mem_of_bot_lt (bot_lt_iff_ne_bot.2 hPne)
  have hp0ne' : p0 ≠ 0 := by
    intro h0
    apply hp0ne
    simp [Subtype.ext_iff, h0]
  -- Pick `f ∈ P` of minimal `natDegree` among the nonzero elements of `P`.
  let Q : ℕ → Prop := fun n => ∃ f : R[X], f ∈ P ∧ f ≠ 0 ∧ f.natDegree = n
  have hQ : ∃ n, Q n := ⟨p0.natDegree, p0, hp0P, hp0ne', rfl⟩
  set nmin : ℕ := Nat.find hQ
  have hspec : Q nmin := Nat.find_spec hQ
  rcases hspec with ⟨f, hfP, hfne, hfnat⟩
  have hfmin : ∀ g : R[X], g ∈ P → g ≠ 0 → f.natDegree ≤ g.natDegree := by
    intro g hg hgne
    have : Q g.natDegree := ⟨g, hg, hgne, rfl⟩
    have hle : nmin ≤ g.natDegree := Nat.find_min' hQ this
    simpa [hfnat] using hle
  -- `f` cannot have degree `0`, because `P ∩ R = (0)`.
  have hf_natDegree_ne_zero : f.natDegree ≠ 0 := by
    intro hdeg0
    have hfC : f = C (f.coeff 0) := eq_C_of_natDegree_eq_zero hdeg0
    have hmem : C (f.coeff 0) ∈ P := hfC ▸ hfP
    have hcoeff0 : f.coeff 0 = 0 := hP (f.coeff 0) hmem
    apply hfne
    calc f = C (f.coeff 0) := hfC
      _ = C 0 := by simp [hcoeff0]
      _ = 0 := by simp
  let K := FractionRing R
  let i : R →+* K := algebraMap R K
  have hi : Function.Injective i := IsFractionRing.injective R K
  let fK : K[X] := f.map i
  have hfKne : fK ≠ 0 := by
    intro h0
    apply hfne
    exact (Polynomial.map_injective i hi) (by simpa [fK] using h0)
  have hfK_natDegree_ne_zero : fK.natDegree ≠ 0 := by
    have hfKdeg : fK.natDegree = f.natDegree := by
      simpa [fK] using natDegree_map_eq_of_injective hi f
    simpa only [hfKdeg, ne_eq] using hf_natDegree_ne_zero
  let : Algebra R[X] K[X] := (mapRingHom (algebraMap R K)).toAlgebra
  have : IsLocalization ((nonZeroDivisors R).map (C : R →+* R[X])) K[X] := by
    simpa using (isLocalization (nonZeroDivisors R) K)
  let q (g : R[X]) : K[X] := (g.map i) / fK
  let r (g : R[X]) : K[X] := (g.map i) % fK
  let fracs : Finset K[X] := s.biUnion fun g => ({q g, r g} : Finset K[X])
  obtain ⟨b, hb⟩ := IsLocalization.exist_integer_multiples_of_finset
    ((nonZeroDivisors R).map (C : R →+* R[X])) fracs
  rcases b.2 with ⟨d, hd, hdEq⟩
  have hbEq : (b : R[X]) = C d := by
    simpa using hdEq.symm
  have hd0 : d ≠ 0 := nonZeroDivisors.ne_zero hd
  have hid0 : i d ≠ 0 := by
    intro h0
    apply hd0
    exact hi (by simpa only [map_zero] using h0)
  have hgen : ∀ g, g ∈ (s : Set R[X]) → C d * g ∈ Ideal.span ({f} : Set R[X]) := by
    intro g hg
    have hg' : g ∈ s := by simpa using hg
    have hq : IsLocalization.IsInteger (R[X]) ((b : R[X]) • q g) := by
      have : q g ∈ fracs := by
        refine Finset.mem_biUnion.2 ⟨g, hg', ?_⟩
        simp only [Finset.mem_insert, Finset.mem_singleton, true_or]
      simpa only [Algebra.smul_def, algebraMap_def, coe_mapRingHom] using hb (q g) this
    have hr : IsLocalization.IsInteger (R[X]) ((b : R[X]) • r g) := by
      have : r g ∈ fracs := by
        refine Finset.mem_biUnion.2 ⟨g, hg', ?_⟩
        simp only [Finset.mem_insert, Finset.mem_singleton, or_true]
      simpa [Algebra.smul_def] using hb (r g) this
    rcases hq with ⟨qR, hqR⟩
    rcases hr with ⟨rR, hrR⟩
    have hdiv : q g * fK + r g = (g.map i) := by
      simpa only [mul_comm, add_comm] using (EuclideanDomain.div_add_mod (g.map i) fK)
    have hEq : (b : R[X]) * g = qR * f + rR := by
      apply (map_injective i hi)
      have : (mapRingHom i) ((b : R[X]) * g) = (mapRingHom i) (qR * f + rR) := by
        have hqR' : (mapRingHom i) (b : R[X]) * q g = (mapRingHom i) qR := by
          simpa [Algebra.smul_def, mul_assoc] using (Eq.symm hqR)
        have hrR' : (mapRingHom i) (b : R[X]) * r g = (mapRingHom i) rR := by
          simpa [Algebra.smul_def, mul_assoc] using (Eq.symm hrR)
        calc _ = (mapRingHom i) (b : R[X]) * (g.map i) := by simp only [coe_mapRingHom, map_mul]
          _ = (mapRingHom i) (b : R[X]) * (q g * fK + r g) := by simp only [coe_mapRingHom, hdiv]
          _ = (mapRingHom i) (b : R[X]) * (q g * fK) + (mapRingHom i) (b : R[X]) * r g := by
            simp only [coe_mapRingHom, mul_add]
          _ = (mapRingHom i) qR * fK + (mapRingHom i) rR := by
            have hqRmul : (mapRingHom i) (b : R[X]) * (q g * fK) = (mapRingHom i) qR * fK := by
              calc _ = ((mapRingHom i) (b : R[X]) * q g) * fK := by simp [mul_assoc]
                _ = (mapRingHom i) qR * fK := by simpa using congrArg (fun t => t * fK) hqR'
            calc _ = (mapRingHom i) qR * fK + (mapRingHom i) (b : R[X]) * r g := by simpa [hqRmul]
              _ = (mapRingHom i) qR * fK + (mapRingHom i) rR := by
                simpa only [coe_mapRingHom, add_right_inj]
          _ = (mapRingHom i) (qR * f) + (mapRingHom i) rR := by simp [fK, map_mul]
          _ = (mapRingHom i) (qR * f + rR) := by simp [map_add, map_mul]
      simpa only [Polynomial.map_mul, Polynomial.map_add, coe_mapRingHom] using this
    have hrRP : rR ∈ P := by
      have hgP : g ∈ P := by
        simpa [hs] using (Ideal.subset_span hg)
      have hbgg : (b : R[X]) * g ∈ P := P.mul_mem_left _ hgP
      have hqff : qR * f ∈ P := P.mul_mem_left _ hfP
      have : rR = (b : R[X]) * g - qR * f := by
        have hsub : (b : R[X]) * g - qR * f = rR := by
          simpa [sub_eq_add_neg, add_assoc, add_left_comm, add_comm] using
            congrArg (fun t => t - qR * f) hEq
        simpa only [sub_eq_add_neg] using hsub.symm
      have hmem : (b : R[X]) * g - qR * f ∈ P := P.sub_mem hbgg hqff
      simpa [this] using hmem
    have hdegK : (r g).natDegree < fK.natDegree := by
      simpa only using natDegree_mod_lt (g.map i) hfK_natDegree_ne_zero
    have hdegK' : (rR.map i).natDegree < fK.natDegree := by
      have hrR' : rR.map i = C (i d) * r g := by
        simpa [Algebra.smul_def, hbEq, map_mul] using hrR
      simpa [hrR', natDegree_C_mul hid0] using hdegK
    have hrdeg : rR.natDegree < f.natDegree := by
      have hrRdeg : (rR.map i).natDegree = rR.natDegree := by
        simpa only [natDegree_map_eq_iff, ne_eq] using (natDegree_map_eq_of_injective hi rR)
      have hfKdeg : fK.natDegree = f.natDegree := by
        simpa [fK] using (natDegree_map_eq_of_injective hi f)
      simpa [hrRdeg, hfKdeg] using hdegK'
    have hrR0 : rR = 0 := by
      by_contra hrR0
      have hle : f.natDegree ≤ rR.natDegree := hfmin rR hrRP hrR0
      exact (not_lt_of_ge hle) hrdeg
    have hEq' : (b : R[X]) * g = qR * f := by
      simpa [hrR0] using hEq
    have hbmem : (b : R[X]) * g ∈ Ideal.span ({f} : Set R[X]) := by
      refine (Ideal.mem_span_singleton.2 ?_)
      refine ⟨qR, ?_⟩
      calc _ = qR * f := hEq'
        _ = f * qR := by simp [mul_comm]
    simpa [hbEq] using hbmem
  refine ⟨d, hd0, f, hfP, hfne, ?_⟩
  intro g hgP
  have hgspan : g ∈ Ideal.span (s : Set R[X]) := by simpa [hs] using hgP
  exact Submodule.span_induction hgen (by simp only [mul_zero, zero_mem])
    (fun x y _ _ hx hy => by simpa only [mul_add] using Ideal.add_mem _ hx hy)
    (fun a x _ hx => by
      have : C d * (a * x) = a * (C d * x) := by simp only [mul_comm, mul_assoc]
      simpa only [smul_eq_mul, this] using Ideal.mul_mem_left _ a hx) hgspan

set_option maxHeartbeats 600000 in
private theorem hasFiniteFreeResolution_quotient_prime_aux [IsNoetherianRing R]
    (hR : ∀ (P : Type u), [AddCommGroup P] → [Module R P] → Module.Finite R P →
      HasFiniteFreeResolution R P) : ∀ I : Ideal R, ∀ q : PrimeSpectrum R[X],
    Ideal.comap (C : R →+* R[X]) q.1 = I → HasFiniteFreeResolution (R[X]) (R[X] ⧸ q.1) := by
  -- Noetherian induction on the contraction `p.1 ∩ R`.
  let A : Type u := R[X]
  let contr : PrimeSpectrum A → Ideal R := fun q => Ideal.comap (C : R →+* A) q.1
  refine IsNoetherian.induction ?_
  intro I ih q hqI
  let P : Ideal A := q.1
  have : P.IsPrime := q.2
  have hcomap : Ideal.comap (C : R →+* A) P = I := by simpa [contr, P] using hqI
  have hIA_le_P : Ideal.map (C : R →+* A) I ≤ P :=
    (Ideal.map_le_iff_le_comap).2 <| by simp [hcomap]
  let IA : Ideal A := Ideal.map (C : R →+* A) I
  by_cases hPIA : P = IA
  · have hI_res : HasFiniteFreeResolution R I := hR I inferInstance
    have hIA_res : HasFiniteFreeResolution A IA :=
      hasFiniteFreeResolution_map_C_of_hasFiniteFreeResolution I hI_res
    have hA : HasFiniteFreeResolution A A := hasFiniteFreeResolution_of_finite_of_free A
    have hquot : HasFiniteFreeResolution A (A ⧸ IA) :=
      hasFiniteFreeResolution_of_shortExact_of_left_of_middle IA A (A ⧸ IA)
        (f := IA.subtype) Subtype.coe_injective (Submodule.mkQ_surjective IA)
          (by simpa using LinearMap.exact_subtype_mkQ IA) hIA_res hA
    have hquotP : HasFiniteFreeResolution A (A ⧸ P) :=
      hasFiniteFreeResolution_of_linearEquiv (Submodule.quotEquivOfEq IA P hPIA.symm) hquot
    simpa [P] using hquotP
  · have hIprime : Ideal.IsPrime I := by
      simpa [hcomap] using show (Ideal.comap (C : R →+* A) P).IsPrime from inferInstance
    let R₀ : Type u := R ⧸ I
    let A₀ : Type u := R₀[X]
    let B : Type u := A ⧸ IA
    let π : A →+* B := Ideal.Quotient.mk IA
    let Pbar : Ideal B := Ideal.map π P
    let e : A₀ ≃+* B := Ideal.polynomialQuotientEquivQuotientPolynomial I
    let P₀ : Ideal A₀ := Ideal.comap e.toRingHom Pbar
    have hPbar_ne : Pbar ≠ ⊥ := by
      intro hbot
      have hle : P ≤ RingHom.ker π := (P.map_eq_bot_iff_le_ker π).1 hbot
      have hker : RingHom.ker π = IA := IA.mk_ker
      have hP_le_IA : P ≤ IA := by
        simpa [A, hker] using hle
      exact hPIA (le_antisymm hP_le_IA hIA_le_P)
    have hP₀_ne : P₀ ≠ ⊥ := by
      intro hbot
      have : Ideal.map e.toRingHom P₀ = Pbar := by
        simpa [P₀] using (Ideal.map_comap_of_surjective e.toRingHom e.surjective Pbar)
      have : Pbar = ⊥ := by simpa [hbot] using this.symm
      exact hPbar_ne this
    have hP₀_contr : ∀ x : R₀, (C x : A₀) ∈ P₀ → x = 0 := by
      intro x hx
      rcases Ideal.Quotient.mk_surjective x with ⟨r, rfl⟩
      have hx' : (e (C (Ideal.Quotient.mk I r) : A₀)) ∈ Pbar := by
        simpa [P₀, Ideal.mem_comap] using hx
      have hCr : e (C (Ideal.Quotient.mk I r) : A₀) = (Ideal.Quotient.mk IA) (C r) := by
        simpa [IA, Polynomial.map_C] using
          (Ideal.polynomialQuotientEquivQuotientPolynomial_map_mk I (C r : A))
      have hx'' : (Ideal.Quotient.mk IA) (C r) ∈ Pbar := by simpa [hCr] using hx'
      rcases (Ideal.mem_map_iff_of_surjective π Ideal.Quotient.mk_surjective).1 hx'' with
        ⟨a, haP, haEq⟩
      have hab : a - C r ∈ IA := (Ideal.Quotient.eq).1 haEq
      have habP : a - C r ∈ P := hIA_le_P hab
      have hCrP : (C r : A) ∈ P := by
        have : (C r : A) = a - (a - C r) := by abel
        exact this ▸ P.sub_mem haP habP
      have hrI : r ∈ I := by
        have : r ∈ Ideal.comap (C : R →+* A) P := by simpa [Ideal.mem_comap] using hCrP
        simpa [hcomap] using this
      exact (Ideal.Quotient.eq_zero_iff_mem).2 hrI
    obtain ⟨d₀, hd₀, f₀, hf₀P₀, hf₀ne, hmul₀⟩ :=
      exists_nonzero_C_mul_mem_span_singleton hP₀_contr hP₀_ne
    rcases Ideal.Quotient.mk_surjective d₀ with ⟨d, rfl⟩
    have hd_not_mem : d ∉ I := by
      intro hdI
      apply hd₀
      exact (Ideal.Quotient.eq_zero_iff_mem).2 hdI
    let fbar : B := e f₀
    have hfbar_mem : fbar ∈ Pbar := by
      have : f₀ ∈ P₀ := hf₀P₀
      simpa [P₀, Ideal.mem_comap, fbar] using this
    have hfbar_ne : fbar ≠ 0 := by
      intro h0
      apply hf₀ne
      exact e.injective (by simpa [fbar] using h0)
    let Fbar : Ideal B := Ideal.span ({fbar} : Set B)
    have hFbar_le : Fbar ≤ Pbar := by
      intro x hx
      rcases (Ideal.mem_span_singleton.1 hx) with ⟨y, rfl⟩
      exact Pbar.mul_mem_right y hfbar_mem
    have hmul_bar : ∀ g : B, g ∈ Pbar → (Ideal.Quotient.mk IA (C d) : B) * g ∈ Fbar := by
      intro g hg
      let g₀ : A₀ := e.symm g
      have hg₀ : g₀ ∈ P₀ := by
        have : (e g₀) ∈ Pbar := by simpa [g₀] using hg
        simpa [P₀, Ideal.mem_comap] using this
      have h0 : (C (Ideal.Quotient.mk I d) : A₀) * g₀ ∈ Ideal.span ({f₀} : Set A₀) :=
        hmul₀ g₀ hg₀
      have hCd : e (C (Ideal.Quotient.mk I d) : A₀) = (Ideal.Quotient.mk IA) (C d) := by
        simpa [IA, Polynomial.map_C] using
          (Ideal.polynomialQuotientEquivQuotientPolynomial_map_mk I (C d : A))
      have hmem : e ((C (Ideal.Quotient.mk I d) : A₀) * g₀) ∈
          Ideal.map e.toRingHom (Ideal.span ({f₀} : Set A₀)) :=
        Ideal.mem_map_of_mem e.toRingHom h0
      have hspan :
          Ideal.map (e : A₀ →+* B) (Ideal.span ({f₀} : Set A₀)) = Ideal.span ({fbar} : Set B) := by
        simpa [fbar] using (Ideal.map_span e.toRingHom ({f₀} : Set A₀))
      have : e (C (Ideal.Quotient.mk I d) : A₀) * e g₀ ∈ Fbar := by
        simpa [Fbar, hspan, map_mul] using hmem
      simpa [g₀, hCd] using this
    let Psub : Submodule A B := (Pbar : Submodule B B).restrictScalars A
    let Fsub : Submodule A B := (Fbar : Submodule B B).restrictScalars A
    have hFsub_le : Fsub ≤ Psub := by
      intro x hx
      exact hFbar_le hx
    let K : Submodule A Psub := Submodule.comap Psub.subtype Fsub
    let N := Psub ⧸ K
    let acgN : AddCommGroup N := Submodule.Quotient.addCommGroup K
    let : AddCommMonoid N := acgN.toAddCommMonoid
    have hAnn_d : ∀ x : N, (C d : A) • x = 0 := by
      intro x
      refine Quotient.inductionOn' x ?_
      intro y
      have hyF : ((C d : A) • (y : B)) ∈ Fsub := by
        have hyFmul : (π (C d) : B) * (y : B) ∈ Fsub := by
          have : (Ideal.Quotient.mk IA (C d) : B) * (y : B) ∈ Fbar := hmul_bar (y : B) y.2
          simpa [Fsub, π] using this
        have hsmul : ((C d : A) • (y : B)) = (π (C d) : B) * (y : B) := by
          have hAlgebraMap : (algebraMap A B) = π := rfl
          simpa [hAlgebraMap] using
            (Algebra.smul_def (C d : A) (y : B))
        simpa [hsmul] using hyFmul
      have hyK : (C d : A) • y ∈ K := by
        simpa [K] using hyF
      have h0 : Submodule.Quotient.mk ((C d : A) • y) = (0 : N) :=
        (Submodule.Quotient.mk_eq_zero K).2 hyK
      have hmksmul : Submodule.Quotient.mk ((C d : A) • y) = (C d : A) • Submodule.Quotient.mk y :=
        Submodule.Quotient.mk_smul K (C d : A) y
      exact hmksmul.symm.trans h0
    have hN : HasFiniteFreeResolution A N := by
      have hAnn_I : ∀ r : R, r ∈ I → ∀ x : N, (C r : A) • x = 0 := by
        intro r hrI x
        refine Quotient.inductionOn' x ?_
        intro y
        have hCrIA : (C r : A) ∈ IA := Ideal.mem_map_of_mem (C : R →+* A) hrI
        have hπCr : (π (C r) : B) = 0 := (Ideal.Quotient.eq_zero_iff_mem).2 hCrIA
        have hy0 : (C r : A) • (y : B) = 0 := by
          have hAlgebraMap : (algebraMap A B) = π := rfl
          have hsmul : (C r : A) • (y : B) = (π (C r) : B) * (y : B) := by
            simpa [hAlgebraMap] using (Algebra.smul_def (C r : A) (y : B))
          simp [hsmul, hπCr]
        have hyF : (C r : A) • (y : B) ∈ Fsub := by simp [hy0]
        have hyK : (C r : A) • y ∈ K := by simpa [K] using hyF
        have h0 : Submodule.Quotient.mk ((C r : A) • y) = (0 : N) :=
          (Submodule.Quotient.mk_eq_zero K).2 hyK
        have hmksmul : Submodule.Quotient.mk ((C r : A) • y) =
            (C r : A) • Submodule.Quotient.mk y :=
          Submodule.Quotient.mk_smul K (C r : A) y
        exact hmksmul.symm.trans h0
      let motive : ∀ (M : Type u), [AddCommGroup M] → [Module A M] → [Module.Finite A M] → Prop :=
        fun M _ _ _ => (∀ x : M, (C d : A) • x = 0) →
          (∀ r : R, r ∈ I → ∀ x : M, (C r : A) • x = 0) → HasFiniteFreeResolution A M
      have hN' : motive N := by
        refine IsNoetherianRing.induction_on_isQuotientEquivQuotientPrime A
          inferInstance (motive := motive) ?_ ?_ ?_
        · intro M _ _ _ _ _ _
          exact hasFiniteFreeResolution_of_subsingleton M
        · intro M _ _ _ p' eM hAnn_dM hAnn_IM
          have hCd0_M : (C d : A) • (1 : A ⧸ p'.1) = 0 := by
            have h := hAnn_dM (eM.symm (1 : A ⧸ p'.1))
            have h' : eM ((C d : A) • eM.symm (1 : A ⧸ p'.1)) = eM (0 : M) := congrArg eM h
            have hs :
                eM ((C d : A) • eM.symm (1 : A ⧸ p'.1)) = (C d : A) • eM (eM.symm (1 : A ⧸ p'.1)) :=
              eM.map_smul (C d : A) (eM.symm (1 : A ⧸ p'.1))
            have h'' : (C d : A) • eM (eM.symm (1 : A ⧸ p'.1)) = eM (0 : M) := by
              calc _ = eM ((C d : A) • eM.symm (1 : A ⧸ p'.1)) := hs.symm
                _ = eM (0 : M) := h'
            have : (C d : A) • eM (eM.symm (1 : A ⧸ p'.1)) = (0 : A ⧸ p'.1) :=
              h''.trans eM.map_zero
            have h1 : eM (eM.symm (1 : A ⧸ p'.1)) = (1 : A ⧸ p'.1) :=
              eM.apply_symm_apply (1 : A ⧸ p'.1)
            rwa [← h1]
          have hCd_mem : (C d : A) ∈ p'.1 := by
            have hmk : (Ideal.Quotient.mk p'.1 (C d : A) : A ⧸ p'.1) = 0 := by
              have h := hCd0_M
              rw [Algebra.smul_def] at h
              rw [mul_one] at h
              have hAlgebraMap : (algebraMap A (A ⧸ p'.1)) = Ideal.Quotient.mk p'.1 := rfl
              simpa using by rwa [hAlgebraMap] at h
            exact (Ideal.Quotient.eq_zero_iff_mem).1 hmk
          have hI_le_contr : I ≤ Ideal.comap (C : R →+* A) p'.1 := by
            intro r hrI
            have hCr0_M : (C r : A) • (1 : A ⧸ p'.1) = 0 := by
              have h := hAnn_IM r hrI (eM.symm (1 : A ⧸ p'.1))
              have h' : eM ((C r : A) • eM.symm (1 : A ⧸ p'.1)) = eM (0 : M) := congrArg eM h
              have hs : eM ((C r : A) • eM.symm (1 : A ⧸ p'.1)) =
                  (C r : A) • eM (eM.symm (1 : A ⧸ p'.1)) :=
                eM.map_smul (C r : A) (eM.symm (1 : A ⧸ p'.1))
              have h'' : (C r : A) • eM (eM.symm (1 : A ⧸ p'.1)) = eM (0 : M) := by
                calc _ = eM ((C r : A) • eM.symm (1 : A ⧸ p'.1)) := hs.symm
                  _ = eM (0 : M) := h'
              have : (C r : A) • eM (eM.symm (1 : A ⧸ p'.1)) = (0 : A ⧸ p'.1) :=
                h''.trans eM.map_zero
              have h1 : eM (eM.symm (1 : A ⧸ p'.1)) = (1 : A ⧸ p'.1) :=
                eM.apply_symm_apply (1 : A ⧸ p'.1)
              rwa [← h1]
            have hCr_mem : (C r : A) ∈ p'.1 := by
              have hmk : (Ideal.Quotient.mk p'.1 (C r : A) : A ⧸ p'.1) = 0 := by
                have h := hCr0_M
                rw [Algebra.smul_def] at h
                rw [mul_one] at h
                have hAlgebraMap : (algebraMap A (A ⧸ p'.1)) = Ideal.Quotient.mk p'.1 := rfl
                simpa using by rwa [hAlgebraMap] at h
              exact (Ideal.Quotient.eq_zero_iff_mem).1 hmk
            simpa [Ideal.mem_comap] using hCr_mem
          have hlt : Ideal.comap (C : R →+* A) p'.1 > I := by
            refine lt_of_le_of_ne hI_le_contr ?_
            intro hEq
            have : d ∈ I := by
              have : d ∈ Ideal.comap (C : R →+* A) p'.1 := by
                simpa [Ideal.mem_comap] using hCd_mem
              simpa [hEq] using this
            exact hd_not_mem this
          have hquot : HasFiniteFreeResolution A (A ⧸ p'.1) :=
            ih (Ideal.comap (C : R →+* A) p'.1) hlt p' rfl
          exact hasFiniteFreeResolution_of_linearEquiv eM.symm hquot
        · intro M₁ _ _ _ M₂ _ _ _ M₃ _ _ _ f g hf hg hfg h₁ h₃ hAnn_d2 hAnn_I2
          have hAnn_d1 : ∀ x : M₁, (C d : A) • x = 0 := by
            intro x
            apply hf
            have : f ((C d : A) • x) = 0 := by simpa using hAnn_d2 (f x)
            simpa using this
          have hAnn_I1 : ∀ r : R, r ∈ I → ∀ x : M₁, (C r : A) • x = 0 := by
            intro r hrI x
            apply hf
            have : f ((C r : A) • x) = 0 := by simpa using hAnn_I2 r hrI (f x)
            simpa using this
          have hAnn_d3 : ∀ x : M₃, (C d : A) • x = 0 := by
            intro z
            rcases hg z with ⟨y, rfl⟩
            simpa only [map_smul, map_zero] using congrArg g (hAnn_d2 y)
          have hAnn_I3 : ∀ r : R, r ∈ I → ∀ x : M₃, (C r : A) • x = 0 := by
            intro r hrI z
            rcases hg z with ⟨y, rfl⟩
            simpa only [map_smul, map_zero] using congrArg g (hAnn_I2 r hrI y)
          have h₁' : HasFiniteFreeResolution A M₁ := h₁ hAnn_d1 hAnn_I1
          have h₃' : HasFiniteFreeResolution A M₃ := h₃ hAnn_d3 hAnn_I3
          exact hasFiniteFreeResolution_of_shortExact_of_left_of_right M₁ M₂ M₃ hf hg hfg h₁' h₃'
      exact hN' hAnn_d hAnn_I
    have hI_res : HasFiniteFreeResolution R I := hR I inferInstance
    have hIA_res : HasFiniteFreeResolution A IA :=
      hasFiniteFreeResolution_map_C_of_hasFiniteFreeResolution I hI_res
    have hA : HasFiniteFreeResolution A A := hasFiniteFreeResolution_of_finite_of_free A
    have hB : HasFiniteFreeResolution A B :=
      hasFiniteFreeResolution_of_shortExact_of_left_of_middle IA A (A ⧸ IA)
        (f := IA.subtype) Subtype.coe_injective (Submodule.mkQ_surjective IA)
          (by simpa using (LinearMap.exact_subtype_mkQ IA)) hIA_res hA
    have : IsDomain B := MulEquiv.isDomain A₀ e.symm.toMulEquiv
    have hFbar : HasFiniteFreeResolution A Fbar :=
      hasFiniteFreeResolution_of_linearEquiv
        ((linearEquiv_mul_spanSingleton hfbar_ne).restrictScalars A) hB
    have hK : HasFiniteFreeResolution A K :=
      have hFsub : HasFiniteFreeResolution A Fsub := by simpa [Fsub] using hFbar
      hasFiniteFreeResolution_of_linearEquiv (Submodule.comapSubtypeEquivOfLe hFsub_le).symm hFsub
    have hPbar : HasFiniteFreeResolution A Psub := by
      -- Short exact sequence `0 → K → Psub → N → 0`.
      refine hasFiniteFreeResolution_of_shortExact_of_left_of_right K Psub N
        (f := (K.subtype).restrictScalars A) (Subtype.coe_injective) (Submodule.mkQ_surjective K)
          (by simpa using LinearMap.exact_subtype_mkQ K) hK hN
    let fIP : IA →ₗ[A] P := Submodule.inclusion hIA_le_P
    let gPP : P →ₗ[A] Pbar :=
      { toFun := fun x => ⟨π x.1, Ideal.mem_map_of_mem π x.2⟩
        map_add' := fun _ _ => by congr
        map_smul' := by
          intro m x
          ext
          show π (m • x.1) = m • π x.1
          rw [smul_eq_mul]
          have hAlgebraMap : (algebraMap A B) = π := rfl
          have hsmulB : m • π x.1 = (π m : B) * π x.1 := by
            simpa [hAlgebraMap] using Algebra.smul_def m (π (x : A) : B)
          rw [hsmulB]
          exact π.map_mul m x.1 }
    have hfIP : Function.Injective fIP := by
      intro x y hxy
      apply Subtype.ext
      simpa [fIP] using congrArg (fun z : P => (z : A)) hxy
    have hgPP : Function.Surjective gPP := by
      intro y
      rcases (Ideal.mem_map_iff_of_surjective π Ideal.Quotient.mk_surjective).1 y.2 with
        ⟨a, haP, haEq⟩
      refine ⟨⟨a, haP⟩, ?_⟩
      apply Subtype.ext
      simpa [gPP] using haEq
    have hexPP : Function.Exact fIP gPP := by
      intro x
      constructor
      · intro hx0
        refine ⟨⟨x.1, (Ideal.Quotient.eq_zero_iff_mem).1 <| congrArg (fun z : Pbar => z.1) hx0⟩, ?_⟩
        apply Subtype.ext
        rfl
      · rintro ⟨y, rfl⟩
        apply Subtype.ext
        simpa [gPP, fIP] using (Ideal.Quotient.eq_zero_iff_mem).2 y.2
    have hP : HasFiniteFreeResolution A P :=
      -- Use `0 → IA → P → Pbar → 0`.
      hasFiniteFreeResolution_of_shortExact_of_left_of_right IA P Pbar hfIP hgPP hexPP
        hIA_res <| by simpa only [Psub] using hPbar
    -- Finally, `0 → P → A → A ⧸ P → 0`.
    have hquot : HasFiniteFreeResolution A (A ⧸ P) :=
      hasFiniteFreeResolution_of_shortExact_of_left_of_middle P A (A ⧸ P)
        (f := P.subtype) Subtype.coe_injective (Submodule.mkQ_surjective P)
          (by simpa only [Submodule.coe_subtype] using (LinearMap.exact_subtype_mkQ P)) hP hA
    exact hquot

variable (R)

theorem hasFiniteFreeResolution_quotient_prime [IsNoetherianRing R]
    (hR : ∀ (P : Type u), [AddCommGroup P] → [Module R P] → Module.Finite R P →
      HasFiniteFreeResolution R P)
    (p : PrimeSpectrum (R[X])) : HasFiniteFreeResolution (R[X]) (R[X] ⧸ p.1) := by
  simpa using hasFiniteFreeResolution_quotient_prime_aux hR (Ideal.comap (C : R →+* R[X]) p.1) p rfl

/-- Let `R` be a noetherian ring such that every finitely generated `R`-module admits a finite
free resolution. Then the same property holds for finitely generated `R[X]`-modules. -/
theorem polynomial_hasFiniteFreeResolution_of_isNoetherianRing [IsNoetherianRing R]
    (hR : ∀ (P : Type u), [AddCommGroup P] → [Module R P] → Module.Finite R P →
      HasFiniteFreeResolution R P)
    (P : Type v) [AddCommGroup P] [Module R[X] P] [Module.Finite R[X] P] :
    HasFiniteFreeResolution R[X] P :=
  IsNoetherianRing.induction_on_isQuotientEquivQuotientPrime R[X]
    inferInstance (motive := fun N _ _ _ => HasFiniteFreeResolution R[X] N)
      (fun N _ _ _ _ => hasFiniteFreeResolution_of_subsingleton N)
      (fun _ _ _ _ p e => hasFiniteFreeResolution_of_linearEquiv e.symm
        (hasFiniteFreeResolution_quotient_prime R hR p))
      (fun N₁ _ _ _ N₂ _ _ _ N₃ _ _ _ _ _ hf hg hfg h₁ h₃ =>
        hasFiniteFreeResolution_of_shortExact_of_left_of_right N₁ N₂ N₃ hf hg hfg h₁ h₃)

end polynomial

section MvPolynomial

theorem mvPolynomial_hasFiniteFreeResolution_of_isNoetherianRing_aux [IsNoetherianRing R]
    (s : Type) [Finite s]
    (hR : ∀ (P : Type u), [AddCommGroup P] → [Module R P] → Module.Finite R P →
      HasFiniteFreeResolution R P)
    (P : Type u) [AddCommGroup P] [Module (MvPolynomial s R) P]
    [Module.Finite (MvPolynomial s R) P] : HasFiniteFreeResolution (MvPolynomial s R) P := by
  let Q : Type → Prop := fun t =>
    ∀ (M : Type u) [AddCommGroup M] [Module (MvPolynomial t R) M]
      [Module.Finite (MvPolynomial t R) M], HasFiniteFreeResolution (MvPolynomial t R) M
  have hs : Q s := by
    refine Finite.induction_empty_option ?_ ?_ ?_ s
    · intro α β a hα M _ _ _
      let e : MvPolynomial α R ≃+* MvPolynomial β R := (MvPolynomial.renameEquiv R a).toRingEquiv
      let : Module (MvPolynomial α R) M := Module.compHom M e.toRingHom
      have hA : HasFiniteFreeResolution (MvPolynomial α R) M := by
        have : Module.Finite (MvPolynomial α R) M := moduleFinite_of_ringEquiv e M
        simpa using hα M
      simpa using hasFiniteFreeResolution_of_ringEquiv_right e M hA
    · intro M _ _ _
      let e : MvPolynomial PEmpty R ≃+* R := MvPolynomial.isEmptyRingEquiv R PEmpty
      let : Module R M := Module.compHom M e.symm.toRingHom
      have hRM : HasFiniteFreeResolution R M := by
        have : Module.Finite R M := moduleFinite_of_ringEquiv e.symm M
        exact hR M (inferInstance : Module.Finite R M)
      simpa using hasFiniteFreeResolution_of_ringEquiv_left e M hRM
    · intro α _ hα M _ _ _
      let e : MvPolynomial (Option α) R ≃+* (MvPolynomial α R)[X] :=
        (MvPolynomial.optionEquivLeft R α).toRingEquiv
      let : Module (MvPolynomial α R)[X] M := Module.compHom M e.symm.toRingHom
      have hPoly : HasFiniteFreeResolution (MvPolynomial α R)[X] M := by
        have : Module.Finite (MvPolynomial α R)[X] M := moduleFinite_of_ringEquiv e.symm M
        simpa using polynomial_hasFiniteFreeResolution_of_isNoetherianRing (MvPolynomial α R) hα M
      simpa using hasFiniteFreeResolution_of_ringEquiv_left e M hPoly
  exact hs P

theorem mvPolynomial_hasFiniteFreeResolution_of_isNoetherianRing [IsNoetherianRing R]
    (s : Type w) [Finite s]
    (hR : ∀ (P : Type u), [AddCommGroup P] → [Module R P] → Module.Finite R P →
      HasFiniteFreeResolution R P)
    (P : Type v) [AddCommGroup P] [Module (MvPolynomial s R) P]
    [Module.Finite (MvPolynomial s R) P] : HasFiniteFreeResolution (MvPolynomial s R) P := by
  let : Fintype s := Fintype.ofFinite s
  let n : ℕ := Fintype.card s
  let a : s ≃ Fin n := Fintype.equivFin s
  let e : MvPolynomial s R ≃+* MvPolynomial (Fin n) R := (MvPolynomial.renameEquiv R a).toRingEquiv
  let B : Type u := MvPolynomial (Fin n) R
  let : Module B P := Module.compHom P e.symm.toRingHom
  have : Module.Finite B P := by simpa [B] using (moduleFinite_of_ringEquiv' e.symm P)
  have : Small.{u} P := Module.Finite.small B P
  let P' : Type u := Shrink.{u} P
  have : Module.Finite B P' :=
    Module.Finite.of_surjective ((Shrink.linearEquiv B P).symm.toLinearMap)
      (Shrink.linearEquiv B P).symm.surjective
  have hP' : HasFiniteFreeResolution B P' :=
    mvPolynomial_hasFiniteFreeResolution_of_isNoetherianRing_aux (Fin n) hR P'
  have hPB : HasFiniteFreeResolution B P := by
    simpa [P'] using hasFiniteFreeResolution_of_linearEquiv (Shrink.linearEquiv B P) hP'
  let UB : Type (max u w) := ULift.{w} B
  let eU : MvPolynomial s R ≃+* UB := e.trans ringEquivULift.symm
  let instUB₀ : Module UB P := Module.compHom P ringEquivULift.toRingHom
  have hUB₀ : HasFiniteFreeResolution UB P := by
    simpa [UB] using (hasFiniteFreeResolution_ulift P hPB)
  let instUB₁ : Module UB P := Module.compHom P eU.symm.toRingHom
  have hinst : instUB₀ = instUB₁ := by
    refine Module.ext' instUB₀ instUB₁ ?_
    intro b x
    rfl
  have hUB₁ : @HasFiniteFreeResolution UB P _ _ instUB₁ := by
    simpa [hinst] using (show @HasFiniteFreeResolution UB P _ _ instUB₀ from hUB₀)
  have hU' : (let : Module UB P := instUB₁; HasFiniteFreeResolution UB P) := by simpa using hUB₁
  simpa [UB] using hasFiniteFreeResolution_of_ringEquiv_left eU P hU'

end MvPolynomial
