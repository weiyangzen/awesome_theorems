import Mathlib.MeasureTheory.Function.Egorov

/-!
# THM-M-0286 discovery-only intake probe

These commands authenticate the direct Egorov interfaces in the pinned mathlib snapshot. They do
not select one interface as the catalog root, establish source-statement identity, or prove a new
target.
-/

#check MeasureTheory.Egorov.notConvergentSeq
#check MeasureTheory.tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist
#check MeasureTheory.tendstoUniformlyOn_of_ae_tendsto
#check MeasureTheory.tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist'
#check MeasureTheory.tendstoUniformlyOn_of_ae_tendsto'

#print axioms MeasureTheory.tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist
#print axioms MeasureTheory.tendstoUniformlyOn_of_ae_tendsto
#print axioms MeasureTheory.tendstoUniformlyOn_of_ae_tendsto'
