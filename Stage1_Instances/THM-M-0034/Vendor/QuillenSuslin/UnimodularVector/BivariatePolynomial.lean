/-
Copyright (c) 2026 Yongle Hu. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yongle Hu
-/
import Mathlib.Algebra.Polynomial.Bivariate
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Defs
import Mathlib.RingTheory.Localization.Integer

open Module Polynomial Finset Bivariate

noncomputable section

variable {R : Type*} [CommRing R]
variable {s : Type*} [Fintype s] [DecidableEq s]

section definitions

variable {S : Submonoid R} (v : s → R[X])
  {x : (Localization S)[X][Y]} (c : S) (M : GL s (Localization S)[X])

instance : Algebra R[X] (Localization S)[X] :=
  (mapRingHom (algebraMap R (Localization S))).toAlgebra

/-- The canonical `R[X][Y]`-algebra structure on `(Localization S)[X][Y]`. -/
instance : Algebra R[X][Y] (Localization S)[X][Y] :=
  (mapRingHom (algebraMap R[X] (Localization S)[X])).toAlgebra

/-- The `R[X][Y]`-endomorphism scaling `Y` by `c`. -/
def σR : R[X][Y] →+* R[X][Y] :=
    eval₂RingHom (C : R[X] →+* R[X][Y]) ((c : R) • (X : R[X][Y]))

/-- The `(Localization S)[X][Y]`-endomorphism scaling `Y` by the image of `c`. -/
def σA : (Localization S)[X][Y] →+* (Localization S)[X][Y] :=
  eval₂RingHom C
    (((algebraMap R (Localization S)) (c : R)) • (X : (Localization S)[X][Y]))

/-- `σA` commutes with the canonical map `R[X][Y] → (Localization S)[X][Y]`. -/
theorem σA_comp : (σA c).comp (algebraMap R[X][Y] (Localization S)[X][Y]) =
    (algebraMap R[X][Y] (Localization S)[X][Y]).comp (σR c) := by
  have hAlg : algebraMap R[X][Y] (Localization S)[X][Y] =
    (mapRingHom (algebraMap R[X] (Localization S)[X])) := rfl
  refine ringHom_ext ?_ ?_
  · intro p
    have hC : algebraMap R[X][Y] (Localization S)[X][Y] (C p) =
        C (algebraMap R[X] (Localization S)[X] p) := by
      rw [hAlg]
      simp
    have hσR : σR c (C p) = C p := by
      show (C p).eval₂ (C : R[X] →+* R[X][Y]) ((c : R) • (X : R[X][Y])) = C p
      rw [eval₂_C]
    simp only [RingHom.comp_apply]
    rw [hσR, hC]
    show (C (algebraMap R[X] (Localization S)[X] p)).eval₂ C _ = _
    rw [eval₂_C]
  · have hX : algebraMap R[X][Y] (Localization S)[X][Y] X = X := by
      rw [hAlg]
      simp [mapRingHom]
    have hσR : σR c X = (c : R) • X := by
      show X.eval₂ (C : R[X] →+* R[X][Y]) ((c : R) • (X : R[X][Y])) = (c : R) • X
      rw [eval₂_X]
    have hσA : σA c X = ((algebraMap R (Localization S)) (c : R)) • X := by
      show X.eval₂ C (((algebraMap R (Localization S)) (c : R)) • X) = _
      rw [eval₂_X]
    simp only [RingHom.comp_apply]
    rw [hσR, hX, hσA, Algebra.smul_def, Algebra.smul_def]
    simp

theorem isInteger_σA (hx : IsLocalization.IsInteger R[X][Y] x) :
    IsLocalization.IsInteger R[X][Y] (σA c x) := by
  rcases hx with ⟨r, rfl⟩
  refine ⟨σR c r, ?_⟩
  have := congrArg (fun f => f r) (σA_comp c)
  simpa using this.symm

variable (S)

def CAY : (Localization S)[X] →+* (Localization S)[X][Y] := C

def φ : (Localization S)[X] →+* (Localization S)[X][Y] :=
  eval₂RingHom ((CAY S).comp C) ((CAY S X) + Y)

