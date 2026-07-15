/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.FiltrationFromInterfaces
import ErgodicTheory.Lyapunov.ForwardAngle

/-!
# Reducing the interface hypotheses of the Oseledets filtration

This file provides three independent reduction steps feeding the final assembly of
`ErgodicTheory.oseledets_filtration`:

1. `tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower` — the per-vector exact growth interface
   (`hgrowth`) from the per-vector upper bound (`limsup ≤ specList`) and lower bound
   (`specList ≤ liminf`), squeezed to a genuine `Tendsto` via
   `tendsto_inv_mul_log_norm_cocycle_apply`.

2. `oseledets_filtration_of_interfaces'` — a re-pointing of the assembly from the
   only-a.e.-measurable limsup flag `vflag` onto an everywhere-measurable family (built from the
   slow spectral filtration `vslow`), transporting the a.e. structural interfaces along the a.e.
   identification `vslow = vflag`.

3. `specList_eq_expEnum_of_lyapunovSpectrum_const` — the spectrum-constancy interface (`hspec`),
   reducing it to the a.e. constancy of the (`T`-invariant) per-point Lyapunov spectrum.

## Main results

* `ErgodicTheory.tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower`: the per-vector growth limit
  from the two one-sided bounds.
* `ErgodicTheory.vassembled_structure_ae`: the a.e. structural block of the assembled flag
  `vassembled`, stated without any measurability conclusion.
* `ErgodicTheory.oseledets_filtration_of_interfaces'`: the Oseledets filtration target with the
  measurability clause carried by an everywhere-measurable witness family.
* `ErgodicTheory.specList_eq_expEnum_of_lyapunovSpectrum_const`: the `hspec` interface from a.e.
  spectrum constancy.
-/

open MeasureTheory Filter Topology
open scoped Matrix Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-! ## The per-vector growth interface from the upper and lower bounds

The `hgrowth` interface of `oseledets_filtration_of_interfaces` asks, a.e., for a genuine limit
`(1/n) log‖A⁽ⁿ⁾ v‖ → specList A T x i` on each stratum `vflag castSucc \ vflag succ`.
The analytic core supplies the two one-sided bounds:

* the per-vector lower bound `specList A T x i ≤ liminf …` (from
  `log_le_liminf_log_cocycle_apply` at threshold `c = e^{specList i}`, packaged here as the
  hypothesis `hlb`); and
* the spectral upper bound `limsup … ≤ specList A T x i` (packaged here as the hypothesis
  `hub`).

The squeeze `tendsto_inv_mul_log_norm_cocycle_apply` turns the two bounds into the limit, modulo
the two `IsBoundedUnder` side-conditions; we take those as the minimal a.e. hypothesis `hbdd`. -/

/-- **`hgrowth` from upper + lower bounds.**  Given, a.e., the per-stratum-vector upper bound
(`limsup ≤ specList`), lower bound (`specList ≤ liminf`), and the two `IsBoundedUnder`
side-conditions, the per-vector growth interface of `oseledets_filtration_of_interfaces` holds.

