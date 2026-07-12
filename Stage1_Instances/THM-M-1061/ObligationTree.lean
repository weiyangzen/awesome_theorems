/-!
# THM-M-1061 obligation-tree composition boundary

The analytic subtree remains an explicit premise.  This file checks only that
its exact output composes to the frozen public target; it is not a proof of
Varadhan's lemma.
-/

namespace Stage1Instances.THM_M_1061.ObligationTree

universe u

/-- Exact output required from the lower/upper large-deviation proof tree. -/
abbrev IntegralLemmaTerminal : Prop :=
  Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget.{u}

/-- Checked transport from the terminal package to the canonical root. -/
theorem root_of_integralLemmaTerminal
    (h : IntegralLemmaTerminal.{u}) :
    Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget.{u} := h

#check root_of_integralLemmaTerminal
#print axioms root_of_integralLemmaTerminal

end Stage1Instances.THM_M_1061.ObligationTree
