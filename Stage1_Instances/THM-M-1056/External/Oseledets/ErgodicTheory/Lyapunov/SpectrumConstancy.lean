/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.FiltrationInterfaceReduction

/-!
# Spectrum constancy: identifying the per-point spectrum with the deterministic exponent set

`ErgodicTheory.specList_eq_expEnum_of_lyapunovSpectrum_const` (in
`FiltrationInterfaceReduction.lean`) reduces the `hspec` interface of the final assembly to the
single hypothesis

```
hspecconst : ∀ᵐ x ∂μ, lyapunovSpectrum A T x = distinctExp lam0 d.
```

This file discharges `hspecconst`.  The per-point limsup spectrum `lyapunovSpectrum A T x` is the
finite set of values of the upper Lyapunov growth function `lambdaBar A T x` on nonzero vectors
(`ErgodicTheory.lyapunovSpectrum`, `ErgodicTheory.mem_lyapunovSpectrum`). Pinning that finite set to
the deterministic distinct-exponent set `distinctExp lam0 d` is a `Finset.Subset.antisymm` of two
per-vector inclusions:

* **upper inclusion** `lyapunovSpectrum A T x ⊆ distinctExp lam0 d` — every realized `lambdaBar`
  value is one of the deterministic singular-value exponents `lam0 i` (`i < d`).  This is the
  growth→exponent direction; its per-vector core is the spectral upper bound, the genuine
  analytic step of the multiplicative ergodic theorem (via the determinant/tempering squeeze).

* **lower inclusion** `distinctExp lam0 d ⊆ lyapunovSpectrum A T x` — every distinct deterministic
  exponent `lam0 i` is *attained* by some nonzero vector, i.e. lies in the `lambdaBar`-range.  Its
  per-vector core is the lower bound (`log_le_liminf_log_cocycle_apply`) combined with the
  stratum-exact `lambdaBar_eq_on_stratum`.

The two inclusions compose to the constant `distinctExp lam0 d`, so ergodic constancy of the
spectrum is automatic — the limit set is deterministic by construction, hence trivially
`T`-invariant and constant; no separate `Finset ℝ` measurability / ergodic-averaging step
is needed once the identification is in hand.  For completeness we also record, unconditionally
from `lyapunovSpectrum_equivariant_ae` together with ergodicity, that the identification
self-propagates: if it holds it holds at `T x` too, and on the full orbit.

## What is unconditional vs. hypothesis-gated

* `lyapunovSpectrum_eq_of_subsets` and `lyapunovSpectrum_eq_distinctExp_of_subsets_ae` are
  unconditional `Finset` algebra: they turn the two per-vector inclusions into the Finset identity /
  the `hspec` interface, using nothing but
  `ErgodicTheory.specList_eq_expEnum_of_lyapunovSpectrum_const`.
* The two per-vector inclusion hypotheses `hub_spec` / `hlb_spec` are the analytic interface.  The
  lower one follows from the established lower bound; the upper one is the spectral upper bound.
  They are stated here in a minimal cleanly-typed Finset shape so that the surrounding assembly can
  plug the per-vector outputs in directly.
-/

open MeasureTheory Filter Topology

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-! ## Unconditional Finset algebra: two inclusions ⟹ the identity -/

omit [MeasurableSpace X] in
/-- **The spectrum identity from the two per-vector inclusions (pointwise).**  If, at the point `x`,
every spectrum value is a deterministic exponent and every deterministic exponent is attained, then
the per-point limsup spectrum equals the deterministic distinct-exponent set. -/
theorem lyapunovSpectrum_eq_of_subsets
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {lam0 : ℕ → ℝ}
    (hub : lyapunovSpectrum A T x ⊆ distinctExp lam0 d)
    (hlb : distinctExp lam0 d ⊆ lyapunovSpectrum A T x) :
    lyapunovSpectrum A T x = distinctExp lam0 d :=
  Finset.Subset.antisymm hub hlb

