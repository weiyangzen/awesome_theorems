import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-!
Elaboration witnesses for the supporting mathlib surfaces found by the
THM-M-1235 anchor audit. These are object-model anchors only; none states or
proves Wolibner's global existence and uniqueness theorem.
-/

open MeasureTheory

#check EuclideanSpace
#check fderiv
#check ContDiff
#check MeasureTheory.MemLp
#check MeasureTheory.Integrable
#check Laplacian.laplacian
#check MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable

