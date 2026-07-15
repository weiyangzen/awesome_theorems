import ErgodicTheory.TwoSided.SplittingAssembly
import Mathlib.Algebra.DirectSum.Decomposition
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

open MeasureTheory Matrix DirectSum
open scoped Matrix.Norms.L2Operator RealInnerProductSpace BigOperators

noncomputable section

namespace Stage1Instances.THM_M_1056.ProjectionBridge

open ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d k : Nat}

def orthogonalMatrix
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) : Matrix (Fin d) (Fin d) Real :=
  orthProjMatrix (E i x)

def sumOrthogonalMatrix
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) : Matrix (Fin d) (Fin d) Real :=
  ∑ i, orthogonalMatrix E i x

def componentMatrix
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) : Matrix (Fin d) (Fin d) Real :=
  orthogonalMatrix E i x * (sumOrthogonalMatrix E x)⁻¹

theorem measurable_orthogonalMatrix
    {E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d))}
    (hE : forall i, MeasurableSubspace fun x => E i x) (i : Fin k) :
    Measurable (orthogonalMatrix E i) := by
  exact hE i

theorem measurable_sumOrthogonalMatrix
    {E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d))}
    (hE : forall i, MeasurableSubspace fun x => E i x) :
    Measurable (sumOrthogonalMatrix E) := by
  exact Finset.measurable_sum Finset.univ fun i _ => hE i

theorem measurable_componentMatrix
    {E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d))}
    (hE : forall i, MeasurableSubspace fun x => E i x) (i : Fin k) :
    Measurable (componentMatrix E i) := by
  exact (hE i).mul (measurable_inv_matrix.comp (measurable_sumOrthogonalMatrix hE))

theorem toEuclideanCLM_orthogonalMatrix_apply
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) (v : EuclideanSpace Real (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := Real) (orthogonalMatrix E i x) v =
      (E i x).starProjection v := by
  rw [orthogonalMatrix, orthProjMatrix, StarAlgEquiv.apply_symm_apply]

theorem inner_sumOrthogonalMatrix_apply
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) (v : EuclideanSpace Real (Fin d)) :
    inner Real (Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x) v) v =
      ∑ i, norm ((E i x).starProjection v) ^ 2 := by
  rw [sumOrthogonalMatrix, map_sum]
  rw [ContinuousLinearMap.sum_apply, sum_inner]
  apply Finset.sum_congr rfl
  intro i _
  rw [toEuclideanCLM_orthogonalMatrix_apply]
  exact (Submodule.re_inner_starProjection_eq_normSq (E i x) v)

theorem sumOrthogonalMatrix_injective
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) (hinternal : DirectSum.IsInternal fun i => E i x) :
    Function.Injective (sumOrthogonalMatrix E x).mulVec := by
  intro v w hv
  apply sub_eq_zero.mp
  set z : EuclideanSpace Real (Fin d) := WithLp.toLp 2 (v - w) with hz
  have hvw : Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x) z = 0 := by
    apply WithLp.ofLp_injective 2
    simpa [z, Matrix.ofLp_toEuclideanCLM, Matrix.mulVec_sub] using sub_eq_zero.mpr hv
  have hinner := congrArg (fun y => inner Real y z) hvw
  change inner Real
      (Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x) z) z =
    inner Real 0 z at hinner
  rw [inner_zero_left, inner_sumOrthogonalMatrix_apply] at hinner
  have hzero : forall i : Fin k, norm ((E i x).starProjection z) ^ 2 = 0 := by
    intro i
    exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg _)).mp hinner i
      (Finset.mem_univ i)
  have hortho : forall i : Fin k, z ∈ (E i x)ᗮ := by
    intro i
    rw [← Submodule.starProjection_apply_eq_zero_iff]
    exact norm_eq_zero.mp (sq_eq_zero_iff.mp (hzero i))
  have hall : z ∈ (iInf fun i : Fin k => (E i x)ᗮ) := by
    rw [Submodule.mem_iInf]
    exact hortho
  rw [Submodule.iInf_orthogonal, hinternal.submodule_iSup_eq_top,
    Submodule.top_orthogonal_eq_bot, Submodule.mem_bot] at hall
  subst z
  simpa using congrArg WithLp.ofLp hall

