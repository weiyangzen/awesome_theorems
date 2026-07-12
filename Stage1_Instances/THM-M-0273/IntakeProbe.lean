import Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym
import Mathlib.MeasureTheory.VectorMeasure.Decomposition.RadonNikodym

/-!
# THM-M-0273 discovery-only intake probe

These commands authenticate the pinned positive-measure Radon-Nikodym interfaces. They do not
select the catalogue's exact statement, establish a source-to-Lean transport, or prove the target.
-/

#check MeasureTheory.Measure
#check MeasureTheory.Measure.AbsolutelyContinuous
#check MeasureTheory.Measure.HaveLebesgueDecomposition
#check MeasureTheory.Measure.rnDeriv
#check MeasureTheory.Measure.withDensity_rnDeriv_eq
#check MeasureTheory.Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq
#check MeasureTheory.Measure.haveLebesgueDecomposition_of_finiteMeasure
#check MeasureTheory.Measure.haveLebesgueDecomposition_of_sigmaFinite
#check MeasureTheory.SignedMeasure.rnDeriv
#check MeasureTheory.SignedMeasure.absolutelyContinuous_iff_withDensityᵥ_rnDeriv_eq

#print axioms MeasureTheory.Measure.withDensity_rnDeriv_eq
#print axioms MeasureTheory.Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq
#print axioms MeasureTheory.SignedMeasure.absolutelyContinuous_iff_withDensityᵥ_rnDeriv_eq
