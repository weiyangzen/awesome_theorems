import Statement
import Mathlib.Analysis.Normed.Operator.Bilinear
import Mathlib.MeasureTheory.Function.LpSeminorm.TriangleInequality
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1171 same-worker differential validation

This module deliberately imports neither `Proof` nor an obligation-tree Lean
module. It separately reimplements the two finite-dimensional ingredients
implemented by the proof phase. It does not state or prove the missing strong
`L^p` multiplier estimate, any frozen whole obligation, or the exact root.
-/

set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 100000

namespace Stage1Instances.THM_M_1171.Validation

private abbrev CoordinateSpace (n : Nat) := Fin n -> Real

/-- No-import reimplementation of the pointwise finite-dimensional operator
norm estimate used by the planned Hessian assembly. -/
theorem differentialOpNormLeComponentSum {n : Nat}
    (A : CoordinateSpace n →L[Real] CoordinateSpace n →L[Real] Real) :
    ‖A‖ <= ∑ i : Fin n, ∑ j : Fin n,
      ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
  apply ContinuousLinearMap.opNorm_le_bound₂ A
    (Finset.sum_nonneg fun _ _ =>
      Finset.sum_nonneg fun _ _ => norm_nonneg _)
  intro x y
  have hxy : A x y = ∑ i : Fin n, ∑ j : Fin n,
      A (Pi.single i (x i)) (Pi.single j (y j)) := by
    calc
      A x y = A (∑ i : Fin n, Pi.single i (x i))
          (∑ j : Fin n, Pi.single j (y j)) := by
            rw [Finset.univ_sum_single, Finset.univ_sum_single]
      _ = ∑ i : Fin n, ∑ j : Fin n,
          A (Pi.single i (x i)) (Pi.single j (y j)) := by
            simp_rw [map_sum, ContinuousLinearMap.sum_apply]
            rw [Finset.sum_comm]
  rw [hxy]
  calc
    ‖∑ i : Fin n, ∑ j : Fin n,
        A (Pi.single i (x i)) (Pi.single j (y j))‖
        <= ∑ i : Fin n, ∑ j : Fin n,
          ‖A (Pi.single i (x i)) (Pi.single j (y j))‖ := by
            exact (norm_sum_le _ _).trans
              (Finset.sum_le_sum fun i _ => norm_sum_le _ _)
    _ = ∑ i : Fin n, ∑ j : Fin n,
          (|x i| * |y j|) *
            ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      have hi : Pi.single i (x i) =
          (x i) • (Pi.single i (1 : Real) : CoordinateSpace n) := by
        ext k
        simp [Pi.single_apply]
      have hj : Pi.single j (y j) =
          (y j) • (Pi.single j (1 : Real) : CoordinateSpace n) := by
        ext k
        simp [Pi.single_apply]
      calc
        ‖A (Pi.single i (x i)) (Pi.single j (y j))‖
            = ‖(x i * y j) •
                A (Pi.single i 1) (Pi.single j 1)‖ := by
              rw [hi, hj, map_smul, map_smul]
              simp
              ring
        _ = |x i| * |y j| *
              ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
              rw [norm_smul, Real.norm_eq_abs, abs_mul]
    _ <= ∑ i : Fin n, ∑ j : Fin n,
          (‖x‖ * ‖y‖) *
            ‖A (Pi.single i 1) (Pi.single j 1)‖ := by
      apply Finset.sum_le_sum
      intro i _
      apply Finset.sum_le_sum
      intro j _
      have hxi : |x i| <= ‖x‖ := by
        simpa [Real.norm_eq_abs] using norm_le_pi_norm x i
      have hyj : |y j| <= ‖y‖ := by
        simpa [Real.norm_eq_abs] using norm_le_pi_norm y j
      gcongr
    _ = (∑ i : Fin n, ∑ j : Fin n,
          ‖A (Pi.single i 1) (Pi.single j 1)‖) * ‖x‖ * ‖y‖ := by
      calc
        ∑ i : Fin n, ∑ j : Fin n,
            (‖x‖ * ‖y‖) * ‖A (Pi.single i 1) (Pi.single j 1)‖
          = (‖x‖ * ‖y‖) *
              (∑ i : Fin n, ∑ j : Fin n,
                ‖A (Pi.single i 1) (Pi.single j 1)‖) := by
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro i _
              rw [Finset.mul_sum]
        _ = (∑ i : Fin n, ∑ j : Fin n,
              ‖A (Pi.single i 1) (Pi.single j 1)‖) * ‖x‖ * ‖y‖ := by
              ring

/-- Separately derived finite-sum `eLpNorm` triangle
inequality. It still assumes measurability and supplies no component bound. -/
theorem differentialELpNormFinsetSumLe {alpha : Type*}
    [MeasurableSpace alpha] {iota : Type*} (s : Finset iota)
    (f : iota -> alpha -> Real) (p : ENNReal)
    (mu : MeasureTheory.Measure alpha)
    (hf : forall i, i ∈ s -> MeasureTheory.AEStronglyMeasurable (f i) mu)
    (hp : 1 <= p) :
    MeasureTheory.eLpNorm (∑ i ∈ s, f i) p mu <=
      ∑ i ∈ s, MeasureTheory.eLpNorm (f i) p mu := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [MeasureTheory.eLpNorm_zero]
  | @insert i s hi ih =>
      rw [Finset.sum_insert hi]
      refine (MeasureTheory.eLpNorm_add_le (hf i (Finset.mem_insert_self i s))
        (Finset.aestronglyMeasurable_sum s
          (fun j hj => hf j (Finset.mem_insert_of_mem hj))) hp).trans ?_
      rw [Finset.sum_insert hi]
      exact add_le_add_right
        (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))
        (MeasureTheory.eLpNorm (f i) p mu)

assert_no_sorry differentialOpNormLeComponentSum
assert_no_sorry differentialELpNormFinsetSumLe

#print sorries differentialOpNormLeComponentSum
#print sorries differentialELpNormFinsetSumLe
#print axioms differentialOpNormLeComponentSum
#print axioms differentialELpNormFinsetSumLe

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_1171.Validation.differentialOpNormLeComponentSum,
    ``Stage1Instances.THM_M_1171.Validation.differentialELpNormFinsetSumLe
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

end Stage1Instances.THM_M_1171.Validation
