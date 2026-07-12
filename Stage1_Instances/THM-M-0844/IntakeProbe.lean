import Mathlib.Combinatorics.SetFamily.Shatter
import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma

/-!
# THM-M-0844 discovery-only intake probe

These checks authenticate pinned APIs adjacent to possible future Alon-Fischer-Newman graph
regularity or property-testing encodings. They do not select the catalog proposition, connect a
graph's neighborhood family to VC dimension, define a property tester, or prove THM-M-0844.
-/

#check Finset.Shatters
#check Finset.vcDim
#check SimpleGraph.IsBipartite
#check SimpleGraph.edgeDensity
#check SimpleGraph.IsUniform
#check Finpartition
#check Finpartition.IsUniform
#check szemeredi_regularity
