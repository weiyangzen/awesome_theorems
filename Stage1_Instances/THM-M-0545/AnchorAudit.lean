import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.RingTheory.Kaehler.Basic

/-!
Pinned mathlib probes for `S56-M-0545-ANCHOR_AUDIT`. These are supporting
APIs only; none has the type of the frozen Hodge-decomposition target.
-/

#check extDeriv
#check extDeriv_extDeriv
#check InnerProductSpace.HarmonicAt
#check InnerProductSpace.HarmonicOnNhd
#check InnerProductSpace.harmonicOnNhd_const
#check Submodule.finrank_add_finrank_orthogonal
#check OrthogonalFamily.decomposition
#check IsRiemannianManifold
#check CategoryTheory.Sheaf.H
#check KaehlerDifferential
#check KaehlerDifferential.D

