import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Torsion

/-!
# THM-M-0163 statement substrate probe

This file checks only the closest pinned mathlib types found for a Riemannian
metric, a covariant derivative, and torsion. It does not define or prove a
geodesic equation.
-/

#check Bundle.ContMDiffRiemannianMetric
#check CovariantDerivative
#check CovariantDerivative.torsion
#check CovariantDerivative.torsion_eq_zero_iff
