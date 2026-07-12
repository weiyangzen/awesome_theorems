import Mathlib.Algebra.Polynomial.AlgebraMap
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-! Concrete elaboration probes for the two degenerate classes included by THM-M-0041. -/

namespace Stage1Instances.THM_M_0041

universe u v

noncomputable section

/-- The characteristic polynomial, expanded as the determinant of `X I - A`. -/
def characteristicPolynomial {R : Type u} [CommRing R]
    {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n R) : Polynomial R :=
  Matrix.det (Matrix.scalar n Polynomial.X - A.map Polynomial.C)

/-- The exact target expression remains well-typed for the empty matrix index type. -/
example {R : Type u} [CommRing R] (A : Matrix Empty Empty R) : Prop :=
  Polynomial.aeval A (characteristicPolynomial A) = 0

/-- The exact target expression remains well-typed over the concrete zero ring `PUnit`. -/
example {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n PUnit) : Prop :=
  Polynomial.aeval A (characteristicPolynomial A) = 0

example : CommRing PUnit := inferInstance
example : Fintype Empty := inferInstance
example : DecidableEq Empty := inferInstance
example : Not (Nonempty Empty) := not_nonempty_iff.mpr (by infer_instance)
example : (0 : PUnit) = 1 := rfl

end

end Stage1Instances.THM_M_0041
