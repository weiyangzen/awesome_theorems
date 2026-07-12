import Mathlib.Geometry.Manifold.Bordism

/-!
Elaboration probe for the THM-M-0563 exact-statement blocker.

This checks only the nearest pinned mathlib substrate. The imported module explicitly provides
singular manifolds but leaves bordisms, the bordism relation and groups, and their classification
as future work, so this is not a canonical target for Thom's classification theorem.
-/

#check SingularManifold
#check SingularManifold.toPUnit
#check SingularManifold.sum
