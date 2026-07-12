import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.VectorBundle.Riemannian

/-!
# THM-M-0118 anchor-audit probes

These checks identify nearby APIs in the pinned mathlib snapshot. They do not
state Nakano positivity, coefficient Dolbeault cohomology, or Nakano vanishing.
-/

namespace Stage1Instances.THMM0118.AnchorAudit

def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

def missingTerminalInterfaces : List String := [
  "compact Kahler manifold structure",
  "holomorphic Hermitian vector bundle and curvature",
  "Nakano positivity",
  "Dolbeault cohomology with vector-bundle coefficients",
  "Nakano vanishing terminal theorem"
]

#check MDifferentiable.apply_eq_of_compactSpace
#check Bundle.ContMDiffRiemannianMetric
#check CategoryTheory.Sheaf.H
#check CategoryTheory.Sheaf.subsingleton_H_of_isZero

end Stage1Instances.THMM0118.AnchorAudit
