import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic

/-!
# THM-M-1152 statement-boundary probe

This file checks only one possible pinned classical harmonic-function substrate.
The repository wording does not determine a closed Perron theorem, so this file
deliberately does not declare a canonical target or a Perron solution interface.
-/

#check Laplacian.laplacian
#check InnerProductSpace.HarmonicAt
#check InnerProductSpace.HarmonicOnNhd
