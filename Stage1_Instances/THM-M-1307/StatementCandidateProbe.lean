import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.LineDeriv.Basic
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.FourierMultiplier
import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-1307 statement candidate probe

This probe checks that the eight direct mathlib imports used by the historical
Stage1 discovery module are available in the pinned Lean environment. These
analysis substrates do not identify the source theorem and receive no
statement or proof credit here.
-/

#check deriv
#check lineDeriv
#check Laplacian.laplacian
#check MeasureTheory.MemLp
#check Distribution
#check TemperedDistribution.laplacian_eq_fourierMultiplierCLM
