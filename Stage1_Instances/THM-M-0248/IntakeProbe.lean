import Mathlib.Analysis.Complex.Basic
import Mathlib.Topology.ContinuousMap.StoneWeierstrass

/-!
# THM-M-0248 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for compact subsets of the complex plane,
continuous functions, closed subalgebras, and uniform-density statements. They do not define
rational functions with controlled poles, Bishop's minimal boundary, or a target theorem.
-/

#check Complex
#check IsCompact
#check interior
#check ContinuousMap
#check Subalgebra.SeparatesPoints
#check ContinuousMap.subalgebra_topologicalClosure_eq_top_of_separatesPoints
#check ContinuousMap.continuousMap_mem_subalgebra_closure_of_separatesPoints
