import Mathlib.AlgebraicGeometry.Geometrically.Basic
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic
import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.GroupTheory.Descent
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.Topology.Sheaves.Abelian

/-!
# THM-M-0122 immutable anchor probes

This module checks the pinned statement substrate and two adjacent arithmetic
finiteness interfaces found by the bounded anchor audit. None of these
declarations proves `FaltingsTarget`: `Northcott.finite_le` needs an a priori
height bound, and `AddCommGroup.fg_of_descent'` proves finite generation of an
abstract group rather than finiteness of rational points on a curve.
-/

open CategoryTheory AlgebraicGeometry

#check NumberField
#check Scheme
#check SmoothOfRelativeDimension
#check geometrically
#check IsClosedImmersion
#check Proj.toSpecZero
#check CategoryTheory.Sheaf.H
#check Northcott.finite_le
#check AddCommGroup.fg_of_descent'

namespace Stage1Instances.THMM0122.AnchorAudit

variable {α β : Type*} [LE β] (height : α → β) [Northcott height]

/-- Directly checked support wrapper. It proves only bounded-height finiteness. -/
theorem checked_northcott_sublevel (bound : β) :
    {a : α | height a ≤ bound}.Finite :=
  Northcott.finite_le bound

#print axioms checked_northcott_sublevel

end Stage1Instances.THMM0122.AnchorAudit
