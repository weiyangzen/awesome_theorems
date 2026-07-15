/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.GrowthFunction
import Mathlib.Data.Finset.Sort
import Mathlib.Order.Fin.Basic

/-!
# The limsup flag (Lyapunov filtration)

This module builds, at each point `x`, the **limsup flag** associated to the upper Lyapunov
growth function `lambdaBar A T x` of `ErgodicTheory.Lyapunov.GrowthFunction`.

For a.e. `x` the function `lambdaBar A T x` is an `IsUltrametricGrowth` function
(`isUltrametricGrowth_lambdaBar`); its values on nonzero vectors then form a finite set
(`IsUltrametricGrowth.finite_range`), the **limsup spectrum** `lyapunovSpectrum A T x`. Enumerating
the spectrum **descending** as `λ₀ > λ₁ > ⋯ > λ_{k-1}` (`specList`), the sublevel sets
`{v | v = 0 ∨ lambdaBar A T x v ≤ λᵢ}` form a strictly decreasing flag

`⊤ = vflag x 0 ⊋ vflag x 1 ⊋ ⋯ ⊋ vflag x k = ⊥`

along which the cocycle grows at exactly the rate `λᵢ` on each stratum.

All objects are defined **totally** (with a `⊥`/`∅` junk value off the a.e. good set where
`lambdaBar A T x` is `IsUltrametricGrowth`), so the structural theorems carry an explicit
hypothesis `hx : IsUltrametricGrowth (lambdaBar A T x)`.

## Main results

* `spectrum`, `specCard`, `specList` — the finite, descending limsup spectrum;
* `vflag` — the limsup flag, indexed by `Fin (specCard A T x + 1)`;
* `vflag_zero` / `vflag_last` — the extremal levels are `⊤` / `⊥`;
* `vflag_strictAnti` — strict decrease between consecutive levels;
* `lambdaBar_eq_on_stratum` — on each stratum `lambdaBar` equals the exact exponent `λᵢ`;
* `lyapunovSpectrum_equivariant_ae` / `vflag_equivariant` — `A`-equivariance of the spectrum and the
  flag, a.e. in `x`.

## References

* D. Ruelle, *Ergodic theory of differentiable dynamical systems*,
  Publ. Math. IHÉS **50** (1979), 27–58.
* M. Viana, *Lectures on Lyapunov Exponents*, Cambridge Studies in Adv. Math. **145** (2014).
-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} {T : X → X} {d : ℕ}

/-! ### The limsup spectrum -/

/-- The (finite) **limsup spectrum** at `x`: the set of values of `lambdaBar A T x` on nonzero
vectors. Defined totally, with junk value `∅` off the set where `lambdaBar A T x` is an
`IsUltrametricGrowth` function. -/
noncomputable def lyapunovSpectrum (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) :
    Finset ℝ :=
  open Classical in
  if h : IsUltrametricGrowth (lambdaBar A T x) then h.finite_range.toFinset else ∅

/-- Membership in the spectrum: a value lies in `lyapunovSpectrum A T x` iff it is realized by some
nonzero vector. -/
theorem mem_lyapunovSpectrum {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) {r : ℝ} :
    r ∈ lyapunovSpectrum A T x ↔
      ∃ v : EuclideanSpace ℝ (Fin d), v ≠ 0 ∧ lambdaBar A T x v = r := by
  rw [lyapunovSpectrum, dif_pos hx, Set.Finite.mem_toFinset, Set.mem_range]
  exact ⟨fun ⟨v, hv⟩ => ⟨v.1, v.2, hv⟩, fun ⟨v, hv, hvr⟩ => ⟨⟨v, hv⟩, hvr⟩⟩

/-- Every value of `lambdaBar A T x` on a nonzero vector is in the spectrum. -/
theorem lambdaBar_mem_lyapunovSpectrum {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) {v : EuclideanSpace ℝ (Fin d)} (hv : v ≠ 0) :
    lambdaBar A T x v ∈ lyapunovSpectrum A T x :=
  (mem_lyapunovSpectrum hx).mpr ⟨v, hv, rfl⟩

/-- The number of distinct exponents at `x`. -/
noncomputable def specCard (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) : ℕ :=
  (lyapunovSpectrum A T x).card

/-- The **descending** enumeration of the limsup spectrum,
`specList A T x : Fin (specCard …) → ℝ`. Index `0` is the largest exponent; the listing is
strictly antitone. -/
noncomputable def specList (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) :
    Fin (specCard A T x) → ℝ :=
  fun i => (lyapunovSpectrum A T x).orderEmbOfFin rfl i.rev