theorem sumOrthogonalMatrix_isUnit
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) (hinternal : DirectSum.IsInternal fun i => E i x) :
    IsUnit (sumOrthogonalMatrix E x).det := by
  rw [← Matrix.isUnit_iff_isUnit_det, ← Matrix.mulVec_injective_iff_isUnit]
  exact sumOrthogonalMatrix_injective E x hinternal

theorem toEuclideanCLM_sumOrthogonalMatrix_apply
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) (v : EuclideanSpace Real (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x) v =
      ∑ i, (E i x).starProjection v := by
  rw [sumOrthogonalMatrix, map_sum, ContinuousLinearMap.sum_apply]
  apply Finset.sum_congr rfl
  intro i _
  exact toEuclideanCLM_orthogonalMatrix_apply E i x v

theorem sum_starProjection_nonsingInv_of_mem_same
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) (hinternal : DirectSum.IsInternal fun i => E i x)
    (i : Fin k) (v : EuclideanSpace Real (Fin d)) (hv : v ∈ E i x) :
    (E i x).starProjection
        (Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x)⁻¹ v) = v := by
  let hdet := sumOrthogonalMatrix_isUnit E x hinternal
  set w := Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x)⁻¹ v with hw
  have hsum : ∑ j, (E j x).starProjection w = v := by
    rw [← toEuclideanCLM_sumOrthogonalMatrix_apply]
    subst w
    rw [← ContinuousLinearMap.mul_apply, ← map_mul,
      Matrix.mul_nonsing_inv _ hdet, map_one, ContinuousLinearMap.one_apply]
  have hmemLeft : ∀ a ∈ (Finset.univ : Finset (Fin k)),
      (E a x).starProjection w ∈ E a x := fun a _ => (E a x).starProjection_apply_mem w
  have hmemRight : ∀ a ∈ (Finset.univ : Finset (Fin k)),
      (if a = i then v else 0) ∈ E a x := by
    intro a _
    split_ifs with hai
    · simpa [hai] using hv
    · exact (E a x).zero_mem
  have hsumEq :
      ∑ a ∈ (Finset.univ : Finset (Fin k)), (E a x).starProjection w =
        ∑ a ∈ (Finset.univ : Finset (Fin k)), if a = i then v else 0 := by
    simpa using hsum
  have hi :=
    (iSupIndep_iff_finset_sum_eq_imp_eq (fun a : Fin k => E a x)).mp
      hinternal.submodule_iSupIndep Finset.univ
      (fun a => (E a x).starProjection w) (fun a => if a = i then v else 0)
      (fun a ha => ⟨hmemLeft a ha, hmemRight a ha⟩) hsumEq i (Finset.mem_univ i)
  simpa using hi

theorem sum_starProjection_nonsingInv_of_mem_ne
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) (hinternal : DirectSum.IsInternal fun i => E i x)
    (i j : Fin k) (hij : i ≠ j) (v : EuclideanSpace Real (Fin d)) (hv : v ∈ E j x) :
    (E i x).starProjection
        (Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x)⁻¹ v) = 0 := by
  let hdet := sumOrthogonalMatrix_isUnit E x hinternal
  set w := Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x)⁻¹ v with hw
  have hsum : ∑ l, (E l x).starProjection w = v := by
    rw [← toEuclideanCLM_sumOrthogonalMatrix_apply]
    subst w
    rw [← ContinuousLinearMap.mul_apply, ← map_mul,
      Matrix.mul_nonsing_inv _ hdet, map_one, ContinuousLinearMap.one_apply]
  have hmemLeft : ∀ a ∈ (Finset.univ : Finset (Fin k)),
      (E a x).starProjection w ∈ E a x := fun a _ => (E a x).starProjection_apply_mem w
  have hmemRight : ∀ a ∈ (Finset.univ : Finset (Fin k)),
      (if a = j then v else 0) ∈ E a x := by
    intro a _
    split_ifs with haj
    · simpa [haj] using hv
    · exact (E a x).zero_mem
  have hsumEq :
      ∑ a ∈ (Finset.univ : Finset (Fin k)), (E a x).starProjection w =
        ∑ a ∈ (Finset.univ : Finset (Fin k)), if a = j then v else 0 := by
    simpa using hsum
  have hi :=
    (iSupIndep_iff_finset_sum_eq_imp_eq (fun a : Fin k => E a x)).mp
      hinternal.submodule_iSupIndep Finset.univ
      (fun a => (E a x).starProjection w) (fun a => if a = j then v else 0)
      (fun a ha => ⟨hmemLeft a ha, hmemRight a ha⟩) hsumEq i (Finset.mem_univ i)
  simpa [hij] using hi

