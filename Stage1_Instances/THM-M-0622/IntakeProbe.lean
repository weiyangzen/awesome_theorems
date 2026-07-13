import Mathlib.Topology.TietzeExtension

/-!
# THM-M-0622 discovery-only intake probe

These checks authenticate pinned Tietze-extension interfaces and expose the choices omitted by the
catalog. They do not select a canonical target, add a theorem declaration, or claim proof credit.
-/

#check NormalSpace
#check T4Space
#check TietzeExtension
#check ContinuousMap.exists_restrict_eq
#check ContinuousMap.exists_extension
#check BoundedContinuousFunction.exists_extension_norm_eq_of_isClosedEmbedding
#check BoundedContinuousFunction.exists_norm_eq_restrict_eq_of_closed
#check ContinuousMap.exists_restrict_eq_forall_mem_of_closed
#check Real.instTietzeExtension

#print axioms ContinuousMap.exists_restrict_eq
#print axioms Real.instTietzeExtension
