import «Stage1_Instances».«THM-M-0321».Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0321 same-worker validation probe

This module replays the exact frozen target without invoking the terminal
`markovKakutani_proof` declaration. It deliberately reuses the proof phase's
substantive finite-family and compactness helpers, so it is a differential
composition check, not an independent proof or a second-runner attestation.
-/

open Set

namespace Stage1Instances.THM_M_0321.Validation

universe u v

/-- Recompose the exact target from the two sound proof packages while
bypassing both the terminal theorem and the false frozen helper interface. -/
theorem recomposedMarkovKakutani : MarkovKakutaniTarget.{u, v} := by
  intro E _ _ _ _ _ _ _ I K f hK hCompact hConvex hMaps hContinuous hAffine hCommute
  exact continuousCompactnessUpgrade hCompact hContinuous
    (finiteFamilyStep E I K f hK hCompact hConvex hMaps hContinuous hAffine hCommute)

assert_no_sorry isClosed_fixedSetWithin
assert_no_sorry isCompact_fixedSetWithin
assert_no_sorry convex_fixedSetWithin
assert_no_sorry mapsTo_fixedSetWithin_of_commute
assert_no_sorry continuousOn_fixedSetWithin
assert_no_sorry isAffineOn_fixedSetWithin
assert_no_sorry cesaroAverage_mem
assert_no_sorry affine_centerMass
assert_no_sorry map_cesaroAverage
assert_no_sorry cesaro_defect_eq
assert_no_sorry tendsto_cesaro_defect_zero
assert_no_sorry singleMap_fixedPoint
assert_no_sorry isClosed_commonFixedSet
assert_no_sorry isCompact_commonFixedSet
assert_no_sorry convex_commonFixedSet
assert_no_sorry mapsTo_commonFixedSet_of_commute
assert_no_sorry finiteFamilyStep
assert_no_sorry continuousCompactnessUpgrade
assert_no_sorry markovKakutani_of_finiteFamily
assert_no_sorry markovKakutani_proof
assert_no_sorry recomposedMarkovKakutani

#print sorries markovKakutani_proof
#print sorries recomposedMarkovKakutani
#print axioms markovKakutani_proof
#print axioms recomposedMarkovKakutani

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0321.markovKakutani_proof,
    ``Stage1Instances.THM_M_0321.Validation.recomposedMarkovKakutani
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
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0321.Validation
