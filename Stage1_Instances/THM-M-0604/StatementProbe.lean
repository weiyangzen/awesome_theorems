import Mathlib.Geometry.Manifold.Bordism

/-!
Elaboration probe for the THM-M-0604 exact-statement blocker.

The pinned module provides only the precursor type and representative-level
operations. It explicitly leaves the bordism relation, quotient groups, and
ring structure as future work, so none of these declarations is promoted to a
canonical target.
-/

#check SingularManifold
#check SingularManifold.empty
#check SingularManifold.toPUnit
#check SingularManifold.sum
#check SingularManifold.prod