def Mx : GL s (Localization S)[X][Y] := (Matrix.GeneralLinearGroup.map (CAY S)) M

def Mxy : GL s (Localization S)[X][Y] := (Matrix.GeneralLinearGroup.map (φ S)) M

def N : GL s (Localization S)[X][Y] := (Mx S M)⁻¹ * (Mxy S M)

def W : Matrix s s (Localization S)[X][Y] := fun i j => ((N S M).1 i j).divX

variable {S}

def Ncy : GL s (Localization S)[X][Y] := Matrix.GeneralLinearGroup.map (σA c) (N S M)

def NcyInv : GL s (Localization S)[X][Y] := Matrix.GeneralLinearGroup.map (σA c) (N S M)⁻¹

end definitions

section lemmas

variable [IsDomain R] {S : Submonoid R} (hs : S ≤ nonZeroDivisors R) (v : s → R[X])
  {x : (Localization S)[X][Y]} (M : GL s (Localization S)[X])
  (hM : (M.1.mulVec fun i ↦ Polynomial.map (algebraMap R (Localization S)) (v i)) =
     fun i ↦ C ((algebraMap R (Localization S)) (eval 0 (v i))))
  {c : S} (hc : ∀ i j : s, IsLocalization.IsInteger R[X][Y]
    ((C (C (c : R)) : R[X][Y]) • σA c ((W S M) i j)))

omit [IsDomain R] in
lemma N_entry_decomp (M : GL s (Localization S)[X]) (i j : s) :
    (N S M).1 i j = X * (W S M i j) + C (if i = j then 1 else 0) := by
  let ev0 : (Localization S)[X][Y] →+* (Localization S)[X] := eval₂RingHom (RingHom.id _) 0
  let map0 : GL s (Localization S)[X][Y] →* GL s (Localization S)[X] :=
    Matrix.GeneralLinearGroup.map ev0
  have hMx0 : map0 (Mx S M) = M := by
    ext i j
    simp [map0, Mx, ev0, CAY]
  have hev0φ : ev0.comp (φ S) = RingHom.id (Localization S)[X] := by
    refine ringHom_ext (fun a => ?_) ?_
    · simp [ev0, φ, CAY]
    · simp [ev0, φ, CAY]
  have hφ0 (p : (Localization S)[X]) : ev0 (φ S p) = p := by
    simpa [RingHom.comp_apply] using congrArg (fun f => f p) hev0φ
  have hMxy0 : map0 (Mxy S M) = M := by
    ext i j
    simp [map0, Mxy, Matrix.GeneralLinearGroup.map_apply, hφ0]
  have hN0 : map0 (N S M) = 1 := by
    simp [map0, N, hMx0, hMxy0]
  have hcoeff0N : ((N S M).1 i j).coeff 0 =
      (if i = j then 1 else 0) := by
    have hij' : ev0 ((N S M).1 i j) = (if i = j then 1 else 0) := by
      simpa [map0, Matrix.GeneralLinearGroup.map_apply, Matrix.one_apply] using
        congrArg (fun A : Matrix s s (Localization S)[X] => A i j) <| congrArg Units.val hN0
    simpa [ev0, coeff_zero_eq_eval_zero] using hij'
  simpa [W, hcoeff0N, add_comm] using ( X_mul_divX_add ((N S M) i j)).symm

