import Mathlib.Analysis.Calculus.VectorField
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# THM-M-1259 anchor audit

These checks identify the pinned mathlib declarations that can support the frozen target. They do
not assert Hormander's theorem and do not supply a proof of `hormanderTarget`.
-/

#check VectorField.lieBracket
#check ContDiff.lieBracket_vectorField
#check Distribution
#check MeasureTheory.eLpNorm
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv

