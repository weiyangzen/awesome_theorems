import ObligationTree
import Mathlib.Analysis.Convex.Cone.Extension
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

namespace Stage1.THM_M_0338

open scoped ComplexOrder ComplexStarModule

noncomputable section

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

local instance operatorsIsScalarTower : IsScalarTower ℝ ℂ (Operators H) :=
  IsScalarTower.of_algebraMap_smul (fun r T => by
    ext x
    change (r : ℂ) • T x = r • T x
    rfl)

local instance selfAdjointPosSMulMono : PosSMulMono ℝ (selfAdjoint (Operators H)) where
  smul_le_smul_of_nonneg_left := by
    intro r hr x y hxy
    change r • (x : Operators H) ≤ r • (y : Operators H)
    exact @smul_le_smul_of_nonneg_left ℝ (Operators H) r (x : Operators H)
      (y : Operators H) _ _ _ _ _ hxy hr

private lemma state_im_eq_zero (diagonal : StarSubalgebra ℂ (Operators H))
    (phi : State diagonal) (d : diagonal)
    (hd : IsSelfAdjoint (d : Operators H)) : (phi d).im = 0 := by
  let r : ℝ := ‖(d : Operators H)‖
  have hnonneg_ambient : 0 ≤ (r • (1 : Operators H)) + d := by
    rw [← neg_le_iff_add_nonneg']
    simpa [r, Algebra.algebraMap_eq_smul_one] using hd.neg_algebraMap_norm_le_self
  have hnonneg_diag : 0 ≤ (r • (1 : diagonal)) + d := hnonneg_ambient
  have himage := phi.toPositiveLinearMap.map_nonneg hnonneg_diag
  have him : (phi ((r • (1 : diagonal)) + d)).im = 0 :=
    (Complex.nonneg_iff.mp himage).2.symm
  have hsmul : phi.toPositiveLinearMap (r • (1 : diagonal)) = (r : ℂ) := by
    change phi.toPositiveLinearMap ((r : ℂ) • (1 : diagonal)) = (r : ℂ)
    rw [map_smul]
    simp [phi.map_one]
  rw [map_add, hsmul] at him
  simpa using him

set_option maxHeartbeats 1000000

private lemma extension_exists_unconditional
    (diagonal : StarSubalgebra ℂ (Operators H)) (phi : State diagonal) :
    ExtensionExists diagonal phi := by
  let p : Submodule ℝ (selfAdjoint (Operators H)) :=
    { carrier := {x | (x : Operators H) ∈ diagonal}
      zero_mem' := diagonal.zero_mem
      add_mem' := fun hx hy ↦ diagonal.add_mem hx hy
      smul_mem' := fun r x hx ↦ diagonal.smul_mem hx (r : ℂ) }
  let f : p →ₗ[ℝ] ℝ :=
    { toFun := fun x ↦ (phi ⟨(x.1 : Operators H), x.2⟩).re
      map_add' := by
        intro x y
        have h := map_add phi.toPositiveLinearMap
          ⟨(x.1 : Operators H), x.2⟩ ⟨(y.1 : Operators H), y.2⟩
        exact congrArg Complex.re h
      map_smul' := by
        intro r x
        have h := phi.toPositiveLinearMap.toLinearMap.map_smul (r : ℂ)
          ⟨(x.1 : Operators H), x.2⟩
        change (phi ⟨(r • (x.1 : Operators H)), _⟩).re =
          r * (phi ⟨(x.1 : Operators H), x.2⟩).re
        rw [show (⟨r • (x.1 : Operators H), _⟩ : diagonal) =
            (r : ℂ) • (⟨(x.1 : Operators H), x.2⟩ : diagonal) by rfl]
        exact (congrArg Complex.re h).trans (Complex.re_ofReal_mul _ _) }
  let fp : selfAdjoint (Operators H) →ₗ.[ℝ] ℝ := ⟨p, f⟩
  have hf_nonneg : ∀ x : fp.domain, (x : selfAdjoint (Operators H)) ∈
      ConvexCone.positive ℝ (selfAdjoint (Operators H)) → 0 ≤ fp x := by
    intro x hx
    have hx0 : 0 ≤ (x : Operators H) := by
      change 0 ≤ (x : selfAdjoint (Operators H)) at hx
      exact hx
    exact (Complex.nonneg_iff.mp (phi.toPositiveLinearMap.map_nonneg hx0)).1
  have hf_dense : ∀ y : selfAdjoint (Operators H), ∃ x : fp.domain,
      (x : selfAdjoint (Operators H)) + y ∈
        ConvexCone.positive ℝ (selfAdjoint (Operators H)) := by
    intro y
    let x0 : selfAdjoint (Operators H) :=
      ⟨‖(y : Operators H)‖ • (1 : Operators H), by
        exact IsSelfAdjoint.smul (IsSelfAdjoint.all ‖(y : Operators H)‖)
          (IsSelfAdjoint.one (Operators H))⟩
    have hx0 : (x0 : Operators H) ∈ diagonal := by
      exact diagonal.smul_mem diagonal.one_mem (‖(y : Operators H)‖ : ℂ)
    refine ⟨⟨x0, hx0⟩, ?_⟩
    change 0 ≤ (x0 : Operators H) + (y : Operators H)
    rw [← neg_le_iff_add_nonneg']
    simpa [x0, Algebra.algebraMap_eq_smul_one] using y.property.neg_algebraMap_norm_le_self
  obtain ⟨g, hg_eq, hg_nonneg⟩ :=
    riesz_extension (ConvexCone.positive ℝ (selfAdjoint (Operators H))) fp hf_nonneg hf_dense
  let L : Operators H →ₗ[ℂ] ℂ :=
    { toFun := fun a ↦ (g (ℜ a) : ℂ) + Complex.I * (g (ℑ a) : ℂ)
      map_add' := by
        intro a b
        simp only [map_add, Complex.ofReal_add]
        ring
      map_smul' := by
        intro z a
        rw [realPart_smul, imaginaryPart_smul]
        simp only [map_sub, map_add, map_smul, Complex.ofReal_sub, Complex.ofReal_add]
        apply Complex.ext
        · simp [Complex.mul_re]
        · simp [Complex.mul_im] }
  have hL_nonneg : ∀ a : Operators H, 0 ≤ a → 0 ≤ L a := by
    intro a ha
    have ha_sa : IsSelfAdjoint a := IsSelfAdjoint.of_nonneg ha
    have hg_a : 0 ≤ g ⟨a, ha_sa⟩ := by
      apply hg_nonneg
      change 0 ≤ (⟨a, ha_sa⟩ : selfAdjoint (Operators H))
      exact ha
    rw [Complex.nonneg_iff]
    constructor
    · change 0 ≤ ((g (ℜ a) : ℂ) + Complex.I * (g (ℑ a) : ℂ)).re
      have hre : ℜ a = ⟨a, ha_sa⟩ := Subtype.ext ha_sa.coe_realPart
      rw [hre, ha_sa.imaginaryPart, map_zero]
      simpa using hg_a
    · change 0 = ((g (ℜ a) : ℂ) + Complex.I * (g (ℑ a) : ℂ)).im
      have hre : ℜ a = ⟨a, ha_sa⟩ := Subtype.ext ha_sa.coe_realPart
      rw [hre, ha_sa.imaginaryPart, map_zero]
      simp
  let extensionMap : Operators H →ₚ[ℂ] ℂ := PositiveLinearMap.mk₀ L hL_nonneg
  have hagree_sa (x : selfAdjoint (Operators H)) (hx : (x : Operators H) ∈ diagonal) :
      g x = (phi ⟨(x : Operators H), hx⟩).re := by
    exact hg_eq ⟨x, hx⟩
  have hmap_real (x : selfAdjoint (Operators H)) (hx : (x : Operators H) ∈ diagonal) :
      phi ⟨(x : Operators H), hx⟩ = (g x : ℂ) := by
    apply Complex.ext
    · simpa using (hagree_sa x hx).symm
    · simpa using state_im_eq_zero diagonal phi ⟨(x : Operators H), hx⟩ x.property
  have hagree (d : diagonal) : extensionMap (d : Operators H) = phi d := by
    have hre_mem : ((ℜ (d : Operators H) : selfAdjoint (Operators H)) : Operators H) ∈ diagonal := by
      rw [realPart_apply_coe]
      apply diagonal.smul_mem
      exact diagonal.add_mem d.property (diagonal.star_mem' d.property)
    have him_mem : ((ℑ (d : Operators H) : selfAdjoint (Operators H)) : Operators H) ∈ diagonal := by
      rw [imaginaryPart_apply_coe]
      apply diagonal.smul_mem
      apply diagonal.smul_mem
      exact diagonal.sub_mem d.property (diagonal.star_mem' d.property)
    change (g (ℜ (d : Operators H)) : ℂ) + Complex.I * (g (ℑ (d : Operators H)) : ℂ) = phi d
    rw [← hmap_real (ℜ (d : Operators H)) hre_mem,
      ← hmap_real (ℑ (d : Operators H)) him_mem]
    have hre : (⟨(ℜ (d : Operators H) : Operators H), hre_mem⟩ : diagonal) = ℜ d := by
      apply Subtype.ext
      simp [realPart_apply_coe]
    have him : (⟨(ℑ (d : Operators H) : Operators H), him_mem⟩ : diagonal) = ℑ d := by
      apply Subtype.ext
      simp [imaginaryPart_apply_coe]
    rw [hre, him]
    calc
      phi (ℜ d) + Complex.I * phi (ℑ d) = phi (ℜ d) + phi (Complex.I • ℑ d) := by
        rw [map_smul]
        rfl
      _ = phi (ℜ d + Complex.I • ℑ d) := by rw [map_add]
      _ = phi d := congrArg phi.toPositiveLinearMap (realPart_add_I_smul_imaginaryPart d)
  refine ⟨⟨extensionMap, ?_⟩, hagree⟩
  have hone := hagree (1 : diagonal)
  simpa [phi.map_one] using hone

theorem extension_exists_for_state
    (diagonal : StarSubalgebra ℂ (Operators H)) (phi : State diagonal) :
    ExtensionExists diagonal phi := by
  exact extension_exists_unconditional diagonal phi

/- This wrapper exposes the proved existence body at the exact frozen
Kadison-Singer input boundary.  The basis, diagonal characterization, and
purity hypotheses are not needed for existence; they remain explicit here so
the body composes with the still-open uniqueness half without a transport. -/
theorem extension_exists_for_kadison_singer_input
    (basis : HilbertBasis ℕ ℂ H) (diagonal : StarSubalgebra ℂ (Operators H))
    (_hdiagonal : ∀ T : Operators H,
      T ∈ diagonal ↔ ∀ i j : ℕ, i ≠ j → inner ℂ (basis i) (T (basis j)) = 0)
    (phi : State diagonal) (_hpure : IsPure phi) :
    ExtensionExists diagonal phi := by
  exact extension_exists_for_state diagonal phi

assert_no_sorry extension_exists_for_state
#print sorries extension_exists_for_state
#print axioms extension_exists_for_state
assert_no_sorry extension_exists_for_kadison_singer_input
#print sorries extension_exists_for_kadison_singer_input
#print axioms extension_exists_for_kadison_singer_input

end

end Stage1.THM_M_0338
