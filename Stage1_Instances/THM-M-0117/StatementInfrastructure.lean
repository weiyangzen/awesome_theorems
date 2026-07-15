import Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.Analysis.Meromorphic.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.RingTheory.AlgebraicIndependent.Basic

/-!
# THM-M-0117 statement-infrastructure probe

This module checks the separate analytic, field-theoretic, and scheme-side
surfaces available in the pinned dependency closure. It deliberately does not
declare a Moishezon theorem target: the repository has not identified an exact
source statement, and the dependency closure has no native meromorphic-function
field or algebraic-dimension API for complex manifolds, no complex analytic
space or bimeromorphism interface, and no analytification comparison with a
projective algebraic variety. These imports are probe imports, not a minimal
import claim for the absent canonical target.
-/

namespace Stage1Instances.THMM0117.StatementInfrastructure

#check ModelWithCorners
#check IsManifold
#check CompactSpace
#check MDifferentiable
#check MDifferentiable.exists_eq_const_of_compactSpace

#check MeromorphicAt
#check MeromorphicOn
#check Meromorphic
#check Algebra.trdeg

#check AlgebraicGeometry.Scheme
#check AlgebraicGeometry.IsClosedImmersion
#check AlgebraicGeometry.IsProper
#check AlgebraicGeometry.Proj.toSpecZero

end Stage1Instances.THMM0117.StatementInfrastructure
