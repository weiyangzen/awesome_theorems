import Mathlib.Algebra.Lie.Semisimple.Defs
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Geometry.Manifold.Algebra.LieGroup
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Measure.Haar.Basic
import Mathlib.RepresentationTheory.Character

/-!
# THM-M-0097 discovery-only intake probe

These checks authenticate adjacent pinned semisimple-Lie-algebra, manifold Lie-group, algebraic
representation, Haar-measure, local-integrability, test-function, and distribution APIs. They do
not define a Harish-Chandra distribution character, select a source theorem, or prove THM-M-0097.
-/

#check LieAlgebra.IsSemisimple
#check LieGroup
#check Representation
#check Representation.character
#check MeasureTheory.Measure.haarMeasure
#check MeasureTheory.LocallyIntegrable
#check TestFunction
#check Distribution
