import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
This file checks only the pinned Riemannian-manifold substrate adjacent to
THM-M-0178. It deliberately does not declare a Bochner-technique target: the
repository metadata does not identify one proposition, and pinned mathlib has
no concrete harmonic differential-form, Hodge-Laplacian, or Ricci-curvature
interface from which to state one exactly.
-/

#check IsRiemannianManifold
#check Bundle.RiemannianBundle
#check IsContMDiffRiemannianBundle
