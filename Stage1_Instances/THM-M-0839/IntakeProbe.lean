import Mathlib.Combinatorics.SimpleGraph.Coloring

/-!
# THM-M-0839 discovery-only intake probe

These checks authenticate pinned APIs needed by a possible finite-simple-graph encoding of the weak
perfect graph theorem. They do not define perfectness, select a canonical proposition, audit the
terminal proof body, or prove THM-M-0839.
-/

#check SimpleGraph.compl_adj
#check SimpleGraph.induce
#check SimpleGraph.chromaticNumber
#check SimpleGraph.cliqueNum
#check SimpleGraph.cliqueNum_le_chromaticNumber
#check SimpleGraph.cliqueNum_compl
