import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Combinatorics.SimpleGraph.AdjMatrix
import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.LapMatrix
import Mathlib.Data.Matrix.PEquiv

/-!
# THM-M-0886 discovery-only intake probe

These checks authenticate pinned finite graph, bipartite, degree, adjacency-matrix, Hermitian
spectrum, multigraph, and permutation-matrix interfaces adjacent to a future source-faithful
encoding. They do not define a biregular Ramanujan graph, select an infinite-sequence encoding,
or prove THM-M-0886.
-/

#check SimpleGraph
#check Graph
#check SimpleGraph.IsBipartiteWith
#check SimpleGraph.IsBipartite
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.adjMatrix
#check SimpleGraph.isHermitian_adjMatrix
#check Matrix.IsHermitian.eigenvalues
#check Equiv.toPEquiv
#check PEquiv.toMatrix
