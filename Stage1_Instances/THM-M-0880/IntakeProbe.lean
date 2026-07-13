import Mathlib.Combinatorics.SimpleGraph.Connectivity.EdgeConnectivity
import Mathlib.Combinatorics.SimpleGraph.Density
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Partition

/-!
# THM-M-0880 discovery-only intake probe

These checks authenticate pinned finite-simple-graph interfaces adjacent to possible future cut
statements. `SimpleGraph.Partition` is a coloring partition into independent sets, not a sparse-cut
definition. This file does not choose a sparsity objective, define the catalog target, or prove it.
-/

#check SimpleGraph.edgeSet
#check SimpleGraph.mem_edgeSet
#check SimpleGraph.edgeFinset
#check SimpleGraph.coe_edgeFinset
#check SimpleGraph.interedges
#check SimpleGraph.mem_interedges_iff
#check SimpleGraph.edgeDensity
#check SimpleGraph.edgeDensity_nonneg
#check SimpleGraph.edgeDensity_le_one
#check SimpleGraph.neighborFinset
#check SimpleGraph.degree
#check SimpleGraph.induce
#check SimpleGraph.map_edgeFinset_induce
#check SimpleGraph.IsEdgeConnected
#check SimpleGraph.isEdgeConnected_one
#check SimpleGraph.Partition
#check SimpleGraph.Partitionable
#check SimpleGraph.partitionable_iff_colorable

#print axioms SimpleGraph.map_edgeFinset_induce
#print axioms SimpleGraph.edgeDensity_le_one
#print axioms SimpleGraph.isEdgeConnected_one
#print axioms SimpleGraph.partitionable_iff_colorable
