import ConditionalWrapper
import M1056ProjectionBridge

open Filter Function MeasureTheory
open scoped Matrix.Norms.L2Operator

noncomputable section

universe u v

namespace Stage1Instances.THM_M_1056

open ProjectionBridge

theorem stronglyMeasurable_toEuclideanCLM
    {Omega : Type u} [MeasurableSpace Omega] {d : Nat}
    {F : Omega -> Matrix (Fin d) (Fin d) Real} (hF : Measurable F) :
    StronglyMeasurable (fun omega =>
      Matrix.toEuclideanCLM (𝕜 := Real) (F omega)) := by
  let fLM : Matrix (Fin d) (Fin d) Real →ₗ[Real]
      (EuclideanSpace Real (Fin d) →L[Real] EuclideanSpace Real (Fin d)) :=
    { toFun := Matrix.toEuclideanCLM (𝕜 := Real)
      map_add' := map_add _
      map_smul' := map_smul _ }
  let f := fLM.toContinuousLinearMap
  have hstrong : StronglyMeasurable (fun M : Matrix (Fin d) (Fin d) Real => f M) :=
    f.continuous.stronglyMeasurable
  exact hstrong.comp_measurable hF

theorem measurableObliqueProjectionPackage :
    MeasurableObliqueProjectionPackage.{u, v} := by
  intro Omega _ E _ _ _ mu k V hV hinternal
  let P : Omega -> Fin k -> Euclid E →L[Real] Euclid E :=
    fun omega i => Matrix.toEuclideanCLM (𝕜 := Real)
      (componentMatrix V i omega)
  refine ⟨P, ?_, ?_⟩
  · intro i
    exact stronglyMeasurable_toEuclideanCLM (measurable_componentMatrix hV i)
  · filter_upwards [hinternal] with omega hint
    refine ⟨fun i y => componentMatrix_apply_mem V i omega y, ?_, ?_, ?_⟩
    · intro i y hy
      exact toEuclideanCLM_componentMatrix_apply_of_mem_same V i omega hint y hy
    · intro i j hij
      have h := componentMatrix_disjoint V i j hij omega hint
      have hm := congrArg
        (Matrix.toEuclideanCLM (𝕜 := Real) (n := Fin (dE (E := E)))) h
      simpa [P] using hm
    · have h := componentMatrix_sum V omega hint
      have hm := congrArg
        (Matrix.toEuclideanCLM (𝕜 := Real) (n := Fin (dE (E := E)))) h
      simpa [P] using hm

theorem oseledets_multiplicative_ergodic_target :
    Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget.{u, v} :=
  oseledets_target_of_projection_package measurableObliqueProjectionPackage

#print axioms oseledets_multiplicative_ergodic_target

end Stage1Instances.THM_M_1056

