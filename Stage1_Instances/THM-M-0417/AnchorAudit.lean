import Mathlib.MeasureTheory.Group.GeometryOfNumbers

/-!
# THM-M-0417 anchor audit

This module checks the exact pinned mathlib theorem against the frozen strict
Minkowski target. It is audit evidence, not the later proof-node deliverable.
-/

namespace Stage1Instances.THM_M_0417.AnchorAudit

open MeasureTheory Module

universe u

/-- Exact-type transport from the pinned mathlib declaration to the frozen target. -/
theorem mathlibCandidateClosesFrozenTarget
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
    (mu : Measure E) [mu.IsAddHaarMeasure]
    (L : AddSubgroup E) [Countable L] (F s : Set E)
    (fund : IsAddFundamentalDomain L F mu)
    (hSymm : ∀ x ∈ s, -x ∈ s)
    (hConv : Convex ℝ s)
    (hMeasure : mu F * 2 ^ finrank ℝ E < mu s) :
    ∃ x ≠ 0, ((x : L) : E) ∈ s := by
  exact MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
    fund hSymm hConv hMeasure

#check MeasureTheory.exists_pair_mem_lattice_not_disjoint_vadd
#check MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
#check MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_le_measure
#check mathlibCandidateClosesFrozenTarget

#print axioms MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
#print axioms mathlibCandidateClosesFrozenTarget

end Stage1Instances.THM_M_0417.AnchorAudit
