import Mathlib.Geometry.Manifold.Instances.Sphere

/-!
Pinned-environment substrate probe for the THM-M-0614 exact-statement blocker.

This checks only mathlib's general smooth-manifold API. It does not define a symplectic
four-manifold, a Spin-c structure, either invariant in Taubes's theorem, or their comparison, so
it is deliberately not presented as the canonical target.
-/

#check IsManifold
#check ContMDiff
#check Module.finrank
