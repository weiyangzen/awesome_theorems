import Mathlib.Probability.Process.Kolmogorov

/-!
# THM-M-1083 pinned-mathlib anchor audit

This module checks the declarations actually present at the repository's pinned mathlib revision.
They encode the increment hypothesis and modification relation, but not the terminal Holder
modification theorem required by the canonical statement.
-/

open MeasureTheory
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1083.AnchorAudit

#check ProbabilityTheory.IsKolmogorovProcess
#check ProbabilityTheory.IsAEKolmogorovProcess
#check ProbabilityTheory.IsKolmogorovProcess.mk_of_secondCountableTopology
#check ProbabilityTheory.IsKolmogorovProcess.IsAEKolmogorovProcess
#check ProbabilityTheory.IsAEKolmogorovProcess.ae_eq_mk
#check ProbabilityTheory.IsAEKolmogorovProcess.kolmogorovCondition

#print axioms ProbabilityTheory.IsKolmogorovProcess.mk_of_secondCountableTopology
#print axioms ProbabilityTheory.IsKolmogorovProcess.IsAEKolmogorovProcess
#print axioms ProbabilityTheory.IsAEKolmogorovProcess.ae_eq_mk
#print axioms ProbabilityTheory.IsAEKolmogorovProcess.kolmogorovCondition

end Stage1Instances.THM_M_1083.AnchorAudit
