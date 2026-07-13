import Proof
import Validation
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1177 release-phase narrow kernel probes

These declarations recheck the implemented nonpositive-maximum branch, the
same-worker differential reconstruction, and the conditional final interface.
The positive-maximum package remains an explicit premise, so this module is
evidence for a blocked release verdict rather than a proof of the ABP root.
-/

noncomputable section

namespace Stage1Instances.THM_M_1177.ReleaseCheck

theorem localDegenerateMaximumPackage (n : Nat) (Cn : Real)
    (hCn : 0 <= Cn) : DegenerateMaximumPackage n Cn :=
  degenerateMaximumPackage n Cn hCn

theorem differentialDegenerateMaximumPackage (n : Nat) (Cn : Real)
    (hCn : 0 <= Cn) : DegenerateMaximumPackage n Cn := by
  intro Omega u f A hypotheses hmax
  exact Validation.differentialDegenerateMaximumPackage n Cn hCn
    Omega u f A hypotheses.1 hypotheses.2.1 hypotheses.2.2.1
    hypotheses.2.2.2.1 hypotheses.2.2.2.2.1
    hypotheses.2.2.2.2.2.1 hypotheses.2.2.2.2.2.2.1
    hypotheses.2.2.2.2.2.2.2.1 hypotheses.2.2.2.2.2.2.2.2.1
    hypotheses.2.2.2.2.2.2.2.2.2.1
    hypotheses.2.2.2.2.2.2.2.2.2.2 hmax

theorem conditionalRoot
    (positive : forall n : Nat, 1 <= n ->
      exists Cn : Real, 0 <= Cn /\ PositiveMaximumPackage n Cn) :
    AlexandrovBakelmanPucciTarget :=
  abpTarget_of_positiveMaximumPackage positive

assert_no_sorry localDegenerateMaximumPackage
assert_no_sorry differentialDegenerateMaximumPackage
assert_no_sorry conditionalRoot

#print sorries localDegenerateMaximumPackage
#print sorries differentialDegenerateMaximumPackage
#print sorries conditionalRoot

#print axioms localDegenerateMaximumPackage
#print axioms differentialDegenerateMaximumPackage
#print axioms conditionalRoot

end Stage1Instances.THM_M_1177.ReleaseCheck
