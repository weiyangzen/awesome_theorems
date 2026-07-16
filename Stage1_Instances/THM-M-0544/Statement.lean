import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0544 statement boundary probe

The intended root is the classical unique-harmonic-representative form of the Hodge theorem for
real de Rham cohomology on compact oriented boundaryless Riemannian manifolds. The pinned library
does not yet provide bundled smooth manifold differential forms or the de Rham and Hodge operators
needed to type that proposition. This module therefore checks only the adjacent pinned interfaces.
It deliberately declares no canonical target, transport, mutation fixture, axiom, or placeholder.
-/

namespace Stage1Instances.THM_M_0544

#check ModelWithCorners
#check IsManifold
#check CompactSpace
#check IsRiemannianManifold
#check extDeriv

end Stage1Instances.THM_M_0544
