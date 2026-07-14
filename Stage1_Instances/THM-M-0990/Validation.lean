import «Stage1_Instances».«THM-M-0990».Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0990 validation probe

This module replays the exact frozen root through a separately written final
composition. It deliberately shares the proof phase's normalization and
analytic packages, so it is same-worker differential evidence rather than a
second proof body or an independent-runner attestation.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped BigOperators ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0990.Validation

open Stage1Instances.THM_M_0990

universe u v

/-- Exact-type replay of the Lyapunov-to-Lindeberg composition. This is written
separately from `lyapunovCentralLimit_exact` but shares its analytic packages. -/
theorem lyapunovCentralLimit_composition_replay : StatementShape.{u, v} := by
  intro Omega _ Omega' _ P P' _ _ X Y delta hY hdelta hMeas hInd hLp
    hMoment hVar hLyap
  let A : EventuallyNormalizedTriangularArray Omega := {
    probabilityMeasure := P
    isProbabilityMeasure := inferInstance
    increment := normalizedIncrement P X
    rowIndependent := fun n => normalizedIncrement_independent X hInd n
    rowAEMeasurable := fun n k =>
      (normalizedIncrement_memLp X hLp n k).aemeasurable
    rowIntegrable := fun n k =>
      (normalizedIncrement_memLp X hLp n k).integrable (by norm_num)
    rowSquareIntegrable := fun n k =>
      (normalizedIncrement_memLp X hLp n k).integrable_sq
    rowCentered := fun n k => normalizedIncrement_integral_eq_zero X hLp n k
    rowVarianceNormalized := by
      filter_upwards [hVar] with n hn
      exact normalizedIncrement_variance_sum X hMeas n hn
    lindebergCondition := by
      intro epsilon hepsilon
      have hupper : Tendsto
          (fun n => epsilon ^ (-delta) * lyapunovRatio P X delta n)
          atTop (nhds 0) := by
        simpa using tendsto_const_nhds.mul hLyap
      refine squeeze_zero' ?_ ?_ hupper
      · exact Eventually.of_forall fun n => Finset.sum_nonneg fun k _ =>
          THM_M_0989.truncatedSecondMoment_nonneg P
            (normalizedIncrement P X n k) epsilon
      · filter_upwards [hVar] with n hn
        exact sum_truncatedSecondMoment_normalized_le_final X delta epsilon
          hepsilon hdelta hMeas hLp hMoment n hn }
  have hCLT := eventualLindebergFeller_exact A
  refine {
    forall_aemeasurable := fun n =>
      (normalizedRowSum_measurable_final P X hMeas n).aemeasurable
    aemeasurable_limit := hY.aemeasurable
    tendsto := ?_ }
  have ht := hCLT.tendsto
  convert ht using 2 with n
  · apply Subtype.ext
    apply Measure.map_congr
    exact Filter.Eventually.of_forall fun omega => by
      simpa only [A, eventualRowSum] using
        (congrFun (normalizedIncrement_sum P X n) omega).symm
  · apply Subtype.ext
    simpa [Measure.map_id] using hY.map_eq

assert_no_sorry Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact
assert_no_sorry lyapunovCentralLimit_composition_replay
assert_no_sorry Stage1Instances.THM_M_0990.eventualLindebergFeller_exact
assert_no_sorry ProbabilityMeasure.tendsto_iff_tendsto_charFun
assert_no_sorry iIndepFun.charFun_map_fun_sum_eq_prod
assert_no_sorry charFun_gaussianReal

#print sorries Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact
#print sorries lyapunovCentralLimit_composition_replay
#print sorries Stage1Instances.THM_M_0990.eventualLindebergFeller_exact
#print sorries ProbabilityMeasure.tendsto_iff_tendsto_charFun
#print sorries iIndepFun.charFun_map_fun_sum_eq_prod
#print sorries charFun_gaussianReal

#print axioms Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact
#print axioms lyapunovCentralLimit_composition_replay
#print axioms Stage1Instances.THM_M_0990.eventualLindebergFeller_exact
#print axioms ProbabilityMeasure.tendsto_iff_tendsto_charFun
#print axioms iIndepFun.charFun_map_fun_sum_eq_prod
#print axioms charFun_gaussianReal

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact,
    ``Stage1Instances.THM_M_0990.Validation.lyapunovCentralLimit_composition_replay
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

end Stage1Instances.THM_M_0990.Validation
