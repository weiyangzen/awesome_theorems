import ObligationTree
import Counterexample

/-!
# THM-M-1200: proof-phase impossibility certificate

The frozen target's analytic compact-support test class makes the requested
nonzero trace package impossible. This file records the resulting checked
proof-phase barrier; it is not a positive proof of the Rankine-Hugoniot target.
-/

namespace Stage1Instances.THM_M_1200

/-- The construction required by the frozen obligation tree cannot exist. -/
theorem not_nonzeroTracePackage : Not NonzeroTracePackage := by
  intro package
  obtain ⟨phi, smooth, compact, integral_ne⟩ := package 0
  rw [Counterexample.analytic_compactSupport_eq_zero phi smooth compact] at integral_ne
  simp at integral_ne

#check not_nonzeroTracePackage
#print axioms not_nonzeroTracePackage

end Stage1Instances.THM_M_1200
