/-!
# THM-M-0721 conditional obligation composition

This checks the final composition interface of the frozen architecture.  The
membership and hardness packages remain explicit hypotheses; this file does
not prove that either package exists.
-/

namespace Stage1Instances.THM_M_0721

/-- The membership package for the selected encoded satisfiability language. -/
def CandidateMembership (candidate : Language) : Prop := InNP candidate

/-- The universal polynomial-time many-one hardness package for that language. -/
def CandidateHardness (candidate : Language) : Prop :=
  forall source : Language, InNP source -> PolyManyOneReducible source candidate

/-- Checked composition from the two exact candidate packages to the root. -/
theorem root_of_candidate_packages
    (candidate : Language)
    (membership : CandidateMembership candidate)
    (hardness : CandidateHardness candidate) :
    ExistsNPCompleteLanguage := by
  exact Exists.intro candidate (And.intro membership hardness)

#print axioms root_of_candidate_packages

end Stage1Instances.THM_M_0721
