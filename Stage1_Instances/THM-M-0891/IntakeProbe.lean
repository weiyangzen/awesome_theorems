import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Combinatorics.SimpleGraph.LapMatrix

/-!
# THM-M-0891 discovery-only intake probe

These checks authenticate pinned graph-coloring, adjacency-matrix, connectedness, and Hermitian
eigenvalue interfaces adjacent to a future source-faithful Wilf statement. They do not select an
eigenvalue/chromatic-number encoding, define the equality cases, or prove THM-M-0891.
-/

#check SimpleGraph.Colorable
#check SimpleGraph.chromaticNumber
#check SimpleGraph.chromaticNumber_le_iff_colorable
#check SimpleGraph.adjMatrix
#check SimpleGraph.isHermitian_adjMatrix
#check Matrix.IsHermitian.eigenvalues₀
#check Matrix.IsHermitian.eigenvalues₀_antitone
#check Matrix.IsHermitian.eigenvalues
#check SimpleGraph.Connected
#check SimpleGraph.completeGraph
