import Mathlib.Combinatorics.SimpleGraph.Coloring

/-!
# THM-M-0908 discovery-only intake probe

These checks authenticate the pinned ordinary graph-coloring substrate. They do not define list
coloring or planarity, select a source statement, freeze a canonical Lean target, audit a proof
body, or prove Thomassen's theorem.
-/

#check SimpleGraph
#check SimpleGraph.Coloring
#check SimpleGraph.Coloring.mk
#check SimpleGraph.Coloring.valid
#check SimpleGraph.Colorable
#check SimpleGraph.Colorable.mono
#check SimpleGraph.chromaticNumber
#check SimpleGraph.chromaticNumber_le_iff_colorable
