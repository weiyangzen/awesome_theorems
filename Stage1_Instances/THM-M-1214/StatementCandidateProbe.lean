import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# THM-M-1214 statement candidate probe

This file checks only that the analysis substrates used by the historical
Cazenave-Weissler discovery boundary are present in the pinned environment.
The historical module does not identify a source theorem, so nothing here is a
canonical target.
-/

#check Distribution
#check MeasureTheory.MemLp
#check MeasureTheory.MemLp.toLp
#check Laplacian.laplacian
