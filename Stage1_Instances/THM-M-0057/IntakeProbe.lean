import Mathlib.Algebra.Star.SelfAdjoint
import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Eigenspace.Matrix

/-!
# THM-M-0057 discovery-only intake probe

These commands authenticate pinned normality, Frobenius-norm, matrix-spectrum, and Hermitian
eigenvalue APIs adjacent to the Hoffman-Wielandt theorem. They do not enumerate the eigenvalues of
a general normal matrix, choose a canonical perturbation inequality, declare the target, or grant
proof credit.
-/

#check IsStarNormal
#check Matrix.frobenius_norm_def
#check Matrix.frobenius_norm_conjTranspose
#check Matrix.spectrum_toLin'
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.eigenvalues_mem_spectrum_real
#check Matrix.IsHermitian.spectral_theorem
#check Matrix.IsHermitian.roots_charpoly_eq_eigenvalues

#print axioms Matrix.frobenius_norm_def
#print axioms Matrix.IsHermitian.spectral_theorem
#print axioms Matrix.IsHermitian.roots_charpoly_eq_eigenvalues
