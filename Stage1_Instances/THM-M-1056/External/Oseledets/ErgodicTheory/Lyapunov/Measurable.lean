/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.Filtration
import ErgodicTheory.Lyapunov.MeasurableSubspace
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Lp.MeasurableSpace
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order
import Mathlib.MeasureTheory.Constructions.BorelSpace.Metrizable
import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Continuity
import Mathlib.LinearAlgebra.Matrix.Polynomial
import Mathlib.Topology.ContinuousMap.Weierstrass

/-!
# Measurability infrastructure for the Lyapunov filtration

This module develops the measurability tools for the Oseledets flag. The measurability of the
flag is established **through the concrete continuous-functional-calculus spectral projections
of the Oseledets limit operator** `Λ x = lim_n ((A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾)^{1/(2n)}`, rather than through
a measurable selection of an orthonormal frame for the abstract sublevel subspace (which would
require a Kuratowski–Ryll-Nardzewski selection theorem).

Defining the `i`-th flag projection as the CFC element `Pᵢ x := cfc gᵢ (Λ x)` (with `gᵢ` a
continuous gap function) makes `orthProjMatrix (range (toEuclideanCLM (Pᵢ x))) = Pᵢ x`
definitionally — a self-adjoint idempotent equals the orthogonal projection onto its range — so
`MeasurableSubspace` reduces to measurability of `x ↦ cfc gᵢ (Λ x)`.

## Main results

* `ErgodicTheory.measurable_lambdaBar_apply` — for fixed `v`, `x ↦ lambdaBar A T x v` is measurable
  (the scalar measurability used by the later arguments).
* `ErgodicTheory.orthProjMatrix_apply` / `ErgodicTheory.measurable_orthProjMatrix_iff` —
  the projection
  matrix's entry formula and the resulting reduction of matrix measurability to projecting the
  fixed standard basis vectors.
* `ErgodicTheory.instMeasurableAdd₂Matrix`, `ErgodicTheory.measurable_matrix_pow`,
  `ErgodicTheory.measurable_aeval_matrix` — matrix-algebra measurability (a polynomial in a
  measurable matrix is measurable).
* `ErgodicTheory.measurable_cfc_eqOn_polynomial` — if a fixed polynomial `q` agrees with `g` on the
  spectrum of every (self-adjoint) `M x`, then `x ↦ cfc g (M x)` is measurable. This polynomial
  bypass uses only the bare Hermitian CFC instance, not the (absent for real matrices)
  `IsometricContinuousFunctionalCalculus`.
* `ErgodicTheory.measurable_cfc_continuous` — for a continuous `f` and a measurable family of
  self-adjoint matrices `M`, `x ↦ cfc f (M x)` is measurable, via a per-point Weierstrass
  approximation.

The terminal `MeasurableSubspace` lemma for the concrete flag is assembled once the Oseledets
limit `Λ` is available (in `ErgodicTheory.Lyapunov.OseledetsLimit`), since it needs `Measurable Λ`
and the fixed Lyapunov spectrum on which the gap function is interpolated by a polynomial.
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix.Norms.L2Operator RealInnerProductSpace

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {μ : Measure X} {T : X → X} {d : ℕ}

/- The measurable and Borel structures on `EuclideanSpace ℝ (Fin d)` used by the
`EuclideanSpace`-valued measurable maps below are Mathlib's **canonical** ones,
`WithLp.measurableSpace` and `PiLp.borelSpace` (from `Mathlib.Analysis.Normed.Lp.MeasurableSpace`,
imported above).

Historically this module declared its own `MeasurableSpace (EuclideanSpace ℝ (Fin d)) := borel _`
(with the `BorelSpace` witness `⟨rfl⟩`). That term is only *propositionally* — not syntactically —
equal to Mathlib's `WithLp.measurableSpace` (which is `MeasurableSpace.comap ofLp inferInstance`);
their agreement is exactly the content of `PiLp.borelSpace`. Since some downstream modules also
import Mathlib measure-theory files that transitively provide `WithLp.measurableSpace`, keeping the
local `borel _` instance created a genuine (propositional-not-syntactic) instance diamond on this
type. We therefore use Mathlib's single canonical instance everywhere, which removes the diamond at
its root: `MeasurableSpace`/`BorelSpace` typeclass resolution can no longer land on two distinct
terms in mixed contexts. All the Borel-measurability lemmas used below only need
`BorelSpace (EuclideanSpace ℝ (Fin d))`, which `PiLp.borelSpace` supplies. -/

/-! ### Scalar measurability -/

