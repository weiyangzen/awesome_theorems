import Mathlib.Topology.Algebra.Module.LocallyConvex
import Mathlib.Topology.Algebra.Module.StrongTopology

/-!
This file checks the two independent pinned mathlib substrates nearest to the
intended theorem. It is deliberately not a canonical statement: pinned mathlib
has no nuclear locally convex space predicate with which to connect them.
-/

#check LocallyConvexSpace
#check CompactConvergenceCLM
#check UniformConvergenceCLM.tendsto_iff_tendstoUniformlyOn
