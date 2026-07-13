import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.LapMatrix
import Mathlib.Combinatorics.SimpleGraph.Metric

/-!
# THM-M-0889 discovery-only intake probe

These checks authenticate pinned finite-simple-graph, distance, degree, adjacency-matrix,
Laplacian, positivity, and Hermitian-spectrum interfaces adjacent to a future source-faithful
encoding. They do not define an expansion invariant or spectral gap, choose a numbered
Alon-Milman result, or prove THM-M-0889.
-/

#check SimpleGraph
#check SimpleGraph.edgeFinset
#check SimpleGraph.neighborFinset
#check SimpleGraph.degree
#check SimpleGraph.maxDegree
#check SimpleGraph.dist
#check SimpleGraph.adjMatrix
#check SimpleGraph.lapMatrix
#check SimpleGraph.isHermitian_lapMatrix
#check SimpleGraph.posSemidef_lapMatrix
#check Matrix.IsHermitian.eigenvalues
