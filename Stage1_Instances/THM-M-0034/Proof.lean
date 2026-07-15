import «Stage1_Instances».«THM-M-0034».Statement
import «Stage1_Instances».«THM-M-0034».Vendor.QuillenSuslin.MainTheorem

/-!
# THM-M-0034 Quillen-Suslin proof adapter

The vendored theorem proves the stronger principal-ideal-domain coefficient form. A field is a
principal ideal domain, so specializing its finite variable type to `Fin n` proves the exact frozen
target. The positivity hypothesis is retained by the target and is not needed by the stronger body.
-/

namespace Stage1Instances.THM_M_0034

universe u v

/-- The exact canonical Quillen-Suslin target, discharged by the vendored stronger PID theorem. -/
theorem quillenSuslinTarget : QuillenSuslinTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact quillenSuslin k (Fin n) P

#print sorries quillenSuslin
#print sorries quillenSuslinTarget
#print axioms quillenSuslin
#print axioms quillenSuslinTarget

end Stage1Instances.THM_M_0034
