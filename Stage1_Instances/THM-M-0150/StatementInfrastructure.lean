import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
Kernel-checked infrastructure probe for the THM-M-0150 statement gate.

The pinned library can state that a morphism of schemes is smooth or proper. It does not provide
the canonical sheaf/divisor, its tensor powers and section ring, or a general-type predicate needed
for the canonical target. This file therefore declares no substitute target.
-/

namespace Stage1Instances.THM_M_0150.StatementInfrastructure

open AlgebraicGeometry

universe u

/-- The available scheme-level part of the intended geometric input. -/
def SmoothProper (X S : Scheme.{u}) (f : X ⟶ S) : Prop := Smooth f ∧ IsProper f

#check Scheme
#check Smooth
#check IsProper
#check Algebra.FiniteType

end Stage1Instances.THM_M_0150.StatementInfrastructure
