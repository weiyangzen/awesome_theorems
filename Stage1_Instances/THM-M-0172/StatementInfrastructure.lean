import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0172 statement-infrastructure probe

This file checks the narrowest pinned manifold import found for the intended
Chern-Gauss-Bonnet target.  It is deliberately not a surrogate theorem: the
current dependency closure has no definitions for the Euler form, its
Pfaffian-curvature construction, integration of top-degree forms, or the
topological Euler characteristic of a manifold.
-/

open scoped ContDiff Manifold

#check IsManifold
#check IsRiemannianManifold
#check Bundle.RiemannianBundle
#check TangentSpace

-- Required target vocabulary is absent from the pinned environment.
#check_failure eulerForm
#check_failure pfaffian
#check_failure leviCivitaConnection
#check_failure manifoldEulerCharacteristic
