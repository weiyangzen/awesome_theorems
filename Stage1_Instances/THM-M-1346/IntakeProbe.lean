import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.Geometry.Manifold.IntegralCurve.Basic
import Mathlib.Geometry.Manifold.SmoothEmbedding

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-1346 catalog wording.

These declarations do not define hyperbolicity, stable or unstable sets, spectral splittings, or
the stable-manifold theorem. Their availability supplies no source-statement or proof credit.
-/

#check IsIntegralCurve
#check IsMIntegralCurve
#check Function.IsFixedPt
#check IsInvariant
#check Flow
#check Flow.orbit
#check Manifold.IsSmoothEmbedding
