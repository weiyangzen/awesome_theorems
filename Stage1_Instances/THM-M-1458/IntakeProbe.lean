import Mathlib.Analysis.Fourier.FiniteAbelian.PontryaginDuality
import Mathlib.Analysis.Fourier.ZMod

/-!
# THM-M-1458 discovery-only intake probe

These checks authenticate pinned dense DFT, inversion, and finite-character interfaces. They do
not select an FFT theorem, define a fast algorithm, prove algorithmic correctness, or establish a
complexity bound.
-/

#check ZMod.dft
#check ZMod.dft_apply
#check ZMod.dft_def
#check ZMod.invDFT_apply
#check ZMod.dft_dft
#check AddChar.zmod
#check AddChar.zmodAddEquiv
#check AddChar.complexBasis

#print axioms ZMod.dft_dft
#print axioms AddChar.zmodAddEquiv
