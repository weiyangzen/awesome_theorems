import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.OmegaLimit
import Mathlib.Geometry.Manifold.Diffeomorph
import Mathlib.Geometry.Manifold.IntegralCurve.Basic
import Mathlib.Geometry.Manifold.VectorBundle.SmoothSection

/-!
# THM-M-1367 discovery-only intake probe

These checks authenticate pinned manifold vector-field, integral-curve, flow, orbit, conjugacy,
omega-limit, and diffeomorphism interfaces adjacent to possible Peixoto-theorem encodings. They do
not define structural stability, hyperbolicity, recurrence, saddle connections, genericity, or a
canonical statement, and they prove no part of THM-M-1367.
-/

#check TangentSpace
#check TangentBundle
#check ContMDiffSection
#check IsMIntegralCurve
#check Flow
#check Flow.orbit
#check Flow.toHomeomorph
#check Flow.IsSemiconjugacy
#check omegaLimit
#check Flow.isInvariant_omegaLimit
#check Homeomorph
#check Diffeomorph
