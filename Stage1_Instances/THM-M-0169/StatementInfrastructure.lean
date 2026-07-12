import Mathlib.Geometry.Manifold.Immersion
import Mathlib.Geometry.Manifold.VectorBundle.Riemannian

/-!
Kernel-checked infrastructure probe for the THM-M-0169 statement gate.

Pinned mathlib can express smooth manifold immersions and smooth Riemannian vector bundles. It does
not expose the Gaussian/sectional-curvature, Levi-Civita connection, induced metric, or Riemannian
completeness interfaces needed to encode Hilbert's theorem. Accordingly this file declares no
canonical target, axiom, proof, or proxy predicate.
-/

namespace Stage1Instances.THM_M_0169.StatementInfrastructure

#check Manifold.IsImmersion
#check Bundle.RiemannianBundle
#check IsContMDiffRiemannianBundle
#check Fin 3 -> Real
#check CompleteSpace

end Stage1Instances.THM_M_0169.StatementInfrastructure
