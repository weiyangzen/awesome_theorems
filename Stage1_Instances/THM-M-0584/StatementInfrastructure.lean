import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Geometry.Manifold.Bordism
import Mathlib.LinearAlgebra.BilinearForm.Properties

/-!
Kernel-checked infrastructure probe for the THM-M-0584 statement gate.

Pinned mathlib has separate APIs for closed smooth manifolds, singular homology, and integral
bilinear forms. It does not provide the construction of a four-manifold's integral intersection
form needed to state Donaldson's theorem. Accordingly this file declares no canonical theorem,
axiom, proxy predicate, or proof.
-/

namespace Stage1Instances.THM_M_0584.StatementInfrastructure

#check SingularManifold
#check AlgebraicTopology.singularHomologyFunctor
#check LinearMap.BilinForm
#check LinearMap.BilinForm.IsSymm
#check LinearMap.BilinForm.IsNonneg

end Stage1Instances.THM_M_0584.StatementInfrastructure
