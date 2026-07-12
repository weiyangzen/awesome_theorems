import Statement
import Mathlib.LinearAlgebra.StdBasis

/-!
# THM-M-1258 proof execution

The frozen target names a condition rather than asserting it for every family of fields. This file
provides both the exact conditional constructor for supplied span evidence and a non-vacuous
concrete family: the constant coordinate vector fields satisfy the condition on every open set.
-/

noncomputable section

namespace Stage1Instances.THM_M_1258

/-- Close the condition from exactly its frozen pointwise span obligation. -/
theorem of_pointwise_span {n r : Nat}
    (Omega : TopologicalSpace.Opens (Euclidean n))
    (X0 : Coefficients n) (X : Fin r -> Coefficients n)
    (hspan : forall x, x ∈ (Omega : Set (Euclidean n)) ->
      Submodule.span Real
        ((fun V : RealVectorField n => V x) '' {V | GeneratedBracket X0 X V}) = ⊤) :
    hormanderCondition Omega X0 X := by
  exact hspan

/-- The zero drift field, used in the concrete coordinate-field instance. -/
def zeroDrift (n : Nat) : Coefficients n := fun _ _ => 0

/-- The `j`th constant coordinate vector field. -/
def coordinateFields (n : Nat) : Fin n -> Coefficients n :=
  fun j i _ => if i = j then 1 else 0

theorem coordinateFields_value (n : Nat) (j : Fin n) (x : Euclidean n) :
    asVectorField (coordinateFields n j) x = Pi.basisFun Real (Fin n) j := by
  funext i
  simp [asVectorField, coordinateFields, Pi.basisFun_apply, Pi.single_apply]

/-- Constant coordinate fields contain a basis among their generated fields, hence satisfy the
bracket-generating condition on any open subset of `Real^n`. -/
theorem coordinateFields_hormanderCondition (n : Nat)
    (Omega : TopologicalSpace.Opens (Euclidean n)) :
    hormanderCondition Omega (zeroDrift n) (coordinateFields n) := by
  apply of_pointwise_span
  intro x _hx
  apply (Submodule.eq_top_iff_forall_basis_mem (Pi.basisFun Real (Fin n))).mpr
  intro j
  apply Submodule.subset_span
  refine ⟨asVectorField (coordinateFields n j), ?_, coordinateFields_value n j x⟩
  exact GeneratedBracket.square j

#print axioms of_pointwise_span
#print axioms coordinateFields_hormanderCondition

end Stage1Instances.THM_M_1258
