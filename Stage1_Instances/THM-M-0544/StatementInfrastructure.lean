import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0544 statement infrastructure

This file checks only the pinned APIs adjacent to the intended Hodge theorem.
It deliberately declares no proxy for de Rham cohomology, harmonic differential
forms, or the Hodge theorem, because those concrete APIs are absent here.
-/

#check ModelWithCorners
#check IsManifold
#check CompactSpace
#check IsRiemannianManifold
#check extDeriv

