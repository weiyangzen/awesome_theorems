import Statement
import Mathlib.Analysis.Analytic.Uniqueness
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1248 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
independently reconstructs the exact frozen proposition and checks the order
mistake that makes the reconstruction possible. It does not prove the source
Caffarelli-Kohn-Nirenberg theorem.
-/

open scoped ContDiff

namespace Stage1Instances.THM_M_1248.Validation

open MeasureTheory Set Filter

/-- The unqualified top order in the frozen statement is the analytic order. -/
theorem frozenOrder_eq_omega : (⊤ : WithTop ℕ∞) = ω := rfl

/-- The analytic order is distinct from the smooth order intended by the source. -/
theorem frozenOrder_ne_infinity : (⊤ : WithTop ℕ∞) ≠ ∞ := by
  simp

/-- A separately written derivation of the vacuity exposed by the proof phase.
This version invokes the setwise identity principle directly. -/
theorem independentlyCompactlySupportedTopEqZero
    {n : Nat} (hn : 0 < n)
    (u : EuclideanSpace Real (Fin n) -> Real)
    (hu : ContDiff Real ⊤ u) (hcomp : HasCompactSupport u) :
    u = 0 := by
  letI : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  letI : NoncompactSpace (EuclideanSpace Real (Fin n)) :=
    RealNormedSpace.noncompactSpace _
  obtain ⟨z, hz⟩ := (Set.ne_univ_iff_exists_notMem (tsupport u)).mp hcomp.ne_univ
  have hz0 : u =ᶠ[nhds z] 0 := notMem_tsupport_iff_eventuallyEq.mp hz
  have hzero :=
    (hu.analyticOnNhd (s := Set.univ)).eqOn_zero_of_preconnected_of_eventuallyEq_zero
      isPreconnected_univ (mem_univ z) hz0
  exact funext fun x => hzero (mem_univ x)

/-- Same-worker, no-import reconstruction of the exact frozen root. The proof
is deliberately classified as a differential check of a defective target. -/
theorem independentlyReconstructedFrozenTarget :
    CaffarelliKohnNirenbergTarget := by
  intro n p q r alpha beta gamma sigma a hadm
  have hn := hadm.1
  have hr := hadm.2.2.2.1
  refine ⟨1, by norm_num, ?_⟩
  intro u hu hcomp
  have hu0 : u = 0 := independentlyCompactlySupportedTopEqZero hn u hu hcomp
  subst u
  have hlhs : weightedLp r gamma
      (0 : EuclideanSpace Real (Fin n) -> Real) = 0 := by
    simp [weightedLp, Real.zero_rpow hr.ne', inv_ne_zero hr.ne']
  rw [hlhs]
  exact mul_nonneg
    (mul_nonneg zero_le_one
      (Real.rpow_nonneg (by
        apply Real.rpow_nonneg
        apply integral_nonneg
        intro x
        exact Real.rpow_nonneg
          (mul_nonneg (Real.rpow_nonneg (norm_nonneg x) alpha) (norm_nonneg _)) p) a))
    (Real.rpow_nonneg (by
      apply Real.rpow_nonneg
      apply integral_nonneg
      intro x
      exact Real.rpow_nonneg
        (mul_nonneg (Real.rpow_nonneg (norm_nonneg x) beta) (abs_nonneg _)) q) (1 - a))

assert_no_sorry frozenOrder_eq_omega
assert_no_sorry frozenOrder_ne_infinity
assert_no_sorry independentlyCompactlySupportedTopEqZero
assert_no_sorry independentlyReconstructedFrozenTarget

#print sorries frozenOrder_eq_omega
#print sorries frozenOrder_ne_infinity
#print sorries independentlyCompactlySupportedTopEqZero
#print sorries independentlyReconstructedFrozenTarget
#print axioms frozenOrder_eq_omega
#print axioms frozenOrder_ne_infinity
#print axioms independentlyCompactlySupportedTopEqZero
#print axioms independentlyReconstructedFrozenTarget

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_1248.Validation.independentlyCompactlySupportedTopEqZero,
    ``Stage1Instances.THM_M_1248.Validation.independentlyReconstructedFrozenTarget
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

open Lean Elab Command in
elab "#print_validation_axioms" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_1248.Validation.independentlyCompactlySupportedTopEqZero,
    ``Stage1Instances.THM_M_1248.Validation.independentlyReconstructedFrozenTarget
  ]
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  logInfo m!"VALIDATION_AXIOMS {uniqueAxioms.qsort Name.lt}"

#print_validation_axioms

end Stage1Instances.THM_M_1248.Validation
