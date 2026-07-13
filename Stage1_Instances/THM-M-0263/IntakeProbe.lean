import Mathlib.Data.Real.Archimedean
import Mathlib.Topology.UniformSpace.Real

/-!
# THM-M-0263 discovery-only intake probe

These checks authenticate distinct pinned order-completeness and metric-completeness interfaces for
the real numbers. They do not select one interpretation of the catalog gloss, establish a checked
source transport, or claim proof credit for THM-M-0263.
-/

#check Real.exists_isLUB
#check Real.exists_isGLB
#check Real.isLUB_sSup
#check Real.instConditionallyCompleteLinearOrder
#check Real.instCompleteSpace
#check cauchySeq_tendsto_of_complete

#synth ConditionallyCompleteLinearOrder Real
#synth CompleteSpace Real

#print axioms Real.exists_isLUB
#print axioms Real.isLUB_sSup
#print axioms Real.instConditionallyCompleteLinearOrder
#print axioms Real.instCompleteSpace
#print axioms cauchySeq_tendsto_of_complete
