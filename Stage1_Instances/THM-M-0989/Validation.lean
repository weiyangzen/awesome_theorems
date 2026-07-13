import «Stage1_Instances».«THM-M-0989».LindebergArray
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0989 validation probe

This module checks the exact frozen root through a separately written final
composition.  It reuses the proof phase's analytic packages, so it is
same-worker differential evidence rather than a second proof body or an
independent-runner attestation.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0989.Validation

open Stage1Instances.THM_M_0989

universe u

/-- Exact-type replay through the frozen Levy composition, written separately
from `lindebergFeller_exact` but deliberately sharing its analytic packages. -/
theorem lindebergFeller_composition_replay : Statement.{u} := by
  intro Omega _ A
  letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
  refine {
    forall_aemeasurable := rowSumsAEMeasurable_proof A
    aemeasurable_limit := measurable_id.aemeasurable
    tendsto := ?_
  }
  apply ProbabilityMeasure.tendsto_iff_tendsto_charFun.2
  simpa using rowLawCharFunConverges_proof A

assert_no_sorry Stage1Instances.THM_M_0989.lindebergFeller_exact
assert_no_sorry lindebergFeller_composition_replay
assert_no_sorry ProbabilityMeasure.tendsto_iff_tendsto_charFun
assert_no_sorry iIndepFun.charFun_map_fun_sum_eq_prod
assert_no_sorry charFun_gaussianReal

#print sorries Stage1Instances.THM_M_0989.lindebergFeller_exact
#print sorries lindebergFeller_composition_replay
#print sorries ProbabilityMeasure.tendsto_iff_tendsto_charFun
#print sorries iIndepFun.charFun_map_fun_sum_eq_prod
#print sorries charFun_gaussianReal

#print axioms Stage1Instances.THM_M_0989.lindebergFeller_exact
#print axioms lindebergFeller_composition_replay
#print axioms ProbabilityMeasure.tendsto_iff_tendsto_charFun
#print axioms iIndepFun.charFun_map_fun_sum_eq_prod
#print axioms charFun_gaussianReal

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0989.lindebergFeller_exact,
    ``Stage1Instances.THM_M_0989.Validation.lindebergFeller_composition_replay
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
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0989.Validation
