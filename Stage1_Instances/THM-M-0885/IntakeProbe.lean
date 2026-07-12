import Mathlib.Combinatorics.SimpleGraph.LapMatrix
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Data.Real.Sqrt

/-!
Discovery-only API checks for a later source-frozen Morgenstern statement.

These are adjacent graph and spectral interfaces. They neither define the
source-specific Ramanujan predicate nor state or prove Morgenstern's theorem.
-/

#check SimpleGraph
#check SimpleGraph.degree
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.adjMatrix
#check SimpleGraph.isHermitian_adjMatrix
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.eigenvalues_mem_spectrum_real
#check Real.sqrt
