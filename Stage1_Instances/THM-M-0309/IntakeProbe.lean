import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.Normed.Operator.Compact
import Mathlib.MeasureTheory.Function.LpSpace.Complete

/-!
# THM-M-0309 discovery-only intake probe

These checks authenticate adjacent pinned `L^p`, compact-operator, and Sobolev-inequality APIs.
They do not select, state, or prove a Rellich-Kondrachov compact embedding theorem.
-/

#check MeasureTheory.Lp
#check MeasureTheory.MemLp
#check IsCompactOperator
#check IsCompactOperator.isCompact_closure_image_of_bounded
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le
