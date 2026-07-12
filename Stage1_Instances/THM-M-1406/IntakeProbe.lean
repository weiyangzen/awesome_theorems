import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog
import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.MeasureTheory.MeasurableSpace.MeasurablyGenerated
import Mathlib.MeasureTheory.Measure.PreVariation

/-!
# THM-M-1406 discovery-only intake probe

These checks authenticate nearby pinned APIs. They neither define
Kolmogorov-Sinai entropy nor select or prove a theorem about it.
-/

open MeasureTheory

universe u

variable {X : Type u} [MeasurableSpace X]

#check MeasurePreserving
#check MeasurePreserving.iterate
#check Ergodic
#check IsProbabilityMeasure
#check (Finpartition (⟨Set.univ, MeasurableSet.univ⟩ : Subtype MeasurableSet))
#check MeasurableSpace.generateFrom
#check MeasurableSpace.comap
#check Real.negMulLog
