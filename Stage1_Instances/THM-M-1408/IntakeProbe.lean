import Mathlib.Probability.ProductMeasure
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy

/-! Discovery-only API checks for a later exact Ornstein isomorphism statement. -/

open MeasureTheory

#check Measure.infinitePi
#check measurePreserving_eval_infinitePi
#check MeasurePreserving
#check MeasurableEquiv
#check MeasurePreserving.symm
#check Real.negMulLog
#check Real.negMulLog_zero
#check Real.binEntropy

