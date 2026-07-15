import Proof
import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0509 validation probes

This module rechecks every proof-phase theorem and the frozen conditional root
handoff. It also recomposes the exact canonical target from the finite-count
interface without invoking the proof phase's final equivalence theorem.

The positivity package remains an explicit premise. This is a same-worker
differential composition check, not a proof of Chen's theorem or a distinct
runner attestation.
-/

namespace Stage1Instances.THM_M_0509.Validation

open Stage1Instances.THM_M_0509
open Stage1Instances.THM_M_0509.Proof

/-- A separately written composition from the still-open eventual-positivity
package to the exact frozen root. -/
theorem rootFromEventualPositiveCount
    (positive : EventualPositiveRepresentationCount) :
    ChenTheoremTarget := by
  rcases positive with ⟨threshold, hpositive⟩
  refine ⟨threshold, fun N hN hEven => ?_⟩
  exact (representationCount_pos_iff N).mp (hpositive N hN hEven)

assert_no_sorry isP2_iff_cardFactors_pos_le_two
assert_no_sorry representationCount_pos_iff
assert_no_sorry chenTheoremTarget_iff_eventualPositiveRepresentationCount
assert_no_sorry root_of_sieve_package
assert_no_sorry rootFromEventualPositiveCount

#print sorries isP2_iff_cardFactors_pos_le_two
  representationCount_pos_iff
  chenTheoremTarget_iff_eventualPositiveRepresentationCount
  root_of_sieve_package
  rootFromEventualPositiveCount

#print axioms isP2_iff_cardFactors_pos_le_two
#print axioms representationCount_pos_iff
#print axioms chenTheoremTarget_iff_eventualPositiveRepresentationCount
#print axioms root_of_sieve_package
#print axioms rootFromEventualPositiveCount

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0509.Proof.isP2_iff_cardFactors_pos_le_two,
    ``Stage1Instances.THM_M_0509.Proof.representationCount_pos_iff,
    ``Stage1Instances.THM_M_0509.Proof.chenTheoremTarget_iff_eventualPositiveRepresentationCount,
    ``Stage1Instances.THM_M_0509.root_of_sieve_package,
    ``Stage1Instances.THM_M_0509.Validation.rootFromEventualPositiveCount
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE roots={roots.size} declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0509.Validation
