import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Combinatorics.SimpleGraph.LapMatrix

/-!
# THM-M-0887 discovery-only intake probe

These checks authenticate pinned finite-simple-graph, adjacency/Laplacian, walk-count, Hermitian
eigenvalue, and algebraic-spectrum interfaces adjacent to spectral graph theory. They do not select
one source proposition, define a canonical target, or prove THM-M-0887.
-/

#check SimpleGraph
#check SimpleGraph.adjMatrix
#check SimpleGraph.isHermitian_adjMatrix
#check Matrix.IsHermitian.eigenvalues
#check SimpleGraph.adjMatrix_pow_apply_eq_card_walk
#check SimpleGraph.lapMatrix
#check SimpleGraph.posSemidef_lapMatrix
#check SimpleGraph.card_connectedComponent_eq_finrank_ker_toLin'_lapMatrix
#check Matrix.IsHermitian.eigenvalues_mem_spectrum_real
