import Mathlib.Topology.ContinuousMap.Bounded.ArzelaAscoli
import Mathlib.Topology.UniformSpace.Ascoli

/-!
# THM-M-0267 discovery-only intake probe

These checks authenticate direct named interfaces in the pinned mathlib snapshot. They do not
select an Arzela-Ascoli variant as the catalog root, establish statement identity, or prove the
target.
-/

#check BoundedContinuousFunction.arzela_ascoli₁
#check BoundedContinuousFunction.arzela_ascoli₂
#check BoundedContinuousFunction.arzela_ascoli
#check ArzelaAscoli.compactSpace_of_isClosedEmbedding
#check ArzelaAscoli.isCompact_closure_of_isClosedEmbedding
#check ArzelaAscoli.isCompact_of_equicontinuous

#print axioms BoundedContinuousFunction.arzela_ascoli
#print axioms ArzelaAscoli.isCompact_closure_of_isClosedEmbedding
#print axioms ArzelaAscoli.isCompact_of_equicontinuous
