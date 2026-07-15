/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.ForwardMeasurable
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit

/-!
# The measurable Λ-spectral filtration `V`

This module constructs the **measurable spectral filtration** of the Oseledets limit operator
`Λ x = oseledetsLimit A T x` and discharges its global measurability through the
projector/range bridge `measurableSubspace_range_of_measurable`
(`ErgodicTheory/Lyapunov/ForwardMeasurable.lean`).

## Main results

* `lambdaHat` — the sanitized, everywhere-self-adjoint Oseledets limit.
* `measurableSet_isHermitian_oseledetsLimit` — the Hermitian set is measurable.
* `measurable_lambdaHat`, `lambdaHat_isSelfAdjoint` — sanitization is measurable and self-adjoint.
* `slowProjector_isSelfAdjoint`, `slowProjector_mul_self` — the indicator-CFC is, for every `x`, a
  self-adjoint idempotent (a genuine orthogonal projector).
* `vslow` — the spectral sublevel filtration `t ↦ x ↦ range (toEuclideanCLM (slowProjector t x))`.
* `measurableSubspace_vslow_of_measurable_slowProjector` — the bridge application: `vslow t` is a
  `MeasurableSubspace` once `x ↦ slowProjector t x` is measurable.
* `measurableSubspace_vslow` — measurability of the filtration, given measurability of the
  indicator-CFC family (`measurable_slowProjector`).

## Implementation notes

The projector/range bridge consumes a measurable family of **self-adjoint idempotent** matrices
`P x`, and requires those two algebraic facts to hold *globally* (for every `x`), not merely
almost everywhere. Two obstructions are resolved here, and the residual measurability obligation
is taken as a hypothesis.

### Everywhere a genuine projector

1. **`Λ` need not be self-adjoint off the a.e.-full convergence set.** The named limit
   `oseledetsLimit A T x` is only known to be Hermitian almost everywhere. It is **sanitized** to a
   genuinely-everywhere-self-adjoint matrix `lambdaHat A T x`, equal to `Λ x` on the (measurable)
   Hermitian set and to the (self-adjoint) identity off it. Measurability is preserved because the
   Hermitian set is the equalizer of two measurable matrix-valued maps.

2. **A *continuous* gap function does not give an idempotent CFC.** For a genuine orthogonal
   projector the `0/1`-valued **indicator** `Set.indicator (Set.Iic t) 1` is used: being
   `0/1`-valued it satisfies `g² = g` on *any* finite spectrum, so `cfc g (lambdaHat A T x)` is
   self-adjoint (`cfc_predicate`) and idempotent (`cfc_mul` + `cfc_congr`) for **every** `x`.

### Indicator-CFC measurability

The remaining genuine obligation is `Measurable (fun x => slowProjector t x)`, i.e. measurability of
`x ↦ cfc (Set.indicator (Set.Iic t) 1) (lambdaHat A T x)`. The indicator is **discontinuous**, so
the continuous-CFC measurability crux `measurable_cfc_continuous` does not apply, and the polynomial
bypass `measurable_cfc_eqOn_polynomial` would need a *single* polynomial agreeing with the indicator
on the spectrum of *every* `lambdaHat A T x` — which requires global control of the spectra that is
not available here. This module therefore takes that measurability as an explicit hypothesis
(`measurable_slowProjector`) and discharges everything else: the sanitization and its properties,
the everywhere self-adjointness and idempotence of the indicator-CFC, and the bridge application
reduced to exactly that one measurability goal.
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix

namespace ErgodicTheory

variable {X : Type*} {T : X → X} {d : ℕ}

/-! ### Step 1 — sanitize `Λ` to be self-adjoint everywhere -/

/-- **Sanitized Oseledets limit.**  Equal to `oseledetsLimit A T x` on the Hermitian set and to the
identity matrix off it.  This is genuinely (everywhere) self-adjoint, while remaining measurable and
agreeing with the named limit `Λ` wherever the latter is Hermitian (in particular a.e.). -/
noncomputable def lambdaHat (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) :
    Matrix (Fin d) (Fin d) ℝ :=
  if (oseledetsLimit A T x).IsHermitian then oseledetsLimit A T x else 1