/-- For a fixed vector `v`, the upper Lyapunov growth `x ↦ lambdaBar A T x v` is measurable: it is
the `limsup` of the measurable sequence `x ↦ n⁻¹ · log ‖toEuclideanCLM (cocycle A T n x) v‖`. -/
theorem measurable_lambdaBar_apply [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hAmeas : Measurable A)
    (v : EuclideanSpace ℝ (Fin d)) :
    Measurable fun x => lambdaBar A T x v := by
  have hTmeas : Measurable T := hT.toMeasurePreserving.measurable
  -- `lambdaBar A T x v = limsup_n (fun n => n⁻¹ · log ‖toEuclideanCLM (cocycle A T n x) v‖)`.
  refine Measurable.limsup (fun n => ?_)
  -- Each term is measurable: `cocycle` is measurable in `x`, and
  -- `M ↦ log ‖toEuclideanCLM M v‖` is continuous in the matrix `M`.
  have hcoc : Measurable fun x => cocycle A T n x := measurable_cocycle hAmeas hTmeas n
  -- `M ↦ ‖toEuclideanCLM M v‖` is continuous in `M`.
  have hcontNorm : Continuous fun M : Matrix (Fin d) (Fin d) ℝ =>
      ‖Matrix.toEuclideanCLM (𝕜 := ℝ) M v‖ := by
    -- `M ↦ toEuclideanCLM M v` is ℝ-linear in `M`, hence continuous (finite dimensional).
    have hlin : Continuous fun M : Matrix (Fin d) (Fin d) ℝ =>
        Matrix.toEuclideanCLM (𝕜 := ℝ) M v := by
      let L : Matrix (Fin d) (Fin d) ℝ →ₗ[ℝ] EuclideanSpace ℝ (Fin d) :=
        { toFun := fun M => Matrix.toEuclideanCLM (𝕜 := ℝ) M v
          map_add' := fun M N => by simp [map_add]
          map_smul' := fun c M => by simp [map_smul] }
      exact (L.continuous_of_finiteDimensional)
    exact continuous_norm.comp hlin
  have hnorm : Measurable fun x =>
      ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖ :=
    hcontNorm.measurable.comp hcoc
  have hlog : Measurable fun x =>
      Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖ :=
    Real.measurable_log.comp hnorm
  exact measurable_const.mul hlog

/-! ### The projection-matrix entry formula and reduction -/

/-- **Entry formula for the projection matrix.** The `(i, j)` entry of `orthProjMatrix K`
equals the `i`-th coordinate of the orthogonal projection `K.starProjection` applied to the
standard basis vector `EuclideanSpace.single j 1`. -/
theorem orthProjMatrix_apply (K : Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (i j : Fin d) :
    orthProjMatrix K i j = K.starProjection (EuclideanSpace.single j (1 : ℝ)) i := by
  -- `M := orthProjMatrix K` satisfies `toEuclideanCLM M = K.starProjection`.
  have hM : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) = K.starProjection := by
    rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
  -- Apply both sides to `single j 1` and read coordinate `i`.
  have hcongr := congrArg
    (fun L : EuclideanSpace ℝ (Fin d) →L[ℝ] EuclideanSpace ℝ (Fin d) =>
      (L (EuclideanSpace.single j (1 : ℝ))) i) hM
  simp only at hcongr
  rw [← hcongr]
  -- LHS: `(toEuclideanCLM M (single j 1)) i = (M *ᵥ Pi.single j 1) i = M i j`.
  have hofLp : (Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K)
      (EuclideanSpace.single j (1 : ℝ))) i
      = ((orthProjMatrix K) *ᵥ (WithLp.ofLp (EuclideanSpace.single j (1 : ℝ)))) i := by
    rw [← Matrix.ofLp_toEuclideanCLM]
  rw [hofLp, show WithLp.ofLp (EuclideanSpace.single j (1 : ℝ)) = Pi.single j (1 : ℝ) from rfl,
    Matrix.mulVec_single_one]
  simp [Matrix.col_apply]

