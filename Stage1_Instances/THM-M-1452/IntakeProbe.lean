import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.Analysis.Matrix.Spectrum

/-!
# THM-M-1452 discovery-only intake probe

These checks authenticate pinned Hermitian spectral and Gram-Schmidt interfaces adjacent to a
possible Lanczos statement. They do not select a canonical recurrence, define a Lanczos algorithm,
prove a Krylov or tridiagonal invariant, audit terminal proof provenance, or prove the catalog
claim.
-/

#check Matrix.IsHermitian
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.eigenvectorBasis
#check Matrix.IsHermitian.mulVec_eigenvectorBasis
#check Matrix.IsHermitian.eigenvectorUnitary
#check Matrix.IsHermitian.spectral_theorem
#check InnerProductSpace.gramSchmidt
#check InnerProductSpace.gramSchmidt_orthogonal
#check InnerProductSpace.span_gramSchmidt
#check InnerProductSpace.gramSchmidtNormed_orthonormal
#check InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular

#print axioms Matrix.IsHermitian.spectral_theorem
#print axioms InnerProductSpace.gramSchmidt_orthogonal