/-- The conjugate-transpose of a measurable matrix family is measurable (entrywise the `star` of a
transposed measurable entry; over `ℝ`, `star = id`). -/
theorem measurable_conjTranspose [MeasurableSpace X] [NeZero d]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hAmeas : Measurable A) (hTmeas : Measurable T) :
    Measurable (fun x ↦ (oseledetsLimit A T x)ᴴ) := by
  have hΛ : Measurable (oseledetsLimit A T) := measurable_oseledetsLimit hAmeas hTmeas
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  simp only [Matrix.conjTranspose_apply, star_trivial]
  exact (measurable_pi_apply i).comp ((measurable_pi_apply j).comp hΛ)

/-- **The Hermitian set is measurable.**  `{x | (oseledetsLimit A T x).IsHermitian}` is the
equalizer `{x | (Λ x)ᴴ = Λ x}` of the two measurable matrix-valued maps `x ↦ (Λ x)ᴴ` and
`x ↦ Λ x`; equalizers of measurable maps into a metrizable space are measurable
(`measurableSet_eq_fun`). -/
theorem measurableSet_isHermitian_oseledetsLimit [MeasurableSpace X] [NeZero d]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hAmeas : Measurable A) (hTmeas : Measurable T) :
    MeasurableSet {x | (oseledetsLimit A T x).IsHermitian} := by
  have hΛ : Measurable (oseledetsLimit A T) := measurable_oseledetsLimit hAmeas hTmeas
  have hentry : ∀ i j : Fin d, Measurable fun x => oseledetsLimit A T x i j := fun i j =>
    (measurable_pi_apply j).comp ((measurable_pi_apply i).comp hΛ)
  -- `(Λ x)ᴴ = Λ x` ⟺ `∀ i j, Λ x j i = Λ x i j` (over `ℝ`, `star = id`), a countable
  -- intersection of equalizers of measurable real functions.
  have hset : {x | (oseledetsLimit A T x).IsHermitian}
      = ⋂ i : Fin d, ⋂ j : Fin d,
          {x | oseledetsLimit A T x j i = oseledetsLimit A T x i j} := by
    ext x
    simp only [Set.mem_iInter, Set.mem_setOf_eq]
    constructor
    · intro h i j
      have := congrFun (congrFun h i) j
      simpa only [Matrix.conjTranspose_apply, star_trivial] using this
    · intro h
      refine Matrix.IsHermitian.ext fun i j => ?_
      simpa only [star_trivial] using h i j
  rw [hset]
  refine MeasurableSet.iInter fun i => MeasurableSet.iInter fun j => ?_
  exact measurableSet_eq_fun (hentry j i) (hentry i j)

/-- **Sanitization is measurable.**  `lambdaHat A T` is a measurable family: it is the piecewise
combination of two measurable matrix maps (`Λ` and the constant `1`) over the measurable Hermitian
set. -/
theorem measurable_lambdaHat [MeasurableSpace X] [NeZero d]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hAmeas : Measurable A) (hTmeas : Measurable T) :
    Measurable (lambdaHat A T) := by
  have hΛ : Measurable (oseledetsLimit A T) := measurable_oseledetsLimit hAmeas hTmeas
  have hset : MeasurableSet {x | (oseledetsLimit A T x).IsHermitian} :=
    measurableSet_isHermitian_oseledetsLimit hAmeas hTmeas
  exact hΛ.piecewise hset measurable_const

/-- **Sanitization is everywhere self-adjoint.**  On the Hermitian set `lambdaHat A T x = Λ x` is
self-adjoint (`Matrix.isHermitian_iff_isSelfAdjoint`); off it `lambdaHat A T x = 1` is self-adjoint
(`isSelfAdjoint_one`). -/
theorem lambdaHat_isSelfAdjoint (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) :
    IsSelfAdjoint (lambdaHat A T x) := by
  unfold lambdaHat
  by_cases h : (oseledetsLimit A T x).IsHermitian
  · rw [if_pos h]; exact (Matrix.isHermitian_iff_isSelfAdjoint).mp h
  · rw [if_neg h]; exact IsSelfAdjoint.one _

/-! ### Step 2 — the indicator-CFC is everywhere a genuine projector -/

