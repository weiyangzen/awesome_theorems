import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.RingTheory.Kaehler.Basic

/-!
# THM-M-0113 anchor probes

These probes elaborate nearby APIs in the pinned mathlib snapshot. None is a
compact-Kahler Hodge decomposition theorem, and this file gives them no root
proof credit.
-/

#check ModelWithCorners
#check IsManifold
#check IsRiemannianManifold
#check extDeriv
#check extDeriv_extDeriv
#check InnerProductSpace.HarmonicAt
#check InnerProductSpace.HarmonicOnNhd
#check InnerProductSpace.harmonicOnNhd_const
#check CategoryTheory.Sheaf.H
#check KaehlerDifferential
#check KaehlerDifferential.D
#check iSupIndep
