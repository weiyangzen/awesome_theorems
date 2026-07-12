import Statement

/-!
# THM-M-1026 obligation-tree composition boundary

This file checks only the exact composition interface between the two generalized-CLT
directions and the frozen public statement. The direction propositions remain proof-phase
obligations.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1026.ObligationTree

/-- Necessity: every nondegenerate normalized-sum limit is stable. -/
abbrev NecessityTerminal : Prop :=
  forall nu : Measure Real, IsProbabilityLaw nu -> IsNondegenerate nu ->
    (exists mu : Measure Real, IsProbabilityLaw mu /\ InDomainOfAttraction mu nu) ->
      IsStableLaw nu

/-- Converse: every nondegenerate stable law attracts some probability law. -/
abbrev ConverseTerminal : Prop :=
  forall nu : Measure Real, IsProbabilityLaw nu -> IsNondegenerate nu ->
    IsStableLaw nu ->
      exists mu : Measure Real, IsProbabilityLaw mu /\ InDomainOfAttraction mu nu

/-- Checked branch merge into the complete frozen biconditional. -/
theorem root_of_directions
    (necessity : NecessityTerminal) (converse : ConverseTerminal) :
    Stage1Instances.THM_M_1026.Statement := by
  intro nu hprob hnondeg
  exact ⟨converse nu hprob hnondeg, necessity nu hprob hnondeg⟩

#check root_of_directions
#print axioms root_of_directions

end Stage1Instances.THM_M_1026.ObligationTree
