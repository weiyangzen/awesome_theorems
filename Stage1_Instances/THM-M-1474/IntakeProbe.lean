import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.Analysis.Normed.Algebra.Spectrum

/-!
# THM-M-1474 discovery-only intake probe

These checks authenticate pinned L2 Fourier-isometry, Plancherel, and abstract spectral-radius
interfaces. They do not define a finite-difference grid, scheme, symbol, amplification factor, or
stability predicate, select a source proposition, or prove a von Neumann stability theorem.
-/

#check MeasureTheory.Lp.fourierTransformₗᵢ
#check MeasureTheory.Lp.norm_fourier_eq
#check spectralRadius
#check spectrum.spectralRadius_le_nnnorm

#print axioms MeasureTheory.Lp.norm_fourier_eq
#print axioms spectrum.spectralRadius_le_nnnorm
