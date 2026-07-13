import Mathlib.MeasureTheory.OuterMeasure.BorelCantelli
import Mathlib.Probability.BorelCantelli

/-!
# THM-M-0285 discovery-only intake probe

The repository gloss does not choose the first Borel-Cantelli lemma, the second lemma, or a
conjunction. These checks authenticate the two adjacent pinned mathlib endpoints only. They do not
select a canonical statement, establish a source transport, or prove the repository target.
-/

#check MeasureTheory.measure_limsup_atTop_eq_zero
#check MeasureTheory.ae_finite_setOf_mem
#check ProbabilityTheory.measure_limsup_eq_one
#check MeasureTheory.ae_mem_limsup_atTop_iff

#print axioms MeasureTheory.measure_limsup_atTop_eq_zero
#print axioms ProbabilityTheory.measure_limsup_eq_one
