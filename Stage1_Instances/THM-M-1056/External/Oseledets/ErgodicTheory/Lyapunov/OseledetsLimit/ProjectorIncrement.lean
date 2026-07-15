/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.OseledetsLimit.BandProjector

/-!
# The band-projector increment bound and convergence

The single-step band-projector increment bound and its consequences: the abstract Pythagoras /
sin-Θ assembly, the Plücker det-Gram wiring of the cocycle data, and the geometric summability of
the increments that yields a.e. convergence of the band projectors at a spectral gap.

## Main definitions

* `ErgodicTheory.lamCocycle`, `ErgodicTheory.pluckerTopVec` — the per-step exponent cocycle and the
  Plücker
  (wedge) top vector carrying the gap data.
* `ErgodicTheory.bCocycle`, `ErgodicTheory.stepHypCocycle` — the increment-bound and step cocycles.

## Main results

* `ErgodicTheory.norm_bandProjector_succ_sub_le`,
  `ErgodicTheory.norm_bandProjector_succ_sub_le_cocycle` —
  the single-step band-projector increment bound, abstract and cocycle forms.
* `ErgodicTheory.exists_tendsto_bandProjector` — a.e. convergence of the band projectors.
* `ErgodicTheory.tendsto_bandProjector_of_gap` — convergence at a genuine spectral gap.
-/

open Module InnerProductSpace MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator Matrix MatrixOrder RealInnerProductSpace

noncomputable section

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}
variable [NeZero d]
variable {μ : Measure X} {T : X → X}

/-! ## The band-projector increment bound (assembly)

The single-step band-projector increment bound `norm_bandProjector_succ_sub_le` — the convergence
point of the refined off-diagonal sin-Θ route. It threads:

* the Frobenius back-transport `ExteriorNorm.norm_proj_sub_le_wedge`
  (`‖UUᵀ − VVᵀ‖² ≤ 2k(1 − det(UᵀV)²)`),
* the Plücker det-Gram identity `ExteriorNorm.inner_hodgeTrivialization_ιMulti`
  (`det(UᵀV) = ⟪wedge U, wedge V⟫`),
* the refined off-diagonal sin-Θ core `offdiag_sin_le_residual_div_gap`
  (`‖vt − ⟪vt,v₀⟫v₀‖ ≤ residual/(μ₀ − ν)`),
* the cocycle off-diagonal numerator `ExteriorNorm.norm_offdiag_residual_compound_le` and the
  `ν`-ceiling `ExteriorNorm.perturbed_compound_gram_ceiling`,
* the Plücker eigenpair `ExteriorNorm.plucker_eigenpair_ceiling_standard`.

The abstract Pythagoras-to-sin bound and the abstract assembly of steps 1–4
(`norm_proj_sub_le_residual_div_gap`), followed by the cocycle data. -/

open scoped RealInnerProductSpace in
/-- **Pythagoras gap, unit form.** For unit vectors `vt`, `v₀` in a real inner product space, the
squared sine of the angle equals one minus the squared cosine:
`‖vt − ⟪vt, v₀⟫ v₀‖² = 1 − ⟪vt, v₀⟫²`. -/
theorem norm_sub_proj_sq_eq_one_sub_inner_sq {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] {v₀ vt : E} (hv₀ : ‖v₀‖ = 1) (hvt : ‖vt‖ = 1) :
    ‖vt - (⟪vt, v₀⟫_ℝ) • v₀‖ ^ 2 = 1 - (⟪vt, v₀⟫_ℝ) ^ 2 := by
  set p : ℝ := ⟪vt, v₀⟫_ℝ with hp
  have hv₀v₀ : ⟪v₀, v₀⟫_ℝ = (1 : ℝ) := by rw [real_inner_self_eq_norm_sq, hv₀]; norm_num
  have hvtvt : ⟪vt, vt⟫_ℝ = (1 : ℝ) := by rw [real_inner_self_eq_norm_sq, hvt]; norm_num
  have hexp : ‖vt - p • v₀‖ ^ 2
      = ⟪vt, vt⟫_ℝ - 2 * p * ⟪vt, v₀⟫_ℝ + p ^ 2 * ⟪v₀, v₀⟫_ℝ := by
    rw [← real_inner_self_eq_norm_sq]
    simp only [inner_sub_left, inner_sub_right, real_inner_smul_left, real_inner_smul_right]
    rw [real_inner_comm v₀ vt]
    ring
  rw [hexp, hvtvt, hv₀v₀, ← hp]; ring

open scoped RealInnerProductSpace in
set_option linter.unusedSectionVars false in
/-- **Abstract assembly (steps 1–4).** Combines the Frobenius back-transport, the Plücker
det-Gram identity, the Pythagoras gap, and the refined off-diagonal sin-Θ core into a single
per-step projector-increment bound. Given orthonormal frames `U`, `V` (`UᵀU = VᵀV = 1`), an
abstract symmetric operator `C` (the perturbed compound Gram) with top unit eigenvector `vt`
(eigenvalue `μ₀`) and `ν`-ceiling on `v₀^⊥`, a reference unit eigenline `v₀`, and the
det-Gram/wedge identification `det(UᵀV) = ⟪vt, v₀⟫`, the band-projector increment obeys
`‖UUᵀ − VVᵀ‖ ≤ √(2k) · ‖C v₀ − ⟪C v₀, v₀⟫ v₀‖ / (μ₀ − ν)`. -/
theorem norm_proj_sub_le_residual_div_gap {k : ℕ} (U V : Matrix (Fin d) (Fin k) ℝ)
    (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1)
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {C : E →ₗ[ℝ] E} {μ₀ ν : ℝ} {v₀ vt : E} (hv₀ : ‖v₀‖ = 1) (hvtnorm : ‖vt‖ = 1)
    (hev : C vt = μ₀ • vt) (hgap : ν < μ₀)
    (hν : ∀ w : E, ⟪w, v₀⟫_ℝ = 0 → ⟪C w, w⟫_ℝ ≤ ν * ‖w‖ ^ 2)
    (hdet : (Uᵀ * V).det = ⟪vt, v₀⟫_ℝ) :
    ‖U * Uᵀ - V * Vᵀ‖ ≤ Real.sqrt (2 * k) * (‖C v₀ - (⟪C v₀, v₀⟫_ℝ) • v₀‖ / (μ₀ - ν)) := by
  -- step 4: the refined off-diagonal sin-Θ bound on the wedge angle
  have hsin := offdiag_sin_le_residual_div_gap hv₀ hvtnorm hev hgap hν
  set res : ℝ := ‖C v₀ - (⟪C v₀, v₀⟫_ℝ) • v₀‖ / (μ₀ - ν) with hresdef
  have hresnn : 0 ≤ res := by
    rw [hresdef]; apply div_nonneg (norm_nonneg _); linarith
  -- step 3: Pythagoras turns `1 − det²` into the squared sine `‖vt − ⟪vt,v₀⟫v₀‖²`
  have hpyth := norm_sub_proj_sq_eq_one_sub_inner_sq hv₀ hvtnorm
  -- step 1–2: the Frobenius back-transport bound
  have hwedge := ExteriorNorm.norm_proj_sub_le_wedge U V hU hV
  rw [hdet, ← hpyth] at hwedge
  -- combine: `‖UUᵀ − VVᵀ‖² ≤ 2k · sin² ≤ 2k · res²`
  have hsin' : ‖vt - (⟪vt, v₀⟫_ℝ) • v₀‖ ≤ res := hsin
  have hsinnn : 0 ≤ ‖vt - (⟪vt, v₀⟫_ℝ) • v₀‖ := norm_nonneg _
  have hsq : ‖vt - (⟪vt, v₀⟫_ℝ) • v₀‖ ^ 2 ≤ res ^ 2 := by
    apply sq_le_sq'
    · linarith
    · exact hsin'
  have hk2 : (0 : ℝ) ≤ 2 * (k : ℝ) := by positivity
  have hbound : ‖U * Uᵀ - V * Vᵀ‖ ^ 2 ≤ (Real.sqrt (2 * k) * res) ^ 2 := by
    calc ‖U * Uᵀ - V * Vᵀ‖ ^ 2
        ≤ 2 * (k : ℝ) * ‖vt - (⟪vt, v₀⟫_ℝ) • v₀‖ ^ 2 := hwedge
      _ ≤ 2 * (k : ℝ) * res ^ 2 := by
          apply mul_le_mul_of_nonneg_left hsq hk2
      _ = (Real.sqrt (2 * k) * res) ^ 2 := by
          rw [mul_pow, Real.sq_sqrt hk2]
  have hlhsnn : 0 ≤ ‖U * Uᵀ - V * Vᵀ‖ := norm_nonneg _
  have hrhsnn : 0 ≤ Real.sqrt (2 * k) * res := by positivity
  nlinarith [hbound, hlhsnn, hrhsnn, sq_nonneg (‖U * Uᵀ - V * Vᵀ‖ - Real.sqrt (2 * k) * res)]

/-- **Scalar simplification.** The off-diagonal numerator over the gap denominator
collapses
to the `κ²·r/(1 − κ²r²)` shape that drives the root test. With the compound-norm abbreviations
`cM = ‖compound k Mₙ‖`, `cB = ‖compound k B‖`, `cBi = ‖compound k B⁻¹‖`, `κ = cB·cBi`, `r =
σₖ/σₖ₋₁`,
the off-diagonal numerator is `cM·√μ₁·cB²` with `μ₁ = cM²·r²` (so `√μ₁ = cM·r`, using `cM ≥ 0`,
`r ≥ 0`), and a lower bound on the gap `μ̃₀ − ν ≥ cM²/cBi² · (1 − κ²r²)`. When `κ²r² < 1` the ratio
`numerator / (μ̃₀ − ν) ≤ κ²·r / (1 − κ²r²)`. This is the constant whose `(1/n)·log` limit is
`λₖ − λₖ₋₁ < 0`. -/
theorem numerator_div_gap_le {cM cB cBi r denom : ℝ}
    (hcM : 0 ≤ cM) (_hcB : 0 ≤ cB) (_hcBi : 0 ≤ cBi) (hr : 0 ≤ r)
    (hκr : (cB * cBi) ^ 2 * r ^ 2 < 1)
    (hdenom : cM ^ 2 / cBi ^ 2 * (1 - (cB * cBi) ^ 2 * r ^ 2) ≤ denom)
    (_hdenompos : 0 < denom) (hcBipos : 0 < cBi) :
    cM * (cM * r) * cB ^ 2 / denom
      ≤ (cB * cBi) ^ 2 * r / (1 - (cB * cBi) ^ 2 * r ^ 2) := by
  set κ2 : ℝ := (cB * cBi) ^ 2 with hκ2
  have hgapfac : 0 < 1 - κ2 * r ^ 2 := by rw [hκ2]; linarith
  -- the lower bound on `denom` is itself positive, and the numerator nonneg.
  have hnumnn : 0 ≤ cM * (cM * r) * cB ^ 2 := by positivity
  -- `numerator / denom ≤ numerator / lowerbound` since `lowerbound ≤ denom` and both positive.
  set lb : ℝ := cM ^ 2 / cBi ^ 2 * (1 - κ2 * r ^ 2) with hlb
  have hcM2 : (0 : ℝ) ≤ cM ^ 2 := by positivity
  rcases eq_or_lt_of_le hcM with hcM0 | hcMpos
  · -- `cM = 0`: numerator is 0, RHS nonneg.
    rw [← hcM0]; simp only [zero_mul, mul_zero, zero_div]
    positivity
  · have hlbpos : 0 < lb := by
      rw [hlb]; apply mul_pos; · positivity
      · exact hgapfac
    -- `numerator / denom ≤ numerator / lb`
    have hstep1 : cM * (cM * r) * cB ^ 2 / denom ≤ cM * (cM * r) * cB ^ 2 / lb := by
      apply div_le_div_of_nonneg_left hnumnn hlbpos
      rw [hlb, hκ2]; exact hdenom
    -- `numerator / lb = κ² r / (1 − κ²r²)`
    have hcMne : cM ≠ 0 := ne_of_gt hcMpos
    have hcBine : cBi ≠ 0 := ne_of_gt hcBipos
    have hgapne : (1 - κ2 * r ^ 2) ≠ 0 := ne_of_gt hgapfac
    have hlbne : lb ≠ 0 := ne_of_gt hlbpos
    have hstep2 : cM * (cM * r) * cB ^ 2 / lb = κ2 * r / (1 - κ2 * r ^ 2) := by
      rw [div_eq_div_iff hlbne hgapne, hlb, hκ2]
      field_simp
    rw [hstep2] at hstep1
    rw [hκ2]; exact hstep1