The conclusion is stated with `Matrix.toEuclideanCLM` (the form consumed by the assembly); the
hypotheses use `Matrix.toEuclideanLin`, and the two coincide
(`Matrix.coe_toEuclideanCLM_eq_toEuclideanLin`). -/
theorem tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower
    {μ : Measure X} {T : X → X} (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hub : ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        limsup (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop ≤ specList A T x i)
    (hlb : ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        specList A T x i ≤ liminf (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop)
    (hbdd : ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        (IsBoundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖)) ∧
        (IsBoundedUnder (· ≥ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖))) :
    ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        Tendsto
          (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
          atTop (𝓝 (specList A T x i)) := by
  filter_upwards [hub, hlb, hbdd] with x hubx hlbx hbddx i v hv hvnot
  -- Rewrite the conclusion from `toEuclideanCLM` to `toEuclideanLin`.
  have hcoe : ∀ n : ℕ, (Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v)
      = Matrix.toEuclideanLin (cocycle A T n x) v := by
    intro n
    rw [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]; rfl
  simp_rw [hcoe]
  obtain ⟨hba, hbb⟩ := hbddx i v hv hvnot
  exact tendsto_inv_mul_log_norm_cocycle_apply T A x v (specList A T x i)
    (hubx i v hv hvnot) (hlbx i v hv hvnot) hba hbb

/-! ## The measurability-independent structural core of the assembly

`oseledets_filtration_of_interfaces` bundles the a.e. structural block with the existential
(`V := vassembled`) and the `hmeas` argument.  To re-point onto an everywhere-measurable witness
we need that a.e. block *separately*, without the `hmeas` argument.  `vassembled_structure_ae`
extracts exactly that block; its proof is the structural body of
`oseledets_filtration_of_interfaces`, dropping only the existential-introduction `refine`. -/

/-- The a.e. structural block of the assembled flag `vassembled`: almost everywhere the flag is
full at `0`, trivial at `Fin.last`, strictly decreasing, equivariant under `A x`, and carries the
exact per-vector growth rates `expEnum lam0 d`.  This is the conclusion of
`oseledets_filtration_of_interfaces` without the measurability clause and without the existential
packaging. -/
theorem vassembled_structure_ae
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hspec : ∀ᵐ x ∂μ, ∃ h : specCard A T x = numExp lam0 d,
      ∀ i : Fin (specCard A T x), specList A T x i = expEnum lam0 d (Fin.cast h i))
    (hgrowth : ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        Tendsto
          (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
          atTop (𝓝 (specList A T x i))) :
    ∀ᵐ x ∂μ,
      vassembled A T (numExp lam0 d) 0 x = ⊤ ∧
      vassembled A T (numExp lam0 d) (Fin.last (numExp lam0 d)) x = ⊥ ∧
      (∀ i : Fin (numExp lam0 d), vassembled A T (numExp lam0 d) i.succ x
        < vassembled A T (numExp lam0 d) i.castSucc x) ∧
      (∀ i : Fin (numExp lam0 d + 1),
        Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap
          (vassembled A T (numExp lam0 d) i x) = vassembled A T (numExp lam0 d) i (T x)) ∧
      (∀ i : Fin (numExp lam0 d), ∀ v ∈ (vassembled A T (numExp lam0 d) i.castSucc x :
          Set (EuclideanSpace ℝ (Fin d))),
          v ∉ vassembled A T (numExp lam0 d) i.succ x →
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
            atTop (𝓝 (expEnum lam0 d i))) := by
  classical
  set k := numExp lam0 d with hk
  have hspec' := hT.toMeasurePreserving.quasiMeasurePreserving.ae hspec
  have hUM := isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint'
  have hUM' := hT.toMeasurePreserving.quasiMeasurePreserving.ae hUM
  have hsubeq := vflag_equivariant hT hA hAmeas hint hint'
  have hspeceq := lyapunovSpectrum_equivariant_ae hT hA hAmeas hint hint'
  filter_upwards [hspec, hspec', hUM, hUM', hsubeq, hspeceq, hgrowth]
    with x hsx hsTx hx hTx hmapeq hseq hgx
  obtain ⟨hcardx, hlistx⟩ := hsx
  obtain ⟨hcardTx, hlistTx⟩ := hsTx
  have hcardeq : specCard A T x = specCard A T (T x) := by
    rw [specCard, specCard, hseq]
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [vassembled_of_eq hcardx]
    have : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) (0 : Fin (k + 1)))
        = (0 : Fin (specCard A T x + 1)) := by
      apply Fin.ext; simp
    rw [this]; exact vflag_zero hx
  · rw [vassembled_of_eq hcardx]
    have : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) (Fin.last k))
        = Fin.last (specCard A T x) := by
      apply Fin.ext; simp [hcardx]
    rw [this]; exact vflag_last A T x
  · intro i
    rw [vassembled_of_eq hcardx, vassembled_of_eq hcardx]
    set i' : Fin (specCard A T x) := Fin.cast hcardx.symm i with hi'
    have hsucc : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.succ)
        = i'.succ := by apply Fin.ext; simp [hi']
    have hcast : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.castSucc)
        = i'.castSucc := by apply Fin.ext; simp [hi']
    rw [hsucc, hcast]
    exact vflag_strictAnti hx i'
  · intro i
    rw [vassembled_of_eq hcardx, vassembled_of_eq hcardTx]
    by_cases hint_i : (i : ℕ) < specCard A T x
    · have hcx : ((Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i :
            Fin (specCard A T x + 1)) : ℕ) < specCard A T x := hint_i
      have hcTx : ((Fin.cast (by rw [hcardTx] : k + 1 = specCard A T (T x) + 1) i :
            Fin (specCard A T (T x) + 1)) : ℕ) < specCard A T (T x) := by
        simp only [Fin.val_cast]; omega
      rw [vflag_of_lt hcx, vflag_of_lt hcTx]
      have hjk : (i : ℕ) < numExp lam0 d := by rw [hcardx] at hint_i; exact hint_i
      set j : Fin (numExp lam0 d) := ⟨(i : ℕ), hjk⟩ with hj
      have hthrx : specList A T x ⟨_, hcx⟩ = expEnum lam0 d j := by
        rw [hlistx]
        exact congrArg (expEnum lam0 d) (Fin.ext (by simp [hj]))
      have hthrTx : specList A T (T x) ⟨_, hcTx⟩ = expEnum lam0 d j := by
        rw [hlistTx]
        exact congrArg (expEnum lam0 d) (Fin.ext (by simp [hj]))
      rw [hthrx, hthrTx]
      exact hmapeq (expEnum lam0 d j)
    · have hnx : ¬ ((Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i :
          Fin (specCard A T x + 1)) : ℕ) < specCard A T x := hint_i
      have hnTx : ¬ ((Fin.cast (by rw [hcardTx] : k + 1 = specCard A T (T x) + 1) i :
          Fin (specCard A T (T x) + 1)) : ℕ) < specCard A T (T x) := by
        simp only [Fin.val_cast]; omega
      rw [vflag, dif_neg hnx, vflag, dif_neg hnTx, Submodule.map_bot]
  · intro i v hv hvnot
    rw [vassembled_of_eq hcardx] at hv hvnot
    set i' : Fin (specCard A T x) := Fin.cast hcardx.symm i with hi'
    have hcast : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.castSucc)
        = i'.castSucc := by apply Fin.ext; simp [hi']
    have hsucc : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.succ)
        = i'.succ := by apply Fin.ext; simp [hi']
    rw [hcast] at hv
    rw [hsucc] at hvnot
    have hgrow := hgx i' v hv hvnot
    have hval : specList A T x i' = expEnum lam0 d i := by
      rw [hlistx i']
      have : Fin.cast hcardx i' = i := by apply Fin.ext; simp [hi']
      rw [this]
    rwa [hval] at hgrow

/-! ## Re-pointing the assembly onto an everywhere-measurable family

`vassembled` is built from the limsup flag `vflag`, whose measurability is only available a.e.
The `MeasurableSubspace` predicate is an *everywhere* statement, so `hmeas` cannot be discharged
for `vassembled` directly.  The fix is to carry the structural conclusion on a *different*,
everywhere-measurable family `vprime` (built from the slow spectral filtration `vslow`, whose
measurability is `measurableSubspace_vslow`), and transport the a.e. structural facts along the
a.e. identification `vprime = vassembled`.

`oseledets_filtration_of_interfaces'` takes:
* the same `hspec`/`hgrowth` interfaces as `oseledets_filtration_of_interfaces` (they feed
  `vassembled`);
* `hmeas'` — `MeasurableSubspace` for the slow-based family `vprime` (discharged via
  `measurableSubspace_vslow`); and
* `hae` — the a.e. identification `vprime i x = vassembled A T (numExp lam0 d) i x`.

It produces the `oseledets_filtration` target with witness `V := vprime`.  The structural a.e. block
is the `vassembled` block of `vassembled_structure_ae` rewritten, level by level, through `hae`.

The a.e. identification `hae` is itself the substantive mathematical content (`vslow = vflag`
a.e.); it is taken here as a cleanly-typed hypothesis and is discharged by
`vprime_eq_vassembled_of_slowflag`. -/

/-- The Oseledets filtration target from the structural interfaces, with the measurability clause
carried by an everywhere-measurable family `vprime` that agrees a.e. with the assembled flag
`vassembled`. -/
theorem oseledets_filtration_of_interfaces'
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hspec : ∀ᵐ x ∂μ, ∃ h : specCard A T x = numExp lam0 d,
      ∀ i : Fin (specCard A T x), specList A T x i = expEnum lam0 d (Fin.cast h i))
    (vprime : Fin (numExp lam0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (hmeas' : ∀ i, MeasurableSubspace (fun x => vprime i x))
    (hae : ∀ᵐ x ∂μ, ∀ i, vprime i x = vassembled A T (numExp lam0 d) i x)
    (hgrowth : ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        Tendsto
          (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
          atTop (𝓝 (specList A T x i))) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (V : Fin (k + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))),
      StrictAnti lam ∧
      (∀ i, MeasurableSubspace fun x => V i x) ∧
      ∀ᵐ x ∂μ,
        V 0 x = ⊤ ∧ V (Fin.last k) x = ⊥ ∧
        (∀ i : Fin k, V i.succ x < V i.castSucc x) ∧
        (∀ i : Fin (k + 1),
          Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x)
            = V i (T x)) ∧
        (∀ i : Fin k, ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))),
            v ∉ V i.succ x →
            Tendsto
              (fun n : ℕ => (n : ℝ)⁻¹ *
                Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
              atTop (𝓝 (lam i))) := by
  classical
  refine ⟨numExp lam0 d, expEnum lam0 d, vprime, expEnum_strictAnti lam0 d, hmeas', ?_⟩
  -- Structural a.e. block on `vassembled` (the measurability-independent core of the assembly),
  -- then transport level-by-level through `hae`.
  have hstruct := vassembled_structure_ae hT A hA hAmeas hint hint' lam0 hspec hgrowth
  -- The identification transported to the image point `T x` (needed for the equivariance level).
  have haeT := hT.toMeasurePreserving.quasiMeasurePreserving.ae hae
  filter_upwards [hstruct, hae, haeT] with x hsx haex haeTx
  obtain ⟨h0, hlast, hstrict, hmap, hgrow⟩ := hsx
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [haex 0]; exact h0
  · rw [haex (Fin.last (numExp lam0 d))]; exact hlast
  · intro i; rw [haex i.succ, haex i.castSucc]; exact hstrict i
  · intro i; rw [haex i, haeTx i]; exact hmap i
  · intro i v hv hvnot
    rw [haex i.castSucc] at hv
    rw [haex i.succ] at hvnot
    exact hgrow i v hv hvnot

