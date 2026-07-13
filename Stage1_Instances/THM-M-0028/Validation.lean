import Statement
import Mathlib.RingTheory.Noetherian.Defs
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0028 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen root directly from the two pinned mathlib terminal declarations. This is same-worker
corroboration, not a second proof body or independent-runner evidence.
-/

namespace Stage1Instances.THM_M_0028.Validation

open Stage1Instances.THM_M_0028

universe u

/-- A separately written exact-type route from the pinned terminal theorems to the frozen target. -/
theorem differentialIdealAscendingChainTheorem :
    IdealAscendingChainTarget.{u} := by
  intro R _ hfg f
  have hNoetherian : IsNoetherianRing R :=
    (isNoetherianRing_iff_ideal_fg R).mpr hfg
  exact monotone_stabilizes_iff_noetherian.mpr hNoetherian f

assert_no_sorry isNoetherianRing_iff_ideal_fg
assert_no_sorry monotone_stabilizes_iff_noetherian
assert_no_sorry differentialIdealAscendingChainTheorem

#print sorries isNoetherianRing_iff_ideal_fg
#print sorries monotone_stabilizes_iff_noetherian
#print sorries differentialIdealAscendingChainTheorem

#print axioms isNoetherianRing_iff_ideal_fg
#print axioms monotone_stabilizes_iff_noetherian
#print axioms differentialIdealAscendingChainTheorem

end Stage1Instances.THM_M_0028.Validation
