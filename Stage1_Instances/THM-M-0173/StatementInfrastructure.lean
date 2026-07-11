import Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary
import Mathlib.Topology.VectorBundle.FiniteDimensional

/-!
# THM-M-0173 statement-infrastructure probe

Pinned mathlib can express smooth boundaryless manifolds and finite-rank topological complex vector
bundles. It does not currently expose the remaining objects needed by the intake-selected target:
a differential operator between smooth bundle sections, its principal symbol and ellipticity, its
Fredholm analytic index, the compactly supported K-theory symbol class, or its topological
pushforward index.

Consequently this module deliberately does not declare a canonical target. Introducing locally
invented integer-valued fields named after the two indices would weaken the mathematical claim to
an unrelated equality about an unconstrained record.
-/

namespace Stage1Instances.THM_M_0173.StatementInfrastructure

#check IsManifold
#check BoundarylessManifold
#check CompactSpace
#check FiberBundle
#check VectorBundle
#check FiniteDimensional

end Stage1Instances.THM_M_0173.StatementInfrastructure
