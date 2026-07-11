import «Stage1_Instances».«THM-M-0400».Statement

/-!
# THM-M-0400 independent validation probes

These probes independently reconstruct the elementary proof-phase results
without importing `Proof.lean`. They do not prove the Subspace Theorem root.
-/

noncomputable section

namespace Stage1Rev56.THMM0400.Validation

open Stage1Rev56.THMM0400

theorem independent_natAbs_le_integerHeight {n : Nat} (x : Fin n → Int)
    (j : Fin n) : (Int.natAbs (x j) : Real) ≤ integerHeight x := by
  unfold integerHeight
  exact_mod_cast Finset.le_sup (f := fun k => Int.natAbs (x k)) (Finset.mem_univ j)

theorem independent_one_le_integerHeight {n : Nat} {x : Fin n → Int}
    (hx : x ≠ 0) : 1 ≤ integerHeight x := by
  have hex : ∃ j, x j ≠ 0 := by
    by_contra h
    push Not at h
    exact hx (funext h)
  obtain ⟨j, hj⟩ := hex
  have hone : (1 : Real) ≤ Int.natAbs (x j) := by
    exact_mod_cast (Nat.one_le_iff_ne_zero.mpr (Int.natAbs_ne_zero.mpr hj))
  exact hone.trans (independent_natAbs_le_integerHeight x j)

theorem independent_rationalVector_ne_zero {n : Nat} {x : Fin n → Int}
    (hx : x ≠ 0) : rationalVector x ≠ 0 := by
  intro h
  apply hx
  funext j
  have hj : (x j : Rat) = 0 := congrFun h j
  exact_mod_cast hj

#print axioms independent_natAbs_le_integerHeight
#print axioms independent_one_le_integerHeight
#print axioms independent_rationalVector_ne_zero

end Stage1Rev56.THMM0400.Validation
