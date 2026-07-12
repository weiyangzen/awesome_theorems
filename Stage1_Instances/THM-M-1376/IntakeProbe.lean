import Mathlib.Dynamics.Ergodic.Conservative

/-!
# THM-M-1376 discovery-only intake probe

These checks authenticate pinned finite-measure, measure-preservation, conservativity, and
recurrence interfaces adjacent to a future Poincare recurrence encoding. They do not select the
catalog's exact statement, import the duplicate target, or prove THM-M-1376.
-/

open Filter Set

#check MeasureTheory.IsFiniteMeasure
#check MeasureTheory.MeasurePreserving
#check MeasureTheory.Conservative
#check MeasureTheory.MeasurePreserving.conservative
#check MeasureTheory.Conservative.exists_mem_iterate_mem
#check MeasureTheory.Conservative.frequently_measure_inter_ne_zero
#check MeasureTheory.Conservative.ae_mem_imp_frequently_image_mem
#check MeasureTheory.Conservative.ae_forall_image_mem_imp_frequently_image_mem
#check MeasureTheory.Conservative.ae_frequently_mem_of_mem_nhds

/- The exact type printed here belongs to the duplicate target's candidate expression. Repeating
its type as an API check neither imports that target nor transfers its scope or evidence. -/
#check (fun (alpha : Type) [MeasurableSpace alpha] =>
  forall (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
    MeasureTheory.IsFiniteMeasure mu ->
      MeasureTheory.MeasurePreserving f mu mu ->
        forall s : Set alpha,
          MeasureTheory.NullMeasurableSet s mu ->
            ∀ᵐ x ∂mu, x ∈ s -> ∃ᶠ n in atTop, f^[n] x ∈ s)
