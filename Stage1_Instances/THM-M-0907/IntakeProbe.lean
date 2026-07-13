import Mathlib.Combinatorics.Digraph.Orientation
import Mathlib.Combinatorics.Nullstellensatz
import Mathlib.Combinatorics.SimpleGraph.Coloring

/-!
# THM-M-0907 discovery-only intake probe

These checks authenticate adjacent pinned digraph, ordinary-coloring, and generic polynomial APIs.
They do not define list coloring, Eulerian spanning-subdigraph parity counts, the graph polynomial,
or an Alon-Tarsi target.
-/

#check Digraph
#check Digraph.toSimpleGraphInclusive
#check SimpleGraph.Coloring
#check SimpleGraph.Coloring.mk
#check SimpleGraph.Colorable
#check MvPolynomial.eq_zero_of_eval_zero_at_prod_finset
#check MvPolynomial.combinatorial_nullstellensatz_exists_linearCombination
#check MvPolynomial.combinatorial_nullstellensatz_exists_eval_nonzero
