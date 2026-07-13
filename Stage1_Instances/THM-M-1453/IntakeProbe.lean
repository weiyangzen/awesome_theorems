import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1453 discovery-only intake probe

These checks authenticate pinned Gram-Schmidt, span, orthonormality, linear-map power, and matrix
representation interfaces. They do not define a Krylov subspace, select a canonical Arnoldi
correctness or convergence theorem, construct Arnoldi data, or prove the catalog claim.
-/

#check InnerProductSpace.gramSchmidt
#check InnerProductSpace.gramSchmidt_orthogonal
#check InnerProductSpace.span_gramSchmidt
#check InnerProductSpace.gramSchmidt_ne_zero
#check InnerProductSpace.gramSchmidtNormed_orthonormal
#check Matrix.mulVecLin
#check LinearMap.toMatrix_mulVec_repr
#check LinearMap.toMatrix_comp
#check LinearMap.toMatrix_pow

#print axioms InnerProductSpace.span_gramSchmidt
#print axioms LinearMap.toMatrix_pow
