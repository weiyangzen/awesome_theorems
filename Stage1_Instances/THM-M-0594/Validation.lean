import Statement
import Mathlib.Topology.Maps.Proper.Basic
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0594 validation probes

This module supplies independently written same-worker differential probes for
the topological bridge and its conditional composition into the frozen target.
The validation runner separately checks every extant local proof or composition
body. This file does not add the missing finite-dimensional global embedding
construction, so the exact unrestricted root remains open.
-/

namespace Stage1Instances.THM_M_0594.Validation

open Stage1Instances.THM_M_0594
open Function Topology
open scoped Manifold ContDiff

universe uE uH uM uN

/-- Independently written same-worker probe of the proper-injective topological bridge. -/
theorem properInjectiveProbe
    {M : Type uM} {N : Type uN} [TopologicalSpace M] [TopologicalSpace N]
    {f : M -> N} (proper : IsProperMap f) (injective : Injective f) :
    IsEmbedding f :=
  (IsClosedEmbedding.of_continuous_injective_isClosedMap
    proper.continuous injective proper.isClosedMap).isEmbedding

/-- Independently written conditional probe of the exact frozen root expression. -/
theorem conditionalExactTargetProbe
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M]
    (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n))
    (smooth : CMDiff ∞ e) (proper : IsProperMap e)
    (injective : Injective e)
    (immersion : ∀ x : M, Injective (mfderiv I (𝓡 n) e x)) :
    WhitneyEmbeddingTarget E H I M :=
  ⟨n, e, smooth, properInjectiveProbe proper injective, immersion⟩

assert_no_sorry properInjectiveProbe
assert_no_sorry conditionalExactTargetProbe

#print sorries properInjectiveProbe
#print sorries conditionalExactTargetProbe

#print axioms properInjectiveProbe
#print axioms conditionalExactTargetProbe

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0594.Validation.properInjectiveProbe,
    ``Stage1Instances.THM_M_0594.Validation.conditionalExactTargetProbe
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

end Stage1Instances.THM_M_0594.Validation
