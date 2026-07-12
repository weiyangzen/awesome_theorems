import Mathlib.Geometry.Manifold.Immersion
import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0186 statement-infrastructure probe

This file checks the narrow pinned manifold surface relevant to the intended
Willmore target. It is not a surrogate statement: the dependency closure has
no induced metric, second fundamental form, mean curvature, induced area
measure, or Willmore functional for an immersion.
-/

open scoped ContDiff Manifold

#check Manifold.IsImmersion
#check IsRiemannianManifold
#check TangentSpace
#check MeasureTheory.integral
#check Real.pi

-- Required geometric vocabulary is absent from the pinned environment.
#check_failure secondFundamentalForm
#check_failure principalCurvature
#check_failure meanCurvature
#check_failure willmoreEnergy