omit [IsDomain R] in
lemma ncy_isInteger_eq (i j : s) (w : R[X][Y]) (hw : (algebraMap R[X][Y] (Localization S)[X][Y]) w =
    (C (C (c : R)) : R[X][Y]) • σA c ((W S M) i j)) :
    algebraMap R[X][Y] (Localization S)[X][Y] (X * w + C (if i = j then 1 else 0 : R[X])) =
      (Ncy c M).1 i j := by
  let b : R[X][Y] := C (C (c : R))
  have hN_entry := N_entry_decomp M i j
  let ι : R →+* Localization S := algebraMap R (Localization S)
  have hCι : mapRingHom ι (C (c : R)) = C (ι (c : R)) := by
    rw [← RingHom.comp_apply]
    exact congrArg (fun g : R →+* (Localization S)[X] => g (c : R)) (mapRingHom_comp_C ι)
  have hbMap : algebraMap R[X][Y] (Localization S)[X][Y] b = (C (C (ι (c : R)))) := by
    simp [b, ι, map_C, hCι]
  have hσA_X : σA c Y = algebraMap R[X][Y] (Localization S)[X][Y] b * X := by
    have hσA_X0 : σA c Y = (ι (c : R)) • Y := by
      dsimp [σA, ι]
      exact eval₂_X _ ((algebraMap R (Localization S) (c : R)) • Y)
    calc _ = (ι (c : R)) • Y := hσA_X0
      _ = (C (C (ι (c : R)))) * X := by simp [Algebra.smul_def]
      _ = algebraMap R[X][Y] (Localization S)[X][Y] b * X := congrArg (fun t => t * X) hbMap.symm
  have hNcyij : ((Ncy c M).1 i j) = σA c ((N S M).1 i j) := by
    simp only [Ncy, Matrix.GeneralLinearGroup.map_apply]
  have hmap : algebraMap R[X][Y] (Localization S)[X][Y] (X * w + C (if i = j then 1 else 0 : R[X]))
      = X * algebraMap R[X][Y] (Localization S)[X][Y] w + C (if i = j then 1 else 0) := by
    let f : R[X][Y] →+* (Localization S)[X][Y] := algebraMap R[X][Y] (Localization S)[X][Y]
    have hadd : f (X * w + C (if i = j then 1 else 0 : R[X])) =
        f (X * w) + f (C (if i = j then 1 else 0 : R[X])) :=
      f.map_add (X * w) (C (if i = j then 1 else 0 : R[X]))
    have hmul : f (X * w) = f X * f w := f.map_mul X w
    have hC : f (C (if i = j then 1 else 0 : R[X])) =
        C (if i = j then 1 else 0 : (Localization S)[X]) := by simp [f]
    have hX : f X = X := by simp [f]
    rw [hadd, hmul, hC, hX]
  rw [hmap, hw, hNcyij, hN_entry]
  rw [(σA c).map_add (X * W S M i j) (C (if i = j then 1 else 0 : (Localization S)[X]))]
  rw [(σA c).map_mul X (W S M i j)]
  have hσA_C : σA c (C (if i = j then 1 else 0 : (Localization S)[X])) =
      C (if i = j then 1 else 0 : (Localization S)[X]) := by
    show eval₂ C _ _ = _
    rw [eval₂_C]
  rw [hσA_X, hbMap, hσA_C, Algebra.smul_def]
  have hbMapC : algebraMap R[X][Y] (Localization S)[X][Y] (C (C (c : R))) = C (C (ι (c : R))) := by
    simpa [b] using hbMap
  rw [hbMapC]
  have hmul : Y * (C (C (ι (c : R))) * (σA c) (W S M i j)) =
      C (C (ι (c : R))) * (Y * (σA c) (W S M i j)) := by
    calc _ = (Y * C (C (ι (c : R)))) * (σA c) (W S M i j) := by rw [← mul_assoc]
      _ = (C (C (ι (c : R))) * Y) * (σA c) (W S M i j) := by rw [mul_comm Y (C (C (ι (c : R))))]
      _ = C (C (ι (c : R))) * (Y * (σA c) (W S M i j)) := by rw [mul_assoc]
  simp [hmul, mul_assoc]

