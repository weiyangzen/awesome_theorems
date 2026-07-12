import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.SmoothEmbedding

/-!
Elaboration probe for the THM-M-0597 exact-statement blocker.

This checks the pinned ambient Riemannian-manifold, smooth-embedding, tangent-
bundle, and diffeomorphism vocabulary. It deliberately does not define a
tubular-neighborhood target: the pinned library has no embedded-submanifold
normal-bundle total space whose open subsets can be the source of a manifold
diffeomorphism.
-/

open scoped Manifold

#check IsRiemannianManifold
#check Bundle.RiemannianBundle
#check IsContMDiffRiemannianBundle
#check Manifold.IsSmoothEmbedding
#check TangentSpace
#check Bundle.TotalSpace
#check Diffeomorph
