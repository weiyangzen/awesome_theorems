import Mathlib.AlgebraicGeometry.Geometrically.Basic
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.GroupTheory.Descent
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.Topology.Sheaves.Abelian

/-!
# THM-M-0123 immutable anchor probes

This module checks the pinned representation and arithmetic support discovered
by the bounded anchor audit. None of these declarations proves Mordell's
conjecture: `Northcott.finite_le` needs an a priori height bound, while
`AddCommGroup.fg_of_descent'` proves finite generation of an abstract group.
-/

open CategoryTheory AlgebraicGeometry

#check NumberField
#check Scheme
#check SmoothOfRelativeDimension
#check IsProper
#check geometrically
#check CategoryTheory.Sheaf.H
#check Northcott.finite_le
#check AddCommGroup.fg_of_descent'

namespace Stage1Instances.THM_M_0123.AnchorAudit

variable {alpha beta : Type*} [LE beta] (height : alpha -> beta) [Northcott height]

/-- Directly checked support wrapper. It proves only bounded-height finiteness. -/
theorem checked_northcott_sublevel (bound : beta) :
    {a : alpha | height a <= bound}.Finite :=
  Northcott.finite_le bound

#print axioms checked_northcott_sublevel

end Stage1Instances.THM_M_0123.AnchorAudit