theorem toEuclideanCLM_componentMatrix_apply
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) (v : EuclideanSpace Real (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v =
      (E i x).starProjection
        (Matrix.toEuclideanCLM (𝕜 := Real) (sumOrthogonalMatrix E x)⁻¹ v) := by
  rw [componentMatrix, map_mul, ContinuousLinearMap.mul_apply,
    toEuclideanCLM_orthogonalMatrix_apply]

theorem toEuclideanCLM_componentMatrix_apply_of_mem_same
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) (hinternal : DirectSum.IsInternal fun a => E a x)
    (v : EuclideanSpace Real (Fin d)) (hv : v ∈ E i x) :
    Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v = v := by
  rw [toEuclideanCLM_componentMatrix_apply]
  exact sum_starProjection_nonsingInv_of_mem_same E x hinternal i v hv

theorem toEuclideanCLM_componentMatrix_apply_of_mem_ne
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i j : Fin k) (hij : i ≠ j) (x : X)
    (hinternal : DirectSum.IsInternal fun a => E a x)
    (v : EuclideanSpace Real (Fin d)) (hv : v ∈ E j x) :
    Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v = 0 := by
  rw [toEuclideanCLM_componentMatrix_apply]
  exact sum_starProjection_nonsingInv_of_mem_ne E x hinternal i j hij v hv

theorem componentMatrix_apply_mem
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) (v : EuclideanSpace Real (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v ∈ E i x := by
  rw [toEuclideanCLM_componentMatrix_apply]
  exact (E i x).starProjection_apply_mem _

theorem componentMatrix_idempotent
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) (hinternal : DirectSum.IsInternal fun a => E a x) :
    componentMatrix E i x * componentMatrix E i x = componentMatrix E i x := by
  apply (Matrix.toEuclideanCLM (𝕜 := Real) (n := Fin d)).injective
  rw [map_mul]
  apply ContinuousLinearMap.ext
  intro v
  exact toEuclideanCLM_componentMatrix_apply_of_mem_same E i x hinternal _
    (componentMatrix_apply_mem E i x v)

theorem componentMatrix_disjoint
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i j : Fin k) (hij : i ≠ j) (x : X)
    (hinternal : DirectSum.IsInternal fun a => E a x) :
    componentMatrix E i x * componentMatrix E j x = 0 := by
  apply (Matrix.toEuclideanCLM (𝕜 := Real) (n := Fin d)).injective
  rw [map_mul, map_zero]
  apply ContinuousLinearMap.ext
  intro v
  exact toEuclideanCLM_componentMatrix_apply_of_mem_ne E i j hij x hinternal _
    (componentMatrix_apply_mem E j x v)

theorem componentMatrix_sum
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (x : X) (hinternal : DirectSum.IsInternal fun a => E a x) :
    ∑ i, componentMatrix E i x = 1 := by
  simp only [componentMatrix]
  rw [← Finset.sum_mul, ← sumOrthogonalMatrix,
    Matrix.mul_nonsing_inv _ (sumOrthogonalMatrix_isUnit E x hinternal)]

theorem componentMatrix_ne_zero
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) (hinternal : DirectSum.IsInternal fun a => E a x)
    (hne : E i x ≠ ⊥) : componentMatrix E i x ≠ 0 := by
  intro hzero
  have hnontrivial : Nontrivial (E i x) := Submodule.nontrivial_iff_ne_bot.mpr hne
  letI := hnontrivial
  obtain ⟨v : E i x, hv0 : v ≠ 0⟩ := exists_ne (0 : E i x)
  have hv : (v : EuclideanSpace Real (Fin d)) ∈ E i x := v.property
  have hfix := toEuclideanCLM_componentMatrix_apply_of_mem_same E i x hinternal (v :
    EuclideanSpace Real (Fin d)) hv
  rw [hzero, map_zero, ContinuousLinearMap.zero_apply] at hfix
  exact hv0 (Subtype.ext hfix.symm)

