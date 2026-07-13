import Mathlib.Combinatorics.SimpleGraph.Density
import Mathlib.MeasureTheory.Constructions.UnitInterval

/-!
# THM-M-0847 discovery-only intake probe

These checks authenticate pinned finite-graph density and unit-interval probability-space APIs
adjacent to possible graphon encodings. They do not define a graphon, a cut norm or distance,
homomorphism density, equivalence under measure-preserving maps, graph convergence, compactness,
or a limit theorem.
-/

#check SimpleGraph
#check SimpleGraph.edgeDensity
#check Rel.edgeDensity
#check unitInterval
#check unitInterval.volume_def
#check unitInterval.measurePreserving_symm
#check MeasureTheory.Measure.prod
#check MeasureTheory.MeasurePreserving
#check MeasureTheory.IsProbabilityMeasure

#print axioms unitInterval.volume_def
#print axioms unitInterval.measurePreserving_symm
