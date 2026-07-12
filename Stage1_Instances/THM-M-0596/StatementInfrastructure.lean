import Mathlib.Geometry.Manifold.Bordism
import Mathlib.Topology.Baire.Lemmas

/-!
Kernel-checked infrastructure probe for the THM-M-0596 statement blocker.

The pinned library has separate smooth-manifold and residual-set substrates, and its bordism
module mentions transversality only as missing future infrastructure. This file deliberately does
not manufacture a transversality predicate, mapping-space topology, or canonical theorem.
-/

namespace Stage1Instances.THM_M_0596.StatementInfrastructure

#check ContMDiff
#check mfderiv
#check residual
#check mem_residual
#check SingularManifold

end Stage1Instances.THM_M_0596.StatementInfrastructure
