import Mathlib.MeasureTheory.Constructions.Pi

/-! The external project is not imported; these are the pinned statement APIs. -/

/-!
# THM-M-0786 anchor-audit probe

This probe re-elaborates the frozen target in the pinned local environment.
The external BorelDet project is not a local dependency, so no external
declaration is imported or credited here.
-/

#check MeasurableSet
#check (inferInstance : MeasurableSpace (ℕ → ℕ))