/-- **The reduction.** `x ↦ orthProjMatrix (V x)` is measurable iff for every standard basis
index `j`, the `EuclideanSpace`-valued map `x ↦ (V x).starProjection (single j 1)` is
measurable. -/
theorem measurable_orthProjMatrix_iff
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} :
    (Measurable fun x => orthProjMatrix (V x)) ↔
      ∀ j : Fin d, Measurable fun x => (V x).starProjection (EuclideanSpace.single j (1 : ℝ)) := by
  constructor
  · intro hmeas j
    -- Each coordinate `i` of `x ↦ starProjection (single j 1)` equals entry `(i, j)` of the
    -- matrix, hence is measurable; the map into `Fin d → ℝ` is then measurable, and post-
    -- composing with the continuous `toLp : (Fin d → ℝ) → EuclideanSpace` recovers it.
    have hpi : Measurable fun x =>
        WithLp.ofLp ((V x).starProjection (EuclideanSpace.single j (1 : ℝ))) := by
      refine measurable_pi_iff.2 fun i => ?_
      have hentry : Measurable fun x => orthProjMatrix (V x) i j :=
        (measurable_pi_apply j).comp ((measurable_pi_apply i).comp hmeas)
      have : (fun x => WithLp.ofLp ((V x).starProjection (EuclideanSpace.single j (1 : ℝ))) i)
          = fun x => orthProjMatrix (V x) i j := by
        funext x; rw [orthProjMatrix_apply]
      rw [this]; exact hentry
    -- `starProjection (single j 1) = toLp (ofLp (starProjection (single j 1)))`.
    have hcont : Continuous (WithLp.toLp 2 : (Fin d → ℝ) → EuclideanSpace ℝ (Fin d)) :=
      PiLp.continuous_toLp 2 (fun _ : Fin d => ℝ)
    have := (hcont.measurable).comp hpi
    simpa only [WithLp.toLp_ofLp] using this
  · intro hcol
    -- assemble the matrix entrywise: entry `(i, j)` is coordinate `i` of column `j`.
    refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
    simp only [orthProjMatrix_apply]
    have hcoord : Continuous fun w : EuclideanSpace ℝ (Fin d) => w i :=
      PiLp.continuous_apply (β := fun _ : Fin d => ℝ) 2 i
    exact hcoord.measurable.comp (hcol j)

/-! ### Matrix-algebra measurability (a polynomial in a measurable matrix is measurable) -/

/-- Matrix addition is measurable in both arguments (entrywise Pi addition); the additive
counterpart of `ErgodicTheory.instMeasurableMul₂Matrix`. -/
instance instMeasurableAdd₂Matrix {m α : Type*} [MeasurableSpace α]
    [Add α] [MeasurableAdd₂ α] : MeasurableAdd₂ (Matrix m m α) := by
  have hentry : ∀ i j : m, Measurable fun M : Matrix m m α => M i j := fun i j =>
    (measurable_pi_apply j).comp (measurable_pi_apply i)
  refine ⟨measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_⟩
  simp only [Matrix.add_apply]
  exact ((hentry i j).comp measurable_fst).add ((hentry i j).comp measurable_snd)

/-- `a ↦ a ^ n` is measurable in the matrix `a` (iterated measurable multiplication). -/
theorem measurable_matrix_pow (n : ℕ) :
    Measurable (fun a : Matrix (Fin d) (Fin d) ℝ => a ^ n) := by
  induction n with
  | zero => simp only [pow_zero]; exact measurable_const
  | succ k ih => simpa [pow_succ] using ih.mul measurable_id

/-- `a ↦ aeval a q` is measurable in the matrix `a`: a polynomial built from `+`, `•`, `*` of the
(measurable) identity, using the matrix `MeasurableMul₂`/`MeasurableAdd₂` instances. -/
theorem measurable_aeval_matrix (q : Polynomial ℝ) :
    Measurable (fun a : Matrix (Fin d) (Fin d) ℝ => (Polynomial.aeval a) q) := by
  induction q using Polynomial.induction_on with
  | C r => simp only [Polynomial.aeval_C]; exact measurable_const
  | add p q hp hq => simpa [map_add] using hp.add hq
  | monomial n r _ =>
      have : (fun a : Matrix (Fin d) (Fin d) ℝ =>
            (Polynomial.aeval a) (Polynomial.C r * Polynomial.X ^ (n + 1)))
          = fun a => algebraMap ℝ (Matrix (Fin d) (Fin d) ℝ) r * a ^ (n + 1) := by
        funext a
        rw [map_mul, Polynomial.aeval_C, map_pow, Polynomial.aeval_X]
      rw [this]
      exact (measurable_matrix_pow (n + 1)).const_mul _

/-! ### Measurability of the CFC via a fixed interpolating polynomial -/

/-- **The CFC polynomial bypass.** Let `M : X → Matrix (Fin d) (Fin d) ℝ` be measurable with each
`M x` self-adjoint (Hermitian). Suppose a *fixed* polynomial `q` agrees with `g : ℝ → ℝ` on the
spectrum of every `M x`. Then `x ↦ cfc g (M x)` is measurable.

This is the situation in the intended application: `M x = Λ x` (the a.e.-existing Oseledets limit
matrix, measurable as a limit of measurable matrices), `g = gᵢ` the continuous gap function, and
on the a.e. good set the spectrum is the fixed gapped Lyapunov set, on which `gᵢ` equals an
interpolating polynomial `q`. It uses only the bare Hermitian CFC instance — no
`IsometricContinuousFunctionalCalculus` (which does not synthesize for real matrices), no
`continuousOn_cfc`, no measurable selection, no analytic sets. -/
theorem measurable_cfc_eqOn_polynomial
    (g : ℝ → ℝ) (q : Polynomial ℝ)
    (M : X → Matrix (Fin d) (Fin d) ℝ)
    (hM : Measurable M)
    (hMsa : ∀ x, IsSelfAdjoint (M x))
    (hagree : ∀ x, (_root_.spectrum ℝ (M x)).EqOn g q.eval) :
    Measurable (fun x => cfc g (M x)) := by
  have hpt : ∀ x, cfc g (M x) = (Polynomial.aeval (M x)) q := by
    intro x
    rw [cfc_congr (a := M x) (f := g) (g := q.eval) (hagree x), cfc_polynomial q (M x) (hMsa x)]
  simp only [hpt]
  exact (measurable_aeval_matrix q).comp hM

/-! ### Measurability of the CFC for a *continuous* function (Weierstrass bypass)

The polynomial bypass `measurable_cfc_eqOn_polynomial` needs a single polynomial agreeing with `g`
on the spectrum of *every* `M x`. For the Oseledets root `t ↦ t^{1/(2n)}` the spectra (the squared
singular values) range over an unbounded family, so no single polynomial works globally. The
remedy is a **per-point** Weierstrass approximation: for each `k` pick a polynomial `qₖ` agreeing
with `g` to within `1/(k+1)` on the compact interval `[-k, k]`. For a fixed `x` the (finite)
spectrum of `M x` lies in some `[-R, R]`, so `qₖ → g` uniformly on `spectrum (M x)`, whence
`cfc qₖ (M x) → cfc g (M x)` by `tendsto_cfc_fun`. Each `x ↦ cfc qₖ (M x) = aeval (M x) qₖ` is
measurable, and matrix-entrywise `measurable_of_tendsto_metrizable` upgrades the pointwise limit to
measurability of `x ↦ cfc g (M x)`. This needs only the bare Hermitian CFC instance (the generic
`tendsto_cfc_fun`, not the absent-for-real-matrices isometric CFC). -/

