import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Combinatorics.SimpleGraph.LapMatrix
import Mathlib.Data.Real.Sqrt
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Projective
import Mathlib.LinearAlgebra.Matrix.ProjectiveSpecialLinearGroup
import Mathlib.NumberTheory.LegendreSymbol.Basic

/-!
# THM-M-0883 discovery-only intake probe

These checks authenticate pinned graph, spectrum, projective-linear-group,
quadratic-residue, and square-root interfaces adjacent to a future source-frozen
LPS statement. They do not define the LPS generators or graph and prove no theorem.
-/

#check SimpleGraph
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.adjMatrix
#check SimpleGraph.isHermitian_adjMatrix
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.eigenvalues_mem_spectrum_real
#check Matrix.ProjectiveSpecialLinearGroup
#check Matrix.ProjGenLinGroup
#check legendreSym
#check legendreSym.eq_one_iff
#check Real.sqrt
