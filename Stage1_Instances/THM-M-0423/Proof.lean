import Mathlib.LinearAlgebra.QuadraticForm.AlgClosed
import ObligationTree

/-!
# THM-M-0423 partial proof execution

These declarations elaborate candidate signatures for three leaves from the
frozen Hasse-Minkowski architecture: global isotropy transport along an
isometry, diagonalization of a nondegenerate form, and the algebraically closed
classification used at complex places. They do not implement the hard
local-to-global implication or create accepted leaf closure.
-/

noncomputable section

namespace Stage1.THM_M_0423.Proof

universe u v w

open QuadraticMap

/-- A quadratic-form isometry transports nonzero isotropic witnesses in both
directions. This matches the planned signature of
`M0423-T-GLOBAL-ISOTROPY-TRANSPORT`. -/
theorem isIsotropic_iff_of_isometryEquiv
    {K : Type u} {V : Type v} {W : Type w}
    [CommRing K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    {Q : QuadraticForm K V} {Q' : QuadraticForm K W}
    (e : Q.IsometryEquiv Q') :
    IsIsotropic Q ↔ IsIsotropic Q' := by
  constructor
  · rintro ⟨x, hx, hQx⟩
    refine ⟨e x, ?_, ?_⟩
    · simpa using e.injective.ne hx
    · simp [e.map_app x, hQx]
  · rintro ⟨y, hy, hQy⟩
    refine ⟨e.symm y, ?_, ?_⟩
    · simpa using e.symm.injective.ne hy
    · simp [e.symm.map_app y, hQy]

/-- Diagonalize a nondegenerate finite-dimensional quadratic form with
unit-valued, hence nonzero, coefficients. This implements the planned wrapper of
`M0423-C-BASIS-DIAGONAL`. -/
theorem equivalent_weightedSumSquares_units
    {K : Type u} {V : Type v}
    [Field K] [CharZero K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V) (hQ : Q.Nondegenerate) :
    ∃ a : Fin (Module.finrank K V) → Kˣ,
      QuadraticMap.Equivalent Q (QuadraticMap.weightedSumSquares K a) := by
  letI : Invertible (2 : K) := invertibleOfNonzero (by norm_num)
  apply Q.equivalent_weightedSumSquares_units_of_nondegenerate'
  exact (QuadraticForm.associated_isSymm K Q).isRefl.nondegenerate_iff_separatingLeft.mp
    (QuadraticMap.nondegenerate_associated_iff.mpr hQ)

/-- Over an algebraically closed characteristic-zero field, a nondegenerate
form is isometric to the sum of squares. This supplies the general engine for
`M0423-L-COMPLEX-CLASSIFICATION`. -/
theorem equivalent_sumSquares_of_isAlgClosed
    {K : Type u} {V : Type v}
    [Field K] [CharZero K] [IsAlgClosed K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V) (hQ : Q.Nondegenerate) :
    QuadraticMap.Equivalent Q
      (QuadraticMap.weightedSumSquares K
        (1 : Fin (Module.finrank K V) → K)) := by
  letI : Invertible (2 : K) := invertibleOfNonzero (by norm_num)
  apply Q.equivalent_weightedSumSquares_of_isAlgClosed
  exact (QuadraticForm.associated_isSymm K Q).isRefl.nondegenerate_iff_separatingLeft.mp
    (QuadraticMap.nondegenerate_associated_iff.mpr hQ)

/-- Literal specialization of the algebraically closed classification to
complex scalars, matching the planned complex-place leaf signature. -/
theorem equivalent_sumSquares_complex
    {V : Type v} [AddCommGroup V] [Module ℂ V] [FiniteDimensional ℂ V]
    (Q : QuadraticForm ℂ V) (hQ : Q.Nondegenerate) :
    QuadraticMap.Equivalent Q
      (QuadraticMap.weightedSumSquares ℂ
        (1 : Fin (Module.finrank ℂ V) → ℂ)) :=
  equivalent_sumSquares_of_isAlgClosed Q hQ

#check isIsotropic_iff_of_isometryEquiv
#check equivalent_weightedSumSquares_units
#check equivalent_sumSquares_of_isAlgClosed
#check equivalent_sumSquares_complex
#print axioms isIsotropic_iff_of_isometryEquiv
#print axioms equivalent_weightedSumSquares_units
#print axioms equivalent_sumSquares_of_isAlgClosed
#print axioms equivalent_sumSquares_complex

end Stage1.THM_M_0423.Proof
