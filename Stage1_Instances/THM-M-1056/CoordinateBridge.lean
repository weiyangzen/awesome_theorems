import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.MeasureTheory.Constructions.BorelSpace.ContinuousLinearMap
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic
import Mathlib.MeasureTheory.Function.StronglyMeasurable.Lemmas

open MeasureTheory
open scoped Matrix.Norms.L2Operator

noncomputable section

universe u v

namespace Stage1Instances.THM_M_1056

instance instMeasurableSpaceMatrix {m n alpha : Type*} [MeasurableSpace alpha] :
    MeasurableSpace (Matrix m n alpha) :=
  inferInstanceAs (MeasurableSpace (m -> n -> alpha))

instance instOpensMeasurableSpaceMatrix {d : Nat} :
    OpensMeasurableSpace (Matrix (Fin d) (Fin d) Real) :=
  inferInstanceAs (OpensMeasurableSpace (Fin d -> Fin d -> Real))

variable {Omega : Type u} [MeasurableSpace Omega]
variable {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
variable [FiniteDimensional Real E]

abbrev dE : Nat := Module.finrank Real E

noncomputable def coordEquiv : E ≃L[Real] EuclideanSpace Real (Fin (dE (E := E))) :=
  ContinuousLinearEquiv.ofFinrankEq (by simp [dE])

noncomputable def conjugateCLM
    (L : E →L[Real] E) :
    EuclideanSpace Real (Fin (dE (E := E))) →L[Real]
      EuclideanSpace Real (Fin (dE (E := E))) :=
  (coordEquiv (E := E)).toContinuousLinearMap.comp
    (L.comp (coordEquiv (E := E)).symm.toContinuousLinearMap)

noncomputable def matrixOfCLM
    (L : E →L[Real] E) : Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real :=
  (Matrix.toEuclideanCLM (n := Fin (dE (E := E))) (𝕜 := Real)).symm (conjugateCLM L)

theorem toEuclideanCLM_matrixOfCLM
    (L : E →L[Real] E) :
    Matrix.toEuclideanCLM (𝕜 := Real) (matrixOfCLM L) = conjugateCLM L := by
  exact StarAlgEquiv.apply_symm_apply _ _

theorem conjugateCLM_apply (L : E →L[Real] E) (x : E) :
    conjugateCLM L (coordEquiv (E := E) x) = coordEquiv (E := E) (L x) := by
  simp [conjugateCLM]

theorem conjugateCLM_id :
    conjugateCLM (ContinuousLinearMap.id Real E) =
      ContinuousLinearMap.id Real (EuclideanSpace Real (Fin (dE (E := E)))) := by
  ext x
  simp [conjugateCLM]

theorem conjugateCLM_comp (L M : E →L[Real] E) :
    conjugateCLM (L.comp M) = (conjugateCLM L).comp (conjugateCLM M) := by
  ext x
  simp [conjugateCLM]

theorem matrixOfCLM_id :
    matrixOfCLM (ContinuousLinearMap.id Real E) = 1 := by
  apply (Matrix.toEuclideanCLM (n := Fin (dE (E := E))) (𝕜 := Real)).injective
  change Matrix.toEuclideanCLM (𝕜 := Real)
      (matrixOfCLM (ContinuousLinearMap.id Real E)) =
    Matrix.toEuclideanCLM (𝕜 := Real) 1
  rw [toEuclideanCLM_matrixOfCLM, conjugateCLM_id]
  exact (map_one (Matrix.toEuclideanCLM (n := Fin (dE (E := E))) (𝕜 := Real))).symm

theorem matrixOfCLM_comp (L M : E →L[Real] E) :
    matrixOfCLM (L.comp M) = matrixOfCLM L * matrixOfCLM M := by
  apply (Matrix.toEuclideanCLM (n := Fin (dE (E := E))) (𝕜 := Real)).injective
  change Matrix.toEuclideanCLM (𝕜 := Real) (matrixOfCLM (L.comp M)) =
    Matrix.toEuclideanCLM (𝕜 := Real) (matrixOfCLM L * matrixOfCLM M)
  rw [toEuclideanCLM_matrixOfCLM, map_mul, toEuclideanCLM_matrixOfCLM,
    toEuclideanCLM_matrixOfCLM, conjugateCLM_comp]
  rfl

theorem stronglyMeasurable_conjugateCLM
    {F : Omega → E →L[Real] E} (hF : StronglyMeasurable F) :
    StronglyMeasurable (fun omega => conjugateCLM (F omega)) := by
  let post : (E →L[Real] E) →L[Real]
      E →L[Real] EuclideanSpace Real (Fin (dE (E := E))) :=
    (ContinuousLinearMap.compL Real E E
      (EuclideanSpace Real (Fin (dE (E := E)))))
      (coordEquiv (E := E)).toContinuousLinearMap
  let pre : (E →L[Real] EuclideanSpace Real (Fin (dE (E := E)))) →L[Real]
      (EuclideanSpace Real (Fin (dE (E := E))) →L[Real]
        EuclideanSpace Real (Fin (dE (E := E)))) :=
    (ContinuousLinearMap.compL Real
      (EuclideanSpace Real (Fin (dE (E := E)))) E
      (EuclideanSpace Real (Fin (dE (E := E))))).flip
      (coordEquiv (E := E)).symm.toContinuousLinearMap
  have hpost : StronglyMeasurable (fun omega => post (F omega)) :=
    post.continuous.comp_stronglyMeasurable hF
  have hpre : StronglyMeasurable (fun omega => pre (post (F omega))) :=
    pre.continuous.comp_stronglyMeasurable hpost
  simpa only [post, pre, ContinuousLinearMap.compL_apply,
    ContinuousLinearMap.flip_apply, conjugateCLM] using hpre

theorem measurable_of_stronglyMeasurable_pi
    {G : Omega → Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real}
    (hG : StronglyMeasurable G) : Measurable G := by
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  exact (show StronglyMeasurable (fun omega => G omega i j) from
    (show Continuous (fun M : Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real =>
        M i j) by fun_prop).comp_stronglyMeasurable hG).measurable

theorem measurable_matrixOfCLM
    {F : Omega → E →L[Real] E} (hF : StronglyMeasurable F) :
    Measurable (fun omega => matrixOfCLM (F omega)) := by
  have hconj := stronglyMeasurable_conjugateCLM (F := F) hF
  let invLM :
      (EuclideanSpace Real (Fin (dE (E := E))) →L[Real]
        EuclideanSpace Real (Fin (dE (E := E)))) →ₗ[Real]
      Matrix (Fin (dE (E := E))) (Fin (dE (E := E))) Real :=
    { toFun := (Matrix.toEuclideanCLM (n := Fin (dE (E := E))) (𝕜 := Real)).symm
      map_add' := map_add _
      map_smul' := map_smul _ }
  let inv := invLM.toContinuousLinearMap
  have hmat : StronglyMeasurable (fun omega => inv (conjugateCLM (F omega))) :=
    inv.continuous.comp_stronglyMeasurable hconj
  have hstrong : StronglyMeasurable (fun omega => matrixOfCLM (F omega)) := by
    simpa only [inv, invLM, matrixOfCLM] using hmat
  exact measurable_of_stronglyMeasurable_pi hstrong

theorem det_matrixOf_equiv_ne_zero (L : E ≃L[Real] E) :
    (matrixOfCLM L.toContinuousLinearMap).det ≠ 0 := by
  apply Matrix.det_ne_zero_of_left_inverse
  rw [← matrixOfCLM_comp]
  have hcomp : L.symm.toContinuousLinearMap.comp L.toContinuousLinearMap =
      ContinuousLinearMap.id Real E := by
    ext x
    exact L.symm_apply_apply x
  rw [hcomp, matrixOfCLM_id]

theorem matrixOf_equiv_symm
    (L : E ≃L[Real] E) :
    matrixOfCLM L.symm.toContinuousLinearMap =
      (matrixOfCLM L.toContinuousLinearMap)⁻¹ := by
  let M := matrixOfCLM L.toContinuousLinearMap
  let N := matrixOfCLM L.symm.toContinuousLinearMap
  have hNM : N * M = 1 := by
    rw [← matrixOfCLM_comp]
    have hcomp : L.symm.toContinuousLinearMap.comp L.toContinuousLinearMap =
        ContinuousLinearMap.id Real E := by
      ext x
      exact L.symm_apply_apply x
    rw [hcomp, matrixOfCLM_id]
  have hdet : IsUnit M.det := (Matrix.isUnit_iff_isUnit_det M).mp
    (Matrix.isUnit_iff_isUnit_det M |>.mpr
      (isUnit_iff_ne_zero.mpr (det_matrixOf_equiv_ne_zero L)))
  calc
    N = N * 1 := by rw [mul_one]
    _ = N * (M * M⁻¹) := by rw [Matrix.mul_nonsing_inv M hdet]
    _ = (N * M) * M⁻¹ := by rw [mul_assoc]
    _ = M⁻¹ := by rw [hNM, one_mul]

end Stage1Instances.THM_M_1056
