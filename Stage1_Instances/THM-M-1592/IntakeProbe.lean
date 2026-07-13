import Mathlib.InformationTheory.Hamming
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.LinearAlgebra.Vandermonde

/-!
# THM-M-1592 discovery-only intake probe

These checks authenticate generic pinned APIs adjacent to a possible polynomial-evaluation-code
encoding. They do not define a Reed-Solomon code, state an MDS theorem, select the catalog target,
or provide theorem or proof credit.
-/

#check hammingDist
#check hammingNorm
#check Hamming
#check Polynomial.eval
#check Polynomial.card_roots'
#check Matrix.vandermonde
#check Matrix.det_vandermonde
#check Matrix.det_vandermonde_ne_zero_iff
#check Matrix.eval_matrixOfPolynomials_eq_vandermonde_mul_matrixOfPolynomials
