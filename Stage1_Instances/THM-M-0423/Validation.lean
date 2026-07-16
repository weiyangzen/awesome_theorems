import Proof

/-!
# THM-M-0423 independent validation surface

This module independently reconstructs the checked partial declarations from
their definitions or pinned mathlib endpoints. It deliberately does not
provide the missing Hasse-Minkowski local-to-global implication.
-/

noncomputable section

namespace Stage1.THM_M_0423.Validation

universe u v w

open QuadraticMap

/-- Independent replay of isotropic-witness transport along an isometry. -/
theorem independent_isIsotropic_iff_of_isometryEquiv
    {K : Type u} {V : Type v} {W : Type w}
    [CommRing K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    {Q : QuadraticForm K V} {Q' : QuadraticForm K W}
    (e : Q.IsometryEquiv Q') :
    IsIsotropic Q ↔ IsIsotropic Q' := by
  constructor
  · rintro ⟨x, hx, hQx⟩
    refine ⟨e x, ?_, ?_⟩
    · simpa using e.injective.ne hx
    simp [e.map_app x, hQx]
  · rintro ⟨y, hy, hQy⟩
    refine ⟨e.symm y, ?_, ?_⟩
    · simpa using e.symm.injective.ne hy
    simp [e.symm.map_app y, hQy]

/-- Independent wrapper around the pinned nondegenerate diagonalization. -/
theorem independent_equivalent_weightedSumSquares_units
    {K : Type u} {V : Type v}
    [Field K] [CharZero K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V) (hQ : Q.Nondegenerate) :
    ∃ a : Fin (Module.finrank K V) → Kˣ,
      QuadraticMap.Equivalent Q (QuadraticMap.weightedSumSquares K a) := by
  letI : Invertible (2 : K) := invertibleOfNonzero (by norm_num)
  apply Q.equivalent_weightedSumSquares_units_of_nondegenerate'
  exact (QuadraticForm.associated_isSymm K Q).isRefl.nondegenerate_iff_separatingLeft.mp
    (QuadraticMap.nondegenerate_associated_iff.mpr hQ)

/-- Independent complex specialization of the pinned algebraically closed
classification. -/
theorem independent_equivalent_sumSquares_complex
    {V : Type v} [AddCommGroup V] [Module ℂ V] [FiniteDimensional ℂ V]
    (Q : QuadraticForm ℂ V) (hQ : Q.Nondegenerate) :
    QuadraticMap.Equivalent Q
      (QuadraticMap.weightedSumSquares ℂ
        (1 : Fin (Module.finrank ℂ V) → ℂ)) := by
  letI : Invertible (2 : ℂ) := invertibleOfNonzero (by norm_num)
  apply Q.equivalent_weightedSumSquares_of_isAlgClosed
  exact (QuadraticForm.associated_isSymm ℂ Q).isRefl.nondegenerate_iff_separatingLeft.mp
    (QuadraticMap.nondegenerate_associated_iff.mpr hQ)

#check independent_isIsotropic_iff_of_isometryEquiv
#check independent_equivalent_weightedSumSquares_units
#check independent_equivalent_sumSquares_complex
#print axioms independent_isIsotropic_iff_of_isometryEquiv
#print axioms independent_equivalent_weightedSumSquares_units
#print axioms independent_equivalent_sumSquares_complex

end Stage1.THM_M_0423.Validation
