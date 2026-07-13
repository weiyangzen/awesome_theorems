import Mathlib.Combinatorics.SimpleGraph.Coloring

/-!
# THM-M-0833 discovery-only intake probe

These checks authenticate pinned simple-graph coloring interfaces adjacent to a possible future
Four Color statement. They do not define graph planarity, select a graph/map representation,
perform the downstream anchor audit, or prove the Four Color Theorem.
-/

#check SimpleGraph
#check SimpleGraph.Coloring
#check SimpleGraph.Coloring.mk
#check SimpleGraph.Coloring.valid
#check SimpleGraph.Colorable
#check SimpleGraph.colorable_iff_exists_bdd_nat_coloring
#check SimpleGraph.chromaticNumber
#check SimpleGraph.chromaticNumber_le_iff_colorable

#print axioms SimpleGraph.colorable_iff_exists_bdd_nat_coloring
#print axioms SimpleGraph.chromaticNumber_le_iff_colorable