/-- **`hspecconst` from the two a.e. per-vector inclusions.**  The minimal cleanly-typed reduction:
the a.e. upper inclusion (`spectrum ⊆ distinctExp`, the spectral upper bound) and the a.e.
lower inclusion (`distinctExp ⊆ spectrum`, the attainment/lower-bound layer) give the a.e. spectrum
constancy `lyapunovSpectrum A T x = distinctExp lam0 d` consumed by
`specList_eq_expEnum_of_lyapunovSpectrum_const`. -/
theorem lyapunovSpectrum_eq_distinctExp_of_subsets_ae
    {μ : Measure X} {T : X → X} (A : X → Matrix (Fin d) (Fin d) ℝ) (lam0 : ℕ → ℝ)
    (hub_spec : ∀ᵐ x ∂μ, lyapunovSpectrum A T x ⊆ distinctExp lam0 d)
    (hlb_spec : ∀ᵐ x ∂μ, distinctExp lam0 d ⊆ lyapunovSpectrum A T x) :
    ∀ᵐ x ∂μ, lyapunovSpectrum A T x = distinctExp lam0 d := by
  filter_upwards [hub_spec, hlb_spec] with x hub hlb
  exact lyapunovSpectrum_eq_of_subsets hub hlb

/-- **The `hspec` interface, discharged from the two a.e. per-vector inclusions.**  Composes
`lyapunovSpectrum_eq_distinctExp_of_subsets_ae` with
`specList_eq_expEnum_of_lyapunovSpectrum_const`: the output is *exactly* the
`hspec` hypothesis of `oseledets_filtration_of_interfaces`. -/
theorem specList_eq_expEnum_of_subsets_ae
    {μ : Measure X} {T : X → X} (A : X → Matrix (Fin d) (Fin d) ℝ) (lam0 : ℕ → ℝ)
    (hub_spec : ∀ᵐ x ∂μ, lyapunovSpectrum A T x ⊆ distinctExp lam0 d)
    (hlb_spec : ∀ᵐ x ∂μ, distinctExp lam0 d ⊆ lyapunovSpectrum A T x) :
    ∀ᵐ x ∂μ, ∃ h : specCard A T x = numExp lam0 d,
      ∀ i : Fin (specCard A T x), specList A T x i = expEnum lam0 d (Fin.cast h i) :=
  specList_eq_expEnum_of_lyapunovSpectrum_const A lam0
    (lyapunovSpectrum_eq_distinctExp_of_subsets_ae A lam0 hub_spec hlb_spec)

/-! ## Reducing the inclusions to the native `lambdaBar` shape

The two Finset inclusions are equivalent, on the a.e. good set where `lambdaBar A T x` is an
`IsUltrametricGrowth` function (`isUltrametricGrowth_lambdaBar`), to per-vector `lambdaBar`
statements:

* upper inclusion ⟺ every realized value `lambdaBar A T x v` (`v ≠ 0`) is some `lam0 j` (`j < d`) —
  this is the spectral-upper-bound output (`lambdaBar v = λᵢ` on each stratum,
  the values being the deterministic exponents);
* lower inclusion ⟺ every `lam0 j` (`j < d`) is realized by some nonzero `v` — the attainment/
  lower-bound layer.

These reductions are unconditional `mem_lyapunovSpectrum`/`mem_distinctExp` unfoldings; they let the
per-vector outputs be fed in without first repackaging into Finsets. -/

omit [MeasurableSpace X] in
/-- **Upper inclusion in native `lambdaBar`/`lam0` form.**  On the `IsUltrametricGrowth` good set,
the Finset upper inclusion `spectrum ⊆ distinctExp` is exactly: every value of `lambdaBar A T x` on
a nonzero vector is one of the deterministic exponents `lam0 j` (`j < d`). -/
theorem lyapunovSpectrum_subset_iff_lambdaBar_mem
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {lam0 : ℕ → ℝ}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) :
    lyapunovSpectrum A T x ⊆ distinctExp lam0 d ↔
      ∀ v : EuclideanSpace ℝ (Fin d), v ≠ 0 →
        ∃ j : ℕ, j < d ∧ lam0 j = lambdaBar A T x v := by
  constructor
  · intro hsub v hv
    have : lambdaBar A T x v ∈ distinctExp lam0 d := hsub (lambdaBar_mem_lyapunovSpectrum hx hv)
    exact (mem_distinctExp lam0 d).mp this
  · intro hall r hr
    obtain ⟨v, hv, hvr⟩ := (mem_lyapunovSpectrum hx).mp hr
    obtain ⟨j, hj, hjr⟩ := hall v hv
    exact (mem_distinctExp lam0 d).mpr ⟨j, hj, by rw [hjr, hvr]⟩

