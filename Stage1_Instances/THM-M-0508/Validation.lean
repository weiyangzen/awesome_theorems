import Proof
import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0508 validation probes

This module rechecks the proof-phase interfaces and the frozen conditional root
handoff. It also recomposes the exact canonical target from eventual positivity
without using the proof phase's final composition theorem.

Eventual positivity remains an explicit premise. This is a same-worker
differential composition check, not a proof of Vinogradov's theorem or an
independent runner attestation.
-/

namespace Stage1Instances.THM_M_0508.Validation

open Stage1Instances.THM_M_0508
open Stage1Instances.THM_M_0508.Proof

/-- A separately written composition from the still-open analytic package to
the exact frozen root. -/
theorem rootFromEventualPositiveCount
    (positive : ObligationTree.EventualPositiveRepresentationCount) :
    VinogradovThreePrimesTarget := by
  rcases positive with ⟨threshold, hpositive⟩
  refine ⟨threshold, fun n hn hodd => ?_⟩
  exact (ObligationTree.representationCount_pos_iff n).mp
    (hpositive n hn hodd)

assert_no_sorry ObligationTree.representationCount_pos_iff
assert_no_sorry ObligationTree.root_of_eventualPositiveRepresentationCount
assert_no_sorry vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount
assert_no_sorry vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount
assert_no_sorry rootFromEventualPositiveCount

#print sorries ObligationTree.representationCount_pos_iff
  ObligationTree.root_of_eventualPositiveRepresentationCount
  vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount
  vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount
  rootFromEventualPositiveCount

#print axioms ObligationTree.representationCount_pos_iff
#print axioms ObligationTree.root_of_eventualPositiveRepresentationCount
#print axioms vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount
#print axioms vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount
#print axioms rootFromEventualPositiveCount

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0508.ObligationTree.representationCount_pos_iff,
    ``Stage1Instances.THM_M_0508.ObligationTree.root_of_eventualPositiveRepresentationCount,
    ``Stage1Instances.THM_M_0508.Proof.vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount,
    ``Stage1Instances.THM_M_0508.Proof.vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount,
    ``Stage1Instances.THM_M_0508.Validation.rootFromEventualPositiveCount
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

end Stage1Instances.THM_M_0508.Validation
