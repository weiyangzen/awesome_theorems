import Mathlib.Probability.BorelCantelli

/-!
# THM-M-1009 anchor elaboration checks

This file checks the exact nearby declarations found by the anchor audit.  None
has the generalized Erdos-Renyi lower-bound type frozen in `Statement.lean`.
-/

#check ProbabilityTheory.measure_limsup_eq_one
#check MeasureTheory.ae_mem_limsup_atTop_iff
#check MeasureTheory.measure_limsup_atTop_eq_zero
#check ProbabilityTheory.iIndepSet.condExp_indicator_filtrationOfSet_ae_eq

