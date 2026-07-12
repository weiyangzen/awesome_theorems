import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# THM-M-1356 discovery-only intake probe

These checks authenticate pinned polynomial-root, complex-real-part, and finite-matrix determinant
interfaces adjacent to a future Routh-Hurwitz statement. They neither define the source's Hurwitz
matrix convention nor state or prove THM-M-1356.
-/

#check Polynomial
#check Polynomial.IsRoot
#check Polynomial.roots
#check Polynomial.mem_roots
#check Polynomial.map
#check Polynomial.eval₂
#check Complex.ofRealHom
#check Complex.re
#check Matrix
#check Matrix.submatrix
#check Matrix.det
#check Fin.castLE
