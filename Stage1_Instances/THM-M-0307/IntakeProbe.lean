import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-0307 discovery-only intake probe

These checks authenticate pinned `Lp`, measure-restriction, manifold-boundary, and adjacent
Gagliardo-Nirenberg-Sobolev interfaces. They do not select a domain or Sobolev model, construct a
boundary surface measure or trace operator, state the catalog root, or prove THM-M-0307.
-/

open MeasureTheory

#check MeasureTheory.Lp
#check MeasureTheory.MemLp
#check Measure.restrict
#check ModelWithCorners.boundary
#check ModelWithCorners.interior_union_boundary_eq_univ
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
