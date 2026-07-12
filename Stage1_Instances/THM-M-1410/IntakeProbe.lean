import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.MeasureTheory.Constructions.Polish.Basic
import Mathlib.MeasureTheory.Measure.AEDisjoint
import Mathlib.MeasureTheory.Measure.Typeclasses.NoAtoms

/-! Discovery-only checks for adjacent APIs; this file states no Rokhlin theorem. -/

#check MeasureTheory.MeasurePreserving
#check MeasureTheory.MeasurePreserving.iterate
#check MeasureTheory.Measure.QuasiMeasurePreserving
#check Ergodic
#check Function.periodicPts
#check StandardBorelSpace
#check MeasureTheory.IsProbabilityMeasure
#check MeasureTheory.NoAtoms
#check MeasureTheory.AEDisjoint
