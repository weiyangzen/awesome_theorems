import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0822 validation probe

This module adds no proof content. It imports and rechecks the exact proof root
and pinned terminal already implemented by the proof phase.
-/

namespace Stage1Instances.THM_M_0822.Validation

open Stage1Instances.THM_M_0822.Proof

assert_no_sorry Finset.erdos_ko_rado
assert_no_sorry erdosKoRadoMaximum

#print sorries Finset.erdos_ko_rado
#print sorries erdosKoRadoMaximum

#print axioms Finset.erdos_ko_rado
#print axioms erdosKoRadoMaximum

end Stage1Instances.THM_M_0822.Validation
