import Mathlib.Geometry.Manifold.Immersion
import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
Kernel-checked infrastructure probe for the THM-M-0160 statement gate.

The repository source does not determine an exact version of the fundamental theorem of surface
theory. Accordingly, this module does not declare a canonical target. It checks only that the
pinned environment exposes manifold immersions and Riemannian metrics. It does not invent a second
fundamental form, Gauss-Codazzi compatibility predicate, realization relation, or uniqueness
statement.
-/

namespace Stage1Instances.THM_M_0160.StatementInfrastructure

#check Manifold.IsImmersion
#check IsContMDiffRiemannianBundle

end Stage1Instances.THM_M_0160.StatementInfrastructure
