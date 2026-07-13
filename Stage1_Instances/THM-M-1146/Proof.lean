import ObligationTree
import Mathlib.Analysis.Calculus.ContDiff.Basic

/-!
# THM-M-1146 proof-phase bodies

This module closes conjugation preservation and the upper/lower off-axis branches in the frozen
proof tree.
The real-axis harmonic-gluing obligation remains open; no root proof is asserted here.
-/

namespace Stage1Instances.THM_M_1146

open Complex InnerProductSpace Laplacian Topology
open scoped ComplexConjugate

noncomputable section

/-- The real Laplacian commutes with precomposition by complex conjugation. -/
theorem laplacian_comp_conj (u : ℂ → ℝ) :
    Δ (u ∘ conj) = Δ u ∘ conj := by
  rw [laplacian_eq_iteratedFDeriv_complexPlane]
  rw [laplacian_eq_iteratedFDeriv_complexPlane]
  funext z
  rw [show (u ∘ conj) = u ∘ (conjCLE : ℂ → ℂ) by rfl]
  simp only [← iteratedFDerivWithin_univ]
  change
    (iteratedFDerivWithin ℝ 2 (u ∘ (conjCLE : ℂ → ℂ))
        ((conjCLE : ℂ → ℂ) ⁻¹' Set.univ) z) ![1, 1] +
      (iteratedFDerivWithin ℝ 2 (u ∘ (conjCLE : ℂ → ℂ))
        ((conjCLE : ℂ → ℂ) ⁻¹' Set.univ) z) ![I, I] = _
  rw [conjCLE.iteratedFDerivWithin_comp_right u uniqueDiffOn_univ (Set.mem_univ _) 2]
  simp only [Function.comp_apply, ContinuousMultilinearMap.compContinuousLinearMap_apply,
    conjCLE_apply]
  congr 1
  · congr 1
    ext i
    fin_cases i <;> simp [conjCLE_apply]
  · change
      (iteratedFDerivWithin ℝ 2 u Set.univ (conj z))
          (fun i => (conjCLE : ℂ →L[ℝ] ℂ) (![I, I] i)) =
        (iteratedFDerivWithin ℝ 2 u Set.univ (conj z)) ![I, I]
    have harg : (fun i => (conjCLE : ℂ →L[ℝ] ℂ) (![I, I] i)) = ![-I, -I] := by
      ext i
      fin_cases i <;> simp [conjCLE_apply]
    rw [harg]
    let M := iteratedFDerivWithin ℝ 2 u Set.univ (conj z)
    calc
      M ![-I, -I] = M ((-1 : ℝ) • ![I, I]) := by
        congr 1
        ext i
        fin_cases i <;> simp
      _ = (∏ _ : Fin 2, (-1 : ℝ)) • M ![I, I] :=
        M.map_smul_univ (fun _ => (-1 : ℝ)) ![I, I]
      _ = M ![I, I] := by norm_num

/-- Precomposition by complex conjugation preserves real-valued harmonicity at a point. -/
theorem harmonicAt_comp_conj {u : ℂ → ℝ} {z : ℂ}
    (h : HarmonicAt u (conj z)) : HarmonicAt (u ∘ conj) z := by
  constructor
  · rw [show (u ∘ conj) = u ∘ (conjCLE : ℂ → ℂ) by rfl]
    have hcont := h.1.comp_continuousLinearMap (conjCLE : ℂ →L[ℝ] ℂ)
    simpa using hcont
  · rw [laplacian_comp_conj]
    exact h.2.comp_tendsto conjCLE.continuous.continuousAt

/-- Conjugation followed by output negation preserves harmonicity. -/
theorem harmonicAt_neg_comp_conj {u : ℂ → ℝ} {z : ℂ}
    (h : HarmonicAt u (conj z)) :
    HarmonicAt (fun w => -u (conj w)) z := by
  exact (harmonicAt_comp_conj h).neg

/-- Setwise form of conjugation preservation. -/
theorem harmonicOnNhd_comp_conj {u : ℂ → ℝ} {s : Set ℂ}
    (h : HarmonicOnNhd u s) :
    HarmonicOnNhd (u ∘ conj) (conj ⁻¹' s) := by
  intro z hz
  exact harmonicAt_comp_conj (h _ hz)

/-- Above the axis, the odd reflection is locally the input harmonic function. -/
theorem oddReflection_harmonicAt_of_pos {u : ℂ → ℝ} {z : ℂ}
    (hz : 0 < z.im) (hu : HarmonicAt u z) :
    HarmonicAt (oddReflection u) z := by
  apply (harmonicAt_congr_nhds ?_).mp hu
  filter_upwards [isOpen_lt continuous_const continuous_im |>.mem_nhds hz] with w hw
  simp [oddReflection, hw.le]

/-- Below the axis, the odd reflection is locally the negated conjugate input. -/
theorem oddReflection_harmonicAt_of_neg {u : ℂ → ℝ} {z : ℂ}
    (hz : z.im < 0) (hu : HarmonicAt u (conj z)) :
    HarmonicAt (oddReflection u) z := by
  apply (harmonicAt_congr_nhds ?_).mp (harmonicAt_neg_comp_conj hu)
  filter_upwards [isOpen_lt continuous_im continuous_const |>.mem_nhds hz] with w hw
  simp [oddReflection, not_le.mpr hw]

/-- The positive branch closes on the exact `upperPart` selected by the statement. -/
theorem oddReflection_harmonicOnNhd_upperPart {V : Set ℂ} {u : ℂ → ℝ}
    (hu : HarmonicOnNhd u (upperPart V)) :
    HarmonicOnNhd (oddReflection u) (upperPart V) := by
  intro z hz
  exact oddReflection_harmonicAt_of_pos hz.2 (hu z hz)

/-- The strict lower branch closes using domain symmetry and conjugation preservation. -/
theorem oddReflection_harmonicAt_of_mem_negative
    {V : Set ℂ} {u : ℂ → ℝ} {z : ℂ}
    (hsym : ∀ w, w ∈ V ↔ conj w ∈ V)
    (hu : HarmonicOnNhd u (upperPart V))
    (hzV : z ∈ V) (hzim : z.im < 0) :
    HarmonicAt (oddReflection u) z := by
  apply oddReflection_harmonicAt_of_neg hzim
  apply hu (conj z)
  exact ⟨(hsym z).mp hzV, by simpa using hzim⟩

#print axioms laplacian_comp_conj
#print axioms harmonicAt_comp_conj
#print axioms harmonicAt_neg_comp_conj
#print axioms harmonicOnNhd_comp_conj
#print axioms oddReflection_harmonicAt_of_pos
#print axioms oddReflection_harmonicAt_of_neg
#print axioms oddReflection_harmonicOnNhd_upperPart
#print axioms oddReflection_harmonicAt_of_mem_negative

end
end Stage1Instances.THM_M_1146
