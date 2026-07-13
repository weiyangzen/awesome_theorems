import Mathlib.MeasureTheory.Covering.Vitali
import Mathlib.MeasureTheory.Covering.Differentiation

/-!
# THM-M-0288 discovery-only intake probe

These commands authenticate distinct pinned covering and differentiation interfaces. They do not
select the catalogue's exact statement or bundle, establish a source-to-Lean transport or
composition, or prove the target.
-/

#check Vitali.exists_disjoint_subfamily_covering_enlargement
#check Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall
#check Vitali.exists_disjoint_covering_ae
#check Vitali.exists_disjoint_covering_ae'
#check Vitali.vitaliFamily
#check VitaliFamily.FineSubfamilyOn.exists_disjoint_covering_ae
#check VitaliFamily.ae_tendsto_rnDeriv
#check VitaliFamily.ae_tendsto_measure_inter_div
#check VitaliFamily.ae_tendsto_average_norm_sub
#check VitaliFamily.ae_tendsto_average

#print axioms Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall
#print axioms Vitali.exists_disjoint_covering_ae
#print axioms Vitali.vitaliFamily
#print axioms VitaliFamily.ae_tendsto_rnDeriv
#print axioms VitaliFamily.ae_tendsto_average
