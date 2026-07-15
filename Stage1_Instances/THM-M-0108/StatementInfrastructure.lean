import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Topology
import Mathlib.Analysis.Analytic.Polynomial
import Mathlib.Geometry.Manifold.Complex
import Mathlib.LinearAlgebra.Projectivization.Basic
import Mathlib.RingTheory.MvPolynomial.Homogeneous

/-!
# THM-M-0108 statement-infrastructure probe

This module checks the separate analytic, projective-carrier, homogeneous-
polynomial, and algebraic-zero-locus surfaces available in the pinned
dependency closure. It deliberately does not declare a Chow theorem target:
the closure has no native closed complex-analytic subvariety object on finite
complex projective space and no comparison with the algebraic zero-locus
surface. The imports are probe imports, not minimal-target evidence.
-/

noncomputable section

namespace Stage1Instances.THMM0108.StatementInfrastructure

/-- The bare algebraic quotient carrier available for finite-dimensional
complex projective space. The imported projectivization module supplies no
inferred topology or complex-manifold structure on this carrier. -/
abbrev ComplexProjectiveCarrier (n : Nat) : Type :=
  Projectivization Complex (Fin (n + 1) -> Complex)

#check ModelWithCorners
#check IsManifold
#check MDifferentiable
#check AnalyticOnNhd
#check AnalyticOnNhd.eval_mvPolynomial
#check MvPolynomial.IsHomogeneous
#check Projectivization
#check ComplexProjectiveCarrier
#check_failure (inferInstance : TopologicalSpace (ComplexProjectiveCarrier 1))

#check ProjectiveSpectrum
#check ProjectiveSpectrum.zeroLocus
#check ProjectiveSpectrum.vanishingIdeal
#check ProjectiveSpectrum.isClosed_iff_zeroLocus
#check ProjectiveSpectrum.zeroLocus_vanishingIdeal_eq_closure

end Stage1Instances.THMM0108.StatementInfrastructure
