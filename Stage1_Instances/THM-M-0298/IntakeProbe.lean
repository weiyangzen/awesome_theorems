import Mathlib.MeasureTheory.Integral.Average
import Mathlib.MeasureTheory.Covering.Vitali
import Mathlib.MeasureTheory.Covering.BesicovitchVectorSpace
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# THM-M-0298 discovery-only intake probe

These commands authenticate pinned APIs adjacent to a future exact Calderon-Zygmund decomposition.
They do not select the catalogue statement, construct the decomposition, or prove the target.
-/

#check MeasureTheory.IntegrableOn
#check MeasureTheory.setAverage_eq
#check MeasureTheory.setIntegral_setAverage_sub
#check Real.volume_Icc_pi
#check Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall
#check HasBesicovitchCovering
#check Besicovitch.exists_disjoint_closedBall_covering_ae

#print axioms MeasureTheory.setIntegral_setAverage_sub
#print axioms Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall
#print axioms Besicovitch.exists_disjoint_closedBall_covering_ae
