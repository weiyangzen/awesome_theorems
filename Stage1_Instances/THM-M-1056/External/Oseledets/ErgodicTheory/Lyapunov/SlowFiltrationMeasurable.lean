/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.FiltrationInterfaceReduction
import ErgodicTheory.Lyapunov.SpectralMeasurable

/-!
# The everywhere-measurable slow filtration `vprime` and the identification `hae`

This module provides the `vprime`/`hmeas'`/`hae` inputs of
`ErgodicTheory.oseledets_filtration_of_interfaces'`.

## Main results

* `slowCutoff`, `vprime` — the explicit deterministic-cutoff slow family.
* `measurableSubspace_vprime` — `MeasurableSubspace` for every level, with no a.e. hypothesis.
* `vprime_eq_vassembled_of_slowflag` — `hae` from `hslowflag` and `hspec`.

## Implementation notes

### The construction

`vprime` is the deterministic-index reindexing of the **slow spectral filtration** `vslow`:
for an index `i : Fin (numExp lam0 d + 1)`,

* on the interior `(i : ℕ) < numExp lam0 d` it is `vslow` at the deterministic cutoff
  `slowCutoff lam0 d i := expEnum lam0 d ⟨i, _⟩` (the `i`-th descending exponent), the natural
  threshold matching the `i`-th `vflag` stratum (whose level is `lambdaSublevel … (specList i)`
  and, under the ergodic identification `specList = expEnum`, that is exactly `expEnum lam0 d i`);
* at the last index `i = numExp lam0 d` it is the everywhere-`⊥` family.

`vprime` is built only from `vslow`, which is everywhere-defined and everywhere-measurable, so
`hmeas' : ∀ i, MeasurableSubspace (vprime i)` carries no a.e. hypothesis (it uses only
`measurableSubspace_vslow` fed `measurable_slowProjector`).

### The identification `hae` (`vslow = vflag` a.e. levelwise)

The content `vprime i x = vassembled A T (numExp lam0 d) i x` a.e. is the levelwise
identification of the slow spectral filtration with the limsup flag.  It factors through the
single a.e. hypothesis

  `hslowflag : ∀ᵐ x, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t`

— the per-point identification of the slow band's range with the `lambdaBar`-sublevel, **with the
exponential change of scale**: `vslow`'s threshold cuts the spectrum of the limit matrix
`Λ = lim (Qₙ)^{1/2n}` whose eigenvalues are `e^{λᵢ}` (exp scale), while `lambdaSublevel`'s
threshold cuts the growth function `lambdaBar` whose values are the exponents `λᵢ` themselves
(log scale).  This `hslowflag` packages the two inclusions:

* `lambdaSublevel ⊆ vslow` — the *growth-slowness ⟹ membership in the Λ-slow space*
  direction (via `overlap_limsup_le_of_slow_growth` / `limsup_log_norm_cocycle_eq_lambdaBar`);
* `vslow ⊆ lambdaSublevel` — the per-vector **spectral upper bound** (`v` in the Λ-slow space at
  level `e^t` ⟹ `lambdaBar v ≤ t`), following Ruelle's Prop. 1.3.

A `vslow (exp t) = lambdaSublevel t` lemma discharges `hslowflag` verbatim, and `hae`
follows from it together with the deterministic `vassembled` cast bookkeeping and the ergodic
`hspec` alignment (the same `hspec` interface consumed by the assembly).
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]

/-! ## The deterministic slow cutoffs and the family `vprime` -/

/-- **Deterministic slow cutoff.**  For an index `i : Fin (numExp lam0 d + 1)`, the threshold at
which to take the slow band: on the interior `(i : ℕ) < numExp lam0 d` it is the `i`-th descending
exponent `expEnum lam0 d ⟨i, _⟩`; at the last index it is an (irrelevant) junk value `0`. -/
noncomputable def slowCutoff (lam0 : ℕ → ℝ) (d : ℕ) (i : Fin (numExp lam0 d + 1)) : ℝ :=
  if h : (i : ℕ) < numExp lam0 d then expEnum lam0 d ⟨i, h⟩ else 0

