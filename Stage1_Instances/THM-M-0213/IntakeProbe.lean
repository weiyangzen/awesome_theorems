import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
import Mathlib.Data.Set.Finite.Basic
import Mathlib.LinearAlgebra.AffineSpace.AffineMap

/-!
# THM-M-0213 discovery-only intake probe

These checks authenticate adjacent pinned hyperbolic-model, affine-line, and infinitude APIs. They
do not define hyperbolic lines or parallelism, select a synthetic geometric postulate system, state
the catalog claim, or supply proof credit.
-/

#check UpperHalfPlane
#check UpperHalfPlane.dist_eq
#check UpperHalfPlane.isometry_vertical_line
#synth MetricSpace UpperHalfPlane
#check AffineMap.lineMap
#check AffineMap.lineMap_injective
#check Set.Infinite
#check Set.Infinite.natEmbedding
