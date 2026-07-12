import Mathlib.Algebra.Polynomial.OfFn
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# THM-M-1356 pinned anchor probes

The checked declarations below are representation and algebra substrate for
the frozen Routh-Hurwitz statement. None states the stability/minor
equivalence in `RouthHurwitzTarget`, and this file supplies no proof of it.
-/

#check Polynomial.ofFn
#check Polynomial.ofFn_coeff_eq_val_of_lt
#check Polynomial.ofFn_coeff_eq_zero_of_ge
#check Polynomial.ofFn_natDegree_lt
#check Polynomial.IsRoot
#check Polynomial.IsRoot.map
#check Polynomial.IsRoot.of_map
#check Polynomial.isRoot_map_iff
#check Complex.ofRealHom
#check Fin.castLE
#check Matrix.submatrix
#check Matrix.det
#check Matrix.det_submatrix_equiv_self
