import Mathlib.Analysis.Normed.Algebra.Spectrum
import Mathlib.LinearAlgebra.Eigenspace.Matrix
import Mathlib.LinearAlgebra.Eigenspace.Triangularizable
import Mathlib.LinearAlgebra.Matrix.Irreducible.Defs

/-!
# THM-M-0054 discovery-only intake probe

These checks authenticate adjacent pinned nonnegative-matrix, eigenspace, spectrum, and spectral
radius APIs. They do not select a Perron-Frobenius variant or prove THM-M-0054.
-/

#check Matrix.IsIrreducible
#check Matrix.IsPrimitive
#check Matrix.isIrreducible_iff_exists_pow_pos
#check Matrix.spectrum_toLin'
#check Module.End.exists_eigenvalue
#check spectralRadius
#check spectrum.exists_nnnorm_eq_spectralRadius_of_nonempty
#check Real.spectralRadius_mem_spectrum_or
