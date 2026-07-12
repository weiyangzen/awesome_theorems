import Statement

/-!
# THM-M-0769 differential validation probe

This module deliberately imports neither the dossier proof nor its obligation
tree. It reconstructs the exact frozen root directly through Lean core's
dependent `Pi.instNonempty` instance.
-/

universe u v

namespace Stage1Instances.THM_M_0769.Validation

/-- A separately written route to the exact frozen proposition. -/
theorem independentAxiomOfChoice : AxiomOfChoiceTarget.{u, v} :=
  fun _ _ h => @Pi.instNonempty _ _ h

end Stage1Instances.THM_M_0769.Validation

#print axioms Stage1Instances.THM_M_0769.Validation.independentAxiomOfChoice
