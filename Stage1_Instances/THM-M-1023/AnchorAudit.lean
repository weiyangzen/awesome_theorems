import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1023 anchor probes

These checks bind the anchor inventory to the APIs actually present in the
pinned mathlib snapshot. They do not prove the Levy-Khinchin theorem.
-/

open MeasureTheory

#check MeasureTheory.charFun
#check MeasureTheory.charFun_apply_real
#check MeasureTheory.charFun_dirac
#check MeasureTheory.charFun_conv
#check MeasureTheory.Measure.ext_of_charFun
#check MeasureTheory.norm_charFun_le_one

example {mu nu : Measure Real} [IsFiniteMeasure mu] [IsFiniteMeasure nu] (t : Real) :
    charFun (mu ∗ nu) t = charFun mu t * charFun nu t := by
  exact charFun_conv t

example {mu nu : Measure Real} [IsFiniteMeasure mu] [IsFiniteMeasure nu]
    (h : charFun mu = charFun nu) : mu = nu := by
  exact Measure.ext_of_charFun h