/-- The descending enumeration is strictly antitone. -/
theorem specList_strictAnti (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) :
    StrictAnti (specList A T x) :=
  fun _ _ hij => (lyapunovSpectrum A T x).orderEmbOfFin rfl |>.strictMono (Fin.rev_lt_rev.mpr hij)

/-- Each enumerated exponent lies in the spectrum. -/
theorem specList_mem (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X)
    (i : Fin (specCard A T x)) : specList A T x i ∈ lyapunovSpectrum A T x :=
  (lyapunovSpectrum A T x).orderEmbOfFin_mem rfl i.rev

/-- Every spectrum value is `specList A T x i` for some index `i`. -/
theorem exists_specList_eq {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X} {r : ℝ}
    (hr : r ∈ lyapunovSpectrum A T x) : ∃ i : Fin (specCard A T x), specList A T x i = r := by
  have hrange :
      r ∈ Set.range ⇑((lyapunovSpectrum A T x).orderEmbOfFin (rfl : _ = specCard A T x)) := by
    rw [Finset.range_orderEmbOfFin]; exact hr
  obtain ⟨j, hj⟩ := hrange
  exact ⟨j.rev, by simpa [specList] using hj⟩

/-! ### The limsup flag -/

/-- The sublevel submodule of `lambdaBar A T x` at threshold `t`, defined totally with junk
value `⊥` off the `IsUltrametricGrowth` set. -/
noncomputable def lambdaSublevel (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X)
    (t : ℝ) :
    Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
  open Classical in
  if h : IsUltrametricGrowth (lambdaBar A T x) then h.sublevel t else ⊥

/-- Membership in the sublevel submodule (under the `IsUltrametricGrowth` hypothesis). -/
theorem mem_lambdaSublevel {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) (t : ℝ) (v : EuclideanSpace ℝ (Fin d)) :
    v ∈ lambdaSublevel A T x t ↔ v = 0 ∨ lambdaBar A T x v ≤ t := by
  rw [lambdaSublevel, dif_pos hx, IsUltrametricGrowth.mem_sublevel]

/-- The **limsup flag** at `x`, indexed by `Fin (specCard A T x + 1)`. Interior levels are
sublevel sets of `lambdaBar A T x` at the spectrum values; the last level (index `specCard`)
is `⊥`. With the descending enumeration `specList`, level `j` (for `j < specCard`) is the
sublevel at exponent `λ_j`, so `vflag x 0 = ⊤` and `vflag x (last) = ⊥`. -/
noncomputable def vflag (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X)
    (j : Fin (specCard A T x + 1)) : Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
  if h : (j : ℕ) < specCard A T x then lambdaSublevel A T x (specList A T x ⟨j, h⟩) else ⊥

