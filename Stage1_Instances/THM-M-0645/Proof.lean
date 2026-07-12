import ObligationTree

/-!
# THM-M-0645 proof execution

This module discharges the classical contraposition and final-composition obligations. The
countermodel construction is kept as an explicit, exact interface: no inhabitant is asserted for
it until the Henkin, equality-congruence, term-model, and truth-lemma obligations are implemented.
-/

namespace Stage1Instances.THM_M_0645

universe u v

open FirstOrder
open FirstOrder.Language

/-- Exact output required from the open countermodel branch of the frozen proof graph. -/
def CountermodelProperty : Prop :=
  forall (L : Language.{u, v}) (phi : L.Sentence),
    (Provable phi -> False) -> (Valid phi -> False)

/-- Classical contraposition turns the countermodel property into the required derivation
builder. This is the proof body for obligation `M0645-T-CLASSICAL`. -/
theorem builder_of_countermodel
    (countermodel : CountermodelProperty.{u, v}) :
    CompletenessDerivationBuilder.{u, v} := by
  intro L phi valid
  classical
  by_contra notProvable
  exact countermodel L phi notProvable valid

/-- Kernel-checked composition of the countermodel branch with the exact frozen root. -/
theorem completenessTarget_of_countermodel
    (countermodel : CountermodelProperty.{u, v}) : CompletenessTarget.{u, v} := by
  exact completenessTarget_of_builder (builder_of_countermodel countermodel)

#check builder_of_countermodel
#check completenessTarget_of_countermodel
#print axioms builder_of_countermodel
#print axioms completenessTarget_of_countermodel

end Stage1Instances.THM_M_0645