/-- **Weierstrass polynomial approximation on `[-k, k]`.** For a continuous `f : ℝ → ℝ` and each
`k : ℕ` there is a polynomial `q` with `|q(t) − f(t)| ≤ 1/(k+1)` on `[-k, k]`. -/
theorem exists_poly_approx (f : ℝ → ℝ) (hf : Continuous f) (k : ℕ) :
    ∃ q : Polynomial ℝ, ∀ t ∈ Set.Icc (-(k : ℝ)) (k : ℝ), |q.eval t - f t| ≤ 1 / (k + 1) := by
  have hclo := polynomialFunctions_closure_eq_top (-(k : ℝ)) (k : ℝ)
  set s := Set.Icc (-(k : ℝ)) (k : ℝ) with hs
  set g : C(s, ℝ) := ⟨fun t => f t, by fun_prop⟩ with hg
  have hmem : g ∈ closure (polynomialFunctions s : Set C(s, ℝ)) := by
    have : g ∈ (polynomialFunctions s).topologicalClosure := by rw [hclo]; trivial
    exact this
  have hpos : (0 : ℝ) < 1 / (k + 1) := by positivity
  rw [Metric.mem_closure_iff] at hmem
  obtain ⟨p', hp'mem, hp'dist⟩ := hmem (1 / (k + 1)) hpos
  rw [polynomialFunctions_coe] at hp'mem
  obtain ⟨q, hq⟩ := hp'mem
  refine ⟨q, fun t ht => ?_⟩
  have hpt : dist (p' ⟨t, ht⟩) (g ⟨t, ht⟩) ≤ dist p' g := ContinuousMap.dist_apply_le_dist _
  have hp'eval : p' ⟨t, ht⟩ = q.eval t := by rw [← hq]; rfl
  have hgeval : g ⟨t, ht⟩ = f t := rfl
  rw [hp'eval, hgeval, Real.dist_eq] at hpt
  rw [dist_comm] at hp'dist
  linarith [hp'dist, hpt]

/-- The spectrum of a matrix is finite, hence contained in some symmetric interval `[-R, R]`. -/
theorem exists_spectrum_subset_Icc (M : Matrix (Fin d) (Fin d) ℝ) :
    ∃ R : ℝ, _root_.spectrum ℝ M ⊆ Set.Icc (-R) R := by
  have hfin : (_root_.spectrum ℝ M).Finite := M.finite_real_spectrum
  obtain ⟨R, hR⟩ := (hfin.image (fun x => |x|)).bddAbove
  refine ⟨R, fun t ht => ?_⟩
  have : |t| ≤ R := hR ⟨t, ht, rfl⟩
  rw [Set.mem_Icc]
  constructor <;> [linarith [neg_abs_le t]; linarith [le_abs_self t]]

/-- Continuity of the matrix-entry projection in the (L2 operator) matrix metric topology
(a linear functional on a finite-dimensional space). -/
theorem continuous_matrix_entry (i j : Fin d) :
    Continuous (fun M : Matrix (Fin d) (Fin d) ℝ => M i j) := by
  let L : Matrix (Fin d) (Fin d) ℝ →ₗ[ℝ] ℝ :=
    { toFun := fun M => M i j, map_add' := fun M N => rfl, map_smul' := fun c M => rfl }
  exact L.continuous_of_finiteDimensional

/-- **Continuous functional calculus of a measurable self-adjoint matrix family.** If
`M : X → Matrix (Fin d) (Fin d) ℝ` is measurable with each `M x` self-adjoint, and `f : ℝ → ℝ`
is continuous, then `x ↦ cfc f (M x)` is measurable. Proved by the per-point Weierstrass
approximation described above. -/
theorem measurable_cfc_continuous (f : ℝ → ℝ) (hf : Continuous f)
    (M : X → Matrix (Fin d) (Fin d) ℝ) (hM : Measurable M)
    (hMsa : ∀ x, IsSelfAdjoint (M x)) :
    Measurable (fun x => cfc f (M x)) := by
  classical
  choose q hq using fun k => exists_poly_approx f hf k
  -- per-point convergence in the matrix metric, via `tendsto_cfc_fun`
  have htend : ∀ x, Tendsto (fun k => cfc (q k).eval (M x)) atTop (𝓝 (cfc f (M x))) := by
    intro x
    obtain ⟨R, hR⟩ := exists_spectrum_subset_Icc (M x)
    apply tendsto_cfc_fun
    · rw [Metric.tendstoUniformlyOn_iff]
      intro ε hε
      obtain ⟨N, hN⟩ := exists_nat_gt (max R (1 / ε))
      filter_upwards [eventually_ge_atTop N] with k hk
      intro t ht
      have hkN : (N : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
      have hRk : R ≤ (k : ℝ) := le_trans (le_max_left _ _) (le_trans hN.le hkN)
      have h1k : 1 / ε ≤ (k : ℝ) := le_trans (le_max_right _ _) (le_trans hN.le hkN)
      have htIcc : t ∈ Set.Icc (-(k : ℝ)) (k : ℝ) := by
        have := hR ht; rw [Set.mem_Icc] at this ⊢
        constructor <;> [linarith [this.1]; linarith [this.2]]
      have hbound := hq k t htIcc
      have hlt : (1 : ℝ) / (k + 1) < ε := by
        rw [div_lt_iff₀ (by positivity)]
        have hεk : 1 ≤ ε * (k : ℝ) := by rw [div_le_iff₀ hε] at h1k; linarith
        nlinarith [hε.le]
      rw [Real.dist_eq]
      calc |f t - (q k).eval t| = |(q k).eval t - f t| := by rw [abs_sub_comm]
        _ ≤ 1 / (k + 1) := hbound
        _ < ε := hlt
    · filter_upwards with k
      exact (Polynomial.continuous (q k)).continuousOn
  -- entrywise measurability, then assemble
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  have hentry : ∀ k, Measurable (fun x => (cfc (q k).eval (M x)) i j) := by
    intro k
    have hpt : ∀ x, cfc (q k).eval (M x) = (Polynomial.aeval (M x)) (q k) := fun x =>
      cfc_polynomial (q k) (M x) (hMsa x)
    have heq : (fun x => (cfc (q k).eval (M x)) i j)
        = fun x => ((Polynomial.aeval (M x)) (q k)) i j := by
      funext x; rw [hpt x]
    rw [heq]
    exact ((measurable_pi_apply j).comp (measurable_pi_apply i)).comp
      ((measurable_aeval_matrix (q k)).comp hM)
  refine measurable_of_tendsto_metrizable hentry ?_
  rw [tendsto_pi_nhds]; intro x
  exact ((continuous_matrix_entry i j).tendsto _).comp (htend x)

end ErgodicTheory