lemma det_N_eq_one (M : GL s (Localization S)[X]) : Matrix.det ((N S M).1) = 1 := by
  let ev0 : (Localization S)[X][Y] →+* (Localization S)[X] := eval₂RingHom (RingHom.id _) 0
  have hev0_X : ev0 X = 0 := by simp [ev0]
  have hN0mat : ev0.mapMatrix ((N S M).1) = 1 := by
    apply Matrix.ext
    intro i j
    rw [Matrix.one_apply, RingHom.mapMatrix_apply, Matrix.map_apply]
    rw [N_entry_decomp M i j, ev0.map_add, ev0.map_mul, hev0_X]
    simp [ev0]
  have hdet_ev0 : ev0 (Matrix.det ((N S M).1)) = 1 := by
    calc _ = Matrix.det (ev0.mapMatrix ((N S M).1)) := by simpa using RingHom.map_det ev0 (N S M).1
      _ = 1 := by simp [hN0mat]
  have hdet_isUnit : IsUnit (Matrix.det ((N S M).1)) := by simp
  let p : (Localization S)[X][Y] := Matrix.det ((N S M).1)
  have hp_isUnit : IsUnit p := by simp [p]
  have hp0_unit : IsUnit (p.coeff 0) ∧ ∀ n : ℕ, n ≠ 0 → IsNilpotent (p.coeff n) :=
    isUnit_iff_coeff_isUnit_isNilpotent.1 hp_isUnit
  have hp_coeff : ∀ n : ℕ, n ≠ 0 → p.coeff n = 0 := by
    intro n hn
    exact (hp0_unit.2 n hn).eq_zero
  have hpC : C (p.coeff 0) = p := by
    apply Polynomial.ext
    intro n
    by_cases hn : n = 0
    · subst hn; simp
    · simp [coeff_C, hn, hp_coeff n hn]
  have hp0 : p.coeff 0 = 1 := by
    have : ev0 p = 1 := by simpa [p] using hdet_ev0
    simpa [ev0, eval₂_at_zero] using this
  have : p = 1 := by
    calc p = C (p.coeff 0) := by simp [hpC]
      _ = C (1 : (Localization S)[X]) := by simp [hp0]
      _ = 1 := by simp
  simpa [p] using this

omit [IsDomain R] in
lemma σA_map_det (c : S) (A : Matrix s s (Localization S)[X][Y]) :
    σA c A.det = Matrix.det ((σA c).mapMatrix A) := by
  let t : (Localization S)[X][Y] := ((algebraMap R (Localization S)) (c : R)) • Y
  have hC (p : (Localization S)[X]) : σA c (C p) = C p := by
    dsimp [σA, t]
    show eval₂ (C : (Localization S)[X] →+* (Localization S)[X][Y]) t (C p) = C p
    simp
  have hInt (n : ℤ) : σA c (n : (Localization S)[X][Y]) = (n : (Localization S)[X][Y]) := by
    calc _ = σA c (C (n : (Localization S)[X])) := by simp
      _ = C (n : (Localization S)[X]) := hC (n : (Localization S)[X])
      _ = (n : (Localization S)[X][Y]) := by simp
  simp only [Matrix.det_apply', map_sum, map_mul, hInt, map_prod, RingHom.mapMatrix_apply,
    Matrix.map_apply]

lemma det_Ncy_eq_one (c : S) (M : GL s (Localization S)[X]) :
    Matrix.det ((Ncy c M).1) = 1 := by
  have hdetN : Matrix.det ((N S M).1) = 1 := det_N_eq_one M
  have hNcy : (σA c).mapMatrix (N S M).1 = (Ncy c M).1 := by
    ext i j
    simp [Ncy, Matrix.GeneralLinearGroup.map_apply]
  have hdetVal : σA c (Matrix.det ((N S M).1)) = Matrix.det ((Ncy c M).1) := by
    simpa [hNcy] using σA_map_det c (N S M).1
  calc _ = σA c (Matrix.det ((N S M).1)) := by simpa using hdetVal.symm
    _ = 1 := by simp [hdetN]

include hc

omit [IsDomain R] in
theorem ncy_isInteger (i j : s) : IsLocalization.IsInteger R[X][Y] ((Ncy c M).1 i j) := by
  rcases hc i j with ⟨w, hw⟩
  exact ⟨X * w + C (if i = j then 1 else 0 : R[X]), ncy_isInteger_eq M i j w hw⟩

def N0 : Matrix s s R[X][Y] := fun i j => (ncy_isInteger M hc i j).choose

def N0Inv : Matrix s s R[X][Y] := (N0 M hc).adjugate

