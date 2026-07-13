import Statement
import ObligationTree

/-!
# THM-M-0417 proof integration

This module checks a repo-local wrapper for the exact strict Minkowski target.
The terminal proof body remains in the pinned mathlib dependency.
-/

namespace Stage1Instances.THM_M_0417.Proof

open ENNReal MeasureTheory MeasureTheory.Measure Module
open scoped Pointwise
open Stage1Instances.THM_M_0417.ObligationTree

universe u

/-- The half-body measure calculation from the pinned terminal proof, exposed
at the interface frozen by the obligation tree. -/
theorem halfBodyVolume : HalfBodyVolume.{u} := by
  intro E _ _ _ _ _ mu _ L _ F s _ _ _ hMeasure
  rw [addHaar_smul_of_nonneg mu (by simp : 0 ≤ (2 : ℝ)⁻¹) s,
    ← ENNReal.mul_lt_mul_iff_left
      (pow_ne_zero (finrank ℝ E) (two_ne_zero' _)) (by finiteness),
    mul_right_comm, ofReal_pow (by simp : 0 ≤ (2 : ℝ)⁻¹),
    ofReal_inv_of_pos zero_lt_two]
  norm_num
  rwa [← mul_pow, ENNReal.inv_mul_cancel two_ne_zero ofNat_ne_top,
    one_pow, one_mul]

/-- Blichfeldt's theorem, specialized to the half-body collision interface. -/
theorem blichfeldtBridge : BlichfeldtBridge.{u} := by
  intro E _ _ _ _ _ mu _ L _ F s fund hConv hVolume
  exact MeasureTheory.exists_pair_mem_lattice_not_disjoint_vadd
    fund ((hConv.smul _).nullMeasurableSet _) hVolume

/-- Extract the nonzero lattice difference from two overlapping translates. -/
theorem differenceExtraction : DifferenceExtraction.{u} := by
  intro E _ _ L s hSymm hConv hCollision
  obtain ⟨x, y, hxy, hOverlap⟩ := hCollision
  obtain ⟨_, ⟨v, hv, rfl⟩, w, hw, hvw⟩ :=
    Set.not_disjoint_iff.mp hOverlap
  refine ⟨x - y, sub_ne_zero.2 hxy, ?_⟩
  rw [Set.mem_inv_smul_set_iff₀ (two_ne_zero' ℝ)] at hv hw
  simp_rw [AddSubgroup.vadd_def, vadd_eq_add, add_comm _ w,
    ← sub_eq_sub_iff_add_eq_add, ← AddSubgroup.coe_sub] at hvw
  rw [← hvw, ← inv_smul_smul₀ (two_ne_zero' ℝ) (_ - _), smul_sub,
    sub_eq_add_neg, smul_add]
  refine hConv hw (hSymm _ hv) ?_ ?_ ?_ <;> norm_num

/-- The exact strict Minkowski target, closed by the audited declaration in
the pinned mathlib geometry-of-numbers module. -/
theorem minkowskiConvexBody :
    ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
        [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
        (mu : Measure E) [mu.IsAddHaarMeasure]
        (L : AddSubgroup E) [Countable L] (F s : Set E),
      IsAddFundamentalDomain L F mu →
        (∀ x ∈ s, -x ∈ s) →
          Convex ℝ s →
            mu F * 2 ^ finrank ℝ E < mu s →
              ∃ x ≠ 0, ((x : L) : E) ∈ s := by
  intro E _ _ _ _ _ mu _ L _ F s fund hSymm hConv hMeasure
  exact MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
    fund hSymm hConv hMeasure

/-- The proof declaration has the literal proposition frozen by
`Stage1Instances.THM_M_0417.Statement`. -/
theorem closesFrozenStatement :
    Stage1Instances.THM_M_0417.Statement.{u} :=
  minkowskiConvexBody

/-- Independent checked composition through all three frozen mathematical
interfaces. -/
theorem closesViaFrozenComposition : Root.{u} :=
  root_compose halfBodyVolume blichfeldtBridge differenceExtraction

/-- The frozen child composition also closes the canonical statement
definition, so the decomposition cannot drift to a nearby root. -/
theorem closesFrozenStatementViaComposition :
    Stage1Instances.THM_M_0417.Statement.{u} :=
  closesViaFrozenComposition

/-- Re-export the frozen root-identity certificate at the proof boundary. -/
theorem frozenRootExactType :
    Root.{u} = Stage1Instances.THM_M_0417.Statement.{u} :=
  rfl

#check minkowskiConvexBody
#check closesFrozenStatement
#check closesViaFrozenComposition
#check closesFrozenStatementViaComposition
#check frozenRootExactType

#print axioms MeasureTheory.exists_pair_mem_lattice_not_disjoint_vadd
#print axioms MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
#print axioms halfBodyVolume
#print axioms blichfeldtBridge
#print axioms differenceExtraction
#print axioms minkowskiConvexBody
#print axioms closesFrozenStatement
#print axioms closesViaFrozenComposition
#print axioms closesFrozenStatementViaComposition
#print axioms frozenRootExactType

end Stage1Instances.THM_M_0417.Proof