/-! ### The per-step band-projector increment bound (cocycle target)

The convergence point of the refined off-diagonal sin-Θ route. With `Mₙ = cocycle A T n x`,
`B = A(T^[n] x)`
the one-step left factor (so `cocycle A T (n+1) x = B * Mₙ`), `σ = (toEuclideanLin
Mₙ).singularValues`,
`r = σₖ/σₖ₋₁`, and `κ = ‖compound k B‖·‖compound k B⁻¹‖`, the band projectors at consecutive steps
satisfy `‖Pₙ₊₁ − Pₙ‖ ≤ √(2k)·κ²r/(1 − κ²r²)` in the EVENTUAL regime `κ²r² < 1`.

The proof composes the pieces:
* `bandProjector_indicator_eq_sortedTopFrame` (n, n+1) → `Pₙ = UUᵀ`, `Pₙ₊₁ = VVᵀ`, `UᵀU = VᵀV = 1`;
* `ExteriorNorm.norm_offdiag_residual_compound_le` → off-diagonal numerator
  `‖C v₀ − ⟪C v₀,v₀⟫v₀‖ ≤ cM·√μ₁·cB²`;
* `ExteriorNorm.perturbed_compound_gram_ceiling` → the `ν = μ₁·cB²` ceiling on `v₀^⊥`;
* `offdiag_sin_le_residual_div_gap` (via the abstract assembly `norm_proj_sub_le_residual_div_gap`)
  → `‖Pₙ₊₁ − Pₙ‖ ≤ √(2k)·(numerator/(μ̃₀ − ν))`;
* `numerator_div_gap_le` → the final `κ²r/(1 − κ²r²)` shape.

**Eventual-regime caveat.** The denominator positivity `μ̃₀ − ν > 0` holds only for `r < 1/κ`,
which is a tail property along the orbit (since `r → 0` geometrically while `κ` is tempered); hence
the bound is stated under the explicit regime hypothesis `hev`.

**Threaded gap hypotheses.** To keep the statement's elaboration
cheap (the `⋀^k`-finrank-indexed Euclidean types are extremely costly to `whnf` repeatedly), the
perturbed compound Gram operator is kept ABSTRACT here: `C : EuclideanSpace ℝ (Fin N) →ₗ[ℝ] _` with
`N` the wedge dimension, `v₀`/`vt` the reference / perturbed top eigenvectors, and `cM, cB, cBi` the
abstract compound operator norms `‖compound k Mₙ‖`, `‖compound k B‖`, `‖compound k B⁻¹‖`. The
cocycle instantiation — `N = finrank(⋀^k ℝᵈ)`, `C = adjoint Gₙ₊₁ ∘ₗ Gₙ₊₁`, the eigenpair/ceiling
data from `ExteriorNorm.plucker_eigenpair_ceiling_standard` (at `gram A T n x`, `gram A T (n+1) x`,
identified with the compound Gram via `ExteriorNorm.compoundMatrix_gram`), the off-diagonal
numerator
`ExteriorNorm.norm_offdiag_residual_compound_le`, the `ν = μ₁·cB²` ceiling
`ExteriorNorm.perturbed_compound_gram_ceiling`, and the det-Gram / wedge↔frame identification
`det(UᵀV) = ⟪vt, v₀⟫` (via `ExteriorNorm.inner_hodgeTrivialization_ιMulti`) — is pure bookkeeping
with no further analytic content; it is threaded as hypotheses here because the band-projector
frame ↔ Plücker eigenvector bridge and the rank-1 lower bound `μ̃₀ ≥ cM²/cBi²` are discharged
separately, and the `⋀^k`-type instantiation times out the elaborator at this granularity.

**Eventual-regime caveat.** The denominator positivity `μ̃₀ − ν > 0` holds only for `r < 1/κ`,
which is a tail property along the orbit (since `r → 0` geometrically while `κ` is tempered); hence
the bound is stated under the explicit regime hypotheses `hgap`/`hκr`. -/
set_option linter.unusedSectionVars false in
open scoped RealInnerProductSpace in
theorem norm_bandProjector_succ_sub_le {c : ℝ} (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    {k : ℕ} (n : ℕ) (x : X)
    (U V : Matrix (Fin d) (Fin k) ℝ) (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1)
    (hPn : bandProjector A T (Set.indicator (Set.Ioi c) 1) n x = U * Uᵀ)
    (hPn1 : bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x = V * Vᵀ)
    -- the abstract perturbed compound Gram operator `Cₙ₊₁` and its top eigenpair / reference line:
    {N : ℕ} {C : EuclideanSpace ℝ (Fin N) →ₗ[ℝ] EuclideanSpace ℝ (Fin N)}
    {v₀ vt : EuclideanSpace ℝ (Fin N)} (hv₀ : ‖v₀‖ = 1) (hvt : ‖vt‖ = 1)
    {μ₀ μ₁ : ℝ} (hev : C vt = μ₀ • vt)
    -- the off-diagonal numerator and `ν = μ₁·cB²` ceiling (cocycle lemmas):
    {cM cB cBi r : ℝ} (hcM : 0 ≤ cM) (hcB : 0 ≤ cB) (hr : 0 ≤ r)
    (hnum : ‖C v₀ - (⟪C v₀, v₀⟫_ℝ) • v₀‖ ≤ cM * (cM * r) * cB ^ 2)
    (hceil : ∀ z, (inner ℝ z v₀ : ℝ) = 0 → ⟪C z, z⟫_ℝ ≤ (μ₁ * cB ^ 2) * ‖z‖ ^ 2)
    -- the det-Gram / wedge identification (the Plücker bridge):
    (hdet : (Uᵀ * V).det = ⟪vt, v₀⟫_ℝ)
    -- the scalar linkages: the gap denominator lower bound, gap positivity, the regime:
    (hμ₀lb : cM ^ 2 / cBi ^ 2 * (1 - (cB * cBi) ^ 2 * r ^ 2) ≤ μ₀ - μ₁ * cB ^ 2)
    (hgap : μ₁ * cB ^ 2 < μ₀) (hκr : (cB * cBi) ^ 2 * r ^ 2 < 1)
    (hcBipos : 0 < cBi) :
    ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
        - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖
      ≤ Real.sqrt (2 * k)
        * ((cB * cBi) ^ 2 * r / (1 - (cB * cBi) ^ 2 * r ^ 2)) := by
  set ν : ℝ := μ₁ * cB ^ 2 with hν
  have hgap' : ν < μ₀ := by rw [hν]; exact hgap
  have hgappos : 0 < μ₀ - ν := by linarith
  -- abstract assembly (steps 1–4): `‖UUᵀ − VVᵀ‖ ≤ √(2k)·(numerator/(μ₀ − ν))`.
  have hassembly := norm_proj_sub_le_residual_div_gap U V hU hV hv₀ hvt
    (C := C) (μ₀ := μ₀) (ν := ν) hev hgap' hceil hdet
  -- bound the numerator/gap by the scalar `κ²r/(1−κ²r²)` shape.
  have hnumgap : ‖C v₀ - (⟪C v₀, v₀⟫_ℝ) • v₀‖ / (μ₀ - ν)
      ≤ (cB * cBi) ^ 2 * r / (1 - (cB * cBi) ^ 2 * r ^ 2) := by
    calc ‖C v₀ - (⟪C v₀, v₀⟫_ℝ) • v₀‖ / (μ₀ - ν)
        ≤ cM * (cM * r) * cB ^ 2 / (μ₀ - ν) :=
          div_le_div_of_nonneg_right hnum (le_of_lt hgappos)
      _ ≤ (cB * cBi) ^ 2 * r / (1 - (cB * cBi) ^ 2 * r ^ 2) := by
          have hμ₀lb' : cM ^ 2 / cBi ^ 2 * (1 - (cB * cBi) ^ 2 * r ^ 2) ≤ μ₀ - ν := by
            rw [hν]; exact hμ₀lb
          exact numerator_div_gap_le hcM hcB (le_of_lt hcBipos) hr hκr hμ₀lb' hgappos hcBipos
  -- assemble.
  rw [hPn, hPn1, ← norm_sub_rev]
  calc ‖U * Uᵀ - V * Vᵀ‖
      ≤ Real.sqrt (2 * k) * (‖C v₀ - (⟪C v₀, v₀⟫_ℝ) • v₀‖ / (μ₀ - ν)) := hassembly
    _ ≤ Real.sqrt (2 * k) * ((cB * cBi) ^ 2 * r / (1 - (cB * cBi) ^ 2 * r ^ 2)) := by
        apply mul_le_mul_of_nonneg_left hnumgap (Real.sqrt_nonneg _)

/-! ### The cocycle instantiation of the per-step band-projector bound

This instantiation discharges the abstract hypotheses of `norm_bandProjector_succ_sub_le` from the
cocycle exterior-power machinery, using the sorted Gram eigenframes
(`bandProjector_indicator_eq_sortedTopFrame`). With
`Mₙ = cocycle A T n x`, `B = A(T^[n] x)` (so `cocycle A T (n+1) x = B · Mₙ`), the perturbed compound
Gram operator `Cₙ₊₁ = adjoint Gₙ₊₁ ∘ₗ Gₙ₊₁` (`Gₙ₊₁ = toEuclideanLin (compoundMatrix k (B·Mₙ))`), the
Plücker top eigenvectors `v₀ = ⋀{u₀…u_{k-1}}(gram n)`, `vt = ⋀{u'₀…u'_{k-1}}(gram (n+1))`:

* `hev` from `ExteriorNorm.plucker_eigenpair_ceiling_standard'` at `gram (n+1)` (via
  `compound_gram_op_eq`);
* `hnum` from `ExteriorNorm.norm_offdiag_residual_compound_le` (with `√μ₁ = cM·r`);
* `hceil` from `ExteriorNorm.perturbed_compound_gram_ceiling`;
* `hdet` from `ExteriorNorm.det_transpose_mul_eq_inner_onbTriv` + `colE_sortedTopFrame`;
* `hPn`, `hPn1` from `bandProjector_indicator_eq_sortedTopFrame`;
* the scalar regime hypotheses (`hμ₀lb`, `hgapμ`, `hκr`, `hcBipos`) threaded as inputs (the EVENTUAL
  `κ²r² < 1` regime — discharged a.e. by the unconditional root-test convergence layer below). -/

set_option maxHeartbeats 1600000 in -- heavy elaboration; exceeds the default budget
-- raised: the `⋀^k`-indexed compound/Plücker Euclidean elaboration is heartbeat-heavy.
set_option linter.unusedSectionVars false in
/-- **The compound Gram operator of the cocycle is `toEuclideanLin (compoundMatrix k (gram))`.**
`adjoint Gₙ ∘ₗ Gₙ = toEuclideanLin (compoundMatrix k (gram A T n x))`, where
`Gₙ = toEuclideanLin (compoundMatrix k (cocycle A T n x))`. Via `compoundMatrix_gram` and the matrix
adjoint identity `toEuclideanLin (Nᴴ) = (toEuclideanLin N).adjoint` (no `NeZero` on the wedge
dimension needed). -/
theorem compound_gram_op_eq (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) (k : ℕ) :
    (LinearMap.adjoint (Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x))) ∘ₗ
      Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x)))
      = Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (gram A T n x)) := by
  rw [gram, ExteriorNorm.compoundMatrix_gram]
  have hadj := Matrix.toEuclideanLin_conjTranspose_eq_adjoint
    (ExteriorNorm.compoundMatrix k (cocycle A T n x))
  rw [Matrix.conjTranspose_eq_transpose_of_trivial] at hadj
  calc
    LinearMap.adjoint
          (Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x))) ∘ₗ
        Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x)) =
        Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x))ᵀ ∘ₗ
          Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x)) := by
            congr 1
            exact hadj.symm
    _ = Matrix.toEuclideanLin
          ((ExteriorNorm.compoundMatrix k (cocycle A T n x))ᵀ *
            ExteriorNorm.compoundMatrix k (cocycle A T n x)) := by
            ext v i
            simp only [LinearMap.comp_apply, Matrix.toLpLin_apply, Matrix.mulVec_mulVec]

