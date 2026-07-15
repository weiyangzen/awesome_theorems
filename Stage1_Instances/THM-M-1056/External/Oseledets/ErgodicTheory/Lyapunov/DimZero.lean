/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Cocycle.Basic
import ErgodicTheory.Lyapunov.MeasurableSubspace

/-!
# The Oseledets filtration theorem, dimension-zero case

This module proves `ErgodicTheory.oseledets_filtration_dim_zero`, the trivial `d = 0` base case of
the Oseledets multiplicative ergodic theorem `ErgodicTheory.oseledets_filtration` (see
`ErgodicTheory/MultiplicativeErgodic.lean`).  When the ambient space is `EuclideanSpace ℝ (Fin 0)`
there are no exponents (`k = 0`) and the single subspace `⊤ = ⊥` is the whole (zero) space, so
every conjunct of the conclusion holds trivially.  The main theorem composes this with the
positive-dimensional `ErgodicTheory.oseledets_filtration_of_topgap`.

## Main results

* `ErgodicTheory.oseledets_filtration_dim_zero`: the dimension-zero case of the Oseledets filtration
  theorem.
-/

open MeasureTheory Filter Topology

noncomputable section

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X]

private lemma euclidean_zero_subsingleton : Subsingleton (EuclideanSpace ℝ (Fin 0)) :=
  ⟨fun a b => by ext i; exact i.elim0⟩

private lemma submodule_zero_subsingleton :
    Subsingleton (Submodule ℝ (EuclideanSpace ℝ (Fin 0))) := by
  haveI := euclidean_zero_subsingleton
  exact ⟨fun p q => by
    ext v
    have hv : v = 0 := Subsingleton.elim v 0
    simp [hv]⟩

/-- **The Oseledets filtration theorem, dimension-zero case.**
Trivial: `k = 0`, `V ≡ ⊤ = ⊥`. -/
theorem oseledets_filtration_dim_zero
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (_hT : Ergodic T μ)
    (A : X → Matrix (Fin 0) (Fin 0) ℝ)
    (_hA : ∀ x, (A x).det ≠ 0)
    (_hAmeas : Measurable A)
    (_hint : IntegrableLogNorm A μ)
    (_hint' : IntegrableLogNorm (fun x ↦ (A x)⁻¹) μ) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (V : Fin (k + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin 0))),
      StrictAnti lam ∧
      (∀ i, MeasurableSubspace fun x => V i x) ∧
      ∀ᵐ x ∂μ,
        V 0 x = ⊤ ∧ V (Fin.last k) x = ⊥ ∧
        (∀ i : Fin k, V i.succ x < V i.castSucc x) ∧
        (∀ i : Fin (k + 1),
          Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x)
            = V i (T x)) ∧
        (∀ i : Fin k, ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin 0))),
            v ∉ V i.succ x →
            Tendsto
              (fun n : ℕ => (n : ℝ)⁻¹ *
                Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
              atTop (𝓝 (lam i))) := by
  haveI := submodule_zero_subsingleton
  refine ⟨0, fun i => i.elim0, fun _ _ => ⊤, fun i => i.elim0, ?_, ?_⟩
  · intro i
    change Measurable fun _ : X ↦
      orthProjMatrix (⊤ : Submodule ℝ (EuclideanSpace ℝ (Fin 0)))
    exact measurable_const
  · refine Eventually.of_forall fun x => ⟨rfl, Subsingleton.elim _ _, fun i => i.elim0,
      fun i => Subsingleton.elim _ _, fun i => i.elim0⟩

end ErgodicTheory
