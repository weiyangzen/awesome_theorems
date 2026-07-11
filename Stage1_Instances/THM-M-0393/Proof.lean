import Mathlib.Data.Int.Basic
import Mathlib.Data.Int.Interval

/-!
# THM-M-0393 proof execution

This module implements a finite-common-factor lemma from the frozen proof
architecture. It does not assert the open Thue root.
-/

namespace Stage1.THM_M_0393.Proof

/-- For a nonzero right-hand side, only finitely many integers can have their
`n`th power divide it. This closes the finite-choice part of frozen obligation
`M0393-N1`; connecting these choices to gcd normalization remains open. -/
theorem finite_pow_divisors (n : Nat) (m : Int) (hn : 0 < n) (hm : m ≠ 0) :
    {g : Int | g ^ n ∣ m}.Finite := by
  apply (Set.finite_Icc (-m.natAbs : Int) m.natAbs).subset
  intro g hg
  have hpow_bound : (g ^ n).natAbs ≤ m.natAbs :=
    Int.natAbs_le_of_dvd_ne_zero hg hm
  have hg_bound : g.natAbs ≤ m.natAbs := by
    rw [Int.natAbs_pow] at hpow_bound
    exact le_trans (Nat.le_pow hn) hpow_bound
  have hg_lower : (-g.natAbs : Int) ≤ g := by
    rcases Int.natAbs_eq g with hg | hg <;> omega
  have hg_upper : g ≤ (g.natAbs : Int) := by
    rcases Int.natAbs_eq g with hg | hg <;> omega
  have hcast : (g.natAbs : Int) ≤ (m.natAbs : Int) := by exact_mod_cast hg_bound
  constructor
  · have : (-m.natAbs : Int) ≤ -g.natAbs := by omega
    exact this.trans hg_lower
  · exact hg_upper.trans hcast

#print axioms finite_pow_divisors

end Stage1.THM_M_0393.Proof