/-- **The everywhere-measurable slow filtration `vprime`.**  Built solely from the slow spectral
filtration `vslow` (interior levels) and the everywhere-`⊥` family (last level), so it is
everywhere-defined and everywhere-measurable. -/
noncomputable def vprime (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (lam0 : ℕ → ℝ)
    (i : Fin (numExp lam0 d + 1)) (x : X) : Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
  if (i : ℕ) < numExp lam0 d then vslow A T (Real.exp (slowCutoff lam0 d i)) x else ⊥

/-! ## `hmeas'` — measurability of every level -/

/-- **Measurability of every level of `vprime`.**  Each level is a `MeasurableSubspace`.  Interior
levels are `vslow` at a fixed cutoff (measurable via `measurableSubspace_vslow` fed
`measurable_slowProjector`); the last level is the constant `⊥`, trivially a `MeasurableSubspace`.

This carries no a.e. hypothesis — only the measurability of `A` and `T`, as the slow-projector
measurability bridge requires. -/
theorem measurableSubspace_vprime (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    (hAmeas : Measurable A) (hTmeas : Measurable T) (lam0 : ℕ → ℝ) :
    ∀ i : Fin (numExp lam0 d + 1), MeasurableSubspace (fun x => vprime A T lam0 i x) := by
  intro i
  unfold vprime
  by_cases h : (i : ℕ) < numExp lam0 d
  · simp only [if_pos h]
    exact measurableSubspace_vslow A T (Real.exp (slowCutoff lam0 d i))
      (measurable_slowProjector A T (Real.exp (slowCutoff lam0 d i)) hAmeas hTmeas)
  · simp only [if_neg h]
    -- the constant `⊥` family is a `MeasurableSubspace`: its projection matrix is constant.
    exact measurable_const

/-! ## `hae` — the levelwise identification `vprime = vassembled` a.e.

The only non-spectral input is `hslowflag`: the per-point identification of the slow band range
with the `lambdaBar`-sublevel at the same real threshold.  Given it, `hae` is pure `vassembled`/cast
bookkeeping against the ergodic `hspec` interface. -/

omit [NeZero d] in
/-- **`hae` from the slow-flag identification.**  Under

* `hspec` — the ergodic spectrum-constancy interface consumed by the assembly
  (`specCard = numExp` and `specList = expEnum` along the cast, a.e.); and
* `hslowflag` — the per-point identification
  `vslow A T (Real.exp t) x = lambdaSublevel A T x t` for all
  thresholds `t`, a.e. `x`,

the deterministic-cutoff slow family `vprime` agrees, a.e. and levelwise, with the assembled
family `vassembled A T (numExp lam0 d)`.  This is exactly the `hae` input of
`oseledets_filtration_of_interfaces'`. -/
theorem vprime_eq_vassembled_of_slowflag
    {μ : Measure X} {T : X → X} (A : X → Matrix (Fin d) (Fin d) ℝ) (lam0 : ℕ → ℝ)
    (hspec : ∀ᵐ x ∂μ, ∃ h : specCard A T x = numExp lam0 d,
      ∀ i : Fin (specCard A T x), specList A T x i = expEnum lam0 d (Fin.cast h i))
    (hslowflag : ∀ᵐ x ∂μ, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t) :
    ∀ᵐ x ∂μ, ∀ i, vprime A T lam0 i x = vassembled A T (numExp lam0 d) i x := by
  filter_upwards [hspec, hslowflag] with x hspecx hflagx
  obtain ⟨hcard, hlist⟩ := hspecx
  intro i
  -- Unfold `vassembled` through the cardinality equality.
  rw [vassembled, dif_pos hcard]
  unfold vprime
  by_cases hi : (i : ℕ) < numExp lam0 d
  · -- Interior level: both sides are the sublevel at `expEnum lam0 d ⟨i,_⟩`.
    simp only [if_pos hi]
    -- The cast index `i' : Fin (specCard A T x + 1)` has the same `val` and is interior.
    set i' : Fin (specCard A T x + 1) :=
      Fin.cast (by rw [hcard] : numExp lam0 d + 1 = specCard A T x + 1) i with hi'
    have hi'val : (i' : ℕ) = (i : ℕ) := by simp [hi']
    have hi'lt : (i' : ℕ) < specCard A T x := by rw [hi'val, hcard]; exact hi
    -- RHS: `vflag … i' = lambdaSublevel … (specList … ⟨i', hi'lt⟩)`.
    rw [vflag_of_lt hi'lt]
    -- LHS: `vslow … (slowCutoff …) = lambdaSublevel … (slowCutoff …)` by `hflagx`.
    rw [hflagx (slowCutoff lam0 d i)]
    -- Both thresholds equal `expEnum lam0 d ⟨i, hi⟩`.
    have hcut : slowCutoff lam0 d i = expEnum lam0 d ⟨i, hi⟩ := by
      rw [slowCutoff, dif_pos hi]
    have hspeclist : specList A T x ⟨i', hi'lt⟩ = expEnum lam0 d ⟨i, hi⟩ := by
      rw [hlist ⟨i', hi'lt⟩]
      exact congrArg (expEnum lam0 d) (Fin.ext (by simp [hi'val]))
    rw [hcut, hspeclist]
  · -- Last level: both sides are `⊥`.
    simp only [if_neg hi]
    set i' : Fin (specCard A T x + 1) :=
      Fin.cast (by rw [hcard] : numExp lam0 d + 1 = specCard A T x + 1) i with hi'
    have hi'val : (i' : ℕ) = (i : ℕ) := by simp [hi']
    have hi'ge : ¬ (i' : ℕ) < specCard A T x := by rw [hi'val, hcard]; exact hi
    rw [vflag, dif_neg hi'ge]

/-! ## The end-to-end application

Feeding `vprime`, `measurableSubspace_vprime`, and `vprime_eq_vassembled_of_slowflag` into
`oseledets_filtration_of_interfaces'` discharges its `vprime`/`hmeas'`/`hae` arguments. -/

/-- **End-to-end application.**  The theorem `oseledets_filtration_of_interfaces'` with its
`vprime`/`hmeas'`/`hae` arguments supplied by `vprime`, `measurableSubspace_vprime`, and
`vprime_eq_vassembled_of_slowflag`.  The remaining hypotheses are those the assembly needs,
together with the single datum `hslowflag`. -/
theorem oseledets_filtration_of_slowflag
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hTmeas : Measurable T)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hspec : ∀ᵐ x ∂μ, ∃ h : specCard A T x = numExp lam0 d,
      ∀ i : Fin (specCard A T x), specList A T x i = expEnum lam0 d (Fin.cast h i))
    (hslowflag : ∀ᵐ x ∂μ, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t)
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
          Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x) = V i (T x)) ∧
        (∀ i : Fin k, ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))),
            v ∉ V i.succ x →
            Tendsto
              (fun n : ℕ => (n : ℝ)⁻¹ *
                Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
              atTop (𝓝 (lam i))) :=
  oseledets_filtration_of_interfaces' hT A hA hAmeas hint hint' lam0 hspec
    (vprime A T lam0) (measurableSubspace_vprime A T hAmeas hTmeas lam0)
    (vprime_eq_vassembled_of_slowflag A lam0 hspec hslowflag) hgrowth

end ErgodicTheory
