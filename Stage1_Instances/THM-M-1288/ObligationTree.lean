import Statement

/-!
# THM-M-1288 conditional root composition

This module checks the final composition interface.  Its two package arguments
are the open admissibility and optimality subtrees; they are not asserted here.
-/

namespace Stage1Instances.THM_M_1288

/-- The exact inequality half delivered by the analytic subtree. -/
def TalentiAdmissibilityPackage : Prop :=
  forall (n : Nat) (p : Real),
    1 < p -> p < (n : Real) ->
      IsAdmissibleConstant n p (talentiConstant n p)

/-- The exact least-constant half delivered by the sharpness subtree. -/
def TalentiOptimalityPackage : Prop :=
  forall (n : Nat) (p : Real),
    1 < p -> p < (n : Real) ->
      forall C : Real, IsAdmissibleConstant n p C -> talentiConstant n p <= C

/-- Checked composition of the two exact packages into the frozen root. -/
theorem talentiSharpSobolevTarget_of_packages
    (admissibility : TalentiAdmissibilityPackage)
    (optimality : TalentiOptimalityPackage) : TalentiSharpSobolevTarget := by
  intro n p hp hpn
  exact ⟨admissibility n p hp hpn, optimality n p hp hpn⟩

#print axioms talentiSharpSobolevTarget_of_packages

end Stage1Instances.THM_M_1288
