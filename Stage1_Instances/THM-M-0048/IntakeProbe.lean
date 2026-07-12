import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Order.Hom.PowersetCard

/-!
# THM-M-0048 discovery-only intake probe

These checks authenticate pinned determinant, submatrix, and ordered-subset interfaces and verify
that one candidate rectangular proposition shape elaborates. They do not select the canonical
source claim, declare or prove Cauchy-Binet, or give proof credit to the square specialization.
-/

open scoped BigOperators

#check Matrix.det_apply
#check Matrix.det_mul
#check Matrix.det_mul_aux
#check Matrix.submatrix
#check Matrix.det_submatrix_equiv_self
#check Set.powersetCard.ofFinEmbEquiv
#check Set.powersetCard.ofFinEmbEquiv.symm

#check fun {m n : ℕ} {R : Type} [CommRing R]
    (A : Matrix (Fin m) (Fin n) R) (B : Matrix (Fin n) (Fin m) R) =>
  (A * B).det =
    ∑ S : Set.powersetCard (Fin n) m,
      (A.submatrix id (Set.powersetCard.ofFinEmbEquiv.symm S)).det *
        (B.submatrix (Set.powersetCard.ofFinEmbEquiv.symm S) id).det

-- Source-scoped shape from Konstantopoulos formula (1); still not the canonical target.
#check fun {m n : ℕ} (_h : m ≤ n) {K : Type} [Field K]
    (A : Matrix (Fin m) (Fin n) K) (B : Matrix (Fin n) (Fin m) K) =>
  (A * B).det =
    ∑ S : Set.powersetCard (Fin n) m,
      (A.submatrix id (Set.powersetCard.ofFinEmbEquiv.symm S)).det *
        (B.submatrix (Set.powersetCard.ofFinEmbEquiv.symm S) id).det

#print axioms Matrix.det_mul
