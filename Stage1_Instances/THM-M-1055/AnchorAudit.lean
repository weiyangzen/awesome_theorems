import Mathlib.Dynamics.BirkhoffSum.NormedSpace
import Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1055 pinned anchor probes

This module elaborates the mathlib declarations used by the anchor audit. It
does not assert the pointwise Birkhoff theorem.
-/

open Filter MeasureTheory

#check birkhoffSum
#check birkhoffAverage
#check birkhoffAverage_add
#check birkhoffAverage_neg
#check birkhoffAverage_sub
#check Function.IsFixedPt.tendsto_birkhoffAverage
#check MeasureTheory.Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq
#check MeasureTheory.MeasurePreserving
#check Ergodic
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae
#check Integrable
#check MeasureTheory.AEStronglyMeasurable
#print axioms Function.IsFixedPt.tendsto_birkhoffAverage
#print axioms MeasureTheory.Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq
#print axioms Ergodic.ae_eq_const_of_ae_eq_comp_ae
