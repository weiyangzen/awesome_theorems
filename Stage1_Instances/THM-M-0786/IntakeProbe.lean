import Mathlib.MeasureTheory.Constructions.Pi

/-! A narrow API probe only. It is not a statement or proof of Borel determinacy. -/

namespace Stage1Instances.THM_M_0786.IntakeProbe

abbrev Play := ℕ → ℕ

#check Play
#check Set Play
#check MeasurableSet
#check @MeasurableSet Play inferInstance

example : TopologicalSpace Play := inferInstance
example : MeasurableSpace Play := inferInstance

end Stage1Instances.THM_M_0786.IntakeProbe
