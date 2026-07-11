import Mathlib.Algebra.Quaternion
import Mathlib.AlgebraicGeometry.Scheme

/-!
Kernel-checked infrastructure probe for the THM-M-0126 statement gate.

The repository source does not specify which Shimura-curve theorem is intended. Accordingly this
module does not declare a canonical target. It only checks that the pinned environment can express
a generic quaternion algebra and the type of schemes, without choosing a base field, order, level,
moduli problem, or geometric conclusion.
-/

namespace Stage1Instances.THM_M_0126.StatementInfrastructure

universe u

/-- The generic quaternion-algebra type constructor available in pinned mathlib. -/
abbrev QuaternionAlgebraCarrier (R : Type u) [CommRing R] (a b c : R) : Type u :=
  QuaternionAlgebra R a b c

/-- The scheme type available in pinned mathlib. This does not select a Shimura moduli scheme. -/
abbrev SchemeCarrier : Type (u + 1) :=
  AlgebraicGeometry.Scheme.{u}

#check QuaternionAlgebra
#check AlgebraicGeometry.Scheme

end Stage1Instances.THM_M_0126.StatementInfrastructure
