import Mathlib.Geometry.Manifold.Complex
import Mathlib.LinearAlgebra.Projectivization.Basic

/-!
# THM-M-0111 statement-infrastructure probe

This module checks the native complex-manifold and algebraic projectivization
surfaces available in the pinned dependency closure. It deliberately does not
declare a Kodaira embedding target: the closure has no native Kahler-manifold,
integral-to-de Rham comparison, or complex-projective-manifold embedding API,
and the target scope forbids replacing those notions with abstract predicates.
-/

noncomputable section

namespace Stage1Instances.THMM0111.StatementInfrastructure

/-- The algebraic carrier currently available for finite complex projective
space. Generic quotient topology can be exposed with additional definitions,
but the imported projectivization module exports no inferred topology,
projective charts, complex-manifold structure, or notion of holomorphic maps
into this carrier. -/
abbrev ComplexProjectiveCarrier (n : Nat) : Type :=
  Projectivization Complex (Fin (n + 1) -> Complex)

#check ModelWithCorners
#check IsManifold
#check MDifferentiable
#check CompactSpace
#check Projectivization
#check ComplexProjectiveCarrier
#check_failure (inferInstance : TopologicalSpace (ComplexProjectiveCarrier 1))
#check Topology.IsClosedEmbedding

end Stage1Instances.THMM0111.StatementInfrastructure
