import Mathlib.Algebra.Order.Rearrangement
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Function.LpSeminorm.Defs

open scoped ENNReal

-- These are the closest pinned mathlib declarations found by the anchor audit.
-- The checks make their actual interfaces explicit; none constructs a Schwarz
-- rearrangement or proves the frozen weak-gradient energy comparison.
#check MonovaryOn.sum_smul_comp_perm_le_sum_smul
#check AntivaryOn.sum_smul_le_sum_smul_comp_perm
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
