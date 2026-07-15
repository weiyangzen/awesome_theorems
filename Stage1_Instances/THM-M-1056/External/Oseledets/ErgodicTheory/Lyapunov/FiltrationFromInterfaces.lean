/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Cocycle.Basic
import ErgodicTheory.Lyapunov.MeasurableSubspace
import ErgodicTheory.Lyapunov.Forward
import ErgodicTheory.Lyapunov.ForwardV

/-!
# The Oseledets filtration from structural interfaces

This file assembles the full Oseledets filtration statement from the structural layers
already in place — the limsup flag `ErgodicTheory.vflag` and the deterministic exponent
enumeration `ErgodicTheory.expEnum` — together with explicit analytic hypotheses (ergodic
spectrum constancy, measurability of the flag levels, and exact per-vector growth).

## Main definitions

* `ErgodicTheory.vassembled`: the limsup flag `vflag`, reindexed to the deterministic index set
  `Fin (k + 1)` on the set where the per-point spectrum cardinality equals `k`.

## Main results

* `ErgodicTheory.oseledets_filtration_of_interfaces`: the Oseledets filtration conclusion,
  given the three analytic hypotheses.
-/

open MeasureTheory Filter Topology
open scoped Matrix Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} {d : ℕ}

/-- The assembled deterministic-index filtration: on the (a.e.) good set where the per-point
spectrum cardinality equals the deterministic `k`, it is the limsup flag `vflag` reindexed via
the cast `Fin (k+1) ≃ Fin (specCard x + 1)`; off the good set it is the junk value `⊤`. -/
noncomputable def vassembled (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (k : ℕ)
    (i : Fin (k + 1)) (x : X) : Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
  if h : specCard A T x = k then vflag A T x (Fin.cast (by rw [h]) i) else ⊤

/-- On the good set, where the per-point spectrum cardinality equals `k`, the assembled
filtration `vassembled` is the limsup flag `vflag` reindexed by the cast. -/
theorem vassembled_of_eq {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {k : ℕ}
    {x : X} (h : specCard A T x = k) (i : Fin (k + 1)) :
    vassembled A T k i x = vflag A T x (Fin.cast (by rw [h]) i) := by
  rw [vassembled, dif_pos h]

variable [MeasurableSpace X]

/-- **Assembly of the Oseledets filtration, modulo three analytic hypotheses.**

The deterministic exponents `lam = expEnum lam0 d` (strictly antitone) and `k = numExp lam0 d`
come from the ergodic singular-value Lyapunov spectrum `lam0` of
`exists_lam_tendsto_singularValue`.  The subspace family is the limsup flag `vflag` reindexed
to the deterministic index set (`vassembled`).

Three structural inputs are taken as explicit hypotheses; they are discharged downstream by
the spectrum-constancy, measurability, and exact-growth layers:

* `hspec` — **ergodic spectrum constancy**: for a.e. `x` the per-point limsup spectrum
  cardinality equals `k` and its descending enumeration equals the deterministic `lam`.
* `hmeas` — **measurability**: each reindexed flag level is a `MeasurableSubspace`
  (discharged via `measurableSubspace_vslow` after the a.e. flag/Λ-spectral
  identification).
* `hgrowth` — **per-vector exact growth**: for a.e. `x`, on each stratum
  `vflag castSucc \ vflag succ` the normalized log-growth converges to the stratum exponent
  `specList A T x i` (the limsup is already pinned by `lambdaBar_eq_on_stratum`; this is
  upgraded to a genuine limit via
  `tendsto_inv_mul_log_norm_cocycle_apply`). -/
theorem oseledets_filtration_of_interfaces
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
    (hmeas : ∀ i : Fin (numExp lam0 d + 1),
      MeasurableSubspace (fun x => vassembled A T (numExp lam0 d) i x))
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
  set k := numExp lam0 d with hk
  refine ⟨k, expEnum lam0 d, vassembled A T k,
    expEnum_strictAnti lam0 d, hmeas, ?_⟩
  -- Collect the a.e. structural facts.
  have hspec' := hT.toMeasurePreserving.quasiMeasurePreserving.ae hspec
  have hUM := isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint'
  have hUM' := hT.toMeasurePreserving.quasiMeasurePreserving.ae hUM
  have hsubeq := vflag_equivariant hT hA hAmeas hint hint'
  have hspeceq := lyapunovSpectrum_equivariant_ae hT hA hAmeas hint hint'
  filter_upwards [hspec, hspec', hUM, hUM', hsubeq, hspeceq, hgrowth]
    with x hsx hsTx hx hTx hmapeq hseq hgx
  obtain ⟨hcardx, hlistx⟩ := hsx
  obtain ⟨hcardTx, hlistTx⟩ := hsTx
  -- `specCard` agrees at `x` and `T x`.
  have hcardeq : specCard A T x = specCard A T (T x) := by
    rw [specCard, specCard, hseq]
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · -- `V 0 x = ⊤`.
    rw [vassembled_of_eq hcardx]
    have : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) (0 : Fin (k + 1)))
        = (0 : Fin (specCard A T x + 1)) := by
      apply Fin.ext; simp
    rw [this]; exact vflag_zero hx
  · -- `V (last k) x = ⊥`.
    rw [vassembled_of_eq hcardx]
    have : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) (Fin.last k))
        = Fin.last (specCard A T x) := by
      apply Fin.ext; simp [hcardx]
    rw [this]; exact vflag_last A T x
  · -- strict decrease.
    intro i
    rw [vassembled_of_eq hcardx, vassembled_of_eq hcardx]
    set i' : Fin (specCard A T x) := Fin.cast hcardx.symm i with hi'
    have hsucc : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.succ)
        = i'.succ := by apply Fin.ext; simp [hi']
    have hcast : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.castSucc)
        = i'.castSucc := by apply Fin.ext; simp [hi']
    rw [hsucc, hcast]
    exact vflag_strictAnti hx i'
  · -- equivariance.
    intro i
    rw [vassembled_of_eq hcardx, vassembled_of_eq hcardTx]
    by_cases hint_i : (i : ℕ) < specCard A T x
    · -- interior level: a sublevel set, transported by `vflag_equivariant`.
      have hcx : ((Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i :
            Fin (specCard A T x + 1)) : ℕ) < specCard A T x := hint_i
      have hcTx : ((Fin.cast (by rw [hcardTx] : k + 1 = specCard A T (T x) + 1) i :
            Fin (specCard A T (T x) + 1)) : ℕ) < specCard A T (T x) := by
        simp only [Fin.val_cast]; omega
      rw [vflag_of_lt hcx, vflag_of_lt hcTx]
      -- The exponent index `j : Fin (numExp lam0 d)` with value `i.val`.
      have hjk : (i : ℕ) < numExp lam0 d := hcardx ▸ hint_i
      set j : Fin (numExp lam0 d) := ⟨(i : ℕ), hjk⟩ with hj
      -- Both thresholds equal the deterministic value `expEnum lam0 d j`.
      have hthrx : specList A T x ⟨_, hcx⟩ = expEnum lam0 d j := by
        rw [hlistx]
        exact congrArg (expEnum lam0 d) (Fin.ext (by simp [hj]))
      have hthrTx : specList A T (T x) ⟨_, hcTx⟩ = expEnum lam0 d j := by
        rw [hlistTx]
        exact congrArg (expEnum lam0 d) (Fin.ext (by simp [hj]))
      rw [hthrx, hthrTx]
      -- Apply the sublevel equivariance at that deterministic threshold.
      exact hmapeq (expEnum lam0 d j)
    · -- top-of-range index: both levels are `⊥`.
      have hnx : ¬ ((Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i :
          Fin (specCard A T x + 1)) : ℕ) < specCard A T x := hint_i
      have hnTx : ¬ ((Fin.cast (by rw [hcardTx] : k + 1 = specCard A T (T x) + 1) i :
          Fin (specCard A T (T x) + 1)) : ℕ) < specCard A T (T x) := by
        simp only [Fin.val_cast]; omega
      rw [vflag, dif_neg hnx, vflag, dif_neg hnTx, Submodule.map_bot]
  · -- exact growth.
    intro i v hv hvnot
    rw [vassembled_of_eq hcardx] at hv hvnot
    set i' : Fin (specCard A T x) := Fin.cast hcardx.symm i with hi'
    have hcast : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.castSucc)
        = i'.castSucc := by apply Fin.ext; simp [hi']
    have hsucc : (Fin.cast (by rw [hcardx] : k + 1 = specCard A T x + 1) i.succ)
        = i'.succ := by apply Fin.ext; simp [hi']
    rw [hcast] at hv
    rw [hsucc] at hvnot
    have hgrow := hgx i' v hv hvnot
    -- `specList A T x i' = expEnum lam0 d (cast i') = expEnum lam0 d i`.
    have hval : specList A T x i' = expEnum lam0 d i := by
      rw [hlistx i']
      have : Fin.cast hcardx i' = i := by apply Fin.ext; simp [hi']
      rw [this]
    rwa [hval] at hgrow

end ErgodicTheory
