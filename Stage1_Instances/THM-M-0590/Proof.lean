import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

noncomputable section

open scoped ComplexConjugate InnerProduct

namespace THMM0590

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

/-- A normal bounded operator lies on the essentially-normal boundary of the target. -/
theorem isEssentiallyNormal_of_adjoint_comp_eq_comp_adjoint (A : E →L[ℂ] E)
    (h : A† ∘L A = A ∘L A†) : IsEssentiallyNormal A := by
  unfold IsEssentiallyNormal
  rw [h, sub_self]
  exact isCompactOperator_zero

/-- Unitary equivalence modulo compact operators is reflexive. -/
theorem unitaryEquivalentModuloCompacts_refl (A : E →L[ℂ] E) :
    UnitaryEquivalentModuloCompacts A A := by
  refine ⟨LinearIsometryEquiv.refl ℂ E, ?_⟩
  have hzero :
      (LinearIsometryEquiv.refl ℂ E).toContinuousLinearEquiv.toContinuousLinearMap ∘L A ∘L
          (LinearIsometryEquiv.refl ℂ E).symm.toContinuousLinearEquiv.toContinuousLinearMap - A = 0 := by
    ext x
    simp
  rw [hzero]
  exact isCompactOperator_zero

omit [CompleteSpace E] in
/-- Compactness is preserved by conjugation with a unitary equivalence. -/
theorem isCompactOperator_unitary_conjugate
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    (U : E ≃ₗᵢ[ℂ] F) {C : E →L[ℂ] E} (hC : IsCompactOperator C) :
    IsCompactOperator
      (U.toContinuousLinearEquiv.toContinuousLinearMap ∘L C ∘L
        U.symm.toContinuousLinearEquiv.toContinuousLinearMap) := by
  exact (hC.comp_clm U.symm.toContinuousLinearEquiv.toContinuousLinearMap).clm_comp
    U.toContinuousLinearEquiv.toContinuousLinearMap

/-- Essential normality is preserved by conjugation with a unitary equivalence. -/
theorem isEssentiallyNormal_unitary_conjugate
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
    (U : E ≃ₗᵢ[ℂ] F) (A : E →L[ℂ] E) (hA : IsEssentiallyNormal A) :
    IsEssentiallyNormal
      (U.toContinuousLinearEquiv.toContinuousLinearMap ∘L A ∘L
        U.symm.toContinuousLinearEquiv.toContinuousLinearMap) := by
  unfold IsEssentiallyNormal at hA ⊢
  let u : E →L[ℂ] F := U.toContinuousLinearEquiv.toContinuousLinearMap
  let v : F →L[ℂ] E := U.symm.toContinuousLinearEquiv.toContinuousLinearMap
  have hvu : v ∘L u = ContinuousLinearMap.id ℂ E := by
    ext x
    simp [u, v]
  have hcomm :
      ((u ∘L A ∘L v)† ∘L (u ∘L A ∘L v)) -
          ((u ∘L A ∘L v) ∘L (u ∘L A ∘L v)†) =
        u ∘L ((A† ∘L A) - (A ∘L A†)) ∘L v := by
    change
      (((u ∘L A ∘L v)† ∘L (u ∘L A ∘L v)) -
          ((u ∘L A ∘L v) ∘L (u ∘L A ∘L v)†)) = _
    rw [ContinuousLinearMap.adjoint_comp, ContinuousLinearMap.adjoint_comp]
    have huadj : u† = v := by
      dsimp only [u, v]
      exact U.adjoint_eq_symm
    have hvadj : v† = u := by
      dsimp only [u, v]
      exact U.symm.adjoint_eq_symm
    rw [huadj, hvadj]
    simp only [ContinuousLinearMap.comp_assoc]
    rw [← ContinuousLinearMap.comp_assoc v u (A ∘L v)]
    rw [hvu, ContinuousLinearMap.id_comp]
    rw [← ContinuousLinearMap.comp_assoc v u (A† ∘L v)]
    rw [hvu, ContinuousLinearMap.id_comp]
    simp only [← ContinuousLinearMap.comp_assoc]
    rw [← ContinuousLinearMap.sub_comp]
    rw [ContinuousLinearMap.comp_assoc, ContinuousLinearMap.comp_assoc]
    rw [← ContinuousLinearMap.comp_sub]
  rw [hcomm]
  exact isCompactOperator_unitary_conjugate U hA

/-- The frozen BDF invariant equivalence holds on the exact diagonal boundary case. -/
theorem bdfInvariantEquivalence_refl (A : E →L[ℂ] E) :
    UnitaryEquivalentModuloCompacts A A ↔
      essentialSpectrum A = essentialSpectrum A ∧
        ∀ z : ℂ, z ∉ essentialSpectrum A →
          fredholmIndex (A - z • ContinuousLinearMap.id ℂ E) =
            fredholmIndex (A - z • ContinuousLinearMap.id ℂ E) := by
  constructor
  · intro _
    exact ⟨rfl, fun _ _ => rfl⟩
  · intro _
    exact unitaryEquivalentModuloCompacts_refl A

assert_no_sorry isEssentiallyNormal_of_adjoint_comp_eq_comp_adjoint
assert_no_sorry unitaryEquivalentModuloCompacts_refl
assert_no_sorry isCompactOperator_unitary_conjugate
assert_no_sorry isEssentiallyNormal_unitary_conjugate
assert_no_sorry bdfInvariantEquivalence_refl

#print sorries isEssentiallyNormal_of_adjoint_comp_eq_comp_adjoint
#print sorries unitaryEquivalentModuloCompacts_refl
#print sorries isCompactOperator_unitary_conjugate
#print sorries isEssentiallyNormal_unitary_conjugate
#print sorries bdfInvariantEquivalence_refl
#print axioms isEssentiallyNormal_of_adjoint_comp_eq_comp_adjoint
#print axioms unitaryEquivalentModuloCompacts_refl
#print axioms isCompactOperator_unitary_conjugate
#print axioms isEssentiallyNormal_unitary_conjugate
#print axioms bdfInvariantEquivalence_refl

end THMM0590
