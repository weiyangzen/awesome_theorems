import Mathlib.Combinatorics.Graph.Basic
import Mathlib.Probability.Distributions.Uniform

/-!
# THM-M-0831 discovery-only intake probe

These checks authenticate pinned multigraph and finite uniform-sampling interfaces that could
support a future Karger contraction model. They do not define graph contraction or cuts, choose a
canonical theorem, implement Karger's algorithm, or prove a probability or complexity bound.
-/

#check Graph
#check Graph.IsLink
#check Graph.Inc
#check Graph.Adj
#check Graph.IsLoopAt
#check Graph.banana
#check PMF.uniformOfFinset
#check PMF.uniformOfFinset_apply
#check PMF.ofMultiset
#check PMF.ofMultiset_apply