set_option maxHeartbeats 1600000 in -- heavy elaboration; exceeds the default budget
-- raised: the `⋀^k`-indexed compound/Plücker Euclidean elaboration is heartbeat-heavy.
/-- **The Plücker top eigenvector achieves the compound operator norm.** If `v₀` is a unit Plücker
top eigenvector of `Cₙ = adjoint Gₙ ∘ₗ Gₙ` (eigenvalue `∏_{i<k} σᵢ²`), then `‖Gₙ v₀‖ = ‖compound
Mₙ‖`
(`= ∏_{i<k} σᵢ = √μ₀`). This `htop` hypothesis of `ExteriorNorm.norm_offdiag_residual_compound_le`.
-/
theorem norm_compound_apply_pluckerVec (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ)
    (x : X)
    {k : ℕ}
    (v₀ : EuclideanSpace ℝ (Fin (Module.finrank ℝ (⋀[ℝ]^k (EuclideanSpace ℝ (Fin d))))))
    (hv₀ : ‖v₀‖ = 1)
    (hev : Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (gram A T n x)) v₀
      = (∏ i ∈ Finset.range k,
          (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i ^ 2) • v₀) :
    ‖Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x)) v₀‖
      = ‖ExteriorNorm.compoundMatrix k (cocycle A T n x)‖ := by
  set G := Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (cocycle A T n x)) with hG
  set prodσ := ∏ i ∈ Finset.range k, (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i
    with hprod
  have hprodnn : 0 ≤ prodσ := by
    rw [hprod]; exact Finset.prod_nonneg (fun i _ =>
      (Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg i)
  have hnormsq : ‖G v₀‖ ^ 2 = (inner ℝ (G v₀) (G v₀) : ℝ) := (real_inner_self_eq_norm_sq _).symm
  have hadj : (inner ℝ (G v₀) (G v₀) : ℝ)
      = (inner ℝ (Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (gram A T n x)) v₀)
          v₀ : ℝ) := by
    rw [← compound_gram_op_eq A T n x k, LinearMap.comp_apply, LinearMap.adjoint_inner_left]
  rw [hev, inner_smul_left] at hadj
  rw [show (inner ℝ v₀ v₀ : ℝ) = 1 from by rw [real_inner_self_eq_norm_sq, hv₀]; norm_num] at hadj
  simp only [conj_trivial, mul_one] at hadj
  have hsq : ‖G v₀‖ ^ 2 = prodσ ^ 2 := by
    rw [hnormsq, hadj, hprod, ← Finset.prod_pow]
  rw [← ExteriorNorm.prod_singularValues_eq_l2_opNorm_compound, ← hprod]
  have hGnn := norm_nonneg (G v₀)
  nlinarith [hsq, hGnn, hprodnn]

/-- The sorted-Gram-eigenvalue family `lam i = σᵢ²` of the cocycle iterate (= `eigenvalues₀ (gram)`,
antitone, nonneg). The `lam` consumed by `ExteriorNorm.plucker_eigenpair_ceiling_standard'`. -/
noncomputable def lamCocycle (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    ℕ → ℝ :=
  fun i => (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i ^ 2

set_option linter.unusedSectionVars false in
theorem lamCocycle_antitone (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    Antitone (lamCocycle A T n x) := by
  intro i j hij
  exact pow_le_pow_left₀ ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg j)
    ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues_antitone hij) 2

set_option linter.unusedSectionVars false in
theorem lamCocycle_nonneg (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) (i : ℕ) :
    0 ≤ lamCocycle A T n x i := by rw [lamCocycle]; positivity

theorem lamCocycle_eigenpair (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X)
    (i : Fin (Fintype.card (Fin d))) :
    Matrix.toEuclideanLin (gram A T n x) (sortedGramEigenbasis A T n x i)
      = lamCocycle A T n x (i:ℕ) • sortedGramEigenbasis A T n x i := by
  rw [sortedGramEigenbasis_eigenpair, lamCocycle, gram_eigenvalues₀_eq_sq_singularValues]

/-- The Plücker top eigenvector of `Cₙ`: the Hodge-trivialized wedge `onbTriv basisFun (⋀
{u₀…u_{k-1}})`
of the sorted top-`k` Gram eigenvectors. This is the `v₀` shared by
`ExteriorNorm.plucker_eigenpair_ceiling_standard'` and
`ExteriorNorm.det_transpose_mul_eq_inner_onbTriv`
(via `colE_sortedTopFrame`). -/
noncomputable def pluckerTopVec (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X)
    {k : ℕ} (hkd : k ≤ Fintype.card (Fin d)) :
    EuclideanSpace ℝ (Fin (Module.finrank ℝ (⋀[ℝ]^k (EuclideanSpace ℝ (Fin d))))) :=
  ExteriorNorm.onbTriv (EuclideanSpace.basisFun (Fin d) ℝ) k
    (exteriorPower.ιMulti ℝ k
      (fun j : Fin k => sortedGramEigenbasis A T n x ⟨j, lt_of_lt_of_le j.2 hkd⟩))

set_option maxHeartbeats 3200000 in -- load-bearing (measured): default 200000 overflows at whnf
-- raised: the `⋀^k`-indexed compound/Plücker Euclidean elaboration is heartbeat-heavy.
/-- **The Plücker eigenpair/ceiling data for the cocycle compound Gram operator.** Specialization of
`ExteriorNorm.plucker_eigenpair_ceiling_standard'` to `gram A T n x` with the sorted eigenbasis and
`lam = σ²`: the top eigenvector `pluckerTopVec` is a unit vector, an eigenvector of
`toEuclideanLin (compoundMatrix k (gram))` with eigenvalue `∏_{i<k} σᵢ²`, the gap
`∏_{i<k-1}σᵢ²·σₖ² < ∏_{i<k}σᵢ²` holds, and the second-eigenvalue ceiling on its orthocomplement. -/
theorem plucker_cocycle_data (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X)
    {k : ℕ} (hk1 : 1 ≤ k) (hkd : k ≤ Fintype.card (Fin d))
    (hgap : lamCocycle A T n x k < lamCocycle A T n x (k - 1)) :
    ‖pluckerTopVec A T n x hkd‖ = 1
    ∧ Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (gram A T n x))
          (pluckerTopVec A T n x hkd)
        = (∏ i ∈ Finset.range k, lamCocycle A T n x i) • pluckerTopVec A T n x hkd
    ∧ ((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k)
        < (∏ i ∈ Finset.range k, lamCocycle A T n x i)
    ∧ ∀ w, (inner ℝ w (pluckerTopVec A T n x hkd) : ℝ) = 0 →
        (inner ℝ (Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (gram A T n x)) w) w : ℝ)
          ≤ ((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k) * ‖w‖ ^ 2 :=
  ExteriorNorm.plucker_eigenpair_ceiling_standard' (gram A T n x) (sortedGramEigenbasis A T n x)
    (lamCocycle A T n x) (lamCocycle_antitone A T n x) (lamCocycle_nonneg A T n x)
    (lamCocycle_eigenpair A T n x) hk1 hkd hgap

set_option maxHeartbeats 3200000 in -- load-bearing (measured): default 200000 overflows at whnf
-- raised: the `⋀^k`-indexed compound/Plücker Euclidean elaboration is heartbeat-heavy.
/-- **The cocycle per-step band-projector increment bound.** Instantiating the
abstract `norm_bandProjector_succ_sub_le` with the SORTED Gram eigenframes
(`bandProjector_indicator_eq_sortedTopFrame`), the
Plücker eigenpairs of `gram n`/`gram (n+1)`, and the off-diagonal numerator / `ν`-ceiling
/
lower-bound exterior lemmas. With `B = A(T^[n] x)`, `cM = ‖compound k Mₙ‖`, `cB = ‖compound k B‖`,
`cBi = ‖compound k B⁻¹‖`, `r = σₖ/σₖ₋₁`, in the EVENTUAL regime `(cB·cBi)²r² < 1`, the band
projectors
satisfy `‖Pₙ₊₁ − Pₙ‖ ≤ √(2k)·(cB·cBi)²·r/(1 − (cB·cBi)²r²)`. The cut hypotheses (`htop*`, `hcount*`)
identify both band projectors with the sorted top-`k` frames; the gap hypotheses (`hgap*`) feed the
Plücker spectral gap; the scalar linkage hypotheses (`hμ₀lb`, `hgapμ`, `hκr`) are the genuine
outputs
of `ExteriorNorm.norm_sq_compound_mul_ge` + the eventual regime, discharged a.e. by the
unconditional root-test convergence layer below.
-/
theorem norm_bandProjector_succ_sub_le_cocycle
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (hA : ∀ x, (A x).det ≠ 0)
    (n : ℕ) (x : X) (c : ℝ) {k : ℕ} (hk1 : 1 ≤ k) (hkd : k ≤ Fintype.card (Fin d))
    (htopN : ∀ j : Fin k, c < (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀
      ⟨j, lt_of_lt_of_le j.2 hkd⟩)
    (hcountN : Fintype.card
      {i : Fin d // c < (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues i} = k)
    (htopN1 : ∀ j : Fin k, c < (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀
      ⟨j, lt_of_lt_of_le j.2 hkd⟩)
    (hcountN1 : Fintype.card
      {i : Fin d // c < (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues i} = k)
    (hgapN : lamCocycle A T n x k < lamCocycle A T n x (k-1))
    (hgapN1 : lamCocycle A T (n+1) x k < lamCocycle A T (n+1) x (k-1))
    (hcBipos : 0 < ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖)
    (hμ₀lb : ‖ExteriorNorm.compoundMatrix k (cocycle A T n x)‖ ^ 2
          / ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖ ^ 2
        * (1 - (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
            * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
          * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
            / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2)
        ≤ (∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i)
          - ((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k)
            * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ ^ 2)
    (hgapμ : ((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k)
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ ^ 2
        < ∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i)
    (hκr : (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
        * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2 < 1) :
    ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
        - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖
      ≤ Real.sqrt (2 * k)
        * ((‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
            * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
          * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
            / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1))
          / (1 - (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
              * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
            * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
              / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2)) := by
  classical
  set B := A (T^[n] x) with hB
  set M := cocycle A T n x with hM
  have hBM : B * M = cocycle A T (n+1) x := by
    rw [hB, hM, show n+1 = 1 + n from by omega, cocycle_add, cocycle_one]
  set U := sortedTopFrame A T n x hkd with hU
  set V := sortedTopFrame A T (n+1) x hkd with hV
  obtain ⟨hUframe, hUortho⟩ := bandProjector_indicator_eq_sortedTopFrame A T n x c hkd htopN hcountN
  obtain ⟨hVframe, hVortho⟩ :=
    bandProjector_indicator_eq_sortedTopFrame A T (n+1) x c hkd htopN1 hcountN1
  obtain ⟨hv₀norm, hv₀ev, hv₀gap, hv₀ceil⟩ := plucker_cocycle_data A T n x hk1 hkd hgapN
  obtain ⟨hvtnorm, hvtev, hvtgap, hvtceil⟩ := plucker_cocycle_data A T (n+1) x hk1 hkd hgapN1
  set v₀ := pluckerTopVec A T n x hkd with hv₀def
  set vt := pluckerTopVec A T (n+1) x hkd with hvtdef
  set μ₀ := ∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i with hμ₀
  set μ₁ := (∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k with hμ₁
  set cM := ‖ExteriorNorm.compoundMatrix k M‖ with hcM
  set cB := ‖ExteriorNorm.compoundMatrix k B‖ with hcB
  set cBi := ‖ExteriorNorm.compoundMatrix k B⁻¹‖ with hcBi
  set r := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
    / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) with hr
  set C := LinearMap.adjoint (Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (B * M))) ∘ₗ
    Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k (B * M)) with hC
  have hev : C vt = μ₀ • vt := by
    rw [hC, hBM, compound_gram_op_eq A T (n+1) x k, hvtev]
  have htop : ‖Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k M) v₀‖
      = ‖ExteriorNorm.compoundMatrix k M‖ :=
    norm_compound_apply_pluckerVec A T n x v₀ hv₀norm hv₀ev
  have hceilN : ∀ z, (inner ℝ z v₀ : ℝ) = 0 →
      (inner ℝ ((LinearMap.adjoint (Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k M)) ∘ₗ
        Matrix.toEuclideanLin (ExteriorNorm.compoundMatrix k M)) z) z : ℝ) ≤ μ₁ * ‖z‖ ^ 2 := by
    intro z hz
    rw [compound_gram_op_eq A T n x k]
    exact hv₀ceil z hz
  have hnum : ‖C v₀ - (inner ℝ (C v₀) v₀ : ℝ) • v₀‖ ≤ cM * (cM * r) * cB ^ 2 := by
    have hμ₁nn : 0 ≤ μ₁ := by
      rw [hμ₁]
      exact mul_nonneg (Finset.prod_nonneg (fun i _ => lamCocycle_nonneg A T n x i))
        (lamCocycle_nonneg A T n x k)
    have hres := ExteriorNorm.norm_offdiag_residual_compound_le (d := d) k B M (μ₁ := μ₁)
      hμ₁nn hv₀norm htop hceilN
    rw [← hC] at hres
    refine le_trans hres ?_
    rw [hcM, hcB]
    have hsqrt : Real.sqrt μ₁ = cM * r := by
      have hcMr : 0 ≤ cM * r := by
        rw [hcM, hr]; apply mul_nonneg (norm_nonneg _)
        apply div_nonneg ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg k)
          ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg (k-1))
      rw [← Real.sqrt_sq hcMr]
      congr 1
      rw [hμ₁, hcM, hr, ← ExteriorNorm.prod_singularValues_eq_l2_opNorm_compound]
      simp only [lamCocycle]
      have hsplit : (∏ i ∈ Finset.range k,
            (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)
          = (∏ i ∈ Finset.range (k-1),
            (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)
            * (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) := by
        conv_lhs => rw [show k = (k - 1) + 1 from by omega, Finset.prod_range_succ]
      rw [hsplit, Finset.prod_pow]
      have hσpos : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) :=
        singularValues_cocycle_pos hA n x (by
          have hkk : k - 1 < k := by omega
          exact lt_of_lt_of_le (lt_of_lt_of_le hkk hkd) (le_of_eq (Fintype.card_fin d)))
      have hσne : (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) ≠ 0 :=
        ne_of_gt hσpos
      field_simp
    rw [hsqrt]
  have hceil : ∀ z, (inner ℝ z v₀ : ℝ) = 0 →
      (inner ℝ (C z) z : ℝ) ≤ (μ₁ * cB ^ 2) * ‖z‖ ^ 2 := by
    intro z hz
    rw [hcB, hC]
    exact ExteriorNorm.perturbed_compound_gram_ceiling (d := d) k B M hceilN z hz
  have hcolU : (fun i => ExteriorNorm.colE U i)
      = (fun j : Fin k => sortedGramEigenbasis A T n x ⟨j, lt_of_lt_of_le j.2 hkd⟩) := by
    funext i; rw [hU, colE_sortedTopFrame]
  have hcolV : (fun j => ExteriorNorm.colE V j)
      = (fun j : Fin k => sortedGramEigenbasis A T (n+1) x ⟨j, lt_of_lt_of_le j.2 hkd⟩) := by
    funext j; rw [hV, colE_sortedTopFrame]
  have hdet : (Uᵀ * V).det = (inner ℝ vt v₀ : ℝ) := by
    rw [ExteriorNorm.det_transpose_mul_eq_inner_onbTriv U V, hcolU, hcolV, hvtdef, hv₀def,
      pluckerTopVec, pluckerTopVec]
  have hrnn : 0 ≤ r := by
    rw [hr]; exact div_nonneg
      ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg k)
      ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg (k-1))
  exact norm_bandProjector_succ_sub_le (c := c) A T n x U V hUortho hVortho
    hUframe hVframe (N := Module.finrank ℝ (⋀[ℝ]^k (EuclideanSpace ℝ (Fin d))))
    (C := C) (v₀ := v₀) (vt := vt) hv₀norm hvtnorm
    (μ₀ := μ₀) (μ₁ := μ₁) hev
    (cM := cM) (cB := cB) (cBi := cBi) (r := r)
    (norm_nonneg _) (norm_nonneg _) hrnn
    hnum hceil hdet hμ₀lb hgapμ hκr hcBipos

/-! ## A.e. summability of the band-projector increments (the root-test conclusion)

The per-step band-projector bound `‖Pₙ₊₁ − Pₙ‖ ≤ bₙ` with `bₙ = √(2k)·κ(⋀ᵏB)²·rₙ/(1 − κ²rₙ²)`
(`norm_bandProjector_succ_sub_le`) is summable along the orbit by the root test: `(1/n)log bₙ →
λₖ − λₖ₋₁ < 0`. The scalar layer supplies the log-limit (`(1/n)log rₙ → λₖ − λₖ₋₁` via
`tendsto_log_singularValue` at indices `k`, `k−1`; the `κ²` factor subexponential via
`tendsto_logNorm_compound_orbit_div_atTop_zero`; the `1/(1−κ²rₙ²)` factor `→ 1` since `κ²rₙ² → 0`).
We package the comparison + root test abstractly, then state the cocycle conclusion taking the
per-step bound and the negative log-limit of its RHS as hypotheses (the genuine outputs of the
per-step bound `norm_bandProjector_succ_sub_le` and the scalar layer). -/

/-- **Packaging: comparison + root test.** If the increment norms `‖incr n‖` are eventually
dominated by a nonnegative sequence `b` whose normalized log tends to a negative limit, then the
increment norms are summable. Pure soft analysis (`summable_of_logLimit_neg` +
`Summable.of_norm_bounded_eventually_nat`). -/
theorem summable_norm_of_logLimit_neg_of_le {E : Type*} [NormedAddCommGroup E]
    (incr : ℕ → E) (b : ℕ → ℝ)
    (hb : ∀ n, 0 ≤ b n) (hpos : ∀ᶠ n in atTop, 0 < b n)
    {L : ℝ} (hL : L < 0)
    (hlog : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (b n)) atTop (𝓝 L))
    (hstep : ∀ᶠ n in atTop, ‖incr n‖ ≤ b n) :
    Summable (fun n => ‖incr n‖) := by
  have hsumb : Summable b := summable_of_logLimit_neg b hb hpos hL hlog
  apply Summable.of_norm_bounded_eventually_nat hsumb
  filter_upwards [hstep] with n hn
  rw [Real.norm_eq_abs, abs_of_nonneg (norm_nonneg _)]
  exact hn

set_option linter.unusedSectionVars false in
/-- **A.e. summability of the band-projector increments.** For `μ`-a.e. `x`, the
consecutive band-projector increments `‖Pₙ₊₁ − Pₙ‖` are summable. The per-step dominating sequence
`b x n` (the RHS of `norm_bandProjector_succ_sub_le`, eventually `√(2k)·κ²rₙ/(1−κ²rₙ²)`), its
nonnegativity / eventual positivity, the negative root-test log-limit `L x` (`= λₖ − λₖ₋₁`), and the
eventual per-step bound are taken as hypotheses — the genuine outputs of the per-step bound and the
scalar layer (`tendsto_log_singularValue`,
`tendsto_logNorm_compound_orbit_div_atTop_zero`).
The conclusion is the summability that feeds the Cauchy packaging
`cauchySeq_cfc_of_summable`. -/
theorem summable_norm_bandProjector_succ_sub {c : ℝ} (A : X → Matrix (Fin d) (Fin d) ℝ)
    (b : X → ℕ → ℝ)
    (hb : ∀ᵐ x ∂μ, ∀ n, 0 ≤ b x n)
    (hpos : ∀ᵐ x ∂μ, ∀ᶠ n in atTop, 0 < b x n)
    (L : X → ℝ) (hL : ∀ᵐ x ∂μ, L x < 0)
    (hlog : ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (b x n)) atTop (𝓝 (L x)))
    (hstep : ∀ᵐ x ∂μ, ∀ᶠ n in atTop,
      ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
          - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖ ≤ b x n) :
    ∀ᵐ x ∂μ, Summable (fun n =>
      ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
          - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖) := by
  filter_upwards [hb, hpos, hL, hlog, hstep] with x hbx hposx hLx hlogx hstepx
  exact summable_norm_of_logLimit_neg_of_le _ (b x) hbx hposx hLx hlogx hstepx

/-! ## A.e. assembly: the band projectors converge

The Cauchy packaging `exists_tendsto_cfc_of_summable` turns the a.e. summability of the
band-projector increments (`summable_norm_bandProjector_succ_sub`) into a.e. convergence of
the band projectors themselves: the candidate Oseledets spectral projector exists `μ`-a.e. The
`bandProjector A T (indicator (Ioi c) 1) n x = cfc (indicator (Ioi c) 1) (qpow A T n x)` sequence is
the `cfc χ (H n)` sequence with `H = fun n => qpow A T n x`, so this is a direct specialization. -/

/-- **A.e. assembly.** For `μ`-a.e. `x`, the band projectors
`bandProjector A T (indicator (Ioi c) 1) n x` converge: there is a limiting projector `P` with
`Tendsto (fun n => bandProjector A T (indicator (Ioi c) 1) n x) atTop (𝓝 P)`. This is the
convergence of the Oseledets spectral projector pinned by the growing spectral gap, obtained by
feeding the a.e. summability of the increments (`summable_norm_bandProjector_succ_sub`) into
the soft-analysis Cauchy packaging `exists_tendsto_cfc_of_summable`. The summability
hypotheses are the genuine outputs of the per-step bound `norm_bandProjector_succ_sub_le` and the
scalar root-test layer (`tendsto_log_singularValue`,
`tendsto_logNorm_compound_orbit_div_atTop_zero`). -/
theorem exists_tendsto_bandProjector {c : ℝ} (A : X → Matrix (Fin d) (Fin d) ℝ)
    (b : X → ℕ → ℝ)
    (hb : ∀ᵐ x ∂μ, ∀ n, 0 ≤ b x n)
    (hpos : ∀ᵐ x ∂μ, ∀ᶠ n in atTop, 0 < b x n)
    (L : X → ℝ) (hL : ∀ᵐ x ∂μ, L x < 0)
    (hlog : ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (b x n)) atTop (𝓝 (L x)))
    (hstep : ∀ᵐ x ∂μ, ∀ᶠ n in atTop,
      ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
          - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖ ≤ b x n) :
    ∀ᵐ x ∂μ, ∃ P : Matrix (Fin d) (Fin d) ℝ,
      Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) atTop (𝓝 P) := by
  have hsummable := summable_norm_bandProjector_succ_sub (c := c) A b hb hpos L hL hlog hstep
  filter_upwards [hsummable] with x hx
  -- `bandProjector A T χ n x = cfc χ (qpow A T n x)` is `cfc χ (H n)` with `H = qpow A T · x`.
  exact exists_tendsto_cfc_of_summable (fun n => qpow A T n x)
    (Set.indicator (Set.Ioi c) 1) hx

/-! ### Unconditional band-projector a.e. convergence (cocycle)

Feeding the per-step bound `norm_bandProjector_succ_sub_le_cocycle` through the Cauchy
packaging `exists_tendsto_bandProjector`: for `μ`-a.e. `x`, the band projector
`bandProjector A T (indicator (Ioi c) 1) n x` converges. The per-step bound
`bCocycle x n = √(2k)·κ²r/(1 − κ²r²)` is summable along the orbit by the root test (its `(1/n)·log`
tends to `λₖ − λₖ₋₁ < 0` a.e. via the scalar layer `tendsto_log_singularValue` at the two
cut indices and `tendsto_logNorm_compound_orbit_div_atTop_zero`; the eventual regime `κ²r² < 1`
holds
a.e. since `r → 0` geometrically while `κ` is tempered). The a.e. eventual cut/gap/regime conditions
are packaged as `stepHypCocycle` and discharged through the per-step bound by
`stepHypCocycle_imp_step`.
-/

/-- **The per-step dominating sequence.** The RHS of the cocycle band-projector
increment bound (`norm_bandProjector_succ_sub_le_cocycle`): `√(2k)·κ²·r/(1 − κ²r²)` with
`κ = ‖compound k B‖·‖compound k B⁻¹‖`, `r = σₖ/σₖ₋₁`, `B = A(T^[n] x)`. Its `(1/n)·log` tends to
`λₖ − λₖ₋₁ < 0` a.e., making it summable by the root test. -/
noncomputable def bCocycle (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) (k : ℕ) :
    ℕ → ℝ :=
  fun n => Real.sqrt (2 * k)
    * ((‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
        * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
      * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
        / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1))
      / (1 - (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
        * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2))

/-- **The per-step cut/gap/regime conditions at a single `n`.** The conjunction of
all
hypotheses of `norm_bandProjector_succ_sub_le_cocycle` at step `n`: the cut counts `= k` (at `n` and
`n+1`), the top-`k` sorted `qpow` eigenvalues exceed `c`, the Plücker spectral gaps, and the scalar
regime/linkage conditions. Eventually true a.e. along the orbit (the cut is stable in the eventual
Lyapunov-gap regime; `r → 0` geometrically); see the section note above. -/
def stepHypCocycle (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (c : ℝ) (k : ℕ)
    (hkd : k ≤ Fintype.card (Fin d)) (x : X) (n : ℕ) : Prop :=
  (∀ j : Fin k, c < (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀
      ⟨j, lt_of_lt_of_le j.2 hkd⟩)
  ∧ Fintype.card {i : Fin d // c < (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues i} = k
  ∧ (∀ j : Fin k, c < (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀
      ⟨j, lt_of_lt_of_le j.2 hkd⟩)
  ∧ Fintype.card {i : Fin d // c < (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues i} = k
  ∧ lamCocycle A T n x k < lamCocycle A T n x (k-1)
  ∧ lamCocycle A T (n+1) x k < lamCocycle A T (n+1) x (k-1)
  ∧ 0 < ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖
  ∧ (‖ExteriorNorm.compoundMatrix k (cocycle A T n x)‖ ^ 2
        / ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖ ^ 2
      * (1 - (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
        * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2)
      ≤ (∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i)
        - ((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k)
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ ^ 2)
  ∧ (((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k)
        * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ ^ 2
      < ∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i)
  ∧ ((‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
        * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
      * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
        / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2 < 1)

/-- **Per-step conditions discharge the increment bound.** `stepHypCocycle` at `n`
gives the band-projector increment bound `‖Pₙ₊₁ − Pₙ‖ ≤ bCocycle x n` via
`norm_bandProjector_succ_sub_le_cocycle`. -/
theorem stepHypCocycle_imp_step (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    (hA : ∀ x, (A x).det ≠ 0) (c : ℝ) {k : ℕ} (hk1 : 1 ≤ k) (hkd : k ≤ Fintype.card (Fin d))
    (x : X) (n : ℕ) (h : stepHypCocycle A T c k hkd x n) :
    ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
        - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖ ≤ bCocycle A T x k n := by
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩ := h
  exact norm_bandProjector_succ_sub_le_cocycle A T hA n x c hk1 hkd h1 h2 h3 h4 h5 h6 h7 h8 h9 h10

/-- **Unconditional band-projector a.e. convergence.** For `μ`-a.e. `x`, the band
projector `bandProjector A T (indicator (Ioi c) 1) n x` converges to a limiting projector `P`. This
is
the convergence of the Oseledets spectral projector pinned by the growing spectral gap. The proof
discharges the per-step increment bound (via `stepHypCocycle_imp_step`) from the a.e.
eventual cut/gap/regime conditions `hstepAE`, and feeds the resulting a.e. summability — by the root
test on `bCocycle` (whose `(1/n)·log` tends to `λₖ − λₖ₋₁ < 0` a.e., supplied as `hblog`/`hLneg` by
the scalar layer) — into the soft-analysis Cauchy packaging
`exists_tendsto_bandProjector`.
The hypotheses `hstepAE`, `hblog`, `hLneg`, `hbnn`, `hbpos` are the genuine outputs of the ergodic
Lyapunov-spectrum structure and the scalar root-test layer (`tendsto_log_singularValue`,
`tendsto_logNorm_compound_orbit_div_atTop_zero`); the conclusion is the UNCONDITIONAL a.e. existence
of the limiting Oseledets band projector. -/
theorem exists_tendsto_bandProjector_cocycle
    (A : X → Matrix (Fin d) (Fin d) ℝ) (hA : ∀ x, (A x).det ≠ 0)
    (c : ℝ) {k : ℕ} (hk1 : 1 ≤ k) (hkd : k ≤ Fintype.card (Fin d))
    (hstepAE : ∀ᵐ x ∂μ, ∀ᶠ n in atTop, stepHypCocycle A T c k hkd x n)
    (hbnn : ∀ᵐ x ∂μ, ∀ n, 0 ≤ bCocycle A T x k n)
    (hbpos : ∀ᵐ x ∂μ, ∀ᶠ n in atTop, 0 < bCocycle A T x k n)
    (L : X → ℝ) (hLneg : ∀ᵐ x ∂μ, L x < 0)
    (hblog : ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (bCocycle A T x k n)) atTop (𝓝 (L x))) :
    ∀ᵐ x ∂μ, ∃ P : Matrix (Fin d) (Fin d) ℝ,
      Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) atTop (𝓝 P) := by
  have hstep : ∀ᵐ x ∂μ, ∀ᶠ n in atTop,
      ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
          - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖ ≤ bCocycle A T x k n := by
    filter_upwards [hstepAE] with x hx
    filter_upwards [hx] with n hn
    exact stepHypCocycle_imp_step A T hA c hk1 hkd x n hn
  exact exists_tendsto_bandProjector (μ := μ) (c := c) A (fun x => bCocycle A T x k)
    hbnn hbpos L hLneg hblog hstep


/-- A nonnegative, eventually-positive sequence whose normalized log tends to a negative
limit converges to `0`. (Root test ⟹ summable ⟹ tail vanishes.) -/
theorem tendsto_zero_of_logLimit_neg (a : ℕ → ℝ) (hnn : ∀ n, 0 ≤ a n)
    (hpos : ∀ᶠ n in atTop, 0 < a n) {L : ℝ} (hL : L < 0)
    (hlog : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (a n)) atTop (𝓝 L)) :
    Tendsto a atTop (𝓝 0) :=
  (summable_of_logLimit_neg a hnn hpos hL hlog).tendsto_atTop_zero

/-- Per-point log-limit for `bCocycle`. -/
theorem tendsto_log_bCocycle_point {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) {x : X} {k : ℕ} (hk1 : 1 ≤ k) (hkd : k < d)
    {lamK lamK1 : ℝ}
    (hσk : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k))
      atTop (𝓝 lamK))
    (hσk1 : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)))
      atTop (𝓝 lamK1))
    (hcomp : Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖)
      atTop (𝓝 0))
    (hcompinv : Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖)
      atTop (𝓝 0))
    (hgap : lamK < lamK1) :
    Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (bCocycle A T x k n)) atTop (𝓝 (lamK - lamK1)) := by
  have hd : 0 < d := lt_of_le_of_lt (Nat.zero_le _) hkd
  -- abbreviations
  set cB : ℕ → ℝ := fun n => ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ with hcBdef
  set cBi : ℕ → ℝ := fun n => ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖ with hcBidef
  set σk : ℕ → ℝ := fun n => (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k with hσkdef
  set σk1 : ℕ → ℝ := fun n => (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)
    with hσk1def
  -- positivity facts for n ≥ 1
  have hcBpos : ∀ n, 0 < cB n := fun n =>
    norm_compound_pos k (hA _) (le_of_lt hkd) hd
  have hcBipos : ∀ n, 0 < cBi n := by
    intro n
    have hdet : ((A (T^[n] x))⁻¹).det ≠ 0 := by
      rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA _)
    exact norm_compound_pos k hdet (le_of_lt hkd) hd
  have hσkpos : ∀ n, 0 < σk n := fun n =>
    singularValues_cocycle_pos hA n x (lt_of_lt_of_le hkd (le_refl d))
  have hσk1pos : ∀ n, 0 < σk1 n := fun n =>
    singularValues_cocycle_pos hA n x (by omega)
  -- the ratio
  set r : ℕ → ℝ := fun n => σk n / σk1 n with hrdef
  have hrpos : ∀ n, 0 < r n := fun n => div_pos (hσkpos n) (hσk1pos n)
  -- κ² := (cB·cBi)²
  set κ2 : ℕ → ℝ := fun n => (cB n * cBi n) ^ 2 with hκ2def
  have hκ2pos : ∀ n, 0 < κ2 n := fun n => by
    rw [hκ2def]; exact pow_pos (mul_pos (hcBpos n) (hcBipos n)) 2
  -- (1/n) log r → lamK - lamK1
  have hlogr : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (r n)) atTop (𝓝 (lamK - lamK1)) := by
    have : (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (r n))
        = fun n : ℕ => ((n : ℝ)⁻¹ * Real.log (σk n)) - ((n : ℝ)⁻¹ * Real.log (σk1 n)) := by
      funext n
      rw [hrdef, Real.log_div (ne_of_gt (hσkpos n)) (ne_of_gt (hσk1pos n))]; ring
    rw [this]; exact hσk.sub hσk1
  -- (1/n) log κ² → 0
  have hlogκ2 : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2 n)) atTop (𝓝 0) := by
    have heq : (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2 n))
        = fun n : ℕ =>
          (2 : ℝ) * (((n : ℝ)⁻¹ * Real.log (cB n)) + ((n : ℝ)⁻¹ * Real.log (cBi n))) := by
      funext n
      rw [hκ2def, Real.log_pow, Real.log_mul (ne_of_gt (hcBpos n)) (ne_of_gt (hcBipos n))]
      push_cast; ring
    rw [heq]
    have := (hcomp.add hcompinv).const_mul (2 : ℝ)
    simpa using this
  -- (1/n) log (κ²·r) → lamK - lamK1
  have hlogκ2r : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2 n * r n)) atTop
      (𝓝 (lamK - lamK1)) := by
    have heq : (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2 n * r n))
        = fun n : ℕ => ((n : ℝ)⁻¹ * Real.log (κ2 n)) + ((n : ℝ)⁻¹ * Real.log (r n)) := by
      funext n
      rw [Real.log_mul (ne_of_gt (hκ2pos n)) (ne_of_gt (hrpos n))]; ring
    rw [heq]
    have := hlogκ2.add hlogr
    simpa using this
  -- κ²r² → 0  (since (1/n)log(κ²r²) → 2(lamK-lamK1) < 0)
  have hlogκ2r2 : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2 n * (r n) ^ 2)) atTop
      (𝓝 (2 * (lamK - lamK1))) := by
    have heq : (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2 n * (r n) ^ 2))
        = fun n : ℕ => ((n : ℝ)⁻¹ * Real.log (κ2 n))
            + (2 : ℝ) * ((n : ℝ)⁻¹ * Real.log (r n)) := by
      funext n
      have hrlog : Real.log ((r n) ^ 2) = 2 * Real.log (r n) := by
        rw [Real.log_pow]; push_cast; ring
      rw [Real.log_mul (ne_of_gt (hκ2pos n)) (pow_ne_zero 2 (ne_of_gt (hrpos n))), hrlog]
      ring
    rw [heq]
    have := hlogκ2.add (hlogr.const_mul (2 : ℝ))
    simpa using this
  have hκ2r2_tendsto : Tendsto (fun n : ℕ => κ2 n * (r n) ^ 2) atTop (𝓝 0) := by
    apply tendsto_zero_of_logLimit_neg _
      (fun n => le_of_lt (mul_pos (hκ2pos n) (pow_pos (hrpos n) 2)))
      (Filter.Eventually.of_forall (fun n => mul_pos (hκ2pos n) (pow_pos (hrpos n) 2)))
      (L := 2 * (lamK - lamK1)) (by linarith) hlogκ2r2
  -- v n := 1 - κ²r² → 1
  set v : ℕ → ℝ := fun n => 1 - κ2 n * (r n) ^ 2 with hvdef
  have hv_tendsto : Tendsto v atTop (𝓝 1) := by
    have : Tendsto (fun n : ℕ => (1 : ℝ) - κ2 n * (r n) ^ 2) atTop (𝓝 (1 - 0)) :=
      tendsto_const_nhds.sub hκ2r2_tendsto
    simpa using this
  -- log v → 0
  have hlogv0 : Tendsto (fun n : ℕ => Real.log (v n)) atTop (𝓝 0) := by
    have : Tendsto (fun n : ℕ => Real.log (v n)) atTop (𝓝 (Real.log 1)) :=
      (Real.continuousAt_log (by norm_num)).tendsto.comp hv_tendsto
    simpa using this
  -- (1/n) log v → 0
  have hloginvv : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (v n)) atTop (𝓝 0) := by
    have h1 : Tendsto (fun n : ℕ => (n : ℝ)⁻¹) atTop (𝓝 0) :=
      tendsto_inv_atTop_zero.comp tendsto_natCast_atTop_atTop
    have := h1.mul hlogv0
    simpa using this
  -- (1/n) log √(2k) → 0
  have hsqrt : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (Real.sqrt (2 * k))) atTop (𝓝 0) := by
    have h1 : Tendsto (fun n : ℕ => (n : ℝ)⁻¹) atTop (𝓝 0) :=
      tendsto_inv_atTop_zero.comp tendsto_natCast_atTop_atTop
    have := h1.mul_const (Real.log (Real.sqrt (2 * k)))
    simpa [mul_comm] using this
  have hsqrtpos : 0 < Real.sqrt (2 * k) := by
    apply Real.sqrt_pos.mpr
    have : (1:ℝ) ≤ (k:ℝ) := by exact_mod_cast hk1
    linarith
  -- assemble: log bCocycle = log√(2k) + log(κ²r) - log v
  have hfinal : Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (Real.sqrt (2 * k))
          + ((n : ℝ)⁻¹ * Real.log (κ2 n * r n) - (n : ℝ)⁻¹ * Real.log (v n))) atTop
      (𝓝 (lamK - lamK1)) := by
    have h := hsqrt.add (hlogκ2r.sub hloginvv)
    have : (0:ℝ) + ((lamK - lamK1) - 0) = lamK - lamK1 := by ring
    rwa [this] at h
  -- need eventual v > 0 to split logs
  have hvpos : ∀ᶠ n in atTop, 0 < v n := by
    have := hv_tendsto.eventually (eventually_gt_nhds (show (0:ℝ) < 1 by norm_num))
    exact this
  refine hfinal.congr' ?_
  filter_upwards [hvpos] with n hvn
  -- bCocycle n = √(2k) · (κ²·r / v)
  have hbeq : bCocycle A T x k n = Real.sqrt (2 * k) * (κ2 n * r n / v n) := by
    rw [bCocycle]
  have hquot : (0:ℝ) < κ2 n * r n / v n := div_pos (mul_pos (hκ2pos n) (hrpos n)) hvn
  rw [hbeq, Real.log_mul (ne_of_gt hsqrtpos) (ne_of_gt hquot),
      Real.log_div (ne_of_gt (mul_pos (hκ2pos n) (hrpos n))) (ne_of_gt hvn)]
  ring