include hs

/-- The determinant of `N0` is `1`. -/
lemma det_N0_eq_one : Matrix.det (N0 M hc) = 1 :=
  let f : R[X][Y] →+* (Localization S)[X][Y] := algebraMap R[X][Y] (Localization S)[X][Y]
  have hf : Function.Injective f := by
    have hR : Function.Injective (algebraMap R (Localization S)) :=
      IsLocalization.injective (Localization S) hs
    have hRX : Function.Injective (algebraMap R[X] (Localization S)[X]) := by
      simpa [Polynomial.algebraMap_def] using map_injective (algebraMap R _) hR
    simpa [f, Polynomial.algebraMap_def] using
      map_injective (algebraMap R[X] (Localization S)[X]) hRX
  have hN0 : f.mapMatrix (N0 M hc) = (Ncy c M).1 := by
    apply Matrix.ext
    intro i j
    simpa [RingHom.mapMatrix_apply, Matrix.map_apply, N0, f] using
      (ncy_isInteger M hc i j).choose_spec
  have hdet_map (A : Matrix s s R[X][Y]) : f (Matrix.det A) = Matrix.det (f.mapMatrix A) := by
    simp [Matrix.det_apply', map_sum, map_prod, RingHom.mapMatrix_apply, Matrix.map_apply]
  have hdet : f (Matrix.det (N0 M hc)) = f 1 := by
    calc _ = Matrix.det (f.mapMatrix (N0 M hc)) := hdet_map (N0 M hc)
      _ = Matrix.det ((Ncy c M).1) := by simp [hN0]
      _ = 1 := det_Ncy_eq_one c M
      _ = f 1 := by simp [f]
  hf hdet

theorem hN0_mul : N0 M hc * N0Inv M hc = 1 := by
  have hdet : Matrix.det (N0 M hc) = 1 := det_N0_eq_one hs M hc
  have h : N0 M hc * (N0 M hc).adjugate = _ := Matrix.mul_adjugate (N0 M hc)
  calc _ = Matrix.det (N0 M hc) • (1 : Matrix s s R[X][Y]) := h
    _ = (1 : R[X][Y]) • (1 : Matrix s s R[X][Y]) := by rw [hdet]
    _ = 1 := one_smul _ _

theorem hN0inv_mul : N0Inv M hc * N0 M hc = 1 := by
  have hdet : Matrix.det (N0 M hc) = 1 := det_N0_eq_one hs M hc
  have h : (N0 M hc).adjugate * N0 M hc = _ := Matrix.adjugate_mul (N0 M hc)
  calc _ = Matrix.det (N0 M hc) • (1 : Matrix s s R[X][Y]) := h
    _ = (1 : R[X][Y]) • (1 : Matrix s s R[X][Y]) := by rw [hdet]
    _ = 1 := one_smul _ _

def U : GL s R[X][Y] := ⟨N0 M hc, N0Inv M hc, hN0_mul hs M hc, hN0inv_mul hs M hc⟩

include hM

set_option maxHeartbeats 300000 in
theorem hU : (N0Inv M hc).mulVec (fun i => C (v i)) =
    fun i => (v i).eval₂ ((C : R[X] →+* R[X][Y]).comp C) (C X + (c : R) • Y) := by
  let f : R[X][Y] →+* (Localization S)[X][Y] := algebraMap R[X][Y] (Localization S)[X][Y]
  have hf : Function.Injective f := by
    have hR : Function.Injective (algebraMap R (Localization S)) :=
      IsLocalization.injective (Localization S) hs
    have hRX : Function.Injective (algebraMap R[X] (Localization S)[X]) := by
      simpa [Polynomial.algebraMap_def] using map_injective (algebraMap R _) hR
    simpa [f, Polynomial.algebraMap_def] using
      map_injective (algebraMap R[X] (Localization S)[X]) hRX
  have hN0 : f.mapMatrix (N0 M hc) = (Ncy c M).1 := by
    apply Matrix.ext
    intro i j
    simpa [RingHom.mapMatrix_apply, Matrix.map_apply, N0, f] using
      (ncy_isInteger M hc i j).choose_spec
  have hUinv : f.mapMatrix (N0Inv M hc) = (NcyInv c M).1 := by
    have hN0inv : f.mapMatrix (N0Inv M hc) * f.mapMatrix (N0 M hc) = 1 := by
      simpa [Matrix.map_mul] using congrArg f.mapMatrix (hN0inv_mul hs M hc)
    have hN0mul : f.mapMatrix (N0 M hc) * f.mapMatrix (N0Inv M hc) = 1 := by
      simpa [Matrix.map_mul] using congrArg f.mapMatrix (hN0_mul hs M hc)
    have hNcyInv : (Ncy c M).1 * (NcyInv c M).1 = 1 := by
      have hdef : NcyInv c M = (Ncy c M)⁻¹ := by simp [NcyInv, Ncy]
      have hGL : Ncy c M * NcyInv c M = 1 := by
        rw [hdef]
        simp
      simpa using congrArg (fun g : GL s (Localization S)[X][Y] => g.1) hGL
    have hNcyInv' : (NcyInv c M).1 * (Ncy c M).1 = 1 := by
      have hdef : NcyInv c M = (Ncy c M)⁻¹ := by simp [NcyInv, Ncy]
      have hGL : NcyInv c M * Ncy c M = 1 := by
        rw [hdef]
        simp
      simpa using congrArg (fun g : GL s (Localization S)[X][Y] =>
        g.1) hGL
    have hleft : f.mapMatrix (N0Inv M hc) * (Ncy c M).1 = 1 := by
      simpa [hN0] using hN0inv
    have hright : (Ncy c M).1 * f.mapMatrix (N0Inv M hc) = 1 := by
      simpa [hN0] using hN0mul
    have hinv : f.mapMatrix (N0Inv M hc) = (NcyInv c M).1 := by
      calc _ = f.mapMatrix (N0Inv M hc) * 1 := by simp
        _ = f.mapMatrix (N0Inv M hc) * ((Ncy c M).1 * (NcyInv c M).1) := by rw [← hNcyInv]
        _ = (f.mapMatrix (N0Inv M hc) * (Ncy c M).1) * (NcyInv c M).1 := by
          simp [Matrix.mul_assoc]
        _ = (NcyInv c M).1 := by rw [hleft]; simp
    exact hinv
  have hvec : (fun i => f (C (v i))) =
      fun i => C (map (algebraMap R (Localization S)) (v i)) := by
    funext i
    simp [f]
  have hloc : (NcyInv c M).1.mulVec (fun i => C (map (algebraMap R (Localization S)) (v i))) =
      fun i => σA c (φ S (map (algebraMap R (Localization S)) (v i))) := by
    let a : R →+* Localization S := algebraMap R (Localization S)
    let u : s → (Localization S)[X] := fun i => (v i).map a
    let uC : s → (Localization S)[X][Y] := fun i => C (u i)
    let uφ : s → (Localization S)[X][Y] := fun i => φ S (u i)
    let b : s → (Localization S)[X][Y] := fun i => C (C (a (eval 0 (v i))))
    have hMx : (Mx S M).1.mulVec uC = b := by
      have h1 : ((CAY S).mapMatrix M.1).mulVec (fun i => CAY S (u i)) =
          fun i => CAY S ((M.1.mulVec u) i) := by
        funext i
        simpa [RingHom.mapMatrix_apply, Matrix.map_apply, Function.comp] using
          (RingHom.map_mulVec (CAY S) M.1 u i).symm
      have h2 : (Mx S M).1 = (CAY S).mapMatrix M.1 := by simp [Mx]
      have h3 : (fun i => (CAY S) ((M.1.mulVec u) i)) = b := by
        funext i
        have : (M.1.mulVec u) i = C (a (eval 0 (v i))) := by
          simpa [u, a] using congrArg (fun v => v i) hM
        simp [b, this, CAY]
      have h1' : (Mx S M).1.mulVec uC = fun i => CAY S ((M.1.mulVec u) i) := by
        simpa [h2, uC, CAY] using h1
      exact h1'.trans h3
    have hMxy : (Mxy S M).1.mulVec uφ = b := by
      have h1 : ((φ S).mapMatrix M.1).mulVec (fun i => φ S (u i)) =
          fun i => φ S ((M.1.mulVec u) i) := by
        funext i
        simpa [RingHom.mapMatrix_apply, Matrix.map_apply, Function.comp] using
          (RingHom.map_mulVec (φ S) M.1 u i).symm
      have h2 : (Mxy S M).1 = (φ S).mapMatrix M.1 := by simp [Mxy]
      have h3 : (fun i => (φ S) ((M.1.mulVec u) i)) = b := by
        funext i
        have : (M.1.mulVec u) i = C (a (eval 0 (v i))) := by
          simpa [u, a] using congrArg (fun v => v i) hM
        simp [b, this, φ, CAY]
      have h1' : (Mxy S M).1.mulVec uφ = fun i => φ S ((M.1.mulVec u) i) := by
        simpa [h2, uφ] using h1
      exact h1'.trans h3
    have hN : (N S M).1.mulVec uφ = uC := by
      calc _ = (((Mx S M)⁻¹).1 * (Mxy S M).1).mulVec uφ := rfl
        _ = ((Mx S M)⁻¹).1.mulVec ((Mxy S M).1.mulVec uφ) := by simp
        _ = ((Mx S M)⁻¹).1.mulVec b := by rw [hMxy]
        _ = ((Mx S M)⁻¹).1.mulVec ((Mx S M).1.mulVec uC) := by rw [← hMx]
        _ = uC := by
          have hGL : (Mx S M)⁻¹ * Mx S M = 1 :=
            inv_mul_cancel (Mx S M)
          have hmat : ((Mx S M)⁻¹).1 * (Mx S M).1 = 1 :=
            congrArg (fun g : GL s (Localization S)[X][Y] =>
              g.1) (inv_mul_cancel (Mx S M))
          rw [Matrix.mulVec_mulVec, hmat]
          simp
    have hNcy : (Ncy c M).1.mulVec (fun i => σA c (uφ i)) = uC := by
      have h1 : ((σA c).mapMatrix (N S M).1).mulVec (fun i => σA c (uφ i)) =
          fun i => σA c (((N S M).1.mulVec uφ) i) := by
        funext i
        simpa [RingHom.mapMatrix_apply, Matrix.map_apply, Function.comp] using
          (RingHom.map_mulVec (σA c) (N S M).1 uφ i).symm
      have h2 : (Ncy c M).1 = (σA c).mapMatrix (N S M).1 := by simp [Ncy]
      have h3 : (fun i => σA c ((N S M).1.mulVec uφ i)) = uC := by
        funext i
        have hi : (N S M).1.mulVec uφ i = uC i := by
          simpa using congrArg (fun g => g i) hN
        rw [hi]
        exact (congrArg (fun f => f (C (u i))) <| coe_eval₂RingHom
          (C : (Localization S)[X] →+* (Localization S)[X][Y])
            (((algebraMap R (Localization S)) (c : R)) • Y)).trans <|
              eval₂_C (C : (Localization S)[X] →+* (Localization S)[X][Y])
                (((algebraMap R (Localization S)) (c : R)) • Y)
      simpa [h2, h3] using h1
    have hInv : NcyInv c M * Ncy c M = 1 := by
      have hNcyInv : NcyInv c M = (Ncy c M)⁻¹ := by rfl
      rw [hNcyInv]
      exact inv_mul_cancel (Ncy c M)
    have hvec := congrArg (fun A : Matrix s s (Localization S)[X][Y] =>
      A.mulVec (fun i => σA c (uφ i))) <| congrArg Units.val hInv
    have hmul : ((NcyInv c M).1 * (Ncy c M).1).mulVec (fun i => σA c (uφ i)) =
        (NcyInv c M).1.mulVec ((Ncy c M).1.mulVec (fun i => σA c (uφ i))) := by
      simp
    have hone : (1 : Matrix s s (Localization S)[X][Y]).mulVec
        (fun i => σA c (uφ i)) = fun i => σA c (uφ i) := by
      simp
    have hres : (NcyInv c M).1.mulVec uC = fun i => σA c (uφ i) := by
      dsimp at hvec
      rw [hmul] at hvec
      rw [hNcy] at hvec
      simpa [hone] using hvec
    simpa [u, a, uφ] using hres
  funext i
  apply hf
  have hL : f ((N0Inv M hc).mulVec (fun i => C (v i)) i) =
      (NcyInv c M).1.mulVec (fun i => C (map (algebraMap R (Localization S)) (v i))) i := by
    have hv : (f ∘ fun j => C (v j)) = fun j => C (map (algebraMap R (Localization S)) (v j)) := by
      simpa [Function.comp] using hvec
    have hUinv' : (N0Inv M hc).map f = (NcyInv c M).1 := by
      apply Matrix.ext
      intro j k
      have hjk := congrArg (fun A : Matrix s s (Localization S)[X][Y] => A j k) hUinv
      simpa [RingHom.mapMatrix_apply, Matrix.map_apply] using hjk
    have h := RingHom.map_mulVec f (N0Inv M hc) (fun j => C (v j)) i
    rw [hv] at h
    rwa [hUinv'] at h
  have hR : f ((v i).eval₂ ((C : R[X] →+* R[X][Y]).comp C) (C X + (c : R) • Y)) =
      σA c (φ S (map (algebraMap R (Localization S)) (v i))) := by
    let a0 : R →+* Localization S := algebraMap R (Localization S)
    let coeff : R →+* R[X][Y] := (C : R[X] →+* R[X][Y]).comp C
    let P : R[X][Y] := (v i).eval₂ coeff (C X + Y)
    have hcoeff : (σR c).comp coeff = coeff := by
      refine RingHom.ext fun r => ?_
      dsimp [coeff, σR]
      rw [eval₂_C]
    have hx : σR c (C X + Y) = C X + (c : R) • Y := by
      dsimp [σR]
      rw [eval₂_add, eval₂_C, eval₂_X]
    have hσR : σR c P = (v i).eval₂ coeff (C X + (c : R) • Y) := by
      have h := hom_eval₂ (v i) coeff (σR c) (C X + Y)
      rwa [hcoeff, hx] at h
    have hσAcomp := congrArg (fun g : R[X][Y] →+* (Localization S)[X][Y] => g P) (σA_comp c)
    have hσA : f (σR c P) = σA c (f P) := hσAcomp.symm
    let CC : Localization S →+* (Localization S)[X][Y] :=
      (C : (Localization S)[X] →+* (Localization S)[X][Y]).comp
        (C : Localization S →+* (Localization S)[X])
    have hfcoeff : f.comp coeff = CC.comp a0 := by
      ext r
      simp [coeff, CC, a0, f]
    have hfx : f (C X + Y) = C X + Y := by
      simp [f]
    have hP : f P = φ S (map a0 (v i)) := by
      have h := hom_eval₂ (v i) coeff f (C X + Y)
      have hfP : f P = (v i).eval₂ (f.comp coeff) (f (C X + Y)) := by simpa [P] using h
      rw [hfcoeff, hfx] at hfP
      calc f P = (v i).eval₂ (CC.comp a0) (C X + Y) := hfP
        _ = (map a0 (v i)).eval₂ CC (C X + Y) := by simpa using (eval₂_map a0 CC (C X + Y)).symm
        _ = φ S (map a0 (v i)) := rfl
    have hR0 : f ((v i).eval₂ coeff (C X + (c : R) • Y)) = σA c (f P) := by
      have : (v i).eval₂ coeff (C X + (c : R) • Y) = σR c P := hσR.symm
      rw [this]
      exact hσA
    have hR1 : σA c (f P) = σA c (φ S (map a0 (v i))) := by simp [hP]
    exact hR0.trans hR1
  exact hL.trans <| (congrArg (fun g => g i) hloc).trans hR.symm

end lemmas
