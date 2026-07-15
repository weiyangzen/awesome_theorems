import Proof
import ObligationTree
import Mathlib.Util.PrintSorries

/-!
# THM-M-1060 validation audit

This module audits every proof-phase declaration and both conditional composition declarations.
It adds no Schilder proof: the open lower bound, closed upper bound, good-rate package, and exact
canonical root remain unavailable.
-/

namespace Stage1Instances.THM_M_1060.Validation

#print sorries Stage1Instances.THM_M_1060.isProbabilityMeasure_of_isWienerMeasure
#print sorries Stage1Instances.THM_M_1060.measurableEvaluationLinear
#print sorries Stage1Instances.THM_M_1060.continuousScale
#print sorries Stage1Instances.THM_M_1060.zeroTimeVarianceAndLaw
#print sorries Stage1Instances.THM_M_1060.zeroTimeLaw
#print sorries Stage1Instances.THM_M_1060.oneTimeVarianceAndLaw
#print sorries Stage1Instances.THM_M_1060.oneTimeLaw
#print sorries Stage1Instances.THM_M_1060.isGaussianProcess_of_isWienerMeasure
#print sorries Stage1Instances.THM_M_1060.ObligationTree.smallNoiseLDP_of_bounds_and_good
#print sorries Stage1Instances.THM_M_1060.ObligationTree.schilderTarget_of_components

#print axioms Stage1Instances.THM_M_1060.isProbabilityMeasure_of_isWienerMeasure
#print axioms Stage1Instances.THM_M_1060.measurableEvaluationLinear
#print axioms Stage1Instances.THM_M_1060.continuousScale
#print axioms Stage1Instances.THM_M_1060.zeroTimeVarianceAndLaw
#print axioms Stage1Instances.THM_M_1060.zeroTimeLaw
#print axioms Stage1Instances.THM_M_1060.oneTimeVarianceAndLaw
#print axioms Stage1Instances.THM_M_1060.oneTimeLaw
#print axioms Stage1Instances.THM_M_1060.isGaussianProcess_of_isWienerMeasure
#print axioms Stage1Instances.THM_M_1060.ObligationTree.smallNoiseLDP_of_bounds_and_good
#print axioms Stage1Instances.THM_M_1060.ObligationTree.schilderTarget_of_components

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_1060.isProbabilityMeasure_of_isWienerMeasure,
    ``Stage1Instances.THM_M_1060.measurableEvaluationLinear,
    ``Stage1Instances.THM_M_1060.continuousScale,
    ``Stage1Instances.THM_M_1060.zeroTimeVarianceAndLaw,
    ``Stage1Instances.THM_M_1060.zeroTimeLaw,
    ``Stage1Instances.THM_M_1060.oneTimeVarianceAndLaw,
    ``Stage1Instances.THM_M_1060.oneTimeLaw,
    ``Stage1Instances.THM_M_1060.isGaussianProcess_of_isWienerMeasure,
    ``Stage1Instances.THM_M_1060.ObligationTree.smallNoiseLDP_of_bounds_and_good,
    ``Stage1Instances.THM_M_1060.ObligationTree.schilderTarget_of_components
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
  logInfo m!"VALIDATION_CLOSURE roots={roots.size} declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_1060.Validation
