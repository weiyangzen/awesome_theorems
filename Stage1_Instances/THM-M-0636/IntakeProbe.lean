import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Dynamics.FixedPoints.Basic

/-!
# THM-M-0636 discovery-only intake probe

These checks authenticate adjacent pinned compactness, convexity, continuity, self-map,
finite-dimensional, and fixed-point interfaces. They do not choose the catalog's ambient space or
exact proposition, state Brouwer's theorem, or supply proof credit.
-/

#check Set.Nonempty
#check IsCompact
#check Convex
#check Continuous
#check ContinuousOn
#check Set.MapsTo
#check FiniteDimensional
#check Function.IsFixedPt
#check Function.fixedPoints