omit [MeasurableSpace X] in
/-- **Lower inclusion in native `lam0`/`lambdaBar` form.**  On the `IsUltrametricGrowth` good set,
the Finset lower inclusion `distinctExp ⊆ spectrum` is exactly: every deterministic exponent
`lam0 j` (`j < d`) is realized as `lambdaBar A T x v` for some nonzero `v`. -/
theorem distinctExp_subset_iff_lambdaBar_attained
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {lam0 : ℕ → ℝ}
    (hx : IsUltrametricGrowth (lambdaBar A T x)) :
    distinctExp lam0 d ⊆ lyapunovSpectrum A T x ↔
      ∀ j : ℕ, j < d →
        ∃ v : EuclideanSpace ℝ (Fin d), v ≠ 0 ∧ lambdaBar A T x v = lam0 j := by
  constructor
  · intro hsub j hj
    have hr : lam0 j ∈ lyapunovSpectrum A T x := hsub ((mem_distinctExp lam0 d).mpr ⟨j, hj, rfl⟩)
    exact (mem_lyapunovSpectrum hx).mp hr
  · intro hall r hr
    obtain ⟨j, hj, hjr⟩ := (mem_distinctExp lam0 d).mp hr
    obtain ⟨v, hv, hvr⟩ := hall j hj
    rw [← hjr, ← hvr]
    exact lambdaBar_mem_lyapunovSpectrum hx hv

/-- **`hspecconst` from the native per-vector outputs.**  Combines the two `lambdaBar`-level
reductions with the a.e. `IsUltrametricGrowth` good set: given a.e. that every realized
`lambdaBar` value is a deterministic exponent (`hub_lam`, the spectral upper bound) and every
deterministic exponent is attained (`hlb_lam`, the lower-bound/attainment layer), the spectrum is
a.e. the deterministic constant `distinctExp lam0 d`. -/
theorem lyapunovSpectrum_eq_distinctExp_of_lambdaBar
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hub_lam : ∀ᵐ x ∂μ, ∀ v : EuclideanSpace ℝ (Fin d), v ≠ 0 →
      ∃ j : ℕ, j < d ∧ lam0 j = lambdaBar A T x v)
    (hlb_lam : ∀ᵐ x ∂μ, ∀ j : ℕ, j < d →
      ∃ v : EuclideanSpace ℝ (Fin d), v ≠ 0 ∧ lambdaBar A T x v = lam0 j) :
    ∀ᵐ x ∂μ, lyapunovSpectrum A T x = distinctExp lam0 d := by
  have hUM := isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint'
  filter_upwards [hUM, hub_lam, hlb_lam] with x hx hub hlb
  refine lyapunovSpectrum_eq_of_subsets ?_ ?_
  · exact (lyapunovSpectrum_subset_iff_lambdaBar_mem hx).mpr hub
  · exact (distinctExp_subset_iff_lambdaBar_attained hx).mpr hlb

/-! ## End-to-end: the `hspec` interface under the standing hypotheses

Bundling everything: under the standard standing hypotheses, *given* the two analytic per-vector
inclusions, the `hspec` interface (and hence — via the `FiltrationInterfaceReduction` results — the
`oseledets_filtration` `hspec` slot) is discharged.  The signature lists the full standing
hypotheses so it slots directly into the surrounding assembly, even though the proof only needs the
two inclusions; this fixes the *shape* the spectral upper bound must provide. -/

-- The standing hypotheses `hT`, `hA`, `hAmeas`, `hint`, `hint'` are listed to fix the call-site
-- signature; the proof itself only consumes the two inclusions, so they are deliberately unused.
set_option linter.unusedVariables false in
/-- **Standing-hypotheses wrapper for the `hspec` interface.**  Under `Ergodic T μ`, a probability
measure, measurable invertible log-integrable `A` (and `A⁻¹`), and the two per-vector spectrum
inclusions, the `hspec` hypothesis of `oseledets_filtration_of_interfaces` holds. -/
theorem specList_eq_expEnum_of_subsets_standing
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hub_spec : ∀ᵐ x ∂μ, lyapunovSpectrum A T x ⊆ distinctExp lam0 d)
    (hlb_spec : ∀ᵐ x ∂μ, distinctExp lam0 d ⊆ lyapunovSpectrum A T x) :
    ∀ᵐ x ∂μ, ∃ h : specCard A T x = numExp lam0 d,
      ∀ i : Fin (specCard A T x), specList A T x i = expEnum lam0 d (Fin.cast h i) :=
  specList_eq_expEnum_of_subsets_ae A lam0 hub_spec hlb_spec

end ErgodicTheory
