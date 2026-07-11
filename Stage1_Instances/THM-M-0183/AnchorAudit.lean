import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic
import Mathlib.RingTheory.Kaehler.Basic

/-!
# THM-M-0183: pinned anchor probes

These declarations are nearby infrastructure in the pinned mathlib revision.
They do not define a geometric Kahler metric, a Ricci tensor, a real first
Chern class, or prove Yau's theorem. `KaehlerDifferential` is the unrelated
algebraic notion of Kahler differentials.
-/

open scoped Manifold
open Bundle Manifold

#check IsManifold
#check ContMDiffRiemannianMetric
#check riemannianMetricVectorSpace
#check riemannianEDist
#check IsCovariantDerivativeOn
#check CovariantDerivative
#check TangentSpace
#check TangentBundle
#check KaehlerDifferential
#check KaehlerDifferential.D
