/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Cocycle.Basic
import ErgodicTheory.Lyapunov.MeasurableSubspace
import ErgodicTheory.Lyapunov.FiltrationFromTopGapEnvelope
import ErgodicTheory.Lyapunov.DimZero
import ErgodicTheory.Lyapunov.TopGapEnvelope

/-!
# The Oseledets multiplicative ergodic theorem (one-sided, filtration form)

The main theorem of the development, drawing on `ErgodicTheory/Ergodic/`,
`ErgodicTheory/Cocycle/`, and `ErgodicTheory/Lyapunov/`.

## Main statements

For an ergodic measure-preserving `T` on a probability space and a measurable matrix
cocycle generator `A : X → GL(d, ℝ)` (encoded as `A x : Matrix (Fin d) (Fin d) ℝ` with
`det (A x) ≠ 0`) satisfying the one-sided integrability `log⁺‖A‖, log⁺‖A⁻¹‖ ∈ L¹(μ)`,
there exist finitely many distinct **Lyapunov exponents** `λ₁ > ⋯ > λ_k` and, for
`μ`-a.e. `x`, a strictly decreasing, `A`-equivariant, measurable **filtration** of
`EuclideanSpace ℝ (Fin d)` along which the cocycle grows at the exact rate `λᵢ`:
`(1/n) log‖A⁽ⁿ⁾(x) v‖ → λᵢ` for `v ∈ Vⁱₓ ∖ V^{i+1}ₓ`.

The matrices act on `EuclideanSpace ℝ (Fin d)` via `Matrix.toEuclideanCLM`, so all
norms are the L2 norm and the matrix operator norm is submultiplicative.

## References

* V. I. Oseledets, *A multiplicative ergodic theorem. Lyapunov characteristic numbers for
  dynamical systems*, Trans. Moscow Math. Soc. **19** (1968), 197–231.
* D. Ruelle, *Ergodic theory of differentiable dynamical systems*, Publ. Math. IHÉS **50** (1979).
* M. Viana, *Lectures on Lyapunov Exponents*, Cambridge Studies in Adv. Math. **145** (2014).
-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-- **Oseledets multiplicative ergodic theorem (one-sided, filtration form).**

Let `μ` be a probability measure, `T : X → X` ergodic measure-preserving, and
`A : X → Matrix (Fin d) (Fin d) ℝ` a measurable cocycle generator with `det (A x) ≠ 0`
and `log⁺‖A‖, log⁺‖A⁻¹‖ ∈ L¹(μ)`. Then there are `k` distinct Lyapunov exponents
`lam : Fin k → ℝ` (strictly decreasing) and a measurable family of subspaces
`V : Fin (k+1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))` forming, `μ`-a.e., a
strictly decreasing `A`-equivariant flag `⊤ = V 0 ⊋ ⋯ ⊋ V k = ⊥` along which
`(1/n) log‖A⁽ⁿ⁾(x) v‖ → lam i` for every `v ∈ V iₓ ∖ V (i+1)ₓ`. -/
theorem oseledets_filtration
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
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
              atTop (𝓝 (lam i))) := by
  rcases Nat.eq_zero_or_pos d with hd | hd
  · -- dimension zero: the trivial flag `⊤ = ⊥` with no exponents.
    subst hd
    exact oseledets_filtration_dim_zero hT A hA hAmeas hint hint'
  · -- positive dimension: compose the top-gap assembly with the proved envelope.
    haveI : NeZero d := ⟨hd.ne'⟩
    exact oseledets_filtration_of_topgap hT A hA hAmeas hint hint'
      (fun lam0 hlam0 => topGapMassEnvelope_ae hT hA hAmeas hint hint' lam0 hlam0)

end ErgodicTheory
