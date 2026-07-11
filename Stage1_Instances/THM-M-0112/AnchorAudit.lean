import Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic
import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0112 anchor audit probes

These probes confirm the usable substrate in the pinned mathlib snapshot. None
of the declarations below states or proves weak topological Lefschetz.
-/

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THMM0112.AnchorAudit

def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

def availableSubstrate : List String := [
  "AlgebraicGeometry.IsClosedImmersion",
  "AlgebraicGeometry.IsProper",
  "AlgebraicGeometry.Smooth",
  "AlgebraicGeometry.Proj.basicOpen",
  "AlgebraicGeometry.Scheme.forgetToTop",
  "AlgebraicGeometry.Spec.toTop",
  "HomotopyGroup.Pi",
  "HomotopyGroup.pi1EquivFundamentalGroup"
]

def missingTerminalInterfaces : List String := [
  "complex analytic realization of schemes over Complex",
  "canonical smooth projective hyperplane-section interface",
  "inclusion-induced higher homotopy comparison",
  "weak topological Lefschetz terminal theorem"
]

#check AlgebraicGeometry.IsClosedImmersion
#check AlgebraicGeometry.IsProper
#check AlgebraicGeometry.Smooth
#check AlgebraicGeometry.Proj.basicOpen
#check AlgebraicGeometry.Scheme.forgetToTop
#check AlgebraicGeometry.Spec.toTop
#check HomotopyGroup.Pi
#check HomotopyGroup.pi1EquivFundamentalGroup

end Stage1Instances.THMM0112.AnchorAudit
