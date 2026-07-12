import Mathlib.Algebra.Ring.Periodic
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.Normed.Algebra.Spectrum
import Mathlib.Analysis.ODE.Basic
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs

/-!
# THM-M-1354 discovery-only intake probe

These checks authenticate adjacent pinned periodicity, ODE, matrix-exponential, spectrum,
characteristic-polynomial, and eigenvalue interfaces. They do not define a periodic linear system,
fundamental matrix, monodromy, Floquet multiplier, or characteristic exponent. No target theorem or
proof body is declared here.
-/

#check Function.Periodic
#check IsIntegralCurve
#check Matrix
#check Matrix.det
#check NormedSpace.exp
#check Matrix.isUnit_exp
#check Matrix.charpoly
#check spectrum
#check Matrix.mem_spectrum_iff_isRoot_charpoly
#check Module.End.HasEigenvalue
#check Module.End.hasEigenvalue_iff_mem_spectrum