/-- On the interior, `vflag` is a sublevel set at the corresponding spectrum value. -/
theorem vflag_of_lt {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    {j : Fin (specCard A T x + 1)} (h : (j : ℕ) < specCard A T x) :
    vflag A T x j = lambdaSublevel A T x (specList A T x ⟨j, h⟩) := by
  rw [vflag, dif_pos h]

/-- **Unified membership criterion** for a flag level (under the `IsUltrametricGrowth`
hypothesis), for a nonzero vector. -/
theorem mem_vflag {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) {j : Fin (specCard A T x + 1)}
    {v : EuclideanSpace ℝ (Fin d)} (hv : v ≠ 0) :
    v ∈ vflag A T x j ↔
      ∃ h : (j : ℕ) < specCard A T x, lambdaBar A T x v ≤ specList A T x ⟨j, h⟩ := by
  by_cases h : (j : ℕ) < specCard A T x
  · rw [vflag_of_lt h, mem_lambdaSublevel hx]
    constructor
    · rintro (rfl | hle)
      · exact absurd rfl hv
      · exact ⟨h, hle⟩
    · rintro ⟨_, hle⟩; exact Or.inr hle
  · rw [vflag, dif_neg h]
    simp only [Submodule.mem_bot, hv, false_iff, not_exists]
    exact fun h' => absurd h' h

/-! ### Extremal levels -/

/-- The top level of the flag is everything. -/
theorem vflag_zero {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) : vflag A T x 0 = ⊤ := by
  rw [eq_top_iff]
  intro v _
  by_cases hv : v = 0
  · simp [hv]
  · -- `lambdaBar x v ∈ spectrum`, so `specCard > 0`, and
    -- `lambdaBar x v ≤ specList ⟨0,_⟩ = max'`.
    have hmem : lambdaBar A T x v ∈ lyapunovSpectrum A T x := lambdaBar_mem_lyapunovSpectrum hx hv
    have hpos : 0 < specCard A T x := Finset.card_pos.mpr ⟨_, hmem⟩
    have h0 : ((0 : Fin (specCard A T x + 1)) : ℕ) < specCard A T x := by simpa using hpos
    rw [mem_vflag hx hv]
    refine ⟨h0, ?_⟩
    -- `specList ⟨0,_⟩` is the maximum of the spectrum.
    have hpos' : 0 < (lyapunovSpectrum A T x).card := hpos
    have hmax : specList A T x ⟨(0 : Fin (specCard A T x + 1)), h0⟩
        = (lyapunovSpectrum A T x).max' (Finset.card_pos.mp hpos) := by
      rw [specList, ← Finset.orderEmbOfFin_last (s := lyapunovSpectrum A T x) rfl hpos']
      congr 1
    rw [hmax]
    exact Finset.le_max' _ _ hmem

/-- The bottom level of the flag is trivial. -/
theorem vflag_last (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) :
    vflag A T x (Fin.last (specCard A T x)) = ⊥ := by
  rw [vflag, dif_neg]
  simp

/-! ### Strict decrease and stratum exactness -/

/-- A nonzero witness realizing the exponent `specList A T x i`. -/
private theorem exists_witness {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) (i : Fin (specCard A T x)) :
    ∃ w : EuclideanSpace ℝ (Fin d), w ≠ 0 ∧ lambdaBar A T x w = specList A T x i := by
  exact (mem_lyapunovSpectrum hx).mp (specList_mem A T x i)

/-- The successor index, as a member of `Fin (specCard A T x)`, when it stays interior. -/
private theorem succ_lt_specList {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (i : Fin (specCard A T x))
    (hsucc : ((i.succ : Fin (specCard A T x + 1)) : ℕ) < specCard A T x) :
    specList A T x ⟨(i.succ : Fin (specCard A T x + 1)), hsucc⟩ < specList A T x i := by
  refine specList_strictAnti A T x ?_
  -- `i < ⟨i.val + 1, _⟩` in `Fin (specCard A T x)`.
  have : (i : ℕ) < (⟨(i.succ : Fin (specCard A T x + 1)), hsucc⟩ : Fin (specCard A T x)) := by
    simp only [Fin.val_succ]
    omega
  exact this

/-- Strict decrease of the flag. -/
theorem vflag_strictAnti {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) (i : Fin (specCard A T x)) :
    vflag A T x i.succ < vflag A T x i.castSucc := by
  -- The `castSucc` level is the sublevel at `specList i`.
  have hcastval : ((i.castSucc : Fin (specCard A T x + 1)) : ℕ) = (i : ℕ) := rfl
  have hcastlt : ((i.castSucc : Fin (specCard A T x + 1)) : ℕ) < specCard A T x := i.2
  refine lt_of_le_of_ne ?_ ?_
  · -- `⊆`.
    intro v hvmem
    by_cases hv : v = 0
    · simp [hv]
    · rw [mem_vflag hx hv] at hvmem ⊢
      obtain ⟨hsucc, hle⟩ := hvmem
      refine ⟨hcastlt, ?_⟩
      -- `specList (succ) < specList i`, and the index `⟨i.castSucc⟩ = i`.
      have hid :
          (⟨(i.castSucc : Fin (specCard A T x + 1)), hcastlt⟩ : Fin (specCard A T x)) = i :=
        Fin.ext rfl
      rw [hid]
      exact hle.trans (succ_lt_specList i hsucc).le
  · -- `≠`: a witness `w` lies in `castSucc` but not in `succ`.
    intro heq
    obtain ⟨w, hw, hwval⟩ := exists_witness hx i
    have hwcast : w ∈ vflag A T x i.castSucc := by
      rw [mem_vflag hx hw]
      refine ⟨hcastlt, ?_⟩
      have hid :
          (⟨(i.castSucc : Fin (specCard A T x + 1)), hcastlt⟩ : Fin (specCard A T x)) = i :=
        Fin.ext rfl
      rw [hid, hwval]
    have hwsucc : w ∈ vflag A T x i.succ := heq ▸ hwcast
    rw [mem_vflag hx hw] at hwsucc
    obtain ⟨hsucc, hle⟩ := hwsucc
    rw [hwval] at hle
    exact absurd hle (not_le.mpr (succ_lt_specList i hsucc))

/-- On the stratum between consecutive levels, `lambdaBar` equals the exact exponent `λᵢ`. -/
theorem lambdaBar_eq_on_stratum {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) (i : Fin (specCard A T x))
    {v : EuclideanSpace ℝ (Fin d)} (hmem : v ∈ vflag A T x i.castSucc)
    (hnot : v ∉ vflag A T x i.succ) :
    lambdaBar A T x v = specList A T x i := by
  have hcastlt : ((i.castSucc : Fin (specCard A T x + 1)) : ℕ) < specCard A T x := i.2
  -- `v ≠ 0` since `0` is in every level.
  have hv : v ≠ 0 := by
    rintro rfl; exact hnot (Submodule.zero_mem _)
  -- Upper bound `lambdaBar v ≤ specList i` from `castSucc` membership.
  rw [mem_vflag hx hv] at hmem
  obtain ⟨_, hle⟩ := hmem
  have hid : (⟨(i.castSucc : Fin (specCard A T x + 1)), hcastlt⟩ : Fin (specCard A T x)) = i :=
    Fin.ext rfl
  rw [hid] at hle
  -- `lambdaBar v` is a spectrum value: `lambdaBar v = specList j` for some `j`.
  obtain ⟨j, hj⟩ := exists_specList_eq (lambdaBar_mem_lyapunovSpectrum hx hv)
  rw [← hj] at hle ⊢
  -- `specList j ≤ specList i ⟹ i ≤ j`.
  have hij : i ≤ j := (specList_strictAnti A T x).le_iff_ge.mp hle
  -- From `v ∉ vflag (succ)` and `v ≠ 0`, no interior successor bound holds.
  rw [mem_vflag hx hv, not_exists] at hnot
  -- Goal: `specList j = specList i`, i.e. `j = i` by injectivity.
  congr 1
  refine le_antisymm ?_ hij
  -- Show `j ≤ i`. Split on whether the successor index is interior.
  by_cases hsucc : ((i.succ : Fin (specCard A T x + 1)) : ℕ) < specCard A T x
  · -- Interior successor: `hnot hsucc` gives `¬ (specList j ≤ specList (succ))`,
    -- i.e. `specList (succ) < specList j`, hence `j < succ-index ≤ i + 1`, so `j ≤ i`.
    have hnle := hnot hsucc
    have hlt :
        specList A T x ⟨(i.succ : Fin (specCard A T x + 1)), hsucc⟩ < specList A T x j := by
      rw [hj]; exact not_le.mp hnle
    have hji : j < (⟨(i.succ : Fin (specCard A T x + 1)), hsucc⟩ : Fin (specCard A T x)) :=
      (specList_strictAnti A T x).lt_iff_gt.mp hlt
    have : (j : ℕ) < (i : ℕ) + 1 := by
      have := hji
      simp only [Fin.lt_def, Fin.val_succ] at this
      omega
    omega
  · -- Successor index is `last`: then `i` is the last index, so `j ≤ i` automatically.
    have : (i : ℕ) + 1 = specCard A T x := by
      have hle' : ((i.succ : Fin (specCard A T x + 1)) : ℕ) ≤ specCard A T x := by
        simp only [Fin.val_succ]; omega
      simp only [Fin.val_succ] at hsucc
      omega
    have : (j : ℕ) ≤ (i : ℕ) := by have := j.2; omega
    omega

/-! ### `A`-equivariance

The invertible matrix `A x` acts on `EuclideanSpace ℝ (Fin d)` as the bijective continuous
linear map `Matrix.toEuclideanCLM (A x)`. Since `lambdaBar A T x v = lambdaBar A T (T x) (A x · v)`
a.e. (by `lambdaBar_equivariant_ae`), this bijection identifies the spectrum and the sublevel
sets at `x` with those at `T x`. -/

/-- The continuous linear endomorphism induced by `A x`. -/
private noncomputable def Aclm (A : X → Matrix (Fin d) (Fin d) ℝ) (x : X) :
    EuclideanSpace ℝ (Fin d) →L[ℝ] EuclideanSpace ℝ (Fin d) :=
  Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)

/-- The action of `A x` is a left inverse to the action of `(A x)⁻¹`, and conversely. -/
private theorem Aclm_inv_left {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹ (Aclm A x v) = v := by
  rw [Aclm, ← ContinuousLinearMap.mul_apply, ← map_mul,
    Matrix.nonsing_inv_mul _ (Ne.isUnit (hA x)), map_one, ContinuousLinearMap.one_apply]

private theorem Aclm_inv_right {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)
        (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹ v) = v := by
  rw [← ContinuousLinearMap.mul_apply, ← map_mul,
    Matrix.mul_nonsing_inv _ (Ne.isUnit (hA x)), map_one, ContinuousLinearMap.one_apply]

/-- The action of `A x` sends a nonzero vector to a nonzero vector. -/
private theorem Aclm_ne_zero {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) {v : EuclideanSpace ℝ (Fin d)} (hv : v ≠ 0) :
    Aclm A x v ≠ 0 := by
  intro h
  apply hv
  have := Aclm_inv_left hA x v
  rw [h, map_zero] at this
  exact this.symm

variable [MeasurableSpace X] {μ : Measure X}

/-- **`A`-equivariance of the spectrum (a.e.).** For a.e. `x`,
`lyapunovSpectrum A T x = lyapunovSpectrum A T (T x)`, hence `specCard` and `specList` agree (the
latter as indexed functions over `Fin (specCard …)`). -/
theorem lyapunovSpectrum_equivariant_ae
    [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, lyapunovSpectrum A T x = lyapunovSpectrum A T (T x) := by
  filter_upwards [lambdaBar_equivariant_ae hT hA hAmeas hint hint',
    isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint',
    hT.toMeasurePreserving.quasiMeasurePreserving.ae
      (isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint')] with x hequiv hx hTx
  ext r
  rw [mem_lyapunovSpectrum hx, mem_lyapunovSpectrum hTx]
  constructor
  · -- a witness `v` at `x` maps to the witness `A x · v` at `T x`.
    rintro ⟨v, hv, rfl⟩
    refine ⟨Aclm A x v, Aclm_ne_zero hA x hv, ?_⟩
    rw [Aclm, ← hequiv v hv]
  · -- a witness `w` at `T x` pulls back to `(A x)⁻¹ · w` at `x`.
    rintro ⟨w, hw, rfl⟩
    refine ⟨Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹ w, ?_, ?_⟩
    · intro h
      apply hw
      have := Aclm_inv_right hA x w
      rw [h, map_zero] at this
      exact this.symm
    · -- `lambdaBar x ((A x)⁻¹ w) = lambdaBar (T x) (A x · (A x)⁻¹ w) = lambdaBar (T x) w`.
      have hne : Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹ w ≠ 0 := by
        intro h
        apply hw
        have := Aclm_inv_right hA x w
        rw [h, map_zero] at this
        exact this.symm
      rw [hequiv _ hne]
      congr 1
      exact Aclm_inv_right hA x w

/-- **`A`-equivariance of the flag (a.e.).** For a.e. `x`, the action of `A x` maps each flag
level at `x` onto the corresponding level at `T x` (the indices transport via the a.e.
equality `lyapunovSpectrum A T x = lyapunovSpectrum A T (T x)`, which makes
`specCard A T x = specCard A T (T x)` and `specList A T x = specList A T (T x)` after that
rewrite). -/
theorem vflag_equivariant
    [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, ∀ t : ℝ,
      Submodule.map (Aclm A x).toLinearMap (lambdaSublevel A T x t) =
        lambdaSublevel A T (T x) t := by
  filter_upwards [lambdaBar_equivariant_ae hT hA hAmeas hint hint',
    isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint',
    hT.toMeasurePreserving.quasiMeasurePreserving.ae
      (isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint')] with x hequiv hx hTx
  intro t
  ext w
  rw [Submodule.mem_map]
  constructor
  · -- `w = A x · v` with `v ∈ sublevel x t`.
    rintro ⟨v, hv, rfl⟩
    rw [mem_lambdaSublevel hx] at hv
    rw [mem_lambdaSublevel hTx]
    rcases hv with rfl | hle
    · left; simp [Aclm]
    · by_cases hv0 : v = 0
      · left; simp [hv0, Aclm]
      · right
        rw [ContinuousLinearMap.coe_coe, Aclm, ← hequiv v hv0]
        exact hle
  · -- `w ∈ sublevel (T x) t`; pull back via `(A x)⁻¹`.
    intro hw
    rw [mem_lambdaSublevel hTx] at hw
    refine ⟨Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹ w, ?_, ?_⟩
    · rw [mem_lambdaSublevel hx]
      rcases hw with rfl | hle
      · left; simp
      · by_cases hw0 : w = 0
        · left; simp [hw0]
        · right
          have hne : Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹ w ≠ 0 := by
            intro h
            apply hw0
            have := Aclm_inv_right hA x w
            rw [h, map_zero] at this
            exact this.symm
          rw [hequiv _ hne, Aclm_inv_right hA x w]
          exact hle
    · rw [ContinuousLinearMap.coe_coe]
      exact Aclm_inv_right hA x w

end ErgodicTheory