set_option linter.unusedSectionVars false in
/-- The count of unsorted eigenvalues `> c` equals the count of sorted eigenvalues `> c`. -/
theorem card_eigenvalues_gt_eq_card_eigenvalues₀_gt
    {M : Matrix (Fin d) (Fin d) ℝ} (hM : M.IsHermitian) (c : ℝ) :
    Fintype.card {i : Fin d // c < hM.eigenvalues i}
      = Fintype.card {j : Fin (Fintype.card (Fin d)) // c < hM.eigenvalues₀ j} := by
  classical
  apply Fintype.card_congr
  refine
    { toFun := fun i => ⟨(Fintype.equivOfCardEq (Fintype.card_fin _)).symm i.1, ?_⟩
      invFun := fun j => ⟨(Fintype.equivOfCardEq (Fintype.card_fin _)) j.1, ?_⟩
      left_inv := ?_
      right_inv := ?_ }
  · have := i.2; rwa [Matrix.IsHermitian.eigenvalues] at this
  · have := j.2; rw [Matrix.IsHermitian.eigenvalues]; simpa using this
  · intro i; ext; simp
  · intro j; ext; simp

/-- If an antitone `Fin N → ℝ` family has its value at index `⟨k-1⟩` above `c` and at index `⟨k⟩`
below `c`, then exactly `k` of its values exceed `c`. -/
theorem card_antitone_gt_eq {N : ℕ} (f : Fin N → ℝ) (hf : Antitone f) (c : ℝ)
    {k : ℕ} (hk1 : 1 ≤ k) (hkN : k < N)
    (htop : c < f ⟨k - 1, lt_of_le_of_lt (Nat.sub_le k 1) hkN⟩) (hbot : f ⟨k, hkN⟩ < c) :
    Fintype.card {j : Fin N // c < f j} = k := by
  classical
  have hiff : ∀ j : Fin N, c < f j ↔ (j : ℕ) < k := by
    intro j
    constructor
    · intro hj
      by_contra hjk
      have hjk' : k ≤ (j : ℕ) := not_lt.mp hjk
      have : f j ≤ f ⟨k, hkN⟩ := hf (by simp [Fin.le_def]; omega)
      linarith
    · intro hj
      have : f ⟨k - 1, by omega⟩ ≤ f j := hf (by simp [Fin.le_def]; omega)
      linarith
  have hequiv : {j : Fin N // c < f j} ≃ {j : Fin N // (j : ℕ) < k} :=
    Equiv.subtypeEquivRight hiff
  rw [Fintype.card_congr hequiv, Fintype.card_subtype]
  -- count of `j : Fin N` with `(j:ℕ) < k` is `k`
  have hcardeq : (Finset.univ.filter (fun j : Fin N => (j : ℕ) < k)).card
      = (Finset.range k).card := by
    apply Finset.card_bij (fun (j : Fin N) _ => (j : ℕ))
    · intro j hj; simp only [Finset.mem_filter] at hj
      exact Finset.mem_range.mpr hj.2
    · intro a ha b hb hab
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at ha hb
      exact Fin.ext hab
    · intro b hb
      simp only [Finset.mem_range] at hb
      exact ⟨⟨b, by omega⟩, by simp [hb], rfl⟩
  rw [hcardeq, Finset.card_range]

set_option maxHeartbeats 800000 in -- heavy elaboration; exceeds the default budget
-- raised: the `⋀^k`-indexed compound/Plücker Euclidean elaboration is heartbeat-heavy.
/-- The two scalar inequalities `hμ₀lb`/`hgapμ` of `stepHypCocycle`, from the compound lower bound
`μ̃₀ ≥ cM²/cBi²` (`norm_sq_compound_mul_ge`) and the regime `κ²r² < 1`. -/
theorem step_inequalities {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (n : ℕ) (x : X) {k : ℕ} (hk1 : 1 ≤ k) (hkd : k < d)
    (hcBipos : 0 < ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖)
    (hκr : (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
        * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k - 1)) ^ 2 < 1) :
    (‖ExteriorNorm.compoundMatrix k (cocycle A T n x)‖ ^ 2
          / ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖ ^ 2
        * (1 - (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
            * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
          * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
            / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2)
        ≤ (∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i)
          - ((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k)
            * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ ^ 2)
    ∧ (((∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k)
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ ^ 2
        < ∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i) := by
  classical
  have hd : 0 < d := lt_of_le_of_lt (Nat.zero_le _) hkd
  set B := A (T^[n] x) with hBdef
  set M := cocycle A T n x with hMdef
  set cM := ‖ExteriorNorm.compoundMatrix k M‖ with hcM
  set cB := ‖ExteriorNorm.compoundMatrix k B‖ with hcB
  set cBi := ‖ExteriorNorm.compoundMatrix k B⁻¹‖ with hcBi
  set σk := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k with hσk
  set σk1 := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) with hσk1
  set r := σk / σk1 with hr
  -- positivity
  have hcMpos : 0 < cM := norm_compound_pos k (det_cocycle_ne_zero hA n x) (le_of_lt hkd) hd
  have hcBpos : 0 < cB := norm_compound_pos k (hA _) (le_of_lt hkd) hd
  have hσkpos : 0 < σk := singularValues_cocycle_pos hA n x (lt_of_lt_of_le hkd (le_refl d))
  have hσk1pos : 0 < σk1 := singularValues_cocycle_pos hA n x (by omega)
  have hrpos : 0 < r := div_pos hσkpos hσk1pos
  -- μ₀ = ‖compound k (B*M)‖²  ≥ cM²/cBi²
  have hBM : B * M = cocycle A T (n+1) x := by
    rw [hBdef, hMdef, show n+1 = 1 + n from by omega, cocycle_add, cocycle_one]
  have hμ₀eq : (∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i)
      = ‖ExteriorNorm.compoundMatrix k (B * M)‖ ^ 2 := by
    rw [hBM]
    simp only [lamCocycle]
    rw [Finset.prod_pow, ExteriorNorm.prod_singularValues_eq_l2_opNorm_compound]
  set μ₀ := ∏ i ∈ Finset.range k, lamCocycle A T (n+1) x i with hμ₀
  have hμ₀lb_compound : cM ^ 2 / cBi ^ 2 ≤ μ₀ := by
    rw [hμ₀eq]
    exact ExteriorNorm.norm_sq_compound_mul_ge k (hA _) M hcBipos
  -- μ₁ = cM²·r²
  have hcMsq : cM ^ 2 = (∏ i ∈ Finset.range k,
      (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i) ^ 2 := by
    rw [hcM, hMdef, ← ExteriorNorm.prod_singularValues_eq_l2_opNorm_compound]
  have hμ₁eq : (∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k
      = cM ^ 2 * r ^ 2 := by
    simp only [lamCocycle]
    rw [hcMsq, hr, hσk, hσk1, Finset.prod_pow]
    have hsplit : (∏ i ∈ Finset.range k,
          (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)
        = (∏ i ∈ Finset.range (k-1),
            (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)
          * (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) := by
      conv_lhs => rw [show k = (k-1) + 1 from by omega, Finset.prod_range_succ]
    rw [hsplit]
    have hσk1ne : (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) ≠ 0 :=
      ne_of_gt hσk1pos
    field_simp
  set μ₁ := (∏ i ∈ Finset.range (k-1), lamCocycle A T n x i) * lamCocycle A T n x k with hμ₁
  -- κ²r² in terms of cB,cBi,r
  have hκr' : cB ^ 2 * cBi ^ 2 * r ^ 2 < 1 := by
    have : (cB * cBi) ^ 2 * r ^ 2 < 1 := hκr
    nlinarith [this]
  have hcBi2pos : (0:ℝ) < cBi ^ 2 := by positivity
  have hcM2pos : (0:ℝ) < cM ^ 2 := by positivity
  -- key: cM²r²cB² < cM²/cBi²
  have hkey : cM ^ 2 * r ^ 2 * cB ^ 2 < cM ^ 2 / cBi ^ 2 := by
    rw [lt_div_iff₀ hcBi2pos]
    nlinarith [hκr', hcM2pos, mul_pos hcM2pos (mul_pos (pow_pos hrpos 2) (pow_pos hcBpos 2))]
  refine ⟨?_, ?_⟩
  · -- hμ₀lb
    rw [hμ₁eq]
    have hLHS : cM ^ 2 / cBi ^ 2 * (1 - (cB * cBi) ^ 2 * r ^ 2)
        = cM ^ 2 / cBi ^ 2 - cM ^ 2 * r ^ 2 * cB ^ 2 := by
      have hcBine : cBi ≠ 0 := ne_of_gt hcBipos
      have : cM ^ 2 / cBi ^ 2 * ((cB * cBi) ^ 2 * r ^ 2) = cM ^ 2 * r ^ 2 * cB ^ 2 := by
        field_simp
      rw [mul_sub, mul_one, this]
    rw [hLHS]
    linarith [hμ₀lb_compound]
  · -- hgapμ
    rw [hμ₁eq]
    calc cM ^ 2 * r ^ 2 * cB ^ 2 < cM ^ 2 / cBi ^ 2 := hkey
      _ ≤ μ₀ := hμ₀lb_compound


/-- `bCocycle` is positive once the regime `κ²r² < 1` holds. -/
theorem bCocycle_pos_of_regime {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) {k : ℕ} (hk1 : 1 ≤ k) (hkd : k < d) (n : ℕ)
    (hκr : (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
        * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k - 1)) ^ 2 < 1) :
    0 < bCocycle A T x k n := by
  have hd : 0 < d := lt_of_le_of_lt (Nat.zero_le _) hkd
  rw [bCocycle]
  have hcBpos : 0 < ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ :=
    norm_compound_pos k (hA _) (le_of_lt hkd) hd
  have hcBidet : ((A (T^[n] x))⁻¹).det ≠ 0 := by
    rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA _)
  have hcBipos : 0 < ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖ :=
    norm_compound_pos k hcBidet (le_of_lt hkd) hd
  have hσkpos : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k :=
    singularValues_cocycle_pos hA n x (lt_of_lt_of_le hkd (le_refl d))
  have hσk1pos : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) :=
    singularValues_cocycle_pos hA n x (by omega)
  have hsqrtpos : 0 < Real.sqrt (2 * k) := by
    apply Real.sqrt_pos.mpr
    have : (1:ℝ) ≤ (k:ℝ) := by exact_mod_cast hk1
    linarith
  have hrpos : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
      / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) := div_pos hσkpos hσk1pos
  have hnumpos : 0 < (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
        * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
      * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
        / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) :=
    mul_pos (pow_pos (mul_pos hcBpos hcBipos) 2) hrpos
  have hdenpos : 0 < 1 - (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
        * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2 := by
    linarith [hκr]
  exact mul_pos hsqrtpos (div_pos hnumpos hdenpos)

set_option maxHeartbeats 1600000 in -- heavy elaboration; exceeds the default budget
-- raised: the `⋀^k`-indexed compound/Plücker Euclidean elaboration is heartbeat-heavy.
/-- **Unconditional band-projector a.e. convergence at a distinct-exponent gap.**
For an ergodic, integrable, invertible cocycle and a threshold `c` strictly between the
exponentials of two consecutive distinct Lyapunov exponents at the cut index `k`
(`e^{λₖ} < c < e^{λₖ₋₁}` with `λₖ < λₖ₋₁`), the band spectral projector converges `μ`-a.e. -/
theorem tendsto_bandProjector_of_gap [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (c : ℝ) {k : ℕ} (hk1 : 1 ≤ k) (hkd : k < d)
    (lamK lamK1 : ℝ) (hgap : lamK < lamK1)
    (hclo : Real.exp lamK < c) (hchi : c < Real.exp lamK1)
    (hσkAE : ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k))
      atTop (𝓝 lamK))
    (hσk1AE : ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)))
      atTop (𝓝 lamK1)) :
    ∀ᵐ x ∂μ, ∃ P : Matrix (Fin d) (Fin d) ℝ,
      Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) atTop (𝓝 P) := by
  classical
  have hd : 0 < d := lt_of_le_of_lt (Nat.zero_le _) hkd
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  have hTmeas : Measurable T := hmp.measurable
  have hkdc : k ≤ Fintype.card (Fin d) := le_of_lt (lt_of_lt_of_eq hkd (Fintype.card_fin d).symm)
  -- compound tempered factors (forward and inverse)
  have hcompAE := tendsto_logNorm_compound_orbit_div_atTop_zero hmp hA hAmeas hTmeas hint hint'
    k (le_of_lt hkd) hd
  -- inverse: apply the same lemma to the cocycle `A⁻¹`
  have hAinvmeas : Measurable (fun x => (A x)⁻¹) := measurable_inv_matrix.comp hAmeas
  have hAinvdet : ∀ x, ((A x)⁻¹).det ≠ 0 := by
    intro x; rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA x)
  have hintinvinv : IntegrableLogNorm (fun x => ((A x)⁻¹)⁻¹) μ := by
    apply hint.congr
    filter_upwards with x
    rw [Matrix.nonsing_inv_nonsing_inv _ (Ne.isUnit (hA x))]
  have hcompinvAE := tendsto_logNorm_compound_orbit_div_atTop_zero hmp hAinvdet hAinvmeas hTmeas
    hint' hintinvinv k (le_of_lt hkd) hd
  -- index facts
  have hkcard : k < Fintype.card (Fin d) := lt_of_lt_of_eq hkd (Fintype.card_fin d).symm
  have hk1card : k - 1 < Fintype.card (Fin d) := by rw [Fintype.card_fin]; omega
  -- dominating sequence
  set b : X → ℕ → ℝ := fun x n => max 0 (bCocycle A T x k n) with hbdef
  -- log-limit of bCocycle, a.e.
  have hblogAE : ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (bCocycle A T x k n)) atTop
        (𝓝 (lamK - lamK1)) := by
    filter_upwards [hσkAE, hσk1AE, hcompAE, hcompinvAE] with x hσkx hσk1x hcompx hcompinvx
    exact tendsto_log_bCocycle_point hA hk1 hkd hσkx hσk1x hcompx hcompinvx hgap
  -- the eventual cut/gap/regime data, a.e.
  have hQAE : ∀ᵐ x ∂μ, ∀ᶠ n in atTop,
      (c < (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨k - 1, hk1card⟩
        ∧ (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨k, hkcard⟩ < c
        ∧ (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
            < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)
        ∧ (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
              * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
            * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
              / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2 < 1) := by
    filter_upwards [hσkAE, hσk1AE, hcompAE, hcompinvAE] with x hσkx hσk1x hcompx hcompinvx
    -- eigenvalue convergences
    have hev_k1 : Tendsto
        (fun n : ℕ => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨k - 1, hk1card⟩)
        atTop (𝓝 (Real.exp lamK1)) :=
      eigenvalues_qpow_tendsto hA ⟨k - 1, hk1card⟩ (by
        have hcast : ((⟨k - 1, hk1card⟩ : Fin (Fintype.card (Fin d))) : ℕ) = k - 1 := rfl
        simpa [hcast] using hσk1x)
    have hev_k : Tendsto
        (fun n : ℕ => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨k, hkcard⟩)
        atTop (𝓝 (Real.exp lamK)) :=
      eigenvalues_qpow_tendsto hA ⟨k, hkcard⟩ (by
        have hcast : ((⟨k, hkcard⟩ : Fin (Fintype.card (Fin d))) : ℕ) = k := rfl
        simpa [hcast] using hσkx)
    -- r → 0
    have hσkpos : ∀ n, 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k := fun n =>
      singularValues_cocycle_pos hA n x (lt_of_lt_of_le hkd (le_refl d))
    have hσk1pos : ∀ n, 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) :=
      fun n => singularValues_cocycle_pos hA n x (by omega)
    have hlogr : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)))
        atTop (𝓝 (lamK - lamK1)) := by
      have heq : (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
            / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)))
          = fun n : ℕ => ((n : ℝ)⁻¹ *
              Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k))
            - ((n : ℝ)⁻¹ *
              Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1))) := by
        funext n
        rw [Real.log_div (ne_of_gt (hσkpos n)) (ne_of_gt (hσk1pos n))]; ring
      rw [heq]; exact hσkx.sub hσk1x
    have hr0 : Tendsto (fun n : ℕ => (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
        / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) atTop (𝓝 0) :=
      tendsto_zero_of_logLimit_neg _ (fun n => le_of_lt (div_pos (hσkpos n) (hσk1pos n)))
        (Filter.Eventually.of_forall (fun n => div_pos (hσkpos n) (hσk1pos n)))
        (L := lamK - lamK1) (by linarith) hlogr
    -- κ²r² → 0
    set κ2r2 : ℕ → ℝ := fun n => (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
          * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) ^ 2
        * ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
          / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1)) ^ 2 with hκ2r2def
    have hcBpos : ∀ n, 0 < ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖ := fun n =>
      norm_compound_pos k (hA _) (le_of_lt hkd) hd
    have hcBipos : ∀ n, 0 < ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖ := by
      intro n
      have hdet : ((A (T^[n] x))⁻¹).det ≠ 0 := by
        rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA _)
      exact norm_compound_pos k hdet (le_of_lt hkd) hd
    have hκ2r2pos : ∀ n, 0 < κ2r2 n := by
      intro n; rw [hκ2r2def]
      exact mul_pos (pow_pos (mul_pos (hcBpos n) (hcBipos n)) 2)
        (pow_pos (div_pos (hσkpos n) (hσk1pos n)) 2)
    have hlogκ2r2 : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2r2 n)) atTop
        (𝓝 (2 * 0 + 2 * (lamK - lamK1))) := by
      have heq : (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (κ2r2 n))
          = fun n : ℕ => (2 : ℝ) * ((n : ℝ)⁻¹ *
                Real.log (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
                  * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖))
              + (2 : ℝ) * ((n : ℝ)⁻¹ *
                Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
                  / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1))) := by
        funext n
        rw [hκ2r2def,
          Real.log_mul (ne_of_gt (pow_pos (mul_pos (hcBpos n) (hcBipos n)) 2))
            (pow_ne_zero 2 (ne_of_gt (div_pos (hσkpos n) (hσk1pos n)))),
          Real.log_pow, Real.log_pow]
        push_cast; ring
      rw [heq]
      have hcombo : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
              * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖)) atTop (𝓝 0) := by
        have heqc : (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log (‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖
                * ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖))
            = fun n : ℕ => ((n : ℝ)⁻¹ *
                Real.log ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))‖)
              + ((n : ℝ)⁻¹ *
                Real.log ‖ExteriorNorm.compoundMatrix k (A (T^[n] x))⁻¹‖) := by
          funext n
          rw [Real.log_mul (ne_of_gt (hcBpos n)) (ne_of_gt (hcBipos n))]; ring
        rw [heqc]; simpa using hcompx.add hcompinvx
      exact (hcombo.const_mul (2:ℝ)).add (hlogr.const_mul (2:ℝ))
    have hκ2r20 : Tendsto κ2r2 atTop (𝓝 0) :=
      tendsto_zero_of_logLimit_neg _ (fun n => le_of_lt (hκ2r2pos n))
        (Filter.Eventually.of_forall hκ2r2pos) (L := 2 * 0 + 2 * (lamK - lamK1))
        (by linarith) hlogκ2r2
    -- now eventual facts
    have e1 : ∀ᶠ n in atTop,
        c < (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨k - 1, hk1card⟩ :=
      hev_k1.eventually (eventually_gt_nhds hchi)
    have e2 : ∀ᶠ n in atTop,
        (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨k, hkcard⟩ < c :=
      hev_k.eventually (eventually_lt_nhds hclo)
    have e3 : ∀ᶠ n in atTop, (Matrix.toEuclideanLin (cocycle A T n x)).singularValues k
        / (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (k-1) < 1 :=
      hr0.eventually (eventually_lt_nhds (show (0:ℝ) < 1 by norm_num))
    have e4 : ∀ᶠ n in atTop, κ2r2 n < 1 :=
      hκ2r20.eventually (eventually_lt_nhds (show (0:ℝ) < 1 by norm_num))
    filter_upwards [e1, e2, e3, e4] with n h1 h2 h3 h4
    refine ⟨h1, h2, ?_, h4⟩
    -- σₖ < σₖ₋₁ from r < 1
    have hσk1pos' := hσk1pos n
    rw [div_lt_one hσk1pos'] at h3
    exact h3
  -- build the eventual stepHypCocycle from hQAE (using n and n+1)
  have hstepAE : ∀ᵐ x ∂μ, ∀ᶠ n in atTop, stepHypCocycle A T c k hkdc x n := by
    filter_upwards [hQAE] with x hQ
    -- shift hQ to n+1
    have hQshift : ∀ᶠ n in atTop,
        (c < (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀ ⟨k - 1, hk1card⟩
          ∧ (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀ ⟨k, hkcard⟩ < c
          ∧ (Matrix.toEuclideanLin (cocycle A T (n+1) x)).singularValues k
              < (Matrix.toEuclideanLin (cocycle A T (n+1) x)).singularValues (k-1)
          ∧ (‖ExteriorNorm.compoundMatrix k (A (T^[n+1] x))‖
                * ‖ExteriorNorm.compoundMatrix k (A (T^[n+1] x))⁻¹‖) ^ 2
              * ((Matrix.toEuclideanLin (cocycle A T (n+1) x)).singularValues k
                / (Matrix.toEuclideanLin (cocycle A T (n+1) x)).singularValues (k-1)) ^ 2 < 1) := by
      have := hQ
      rw [eventually_atTop] at this ⊢
      obtain ⟨N, hN⟩ := this
      exact ⟨N, fun n hn => hN (n+1) (by omega)⟩
    filter_upwards [hQ, hQshift] with n hQn hQn1
    obtain ⟨ha, hb', hc', hd'⟩ := hQn
    obtain ⟨ha1, hb1, hc1, hd1⟩ := hQn1
    -- antitone witnesses
    have hanti_n := (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀_antitone
    have hanti_n1 := (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀_antitone
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, hd'⟩
    · -- top n
      intro j
      have : (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨k - 1, hk1card⟩
          ≤ (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ ⟨j, lt_of_lt_of_le j.2 hkdc⟩ :=
        hanti_n (by simp only [Fin.le_def]; omega)
      linarith [ha]
    · -- count n
      rw [card_eigenvalues_gt_eq_card_eigenvalues₀_gt]
      exact card_antitone_gt_eq (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀
        hanti_n c hk1 hkcard ha hb'
    · -- top n+1
      intro j
      have : (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀ ⟨k - 1, hk1card⟩
          ≤ (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀
            ⟨j, lt_of_lt_of_le j.2 hkdc⟩ :=
        hanti_n1 (by simp only [Fin.le_def]; omega)
      linarith [ha1]
    · -- count n+1
      rw [card_eigenvalues_gt_eq_card_eigenvalues₀_gt]
      exact card_antitone_gt_eq (qpow_isSelfAdjoint A T (n+1) x).isHermitian.eigenvalues₀
        hanti_n1 c hk1 hkcard ha1 hb1
    · -- gap n
      simp only [lamCocycle]
      have hnn := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg k
      nlinarith [hc', hnn]
    · -- gap n+1
      simp only [lamCocycle]
      have hnn := (Matrix.toEuclideanLin (cocycle A T (n+1) x)).singularValues_nonneg k
      nlinarith [hc1, hnn]
    · -- cBipos n
      have hdet : ((A (T^[n] x))⁻¹).det ≠ 0 := by
        rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA _)
      exact norm_compound_pos k hdet (le_of_lt hkd) hd
    · -- hμ₀lb
      have hcBidet : ((A (T^[n] x))⁻¹).det ≠ 0 := by
        rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA _)
      exact (step_inequalities hA n x hk1 hkd
        (norm_compound_pos k hcBidet (le_of_lt hkd) hd) hd').1
    · -- hgapμ
      have hcBidet : ((A (T^[n] x))⁻¹).det ≠ 0 := by
        rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA _)
      exact (step_inequalities hA n x hk1 hkd
        (norm_compound_pos k hcBidet (le_of_lt hkd) hd) hd').2
  -- now route through the abstract Cauchy packaging with `b = max 0 bCocycle`
  have hb : ∀ᵐ x ∂μ, ∀ n, 0 ≤ b x n :=
    Filter.Eventually.of_forall (fun x n => le_max_left _ _)
  have hbpos : ∀ᵐ x ∂μ, ∀ᶠ n in atTop, 0 < b x n := by
    filter_upwards [hstepAE] with x hx
    filter_upwards [hx] with n hn
    obtain ⟨_, _, _, _, _, _, _, _, _, hκr⟩ := hn
    exact lt_max_of_lt_right (bCocycle_pos_of_regime hA x hk1 hkd n hκr)
  have hlogb : ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (b x n)) atTop (𝓝 (lamK - lamK1)) := by
    filter_upwards [hblogAE, hstepAE] with x hlx hstepx
    refine hlx.congr' ?_
    filter_upwards [hstepx] with n hn
    obtain ⟨_, _, _, _, _, _, _, _, _, hκr⟩ := hn
    have hbpn : 0 < bCocycle A T x k n := bCocycle_pos_of_regime hA x hk1 hkd n hκr
    have hbxn : b x n = bCocycle A T x k n := by
      rw [hbdef]; exact max_eq_right (le_of_lt hbpn)
    rw [hbxn]
  have hLneg : ∀ᵐ x ∂μ, (fun _ : X => lamK - lamK1) x < 0 :=
    Filter.Eventually.of_forall (fun _ => by dsimp only; linarith)
  have hstep : ∀ᵐ x ∂μ, ∀ᶠ n in atTop,
      ‖bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + 1) x
          - bandProjector A T (Set.indicator (Set.Ioi c) 1) n x‖ ≤ b x n := by
    filter_upwards [hstepAE] with x hx
    filter_upwards [hx] with n hn
    have hle := stepHypCocycle_imp_step A T hA c hk1 hkdc x n hn
    exact le_trans hle (le_max_right _ _)
  exact exists_tendsto_bandProjector (μ := μ) (c := c) A b hb hbpos
    (fun _ => lamK - lamK1) hLneg hlogb hstep

end ErgodicTheory

end
