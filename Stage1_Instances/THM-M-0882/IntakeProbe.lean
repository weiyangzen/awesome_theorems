import Mathlib.Combinatorics.SimpleGraph.AdjMatrix
import Mathlib.Data.ZMod.Basic

/-!
# THM-M-0882 discovery-only intake probe

These checks authenticate nearby pinned graph and modular-arithmetic APIs. They neither select a
Margulis graph construction nor state or prove an expansion theorem.
-/

#check SimpleGraph
#check SimpleGraph.fromRel
#check SimpleGraph.neighborSet
#check SimpleGraph.neighborFinset
#check SimpleGraph.degree
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.adjMatrix
#check ZMod
#check ZMod.card