/-- **Slow (sublevel) band projector.**  The continuous functional calculus of the `0/1`-valued
indicator of `(-∞, t]` applied to the sanitized limit `lambdaHat A T x`.  Being a CFC of a
real-valued function it is self-adjoint for every `x`, and being cut by a `0/1`-valued indicator it
is idempotent for every `x` — a genuine orthogonal projector at *every* point. -/
noncomputable def slowProjector (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (t : ℝ) (x : X) :
    Matrix (Fin d) (Fin d) ℝ :=
  cfc (Set.indicator (Set.Iic t) (1 : ℝ → ℝ)) (lambdaHat A T x)

/-- **The slow projector is self-adjoint for every `x`** (a CFC of a real-valued function is always
self-adjoint). -/
theorem slowProjector_isSelfAdjoint (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (t : ℝ) (x : X) :
    IsSelfAdjoint (slowProjector A T t x) :=
  cfc_predicate _ _

/-- **The slow projector is idempotent for every `x`.**  The `0/1`-valued indicator satisfies
`g² = g` on *any* set, in particular on the (finite) spectrum of `lambdaHat A T x`; the continuity
hypothesis of `cfc_mul` holds since any function is continuous on the finite spectrum.  Hence
`cfc g (lambdaHat …)` is idempotent, a genuine orthogonal projector at every point. -/
theorem slowProjector_mul_self (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (t : ℝ) (x : X) :
    slowProjector A T t x * slowProjector A T t x = slowProjector A T t x := by
  -- On any set the `0/1`-valued indicator satisfies `g² = g`.
  have hidem : (_root_.spectrum ℝ (lambdaHat A T x)).EqOn
      (fun s => Set.indicator (Set.Iic t) (1 : ℝ → ℝ) s * Set.indicator (Set.Iic t) (1 : ℝ → ℝ) s)
      (Set.indicator (Set.Iic t) (1 : ℝ → ℝ)) := by
    intro s _
    by_cases hs : s ∈ Set.Iic t
    · simp [Set.indicator_of_mem hs]
    · simp [Set.indicator_of_notMem hs]
  -- Any function is continuous on the (finite) spectrum.
  have hcont : ContinuousOn (Set.indicator (Set.Iic t) (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (lambdaHat A T x)) :=
    (Matrix.finite_real_spectrum (A := lambdaHat A T x)).continuousOn _
  rw [slowProjector, ← cfc_mul _ _ _ hcont hcont, cfc_congr hidem]

/-! ### Step 3 — the spectral filtration and the bridge application -/

/-- **The slow (sublevel) spectral filtration.**  For each cutoff `t`, the family of range
subspaces of the slow band projector.  By construction `slowProjector A T t x` is, for every `x`, a
self-adjoint idempotent matrix, so `range (toEuclideanCLM (slowProjector …))` is exactly the kind of
family the projector/range bridge consumes. -/
noncomputable def vslow (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (t : ℝ) (x : X) :
    Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
  LinearMap.range (Matrix.toEuclideanCLM (𝕜 := ℝ) (slowProjector A T t x)).toLinearMap

/-- **The bridge application (reduced to the one measurability goal).**  Given measurability of the
indicator-CFC family `x ↦ slowProjector A T t x`, the spectral filtration `vslow A T t` is a
`MeasurableSubspace`.  The two algebraic hypotheses of the bridge
(`measurableSubspace_range_of_measurable`) — self-adjointness and idempotence *everywhere* — are the
discharged `slowProjector_isSelfAdjoint` and `slowProjector_mul_self`. -/
theorem measurableSubspace_vslow_of_measurable_slowProjector [MeasurableSpace X]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (t : ℝ)
    (hP : Measurable (fun x ↦ slowProjector A T t x)) :
    MeasurableSubspace (fun x ↦ vslow A T t x) :=
  measurableSubspace_range_of_measurable (fun x ↦ slowProjector A T t x) hP
    (fun x ↦ slowProjector_isSelfAdjoint A T t x)
    (fun x ↦ slowProjector_mul_self A T t x)

/-- **Measurability of the slow spectral filtration.**  Under the single isolated measurability
hypothesis on the indicator-CFC family, `vslow A T t` is a `MeasurableSubspace`: the
sanitization, the everywhere self-adjointness and idempotence of the slow projector, and the
projector/range bridge reduce the measurability of the filtration to exactly this hypothesis. -/
theorem measurableSubspace_vslow [MeasurableSpace X]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (t : ℝ)
    (measurable_slowProjector : Measurable (fun x ↦ slowProjector A T t x)) :
    MeasurableSubspace (fun x ↦ vslow A T t x) :=
  measurableSubspace_vslow_of_measurable_slowProjector A T t measurable_slowProjector

end ErgodicTheory
