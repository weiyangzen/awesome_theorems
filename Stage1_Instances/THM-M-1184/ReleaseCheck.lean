import Proof
import Validation
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1184 release-phase narrow kernel probes

These probes recheck only the already implemented weak-duality branch and its
conditional composition interface. No declaration supplies the open reverse
duality package, so this module is evidence for a blocked release verdict, not
for the canonical root.
-/

namespace Stage1Instances.THM_M_1184.ReleaseCheck

universe u v

theorem localWeakDuality : WeakDualityPackage.{u, v} :=
  weakDuality

theorem differentialWeakDuality : WeakDualityPackage.{u, v} :=
  Validation.differentialWeakDuality

theorem conditionalRoot
    (reverse : ReverseDualityPackage.{u, v}) :
    KantorovichDualityTarget.{u, v} :=
  kantorovichDuality_of_reverse reverse

assert_no_sorry localWeakDuality
assert_no_sorry differentialWeakDuality
assert_no_sorry conditionalRoot

#print sorries localWeakDuality
#print sorries differentialWeakDuality
#print sorries conditionalRoot

#print axioms localWeakDuality
#print axioms differentialWeakDuality
#print axioms conditionalRoot

end Stage1Instances.THM_M_1184.ReleaseCheck