theorem componentMatrix_fixes_iff_mem
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x : X) (hinternal : DirectSum.IsInternal fun a => E a x)
    (v : EuclideanSpace Real (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v = v ↔ v ∈ E i x := by
  constructor
  · intro h
    rw [← h]
    exact componentMatrix_apply_mem E i x v
  · exact toEuclideanCLM_componentMatrix_apply_of_mem_same E i x hinternal v

theorem componentMatrix_equivariant
    (E : Fin k -> X -> Submodule Real (EuclideanSpace Real (Fin d)))
    (i : Fin k) (x y : X)
    (hinternalX : DirectSum.IsInternal fun a => E a x)
    (hinternalY : DirectSum.IsInternal fun a => E a y)
    (A : Matrix (Fin d) (Fin d) Real) (hA : A.det ≠ 0)
    (hmap : forall a, Submodule.map (Matrix.toEuclideanCLM (𝕜 := Real) A).toLinearMap
      (E a x) = E a y) :
    A * componentMatrix E i x = componentMatrix E i y * A := by
  apply (Matrix.toEuclideanCLM (𝕜 := Real) (n := Fin d)).injective
  rw [map_mul, map_mul]
  apply ContinuousLinearMap.ext
  intro v
  change Matrix.toEuclideanCLM (𝕜 := Real) A
      (Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v) =
    Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i y)
      (Matrix.toEuclideanCLM (𝕜 := Real) A v)
  let u := Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v
  have hu : u ∈ E i x := componentMatrix_apply_mem E i x v
  have hAu : Matrix.toEuclideanCLM (𝕜 := Real) A u ∈ E i y := by
    rw [← hmap i]
    exact ⟨u, hu, rfl⟩
  have hmain : Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i y)
      (Matrix.toEuclideanCLM (𝕜 := Real) A u) =
      Matrix.toEuclideanCLM (𝕜 := Real) A u :=
    toEuclideanCLM_componentMatrix_apply_of_mem_same E i y hinternalY _ hAu
  have hsumv : ∑ j, Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E j x) v = v := by
    have := congrArg (fun M : Matrix (Fin d) (Fin d) Real =>
      Matrix.toEuclideanCLM (𝕜 := Real) M v) (componentMatrix_sum E x hinternalX)
    simpa only [map_sum, ContinuousLinearMap.sum_apply, map_one,
      ContinuousLinearMap.one_apply] using this
  have hother : forall j, j ≠ i ->
      Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i y)
          (Matrix.toEuclideanCLM (𝕜 := Real) A
            (Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E j x) v)) = 0 := by
    intro j hji
    apply toEuclideanCLM_componentMatrix_apply_of_mem_ne E i j hji.symm y hinternalY
    rw [← hmap j]
    exact ⟨_, componentMatrix_apply_mem E j x v, rfl⟩
  -- Compare both sides on the unique component decomposition of `v`.
  have happly := congrArg (Matrix.toEuclideanCLM (𝕜 := Real) A) hsumv
  rw [map_sum] at happly
  change Matrix.toEuclideanCLM (𝕜 := Real) A u =
    Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i y)
      (Matrix.toEuclideanCLM (𝕜 := Real) A v)
  rw [← happly]
  rw [Finset.sum_eq_add_sum_diff_singleton i _ (fun h => (h (Finset.mem_univ i)).elim)]
  rw [map_add, map_sum]
  rw [show Matrix.toEuclideanCLM (𝕜 := Real) A
      (Matrix.toEuclideanCLM (𝕜 := Real) (componentMatrix E i x) v) =
      Matrix.toEuclideanCLM (𝕜 := Real) A u from rfl, hmain]
  rw [Finset.sum_eq_zero fun j hj => hother j (by
    exact fun hji => (Finset.mem_sdiff.mp hj).2 (Finset.mem_singleton.mpr hji))]
  simp

end Stage1Instances.THM_M_1056.ProjectionBridge

