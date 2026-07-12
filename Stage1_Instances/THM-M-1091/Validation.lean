import Statement

/-!
# THM-M-1091 independent validation probe

This module reconstructs the frozen root without importing `Proof` or `ObligationTree`. It uses a
different local proof shape so validation reaches the exact proposition independently of the
proof-phase wrapper.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1091_Validation

universe u

/-- An independently assembled kernel proof of the exact frozen target. -/
theorem independentChapmanKolmogorov :
    Stage1Instances.THM_M_1091.ChapmanKolmogorovTarget.{u} := by
  intro State _ kappa _ m n
  rw [show m + n = n + m from Nat.add_comm m n]
  exact Kernel.pow_add kappa n m

#check independentChapmanKolmogorov
#print axioms independentChapmanKolmogorov

end Stage1Instances.THM_M_1091_Validation
