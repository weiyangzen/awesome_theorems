import «Stage1_Instances».«THM-M-0400».Statement

/-!
# THM-M-0400 proof execution

This module implements elementary boundary and encoding facts from the frozen
obligation tree. The deep Subspace-Theorem engine remains open, so no proof of
the canonical root is declared here.
-/

noncomputable section

namespace Stage1Rev56.THMM0400.Proof

open Stage1Rev56.THMM0400

/-- Every coordinate is bounded by the integer sup height. -/
theorem natAbs_le_integerHeight {n : Nat} (x : Fin n → Int) (j : Fin n) :
    (Int.natAbs (x j) : Real) ≤ integerHeight x := by
  unfold integerHeight
  exact_mod_cast Finset.le_sup (f := fun k => Int.natAbs (x k)) (Finset.mem_univ j)

/-- A nonzero integer vector has height at least one. This closes the
elementary height part of `M0400-S-BOUNDARY`. -/
theorem one_le_integerHeight {n : Nat} {x : Fin n → Int} (hx : x ≠ 0) :
    1 ≤ integerHeight x := by
  have hex : ∃ j, x j ≠ 0 := by
    by_contra h
    push Not at h
    exact hx (funext h)
  obtain ⟨j, hj⟩ := hex
  have hone : (1 : Real) ≤ Int.natAbs (x j) := by
    exact_mod_cast (Nat.one_le_iff_ne_zero.mpr (Int.natAbs_ne_zero.mpr hj))
  exact hone.trans (natAbs_le_integerHeight x j)

/-- The coordinatewise rational embedding reflects the zero vector. -/
theorem rationalVector_ne_zero {n : Nat} {x : Fin n → Int} (hx : x ≠ 0) :
    rationalVector x ≠ 0 := by
  intro h
  apply hx
  funext j
  have hj : (x j : Rat) = 0 := congrFun h j
  exact_mod_cast hj

#print axioms natAbs_le_integerHeight
#print axioms one_le_integerHeight
#print axioms rationalVector_ne_zero

end Stage1Rev56.THMM0400.Proof