/-! ## The spectrum-constancy interface

`hspec` asks that, a.e., the per-point limsup spectrum (`specCard`/`specList`, built from the finite
limsup spectrum `lyapunovSpectrum A T x` of `lambdaBar`) coincides with the deterministic
singular-value spectrum (`numExp`/`expEnum`, built from `distinctExp lam0 d`).

`lyapunovSpectrum_equivariant_ae` provides the `T`-invariance
`lyapunovSpectrum A T x = lyapunovSpectrum A T (T x)` a.e.;
ergodicity upgrades this to a.e. *constancy* of the finite set `lyapunovSpectrum A T x`, and the
spectral identification of `Λ` pins that constant set to `distinctExp lam0 d`.  Packaging both as
the single hypothesis `hspecconst : ∀ᵐ x, lyapunovSpectrum A T x = distinctExp lam0 d`, the `hspec`
shape is
then a pure `Finset`/`Fin`-reindexing computation: `specCard` and `numExp` are both the cardinality
of the (now-equal) finite set, and `specList` and `expEnum` are both its descending
`orderEmbOfFin`-enumeration, so they agree along the cardinality cast.

The constancy-to-`distinctExp` step (`hspecconst`) is the ergodic content; it is taken here as a
cleanly-typed hypothesis and is discharged by `lyapunovSpectrum_eq_distinctExp_of_lambdaBar`. -/

/-- **`hspec` from a.e. spectrum constancy.**  If the per-point limsup spectrum
`lyapunovSpectrum A T x` equals the deterministic distinct-exponent set `distinctExp lam0 d` a.e.,
then the `hspec` interface
of `oseledets_filtration_of_interfaces` holds: a.e. the spectrum cardinality equals `numExp lam0 d`
and the descending enumeration `specList` equals `expEnum lam0 d` along the cardinality cast. -/
theorem specList_eq_expEnum_of_lyapunovSpectrum_const
    {μ : Measure X} {T : X → X} (A : X → Matrix (Fin d) (Fin d) ℝ) (lam0 : ℕ → ℝ)
    (hspecconst : ∀ᵐ x ∂μ, lyapunovSpectrum A T x = distinctExp lam0 d) :
    ∀ᵐ x ∂μ, ∃ h : specCard A T x = numExp lam0 d,
      ∀ i : Fin (specCard A T x), specList A T x i = expEnum lam0 d (Fin.cast h i) := by
  filter_upwards [hspecconst] with x hx
  -- The cardinality cast.
  have hcard : specCard A T x = numExp lam0 d := by
    rw [specCard, numExp, hx]
  refine ⟨hcard, fun i => ?_⟩
  -- Both enumerations are the descending `orderEmbOfFin` of the *same* finite set; on equal
  -- finsets the embedding values agree iff the index values agree
  -- (`Finset.orderEmbOfFin_eq_orderEmbOfFin_iff`).
  have key : ∀ (s t : Finset ℝ), s = t → ∀ {p q : ℕ} (hs : s.card = p) (ht : t.card = q)
      (a : Fin p) (b : Fin q), (a : ℕ) = (b : ℕ) →
      s.orderEmbOfFin hs a = t.orderEmbOfFin ht b := by
    rintro s t rfl p q hs ht a b hab
    rw [Finset.orderEmbOfFin_eq_orderEmbOfFin_iff]; exact hab
  rw [specList, expEnum]
  exact key _ _ hx rfl rfl i.rev (Fin.cast hcard i).rev (by simp [Fin.val_rev, hcard])

end ErgodicTheory
