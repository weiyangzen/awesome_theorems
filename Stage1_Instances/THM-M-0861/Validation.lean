import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0861 validation probes

This module rechecks all proof-phase declarations and separately recomposes the
exact canonical root from the still-open fixed-palette Satz C interface. The
Satz C package remains an explicit premise, so this is neither a proof of the
root nor an independent-runner attestation.
-/

noncomputable section

namespace Stage1Instances.THM_M_0861_Validation

universe u v

open Stage1Instances.THM_M_0861
open Stage1Instances.THM_M_0861_Obligations
open Stage1Instances.THM_M_0861_Proof

/-- A separately written conditional composition from the missing Satz C
package to the exact canonical target. -/
theorem rootFromBoundedSatzC
    (satzC : BoundedSatzCTarget.{u, v}) :
    KonigEdgeColoringTarget.{u, v} := by
  intro Vertex Edge G vertexFinite edgeFinite hBipartite
  refine ⟨?_, lowerBound G vertexFinite edgeFinite hBipartite⟩
  exact satzC G vertexFinite edgeFinite (maxDegree G vertexFinite)
    hBipartite (degree_le_maxDegree G vertexFinite)

assert_no_sorry degree_le_maxDegree
assert_no_sorry incidenceSet_finite
assert_no_sorry incidentColor_injective
assert_no_sorry maxDegree_le_of_degree_le
assert_no_sorry lowerBound
assert_no_sorry edgePaletteEmbedding
assert_no_sorry edgeColorable_of_edge_ncard_le
assert_no_sorry upperBound_of_boundedSatzC
assert_no_sorry konigEdgeColoring_of_boundedSatzC
assert_no_sorry rootFromBoundedSatzC

#print sorries degree_le_maxDegree
  incidenceSet_finite
  incidentColor_injective
  maxDegree_le_of_degree_le
  lowerBound
  edgePaletteEmbedding
  edgeColorable_of_edge_ncard_le
  upperBound_of_boundedSatzC
  konigEdgeColoring_of_boundedSatzC
  rootFromBoundedSatzC

#print axioms degree_le_maxDegree
#print axioms incidenceSet_finite
#print axioms incidentColor_injective
#print axioms maxDegree_le_of_degree_le
#print axioms lowerBound
#print axioms edgePaletteEmbedding
#print axioms edgeColorable_of_edge_ncard_le
#print axioms upperBound_of_boundedSatzC
#print axioms konigEdgeColoring_of_boundedSatzC
#print axioms rootFromBoundedSatzC

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0861_Proof.degree_le_maxDegree,
    ``Stage1Instances.THM_M_0861_Proof.incidenceSet_finite,
    ``Stage1Instances.THM_M_0861_Proof.incidentColor_injective,
    ``Stage1Instances.THM_M_0861_Proof.maxDegree_le_of_degree_le,
    ``Stage1Instances.THM_M_0861_Proof.lowerBound,
    ``Stage1Instances.THM_M_0861_Proof.edgePaletteEmbedding,
    ``Stage1Instances.THM_M_0861_Proof.edgeColorable_of_edge_ncard_le,
    ``Stage1Instances.THM_M_0861_Proof.upperBound_of_boundedSatzC,
    ``Stage1Instances.THM_M_0861_Proof.konigEdgeColoring_of_boundedSatzC,
    ``Stage1Instances.THM_M_0861_Validation.rootFromBoundedSatzC
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

end Stage1Instances.THM_M_0861_Validation
